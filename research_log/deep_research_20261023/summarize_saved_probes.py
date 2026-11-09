"""Summarize immutable saved feasibility outputs; never rerun or patch raw data."""
from collections import defaultdict
from pathlib import Path
import hashlib
import json
import statistics

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

def read(name):
    return json.loads((HERE / name).read_text(encoding='utf-8'))

circuits = read('circuit_feasibility_probe_results.json')
theory = read('theory_probe_results.json')
banks = read('theory_bank_probe_results.json')
hardware = read('hardware_compile_pilot.json')
methods = list(circuits['small'][0]['circuits'])
verifications = {}
for name in methods:
    checks = [row['circuits'][name]['verification'] for row in circuits['small']]
    verifications[name] = {
        'classification':'SIMULATED', 'instances':len(checks),
        'columns':sum(x['columns'] for x in checks),
        'predicate_mismatches':sum(x['predicate_mismatches'] for x in checks),
        'dirty_columns':sum(x['dirty_columns'] for x in checks),
    }

rows = theory['rows']
caps = {method:sum(row['trees'][method]['capped'] for row in rows)
        for method in ('simple','dual','lp')}
ratios = defaultdict(list)
for row in rows:
    if not row['trees']['dual']['capped'] and not row['trees']['lp']['capped']:
        ratios[row['instance_class']].append(row['trees']['dual']['nodes'] / row['trees']['lp']['nodes'])
bank_summary = {}
for name in ('1','2','4'):
    eligible = [row for row in banks['rows']
                if not row['trees']['1']['capped'] and not row['trees'][name]['capped']]
    improvements = [row['trees']['1']['nodes'] / row['trees'][name]['nodes'] for row in eligible]
    bank_summary[name] = {
        'all_rows':len(banks['rows']),
        'caps':sum(row['trees'][name]['capped'] for row in banks['rows']),
        'completed_pairs_vs_one':len(eligible),
        'median_node_reduction_factor':statistics.median(improvements),
        'maximum_node_reduction_factor':max(improvements),
        'strictly_smaller_completed_pairs':sum(x>1 for x in improvements),
        'actual_distinct_multiplier_counts':sorted({len(row['trees'][name]['multipliers']) for row in banks['rows']}),
    }
compiled = [result for row in hardware['instances'] for result in row['one_iteration_resources']]
hw_resources = {}
for topology in ('all_to_all','path'):
    values = [x['two_qubit_gates'] for x in compiled if x['topology']==topology]
    hw_resources[topology] = {'minimum_two_qubit_gates':min(values),'maximum_two_qubit_gates':max(values)}
report = {
    'classification':'DERIVED summary of separately classified saved outputs',
    'scope':'Feasibility probes only. No full quantum walk, hardware job, runtime advantage or established novelty.',
    'circuit_checks':verifications,
    'first_circuit_instance':{k:v for k,v in circuits['small'][0].items() if k!='circuits'},
    'first_instance_resources':{name:circuits['small'][0]['circuits'][name]['resources'] for name in methods},
    'resource_only_cases':len(circuits['resource_only']),
    'exact_falsification':theory['falsification'],
    'tree_rows':len(rows), 'tree_caps':caps,
    'cheap_certificate_improves_full_binary_bound':sum(row['cheap_certificate']<row['full_binary_bound'] for row in rows),
    'root_rejected_rows':sum(row['trees']['lp']['nodes']==1 for row in rows),
    'completed_dual_lp_node_ratios':{key:{'count':len(values),'median':statistics.median(values),'maximum':max(values)} for key,values in ratios.items()},
    'dual_bank_tree_only':bank_summary,
    'hardware_compiler_version':hardware['qiskit_version'],
    'hardware_literal_input_count':len(hardware['instances']),
    'hardware_compilation_failures':hardware['failures'],
    'hardware_compiler_resources':hw_resources,
    'hardware_zero_fixing_inputs':sum(len(x['core'])==len(x['input']['weights']) for x in hardware['instances']),
    'hardware_empty_core_inputs':sum(len(x['core'])==0 for x in hardware['instances']),
    'hardware_marked_set_checks':sum(x['equivalence_checked_thresholds'] for x in hardware['instances']),
    'hardware_marked_set_mismatches':sum(len(x['equivalence_mismatches']) for x in hardware['instances']),
    'hardware_greedy_threshold_has_suboptimal_marked':sum(x['diagnostics'][0]['marked_nonoptimal_count']>0 for x in hardware['instances']),
    'raw_probe_sha256':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in
                       ('circuit_feasibility_probe_results.json','theory_probe_results.json','theory_bank_probe_results.json','hardware_compile_pilot.json')},
    'paper_sha256':{name:hashlib.sha256((ROOT/'paper'/name).read_bytes()).hexdigest() for name in ('main.tex','references.bib','main.pdf')},
}
(HERE/'SAVED_PROBE_SUMMARY.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('first_instance_resources','raw_probe_sha256','paper_sha256')},indent=2))
