# Independent follow-up validation and aggregation audit

23 October 2026. No manuscript, bibliography, production source or historical raw data was modified. New reviewer scripts/results only.

## Exact fixing

See `fixing_audit_result.md` and `fixing_bijection_summary.json`. Exhaustive tiny, explicit adversarial and seed2026102309 random tests cover 6,664 instances, 19,685 independently enumerated opposite-branch LP checks and 28,931 threshold-set bijection checks, with 0 failures (DERIVED exact classical references/counts). The function preserves all feasible assignments of value>=greedy incumbent L and all optima, with shifted-capacity/shifted-value reconstruction. It does not preserve arbitrary assignments below L. The exact tested source remained unchanged.

## Every-input, every-depth scoped compiled-gate check

`reviewer_700_all/summary.json`: each of exact_single, fixedpoint_single and root_dual completed all 700 saved benchmark inputs, with **534,882 input/target basis columns per family, 0 predicate mismatches, 0 dirty-workspace columns and 0 unsafe-pruning outputs** (SIMULATED, scoped clean-workspace samples). Build caps:0 for each family. Total circuit columns:1,604,646. Sources/registry remained unchanged.

The sample policy covers every encoded depth, including invalid depths, but only selected full selection-bit patterns and thresholds: zero/all-one/fixed-seed random selections, zero/max/random thresholds and both sides of exact LP/root-dual bound floors, with both output targets. Every selected encoding and reference flag is retained. This is **not exhaustive simulation of all possible assignments/thresholds on the700 instances**. The independently written exact Fraction reference is separate from the gate arithmetic; its greedy LP semantics were independently checked by vertex enumeration in the tiny audit.

The pilot n12/n18/n24 run is separately retained in `reviewer_700_pilot/`. Code is `reviewer_700_validation.py`; pre-run policy is `reviewer_700_validation_plan.md`. Resource vectors from actual gate lists are DERIVED; build host time is MEASURED; output/cleanup is SIMULATED; seed and sample/budget policy are HARDCODED. No QPU job, full walk or runtime claim follows.

## Compact arithmetic: independent controls

Primary source read: Cuccaro, Draper, Kutin and Moulton, *A new quantum ripple-carry addition circuit*, quant-ph/0410184v1, Sections2 and4.3. The implementation uses the simple MAJ/UMA pattern and high-carry comparison, not the optimized Section3 counts. Inspecting the code found no primitive alias, sign, carry-reset or forward/reverse-gate-order failure under its stated clean-scratch preconditions. Product accumulators are uncomputed before reuse, and the fixed-depth interface is explicit.

An independent scalar interpreter exhausts primitive operands separately from the inherited bit-plane simulator:

- Modular adders widths1..5:1,364 columns,0 mismatches (SIMULATED).
- Unsigned strict comparators widths1..5 with both output bits:2,728 columns,0 mismatches (SIMULATED).
- Controlled constant addition/subtraction widths1..4, all constants/controls/accumulators:1,360 columns,0 mismatches (SIMULATED).

Four matching fixed-depth families (compact/out-of-place root dual and compact/out-of-place exact LP) were checked independently on34 input-depth cases per family:7,012 prefix/threshold/target columns per family,0 predicate mismatches and0 dirty-workspace columns (SIMULATED, ten explicit tiny inputs). See `reviewer_compact_probe.json` and preplan. The exact reference again enumerates fractional vertices; the dual reference uses the direct rational envelope.

A different nonempty dense case w=[1,2],v=[1,3],W=2,d=1 uses22 qubits and32 independent complex random input/target amplitudes, seed2026102321. Qiskit dense evolution agrees with direct rational-dual XOR action with maximum amplitude error0 and0 differing amplitudes above1e-12 (SIMULATED). The original20-qubit-cap skip is retained in `reviewer_compact_dense.json`; a bounded22-qubit rerun is separately saved in `reviewer_compact_dense_q22.json`. This is a fixed-depth dual component, not a full walk or broad compact-family validation.

Gate-count calculation uses the explicit X/CX/CCX list; depth follows wire dependencies and is a valid construction schedule, not a compiler-independent minimum. The reported compact variant substantially cuts workspace while increasing gates and depth. This is meaningful negative/control evidence. A fixed-depth result must not be generalized to the coherent-depth700-input construction without further implementation and checks.

## Paired aggregator audit

Reviewed `analyze_paired.py` for joins, ratios, complete-pair denominators and censoring before its planned retry-overlay patch. Independent direct checks of the retained input/tree panels found:

-700 core resource aliases,389 inherited-original resource mappings;0 mappings to different weights, values or capacity (DERIVED registry comparisons).
-715 original/scaled tree records,700 core records and45 independent stress records, all unique within panels (DERIVED ledger counts).
-0 complete-pair violations of exact-LP tree size<=weaker tree size (DERIVED comparison).
-0 core/original global threshold mismatches after adding fixed-in value offsets (DERIVED comparison).

The compiled quantum-threshold costs are legitimately shared across fixed test thresholds for the same instance. Resource pairs are per input, whereas the two tree conditions are summarized separately. The complete-pair cost ratios and `(C+h)*sqrt(T)` ratios have the intended numerator/denominator, and the break-even overhead algebra is correct. Shared overhead is scaled in the exact construction's cost unit separately for each metric; it is a sensitivity analysis, not a physical overhead estimate. Certificate ratios use complete trees and require the separate cap ledger to avoid a survivor-biased global claim.

Remaining reporting/check recommendations, some already communicated to the parent:

1. Hash the aliases file, aggregator source and retry overlay as well as raw inputs/resources; verify expected key sets, not only row counts.
2. Do not treat wrappers omitted by preselection as build failures; their resource ratio denominator is the preselected subset. Distinguish not scheduled from a cap/missing artifact in presentation.
3. A rerun with higher time allowance must keep the original time-cap record and explain the explicit replacement rule; do not choose whichever measured outcome is favourable. Confirm matched method/target/node cap in each overlay.
4. For capped trees, do not turn processed vertices into exact T. Complete-pair medians remain selected-case summaries; quote denominators and cap rates next to them.
5. Eleven empty cores are classically resolved and need no optimization QPU calls. Their synthetic component gate counts describe a function, not incurred optimization work.
6. The current shared certificate may give identical schedules for different predicates. Actual-T proxy wins cannot simultaneously be called certified query/gate wins without paying for the appropriate tree-bound procedure.

No new integrity-stop trigger was found in these selected independent checks. The historical manuscript's known correctness/citation/provenance issues remain separate until repaired. This review supports the feasibility and scope of the experiment; it does not certify priority, a new asymptotic result, a full-walk resource reduction or acceptance by QIP.
