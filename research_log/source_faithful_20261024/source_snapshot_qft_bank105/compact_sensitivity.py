"""Separate fixed-depth ripple-arithmetic sensitivity control.

Simple Cuccaro MAJ/UMA, not its optimized Section 3 circuit. No change to the
pinned production module. No coherent depth dispatcher or full walk.
"""
from __future__ import annotations

from fractions import Fraction
import time

from .circuits import (
    BudgetCompiler, BuildBudget, CircuitBuildCap, StudyCircuit,
    _data, _build_exact, _less, _wrap, root_multiplier, threshold_bits,
)
try:
    from ..oracle_h.node_bound_reversible import bits, exact_order
except ImportError:
    from oracle_h.node_bound_reversible import bits, exact_order


class Ripple:
    def __init__(self, inputs, scratch_width=0, budget=None):
        self.inputs, self.output = list(range(inputs)), inputs
        self.next_wire, self.gates = inputs + 1, []
        self.started, self.budget = time.monotonic(), budget or BuildBudget()
        self.carry = self.allocate(1)[0]
        self.scratch = self.allocate(scratch_width)

    def allocate(self, size):
        result = list(range(self.next_wire, self.next_wire + size))
        self.next_wire += size
        self.check()
        return result

    def check(self):
        count = {"qubits": self.next_wire, "gates": len(self.gates),
                 "elapsed_seconds": time.monotonic() - self.started,
                 "classification": "MEASURED_BUILD_COUNTERS"}
        if self.next_wire > self.budget.max_qubits:
            raise CircuitBuildCap("qubit_budget", count)
        if len(self.gates) > self.budget.max_gates:
            raise CircuitBuildCap("gate_budget", count)
        if count["elapsed_seconds"] > self.budget.max_seconds:
            raise CircuitBuildCap("build_time_budget", count)

    def emit(self, target, *controls):
        if target in controls or len(set(controls)) != len(controls) or len(controls) > 2:
            raise ValueError("Invalid primitive wires")
        self.gates.append((target, tuple(controls)))
        if len(self.gates) % 1024 == 0:
            self.check()

    def extend(self, gates):
        self.gates.extend(gates)
        self.check()

    @staticmethod
    def maj(a, b, c):
        return [(b, (a,)), (c, (a,)), (a, (c, b))]

    @staticmethod
    def uma(a, b, c):
        return [(a, (c, b)), (c, (a,)), (b, (c,))]

    def adder(self, a, b):
        if len(a) != len(b):
            raise ValueError("Adder widths must match")
        gates = []
        for i in range(len(a)):
            gates.extend(self.maj(a[i], b[i], self.carry if i == 0 else a[i - 1]))
        for i in reversed(range(len(a))):
            gates.extend(self.uma(a[i], b[i], self.carry if i == 0 else a[i - 1]))
        return gates

    def controlled_constant(self, destination, constant, control=None, subtract=False):
        if constant == 0:
            return
        if constant < 0 or constant >= 1 << len(destination):
            raise ValueError("Constant does not fit destination")
        source = self.scratch[:len(destination)]
        loads = [(source[j], () if control is None else (control,))
                 for j in range(len(source)) if (constant >> j) & 1]
        self.extend(loads)
        adder = self.adder(source, destination)
        self.extend(reversed(adder) if subtract else adder)
        self.extend(reversed(loads))

    def variable_add(self, destination, source, shift=0, subtract=False):
        scratch = self.scratch[:len(destination)]
        copies = [(scratch[j + shift], (wire,)) for j, wire in enumerate(source)
                  if j + shift < len(destination)]
        self.extend(copies)
        adder = self.adder(scratch, destination)
        self.extend(reversed(adder) if subtract else adder)
        self.extend(reversed(copies))

    def product_add(self, destination, source, constant):
        for j in range(constant.bit_length()):
            if (constant >> j) & 1:
                self.variable_add(destination, source, j)

    def less(self, left, right, target):
        if len(left) != len(right):
            raise ValueError("Comparator widths must match")
        for wire in right:
            self.emit(wire)
        self.emit(self.carry)
        majority = []
        for i in range(len(left)):
            majority.extend(self.maj(left[i], right[i], self.carry if i == 0 else left[i - 1]))
        self.extend(majority)
        self.emit(target)
        self.emit(target, left[-1])  # NOT carry = unsigned strict less
        self.extend(reversed(majority))
        self.emit(self.carry)
        for wire in reversed(right):
            self.emit(wire)

    def const_less(self, value, register, target, constant_on_left=True):
        constant = self.scratch[:len(register)]
        loads = [(constant[j], ()) for j in range(len(constant)) if (value >> j) & 1]
        self.extend(loads)
        self.less(constant if constant_on_left else register,
                  register if constant_on_left else constant, target)
        self.extend(reversed(loads))

    def finish(self, output_controls, *, union=False):
        forward = list(self.gates)
        for controls in output_controls:
            self.emit(self.output, *controls)
        if union:
            if len(output_controls) != 2 or any(len(x) != 1 for x in output_controls):
                raise ValueError("Union expects exactly two single flags")
            self.emit(self.output, output_controls[0][0], output_controls[1][0])
        self.extend(reversed(forward))
        self.check()

    def circuit(self, order, threshold_width, depth, model, **metadata):
        c = StudyCircuit(len(self.inputs), self.next_wire, self.output, self.gates,
                         tuple(order), -1, depth, -1, threshold_width,
                         {"model": model, "scope": "fixed_depth_pruning_predicate",
                          "arithmetic": "simple_Cuccaro_Section2_MAJ_UMA",
                          "build_seconds": time.monotonic() - self.started,
                          "build_seconds_classification": "MEASURED", **metadata})
        c.depth_register_bits, c.prefix_width = 0, depth
        return c


