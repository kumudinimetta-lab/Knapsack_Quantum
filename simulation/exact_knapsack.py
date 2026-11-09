"""Exact integer/rational reference primitives for the revised experiments."""
from fractions import Fraction


def efficiency_order(weights, values):
    return sorted(range(len(weights)), key=lambda i: Fraction(values[i], weights[i]),
                  reverse=True)


def lp_bound(weights, values, capacity, items=None):
    if capacity < 0:
        return -float("inf")
    items = range(len(weights)) if items is None else items
    order = sorted(items, key=lambda i: Fraction(values[i], weights[i]), reverse=True)
    rem, result = capacity, Fraction(0)
    for i in order:
        if weights[i] <= rem:
            rem -= weights[i]
            result += values[i]
        else:
            result += Fraction(rem * values[i], weights[i])
            break
    return result


def reduced_cost_fixing(n, weights, values, capacity):
    order = efficiency_order(weights, values)
    rem, lower = capacity, 0
    for i in order:
        if weights[i] <= rem:
            rem -= weights[i]
            lower += values[i]
    before, cumulative = set(), 0
    for i in order:
        cumulative += weights[i]
        if cumulative > capacity:
            break
        before.add(i)
    fi, core, fo = [], [], []
    for i in range(n):
        others = [j for j in order if j != i]
        if i in before:
            upper = lp_bound(weights, values, capacity, others)
            (fi if upper < lower else core).append(i)
        else:
            if weights[i] > capacity:
                fo.append(i)
                continue
            upper = values[i] + lp_bound(weights, values, capacity - weights[i], others)
            (fo if upper < lower else core).append(i)
    return fi, core, fo


def branch_and_bound(weights, values, capacity, use_lp=True, max_nodes=500000):
    n = len(weights)
    order = efficiency_order(weights, values)
    best = nodes = pruned = maximum_depth = 0
    stack = [(0, 0, 0)]
    while stack and nodes < max_nodes:
        level, weight, value = stack.pop()
        nodes += 1
        maximum_depth = max(maximum_depth, level)
        if level == n:
            best = max(best, value)
            continue
        if use_lp:
            rem, upper = capacity - weight, Fraction(value)
            for i in order[level:]:
                if weights[i] <= rem:
                    rem -= weights[i]
                    upper += values[i]
                else:
                    upper += Fraction(rem * values[i], weights[i])
                    break
            if upper <= best:
                pruned += 1
                continue
        i = order[level]
        stack.append((level + 1, weight, value))
        if weight + weights[i] <= capacity:
            stack.append((level + 1, weight + weights[i], value + values[i]))
    return best, nodes, pruned, maximum_depth, bool(stack)


def dynamic_programming(weights, values, capacity):
    table = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for c in range(capacity, w - 1, -1):
            table[c] = max(table[c], table[c - w] + v)
    return table[capacity]
