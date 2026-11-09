"""Dense arithmetic kernels and actual full-gate MPS prefix-predicate pilot."""
from __future__ import annotations

import json
import math
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from simulation.source_faithful_20261024.qft_reconstruction import QFTNetwork, build_qft_exact
from simulation.pruning_study_20261023.compact_sensitivity import build_compact_exact, build_compact_root_dual
from research_log.pruning_study_20261023.compact_validation import direct_bound

TOLERANCE = 1e-8


def dense_kernel(network, expected, label):
    circuit = network.circuit(0, 0).to_qiskit()
    maximum, bad, columns = 0.0, 0, 1 << (len(network.inputs) + 1)
    for encoded in range(columns):
        target = expected(encoded)
        actual = Statevector.from_int(encoded, 1 << circuit.num_qubits).evolve(circuit).data
        error = abs(actual[target] - 1)
        actual[target] -= 1
        error = max(error, float(np.max(np.abs(actual))))
        maximum = max(maximum, error)
        bad += error > TOLERANCE
    return {"label": label, "classification": "SIMULATED", "columns": columns,
            "failed_columns_above_tolerance": int(bad), "max_amplitude_error": float(maximum),
            "qubits": circuit.num_qubits, "tolerance_hardcoded": TOLERANCE}


def kernels():
    rows = []
    for width in (1, 2, 3):
        mask = (1 << width) - 1
        for subtract in (False, True):
            c = QFTNetwork(2 * width)
            c.variable_add(list(range(width)), list(range(width, 2 * width)), subtract=subtract)
            def expected(x, n=width, m=mask, sub=subtract):
                left, right = x & m, (x >> n) & m
                return ((left - right if sub else left + right) & m) | (right << n) | ((x >> (2*n)) << (2*n))
            rows.append(dense_kernel(c, expected, f"variable_{'sub' if subtract else 'add'}_{width}"))
        c = QFTNetwork(2 * width, width)
        c.less(list(range(width)), list(range(width, 2 * width)), c.output)
        rows.append(dense_kernel(c, lambda x,n=width,m=mask: (x & ((1 << (2*n))-1)) |
                                 (((x>>(2*n)) ^ int((x&m) < ((x>>n)&m))) << (2*n)),
                                 f"unsigned_compare_{width}"))
        for constant in range(1 << width):
            for subtract in (False, True):
                c = QFTNetwork(width + 1)
                c.controlled_constant(list(range(width)), constant, width, subtract=subtract)
                rows.append(dense_kernel(c, lambda x,n=width,m=mask,k=constant,s=subtract:
                                         (((x&m) + (-k if s else k)*((x>>n)&1)) & m) | (x & ~m),
                                         f"controlled_constant_{constant}_{'sub' if subtract else 'add'}_{width}"))
            for policy in ("direct", "source_generic"):
                for on_left in (False, True):
                    c = QFTNetwork(width, width, mcx_policy=policy)
                    c.const_less(constant, list(range(width)), c.output, on_left)
                    rows.append(dense_kernel(c, lambda x,n=width,m=mask,k=constant,left=on_left:
                                             (x&m) | (((x>>n) ^ int(k<(x&m) if left else (x&m)<k)) << n),
                                             f"const_compare_{constant}_{on_left}_{policy}_{width}"))
    return rows


def common_resources(circuit):
    common = transpile(circuit, basis_gates=["u", "cx"], optimization_level=0)
    return {"classification": "DERIVED", "qubits": circuit.num_qubits,
            "native_counts": dict(circuit.count_ops()), "native_depth": circuit.depth(),
            "common_basis": ["u", "cx"], "common_counts": dict(common.count_ops()),
            "common_depth": common.depth(), "optimization_level": 0,
            "connectivity": "all_to_all", "rotation_synthesis": "ideal_arbitrary_angle_u"}


