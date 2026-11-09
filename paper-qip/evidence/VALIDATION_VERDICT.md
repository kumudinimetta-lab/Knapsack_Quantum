# Adversarial validation verdict

25 October 2026. This report supplements the frozen research milestone. No earlier paper, bibliography, implementation or raw ledger was changed. It deliberately separates mathematical coverage, gate correctness evidence, resource accounting, and historical novelty.

## Verdict

**The precisely scoped pruning-preservation construction is supported.** Fresh counterexample searches found no failure within its assumptions, and exhaustive arithmetic coverage of the original/core panels passed. Actual reversible-gate checks also passed in the retained completed runs. This is evidence for a credible construction contribution candidate, not a guarantee that every implementation path is error-free or that the contribution is historically new or sufficiently substantial for QIP.

The audit found issues that matter to presentation and testing: an unreliable simulator initialization path, idle workspace in the LP resource baseline, and fractional calculations that the LP baseline could safely omit. These were investigated rather than hidden. The stronger comparison changes the numerical headline and worsens the depth tradeoff.

## Exact claim that can be made

For a classically specified knapsack instance with positive integer weights, nonnegative integer profits, nonnegative capacity, and a fixed nonincreasing exact-efficiency prefix order, a certified bank preserves the Boolean predicate

`P + fractional_suffix_LP(R) < tau`

at every capacity-feasible prefix for integer tau. Capacity-infeasible prefixes are separately rejected. A gate implementation has a finite unsigned threshold register, so its input contract is **representable integer thresholds**, zero initial workspace, and an arbitrary XOR target. Mathematical floor preservation extends to all integer thresholds; the finite register does not encode arbitrary integers.

With integer incumbent L, setting tau=L+1 implements rejection when `floor(P+LP)<=L`. This must not be confused with the different test `P+LP<=L` on an unrounded fractional value.

The bank need not reproduce the numerical fractional LP value. It need not preserve rational thresholds, dynamic/nonprefix branching, LP-integrality flags, completion witnesses or LP-selected branching variables. An arbitrary user-supplied bank is not automatically LP-equivalent: its coverage must be established. The older Boolean builder requires strictly positive profits; the mathematical construction and separate QFT-bank builder admit zero profits. No whole-paper correctness or full quantum-walk implementation is claimed.

## Fresh mathematical validation

The independent theory audit re-derived the root-tail argument, integer-profit quotient, strict coverage intervals, finite-grid and arbitrary-rational cardinality certificates, tied-group DP-free radius, and repaired linear-cardinality barrier. It used an independently written **primal LP vertex enumerator**, not the shared greedy LP reference:

- 1,888 systematic/new-seed instances; 15,999 feasible prefixes: **0 root-tail value errors and 0 floor errors** for each of the grid, DP-free and continuous banks.
- 1,369 grid and 1,369 continuous minimum-cardinality certificates: **0 failures**.
- 1,637 independently reconstructed continuous critical intervals and 14 repaired-barrier endpoint checks: **0 mismatches**.

See `theory_claim_audit.md` and `theory_adversarial_audit_v2.json`. Explicit counterexamples to stronger statements are retained: fractional thresholds, nonprefix branching, replacing tied-group weight by one item, nonstrict radius, negative multipliers and unchanged LP semantics after integer gcd normalization.

The root then independently rebuilt reachable states using set-based subset sums and cross-product sorting. Its exact reference enumerates **all suffix dual breakpoints plus zero**, without calling the production greedy, interval or bank routines:

| Panel | Inputs | Every reachable (depth, residual-capacity) state | Four-bank floor comparisons | Mismatches |
|---|---:|---:|---:|---:|
| Original | 700 | 3,148,192 | 12,592,768 | 0 |
| Exact cores | 700 | 2,056,264 | 8,225,056 | 0 |
| Total | 1,400 | 5,204,456 | 20,817,824 | 0 |

These are **DERIVED exact arithmetic** checks of root-tail, minimum-grid, DP-free and continuous banks. Integer prefix profit cancels, so matching a residual floor covers every prefix with that state and every integer threshold. This is exhaustive **bank coverage**, not exhaustive large-circuit statevector simulation. The theory reviewer independently inspected this check and found no circular reference. The core state count includes 59 states skipped by the earlier all-fit shortcut; this explains its difference from the old compiler work count. All 23 all-fit cores, including 11 empty cores, are retained. A separate lineage check matched all 1,445 DP-free source-bank IDs/metadata/hashes with zero conflicts.

Artifacts: `root_all_reachable_v2_summary.json`, `root_all_reachable_v2_rows.jsonl`, `root_bank_lineage.json`. The first driver incorrectly assumed the original registry contained only 700 records; its empty result/source are preserved. The corrected run explicitly selects the declared main700 category from 720 total records, retaining the 15 scaled and 5 tiny auxiliary records outside this particular experiment's scope.

## Reversible gates and the integrity stop

Fresh **SIMULATED** tests used actual gate lists and the separate primal-vertex expected answer:

- QFT bank: 24 method-cases, 1,120 basis columns, **0 gate mismatches**. Certified cases have **0 LP-predicate disagreements**. A deliberately insufficient bank produces 8 expected LP disagreements across the method rows while correctly implementing its supplied-bank predicate; it is not counted as an LP-equivalent circuit.
- Boolean bank: 7 cases, 2,216 exact gate-interpreted columns, **0 gate mismatches**, including 548 invalid-depth encodings and both target values.
- Primitive-unitary coherent preparation: 2 checks spanning 64 logical amplitudes, **0 failures** at the unchanged 1e-8 tolerance.
- Four resource-profiler conditions matched complete Qiskit transpilation with **0 discrepancies**; four input-domain checks had **0 unexpected acceptance/rejection failures**.

