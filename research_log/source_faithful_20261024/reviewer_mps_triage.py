"""Independent phase-sensitive MPS readout and coherent predicate control.

Prior to running: (a) use dense Statevector on small arithmetic networks to
audit tensor indexing and phase, not just probabilities; (b) on the original
23q failed fixture compare direct tensor amplitudes with the exact logical
permutation, including an entangled complex input state and clean workspace;
(c) retain the Aer saved-amplitude conflict rather than edit the failed pilot.
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
from simulation.source_faithful_20261024.qft_reconstruction import QFTNetwork,build_qft_exact
from research_log.source_faithful_20261024.mps_readout import amplitude,norm_squared

SEED=2026102412;rng=random.Random(SEED)
simulator=AerSimulator(method='matrix_product_state',matrix_product_state_truncation_threshold=0.,
                       max_parallel_threads=1,max_parallel_experiments=1)

def independent_expand(mps):
    gammas,lambdas=mps
    # Explicitly branch the left boundary for each successive physical bit.
    amplitudes={0:np.array([1+0j])}
    for j,gamma in enumerate(gammas):
        next_values={}
        for label,row in amplitudes.items():
            for bit in (0,1):
                value=np.einsum('a,ab->b',row,gamma[bit])
                if j<len(lambdas):value=value*lambdas[j]
                next_values[label|(bit<<j)]=value
        amplitudes=next_values
    return np.array([amplitudes[i].item() for i in range(1<<len(gammas))])

def logical_preparation(width):
    prep=QuantumCircuit(width)
    for j in range(width):
        prep.ry(rng.uniform(-2,2),j);prep.p(rng.uniform(-3,3),j)
    for j in range(width-1):prep.cx(j,j+1)
    return prep

rows=[]
for mode in ['variable_add_2','signed_compare_3','constant_compare_3','controlled_add_3']:
    if mode=='variable_add_2':
        net=QFTNetwork(4);net.variable_add([0,1],[2,3])
    elif mode=='signed_compare_3':
        net=QFTNetwork(6,3);net.less([0,1,2],[3,4,5],net.output)
    elif mode=='constant_compare_3':
        net=QFTNetwork(3,3,mcx_policy='source_generic');net.const_less(2,[0,1,2],net.output)
    else:
        net=QFTNetwork(4);net.controlled_constant([0,1,2],5,3)
    c=net.circuit(0,0).to_qiskit();q=QuantumCircuit(c.num_qubits)
    q.compose(logical_preparation(len(net.inputs)+1),range(len(net.inputs)+1),inplace=True)
    q.compose(c,inplace=True)
    exact=Statevector.from_instruction(q).data
    q.save_matrix_product_state();result=simulator.run(q).result();mps=result.data(0)['matrix_product_state']
    expanded=independent_expand(mps)
    helper=np.array([amplitude(mps,i) for i in range(len(exact))])
    rows.append(dict(mode=mode,qubits=c.num_qubits,all_amplitudes=len(exact),
        independent_vs_dense_max_error=float(np.max(np.abs(expanded-exact))),
        helper_vs_dense_max_error=float(np.max(np.abs(helper-exact))),
        helper_norm_error=float(abs(norm_squared(mps)-np.vdot(exact,exact).real))))

c=build_qft_exact([1],[1],0,1);predicate=c.to_qiskit()
q=QuantumCircuit(c.num_qubits);q.x(0);q.compose(predicate,inplace=True)
q.save_amplitudes([1,9],label='saved_amplitudes');q.save_probabilities([0,1,2,3],label='logical_probabilities')
q.save_matrix_product_state();r=simulator.run(q).result();data=r.data(0);mps=data['matrix_product_state']
conflict=dict(initial=1,expected=9,qubits=c.num_qubits,
    saved_amplitudes=[[float(a.real),float(a.imag)] for a in data['saved_amplitudes']],
    logical_probability_at_9=float(data['logical_probabilities'][9]),
    tensor_amplitude_at_9=[amplitude(mps,9).real,amplitude(mps,9).imag],
    tensor_norm_squared=norm_squared(mps))

prep=logical_preparation(c.num_inputs+1);initial=Statevector.from_instruction(prep).data
expected=np.zeros_like(initial)
for x,a in enumerate(initial):
    encoded=x&7;target=x>>3;prefix=encoded&1;tau=encoded>>1
    reject=bool(prefix or tau>0) # W=0: selected sole item infeasible; else LP bound0.
    expected[encoded|((target^reject)<<3)]+=a
q=QuantumCircuit(c.num_qubits);q.compose(prep,range(c.num_inputs+1),inplace=True)
q.compose(predicate,inplace=True);q.save_matrix_product_state()
mps=simulator.run(q).result().data(0)['matrix_product_state']
actual=np.array([amplitude(mps,i) for i in range(len(expected))])
coherent=dict(qubits=c.num_qubits,nonzero_logical_input_amplitudes=len(initial),
    maximum_logical_amplitude_error=float(np.max(np.abs(actual-expected))),
    workspace_probability_leak=float(abs(norm_squared(mps)-np.vdot(actual,actual).real)),
    norm_error=float(abs(norm_squared(mps)-1)))

out={'classification':'SIMULATED phase-sensitive noiseless ideal-gate checks',
     'seed':SEED,'tolerance_hardcoded':1e-8,'dense_readout_controls':rows,
     'saved_amplitude_conflict':conflict,'coherent_first_fixture':coherent,
     'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [
         ROOT/'simulation/source_faithful_20261024/qft_reconstruction.py',
         ROOT/'research_log/source_faithful_20261024/mps_readout.py']}}
path=Path(__file__).with_name('reviewer_mps_triage.json')
if path.exists():raise RuntimeError('Refuse overwrite of independent raw results')
path.write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out,indent=2))
if any(row['helper_vs_dense_max_error']>1e-8 or row['independent_vs_dense_max_error']>1e-8 for row in rows) or coherent['maximum_logical_amplitude_error']>1e-8 or coherent['workspace_probability_leak']>1e-8:
    raise RuntimeError('RESEARCH_INTEGRITY_STOP: MPS control failed; raw retained')
