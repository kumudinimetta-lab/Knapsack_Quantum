# Tree and algorithm study: derivations, checks and scope

Date: 23 October 2026. Restored manuscript, bibliography, historical raw data
and earlier simulation modules are unchanged. New code is isolated in
`simulation/pruning_study_20261023/trees.py`; new experiment records are append-only.

## Derivation / independent-audit boundary

The root-dual identity, strict inequality, static prefix counting envelope and
counterexamples were derived BEFORE new simulation code, in
`research_log/deep_research_20261023/theory_derivation_candidates.md`.
The parent agent independently audited that algebra in a separate pass:
nonnegative multiplier a/b with b>0, residual fractional completions valid,
strict loss comparison (equality survives), generated rejected children included,
root-rejected tree size at least one, and original cumulative prefix losses for
witness calls. This was a LIMITED ALGEBRA AUDIT, not priority approval or a
quantum runtime guarantee. No agent has approved a new central novelty theorem.

The exact LP scan is an independent Fraction-based reference. All methods use
the SAME fixed decreasing exact-efficiency order, stable ties, identical capacity
rejection, and actual leaf-profit marking. Zero capacity, all-fit instances,
empty instances and infeasible prefixes have explicit behavior. Prefix bits
refer to original ordered items; prefix recovery never restarts loss at zero.

## Source/theorem mapping

1. Dey, Dubey and Molinaro, *Branch-and-Bound Solves Random Binary IPs in
   Polytime*, full primary https://arxiv.org/html/2007.15192v4 . Section 3,
   equations (2)--(3), and Section 4 equation (6) already express the reduced-cost
   deviation identity. Their Theorem 3 bounds their best-bound-first final tree
   by 2*n*|G|+1, with G defined using the actual integrality gap. Source n maps
   to item count; source m maps to number of constraints (one here), NOT core
   size. Their Theorem 1 additionally assumes independent uniform [0,1] data
   and fixed packing RHS proportions. Our discrete/correlated generators do
   NOT inherit that distributional theorem. Their Corollary 3 supplies a
   deterministic bucket/binomial envelope for best-bound-first trees. Neither
   that process nor the root integrality gap is substituted for this study's
   static threshold/witness tree. The direct prefix-budget argument is logged
   separately; its novelty remains UNRESOLVED and it overlaps this framework.
2. Borst, Dadush, Huiberts and Tiwari, *On the Integrality Gap of Binary Integer
   Programs with Gaussian Data*, https://arxiv.org/html/2012.08346v2 . Theorem
   1.2 recalls a related best-bound-first reduced-cost counting bound. Theorem
   1.3 assumes independent logconcave columns with identity covariance, n>=
   100(m+1), and a probabilistic integrality-gap bound. No such assumptions are
   asserted for the benchmark. This source rules out presenting the generic
   gap/reduced-cost/counting connection as new.
3. Montanaro, *Quantum-Walk Speedup of Backtracking Algorithms*, Theory of
   Computing 14(15), 2018, https://doi.org/10.4086/toc.2018.v014a015 . Theorem
   1.1 is detection with a supplied size bound T, Boolean-variable count n and
   per-call failure delta. In this study T maps to a generated-node certificate
   B and n to the original item count. Predicate P maps to the chosen safe
   pruning/marking predicate and branching h to fixed next-variable order.
   Source h is NOT this paper's LP-bound oracle h. Its hidden-constant query
   expression is NOT executed by our classical structural accounting. Theorem
   1.2 is a distinct witness result. This code instead records an explicit
   sequence of threshold decisions followed by prefix decisions; it uses no
   separate optimum as advice.
4. Montanaro, *Quantum speedup of branch-and-bound algorithms*, Physical Review
   Research 2, 013056 (2020), https://doi.org/10.1103/PhysRevResearch.2.013056 .
   Full primary cached as `.firecrawl/montanaro2020.md`, Appendix B Theorem 1
   includes size estimation, threshold search, witness finding and logs/depth
   terms. We do NOT claim this adaptive algorithm was executed by our DFS.
5. Chakrabarti, Minssen, Yalovetzky and Pistoia, *Universal Quantum Speedup for
   Branch-and-Bound, Branch-and-Cut, and Tree-Search Algorithms*, preprint
   https://arxiv.org/html/2210.03210v1 . Definition 1.1 requires monotone cost;
   Theorem 1.3 and Theorem 2.1 concern incremental search using coherent branch,
   cost and branch-local heuristic access. We have not implemented those
   procedures and do not inherit their runtime claims. Their existence is
   a novelty boundary for generic quantum speedup/adaptive-size claims.
6. Wilkening et al., *A quantum algorithm for solving 0-1 Knapsack problems*,
   npj Quantum Information 11,146 (2025), https://doi.org/10.1038/s41534-025-01097-8 .
   QTG plus amplification/maximum search, COMBO comparisons, gates/qubits and
   preprocessing/upper-bound improvement directions are existing work. The
   fact that its future-work discussion mentions upper bounds means simply
   adding such a bound is not enough for a substantial contribution.
