"""Tiny all-prefix dual checks and brute finite-cell hitting minima."""
import itertools,json,random,sys
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'simulation'))
from source_faithful_20261024.continuous_bank import build_continuous_bank,coverage_interval,contains
from source_faithful_20261024.compressed_bank import exact_order,bank_floor_at_prefix
from exact_knapsack import lp_bound


def main():
    rng=random.Random(2026102501)
    cases=[([],[],0),([1,1],[1,1],1),([9,9],[1,1],10),([2],[1],1),
           ([2,3],[0,0],0),([3,5,7,8],[3,5,7,8],13),([2,3],[3,2],5)]
    for _ in range(120):
        n=rng.randrange(0,7);w=[rng.randrange(1,9) for i in range(n)];v=[rng.randrange(0,10) for i in range(n)]
        cases.append((w,v,rng.randrange(0,sum(w)+2)))
    counts=dict(instances=len(cases),feasible_prefixes=0,floor_mismatches=0,
        interval_membership_checks=0,interval_membership_mismatches=0,
        brute_cell_minimum_cases=0,brute_cell_candidate_caps=0,brute_cell_minimum_mismatches=0)
    rows=[]
    for w,v,W in cases:
        result=build_continuous_bank(w,v,W);order=exact_order(w,v);n=len(w)
        pw=[0];pv=[0]
        for i in order:pw.append(pw[-1]+w[i]);pv.append(pv[-1]+v[i])
        states=[];ends={Fraction(0)}
        for d in range(n+1):
            for prefix in itertools.product((0,1),repeat=d):
                weight=sum(w[i]*prefix[j] for j,i in enumerate(order[:d]));profit=sum(v[i]*prefix[j] for j,i in enumerate(order[:d]))
                if weight>W:continue
                exact=profit+lp_bound(w,v,W-weight,order[d:]);floor=exact.numerator//exact.denominator
                counts['feasible_prefixes']+=1
                counts['floor_mismatches']+=bank_floor_at_prefix(w,v,W,d,prefix,result['bank'])!=floor
                interval=coverage_interval(pw,pv,d,W-weight,floor-profit+1)
                states.append((d,prefix,floor,interval))
                ends.add(interval[0])
                if interval[2] is not None:ends.add(interval[2])
        ends=sorted(ends);points=[Fraction(0)]+[(a+b)/2 for a,b in zip(ends,ends[1:])]+[ends[-1]+1]
        masks=[]
        for point in points+ends:
            mask=0
            for index,(d,prefix,floor,interval) in enumerate(states):
                direct=bank_floor_at_prefix(w,v,W,d,prefix,[[point.numerator,point.denominator]])==floor
                counts['interval_membership_checks']+=1
                counts['interval_membership_mismatches']+=direct!=contains(interval,point)
                if direct:mask|=1<<index
            if point in points:masks.append(mask)
        brute=None
        if len(masks)<=18:
            goal=(1<<len(states))-1
            for k in range(1,len(masks)+1):
                for choice in itertools.combinations(masks,k):
                    total=0
                    for m in choice:total|=m
                    if total==goal:brute=k;break
                if brute is not None:break
            counts['brute_cell_minimum_cases']+=1
            counts['brute_cell_minimum_mismatches']+=brute!=result['bank_size']
        else:counts['brute_cell_candidate_caps']+=1
        rows.append(dict(weights=w,values=v,capacity=W,result=result,brute_minimum=brute))
    barriers=[]
    for n in range(2,33):
        q=n//2;w=[2]*n+[1];v=[4*(n-i)+1 for i in range(n)]+[1];W=2*q+1
        r=build_continuous_bank(w,v,W)
        barriers.append(dict(main_items=n,expected=n-q+1,actual=r['bank_size'],mismatch=r['bank_size']!=n-q+1,result=r))
    out=dict(counts=counts,barrier_mismatches=sum(r['mismatch'] for r in barriers),rows=rows,barriers=barriers,
             scope='Classical exact all-prefix and endpoint/cell checks; not circuits or priority approval')
    (HERE/'theory_continuous_bank_probe.json').write_text(json.dumps(out,indent=2));print(json.dumps(dict(counts=counts,barrier_mismatches=out['barrier_mismatches'])),flush=True)
    if any(counts[k] for k in ['floor_mismatches','interval_membership_mismatches','brute_cell_minimum_mismatches']) or out['barrier_mismatches']:
        raise RuntimeError('RESEARCH_INTEGRITY_STOP: continuous bank probe failed, raw retained')


if __name__=='__main__':main()
