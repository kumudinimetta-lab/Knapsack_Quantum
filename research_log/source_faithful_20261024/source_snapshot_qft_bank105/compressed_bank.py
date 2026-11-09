"""Data-only finite-density-grid banks preserving all integer LP pruning.

Derivation and independent review precede this implementation in
research_log/source_faithful_20261024/theory_compressed_bank_derivation.md.
Pseudo-polynomial preprocessing is explicit. No circuit synthesis/runtime claim.
"""
from __future__ import annotations
from bisect import bisect_right
from collections import Counter
from fractions import Fraction
import time


def exact_order(weights,values):
    return tuple(sorted(range(len(weights)),key=lambda i:Fraction(values[i],weights[i]),reverse=True))


def _fraction_pair(value): return [value.numerator,value.denominator]


def build_compressed_bank(weights,values,capacity,*,capacity_cap=5000,
                          state_cap=250000,seconds_cap=5.0):
    started=time.perf_counter()
    if len(weights)!=len(values) or any(w<=0 for w in weights) or any(v<0 for v in values) or capacity<0:
        raise ValueError('Require positive integer weights, nonnegative integer values/capacity')
    if any(not isinstance(x,int) for x in [*weights,*values,capacity]):
        raise ValueError('Integer data required')
    n=len(weights);order=exact_order(weights,values)
    full_grid=sorted({Fraction(0),*[Fraction(v,w) for w,v in zip(weights,values)]})
    rem=capacity;split=None
    for j,i in enumerate(order):
        if weights[i]<=rem: rem-=weights[i]
        else: split=j;break
    grid=([Fraction(0)] if split is None else sorted({Fraction(0),*[Fraction(values[i],weights[i]) for i in order[split:]]}))
    base=dict(order=list(order),root_split_position=split,
        full_density_grid=[_fraction_pair(x) for x in full_grid],
        root_tail_grid=[_fraction_pair(x) for x in grid],
        original_grid_size=len(full_grid),root_tail_size=len(grid),
        settings=dict(capacity_cap=capacity_cap,state_cap=state_cap,seconds_cap=seconds_cap),
        taxonomy={'bank_and_coverage':'DERIVED exact integer/rational construction',
                  'seconds_and_operations':'MEASURED classical preprocessing',
                  'caps':'HARDCODED work budget'},
        reachable_state_count=0,coverage_comparisons=0,unique_interval_count=0,
        dp_shift_count=0,peak_reachable_sum_count=1,intervals=[],greedy_witness_intervals=[])

    def finish(status,bank=None,minimum=False):
        base.update(status=status,bank=[_fraction_pair(x) for x in (grid if bank is None else bank)],
                    bank_size=len(grid if bank is None else bank),minimum_on_density_grid=minimum,
                    preprocessing_seconds=time.perf_counter()-started)
        return base
    if split is None:
        return finish('all_fit_exact_shortcut',[Fraction(0)],True)
    if capacity>capacity_cap:
        return finish('capacity_cap_safe_root_tail_fallback')
    pw=[0];pv=[0]
    for i in order:
        pw.append(pw[-1]+weights[i]);pv.append(pv[-1]+values[i])
    grid_index={x:j for j,x in enumerate(grid)}
    pairs=[(x.numerator,x.denominator) for x in grid]
    suffix=[[0]*len(grid) for _ in range(n+1)]
    for d in reversed(range(n)):
        i=order[d]
        for j,(a,b) in enumerate(pairs):
            suffix[d][j]=suffix[d+1][j]+max(b*values[i]-a*weights[i],0)
    intervals=Counter();witness={}
    mask=(1<<(capacity+1))-1
    reachable=1
    for d in range(n+1):
        bits=reachable
        base['peak_reachable_sum_count']=max(base['peak_reachable_sum_count'],bits.bit_count())
        while bits:
            if base['reachable_state_count']>=state_cap:
                return finish('state_cap_safe_root_tail_fallback')
            if base['reachable_state_count']%128==0 and time.perf_counter()-started>=seconds_cap:
                return finish('time_cap_safe_root_tail_fallback')
            lowest=bits&-bits;s=lowest.bit_length()-1;bits^=lowest
            R=capacity-s
            if R>=pw[n]-pw[d]:
                floor_lp=pv[n]-pv[d];opt=grid_index[Fraction(0)]
            else:
                j=bisect_right(pw,pw[d]+R)-1
                residual=R-(pw[j]-pw[d])
                floor_lp=pv[j]-pv[d]+residual*values[order[j]]//weights[order[j]]
                opt=grid_index[Fraction(values[order[j]],weights[order[j]])]
            threshold=floor_lp+1

            def covered(j):
                base['coverage_comparisons']+=1
                a,b=pairs[j]
                return a*R+suffix[d][j]<b*threshold

            if not covered(opt):
                raise AssertionError('RESEARCH_INTEGRITY_STOP: selected LP-optimal candidate fails coverage')
            lo,hi=0,opt
            while lo<hi:
                mid=(lo+hi)//2
                if covered(mid):hi=mid
                else:lo=mid+1
            left=lo
            lo,hi=opt,len(grid)-1
            while lo<hi:
                mid=(lo+hi+1)//2
                if covered(mid):lo=mid
                else:hi=mid-1
            interval=(left,lo)
            intervals[interval]+=1
            witness.setdefault(interval,dict(depth=d,remaining_capacity=R,floor_lp=floor_lp))
            base['reachable_state_count']+=1
        if d<n:
            reachable=(reachable|(reachable<<weights[order[d]]))&mask
            base['dp_shift_count']+=1
    selected=[];critical=[]
    for interval in sorted(intervals,key=lambda x:(x[1],x[0])):
        left,right=interval
        if not selected or selected[-1]<left:
            selected.append(right)
            critical.append(dict(left=left,right=right,**witness[interval]))
    if any(not any(left<=j<=right for j in selected) for left,right in intervals):
        raise AssertionError('RESEARCH_INTEGRITY_STOP: interval greedy leaves uncovered state')
    if any(a['right']>=b['left'] for a,b in zip(critical,critical[1:])):
        raise AssertionError('RESEARCH_INTEGRITY_STOP: minimum-cardinality witness intervals overlap')
    base['intervals']=[dict(left=l,right=r,count=count,first_state=witness[(l,r)]) for (l,r),count in sorted(intervals.items())]
    base['unique_interval_count']=len(intervals)
    base['greedy_witness_intervals']=critical
    return finish('complete',[grid[j] for j in selected],True)


