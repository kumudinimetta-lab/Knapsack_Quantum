"""Bounded fixed-depth compiler-sensitivity experiment, all outcomes retained."""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from simulation.pruning_study_20261023.compact_sensitivity import Ripple, FIXED_BUILDERS
from simulation.pruning_study_20261023.circuits import BuildBudget, CircuitBuildCap


def direct_bound(w, v, capacity, depth, prefix, dual):
    order = sorted(range(len(w)), key=lambda i: Fraction(v[i], w[i]), reverse=True)
    weight = sum(w[order[j]] for j in range(depth) if (prefix >> j) & 1)
    value = sum(v[order[j]] for j in range(depth) if (prefix >> j) & 1)
    rem = capacity - weight
    if rem < 0:
        return None
    if dual:
        root_rem, lam = capacity, Fraction(0)
        for i in order:
            if w[i] > root_rem:
                lam = Fraction(v[i], w[i])
                break
            root_rem -= w[i]
        return Fraction(value) + lam * rem + sum(max(Fraction(v[i]) - lam * w[i], 0) for i in order[depth:])
    result = Fraction(value)
    for i in order[depth:]:
        if w[i] > rem:
            return result + Fraction(rem * v[i], w[i])
        rem -= w[i]
        result += v[i]
    return result


def primitives():
    rows = []
    for width in range(1, 6):
        for comparison in (False, True):
            c = Ripple(2 * width)
            a, b = list(range(width)), list(range(width, 2 * width))
            c.less(a, b, c.output) if comparison else c.extend(c.adder(a, b))
            bad = 0
            for encoded in range(1 << (2 * width + 1)):
                state = encoded
                for t, controls in c.gates:
                    if all((state >> q) & 1 for q in controls):
                        state ^= 1 << t
                av, bv, target = encoded & ((1 << width) - 1), (encoded >> width) & ((1 << width) - 1), encoded >> (2 * width)
                expected = (av | (bv << width) | ((target ^ int(av < bv)) << (2 * width))) if comparison else (
                    av | (((av + bv) & ((1 << width) - 1)) << width) | (target << (2 * width)))
                bad += state != expected
            rows.append({"width": width, "primitive": "less" if comparison else "add_mod",
                         "classification": "SIMULATED", "columns": 1 << (2 * width + 1),
                         "mismatches": bad, "gates": len(c.gates), "qubits": c.next_wire})
    return rows


def verify(c, w, v, cap, d, method):
    inputs = range(1 << c.num_inputs)
    references = [direct_bound(w, v, cap, d, p, method.endswith("dual")) for p in range(1 << d)]
    mismatch, dirty, first = 0, 0, []
    for target in (0, 1):
        flags, garbage = c.simulate_columns(inputs, target)
        dirty += garbage
        for encoded, flag in enumerate(flags):
            p, tau = encoded & ((1 << d) - 1), encoded >> d
            ref = references[p]
            want = target ^ int(ref is None or ref < tau)
            if flag != want:
                mismatch += 1
                if len(first) < 3:
                    first.append({"prefix": p, "tau": tau, "target": target, "expected": want,
                                  "actual": flag, "bound": str(ref)})
    return {"classification": "SIMULATED", "columns": 2 * len(inputs),
            "predicate_mismatches": mismatch, "dirty_columns": dirty, "first_failures": first}


def dense_nonempty(c):
    import numpy as np
    from qiskit.quantum_info import Statevector
    if c.num_qubits > 18:
        return {"status": "SKIPPED_DENSE_QUBIT_CAP", "qubits": c.num_qubits, "cap": 18}
    count = 1 << c.num_inputs
    rng = np.random.default_rng(2026102301)
    amps = rng.normal(size=2 * count) + 1j * rng.normal(size=2 * count)
    amps /= np.linalg.norm(amps)
    before, expected = np.zeros(1 << c.num_qubits, complex), np.zeros(1 << c.num_qubits, complex)
    for target in (0, 1):
        for encoded in range(count):
            before[encoded | (target << c.output)] = amps[target * count + encoded]
            p, tau = encoded & 1, encoded >> 1
            bound = direct_bound([1], [1], 0, 1, p, True)
            flag = target ^ int(bound is None or bound < tau)
            expected[encoded | (flag << c.output)] = amps[target * count + encoded]
    actual = Statevector(before).evolve(c.to_qiskit()).data
    error = float(np.max(np.abs(actual - expected)))
    return {"status": "COMPLETED", "classification": "SIMULATED", "qubits": c.num_qubits,
            "nonzero_input_amplitudes": 2 * count, "max_amplitude_error": error,
            "mismatches_above_1e-12": int(error > 1e-12)}


