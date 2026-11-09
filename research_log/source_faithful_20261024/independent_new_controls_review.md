# Independent review of the new controls (2026-10-24)

The directed-up precision construction and finite-grid compressed bank survived
the independent checks below. The QFT reconstruction also survived independent
phase-sensitive controls after an Aer saved-amplitude readout disagreement was
isolated. These findings concern specified predicates and finite tests. They
do not demonstrate an improvement over the released Wilkening implementation,
an end-to-end quantum speedup, or a journal acceptance probability.

## Directed-up, item-specific fixed-point precision

The algebra was reviewed before implementation in
`independent_precision_review.md`. For reduced density `a/b`, let
`q=ceil(2^k a/b)` and `e=bq−2^k a`. Then `0<=e<=b−1` and the bound error at
an actual split is `r e/(b 2^k)`. For `r=0` the error is zero. Otherwise,
`2^k>(w−1)b` makes the error strictly less than `1/b`; dyadic densities can
instead be represented exactly. Since a strict gap from a rational of
denominator dividing `b` to an integer threshold is at least `1/b`, the
integer-threshold rejection predicates agree. The sufficient precision rule
is not claimed necessary. Upward rounding at insufficient precision can miss
pruning; it cannot create an unsafe rejection while the exact ordering and
other assumptions hold. Noninteger thresholds and approximate density sorting
are outside this argument; counterexamples are retained in the earlier note.

Code audit of `simulation/source_faithful_20261024/rounding.py` found:

- Exact reduced fractions and exact ordering precede the precision choice.
- Non-dyadic `((w−1)b).bit_length()` gives the required strict power-of-two
  inequality, including when `(w−1)b` is a power of two. The dyadic branch is
  exact and may use zero fractional bits.
- `P<<k + r*q` and `tau<<k` are compared directly. The declared common word
  width covers both valid expressions. Inactive modular garbage is masked and
  subsequently uncomputed.
- Fixed-depth and coherent-depth interfaces both retain the original strict
  rejection semantics, and prefix bits beyond the chosen depth are ignored.

Independent script `reviewer_new_controls.py`, seed **2026102411**
(`HARDCODED`), used exact LP vertex enumeration rather than the production
greedy scan. On **47** declared edge/random instances, dynamic depths including
invalid encodings, nonzero ignored suffix bits, selected integer thresholds,
and fixed-depth edge controls, **46,700 SIMULATED gate columns had 0 predicate
mismatches and 0 dirty-workspace columns**. The declared sample is not the full
700-instance assignment/threshold domain.

I also read the author raw ledgers rather than rely on reported totals:
`rounding_main700.jsonl` contains **700 unique complete** cases and
**1,220,488 SIMULATED scoped columns, 0 predicate mismatches, 0 dirty columns**;
`rounding_tiny.jsonl` contains **10** instances and **11,144 SIMULATED exhaustive
clean-input columns, 0 mismatches, 0 dirty columns**. The scalar ledger contains
**192,962 DERIVED exact rational/integer comparisons, 0 mismatches**. These
totals are separately sourced tests, not additional independent replication.
The recorded rounding module hash is
`1d17562bbeda759a4ed26fb9684bca298cd62d7b0d4d34429da3242d29d028ab`.

The original rounding bytes are preserved as `rounding_before_tight_exact.py`.
The later module adds `build_tight_exact` without changing the rounding path's
semantics; its source hash is separately recorded by the tight-control ledgers.

This is an important stronger same-function control. It reduces the persuasive
value of comparisons against the previous uniform fixed-point implementation.
It is a specialization of directed rounding and integer-threshold separation,
not evidence by itself of a new general arithmetic principle.

## Minimum finite-density-grid bank

The pre-code proof review found the root-tail dominance, integer-floor
criterion, residual reachability quotient, strict convex sublevel intervals,
and right-endpoint interval stabbing sound under the stated exact static
density order. Integer prefix profit cancels from the floor test; positivity
of profits is not the reason for that cancellation. The implementation permits
zero profits and correctly retains zero as a density-grid candidate.

`compressed_bank.py` correctly computes reachable prefix weights, uses the
strict test `a*R + suffix_numerator < b*(floor_LP+1)`, and obtains interval
endpoints around a genuinely LP-optimal grid candidate. The minimum-cardinality
witness intervals are pairwise disjoint. The claim is minimum **cardinality on
the fixed density grid**, not minimum over arbitrary rational multipliers or
minimum gate cost. Dominance of points above the root split justifies reducing
the full density grid to the root tail without losing that cardinality optimum.

