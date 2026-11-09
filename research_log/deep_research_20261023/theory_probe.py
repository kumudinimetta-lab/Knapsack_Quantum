"""Isolated exact classical probes; no quantum runtime/novelty claim."""
import itertools
import json
import math
import random
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'simulation'))
from exact_knapsack import efficiency_order, lp_bound, dynamic_programming
from benchmark_v5 import (gen_uncorrelated, gen_weakly_correlated,
                          gen_strongly_correlated, gen_subset_sum,
                          gen_inverse_strongly)

OUT = Path(__file__).with_name('theory_probe_results.json')


def constants(w, v, W):
    order = efficiency_order(w, v)
    rem = W
    lam = Fraction(0)
    for i in order:
        if w[i] <= rem:
            rem -= w[i]
        else:
            lam = Fraction(v[i], w[i])
            break
    a, b = lam.numerator, lam.denominator
    rc = [b * vi - a * wi for wi, vi in zip(w, v)]
    A = a * W + sum(max(r, 0) for r in rc)
    return order, a, b, rc, A


def exact_certificate(costs, H):
    """Count generated nodes, including rejected children, ignoring capacity."""
    if H < 0:
        return 1, 0
    counts = {0: 1}
    internal = 0
    states = 1
    for cost in costs:
        internal += sum(counts.values())
        new = defaultdict(int)
        for val, num in counts.items():
            new[val] += num
            if val + cost <= H:
                new[val + cost] += num
        counts = dict(new)
        states += len(counts)
    return 1 + 2 * internal, states


