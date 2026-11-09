"""Separate, append-only certificate/normalization controls, never runtime data."""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'simulation'))
from pruning_study_20261023.trees import cheap_certificate,bank_multipliers

def records(path):
    with path.open(encoding='utf8') as handle:
        for line in handle:
            if line.strip(): yield json.loads(line)

def main():
    sources=[('inputs.json','trees_full.jsonl'),
             ('inputs_core700.json','trees_core_v3.jsonl'),
             ('inputs_stress_independent.json','trees_independent_v2.jsonl')]
    output=HERE/'certificate_bank_controls.jsonl'
    seen={r['id'] for r in records(output)} if output.exists() else set()
    with output.open('a',encoding='utf8',buffering=1) as handle:
        for reg,trees in sources:
            index={r['id']:r for r in json.loads((HERE/reg).read_text(encoding='utf8'))['records']}
            if not (HERE/trees).exists(): continue
            for result in records(HERE/trees):
                if result['id'] in seen: continue
                row=index[result['id']]
                w,v,W=row['weights'],row['values'],row['capacity']
                out=dict(id=row['id'],category=row['category'],classification='DERIVED bounds; certificate host_seconds MEASURED',
                    thresholds=[],scope='Minimum of separate valid member certificates; not an exact count of the intersection')
                for threshold in result['thresholds']:
                    target=dict(target_kind=threshold['target_kind'],tau=threshold['tau'],banks={})
                    for q in [1,2,4]:
                        certs=[cheap_certificate(w,v,W,threshold['tau'],lam) for lam in bank_multipliers(w,v,W,q)]
                        best=min(c['bound'] for c in certs)
                        for method in (['root_dual','bank2','bank4','exact_lp'] if q==1 else ['bank2','bank4','exact_lp'] if q==2 else ['bank4','exact_lp']):
                            tree=threshold['trees'][method]
                            if tree['nodes']>best:
                                raise RuntimeError('RESEARCH_INTEGRITY_STOP: certificate below processed vertex lower bound')
                        target['banks'][str(q)]=dict(bound=best,member_certificates=certs,
                            distinct_members=len(certs),host_seconds=sum(c['computation_seconds'] for c in certs))
                    out['thresholds'].append(target)
                handle.write(json.dumps(out)+'\n');seen.add(row['id'])
    original=json.loads((HERE/'inputs.json').read_text(encoding='utf8'))
    index={r['id']:r for r in original['records']}
    controls=[]
    for row in original['records']:
        if row['category']!='highbit_scaled': continue
        gw=math.gcd(*row['weights']);gv=math.gcd(*row['values'])
        base=index[row['base_id']]
        bgw=math.gcd(*base['weights']);bgv=math.gcd(*base['values'])
        canonical=([x//gw for x in row['weights']],[x//gv for x in row['values']],row['capacity']//gw)
        canonical_base=([x//bgw for x in base['weights']],[x//bgv for x in base['values']],base['capacity']//bgw)
        if canonical!=canonical_base: raise RuntimeError('Normalization control failed')
        controls.append(dict(id=row['id'],base_id=base['id'],weight_gcd=gw,value_gcd=gv,
            normalized_arrays_equal_base=True,normalized_capacity=row['capacity']//gw,
            threshold_map='ceil(tau/value_gcd)',capacity_map='floor(capacity/weight_gcd)',
            classification='DERIVED exact integer normalization identity'))
    out=dict(cases=controls,mismatches=0,
        scope='Uniform scaling is an encoding control, not independently hard data; circuits can compile the identical normalized arrays',
        source_sha256=hashlib.sha256((HERE/'inputs.json').read_bytes()).hexdigest())
    path=HERE/'normalization_controls.json'
    if path.exists() and json.loads(path.read_text(encoding='utf8'))!=out: raise RuntimeError('Changed controls')
    if not path.exists(): path.write_text(json.dumps(out,indent=2),encoding='utf8')
    print('certificate rows',len(seen),'normalization cases',len(controls),'mismatches 0')

if __name__=='__main__': main()
