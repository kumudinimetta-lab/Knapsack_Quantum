# Theory/generalization track: ranked feasible directions

23 October 2026. No manuscript edit, hardware execution, acceptance probability
or priority guarantee. This report separates standard facts from candidate
research deltas. Full derivations are in `theory_derivation_candidates.md`;
production proof/metric mapping is in
`research_log/pruning_study_20261023/TREE_PROOF_AUDIT.md`.

## Ranked recommendation

### 1. A clean exact pruning portfolio, selected by resource and tree tradeoffs

This is the best low-risk continuation because concrete offline constructions
and matched inputs now exist. It asks whether rebuilding the fractional LP at
every quantum tree node is worth its reversible arithmetic cost. Compare a
simple remaining-profit certificate, one root-dual certificate, small fixed
banks of dual certificates and exact fractional LP, with identical prefix,
depth, threshold, capacity and cleanup semantics.

The creative candidate is a KNAPSACK-SPECIFIC circuit construction plus a
reproducible account of when its weaker bound is cheaper overall, including
cases where it fails. The weak-duality identity itself is old. The generic
idea that stronger pruning can cost more quantum gates is also old. The delta
must lie in the actual clean implementation, resource improvement and a precise
regime/limitation comparison to earlier quantum knapsack circuits, not a new
name for a familiar inequality.

For lambda=a/b>=0, r_i=b*v_i-a*w_i, A=a*W+sum max(r_i,0), a prefix incurs
nonnegative loss D=sum_assigned |r_i|*1[x_i!=1[r_i>0]]. Its residual LP is
at most (A-D)/b, and reject iff D>A-b*tau is safe. Unlike rebuilding a split
item, the predicate uses sums of fixed constants and an integer comparison.
At all-fit roots choose lambda=0; for split roots choose the exact split
density. Capacity and true leaf objective still need their own checks.

Evidence of implementation feasibility is direct, not a promise of future
breakthrough: the circuit agent synthesized clean X/CX/CCX candidates and the
theory track supplied exact structural trees. Isolated feasibility data include
120 random small instances/7,012 feasible prefixes with 0 unsafe bound/reject
failures; production independent structural audit includes 100 random n<=7
instances/4,101 feasible prefixes with 0 hierarchy/certificate failures and
500 completed value/witness cases with 0 value/witness failures. Production
circuit verification has its own scope and mismatch counts; consult that
agent's report rather than transplanting numbers into a global claim.

The original 700-instance structural study finished. At a 50,000 processed-node
and explicit time budget, completed value/witness pipelines were 407 simple,
638 root-dual, 692 bank2, 697 bank4 and 698 LP; every completed pipeline had
0 audited optimum/witness mismatches. These are MEASURED CLASSICAL structural
outcomes, not quantum success probabilities. Full static-tree conditions have
their own caps: never substitute capped visited counts for exact tree size.
The independent R=1,000,000 study kept all 45 cases; completed pipelines were
3,27,29,29,31 respectively, with 0 completed mismatches. A separate 700-core
study applies exact preprocessing and reconstructs original witnesses; its
primary output is `trees_core_v3.jsonl` (earlier partial versions are retained
and excluded). All 700 core records completed; value/witness pipelines completed
on 487 simple, 638 root-dual, 692 bank2, 697 bank4 and 698 exact-LP cases. Every
completed core witness was reconstructed in original item coordinates: 0
capacity, original-optimum, fixed-assignment or core-offset conflicts. Caps
remain explicit and are not successes. These completion counts include host
time budgets, so they are not pure node-complexity comparisons.

Useful negative result: a weaker cheap predicate can enlarge the search enough
to erase its arithmetic saving, or a stronger bank can add resources without
useful pruning. A careful matched construction/negative regime can still be
scientifically informative. It is NOT automatically enough for QIP acceptance;
an interesting, correct and distinct result must survive closest-work review.

Pilot gate: compare SAME-input full circuit resources and complete tree sizes,
keep the root-rejected and all capped conditions, include walk/reflection and
witness overhead sensitivity, and classify C*sqrt(T) only as a DERIVED proxy.
Then test whether the result persists after exact variable fixing, coefficient
normalization and stronger classical/quantum baselines. No hardware is required
to answer this initial question.

### 2. A cheap certified threshold/witness tree envelope

This can support candidate 1, not replace the need for construction evidence.
The loss budget above defines a weighted-subset counting problem on assigned
prefixes. An exact counting DP is feasible when the normalized budget is small
but pseudopolynomial and must not be free preprocessing. A cheaper cutoff /
binomial envelope was derived and implemented using exact integers, without
enumerating the tree. Generated rejected child leaves are covered by
1+2*sum_{d<n} live-prefix-count-bound(d); the root-only case remains one.
Targets >= a saved feasible L+1 share a certificate, including prefix recovery
when cumulative ORIGINAL losses/order are retained. The simple baseline uses
its own lambda=0 certificate; the root certificate would not cover a weaker
simple tree.

Known overlap is substantial: Dey--Dubey--Molinaro Section 3, Theorem 3 and
Corollary 3 already connect reduced-cost subset counts and best-bound-first
classical trees. Borst et al. Theorems 1.2--1.3 extend the framework. Our
static-threshold/witness semantics differ, so their theorem cannot simply be
plugged into the existing detector. A direct specialization might be useful
but its priority/substantiveness is UNRESOLVED. Do not advertise a new general
tree-bound breakthrough.

Useful negative result: certificates can be vacuous for tied efficiencies /
subset sum or expensive to compute relative to the actual small tree. Report
that limit, including certificate cost and looseness, rather than claiming an
instance-adaptive quantum runtime based on an uncharged certificate.