def run_full_mps(compiled, weights, values, cap, depth, dual=False):
    predicate = compiled.to_qiskit()
    total_columns = 2 * (1 << compiled.num_inputs)
    caps = {"qubits": 96, "native_gates": 40000, "columns": 512, "condition_seconds": 90}
    if predicate.num_qubits > caps["qubits"] or len(predicate.data) > caps["native_gates"] or total_columns > caps["columns"]:
        return {"status": "CAPPED", "reason": "predeclared_size_budget", "caps_hardcoded": caps,
                "requested_columns": total_columns}
    simulator = AerSimulator(method="matrix_product_state", matrix_product_state_truncation_threshold=0.0,
                             max_parallel_threads=1, max_parallel_experiments=1)
    cases = []
    for target in (0, 1):
        for encoded in range(1 << compiled.num_inputs):
            prefix, tau = encoded & ((1 << depth) - 1), encoded >> depth
            bound = direct_bound(weights, values, cap, depth, prefix, dual)
            flag = target ^ int(bound is None or bound < tau)
            expected = encoded | (flag << compiled.output)
            initial = encoded | (target << compiled.output)
            qc = QuantumCircuit(predicate.num_qubits)
            for j in range(compiled.num_inputs + 1):
                if (initial >> j) & 1:
                    qc.x(j)
            qc.compose(predicate, inplace=True)
            qc.save_amplitudes([expected], label="expected_output")
            cases.append((qc, expected, initial))
    start = time.monotonic()
    maximum, maximum_leak, failures, completed, first = 0.0, 0.0, 0, 0, []
    metadata = None
    for offset in range(0, len(cases), 8):
        if time.monotonic() - start > caps["condition_seconds"]:
            return {"status": "CAPPED", "reason": "condition_time_budget", "caps_hardcoded": caps,
                    "columns_completed": completed, "predicate_or_cleanup_failures": failures,
                    "max_expected_amplitude_error": maximum, "max_probability_leak": maximum_leak}
        chunk = cases[offset:offset + 8]
        result = simulator.run([x[0] for x in chunk], shots=1).result(timeout=90)
        if not result.success:
            return {"status": "SIMULATOR_FAILURE", "message": str(result.status), "columns_completed": completed}
        for j, (_, expected, initial) in enumerate(chunk):
            amplitude = complex(result.data(j)["expected_output"][0])
            error, leak = abs(amplitude - 1), max(0.0, 1 - abs(amplitude) ** 2)
            maximum, maximum_leak = max(maximum, error), max(maximum_leak, leak)
            if error > TOLERANCE or leak > TOLERANCE:
                failures += 1
                if len(first) < 3:
                    first.append({"initial": initial, "expected": expected, "amplitude": [amplitude.real, amplitude.imag]})
            completed += 1
            if metadata is None:
                raw = result.results[j].metadata
                metadata = {k: raw[k] for k in ("method", "noise", "matrix_product_state_truncation_threshold",
                                                "matrix_product_state_max_bond_dimension")}
                if metadata["matrix_product_state_truncation_threshold"] != 0:
                    raise RuntimeError("Unexpected MPS truncation")
    return {"status": "COMPLETED", "classification": "SIMULATED", "columns": completed,
            "predicate_or_cleanup_failures": failures, "max_expected_amplitude_error": maximum,
            "max_probability_leak": maximum_leak, "first_failures": first,
            "simulator": metadata, "tolerance_hardcoded": TOLERANCE,
            "seconds_measured": time.monotonic() - start, "caps_hardcoded": caps}


def main():
    started = time.monotonic()
    out = {"scope": "OUR source-primitive reconstruction, not released R1 oracle; fixed depth, ideal full QFT.",
           "kernels": kernels(), "rows": [], "errors": []}
    output = Path(__file__).with_name("pilot_results.json")
    output.write_text(json.dumps(out, indent=2), encoding="utf-8")
    if any(r["failed_columns_above_tolerance"] for r in out["kernels"]):
        raise RuntimeError("RESEARCH_INTEGRITY_STOP: kernel failed")
    print("Dense kernels passed", sum(r["columns"] for r in out["kernels"]), flush=True)
    # Declared edge cases, including real fractional split, equality, ties and overweight prefix.
    fixtures = [([1], [1], 0, 1), ([1], [1], 1, 1),
                ([1, 2], [1, 1], 1, 0), ([1, 2], [1, 1], 1, 1),
                ([2, 3], [3, 2], 2, 1), ([2, 4], [1, 2], 3, 1),
                ([2, 3, 1], [2, 1, 1], 3, 1)]
    for index, (w, v, cap, d) in enumerate(fixtures):
        row = {"fixture": index, "weights": w, "values": v, "capacity": cap, "depth": d, "methods": {}}
        methods = {"qft_direct": lambda: build_qft_exact(w, v, cap, d, mcx_policy="direct"),
                   "qft_source_generic": lambda: build_qft_exact(w, v, cap, d, mcx_policy="source_generic"),
                   "compact_exact": lambda: build_compact_exact(w, v, cap, d),
                   "compact_dual": lambda: build_compact_root_dual(w, v, cap, d)}
        for name, builder in methods.items():
            try:
                compiled = builder()
                resources = common_resources(compiled.to_qiskit())
                check = run_full_mps(compiled, w, v, cap, d, dual=name.endswith("dual"))
                row["methods"][name] = {"resources": resources, "check": check,
                                        "metadata": getattr(compiled, "metadata", {})}
                print(index, name, check["status"], check.get("columns"), check.get("predicate_or_cleanup_failures"), flush=True)
                if check.get("predicate_or_cleanup_failures", 0):
                    out["rows"].append(row)
                    output.write_text(json.dumps(out, indent=2), encoding="utf-8")
                    raise RuntimeError("RESEARCH_INTEGRITY_STOP: full predicate failed")
            except Exception as exc:
                out["errors"].append({"fixture": index, "method": name, "error": type(exc).__name__ + ": " + str(exc)})
                output.write_text(json.dumps(out, indent=2), encoding="utf-8")
                raise
        out["rows"].append(row)
        output.write_text(json.dumps(out, indent=2), encoding="utf-8")
    completed = [m["check"] for row in out["rows"] for m in row["methods"].values() if m["check"]["status"] == "COMPLETED"]
    out["summary"] = {"classification": "SIMULATED", "dense_kernel_columns": sum(r["columns"] for r in out["kernels"]),
                      "dense_kernel_failures": sum(r["failed_columns_above_tolerance"] for r in out["kernels"]),
                      "full_method_cases": len(completed), "full_compiled_columns": sum(r["columns"] for r in completed),
                      "full_predicate_or_cleanup_failures": sum(r["predicate_or_cleanup_failures"] for r in completed),
                      "max_expected_amplitude_error": max((r["max_expected_amplitude_error"] for r in completed), default=0),
                      "seconds_measured": time.monotonic() - started}
    output.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out["summary"], indent=2), flush=True)


if __name__ == "__main__":
    main()
