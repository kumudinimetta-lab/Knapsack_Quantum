"""Independent tiny LP-vertex controls; production and author raw data untouched.

Plan: exact vertex enumeration rather than greedy LP reference; dynamic-depth
rounding columns include ignored suffix bits and invalid depths; fixed-depth
controls use the same reference. Compressed-bank checks enumerate all reachable
prefixes and brute-force the finite-grid minimum. No quantum-runtime inference.
"""
import ast
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT));sys.dont_write_bytecode=True
from simulation.source_faithful_20261024.rounding import build_upper_fixedpoint,constants
from simulation.source_faithful_20261024.compressed_bank import build_compressed_bank

REFERENCE=ROOT/'research_log/pruning_study_20261023/reviewer_adversarial_probe.py'
tree=ast.parse(REFERENCE.read_text())
fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='reference')
namespace={'Fraction':Fraction}
exec(compile(ast.Module(body=[fn],type_ignores=[]),str(REFERENCE),'exec'),namespace)
reference=namespace['reference']
SEED=2026102411
rng=random.Random(SEED)
cases=[([],[],0),([1],[1],0),([1],[1],1),([3],[1],2),([3],[2],2),
       ([6,4,1],[7,4,1],5),([8,16],[16,8],17),([2,4,6],[3,6,9],7),
       ([9,1,3],[17,4,2],1),([2,3,5,7],[5,1,8,9],12),
       ([1,3],[1,2],1<<16)]
for _ in range(36):
    n=rng.randrange(1,6)
    w=[rng.randrange(1,14) for _ in range(n)]
    v=[rng.randrange(1,20) for _ in range(n)]
    cases.append((w,v,rng.randrange(sum(w)+3)))

out={'seed':SEED,'configuration_classification':'HARDCODED',
     'reference_classification':'DERIVED exact LP vertex enumeration',
     'column_classification':'SIMULATED reversible X/CX/CCX basis propagation',
     'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [
         ROOT/'simulation/source_faithful_20261024/rounding.py',
         ROOT/'simulation/source_faithful_20261024/compressed_bank.py',REFERENCE]},
     'rows':[],'first_failures':[]}
totals={'rounding_columns':0,'rounding_mismatches':0,'rounding_dirty_columns':0,
        'compressed_feasible_prefixes':0,'compressed_floor_mismatches':0,
        'compressed_root_tail_exact_mismatches':0,'noncontiguous_coverage':0,
        'brute_grid_minimum_cases':0,'brute_grid_minimum_mismatches':0}

for index,(w,v,W) in enumerate(cases):
    n=len(w);db=max(1,n.bit_length());order=sorted(range(n),key=lambda i:Fraction(v[i],w[i]),reverse=True)
    row={'weights':w,'values':v,'capacity':W,'rounding':[]}
    for dfix in [None]+([0,n//2,n] if index<11 else []):
        c=build_upper_fixedpoint(w,v,W,depth=dfix)
        max_tau=(1<<c.threshold_bits)-1
        samples={};suffix_variants=0
        for d in range(1<<db) if dfix is None else [dfix]:
            for p in range(1<<n) if dfix is None else range(1<<d):
                bound=reference(w,v,W,d,p) if d<=n else None
                taus={0,max_tau,rng.randrange(max_tau+1)}
                if bound is not None:
                    f=bound.numerator//bound.denominator
                    taus.update(t for t in [f-1,f,f+1,f+2] if 0<=t<=max_tau)
                for tau in taus:
                    encoded=(p|(d<<n)|(tau<<(n+db))) if dfix is None else p|(tau<<d)
                    samples[encoded]=int(bound is None or bound<tau)
                suffix_variants+=int(d<=n and (p>>d)!=0)
        mismatch=dirty=0
        for target in [0,1]:
            flags,garbage=c.simulate_columns(samples.keys(),target)
            dirty+=garbage
            for encoded,actual in zip(samples,flags):
                expected=target^samples[encoded]
                if actual!=expected:
                    mismatch+=1
                    if len(out['first_failures'])<8:
                        out['first_failures'].append(dict(case=index,depth=dfix,encoding=encoded,
                            target=target,actual=actual,expected=expected))
        check={'fixed_depth':dfix,'columns':2*len(samples),'mismatches':mismatch,
               'dirty_columns':dirty,'prefixes_with_nonzero_ignored_suffix':suffix_variants,
               'precision_bits':c.k,'qubits':c.num_qubits}
        row['rounding'].append(check)
        totals['rounding_columns']+=check['columns'];totals['rounding_mismatches']+=mismatch
        totals['rounding_dirty_columns']+=dirty
    bank=build_compressed_bank(w,v,W)
    grid=[Fraction(*p) for p in bank['root_tail_grid']]
    selected=[Fraction(*p) for p in bank['bank']]
    intervals=[]
    for d in range(n+1):
        for p in range(1<<d):
            chosen=[order[j] for j in range(d) if (p>>j)&1]
            used=sum(w[i] for i in chosen)
            if used>W:continue
            P=sum(v[i] for i in chosen);R=W-used
            exact=reference(w,v,W,d,p);floor=exact.numerator//exact.denominator
            def evaluate(lam):
                return P+lam*R+sum(max(Fraction(v[i])-lam*w[i],0) for i in order[d:])
            values=[evaluate(lam) for lam in grid]
            coverage=[j for j,value in enumerate(values) if value<floor+1]
            actual=min(evaluate(lam) for lam in selected)
            totals['compressed_feasible_prefixes']+=1
            totals['compressed_floor_mismatches']+=actual.numerator//actual.denominator!=floor
            totals['compressed_root_tail_exact_mismatches']+=min(values)!=exact
            totals['noncontiguous_coverage']+=coverage!=list(range(min(coverage),max(coverage)+1))
            intervals.append((min(coverage),max(coverage)))
    for size in range(1,len(grid)+1):
        if any(all(any(lo<=j<=hi for j in choice) for lo,hi in intervals)
               for choice in itertools.combinations(range(len(grid)),size)):
            minimum=size;break
    totals['brute_grid_minimum_cases']+=1
    totals['brute_grid_minimum_mismatches']+=minimum!=bank['bank_size']
    row['bank']={'status':bank['status'],'size':bank['bank_size'],
        'root_tail_size':len(grid),'brute_grid_minimum':minimum}
    out['rows'].append(row)

fallbacks=[]
for kw in [dict(capacity_cap=0),dict(state_cap=0),dict(seconds_cap=0)]:
    result=build_compressed_bank([2,3],[3,2],2,**kw)
    fallbacks.append({'settings':kw,'status':result['status'],'minimum':result['minimum_on_density_grid'],
                     'bank_equals_root_tail':result['bank']==result['root_tail_grid']})
out['fallback_controls']=fallbacks
barriers=[]
for n in range(2,18):
    q=n//2;w=[2]*n+[1];v=[4*(n-i)+1 for i in range(n)]+[1];W=2*q+1
    result=build_compressed_bank(w,v,W)
    barriers.append({'main_items':n,'expected':n-q+1,'actual':result['bank_size'],
        'weights_gcd':__import__('math').gcd(*w),'profits_gcd':__import__('math').gcd(*v)})
out['repaired_barrier']=barriers;out['totals']=totals
path=Path(__file__).with_name('reviewer_new_controls.json')
if path.exists():raise RuntimeError('Refuse overwrite of independent raw results')
path.write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps(totals,indent=2))
if any(totals[k] for k in totals if 'mismatch' in k or k in ['rounding_dirty_columns','noncontiguous_coverage']):
    raise RuntimeError('RESEARCH_INTEGRITY_STOP: independent control failed; raw retained')