`circuit_vertex_adversarial_resume.json` explicitly inherits five already completed basis conditions from the initial run. Counts are not pooled as independent samples. The stopped original superposition test remains separately failed in `circuit_vertex_adversarial.json`.

**RESEARCH_INTEGRITY_STOP was triggered and investigated.** For w=[2,4,1], v=[1,2,0], W=3, depth=1, an opaque partial-register `initialize` followed by Aer MPS simulation gave complex-amplitude error 0.2154. Two independent investigations reproduced an incorrect state **before any oracle gates** on the same 22-wire layout; native backend readouts and explicit tensor contraction agreed on that malformed state. Changing the cutoff or enable_truncation did not fix it. This was not a global-phase discrepancy and was not evidence that the tensor reader caused it.

Independent dense simulation of the complete unchanged 22-qubit raw/cancelled oracle matched the intended complex permutation with maximum errors about 4.77e-15 and 1.94e-15. Decomposed or explicit primitive-gate preparation also passed on the MPS backend at the original tolerance. The remaining planned tests resumed in a new file using native unitary preparation, with **no production-oracle change and no tolerance relaxation**. Thus the failed fixture's oracle check is resolved through independent dense/primitive-preparation evidence; the exact Aer implementation defect remains **UNRESOLVED**. The opaque partial-initialize path must not be used as a trusted validation method. See `theory_phase_readout_findings.md`, both triage families, and their preserved failures.

## Tighter resource comparison

The old frozen ratios are reproducible, but their scope needs care. They counted allocated qubits. Removing truly idle workspace while retaining every input/output wire changes the old median bank/LP qubit ratio from 0.4624 to **0.4817**. The bank remains smaller on all 105 inputs; it is no longer at most half on every input under this control.

The audit then found that the LP scan evaluated fractional products even before the root split, where a fractional split is impossible in the stated prefix model. A new isolated **root-aware LP control** omits those terms and tightens the comparison width accordingly. Its derivation preceded code; the pinned production module and all older raw data remain unchanged. The proof keeps the whole-item/take logic and separately rejects overweight inputs.

Validation of this control: **104 exact compact gate columns, 208 QFT basis columns across 8 conditions, and one primitive-prepared coherent condition spanning 16 amplitudes; 0 mismatches/dirty-workspace or coherent failures**. Four additional complete-transpiler comparisons matched the profiler exactly. Tests use independent primal vertices. This is a bounded control validation, not a new claim of exhaustive gate testing on large inputs.

On all 105 original representatives at depth floor(n/2), the new control completed with **0 caps and 0 compilation errors**. Both sides use the same direct-control QFT engine, exact inverse cancellation and quantum threshold interface. Active qubits retain all interface wires and every gate-touched wire.

| Bank / root-aware LP control, DERIVED logical resources | Median ratio | Lower / equal / higher |
|---|---:|---:|
| Allocated qubits | 0.4641 | 105 / 0 / 0 |
| Interface + touched qubits | 0.4908 | 105 / 0 / 0 |
| CX gates | 0.4981 | 105 / 0 / 0 |
| Arbitrary-angle u gates | 0.4995 | 105 / 0 / 0 |
| Common-basis DAG depth | 1.0720 | 38 / 0 / 67 |

Therefore the tighter headline is roughly **50% fewer CX gates and 51% fewer active qubits in median, with 7% greater median depth**. Worst depth ratio is 2.0480. These are ratios within our reconstructions, not device durations, fault-tolerant T costs or superiority to released R1. Large-input runs are resource-only. The older 59% CX saving remains a historical comparison to a weaker scan and should not be the sole headline. A separate final pass recomputed the new ratios and state counts with **0 discrepancies** (`final_crosscheck.json`). No optimal-baseline claim is supported: copied-control scheduling, additional compiler rewrites and classical-threshold specialization are still outside scope.

The last root-aware control was completed by the root after the reviewing agent reached its usage limit. Its pre-code derivation had been independently discussed; executable checks and a separate aggregation/transpiler pass are recorded. Do not describe this final control as having received a separate post-code multi-agent review.

## Contribution strength, provenance and paper status

The broad idea of affine Lagrangian bounds, multiplier sets or integer-floor pruning is prior work. See the primary-source distinctions in `PRIOR_WORK_RECHECK.md`, particularly Bożejko et al. (2024), equation (17), and Wilkening et al. (2025), Supplement F.2. The possible distinct contribution is the **static all-prefix integer-predicate compiler, coverage/minimum-cardinality certificates, worst-case limitation, and explicit clean reversible resource tradeoff**. Generic reversibility or an LP bound alone is insufficient as a novelty claim.

The audit strengthens confidence in that precise construction candidate. It does **not** establish global priority, sufficiently substantial advance over every closest implementation, guaranteed QIP acceptance, physical speedup, a full gate-model walk, or exhaustive dense statevectors for all 700 circuits. The expensive reachability compilers cannot be treated as free end-to-end acceleration; the DP-free variant avoids that particular preprocessing barrier but is not universally cheaper. Minimum cardinality does not minimize gates.

The independent integrity pass checked all **1,668 manifested files** against both current workspace and the frozen ZIP, reproduced raw resource summaries, and found **0 conflicts**. Paper source, PDF and all **45 bibliography entries** still match the restored backup. This validates the saved research provenance, not the old manuscript's unrelated theorem/citation/spectral claims. The current manuscript still needs its separately planned correction/restructuring pass.
