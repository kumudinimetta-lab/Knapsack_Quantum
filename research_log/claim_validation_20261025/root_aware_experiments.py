"""Bounded stronger-baseline test. Sources/old raw data remain unchanged."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import statistics
import sys
import time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from research_log.claim_validation_20261025.root_aware_control import build_root_aware_control
from research_log.claim_validation_20261025.circuit_vertex_adversarial import fixture,expectation,basis_mps
from research_log.claim_validation_20261025.circuit_vertex_adversarial_resume import native_coherent_check
from simulation.source_faithful_20261024.qft_normal_form import normalized_qft_circuit
from simulation.source_faithful_20261024.resource_profile import primitive_skeletons,profile
from simulation.pruning_study_20261023.circuits import BuildBudget,CircuitBuildCap
OLD=ROOT/'research_log/source_faithful_20261024'
read=lambda p:[json.loads(s) for s in p.read_text().splitlines() if s.strip()]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def validate():
    dest=HERE/'root_aware_validation.json'
    assert not dest.exists()
    examples=[fixture('early_fraction_eliminated',[1,3],[2,1],2,0),
              fixture('all_fit_no_fraction',[1],[1],2,0),
              fixture('capacity_zero',[1],[1],0,1),
              fixture('complete_prefix',[2,3],[3,1],2,2)]
    rows=[]
    for f in examples:
        w,v,W,d=f['weights'],f['values'],f['capacity'],f['depth']
        compact=build_root_aware_control(w,v,W,d,engine='compact_exact')
        inputs=range(1<<compact.num_inputs)
        bad=dirty=columns=0
        for target in [0,1]:
            actual,nonzero=compact.simulate_columns(inputs,output_bit=target)
            dirty+=nonzero
            for encoded,flag in zip(inputs,actual):
                wanted,lp,_=expectation(f,d,encoded&((1<<d)-1),encoded>>d)
                assert wanted==lp
                bad+=flag!=(target^lp);columns+=1
        rows.append(dict(label=f['label'],engine='compact_exact',columns=columns,mismatches=bad,dirty=dirty))
        assert bad==dirty==0,'RESEARCH_INTEGRITY_STOP: root-aware compact control failed'
        raw=build_root_aware_control(w,v,W,d)
        for form,c in [('raw',raw),('cancelled',normalized_qft_circuit(raw))]:
            check=basis_mps(c,f)
            rows.append(dict(label=f['label'],engine='qft',form=form,check=check))
            dest.write_text(json.dumps(dict(rows=rows,status='RUNNING'),indent=2))
            assert check['status']=='COMPLETED' and check['actual_gate_mismatches']==check['bank_vs_vertex_LP_predicate_disagreements']==0, 'RESEARCH_INTEGRITY_STOP: root-aware QFT basis test failed'
        if f['label']=='early_fraction_eliminated':
            check=native_coherent_check(normalized_qft_circuit(raw),f)
            rows.append(dict(label=f['label'],engine='qft_coherent',check=check))
            assert check['failures']==0,'RESEARCH_INTEGRITY_STOP: root-aware coherent test failed'
        print('Validated',f['label'],flush=True)
    result=dict(status='PASS',rows=rows,source_sha256={p.name:sha(p) for p in [Path(__file__),HERE/'root_aware_control.py',HERE/'root_aware_control_derivation.md']},
                scope='Actual gate checks against independent LP vertices, basis and one primitive-unitary coherent control; no partial initialize')
    dest.write_text(json.dumps(result,indent=2))

def resources():
    dest=HERE/'root_aware_resource105_rows.jsonl';assert not dest.exists()
    assert json.loads((HERE/'root_aware_validation.json').read_text())['status']=='PASS'
    manifest=json.loads((OLD/'qft_bank_full105_manifest.json').read_text())
    registry={r['id']:r for r in json.loads((ROOT/'research_log/pruning_study_20261023/inputs.json').read_text())['records']}
    old={(r['source_id'],r['method']):r for r in read(OLD/'qft_bank_full105_rows.jsonl')}
    live={(r['source_id'],r['family']):r for r in read(HERE/'hardware_active_qubits.jsonl')}
    skeletons=primitive_skeletons();rows=[];started=time.perf_counter()
    with dest.open('x') as out:
        for number,ident in enumerate(manifest['cohort_ids']):
            r=registry[ident];row=dict(id=ident,n=r['n'],instance_class=r['instance_class'],depth=r['n']//2,classification='DERIVED logical resources only')
            try:
                c=normalized_qft_circuit(build_root_aware_control(r['weights'],r['values'],r['capacity'],r['n']//2,budget=BuildBudget(150000,2000000,60)))
                p=profile(c,skeletons,budget=BuildBudget(150000,2000000,60))
                alive=set(range(c.num_inputs))|{c.output}|{q for _,wires,_ in c.gates for q in wires}
                bank=old[(ident,'qft_bank_direct_merged')]['resources']
                row.update(status='complete',resources=p,interface_plus_touched_qubits=len(alive),root_split=c.metadata['root_split'],
                           eligible_fraction_positions=c.metadata['eligible_fraction_positions'],
                           bank_resources=bank,bank_active_qubits=live[(ident,'bank')]['interface_plus_touched_qubits'])
            except CircuitBuildCap as e:
                row.update(status='cap',reason=e.reason,counters=e.counters)
            rows.append(row);out.write(json.dumps(row)+'\n');out.flush()
            if (number+1)%15==0:print('Resources',number+1,dict(Counter(x['status'] for x in rows)),flush=True)
    summaries={}
    complete=[r for r in rows if r['status']=='complete']
    for metric in ['allocated_qubits','active_qubits','cx','u','depth']:
        values=[]
        for r in complete:
            p,b=r['resources'],r['bank_resources']
            if metric=='allocated_qubits':numerator,denominator=b['qubits'],p['qubits']
            elif metric=='active_qubits':numerator,denominator=r['bank_active_qubits'],r['interface_plus_touched_qubits']
            elif metric=='depth':numerator,denominator=b['common_depth'],p['common_depth']
            else:numerator,denominator=b['common_counts'][metric],p['common_counts'][metric]
            values.append(numerator/denominator)
        summaries[metric]=dict(n=len(values),median=statistics.median(values),minimum=min(values),maximum=max(values),lower=sum(x<1 for x in values),equal=sum(x==1 for x in values),higher=sum(x>1 for x in values))
    result=dict(classification='DERIVED same-function resources against stronger root-aware LP reconstruction; not released-R1 superiority',
                rows=len(rows),status_counts=dict(Counter(r['status'] for r in rows)),ratios=summaries,
                incomplete_ids=[r['id'] for r in rows if r['status']!='complete'],seconds_measured=time.perf_counter()-started,
                hashes={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),HERE/'root_aware_control.py',dest,OLD/'qft_bank_full105_rows.jsonl',HERE/'hardware_active_qubits.jsonl']})
    (HERE/'root_aware_resource105_summary.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

if __name__=='__main__':
    validate()
    resources()
