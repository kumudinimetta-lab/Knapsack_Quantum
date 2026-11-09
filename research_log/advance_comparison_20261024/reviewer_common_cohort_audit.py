"""Independent common-cohort membership, ratio and winner check; old outputs read-only."""
from collections import Counter,defaultdict
import hashlib
import json
import math
from pathlib import Path
import statistics

HERE=Path(__file__).resolve().parent;OLD=HERE.parent/'pruning_study_20261023'
def read(p):return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
final=json.loads((HERE/'common_cohort_results.json').read_text(encoding='utf-8'))
fail=[]
def ck(x,msg):
 if not x:fail.append(msg)
for p,s in final['source_sha256'].items():ck(sha(HERE.parent/p)==s,['source',p])
trees=sum([read(OLD/p) for p in ['trees_full.jsonl','trees_core_v3.jsonl','trees_independent_v2.jsonl']],[])
index={r['id']:r for r in trees}
for o in read(OLD/'trees_timecap_reruns.jsonl'):
 t=next(t for t in index[o['id']]['thresholds'] if t['target_kind']==o['target_kind'])
 ck(t['trees'][o['method']]==o['old_status'] and t['tau']==o['tau'] and not o['conflict'],['overlay',o['key']])
 t['trees'][o['method']]=o['newtree']
aliases={r['core_id']:r['resource_id'] for r in json.loads((OLD/'core_resource_aliases.json').read_text())['records']}
resources={}
for run in ['main_single_v1','core_changed_single_v1','independent_single_v1','scaled_single_v1']:
 for r in read(OLD/'runs'/run/'resource_records.jsonl'):resources[(r['id'],r['method'])]=r
saved=read(HERE/'common_cohort_conditions.jsonl')
savedmap={(r['id'],r['target_kind'],r['cohort'],r['metric'],r['overhead']):r for r in saved}
ck(len(savedmap)==len(saved),['duplicate_condition_rows'])
cohorts={'dual_family':['root_dual','bank2','bank4','exact_lp'],'with_simple':['simple','root_dual','bank2','bank4','exact_lp']}
coverage=defaultdict(Counter);groups=defaultdict(list);checked=0
for tree in trees:
 for target in tree['thresholds']:
  for cname,methods in cohorts.items():
   rr={m:resources.get((aliases.get(tree['id'],tree['id']),'exact_single' if m=='exact_lp' else m)) for m in methods}
   resolved=all(a['status']=='complete' and not a['calls'] for a in tree['algorithms'].values())
   status='included'
   if resolved:status='classically_resolved'
   elif any(r is None or r['status']!='complete' for r in rr.values()):status='resource_cap_or_missing'
   elif any(not target['trees'][m]['complete'] for m in methods):status='tree_capped'
   elif all(target['trees'][m]['nodes']==1 for m in methods):status='all_root_rejected'
   coverage[(tree['category'],target['target_kind'],cname)][status]+=1
   if status!='included':continue
   for metric in ['ccx','gates','gate_depth']:
    costs={m:(r['resources']['gate_counts']['ccx'] if metric=='ccx' else r['resources'][metric]) for m,r in rr.items()}
    ce=costs['exact_lp'];te=target['trees']['exact_lp']['nodes']
    for h in [0,.25,1,10,100]:
     # Normalize before taking square roots, independently of the producer's model values.
     values={m:((costs[m]/ce+h)/(1+h))*math.sqrt(target['trees'][m]['nodes']/te) for m in methods}
     best=min(values.values());wins=[m for m in methods if abs(values[m]-best)<=1e-10*best]
     key=(tree['id'],target['target_kind'],cname,metric,h);s=savedmap.pop(key,None)
     ck(s is not None,['missing_condition',key])
     if s:
      ck(s['winners']==wins,['winner',key,s['winners'],wins])
      for m,v in values.items():ck(math.isclose(s['ratios'][m],v,rel_tol=1e-12,abs_tol=1e-12),['ratio',key,m,s['ratios'][m],v])
      groups[(tree['category'],target['target_kind'],cname,metric,h)].append({'winners':wins,'ratios':values})
      checked+=1
ck(not savedmap,['extra_saved_rows',len(savedmap)])
for row in final['coverage']:
 k=(row['category'],row['target_kind'],row['cohort']);expected=coverage.pop(k,{})
 ck({x:v for x,v in row.items() if x not in ['category','target_kind','cohort']}==dict(expected),['coverage',k])
ck(not coverage,['missing_coverage_groups',len(coverage)])
for row in final['summary']:
 k=(row['category'],row['target_kind'],row['cohort'],row['metric'],row['overhead']);rr=groups.pop(k,[])
 ck(row['conditions']==len(rr),['denominator',k])
 ck(row['unique_winners']==dict(Counter(r['winners'][0] for r in rr if len(r['winners'])==1)),['winner_counts',k])
 ck(row['tied_winner_conditions']==sum(len(r['winners'])>1 for r in rr),['tie_counts',k])
 for m,stats in row['method_ratios'].items():
  vv=[r['ratios'][m] for r in rr]
  expected={'n':len(vv),'median':statistics.median(vv),'minimum':min(vv),'maximum':max(vv),
            'less_than_exact':sum(x<1-1e-12 for x in vv),'ties_exact':sum(abs(x-1)<=1e-12 for x in vv)}
  for name,v in expected.items():ck(math.isclose(stats[name],v,rel_tol=1e-12,abs_tol=1e-12),['summary_stats',k,m,name])
ck(not groups,['missing_summary_groups',len(groups)])
headlines=[r for r in final['summary'] if r['category']=='main700' and r['target_kind']=='incumbent_plus_one' and r['metric']=='ccx' and r['overhead'] in [0,1,10]]
out={'date':'2026-10-24','scope':'Independent common-cohort joins, observed-tree proxy ratios and hindsight winners',
     'classification':'DERIVED read-only ledger/model verification',
     'source_hashes':{str(p.relative_to(HERE)):sha(p) for p in [HERE/'common_cohort.py',HERE/'common_cohort_results.json',HERE/'common_cohort_conditions.jsonl']},
     'condition_rows_checked':checked,'summary_groups_checked':len(final['summary']),
     'coverage_groups_checked':len(final['coverage']),'failure_count':len(fail),'failures':fail,'headline_groups':headlines}
(HERE/'reviewer_common_cohort_audit_result.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k not in ['headline_groups','source_hashes','failures']},indent=2))
print(json.dumps([{k:v for k,v in r.items() if k in ['cohort','conditions','overhead','unique_winners','tied_winner_conditions']} for r in headlines],indent=2))
if fail:print(json.dumps(fail[:8],indent=2));raise RuntimeError('RESEARCH_INTEGRITY_STOP: common-cohort audit mismatch')
