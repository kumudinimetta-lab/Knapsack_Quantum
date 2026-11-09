# Research advance: preserving LP pruning while changing the oracle

25 October 2026. Research milestone; manuscript not edited. The original paper, its 45 bibliography entries, all earlier raw results and failed attempts are retained.

## Assessment

There is now a more substantive candidate contribution than attaching a weaker cheap bound to the old algorithm: **compile the exact integer LP-pruning predicate into a static collection of affine bounds, and implement that same predicate reversibly.** The construction preserves pruning decisions throughout the specified static prefix tree. The supporting work includes exact arithmetic derivations, a worst-case limitation, two different reversible arithmetic implementations, resource comparisons, and independent adversarial checks.

This is a candidate research contribution, not a claim of historical priority, a demonstrated quantum optimization speedup, or evidence that QIP will accept the paper. Generic LP duality, interval stabbing and reversible arithmetic are established ingredients. Whether this particular combination and its scope are sufficiently distinct from all closest work remains **UNRESOLVED**. The strongest defensible presentation is an oracle-construction and resource-tradeoff paper.

## Mathematical object and scope

Items have positive integer weights and nonnegative integer profits and are sorted once by exact efficiency. At depth d, let P be accrued integer profit, R the remaining capacity of a feasible prefix, and U_d(R) the exact fractional-knapsack relaxation on the suffix. For a nonnegative rational multiplier lambda define

`F_d(R,lambda) = lambda*R + sum_suffix max(v_i - lambda*w_i, 0)`.

LP duality gives `F >= U`. A bank B preserves every strict integer-threshold rejection at that prefix exactly when

`floor(min_{lambda in B} F_d(R,lambda)) = floor(U_d(R))`.

The integer P cancels from this condition. Each state's coverage is therefore the **strict** inequality `F_d(R,lambda) < floor(U_d(R))+1`. Convexity makes this an interval in lambda. These statements concern integer thresholds and feasible density-prefix states; infeasible prefixes are separately rejected by the capacity predicate.

They do **not** preserve exact rational LP values, LP-integrality flags, completion witnesses, dynamic branching choices, or arbitrary variable orderings. Consequently, “same tree” means the same specified static tree using this rejection predicate. It does not license replacing every use of an LP solver in a different branch-and-bound algorithm.

Detailed derivations, including endpoint strictness, counterexamples and independent checks, are in `theory_compressed_bank_derivation.md`, `theory_continuous_bank_derivation.md` and `theory_construction_results.md`. Derivations preceded implementation; the independent audit is a separate pass.

## Four constructions and a limitation

1. Root-tail elimination removes density multipliers above the root split and retains the remaining ratios plus zero. This avoids capacity reachability DP and preserves the exact relaxation in the stated prefix model.
2. The finite-grid compiler enumerates reachable prefix weights and greedily stabs coverage intervals on the density grid. It minimizes multiplier count **on that grid**.
3. A conservative DP-free compiler uses a proved strict radius around each density group to share multipliers. It requires neither the optimum, tree-size advice nor capacity DP. It need not find the smallest bank.
4. The continuous compiler derives exact rational open/closed coverage endpoints and greedily stabs cells. It minimizes cardinality among all nonnegative rational multipliers for the enumerated states. Mediant representatives control coefficient growth in these experiments, without a minimum-bit-width claim.

Allowing non-density multipliers can matter: for `w=[1,1], v=[1,1], W=1`, the density grid `{0,1}` needs both points, while the single multiplier `1/2` preserves all feasible-prefix integer floors. This is a small mathematical illustration, not a benchmark result. A separate independently checked example and gate probe are retained in `reviewer_offgrid_*`.

There is also a gcd-one family requiring linearly many multipliers even when arbitrary rational choices are allowed. Its disjoint strict coverage intervals prove that small banks cannot be guaranteed in general. The first proposed family was invalidated by gcd normalization; the failed family and repaired proof are retained. This is a bank-cardinality lower bound, not a quantum query lower bound or hardness proof.

## Broad gate compilation results

All ratios below are **DERIVED** logical resources from actual reversible netlists. There are 700 original R=100 inputs, 700 exact preprocessed cores, and 45 separate high-coefficient inputs. Original and core inputs are paired transformations, not independent samples. The 11 empty cores are retained. Circuit resources include compute, copy and uncompute.

The comparator is the per-instance, per-metric minimum among our old exact scan, a tightened-width exact scan, and a newly proved directed-up fixed-point scan that preserves integer rejection. This is a conservative lower envelope of three implementations, **not** one circuit simultaneously attaining every minimum.

| Compiler | Panel | Median CCX ratio | Lower / equal / higher CCX |
|---|---|---:|---:|
| Minimum density grid | Original 700 | 0.6945 | 619 / 0 / 81 |
| DP-free sufficient | Original 700 | 0.7470 | 575 / 0 / 125 |
| Minimum arbitrary rational | Original 700 | 0.8657 | 475 / 0 / 225 |
| Minimum density grid | Core 700 | 0.4898 | 662 / 11 / 27 |
| DP-free sufficient | Core 700 | 0.5511 | 643 / 11 / 46 |
| Minimum arbitrary rational | Core 700 | 0.6383 | 584 / 11 / 105 |

The DP-free construction's median logical gate-depth ratios are 0.2108 on original inputs and 0.2314 on cores, relative to that scan lower envelope. These are native Boolean-gate depth comparisons within that implementation family, not physical execution time. Comparison with QFT arithmetic requires a common decomposed gate basis and gives different depth tradeoffs; see the separate matched QFT report.

