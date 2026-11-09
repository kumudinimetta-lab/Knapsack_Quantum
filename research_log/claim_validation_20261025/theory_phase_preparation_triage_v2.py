"""Separated save controls; the first combined-save attempt remains retained.

No oracle gates are applied in this control. Never change the failed audit/raw.
"""
from pathlib import Path
import sys
import json
import hashlib
import time
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import StatePreparation
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from simulation.source_faithful_20261024.qft_bank import build_qft_bank
from research_log.source_faithful_20261024.mps_readout import amplitude,norm_squared
from research_log.claim_validation_20261025.theory_phase_preparation_triage import residuals,pairs


def main():
    destination=Path(__file__).with_suffix('.json')
    if destination.exists():raise RuntimeError('preserve old raw')
    c=build_qft_bank([2,4,1],[1,2,0],3,1,[[0,1],[1,2]],mcx_policy='direct')
    nlogical=c.num_inputs+1
    rng=np.random.default_rng(2026102529)
    v=rng.normal(size=1<<nlogical)+1j*rng.normal(size=1<<nlogical)
    v/=np.linalg.norm(v)
    out=dict(scope='only input preparation; independently saved readouts',
             classifications=dict(amplitudes='SIMULATED',errors='DERIVED',host_seconds='MEASURED'),
             logical_qubits=nlogical,full_qubits=c.num_qubits,seed_hardcoded=2026102529,
             tolerance_hardcoded=1e-8,input_amplitudes=pairs(v),
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),controls=[])
    settings=[(nlogical,'initialize',True),(c.num_qubits,'initialize',True),
              (c.num_qubits,'initialize',False),
              (c.num_qubits,'decomposed_initialize',True),
              (c.num_qubits,'decomposed_preparation',True)]
    for nq,prep,truncation in settings:
        for readout in ['matrix_product_state','amplitudes','statevector']:
            qc=QuantumCircuit(nq)
            if prep=='decomposed_preparation':qc.append(StatePreparation(v),range(nlogical))
            else:qc.initialize(v,range(nlogical))
            if prep.startswith('decomposed'):qc=qc.decompose(reps=10)
            original_phase=float(qc.global_phase)
            if readout=='amplitudes':qc.save_amplitudes(list(range(len(v))),label='out')
            else:getattr(qc,'save_'+readout)(label='out')
            sim=AerSimulator(method='matrix_product_state',matrix_product_state_truncation_threshold=0.0,
                max_parallel_threads=1,max_parallel_experiments=1,enable_truncation=truncation)
            started=time.monotonic()
            output=sim.run(qc,shots=1).result(timeout=90)
            data=output.data()['out']
            row=dict(qubits=nq,preparation=prep,enable_truncation=truncation,readout=readout,
                circuit_global_phase=original_phase,host_seconds_measured=time.monotonic()-started,
                simulator_metadata=output.results[0].metadata)
            if readout=='matrix_product_state':
                actual=np.array([amplitude(data,j) for j in range(len(v))]);norm=norm_squared(data)
                row.update(gamma_count=len(data[0]),lambda_count=len(data[1]),
                    gamma_shapes=[[list(g.shape) for g in pair] for pair in data[0]])
            else:
                full=np.asarray(data);actual=full[:len(v)]
                norm=float(np.vdot(full,full).real)
            row.update(residuals=residuals(actual,v),full_norm_squared=norm,actual_amplitudes=pairs(actual))
            out['controls'].append(row)
            destination.write_text(json.dumps(out,indent=2,default=str),encoding='utf-8')
            print(nq,prep,truncation,readout,row['residuals'], 'fullnorm',norm,flush=True)
    # Dense exact reference has the same 22-wire preparation, no oracle gates.
    qc=QuantumCircuit(c.num_qubits);qc.initialize(v,range(nlogical))
    dense=np.asarray(Statevector.from_instruction(qc))
    out['dense_full_reference']=dict(residuals=residuals(dense[:len(v)],v),
        full_norm_squared=float(np.vdot(dense,dense).real),tail_norm_squared=float(np.vdot(dense[len(v):],dense[len(v):]).real))
    destination.write_text(json.dumps(out,indent=2,default=str),encoding='utf-8')
    print('dense',out['dense_full_reference'],flush=True)


if __name__=='__main__':main()