def main():
    started = time.monotonic()
    out = {"scope": "Fixed classical depth; quantum prefix/threshold, explicit X/CX/CCX; not full walk.",
           "primitives": primitives(), "rows": [], "dense": [], "errors": []}
    if any(x["mismatches"] for x in out["primitives"]):
        Path(__file__).with_name("compact_validation_results.json").write_text(json.dumps(out, indent=2))
        raise RuntimeError("RESEARCH_INTEGRITY_STOP: primitive mismatch")
    cases = [([], [], 0, "empty"), ([1], [1], 0, "nonempty_capacity0"),
             ([1], [1], 1, "one_allfit"), ([2, 3, 4, 5], [3, 4, 5, 8], 8, "tiny4"),
             ([3, 5, 7, 8], [3, 5, 7, 8], 13, "ties4"),
             ([4, 7, 6], [5, 6, 2], 7, "tiny3"),
             ([9, 10, 1], [7, 5, 2], 3, "overweight"),
             ([2, 4, 6], [3, 6, 9], 20, "allfit_gcd")]
    records = json.loads(Path(__file__).with_name("inputs.json").read_text(encoding="utf-8"))["records"]
    pilots = [r for r in records if r.get("category") == "main700" and r["n"] == 12 and r["seed"] == 12000]
    for w, v, cap, label in cases:
        for d in range(len(w) + 1):
            row = {"category": "tiny_all_depths", "label": label, "weights": w,
                   "values": v, "capacity": cap, "depth": d, "methods": {}}
            for name, builder in FIXED_BUILDERS.items():
                try:
                    c = builder(w, v, cap, d)
                    row["methods"][name] = {"status": "COMPLETED", **verify(c, w, v, cap, d, name),
                                            "resources": c.resources(), "metadata": c.metadata}
                    if label == "nonempty_capacity0" and d == 1:
                        out["dense"].append({"method": name, **dense_nonempty(c)})
                except Exception as exc:
                    out["errors"].append({"label": label, "depth": d, "method": name,
                                           "error": type(exc).__name__ + ": " + str(exc)})
            out["rows"].append(row)
    for source in pilots:
        w, v, cap, d = source["weights"], source["values"], source["capacity"], 6
        row = {"category": "fixed_depth_pilot", "source_id": source["id"], "weights": w,
               "values": v, "capacity": cap, "depth": d, "methods": {}}
        for name, builder in FIXED_BUILDERS.items():
            try:
                c = builder(w, v, cap, d, budget=BuildBudget(150_000, 2_000_000, 60))
                row["methods"][name] = {"status": "COMPLETED", **verify(c, w, v, cap, d, name),
                                        "resources": c.resources(), "metadata": c.metadata}
            except CircuitBuildCap as exc:
                row["methods"][name] = {"status": "CAPPED", "reason": exc.reason, "counters": exc.counters}
            except Exception as exc:
                out["errors"].append({"source_id": source["id"], "method": name,
                                       "error": type(exc).__name__ + ": " + str(exc)})
        out["rows"].append(row)
        print(source["id"], "complete", flush=True)
    completed = [x for row in out["rows"] for x in row["methods"].values() if x["status"] == "COMPLETED"]
    out["summary"] = {"classification": "SIMULATED", "method_cases": len(completed),
                      "columns": sum(x["columns"] for x in completed),
                      "predicate_mismatches": sum(x["predicate_mismatches"] for x in completed),
                      "dirty_columns": sum(x["dirty_columns"] for x in completed),
                      "primitive_columns": sum(x["columns"] for x in out["primitives"]),
                      "primitive_mismatches": sum(x["mismatches"] for x in out["primitives"]),
                      "elapsed_seconds_measured": time.monotonic() - started}
    Path(__file__).with_name("compact_validation_results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out["summary"], indent=2), flush=True)
    assert not out["errors"], out["errors"]
    assert out["summary"]["predicate_mismatches"] == out["summary"]["dirty_columns"] == 0
    assert all(x.get("mismatches_above_1e-12", 0) == 0 for x in out["dense"])


if __name__ == "__main__":
    main()
