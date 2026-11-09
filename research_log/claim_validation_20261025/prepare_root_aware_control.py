"""Construct a new isolated control from pinned source; do not edit production."""
from pathlib import Path
import hashlib
import json
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
source = ROOT / 'simulation/source_faithful_20261024/width_controls.py'
code = source.read_text()
assert hashlib.sha256(source.read_bytes()).hexdigest() == '0aef8efb138862d76ad50c9365f217492bac7ddfc893c44fdecfb9c36ce4fbd1'
changes = [
 ('from .qft_reconstruction import QFTNetwork', 'from simulation.source_faithful_20261024.qft_reconstruction import QFTNetwork'),
 ('from ..pruning_study_20261023.compact_sensitivity import Ripple', 'from simulation.pruning_study_20261023.compact_sensitivity import Ripple'),
 ('from ..pruning_study_20261023.circuits import _data, threshold_bits', 'from simulation.pruning_study_20261023.circuits import _data, threshold_bits'),
 ('from ..oracle_h.node_bound_reversible import exact_order', 'from simulation.oracle_h.node_bound_reversible import exact_order'),
 ('def build_exact_control(', 'def build_root_aware_control('),
 ('    wb, vb, cb, tb = widths(weights, values, capacity, width_policy)', '''    wb, vb, cb, tb = widths(weights, values, capacity, width_policy)
    if width_policy != "normalized":
        raise ValueError("This control requires normalized widths")
    cumulative, root_split = 0, len(weights)
    for position, item in enumerate(order):
        cumulative += weights[item]
        if cumulative > capacity:
            root_split = position
            break
    eligible = order[max(depth, root_split):]
    total, tau_max = sum(values), (1 << tb) - 1
    bounds = [total, tau_max]
    for item in eligible:
        ratio = Fraction(values[item], weights[item])
        bounds.extend([total*ratio.denominator + capacity*ratio.numerator, tau_max*ratio.denominator])
    cb = max(1, max(bounds).bit_length() + 1)'''),
 ('    for item in order[depth:]:', '    for position, item in enumerate(order[depth:], start=depth):'),
 ('''        ratio = Fraction(values[item], weights[item])
        start = len(c.gates)
        c.product_add(numerator, pval, ratio.denominator)
        c.product_add(numerator, residual, ratio.numerator)
        c.product_add(threshold, c.inputs[depth:], ratio.denominator)
        products = list(c.gates[start:])
        c.less(numerator, threshold, below)
        c.extend(undo(products))
        outputs.append((split, below))''', '''        if position >= root_split:
            ratio = Fraction(values[item], weights[item])
            start = len(c.gates)
            c.product_add(numerator, pval, ratio.denominator)
            c.product_add(numerator, residual, ratio.numerator)
            c.product_add(threshold, c.inputs[depth:], ratio.denominator)
            products = list(c.gates[start:])
            c.less(numerator, threshold, below)
            c.extend(undo(products))
            outputs.append((split, below))'''),
 ('    meta = dict(width_policy=width_policy, weight_width=wb, value_width=vb, numerator_width=cb,',
  '    meta = dict(root_split=root_split, eligible_fraction_positions=list(range(max(depth, root_split),len(weights))), width_policy="root_aware_normalized", weight_width=wb, value_width=vb, numerator_width=cb,'),
]
for before, after in changes:
    assert code.count(before) == 1, before
    code = code.replace(before, after)
dest = HERE / 'root_aware_control.py'
assert not dest.exists()
dest.write_text('# Isolated root-aware control. See root_aware_control_derivation.md.\n'+code)
(HERE / 'root_aware_source_manifest.json').write_text(json.dumps(dict(
    base_source=str(source),base_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
    new_source_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),
    derivation_sha256=hashlib.sha256((HERE/'root_aware_control_derivation.md').read_bytes()).hexdigest(),
    transformations=changes),indent=2))
print('Created isolated root-aware control; pinned source unchanged.')
