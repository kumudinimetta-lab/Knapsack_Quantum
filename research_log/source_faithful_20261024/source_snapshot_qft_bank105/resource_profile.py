"""Exact local gate-list expansion into the pinned transpiler's u/cx basis."""
from collections import Counter
import time

from qiskit import QuantumCircuit, transpile
from ..pruning_study_20261023.circuits import BuildBudget, CircuitBuildCap


def primitive_skeletons():
    result = {}
    for name, arity in [("x", 1), ("cx", 2), ("ccx", 3), ("h", 1), ("p", 1), ("cp", 2)]:
        qc = QuantumCircuit(arity)
        if name in ("p", "cp"):
            getattr(qc, name)(0.371, *range(arity))
        else:
            getattr(qc, name)(*range(arity))
        common = transpile(qc, basis_gates=["u", "cx"], optimization_level=0)
        result[name] = [(item.operation.name, tuple(common.find_bit(q).index for q in item.qubits))
                        for item in common.data]
        if any(op not in ("u", "cx") for op, _ in result[name]):
            raise ValueError("Unexpected primitive basis")
    return result


def profile(compiled, skeletons, budget=None):
    budget, started = budget or BuildBudget(), time.monotonic()
    if compiled.num_qubits > budget.max_qubits:
        raise CircuitBuildCap("qubit_budget", {"qubits": compiled.num_qubits})
    common_levels, native_levels = [0] * compiled.num_qubits, [0] * compiled.num_qubits
    native_counts, common_counts = Counter(), Counter()
    max_native = max_common = expanded = 0
    for j, gate in enumerate(compiled.gates):
        if len(gate) == 3 and isinstance(gate[0], str):
            name, wires, _ = gate
        else:
            target, controls = gate
            name, wires = ("x", "cx", "ccx")[len(controls)], tuple(controls) + (target,)
        native_counts[name] += 1
        level = max(native_levels[q] for q in wires) + 1
        for q in wires:
            native_levels[q] = level
        max_native = max(max_native, level)
        for operation, local_wires in skeletons[name]:
            mapped = tuple(wires[q] for q in local_wires)
            level = max(common_levels[q] for q in mapped) + 1
            for q in mapped:
                common_levels[q] = level
            max_common = max(max_common, level)
            common_counts[operation] += 1
            expanded += 1
        if j % 1024 == 0:
            counts = {"qubits": compiled.num_qubits, "native_gates_seen": j + 1,
                      "expanded_gates_seen": expanded, "profile_seconds": time.monotonic() - started}
            if j + 1 > budget.max_gates or expanded > budget.max_gates:
                raise CircuitBuildCap("expanded_gate_budget", counts)
            if counts["profile_seconds"] > budget.max_seconds:
                raise CircuitBuildCap("profile_time_budget", counts)
    if expanded > budget.max_gates:
        raise CircuitBuildCap("expanded_gate_budget", {"expanded_gates_seen": expanded})
    return {"classification": "DERIVED", "qubits": compiled.num_qubits,
            "native_counts": dict(native_counts), "native_depth": max_native,
            "common_counts": dict(common_counts), "common_depth": max_common,
            "common_basis": ["u", "cx"], "optimization_level": 0, "connectivity": "all_to_all",
            "profile_seconds_measured": time.monotonic() - started,
            "resource_method": "actual_native_netlist_exact_local_transpiler_expansion_DAG_levels"}
