"""Full compiled-gate checks of identical LP/bank inverse-cancellation control."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from simulation.source_faithful_20261024.qft_bank import build_qft_bank
from simulation.source_faithful_20261024.width_controls import build_exact_control
from simulation.source_faithful_20261024.compressed_bank import build_dp_free_bank
from simulation.source_faithful_20261024.qft_normal_form import normalized_qft_circuit
from research_log.source_faithful_20261024.qft_bank_pilot import check


def main():
    folder = Path(__file__).parent
    output = folder / 'qft_bank_merged_validation.json'
    if output.exists():
        raise RuntimeError('Preserve existing merged validation')
    prereq = json.loads((folder / 'qft_bank_pilot_results.json').read_text())['summary']
    if prereq['predicate_phase_or_cleanup_failures'] or prereq['exact_rational_LP_predicate_disagreements']:
        raise RuntimeError('Initial bank pilot failed')
    fixtures = [([], [], 0, 0), ([1], [1], 0, 1), ([1], [1], 1, 1),
                ([1, 2], [1, 1], 1, 0), ([1, 2], [1, 1], 1, 1),
                ([2, 4], [1, 2], 3, 1), ([2, 3, 1], [2, 1, 1], 3, 1),
                ([1, 2], [0, 0], 0, 1), ([1, 2], [0, 1], 1, 1)]
    files = ['simulation/source_faithful_20261024/qft_bank.py',
             'simulation/source_faithful_20261024/qft_normal_form.py',
             'simulation/source_faithful_20261024/width_controls.py',
             'simulation/source_faithful_20261024/qft_reconstruction.py',
             'simulation/source_faithful_20261024/compressed_bank.py',
             'research_log/source_faithful_20261024/qft_bank_pilot.py',
             'research_log/source_faithful_20261024/mps_readout.py', str(Path(__file__).relative_to(ROOT))]
    out = dict(scope='actual complete merged compiled predicates, ideal QFT, both target bits and full threshold domain',
               cancellation='literal inverses across only disjoint gates; no source-optimality claim', rows=[], errors=[],
               source_sha256={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in files})
    for index, (w, v, W, d) in enumerate(fixtures):
        bank = build_dp_free_bank(w, v, W)['bank']
        for policy in ('direct', 'source_generic'):
            methods = [('bank', lambda: build_qft_bank(w, v, W, d, bank, mcx_policy=policy))]
            if all(x > 0 for x in v):
                methods.append(('lp', lambda: build_exact_control(w, v, W, d, engine='qft_' + policy)))
            for method, build in methods:
                row = dict(fixture=index, weights=w, values=v, capacity=W, depth=d, bank=bank,
                           policy=policy, method=method)
                try:
                    raw = build()
                    merged = normalized_qft_circuit(raw)
                    row.update(raw_gates=len(raw.gates), merged_gates=len(merged.gates),
                               cancellation=merged.metadata['inverse_cancellation'],
                               check=check(merged, w, v, W, d, bank))
                    out['rows'].append(row)
                    output.write_text(json.dumps(out, indent=2), encoding='utf-8')
                    c = row['check']
                    print(index, policy, method, c['status'], c.get('columns'), c.get('predicate_phase_or_cleanup_failures'), flush=True)
                    if c.get('predicate_phase_or_cleanup_failures') or c.get('exact_rational_LP_predicate_disagreements'):
                        raise RuntimeError('RESEARCH_INTEGRITY_STOP: merged bank/LP predicate failed')
                except Exception as exc:
                    out['errors'].append(dict(fixture=index, method=method, policy=policy,
                                             error=type(exc).__name__ + ': ' + str(exc)))
                    output.write_text(json.dumps(out, indent=2), encoding='utf-8')
                    raise
    checks = [r['check'] for r in out['rows']]
    out['summary'] = dict(method_cases=len(checks), columns=sum(c.get('columns', 0) for c in checks),
        statuses={s: sum(c['status'] == s for c in checks) for s in set(c['status'] for c in checks)},
        predicate_phase_or_cleanup_failures=sum(c.get('predicate_phase_or_cleanup_failures', 0) for c in checks),
        exact_rational_LP_predicate_disagreements=sum(c.get('exact_rational_LP_predicate_disagreements', 0) for c in checks),
        max_expected_amplitude_error=max(c.get('max_expected_amplitude_error', 0) for c in checks))
    output.write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(json.dumps(out['summary']), flush=True)


if __name__ == '__main__':
    main()
