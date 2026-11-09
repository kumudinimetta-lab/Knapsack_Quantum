# Minimal manuscript revision: integrity stop

Date: 2026-10-22 (Asia/Calcutta).

Status: RESEARCH_INTEGRITY_STOP. The audit stopped before manuscript edits,
new theorem derivations, circuit changes, experiments, or novelty claims.

## Request and constraints

Revise `paper/main.tex` against the user's pasted QIP assessment, keeping
changes to words and sentences minimal; assess novelty opportunities afterward.
The assessment was read from the supplied attachment, without modification.
Existing uncommitted LaTeX, bibliography, and compiled outputs were detected
and preserved. No experimental data was edited.

The required code-review-graph tools were searched for in the available tool
catalog. None of `semantic_search_nodes`, `query_graph`, `detect_changes`, or
`get_architecture_overview` was available. Targeted filesystem reads were used
as the documented fallback. No subagents were used.

## Stop-triggering evidence

### Assignment recovery differs between manuscript and implementation

`paper/main.tex`, Algorithm 2 (`alg:qbb`), promises an optimal core assignment
and returns that assignment after recovering the optimum threshold/value.
Theorem 1 and the reconstruction phase depend on that assignment.

`simulation/quantum_backtracking.py`, `quantum_bb_optimize`, instead returns
`QBBResult(optimal_value=found, ...)`. `QBBResult` has no assignment field and
the inspected function contains no witness-extraction phase. Its classical
dynamic-programming optimum is used for the `correct` comparison; it does not
provide a returned witness. Establishing a value is insufficient to supply the
assignment required by the manuscript's reconstruction algorithm.

This is a direct code–paper mismatch, triggering the repository's explicit
instruction to stop. No new witness procedure or complexity bound was silently
substituted.

### LP-oracle benchmark verification has narrower semantics than requested

The inspected `simulation/oracle_h/verify_circuit_m4.py`:

- Generates benchmark instances, then caps `v_s`, `w_s`, `W_res`, and `V_int`
  independently to fit the chosen registers. These are modified arithmetic
  inputs, not executions of the original benchmark LP subproblems.
- Computes its comparison target with `exact_e = v_s_scaled // w_s` and
  `exact_frac = W_res * exact_e`. This target is the same truncated arithmetic,
  not the exact non-truncated rational LP bound.
- Uses `GateLevelSimulator` from `simulate_circuit.py`, which tracks Boolean
  bits, per-qubit phases, and Fourier flags under restricted gate assumptions.
  It does not maintain a general quantum statevector. No general coherent
  correctness conclusion follows from this representation alone.
- Checks the final comparator flag in `verify_instance`; that check alone does
  not establish restoration of all workspace registers.

Existing records in `research_log/simulator_m4_results.md` and Table
`tab:h_resources` describe a reported zero-mismatch result on twenty-five
sampled cases. That is a historical SIMULATED report, not a new result from
this audit, and it must not be relabeled as exhaustive statevector verification
against exact LP bounds on the existing seven-hundred-instance benchmark.
The audit did not rerun it or independently verify its mismatch count.

The seven-hundred-instance exhaustive statevector/exact-LP requirement remains
unfulfilled by the inspected circuit verification path. This observation does
not claim that all other verification scripts were exhaustively audited.

## Other observations captured before stopping

These are unresolved revision items, not approved replacement claims:

- The manuscript alternately says the LP heuristic is synthesized at a small
  illustrative size and says it is not synthesized. Scope must be stated
  consistently after the implementation is reconciled.
- Binary-search detection, global error amplification, witness recovery, and
  their costs need a primary-source audit before updating the total query bound.
- The necessity construction uses noninteger values and capacity despite the
  stated positive-integer problem class. Scaling is not assumed to preserve
  its bounded-gap claim.
- A complete binary decision tree of depth m has at most 2^(m+1)-1 nodes
  (DERIVED counting identity); the manuscript uses 2^m as a node bound.
- The containment-to-query exponent needs a separate derivation and adversarial
  check; no corrected central claim was derived and approved in this pass.
- The claim that efficiencies are distinct without loss of generality needs
  reconciliation with the subset-sum benchmarks and spacing assumptions.
- Current novelty language and the prior-work capability table require checking
  the actual primary sources identified by the assessment.
- Journal abstract length, keyword count, article format, author information,
  and declarations need verification against current publisher instructions.

No citations were added, rejected as false, or declared verified. No web search
was performed before the stop. Firecrawl skill guidance was inspected in
preparation, but no Firecrawl operation or document parsing service was used.
No new precision lemma, precision tradeoff, experiment, or regression was run.

## Required next resolution

Reconcile the returned value/assignment contract and the oracle-validation
scope under the user's direction before resuming substantive revision. Preserve
all original data and historical results. Any changed experimental procedure
must write new, separately identified results. Remaining assessment items have
not been marked complete, and no submission-ready PDF is claimed.
