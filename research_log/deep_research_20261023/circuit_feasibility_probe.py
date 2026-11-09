"""Isolated candidate circuits, never imported by manuscript reproduction code.

Derivations precede this file in circuit_derivation_before_probe.md.
All circuits use the existing transparent BooleanCompiler, including its
out-of-place workspace costs. No optimality, full-walk or hardware claim.
"""
from __future__ import annotations

import json
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "simulation"))
from oracle_h.node_bound_reversible import (
    BooleanCompiler, NodeBoundCircuit, bits, exact_order, exact_node_bound,
    build_coherent_node_bound,
)


def less(comp, left, right):
    """Unsigned strict comparison with equal-width nonoverflowing operands."""
    _, ge = comp.sub(left, right)
    return comp.neg(ge)


def build_exact(weights, values, capacity, depth=None, skip_assigned=True, reduce_ratio=True):
    """One exact cross-product scan; coherent depth when depth is None."""
    m, order = len(weights), tuple(exact_order(weights, values))
    db = max(1, m.bit_length()) if depth is None else 0
    pb = m if depth is None else depth
    tb = max(1, (sum(values) + 1).bit_length())
    comp = BooleanCompiler(pb + db + tb)
    tau = comp.inputs[pb + db:]
    if depth is None:
        dreg = comp.inputs[m:m + db]
        assigned = []
        for j in range(m):
            _, le = comp.sub(bits(j, db), dreg)
            assigned.append(comp.neg(le))  # j < d
        _, valid = comp.sub(bits(m, db), dreg)  # d <= m
    else:
        assigned, valid = [int(j < depth) for j in range(m)], 1
    wb = max(1, (capacity + sum(weights)).bit_length() + 1)
    vb = max(1, sum(values).bit_length() + 1)
    wsum, pval = [0] * wb, [0] * vb
    for j, item in enumerate(order):
        flag = comp.land(assigned[j], comp.inputs[j] if j < pb else 0)
        wsum, _ = comp.add(wsum, [comp.land(flag, b) for b in bits(weights[item], wb)])
        pval, _ = comp.add(pval, [comp.land(flag, b) for b in bits(values[item], vb)])
    rem, feasible = comp.sub(bits(capacity, wb), wsum)
    active, split_prune = feasible, 0
    wmax, vmax = max(weights, default=1), max(values, default=1)
    cb = max(sum(values) * wmax + capacity * vmax,
             ((1 << tb) - 1) * wmax).bit_length() + 1
    for j, item in enumerate(order):
        if skip_assigned and depth is not None and j < depth:
            continue  # Compile-time assigned positions have no suffix scan.
        reduced, enough = comp.sub(rem, bits(weights[item], wb))
        scan = comp.land(active, comp.neg(assigned[j]))
        take, split = comp.land(scan, enough), comp.land(scan, comp.neg(enough))
        full, _ = comp.add(pval, bits(values[item], vb))
        pval = comp.mux(take, full, pval)
        divisor = math.gcd(weights[item], values[item]) if reduce_ratio else 1
        denominator, numerator = weights[item] // divisor, values[item] // divisor
        left = comp.const_mul(pval, denominator, cb)
        term = comp.const_mul(rem, numerator, cb)
        left, _ = comp.add(left, term)
        right = comp.const_mul(tau, denominator, cb)
        split_prune = comp.lor(split_prune, comp.land(split, less(comp, left, right)))
        rem = comp.mux(take, reduced, rem)
        active = comp.land(active, comp.neg(split))
    width = max(vb, tb)
    final_below = less(comp, pval + [0] * (width - vb), tau + [0] * (width - tb))
    prune = comp.lor(comp.neg(feasible),
                     comp.lor(split_prune, comp.land(active, final_below)))
    prune = comp.lor(comp.neg(valid), prune)
    gates = comp.finish(prune)
    c = NodeBoundCircuit(pb + db + tb, comp.next_wire - 2, comp.output - 2,
                         gates, order, -1, -1 if depth is None else depth, -1, tb)
    c.depth_register_bits, c.prefix_width = db, pb
    return c


