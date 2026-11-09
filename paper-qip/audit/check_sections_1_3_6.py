"""Read-only evidence checks; writes only a new manuscript-audit summary."""
from pathlib import Path
import sys,json,itertools,hashlib
from fractions import Fraction as Q
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from simulation.exact_knapsack import reduced_cost_fixing
from simulation.source_faithful_20261024.qft_bank import bank_geometry
from research_log.claim_validation_20261025.theory_adversarial_audit import vertices,dual
p=ROOT/'research_log/pruning_study_20261023'
original=json.loads((p/'inputs.json').read_text())['records']
rows=[r for r in original if r['category']=='main700']
assert len(rows)==700
for r in rows:
    n,seed,kind=r['n'],r['seed'],r['instance_class']
    assert seed==1000*n+r['trial']
    rng=np.random.RandomState(seed)
    if kind=='inverse_strongly':
        v=rng.randint(1,101,size=n).tolist();w=[x+10 for x in v]
    else:
        w=rng.randint(1,101,size=n).tolist()
        if kind=='uncorrelated':v=rng.randint(1,101,size=n).tolist()
        elif kind=='weakly_correlated':v=[max(1,x+rng.randint(-10,11)) for x in w]
        elif kind=='strongly_correlated':v=[x+10 for x in w]
        elif kind=='subset_sum':v=w[:]
        else:raise AssertionError(kind)
    assert (w,v,sum(w)//2)==(r['weights'],r['values'],r['capacity'])
lookup={r['id']:r for r in rows}
cores=json.loads((p/'inputs_core700.json').read_text())['records']
for r in cores:
    o=lookup[r['original_id']]
    fi,c,fo=reduced_cost_fixing(o['n'],o['weights'],o['values'],o['capacity'])
    assert (fi,c,fo)==(r['fixed_in_indices'],r['core_original_indices'],r['fixed_out_indices'])
    assert r['weights']==[o['weights'][i] for i in c]
    assert r['values']==[o['values'][i] for i in c]
    assert r['capacity']==o['capacity']-sum(o['weights'][i] for i in fi)
manifest=json.loads((ROOT/'research_log/source_faithful_20261024/qft_bank_full105_manifest.json').read_text())
assert set(manifest['cohort_ids'])=={r['id'] for r in rows if r['trial'] in [0,1,2]}
checks=0
for w,v,W in [([],[],0),([1],[0],0),([2],[3],1),([2,4,1],[1,2,0],3),([17,3],[16,2],1)]:
    bank={Q(0),Q(1,2),*[Q(a,b) for a,b in zip(v,w)]}
    for d in range(len(w)+1):
        *_,order,B,wb,cb,tb,entries=bank_geometry(w,v,W,d,bank)
        assert wb==max(1,1+(W+sum(w)).bit_length())
        assert tb==max(1,(1+sum(v)).bit_length())
        assert cb==max(1,1+max(max(e['constant'],e['accumulator_bound']) for e in entries).bit_length())
        for bits in itertools.product([0,1],repeat=d):
            P=sum(v[i]*x for i,x in zip(order[:d],bits));R=W-sum(w[i]*x for i,x in zip(order[:d],bits))
            for lam,e in zip(B,entries):
                costs=e['costs'];D=sum(max(costs[i],0) for i in order[:d])
                for i,x in zip(order[:d],bits):
                    D-=x*costs[i]
                    assert 0<=D<=sum(abs(costs[j]) for j in order[:d])
                assert Q(e['constant']-D,lam.denominator)==P+dual([w[i] for i in order[d:]],[v[i] for i in order[d:]],R,lam)
                for tau in range(1<<tb):
                    assert D+lam.denominator*tau<=e['accumulator_bound']<1<<cb
                    checks+=1
# A nonrejected node can lack a TARGET-REACHING completion, not any completion.
assert vertices([2],[3],1)==Q(3,2)
assert not (Q(3,2)<1) and max(0,0)==0<1
out={'classification':'DERIVED arithmetic/source consistency checks; no new gate simulation',
     'generator_records':len(rows),'generator_mismatches':0,'core_records':len(cores),'core_mismatches':0,
     'resource_selection_records':len(manifest['cohort_ids']),'selection_mismatches':0,
     'encoded_arithmetic_checks':checks,'arithmetic_mismatches':0,
     'target_completion_counterexample':{'w':[2],'v':[3],'W':1,'tau':1,'LP':'3/2','integer_optimum':0},
     'manuscript_sha256':hashlib.sha256((ROOT/'paper-qip/main.tex').read_bytes()).hexdigest()}
(ROOT/'paper-qip/audit/SECTIONS_1_3_6_CHECKS.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