The independent vertex-reference probe checked **779 feasible prefixes** on
the same **47** instances: **0 bank-floor mismatches, 0 root-tail exact-value
mismatches, and 0 noncontiguous coverage sets** (`DERIVED` exact comparisons).
Brute-force enumeration of all grid subsets found **0 minimum-cardinality
mismatches in 47 cases**. Separate capacity, state, and time cap controls all
returned the safe root-tail fallback and withheld the minimum claim.

The original equal-weight barrier is normalization fragile and remains a
rejected robustness attempt. The repaired family appends one `(w,v)=(1,1)`
dummy after `n` main items `w_i=2`, `v_i=4(n−i)+1`, with
`W=2 floor(n/2)+1`. Both global gcds are one. At depth `d=s−floor(n/2)` with
the earlier prefix all zero, the split main density has neighboring slopes
−1 and +1; other main grid densities are at least two away, and the dummy
density one is at least 1.5 away. All fail the half-unit floor slack. Each of
the `n−floor(n/2)` tail main densities is therefore forced. The all-zero full
leaf forces zero. The dummy density is redundant. Independent cases
**n=2,...,17** had the predicted bank size **n−floor(n/2)+1** and both gcds one.
This is a finite-grid cardinality barrier for an easy family, not a knapsack
hardness or quantum lower bound. A walk that bypasses complete leaves needs the
corresponding leaf convention stated separately.

The preprocessing is pseudopolynomial in capacity, and records reachable
states rather than an optimum. Its cost cannot be treated as free: weight DP
can already solve related reachability tasks and standard profit DP can solve
the classical knapsack instance in the same pseudopolynomial regime. Circuit
cost and host preprocessing need separate ledgers and a break-even question.
Caps do not establish bit-polynomial complexity.

The restriction to the density grid is substantive. A bounded independent
midpoint search found `w=[27,28,12], v=[1,9,5], W=34`: the density-grid minimum
is three, whereas `{1/54,271/1512}` preserves all prefix floors with two
multipliers. All **10** feasible prefixes were independently checked with LP
vertex enumeration, **0 floor mismatches**. The separate theory-agent example
`w=[9,9], v=[1,1], W=10` was independently vertex-checked on all **6** feasible
prefixes, **0 floor mismatches**: grid `{0,1/9}` needs two points, while the
rational singleton `{1/11}` suffices. Raw scripts/results are
`reviewer_offgrid_probe.*` and `reviewer_offgrid_analytic.*`. These examples
include complete leaves; their bypass convention changes the constraints.

There is also a simple normalized algebraic witness:
`w=v=[1,1], W=1`. The density grid `{0,1}` needs both points, since zero fails
at the root and one fails at the all-zero complete leaf. The singleton
`lambda=1/2` yields bounds `3/2` at the root, `1` or `3/2` at depth one, and
`1/2` or `1` at feasible leaves, preserving floors `1,1,0/1`. Both gcds are one.
Thus neither a global minimum rational-bank claim nor a normalization-based
explanation of this limitation would be justified.

The optional DP-free sufficient rule was independently reviewed before code:
if a split density group has global total weight `L`, the slope magnitude of
the dual function on either immediately adjacent density interval is at most
the available group weight, hence at most `L`. Therefore
`|lambda−rho| L < 1/b` is sufficient for floor preservation. Neighbor endpoints
are covered by continuity. This bound cannot be extended across another
density breakpoint using the same `L`; it is sufficient coverage, not the
minimum actual bank. Zero still covers all-fit suffixes.

The subsequent `build_dp_free_bank` implementation uses the equivalent exact
integer radius test `abs(a*d−b*c)*L<d`, which is the correct cross product for
`|a/b−c/d| L<1/b`. It includes an explicit zero constraint and performs interval
stabbing only for this conservative sufficient family. Its minimum flag is
correctly scoped to those sufficient constraints, not actual reachable-state
coverage. This construction avoids the capacity DP; its finite preprocessing
still needs a separate time/work ledger.

## Source-primitive QFT reconstruction and readout triage

The module explicitly reconstructs a fixed-depth LP predicate using Draper
addition and Wilkening supplementary comparison primitives. Its quantum
threshold comparison and cross-product assembly are declared completions.
It is **not** the authors' released R1 oracle, full schedule, or copied-control
parallel implementation. The available source assumptions and symbol mapping
are recorded in `derivation_before_code.md`.

Independent inspection found the no-swap QFT phase convention internally
consistent; the extra comparison bit safely represents the difference of two
unsigned words; valid-branch widths cover the numerator and threshold; and
inverse arithmetic restores reusable words. Infeasible residual wraparound is
masked. The direct small-control policy repairs an avoidable weak-control
baseline while the generic serial policy remains an explicitly labeled
sensitivity control.

