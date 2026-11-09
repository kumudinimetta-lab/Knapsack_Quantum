"""Finite precompiled multiplier-bank tree pilot, reusing immutable pilot rows."""
import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from theory_probe import constants


def tree(w, v, W, tau, bank, cap=50000):
    order, a, b, rc, A = constants(w, v, W)
    root = Fraction(a, b)
    densities = sorted({Fraction(vi, wi) for vi, wi in zip(v, w)})
    if bank == 1:
        multipliers = [root]
    elif bank == 2:
        multipliers = sorted({root, Fraction(0)})
    else:
        multipliers = sorted({root, Fraction(0), densities[0], densities[-1]})
    data = []
    for lam in multipliers:
        aa, bb = lam.numerator, lam.denominator
        reduced = [bb * vi - aa * wi for wi, vi in zip(w, v)]
        AA = aa * W + sum(max(x, 0) for x in reduced)
        data.append((bb, reduced, AA))
    stack = [(0, 0, tuple(0 for _ in data))]
    nodes = 0
    while stack and nodes < cap:
        d, weight, penalties = stack.pop()
        nodes += 1
        if weight > W or any(AA - penalty < bb * tau
                             for (bb, reduced, AA), penalty in zip(data, penalties)):
            continue
        if d == len(w):
            continue
        i = order[d]
        for bit in (1, 0):
            new = tuple(penalty + abs(reduced[i]) * (bit != int(reduced[i] > 0))
                        for (_, reduced, _), penalty in zip(data, penalties))
            stack.append((d + 1, weight + bit * w[i], new))
    return dict(nodes=nodes, capped=bool(stack), multipliers=[[x.numerator, x.denominator] for x in multipliers])


data = json.loads((HERE / 'theory_probe_results.json').read_text())
rows = []
for row in data['rows']:
    rr = {k: row[k] for k in ['n', 'seed', 'instance_class', 'tau', 'target_kind']}
    rr['trees'] = {str(bank): tree(row['weights'], row['values'], row['capacity'], row['tau'], bank) for bank in [1, 2, 4]}
    rr['lp'] = row['trees']['lp']
    rows.append(rr)
out = dict(description='Finite root/zero/extreme-ratio dual bank pilot; no circuits or quantum runtime.',
           taxonomy={'node_counts': 'MEASURED (classical enumeration)', 'cap': 'HARDCODED 50000'}, rows=rows)
(HERE / 'theory_bank_probe_results.json').write_text(json.dumps(out, indent=2))
print('Saved', len(rows), 'rows')
