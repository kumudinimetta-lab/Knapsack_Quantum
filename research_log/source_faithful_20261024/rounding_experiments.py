"""Scoped exact gate propagation and stronger same-function resource control."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import sys
import time

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from simulation.source_faithful_20261024.rounding import build_upper_fixedpoint,build_tight_exact,constants
from simulation.pruning_study_20261023.circuits import BuildBudget,CircuitBuildCap
from research_log.pruning_study_20261023.circuit_validation import check_inputs,reference

def sampled(w,v,W):
    n=len(w);db=max(1,n.bit_length());tb=max(1,(sum(v)+1).bit_length())
    seed=2026102407;rng=random.Random(seed);maximum=(1<<tb)-1;encodings=set()
    for d in range(1<<db):
        for p in [0,(1<<n)-1]+[rng.randrange(1<<n) for _ in range(4)]:
            bound=reference(w,v,W,d,p,'exact_single')
            targets={0,maximum,rng.randrange(maximum+1)}
            if bound is not None:
                f=bound.numerator//bound.denominator
                targets.update(t for t in [f-1,f,f+1,f+2] if 0<=t<=maximum)
            for tau in targets:encodings.add(p|(d<<n)|(tau<<(n+db)))
    return sorted(encodings)

def scalar():
    checks=0;fail=[]
    for w in range(1,41):
        for v in range(1,31):
            spec=constants(w,v);k,q=spec['k'],spec['q']
            for r in range(w):
                for P in [0,7]:
                    U=P+Fraction(r*v,w);f=U.numerator//U.denominator
                    for tau in {0,f,max(0,f+1),f+2}:
                        checks+=1
                        if ((P<<k)+r*q < (tau<<k))!=(U<tau):fail.append([w,v,r,P,tau,spec])
    result=dict(checks=checks,mismatches=len(fail),first_failures=fail[:5],classification='DERIVED exact integer/rational comparison')
    (HERE/'rounding_scalar_results.json').write_text(json.dumps(result,indent=2))
    if fail:raise RuntimeError('RESEARCH_INTEGRITY_STOP: scalar rounding conflict')
    return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--main',action='store_true');parser.add_argument('--core',action='store_true');parser.add_argument('--exact',action='store_true');args=parser.parse_args()
    scalar()
    if args.main or args.core:
        source=ROOT/'research_log/pruning_study_20261023'/('inputs_core700.json' if args.core else 'inputs.json')
        cases=[r for r in json.loads(source.read_text())['records'] if r['category']==('core700' if args.core else 'main700')]
        filename='rounding_core700.jsonl' if args.core else 'rounding_main700.jsonl'
    else:
        data=[([],[],0),([1],[1],0),([1],[1],1),([3],[1],2),([3],[2],2),([2,3],[3,2],2),
              ([2,3,4,5],[3,4,5,8],8),([2,4,6],[3,6,9],6),([1,2],[3,2],0),([2,3],[2,3],5)]
        cases=[dict(id='rounding_tiny_'+str(i),weights=w,values=v,capacity=W) for i,(w,v,W) in enumerate(data)]
        filename='rounding_tiny.jsonl'
    if args.exact:filename=filename.replace('rounding_','tight_exact_')
    output=HERE/filename
    done={json.loads(s)['id'] for s in output.read_text().splitlines()} if output.exists() else set()
    budget=BuildBudget(max_qubits=150000,max_gates=2000000,max_seconds=60)
    with output.open('a',encoding='utf8',buffering=1) as log:
        for index,row in enumerate(cases):
            if row['id'] in done:continue
            started=time.monotonic();w,v,W=row['weights'],row['values'],row['capacity']
            out=dict(id=row['id'],weights=w,values=v,capacity=W,
                module_sha256=hashlib.sha256((ROOT/'simulation/source_faithful_20261024/rounding.py').read_bytes()).hexdigest())
            try:
                circuit=(build_tight_exact if args.exact else build_upper_fixedpoint)(w,v,W,budget=budget)
                inputs=sampled(w,v,W) if args.main or args.core else range(1<<circuit.num_inputs)
                check=check_inputs(circuit,w,v,W,'exact_single',inputs)
                out.update(status='complete',check=check,resources=circuit.resources(),metadata=circuit.metadata,
                    inputs=list(inputs) if args.main or args.core else 'range(0,2**num_inputs)',seed=2026102407,
                    scope='Selected prefixes/thresholds at every encoded depth; both targets' if args.main or args.core else 'Exhaustive clean input/target domain')
            except CircuitBuildCap as exc:out.update(status='build_cap',reason=exc.reason,counters=exc.counters)
            except Exception as exc:
                out.update(status='error',error=repr(exc));log.write(json.dumps(out)+'\n');raise
            out['host_seconds']=time.monotonic()-started;log.write(json.dumps(out)+'\n')
            if out.get('check',{}).get('predicate_mismatches',0) or out.get('check',{}).get('dirty_columns',0):
                raise RuntimeError('RESEARCH_INTEGRITY_STOP: gate output/cleanup conflict')
            if index%50==0:print(json.dumps(dict(completed=index+1,total=len(cases),id=row['id'])),flush=True)
    print('finished',output,flush=True)

if __name__=='__main__':main()
