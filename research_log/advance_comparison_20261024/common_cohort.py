"""Read-only same-cohort model comparison; no competitor-speedup claim."""
from collections import Counter,defaultdict
import hashlib
import json
import math
from pathlib import Path
import statistics

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'pruning_study_20261023'
def read(path): return [json.loads(s) for s in path.read_text(encoding='utf8').splitlines() if s.strip()]
def desc(values):
    return dict(n=len(values),median=statistics.median(values),minimum=min(values),maximum=max(values),
                less_than_exact=sum(x<1-1e-12 for x in values),ties_exact=sum(abs(x-1)<=1e-12 for x in values)) if values else dict(n=0)
paths=[OLD/name for name in ['trees_full.jsonl','trees_core_v3.jsonl','trees_independent_v2.jsonl','trees_timecap_reruns.jsonl','core_resource_aliases.json']]
trees=sum([read(p) for p in paths[:3]],[]); index={r['id']:r for r in trees}
for row in read(paths[3]):
    target=next(t for t in index[row['id']]['thresholds'] if t['target_kind']==row['target_kind'])
    assert target['trees'][row['method']]==row['old_status']
    target['trees'][row['method']]=row['newtree']
aliases={r['core_id']:r['resource_id'] for r in json.loads(paths[4].read_text())['records']}
resources={}
for name in ['main_single_v1','core_changed_single_v1','independent_single_v1','scaled_single_v1']:
    path=OLD/'runs'/name/'resource_records.jsonl';paths.append(path)
    resources.update({(r['id'],r['method']):r for r in read(path)})
def resource(ident,method): return resources.get((aliases.get(ident,ident),'exact_single' if method=='exact_lp' else method))
cohorts={'dual_family':['root_dual','bank2','bank4','exact_lp'],
         'with_simple':['simple','root_dual','bank2','bank4','exact_lp']}
groups=defaultdict(list);coverage=defaultdict(Counter);conditions=[]
for tree in trees:
    for t in tree['thresholds']:
        for name,methods in cohorts.items():
            key=(tree['category'],t['target_kind'],name)
            resolved=all(a['status']=='complete' and not a['calls'] for a in tree['algorithms'].values())
            rr={m:resource(tree['id'],m) for m in methods}
            status=('classically_resolved' if resolved else
                    'resource_cap_or_missing' if any(not r or r['status']!='complete' for r in rr.values()) else
                    'tree_capped' if any(not t['trees'][m]['complete'] for m in methods) else
                    'all_root_rejected' if all(t['trees'][m]['nodes']==1 for m in methods) else 'included')
            coverage[key][status]+=1
            if status!='included': continue
            for metric in ['ccx','gates','gate_depth']:
                costs={m:(r['resources']['gate_counts']['ccx'] if metric=='ccx' else r['resources'][metric]) for m,r in rr.items()}
                for h in [0,.25,1,10,100]:
                    shared=h*costs['exact_lp']
                    model={m:(costs[m]+shared)*math.sqrt(t['trees'][m]['nodes']) for m in methods}
                    best=min(model.values());winners=[m for m in methods if abs(model[m]-best)<=1e-10*max(1,best)]
                    ratios={m:model[m]/model['exact_lp'] for m in methods}
                    row=dict(id=tree['id'],category=tree['category'],target_kind=t['target_kind'],cohort=name,
                        metric=metric,overhead=h,ratios=ratios,winners=winners,
                        classification='DERIVED conditional proxy; winner uses observed T, not a deployable selector')
                    conditions.append(row);groups[(*key,metric,h)].append(row)
summary=[]
for key,rows in sorted(groups.items()):
    summary.append(dict(category=key[0],target_kind=key[1],cohort=key[2],metric=key[3],overhead=key[4],
        conditions=len(rows),method_ratios={m:desc([r['ratios'][m] for r in rows]) for m in rows[0]['ratios']},
        unique_winners=dict(Counter(r['winners'][0] for r in rows if len(r['winners'])==1)),
        tied_winner_conditions=sum(len(r['winners'])>1 for r in rows)))
out=dict(scope='Same-cohort internal construction comparison; no third-party implementation benchmark or measured runtime',
    source_sha256={str(p.relative_to(HERE.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
    coverage=[dict(category=k[0],target_kind=k[1],cohort=k[2],**dict(v)) for k,v in sorted(coverage.items())],
    summary=summary)
(HERE/'common_cohort_results.json').write_text(json.dumps(out,indent=2),encoding='utf8')
with (HERE/'common_cohort_conditions.jsonl').open('w',encoding='utf8') as f:
    for row in conditions: f.write(json.dumps(row)+'\n')
print(json.dumps([r for r in summary if r['category']=='main700' and r['cohort']=='dual_family' and r['target_kind']=='incumbent_plus_one' and r['metric']=='ccx' and r['overhead'] in [0,1,10]],indent=2))