7. Gabbassov, Rosenberg and Scherer, *Lagrangian duality in quantum optimization:
   Overcoming QUBO limitations for constrained problems*, Physical Review
   Research 7,023305 (25 June 2025), https://doi.org/10.1103/53gd-2374 . Sections
   III--IV use Lagrangian formulations in digital adiabatic circuits and study
   knapsack resources. That differs from a clean prefix-tree reject predicate,
   but precludes claims of the first quantum use of Lagrangian knapsack bounds.

## Certification and query-scale semantics

For lambda=a/b>=0, r_i=b*v_i-a*w_i, A=a*W+sum(max(r_i,0)) and loss
D(prefix)=sum_assigned |r_i|*1[x_i != 1[r_i>0]], weak duality gives residual
LP <= (A-D)/b. Reject if D>A-b*tau. For H=A-b*tau, live depth-d prefixes are
contained in cost-subsets of the first d items with total <=H. If a cutoff t>0
leaves s costs below t and l costs >=t, at most floor(H/t) costly deviations
are possible, yielding 2^s * sum_{j<=min(l,floor(H/t))} binom(l,j). Optimize
over positive stored costs and t=1, cap at 2^d. The generated-node bound is
1+2*sum_{d=0}^{n-1} upper_live_prefix_count(d); when H<0 it is exactly one.
No tree enumeration is used to obtain this cheap certificate. Its integer
computation time is recorded separately and must be included in any future
end-to-end resource claim. Arithmetic bit costs are not erased by counting
only the number of integer operations.

All optimization targets are >= initial feasible incumbent L+1. The initial
incumbent comes with a saved feasible witness. If optimum=L, that witness is
returned. Otherwise binary search is followed by n prefix decisions at the
found target. Calls use original instance/order/loss, not a freshly recentered
dual system. The same certificate at tau=L+1 covers those trees. For `simple`,
the certificate explicitly uses lambda=0; a root-dual certificate would not
necessarily cover this weaker method. Bank2 and bank4 contain root lambda,
so the root-dual certificate covers them; it also covers exact LP.

The `conditional_detection_scale` is sqrt(B*max(1,n))*log(M/delta), tagged
SCHEDULED, with hidden constants omitted. It is an analytical comparison
scale from a theorem, NOT an executed number of quantum queries, an empirical
measurement, a complete error-bounded walk implementation or a runtime.
All actual decisions are from exact CLASSICAL DFS. A cap can still establish
SAT if a witness was already found; UNSAT is known only after full enumeration.
Complete tree sizes and early-stopped decision traversals are separate fields.
The implementation's `nodes` counter increments when a vertex is popped and
evaluated, including rejected children. For COMPLETE trees it equals the full
generated tree size. For capped or first-witness-stopped traversals it is a
processed-vertex count/lower bound; pending stack children have not been counted.
Never treat a capped `nodes` field as a complete T. Elapsed-time caps are checked
every 128 processed vertices, so they are soft diagnostic caps at that granularity.
This is explicitly a FIXED-ORDER, FULL-ASSIGNMENT-MARKING tree family. It does
not implement best-bound-first selection, fractional-variable branching,
partial-prefix success marking, or early return of an integral LP completion.
For example, a prefix whose profit already reaches tau could supply a witness
by filling the suffix with zero; this study still marks only at full depth.
Standard specialized classical B&B/COMBO may exploit stronger constructive
termination and many other reductions. A paired predicate comparison on this
chosen tree must not be presented as superiority over those algorithms or as
an optimal quantum/classical search tree. Adding such early-success rules
would require new matched tree semantics and witness handling, not relabeling
the existing records.

## Inputs and failures retained

- `inputs.json`: 720 unique inputs = five preserved tiny cases + 700 original
  generator settings + 15 scaled controls. Ten pilot IDs reference the five
  tiny and five n=12/seed=12000 main inputs. Input arrays and source provenance
  are retained, and an existing nonmatching registry is never overwritten.
- Uniformly scaled controls preserve feasible assignments and exact target
  predicates only when targets are scaled too. They are REPRESENTATION
  INVARIANCE controls. A competent solver can remove the common gcd, so these
  are not intrinsically hard large-coefficient examples or an advantage claim.
  Structural optimizer binary search intentionally receives unnormalized input;
  its extra integer-search calls on scaled data are a representation artifact.
- `inputs_stress_independent.json`: 45 unmodified R=1,000,000 instances from
  the prior saved exact-MITM comparison, n=20/24/28, five classes, three seeds.
  Its source SHA is retained and exact MITM optimum is independently recomputed
  before new tree experiments. These are separate from uniform scaling.
