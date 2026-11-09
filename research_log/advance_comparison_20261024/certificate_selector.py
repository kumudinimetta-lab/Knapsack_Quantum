"""Input/certificate-only choice, then separately evaluate observed-tree proxies."""
from collections import Counter,defaultdict
import hashlib
import json
import math
from pathlib import Path
import statistics

HERE=Path(__file__).resolve().parent;OLD=HERE.parent/'pruning_study_20261023'
def read(path):return [json.loads(s) for s in path.read_text(encoding='utf8').splitlines() if s.strip()]
cert_path=OLD/'certificate_bank_controls.jsonl'
certs={r['id']:r for r in read(cert_path)}
alias_path=OLD/'core_resource_aliases.json'
aliases={r['core_id']:r['resource_id'] for r in json.loads(alias_path.read_text())['records']}
resources={};sources=[cert_path,alias_path,HERE/'common_cohort_conditions.jsonl',Path(__file__).resolve()]
for name in ['main_single_v1','core_changed_single_v1','independent_single_v1','scaled_single_v1']:
    path=OLD/'runs'/name/'resource_records.jsonl';sources.append(path)
    resources.update({(r['id'],r['method']):r for r in read(path)})
methods=['root_dual','bank2','bank4','exact_lp'];groups=defaultdict(list);outputs=[]
for row in read(HERE/'common_cohort_conditions.jsonl'):
    if row['cohort']!='dual_family':continue
    cert=next(t for t in certs[row['id']]['thresholds'] if t['target_kind']==row['target_kind'])
    bounds={m:cert['banks'][q]['bound'] for m,q in zip(methods,['1','2','4','4'])}
    costs={}
    for m in methods:
        r=resources[aliases.get(row['id'],row['id']),'exact_single' if m=='exact_lp' else m]['resources']
        costs[m]=r['gate_counts']['ccx'] if row['metric']=='ccx' else r[row['metric']]
    overhead=row['overhead']*costs['exact_lp']
    chosen=min(methods,key=lambda m:(costs[m]+overhead)*math.sqrt(bounds[m]))
    actual=row['ratios'][chosen];best=min(row['ratios'].values())
    out=dict(id=row['id'],category=row['category'],target_kind=row['target_kind'],metric=row['metric'],
        overhead=row['overhead'],selected=chosen,ratio_to_exact=actual,hindsight_regret=actual/best,
        recorded_certificate_host_seconds=sum(c['host_seconds'] for c in cert['banks'].values()),
        four_member_reuse_host_seconds=cert['banks']['4']['host_seconds'],
        classification='DERIVED model; recorded certificate host time MEASURED; candidate compilation/setup excluded from quantum gate units')
    outputs.append(out);groups[row['category'],row['target_kind'],row['metric'],row['overhead']].append(out)
summary=[]
for key,rows in sorted(groups.items()):
    summary.append(dict(category=key[0],target_kind=key[1],metric=key[2],overhead=key[3],conditions=len(rows),
        selected=dict(Counter(r['selected'] for r in rows)),median_ratio_to_exact=statistics.median(r['ratio_to_exact'] for r in rows),
        less_than_exact=sum(r['ratio_to_exact']<1-1e-12 for r in rows),
        median_hindsight_regret=statistics.median(r['hindsight_regret'] for r in rows),
        maximum_hindsight_regret=max(r['hindsight_regret'] for r in rows)))
result=dict(scope='Certificate-only diagnostic; no novelty/guaranteed improvement or full quantum runtime claim',summary=summary,
    source_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources})
(HERE/'certificate_selector_results.json').write_text(json.dumps(result,indent=2),encoding='utf8')
with (HERE/'certificate_selector_conditions.jsonl').open('w',encoding='utf8') as f:
    for row in outputs:f.write(json.dumps(row)+'\n')
print(json.dumps([r for r in summary if r['category']=='main700' and r['target_kind']=='incumbent_plus_one' and r['metric']=='ccx' and r['overhead'] in [0,1,10]],indent=2))
