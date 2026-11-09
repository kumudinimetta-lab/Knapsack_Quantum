"""Independent final matched-QFT resource and synthesis-number audit.

Plan: all 840 rows, both forms/policies, identical registry/interface/bank,
raw LP lineage, every manifest hash, every aggregate metric and dominance
count. Preserve depth regressions and keep resource-only scope explicit.
"""
from collections import Counter,defaultdict
import hashlib
import json
from pathlib import Path
import statistics
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
read=lambda p:[json.loads(x) for x in p.read_text().splitlines() if x.strip()]
rows=read(HERE/'qft_bank_full105_rows.jsonl')
manifest=json.loads((HERE/'qft_bank_full105_manifest.json').read_text())
summary=json.loads((HERE/'qft_bank_full105_summary.json').read_text())
analysis=json.loads((HERE/'qft_bank_full105_analysis.json').read_text())
registry_path=ROOT/'research_log/pruning_study_20261023/inputs.json'
registry={r['id']:r for r in json.loads(registry_path.read_text())['records']}
bank_path=HERE/'theory_banks_dp_free.jsonl';banks={r['id']:r for r in read(bank_path)}
old_path=HERE/'resource105_rows.jsonl';old={(r['source_id'],r['method']):r for r in read(old_path)}
fail=[];checks=[]
for p,wanted in manifest['source_sha256'].items():
    actual=hashlib.sha256((ROOT/p).read_bytes()).hexdigest();checks.append(dict(path=p,match=actual==wanted))
    if actual!=wanted:fail.append(['hash',p])
for p,key in [(registry_path,'input_registry_sha256'),(bank_path,'theory_bank_ledger_sha256'),(old_path,'reused_raw_LP_ledger_sha256')]:
    if hashlib.sha256(p.read_bytes()).hexdigest()!=manifest[key]:fail.append(['ledger hash',str(p)])
cohort=[r['id'] for r in registry.values() if r['category']=='main700' and r['seed']-1000*r['n'] in (0,1,2)]
if cohort!=manifest['cohort_ids'] or len(cohort)!=105:fail.append(['cohort'])
grouped=defaultdict(dict);seen=set()
methods=[f'qft_{family}_{policy}_{form}' for policy in ['direct','source_generic'] for family in ['lp','bank'] for form in ['raw','merged']]
for r in rows:
    ident,method=r['source_id'],r['method'];key=(ident,method)
    if key in seen:fail.append(['duplicate',key])
    seen.add(key);grouped[ident][method]=r;base=registry[ident]
    for name in ['weights','values','capacity','n','seed','instance_class']:
        if r[name]!=base[name]:fail.append(['array/domain',key,name])
    d=base['n']//2;tb=max(1,(sum(base['values'])+1).bit_length())
    if r['depth']!=d or r['num_inputs']!=d+tb or r['quantum_threshold_bits']!=tb:fail.append(['interface',key])
    if r['bank']!=banks[ident]['result']['bank'] or r['bank_size']!=len(r['bank']):fail.append(['bank',key])
    if r['classification']!='DERIVED' or r['scope']!='resource_only':fail.append(['metric taxonomy',key])
    if r['family']=='lp' and r['form']=='raw':
        earlier=old[(ident,f"qft_{r['policy']}_normalized")]
        if r['resources']!=earlier['resources']:fail.append(['raw resource lineage',key])
    if r['status']=='COMPLETED':
        resource=r['resources']
        if resource['common_basis']!=['u','cx'] or resource['optimization_level']!=0 or resource['connectivity']!='all_to_all':fail.append(['gate model',key])
if seen!={(ident,method) for ident in cohort for method in methods}:fail.append(['complete condition matrix'])
status=dict(Counter(r['status'] for r in rows))
if summary['status_counts']!=status or summary['inputs']!=len(grouped) or summary['rows']!=len(rows):fail.append(['summary counts'])
for ident,conditions in grouped.items():
    for policy in ['direct','source_generic']:
        for family in ['lp','bank']:
            raw=conditions[f'qft_{family}_{policy}_raw'];merged=conditions[f'qft_{family}_{policy}_merged']
            a,b=raw['resources'],merged['resources'];audit=merged['metadata']['inverse_cancellation']
            if a['qubits']!=b['qubits'] or b['common_depth']>a['common_depth']:fail.append(['cancellation geometry/depth',ident,family,policy])
            if audit['input_gates']!=sum(a['native_counts'].values()) or audit['output_gates']!=sum(b['native_counts'].values()):fail.append(['cancellation totals',ident,family,policy])
            for gate in set(a['native_counts'])|set(b['native_counts'])|set(audit['removed_gate_counts']):
                if a['native_counts'].get(gate,0)-b['native_counts'].get(gate,0)!=audit['removed_gate_counts'].get(gate,0):fail.append(['removed gate count',ident,family,policy,gate])

