"""Fresh actual-netlist audit against exact LP vertices, never a greedy bound."""
from collections import Counter
from fractions import Fraction
from functools import cmp_to_key
import hashlib
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from simulation.source_faithful_20261024.qft_bank import build_qft_bank
from simulation.source_faithful_20261024.qft_normal_form import normalized_qft_circuit
from simulation.source_faithful_20261024.resource_profile import primitive_skeletons, profile
from simulation.pruning_study_20261023.circuits import build_dual_bank, BuildBudget, CircuitBuildCap
from research_log.source_faithful_20261024.mps_readout import amplitude, norm_squared

TOL = 1e-8
SEED = 2026102529
CAPS = dict(qubits=128, gates=40000, columns=512, seconds=90)


def ordering(w, v):
    def compare(i, j):
        difference = v[i] * w[j] - v[j] * w[i]
        return -1 if difference > 0 else 1 if difference < 0 else i - j
    return tuple(sorted(range(len(w)), key=cmp_to_key(compare)))


def reference(w, v, W, d, prefix, bank):
    """One-capacity box vertices: all integral, or one strictly fractional item."""
    if d > len(w):
        return None, None, 0
    order = ordering(w, v)
    P = sum(v[i] for j, i in enumerate(order[:d]) if (prefix >> j) & 1)
    R = W - sum(w[i] for j, i in enumerate(order[:d]) if (prefix >> j) & 1)
    if R < 0:
        return None, None, 0
    suffix = order[d:]
    best, vertices = Fraction(0), 0
    for subset in range(1 << len(suffix)):
        weight = sum(w[i] for j, i in enumerate(suffix) if (subset >> j) & 1)
        if weight > R:
            continue
        value = sum(v[i] for j, i in enumerate(suffix) if (subset >> j) & 1)
        best = max(best, Fraction(value))
        vertices += 1
        for j, i in enumerate(suffix):
            if not (subset >> j) & 1 and 0 < R - weight < w[i]:
                best = max(best, Fraction(value) + Fraction((R - weight) * v[i], w[i]))
                vertices += 1
    duals = [Fraction(P) + lam * R + sum(max(Fraction(v[i]) - lam * w[i], 0) for i in suffix)
             for lam in bank]
    return Fraction(P) + best, min(duals), vertices


def fixture(label, w, v, W, d, bank=None, certified=True):
    bank = sorted({Fraction(0), *[Fraction(x, y) for x, y in zip(v, w)]}) if bank is None else [Fraction(*r) for r in bank]
    return dict(label=label, weights=w, values=v, capacity=W, depth=d,
                bank=[[r.numerator, r.denominator] for r in bank], certified=certified)


def expectation(f, d, prefix, tau):
    lp, upper, vertices = reference(f['weights'], f['values'], f['capacity'], d, prefix,
                                    [Fraction(*r) for r in f['bank']])
    flag = upper is None or upper < tau
    lpflag = lp is None or lp < tau
    return flag, lpflag, vertices


def simulator():
    return AerSimulator(method='matrix_product_state', matrix_product_state_truncation_threshold=0.0,
                        max_parallel_threads=1, max_parallel_experiments=1)


