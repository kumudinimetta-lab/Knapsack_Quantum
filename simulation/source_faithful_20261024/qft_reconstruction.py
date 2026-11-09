"""OUR fixed-depth LP reconstruction using Draper/Wilkening arithmetic.

Not a released Wilkening oracle or its optimized full parallel schedule.
Ideal full QFT; no omitted rotations or opaque arithmetic simulation.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import math
import time

from ..pruning_study_20261023.circuits import _data, threshold_bits, BuildBudget, CircuitBuildCap
from ..oracle_h.node_bound_reversible import exact_order


@dataclass
class QFTCircuit:
    num_inputs: int
    num_qubits: int
    output: int
    gates: list
    metadata: dict
    depth: int
    threshold_bits: int

    def to_qiskit(self):
        from qiskit import QuantumCircuit
        qc = QuantumCircuit(self.num_qubits)
        for name, qubits, angle in self.gates:
            if name in ("p", "cp"):
                getattr(qc, name)(angle, *qubits)
            else:
                getattr(qc, name)(*qubits)
        return qc

    def resources(self):
        from qiskit import transpile
        qc = self.to_qiskit()
        common = transpile(qc, basis_gates=["u", "cx"], optimization_level=0)
        return {"classification": "DERIVED", "qubits": self.num_qubits,
                "native_counts": dict(Counter(g[0] for g in self.gates)),
                "native_depth": qc.depth(), "common_basis": ["u", "cx"],
                "common_counts": dict(common.count_ops()), "common_depth": common.depth(),
                "optimization_level": 0, "connectivity": "all_to_all",
                "rotation_synthesis": "ideal_arbitrary_angle_u_no_Clifford_T_approximation"}


class QFTNetwork:
    def __init__(self, inputs, max_width=0, budget=None, mcx_policy="direct"):
        self.inputs, self.output = list(range(inputs)), inputs
        self.next_wire, self.gates = inputs + 1, []
        self.max_width = max_width
        if mcx_policy not in ("direct", "source_generic"):
            raise ValueError("Unknown control policy")
        self.mcx_policy = mcx_policy
        self.compare_word, self.mc_word = [], []
        self.started, self.budget = time.monotonic(), budget or BuildBudget()

    def check(self):
        counts = {"qubits": self.next_wire, "gates": len(self.gates),
                  "elapsed_seconds": time.monotonic() - self.started}
        for reason, exceeded in [("qubit_budget", self.next_wire > self.budget.max_qubits),
                                 ("gate_budget", len(self.gates) > self.budget.max_gates),
                                 ("build_time_budget", counts["elapsed_seconds"] > self.budget.max_seconds)]:
            if exceeded:
                raise CircuitBuildCap(reason, counts)

    def allocate(self, width):
        result = list(range(self.next_wire, self.next_wire + width))
        self.next_wire += width
        self.check()
        return result

    def emit(self, target, *controls):
        self.gates.append(("x" if not controls else "cx" if len(controls) == 1 else "ccx",
                           tuple(controls) + (target,), None))

    def append(self, name, qubits, angle=None):
        self.gates.append((name, tuple(qubits), angle))
        if len(self.gates) % 1024 == 0:
            self.check()

    @staticmethod
    def inverse(gates):
        return [(name, qubits, -angle if name in ("p", "cp") else angle)
                for name, qubits, angle in reversed(gates)]

    def extend(self, gates):
        self.gates.extend(gates)
        self.check()

    @staticmethod
    def qft_gates(register):
        result = []
        for j in reversed(range(len(register))):
            result.append(("h", (register[j],), None))
            for k in reversed(range(j)):
                result.append(("cp", (register[j], register[k]), math.pi / 2 ** (j - k)))
        return result

    def controlled_constant(self, destination, constant, control=None, subtract=False):
        if not 0 <= constant < (1 << len(destination)):
            raise ValueError("Constant outside declared width")
        if not constant:
            return
        qft = self.qft_gates(destination)
        self.extend(qft)
        sign = -1 if subtract else 1
        for j, wire in enumerate(destination):
            numerator = constant % (1 << (j + 1))
            if numerator:
                angle = sign * 2 * math.pi * numerator / (1 << (j + 1))
                self.append("p" if control is None else "cp",
                            (wire,) if control is None else (control, wire), angle)
        self.extend(self.inverse(qft))

    def variable_add(self, destination, source, shift=0, subtract=False):
        qft = self.qft_gates(destination)
        self.extend(qft)
        sign = -1 if subtract else 1
        for j, source_wire in enumerate(source):
            for k in range(j + shift, len(destination)):
                self.append("cp", (source_wire, destination[k]), sign * math.pi / 2 ** (k - j - shift))
        self.extend(self.inverse(qft))

    def product_add(self, destination, source, coefficient):
        # Same repeated shifted-add recurrence as the compact arithmetic control.
        for j in range(coefficient.bit_length()):
            if (coefficient >> j) & 1:
                self.variable_add(destination, source, shift=j)

    def less(self, left, right, target):
        """Declared quantum/quantum extension: sign of an extra-bit subtraction."""
        if len(left) != len(right):
            raise ValueError("Comparison widths must match")
        if not self.compare_word:
            self.compare_word = self.allocate(max(self.max_width, len(left)) + 1)
        temporary = self.compare_word[:len(left) + 1]
        copies = [("cx", (a, b), None) for a, b in zip(left, temporary)]
        self.extend(copies)
        subtraction_start = len(self.gates)
        self.variable_add(temporary, right, subtract=True)
        subtraction = list(self.gates[subtraction_start:])
        self.emit(target, temporary[-1])
        self.extend(self.inverse(subtraction))
        self.extend(self.inverse(copies))

    def mcx_source_chain(self, controls, target):
        """Generic E(i) serial clean AND chain, with a final controlled X."""
        if not controls:
            self.emit(target)
            return
        if len(controls) == 1:
            self.emit(target, controls[0])
            return
        if self.mcx_policy == "direct" and len(controls) == 2:
            self.emit(target, *controls)
            return
        if not self.mc_word:
            self.mc_word = self.allocate(max(self.max_width, len(controls)) - (2 if self.mcx_policy == "direct" else 1))
        start = len(self.gates)
        self.emit(self.mc_word[0], controls[0], controls[1])
        for j in range(2, len(controls) - (1 if self.mcx_policy == "direct" else 0)):
            self.emit(self.mc_word[j - 1], self.mc_word[j - 2], controls[j])
        chain = list(self.gates[start:])
        if self.mcx_policy == "direct":
            self.emit(target, self.mc_word[len(controls) - 3], controls[-1])
        else:
            self.emit(target, self.mc_word[len(controls) - 2])
        self.extend(self.inverse(chain))

    def const_less(self, constant, register, target, constant_on_left=True):
        """Wilkening E.5 orthogonal lexicographic comparison clauses."""
        if not 0 <= constant < 1 << len(register):
            raise ValueError("Comparison constant outside width")
        for j in range(len(register)):
            bit = (constant >> j) & 1
            if (constant_on_left and bit) or (not constant_on_left and not bit):
                continue
            desired = {j: 1 if constant_on_left else 0}
            desired.update({k: (constant >> k) & 1 for k in range(j + 1, len(register))})
            negative = [register[k] for k, value in desired.items() if not value]
            for wire in negative:
                self.emit(wire)
            self.mcx_source_chain([register[k] for k in sorted(desired)], target)
            for wire in reversed(negative):
                self.emit(wire)

    def finish(self, controls):
        forward = list(self.gates)
        for flags in controls:
            self.emit(self.output, *flags)
        self.extend(self.inverse(forward))

    def circuit(self, depth, tb, **metadata):
        self.check()
        return QFTCircuit(len(self.inputs), self.next_wire, self.output, self.gates,
                          {"scope": "OUR_source_primitive_reconstruction_NOT_released_R1_oracle",
                           "qft_precision": "ideal_full_no_omitted_rotations",
                           "control_strategy": "serial_shared_clean_ancillas_no_copied_control_parallelization",
                           "multi_control_policy": self.mcx_policy,
                           "build_seconds_measured": time.monotonic() - self.started,
                           **metadata}, depth, tb)


def build_qft_exact(weights, values, capacity, depth, budget=None, mcx_policy="direct"):
    weights, values, capacity = _data(weights, values, capacity)
    if not 0 <= depth <= len(weights):
        raise ValueError("Invalid depth")
    order, tb = tuple(exact_order(weights, values)), threshold_bits(values)
    wb = max(1, (capacity + sum(weights)).bit_length() + 1)
    vb = max(1, sum(values).bit_length() + 1)
    cb = max(sum(values) * max(weights, default=1) + capacity * max(values, default=1),
             ((1 << tb) - 1) * max(weights, default=1)).bit_length() + 1
    c = QFTNetwork(depth + tb, max(wb, vb, cb), budget, mcx_policy)
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
        c.extend(c.inverse(products))
        outputs.append((split, below))
        active = take
    integer_below = c.allocate(1)[0]
    start = len(c.gates)
    c.variable_add(numerator, pval)
    c.variable_add(threshold, c.inputs[depth:])
    products = list(c.gates[start:])
    c.less(numerator, threshold, integer_below)
    c.extend(c.inverse(products))
    outputs.append((active, integer_below))
    c.finish(outputs)
    return c.circuit(depth, tb, weights=list(weights), values=list(values), capacity=capacity,
                     order=list(order), weight_width=wb, value_width=vb, numerator_width=cb)
