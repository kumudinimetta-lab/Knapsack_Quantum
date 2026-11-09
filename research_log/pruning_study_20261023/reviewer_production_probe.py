"""Independent selected production-circuit audit; no other files mutated."""
import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path
import random
import sys

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from simulation.pruning_study_20261023 import circuits as c
from simulation.pruning_study_20261023 import trees
spec=importlib.util.spec_from_file_location('independent_reference',Path(__file__).with_name('reviewer_adversarial_probe.py'))
# Load the reference function without executing the prototype test script.
import ast
source=ast.parse(Path(__file__).with_name('reviewer_adversarial_probe.py').read_text(encoding='utf-8'))
fn=next(n for n in source.body if isinstance(n,ast.FunctionDef) and n.name=='reference')
ns={'Fraction':Fraction}
exec(compile(ast.Module(body=[fn],type_ignores=[]),'<independent LP vertices>','exec'),ns)
reference=ns['reference']
cases=[([],[],0),([],[],5),([1],[1],0),([1],[1],1),([1],[1],2),
 ([2,2],[3,3],2),([2,4,6],[3,6,9],7),([4,7,6],[5,6,2],7),
 ([9,1,3],[17,4,2],1),([2,3,4],[7,1,5],9),([8,16],[16,8],16),
 ([3,5,7,8],[3,5,7,8],13),([2,3,4,5],[3,4,5,8],8),
 ([1024,2048],[2048,1024],2048),([1,2],[1,3],1<<20)]
builders={'simple':c.build_simple,'root_dual':c.build_root_dual,
 'bank2':lambda w,v,W:c.build_dual_bank(w,v,W,q=2),
 'bank4':lambda w,v,W:c.build_dual_bank(w,v,W,q=4),
 'exact_single':c.build_exact_single_scan,'fixedpoint_single':c.build_fixedpoint_single_scan,
 'exact_wrapper':c.build_exact_depth_wrapper}
rng=random.Random(2026102308)
out={'scope':'Independent production audit; clean-workspace basis columns, selected fifteen inputs',
 'taxonomy':{'outputs':'SIMULATED','references':'DERIVED','configs':'HARDCODED'},
 'source_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
    [ROOT/'simulation/pruning_study_20261023/circuits.py',ROOT/'simulation/pruning_study_20261023/trees.py']},
 'cases':[],'tree_checks':[],'budget_checks':[]}
for w,v,W in cases:
 row={'weights':w,'values':v,'capacity':W,'circuits':{}}
 for name,builder in builders.items():
  circuit=builder(w,v,W)
  inputs=range(1<<circuit.num_inputs) if circuit.num_inputs<=14 else [0,(1<<circuit.num_inputs)-1]+[rng.randrange(1<<circuit.num_inputs) for _ in range(126)]
  failures=[];dirty=0;safety=0
  for target in [0,1]:
   flags,garbage=circuit.simulate_columns(inputs,target);dirty+=garbage
   for encoding,flag in zip(inputs,flags):
    n=len(w);d=(encoding>>n)&((1<<circuit.depth_register_bits)-1);p=encoding&((1<<n)-1);tau=encoding>>(n+circuit.depth_register_bits)
    exact=None if d>n else reference(w,v,W,d,p)
    bound=exact
    if exact is not None and name in ['simple','root_dual','bank2','bank4']:
     chosen=[circuit.order[j] for j in range(d) if p>>j&1]
     profit=sum(v[i] for i in chosen);weight=sum(w[i] for i in chosen)
     multipliers=[Fraction(0)] if name=='simple' else [Fraction(a,b) for a,b in circuit.metadata['multipliers']]
     bound=min(profit+lam*(W-weight)+sum(max(Fraction(v[i])-lam*w[i],0) for i in circuit.order[d:]) for lam in multipliers)
    expected=target^int(bound is None or bound<tau)
    if flag!=expected:failures.append({'encoding':encoding,'target':target,'expected':expected,'actual':flag,'bound':str(bound)})
    safety+=bool((flag^target) and exact is not None and exact>=tau)
  row['circuits'][name]={'columns':2*len(inputs),'exhaustive':isinstance(inputs,range),'mismatches':failures,'dirty_columns':dirty,'unsafe_pruning':safety}
 out['cases'].append(row)
 # Tree full counts and structural recovery must agree with independent integral enumeration.
 opt=max(sum(v[i] for i in range(len(w)) if x>>i&1) for x in range(1<<len(w)) if sum(w[i] for i in range(len(w)) if x>>i&1)<=W)
 for method in trees.METHODS:
  result=trees.structural_optimize(w,v,W,method,node_cap=100000,seconds_cap=10)
  checks={'input':[w,v,W],'method':method,'status':result['status'],'value_match':result['lower']==opt,'witness_valid':result['witness_valid']}
  floor=result['initial_lower']+1
  cert=result['certificate']['bound']
  violations=[]
  for tau in range(floor,min(sum(v)+2,floor+3)):
   full=trees.enumerate_threshold_tree(w,v,W,tau,method,node_cap=100000,seconds_cap=10)
   if full['nodes']>cert:violations.append([tau,full['nodes'],cert])
  checks['certificate_violations']=violations
  out['tree_checks'].append(checks)
 print('done',w,v,W,flush=True)
for label,budget in [('qubit',c.BuildBudget(max_qubits=3,max_gates=100000,max_seconds=10)),('gate',c.BuildBudget(max_qubits=100000,max_gates=2,max_seconds=10)),('time',c.BuildBudget(max_qubits=100000,max_gates=100000,max_seconds=0))]:
 try:c.build_root_dual([2,3],[3,4],3,budget);out['budget_checks'].append({'configured':label,'cap':None})
 except c.CircuitBuildCap as err:out['budget_checks'].append({'configured':label,'cap':err.reason,'counters':err.counters})
dest=Path(__file__).with_name('reviewer_production_probe.json');dest.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print('Saved',dest,flush=True)
