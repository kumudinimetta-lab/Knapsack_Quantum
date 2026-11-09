"""Matched same-QFT-engine bank/LP summaries; preserves all raw rows and caps."""
import argparse
import json
from pathlib import Path
from statistics import median


def value(row, metric):
    resources = row['resources']
    return resources['common_counts'].get(metric, 0) if metric in ('u', 'cx') else resources[metric]


def comparison(rows, numerator, denominator):
    inputs = {}
    for row in rows:
        inputs.setdefault(row['source_id'], {})[row['method']] = row
    pairs, missing = [], []
    for key, methods in inputs.items():
        a, b = methods.get(numerator), methods.get(denominator)
        if a and b and a['status'] == b['status'] == 'COMPLETED':
            if a['num_inputs'] != b['num_inputs'] or a['quantum_threshold_bits'] != b['quantum_threshold_bits']:
                raise RuntimeError('RESEARCH_INTEGRITY_STOP: compared quantum domains differ')
            pairs.append((a, b))
        else:
            missing.append(key)
    metrics = {}
    for key in ('qubits', 'u', 'cx', 'common_depth'):
        ratios = [value(a, key) / value(b, key) for a, b in pairs]
        metrics[key] = dict(median_ratio=median(ratios), min_ratio=min(ratios), max_ratio=max(ratios),
            lower=sum(value(a, key) < value(b, key) for a, b in pairs),
            tied=sum(value(a, key) == value(b, key) for a, b in pairs),
            higher=sum(value(a, key) > value(b, key) for a, b in pairs)) if ratios else None
    weakly_dominates = lambda a, b: all(value(a, k) <= value(b, k) for k in metrics)
    return dict(numerator=numerator, denominator=denominator, paired=len(pairs), incomplete_pair_ids=missing,
         metrics=metrics, numerator_weakly_dominates_all_four=sum(weakly_dominates(a, b) for a, b in pairs),
         denominator_weakly_dominates_all_four=sum(weakly_dominates(b, a) for a, b in pairs),
         examples=[dict(source_id=a['source_id'], bank_size=a['bank_size'],
              numerator={k: value(a, k) for k in metrics}, denominator={k: value(b, k) for k in metrics})
              for a, b in pairs] if len(pairs) <= 5 else [])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scope', choices=['pilot5', 'full105'], required=True)
    scope = parser.parse_args().scope
    folder = Path(__file__).parent
    rows = list(map(json.loads, (folder / f'qft_bank_{scope}_rows.jsonl').read_text().splitlines()))
    summaries = []
    for policy in ('direct', 'source_generic'):
        summaries.extend([comparison(rows, f'qft_bank_{policy}_merged', f'qft_lp_{policy}_merged'),
                          comparison(rows, f'qft_bank_{policy}_raw', f'qft_lp_{policy}_raw'),
                          comparison(rows, f'qft_bank_{policy}_merged', f'qft_bank_{policy}_raw'),
                          comparison(rows, f'qft_lp_{policy}_merged', f'qft_lp_{policy}_raw')])
    by_class = {group: comparison([r for r in rows if r['instance_class'] == group],
                 'qft_bank_direct_merged', 'qft_lp_direct_merged') for group in sorted({r['instance_class'] for r in rows})}
    out = dict(classification='DERIVED resources; descriptive matched ratios, no extrapolation/quantum advantage claim',
        statuses={s: sum(r['status'] == s for r in rows) for s in {r['status'] for r in rows}},
        inputs=len({r['source_id'] for r in rows}), rows=len(rows), comparisons=summaries, by_class=by_class,
        bank_sizes={source_id: next(r['bank_size'] for r in rows if r['source_id'] == source_id)
                    for source_id in sorted({r['source_id'] for r in rows})})
    (folder / f'qft_bank_{scope}_analysis.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(json.dumps(summaries[0], indent=2))


if __name__ == '__main__':
    main()
