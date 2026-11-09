"""Separate aggregation and full-transpiler check of the new root-aware control."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import statistics
import sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path.insert(0,str(ROOT))
from research_log.claim_validation_20261025.root_aware_control import build_root_aware_control
from simulation.source_faithful_20261024.qft_normal_form import normalized_qft_circuit
from simulation.source_faithful_20261024.resource_profile import primitive_skeletons,profile
rows=[json.loads(s) for s in (HERE/'root_aware_resource105_rows.jsonl').read_text().splitlines()]
summary=json.loads((HERE/'root_aware_resource105_summary.json').read_text())
assert len(rows)==len({r['id'] for r in rows})==105
assert all(r['status']=='complete' for r in rows)
recomputed={}
for metric in ['allocated_qubits','active_qubits','cx','u','depth']:
    values=[]
    for row in rows:
        bank,scan=row['bank_resources'],row['resources']
        if metric=='allocated_qubits':a,b=bank['qubits'],scan['qubits']
        elif metric=='active_qubits':a,b=row['bank_active_qubits'],row['interface_plus_touched_qubits']
        elif metric=='depth':a,b=bank['common_depth'],scan['common_depth']
        else:a,b=bank['common_counts'][metric],scan['common_counts'][metric]
        values.append(a/b)
    recomputed[metric]=dict(n=len(values),median=statistics.median(values),minimum=min(values),maximum=max(values),lower=sum(x<1 for x in values),equal=sum(x==1 for x in values),higher=sum(x>1 for x in values))
assert recomputed==summary['ratios']
profile_checks=[];skeletons=primitive_skeletons()
for w,v,W,d in [([1,3],[2,1],2,0),([1],[1],2,0)]:
    raw=build_root_aware_control(w,v,W,d)
    for form,c in [('raw',raw),('cancelled',normalized_qft_circuit(raw))]:
        actual=c.resources();derived=profile(c,skeletons)
        assert actual['common_counts']==derived['common_counts']
        assert actual['common_depth']==derived['common_depth']
        profile_checks.append(dict(weights=w,values=v,capacity=W,depth=d,form=form,
                                   actual_full_transpiler_counts=actual['common_counts'],actual_full_transpiler_depth=actual['common_depth'],discrepancy=False))
coverage=[json.loads(s) for s in (HERE/'root_all_reachable_v2_rows.jsonl').read_text().splitlines()]
assert len(coverage)==len({r['id'] for r in coverage})==1400
assert Counter(r['panel'] for r in coverage)=={'main':700,'core':700}
assert all(r['status']=='complete' and r['predicate_floor_mismatches']==0 for r in coverage)
aggregate=dict(reachable_states=sum(r['reachable_states'] for r in coverage),bank_floor_comparisons=sum(r['bank_floor_comparisons'] for r in coverage))
assert aggregate==dict(reachable_states=5204456,bank_floor_comparisons=20817824)
validation=json.loads((HERE/'root_aware_validation.json').read_text())
gate_totals=Counter()
for r in validation['rows']:
    if r['engine']=='compact_exact':
        assert r['mismatches']==r['dirty']==0;gate_totals['compact_columns']+=r['columns']
    else:
        check=r['check']
        if r['engine']=='qft':
            assert check['actual_gate_mismatches']==0;gate_totals['qft_basis_columns']+=check['columns']
        else:
            assert check['failures']==0;gate_totals['coherent_amplitudes']+=check['logical_amplitudes']
        gate_totals[r['engine']+'_conditions']+=1
result=dict(classification='DERIVED separate final aggregation and full-transpiler comparison',
            conflicts=0,resource_inputs=105,ratios=recomputed,coverage_aggregate=aggregate,
            root_aware_actual_gate_check_totals=dict(gate_totals),full_transpiler_checks=profile_checks,
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(HERE/'final_crosscheck.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
