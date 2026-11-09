"""Predeclared limited time-cap escalation, same deterministic node budget.

All original raw rows are immutable. This is structural completion accounting,
not a machine-runtime experiment. Every original time cap remains in the ledger.
"""
import collections
import hashlib
import json
import sys
import time
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'simulation'))
from pruning_study_20261023.trees import enumerate_threshold_tree

SOURCES=['trees_full.jsonl','trees_core_v3.jsonl','trees_independent_v2.jsonl']
REGISTRIES=['inputs.json','inputs_core700.json','inputs_stress_independent.json']
OUT=HERE/'trees_timecap_reruns.jsonl'


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    inputs={}
    for name in REGISTRIES:
        for row in json.loads((HERE/name).read_text(encoding='utf8'))['records']:
            inputs[row['id']]=row
    original_hashes={name:sha(HERE/name) for name in SOURCES}
    code_hashes={str(path):sha(path) for path in [Path(__file__),ROOT/'simulation/pruning_study_20261023/trees.py']}
    conditions=[]
    for name in SOURCES:
        for line in (HERE/name).read_text(encoding='utf8').splitlines():
            row=json.loads(line)
            for target in row['thresholds']:
                for method,tree in target['trees'].items():
                    if tree.get('cap_reason')=='time_cap':
                        key='|'.join([row['id'],target['target_kind'],method])
                        conditions.append((key,name,row,target,method,tree))
    manifest=dict(reason='Initial soft time caps under concurrent builds materially censor structural comparisons. Rerun ALL such method/condition pairs; same 50000 node budget, time cap escalated from 0.4 to 5 seconds. Not runtime benchmarking.',
                  settings=dict(node_cap=50000,seconds_cap=5.0),source_hashes=original_hashes,
                  code_hashes=code_hashes,attempted=len(conditions),
                  by_panel=dict(collections.Counter(x[1] for x in conditions)))
    mp=HERE/'trees_timecap_reruns_before_manifest.json'
    if not mp.exists(): mp.write_text(json.dumps(manifest,indent=2))
    seen=set()
    if OUT.exists():
        seen={json.loads(line)['key'] for line in OUT.read_text().splitlines() if line.strip()}
    with OUT.open('a',encoding='utf8') as out:
        for num,(key,name,row,target,method,oldtree) in enumerate(conditions):
            if key in seen: continue
            case=inputs[row['id']]
            new=enumerate_threshold_tree(case['weights'],case['values'],case['capacity'],
                 target['tau'],method,node_cap=50000,seconds_cap=5.0)
            conflict=(new['complete'] and new['nodes']<oldtree['nodes']) or (oldtree['sat'] is True and new['sat'] is False)
            record=dict(key=key,id=row['id'],category=row['category'],source_file=name,
                target_kind=target['target_kind'],tau=target['tau'],method=method,
                old_status=oldtree, newtree=new,source_hashes=original_hashes,
                code_hashes=code_hashes,settings=manifest['settings'],conflict=conflict,
                taxonomy='MEASURED classical deterministic vertex counts; rerun host seconds diagnostic only')
            out.write(json.dumps(record)+'\n');out.flush()
            if conflict: raise RuntimeError('RESEARCH_INTEGRITY_STOP: rerun conflicts with retained initial processed prefix or decision')
            if num%25==0: print(num+1,'/',len(conditions),key,new['complete'],new['cap_reason'],flush=True)
    after={name:sha(HERE/name) for name in SOURCES}
    if after!=original_hashes: raise RuntimeError('RESEARCH_INTEGRITY_STOP: immutable source changed during rerun')
    records=[json.loads(x) for x in OUT.read_text().splitlines() if x.strip()]
    summary=dict(attempted=len(records),conflicts=sum(x['conflict'] for x in records),by_panel={})
    for panel in SOURCES:
        rr=[x for x in records if x['source_file']==panel]
        summary['by_panel'][panel]=dict(attempted=len(rr),completed=sum(x['newtree']['complete'] for x in rr),
            cap_reasons=dict(collections.Counter(x['newtree']['cap_reason'] for x in rr if x['newtree']['capped'])),
            methods={m:dict(attempted=sum(x['method']==m for x in rr),completed=sum(x['method']==m and x['newtree']['complete'] for x in rr)) for m in ['simple','root_dual','bank2','bank4','exact_lp']})
    (HERE/'trees_timecap_reruns_summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary),flush=True)


if __name__=='__main__': main()
