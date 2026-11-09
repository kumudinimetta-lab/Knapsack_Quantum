"""Minimum-cardinality rational banks for static integer LP-pruning predicates.

25 October implementation after separately recorded derivation and two-agent
algebra review. Pseudopolynomial preprocessing is charged; no quantum runtime,
minimum-gate or priority claim. Earlier bank modules remain unchanged.
"""
from bisect import bisect_right,bisect_left
from collections import Counter
from fractions import Fraction
import time
from .compressed_bank import exact_order


def pair(value):return None if value is None else [value.numerator,value.denominator]


def contains(interval,point):
    lower,opened,upper=interval
    return (point>lower or (not opened and point==lower)) and (upper is None or point<upper)


def coverage_interval(prefix_weights,prefix_values,depth,residual,threshold):
    """Exact {lambda>=0: max_j(V_j+lambda*(R-W_j))<threshold}."""
    lower=Fraction(0);opened=False;upper=None
    for j in range(depth,len(prefix_weights)):
        D=residual-(prefix_weights[j]-prefix_weights[depth])
        C=threshold-(prefix_values[j]-prefix_values[depth])
        if D>0:
            candidate=Fraction(C,D)
            if upper is None or candidate<upper:upper=candidate
        elif D<0:
            candidate=Fraction(C,D)
            if candidate>lower:lower=candidate;opened=True
            elif candidate==lower:opened=True
        elif C<=0:
            raise AssertionError('RESEARCH_INTEGRITY_STOP: empty continuous coverage interval')
    if upper is not None and lower>=upper:
        raise AssertionError('RESEARCH_INTEGRITY_STOP: crossed continuous endpoints')
    return lower,opened,upper


def build_continuous_bank(weights,values,capacity,*,capacity_cap=5000,
                          state_cap=250000,seconds_cap=5.0,representative='mediant'):
    started=time.perf_counter()
    if len(weights)!=len(values) or any(w<=0 for w in weights) or any(v<0 for v in values) or capacity<0:
        raise ValueError('Require positive integer weights/nonnegative values/capacity')
    if any(not isinstance(x,int) for x in [*weights,*values,capacity]):raise ValueError('Integer data required')
    if representative not in ('mediant','midpoint'):raise ValueError('Unknown cell representative')
    order=exact_order(weights,values);n=len(order)
    rem=capacity;split=None
    for j,i in enumerate(order):
        if weights[i]<=rem:rem-=weights[i]
        else:split=j;break
    tail=([Fraction(0)] if split is None else sorted({Fraction(0),*[Fraction(values[i],weights[i]) for i in order[split:]]}))
    result=dict(order=list(order),root_split_position=split,root_tail_grid=[pair(x) for x in tail],
        representative=representative,reachable_state_count=0,affine_constraint_count=0,
        dp_shift_count=0,peak_reachable_sum_count=1,unique_interval_count=0,endpoint_count=0,
        critical_intervals=[],settings=dict(capacity_cap=capacity_cap,state_cap=state_cap,seconds_cap=seconds_cap),
        taxonomy='DERIVED exact rational cardinality construction; classical preprocessing time/counts MEASURED; caps HARDCODED')
    def finish(status,bank=None,minimum=False):
        bank=tail if bank is None else bank
        result.update(status=status,bank=[pair(x) for x in bank],bank_size=len(bank),
            minimum_among_nonnegative_rationals=minimum,
            max_numerator_bits=max(x.numerator.bit_length() for x in bank),
            max_denominator_bits=max(x.denominator.bit_length() for x in bank),
            preprocessing_seconds=time.perf_counter()-started)
        return result
    if split is None:return finish('all_fit_exact_shortcut',[Fraction(0)],True)
    if capacity>capacity_cap:return finish('capacity_cap_safe_root_tail_fallback')
    pw=[0];pv=[0]
    for i in order:pw.append(pw[-1]+weights[i]);pv.append(pv[-1]+values[i])
    intervals=Counter();witness={};endpoints={Fraction(0)}
    reachable=1;mask=(1<<(capacity+1))-1
    for depth in range(n+1):
        bits=reachable
        result['peak_reachable_sum_count']=max(result['peak_reachable_sum_count'],bits.bit_count())
        while bits:
            if result['reachable_state_count']>=state_cap:return finish('state_cap_safe_root_tail_fallback')
            if result['reachable_state_count']%128==0 and time.perf_counter()-started>=seconds_cap:
                return finish('time_cap_safe_root_tail_fallback')
            least=bits&-bits;s=least.bit_length()-1;bits^=least;R=capacity-s
            if R>=pw[n]-pw[depth]:floor_lp=pv[n]-pv[depth];optimal=Fraction(0)
            else:
                j=bisect_right(pw,pw[depth]+R)-1
                r=R-(pw[j]-pw[depth]);i=order[j]
                floor_lp=pv[j]-pv[depth]+r*values[i]//weights[i]
                optimal=Fraction(values[i],weights[i])
            interval=coverage_interval(pw,pv,depth,R,floor_lp+1)
            result['affine_constraint_count']+=n-depth+1
            if not contains(interval,optimal):
                raise AssertionError('RESEARCH_INTEGRITY_STOP: optimal multiplier outside continuous coverage')
            intervals[interval]+=1
            witness.setdefault(interval,dict(depth=depth,remaining_capacity=R,floor_lp=floor_lp))
            endpoints.add(interval[0])
            if interval[2] is not None:endpoints.add(interval[2])
            result['reachable_state_count']+=1
        if depth<n:
            reachable=(reachable|(reachable<<weights[order[depth]]))&mask
            result['dp_shift_count']+=1
    endpoints=sorted(endpoints);selected=[];critical=[]
    ordered=sorted(intervals,key=lambda x:(x[2] is None,Fraction(0) if x[2] is None else x[2],x[0],x[1]))
    for interval in ordered:
        if selected and contains(interval,selected[-1]):continue
        lower,opened,upper=interval
        if upper is None:point=endpoints[-1]+1;previous=None
        else:
            index=bisect_left(endpoints,upper)
            if index<=0:raise AssertionError('RESEARCH_INTEGRITY_STOP: no predecessor of positive coverage upper endpoint')
            previous=endpoints[index-1]
            point=(Fraction(previous.numerator+upper.numerator,previous.denominator+upper.denominator)
                   if representative=='mediant' else (previous+upper)/2)
        if not contains(interval,point):raise AssertionError('RESEARCH_INTEGRITY_STOP: chosen cell point misses critical interval')
        selected.append(point)
        critical.append(dict(lower=pair(lower),lower_open=opened,upper=pair(upper),
            point=pair(point),predecessor_endpoint=pair(previous),**witness[interval]))
    if any(not any(contains(interval,x) for x in selected) for interval in intervals):
        raise AssertionError('RESEARCH_INTEGRITY_STOP: uncovered reachable continuous state')
    for left,right in zip(critical,critical[1:]):
        if left['upper'] is None or Fraction(*left['upper'])>Fraction(*right['lower']):
            raise AssertionError('RESEARCH_INTEGRITY_STOP: critical coverage intervals overlap')
    result.update(unique_interval_count=len(intervals),endpoint_count=len(endpoints),critical_intervals=critical,
                  coverage_interval_frequencies=[dict(lower=pair(l),lower_open=o,upper=pair(u),count=count) for (l,o,u),count in intervals.items()])
    return finish('complete',selected,True)
