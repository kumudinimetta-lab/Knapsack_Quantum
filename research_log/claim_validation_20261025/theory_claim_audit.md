# Fresh adversarial theory audit

25 October 2026. No old implementation, raw result or manuscript was changed.
This is an adversarial reconstruction, not a confirmation of a desired claim.
Graph tools were discovered first and were unavailable; targeted source reads
followed. The tested source hashes are retained in the audit JSON.

## Verdict and exact contract

The reconstructed mathematics supports the following conditional contract:

> For the provided positive-integer-weight, nonnegative-integer-profit instance
> and a fixed nonincreasing-exact-efficiency prefix order, the constructed bank
> preserves the Boolean decision `fractional LP upper bound < integer tau`
> at every capacity-feasible prefix. Overweight prefixes require a separate
> capacity-rejection rule. A reversible implementation must separately establish
> its exact encoding, register widths, strict comparisons and clean workspace.

This audit found no mathematical counterexample WITHIN those assumptions and
no mismatch in the tested constructor outputs. It does not alone verify any
quantum gate list or physical implementation. “A reversible oracle preserving
exact integer LP-pruning decisions” is defensible only with those assumptions
and the separate circuit-verification scope attached. It must not be shortened
to “implements the exact LP solver” or a general branch-and-bound oracle.

## Reconstructed proof, independent of the earlier narrative

1. **Root tail.** Let s be the root greedy split. For a prefix ending before s,
   selected prefix weight plus suffix weight through any earlier index is at
   most the original cumulative weight through that index, which is <=W.
   Such an earlier split is impossible. Prefixes ending after s have only later
   suffix items. Thus an optimal suffix dual multiplier is <=root split ratio.
   Convex dual objectives are nondecreasing above that ratio; discarded larger
   multipliers are globally dominated. All-fit roots use0. Ties are deduplicated.
2. **Integer thresholds.** Accrued prefix profit P is integer, so all integer
   threshold decisions agree exactly iff the residual upper-bound floors agree.
   For U equal to the true residual LP, a dual multiplier covers the state iff
   F(lambda)<floor(U)+1, STRICTLY. Reachability is indexed by depth and residual
   capacity; different integer P values at the same state do not change coverage.
3. **Finite-grid minimum.** Convexity gives contiguous density-index coverage.
   Earliest-right-endpoint stabbing produces a feasible bank and pairwise
   disjoint critical index intervals of the same cardinality, proving minimum
   ON the density grid. Root-tail dominance means omitting higher input ratios
   does not increase that finite-grid minimum.
4. **Arbitrary-rational minimum.** F is the maximum of all suffix-prefix affine
   functions, because positive reduced costs form a density prefix. Intersecting
   strict affine inequalities gives nonempty rational intervals. Finite upper
   endpoints are open;0 may be closed; R=0 can give infinity. Global endpoint
   cells preserve membership. Replace point0 by a sufficiently small positive
   point when needed, then exchange any point in the earliest-ending interval
   for a point just left of its upper limit. All intervals it hit remain hit.
   Disjoint critical intervals supply the matching lower bound. This proves
   minimum CARDINALITY among nonnegative rational multiplier banks, not gates.
5. **DP-free sufficient coverage.** Between adjacent distinct density breakpoints,
   the dual slope around a split-density group is r or r-L_suffix. Its absolute
   value is <=the full tied-group weight L. The residual LP denominator divides
   b when rho=a/b; its distance to the next integer is >=1/b. Therefore the
   STRICT radius |lambda-rho|<1/(bL) suffices. Using a single item's weight for
   a tied group is invalid. Crossing another breakpoint invalidates this simple
   slope bound. Keeping0 covers all-fit/empty suffixes.
6. **Linear barrier.** For n main items w=2, v_i=4(n-i)+1, W=2*floor(n/2)+1,
   plus the unit dummy w=v=1, selected all-zero prefix states have disjoint
   continuous coverage intervals (rho_i-1/2,rho_i+1/2). An all-zero full leaf
   adds [0,1/W), disjoint from them. The n-floor(n/2)+1 lower bound is attained
   by0 and the main root-tail densities. The dummy removes a common-weight gcd
   artifact. This is a bank-cardinality barrier on an EASY optimization family,
   not a quantum-query/gate lower bound or knapsack hardness statement.

## Fresh independent code/reference checks

`theory_adversarial_audit_v2.json`: 1,888 instances = 1,792 exhaustive two-item
inputs (weights1..4, profits0..3, all zero/all-fit transition capacities) plus
96 new-seed random n=3..7 instances emphasizing ties and zero profits.