The first full-gate pilot reported 15/16 failed expected amplitudes. That raw
attempt is retained. I independently reproduced a readout contradiction on the
same **23-qubit, 330-native-gate** fixture: Aer MPS `save_amplitudes([1,9])`
returned `[0,0]`, whereas the same result's logical probability at 9 was
**1.0000000000000369**. Direct contraction of saved Gamma/lambda tensors gave
amplitude **1.0000000000000184 + 1.80e−15 i**. This evidence isolates the
saved-amplitude result as unsuitable for this test; it does not justify
discarding the raw failure or assuming all other predicates correct.

`reviewer_mps_triage.py`, seed **2026102412** (`HARDCODED`), compares an
independent tensor expansion and the shared contraction helper with dense
Statevector simulation. Four arithmetic networks cover **2,176 amplitudes**;
the largest amplitude discrepancy was **5.70e−11**. A separate entangled
complex input on all **16 logical amplitudes** of the original full fixture
agreed with the exact predicate permutation within **1.18e−10**, with
workspace probability leak **3.33e−16**. All are `SIMULATED` and below the
declared **1e−8 HARDCODED** tolerance. These phase-sensitive checks are stronger
than probability-only checks, but are finite numerical evidence.

The agent's replacement pilot ledger reports **28 method cases, 608 full-gate
MPS columns, 0 predicate/cleanup failures**, plus **1,848 dense kernel columns,
0 failures**. That is a tiny finite source-comparison pilot, not whole-700 QFT
verification. The failed and replacement ledgers are separate.

## Claim and comparison gates

1. Use the upper-ceiling control when comparing the same LP function. Preserve
   fixed versus coherent depth, threshold domain, ordering, and cleanup.
2. Report common `{u,cx}` basis costs as `DERIVED`, including arbitrary ideal
   rotation assumptions. These are not Clifford+T synthesis costs, physical
   noisy runtimes, or IBM executions.
3. Keep qubits, gates, depth, preprocessing, and capped conditions visible.
   A workspace reduction can increase gate count/depth; the source QFT
   reconstruction can beat a dual candidate on some cases.
4. Claims of improvement over a published implementation require matching the
   actual source artifact and its problem/interface assumptions. A declared
   primitive reconstruction cannot satisfy that obligation by its name alone.
5. The defensible current contribution is a studied construction and tradeoff,
   including a finite-grid exact-pruning compression and its limitations.
   A substantial cross-source performance advance remains unestablished.

## Final coherent-bank and stronger-scan compilation audit

`reviewer_compilation_audit.py`, seed **2026102414** (`HARDCODED`), tested
**35** independent tiny/adversarial/random instances against the LP-vertex
reference. It includes empty, zero capacity, all-fit, equal densities, both
off-grid boundary cases, a large encoded capacity, invalid encoded depths,
all prefix encodings including ignored suffix bits, selected thresholds, and
both target bits. Results (`SIMULATED`):

| Construction | Columns | Predicate mismatches | Dirty columns |
| --- | ---: | ---: | ---: |
| Tight normalized-width exact scan | 24,714 | 0 | 0 |
| Reachable-state compressed-grid bank | 24,726 | 0 | 0 |
| DP-free sufficient bank | 24,728 | 0 | 0 |

The tiny sample counts differ because each method receives an independent
deterministic random threshold draw. Exact/near-floor, extreme thresholds,
depths, prefix coverage, and both target bits are shared by design. No inference
depends on comparing these tiny sample denominators.

I independently recomputed **84,000 resource pair rows**, **720 summary groups**,
**14 recorded file hashes**, and all **9** raw ledger counts, unique IDs, statuses,
column totals, mismatch totals, and cleanup totals in `compilation_summary.json`:
**0 aggregation discrepancies and 0 undefined ratios**. The ledger contains
all 700 original and all 700 core conditions for each main construction, plus
the separately reported 45 independent large-coefficient bank conditions.
No capped rows were hidden in these particular ledgers; all are complete.

`best_scan` is the minimum of the old exact, directed-up, and tight exact scan
costs **separately for each instance and each metric**. It is a conservative
lower resource envelope for comparisons, not a single circuit simultaneously
attaining all displayed qubit, gate, and depth minima. No tree size or optimum
is used to choose it. The numerical summary is reproducible; source-level
priority and cross-artifact superiority remain separate questions.

No manuscript, bibliography, previous raw ledger, or production module was
edited by this review. Independent scripts and raw results are new files.