**Minimum cardinality is not minimum circuit cost.** The continuous compiler reduces the grid minimum on 128 original and 105 core inputs, yet usually has greater circuit cost because rational coefficient widths also matter. All regressions are included. Exact reachability compilation also costs substantially more than classical profit DP on these small-capacity cases: continuous construction took 37.42 aggregate host seconds versus 0.299 for that DP reference on originals, and 24.24 versus 0.206 on cores (**MEASURED**, diagnostic local timings). This rules out treating that preprocessing as free in an end-to-end speedup claim. The DP-free method avoids this particular preprocessing barrier.

The 45 high-capacity cases explicitly retain root-tail fallbacks for reachability-based methods; no minimum-bank claim applies to those fallbacks. The DP-free method completed directly but achieved no additional bank-cardinality reduction there. These results remain in the ledger.

Full figures, class breakdowns, outliers, source hashes and exact ratios are in `compilation_extended_summary.json` and `compilation_extended_pairs.jsonl`.

## Validation and what was not tested

**SIMULATED** exact Boolean-gate propagation across the 11 new scan/bank ledgers: 7,045 circuit records and 10,843,350 checked basis columns, **0 predicate mismatches and 0 dirty-workspace columns**. These columns deliberately overlap across methods; they are not independent observations. The test generator uses seed 2026102407, every encoded depth, selected zero/all-one/random prefixes, nearby integer thresholds, and both initial target values. The bank ledgers check against the exact non-truncated LP predicate. This is not exhaustive enumeration of every assignment and threshold on every large input.

Independent checks include tiny exhaustive comparisons against separately computed LP vertices; brute interval minima and critical-interval certificates; width/overflow checks; and independently reproduced resource aggregation. They are documented in `independent_new_controls_review.md` and the `reviewer_*` artifacts. Claims must cite the particular panel, precision and validation ledger rather than saying globally “h is correct.”

The QFT construction receives separate phase-sensitive full-gate simulation on tiny fixtures, including complex superpositions, overweight states, zero profits, overlapping rejection flags and uncomputation. Larger QFT runs are resource compilation only. The literal requested exhaustive dense statevector validation over all 700 large inputs has **not** been fulfilled: their workspace is too large for dense simulation. Exact Boolean basis propagation and small QFT/MPS checks are reported separately rather than relabelled as that experiment.

An initial MPS amplitude-readout failure was preserved and independently reproduced as an API/readout discrepancy. The replacement contracts saved MPS tensors and was cross-checked against dense complex statevectors. The failed run is not counted as a passing circuit test. No raw data was manually corrected.

## Closest implementation and fair comparison

The earlier source audit traced Wilkening et al.'s R1 evaluation path, including its actual specialized simulator, resource routines and analytic backtracking model. It did not find a full clean fractional-LP predicate netlist in that audited path. This observation is restricted to that path and does not imply that the authors failed to implement their algorithm or that our implementation is faster.

Our second arithmetic engine reconstructs primitives from Draper's *Addition on a Quantum Computer* (2000), Sections 3 and 5, and Wilkening et al. (2025), Supplement E.3–E.5. It is **our declared reconstruction**, with shared serial scratch and ideal arbitrary-angle rotations; it does not reproduce their optimized copied-control parallel scheduling or their released simulator. Primary-source references and cached evidence are recorded in `PILOT_REPORT.md` and the previous source audit.

The fair new control compares LP scan and DP-free bank **inside this same QFT engine**, on identical fixed-depth quantum prefix/threshold interfaces. Both direct and literal generic control decompositions are retained. Exact inverse-QFT cancellations, including commuting past disjoint wires, are applied equally to both sides. Raw uncancelled ledgers remain available; cancelled comparisons are primary. Common `{u,cx}` resources are logical all-to-all counts and DAG depths, with no hardware calibration or Clifford+T rotation-synthesis claim. The representative cohort is predeclared: first three trials in each of five classes at each of seven sizes, giving 105 inputs. Large-input results are resource-only.

The completed comparison contains **840/840 resource rows, with zero caps or compilation errors**. For the primary cancelled-direct bank/LP comparison, median ratios are **0.4624 qubits, 0.4099 u gates, 0.4091 CX gates, and 0.9433 depth**. Qubits, u and CX are lower on all 105 inputs; depth is lower on 57 and higher on 48, with a worst depth ratio of 1.9165. Aggregate host compilation/profile time was 283.1 seconds (MEASURED). Ratios and counts of netlist resources are DERIVED. This is a meaningful same-function resource result within our matched reconstruction, with an explicit depth tradeoff. It does not demonstrate superiority to the released R1 implementation. Exact data, per-class results and both control policies are in `qft_bank_full105_*`.

## Paper fit and remaining limitations

The paper can be rebuilt around the precise predicate compiler, its sufficient and minimum-cardinality constructions, the worst-case barrier, and derived logical resource tradeoffs under two arithmetic engines. The fixed-point lemma provides an exact-pruning control. This directly addresses an unsynthesized bounding-oracle gap and provides a concrete research result to explain.

Before manuscript revision, retain these limits: global priority remains unresolved; there is no complete gate-model quantum walk, IBM execution, physical runtime advantage, guaranteed acceptance, or demonstrated asymptotic improvement. Existing paper errors in citations, witness/search theorem attribution, schedule semantics and spectral interpretations still need explicit repair. New oracle experiments do not validate unrelated old claims.

The eventual revision should preserve legitimate references and describe negative findings, compilation overhead, baseline choices, and every capped or trivial case. No manuscript text or bibliography was removed during this research milestone.
