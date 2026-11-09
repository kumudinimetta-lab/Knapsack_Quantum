"""Tiny full-gate phase/cleanup checks for the supplied QFT bank predicate."""
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from simulation.source_faithful_20261024.qft_bank import build_qft_bank, bank_geometry
from simulation.source_faithful_20261024.compressed_bank import build_dp_free_bank
from simulation.source_faithful_20261024.resource_profile import primitive_skeletons, profile
from research_log.source_faithful_20261024.mps_readout import amplitude, norm_squared

TOLERANCE = 1e-8
CAPS = dict(qubits=128, native_gates=40000, columns=512, condition_seconds=90)


def references(w, v, W, d, prefix, bank):
    order = sorted(range(len(w)), key=lambda i: Fraction(v[i], w[i]), reverse=True)
    P = sum(v[i] for j, i in enumerate(order[:d]) if (prefix >> j) & 1)
    R = W - sum(w[i] for j, i in enumerate(order[:d]) if (prefix >> j) & 1)
    if R < 0:
        return None, None
    lp, residual = Fraction(P), R
    for i in order[d:]:
        if w[i] > residual:
            lp += Fraction(residual * v[i], w[i])
            break
        lp += v[i]
        residual -= w[i]
    duals = [Fraction(P) + Fraction(*r) * R +
             sum(max(Fraction(v[i]) - Fraction(*r) * w[i], 0) for i in order[d:])
             for r in bank]
    return lp, duals


def check(compiled, w, v, W, d, bank):
    qc = compiled.to_qiskit()
    columns = 2 << compiled.num_inputs
    if qc.num_qubits > CAPS['qubits'] or len(qc.data) > CAPS['native_gates'] or columns > CAPS['columns']:
        return dict(status='CAPPED', reason='size_budget', requested_columns=columns, caps_hardcoded=CAPS)
    sim = AerSimulator(method='matrix_product_state', matrix_product_state_truncation_threshold=0.0,
                       max_parallel_threads=1, max_parallel_experiments=1)
    start = time.monotonic()
    row = dict(status='COMPLETED', classification='SIMULATED', columns=0,
               predicate_phase_or_cleanup_failures=0, exact_rational_LP_predicate_disagreements=0,
               exact_rational_bank_predicate_disagreements=0, overlapping_reject_flag_columns=0,
               max_expected_amplitude_error=0.0, max_probability_leak=0.0,
               max_normalization_error=0.0, caps_hardcoded=CAPS,
               tolerance_hardcoded=TOLERANCE, first_failures=[])
    cases = []
    for target in (0, 1):
        for encoded in range(1 << compiled.num_inputs):
            prefix, tau = encoded & ((1 << d) - 1), encoded >> d
            lp, duals = references(w, v, W, d, prefix, bank)
            flag = lp is None or min(duals) < tau
            lpflag = lp is None or lp < tau
            row['exact_rational_LP_predicate_disagreements'] += flag != lpflag
            row['overlapping_reject_flag_columns'] += lp is not None and sum(x < tau for x in duals) >= 2
            initial = encoded | (target << compiled.output)
            expected = encoded | ((target ^ flag) << compiled.output)
            prepared = QuantumCircuit(qc.num_qubits)
            for j in range(compiled.num_inputs + 1):
                if (initial >> j) & 1:
                    prepared.x(j)
            prepared.compose(qc, inplace=True)
            prepared.save_matrix_product_state(label='mps')
            cases.append((prepared, expected, initial))
    if row['exact_rational_LP_predicate_disagreements']:
        row['status'] = 'REFERENCE_FAILURE'
        return row
    for offset in range(0, len(cases), 8):
        if time.monotonic() - start > CAPS['condition_seconds']:
            row.update(status='CAPPED', reason='condition_time_budget')
            return row
        batch = cases[offset:offset + 8]
        result = sim.run([x[0] for x in batch], shots=1).result(timeout=90)
        if not result.success:
            row.update(status='SIMULATOR_FAILURE', message=str(result.status))
            return row
        for j, (_, expected, initial) in enumerate(batch):
            state = result.data(j)['mps']
            amp, norm = amplitude(state, expected), norm_squared(state)
            error, leak = abs(amp - 1), max(0.0, norm - abs(amp) ** 2)
            row['max_expected_amplitude_error'] = max(row['max_expected_amplitude_error'], error)
            row['max_probability_leak'] = max(row['max_probability_leak'], leak)
            row['max_normalization_error'] = max(row['max_normalization_error'], abs(norm - 1))
            failed = error > TOLERANCE or leak > TOLERANCE or abs(norm - 1) > TOLERANCE
            row['predicate_phase_or_cleanup_failures'] += failed
            if failed and len(row['first_failures']) < 3:
                row['first_failures'].append(dict(initial=initial, expected=expected, amplitude=[amp.real, amp.imag]))
            row['columns'] += 1
        if 'simulator' not in row:
            meta = result.results[0].metadata
            row['simulator'] = {k: meta[k] for k in ('method', 'noise', 'matrix_product_state_truncation_threshold',
                                                    'matrix_product_state_max_bond_dimension')}
            row['simulator']['zero_threshold_config'] = sim.options.zero_threshold
    row['seconds_measured'] = time.monotonic() - start
    return row


