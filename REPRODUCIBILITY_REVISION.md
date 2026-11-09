# Revised manuscript reproduction

Revision started 22 October 2026; manuscript audit continued 23 October 2026
(Asia/Calcutta). The `20261022` filename tag identifies this revision.

## Build the paper

From `paper/`, run `pdflatex -interaction=nonstopmode -halt-on-error main.tex`,
then `bibtex main`, then run the same `pdflatex` command twice. The official
Springer Nature class and numeric bibliography style are included locally.
The editable source is `paper/main.tex`; the compiled artifact is `paper/main.pdf`.
There are no external figure dependencies in this revision.

The journal-specific instructions specify an 80–100 word abstract and 4–6
keywords. This manuscript has 89 words and six keywords. The official page also
contains generic 150–250-word boilerplate; the journal-specific requirement was
used. Source: https://link.springer.com/journal/11128/submission-guidelines.

## Run the research checks

Use Python 3.13 with `simulation/requirements-revision.txt`. From the repository
root, run:

```powershell
python simulation/run_repro.py
```

For the faster exact-reference, adversarial-mathematics and small witness checks:

```powershell
python simulation/run_repro.py --quick
```

All new results are written under `research_log/revision_20261022_*_results.json`.
These commands regenerate those revision artifacts, not historical experimental
files in `simulation/`. Preserve any previous revision run if comparing timing
changes. Timings vary by host and are not a quantum execution estimate.

## Evidence and scope

| Evidence | Classification | Scope and result |
|---|---|---|
| Exact classical audit | MEASURED outcomes, DERIVED rational bounds | 700 instances; 0 fixing/optimum mismatches; 0 B&B mismatches; 0 caps |
| New reversible node predicate | SIMULATED exact sparse statevectors | All prefix, threshold and target inputs at depth 3 on all 700 instances; 15,859,712 columns; 0 predicate mismatches; 0 dirty-workspace columns |
| Small node circuits | SIMULATED | All depths for three explicitly stored instances: 1984, 1984 and 480 columns; 0 mismatches and 0 dirty columns |
| Coherent depth wrappers | SIMULATED | All prefix/depth/threshold/target encodings for the same three small instances at k=5,7,6: 8192, 8192 and 1024 columns; 0 mismatches and 0 dirty columns |
| Independent Qiskit node check | SIMULATED dense statevector | One-item, 25-qubit circuit; maximum amplitude error about 5.55e-17 |
| Value and witness recovery | SIMULATED analytical-majority decisions | 135 configurations at n=0..8; 0 value/witness mismatches; 0 caps |
| Phase predicate V | SIMULATED dense statevector | Four items, 16 selection states, each threshold 0..21; 0 mismatches |
| Fresh spectral audit | SIMULATED | 1200 conditions: 889 completed; 0 endpoint violations and 0 analytical-majority disagreements on completed trees |
| Large coefficients | MEASURED classical | 45 cases, R=1,000,000; all exact MitM references available; OR-Tools: 45 solved, 0 mismatches; B&B: 36 complete, 0 mismatches, 9 capped |
| Regression | DERIVED exploratory statistics | Actual core-tree nodes, 559 positive-gap cases; 141 zero-gap cases explicitly excluded; grouped cross-validation |
| Circuit qubits, gates, depth | DERIVED from synthesized gate lists | Not hardware measurements or full-algorithm fault-tolerant estimates |
| Quantum query counts | SCHEDULED | Selected by PE precision/repetition policy; not independent experimental scaling evidence |

The 700 cases use the five generators in `benchmark_v5.py`, but their old
floating-point solvers and old correctness flags are not the new reference.
The revision uses `exact_knapsack.py`. Item counts are 12,14,16,18,20,22,24;
trial indices 0..19; seed=1000*n+trial; R=100; capacity=floor(sum(weights)/2).
The gate builder is `oracle_h/node_bound_reversible.py`. It implements fixed
depth predicates and a clean coherent-depth wrapper, and compiles exact fixed-point efficiency constants, avoiding
variable quantum division. It uses explicit X/CX/CCX gates and uncomputes all
working wires. Sparse simulation tracks every gate's exact permutation action
on every tested basis column; it does not use the legacy Fourier-flag simulator.

The spectral benchmark has a DIFFERENT generator parameter R=50 and sizes
8,10,12,14,16,18. Each of 600 seed configurations has a marked and unmarked
condition, with a 2000-node cap. The 311 noncompleted conditions comprise 74
marked caps, 74 bypassed empty-core conditions, and 163 pruned unmarked roots.
Known optima choose the diagnostic thresholds only in this audit. They are not
inputs to the optimization simulator's threshold or witness decisions.

`quantum_bb_optimize` returns an assignment and value; its `correct` field uses
DP only for independent checking. It computes analytical majority probabilities
rather than sampling a physical quantum measurement. The calibrated precision
constant is not a universal finite-error certificate. The theoretical error
allocation assumes the cited detection theorem's conditions and a supplied
certified bound covering every value and recovery tree. Enumerating those trees
to obtain their sizes incurs classical cost, excluded from the conditional
query theorem. Neither a full walk circuit nor a wall-clock quantum advantage
is demonstrated.

Historical OR-Tools and runtime tables are explicitly labeled archived. The
new tests do not claim to recreate those historical timing measurements.
Historical IBM summaries lack job/circuit provenance required to connect them
to the current circuit and are excluded from the revised algorithm evidence.
Legacy files, including explicitly contaminated historical quantum-scaling
data, are not inputs to the revision's claimed validation results. The new
reproduction entry point does not run legacy query-scaling regression scripts.

## Author-supplied facts still needed

Madhavi A. is the proposed corresponding author, following the user's reply;
confirm this designation before submission. Funding, competing interests and
individual contributions remain unconfirmed. The manuscript says so rather
than fabricating them. QIP requests contribution and competing-interest
information through its submission interface. All authors must review the
analysis, code, AI-use disclosure, authorship and final text before submission.
The revision has not been submitted, pushed, or published by this task.

## Source preservation

`paper/backups/2026-10-22_before_revision/` preserves the user's starting LaTeX,
bibliography and PDF, including preexisting uncommitted edits. The decision
history and failed attempts are in `research_log/2026-10-22_revision_derivations.md`
and `research_log/2026-10-23_revision_audit.md`. Raw experiments were not edited
by hand. New outputs are reproducible from the revision scripts and carry
explicit parameter/seed scopes. The local corrected source and results must
be deposited with the eventual public revision; a public URL does not imply
these unpushed changes are already available there.
