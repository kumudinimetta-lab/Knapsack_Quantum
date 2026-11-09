"""Isolated bounded gate-list builds, paired by canonical immutable input ID."""
from __future__ import annotations
import argparse
import hashlib
import json
import multiprocessing as mp
from pathlib import Path
import sys
import time
import traceback

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MODULE = ROOT/'simulation/pruning_study_20261023/circuits.py'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def worker(record, method, expected_sha, limits, result_path):
    started = time.monotonic()
    result = {'id':record['id'], 'method':method, 'n':record['n'],
              'category':record.get('category'), 'instance_class':record.get('instance_class'),
              'seed':record.get('seed'), 'module_sha256':digest(MODULE),
              'metric_classification':{'resources':'DERIVED','host_seconds':'MEASURED','limits':'HARDCODED'}}
    try:
        if result['module_sha256'] != expected_sha:
            raise RuntimeError('Circuit source changed after manifest was recorded')
        sys.path.insert(0,str(ROOT/'simulation'))
        from pruning_study_20261023.circuits import BUILDERS, BuildBudget, CircuitBuildCap
        w,v,c = record['weights'],record['values'],record['capacity']
        if method == 'fixedpoint_wrapper':
            from oracle_h.node_bound_reversible import build_coherent_node_bound
            circuit=build_coherent_node_bound(w,v,c)
            # Legacy builder has no internal budget; parent enforces a hard process cap.
            if circuit.num_qubits>limits['max_qubits'] or len(circuit.gates)>limits['max_gates']:
                result.update(status='build_cap',reason='legacy_postbuild_size',
                              counters={'qubits':circuit.num_qubits,'gates':len(circuit.gates)})
            else:
                result.update(status='complete',resources=circuit.resources(),
                              metadata={'baseline':'preserved fixed-point coherent depth wrapper'})
        else:
            circuit=BUILDERS[method](w,v,c,budget=BuildBudget(**limits))
            result.update(status='complete',resources=circuit.resources(),metadata=circuit.metadata)
    except Exception as exc:
        if exc.__class__.__name__=='CircuitBuildCap':
            result.update(status='build_cap',reason=exc.reason,counters=exc.counters)
        else:
            result.update(status='error',error=repr(exc),traceback=traceback.format_exc())
    result['host_seconds']=time.monotonic()-started
    Path(result_path).write_text(json.dumps(result,ensure_ascii=True),encoding='utf-8')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--subset',choices=['pilot','main','representative','scaled','all'],default='pilot')
    parser.add_argument('--registry',default=str(HERE/'inputs.json'))
    parser.add_argument('--methods',default='simple,root_dual,bank2,bank4,exact_single,fixedpoint_single,exact_wrapper,fixedpoint_wrapper')
    parser.add_argument('--run-name',required=True)
    parser.add_argument('--workers',type=int,default=2)
    parser.add_argument('--max-gates',type=int,default=2000000)
    parser.add_argument('--max-qubits',type=int,default=150000)
    parser.add_argument('--build-seconds',type=float,default=60)
    parser.add_argument('--process-seconds',type=float,default=75)
    parser.add_argument('--limit',type=int)
    args=parser.parse_args()
    if not 1<=args.workers<=2:
        raise ValueError('One or two bounded workers are supported')
    run=HERE/'runs'/args.run_name
    run.mkdir(parents=True,exist_ok=True)
    registry_path=Path(args.registry)
    registry=json.loads(registry_path.read_text(encoding='utf-8'))
    records=registry['records']
    if args.subset=='pilot': records=[r for r in records if r.get('pilot')]
    elif args.subset=='main': records=[r for r in records if r['category']=='main700']
    elif args.subset=='representative': records=[r for r in records if r['category']=='main700' and r.get('trial',999)<3]
    elif args.subset=='scaled': records=[r for r in records if r['category']=='highbit_scaled']
    if args.limit is not None: records=records[:args.limit]
    methods=args.methods.split(',')
    limits={'max_qubits':args.max_qubits,'max_gates':args.max_gates,'max_seconds':args.build_seconds}
    manifest={'module_sha256':digest(MODULE),'registry_sha256':digest(registry_path),
              'dependency_sha256':{str(path.relative_to(ROOT)):digest(path) for path in
                  [ROOT/'simulation/oracle_h/node_bound_reversible.py',Path(__file__).resolve()]},
              'python_version':sys.version,
              'subset':args.subset,'ids':[r['id'] for r in records], 'methods':methods,
              'limits':limits,'process_seconds':args.process_seconds,'workers':args.workers,
              'classification':'HARDCODED predeclared resource build configuration',
              'scope':'Gate-list resources only; not hardware or full-walk execution'}
    manifest_path=run/'manifest.json'
    if manifest_path.exists():
        if json.loads(manifest_path.read_text())!=manifest: raise RuntimeError('Run manifest differs; choose a new run name')
    else: manifest_path.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    output=run/'resource_records.jsonl'
    done=set()
    if output.exists():
        for line in output.read_text(encoding='utf-8').splitlines():
            row=json.loads(line); done.add((row['id'],row['method']))
    jobs=[(r,m) for r in records for m in methods if (r['id'],m) not in done]
    total=len(records)*len(methods)
    context=mp.get_context('spawn')
    active=[]; cursor=0; last_print=0; errors=0
    with output.open('a',encoding='utf-8',buffering=1) as log:
        while cursor<len(jobs) or active:
            if digest(MODULE)!=manifest['module_sha256']:
                for process,*_ in active: process.terminate(); process.join()
                raise RuntimeError('Circuit source changed: stop rather than mix versions')
            if any(digest(ROOT/path)!=sha for path,sha in manifest['dependency_sha256'].items()):
                for process,*_ in active: process.terminate(); process.join()
                raise RuntimeError('Dependency source changed: stop rather than mix versions')
            while cursor<len(jobs) and len(active)<args.workers:
                record,method=jobs[cursor]; cursor+=1
                key=hashlib.sha256((record['id']+'|'+method).encode()).hexdigest()[:20]
                result_path=run/(key+'.json')
                process=context.Process(target=worker,args=(record,method,manifest['module_sha256'],limits,str(result_path)))
                process.start()
                active.append((process,record,method,time.monotonic(),result_path))
            remaining=[]
            for process,record,method,started,result_path in active:
                expired=time.monotonic()-started>args.process_seconds
                if process.is_alive() and not expired:
                    remaining.append((process,record,method,started,result_path));continue
                if expired and process.is_alive(): process.terminate()
                process.join()
                if result_path.exists(): row=json.loads(result_path.read_text(encoding='utf-8'))
                else:
                    row={'id':record['id'],'method':method,'n':record['n'],
                         'category':record.get('category'),'instance_class':record.get('instance_class'),
                         'module_sha256':manifest['module_sha256'],
                         'status':'process_time_cap' if expired else 'worker_failure',
                         'host_seconds':time.monotonic()-started,'exit_code':process.exitcode,
                         'limits':limits,'classification':'MEASURED build status'}
                log.write(json.dumps(row,ensure_ascii=True)+'\n')
                done.add((record['id'],method));errors+=row['status'] in ('error','worker_failure')
            active=remaining
            if time.monotonic()-last_print>10 or not active and cursor==len(jobs):
                print(json.dumps({'completed':len(done),'total':total,'active':len(active),'errors':errors}),flush=True)
                last_print=time.monotonic()
            if errors:
                for process,*_ in active: process.terminate();process.join()
                raise RuntimeError('Build error retained: stop for inspection')
            time.sleep(.04)
    print('saved',output,flush=True)

if __name__=='__main__': main()
