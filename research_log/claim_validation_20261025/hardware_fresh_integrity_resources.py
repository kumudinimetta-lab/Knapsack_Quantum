"""Fresh read-only checkpoint and numerical falsification pass.

Accept no existing reviewer result as proof. Rehash frozen current/archive
members, verify restored paper identity, and recompute all 700/core summary
resources and all 105 primary QFT ratios directly from raw ledgers. New outputs
only; old data, sources, derived summaries and checkpoint are never overwritten.
"""
from collections import Counter,defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import statistics
import zipfile

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
PHASE=ROOT/'research_log/source_faithful_20261024';OLD=ROOT/'research_log/pruning_study_20261023'
read=lambda p:[json.loads(s) for s in p.read_text().splitlines() if s.strip()]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
verification=json.loads((ROOT/'research_log/source_faithful_20261025_checkpoint_verification.json').read_text())
manifest=json.loads((PHASE/'CHECKPOINT_MANIFEST.json').read_text())
archive=ROOT/'research_log/source_faithful_20261025_checkpoint.zip'
out={'classification':'DERIVED consistency checks; exact byte/hash comparisons','conflicts':[]}
def conflict(*args):
    out['conflicts'].append(args)
    (HERE/'hardware_fresh_integrity_resources.json').write_text(json.dumps(out,indent=2))
    raise RuntimeError('RESEARCH_INTEGRITY_STOP: '+str(args))
if sha(archive)!=verification['sha256']:conflict('outer checkpoint hash')
frozen=manifest['files'];checked=0
with zipfile.ZipFile(archive) as z:
    if z.testzip() is not None:conflict('ZIP CRC')
    names=z.namelist()
    if len(set(names))!=len(names):conflict('duplicate ZIP member')
    expected={r['path'] for r in frozen}|{'research_log/source_faithful_20261024/CHECKPOINT_MANIFEST.json'}
    if set(names)!=expected:conflict('archive inventory')
    for r in frozen:
        current=ROOT/r['path'];stored=z.read(r['path'])
        if not current.is_file() or current.stat().st_size!=r['bytes'] or sha(current)!=r['sha256']:conflict('current frozen member',r['path'])
        if len(stored)!=r['bytes'] or hashlib.sha256(stored).hexdigest()!=r['sha256']:conflict('archive frozen member',r['path'])
        checked+=1
    if z.read('research_log/source_faithful_20261024/CHECKPOINT_MANIFEST.json')!=(PHASE/'CHECKPOINT_MANIFEST.json').read_bytes():conflict('manifest bytes')
paper={}
for name,wanted in manifest['paper_byte_identical_to_restored_backup'].items():
    p=ROOT/'paper'/name;b=ROOT/'paper/backups/2026-10-22_before_revision'/name
    if p.read_bytes()!=b.read_bytes() or sha(p)!=wanted:conflict('restored paper bytes',name)
    paper[name]=sha(p)
bib=len(re.findall(r'^\s*@\w+\s*\{',(ROOT/'paper/references.bib').read_text(),re.M))
if bib!=45:conflict('bibliography count',bib)
out['checkpoint']=dict(sha256=sha(archive),current_and_archive_members_checked=checked,crc='PASS',paper_hashes=paper,bibliography_entries=bib)

old={}
for folder in ['main_single_v1','core_changed_single_v1']:
    for r in read(OLD/'runs'/folder/'resource_records.jsonl'):
        if r['method']=='exact_single':old[r['id']]=r