def build_compact_root_dual(weights, values, capacity, depth, budget=None):
    weights, values, capacity = _data(weights, values, capacity)
    if not 0 <= depth <= len(weights):
        raise ValueError("Invalid depth")
    order, tb = tuple(exact_order(weights, values)), threshold_bits(values)
    lam = root_multiplier(weights, values, capacity)
    a, b = lam.numerator, lam.denominator
    reduced = [b * v - a * w for w, v in zip(weights, values)]
    n0 = a * capacity + sum(max(x, 0) for x in reduced)
    wb = max(1, (capacity + sum(weights)).bit_length() + 1)
    cb = max(n0, sum(abs(x) for x in reduced) + ((1 << tb) - 1) * b).bit_length() + 1
    c = Ripple(depth + tb, max(wb, cb), budget)
    weight, loss = c.allocate(wb), c.allocate(cb)
    bad_capacity, bad_bound = c.allocate(2)
    for j, item in enumerate(order[:depth]):
        x = c.inputs[j]
        c.controlled_constant(weight, weights[item], x)
        r = reduced[item]
        if r > 0:
            c.emit(x)
        c.controlled_constant(loss, abs(r), x)
        if r > 0:
            c.emit(x)
    c.product_add(loss, c.inputs[depth:], b)
    c.const_less(capacity, weight, bad_capacity)
    c.const_less(n0, loss, bad_bound)
    c.finish([(bad_capacity,), (bad_bound,)], union=True)
    return c.circuit(order, tb, depth, "compact_root_dual", multiplier=[a, b],
                     weight_width=wb, loss_width=cb)


