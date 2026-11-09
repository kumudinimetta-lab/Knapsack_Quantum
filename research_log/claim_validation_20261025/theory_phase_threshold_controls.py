"""Bounded MPS threshold/preparation sensitivity controls, no oracle applied.

Fixed same seed and 1e-8 acceptance tolerance throughout. Threshold differences
diagnose a backend path; they are not a redefinition of circuit correctness.
"""
from pathlib import Path
import sys,json,hashlib,time
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
import numpy as np
import qiskit,qiskit_aer
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from research_log.source_faithful_20261024.mps_readout import amplitude,norm_squared
from research_log.claim_validation_20261025.theory_phase_preparation_triage import residuals


def main():
    dest=Path(__file__).with_suffix('.json')
    if dest.exists():raise RuntimeError('Preserve prior raw')
    rng=np.random.default_rng(2026102529)
    vector=rng.normal(size=32)+1j*rng.normal(size=32);vector/=np.linalg.norm(vector)
    out=dict(scope='no-oracle 22-wire input-preparation threshold sensitivity',
       seed_hardcoded=2026102529,tolerance_hardcoded=1e-8,
       qiskit=qiskit.__version__,qiskit_aer=qiskit_aer.__version__,
       source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       classifications=dict(amplitudes='SIMULATED',errors='DERIVED',host_seconds='MEASURED'),rows=[])
    for requested_threshold in ['default',0.0,1e-20,1e-16]:
        for prep in ['initialize','decomposed_initialize']:
            options=dict(method='matrix_product_state',max_parallel_threads=1,max_parallel_experiments=1)
            if requested_threshold!='default':options['matrix_product_state_truncation_threshold']=requested_threshold
            simulator=AerSimulator(**options)
            qc=QuantumCircuit(22);qc.initialize(vector,range(5))
            if prep.startswith('decomposed'):qc=qc.decompose(reps=10)
            qc.save_matrix_product_state(label='mps')
            started=time.monotonic();output=simulator.run(qc,shots=1).result(timeout=90)
            state=output.data()['mps']
            actual=np.array([amplitude(state,j) for j in range(32)])
            row=dict(preparation=prep,requested_threshold=requested_threshold,
                effective_threshold=simulator.options.matrix_product_state_truncation_threshold,
                zero_threshold=simulator.options.zero_threshold,
                norm_squared=norm_squared(state),residuals=residuals(actual,vector),
                host_seconds_measured=time.monotonic()-started,
                metadata=output.results[0].metadata)
            out['rows'].append(row);dest.write_text(json.dumps(out,indent=2,default=str),encoding='utf-8')
            print(prep,requested_threshold,row['norm_squared'],row['residuals'],flush=True)


if __name__=='__main__':main()