def cost(row,metric):
    return row['resources']['common_counts'].get(metric,0) if metric in ['u','cx'] else row['resources'][metric]
def verify_comparison(s,selected):
    by=defaultdict(dict)
    for r in selected:by[r['source_id']][r['method']]=r
    pairs=[];missing=[]
    for ident,conditions in by.items():
        a=conditions.get(s['numerator']);b=conditions.get(s['denominator'])
        if a and b and a['status']==b['status']=='COMPLETED':pairs.append((a,b))
        else:missing.append(ident)
    if s['paired']!=len(pairs) or s['incomplete_pair_ids']!=missing:fail.append(['comparison cohort',s['numerator'],s['denominator']])
    for metric,expected in s['metrics'].items():
        ratios=[cost(a,metric)/cost(b,metric) for a,b in pairs]
        actual=dict(median_ratio=statistics.median(ratios),min_ratio=min(ratios),max_ratio=max(ratios),
            lower=sum(cost(a,metric)<cost(b,metric) for a,b in pairs),
            tied=sum(cost(a,metric)==cost(b,metric) for a,b in pairs),
            higher=sum(cost(a,metric)>cost(b,metric) for a,b in pairs))
        if actual!=expected:fail.append(['comparison metric',s['numerator'],s['denominator'],metric])
    for field,reverse in [('numerator_weakly_dominates_all_four',False),('denominator_weakly_dominates_all_four',True)]:
        actual=sum(all(cost(b if reverse else a,m)<=cost(a if reverse else b,m) for m in s['metrics']) for a,b in pairs)
        if s[field]!=actual:fail.append(['dominance',s['numerator'],field])
for s in analysis['comparisons']:verify_comparison(s,rows)
for name,s in analysis['by_class'].items():verify_comparison(s,[r for r in rows if r['instance_class']==name])
if analysis['statuses']!=status or analysis['inputs']!=105 or analysis['rows']!=840:fail.append(['analysis overall counts'])
if analysis['bank_sizes']!={ident:conditions['qft_bank_direct_merged']['bank_size'] for ident,conditions in sorted(grouped.items())}:fail.append(['bank sizes'])

# Recompute numerical facts quoted in the root synthesis from their raw ledgers.
extended=json.loads((HERE/'compilation_extended_summary.json').read_text())
validation=dict(records=sum(r['records'] for r in extended['ledger'].values()),
    columns=sum(r['simulated_columns'] for r in extended['ledger'].values()),
    predicate_mismatches=sum(r['predicate_mismatches'] for r in extended['ledger'].values()),
    dirty_columns=sum(r['dirty_columns'] for r in extended['ledger'].values()))
if validation!=dict(records=7045,columns=10843350,predicate_mismatches=0,dirty_columns=0):fail.append(['synthesis validation totals',validation])
continuous={}
for panel in ['main','core']:
    raw=read(HERE/f'theory_banks_continuous_{panel}.jsonl')
    continuous[panel]=dict(strict_grid_improvements=sum(r['exact_density_grid_minimum'] is not None and r['result']['bank_size']<r['exact_density_grid_minimum'] for r in raw),
        preprocessing_seconds=sum(r['result']['preprocessing_seconds'] for r in raw),
        profit_dp_seconds=sum((r['comparison_profit_dp'] or {}).get('seconds',0) for r in raw))
    source=json.loads((HERE/f'theory_banks_continuous_{panel}_summary.json').read_text())
    if continuous[panel]['strict_grid_improvements']!=source['strict_density_grid_improvements'] or continuous[panel]['preprocessing_seconds']!=source['total_preprocessing_seconds'] or continuous[panel]['profit_dp_seconds']!=source['total_comparison_dp_seconds']:fail.append(['continuous synthesis stats',panel])
out=dict(scope='Final matched QFT reconstruction and synthesis consistency; not an external implementation speedup',
    classification='DERIVED independent exact ledger recomputation',rows=len(rows),inputs=len(grouped),status_counts=status,
    source_hash_checks=checks,comparisons_checked=len(analysis['comparisons'])+len(analysis['by_class']),
    synthesis_validation=validation,synthesis_continuous_stats=continuous,primary=analysis['comparisons'][0],failures=fail)
dest=HERE/'reviewer_qft_full105_audit.json'
if dest.exists():raise RuntimeError('Refuse overwrite')
dest.write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in out.items() if k not in ['source_hash_checks','primary']},indent=2))
if fail:raise RuntimeError('RESEARCH_INTEGRITY_STOP: matched source reconstruction audit failed')