aliases={r['core_id']:r['resource_id'] for r in json.loads((OLD/'core_resource_aliases.json').read_text())['records']}
summary=json.loads((PHASE/'compilation_extended_summary.json').read_text())
summap={(r['panel'],r['method'],r['baseline'],r['metric'],r['group']):r for r in summary['summary']}
raw_counts={};metrics=[]
for panel in ['main','core']:
    stems={'upper':f'rounding_{panel}700','tight_exact':f'tight_exact_{panel}700',
           'dp_bank':f'bank_circuits_{panel}','dp_free_bank':f'bank_circuits_{panel}_dp_free',
           'continuous_bank':f'bank_circuits_{panel}_continuous'}
    tables={}
    canonical=json.loads((OLD/('inputs.json' if panel=='main' else 'inputs_core700.json')).read_text())['records']
    canonical={r['id']:r for r in canonical if r['category']==('main700' if panel=='main' else 'core700')}
    for name,stem in stems.items():
        raw=read(PHASE/(stem+'.jsonl'))
        if len(raw)!=700 or len({r['id'] for r in raw})!=700:conflict('raw count/duplicates',stem)
        if any(r['status']!='complete' for r in raw):conflict('noncomplete condition',stem)
        if any(r['check']['predicate_mismatches'] or r['check']['dirty_columns'] for r in raw):conflict('raw correctness',stem)
        for r in raw:
            if r['resources']['gates']!=sum(r['resources']['gate_counts'].values()):conflict('native gate count sum',stem,r['id'])
        tables[name]={r['id']:r for r in raw}
        raw_counts[stem]=dict(records=len(raw),columns=sum(r['check']['columns'] for r in raw),predicate_mismatches=0,dirty_columns=0)
    groups=defaultdict(list)
    for ident in tables['upper']:
        base=canonical[ident]
        for name in ['upper','tight_exact']:
            if any(tables[name][ident][k]!=base[k] for k in ['weights','values','capacity']):conflict('canonical arrays',panel,name,ident)
        variants={name:table[ident] for name,table in tables.items()}
        variants['old_exact']=old[aliases.get(ident,ident)]
        for metric in ['ccx','gates','gate_depth','qubits']:
            value=lambda r:r['resources']['gate_counts']['ccx'] if metric=='ccx' else r['resources'][metric]
            costs={name:value(r) for name,r in variants.items()}
            baseline=min(costs[x] for x in ['old_exact','upper','tight_exact'])
            for name,a in costs.items():
                ratio=float(Fraction(a,baseline)) if baseline else (1. if not a else None)
                if ratio is None:conflict('undefined ratio',panel,name,metric,ident)
                groups[(name,metric)].append(ratio)
    for (name,metric),ratios in groups.items():
        actual=dict(n=len(ratios),median=statistics.median(ratios),minimum=min(ratios),maximum=max(ratios),
            below_one=sum(x<1-1e-12 for x in ratios),equal_one=sum(abs(x-1)<1e-12 for x in ratios),above_one=sum(x>1+1e-12 for x in ratios))
        expected=summap[(panel,name,'best_scan',metric,'ALL')]
        if any(actual[k]!=expected[k] for k in actual):conflict('same-function summary',panel,name,metric,actual,expected)
        metrics.append(dict(panel=panel,method=name,metric=metric,**actual))
out['same_function_raw_ledgers']=raw_counts;out['same_function_metrics']=metrics

rows=read(PHASE/'qft_bank_full105_rows.jsonl');counts=Counter((r['source_id'],r['method']) for r in rows)
if len(rows)!=840 or any(n!=1 for n in counts.values()):conflict('QFT unique matrix')
if any(r['status']!='COMPLETED' for r in rows):conflict('QFT noncomplete matrix')
grouped=defaultdict(dict)
for r in rows:grouped[r['source_id']][r['method']]=r
primary=[]
for metric in ['qubits','u','cx','common_depth']:
    ratios=[];lower=tied=higher=0
    for ident,conditions in grouped.items():
        a=conditions['qft_bank_direct_merged'];b=conditions['qft_lp_direct_merged']
        if any(a[k]!=b[k] for k in ['weights','values','capacity','depth','num_inputs','quantum_threshold_bits']):conflict('matched interface',ident)
        value=lambda r:r['resources']['common_counts'].get(metric,0) if metric in ['u','cx'] else r['resources'][metric]
        aa,bb=value(a),value(b);ratios.append(float(Fraction(aa,bb)))
        lower+=aa<bb;tied+=aa==bb;higher+=aa>bb
    primary.append(dict(metric=metric,n=len(ratios),median=statistics.median(ratios),minimum=min(ratios),maximum=max(ratios),lower=lower,tied=tied,higher=higher))
expected=json.loads((PHASE/'qft_bank_full105_analysis.json').read_text())['comparisons'][0]['metrics']
for r in primary:
    e=expected[r['metric']]
    if any(r[a]!=e[b] for a,b in [('median','median_ratio'),('minimum','min_ratio'),('maximum','max_ratio'),('lower','lower'),('tied','tied'),('higher','higher')]):conflict('105 primary summary',r)
out['QFT_primary']=primary;out['QFT_rows']=dict(attempted=840,complete=840,inputs=len(grouped))
out['conclusion']='No integrity or numerical conflict found. These checks establish frozen-byte and raw-ledger consistency, not physical performance or priority.'
dest=HERE/'hardware_fresh_integrity_resources.json'
if dest.exists():raise RuntimeError('Refuse overwrite of audit result')
dest.write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps({'checkpoint_members':checked,'same_function_summary_groups':len(metrics),'QFT_primary':primary,'conflicts':out['conflicts']},indent=2))
