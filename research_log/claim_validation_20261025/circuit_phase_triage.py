"""Diagnose the preserved complex-state failure, without changing its criterion."""
import hashlib
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from simulation.source_faithful_20261024.qft_bank import build_qft_bank
from simulation.source_faithful_20261024.qft_normal_form import normalized_qft_circuit
from research_log.source_faithful_20261024.mps_readout import amplitude, norm_squared
from research_log.claim_validation_20261025.circuit_vertex_adversarial import fixture, expectation, SEED


def compare(actual, wanted, norm):
    overlap = complex(np.vdot(wanted, actual))
    phase = overlap / abs(overlap) if overlap else 1
    return dict(raw_maximum_amplitude_error=float(np.max(np.abs(actual - wanted))),
        complex_overlap=[overlap.real, overlap.imag], overlap_magnitude=abs(overlap),
        overlap_phase_radians=float(np.angle(overlap)),
        phase_aligned_maximum_amplitude_error=float(np.max(np.abs(actual / phase - wanted))),
        normalization_error=abs(norm - 1), workspace_leak=max(0.0, norm - float(np.sum(np.abs(actual) ** 2))),
        actual_amplitudes=[[float(a.real), float(a.imag)] for a in actual])


def main():
    folder = Path(__file__).parent
    output = folder / 'circuit_phase_triage.json'
    if output.exists():
        raise RuntimeError('Preserve prior triage')
    f = fixture('ties_and_zero_profit', [2, 4, 1], [1, 2, 0], 3, 1)
    raw = build_qft_bank(f['weights'], f['values'], f['capacity'], f['depth'], f['bank'])
    rng = np.random.default_rng(SEED)
    nlogical = 1 << (raw.num_inputs + 1)
    vector = rng.normal(size=nlogical) + 1j * rng.normal(size=nlogical)
    vector /= np.linalg.norm(vector)
    wanted = np.zeros(nlogical, dtype=complex)
    for initial, amp in enumerate(vector):
        encoded = initial & ((1 << raw.num_inputs) - 1)
        flag, _, _ = expectation(f, f['depth'], encoded & 1, encoded >> f['depth'])
        wanted[encoded | (((initial >> raw.output) ^ flag) << raw.output)] = amp
    out = dict(scope='triage only, original failed criterion/data remain untouched', fixture=f,
        seed=SEED, qubits=raw.num_qubits, native_gates=len(raw.gates), original_tolerance=1e-8,
        expected_input=[[float(a.real), float(a.imag)] for a in vector],
        expected_oracle_output=[[float(a.real), float(a.imag)] for a in wanted], rows=[],
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    for label, qubits, oracle, reference in [('prep_logical_only', raw.num_inputs + 1, None, vector),
            ('prep_full_layout', raw.num_qubits, None, vector),
            ('raw_full_oracle', raw.num_qubits, raw, wanted),
            ('cancelled_full_oracle', raw.num_qubits, normalized_qft_circuit(raw), wanted)]:
        qc = QuantumCircuit(qubits)
        qc.initialize(vector, range(raw.num_inputs + 1))
        if oracle:
            qc.compose(oracle.to_qiskit(), inplace=True)
        row = dict(label=label, qubits=qubits, global_phase=float(qc.global_phase),
                   prep_decomposed_global_phase=float(qc.decompose(reps=8).global_phase))
        for method in ['matrix_product_state', 'statevector']:
            trial = qc.copy()
            if method == 'matrix_product_state':
                trial.save_matrix_product_state(label='saved')
                sim = AerSimulator(method=method, matrix_product_state_truncation_threshold=0.0, max_parallel_threads=1)
            else:
                trial.save_statevector(label='saved')
                sim = AerSimulator(method=method, max_parallel_threads=1)
            started = time.monotonic()
            result = sim.run(trial, shots=1).result(timeout=90)
            if not result.success:
                raise RuntimeError('Backend failure: ' + str(result.status))
            saved = result.data()['saved']
            if method == 'matrix_product_state':
                actual = np.array([amplitude(saved, j) for j in range(nlogical)])
                norm = norm_squared(saved)
            else:
                full = np.asarray(saved)
                actual, norm = full[:nlogical], float(np.sum(np.abs(full) ** 2))
            row[method] = dict(**compare(actual, reference, norm), seconds_measured=time.monotonic() - started)
            output.write_text(json.dumps(out, indent=2), encoding='utf-8')
        out['rows'].append(row)
        output.write_text(json.dumps(out, indent=2), encoding='utf-8')
        print(label, row['matrix_product_state']['raw_maximum_amplitude_error'],
              row['matrix_product_state']['phase_aligned_maximum_amplitude_error'],
              row['statevector']['raw_maximum_amplitude_error'], flush=True)
    output.write_text(json.dumps(out, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
