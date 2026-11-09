"""Directed-up precision control; see pre-code derivation and independent review."""
from fractions import Fraction
from simulation.pruning_study_20261023.circuits import (
    BudgetCompiler,_data,_prefix_state,_less,_wrap,threshold_bits,
)
from simulation.oracle_h.node_bound_reversible import bits,exact_order

def constants(weight,value):
    ratio=Fraction(value,weight);a,b=ratio.numerator,ratio.denominator
    k=b.bit_length()-1 if b & (b-1)==0 else ((weight-1)*b).bit_length()
    q=((a<<k)+b-1)//b
    return dict(a=a,b=b,k=k,q=q,exact=(b*q==(a<<k)))

def build_upper_fixedpoint(weights,values,capacity,depth=None,budget=None,*,exact=False):
    weights,values,capacity=_data(weights,values,capacity)
    n=len(weights);order=tuple(exact_order(weights,values))
    if depth is not None and not 0<=depth<=n:raise ValueError('Invalid depth')
    db= max(1,n.bit_length()) if depth is None else 0
    pb=n if depth is None else depth;tb=threshold_bits(values)
    comp=BudgetCompiler(pb+db+tb,budget)
    assigned,selected,valid,rem,feasible,wb=_prefix_state(comp,weights,values,capacity,order,depth)
    tau=comp.inputs[pb+db:];S=sum(values);vb=max(1,S.bit_length()+1)
    specifications=[constants(w,v) for w,v in zip(weights,values)]
    max_encoded=(1<<tb)-1
    biggest=max([max_encoded]+[max(S*c['b']+capacity*c['a'],max_encoded*c['b']) if exact else max((S<<c['k'])+capacity*c['q'],max_encoded<<c['k']) for c in specifications])
    cb=biggest.bit_length()+1
    pval=[0]*vb
    for flag,i in zip(selected,order):pval,_=comp.add(pval,[comp.land(flag,x) for x in bits(values[i],vb)])
    active=feasible;split_reject=0
    for j,i in enumerate(order):
        if depth is not None and j<depth:continue
        reduced,enough=comp.sub(rem,bits(weights[i],wb))
        scan=comp.land(active,comp.neg(assigned[j]))
        take=comp.land(scan,enough);split=comp.land(scan,comp.neg(enough))
        whole,_=comp.add(pval,bits(values[i],vb));pval=comp.mux(take,whole,pval)
        k,q=specifications[i]['k'],specifications[i]['q']
        if exact:
            fraction=comp.const_mul(rem,specifications[i]['a'],cb)
            whole_scaled=comp.const_mul(pval,specifications[i]['b'],cb)
            total,_=comp.add(whole_scaled,fraction)
            threshold_scaled=comp.const_mul(tau,specifications[i]['b'],cb)
        else:
            fraction=comp.const_mul(rem,q,cb)
            whole_scaled=([0]*k+pval+[0]*cb)[:cb]
            total,_=comp.add(whole_scaled,fraction)
            threshold_scaled=([0]*k+tau+[0]*cb)[:cb]
        below=_less(comp,total,threshold_scaled)
        split_reject=comp.lor(split_reject,comp.land(split,below))
        rem=comp.mux(take,reduced,rem);active=comp.land(active,comp.neg(split))
    final=max(vb,tb)
    below=_less(comp,pval+[0]*(final-vb),tau+[0]*(final-tb))
    reject=comp.lor(comp.neg(valid),comp.lor(comp.neg(feasible),comp.lor(split_reject,comp.land(active,below))))
    comp.finish(reject)
    result=_wrap(comp,order,tb,db,pb,'tight_exact' if exact else 'upper_item_precision',fixed_depth=depth,
        item_constants=[dict(a=c['a'],b=c['b']) for c in specifications] if exact else specifications,
        weight_width=wb,value_width=vb,numerator_width=cb,
        precision_bits=0 if exact else max([0]+[c['k'] for c in specifications]))
    result.k=-1 if exact else max([0]+[c['k'] for c in specifications]);return result

def build_tight_exact(weights,values,capacity,depth=None,budget=None):
    return build_upper_fixedpoint(weights,values,capacity,depth=depth,budget=budget,exact=True)
