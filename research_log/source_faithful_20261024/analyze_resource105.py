"""Summarize the preserved DERIVED 105-source control ledger, no data edits."""
import json
from pathlib import Path
from statistics import median


def metric(row, name):
    resources = row['resources']
    return resources['common_counts'].get(name, 0) if name in ('u', 'cx') else resources[name]


def compare(rows, numerator, denominator):
    by_id = {}
    for row in rows:
        by_id.setdefault(row['source_id'], {})[row['method']] = row
    result = dict(numerator=numerator, denominator=denominator, total_inputs=len(by_id), paired=0,
                  incomplete_pair_ids=[], metrics={})
    pairs = []
    for key, methods in by_id.items():
        a, b = methods.get(numerator), methods.get(denominator)
        if a and b and a['status'] == b['status'] == 'COMPLETED':
            pairs.append((a, b))
        else:
            result['incomplete_pair_ids'].append(key)
    result['paired'] = len(pairs)
    for name in ('qubits', 'u', 'cx', 'common_depth'):
        ratios = [metric(a, name) / metric(b, name) for a, b in pairs]
        result['metrics'][name] = dict(median_ratio=median(ratios), min_ratio=min(ratios), max_ratio=max(ratios),
             numerator_lower=sum(metric(a, name) < metric(b, name) for a, b in pairs),
             tied=sum(metric(a, name) == metric(b, name) for a, b in pairs),
             numerator_higher=sum(metric(a, name) > metric(b, name) for a, b in pairs))
    return result


def main():
    folder = Path(__file__).parent
    rows = [json.loads(line) for line in (folder / 'resource105_rows.jsonl').read_text().splitlines()]
    pairs = [('qft_direct_normalized', 'compact_exact_normalized'),
             ('qft_source_generic_normalized', 'qft_direct_normalized'),
             ('qft_direct_normalized', 'qft_direct_conservative'),
             ('compact_exact_normalized', 'compact_exact_conservative'),
             ('compact_root_dual', 'qft_direct_normalized')]
    out = dict(scope='DERIVED serial unmerged controls; no full-walk/hardware/compiler-optimality claim',
               rows=len(rows), status_counts={s: sum(r['status'] == s for r in rows) for s in set(r['status'] for r in rows)},
               comparisons=[compare(rows, a, b) for a, b in pairs],
               by_class={group: compare([r for r in rows if r['instance_class'] == group], *pairs[0])
                         for group in sorted(set(r['instance_class'] for r in rows))})
    (folder / 'resource105_analysis.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(json.dumps(out['comparisons'], indent=2))


if __name__ == '__main__':
    main()