def build_compact_exact(weights, values, capacity, depth, budget=None):
    weights, values, capacity = _data(weights, values, capacity)
    if not 0 <= depth <= len(weights):
        raise ValueError("Invalid depth")
    order, tb = tuple(exact_order(weights, values)), threshold_bits(values)
    wb, vb = max(1, (capacity + sum(weights)).bit_length() + 1), max(1, sum(values).bit_length() + 1)
    cb = max(sum(values) * max(weights, default=1) + capacity * max(values, default=1),
             ((1 << tb) - 1) * max(weights, default=1)).bit_length() + 1
    c = Ripple(depth + tb, max(wb, vb, cb), budget)
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
    output_controls = [(bad_capacity,)]
    for item in order[depth:]:
        enough, take, split, below = c.allocate(4)
        c.const_less(weights[item], residual, enough, constant_on_left=False)
        c.emit(enough)  # residual >= weight
        c.emit(take, active, enough)
        c.emit(enough)
        c.emit(split, active, enough)
        c.emit(enough)
        c.controlled_constant(pval, values[item], take)
        c.controlled_constant(residual, weights[item], take, subtract=True)
        ratio = Fraction(values[item], weights[item])
        product_start = len(c.gates)
        c.product_add(numerator, pval, ratio.denominator)
        c.product_add(numerator, residual, ratio.numerator)
        c.product_add(threshold, c.inputs[depth:], ratio.denominator)
        products = list(c.gates[product_start:])
        c.less(numerator, threshold, below)
        c.extend(reversed(products))
        output_controls.append((split, below))
        active = take
    below_integer = c.allocate(1)[0]
    product_start = len(c.gates)
    c.variable_add(numerator, pval)
    c.variable_add(threshold, c.inputs[depth:])
    products = list(c.gates[product_start:])
    c.less(numerator, threshold, below_integer)
    c.extend(reversed(products))
    output_controls.append((active, below_integer))
    c.finish(output_controls)
    return c.circuit(order, tb, depth, "compact_exact", weight_width=wb,
                     value_width=vb, numerator_width=cb)


def build_outplace_fixed_root_dual(weights, values, capacity, depth, budget=None):
    """Fair fixed-depth counterpart with the pinned Boolean arithmetic compiler."""
    weights, values, capacity = _data(weights, values, capacity)
    if not 0 <= depth <= len(weights):
        raise ValueError("Invalid depth")
    order, tb = tuple(exact_order(weights, values)), threshold_bits(values)
    lam = root_multiplier(weights, values, capacity)
    a, b = lam.numerator, lam.denominator
    coefficients = [b * v - a * w for w, v in zip(weights, values)]
    n0 = a * capacity + sum(max(x, 0) for x in coefficients)
    wb = max(1, (capacity + sum(weights)).bit_length() + 1)
    cb = max(n0, sum(abs(x) for x in coefficients) + ((1 << tb) - 1) * b).bit_length() + 1
    comp = BudgetCompiler(depth + tb, budget)
    weight, loss = [0] * wb, [0] * cb
    for j, i in enumerate(order[:depth]):
        flag = comp.inputs[j]
        weight, _ = comp.add(weight, [comp.land(flag, x) for x in bits(weights[i], wb)])
        bad = flag if coefficients[i] < 0 else comp.neg(flag)
        loss, _ = comp.add(loss, [comp.land(bad, x) for x in bits(abs(coefficients[i]), cb)])
    rhs = comp.const_mul(comp.inputs[depth:], b, cb)
    rhs, _ = comp.add(loss, rhs)
    _, feasible = comp.sub(bits(capacity, wb), weight)
    below = _less(comp, bits(n0, cb), rhs)
    comp.finish(comp.lor(comp.neg(feasible), below))
    result = _wrap(comp, order, tb, 0, depth, "outplace_fixed_root_dual", multiplier=[a, b])
    result.depth = depth
    return result


def build_outplace_fixed_exact(weights, values, capacity, depth, budget=None):
    return _build_exact(weights, values, capacity, depth=depth, budget=budget)


FIXED_BUILDERS = {"outplace_dual": build_outplace_fixed_root_dual,
                  "compact_dual": build_compact_root_dual,
                  "outplace_exact": build_outplace_fixed_exact,
                  "compact_exact": build_compact_exact}