def cheap_certificate(costs, H):
    if H < 0:
        return 1
    total = 1
    for d in range(len(costs)):
        pref = costs[:d]
        best = 1 << d
        for t in sorted({1, *[x for x in pref if x > 0]}):
            small = sum(x < t for x in pref)
            large = d - small
            k = min(large, H // t)
            bound = (1 << small) * sum(math.comb(large, j) for j in range(k + 1))
            best = min(best, bound)
        total += 2 * best
    return total


def static_tree(w, v, W, tau, kind, cap=50000):
    order, a, b, rc, A = constants(w, v, W)
    n = len(w)
    suffix = [0] * (n + 1)
    for d in reversed(range(n)):
        suffix[d] = suffix[d + 1] + v[order[d]]
    stack = [(0, 0, 0, 0)]
    nodes = marked = 0
    while stack and nodes < cap:
        d, weight, value, penalty = stack.pop()
        nodes += 1
        if weight > W:
            continue
        if kind == 'dual':
            reject = A - penalty < b * tau
        elif kind == 'lp':
            reject = value + lp_bound(w, v, W - weight, order[d:]) < tau
        else:
            reject = value + suffix[d] < tau
        if reject:
            continue
        if d == n:
            marked += value >= tau
            continue
        i = order[d]
        z = int(rc[i] > 0)
        cost = abs(rc[i])
        stack.append((d + 1, weight + w[i], value + v[i], penalty + cost * (1 != z)))
        stack.append((d + 1, weight, value, penalty + cost * (0 != z)))
    return dict(nodes=nodes, marked=marked, capped=bool(stack))


def falsification():
    rng = random.Random(20261023)
    result = dict(instances=0, prefix_cases=0, upper_bound_failures=0,
                  unsafe_rejects=0, dual_versus_lp_tree_failures=0,
                  certificate_failures=0, finite_bank_lp_mismatches=0)
    first_failures = []
    for case in range(120):
        n = rng.randrange(0, 9)
        w = [rng.randrange(1, 16) for _ in range(n)]
        v = [rng.randrange(1, 16) for _ in range(n)]
        W = rng.randrange(0, sum(w) + 5)
        order, a, b, rc, A = constants(w, v, W)
        result['instances'] += 1
        multipliers = {Fraction(0), *[Fraction(vi, wi) for wi, vi in zip(w, v)]}
        for d in range(n + 1):
            for pref in itertools.product((0, 1), repeat=d):
                weight = sum(w[i] * bit for i, bit in zip(order[:d], pref))
                value = sum(v[i] * bit for i, bit in zip(order[:d], pref))
                penalty = sum(abs(rc[i]) * (bit != int(rc[i] > 0))
                              for i, bit in zip(order[:d], pref))
                if weight > W:
                    continue
                exact_lp = value + lp_bound(w, v, W - weight, order[d:])
                dual = Fraction(A - penalty, b)
                result['prefix_cases'] += 1
                if dual < exact_lp:
                    result['upper_bound_failures'] += 1
                    first_failures.append([w, v, W, pref, str(exact_lp), str(dual)])
                # Independent finite-family multiplier envelope must equal LP.
                bank = min(value + lam * (W - weight) +
                           sum(max(Fraction(v[i]) - lam * w[i], 0) for i in order[d:])
                           for lam in multipliers)
                result['finite_bank_lp_mismatches'] += bank != exact_lp
                for tau in {0, value, int(exact_lp), int(exact_lp) + 1, sum(v) + 1}:
                    if dual < tau and exact_lp >= tau:
                        result['unsafe_rejects'] += 1
        opt = dynamic_programming(w, v, W)
        for tau in {opt, opt + 1}:
            dual = static_tree(w, v, W, tau, 'dual', cap=1000000)
            lp = static_tree(w, v, W, tau, 'lp', cap=1000000)
            costs = [abs(rc[i]) for i in order]
            exact, _ = exact_certificate(costs, A - b * tau)
            cheap = cheap_certificate(costs, A - b * tau)
            result['dual_versus_lp_tree_failures'] += lp['nodes'] > dual['nodes']
            result['certificate_failures'] += (dual['nodes'] > exact or exact > cheap)
    result['first_failures'] = first_failures[:5]
    return result


def benchmark():
    rows = []
    gens = [gen_uncorrelated, gen_weakly_correlated, gen_strongly_correlated,
            gen_subset_sum, gen_inverse_strongly]
    for n in [12, 16, 20]:
        for gen in gens:
            for trial in range(3):
                seed = n * 1000 + trial
                w, v, W, cls = gen(n, seed=seed, R=100)
                opt = dynamic_programming(w, v, W)
                order, a, b, rc, A = constants(w, v, W)
                # Greedy feasible witness: scan exact efficiency order, skipping overweight items.
                used = lower = 0
                for i in order:
                    if used + w[i] <= W:
                        used += w[i]
                        lower += v[i]
                for target_kind, tau in [('incumbent_plus_one', lower + 1),
                                         ('optimum_plus_one', opt + 1)]:
                    H = A - b * tau
                    costs = [abs(rc[i]) for i in order]
                    exact, dpstates = exact_certificate(costs, H)
                    cheap = cheap_certificate(costs, H)
                    trees = {kind: static_tree(w, v, W, tau, kind) for kind in ['simple', 'dual', 'lp']}
                    rows.append(dict(n=n, seed=seed, instance_class=cls, weights=w,
                                     values=v, capacity=W, optimum=opt, incumbent=lower,
                                     target_kind=target_kind, tau=tau, multiplier=[a, b],
                                     exact_certificate=exact, cheap_certificate=cheap,
                                     dpstates=dpstates, full_binary_bound=(1 << (n + 1)) - 1,
                                     trees=trees))
    return rows


if __name__ == '__main__':
    data = dict(description='Isolated theory feasibility pilot; NOT quantum execution.',
                taxonomy={'tree_counts': 'MEASURED (classical enumeration)',
                          'certificate_bounds': 'DERIVED (exact integer computation)',
                          'optimum': 'DERIVED (exact classical DP)',
                          'cap': 'HARDCODED 50000 nodes per tree'},
                falsification=falsification(), rows=benchmark())
    OUT.write_text(json.dumps(data, indent=2), encoding='utf8')
    print(json.dumps(data['falsification']))
    print('benchmark rows', len(data['rows']), 'saved', OUT)