def basis_mps(compiled, f):
    circuit, sim = compiled.to_qiskit(), simulator()
    requested = 2 << compiled.num_inputs
    if circuit.num_qubits > CAPS['qubits'] or len(circuit.data) > CAPS['gates'] or requested > CAPS['columns']:
        return dict(status='CAPPED', reason='predeclared_size_cap', requested_columns=requested, caps=CAPS)
    result = dict(status='COMPLETED', classification='SIMULATED', columns=0, actual_gate_mismatches=0,
                  bank_vs_vertex_LP_predicate_disagreements=0, LP_vertices_evaluated=0,
                  maximum_amplitude_error=0.0, maximum_leakage=0.0, maximum_norm_error=0.0,
                  first_failures=[], tolerance_hardcoded=TOL, caps_hardcoded=CAPS)
    started = time.monotonic()
    cases = []
    for target in (0, 1):
        for encoded in range(1 << compiled.num_inputs):
            prefix, tau = encoded & ((1 << f['depth']) - 1), encoded >> f['depth']
            flag, lpflag, count = expectation(f, f['depth'], prefix, tau)
            result['bank_vs_vertex_LP_predicate_disagreements'] += flag != lpflag
            result['LP_vertices_evaluated'] += count
            initial = encoded | (target << compiled.output)
            expected = encoded | ((target ^ flag) << compiled.output)
            qc = QuantumCircuit(circuit.num_qubits)
            for j in range(compiled.num_inputs + 1):
                if (initial >> j) & 1:
                    qc.x(j)
            qc.compose(circuit, inplace=True)
            qc.save_matrix_product_state(label='mps')
            cases.append((qc, initial, expected))
    for offset in range(0, len(cases), 8):
        if time.monotonic() - started > CAPS['seconds']:
            result.update(status='CAPPED', reason='condition_time_cap')
            return result
        chunk = cases[offset:offset + 8]
        output = sim.run([x[0] for x in chunk], shots=1).result(timeout=90)
        if not output.success:
            result.update(status='SIMULATOR_FAILURE', reason=str(output.status))
            return result
        for j, (_, initial, expected) in enumerate(chunk):
            state = output.data(j)['mps']
            amp, norm = amplitude(state, expected), norm_squared(state)
            error, leak = abs(amp - 1), max(0.0, norm - abs(amp) ** 2)
            bad = error > TOL or leak > TOL or abs(norm - 1) > TOL
            result['actual_gate_mismatches'] += bad
            result['maximum_amplitude_error'] = max(result['maximum_amplitude_error'], error)
            result['maximum_leakage'] = max(result['maximum_leakage'], leak)
            result['maximum_norm_error'] = max(result['maximum_norm_error'], abs(norm - 1))
            result['columns'] += 1
            if bad and len(result['first_failures']) < 3:
                result['first_failures'].append(dict(initial=initial, expected=expected, actual_amplitude=[amp.real, amp.imag]))
        if 'simulator' not in result:
            metadata = output.results[0].metadata
            result['simulator'] = {key: metadata[key] for key in ['method', 'noise', 'matrix_product_state_truncation_threshold',
                'matrix_product_state_max_bond_dimension']}
            result['simulator']['zero_threshold'] = sim.options.zero_threshold
    result['host_seconds_measured'] = time.monotonic() - started
    return result


def superposition(compiled, f):
    rng = np.random.default_rng(SEED)
    nlogical = 1 << (compiled.num_inputs + 1)
    vector = rng.normal(size=nlogical) + 1j * rng.normal(size=nlogical)
    vector /= np.linalg.norm(vector)
    wanted = np.zeros(nlogical, dtype=complex)
    for initial, amp in enumerate(vector):
        encoded = initial & ((1 << compiled.num_inputs) - 1)
        prefix, tau = encoded & ((1 << f['depth']) - 1), encoded >> f['depth']
        flag, _, _ = expectation(f, f['depth'], prefix, tau)
        wanted[encoded | (((initial >> compiled.output) ^ flag) << compiled.output)] = amp
    qc = QuantumCircuit(compiled.num_qubits)
    qc.initialize(vector, range(compiled.num_inputs + 1))
    qc.compose(compiled.to_qiskit(), inplace=True)
    qc.save_matrix_product_state(label='mps')
    output = simulator().run(qc, shots=1).result(timeout=90)
    if not output.success:
        return dict(status='SIMULATOR_FAILURE', reason=str(output.status))
    state = output.data()['mps']
    actual = np.array([amplitude(state, j) for j in range(nlogical)])
    norm = norm_squared(state)
    error, leak = float(np.max(np.abs(actual - wanted))), max(0.0, norm - float(np.sum(np.abs(actual) ** 2)))
    return dict(status='COMPLETED', classification='SIMULATED', seed_hardcoded=SEED,
                logical_amplitudes=nlogical, maximum_amplitude_error=error, workspace_leakage=leak,
                normalization_error=abs(norm - 1), failures=int(error > TOL or leak > TOL or abs(norm - 1) > TOL))


