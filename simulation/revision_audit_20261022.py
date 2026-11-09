"""Non-destructive, reproducible checks for the manuscript revision.

Writes only research_log/revision_20261022_results.json (new audit artifact).
No historical experimental JSON is overwritten. Run from the repository root.
"""
import argparse
from collections import Counter, defaultdict
from dataclasses import asdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import time

import numpy as np

from benchmark_v5 import (gen_uncorrelated, gen_weakly_correlated,
                         gen_strongly_correlated, gen_subset_sum,
                         gen_inverse_strongly)
from exact_knapsack import (lp_bound, reduced_cost_fixing, dynamic_programming,
                            branch_and_bound)
from oracle_h.node_bound_reversible import (build_node_bound, exact_node_bound,
                                            precision_bits)

ROOT = Path(__file__).resolve().parents[1]
GENERATORS = [gen_uncorrelated, gen_weakly_correlated, gen_strongly_correlated,
              gen_subset_sum, gen_inverse_strongly]


def run_benchmark():
    rows = []
    started = time.perf_counter()
    for gen in GENERATORS:
        for n in [12, 14, 16, 18, 20, 22, 24]:
            for trial in range(20):
                seed = n * 1000 + trial
                w, v, cap, kind = gen(n, seed=seed)
                fi, core, fo = reduced_cost_fixing(n, w, v, cap)
                cw, cv = [w[i] for i in core], [v[i] for i in core]
                residual = cap - sum(w[i] for i in fi)
                fixed_value = sum(v[i] for i in fi)
                optimum = dynamic_programming(w, v, cap)
                core_opt = dynamic_programming(cw, cv, residual)
                bb, nodes, _, _, capped = branch_and_bound(cw, cv, residual,
                                                           max_nodes=1000000)
                zlp = lp_bound(w, v, cap)
                rows.append({"type": kind, "n": n, "seed": seed, "m": len(core),
                             "fixed_in": len(fi), "fixed_out": len(fo),
                             "optimum": optimum, "lp_gap": str(zlp - optimum),
                             "fixing_mismatch": fixed_value + core_opt != optimum,
                             "bb_mismatch": not capped and fixed_value + bb != optimum,
                             "bb_capped": capped, "core_nodes": nodes})
        print("MEASURED exact benchmark completed:", kind, flush=True)
    return {"classification": "MEASURED_CLASSICAL_WITH_DERIVED_EXACT_LP",
            "instances": len(rows), "fixing_mismatches": sum(r["fixing_mismatch"] for r in rows),
            "bb_mismatches": sum(r["bb_mismatch"] for r in rows),
            "capped": sum(r["bb_capped"] for r in rows), "rows": rows,
            "elapsed_seconds": time.perf_counter() - started}


def run_oracle(limit=None):
    rows = []
    for gen in GENERATORS:
        for n in [12, 14, 16, 18, 20, 22, 24]:
            for trial in range(20):
                seed = n * 1000 + trial
                w, v, cap, kind = gen(n, seed=seed)
                depth = 3
                circuit = build_node_bound(w, v, cap, depth, 0, quantum_threshold=True)
                inputs = range(1 << circuit.num_inputs)
                flags, dirty = circuit.simulate_columns(inputs)
                inverse_flags, inverse_dirty = circuit.simulate_columns(inputs, output_bit=1)
                threshold_range = 1 << circuit.threshold_bits
                bad = 0
                for prefix in range(1 << depth):
                    upper = exact_node_bound(w, v, cap, depth, prefix)
                    floor = None if upper is None else upper.numerator // upper.denominator
                    for tau in range(threshold_range):
                        index = prefix + (tau << depth)
                        expected = int(floor is None or tau > floor)
                        bad += flags[index] != expected
                        bad += inverse_flags[index] != 1 - expected
                rows.append({"type": kind, "n": n, "seed": seed,
                             "depth": depth, "k": circuit.k,
                             "threshold_bits": circuit.threshold_bits,
                             "statevector_columns": len(inputs) * 2,
                             "predicate_mismatches": bad,
                             "dirty_columns": dirty + inverse_dirty,
                             **circuit.resources()})
                if limit and len(rows) >= limit:
                    return {"classification": "SIMULATED_EXACT_SPARSE_STATEVECTOR",
                            "rows": rows, "partial": True}
        print("SIMULATED exhaustive depth-3 oracle completed:", kind, flush=True)
    return {"classification": "SIMULATED_EXACT_SPARSE_STATEVECTOR", "rows": rows,
            "partial": False,
            "scope": "All prefix/threshold/target basis states at depth 3; workspace initially zero. Not all depths or a full walk."}