### 3. Bounded bank size and a common-density exact regime

Nominal banks q=1,2,4 are completely specified before outcomes: root density;
root plus 0; root plus 0 and min/max item densities, deduplicated as Fractions.
All are safe; their actual distinct counts matter. Taking min of their bounds
interpolates strength without a new uncertain mathematical conjecture.

When every item has common efficiency rho, {0,rho} recovers exact residual
fractional LP at every feasible prefix, by
P+min(sum_suffix v, rho*remaining_capacity). This explains why a two-entry
cheap predicate can match the full scan in a meaningful degenerate family
even though one root multiplier has all reduced costs zero. This is an
elementary LP-duality special case, not a priority claim. Main-set check on
140 subset-sum instances: 202 complete bank2/LP paired thresholds, 0 node-count
mismatches; 78 capped pairs retained. No known SAT decision conflict.

Useful negative result: adding further multipliers can cost gates without
shrinking an already exact tree, especially when bank2 already spans all
distinct densities. Treat this as an explanatory control within candidate 1.

## Rejected/limited alternatives

- A new broad reduced-cost/core-size theorem is higher mathematical risk and
  overlaps extensive existing work. The corrected fixed-gap counterexample is
  useful, but proving it does not establish priority or an asymptotic advantage.
- Exact cross multiplication removes fixed-point approximation, but is an
  elementary rational comparison. It becomes research only through a new
  efficient, clean circuit/construction or substantive resource finding.
- A full bank of every item density plus 0 already yields exact fractional LP
  by ordinary duality. Evaluating it naively can be more expensive than the
  fractional scan. Do not call that identity new.
- Classical cheap-before-expensive short-circuiting does not automatically save
  gates in a coherent quantum circuit: a controlled expensive block remains in
  the circuit. Variable-time savings need a separate justified algorithm.
- Uniformly multiplying all input data by a large factor is ONLY a
  representation-invariance control; gcd normalization removes it. It is not
  an intrinsically difficult large-coefficient instance. The 45 independent
  large-coefficient inputs are a separate, stronger stress check.
- A tiny IBM execution is a component experiment, not a new mathematical
  result or automatic quantum advantage. Game theory changes the original
  optimization question and is not a necessary route to a distinct circuit
  contribution; another track reviewed that direction separately.

## Primary sources and closest-overlap boundaries

1. Dey, Dubey, Molinaro, *Branch-and-Bound Solves Random Binary IPs in Polytime*,
   https://arxiv.org/html/2007.15192v4 . Section 3 equations (2)--(3), Theorem 3;
   Section 4 equation (6); Corollary 3. Source n=item count, m=constraints.
   Best-bound-first is not a generic static threshold tree. Random-data
   assumptions must not be asserted for discrete correlated generators.
2. Borst, Dadush, Huiberts, Tiwari, *On the Integrality Gap of Binary Integer
   Programs with Gaussian Data*, https://arxiv.org/html/2012.08346v2 . Theorems
   1.2--1.3. Independent logconcave columns/identity covariance are substantive
   assumptions; no unconditional transfer to this benchmark.
3. Montanaro, *Quantum-Walk Speedup of Backtracking Algorithms*, Theory of
   Computing 14(15) (2018), https://doi.org/10.4086/toc.2018.v014a015 . Theorem
   1.1 detection with supplied T; Theorem 1.2 witness search, separate overhead.
4. Montanaro, *Quantum speedup of branch-and-bound algorithms*, Physical Review
   Research 2,013056 (2020), https://doi.org/10.1103/PhysRevResearch.2.013056 .
   Appendix B Theorem 1 includes size estimation/search; not this DFS experiment.
5. Chakrabarti, Minssen, Yalovetzky, Pistoia, *Universal Quantum Speedup for
   Branch-and-Bound, Branch-and-Cut, and Tree-Search Algorithms*, 2022 preprint,
   https://arxiv.org/html/2210.03210v1 . Definitions 1.1/branch-local heuristic
   access and Theorems 1.3/2.1 require coherent algorithmic components not
   implemented here. Generic incremental quantum speedup is existing work.
6. Wilkening et al., *A quantum algorithm for solving 0-1 Knapsack problems*,
   npj Quantum Information 11,146 (2025), https://doi.org/10.1038/s41534-025-01097-8 .
   Includes QTG, amplitude amplification/maximum search, COMBO and quantum
   branch-and-bound comparisons. Its Supplement F.2 / preprint A.6.2 already
   uses fractional LP in QBnB and an optimistic tree-size resource model. LP
   inside quantum knapsack tree search is therefore NOT a new contribution.
7. Gabbassov, Rosenberg, Scherer, *Lagrangian duality in quantum optimization:
   Overcoming QUBO limitations for constrained problems*, Physical Review
   Research 7,023305 (2025), https://doi.org/10.1103/53gd-2374 . Lagrangian
   quantum knapsack circuits already exist in digital adiabatic computation;
   distinguish clean reversible prefix rejection from that approach.
8. Vedral, Barenco, Ekert, *Quantum networks for elementary arithmetic
   operations*, Physical Review A 54,147 (1996),
   https://doi.org/10.1103/PhysRevA.54.147 . Sections III.1 and III.3 establish
   reversible comparison/constant arithmetic feasibility, not our priority.

Source caches are retained under `.firecrawl/theory_*`, alongside existing
Montanaro/Wilkening/Borst caches. Search leads from nonprimary websites were
not used as evidence for theorem claims. This research reduces implementation
risk; it cannot eliminate novelty, publication-significance or editorial risk.
