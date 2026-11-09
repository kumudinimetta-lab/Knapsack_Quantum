"""Independent coherent-input check of QFT bank OR/width/cleanup.

Plan before execution: a new fixture with zero profit, nontrivial reduced
denominators, an extra redundant multiplier, overlapping rejection flags,
and an overweight prefix. Simulate the entire raw/reduced gate lists on a
complex entangled state spanning all logical input and target encodings.
Expected action is computed from the direct Fraction dual, not A-minus-loss.
"""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import sys
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT));sys.dont_write_bytecode=True
from simulation.source_faithful_20261024.qft_bank import build_qft_bank
from simulation.source_faithful_20261024.qft_normal_form import normalized_qft_circuit
from research_log.source_faithful_20261024.mps_readout import amplitude,norm_squared
SEED=2026102516;rng=random.Random(SEED)
w,v,W,d=[5,2,3],[0,3,2],4,2
bank=[Fraction(0),Fraction(1,2),Fraction(2,3),Fraction(4,6)]
c=build_qft_bank(w,v,W,d,bank);order=[1,2,0]
prep=QuantumCircuit(c.num_inputs+1)
for j in range(c.num_inputs+1):
    prep.ry(rng.uniform(-2,2),j);prep.p(rng.uniform(-3,3),j)
for j in range(c.num_inputs):prep.cx(j,j+1)
initial=Statevector.from_instruction(prep).data;expected=np.zeros_like(initial)
overlapping=overweight=0
for encoded,a in enumerate(initial):
    inputs=encoded&((1<<c.num_inputs)-1);target=encoded>>c.num_inputs
    prefix=inputs&((1<<d)-1);tau=inputs>>d
    chosen=[order[j] for j in range(d) if prefix>>j&1]
    P=sum(v[i] for i in chosen);R=W-sum(w[i] for i in chosen)
    duals=[P+lam*R+sum(max(Fraction(v[i])-lam*w[i],0) for i in order[d:]) for lam in set(bank)]
    reject=R<0 or any(upper<tau for upper in duals)
    overlapping+=sum(x<tau for x in duals)>=2;overweight+=R<0
    expected[inputs|((target^reject)<<c.output)]+=a
simulator=AerSimulator(method='matrix_product_state',matrix_product_state_truncation_threshold=0.,
    max_parallel_threads=1,max_parallel_experiments=1)
rows=[]
for label,compiled in [('raw',c),('exact_inverse_cancellation',normalized_qft_circuit(c))]:
    qc=QuantumCircuit(compiled.num_qubits);qc.compose(prep,range(c.num_inputs+1),inplace=True)
    qc.compose(compiled.to_qiskit(),inplace=True);qc.save_matrix_product_state()
    result=simulator.run(qc).result();mps=result.data(0)['matrix_product_state']
    actual=np.array([amplitude(mps,i) for i in range(len(expected))]);norm=norm_squared(mps)
    rows.append(dict(method=label,qubits=compiled.num_qubits,gates=len(compiled.gates),
        logical_amplitudes=len(initial),maximum_expected_amplitude_error=float(np.max(np.abs(actual-expected))),
        workspace_probability_leak=float(abs(norm-np.vdot(actual,actual).real)),normalization_error=float(abs(norm-1))))
out=dict(seed=SEED,classification='SIMULATED complete ideal-gate MPS on complex coherent input',
    weights=w,values=v,capacity=W,depth=d,bank=[[x.numerator,x.denominator] for x in bank],
    overlapping_rejection_logical_encodings=overlapping,overweight_logical_encodings=overweight,
    rows=rows,failures=sum(r['maximum_expected_amplitude_error']>1e-8 or r['workspace_probability_leak']>1e-8 for r in rows),
    source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [
        ROOT/'simulation/source_faithful_20261024/qft_bank.py',
        ROOT/'simulation/source_faithful_20261024/qft_normal_form.py']})
dest=Path(__file__).with_name('reviewer_qft_bank_probe.json')
if dest.exists():raise RuntimeError('Refuse overwrite')
dest.write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out,indent=2))
if out['failures']:raise RuntimeError('RESEARCH_INTEGRITY_STOP: independent coherent bank probe failed')
