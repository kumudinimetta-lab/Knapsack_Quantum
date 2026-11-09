from pathlib import Path
import json,statistics,hashlib
p=Path(__file__).resolve().parents[2]/'research_log/claim_validation_20261025'
read=lambda n:json.loads((p/n).read_text())
lines=lambda n:[json.loads(s) for s in (p/n).read_text().splitlines()]
out={'scope':'Fresh aggregation of saved records, not new experiments','classification':'DERIVED'}
rows=lines('root_all_reachable_v2_rows.jsonl')
assert len(rows)==1400 and all(r['status']=='complete' and r['predicate_floor_mismatches']==0 for r in rows)
out['coverage']={}
for panel,count,states,comps in [('main',700,3148192,12592768),('core',700,2056264,8225056)]:
    rs=[r for r in rows if r['panel']==panel]
    actual=[len(rs),sum(r['reachable_states'] for r in rs),sum(r['bank_floor_comparisons'] for r in rs)]
    assert actual==[count,states,comps],(panel,actual)
    out['coverage'][panel]=actual
cores=json.loads((p.parent/'pruning_study_20261023/inputs_core700.json').read_text())['records']
assert sum(sum(r['weights'])<=r['capacity'] for r in cores)==23
assert sum(r['n']==0 for r in cores)==11
initial=read('circuit_vertex_adversarial.json');resume=read('circuit_vertex_adversarial_resume.json')
assert hashlib.sha256((p/'circuit_vertex_adversarial.json').read_bytes()).hexdigest()==resume['previous_raw_sha256']
qft=initial['qft_rows']+resume['qft_rows'];boolean=resume['boolean_rows']
assert len(qft)==24 and sum(r['result']['columns'] for r in qft)==1120
assert len(boolean)==7 and sum(r['result']['columns'] for r in boolean)==2216
assert all(r['result']['actual_gate_mismatches']==0 for r in qft+boolean)
assert sum(r['result']['bank_vs_vertex_LP_predicate_disagreements'] for r in qft)==8
assert all(r['result']['bank_vs_vertex_LP_predicate_disagreements']==0 for r in qft if r['certified'])
assert sum(r['result']['invalid_depth_columns'] for r in boolean)==548
assert sum(r['result']['logical_amplitudes'] for r in resume['native_superpositions'])==64
assert all(r['result']['failures']==0 for r in resume['native_superpositions'])
assert initial['superpositions'][0]['result']['failures']==1
assert abs(initial['superpositions'][0]['result']['maximum_amplitude_error']-.2154)<.00005
out['bank_checks']={'qft_columns':1120,'boolean_columns':2216,'gate_mismatches':0,'expected_insufficient_bank_disagreements':8,'retained_initialization_failures':1}
rr=read('root_aware_validation.json')['rows']
assert sum(r['columns'] for r in rr if r['engine']=='compact_exact')==104
qr=[r for r in rr if r['engine']=='qft']
assert len(qr)==8 and sum(r['check']['columns'] for r in qr)==208
assert all(r['check']['actual_gate_mismatches']==0 for r in qr)
assert all(r['mismatches']==r['dirty']==0 for r in rr if r['engine']=='compact_exact')
assert all(r['check']['failures']==0 and r['check']['logical_amplitudes']==16 for r in rr if r['engine']=='qft_coherent')
cross=read('final_crosscheck.json')['full_transpiler_checks']
assert len(cross)==4 and not any(r['discrepancy'] for r in cross)
out['control_checks']={'boolean_columns':104,'qft_columns':208,'coherent_amplitudes':16,'transpiler_conditions':4,'mismatches':0}
out['primal_checks']=read('theory_adversarial_audit_v2.json')['counts']
rows=lines('root_aware_resource105_rows.jsonl')
assert len(rows)==105 and all(r['status']=='complete' for r in rows)
out['resource_ratios']={}
for metric in ['allocated_qubits','active_qubits','cx','u','depth']:
    vals=[]
    for r in rows:
        a,b=r['bank_resources'],r['resources']
        if metric=='allocated_qubits':val=a['qubits']/b['qubits']
        elif metric=='active_qubits':val=r['bank_active_qubits']/r['interface_plus_touched_qubits']
        elif metric=='depth':val=a['common_depth']/b['common_depth']
        else:val=a['common_counts'][metric]/b['common_counts'][metric]
        vals.append(val)
    summary=dict(n=len(vals),median=statistics.median(vals),minimum=min(vals),maximum=max(vals),lower=sum(v<1 for v in vals),equal=sum(v==1 for v in vals),higher=sum(v>1 for v in vals))
    assert summary==read('root_aware_resource105_summary.json')['ratios'][metric]
    out['resource_ratios'][metric]=summary
out['dense_errors']={r['label']:r['statevector']['raw_maximum_amplitude_error'] for r in read('circuit_phase_triage.json')['rows'] if 'statevector' in r}
out['discrepancies']=0
(Path(__file__).parent/'SECTIONS_7_9_CHECKS.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
