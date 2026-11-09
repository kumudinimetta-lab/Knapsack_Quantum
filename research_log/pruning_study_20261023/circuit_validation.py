"""Independent rational references and bounded compiled-circuit verification."""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from simulation.pruning_study_20261023.circuits import (
    BUILDERS, BuildBudget, CircuitBuildCap, multiplier_bank,
)
from simulation.oracle_h.node_bound_reversible import build_coherent_node_bound


def reference(weights, values, capacity, depth, prefix, method):
    """Direct Fraction bounds, deliberately not the circuit's loss arithmetic."""
    n = len(weights)
    if depth > n:
        return None
    order = sorted(range(n), key=lambda i: Fraction(values[i], weights[i]), reverse=True)
    selected = [order[j] for j in range(depth) if (prefix >> j) & 1]
    weight = sum(weights[i] for i in selected)
    value = sum(values[i] for i in selected)
    rem = capacity - weight
    if rem < 0:
        return None
    suffix = order[depth:]
    if method == "simple":
        return Fraction(value + sum(values[i] for i in suffix))
    if method in ("root_dual", "bank2", "bank4"):
        q = {"root_dual": 1, "bank2": 2, "bank4": 4}[method]
        bank = multiplier_bank(weights, values, capacity, q)
        return min(Fraction(value) + lam * rem + sum(
            max(Fraction(values[i]) - lam * weights[i], 0) for i in suffix) for lam in bank)
    total = Fraction(value)
    for i in suffix:
        if weights[i] <= rem:
            total += values[i]
            rem -= weights[i]
        else:
            return total + Fraction(rem * values[i], weights[i])
    return total


def check_inputs(circuit, weights, values, capacity, method, inputs):
    n, db = len(weights), circuit.depth_register_bits
    expected_bound = {}
    for encoded in inputs:
        prefix = encoded & ((1 << n) - 1)
        depth = (encoded >> n) & ((1 << db) - 1)
        if (depth, prefix) not in expected_bound:
            expected_bound[depth, prefix] = reference(weights, values, capacity, depth, prefix, method)
    mismatch, dirty, first = 0, 0, []
    for target in (0, 1):
        flags, garbage = circuit.simulate_columns(inputs, target)
        dirty += garbage
        for encoded, actual in zip(inputs, flags):
            prefix = encoded & ((1 << n) - 1)
            depth = (encoded >> n) & ((1 << db) - 1)
            tau = encoded >> (n + db)
            bound = expected_bound[depth, prefix]
            expected = target ^ int(bound is None or bound < tau)
            if actual != expected:
                mismatch += 1
                if len(first) < 4:
                    first.append({"encoded": encoded, "target": target, "depth": depth,
                                  "prefix": prefix, "tau": tau, "bound": str(bound),
                                  "expected": expected, "actual": actual})
    return {"classification": "SIMULATED", "columns": 2 * len(inputs),
            "predicate_mismatches": mismatch, "dirty_columns": dirty, "first_failures": first}


def dense_check(circuit, weights, values, capacity, method):
    import numpy as np
    from qiskit.quantum_info import Statevector
    if circuit.num_qubits > 18:
        return {"status": "SKIPPED_DENSE_QUBIT_CAP", "qubits": circuit.num_qubits,
                "cap": 18, "cap_classification": "HARDCODED"}
    rng = np.random.default_rng(20261023)
    count = 1 << circuit.num_inputs
    amplitudes = rng.normal(size=2 * count) + 1j * rng.normal(size=2 * count)
    amplitudes /= np.linalg.norm(amplitudes)
    state = np.zeros(1 << circuit.num_qubits, dtype=complex)
    expected = np.zeros_like(state)
    n, db = len(weights), circuit.depth_register_bits
    for target in (0, 1):
        for encoded in range(count):
            amplitude = amplitudes[target * count + encoded]
            state[encoded | (target << circuit.output)] = amplitude
            p, d, tau = (encoded & ((1 << n) - 1),
                          (encoded >> n) & ((1 << db) - 1), encoded >> (n + db))
            bound = reference(weights, values, capacity, d, p, method)
            flag = target ^ int(bound is None or bound < tau)
            expected[encoded | (flag << circuit.output)] = amplitude
    actual = Statevector(state).evolve(circuit.to_qiskit()).data
    error = float(np.max(np.abs(actual - expected)))
    return {"classification": "SIMULATED", "status": "COMPLETED",
            "nonzero_input_amplitudes": 2 * count,
            "max_amplitude_error": error, "mismatches_above_1e-12": int(error > 1e-12)}


