# Introduction and Sections 3–6 review

27 October 2026. Scope: Introduction, problem/contract, certified banks, reversible implementation/control, and evaluation protocol. The abstract and literature review were preserved. Results, discussion, conclusion and appendices remain for their separate editorial review. All figures/tables were checked for numbering and layout. This review is a separate same-agent pass, not independent certification or proof that no errors remain.

## Findings and corrections

1. **Contract wording error:** a capacity-feasible prefix always has an integer completion by choosing no further items. Nonrejection fails to guarantee a completion *reaching the target*, rather than any completion. Exact counterexample: w=(2), v=(3), W=1, tau=1 gives LP=3/2 and integer optimum 0. Corrected without changing the predicate.
2. Defined the item count and bitlength convention explicitly, including bitlength(0)=0. Checked displayed widths against `qft_bank.bank_geometry`, and the loss accumulator against `build_qft_bank`.
3. Core preprocessing now explicitly includes infeasible opposite assignments, matching the direct overweight rejection in `exact_knapsack.reduced_cost_fixing`.
4. Made the unbounded endpoint cell explicit in the rational-bank proof. It was already used later in the proof and by `continuous_bank.build_continuous_bank`; no algorithm or theorem is changed.
5. Resource accounting now states that the profiler applies transpiled primitive decomposition templates. It does not suggest that each full large circuit was independently transpiled. The small-control transpilation cross-check remains stated.
6. Removed draft-status language, historical editing language, unused scheduled-work classification, and lists of unimplemented comparison variants from the reviewed sections. Preserved substantive assumptions, preprocessing costs, finite circuit-test scope, and the reconstruction distinction.
7. Moved the factual AI-use disclosure from evaluation methods into declarations, without inventing completed author approval. Detailed editorial notes remain in audit documents rather than these sections.
8. Improved Figure 1 legend contrast so the LP reference line no longer crosses the label text.

## Paragraph-level evidence coverage

| Section | Review scope and evidence |
|---|---|
| Introduction | Every paragraph checked against the explicit contract, existing primary-reference ledger, saved coverage derivations and 105-row resource comparison. Replaced “large-instance” with separate arithmetic/circuit/resource evaluation and qualified the depth increase as median. No claim of first implementation, hardware advantage or optimal circuit cost added. |
| 3, definitions and predicate | Checked integrality/sign assumptions, stable efficiency ties, empty case, R<0 rejection, integer tau vs unsigned encoding, and incumbent tau=L+1. Floor inequality and strict comparison checked algebraically. |
| 3, dual equality | Checked weak-duality inequality termwise and greedy equality for ties, exact-fill boundary, zero capacity, all-fit, empty and zero-profit cases. No new external theorem attribution. |
| 3.1, core | Traced `make_core_inputs.py` to `reduced_cost_fixing` and regenerated the saved fixings. Joint fixing preserves every solution of value at least the greedy lower bound; arbitrary lower thresholds are not asserted. |
| 4, bank/root tail | Read lemma and proof against cumulative-weight argument and `compressed_bank` construction. Feasible prefixes cannot create an earlier first nonfitting item. Zero covers all-fit cases. |
| 4.1 | Checked reachable-state recurrence, integer-profit cancellation, both directions of floor-equivalence proof, finite threshold distinction, and disjoint-interval lower bound. |
| 4.2 | Checked max-prefix affine representation, sign of interval inequalities, open positive boundaries, possible closed zero, and unbounded cell. Greedy exchange and critical disjoint intervals agree with the implementation. Minimum cardinality is not minimum arithmetic cost. |
| 4.3 | Rechecked denominator and slope reasoning against the prior independent theory audit and `build_dp_free_bank`: reduced rho=a/b, whole tied-group weight, strict radius, adjacent grid candidates, mandatory zero. Prior counterexamples to relaxed conditions retained in Appendix A. |
| 4.4 | Checked pseudopolynomial state count, affine constraints per state, capped-constructor fallback, and the one-based linear-cardinality family. Fresh 14 endpoint comparisons against independent primal/all-subset reference: zero mismatches. |
| 5.1 | Traced normalization, sorted prefix mapping, coefficient/loss identity, unsigned widths, controlled addition/subtraction, comparison, full QFT rotations, and separate Boolean profit domain. No fixed-point divider or rotation-synthesis implementation is claimed. |
| 5.2 | Traced capacity flag, per-bank comparison flags, accumulator uncomputation, OR aggregation, target XOR and final inversion through `QFTNetwork.finish`. Initial workspace and fixed-depth assumptions retained. This pass adds no new gate-simulation result. |
| 5.3 | Traced root split and eligible suffix positions through `root_aware_control.py`, including all-fit cases, widths, masking, serial workspace, and common inverse cancellation. Comparison remains a reconstruction, not a released competitor circuit. |
| 6.1 | Regenerated all 700 arrays from the written generator specification and seeds; regenerated all 700 core transformations; matched all 105 selected IDs to trials 0–2. Zero mismatches in each check. Metric classifications retained for actual reported quantities. |
| 6.2 | Read independent reachability and primal-vertex methodology against saved source; verified systematic-domain counts and random-seed specification. Distinguishes arithmetic coverage from gate simulation. |
| 6.3 | Checked original/resumed circuit-test records and gate-list interpretation, tolerance and domain scopes, profiler templates/dependency scheduling, interface-plus-touched active wires, and computational budgets. Failed runs remain in results and research records. |

## Verification and limits

`SECTIONS_1_3_6_CHECKS.json`: 700 generator records, 700 cores, 105 selection records, and 1,224 encoded-arithmetic checks, with zero mismatches. These are DERIVED checks; they do not enlarge the paper's SIMULATED gate-test counts. `REVISION_VERIFICATION.json`: 14 barrier endpoints and 1,376 arithmetic identity/width checks, zero mismatches; all 467 original-paper files unchanged; 40 cited references; 199-word abstract; no unresolved cross-references.

Compiled PDF: 32 pages. Figures 1–3 and Tables 1–4 have unique sequential numbers and resolved references. Inspected all rendered page contact sheets and Figure 1 at full page size. No overfull boxes or off-page text detected. Float placement follows the Springer class; a top-of-page figure/table may precede its nearby prose reference.

Prior unresolved simulator-initialization details and source-access limits are not reclassified as resolved. No new theorem was derived and approved in this pass. Numerical ledgers and production research code were not edited. The code/header's historical claims of benchmark hardness or quantum advantage were not imported into the manuscript.

Backup: `../backups/before_sections_1_3_6_20261027/`. Exact prose changes: `sections_1_3_6.diff`. Remaining author decisions and later-section editorial cleanup are outside this pass.
