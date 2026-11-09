"""Independent exact-cancellation control: derivation and plan before run.

A removed pair has opposite phases or identical self-inverse action and every
intervening gate is disjoint from its wires. Thus it can commute to its inverse
and cancel exactly. Floating angle equality is literal; no near-zero gate is
dropped. Check complete dense states on interleaved controlled arithmetic with
complex superpositions, plus randomized general supported-gate circuits. Keep
raw and reduced counts; do not infer upstream implementation performance.
"""
import hashlib
import json
from pathlib import Path
import random
import sys
import numpy as np
from qiskit.quantum_info import Statevector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT));sys.dont_write_bytecode=True
from simulation.source_faithful_20261024.qft_reconstruction import QFTNetwork
from simulation.source_faithful_20261024.qft_normal_form import normalized_qft_circuit
SEED=2026102515;rng=random.Random(SEED);nrng=np.random.default_rng(SEED)
networks=[]
for _ in range(3):
    net=QFTNetwork(8,3)
    for control,k,word in [(6,3,[0,1,2]),(7,5,[3,4,5]),(6,2,[0,1,2]),(7,7,[3,4,5])]:
        net.controlled_constant(word,k,control,subtract=(k==2))
    net.variable_add([0,1,2],[3,4,5])
    net.less([0,1,2],[3,4,5],net.output)
    networks.append(net.circuit(0,0))
for _ in range(12):
    net=QFTNetwork(5,5)
    for j in range(60):
        if j%5==0:
            wires=rng.sample(range(6),2);a=rng.choice([.25,.5,1.,2.])*np.pi
            net.append('cp',wires,a)
            other=next(q for q in range(6) if q not in wires)
            net.append('h',[other]);net.append('cp',wires,-a);net.append('h',[other])
        else:
            gate=rng.choice(['h','x','cx','ccx','p','cp'])
            arity={'h':1,'x':1,'p':1,'cx':2,'cp':2,'ccx':3}[gate]
            wires=rng.sample(range(6),arity)
            net.append(gate,wires,rng.choice([.25,.5,1.,2.])*np.pi if gate in ['p','cp'] else None)
    networks.append(net.circuit(0,0))
rows=[]
for index,c in enumerate(networks):
    state=np.zeros(1<<c.num_qubits,dtype=complex)
    logical=1<<(c.num_inputs+1)
    amplitudes=nrng.normal(size=logical)+1j*nrng.normal(size=logical);amplitudes/=np.linalg.norm(amplitudes)
    state[:logical]=amplitudes
    raw=Statevector(state).evolve(c.to_qiskit()).data
    for commute in [False,True]:
        reduced=normalized_qft_circuit(c,commute_disjoint=commute)
        actual=Statevector(state).evolve(reduced.to_qiskit()).data
        rows.append(dict(network=index,qubits=c.num_qubits,commute_disjoint=commute,
            logical_amplitudes=logical,full_amplitudes=len(raw),raw_gates=len(c.gates),
            reduced_gates=len(reduced.gates),maximum_amplitude_difference=float(np.max(np.abs(actual-raw))),
            audit=reduced.metadata['inverse_cancellation']))
out=dict(seed=SEED,classification='SIMULATED dense full-state equivalence',
    conditions=len(rows),failures=sum(r['maximum_amplitude_difference']>1e-10 for r in rows),
    maximum_amplitude_difference=max(r['maximum_amplitude_difference'] for r in rows),rows=rows,
    source_sha256=hashlib.sha256((ROOT/'simulation/source_faithful_20261024/qft_normal_form.py').read_bytes()).hexdigest())
dest=Path(__file__).with_name('reviewer_qft_normal_form.json')
if dest.exists():raise RuntimeError('Refuse overwrite')
dest.write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
if out['failures']:raise RuntimeError('RESEARCH_INTEGRITY_STOP: exact cancellation dense control failed')
