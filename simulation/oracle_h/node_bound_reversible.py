"""Exact X/CX/CCX circuit for the fixed-point node-pruning predicate.

Problem data, depth, threshold and exact efficiency order are classical
parameters. The prefix assignment is quantum input. Each depth has a circuit;
a clean wrapper dispatches those circuits coherently by depth. Walk reflections
are not implemented here.
Efficiencies floor(2**k*v/w) are compiled from fixed problem constants, so no
quantum division of variable data is needed. This is a transparent Boolean
arithmetic construction, not an implementation of a named optimized divider.

The simulator propagates sparse computational-basis statevector columns through
every gate. It is exact for this permutation gate set, including superpositions;
it is not the legacy per-qubit Fourier-phase simulator.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence


def precision_bits(wmax: int) -> int:
    if wmax < 1:
        raise ValueError("wmax must be positive")
    return (wmax * wmax).bit_length()  # 2**k > wmax**2, including powers of two


def exact_order(weights, values):
    return sorted(range(len(weights)),
                  key=lambda i: Fraction(values[i], weights[i]), reverse=True)


class BooleanCompiler:
    """Out-of-place Boolean arithmetic, followed by copy and uncomputation.

    Wire names 0 and 1 are constants, names >=2 are qubits. No opaque gate,
    measurement, lookup of optimal solutions, or arithmetic shortcut is used.
    """
    def __init__(self, inputs: int):
        self.inputs = list(range(2, inputs + 2))
        self.output = inputs + 2
        self.next_wire = inputs + 3
        self.gates = []  # (target qubit, tuple(control qubits))

    def fresh(self):
        w = self.next_wire
        self.next_wire += 1
        return w

    def emit(self, target, *controls):
        self.gates.append((target - 2, tuple(c - 2 for c in controls)))

    def xor(self, a, b):
        if a == b:
            return 0
        if a == 0:
            return b
        if b == 0:
            return a
        out = self.fresh()
        for x in (a, b):
            if x == 1:
                self.emit(out)
            else:
                self.emit(out, x)
        return out

    def neg(self, a):
        return self.xor(a, 1)

    def land(self, a, b):
        if a == 0 or b == 0:
            return 0
        if a == 1:
            return b
        if b == 1 or a == b:
            return a
        out = self.fresh()
        self.emit(out, a, b)
        return out

    def lor(self, a, b):
        return self.neg(self.land(self.neg(a), self.neg(b)))

    def add(self, a, b, carry=0):
        result = []
        for x, y in zip(a, b):
            xy = self.xor(x, y)
            result.append(self.xor(xy, carry))
            carry = self.xor(self.land(x, y), self.land(carry, xy))
        return result, carry

    def sub(self, a, b):
        return self.add(a, [self.neg(x) for x in b], 1)

    def mux(self, flag, yes, no):
        return [self.xor(n, self.land(flag, self.xor(y, n)))
                for y, n in zip(yes, no)]

    def const_mul(self, a, value: int, width: int):
        result = [0] * width
        for j in range(value.bit_length()):
            if (value >> j) & 1:
                term = [0] * j + list(a)
                term = (term + [0] * width)[:width]
                result, _ = self.add(result, term)
        return result

    def finish(self, result):
        forward = list(self.gates)
        if result == 1:
            self.emit(self.output)
        elif result != 0:
            self.emit(self.output, result)
        self.gates.extend(reversed(forward))
        return self.gates


def bits(value: int, width: int):
    return [(value >> i) & 1 for i in range(width)]


@dataclass
class NodeBoundCircuit:
    num_inputs: int
    num_qubits: int
    output: int
    gates: list
    order: tuple
    k: int
    depth: int
    threshold: int
    threshold_bits: int = 0

    def resources(self):
        counts = {"x": 0, "cx": 0, "ccx": 0}
        levels = [0] * self.num_qubits
        for t, cs in self.gates:
            counts[("x", "cx", "ccx")[len(cs)]] += 1
            level = max(levels[q] for q in (t,) + cs) + 1
            for q in (t,) + cs:
                levels[q] = level
        return {"qubits": self.num_qubits, "gates": len(self.gates),
                "gate_depth": max(levels, default=0), "gate_counts": counts,
                "resource_classification": "DERIVED_FROM_SYNTHESIZED_GATE_LIST"}

    def simulate_columns(self, prefixes: Sequence[int], output_bit: int = 0):
        """Exact sparse statevector propagation, batched via bit planes.

        Each lane is a distinct computational-basis column, not a probabilistic
        sample. The X/CX/CCX matrices have one nonzero (+1) per column. Therefore
        basis labels suffice to propagate arbitrary sparse amplitudes exactly.
        Returns output flags and count of columns with nonzero workspace.
        """
        lanes = len(prefixes)
        mask = (1 << lanes) - 1
        planes = [0] * self.num_qubits
        exhaustive = (isinstance(prefixes, range) and prefixes.start == 0
                      and prefixes.step == 1 and lanes == 1 << self.num_inputs)
        for i in range(self.num_inputs):
            planes[i] = (((mask // ((1 << (1 << i)) + 1)) << (1 << i)) & mask
                         if exhaustive else sum(((p >> i) & 1) << lane
                                                for lane, p in enumerate(prefixes)))
        initial_inputs = planes[:self.num_inputs]
        if output_bit:
            planes[self.output] = mask
        for t, cs in self.gates:
            control = mask
            for c in cs:
                control &= planes[c]
            planes[t] ^= control
        dirty = 0
        for i, plane in enumerate(planes):
            if i < self.num_inputs:
                expected = initial_inputs[i]
                dirty |= plane ^ expected
            elif i != self.output:
                dirty |= plane
        flags = [(planes[self.output] >> lane) & 1 for lane in range(lanes)]
        return flags, dirty.bit_count()

    def to_qiskit(self):
        from qiskit import QuantumCircuit
        qc = QuantumCircuit(self.num_qubits, name="node_LP_prune")
        for t, cs in self.gates:
            if not cs:
                qc.x(t)
            elif len(cs) == 1:
                qc.cx(cs[0], t)
            else:
                qc.ccx(cs[0], cs[1], t)
        return qc


def build_node_bound(weights, values, capacity: int, depth: int,
                     threshold: int, k: int | None = None,
                     quantum_threshold: bool = False):
    """Build |prefix,b,0> -> |prefix,b xor [U(prefix)<tau],0>.

    Exact equality of pruning predicates requires the lemma's precision.
    Widths cover sums of all values and weights; intermediate arithmetic is
    modular only in infeasible branches, which are independently rejected.
    """
    weights, values = tuple(weights), tuple(values)
    n = len(weights)
    if (n != len(values) or any(w <= 0 for w in weights)
            or any(v <= 0 for v in values) or not 0 <= depth <= n
            or capacity < 0):
        raise ValueError("Invalid positive-integer knapsack instance/depth")
    wmax = max(weights, default=1)
    k = precision_bits(wmax) if k is None else k
    if (1 << k) <= wmax * wmax:
        raise ValueError("The robust pruning guarantee requires 2**k > Wmax**2")
    order = tuple(exact_order(weights, values))
    tb = max(1, (sum(values) + 1).bit_length()) if quantum_threshold else 0
    comp = BooleanCompiler(depth + tb)
    wb = max(1, (capacity + sum(weights)).bit_length() + 1)
    vb = max(1, (sum(values) * (1 << k)).bit_length() + 1)
    weight, acc = [0] * wb, [0] * vb
    for pos, item in enumerate(order[:depth]):
        x = comp.inputs[pos]
        weight, _ = comp.add(weight, [comp.land(x, c) for c in bits(weights[item], wb)])
        acc, _ = comp.add(acc, [comp.land(x, c) for c in bits(values[item] << k, vb)])
    rem, feasible = comp.sub(bits(capacity, wb), weight)
    active = feasible
    for item in order[depth:]:
        reduced, enough = comp.sub(rem, bits(weights[item], wb))
        take = comp.land(active, enough)
        split = comp.land(active, comp.neg(enough))
        full, _ = comp.add(acc, bits(values[item] << k, vb))
        acc = comp.mux(take, full, acc)
        quotient = (values[item] << k) // weights[item]
        product = comp.const_mul(rem, quotient, vb)
        fractional, _ = comp.add(acc, product)
        acc = comp.mux(split, fractional, acc)
        rem = comp.mux(take, reduced, rem)
        active = comp.land(active, enough)
    if quantum_threshold:
        # A/2**k <= tau-1/Wmax iff A*Wmax+2**k <= tau*2**k*Wmax.
        # This avoids reversible variable division, using exact cross products.
        cb = max(vb, tb + k) + wmax.bit_length() + 2
        left = comp.const_mul(acc, wmax, cb)
        left, _ = comp.add(left, bits(1 << k, cb))
        right = comp.const_mul(comp.inputs[depth:], wmax << k, cb)
        _, below = comp.sub(right, left)
    else:
        h = ((threshold * (1 << k) * wmax - (1 << k)) // wmax)
        if h < 0:
            below = 0
        elif h >= 1 << vb:
            below = 1
        else:
            _, below = comp.sub(bits(h, vb), acc)
    result = comp.lor(comp.neg(feasible), below)
    gates = comp.finish(result)
    return NodeBoundCircuit(depth + tb, comp.next_wire - 2, comp.output - 2,
                            gates, order, k, depth, threshold, tb)


def exact_node_bound(weights, values, capacity, depth, prefix):
    order = exact_order(weights, values)
    chosen = [order[j] for j in range(depth) if (prefix >> j) & 1]
    rem = capacity - sum(weights[i] for i in chosen)
    if rem < 0:
        return None
    value = Fraction(sum(values[i] for i in chosen))
    for i in order[depth:]:
        if weights[i] <= rem:
            rem -= weights[i]
            value += values[i]
        else:
            value += Fraction(rem * values[i], weights[i])
            break
    return value


def build_coherent_node_bound(weights, values, capacity, k=None):
    """Coherently dispatch the fixed-depth predicates, with clean workspace.

    Input order: m prefix bits, binary depth, threshold bits, target bit.
    Prefix bits are in exact efficiency order; bits beyond depth are ignored.
    Invalid depth encodings are rejected. A single work pool is reused, because
    every fixed-depth predicate cleans it before the next block. This is the
    complete depth-dependent h predicate, not a walk/reflection implementation.
    """
    m = len(weights)
    db = max(1, m.bit_length())
    families = [build_node_bound(weights, values, capacity, d, 0, k,
                                quantum_threshold=True) for d in range(m+1)]
    tb = families[0].threshold_bits
    compiler = BooleanCompiler(m+db+tb)
    depth_wires = compiler.inputs[m:m+db]
    flags = []
    for d in range(m+1):
        flag = 1
        for j, wire in enumerate(depth_wires):
            flag = compiler.land(flag, wire if (d>>j)&1 else compiler.neg(wire))
        flags.append(flag)
    valid = 0
    for flag in flags:
        valid = compiler.lor(valid, flag)
    invalid = compiler.neg(valid)
    prefix_gates = list(compiler.gates)
    if invalid == 1:
        compiler.emit(compiler.output)
    elif invalid != 0:
        compiler.emit(compiler.output, invalid)
    temporary = compiler.fresh()-2
    workspace_size = max(c.num_qubits-c.num_inputs-1 for c in families)
    workspace = [compiler.fresh()-2 for _ in range(workspace_size)]
    for d, circuit in enumerate(families):
        mapping = {j:j for j in range(d)}
        mapping.update({d+j:m+db+j for j in range(tb)})
        mapping[circuit.output] = temporary
        for j, q in enumerate(range(circuit.num_inputs+1, circuit.num_qubits)):
            mapping[q] = workspace[j]
        mapped = [(mapping[t], tuple(mapping[c] for c in cs)) for t,cs in circuit.gates]
        compiler.gates.extend(mapped)
        if flags[d] == 1:
            compiler.gates.append((compiler.output-2,(temporary,)))
        elif flags[d] != 0:
            compiler.gates.append((compiler.output-2,(flags[d]-2,temporary)))
        # The clean XOR predicate is its own inverse: clear the private flag.
        compiler.gates.extend(mapped)
    compiler.gates.extend(reversed(prefix_gates))
    result = NodeBoundCircuit(m+db+tb,compiler.next_wire-2,compiler.output-2,
                              compiler.gates,families[0].order,families[0].k,-1,-1,tb)
    result.depth_register_bits = db
    result.prefix_width = m
    return result