def bank_floor_at_prefix(weights,values,capacity,depth,prefix,bank):
    """Independent Fraction reference; None for overweight/invalid prefixes."""
    order=exact_order(weights,values)
    if not 0<=depth<=len(weights):return None
    weight=sum(weights[i]*prefix[j] for j,i in enumerate(order[:depth]))
    profit=sum(values[i]*prefix[j] for j,i in enumerate(order[:depth]))
    if weight>capacity:return None
    R=capacity-weight
    values_dual=[]
    for pair in bank:
        lam=Fraction(*pair)
        upper=profit+lam*R+sum(max(Fraction(values[i])-lam*weights[i],0) for i in order[depth:])
        values_dual.append(upper.numerator//upper.denominator)
    return min(values_dual)


def build_dp_free_bank(weights,values,capacity):
    """Conservative all-state sufficient radius bank; no capacity reachability DP.

    Minimum only for the recorded sufficient interval family, NOT the minimum
    actual density-grid bank. The radius may retain the whole root-tail grid.
    """
    started=time.perf_counter()
    if len(weights)!=len(values) or any(w<=0 for w in weights) or any(v<0 for v in values) or capacity<0:
        raise ValueError('Require positive integer weights/nonnegative values/capacity')
    if any(not isinstance(x,int) for x in [*weights,*values,capacity]):
        raise ValueError('Integer data required')
    order=exact_order(weights,values)
    full=sorted({Fraction(0),*[Fraction(v,w) for w,v in zip(weights,values)]})
    rem=capacity;split=None
    for j,i in enumerate(order):
        if weights[i]<=rem:rem-=weights[i]
        else:split=j;break
    grid=([Fraction(0)] if split is None else sorted({Fraction(0),*[Fraction(values[i],weights[i]) for i in order[split:]]}))
    group_weights=Counter()
    for w,v in zip(weights,values):group_weights[Fraction(v,w)]+=w
    intervals=[dict(left=0,right=0,reason='Mandatory zero for all-fit/empty suffix')]
    comparisons=0
    if split is not None:
        for index,rho in enumerate(grid):
            if not rho:continue
            L=group_weights[rho];covered=[];a,b=rho.numerator,rho.denominator
            for j in range(max(0,index-1),min(len(grid),index+2)):
                c,d=grid[j].numerator,grid[j].denominator
                comparisons+=1
                if abs(a*d-b*c)*L<d:covered.append(j)
            if index not in covered or covered!=list(range(min(covered),max(covered)+1)):
                raise AssertionError('RESEARCH_INTEGRITY_STOP: invalid sufficient radius interval')
            intervals.append(dict(left=min(covered),right=max(covered),density=_fraction_pair(rho),
                                  global_group_weight=L,reason='Strict adjacent-breakpoint radius'))
    selected=[];critical=[]
    for interval in sorted(intervals,key=lambda x:(x['right'],x['left'])):
        if not selected or selected[-1]<interval['left']:
            selected.append(interval['right']);critical.append(interval)
    if any(not any(x['left']<=j<=x['right'] for j in selected) for x in intervals):
        raise AssertionError('RESEARCH_INTEGRITY_STOP: uncovered DP-free sufficient constraint')
    return dict(status='all_fit_exact_shortcut' if split is None else 'complete_sufficient_dp_free',
        bank=[_fraction_pair(grid[j]) for j in selected],bank_size=len(selected),
        original_grid_size=len(full),root_tail_size=len(grid),root_tail_grid=[_fraction_pair(x) for x in grid],
        order=list(order),root_split_position=split,group_intervals=intervals,
        greedy_witness_intervals=critical,minimum_on_density_grid=False,
        minimum_for_sufficient_constraints=True,reachable_state_count=0,dp_shift_count=0,
        radius_comparisons=comparisons,preprocessing_seconds=time.perf_counter()-started,
        taxonomy='DERIVED conservative all-state sufficient bank; local time/comparison counts MEASURED; no quantum execution')
