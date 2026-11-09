"""Separate nonempty dense-state compact-dual check with independent coefficients."""
from fractions import Fraction
import argparse
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
from qiskit.quantum_info import Statevector

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from simulation.pruning_study_20261023.compact_sensitivity import build_compact_root_dual
parser=argparse.ArgumentParser();parser.add_argument('--cap',type=int,default=20);args=parser.parse_args()
path=Path(__file__).with_name('reviewer_compact_dense.json' if args.cap==20 else f'reviewer_compact_dense_q{args.cap}.json')
if path.exists():raise RuntimeError('Refuse to overwrite a previous dense result')
w,v,W,d=[1,2],[1,3],2,1
c=build_compact_root_dual(w,v,W,d)
out={'input':{'weights':w,'values':v,'capacity':W,'depth':d},'seed':2026102321,
     'scope':'Compact root-dual fixed-depth interface; clean workspace; all input/target amplitudes',
     'qubits':c.num_qubits,'qubit_cap':args.cap,'classification':'SIMULATED',
     'source_sha256':hashlib.sha256((ROOT/'simulation/pruning_study_20261023/compact_sensitivity.py').read_bytes()).hexdigest()}
if c.num_qubits>args.cap:out['status']='SKIPPED_DENSE_QUBIT_CAP'
else:
 count=1<<c.num_inputs;rng=np.random.default_rng(out['seed'])
 amp=rng.normal(size=2*count)+1j*rng.normal(size=2*count);amp/=np.linalg.norm(amp)
 state=np.zeros(1<<c.num_qubits,dtype=complex);expected=np.zeros_like(state)
 order=[1,0];lam=Fraction(1)
 for target in [0,1]:
  for encoded in range(count):
   p=encoded&1;tau=encoded>>d;chosen=[order[0]] if p else []
   rem=W-sum(w[i] for i in chosen);value=sum(v[i] for i in chosen)
   bound=None if rem<0 else Fraction(value)+lam*rem+sum(max(Fraction(v[i])-lam*w[i],0) for i in order[d:])
   flag=target^int(bound is None or bound<tau);a=amp[target*count+encoded]
   state[encoded|(target<<c.output)]=a;expected[encoded|(flag<<c.output)]=a
 actual=Statevector(state).evolve(c.to_qiskit()).data
 error=np.abs(actual-expected)
 out.update(status='complete',nonzero_input_amplitudes=2*count,max_amplitude_error=float(error.max()),
            differing_amplitudes_above_1e12=int(np.count_nonzero(error>1e-12)),
            raw_statevector_dimension=1<<c.num_qubits)
path.write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))