def main():
    started = time.monotonic()
    result = {"scope": "Compiled predicates only, zero initial workspace; no full walk/QPU claim.",
              "exhaustive": [], "randomized": [], "dense": [], "caps": [], "errors": []}
    budget = BuildBudget(max_qubits=150_000, max_gates=2_000_000, max_seconds=60)
    builders = dict(BUILDERS)
    builders["fixedpoint_wrapper_legacy"] = lambda w, v, c, **kw: build_coherent_node_bound(w, v, c)
    cases = [([], [], 0), ([1], [1], 0), ([1], [1], 1),
             ([2, 3, 4, 5], [3, 4, 5, 8], 8),
             ([3, 5, 7, 8], [3, 5, 7, 8], 13),
             ([4, 7, 6], [5, 6, 2], 7),
             ([1, 2], [3, 2], 0), ([2, 3], [2, 3], 5),
             ([9, 10, 1], [7, 5, 2], 3),
             ([2, 4, 6], [3, 6, 9], 20)]
    rng = random.Random(20261023)
    for trial in range(6):
        n = 3 + trial % 2
        w = [rng.randint(1, 7) for _ in range(n)]
        v = [rng.randint(1, 9) for _ in range(n)]
        cases.append((w, v, rng.randrange(sum(w) + 1)))
    for case_id, (w, v, cap) in enumerate(cases):
        row = {"case_id": case_id, "weights": w, "values": v, "capacity": cap, "methods": {}}
        for name, builder in builders.items():
            try:
                circuit = builder(w, v, cap, budget=budget)
                check = check_inputs(circuit, w, v, cap, name, range(1 << circuit.num_inputs))
                row["methods"][name] = {"status": "COMPLETED", **check,
                                        "resources": circuit.resources(),
                                        "metadata": getattr(circuit, "metadata", {})}
                if case_id in (0, 1):
                    result["dense"].append({"case_id": case_id, "method": name,
                                             **dense_check(circuit, w, v, cap, name)})
            except CircuitBuildCap as exc:
                row["methods"][name] = {"status": "CAPPED", "reason": exc.reason, **exc.counters}
            except Exception as exc:
                result["errors"].append({"case_id": case_id, "method": name,
                                          "error": type(exc).__name__ + ": " + str(exc)})
        result["exhaustive"].append(row)
        print(f"Exhaustive case {case_id}: {len(row['methods'])} methods", flush=True)
    # Independent wider-integer cases. These are sampled encodings, never called exhaustive.
    for trial, (n, magnitude) in enumerate([(6, 100), (8, 100), (12, 100), (8, 10**6)]):
        seed = 20261100 + trial
        sample_rng = random.Random(seed)
        w = [sample_rng.randint(1, magnitude) for _ in range(n)]
        v = [sample_rng.randint(1, magnitude) for _ in range(n)]
        cap = sum(w) // 2
        row = {"seed": seed, "weights": w, "values": v, "capacity": cap, "methods": {}}
        for name, builder in builders.items():
            try:
                circuit = builder(w, v, cap, budget=budget)
                inputs = []
                db, tb = circuit.depth_register_bits, circuit.threshold_bits
                data_rng = random.Random(seed + 1000)
                for _ in range(60):
                    d, p = data_rng.randrange(1 << db), data_rng.randrange(1 << n)
                    bound = reference(w, v, cap, d, p, name)
                    thresholds = {0, (1 << tb) - 1, data_rng.randrange(1 << tb)}
                    if bound is not None:
                        thresholds.update([max(0, math.floor(bound)), min((1 << tb) - 1, math.floor(bound) + 1)])
                    inputs.extend(p | (d << n) | (tau << (n + db)) for tau in sorted(thresholds))
                row["methods"][name] = {"status": "COMPLETED", **check_inputs(circuit, w, v, cap, name, inputs),
                                        "resources": circuit.resources()}
            except CircuitBuildCap as exc:
                row["methods"][name] = {"status": "CAPPED", "reason": exc.reason, **exc.counters}
            except Exception as exc:
                result["errors"].append({"random_trial": trial, "method": name,
                                          "error": type(exc).__name__ + ": " + str(exc)})
        result["randomized"].append(row)
        print(f"Randomized case {trial}: {len(row['methods'])} methods", flush=True)
    for expected, limited in [("qubit_budget", BuildBudget(max_qubits=5)),
                               ("gate_budget", BuildBudget(max_gates=10)),
                               ("build_time_budget", BuildBudget(max_seconds=0))]:
        try:
            BUILDERS["exact_single"]([2, 3], [3, 4], 3, budget=limited)
            result["caps"].append({"expected": expected, "status": "FAILED_TO_CAP"})
        except CircuitBuildCap as exc:
            result["caps"].append({"expected": expected, "reason": exc.reason,
                                    "status": "EXPECTED_CAP" if expected == exc.reason else "WRONG_CAP",
                                    "counters": exc.counters})
    completed = [x for section in ("exhaustive", "randomized") for row in result[section]
                 for x in row["methods"].values() if x["status"] == "COMPLETED"]
    result["summary"] = {"classification": "SIMULATED", "completed_method_cases": len(completed),
                         "columns": sum(x["columns"] for x in completed),
                         "predicate_mismatches": sum(x["predicate_mismatches"] for x in completed),
                         "dirty_columns": sum(x["dirty_columns"] for x in completed),
                         "elapsed_seconds_measured": time.monotonic() - started}
    path = Path(__file__).with_name("circuit_validation_results.json")
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result["summary"], indent=2), flush=True)
    assert not result["errors"], result["errors"]
    assert result["summary"]["predicate_mismatches"] == result["summary"]["dirty_columns"] == 0
    assert all(x["status"] == "EXPECTED_CAP" for x in result["caps"])
    assert all(x.get("mismatches_above_1e-12", 0) == 0 for x in result["dense"])


if __name__ == "__main__":
    main()
