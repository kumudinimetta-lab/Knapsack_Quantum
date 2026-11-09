"""Gate-level validation before the preregistered resource-only expansion."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from simulation.source_faithful_20261024.width_controls import build_exact_control, widths
from simulation.source_faithful_20261024.resource_profile import primitive_skeletons, profile
from simulation.source_faithful_20261024.qft_reconstruction import build_qft_exact
from simulation.pruning_study_20261023.compact_sensitivity import build_compact_exact, build_compact_root_dual
from research_log.source_faithful_20261024.pilot import run_full_mps, common_resources


def main():
    directory = Path(__file__).parent
    prior = json.loads((directory / 'pilot_results_mps_tensor.json').read_text(encoding='utf-8'))
    skeletons = primitive_skeletons()
    out = {'derivation': 'normalized_width_derivation_before_code.md', 'primitive_skeletons': skeletons,
           'prior_resource_checks': [], 'normalized_checks': [], 'failures': []}
    output = directory / 'normalized_width_validation.json'
    for row in prior['rows']:
        w, v, cap, d = row['weights'], row['values'], row['capacity'], row['depth']
        for name, previous in row['methods'].items():
            if name.startswith('qft'):
                c = build_qft_exact(w, v, cap, d, mcx_policy='direct' if name=='qft_direct' else 'source_generic')
            else:
                c = (build_compact_exact if name=='compact_exact' else build_compact_root_dual)(w, v, cap, d)
            current, reference = profile(c, skeletons), previous['resources']
            mismatch = current['common_counts'] != reference['common_counts'] or current['common_depth'] != reference['common_depth']
            out['prior_resource_checks'].append({'fixture': row['fixture'], 'method': name,
                                                  'count_or_depth_mismatch': mismatch})
    fixtures = [(r['weights'], r['values'], r['capacity'], r['depth']) for r in prior['rows']]
    fixtures += [([], [], 0, 0), ([2, 4], [2, 4], 3, 1)]
    for index, (w, v, cap, d) in enumerate(fixtures):
        if widths(w, v, cap)[2] > widths(w, v, cap, 'conservative')[2]:
            raise RuntimeError('Unexpected width increase')
        for engine in ('qft_direct', 'qft_source_generic', 'compact_exact'):
            c = build_exact_control(w, v, cap, d, engine=engine)
            profiled, full = profile(c, skeletons), common_resources(c.to_qiskit())
            mismatch = profiled['common_counts'] != full['common_counts'] or profiled['common_depth'] != full['common_depth']
            old = build_exact_control(w, v, cap, d, engine=engine, width_policy='conservative')
            pinned = (build_compact_exact(w, v, cap, d) if engine=='compact_exact' else
                      build_qft_exact(w, v, cap, d, mcx_policy='direct' if engine=='qft_direct' else 'source_generic'))
            native_mismatch = old.gates != pinned.gates or old.num_qubits != pinned.num_qubits
            check = run_full_mps(c, w, v, cap, d)
            record = {'fixture': index, 'weights': w, 'values': v, 'capacity': cap, 'depth': d,
                      'engine': engine, 'normalized_widths': widths(w, v, cap),
                      'conservative_widths': widths(w, v, cap, 'conservative'),
                      'resource_profile_count_or_depth_mismatch': mismatch,
                      'conservative_factory_native_netlist_mismatch': native_mismatch,
                      'resources': profiled, 'simulation': check}
            out['normalized_checks'].append(record)
            output.write_text(json.dumps(out, indent=2), encoding='utf-8')
            if mismatch or native_mismatch or check.get('predicate_or_cleanup_failures', 0) or check['status']!='COMPLETED':
                out['failures'].append(record)
                output.write_text(json.dumps(out, indent=2), encoding='utf-8')
                raise RuntimeError('RESEARCH_INTEGRITY_STOP: width/profile control failed')
            print(index, engine, 'zero_mismatches', check['columns'], flush=True)
    out['summary'] = {'classification': 'SIMULATED for circuits; DERIVED resource decomposition crosschecks',
                      'prior_resource_method_cases': len(out['prior_resource_checks']),
                      'normalized_resource_method_cases': len(out['normalized_checks']),
                      'resource_count_or_depth_mismatches': sum(r['count_or_depth_mismatch'] for r in out['prior_resource_checks']) + sum(r['resource_profile_count_or_depth_mismatch'] for r in out['normalized_checks']),
                      'conservative_factory_netlist_mismatches': sum(r['conservative_factory_native_netlist_mismatch'] for r in out['normalized_checks']),
                      'compiled_columns': sum(r['simulation']['columns'] for r in out['normalized_checks']),
                      'predicate_or_cleanup_failures': sum(r['simulation']['predicate_or_cleanup_failures'] for r in out['normalized_checks'])}
    output.write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(out['summary'], flush=True)


if __name__=='__main__':
    main()
