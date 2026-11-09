"""Independent preparation/readout controls for the retained complex-state failure.

Does not edit production code, the failed audit, its tolerance, or its raw output.
All amplitudes below are SIMULATED; residuals are DERIVED from those amplitudes.
"""
from pathlib import Path
import sys
import hashlib
import json
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import StatePreparation
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from simulation.source_faithful_20261024.qft_bank import build_qft_bank
from research_log.source_faithful_20261024.mps_readout import amplitude, norm_squared

SEED = 2026102529
TOL = 1e-8


def pairs(z):
    return [[float(x.real), float(x.imag)] for x in z]


def residuals(actual, desired):
    overlap = np.vdot(desired, actual)
    phase = overlap / abs(overlap) if overlap else 0
    return dict(raw_amplitude_error=float(np.max(abs(actual-desired))),
                complex_overlap=[float(overlap.real), float(overlap.imag)],
                overlap_magnitude=float(abs(overlap)),
                overlap_phase_radians=float(np.angle(overlap)),
                phase_aligned_amplitude_error=float(np.max(abs(actual-phase*desired))),
                vector_norm_squared=float(np.vdot(actual, actual).real))


def main():
    destination = Path(__file__).with_suffix('.json')
    if destination.exists():
        raise RuntimeError('Preserve existing raw diagnostics')
    compiled = build_qft_bank([2, 4, 1], [1, 2, 0], 3, 1, [[0, 1], [1, 2]], mcx_policy='direct')
    logical_qubits = compiled.num_inputs + 1
    rng = np.random.default_rng(SEED)
    desired = rng.normal(size=1 << logical_qubits)+1j*rng.normal(size=1 << logical_qubits)
    desired /= np.linalg.norm(desired)
    simulator = AerSimulator(method='matrix_product_state', matrix_product_state_truncation_threshold=0.0,
                             max_parallel_threads=1, max_parallel_experiments=1)
    result = dict(scope='initialize-only controls on failing fixture full wire layout; no oracle gates',
                  amplitude_classification='SIMULATED', residual_classification='DERIVED',
                  seed_hardcoded=SEED, tolerance_hardcoded=TOL,
                  num_inputs=compiled.num_inputs, output_wire=compiled.output,
                  logical_qubits=logical_qubits, full_qubits=compiled.num_qubits,
                  source_sha256={str(Path(__file__).relative_to(ROOT)):hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
                  input_amplitudes=pairs(desired), controls=[])
    for preparation in ['initialize', 'state_preparation', 'initialize_decomposed']:
        qc = QuantumCircuit(compiled.num_qubits)
        small = QuantumCircuit(logical_qubits)
        if preparation == 'state_preparation':
            qc.append(StatePreparation(desired), range(logical_qubits))
            small.append(StatePreparation(desired), range(logical_qubits))
        else:
            qc.initialize(desired, range(logical_qubits))
            small.initialize(desired, range(logical_qubits))
        if preparation == 'initialize_decomposed':
            qc = qc.decompose(reps=10)
            small = small.decompose(reps=10)
        exact_small = np.asarray(Statevector.from_instruction(small))
        qc.save_matrix_product_state(label='mps')
        qc.save_amplitudes(list(range(len(desired))), label='aer_amplitudes')
        started = time.monotonic()
        output = simulator.run(qc, shots=1).result(timeout=90)
        if not output.success:
            raise RuntimeError(str(output.status))
        state = output.data()['mps']
        contracted = np.array([amplitude(state, j) for j in range(len(desired))])
        native = np.asarray(output.data()['aer_amplitudes'])
        row = dict(preparation=preparation, host_seconds_measured=time.monotonic()-started,
                   circuit_global_phase=float(qc.global_phase),
                   small_statevector_vs_input=residuals(exact_small, desired),
                   custom_MPS_vs_input=residuals(contracted, desired),
                   native_Aer_vs_input=residuals(native, desired),
                   custom_MPS_vs_native_Aer=residuals(contracted, native),
                   custom_MPS_norm_squared=norm_squared(state),
                   contracted_amplitudes=pairs(contracted), native_amplitudes=pairs(native),
                   simulator_metadata=output.results[0].metadata)
        result['controls'].append(row)
        destination.write_text(json.dumps(result, indent=2, default=str), encoding='utf-8')
        print(preparation, row['custom_MPS_vs_input'], row['native_Aer_vs_input'], flush=True)


if __name__ == '__main__':
    main()
