"""Targeted fairness test: allocated versus actually touched workspace qubits.

Plan: rebuild the same predeclared 105 direct-policy LP/bank circuits, apply the
same exact cancellation, count gate-wire union while RETAINING every input and
output wire even if idle. Compare with old allocated counts. No gate/width
optimization, new resource claims, or old-file changes. Total 90-second soft
budget; every cap/unattempted input is retained explicitly if it triggers.
"""
from collections import Counter,defaultdict
import hashlib
import json
from pathlib import Path
import statistics
import sys
import time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path.insert(0,str(ROOT));sys.dont_write_bytecode=True
from simulation.source_faithful_20261024.qft_bank import build_qft_bank
from simulation.source_faithful_20261024.width_controls import build_exact_control
from simulation.source_faithful_20261024.qft_normal_form import normalized_qft_circuit
from simulation.pruning_study_20261023.circuits import BuildBudget,CircuitBuildCap
PHASE=ROOT/'research_log/source_faithful_20261024'
read=lambda p:[json.loads(x) for x in p.read_text().splitlines() if x.strip()]
manifest=json.loads((PHASE/'qft_bank_full105_manifest.json').read_text())
registry={r['id']:r for r in json.loads((ROOT/'research_log/pruning_study_20261023/inputs.json').read_text())['records']}
banks={r['id']:r['result']['bank'] for r in read(PHASE/'theory_banks_dp_free.jsonl')}
old={(r['source_id'],r['method']):r for r in read(PHASE/'qft_bank_full105_rows.jsonl')}
output=HERE/'hardware_active_qubits.jsonl'
if output.exists():raise RuntimeError('Refuse overwrite')
started=time.monotonic();rows=[];remaining=[];budget=BuildBudget(150000,2000000,60)
with output.open('x',encoding='utf8') as stream:
    for index,ident in enumerate(manifest['cohort_ids']):
        if time.monotonic()-started>90:
            remaining=manifest['cohort_ids'][index:];break
        r=registry[ident];w,v,W,d=r['weights'],r['values'],r['capacity'],r['n']//2
        for family in ['lp','bank']:
            begin=time.monotonic();row=dict(source_id=ident,family=family)
            try:
                raw=(build_exact_control(w,v,W,d,budget=budget) if family=='lp'
                     else build_qft_bank(w,v,W,d,banks[ident],budget=budget))
                circuit=normalized_qft_circuit(raw);pinned=old[(ident,f'qft_{family}_direct_merged')]
                counts=dict(Counter(g[0] for g in circuit.gates))
                if counts!=pinned['resources']['native_counts'] or circuit.num_qubits!=pinned['resources']['qubits']:
                    raise RuntimeError('RESEARCH_INTEGRITY_STOP: reconstructed native lineage differs')
                required=set(range(circuit.num_inputs))|{circuit.output}
                touched={wire for name,wires,angle in circuit.gates for wire in wires}
                alive=required|touched
                if any(q<0 or q>=circuit.num_qubits for q in alive):raise RuntimeError('RESEARCH_INTEGRITY_STOP: wire out of range')
                idle=set(range(circuit.num_qubits))-alive
                row.update(status='complete',allocated_qubits=circuit.num_qubits,
                    retained_interface_qubits=len(required),gate_touched_qubits=len(touched),
                    interface_plus_touched_qubits=len(alive),idle_workspace_qubits=len(idle),
                    idle_workspace_indices=sorted(idle),native_counts_match_frozen=True)
            except CircuitBuildCap as e:row.update(status='cap',reason=e.reason,counters=e.counters)
            except Exception as e:
                row.update(status='error',error=repr(e));stream.write(json.dumps(row)+'\n');stream.flush();raise
            row['host_seconds_measured']=time.monotonic()-begin;rows.append(row)
            stream.write(json.dumps(row)+'\n');stream.flush()
        if index in [0,4,24,49,74,104]:print(index+1,[{k:x[k] for k in ['family','allocated_qubits','interface_plus_touched_qubits','idle_workspace_qubits']} for x in rows[-2:]],flush=True)
grouped=defaultdict(dict)
for r in rows:grouped[r['source_id']][r['family']]=r
paired=[x for x in grouped.values() if set(x)=={'lp','bank'} and all(r['status']=='complete' for r in x.values())]
ratios={}
for metric in ['allocated_qubits','interface_plus_touched_qubits']:
    values=[x['bank'][metric]/x['lp'][metric] for x in paired]
    ratios[metric]=dict(n=len(values),median=statistics.median(values),minimum=min(values),maximum=max(values),
                       bank_lower=sum(x['bank'][metric]<x['lp'][metric] for x in paired))
summary=dict(classification='DERIVED qubits in reconstructed native netlists; not optimized minimum qubits',
    input_budget=105,soft_time_budget_seconds=90,attempted_rows=len(rows),status_counts=dict(Counter(r['status'] for r in rows)),
    paired_inputs=len(paired),unattempted_inputs=remaining,ratios=ratios,
    idle_workspace_by_family={family:dict(median=statistics.median(r['idle_workspace_qubits'] for r in rows if r['family']==family and r['status']=='complete'),
      maximum=max(r['idle_workspace_qubits'] for r in rows if r['family']==family and r['status']=='complete')) for family in ['lp','bank']},
    elapsed_seconds_measured=time.monotonic()-started,
    source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in manifest['source_sha256']})
(HERE/'hardware_active_qubits_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
