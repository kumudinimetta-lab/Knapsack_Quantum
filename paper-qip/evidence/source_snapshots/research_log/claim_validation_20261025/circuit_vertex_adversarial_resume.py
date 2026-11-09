"""Resume ONLY the predeclared audit after isolating Aer partial-initialize fault.

No production code or tolerance changes. Failed raw files remain untouched.
Use explicit native unitary preparation for the two coherent controls.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from simulation.source_faithful_20261024.qft_bank import build_qft_bank
from simulation.source_faithful_20261024.qft_normal_form import normalized_qft_circuit
from research_log.source_faithful_20261024.mps_readout import amplitude, norm_squared
from research_log.claim_validation_20261025.circuit_vertex_adversarial import (
    fixture, expectation, basis_mps, boolean_columns, simulator, TOL, CircuitBuildCap)


def native_coherent_check(compiled, f):
    logical = compiled.num_inputs + 1
    prep = QuantumCircuit(logical)
    for j in range(logical):
        prep.h(j); prep.p((j + 1) * 0.271, j)
    prep.cx(0, logical - 1)
    prep.cp(0.413, 1, logical - 1)
    prep.h(2)
    source = Statevector(prep).data
    wanted = np.zeros_like(source)
    for initial, value in enumerate(source):
        encoded = initial & ((1 << compiled.num_inputs) - 1)
        flag, _, _ = expectation(f, f['depth'], encoded & ((1 << f['depth']) - 1), encoded >> f['depth'])
        wanted[encoded | (((initial >> compiled.output) ^ flag) << compiled.output)] = value
    qc = QuantumCircuit(compiled.num_qubits)
    qc.compose(prep, qubits=range(logical), inplace=True)
    qc.compose(compiled.to_qiskit(), inplace=True)
    qc.save_matrix_product_state(label='mps')
    result = simulator().run(qc, shots=1).result(timeout=90)
    if not result.success:
        return dict(status='SIMULATOR_FAILURE', reason=str(result.status))
    state = result.data()['mps']
    actual = np.array([amplitude(state, j) for j in range(1 << logical)])
    norm = norm_squared(state)
    error, leak = float(np.max(np.abs(actual - wanted))), max(0.0, norm - float(np.sum(np.abs(actual) ** 2)))
    return dict(status='COMPLETED', classification='SIMULATED', preparation='native_H_P_CX_CP_no_initialize',
        logical_amplitudes=1 << logical, maximum_amplitude_error=error, workspace_leakage=leak,
        normalization_error=abs(norm - 1), tolerance_hardcoded=TOL,
        failures=int(error > TOL or leak > TOL or abs(norm - 1) > TOL))


def main():
    folder = Path(__file__).parent
    previous_path = folder / 'circuit_vertex_adversarial.json'
    previous = json.loads(previous_path.read_text())
    dest = folder / 'circuit_vertex_adversarial_resume.json'
    if dest.exists():
        raise RuntimeError('Preserve earlier completed resume')
    inherited = previous['qft_rows']
    if len(inherited) != 5 or any(r['result'].get('actual_gate_mismatches') for r in inherited):
        raise RuntimeError('Unexpected initial audit state; do not silently skip tests')
    done = {(r['label'], r['policy'], r['form']) for r in inherited}
    fixtures = [fixture('near_integer_denominator17', [17, 3], [16, 2], 1, 1),
                fixture('ties_and_zero_profit', [2, 4, 1], [1, 2, 0], 3, 1),
                fixture('all_fit_multi_item', [2, 3], [3, 1], 10, 2, [[0, 1]]),
                fixture('zero_capacity_multi_rational', [3, 5], [2, 4], 0, 1),
                fixture('off_grid_integer_floor_only', [1, 1], [1, 1], 1, 1, [[1, 2]]),
                fixture('insufficient_bank_expected_not_LP', [2], [1], 1, 0, [[0, 1]], certified=False)]
    out = dict(scope='remaining predeclared fixtures only; no production/tolerance modification',
        previous_raw_sha256=hashlib.sha256(previous_path.read_bytes()).hexdigest(),
        preserved_initial_harness_sha256=hashlib.sha256((folder / 'circuit_vertex_adversarial.py').read_bytes()).hexdigest(),
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        resolution='AerMPS_partial_initialize_backend_failure_reproduced_before_oracle; dense_full_oracle_and_native_prep_controls_pass',
        inherited_passing_method_cases=len(inherited), inherited_basis_columns=sum(r['result']['columns'] for r in inherited),
        qft_rows=[], boolean_rows=[], native_superpositions=[], input_domain_checks=[])
    def save():
        dest.write_text(json.dumps(out, indent=2), encoding='utf-8')
    save()
    for f in fixtures:
        for policy in ['direct', 'source_generic']:
            raw = build_qft_bank(f['weights'], f['values'], f['capacity'], f['depth'], f['bank'], mcx_policy=policy)
            for form, c in [('raw', raw), ('cancelled', normalized_qft_circuit(raw))]:
                if (f['label'], policy, form) not in done:
                    row = dict(**f, policy=policy, form=form, result=basis_mps(c, f))
                    out['qft_rows'].append(row); save()
                    r = row['result']
                    print(f['label'], policy, form, r['status'], r.get('columns'), r.get('actual_gate_mismatches'), flush=True)
                    if r.get('actual_gate_mismatches') or (f['certified'] and r.get('bank_vs_vertex_LP_predicate_disagreements')):
                        raise RuntimeError('RESEARCH_INTEGRITY_STOP: QFT/LP predicate mismatch')
                if f['label'] == 'ties_and_zero_profit' and policy == 'direct':
                    r = native_coherent_check(c, f)
                    out['native_superpositions'].append(dict(label=f['label'], form=form, result=r)); save()
                    if r.get('failures'):
                        raise RuntimeError('RESEARCH_INTEGRITY_STOP: native coherent gate mismatch')
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
            raise RuntimeError('RESEARCH_INTEGRITY_STOP: Boolean/LP predicate mismatch')
    from simulation.pruning_study_20261023.circuits import build_dual_bank
    calls = [('Boolean_zero_profit_explicitly_unsupported', lambda: build_dual_bank([1], [0], 0)),
             ('QFT_negative_bank_rejected', lambda: build_qft_bank([1], [1], 0, 0, [[-1, 1]])),
             ('QFT_empty_bank_rejected', lambda: build_qft_bank([1], [1], 0, 0, [])),
             ('QFT_invalid_depth_rejected', lambda: build_qft_bank([1], [1], 0, 2, [[0, 1]]))]
    for label, call in calls:
        try:
            call(); result = dict(label=label, expected_rejection=False)
        except ValueError as exc:
            result = dict(label=label, expected_rejection=True, exception=str(exc))
        out['input_domain_checks'].append(result)
    all_qft = inherited + out['qft_rows']
    qr, br = [r['result'] for r in all_qft], [r['result'] for r in out['boolean_rows']]
    out['limitations'] = dict(
        insufficient_bank=dict(weights=[2], values=[1], capacity=1, depth=0, bank=[[0, 1]],
            LP='1/2', bank_upper='1', integer_threshold=1, LP_reject=True, bank_reject=False),
        fractional_threshold=dict(weights=[1, 1], values=[1, 1], capacity=1, depth=0, bank=[[1, 2]],
            LP='1', bank_upper='3/2', threshold='5/4', LP_reject=True, bank_reject=False,
            supported=False, reason='integer-floor preservation does not preserve rational thresholds'),
        unsigned_range=dict(values=[1, 1], threshold_bits=2, representable=[0, 3],
            unsupported_threshold=4, if_caller_truncates_it_encodes=0))
    out['summary'] = dict(qft_method_cases_including_inherited=len(qr), qft_basis_columns=sum(r.get('columns', 0) for r in qr),
        qft_gate_mismatches=sum(r.get('actual_gate_mismatches', 0) for r in qr),
        qft_statuses=dict(Counter(r['status'] for r in qr)),
        expected_insufficient_bank_LP_disagreements=sum(r['result'].get('bank_vs_vertex_LP_predicate_disagreements', 0) for r in all_qft if not r['certified']),
        certified_QFT_LP_disagreements=sum(r['result'].get('bank_vs_vertex_LP_predicate_disagreements', 0) for r in all_qft if r['certified']),
        boolean_cases=len(br), boolean_columns=sum(r.get('columns', 0) for r in br),
        boolean_gate_mismatches=sum(r.get('actual_gate_mismatches', 0) for r in br),
        boolean_invalid_depth_columns=sum(r.get('invalid_depth_columns', 0) for r in br),
        boolean_statuses=dict(Counter(r['status'] for r in br)),
        profiler_conditions=len(previous['profile_rows']), profiler_mismatches=sum(r['mismatch'] for r in previous['profile_rows']),
        native_superposition_conditions=len(out['native_superpositions']),
        native_superposition_amplitudes=sum(r['result'].get('logical_amplitudes', 0) for r in out['native_superpositions']),
        native_superposition_failures=sum(r['result'].get('failures', 0) for r in out['native_superpositions']),
        input_domain_checks=len(calls), input_domain_rejection_failures=sum(not r['expected_rejection'] for r in out['input_domain_checks']))
    save(); print(json.dumps(out['summary']), flush=True)


if __name__ == '__main__':
    main()
