"""Exact classical structural accounting, never a quantum-execution simulator.

Node counts include generated rejected children. Query-scale numbers are
conditional analytic scales without hidden-constant or runtime interpretation.
"""
from __future__ import annotations

import math
import time
from fractions import Fraction
from typing import Iterable

METHODS = ('simple', 'root_dual', 'bank2', 'bank4', 'exact_lp')


def exact_order(weights, values):
    return tuple(sorted(range(len(weights)), key=lambda i: Fraction(values[i], weights[i]), reverse=True))


def root_multiplier(weights, values, capacity):
    rem = capacity
    for i in exact_order(weights, values):
        if weights[i] <= rem:
            rem -= weights[i]
        else:
            return Fraction(values[i], weights[i])
    return Fraction(0)


def bank_multipliers(weights, values, capacity, q=1):
    root = root_multiplier(weights, values, capacity)
    if q == 1:
        return (root,)
    choices = {root, Fraction(0)}
    if q == 4:
        if weights:
            densities = [Fraction(v, w) for v, w in zip(values, weights)]
            choices.update([min(densities), max(densities)])
    elif q != 2:
        raise ValueError('q must be 1, 2, or 4')
    return tuple(sorted(choices))


def dual_constants(weights, values, capacity, multiplier=None):
    lam = root_multiplier(weights, values, capacity) if multiplier is None else Fraction(multiplier)
    if lam < 0:
        raise ValueError('A dual capacity multiplier must be nonnegative')
    a, b = lam.numerator, lam.denominator
    reduced = tuple(b * v - a * w for w, v in zip(weights, values))
    A = a * capacity + sum(max(x, 0) for x in reduced)
    return a, b, reduced, A


def lp_value(weights, values, capacity, items: Iterable[int] | None = None):
    if capacity < 0:
        return None
    order = exact_order(weights, values) if items is None else tuple(items)
    rem = capacity
    profit = 0
    for i in order:
        if weights[i] <= rem:
            rem -= weights[i]
            profit += values[i]
        else:
            return Fraction(profit) + Fraction(rem * values[i], weights[i])
    return Fraction(profit)


def bound_at_prefix(weights, values, capacity, depth, prefix, method='exact_lp'):
    """prefix[j] is assignment to order[j]; trailing bits are ignored."""
    n = len(weights)
    if not 0 <= depth <= n:
        return None
    order = exact_order(weights, values)
    weight = sum(weights[i] * prefix[j] for j, i in enumerate(order[:depth]))
    profit = sum(values[i] * prefix[j] for j, i in enumerate(order[:depth]))
    if weight > capacity:
        return None
    if method == 'simple':
        return Fraction(profit + sum(values[i] for i in order[depth:]))
    if method == 'exact_lp':
        return profit + lp_value(weights, values, capacity - weight, order[depth:])
    q = {'root_dual': 1, 'bank2': 2, 'bank4': 4}[method]
    upper = []
    for lam in bank_multipliers(weights, values, capacity, q):
        _, b, reduced, A = dual_constants(weights, values, capacity, lam)
        loss = sum(abs(reduced[i]) * (prefix[j] != int(reduced[i] > 0))
                   for j, i in enumerate(order[:depth]))
        upper.append(Fraction(A - loss, b))
    return min(upper)


def feasible_incumbent(weights, values, capacity):
    used = value = 0
    witness = [0] * len(weights)
    for i in exact_order(weights, values):
        if used + weights[i] <= capacity:
            used += weights[i]
            value += values[i]
            witness[i] = 1
    return value, witness