def wrap_exact(weights, values, capacity, skip_assigned=True, reduce_ratio=True):
    """Same compute-XOR-uncompute depth dispatch as current baseline."""
    m, db = len(weights), max(1, len(weights).bit_length())
    families = [build_exact(weights, values, capacity, d, skip_assigned, reduce_ratio) for d in range(m + 1)]
    tb = families[0].threshold_bits
    compiler = BooleanCompiler(m + db + tb)
    depth_wires, flags = compiler.inputs[m:m + db], []
    for d in range(m + 1):
        flag = 1
        for j, wire in enumerate(depth_wires):
            flag = compiler.land(flag, wire if (d >> j) & 1 else compiler.neg(wire))
        flags.append(flag)
    valid = 0
    for flag in flags:
        valid = compiler.lor(valid, flag)
    invalid = compiler.neg(valid)
    prefix_gates = list(compiler.gates)
    if invalid == 1:
        compiler.emit(compiler.output)
    elif invalid:
        compiler.emit(compiler.output, invalid)
    temporary = compiler.fresh() - 2
    workspace = [compiler.fresh() - 2 for _ in range(max(
        c.num_qubits - c.num_inputs - 1 for c in families))]
    for d, c in enumerate(families):
        mapping = {j: j for j in range(d)}
        mapping.update({d + j: m + db + j for j in range(tb)})
        mapping[c.output] = temporary
        for j, q in enumerate(range(c.num_inputs + 1, c.num_qubits)):
            mapping[q] = workspace[j]
        mapped = [(mapping[t], tuple(mapping[q] for q in cs)) for t, cs in c.gates]
        compiler.gates.extend(mapped)
        if flags[d] == 1:
            compiler.gates.append((compiler.output - 2, (temporary,)))
        elif flags[d]:
            compiler.gates.append((compiler.output - 2, (flags[d] - 2, temporary)))
        compiler.gates.extend(mapped)
    compiler.gates.extend(reversed(prefix_gates))
    result = NodeBoundCircuit(m + db + tb, compiler.next_wire - 2,
                             compiler.output - 2, compiler.gates,
                             families[0].order, -1, -1, -1, tb)
    result.depth_register_bits, result.prefix_width = db, m
    return result


def dual_constants(weights, values, capacity):
    rem = capacity
    for i in exact_order(weights, values):
        if weights[i] <= rem:
            rem -= weights[i]
        else:
            a, b = values[i], weights[i]
            divisor = math.gcd(a, b)
            a, b = a // divisor, b // divisor
            break
    else:
        a, b = 0, 1
    r = [b * v - a * w for w, v in zip(weights, values)]
    n0 = a * capacity + sum(max(x, 0) for x in r)
    return a, b, r, n0


def build_dual(weights, values, capacity):
    m, db = len(weights), max(1, len(weights).bit_length())
    order = tuple(exact_order(weights, values))
    tb = max(1, (sum(values) + 1).bit_length())
    a, b, coefficients, n0 = dual_constants(weights, values, capacity)
    comp = BooleanCompiler(m + db + tb)
    dreg, tau = comp.inputs[m:m + db], comp.inputs[m + db:]
    _, valid = comp.sub(bits(m, db), dreg)
    wb = (capacity + sum(weights)).bit_length() + 1
    cb = max(n0, sum(abs(x) for x in coefficients) + ((1 << tb) - 1) * b).bit_length() + 1
    weight, loss = [0] * wb, [0] * cb
    for j, i in enumerate(order):
        _, le = comp.sub(bits(j, db), dreg)
        assigned = comp.neg(le)
        selected = comp.land(assigned, comp.inputs[j])
        weight, _ = comp.add(weight, [comp.land(selected, x) for x in bits(weights[i], wb)])
        bad_choice = comp.inputs[j] if coefficients[i] < 0 else comp.neg(comp.inputs[j])
        penalty_flag = comp.land(assigned, bad_choice)
        loss, _ = comp.add(loss, [comp.land(penalty_flag, x) for x in bits(abs(coefficients[i]), cb)])
    _, feasible = comp.sub(bits(capacity, wb), weight)
    threshold_product = comp.const_mul(tau, b, cb)
    right, _ = comp.add(loss, threshold_product)
    below = less(comp, bits(n0, cb), right)
    result = comp.lor(comp.neg(valid), comp.lor(comp.neg(feasible), below))
    gates = comp.finish(result)
    c = NodeBoundCircuit(m + db + tb, comp.next_wire - 2, comp.output - 2,
                         gates, order, -1, -1, -1, tb)
    c.depth_register_bits, c.prefix_width = db, m
    c.dual_parameters = {"a": a, "b": b, "n0": n0}
    return c


def dual_value(weights, values, capacity, depth, prefix):
    order = exact_order(weights, values)
    _, b, coefficients, n0 = dual_constants(weights, values, capacity)
    chosen = [order[j] for j in range(depth) if (prefix >> j) & 1]
    if sum(weights[i] for i in chosen) > capacity:
        return None
    loss = 0
    for j in range(depth):
        r = coefficients[order[j]]
        loss += max(-r, 0) if (prefix >> j) & 1 else max(r, 0)
    return Fraction(n0 - loss, b)


