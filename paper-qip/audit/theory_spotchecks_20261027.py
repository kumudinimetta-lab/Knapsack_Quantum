"""Bounded independent exact checks of the new manuscript's one-based formulas.

No production LP, bank constructor, circuit or saved experimental row is used.
Primal box vertices plus one fractional coordinate define the LP reference.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import floor
import hashlib,json,random


def lp(w,v,R):
    if R<0:return None
    best=Q(0)
    for mask in range(1<<len(w)):
        weight=sum(a for i,a in enumerate(w) if mask>>i&1)
        if weight>R:continue
        profit=sum(a for i,a in enumerate(v) if mask>>i&1)
        best=max(best,Q(profit))
        for j in range(len(w)):
            if not(mask>>j&1) and 0<R-weight<w[j]:
                best=max(best,Q(profit)+Q((R-weight)*v[j],w[j]))
    return best


def dual(w,v,R,a):return a*R+sum(max(Q(b)-a*c,0) for c,b in zip(w,v))


def interval(w,v,R,K):
    # Independently intersect ALL subset affine constraints, not sorted prefixes.
    low=Q(0);opened=False;high=None
    for mask in range(1<<len(w)):
        D=R-sum(a for j,a in enumerate(w) if mask>>j&1)
        A=K-sum(a for j,a in enumerate(v) if mask>>j&1)
        if D>0:
            r=Q(A,D);high=r if high is None else min(high,r)
        elif D<0:
            r=Q(A,D)
            if r>low:low=r;opened=True
            elif r==low:opened=True
        else:assert A>0
    return low,opened,high


def main():
    output=Path(__file__).with_suffix('.json')
    if output.exists():raise RuntimeError('Preserve existing raw checks')
    counts=dict(barrier_instances=0,barrier_intervals=0,barrier_feasible_prefixes=0,
        core_cases=0,core_solutions_preserved=0,radius_states=0,radius_candidates=0,mismatches=0)
    for m in range(2,7):
        k=m//2;W=2*k+1
        w=[2]*m+[1];v=[4*(m-i+1)+1 for i in range(1,m+1)]+[1]
        bank=[Q(0)]+[Q(v[i-1],2) for i in range(k+1,m+1)]
        for i in range(k+1,m+1):
            d=i-k-1;U=lp(w[d:],v[d:],W);rho=Q(v[i-1],2)
            got=interval(w[d:],v[d:],W,floor(U)+1)
            assert got==(rho-Q(1,2),True,rho+Q(1,2)),(m,i,got)
            counts['barrier_intervals']+=1
        for d in range(m+2):
            for mask in range(1<<d):
                R=W-sum(w[j] for j in range(d) if mask>>j&1)
                if R<0:continue
                U=lp(w[d:],v[d:],R)
                assert min(dual(w[d:],v[d:],R,a) for a in bank)==U
                counts['barrier_feasible_prefixes']+=1
        assert interval([],[],W,1)==(Q(0),False,Q(1,W))
        counts['barrier_instances']+=1
    rng=random.Random(20261027)
    fixtures=[([2,1],[4,1],2),([2,2,3],[1,1,1],1),([],[],0)]
    for unused in range(50):
        n=rng.randint(1,5);w=[rng.randint(1,6) for _ in range(n)]
        v=[rng.randint(0,10) for _ in range(n)];W=rng.randint(0,sum(w)+1)
        fixtures.append((w,v,W))
    for w,v,W in fixtures:
        order=sorted(range(len(w)),key=lambda i:Q(v[i],w[i]),reverse=True)
        ws=[w[i] for i in order];vs=[v[i] for i in order]
        R=W;L=0
        for a,b in zip(ws,vs):
            if a<=R:R-=a;L+=b
        fixing={}
        for i in range(len(w)):
            others=[j for j in range(len(w)) if j!=i]
            out=lp([w[j] for j in others],[v[j] for j in others],W)
            inn=lp([w[j] for j in others],[v[j] for j in others],W-w[i])
            if out<L:fixing[i]=1
            if inn is None or v[i]+inn<L:
                assert i not in fixing;fixing[i]=0
        for mask in range(1<<len(w)):
            weight=sum(a for j,a in enumerate(w) if mask>>j&1)
            profit=sum(a for j,a in enumerate(v) if mask>>j&1)
            if weight<=W and profit>=L:
                assert all(((mask>>j)&1)==bit for j,bit in fixing.items())
                counts['core_solutions_preserved']+=1
        counts['core_cases']+=1
        group={rho:sum(a for a,b in zip(ws,vs) if Q(b,a)==rho) for rho in {Q(b,a)for a,b in zip(ws,vs)}}
        densities=sorted({Q(0),*[Q(b,a)for a,b in zip(ws,vs)]})
        for d in range(len(w)+1):
            for mask in range(1<<d):
                R=W-sum(ws[j] for j in range(d) if mask>>j&1)
                if R<0:continue
                U=lp(ws[d:],vs[d:],R);counts['radius_states']+=1
                for index,rho in enumerate(densities):
                    if not rho or dual(ws[d:],vs[d:],R,rho)!=U:continue
                    for a in densities[max(0,index-1):index+2]:
                        if abs(a-rho)<Q(1,rho.denominator*group[rho]):
                            assert floor(dual(ws[d:],vs[d:],R,a))==floor(U)
                            counts['radius_candidates']+=1
    result=dict(classification='DERIVED exact arithmetic checks, not quantum simulation',
       source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),counts=counts,
       fixed_settings=dict(seed=20261027,random_cases=50,barrier_main_counts=list(range(2,7))),
       denominator_wording_counterexample=dict(w=[6],v=[4],R=1,density='2/3',
           fractional_assignment='1/6',LP_value='2/3',density_denominator=3),
       core_low_threshold_boundary=dict(w=[2,1],v=[4,1],W=2,greedy_L=4,
           fixed_in=[0],fixed_out=[1],feasible_solution_below_L=[0,1],value=1))
    output.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
