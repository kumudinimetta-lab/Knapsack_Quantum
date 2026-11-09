"""Independent exact-squared-key audit of certificate-only selector diagnostics."""
from collections import Counter,defaultdict
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import statistics

HERE=Path(__file__).resolve().parent;OLD=HERE.parent/'pruning_study_20261023'
def read(p):return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
final=json.loads((HERE/'certificate_selector_results.json').read_text(encoding='utf-8'))
fail=[]
def ck(test,detail):
 if not test:fail.append(detail)
for p,s in final['source_sha256'].items():ck(sha(Path(p))==s,['source_hash',p])
certs={r['id']:r for r in read(OLD/'certificate_bank_controls.jsonl')}
aliases={r['core_id']:r['resource_id'] for r in json.loads((OLD/'core_resource_aliases.json').read_text())['records']}
resources={}
for run in ['main_single_v1','core_changed_single_v1','independent_single_v1','scaled_single_v1']:
 for r in read(OLD/'runs'/run/'resource_records.jsonl'):resources[(r['id'],r['method'])]=r
methods=['root_dual','bank2','bank4','exact_lp'];saved=read(HERE/'certificate_selector_conditions.jsonl')
savedmap={(r['id'],r['target_kind'],r['metric'],r['overhead']):r for r in saved}
ck(len(savedmap)==len(saved),['duplicate_saved_keys'])
groups=defaultdict(list);checked=0
for row in read(HERE/'common_cohort_conditions.jsonl'):
 if row['cohort']!='dual_family':continue
 cert=next(r for r in certs[row['id']]['thresholds'] if r['target_kind']==row['target_kind'])
 B={m:cert['banks'][q]['bound'] for m,q in zip(methods,['1','2','4','4'])}
 C={}
 for m in methods:
  r=resources[(aliases.get(row['id'],row['id']),'exact_single' if m=='exact_lp' else m)]['resources']
  C[m]=r['gate_counts']['ccx'] if row['metric']=='ccx' else r[row['metric']]
 # Squaring positive keys removes floating sqrt and uses exact rational overhead.
 h=Fraction(str(row['overhead']))*C['exact_lp']
 keys={m:(Fraction(C[m])+h)**2*B[m] for m in methods}
 selected=min(methods,key=lambda m:keys[m]);actual=row['ratios'][selected]
 regret=actual/min(row['ratios'].values());key=(row['id'],row['target_kind'],row['metric'],row['overhead'])
 out=savedmap.pop(key,None);ck(out is not None,['missing_saved_key',key])
 if out:
  ck(out['selected']==selected,['selection',key,out['selected'],selected])
  ck(math.isclose(out['ratio_to_exact'],actual,rel_tol=1e-12,abs_tol=1e-12),['actual_ratio',key])
  ck(math.isclose(out['hindsight_regret'],regret,rel_tol=1e-12,abs_tol=1e-12),['regret',key])
  ck(out['four_member_reuse_host_seconds']==cert['banks']['4']['host_seconds'],['reuse_host_time_source',key])
  ck(out['recorded_certificate_host_seconds']==sum(cert['banks'][q]['host_seconds'] for q in ['1','2','4']),['recorded_host_time_source',key])
  groups[(row['category'],row['target_kind'],row['metric'],row['overhead'])].append(out)
  checked+=1
ck(not savedmap,['unexpected_saved_keys',len(savedmap)])
for out in final['summary']:
 key=(out['category'],out['target_kind'],out['metric'],out['overhead']);rr=groups.pop(key,[])
 ck(len(rr)==out['conditions'],['summary_count',key])
 ck(dict(Counter(r['selected'] for r in rr))==out['selected'],['summary_selected',key])
 if rr:
  expected={'median_ratio_to_exact':statistics.median(r['ratio_to_exact'] for r in rr),
       'median_hindsight_regret':statistics.median(r['hindsight_regret'] for r in rr),
       'maximum_hindsight_regret':max(r['hindsight_regret'] for r in rr),
       'less_than_exact':sum(r['ratio_to_exact']<1-1e-12 for r in rr)}
  for k,v in expected.items():ck(math.isclose(out[k],v,rel_tol=1e-12,abs_tol=1e-12),['summary_value',key,k])
ck(not groups,['missing_summary_groups',len(groups)])
headline=[r for r in final['summary'] if r['category']=='main700' and r['target_kind']=='incumbent_plus_one' and r['metric']=='ccx' and r['overhead'] in [0,1,10]]
result={'date':'2026-10-24','scope':'Exact squared certificate/cost key; observed T only evaluates selected outcome',
    'classification':'DERIVED read-only verification','condition_rows_checked':checked,
    'summary_groups_checked':len(final['summary']),'failure_count':len(fail),'failures':fail,'headline':headline,
    'accounting_limit':'Recorded bank1+bank2+bank4 timings are summed; prospective four-member reuse is separate; compilation/setup is excluded from quantum gate units',
    'source_hashes':{str(p.relative_to(HERE)):sha(p) for p in [HERE/'certificate_selector.py',HERE/'certificate_selector_results.json',HERE/'certificate_selector_conditions.jsonl']}}
(HERE/'reviewer_selector_audit_result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ['failures','headline','source_hashes']},indent=2));print(json.dumps(headline,indent=2))
if fail:print(json.dumps(fail[:8],indent=2));raise RuntimeError('RESEARCH_INTEGRITY_STOP: selector audit mismatch')