def boolean_columns(f):
    bank = [Fraction(*r) for r in f['bank']]
    c = build_dual_bank(f['weights'], f['values'], f['capacity'], multipliers=bank,
                        budget=BuildBudget(30000, 200000, 30))
    # A separate interpreter of actual emitted gates, no production simulate_columns call.
    gates = [(1 << target, sum(1 << q for q in controls)) for target, controls in c.gates]
    result = dict(status='COMPLETED', classification='SIMULATED_exact_X_CX_CCX_gate_labels',
                  columns=0, actual_gate_mismatches=0, LP_predicate_disagreements=0,
                  invalid_depth_columns=0, LP_vertices_evaluated=0, first_failures=[],
                  qubits=c.num_qubits, gates=len(gates), depth_bits=c.depth_register_bits,
                  threshold_bits=c.threshold_bits, phase_argument='only_+1_permutation_gates_no_phase_primitive')
    n, db = len(f['weights']), c.depth_register_bits
    for target in (0, 1):
        for encoded in range(1 << c.num_inputs):
            prefix = encoded & ((1 << n) - 1)
            d = (encoded >> n) & ((1 << db) - 1)
            tau = encoded >> (n + db)
            flag, lpflag, count = expectation(f, d, prefix, tau)
            result['LP_predicate_disagreements'] += flag != lpflag
            result['LP_vertices_evaluated'] += count
            result['invalid_depth_columns'] += d > n
            expected = encoded | ((target ^ flag) << c.output)
            state = encoded | (target << c.output)
            for bit, controls in gates:
                if state & controls == controls:
                    state ^= bit
            result['actual_gate_mismatches'] += state != expected
            if state != expected and len(result['first_failures']) < 3:
                result['first_failures'].append(dict(encoded=encoded, target=target, expected=expected, actual=state))
            result['columns'] += 1
    return result


