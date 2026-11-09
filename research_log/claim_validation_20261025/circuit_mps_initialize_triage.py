"""Separate backend initialization, tensor export and gate-only preparation."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from simulation.source_faithful_20261024.qft_bank import build_qft_bank
from research_log.source_faithful_20261024.mps_readout import amplitude, norm_squared
from research_log.claim_validation_20261025.circuit_vertex_adversarial import fixture, expectation, SEED


def main():
    folder = Path(__file__).parent
    path = folder / 'circuit_mps_initialize_triage.json'
    if path.exists():
        raise RuntimeError('Preserve earlier evidence')
    f = fixture('ties_and_zero_profit', [2, 4, 1], [1, 2, 0], 3, 1)
    compiled = build_qft_bank(f['weights'], f['values'], f['capacity'], f['depth'], f['bank'])
    logical = compiled.num_inputs + 1
    rng = np.random.default_rng(SEED)
    vector = rng.normal(size=1 << logical) + 1j * rng.normal(size=1 << logical)
    vector /= np.linalg.norm(vector)
    gateprep = QuantumCircuit(logical)
    for j in range(logical):
        gateprep.h(j); gateprep.p((j + 1) * 0.271, j)
    gateprep.cx(0, logical - 1)
    gateprep.cp(0.413, 1, logical - 1)
    gateprep.h(2)
    gatevector = Statevector(gateprep).data
    out = dict(scope='same failed fixture only; no altered tolerance or overwritten failed run', rows=[])
    for preparation in ['initialize', 'native_gates']:
        source = vector if preparation == 'initialize' else gatevector
        for oracle in [False, True]:
            qc = QuantumCircuit(compiled.num_qubits)
            qc.initialize(vector, range(logical)) if preparation == 'initialize' else qc.compose(gateprep, qubits=range(logical), inplace=True)
            if oracle:
                qc.compose(compiled.to_qiskit(), inplace=True)
            wanted = np.zeros_like(source)
            for initial, amp in enumerate(source):
                encoded = initial & ((1 << compiled.num_inputs) - 1)
                flag, _, _ = expectation(f, f['depth'], encoded & 1, encoded >> f['depth'])
                final = encoded | (((initial >> compiled.output) ^ flag) << compiled.output) if oracle else initial
                wanted[final] = amp
            qc.save_matrix_product_state(label='mps')
            qc.save_probabilities_dict(label='probabilities')
            qc.save_statevector(label='statevector')
            sim = AerSimulator(method='matrix_product_state', matrix_product_state_truncation_threshold=0.0,
                               max_parallel_threads=1)
            result = sim.run(qc, shots=1).result(timeout=90)
            if not result.success:
                raise RuntimeError(str(result.status))
            data = result.data()
            mps = data['mps']
            exported = np.array([amplitude(mps, j) for j in range(1 << logical)])
            saved = np.asarray(data['statevector'])
            probs = {int(k, 16) if isinstance(k, str) else int(k): float(v) for k, v in data['probabilities'].items()}
            row = dict(preparation=preparation, oracle=oracle,
                tensor_norm_squared=norm_squared(mps), saved_statevector_norm=float(np.sum(np.abs(saved) ** 2)),
                saved_probabilities_sum=sum(probs.values()),
                tensor_amplitude_error=float(np.max(np.abs(exported - wanted))),
                backend_saved_statevector_amplitude_error=float(np.max(np.abs(saved[:1 << logical] - wanted))),
                backend_saved_probability_error=max(abs(probs.get(j, 0) - abs(a) ** 2) for j, a in enumerate(wanted)),
                gamma_shapes=[[list(np.asarray(x).shape) for x in gamma] for gamma in mps[0]],
                lambda_shapes=[list(np.asarray(x).shape) for x in mps[1]])
            out['rows'].append(row)
            path.write_text(json.dumps(out, indent=2), encoding='utf-8')
            print(preparation, oracle, row['tensor_norm_squared'], row['tensor_amplitude_error'],
                  row['backend_saved_statevector_amplitude_error'], row['backend_saved_probability_error'], flush=True)


if __name__ == '__main__':
    main()
