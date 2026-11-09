"""Independent LP-vertex reference for small candidate circuit tests."""
import hashlib
import importlib.util
import itertools
import json
from fractions import Fraction
from pathlib import Path
import random
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
PROBE = ROOT/'research_log/deep_research_20261023/circuit_feasibility_probe.py'
spec = importlib.util.spec_from_file_location('reviewed_candidates', PROBE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def reference(w, v, cap, d, pref):
    order = sorted(range(len(w)),key=lambda i:Fraction(v[i],w[i]),reverse=True)
    chosen = [order[j] for j in range(d) if pref >> j & 1]
    used = sum(w[i] for i in chosen)
    base = sum(v[i] for i in chosen)
    if used > cap:
        return None
    rem = cap-used
    items = order[d:]
    best = Fraction(base)
    for mask in range(1 << len(items)):
        integral = [i for j,i in enumerate(items) if mask >> j & 1]
        weight = sum(w[i] for i in integral)
        if weight > rem:
            continue
        value = base+sum(v[i] for i in integral)
        best = max(best,Fraction(value))
        for j,i in enumerate(items):
            if not mask >> j & 1:
                f = min(Fraction(rem-weight,w[i]),Fraction(1))
                best = max(best,value+f*v[i])
    return best

cases = [([],[],0),([],[],5),([1],[1],0),([1],[1],1),([1],[1],2),
    ([2,2],[3,3],2),([2,4,6],[3,6,9],7),([4,7,6],[5,6,2],7),
    ([9,1,3],[17,4,2],1),([2,3,4],[7,1,5],9),([8,16],[16,8],16),
    ([3,5,7,8],[3,5,7,8],13),([2,3,4,5],[3,4,5,8],8),
    ([1024,2048],[2048,1024],2048),([1,2],[1,3],1 << 20)]
rng = random.Random(2026102307)
output = {'scope':'Independent prototype audit, not production circuit/full walk',
    'source_sha256':hashlib.sha256(PROBE.read_bytes()).hexdigest(),
    'configuration_classification':'HARDCODED',
    'reference_classification':'DERIVED exact vertex enumeration',
    'circuit_output_classification':'SIMULATED', 'cases':[]}
for w,v,cap in cases:
    row = {'weights':w,'values':v,'capacity':cap,'circuits':{}}
    for name,builder in [('exact_single',mod.build_exact),('exact_wrapper',mod.wrap_exact),
                         ('root_dual',mod.build_dual)]:
        circuit=builder(w,v,cap)
        if circuit.num_inputs <= 14:
            inputs=range(1 << circuit.num_inputs)
            scope='exhaustive encoded inputs with clean workspace'
        else:
            inputs=[0,(1 << circuit.num_inputs)-1]+[rng.randrange(1 << circuit.num_inputs) for _ in range(126)]
            scope='128 deterministic adversarial/random encodings'
        mismatches=[]
        dirty=0
        for target in [0,1]:
            flags,garbage=circuit.simulate_columns(inputs,target)
            dirty+=garbage
            m=len(w)
            for encoding,flag in zip(inputs,flags):
                p=encoding & ((1 << m)-1)
                d=(encoding >> m) & ((1 << circuit.depth_register_bits)-1)
                tau=encoding >> (m+circuit.depth_register_bits)
                bound=None if d>m else reference(w,v,cap,d,p)
                if name=='root_dual' and bound is not None:
                    a,b=(circuit.dual_parameters[k] for k in ['a','b'])
                    order=circuit.order
                    selected={order[j] for j in range(d) if p >> j & 1}
                    prefix=sum(v[i] for i in selected)
                    weight=sum(w[i] for i in selected)
                    bound=Fraction(prefix)+Fraction(a,b)*(cap-weight)+sum(
                        max(Fraction(v[i])-Fraction(a,b)*w[i],0) for i in order[d:])
                expected=target ^ int(bound is None or bound<tau)
                if flag!=expected:
                    mismatches.append({'encoding':encoding,'target':target,'actual':flag,
                                       'expected':expected,'bound':str(bound)})
        row['circuits'][name]={'scope':scope,'columns':2*len(inputs),'mismatches':mismatches,
                              'dirty_columns':dirty,'resources':circuit.resources()}
    output['cases'].append(row)
    print('done',w,v,cap,flush=True)
dest=Path(__file__).with_name('reviewer_adversarial_probe.json')
dest.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
print('Saved',dest,flush=True)
