"""Exhaustive adversarial prototype BEFORE any broad bank-size study."""
import itertools
import json
import random
import sys
from fractions import Fraction
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'simulation'))
from source_faithful_20261024.compressed_bank import build_compressed_bank,build_dp_free_bank,bank_floor_at_prefix,exact_order
from exact_knapsack import lp_bound


def main():
    rng=random.Random(2026102401)
    cases=[([],[],0),([2],[1],1),([2,4],[1,2],3),([2,3],[3,2],5),
           ([3,5,7,8],[3,5,7,8],13),([1,2],[3,2],0),([2,3,4],[0,0,0],4)]
    for _ in range(200):
        n=rng.randrange(0,8)
        w=[rng.randrange(1,12) for i in range(n)]
        v=[rng.randrange(0,15) for i in range(n)]
        W=rng.randrange(0,sum(w)+3)
        cases.append((w,v,W))
    counts=dict(instances=len(cases),feasible_prefixes=0,floor_mismatches=0,
                brute_grid_minimum_cases=0,brute_grid_minimum_mismatches=0,
                root_tail_exact_value_mismatches=0,noncontiguous_coverage=0,
                fallback_cases=0,dp_free_floor_mismatches=0,dp_free_cardinality_contradictions=0)
    rows=[]
    for w,v,W in cases:
        result=build_compressed_bank(w,v,W)
        dp_free=build_dp_free_bank(w,v,W)
        counts['dp_free_cardinality_contradictions']+=not (result['bank_size']<=dp_free['bank_size']<=result['root_tail_size'])
        counts['fallback_cases']+=not result['minimum_on_density_grid']
        order=exact_order(w,v);grid=[Fraction(*p) for p in result['root_tail_grid']]
        rawintervals=[]
        for d in range(len(w)+1):
            for prefix in itertools.product((0,1),repeat=d):
                weight=sum(w[i]*prefix[j] for j,i in enumerate(order[:d]))
                profit=sum(v[i]*prefix[j] for j,i in enumerate(order[:d]))
                if weight>W:continue
                exact=profit+lp_bound(w,v,W-weight,order[d:])
                floor=exact.numerator//exact.denominator
                actual=bank_floor_at_prefix(w,v,W,d,prefix,result['bank'])
                counts['feasible_prefixes']+=1
                counts['floor_mismatches']+=actual!=floor
                counts['dp_free_floor_mismatches']+=bank_floor_at_prefix(w,v,W,d,prefix,dp_free['bank'])!=floor
                residual=[Fraction(profit)+lam*(W-weight)+sum(max(Fraction(v[i])-lam*w[i],0) for i in order[d:]) for lam in grid]
                counts['root_tail_exact_value_mismatches']+=min(residual)!=exact
                covered=[j for j,value in enumerate(residual) if value<floor+1]
                counts['noncontiguous_coverage']+=covered!=list(range(min(covered),max(covered)+1))
                rawintervals.append((min(covered),max(covered)))
        minimum=None
        if len(grid)<=9:
            for k in range(1,len(grid)+1):
                if any(all(any(l<=j<=r for j in choice) for l,r in rawintervals)
                       for choice in itertools.combinations(range(len(grid)),k)):
                    minimum=k;break
            counts['brute_grid_minimum_cases']+=1
            counts['brute_grid_minimum_mismatches']+=minimum!=result['bank_size']
        rows.append(dict(weights=w,values=v,capacity=W,result=result,dp_free=dp_free,brute_minimum=minimum))
    barriers=[];repaired=[]
    for n in range(2,65):
        q=n//2;w=[2]*n;v=[4*(n-i)+1 for i in range(n)];W=2*q+1
        result=build_compressed_bank(w,v,W)
        expected=n-q+1
        barriers.append(dict(n=n,q=q,expected=expected,actual=result['bank_size'],
                             mismatch=result['bank_size']!=expected,result=result))
        repaired_result=build_compressed_bank(w+[1],v+[1],W)
        repaired.append(dict(main_items=n,total_items=n+1,q=q,expected=expected,
            actual=repaired_result['bank_size'],mismatch=repaired_result['bank_size']!=expected,
            result=repaired_result))
    out=dict(counts=counts,barrier_mismatches=sum(r['mismatch'] for r in barriers),
             repaired_barrier_mismatches=sum(r['mismatch'] for r in repaired),
             barriers=barriers,repaired_barriers=repaired,rows=rows,
             scope='Exact classical all-prefix checks; not quantum execution, circuit cost or priority approval')
    (HERE/'theory_compressed_bank_probe_v3.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(dict(counts=counts,barrier_mismatches=out['barrier_mismatches'],repaired_barrier_mismatches=out['repaired_barrier_mismatches'])),flush=True)
    if any(counts[k] for k in ['floor_mismatches','brute_grid_minimum_mismatches','root_tail_exact_value_mismatches','noncontiguous_coverage','dp_free_floor_mismatches','dp_free_cardinality_contradictions']) or out['barrier_mismatches'] or out['repaired_barrier_mismatches']:
        raise RuntimeError('RESEARCH_INTEGRITY_STOP: compressed-bank falsification failed, records retained')


if __name__=='__main__':main()