- A first independent-stress run had correct MITM arithmetic but a copied
  metadata string said DP. It was interrupted, retained as
  `trees_independent.jsonl`, and is EXCLUDED from final results. The driver
  was corrected and rerun to `trees_independent_v2.jsonl`; no raw record was
  manually changed. This failed attempt is retained to prevent provenance drift.
- Core experiment v1 used a new core greedy incumbent and could discard the
  stronger saved original incumbent; it remained correct but was an incomplete
  pipeline baseline. The partial `trees_core.jsonl` and source snapshot are
  retained and excluded from primary core results. Core v2 retained that saved
  feasible witness, but its first fixed diagnostic target was still based on
  a new core greedy value, preventing an exact before/after-fixing comparison.
  The partial `trees_core_v2.jsonl` and source snapshot are retained and excluded.
  Core v3 uses original L+1 minus fixed-in profit for the fixed diagnostic,
  exact core optimum+1 for its separate unmarked diagnostic, and the better of
  the saved feasible original witness restricted to the core and a new core
  greedy witness for actual value/witness search. Complete core witnesses are
  reconstructed in ORIGINAL item coordinates and checked for original capacity,
  original optimum, and fixed-in/fixed-out assignment consistency. Source
  snapshots and SHA manifests precede the v3 run.
- Pre-code counterexamples: negative multipliers invalid; equality cannot prune;
  subset sum with lambda=1 has zero reduced costs and no objective pruning;
  all-fit cases require lambda=0; capacity rejection is separate; stronger
  pruning can have more expensive coherent arithmetic. A controlled expensive
  block still costs gates; classical short-circuiting is not a quantum gate
  saving without further variable-time analysis.

## Initial scoped checks

`tree_audit.json`: MEASURED classical checks on 100 random n=0..7 instances,
seed 2026102301, all 4,101 feasible prefixes: 0 hierarchy failures and 0
certificate failures; 500/500 optimizer/method cases completed with 0 optimum
or witness mismatches and 0 caps. `trees_pilot.jsonl`: all ten canonical pilot
inputs across five methods, both fixed thresholds, and value/witness sequences;
0 caps and 0 completed-optimizer mismatches. These checks do not approve global
correctness, novelty, physical execution, practical acceleration or QIP acceptance.

Final structural files: `trees_full.jsonl` has 700 original inputs plus 15
uniform-scaling controls; `trees_independent_v2.jsonl` has 45 independent
large-coefficient inputs with recomputed MITM references;
`trees_core_v3.jsonl` has 700 core inputs. `tree_core_v3_summary.json` records
0 core-offset conflicts and 0 actual original-witness reconstruction failures
on every completed method/input: 487 simple, 638 root-dual, 692 bank2, 697 bank4,
698 exact LP. All noncompleted calls and all time/node caps remain present.
Host concurrency and exact-Fraction reference cost affect time-cap outcomes;
use complete paired trees for structural comparisons, with cap counts alongside.

## Predeclared limited time-cap escalation

Initial fixed-tree time caps materially censored deterministic comparisons,
especially 91 LP conditions on the concurrently loaded host. Per the protocol's
limited escalation rule, ALL 183 initial time-capped conditions were selected
without regard to method/result: five original-panel and 178 core-panel
conditions, zero independent-panel conditions. Before rerun, source/code hashes
and the reason were saved in `trees_timecap_reruns_before_manifest.json`.
The node budget remained 50,000 and the soft time cap increased from 0.4 to
5 seconds. `trees_timecap_reruns.jsonl` is an append-only overlay keyed by
id/target_kind/method, retaining the entire old status alongside the new tree.
All three original raw-file hashes were rechecked unchanged afterward.

All 183 reruns finished: 23 completed whole trees and 160 reached the same node
cap; 0 remained time-capped and 0 deterministic processed-prefix/known-decision
conflicts were observed. Original panel: 3 complete,2 node-capped; core panel:
20 complete,158 node-capped. Core LP alone: 12 of the 91 completed,79 reached
the node cap. Initial cap counts remain part of the failure ledger. Apply this
overlay ONLY to fixed-threshold structural comparisons, not the original
value/witness optimizer budgets/statuses. This is not machine-runtime evidence.

## Additional explanatory candidate, derived before the data check

If every item has the same efficiency rho>0, the two multipliers {0,rho}
already recover the exact residual LP at every feasible prefix: write P for
prefix profit, R for remaining capacity and Vrem for the sum of residual
profits. The lambda=0 bound is P+Vrem. The lambda=rho bound is P+rho*R.
Fractional knapsack with a common efficiency has value
P+min(Vrem,rho*R), equal to the minimum of those two bounds. If the original
root is all-fit, lambda=0 alone remains exact at all prefixes. Thus the
production bank2 predicate should match exact LP for the subset-sum generator
at every feasible node, not merely have similar median trees. This is an
elementary special case of LP duality/finite-bank completeness, not a novelty
claim. Independent review was requested before publication use. It explains
why root lambda alone can have zero-cost degeneracy, while adding zero may
recover full pruning cheaply.