def run_small_oracle():
    instances = [([2, 3, 4, 5], [3, 4, 5, 8], 8),
                 ([3, 5, 7, 8], [3, 5, 7, 8], 13),
                 ([4, 7, 6], [5, 6, 2], 7)]
    records = []
    for w, v, cap in instances:
        total = bad = dirty = 0
        profiles = []
        for depth in range(len(w) + 1):
            c = build_node_bound(w, v, cap, depth, 0, quantum_threshold=True)
            inputs = range(1 << c.num_inputs)
            for target in (0, 1):
                flags, dc = c.simulate_columns(inputs, target)
                dirty += dc
                for p, flag in enumerate(flags):
                    upper = exact_node_bound(w, v, cap, depth, p & ((1 << depth)-1))
                    expected = target ^ int(upper is None or upper < (p >> depth))
                    total += 1
                    bad += flag != expected
            profiles.append({"depth": depth, **c.resources()})
        records.append({"weights": w, "values": v, "capacity": cap,
                        "columns": total, "mismatches": bad, "dirty": dirty,
                        "profiles": profiles})
    # Independent standard dense-statevector check on a genuinely small circuit.
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
    c = build_node_bound([2], [1], 2, 1, 0, quantum_threshold=True)
    qc = QuantumCircuit(c.num_qubits)
    qc.h(range(c.num_inputs))
    sv = Statevector.from_instruction(qc.compose(c.to_qiskit())).data
    expected = np.zeros_like(sv)
    for p in range(1 << c.num_inputs):
        upper = exact_node_bound([2], [1], 2, 1, p & 1)
        flag = int(upper < (p >> 1))
        expected[p | (flag << c.output)] = 1 / np.sqrt(1 << c.num_inputs)
    max_error = float(np.max(np.abs(sv - expected)))
    return {"classification": "SIMULATED", "instances": records,
            "independent_dense_check": {"weights": [2], "values": [1],
                "capacity": 2, "depth": 1, "qubits": c.num_qubits,
                "max_amplitude_error": max_error}}


def run_counterexamples():
    equality = Fraction(5) + 3 * Fraction(2, 6)
    tests = []
    for k in range(1, 17):
        truncated = Fraction(5) + Fraction(3 * ((2 << k) // 6), 1 << k)
        tests.append({"k": k, "exact": str(equality), "truncated": str(truncated),
                      "naive_false_prune": truncated < 6,
                      "robust_false_prune": truncated <= Fraction(6) - Fraction(1, 7)})
    families = []
    for n in range(2, 101):
        M, q = 2*n*n, n//2
        w = [2*(M+i) for i in range(1,n+1)]
        v = [2]*n
        cap = sum(w[:q]) + M+q+1
        fi, core, fo = reduced_cost_fixing(n,w,v,cap)
        gap = lp_bound(w,v,cap)-2*q
        families.append({"n":n,"gap":str(gap),"core":len(core),
                         "valid":not fi and not fo and len(core)==n
                         and gap==1 and sum(w[-q:])<=cap and sum(w[:q+1])>cap})
    return {"classification":"DERIVED_EXACT_ARITHMETIC_CHECKS",
            "equality_counterexample":tests,"integer_families":families}


def run_recovery():
    from quantum_backtracking import quantum_bb_optimize
    rows = []
    for gen in GENERATORS:
        for n in [0,1,2,3,4,5,6,7,8]:
            for trial in range(3):
                if n:
                    w,v,cap,kind=gen(n,seed=1000*n+trial,R=15)
                else:
                    w,v,cap,kind=[],[],0,gen.__name__
                result=quantum_bb_optimize(w,v,cap,constant=2,K=11,max_nodes=2000)
                rows.append({"generator":kind,"n":n,"seed":1000*n+trial,
                             "capped":result is None,
                             "result":None if result is None else asdict(result)})
    return {"classification":"SIMULATED_ANALYTICAL_MAJORITY_WITH_SCHEDULED_QUERIES",
            "rows":rows,"capped":sum(r["capped"] for r in rows),
            "mismatches":sum(not r["result"]["correct"] for r in rows if not r["capped"])}


def summarize_archives():
    spectral=json.loads((ROOT/'simulation/quantum_walk_spectral_full.json').read_text())
    records=spectral['records']
    groups=defaultdict(list)
    for r in records:
        groups[(r['class'],r['n'],r['seed'])].append(r)
    counts=Counter((r['status'],r.get('case_type','seed')) for r in records)
    completed=[r for r in records if r['status']=='COMPLETED']
    paired=Counter(len(v) for v in groups.values())
    ortools=json.loads((ROOT/'simulation/classical_benchmark/raw_results/benchmark_data.json').read_text())
    solved=[r for r in ortools if r['or_opt'] and not r['bb_hit_limit']]
    return {"spectral":{"manifest":spectral['manifest'],
                         "status_counts":{str(k):v for k,v in counts.items()},
                         "seed_groups":len(groups),"records_per_seed":dict(paired),
                         "completed":len(completed),"records":len(records)},
            "ortools":{"attempted":len(ortools),"both_solved":len(solved),
                       "mismatches":sum(not r['match'] for r in solved),
                       "cutoff_rows":len(ortools)-len(solved)}}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--part',choices=['all','oracle','reference','recovery','small'],default='all')
    parser.add_argument('--limit',type=int)
    args=parser.parse_args()
    out=ROOT/f'research_log/revision_20261022_{args.part}_results.json'
    result={"date":"2026-10-22","python":platform.python_version(),"part":args.part}
    if args.part in ['all','reference']:
        result['reference']=run_benchmark()
        result['counterexamples']=run_counterexamples()
        result['archives']=summarize_archives()
    if args.part in ['all','oracle']:
        result['oracle']=run_oracle(args.limit)
    if args.part in ['all','small']:
        result['small_oracle']=run_small_oracle()
    if args.part in ['all','recovery']:
        result['recovery']=run_recovery()
    result['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in [Path(__file__),ROOT/'simulation/exact_knapsack.py',
                                       ROOT/'simulation/oracle_h/node_bound_reversible.py',
                                       ROOT/'simulation/quantum_backtracking.py']}
    out.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('Wrote',out,flush=True)


if __name__=='__main__':
    main()
