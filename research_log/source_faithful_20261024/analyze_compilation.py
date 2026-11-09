"""Same-function gate resource comparisons, with every cap/empty case retained."""
from collections import Counter,defaultdict
import hashlib
import json
from pathlib import Path
import statistics

HERE=Path(__file__).resolve().parent;OLD=HERE.parent/'pruning_study_20261023'
def read(p):return [json.loads(s) for s in p.read_text(encoding='utf8').splitlines() if s.strip()]
def cost(r,m):return r['resources']['gate_counts']['ccx'] if m=='ccx' else r['resources'][m]
def ratio(a,b):return a/b if b else 1 if not a else None
def desc(v):
    v=[x for x in v if x is not None]
    return dict(n=len(v),median=statistics.median(v),minimum=min(v),maximum=max(v),
        below_one=sum(x<1-1e-12 for x in v),equal_one=sum(abs(x-1)<1e-12 for x in v),above_one=sum(x>1+1e-12 for x in v)) if v else dict(n=0)

paths=[HERE/'rounding_main700.jsonl',HERE/'rounding_core700.jsonl',HERE/'tight_exact_main700.jsonl',HERE/'tight_exact_core700.jsonl',
       HERE/'bank_circuits_main.jsonl',HERE/'bank_circuits_core.jsonl',HERE/'bank_circuits_main_dp_free.jsonl',HERE/'bank_circuits_core_dp_free.jsonl',HERE/'bank_circuits_independent_dp_free.jsonl']
tables={p.stem:{r['id']:r for r in read(p)} for p in paths}
ledger={}
for p in paths:
    rows=list(tables[p.stem].values());expected=45 if 'independent' in p.stem else 700
    assert len(rows)==expected,(p,len(rows))
    ledger[p.stem]=dict(records=len(rows),statuses=dict(Counter(r['status'] for r in rows)),
        simulated_columns=sum(r.get('check',{}).get('columns',0) for r in rows),
        predicate_mismatches=sum(r.get('check',{}).get('predicate_mismatches',0) for r in rows),
        dirty_columns=sum(r.get('check',{}).get('dirty_columns',0) for r in rows),
        module_hashes=dict(Counter(r.get('module_sha256','see source_hashes') for r in rows)))
    assert not ledger[p.stem]['predicate_mismatches'] and not ledger[p.stem]['dirty_columns']
old={}
for folder in ['main_single_v1','core_changed_single_v1','independent_single_v1']:
    p=OLD/'runs'/folder/'resource_records.jsonl';paths.append(p)
    old.update({r['id']:r for r in read(p) if r['method']=='exact_single'})
alias_path=OLD/'core_resource_aliases.json';paths.append(alias_path)
alias={r['core_id']:r['resource_id'] for r in json.loads(alias_path.read_text())['records']}
stats=defaultdict(list);detail=[]
for panel in ['main','core']:
    for ident,up in tables[f'rounding_{panel}700'].items():
        variants=dict(old_exact=old[alias.get(ident,ident)],upper=up,tight_exact=tables[f'tight_exact_{panel}700'][ident],
            dp_bank=tables[f'bank_circuits_{panel}'][ident],dp_free_bank=tables[f'bank_circuits_{panel}_dp_free'][ident])
        for metric in ['ccx','gates','gate_depth','qubits']:
            completed={k:cost(r,metric) for k,r in variants.items() if r['status']=='complete'}
            best_scan=min(completed[k] for k in ['old_exact','upper','tight_exact'] if k in completed)
            for method,value in completed.items():
                for baseline,basecost in [('old_exact',completed['old_exact']),('tight_exact',completed['tight_exact']),('best_scan',best_scan)]:
                    value_ratio=ratio(value,basecost);stats[(panel,method,baseline,metric,'ALL')].append(value_ratio)
                    category=variants['dp_bank']['instance_class'];stats[(panel,method,baseline,metric,category)].append(value_ratio)
                    detail.append(dict(id=ident,panel=panel,method=method,baseline=baseline,metric=metric,ratio=value_ratio,
                        classification='DERIVED same integer-pruning predicate on same input; not physical runtime'))
result=dict(scope='Compiled clean predicate resources. Same integer-threshold pruning; no tree-size advice. Classical preprocessing/compilation is additional cost.',
    ledger=ledger,summary=[dict(panel=k[0],method=k[1],baseline=k[2],metric=k[3],group=k[4],**desc(v)) for k,v in sorted(stats.items())],
    source_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths+[Path(__file__)]})
(HERE/'compilation_summary.json').write_text(json.dumps(result,indent=2),encoding='utf8')
with (HERE/'compilation_pairs.jsonl').open('w',encoding='utf8') as f:
    for r in detail:f.write(json.dumps(r)+'\n')
print(json.dumps([r for r in result['summary'] if r['group']=='ALL' and r['baseline']=='best_scan' and r['method'] in ['dp_bank','dp_free_bank']],indent=2))
