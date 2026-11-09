"""Compiled clean knapsack pruning predicates; no walk or hardware execution.

Gate resources are DERIVED; sparse basis-column propagation is SIMULATED.
See research_log/pruning_study_20261023/circuit_derivation_before_implementation.md.
All choices depend only on instance data, never optima or measured tree sizes.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
import time
from typing import Sequence

try:
    from ..oracle_h.node_bound_reversible import (
        BooleanCompiler, NodeBoundCircuit, bits, exact_order,
    )
except ImportError:
    from oracle_h.node_bound_reversible import (
        BooleanCompiler, NodeBoundCircuit, bits, exact_order,
    )


@dataclass(frozen=True)
class BuildBudget:
    max_qubits: int = 250_000
    max_gates: int = 1_000_000
    max_seconds: float = 30.0


class CircuitBuildCap(RuntimeError):
    def __init__(self, reason, counters):
        self.reason, self.counters = reason, counters
        super().__init__(f"Circuit build capped: {reason}; {counters}")


class BudgetCompiler(BooleanCompiler):
    def __init__(self, inputs, budget=None):
        self.budget = budget or BuildBudget()
        self.started = time.monotonic()
        super().__init__(inputs)
        self.check()

    def check(self, extra_gates=0):
        counters = {"qubits": self.next_wire - 2,
                    "gates": len(self.gates),
                    "projected_gates": len(self.gates) + extra_gates,
                    "elapsed_seconds": time.monotonic() - self.started,
                    "classification": "MEASURED_BUILD_COUNTERS"}
        if counters["qubits"] > self.budget.max_qubits:
            raise CircuitBuildCap("qubit_budget", counters)
        if counters["projected_gates"] > self.budget.max_gates:
            raise CircuitBuildCap("gate_budget", counters)
        if counters["elapsed_seconds"] > self.budget.max_seconds:
            raise CircuitBuildCap("build_time_budget", counters)

    def fresh(self):
        result = super().fresh()
        if self.next_wire > self.budget.max_qubits + 2 or self.next_wire % 256 == 0:
            self.check()
        return result

    def emit(self, target, *controls):
        if len(self.gates) >= self.budget.max_gates:
            self.check(1)
        super().emit(target, *controls)
        if len(self.gates) % 1024 == 0:
            self.check()

    def append_gates(self, gates):
        gates = list(gates)
        self.check(len(gates))
        self.gates.extend(gates)

    def finish(self, result):
        forward = list(self.gates)
        self.check(len(forward) + int(result != 0))
        if result == 1:
            self.emit(self.output)
        elif result:
            self.emit(self.output, result)
        self.append_gates(reversed(forward))
        return self.gates


@dataclass
class StudyCircuit(NodeBoundCircuit):
    metadata: dict = field(default_factory=dict)

    def resources(self):
        result = super().resources()
        result["classification"] = "DERIVED"
        return result


def _data(weights, values, capacity):
    weights, values = tuple(weights), tuple(values)
    if (len(weights) != len(values) or not isinstance(capacity, int) or capacity < 0
            or any(not isinstance(x, int) or x <= 0 for x in weights + values)):
        raise ValueError("Matching positive integer data and nonnegative integer capacity required")
    return weights, values, capacity


def threshold_bits(values):
    """Same full threshold domain as the preserved fixed-point baseline."""
    return max(1, (sum(values) + 1).bit_length())


def root_multiplier(weights, values, capacity):
    weights, values, capacity = _data(weights, values, capacity)
    rem = capacity
    for i in exact_order(weights, values):
        if weights[i] > rem:
            return Fraction(values[i], weights[i])
        rem -= weights[i]
    return Fraction(0)


def multiplier_bank(weights, values, capacity, q=2):
    """Predeclared nested bank: root; +0; +minimum and maximum densities."""
    if q not in (1, 2, 4):
        raise ValueError("q must be 1, 2 or 4")
    weights, values, capacity = _data(weights, values, capacity)
    choices = [root_multiplier(weights, values, capacity)]
    if q >= 2:
        choices.append(Fraction(0))
    if q == 4 and weights:
        ratios = [Fraction(v, w) for w, v in zip(weights, values)]
        choices.extend([min(ratios), max(ratios)])
    return tuple(dict.fromkeys(choices))


def _less(comp, left, right):
    _, ge = comp.sub(left, right)
    return comp.neg(ge)


def _wrap(comp, order, tb, db, pb, model, **metadata):
    comp.check()
    circuit = StudyCircuit(len(comp.inputs), comp.next_wire - 2, comp.output - 2,
                           comp.gates, tuple(order), -1, -1, -1, tb,
                           {"model": model, "scope": "compiled_clean_pruning_predicate",
                            "build_seconds": time.monotonic() - comp.started,
                            "build_seconds_classification": "MEASURED",
                            **metadata})
    circuit.depth_register_bits, circuit.prefix_width = db, pb
    return circuit


def _prefix_state(comp, weights, values, capacity, order, fixed_depth=None):
    m = len(weights)
    db = max(1, m.bit_length()) if fixed_depth is None else 0
    pb = m if fixed_depth is None else fixed_depth
    if fixed_depth is None:
        dreg = comp.inputs[m:m + db]
        assigned = []
        for j in range(m):
            _, le = comp.sub(bits(j, db), dreg)
            assigned.append(comp.neg(le))
        _, valid = comp.sub(bits(m, db), dreg)
    else:
        assigned, valid = [int(j < fixed_depth) for j in range(m)], 1
    wb = max(1, (capacity + sum(weights)).bit_length() + 1)
    weight = [0] * wb
    selected = []
    for j, i in enumerate(order):
        flag = comp.land(assigned[j], comp.inputs[j] if j < pb else 0)
        selected.append(flag)
        weight, _ = comp.add(weight, [comp.land(flag, x) for x in bits(weights[i], wb)])
    rem, feasible = comp.sub(bits(capacity, wb), weight)
    return assigned, selected, valid, rem, feasible, wb


def build_dual_bank(weights, values, capacity, q=2, multipliers=None, budget=None):
    weights, values, capacity = _data(weights, values, capacity)
    if multipliers is None:
        multipliers = multiplier_bank(weights, values, capacity, q)
    multipliers = tuple(dict.fromkeys(Fraction(x) for x in multipliers))
    if not multipliers or any(x < 0 for x in multipliers):
        raise ValueError("Nonempty fixed bank of nonnegative rational multipliers required")
    m, order = len(weights), tuple(exact_order(weights, values))
    db, tb = max(1, m.bit_length()), threshold_bits(values)
    comp = BudgetCompiler(m + db + tb, budget)
    assigned, selected, valid, _, feasible, wb = _prefix_state(
        comp, weights, values, capacity, order)
    tau = comp.inputs[m + db:]
    reject, descriptions = 0, []
    for multiplier in multipliers:
        a, b = multiplier.numerator, multiplier.denominator
        r = [b * v - a * w for w, v in zip(weights, values)]
        n0 = a * capacity + sum(max(x, 0) for x in r)
        cb = max(n0, sum(abs(x) for x in r) + ((1 << tb) - 1) * b).bit_length() + 1
        loss = [0] * cb
        for j, i in enumerate(order):
            bad = selected[j] if r[i] < 0 else comp.land(assigned[j], comp.neg(comp.inputs[j]))
            loss, _ = comp.add(loss, [comp.land(bad, x) for x in bits(abs(r[i]), cb)])
        rhs = comp.const_mul(tau, b, cb)
        rhs, _ = comp.add(loss, rhs)
        reject = comp.lor(reject, _less(comp, bits(n0, cb), rhs))
        descriptions.append({"a": a, "b": b, "n0": n0, "width": cb})
    reject = comp.lor(comp.neg(valid), comp.lor(comp.neg(feasible), reject))
    comp.finish(reject)
    return _wrap(comp, order, tb, db, m, "dual_bank", q_requested=q,
                 multipliers=[[x.numerator, x.denominator] for x in multipliers],
                 bank_data=descriptions, weight_width=wb)


def build_root_dual(weights, values, capacity, budget=None):
    result = build_dual_bank(weights, values, capacity, q=1, budget=budget)
    result.metadata["model"] = "root_dual"
    return result


def build_simple(weights, values, capacity, budget=None):
    result = build_dual_bank(weights, values, capacity, multipliers=[Fraction(0)], budget=budget)
    result.metadata["model"] = "simple_remaining_profit"
    return result


def _build_exact(weights, values, capacity, depth=None, budget=None, fixed_point=False):
    weights, values, capacity = _data(weights, values, capacity)
    m, order = len(weights), tuple(exact_order(weights, values))
    if depth is not None and not 0 <= depth <= m:
        raise ValueError("Invalid fixed depth")
    db, pb, tb = (max(1, m.bit_length()) if depth is None else 0), (m if depth is None else depth), threshold_bits(values)
    comp = BudgetCompiler(pb + db + tb, budget)
    assigned, selected, valid, rem, feasible, wb = _prefix_state(
        comp, weights, values, capacity, order, depth)
    tau = comp.inputs[pb + db:]
    vb = max(1, sum(values).bit_length() + 1)
    pval = [0] * vb
    for flag, i in zip(selected, order):
        pval, _ = comp.add(pval, [comp.land(flag, x) for x in bits(values[i], vb)])
    wmax, vmax = max(weights, default=1), max(values, default=1)
    k = (wmax * wmax).bit_length() if fixed_point else 0
    if fixed_point:
        maxq = max(((v << k) // w for w, v in zip(weights, values)), default=0)
        cb = max(((sum(values) << k) + capacity * maxq) * wmax + (1 << k),
                 ((1 << tb) - 1) * (wmax << k)).bit_length() + 1
    else:
        cb = max(sum(values) * wmax + capacity * vmax, ((1 << tb) - 1) * wmax).bit_length() + 1
    active, split_reject = feasible, 0
    for j, i in enumerate(order):
        if depth is not None and j < depth:
            continue
        reduced, enough = comp.sub(rem, bits(weights[i], wb))
        scan = comp.land(active, comp.neg(assigned[j]))
        take, split = comp.land(scan, enough), comp.land(scan, comp.neg(enough))
        whole, _ = comp.add(pval, bits(values[i], vb))
        pval = comp.mux(take, whole, pval)
        if fixed_point:
            quotient = (values[i] << k) // weights[i]
            fraction = comp.const_mul(rem, quotient, cb)
            whole_scaled = ([0] * k + pval + [0] * cb)[:cb]
            total, _ = comp.add(whole_scaled, fraction)
            left = comp.const_mul(total, wmax, cb)
            left, _ = comp.add(left, bits(1 << k, cb))
            right = comp.const_mul(tau, wmax << k, cb)
            _, below = comp.sub(right, left)  # nonstrict safe comparison
        else:
            ratio = Fraction(values[i], weights[i])
            left = comp.const_mul(pval, ratio.denominator, cb)
            fraction = comp.const_mul(rem, ratio.numerator, cb)
            left, _ = comp.add(left, fraction)
            right = comp.const_mul(tau, ratio.denominator, cb)
            below = _less(comp, left, right)
        split_reject = comp.lor(split_reject, comp.land(split, below))
        rem = comp.mux(take, reduced, rem)
        active = comp.land(active, comp.neg(split))
    final_width = max(vb, tb)
    below = _less(comp, pval + [0] * (final_width - vb), tau + [0] * (final_width - tb))
    reject = comp.lor(comp.neg(valid), comp.lor(comp.neg(feasible),
                     comp.lor(split_reject, comp.land(active, below))))
    comp.finish(reject)
    model = "fixedpoint_single_scan" if fixed_point else ("exact_single_scan" if depth is None else "exact_fixed_depth")
    result = _wrap(comp, order, tb, db, pb, model, fixed_depth=depth,
                   weight_width=wb, value_width=vb, numerator_width=cb, precision_bits=k)
    result.k = k if fixed_point else -1
    return result


def build_exact_single_scan(weights, values, capacity, budget=None):
    return _build_exact(weights, values, capacity, budget=budget)


def build_fixedpoint_single_scan(weights, values, capacity, budget=None):
    return _build_exact(weights, values, capacity, budget=budget, fixed_point=True)


def build_exact_depth_wrapper(weights, values, capacity, budget=None):
    """Same depth dispatch as baseline; isolates arithmetic from architecture."""
    weights, values, capacity = _data(weights, values, capacity)
    m, db, tb = len(weights), max(1, len(weights).bit_length()), threshold_bits(values)
    comp = BudgetCompiler(m + db + tb, budget)
    families = []
    for depth in range(m + 1):
        comp.check()
        families.append(_build_exact(weights, values, capacity, depth=depth, budget=budget))
    dreg, flags = comp.inputs[m:m + db], []
    for depth in range(m + 1):
        flag = 1
        for j, wire in enumerate(dreg):
            flag = comp.land(flag, wire if (depth >> j) & 1 else comp.neg(wire))
        flags.append(flag)
    valid = 0
    for flag in flags:
        valid = comp.lor(valid, flag)
    invalid, prefix_gates = comp.neg(valid), list(comp.gates)
    if invalid == 1:
        comp.emit(comp.output)
    elif invalid:
        comp.emit(comp.output, invalid)
    temporary = comp.fresh() - 2
    workspace = [comp.fresh() - 2 for _ in range(max(c.num_qubits - c.num_inputs - 1 for c in families))]
    for depth, circuit in enumerate(families):
        mapping = {j: j for j in range(depth)}
        mapping.update({depth + j: m + db + j for j in range(tb)})
        mapping[circuit.output] = temporary
        for j, wire in enumerate(range(circuit.num_inputs + 1, circuit.num_qubits)):
            mapping[wire] = workspace[j]
        mapped = [(mapping[t], tuple(mapping[x] for x in cs)) for t, cs in circuit.gates]
        comp.append_gates(mapped)
        if flags[depth] == 1:
            comp.gates.append((comp.output - 2, (temporary,)))
        elif flags[depth]:
            comp.gates.append((comp.output - 2, (flags[depth] - 2, temporary)))
        comp.append_gates(mapped)
    comp.append_gates(reversed(prefix_gates))
    return _wrap(comp, families[0].order, tb, db, m, "exact_depth_wrapper")


BUILDERS = {"simple": build_simple, "root_dual": build_root_dual,
            "bank2": lambda w, v, c, **kw: build_dual_bank(w, v, c, q=2, **kw),
            "bank4": lambda w, v, c, **kw: build_dual_bank(w, v, c, q=4, **kw),
            "fixedpoint_single": build_fixedpoint_single_scan,
            "exact_single": build_exact_single_scan,
            "exact_wrapper": build_exact_depth_wrapper}
