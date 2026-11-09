"""Standalone DERIVED resource distributions; reads raw/derived ledgers only."""
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
pairs_path = HERE / 'compilation_extended_pairs.jsonl'
qft_path = HERE / 'qft_bank_full105_rows.jsonl'
pairs = [json.loads(s) for s in pairs_path.read_text().splitlines()]
qft = [json.loads(s) for s in qft_path.read_text().splitlines()]
assert len(qft) == 840 and all(r['status'] == 'COMPLETED' for r in qft)
matched = {}
for r in qft:
    if r['policy'] == 'direct' and r['form'] != 'raw':
        matched.setdefault(r['source_id'], {})[r['family']] = r
assert len(matched) == 105 and all(set(v) == {'bank', 'lp'} for v in matched.values())

fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.1), constrained_layout=True)
def curve(ax, values, label, **kw):
    values = sorted(values)
    ax.step(values, [(i + 1) / len(values) for i in range(len(values))],
            where='post', label=label, **kw)

for method, label, color in [('dp_free_bank', 'DP-free bank', '#126a9e'),
                             ('continuous_bank', 'Minimum-cardinality bank', '#b96921')]:
    values = [r['ratio'] for r in pairs if r['panel'] == 'main' and
              r['baseline'] == 'best_scan' and r['metric'] == 'ccx' and r['method'] == method]
    assert len(values) == 700
    curve(axes[0], values, label, color=color)
axes[0].set_title('Original 700: Boolean arithmetic')
axes[0].set_xlabel('CCX count / best of three scan controls')
for metric, label, color in [('qubits', 'Qubits', '#126a9e'),
                             ('cx', 'CX gates', '#349161'), ('depth', 'Depth', '#b96921')]:
    def resource(r):
        s = r['resources']
        return s['common_counts']['cx'] if metric == 'cx' else s['common_depth'] if metric == 'depth' else s['qubits']
    curve(axes[1], [resource(v['bank']) / resource(v['lp']) for v in matched.values()], label, color=color)
axes[1].set_title('Matched 105: cancelled QFT, direct controls')
axes[1].set_xlabel('DP-free bank / LP scan')
for ax in axes:
    ax.axvline(1, color='0.35', linestyle='--', linewidth=1)
    ax.set_ylabel('Fraction of paired inputs')
    ax.set_ylim(0, 1.02)
    ax.grid(alpha=.18)
    ax.legend(frameon=False, fontsize=8)
fig.suptitle('Logical resource tradeoffs with the same integer-pruning predicate', fontsize=12)
for ext in ['png', 'svg']:
    fig.savefig(HERE / f'research_resource_tradeoffs.{ext}', dpi=190)
(HERE / 'research_resource_tradeoffs_manifest.json').write_text(json.dumps({
    'classification': 'DERIVED logical gate resources; not hardware time',
    'left': 'All original 700 inputs. Baseline is a separate per-metric minimum, not one Pareto circuit.',
    'right': 'All fixed-depth 105 representatives. Same QFT engine, exact inverse cancellation on both sides; resource only.',
    'sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [pairs_path, qft_path, Path(__file__)]}
}, indent=2))
print('Wrote resource distributions from 700 and 105 paired inputs.')
