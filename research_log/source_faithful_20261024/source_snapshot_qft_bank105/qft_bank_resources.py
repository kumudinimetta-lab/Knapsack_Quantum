"""Paired same-function QFT bank/LP resources, raw and exact-inverse controls."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from simulation.source_faithful_20261024.qft_bank import build_qft_bank
from simulation.source_faithful_20261024.qft_normal_form import normalized_qft_circuit
from simulation.source_faithful_20261024.width_controls import build_exact_control
from simulation.source_faithful_20261024.compressed_bank import build_dp_free_bank
from simulation.source_faithful_20261024.resource_profile import primitive_skeletons, profile
from simulation.pruning_study_20261023.circuits import BuildBudget, CircuitBuildCap


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scope', choices=['pilot5', 'full105'], required=True)
    scope = parser.parse_args().scope
    folder = Path(__file__).parent
    check = json.loads((folder / 'qft_bank_merged_validation.json').read_text())['summary']
    if check['predicate_phase_or_cleanup_failures'] or check['exact_rational_LP_predicate_disagreements'] or check['statuses'] != {'COMPLETED': 32}:
        raise RuntimeError('Merged complete-gate validation is not green')
    if scope == 'full105':
        first = json.loads((folder / 'qft_bank_pilot5_summary.json').read_text())
        if first['status_counts'] != {'COMPLETED': 40}:
            raise RuntimeError('The bounded five-input resource pilot must complete before expansion')
    registry_path = ROOT / 'research_log/pruning_study_20261023/inputs.json'
    bank_path = folder / 'theory_banks_dp_free.jsonl'
    registry = json.loads(registry_path.read_text())['records']
    cohort = [r for r in registry if r['category'] == 'main700' and r['seed'] - 1000 * r['n'] in (0, 1, 2)]
    if scope == 'pilot5':
        cohort = [r for r in cohort if r['n'] == 12 and r['seed'] == 12000]
    expected_inputs = 5 if scope == 'pilot5' else 105
    if len(cohort) != expected_inputs:
        raise RuntimeError('Predeclared cohort count differs')
    banks = {r['id']: r for r in map(json.loads, bank_path.read_text().splitlines())}
    lp_path = folder / 'resource105_rows.jsonl'
    old_lp = {(r['source_id'], r['method']): r for r in map(json.loads, lp_path.read_text().splitlines())}
    output = folder / f'qft_bank_{scope}_rows.jsonl'
    if output.exists():
        raise RuntimeError('Preserve existing resource ledger; choose a new run name')
    skeletons = primitive_skeletons()
    source_files = [ROOT / 'simulation/source_faithful_20261024' / p for p in
                    ['qft_bank.py', 'qft_normal_form.py', 'width_controls.py', 'qft_reconstruction.py',
                     'resource_profile.py', 'compressed_bank.py']]
    source_files.append(Path(__file__))
    manifest = dict(scope='DERIVED fixed-depth same-integer-predicate resources; no 105-input gate simulation or full walk',
         cohort_policy='original trial 0,1,2 per 5 classes/7 sizes; depth floor(n/2)',
         cohort_ids=[r['id'] for r in cohort], inputs=expected_inputs,
         source_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files},
         input_registry_sha256=hashlib.sha256(registry_path.read_bytes()).hexdigest(),
         theory_bank_ledger_sha256=hashlib.sha256(bank_path.read_bytes()).hexdigest(),
         reused_raw_LP_ledger_sha256=hashlib.sha256(lp_path.read_bytes()).hexdigest(),
         prerequisite='qft_bank_merged_validation.json: 32 complete method cases / no predicate/cleanup mismatches',
         shared_domain='fixed sorted prefix depth plus identical full quantum threshold register, arbitrary output bit',
         exact_cancellation='literal inverses across disjoint gates applied identically to LP and bank',
         budgets_hardcoded=dict(max_qubits=150000, max_gates=2000000, build_or_profile_seconds=60),
         basis=['u', 'cx'], optimization_level=0, connectivity='all_to_all', ideal_arbitrary_angle_rotations=True,
         unimplemented='diagonal angle merging, copied-control source parallel schedule, fault-tolerant rotation synthesis')
    (folder / f'qft_bank_{scope}_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    counts, started = Counter(), time.monotonic()
    with output.open('x', encoding='utf-8') as stream:
        for index, source in enumerate(cohort):
            w, v, W, d = source['weights'], source['values'], source['capacity'], source['n'] // 2
            bank_record = banks[source['id']]
            bank = bank_record['result']['bank']
            repro = build_dp_free_bank(w, v, W)
            if repro['bank'] != bank:
                raise RuntimeError('RESEARCH_INTEGRITY_STOP: stored DP-free bank does not reproduce')
            for policy in ('direct', 'source_generic'):
                for family in ('lp', 'bank'):
                    begin = time.monotonic()
                    compiled, build_cap = None, None
                    try:
                        budget = BuildBudget(150000, 2000000, 60)
                        compiled = build_exact_control(w, v, W, d, engine='qft_' + policy, budget=budget) if family == 'lp' else build_qft_bank(w, v, W, d, bank, budget=budget, mcx_policy=policy)
                    except CircuitBuildCap as exc:
                        build_cap = dict(reason=exc.reason, partial_counters=exc.counters)
                    build_seconds = time.monotonic() - begin
                    for form in ('raw', 'merged'):
                        row = dict(source_id=source['id'], instance_class=source['instance_class'], n=source['n'],
                            seed=source['seed'], weights=w, values=v, capacity=W, depth=d, bank=bank,
                            bank_size=len(bank), bank_status=bank_record['result']['status'],
                            bank_preprocessing_seconds_measured=repro['preprocessing_seconds'],
                            method=f'qft_{family}_{policy}_{form}', family=family, policy=policy, form=form,
                            classification='DERIVED', scope='resource_only', build_seconds_measured=build_seconds)
                        try:
                            if build_cap:
                                row.update(status='CAPPED', **build_cap)
                            else:
                                current = compiled if form == 'raw' else normalized_qft_circuit(compiled)
                                if family == 'lp' and form == 'raw':
                                    earlier = old_lp[(source['id'], f'qft_{policy}_normalized')]
                                    if earlier['status'] != 'COMPLETED' or dict(Counter(g[0] for g in current.gates)) != earlier['resources']['native_counts']:
                                        raise RuntimeError('RESEARCH_INTEGRITY_STOP: raw LP lineage differs')
                                    resources = earlier['resources']
                                    row['resource_lineage'] = 'reused preserved resource105 row after native-count equality check'
                                else:
                                    resources = profile(current, skeletons, BuildBudget(150000, 2000000, 60))
                                row.update(status='COMPLETED', resources=resources, num_inputs=current.num_inputs,
                                           quantum_threshold_bits=current.threshold_bits, metadata=current.metadata)
                        except CircuitBuildCap as exc:
                            row.update(status='CAPPED', reason=exc.reason, partial_counters=exc.counters)
                        except Exception as exc:
                            row.update(status='ERROR', error=type(exc).__name__ + ': ' + str(exc))
                        counts[row['status']] += 1
                        stream.write(json.dumps(row) + '\n'); stream.flush()
                        if row['status'] == 'ERROR':
                            raise RuntimeError(row['error'])
            print(index + 1, source['id'], dict(counts), flush=True)
    summary = dict(scope=manifest['scope'], inputs=expected_inputs, rows=sum(counts.values()),
                   status_counts=dict(counts), seconds_measured=time.monotonic() - started)
    (folder / f'qft_bank_{scope}_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    main()
