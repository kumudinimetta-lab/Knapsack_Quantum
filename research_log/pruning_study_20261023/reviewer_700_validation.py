"""Every main700 input, scoped every-depth sample simulation of compiled gates."""
from fractions import Fraction
import argparse
import hashlib
import json
from pathlib import Path
import random
import sys
import time

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from simulation.pruning_study_20261023 import circuits as c
HERE=Path(__file__).resolve().parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def refs(w,v,W,depth,prefix,order,lam):
    if depth>len(w):return None,None
    chosen=[order[j] for j in range(depth) if prefix>>j&1]
    rem=W-sum(w[i] for i in chosen)
    if rem<0:return None,None
    value=sum(v[i] for i in chosen)
    dual=Fraction(value)+lam*rem+sum(max(Fraction(v[i])-lam*w[i],0) for i in order[depth:])
    exact=Fraction(value)
    for i in order[depth:]:
        if w[i]<=rem:exact+=v[i];rem-=w[i]
        else:exact+=Fraction(rem*v[i],w[i]);break
    return exact,dual

def selected_inputs(row,seed):
    w,v,W=row['weights'],row['values'],row['capacity'];n=len(w)
    order=sorted(range(n),key=lambda i:Fraction(v[i],w[i]),reverse=True)
    rem=W;lam=Fraction(0)
    for i in order:
        if w[i]<=rem:rem-=w[i]
        else:lam=Fraction(v[i],w[i]);break
    db=max(1,n.bit_length());tb=max(1,(sum(v)+1).bit_length());limit=(1<<tb)-1
    rng=random.Random(seed);samples={};scopes={}
    for d in range(1<<db):
        prefixes={0,(1<<n)-1,rng.getrandbits(n)}
        for p in sorted(prefixes):
            exact,dual=refs(w,v,W,d,p,order,lam)
            thresholds={0,limit,rng.randrange(limit+1)}
            for bound in [exact,dual]:
                if bound is not None:
                    floor=bound.numerator//bound.denominator
                    thresholds.update(max(0,min(limit,t)) for t in [floor,floor+1])
            for tau in sorted(thresholds):
                encoding=p|(d<<n)|(tau<<(n+db))
                samples[encoding]={'exact':int(exact is None or exact<tau),
                                   'root_dual':int(dual is None or dual<tau)}
        scopes[d]=len(prefixes)
    return samples,{'order':order,'root_multiplier':[lam.numerator,lam.denominator],
                    'depth_register_bits':db,'threshold_bits':tb,
                    'depths':list(scopes),'selection_patterns_per_depth':scopes}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--mode',choices=['pilot','all'],required=True)
    args=parser.parse_args();registry=HERE/'inputs.json';data=json.loads(registry.read_text(encoding='utf-8'))
    records=[r for r in data['records'] if r['category']=='main700']
    if len(records)!=700:raise RuntimeError('RESEARCH_INTEGRITY_STOP: registry main700 count differs')
    if args.mode=='pilot':records=[next(r for r in records if r['n']==n) for n in [12,18,24]]
    sourcepaths=[Path(__file__).resolve(),ROOT/'simulation/pruning_study_20261023/circuits.py',
                 ROOT/'simulation/oracle_h/node_bound_reversible.py',registry]
    hashes={str(p.relative_to(ROOT)):sha(p) for p in sourcepaths}
    folder=HERE/('reviewer_700_'+args.mode);folder.mkdir(exist_ok=True)
    manifest={'source_sha256':hashes,'mode':args.mode,'ids':[r['id'] for r in records],
      'seed_base':2026102310,'methods':['exact_single','fixedpoint_single','root_dual'],
      'limits':{'max_qubits':150000,'max_gates':2000000,'max_seconds':60},
      'taxonomy':{'gate_outputs':'SIMULATED','resources_and_exact_references':'DERIVED','time_and_caps':'MEASURED','configs':'HARDCODED'},
      'python_version':sys.version,'scope':'Every listed input; every depth encoding; selected prefixes/thresholds; both target bits; clean workspace'}
    mp=folder/'manifest.json'
    if mp.exists() and json.loads(mp.read_text())!=manifest:raise RuntimeError('Source/config changed; choose a new audit version')
    if not mp.exists():mp.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    outputs=folder/'records.jsonl';done=set()
    if outputs.exists():
        for line in outputs.read_text().splitlines():
            row=json.loads(line);done.add((row['id'],row['method']))
    started=time.monotonic();completed=0
    budget=c.BuildBudget(**manifest['limits'])
    with outputs.open('a',encoding='utf-8',buffering=1) as handle:
      for idx,record in enumerate(records):
        if any(sha(ROOT/p)!=s for p,s in hashes.items()):raise RuntimeError('Audit source changed during execution')
        # Hash-derived per-input seed independent of record reordering or pilot subset.
        seed=manifest['seed_base']+int(hashlib.sha256(record['id'].encode()).hexdigest()[:8],16)
        samples,meta=selected_inputs(record,seed);encodings=sorted(samples)
        for method in manifest['methods']:
          if (record['id'],method) in done:continue
          before=time.monotonic();row={'id':record['id'],'method':method,'n':record['n'],'seed':seed,
            'input':{k:record[k] for k in ['weights','values','capacity']},'scope_metadata':meta,
            'encodings':encodings,'base_reference_flags':[samples[x]['root_dual' if method=='root_dual' else 'exact'] for x in encodings]}
          try:
            circuit=c.BUILDERS[method](record['weights'],record['values'],record['capacity'],budget=budget)
            mismatches=[];dirty=0;unsafe=0
            if method=='root_dual' and circuit.metadata['multipliers']!=[meta['root_multiplier']]:raise RuntimeError('Root multiplier disagreement')
            for target in [0,1]:
              flags,garbage=circuit.simulate_columns(encodings,target);dirty+=garbage
              for encoding,actual in zip(encodings,flags):
                expected=target^samples[encoding]['root_dual' if method=='root_dual' else 'exact']
                if actual!=expected:mismatches.append({'encoding':encoding,'target':target,'expected':expected,'actual':actual})
                unsafe+=bool((actual^target) and not samples[encoding]['exact'])
            row.update(status='complete',columns=2*len(encodings),predicate_mismatches=len(mismatches),
                       mismatch_details=mismatches,dirty_columns=dirty,unsafe_pruning=unsafe,
                       resources=circuit.resources(),circuit_metadata=circuit.metadata)
          except c.CircuitBuildCap as err:row.update(status='build_cap',reason=err.reason,counters=err.counters)
          except Exception as err:row.update(status='error',error=type(err).__name__+': '+str(err))
          row['host_seconds']=time.monotonic()-before;handle.write(json.dumps(row)+'\n');completed+=1
          if row['status']=='error' or row.get('predicate_mismatches',0) or row.get('dirty_columns',0) or row.get('unsafe_pruning',0):
            raise RuntimeError('RESEARCH_INTEGRITY_STOP: retained affected method/input validation failure')
        if idx%20==0 or idx+1==len(records):print(json.dumps({'input':idx+1,'total_inputs':len(records),'new_method_cases':completed,'elapsed_seconds':time.monotonic()-started}),flush=True)
    rows=[json.loads(line) for line in outputs.read_text(encoding='utf-8').splitlines() if line.strip()]
    summary={'scope':manifest['scope'],'input_count':len(records),'method_cases':len(rows),
      'methods':{m:{'complete_cases':sum(r['status']=='complete' for r in rows if r['method']==m),
                    'caps':sum(r['status']=='build_cap' for r in rows if r['method']==m),
                    'columns':sum(r.get('columns',0) for r in rows if r['method']==m),
                    'predicate_mismatches':sum(r.get('predicate_mismatches',0) for r in rows if r['method']==m),
                    'dirty_columns':sum(r.get('dirty_columns',0) for r in rows if r['method']==m),
                    'unsafe_pruning':sum(r.get('unsafe_pruning',0) for r in rows if r['method']==m)} for m in manifest['methods']},
      'source_unchanged':all(sha(ROOT/p)==s for p,s in hashes.items()),'records_sha256':sha(outputs)}
    (folder/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary,indent=2),flush=True)

if __name__=='__main__':main()
