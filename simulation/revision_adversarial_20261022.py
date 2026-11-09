"""Separate falsification pass for the proposed mathematical statements."""
from fractions import Fraction
import json
from pathlib import Path
import numpy as np
from exact_knapsack import lp_bound, reduced_cost_fixing, efficiency_order
from oracle_h.node_bound_reversible import precision_bits

ROOT=Path(__file__).resolve().parents[1]


def main():
    precision_cases=precision_failures=0
    for wmax in range(1,21):
        k=precision_bits(wmax)
        for ws in range(1,wmax+1):
            for vs in range(1,21):
                for residual in range(ws):
                    exact=Fraction(residual*vs,ws)
                    scaled=residual*((vs<<k)//ws)
                    for tau in set([0,exact.numerator//exact.denominator,
                                    exact.numerator//exact.denominator+1]):
                        h=((tau*(1<<k)*wmax-(1<<k))//wmax)
                        precision_cases+=1
                        precision_failures+=(scaled<=h)!=(exact<tau)
    containment_checks=containment_failures=0
    for seed in range(1000):
        rng=np.random.RandomState(seed)
        n=int(rng.randint(2,11))
        w=rng.randint(1,21,size=n).tolist()
        v=rng.randint(1,21,size=n).tolist()
        cap=int(rng.randint(1,sum(w)+1))
        order=efficiency_order(w,v)
        rem,lb=cap,0
        for i in order:
            if w[i]<=rem:
                rem-=w[i];lb+=v[i]
        rem=cap;before=[];split=None
        for i in order:
            if w[i]<=rem:
                rem-=w[i];before.append(i)
            else:
                split=i;break
        if split is None:
            continue
        lam=Fraction(v[split],w[split])
        U=lp_bound(w,v,cap)
        fi,core,fo=reduced_cost_fixing(n,w,v,cap)
        for i in range(n):
            if i==split or w[i]>cap:
                continue
            other=[j for j in range(n) if j!=i]
            perturbed=lp_bound(w,v,cap,other) if i in before else v[i]+lp_bound(w,v,cap-w[i],other)
            dual=U-w[i]*abs(Fraction(v[i],w[i])-lam)
            containment_checks+=1
            containment_failures+=perturbed>dual
            if i in core:
                containment_failures+=w[i]*abs(Fraction(v[i],w[i])-lam)>U-lb
    out={'classification':'DERIVED_EXACT_ADVERSARIAL_CHECKS',
         'precision_cases':precision_cases,'precision_failures':precision_failures,
         'random_instances':1000,'containment_checks':containment_checks,
         'containment_failures':containment_failures,
         'nonnecessity_counterexample':'All integral or dyadic efficiencies can be exact below the sufficient k bound.',
         'truncated_sort_counterexample':{'weights':[2,3],'values':[1,2],'k':1,
             'exact_order':[1,0],'truncated_tie_order':[0,1]}}
    (ROOT/'research_log/revision_20261022_adversarial_results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out))
    assert precision_failures==containment_failures==0


if __name__=='__main__':
    main()
