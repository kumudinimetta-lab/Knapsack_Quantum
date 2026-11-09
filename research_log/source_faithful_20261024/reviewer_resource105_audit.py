"""Audit the preserved UNMERGED 105-input source reconstruction ledger.

Plan: verify every raw condition, registry arrays, fixed-depth interface,
independently derived widths, recorded hashes and summary counts. These are
resource-only netlists; this audit does not turn them into simulated columns.
"""
from collections import Counter,defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import statistics
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
manifest=json.loads((HERE/'resource105_manifest.json').read_text())
summary=json.loads((HERE/'resource105_summary.json').read_text())
rows=[json.loads(x) for x in (HERE/'resource105_rows.jsonl').read_text().splitlines()]
regpath=ROOT/'research_log/pruning_study_20261023/inputs.json'
registry={r['id']:r for r in json.loads(regpath.read_text())['records']}
fail=[];hashes=[]
for p,wanted in manifest['source_sha256'].items():
    actual=hashlib.sha256((ROOT/p).read_bytes()).hexdigest();hashes.append(dict(path=p,match=actual==wanted))
    if actual!=wanted:fail.append(['source hash',p])
if hashlib.sha256(regpath.read_bytes()).hexdigest()!=manifest['input_registry_sha256']:fail.append(['registry hash'])
cohort=[r['id'] for r in registry.values() if r['category']=='main700' and r['seed']-1000*r['n'] in [0,1,2]]
if cohort!=manifest['cohort_ids']:fail.append(['cohort'])
seen=set();methods=manifest['methods'];grouped=defaultdict(dict)
for r in rows:
    key=(r['source_id'],r['method'])
    if key in seen:fail.append(['duplicate condition',key])
    seen.add(key);base=registry[r['source_id']]
    for field in ['weights','values','capacity','n','seed','instance_class']:
        if r[field]!=base[field]:fail.append(['registry field',key,field])
    w,v,W,n=base['weights'],base['values'],base['capacity'],base['n'];d=n//2
    tb=max(1,(sum(v)+1).bit_length())
    if r['depth']!=d or r['num_inputs']!=d+tb or r['quantum_threshold_bits']!=tb:fail.append(['interface',key])
    if r['method']!='compact_root_dual':
        if r['method'].endswith('_normalized'):
            bound=max((max(sum(v)*Fraction(vv,ww).denominator+W*Fraction(vv,ww).numerator,
                           ((1<<tb)-1)*Fraction(vv,ww).denominator) for ww,vv in zip(w,v)),default=(1<<tb)-1)
        else:
            bound=max(sum(v)*max(w,default=1)+W*max(v,default=1),((1<<tb)-1)*max(w,default=1))
        expected=[max(1,(W+sum(w)).bit_length()+1),max(1,sum(v).bit_length()+1),max(1,bound.bit_length()+1),tb]
        if r['shared_widths']!=expected:fail.append(['widths',key,expected,r['shared_widths']])
    if r['classification']!='DERIVED' or r['scope']!='resource_only':fail.append(['taxonomy',key])
    if r['status']=='COMPLETED':
        resource=r['resources']
        if resource['common_basis']!=['u','cx'] or resource['optimization_level']!=0 or resource['connectivity']!='all_to_all':fail.append(['basis model',key])
    grouped[r['source_id']][r['method']]=r
expected={(ident,method) for ident in manifest['cohort_ids'] for method in methods}
if seen!=expected:fail.append(['condition coverage',len(seen),len(expected)])
status=dict(Counter(r['status'] for r in rows));status={k:status.get(k,0) for k in ['COMPLETED','CAPPED','ERROR']}
if summary['inputs']!=len(cohort) or summary['method_rows']!=len(rows) or summary['status_counts']!=status:fail.append(['summary counts'])
ratios=defaultdict(list)
for ident,conditions in grouped.items():
    for stem in ['qft_direct','qft_source_generic','compact_exact']:
        normal=conditions[stem+'_normalized']['resources'];wide=conditions[stem+'_conservative']['resources']
        for metric in ['qubits','common_depth']:
            ratios[(stem,metric)].append(normal[metric]/wide[metric])
        ratios[(stem,'common_cx')].append(normal['common_counts']['cx']/wide['common_counts']['cx'])
out=dict(scope='Audit of historical unmerged source-primitive assembly, not optimized source artifact',
    classification='DERIVED raw-ledger consistency and ratios',rows=len(rows),unique_conditions=len(seen),
    unique_inputs=len(grouped),status_counts=status,source_hash_checks=hashes,failures=fail,
    normalized_over_conservative=[dict(method=k[0],metric=k[1],n=len(x),median=statistics.median(x)) for k,x in ratios.items()])
dest=HERE/'reviewer_resource105_audit.json'
if dest.exists():raise RuntimeError('Refuse overwrite')
dest.write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out,indent=2))
if fail:raise RuntimeError('RESEARCH_INTEGRITY_STOP: source105 ledger audit failed')
