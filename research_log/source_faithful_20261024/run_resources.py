"""Predeclared 105-input fixed-depth resource-only comparison; all caps retained."""
import hashlib
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import qiskit
from simulation.source_faithful_20261024.width_controls import build_exact_control, widths
from simulation.source_faithful_20261024.resource_profile import primitive_skeletons, profile
from simulation.pruning_study_20261023.compact_sensitivity import build_compact_root_dual
from simulation.pruning_study_20261023.circuits import BuildBudget, CircuitBuildCap


def main():
    folder = Path(__file__).parent
    validation = json.loads((folder / 'normalized_width_validation.json').read_text(encoding='utf-8'))
    if validation['summary']['predicate_or_cleanup_failures'] or validation['summary']['resource_count_or_depth_mismatches'] or validation['summary']['conservative_factory_netlist_mismatches']:
        raise RuntimeError('Prerequisite validation failed')
    registry_path = ROOT / 'research_log/pruning_study_20261023/inputs.json'
    registry = json.loads(registry_path.read_text(encoding='utf-8'))['records']
    cohort = [r for r in registry if r['category']=='main700' and r['seed'] - 1000 * r['n'] in (0, 1, 2)]
    if len(cohort) != 105:
        raise RuntimeError(f'Unexpected cohort size {len(cohort)}')
    skeletons = primitive_skeletons()
    sources = [ROOT/'simulation/source_faithful_20261024/width_controls.py',
               ROOT/'simulation/source_faithful_20261024/qft_reconstruction.py',
               ROOT/'simulation/source_faithful_20261024/resource_profile.py',
               ROOT/'simulation/pruning_study_20261023/compact_sensitivity.py',
               ROOT/'simulation/pruning_study_20261023/circuits.py', Path(__file__)]
    manifest = {'scope': 'DERIVED fixed-depth resource-only, not MPS/hardware/full-walk validation',
                'qiskit_version': qiskit.__version__, 'input_registry_sha256': hashlib.sha256(registry_path.read_bytes()).hexdigest(),
                'cohort_ids': [r['id'] for r in cohort], 'depth_policy': 'floor(n/2)',
                'primitive_skeletons': skeletons,
                'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
                'budgets_hardcoded': {'max_qubits': 150000, 'max_native_or_expanded_gates': 2000000, 'build_and_profile_seconds': 60},
                'methods': ['qft_direct_normalized', 'qft_source_generic_normalized', 'compact_exact_normalized',
                            'qft_direct_conservative', 'qft_source_generic_conservative', 'compact_exact_conservative',
                            'compact_root_dual']}
    (folder/'resource105_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    started, counts = time.monotonic(), {'COMPLETED': 0, 'CAPPED': 0, 'ERROR': 0}
    with (folder/'resource105_rows.jsonl').open('x', encoding='utf-8') as stream:
        for index, source in enumerate(cohort):
            w, v, cap, depth = source['weights'], source['values'], source['capacity'], source['n']//2
            for method in manifest['methods']:
                row = {'source_id': source['id'], 'instance_class': source['instance_class'], 'n': source['n'],
                       'seed': source['seed'], 'depth': depth, 'weights': w, 'values': v, 'capacity': cap,
                       'method': method, 'scope': 'resource_only', 'classification': 'DERIVED'}
                begin = time.monotonic()
                try:
                    budget = BuildBudget(150000, 2000000, 60)
                    if method=='compact_root_dual':
                        compiled = build_compact_root_dual(w, v, cap, depth, budget=budget)
                    else:
                        policy = 'normalized' if method.endswith('_normalized') else 'conservative'
                        engine = method.removesuffix('_'+policy)
                        compiled = build_exact_control(w, v, cap, depth, engine=engine, width_policy=policy, budget=budget)
                        row['shared_widths'] = widths(w, v, cap, policy)
                    remaining = 60 - (time.monotonic() - begin)
                    if remaining <= 0:
                        raise CircuitBuildCap('combined_build_profile_time_budget', {'elapsed_seconds': time.monotonic()-begin})
                    resources = profile(compiled, skeletons, BuildBudget(150000, 2000000, remaining))
                    row.update(status='COMPLETED', resources=resources, num_inputs=compiled.num_inputs,
                               quantum_threshold_bits=compiled.threshold_bits, metadata=compiled.metadata)
                except CircuitBuildCap as exc:
                    row.update(status='CAPPED', reason=exc.reason, partial_counters=exc.counters)
                except Exception as exc:
                    row.update(status='ERROR', error=type(exc).__name__+': '+str(exc))
                row['host_seconds_measured'] = time.monotonic()-begin
                counts[row['status']] += 1
                stream.write(json.dumps(row)+'\n');stream.flush()
                if row['status']=='ERROR':
                    raise RuntimeError('Unexpected resource construction error: '+row['error'])
            print(index+1, source['id'], counts, flush=True)
    summary = {'scope': manifest['scope'], 'classification': 'DERIVED resources; MEASURED build/profile host durations',
               'inputs': len(cohort), 'method_rows': sum(counts.values()), 'status_counts': counts,
               'elapsed_seconds_measured': time.monotonic()-started}
    (folder/'resource105_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary), flush=True)


if __name__=='__main__':
    main()
