"""Compile data-only exact-pruning banks; compare against exact LP outputs."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
import time

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from simulation.pruning_study_20261023.circuits import build_dual_bank,BuildBudget,CircuitBuildCap
from research_log.source_faithful_20261024.rounding_experiments import sampled
from research_log.pruning_study_20261023.circuit_validation import check_inputs

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--panel',choices=['main','core','independent'],required=True);parser.add_argument('--dp-free',action='store_true');parser.add_argument('--continuous',action='store_true');args=parser.parse_args()
    if args.dp_free and args.continuous:raise ValueError('Choose one construction')
    source=HERE/('theory_banks_dp_free.jsonl' if args.dp_free else f'theory_banks_continuous_{args.panel}.jsonl' if args.continuous else f'theory_banks_{args.panel}.jsonl')
    records=[json.loads(s) for s in source.read_text(encoding='utf8').splitlines()]
    registry=None
    if args.dp_free:
        records=[r for r in records if r['category']==dict(main='main700',core='core700',independent='independent_large')[args.panel]]
        registry=ROOT/'research_log/pruning_study_20261023'/dict(main='inputs.json',core='inputs_core700.json',independent='inputs_stress_independent.json')[args.panel]
        canonical={r['id']:r for r in json.loads(registry.read_text())['records']}
        records=[dict(r,**{k:canonical[r['id']][k] for k in ['weights','values','capacity']}) for r in records]
    output=HERE/f'bank_circuits_{args.panel}{"_dp_free" if args.dp_free else "_continuous" if args.continuous else ""}.jsonl'
    done={json.loads(s)['id'] for s in output.read_text().splitlines()} if output.exists() else set()
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    sources={str(p):sha(p) for p in [source,Path(__file__),ROOT/'simulation/pruning_study_20261023/circuits.py',ROOT/'simulation/oracle_h/node_bound_reversible.py']}
    if registry:sources[str(registry)]=sha(registry)
    budget=BuildBudget(max_qubits=150000,max_gates=2000000,max_seconds=60)
    with output.open('a',encoding='utf8',buffering=1) as log:
        for index,row in enumerate(records):
            if row['id'] in done:continue
            w,v,W=row['weights'],row['values'],row['capacity'];bank=row['result']['bank']
            out=dict(id=row['id'],category=row['category'],n=row['n'],instance_class=row['instance_class'],
                bank=bank,bank_size=len(bank),construction_status=row['result']['status'],source_hashes=sources)
            start=time.monotonic()
            try:
                circuit=build_dual_bank(w,v,W,q=len(bank),multipliers=[Fraction(a,b) for a,b in bank],budget=budget)
                inputs=sampled(w,v,W)
                check=check_inputs(circuit,w,v,W,'exact_single',inputs)
                out.update(status='complete',check=check,resources=circuit.resources(),metadata=circuit.metadata,
                    sampled_inputs=inputs,sampling_seed=2026102407,
                    scope='Same integer-threshold rejection as exact LP on selected encodings at every depth; initially clean workspace, both targets')
            except CircuitBuildCap as exc:out.update(status='build_cap',reason=exc.reason,counters=exc.counters)
            except Exception as exc:
                out.update(status='error',error=repr(exc));log.write(json.dumps(out)+'\n');raise
            out['host_seconds']=time.monotonic()-start;log.write(json.dumps(out)+'\n')
            if out.get('check',{}).get('predicate_mismatches',0) or out.get('check',{}).get('dirty_columns',0):
                raise RuntimeError('RESEARCH_INTEGRITY_STOP: compiled exact-pruning bank mismatch/cleanup')
            if index%50==0:print(json.dumps(dict(completed=index+1,total=len(records),panel=args.panel)),flush=True)
    print('finished',output,flush=True)

if __name__=='__main__':main()