def cheap_certificate(weights, values, capacity, tau, multiplier=None):
    """O(n^3) small exact-integer envelope; no tree enumeration or DP budget.

    Includes generated children rejected by the predicate. Covers all larger
    targets and prefix-restricted calls using this ORIGINAL instance/order.
    """
    start = time.perf_counter()
    order = exact_order(weights, values)
    a, b, reduced, A = dual_constants(weights, values, capacity, multiplier)
    costs = [abs(reduced[i]) for i in order]
    H = A - b * tau
    total = 1
    counts = []
    if H >= 0:
        for d in range(len(costs)):
            pref = costs[:d]
            best = 1 << d
            for cutoff in {1, *[x for x in pref if x > 0]}:
                small = sum(x < cutoff for x in pref)
                large = d - small
                k = min(large, H // cutoff)
                count = (1 << small) * sum(math.comb(large, j) for j in range(k + 1))
                best = min(best, count)
            counts.append(best)
            total += 2 * best
    return dict(bound=total, prefix_count_bounds=counts, target_floor=tau,
                multiplier=[a, b], A=A, H=H, costs=costs, order=list(order),
                computation_seconds=time.perf_counter() - start,
                taxonomy='DERIVED exact integer upper bound; time MEASURED')


def enumerate_threshold_tree(weights, values, capacity, tau, method='exact_lp',
                             *, prefix=(), node_cap=50000, seconds_cap=1.0,
                             stop_on_first=False):
    """Enumerate a fixed-order tree; every generated rejected child is counted.

    prefix is in ORIGINAL order, and root dual penalties never restart at zero.
    A restricted subtree count includes its own root. In whole-tree mode, a
    first witness is saved but enumeration continues. On cap, sat is known if
    a witness was found; unsat is known only if enumeration completed.
    """
    if method not in METHODS:
        raise ValueError(method)
    started = time.perf_counter()
    n = len(weights)
    order = exact_order(weights, values)
    prefix = tuple(prefix)
    if len(prefix) > n or any(bit not in (0, 1) for bit in prefix):
        raise ValueError('invalid fixed prefix')
    banks = []
    if method in ('root_dual', 'bank2', 'bank4'):
        q = {'root_dual': 1, 'bank2': 2, 'bank4': 4}[method]
        banks = [dual_constants(weights, values, capacity, lam)
                 for lam in bank_multipliers(weights, values, capacity, q)]
    suffix_values = [0] * (n + 1)
    for d in reversed(range(n)):
        suffix_values[d] = suffix_values[d + 1] + values[order[d]]
    weight = sum(weights[i] * prefix[j] for j, i in enumerate(order[:len(prefix)]))
    profit = sum(values[i] * prefix[j] for j, i in enumerate(order[:len(prefix)]))
    losses = tuple(sum(abs(rc[i]) * (prefix[j] != int(rc[i] > 0))
                       for j, i in enumerate(order[:len(prefix)])) for a, b, rc, A in banks)
    stack = [(prefix, weight, profit, losses)]
    nodes = marked = rejected_capacity = rejected_bound = 0
    first_witness = None
    first_witness_prefix = None
    cap_reason = None
    stopped_early = False
    while stack:
        if nodes >= node_cap:
            cap_reason = 'node_cap'
            break
        if nodes % 128 == 0 and time.perf_counter() - started >= seconds_cap:
            cap_reason = 'time_cap'
            break
        assigned, weight, profit, losses = stack.pop()
        d = len(assigned)
        nodes += 1
        if weight > capacity:
            rejected_capacity += 1
            continue
        if method == 'simple':
            reject = profit + suffix_values[d] < tau
        elif method == 'exact_lp':
            reject = profit + lp_value(weights, values, capacity - weight, order[d:]) < tau
        else:
            reject = any(A - loss < b * tau for (a, b, rc, A), loss in zip(banks, losses))
        if reject:
            rejected_bound += 1
            continue
        if d == n:
            if profit >= tau:
                marked += 1
                if first_witness is None:
                    first_witness_prefix = list(assigned)
                    first_witness = [0] * n
                    for j, i in enumerate(order):
                        first_witness[i] = assigned[j]
                if stop_on_first:
                    stopped_early = True
                    break
            continue
        item = order[d]
        for bit in (1, 0):
            newloss = tuple(loss + abs(rc[item]) * (bit != int(rc[item] > 0))
                            for (_, _, rc, _), loss in zip(banks, losses))
            stack.append((assigned + (bit,), weight + bit * weights[item],
                          profit + bit * values[item], newloss))
    complete = not stack and not stopped_early
    sat = True if first_witness is not None else (False if complete else None)
    return dict(nodes=nodes, complete=complete, capped=cap_reason is not None,
                cap_reason=cap_reason, stopped_on_first=stopped_early,
                marked_leaves_seen=marked, sat=sat, witness=first_witness,
                witness_in_order=first_witness_prefix, rejected_capacity=rejected_capacity,
                rejected_bound=rejected_bound, prefix=list(prefix), tau=tau,
                method=method, seconds=time.perf_counter() - started,
                taxonomy='MEASURED classical DFS counts; NOT quantum execution',
                node_cap=node_cap, seconds_cap=seconds_cap)


def structural_optimize(weights, values, capacity, method='exact_lp', *,
                        node_cap=50000, seconds_cap=3.0, delta=0.01):
    """Value search plus explicit prefix witness recovery using exact decisions.

    Does not use a separately computed optimum. Stops honestly on undecided
    capped calls. Output schedules are analytic scales, not circuit execution.
    """
    start = time.perf_counter()
    n = len(weights)
    lower, initial_witness = feasible_incumbent(weights, values, capacity)
    upper = math.floor(lp_value(weights, values, capacity)) + 1
    initial_lower = lower
    max_calls = max(1, (max(1, upper - lower)).bit_length() + n)
    cert = cheap_certificate(weights, values, capacity, initial_lower + 1,
                             Fraction(0) if method == 'simple' else None)
    calls = []
    total_nodes = 0
    # Elementary scale from Montanaro 2018 detection. Hidden constants and full
    # gate/walk costs are deliberately absent. This is not a query count claim.
    scale = math.sqrt(cert['bound'] * max(1, n)) * math.log(max_calls / delta)

    def detect(tau, prefix=(), phase='value'):
        nonlocal total_nodes
        remaining = max(0.0, seconds_cap - (time.perf_counter() - start))
        call = enumerate_threshold_tree(weights, values, capacity, tau, method,
                  prefix=prefix, node_cap=max(0, node_cap-total_nodes),
                  seconds_cap=remaining, stop_on_first=True)
        total_nodes += call['nodes']
        call['phase'] = phase
        call['conditional_detection_scale'] = scale
        call['scale_taxonomy'] = 'SCHEDULED analytic scale; hidden constant absent; NOT executed queries'
        calls.append(call)
        return call['sat']

    status = 'complete'
    while upper - lower > 1:
        target = (lower + upper) // 2
        answer = detect(target)
        if answer is None:
            status = 'capped_undecided'
            break
        if answer:
            lower = target
        else:
            upper = target
    witness = initial_witness if lower == initial_lower else None
    prefix = ()
    if status == 'complete' and lower > initial_lower:
        for d in range(n):
            answer = detect(lower, prefix + (0,), 'witness')
            if answer is None:
                status = 'capped_witness'
                break
            prefix += (0 if answer else 1,)
        if status == 'complete':
            order = exact_order(weights, values)
            witness = [0] * n
            for j, i in enumerate(order):
                witness[i] = prefix[j]
    valid_witness = witness is not None and sum(w*x for w,x in zip(weights,witness)) <= capacity and sum(v*x for v,x in zip(values,witness)) == lower
    return dict(status=status, lower=lower, upper_exclusive=upper,
                initial_lower=initial_lower, witness=witness, witness_valid=valid_witness,
                certificate=cert, calls=calls, total_nodes=total_nodes,
                conditional_detection_scale_sum=sum(c['conditional_detection_scale'] for c in calls),
                seconds=time.perf_counter()-start, max_calls=max_calls, delta=delta,
                taxonomy='CLASSICAL STRUCTURAL ACCOUNTING; schedules SCHEDULED; no quantum decisions')
