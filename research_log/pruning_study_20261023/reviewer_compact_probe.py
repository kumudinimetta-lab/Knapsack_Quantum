"""Independent scalar primitive checks plus selected fixed-depth predicate checks."""
import ast
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from simulation.pruning_study_20261023 import compact_sensitivity as cs
HERE=Path(__file__).resolve().parent
refsource=ast.parse((HERE/'reviewer_adversarial_probe.py').read_text(encoding='utf-8'))
refnode=next(x for x in refsource.body if isinstance(x,ast.FunctionDef) and x.name=='reference')
ns={'Fraction':Fraction};exec(compile(ast.Module(body=[refnode],type_ignores=[]),'<vertex reference>','exec'),ns)
reference=ns['reference']

def scalar(state,gates):
    for target,controls in gates:
        if all(state>>q&1 for q in controls):state^=1<<target
    return state

out={'scope':'Independent compact primitive and matching fixed-depth predicate audit',
 'taxonomy':{'outputs':'SIMULATED','resources_and_references':'DERIVED','domains':'HARDCODED'},
 'source_sha256':hashlib.sha256((ROOT/'simulation/pruning_study_20261023/compact_sensitivity.py').read_bytes()).hexdigest(),
 'primitives':[],'predicate_cases':[]}
for width in range(1,6):
    c=cs.Ripple(2*width);a=list(range(width));b=list(range(width,2*width));add=c.adder(a,b)
    compare=cs.Ripple(2*width);compare.less(a,b,compare.output)
    addition_fail=[];comparison_fail=[];checked=0
    for av in range(1<<width):
      for bv in range(1<<width):
        initial=av|(bv<<width);expected=av|(((av+bv)%(1<<width))<<width)
        after=scalar(initial,add)
        if after!=expected or scalar(after,list(reversed(add)))!=initial:addition_fail.append([av,bv,after,expected])
        for target in [0,1]:
          x=initial|(target<<compare.output);expect=initial|((target^int(av<bv))<<compare.output)
          actual=scalar(x,compare.gates);checked+=1
          if actual!=expect:comparison_fail.append([av,bv,target,actual,expect])
    out['primitives'].append({'width':width,'adder_columns':1<<(2*width),'adder_mismatches':addition_fail,
       'comparator_columns':checked,'comparator_mismatches':comparison_fail})
for width in range(1,5):
    failures=[];count=0
    for constant in range(1<<width):
      for subtract in [False,True]:
        c=cs.Ripple(1+width,scratch_width=width);dest=list(range(1,width+1));c.controlled_constant(dest,constant,0,subtract)
        for control in [0,1]:
          for value in range(1<<width):
            x=control|(value<<1);sign=-1 if subtract else 1
            expected=control|(((value+control*sign*constant)%(1<<width))<<1)
            actual=scalar(x,c.gates);count+=1
            if actual!=expected:failures.append([constant,subtract,control,value,actual,expected])
    out['primitives'].append({'controlled_constant_width':width,'columns':count,'mismatches':failures})
cases=[([],[],0),([1],[1],0),([1],[1],1),([2,2],[3,3],2),
 ([2,4,6],[3,6,9],7),([4,7,6],[5,6,2],7),([9,1,3],[17,4,2],1),
 ([2,3,4],[7,1,5],9),([3,5,7,8],[3,5,7,8],13),([2,3,4,5],[3,4,5,8],8)]
for w,v,W in cases:
 for d in range(len(w)+1):
  for name,builder in cs.FIXED_BUILDERS.items():
   circuit=builder(w,v,W,d);encodings=range(1<<circuit.num_inputs);mismatch=[];dirty=0
   order=sorted(range(len(w)),key=lambda i:Fraction(v[i],w[i]),reverse=True)
   rem=W;lam=Fraction(0)
   for i in order:
    if w[i]<=rem:rem-=w[i]
    else:lam=Fraction(v[i],w[i]);break
   for target in [0,1]:
    flags,garbage=circuit.simulate_columns(encodings,target);dirty+=garbage
    for encoded,actual in zip(encodings,flags):
     p=encoded&((1<<d)-1);tau=encoded>>d;bound=reference(w,v,W,d,p)
     if name.endswith('dual') and bound is not None:
      chosen=[order[j] for j in range(d) if p>>j&1];rem=W-sum(w[i] for i in chosen);profit=sum(v[i] for i in chosen)
      bound=Fraction(profit)+lam*rem+sum(max(Fraction(v[i])-lam*w[i],0) for i in order[d:])
     expected=target^int(bound is None or bound<tau)
     if actual!=expected:mismatch.append({'encoding':encoded,'target':target,'expected':expected,'actual':actual,'bound':str(bound)})
   out['predicate_cases'].append({'input':[w,v,W],'depth':d,'method':name,'columns':2*len(encodings),
      'predicate_mismatches':mismatch,'dirty_columns':dirty,'resources':circuit.resources()})
 print('finished',w,v,W,flush=True)
out['source_unchanged']=out['source_sha256']==hashlib.sha256((ROOT/'simulation/pruning_study_20261023/compact_sensitivity.py').read_bytes()).hexdigest()
dest=HERE/'reviewer_compact_probe.json';dest.write_text(json.dumps(out,indent=2),encoding='utf-8');print('Saved',dest,flush=True)