def verify(circuit, weights, values, capacity, bound_fn):
    m, db = len(weights), circuit.depth_register_bits
    inputs = range(1 << circuit.num_inputs)
    mismatch, dirty = 0, 0
    for target in (0, 1):
        flags, garbage = circuit.simulate_columns(inputs, target)
        dirty += garbage
        for encoded, flag in enumerate(flags):
            prefix = encoded & ((1 << m) - 1)
            depth = (encoded >> m) & ((1 << db) - 1)
            tau = encoded >> (m + db)
            value = None if depth > m else bound_fn(weights, values, capacity, depth, prefix)
            mismatch += flag != (target ^ int(value is None or value < tau))
    return {"classification": "SIMULATED", "columns": 2 * len(inputs),
            "predicate_mismatches": mismatch, "dirty_columns": dirty}


def main():
    out = {"scope": "Candidate-only isolated pilot. Not full walk; not IBM; not 700-instance validation.",
           "derivation": "circuit_derivation_before_probe.md", "small": [], "resource_only": []}
    cases = [([2, 3, 4, 5], [3, 4, 5, 8], 8),
             ([3, 5, 7, 8], [3, 5, 7, 8], 13),
             ([4, 7, 6], [5, 6, 2], 7),
             ([1, 2], [3, 2], 0),
             ([2, 3], [2, 3], 5)]
    for weights, values, capacity in cases:
        row = {"weights": weights, "values": values, "capacity": capacity, "circuits": {}}
        circuits = {"baseline_fixedpoint_wrapper": build_coherent_node_bound(weights, values, capacity),
                    "exact_wrapper_initial_wasted_arithmetic": wrap_exact(weights, values, capacity, False, False),
                    "exact_wrapper_skip_assigned_only": wrap_exact(weights, values, capacity, True, False),
                    "exact_crossproduct_wrapper": wrap_exact(weights, values, capacity),
                    "exact_crossproduct_single_scan": build_exact(weights, values, capacity),
                    "root_dual_single_scan": build_dual(weights, values, capacity)}
        for name, c in circuits.items():
            value_fn = dual_value if name.startswith("root_dual") else exact_node_bound
            row["circuits"][name] = {"resources": c.resources(),
                                     "verification": verify(c, weights, values, capacity, value_fn)}
        # Exact LP is <= root dual on every feasible prefix, independent of tau.
        violations, prefixes = 0, 0
        for d in range(len(weights) + 1):
            for p in range(1 << d):
                lp = exact_node_bound(weights, values, capacity, d, p)
                dual = dual_value(weights, values, capacity, d, p)
                if lp is not None:
                    prefixes += 1
                    violations += lp > dual
        row["dual_bound_check"] = {"classification": "SIMULATED", "feasible_prefixes": prefixes,
                                    "lp_exceeds_dual": violations}
        out["small"].append(row)
        print(json.dumps(row), flush=True)
    for n, magnitude, seed in [(8, 100, 101), (12, 100, 102), (8, 1000000, 103)]:
        rng = random.Random(seed)
        w, v = [rng.randint(1, magnitude) for _ in range(n)], [rng.randint(1, magnitude) for _ in range(n)]
        cap = sum(w) // 2
        row = {"n": n, "magnitude": magnitude, "seed": seed, "weights": w, "values": v,
               "capacity": cap, "classification": "DERIVED", "resources": {}}
        for name, builder in [("baseline_fixedpoint_wrapper", build_coherent_node_bound),
                              ("exact_wrapper_initial_wasted_arithmetic", lambda w,v,c: wrap_exact(w,v,c,False,False)),
                              ("exact_wrapper_skip_assigned_only", lambda w,v,c: wrap_exact(w,v,c,True,False)),
                              ("exact_crossproduct_wrapper", wrap_exact),
                              ("exact_crossproduct_single_scan", build_exact),
                              ("root_dual_single_scan", build_dual)]:
            row["resources"][name] = builder(w, v, cap).resources()
        out["resource_only"].append(row)
        print(json.dumps(row), flush=True)
    path = Path(__file__).with_name("circuit_feasibility_probe_results.json")
    path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    assert all(r["dual_bound_check"]["lp_exceeds_dual"] == 0 for r in out["small"])
    assert all(c["verification"]["predicate_mismatches"] == c["verification"]["dirty_columns"] == 0
               for r in out["small"] for c in r["circuits"].values())


if __name__ == "__main__":
    main()
