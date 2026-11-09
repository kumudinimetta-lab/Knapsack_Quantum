"""OUR fixed-depth static dual-bank reconstruction in the QFT arithmetic engine.

This synthesizes the supplied bank predicate; floor-equivalence to the LP
requires a separate bank certificate. It is not a released competitor oracle.
See qft_bank_derivation_before_code.md for the prior width/cleanup derivation.
"""
from fractions import Fraction

from .qft_reconstruction import QFTNetwork
from ..oracle_h.node_bound_reversible import exact_order


def _bank_data(weights, values, capacity):
    weights, values = tuple(weights), tuple(values)
    if len(weights) != len(values):
        raise ValueError("Weights and values must have equal length")
    if any(type(x) is not int for x in (*weights, *values, capacity)):
        raise ValueError("Integer problem data required")
    if any(x <= 0 for x in weights) or any(x < 0 for x in values) or capacity < 0:
        raise ValueError("Positive weights and nonnegative values/capacity required")
    return weights, values, capacity


def normalized_bank(bank):
    result = []
    for value in bank:
        if isinstance(value, Fraction):
            ratio = value
        elif isinstance(value, (tuple, list)) and len(value) == 2 and all(isinstance(x, int) for x in value):
            ratio = Fraction(*value)
        else:
            raise ValueError("Bank entries must be Fractions or integer numerator/denominator pairs")
        if ratio < 0:
            raise ValueError("Dual multipliers must be nonnegative")
        result.append(ratio)
    if not result:
        raise ValueError("Bank must not be empty")
    return tuple(sorted(set(result)))


def bank_geometry(weights, values, capacity, depth, bank):
    weights, values, capacity = _bank_data(weights, values, capacity)
    if not 0 <= depth <= len(weights):
        raise ValueError("Invalid fixed depth")
    bank = normalized_bank(bank)
    order = tuple(exact_order(weights, values))
    # Same formula/domain as the LP controls, extended explicitly to zero values.
    wb = max(1, (capacity + sum(weights)).bit_length() + 1)
    tb = max(1, (sum(values) + 1).bit_length())
    tau_max = (1 << tb) - 1
    entries = []
    for ratio in bank:
        a, b = ratio.numerator, ratio.denominator
        costs = tuple(b * v - a * w for w, v in zip(weights, values))
        constant = a * capacity + sum(max(c, 0) for c in costs)
        loss_bound = sum(abs(costs[i]) for i in order[:depth])
        entries.append(dict(numerator=a, denominator=b, costs=costs,
                            constant=constant, accumulator_bound=loss_bound + b * tau_max))
    cb = max(1, max(max(e["constant"], e["accumulator_bound"]) for e in entries).bit_length() + 1)
    return weights, values, capacity, order, bank, wb, cb, tb, entries


def build_qft_bank(weights, values, capacity, depth, bank, budget=None, mcx_policy="direct"):
    weights, values, capacity, order, bank, wb, cb, tb, entries = bank_geometry(
        weights, values, capacity, depth, bank)
    c = QFTNetwork(depth + tb, max(wb, cb, len(bank) + 1), budget, mcx_policy)
    weight, accumulator = c.allocate(wb), c.allocate(cb)
    bad_capacity = c.allocate(1)[0]
    for j, item in enumerate(order[:depth]):
        c.controlled_constant(weight, weights[item], c.inputs[j])
    c.const_less(capacity, weight, bad_capacity)
    flags = [bad_capacity]
    for entry in entries:
        start = len(c.gates)
        initial_loss = sum(max(entry["costs"][i], 0) for i in order[:depth])
        for j, wire in enumerate(accumulator):
            if (initial_loss >> j) & 1:
                c.emit(wire)
        for j, item in enumerate(order[:depth]):
            cost = entry["costs"][item]
            c.controlled_constant(accumulator, abs(cost), c.inputs[j], subtract=cost > 0)
        c.product_add(accumulator, c.inputs[depth:], entry["denominator"])
        arithmetic = list(c.gates[start:])
        below = c.allocate(1)[0]
        c.const_less(entry["constant"], accumulator, below)
        c.extend(c.inverse(arithmetic))
        flags.append(below)
    aggregate = c.allocate(1)[0]
    c.emit(aggregate)
    for flag in flags:
        c.emit(flag)
    c.mcx_source_chain(flags, aggregate)
    for flag in reversed(flags):
        c.emit(flag)
    c.finish([(aggregate,)])
    return c.circuit(depth, tb, predicate="supplied_static_dual_bank_OR_capacity_infeasible",
                     coverage_certificate="external_required_for_LP_integer_predicate_equivalence",
                     weights=list(weights), values=list(values), capacity=capacity,
                     item_order=list(order), bank=[[r.numerator, r.denominator] for r in bank],
                     bank_size=len(bank), weight_width=wb, accumulator_width=cb,
                     accumulator_bounds=[e["accumulator_bound"] for e in entries],
                     dual_constants=[e["constant"] for e in entries],
                     aggregation="OR_not_parity_compute_copy_uncompute")
