"""Shared fixed-depth LP control with explicit normalized/conservative widths."""
from fractions import Fraction

from .qft_reconstruction import QFTNetwork
from ..pruning_study_20261023.compact_sensitivity import Ripple
from ..pruning_study_20261023.circuits import _data, threshold_bits
from ..oracle_h.node_bound_reversible import exact_order


def widths(weights, values, capacity, policy="normalized"):
    weights, values, capacity = _data(weights, values, capacity)
    total, tb = sum(values), threshold_bits(values)
    if policy == "normalized":
        ratios = [Fraction(v, w) for w, v in zip(weights, values)]
        bound = max((max(total * r.denominator + capacity * r.numerator,
                         ((1 << tb) - 1) * r.denominator) for r in ratios),
                    default=max(total, (1 << tb) - 1))
    elif policy == "conservative":
        bound = max(total * max(weights, default=1) + capacity * max(values, default=1),
                    ((1 << tb) - 1) * max(weights, default=1))
    else:
        raise ValueError("Unknown width policy")
    return max(1, (capacity + sum(weights)).bit_length() + 1), max(1, total.bit_length() + 1), max(1, bound.bit_length() + 1), tb


def build_exact_control(weights, values, capacity, depth, engine="qft_direct", width_policy="normalized", budget=None):
    weights, values, capacity = _data(weights, values, capacity)
    if not 0 <= depth <= len(weights):
        raise ValueError("Invalid fixed depth")
    order = tuple(exact_order(weights, values))
    wb, vb, cb, tb = widths(weights, values, capacity, width_policy)
    if engine in ("qft_direct", "qft_source_generic"):
        c = QFTNetwork(depth + tb, max(wb, vb, cb), budget,
                       "direct" if engine == "qft_direct" else "source_generic")
        undo = c.inverse
    elif engine == "compact_exact":
        c = Ripple(depth + tb, max(wb, vb, cb), budget)
        undo = lambda gates: list(reversed(gates))
    else:
        raise ValueError("Unknown arithmetic engine")
    weight, pval, residual = c.allocate(wb), c.allocate(vb), c.allocate(wb)
    numerator, threshold = c.allocate(cb), c.allocate(cb)
    bad_capacity, active = c.allocate(2)
    for j, item in enumerate(order[:depth]):
        c.controlled_constant(weight, weights[item], c.inputs[j])
        c.controlled_constant(pval, values[item], c.inputs[j])
    c.const_less(capacity, weight, bad_capacity)
    c.emit(active)
    c.emit(active, bad_capacity)
    for j in range(wb):
        if (capacity >> j) & 1:
            c.emit(residual[j])
    c.variable_add(residual, weight, subtract=True)
    outputs = [(bad_capacity,)]
    for item in order[depth:]:
        enough, take, split, below = c.allocate(4)
        c.const_less(weights[item], residual, enough, constant_on_left=False)
        c.emit(enough)
        c.emit(take, active, enough)
        c.emit(enough)
        c.emit(split, active, enough)
        c.emit(enough)
        c.controlled_constant(pval, values[item], take)
        c.controlled_constant(residual, weights[item], take, subtract=True)
        ratio = Fraction(values[item], weights[item])
        start = len(c.gates)
        c.product_add(numerator, pval, ratio.denominator)
        c.product_add(numerator, residual, ratio.numerator)
        c.product_add(threshold, c.inputs[depth:], ratio.denominator)
        products = list(c.gates[start:])
        c.less(numerator, threshold, below)
        c.extend(undo(products))
        outputs.append((split, below))
        active = take
    integer_below = c.allocate(1)[0]
    start = len(c.gates)
    c.variable_add(numerator, pval)
    c.variable_add(threshold, c.inputs[depth:])
    products = list(c.gates[start:])
    c.less(numerator, threshold, integer_below)
    c.extend(undo(products))
    outputs.append((active, integer_below))
    c.finish(outputs)
    meta = dict(width_policy=width_policy, weight_width=wb, value_width=vb, numerator_width=cb,
                weights=list(weights), values=list(values), capacity=capacity, item_order=list(order))
    if engine.startswith("qft"):
        return c.circuit(depth, tb, **meta)
    return c.circuit(order, tb, depth, "compact_exact_width_control", **meta)
