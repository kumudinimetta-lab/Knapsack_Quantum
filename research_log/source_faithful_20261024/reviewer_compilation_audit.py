"""Independent new-bank columns and complete compilation-summary recomputation.

Plan before running: use LP vertices on small adversarial/random data; propagate
both output bits at every encoded depth, including ignored suffix bits. Audit
all raw IDs/statuses, every hash and summary ratio/count, not selected wins.
"""
import ast
from collections import Counter,defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import statistics
import sys

ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT));sys.dont_write_bytecode=True
from simulation.source_faithful_20261024.rounding import build_tight_exact
from simulation.source_faithful_20261024.compressed_bank import build_compressed_bank,build_dp_free_bank
from simulation.pruning_study_20261023.circuits import build_dual_bank
HERE=Path(__file__).resolve().parent;OLD=HERE.parent/'pruning_study_20261023'
refpath=OLD/'reviewer_adversarial_probe.py'
fn=next(n for n in ast.parse(refpath.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='reference')
ns={'Fraction':Fraction};exec(compile(ast.Module(body=[fn],type_ignores=[]),str(refpath),'exec'),ns)
reference=ns['reference'];SEED=2026102414;rng=random.Random(SEED)
cases=[([],[],0),([1],[1],0),([1],[1],1),([3],[1],2),([2,4],[2,4],3),
       ([1,1],[1,1],1),([9,9],[1,1],10),([27,28,12],[1,9,5],34),
       ([2,3,5],[3,1,7],5),([9,1,3],[17,4,2],1),([1,3],[2,1],1<<16)]
for _ in range(24):
    n=rng.randrange(1,6);w=[rng.randrange(1,16) for _ in range(n)]
    v=[rng.randrange(1,21) for _ in range(n)];cases.append((w,v,rng.randrange(sum(w)+3)))
rows=[];failures=[]
for ci,(w,v,W) in enumerate(cases):
    banks={'dp_bank':build_compressed_bank(w,v,W),'dp_free_bank':build_dp_free_bank(w,v,W)}
    builders={'tight_exact':lambda:build_tight_exact(w,v,W)}
    for name,result in banks.items():
        builders[name]=lambda b=result['bank']:build_dual_bank(w,v,W,multipliers=[Fraction(*x) for x in b])
    n=len(w);db=max(1,n.bit_length());row=dict(weights=w,values=v,capacity=W,methods={})
    for name,builder in builders.items():
        c=builder();max_tau=(1<<c.threshold_bits)-1;inputs={}
        for d in range(1<<db):
            for prefix in range(1<<n):
                U=reference(w,v,W,d,prefix) if d<=n else None
                tau_set={0,max_tau,rng.randrange(max_tau+1)}
                if U is not None:
                    f=U.numerator//U.denominator;tau_set.update(t for t in [f-1,f,f+1,f+2] if 0<=t<=max_tau)
                for tau in tau_set:inputs[prefix|(d<<n)|(tau<<(n+db))]=int(U is None or U<tau)
        mismatch=dirty=0
        for target in (0,1):
            flags,garbage=c.simulate_columns(inputs.keys(),target);dirty+=garbage
            for encoded,flag in zip(inputs,flags):
                if flag!=(target^inputs[encoded]):
                    mismatch+=1
                    if len(failures)<6:failures.append(dict(case=ci,method=name,encoded=encoded,target=target))
        row['methods'][name]=dict(columns=2*len(inputs),mismatches=mismatch,dirty_columns=dirty)
    rows.append(row)

def read(path):return [json.loads(s) for s in path.read_text(encoding='utf8').splitlines() if s.strip()]
summary=json.loads((HERE/'compilation_summary.json').read_text());audit_failures=[];ledger={}
tables={}
for stem,expected in summary['ledger'].items():
    raw=read(HERE/(stem+'.jsonl'));ident_counts=Counter(r['id'] for r in raw)
    if len(raw)!=expected['records'] or any(v!=1 for v in ident_counts.values()):audit_failures.append(['duplicate/count',stem])
    table={r['id']:r for r in raw};tables[stem]=table
    actual=dict(records=len(raw),statuses=dict(Counter(r['status'] for r in raw)),
        simulated_columns=sum(r.get('check',{}).get('columns',0) for r in raw),
        predicate_mismatches=sum(r.get('check',{}).get('predicate_mismatches',0) for r in raw),
        dirty_columns=sum(r.get('check',{}).get('dirty_columns',0) for r in raw),
        module_hashes=dict(Counter(r.get('module_sha256','see source_hashes') for r in raw)))
    if actual!=expected:audit_failures.append(['ledger',stem,actual,expected])
    ledger[stem]=actual
hash_checks=[]
for name,expected in summary['source_sha256'].items():
    actual=hashlib.sha256(Path(name).read_bytes()).hexdigest();hash_checks.append(dict(path=name,match=actual==expected))
    if actual!=expected:audit_failures.append(['hash',name])

old={}
for folder in ['main_single_v1','core_changed_single_v1','independent_single_v1']:
    for r in read(OLD/'runs'/folder/'resource_records.jsonl'):
        if r['method']=='exact_single':old[r['id']]=r
aliases={r['core_id']:r['resource_id'] for r in json.loads((OLD/'core_resource_aliases.json').read_text())['records']}
groups=defaultdict(list);recomputed_pairs={};undefined=0
for panel in ['main','core']:
    for ident,upper in tables[f'rounding_{panel}700'].items():
        variants=dict(old_exact=old[aliases.get(ident,ident)],upper=upper,
            tight_exact=tables[f'tight_exact_{panel}700'][ident],
            dp_bank=tables[f'bank_circuits_{panel}'][ident],
            dp_free_bank=tables[f'bank_circuits_{panel}_dp_free'][ident])
        tight=variants['tight_exact']
        if any(upper[k]!=tight[k] for k in ['weights','values','capacity']):audit_failures.append(['array mismatch',ident])
        for metric in ['ccx','gates','gate_depth','qubits']:
            costs={name:(r['resources']['gate_counts']['ccx'] if metric=='ccx' else r['resources'][metric])
                   for name,r in variants.items() if r['status']=='complete'}
            baselines={k:costs[k] for k in ['old_exact','tight_exact']}
            baselines['best_scan']=min(costs[k] for k in ['old_exact','upper','tight_exact'])
            category=variants['dp_bank']['instance_class']
            for name,value in costs.items():
                for baseline,b in baselines.items():
                    ratio=float(Fraction(value,b)) if b else (1.0 if value==0 else None)
                    undefined+=ratio is None
                    recomputed_pairs[(ident,panel,name,baseline,metric)]=ratio
                    groups[(panel,name,baseline,metric,'ALL')].append(ratio)
                    groups[(panel,name,baseline,metric,category)].append(ratio)
pair_rows=read(HERE/'compilation_pairs.jsonl')
if len(pair_rows)!=len(recomputed_pairs):audit_failures.append(['pair count',len(pair_rows),len(recomputed_pairs)])
seen=set()
for r in pair_rows:
    key=tuple(r[k] for k in ['id','panel','method','baseline','metric'])
    if key in seen:audit_failures.append(['duplicate pair',key])
    seen.add(key)
    if r['ratio']!=recomputed_pairs.get(key):audit_failures.append(['pair ratio',key])
for s in summary['summary']:
    key=tuple(s[k] for k in ['panel','method','baseline','metric','group']);values=groups.pop(key)
    values=[x for x in values if x is not None]
    expected=dict(n=len(values))
    if values:expected.update(median=statistics.median(values),minimum=min(values),maximum=max(values),
        below_one=sum(x<1-1e-12 for x in values),equal_one=sum(abs(x-1)<1e-12 for x in values),above_one=sum(x>1+1e-12 for x in values))
    if any(s[k]!=v for k,v in expected.items()):audit_failures.append(['summary',key,expected,s])
if groups:audit_failures.append(['missing summary groups',len(groups)])
out=dict(seed=SEED,columns_classification='SIMULATED',resource_aggregation_classification='DERIVED',
    own_tiny_cases=rows,own_first_failures=failures,ledger=ledger,source_hash_checks=hash_checks,
    recomputed_pair_rows=len(pair_rows),summary_rows=len(summary['summary']),
    undefined_ratios=undefined,aggregation_failures=audit_failures,
    scope='Best scan is a separate per-instance per-metric minimum resource envelope, not a single simultaneous Pareto point.')
dest=HERE/'reviewer_compilation_audit.json'
if dest.exists():raise RuntimeError('Refuse overwrite')
dest.write_text(json.dumps(out,indent=2),encoding='utf8')
totals={name:{k:sum(r['methods'][name][k] for r in rows) for k in ['columns','mismatches','dirty_columns']} for name in ['tight_exact','dp_bank','dp_free_bank']}
print(json.dumps(dict(own=totals,pairs=len(pair_rows),summary_rows=len(summary['summary']),
    hashes=len(hash_checks),aggregation_failures=len(audit_failures),undefined_ratios=undefined),indent=2))
if failures or audit_failures or any(x['mismatches'] or x['dirty_columns'] for x in totals.values()):
    raise RuntimeError('RESEARCH_INTEGRITY_STOP: compilation review found conflict; raw retained')