def main():
    folder = Path(__file__).parent
    output = folder / 'qft_bank_pilot_results.json'
    if output.exists():
        raise RuntimeError('Preserve existing pilot results; choose a distinct new output for a rerun')
    fixtures = [([], [], 0, 0), ([1], [1], 0, 1), ([1], [1], 1, 1),
                ([1, 2], [1, 1], 1, 0), ([1, 2], [1, 1], 1, 1),
                ([2, 4], [1, 2], 3, 1), ([2, 3, 1], [2, 1, 1], 3, 1),
                ([1, 2], [0, 0], 0, 1), ([1, 2], [0, 1], 1, 1)]
    sources = [ROOT / 'simulation/source_faithful_20261024/qft_bank.py',
               ROOT / 'simulation/source_faithful_20261024/qft_reconstruction.py',
               ROOT / 'simulation/source_faithful_20261024/compressed_bank.py',
               folder / 'mps_readout.py', Path(__file__)]
    out = dict(scope='tiny full-gate supplied QFT bank; all quantum threshold encodings and both output bits',
               source_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
               rows=[], errors=[])
    skeletons = primitive_skeletons()
    for index, (w, v, W, d) in enumerate(fixtures):
        bank = build_dp_free_bank(w, v, W)['bank']
        for policy in ('direct', 'source_generic'):
            row = dict(fixture=index, weights=w, values=v, capacity=W, depth=d, bank=bank, policy=policy)
            try:
                compiled = build_qft_bank(w, v, W, d, bank, mcx_policy=policy)
                row.update(resources=profile(compiled, skeletons), metadata=compiled.metadata,
                           check=check(compiled, w, v, W, d, bank))
                out['rows'].append(row)
                output.write_text(json.dumps(out, indent=2), encoding='utf-8')
                print(index, policy, row['check']['status'], row['check'].get('columns'),
                      row['check'].get('predicate_phase_or_cleanup_failures'), flush=True)
                if row['check'].get('predicate_phase_or_cleanup_failures') or row['check'].get('exact_rational_LP_predicate_disagreements'):
                    raise RuntimeError('RESEARCH_INTEGRITY_STOP: compiled bank or coverage mismatch')
            except Exception as exc:
                out['errors'].append(dict(fixture=index, policy=policy, error=type(exc).__name__ + ': ' + str(exc)))
                output.write_text(json.dumps(out, indent=2), encoding='utf-8')
                raise
    checks = [r['check'] for r in out['rows']]
    out['summary'] = dict(method_cases=len(checks), columns=sum(c.get('columns', 0) for c in checks),
        statuses={status: sum(c['status'] == status for c in checks) for status in set(c['status'] for c in checks)},
        predicate_phase_or_cleanup_failures=sum(c.get('predicate_phase_or_cleanup_failures', 0) for c in checks),
        exact_rational_LP_predicate_disagreements=sum(c.get('exact_rational_LP_predicate_disagreements', 0) for c in checks),
        overlapping_reject_flag_columns=sum(c.get('overlapping_reject_flag_columns', 0) for c in checks),
        max_expected_amplitude_error=max(c.get('max_expected_amplitude_error', 0) for c in checks))
    output.write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(json.dumps(out['summary']), flush=True)


if __name__ == '__main__':
    main()