- 15,999 feasible prefixes: **0** root-tail rational-value errors and **0**
  floor-preservation errors for grid, DP-free or continuous banks.
- 1,369 independent continuous minimum-cardinality certificates: **0** failures;
  1,637 critical intervals re-derived using ALL subset affine functions:
  **0** endpoint/open-boundary mismatches.
- 1,369 independent density-grid minimum certificates: **0** failures; critical
  coverage sets were computed directly, not copied from stored interval bounds.
- Four small repaired-barrier sizes:14 exact endpoint checks, **0** mismatches.

The LP reference enumerates primal box vertices and vertices with one fractional
coordinate, rather than using the production greedy bound or dual-breakpoint
helper. Sorting independently compares cross products. Minimum lower-bound
certificates use all-subset dual functions, not the production prefix-affine
interval routine. Counts are DERIVED exact arithmetic; executed loop/time
observations are classical, not quantum simulation or a statistical success rate.
The initial audit JSON and source remain preserved beside this expanded version.

## Deliberately falsified stronger interpretations

| Invalid extension | Exact witness |
|---|---|
| Noninteger tau | w=[1,1],v=[1,1],W=1: LP=1, continuous-bank bound=3/2. At tau=5/4, pruning decisions differ. |
| Arbitrary/nonprefix branching | w=[10,9],v=[100,1],W=15, fix low-density item IN first: LP=61; original root-tail bank gives905/9. At tau=62 they differ. |
| Replace tie-group L by one item's weight | w=[2,2,3],v=[1,1,1],W=1: LP=1/2, multiplier1/3 gives1. Its distance passes the weaker single-item radius but misses tau=1 pruning. |
| Change strict radius to nonstrict | w=[1],v=[1],W=0: lambda0 is exactly at that boundary and gives1 instead of LP0; tau=1 fails. |
| Allow negative multipliers | w=[1],v=[1],W=2, lambda=-1 gives0 below LP1, creating UNSAFE pruning at tau=1. |
| Reuse original LP semantics after integer gcd normalization | w=[2],v=[3],W=1 has LP3/2; normalized w=1,W=0 has LP0. Integer feasible sets agree, but pruning at tau=1 differs. |

These are actual exact boundary calculations, not defects in the scoped code.
They show why the assumptions must accompany the claim. Equal floors also do
not preserve LP rational values, integrality flags, LP-completion witnesses or
LP-selected branching variables. A minimum bank need not minimize arithmetic
width, gate count, workspace, total walk cost or runtime. Capped construction
fallbacks preserve pruning but must not carry a minimum-cardinality claim.

## Primary-source and contribution assessment

Directly re-read primary cached text: Dey--Dubey--Molinaro,
https://arxiv.org/html/2007.15192v4 , Section3 equations(2)--(3), already provides
the LP Lagrangian/reduced-cost framework. Wilkening et al.,
https://doi.org/10.1038/s41534-025-01097-8 , Supplement F.2 / preprint Appendix
A.6.2, already uses fractional greedy bounds in quantum knapsack B&B. Neither
generic LP duality nor using fractional LP inside quantum knapsack is new.
Erickson's author-hosted *Algorithms* Chapter4 interval-stabbing exercise and
McCauley's author-written Problem1 explicitly establish the standard greedy
subproblem. No invented theorem/exercise number or unverified citation is used.

The possible distinct contribution is a precisely scoped, pruning-preserving
reversible construction/compiler plus a meaningful resource result against
strong optimized baselines. This pass does NOT establish historical priority
for that application. Exact reachability compilation is pseudopolynomial and
can cost more than solving the instance classically; it cannot be free
end-to-end quantum-advantage evidence. The DP-free sufficient variant avoids
that particular compiler cost, but may do no useful compression. A true and
carefully bounded construction is stronger than an unsupported claim; journal
significance/novelty and acceptance still require separate editorial judgment.

## Independent check of the root's all-state audit

`ROOT_AUDIT_PLAN.md` and `root_all_reachable_coverage.py` correctly use a
separately assembled full SUFFIX density+0 dual reference, stable cross-product
sorting and SET reachability. They call no bank-construction/greedy-LP helpers.
The set update uses the prior prefix set (0/1 reachability), and floor(min F)
equals min floor(F). This is not circular validation; expected values are not
computed from selected-bank outputs. It still uses LP duality, so the distinct
primal-vertex reference above is a useful adversarial cross-check. Its broad
claim is exhaustive ARITHMETIC quotient-state coverage, extended to all integer
thresholds by integer P; it is not exhaustive gate propagation. A minor source
provenance suggestion, not a semantic failure, is explicitly checking the
DP-free row's recorded source-bank hash against its actual registry source.
