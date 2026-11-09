"""Independent endpoint, minimum-bank, certificate and compiled-gate controls.

Plan: LP vertex enumeration provides exact floors. Independently derive
continuous endpoints by interpolating the directly evaluated piecewise-linear
dual at density breakpoints, rather than intersecting suffix affine prefixes.
Audit all prefixes, critical disjoint certificates and brute endpoint-cell
minimums where the declared candidate budget allows. Then propagate both
output bits of compiled coherent-depth banks on selected encodings.
"""
import ast
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT));sys.dont_write_bytecode=True
from simulation.source_faithful_20261024.continuous_bank import build_continuous_bank
from simulation.pruning_study_20261023.circuits import build_dual_bank
HERE=Path(__file__).resolve().parent;SEED=2026102517;rng=random.Random(SEED)
refpath=HERE.parent/'pruning_study_20261023/reviewer_adversarial_probe.py'
fn=next(n for n in ast.parse(refpath.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='reference')
ns={'Fraction':Fraction};exec(compile(ast.Module(body=[fn],type_ignores=[]),str(refpath),'exec'),ns)
reference=ns['reference']

def independent_interval(w,v,order,d,R,K):
    grid=sorted({Fraction(0),*[Fraction(v[i],w[i]) for i in order[d:]]})
    def F(lam):return lam*R+sum(max(Fraction(v[i])-lam*w[i],0) for i in order[d:])
    values=[F(x) for x in grid];covered=[j for j,y in enumerate(values) if y<K]
    first,last=min(covered),max(covered)
    if first==0:lower=Fraction(0);opened=False
    else:
        x,y=grid[first-1:first+1];fx,fy=values[first-1:first+1]
        lower=x+(K-fx)*(y-x)/(fy-fx);opened=True
    if last==len(grid)-1:upper=Fraction(K,R) if R else None
    else:
        x,y=grid[last:last+2];fx,fy=values[last:last+2]
        upper=x+(K-fx)*(y-x)/(fy-fx)
    return lower,opened,upper

def contains(interval,lam):
    lo,opened,hi=interval
    return (lam>lo if opened else lam>=lo) and (hi is None or lam<hi)

cases=[([],[],0),([1,1],[1,1],1),([9,9],[1,1],10),([27,28,12],[1,9,5],34),
       ([2],[1],1),([2,4],[1,2],3),([1],[1],0),([2,3],[3,2],5),
       ([2,3],[0,0],0),([1,3],[0,2],1)]
for _ in range(28):
    n=rng.randrange(0,5);w=[rng.randrange(1,9) for _ in range(n)];v=[rng.randrange(0,11) for _ in range(n)]
    cases.append((w,v,rng.randrange(sum(w)+2)))
totals=dict(instance_policy_cases=0,feasible_prefixes=0,floor_mismatches=0,
    endpoint_checks=0,endpoint_mismatches=0,certificate_checks=0,certificate_failures=0,
    brute_minimum_cases=0,brute_candidate_caps=0,brute_minimum_mismatches=0,
    simulated_gate_columns=0,gate_mismatches=0,dirty_columns=0)
rows=[]
for ci,(w,v,W) in enumerate(cases):
    for policy in ['mediant','midpoint']:
        result=build_continuous_bank(w,v,W,representative=policy);order=result['order'];n=len(w)
        bank=[Fraction(*x) for x in result['bank']];states={};ends={Fraction(0)}
        for d in range(n+1):
            for p in range(1<<d):
                U=reference(w,v,W,d,p)
                if U is None:continue
                chosen=[order[j] for j in range(d) if p>>j&1];P=sum(v[i] for i in chosen);R=W-sum(w[i] for i in chosen)
                floor=U.numerator//U.denominator;K=floor-P+1
                interval=independent_interval(w,v,order,d,R,K);states[(d,R)]=(interval,K)
                actual=min(P+lam*R+sum(max(Fraction(v[i])-lam*w[i],0) for i in order[d:]) for lam in bank)
                totals['feasible_prefixes']+=1;totals['floor_mismatches']+=actual.numerator//actual.denominator!=floor
                ends.add(interval[0])
                if interval[2] is not None:ends.add(interval[2])
        if result['status']=='complete':
            recorded={(Fraction(*r['lower']),r['lower_open'],None if r['upper'] is None else Fraction(*r['upper']))
                      for r in result['coverage_interval_frequencies']}
            independent={x[0] for x in states.values()}
            totals['endpoint_checks']+=len(independent)
            totals['endpoint_mismatches']+=len(recorded.symmetric_difference(independent))
            previous=None
            for witness in result['critical_intervals']:
                key=(witness['depth'],witness['remaining_capacity']);interval=states[key][0]
                point=Fraction(*witness['point']);totals['certificate_checks']+=1
                error=not contains(interval,point)
                if previous is not None:error|=previous[2] is None or previous[2]>interval[0]
                totals['certificate_failures']+=error;previous=interval
            totals['certificate_failures']+=len(result['critical_intervals'])!=len(bank)
        ends=sorted(ends);candidates=[(a+b)/2 for a,b in zip(ends,ends[1:])]+[ends[-1]+1]
        brute=None
        if len(candidates)<=18:
            masks=[];state_intervals=[x[0] for x in states.values()]
            for lam in candidates:
                mask=sum(1<<j for j,interval in enumerate(state_intervals) if contains(interval,lam));masks.append(mask)
            full=(1<<len(state_intervals))-1
            for k in range(1,len(candidates)+1):
                if any(__import__('functools').reduce(int.__or__,choice,0)==full for choice in itertools.combinations(masks,k)):
                    brute=k;break
            totals['brute_minimum_cases']+=1;totals['brute_minimum_mismatches']+=brute!=len(bank)
        else:totals['brute_candidate_caps']+=1
        row=dict(weights=w,values=v,capacity=W,representative=policy,bank=result['bank'],bank_size=len(bank),
                 unique_states=len(states),cell_candidates=len(candidates),brute_minimum=brute,status=result['status'])
        # The pre-existing Boolean compiler restricts values to strictly positive.
        if all(x>0 for x in v):
            c=build_dual_bank(w,v,W,multipliers=bank);db=c.depth_register_bits;max_tau=(1<<c.threshold_bits)-1;samples={}
            for d in range(1<<db):
                for p in range(1<<n):
                    U=reference(w,v,W,d,p) if d<=n else None;taus={0,max_tau,rng.randrange(max_tau+1)}
                    if U is not None:
                        f=U.numerator//U.denominator;taus.update(x for x in [f-1,f,f+1,f+2] if 0<=x<=max_tau)
                    for tau in taus:samples[p|(d<<n)|(tau<<(n+db))]=int(U is None or U<tau)
            mismatch=dirty=0
            for target in [0,1]:
                flags,garbage=c.simulate_columns(samples.keys(),target);dirty+=garbage
                mismatch+=sum(flag!=(target^samples[encoded]) for encoded,flag in zip(samples,flags))
            row['gate_check']=dict(columns=2*len(samples),mismatches=mismatch,dirty_columns=dirty)
            totals['simulated_gate_columns']+=2*len(samples);totals['gate_mismatches']+=mismatch;totals['dirty_columns']+=dirty
        else:row['gate_check']=dict(status='NOT_IN_POSITIVE_VALUE_BOOLEAN_COMPILER_DOMAIN')
        rows.append(row);totals['instance_policy_cases']+=1

fallbacks=[]
for kw in [dict(capacity_cap=0),dict(state_cap=0),dict(seconds_cap=0)]:
    r=build_continuous_bank([2,3],[3,2],2,**kw)
    fallbacks.append(dict(settings=kw,status=r['status'],minimum_claim=r['minimum_among_nonnegative_rationals'],safe_tail=r['bank']==r['root_tail_grid']))
barriers=[]
for n in range(2,13):
    q=n//2;w=[2]*n+[1];v=[4*(n-i)+1 for i in range(n)]+[1];W=2*q+1
    r=build_continuous_bank(w,v,W);order=r['order'];fail=0
    for s in range(q,n):
        d=s-q;R=W;whole=sum(v[i] for i in range(d,s));K=whole+v[s]//2+1
        lo,opened,hi=independent_interval(w,v,order,d,R,K)
        rho=Fraction(v[s],2);fail+=(lo,opened,hi)!=(rho-Fraction(1,2),True,rho+Fraction(1,2))
    barriers.append(dict(main_items=n,expected=n-q+1,actual=r['bank_size'],forcing_interval_mismatches=fail))
out=dict(seed=SEED,reference_classification='DERIVED independent LP vertices and breakpoint interpolation',
    gate_classification='SIMULATED clean X/CX/CCX basis propagation',totals=totals,rows=rows,fallback_controls=fallbacks,barriers=barriers,
    source_sha256=hashlib.sha256((ROOT/'simulation/source_faithful_20261024/continuous_bank.py').read_bytes()).hexdigest())
dest=HERE/'reviewer_continuous_probe.json'
if dest.exists():raise RuntimeError('Refuse overwrite')
dest.write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(totals,indent=2))
if any(totals[k] for k in ['floor_mismatches','endpoint_mismatches','certificate_failures','brute_minimum_mismatches','gate_mismatches','dirty_columns']) or any(r['actual']!=r['expected'] or r['forcing_interval_mismatches'] for r in barriers):
    raise RuntimeError('RESEARCH_INTEGRITY_STOP: continuous independent probe failed; raw retained')
