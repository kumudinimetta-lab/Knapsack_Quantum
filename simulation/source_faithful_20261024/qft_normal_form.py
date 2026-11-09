"""Exact inverse cancellation control for OUR QFT primitive assembly.

Only literal inverse pairs are removed. With commute_disjoint=True, the
intervening gates must act on disjoint wires, so the pair can commute together.
No approximate angle test, rotation synthesis, angle merging or register
reallocation is performed. Pinned upstream builders remain unchanged.
"""
from collections import Counter
import copy


def _inverse_pair(left, right):
    name, wires, angle = left
    other_name, other_wires, other_angle = right
    if name != other_name or tuple(wires) != tuple(other_wires):
        return False
    if name in ("x", "cx", "ccx", "h"):
        return angle is None and other_angle is None
    if name in ("p", "cp"):
        return angle == -other_angle
    return False


def cancel_inverse_gates(gates, *, commute_disjoint=True):
    """Return (new_gates, audit) without mutating the supplied native netlist."""
    gates = list(gates)
    removed = Counter()
    if not commute_disjoint:
        kept = []
        for gate in gates:
            if kept and _inverse_pair(kept[-1], gate):
                removed[gate[0]] += 2
                kept.pop()
            else:
                kept.append(gate)
    else:
        records, latest = [], {}
        for gate in gates:
            name, wires, angle = gate
            wires = tuple(wires)
            if not wires or len(set(wires)) != len(wires):
                raise ValueError("Distinct, nonempty gate wires required")
            predecessor = latest.get(wires[0])
            if (predecessor is not None
                    and all(latest.get(q) == predecessor for q in wires)
                    and _inverse_pair(records[predecessor][0], gate)):
                previous, before, _ = records[predecessor]
                for q in wires:
                    if before[q] is None:
                        latest.pop(q, None)
                    else:
                        latest[q] = before[q]
                records[predecessor] = (previous, before, False)
                removed[name] += 2
            else:
                index = len(records)
                records.append((gate, {q: latest.get(q) for q in wires}, True))
                for q in wires:
                    latest[q] = index
        kept = [gate for gate, _, active in records if active]
    return kept, {
        "classification": "DERIVED exact native-netlist inverse cancellation",
        "policy": "inverse_pairs_across_disjoint_wires" if commute_disjoint else "adjacent_inverse_pairs",
        "input_gates": len(gates), "output_gates": len(kept),
        "removed_gate_counts": dict(removed),
        "angle_test": "literal_opposite_no_tolerance",
        "not_performed": "diagonal_angle_merging_register_reallocation_or_approximation",
    }


def normalized_qft_circuit(compiled, *, commute_disjoint=True):
    """Copy a QFTCircuit with exact cancellation; preserve all I/O and widths."""
    result = copy.copy(compiled)
    result.gates, audit = cancel_inverse_gates(compiled.gates, commute_disjoint=commute_disjoint)
    result.metadata = dict(compiled.metadata, inverse_cancellation=audit)
    return result