def main():
    folder = Path(__file__).parent
    dest = folder / 'circuit_vertex_adversarial.json'
    if dest.exists():
        raise RuntimeError('Preserve the old run; choose a new result path')
    fixtures = [fixture('near_integer_denominator17', [17, 3], [16, 2], 1, 1),
                fixture('ties_and_zero_profit', [2, 4, 1], [1, 2, 0], 3, 1),
                fixture('all_fit_multi_item', [2, 3], [3, 1], 10, 2, [[0, 1]]),
                fixture('zero_capacity_multi_rational', [3, 5], [2, 4], 0, 1),
                fixture('off_grid_integer_floor_only', [1, 1], [1, 1], 1, 1, [[1, 2]]),
                fixture('insufficient_bank_expected_not_LP', [2], [1], 1, 0, [[0, 1]], certified=False)]
    source_files = [ROOT / 'simulation/source_faithful_20261024' / name for name in
                    ['qft_bank.py', 'qft_reconstruction.py', 'qft_normal_form.py', 'resource_profile.py']]
    source_files += [ROOT / 'simulation/pruning_study_20261023/circuits.py',
                     ROOT / 'simulation/oracle_h/node_bound_reversible.py', Path(__file__)]
    out = dict(scope='fresh bounded adversarial actual-gate audit; independent exact LP vertices',
               source_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files},
               qft_rows=[], boolean_rows=[], superpositions=[], profile_rows=[], errors=[])
    def save():
        dest.write_text(json.dumps(out, indent=2), encoding='utf-8')
    save()
    skeletons = primitive_skeletons()
    for f in fixtures:
        for policy in ['direct', 'source_generic']:
            raw = build_qft_bank(f['weights'], f['values'], f['capacity'], f['depth'], f['bank'], mcx_policy=policy)
            for form, compiled in [('raw', raw), ('cancelled', normalized_qft_circuit(raw))]:
                row = dict(**f, policy=policy, form=form, result=basis_mps(compiled, f))
                out['qft_rows'].append(row); save()
                r = row['result']
                print(f['label'], policy, form, r['status'], r.get('columns'), r.get('actual_gate_mismatches'), flush=True)
                if r.get('actual_gate_mismatches') or (f['certified'] and r.get('bank_vs_vertex_LP_predicate_disagreements')):
                    raise RuntimeError('RESEARCH_INTEGRITY_STOP: unexpected QFT gate or LP mismatch')
                if f['label'] == 'ties_and_zero_profit' and policy == 'direct':
                    test = superposition(compiled, f)
                    out['superpositions'].append(dict(label=f['label'], form=form, result=test)); save()
                    if test.get('failures'):
                        raise RuntimeError('RESEARCH_INTEGRITY_STOP: complex-state phase/cleanup mismatch')
                if f['label'] == 'near_integer_denominator17':
                    derived = profile(compiled, skeletons)
                    qc = compiled.to_qiskit()
                    common = transpile(qc, basis_gates=['u', 'cx'], optimization_level=0)
                    mismatch = dict(qc.count_ops()) != derived['native_counts'] or qc.depth() != derived['native_depth'] or dict(common.count_ops()) != derived['common_counts'] or common.depth() != derived['common_depth']
                    out['profile_rows'].append(dict(label=f['label'], policy=policy, form=form,
                        mismatch=bool(mismatch), actual_full_transpile_counts=dict(common.count_ops()),
                        actual_full_transpile_depth=common.depth(), derived=derived)); save()
                    if mismatch:
                        raise RuntimeError('RESEARCH_INTEGRITY_STOP: resource profiler discrepancy')
    boolean_fixtures = [f for f in fixtures if all(x > 0 for x in f['values'])]
    boolean_fixtures += [fixture('empty_boolean_invalid_depth', [], [], 0, 0),
        fixture('large_coeff_near_integer', [65537, 65539], [3, 5], 65538, 0)]
    for f in boolean_fixtures:
        try:
            result = boolean_columns(f)
        except CircuitBuildCap as exc:
            result = dict(status='CAPPED', reason=exc.reason, counters=exc.counters)
        out['boolean_rows'].append(dict(**f, result=result)); save()
        print('BOOLEAN', f['label'], result['status'], result.get('columns'), result.get('actual_gate_mismatches'), flush=True)
        if result.get('actual_gate_mismatches') or (f['certified'] and result.get('LP_predicate_disagreements')):
            raise RuntimeError('RESEARCH_INTEGRITY_STOP: Boolean netlist or LP mismatch')
    # Explicit unsupported threshold/bank counterexamples, not circuit failures.
    out['limitations'] = dict(
        insufficient_bank=dict(weights=[2], values=[1], capacity=1, depth=0, bank=[[0, 1]],
            LP='1/2', bank_upper='1', integer_threshold=1, LP_reject=True, bank_reject=False),
        fractional_threshold=dict(weights=[1, 1], values=[1, 1], capacity=1, depth=0, bank=[[1, 2]],
            LP='1', bank_upper='3/2', threshold='5/4', LP_reject=True, bank_reject=False,
            reason='not an encoded integer threshold; floor-preservation never promised rational thresholds'),
        unsigned_range=dict(values=[1, 1], threshold_bits=2, representable=[0, 3],
            unsupported_threshold=4, if_caller_truncates_it_encodes=0,
            reason='no unbounded or signed threshold interface'))
    qr = [r['result'] for r in out['qft_rows']]
    br = [r['result'] for r in out['boolean_rows']]
    out['summary'] = dict(qft_method_cases=len(qr), qft_columns=sum(r.get('columns', 0) for r in qr),
        qft_gate_mismatches=sum(r.get('actual_gate_mismatches', 0) for r in qr),
        qft_statuses=dict(Counter(r['status'] for r in qr)),
        expected_insufficient_bank_LP_disagreements=sum(r['result'].get('bank_vs_vertex_LP_predicate_disagreements', 0) for r in out['qft_rows'] if not r['certified']),
        certified_bank_LP_disagreements=sum(r['result'].get('bank_vs_vertex_LP_predicate_disagreements', 0) for r in out['qft_rows'] if r['certified']),
        boolean_cases=len(br), boolean_columns=sum(r.get('columns', 0) for r in br),
        boolean_gate_mismatches=sum(r.get('actual_gate_mismatches', 0) for r in br),
        boolean_statuses=dict(Counter(r['status'] for r in br)),
        profiler_conditions=len(out['profile_rows']), profiler_mismatches=sum(r['mismatch'] for r in out['profile_rows']),
        superposition_conditions=len(out['superpositions']), superposition_failures=sum(r['result'].get('failures', 0) for r in out['superpositions']))
    save(); print(json.dumps(out['summary']), flush=True)


if __name__ == '__main__':
    main()
