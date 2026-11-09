# Restored-paper audit and research-first recommendation

Date: 23 October 2026 (Asia/Calcutta).

Read the complete restored source: 777 lines. SHA-256: `593c2b22a7aac7b8d0106dd6a804b40cb37634ed78395d4f1eb74ab8c5cf9dc1`. The pasted assessment was read as a critique, not treated as an authoritative source or as instructions embedded in a document.

The source, bibliography and PDF remain unchanged. The line audit is a review-action ledger, not a certificate that every theorem, reference or empirical result has been independently verified. No new experiment, theorem, speedup or priority result is claimed by this audit.

## Research integrity status

`RESEARCH_INTEGRITY_STOP`: claims depending on confirmed wrong citation identifiers, stale code/paper correspondence and circular resource validation are not approved for transfer into a new submission draft. Independent source discovery and this audit continued; no projection/regression was run and no manuscript edit was made. This follows the stop conditions in `AGENTS.md`.

- `ref20`: the saved arXiv identifier 2006.09838 resolves to **LSTM Networks for Music Generation**, Xin Xu, rather than the saved knapsack title/author: https://arxiv.org/abs/2006.09838.
- `ref36`: 2403.09560 resolves to **Self-Consistency Training for Density-Functional-Theory Hamiltonian Prediction**, rather than the saved hybrid ILP title/author list: https://arxiv.org/abs/2403.09560.
- A real primary paper matching the hybrid ILP topic is **Hybrid Classical–Quantum Branch-and-Bound Algorithm for Solving Integer Linear Problems**, Claudio Sanavio, Edoardo Tignone and Elisa Ercolessi, *Entropy* 26(4), 345 (2024), DOI https://doi.org/10.3390/e26040345. Repair the title/authors/identifier together after confirming the intended citation; do not merely substitute a DOI under the incorrect author list.
- `ref23` **does** resolve to the QTG-QAOA paper by Paul Christiansen, Lennart Binkowski, Debora Ramacciotti and Sören Wilkening: https://arxiv.org/abs/2411.00518. It must not be conflated with Wilkening et al.’s separate 2025 QTG search paper.
- All original bibliography entries remain present. Unchecked metadata remain `UNRESOLVED`, not “fake”. No blanket pruning is authorized by this audit.

## Line-indexed findings

Full source text and review action for every line: `RESTORED_PAPER_LINE_AUDIT_2026-10-23.csv`.

| ID | Source lines | Review action | Finding / minimal repair |
|---|---|---|---|
| A01 | 1–54 | FORMAT_LATER | IEEE conference layout, long abstract and seven keywords; apply journal formatting after substantive decisions. Preserve author order; confirm corresponding author and declarations. |
| A02 | 52–52 | CORRECT | Abstract includes unsupported novelty/near-constant-core/general hardware conclusions and the stale query bound. Patch its factual claims after fixing their underlying results; shortening alone cannot repair them. |
| A03 | 61–65 | VERIFY_SOURCE | Qualify polynomial/bit costs and scope of meet-in-the-middle versus subset sum. Verify each reported subset-sum exponent and heuristic interpretation from its primary paper; do not delete its citation merely because that check is pending. |
| A04 | 67–80 | PRIORITY_UNRESOLVED | Hybridization, binary search and quantum knapsack already have close predecessors. Replace uniqueness only after a claim-by-claim comparison; component experiments are not a full quantum optimizer. |
| A05 | 83–83 | CORRECT | Says h is not synthesized, contradicting lines 78 and 275. Select a precise implementation/version and say what was synthesized. |
| A06 | 92–100 | VERIFY_SOURCE | Keep literature breadth. Repair individual metadata and claims. Pisinger abstract credits Balas and Zemel; QTG-QAOA and the separate QTG-plus-maximum-finding algorithm are different papers. |
| A07 | 98–98 | RESEARCH_INTEGRITY_STOP | ref20 and ref36 have confirmed wrong arXiv identifiers. Freeze claims relying on those identifiers; preserve entries and repair individually. ref23 identifier does match the QTG-QAOA paper. |
| A08 | 100–130 | PRIORITY_UNRESOLVED | Capability/uniqueness checklist needs a technical comparison, including Wilkening 2025, Creemers/Perez Armas 2025, Sanavio et al. 2024, Bozejko et al. and relevant quantum tree-search work. Do not infer absence from silence. |
| A09 | 139–167 | CORRECT | Global distinct-efficiency assumption excludes subset-sum benchmarks. Allow ties with deterministic ordering; reserve strict spacing for the spacing result. Handle all-fit instances when no split item exists. |
| A10 | 169–176 | CORRECT | An arbitrary efficiency band does not justify fixing items outside it. Distinguish the analytical band from Algorithm 1 exact forced-item fixing; correct historical attribution. |
| A11 | 178–195 | CORRECT | Use exact source assumptions and theorem numbers. Montanaro 2018 Theorem 1.1 is detection; Theorem 1.2 addresses witnesses. Do not equate this with the complete adaptive 2020 optimizer. |
| A12 | 201–203 | VERIFY_SOURCE | State meet-in-the-middle arithmetic/bit costs consistently, including sorting and odd n. Avoid comparing oracle queries directly with runtime. |
| A13 | 216–247 | CORRECT | Initialize fixing sets and handle overweight/all-fit inputs. Keep the exact forced-item LP tests; distinguish this safe rule from a guessed efficiency band. |
| A14 | 249–257 | CORRECT | Static threshold detection needs a fixed threshold during each call; a changing classical incumbent defines a different process. Bound and account for all value-search and witness calls. |
| A15 | 259–282 | RESEARCH_INTEGRITY_STOP | Old h resource/verification claims do not establish the revised coherent node predicate. Legacy test clips input components and compares to truncated arithmetic. Preserve the table pending a provenance/scope repair; do not silently relabel it as new evidence. |
| A16 | 284–305 | CORRECT | Algorithm 2 returns an assignment but gives only value detection. Specify witness extraction, error allocation and a valid size-bound procedure or adaptive detector. |
| A17 | 307–337 | VERIFY_IMPLEMENTATION | Keep the answer-agnostic threshold predicate. Audit cleanup/threshold domains. Treat QFT synthesis T counts as derived estimates, not hardware measurements or lower bounds; separate the small maximum-finding component from the main optimizer. |
| A18 | 339–375 | CORRECT | Reconstruction requires an actual recovered core assignment. Propagate failure budget and size-bound assumptions into the overall pseudocode; retain its three-phase structure. |
| A19 | 377–398 | VERIFY_DATA | Minimum of per-constraint LP bounds is valid but is not generally a surrogate relaxation using combined constraints. Check the data and confidence interval construction before retaining the multidimensional table; scope conclusions to tested configurations. |
| A20 | 407–414 | CORRECT | Derive the rounding error and rational threshold separation. Extend the safe predicate explicitly to every node/threshold, preserve exact ordering, handle ties/all-fit cases, and state that the precision condition is sufficient, not necessary for every instance. |
| A21 | 417–430 | CORRECT | Current probability/repetition statement omits a complete witness procedure and adaptive decision-error accounting. Correct both directions of fixing and final reconstruction. |
| A22 | 432–442 | VERIFY_DERIVATION | Retain containment/spacing analysis. Supply the dual-bound derivation, include the split-item case and distinguish upper bound from equality after split shifts. The spacing packing argument alone does not establish priority. |
| A23 | 444–445 | CORRECT | A full binary depth-m tree has 2^(m+1)-1 vertices. Re-derive the displayed exponential substitution as well: the stated half-sized exponent does not follow from the preceding core-size bound. Trace the reported check counts to their artifacts. |
| A24 | 447–447 | CORRECT | Rational values/capacity violate the declared integer problem class. Bounded-but-varying gaps alone also do not disprove every arbitrary gap-only function. The preserved revised integer fixed-gap construction is a candidate replacement, not a priority claim. |
| A25 | 449–488 | CORRECT | Replace the complete query accounting consistently in the theorem, proof and table, preserving separate cost models and assumptions for prior work. Actual encountered tree size is not automatically a free input certificate. |
| A26 | 496–501 | RESEARCH_INTEGRITY_STOP | Paper and current code differ after paper-only rollback. Current quantum_bb_optimize includes witness recovery and deterministic analytical-majority decisions; query counts are SCHEDULED and the walk output SIMULATED. Original benchmark_v5 hardcodes correctness for n>20. |
| A27 | 503–524 | VERIFY_DATA | Specify n/seed aggregation for fixing ratios. Old data and exact rerun are different artifacts; choose and label the appropriate version. A zero gap for subset sum is a tested-set fact, not a universal property. |
| A28 | 526–566 | VERIFY_DATA | Keep all capped/trivial/bypassed counts. Reconcile spectral decomposition and paired configurations. Independent-sample tests and binomial population interpretations require assumptions not supplied by a deterministic selected subset. |
| A29 | 568–573 | VERIFY_DATA | Baseline already uses LP bounds. 1500 method records are not 1500 independent matched instances. Attribute timing/memory statistics to the implementation version that produced them. |
| A30 | 575–630 | VERIFY_DATA | Preserve archived OR-Tools solve-time and cutoff tables. Trace rows, trials, limits and certified outcomes; keep excluded cutoffs counted and avoid interpreting rounded times as zero. |
| A31 | 633–653 | RESEARCH_INTEGRITY_STOP | Regression script uses T_full, not actual reduced-core threshold-tree size, and adds epsilon to zero gaps. Separate this from the resource-estimate regression, which is CIRCULAR_VALIDATION because scheduled query budgets are constructed from tree size/depth. |
| A32 | 657–665 | CORRECT | Finite-size small core ratios do not prove a near-constant core. Large core does not imply a hard residual tree, especially subset sum. Compare fixing/no-fixing using matched metrics; the square-root query factor alone is not an empirical speedup. |
| A33 | 667–695 | VERIFY_PROVENANCE | Preserve hardware observations pending provenance reconciliation. Existing summary has no job IDs/circuit hashes connecting it to current code. Use hardware data only within established execution scope; no universal size/noise boundary follows. |
| A34 | 698–704 | CORRECT | Remove universal hardware-size statements and asymptotic performance inferences unsupported by the scoped data; retain useful limitations and component observations. |
| A35 | 706–731 | RESEARCH_INTEGRITY_STOP | T-count estimates are not certified lower bounds or measurements; T gates and classical nodes are unlike units. The fitted query-slope resource path is CIRCULAR_VALIDATION, not independent evidence. Preserve archival estimates and repair the cost model before publication. |
| A36 | 733–735 | CORRECT | Capacity DP can use O(W) working memory. Reconcile h synthesis statements and distinguish an exact pruning decision from exact representation of a rational LP value. |
| A37 | 740–752 | CORRECT | Make conclusion match resolved results and scope; no first/unique or universal hardware boundary claims until supported. Preserve the research idea and useful future directions. |
| A38 | 757–775 | VERIFY_REPRODUCIBILITY | Confirm repository version actually contains every claimed script/result. Add truthful author declarations and appropriate AI disclosure later. Preserve acknowledgments unless an author corrects them. |

## Call paths and primary-source boundaries

- `simulation/quantum_backtracking.py::quantum_bb_optimize` calls `quantum_detect` during binary search and prefix recovery, then calls `_classical_optimum` only for the final audit. `quantum_detect` explicitly constructs its threshold tree, selects phase precision using its size/depth, computes analytical acceptance and a deterministic majority decision. Its `queries` field is SCHEDULED, not a measured quantum runtime. This does not yet compose a full gate-model walk.
- `simulation/oracle_h/node_bound_reversible.py::build_node_bound` compiles fixed item quotients, scans the node’s residual LP bound, compares an integer cross product and uncomputes. `build_coherent_node_bound` dispatches over depth. This is separate from the legacy divider-based resource experiment in the restored paper.
- `simulation/oracle_h/verify_circuit_m4.py` clips v_s, w_s, W_res and V_int to 15 in its old benchmark loop. It therefore does not test the unchanged benchmark inputs or certify every node predicate on them.
- `simulation/benchmark_v5.py` assigns `correct=True` for n>20. The restored statement that all cases were independently checked against DP cannot be supported by that flag.
- `simulation/tlp_regression/analysis.py` fits `T_full` and adds 1e-6 before taking log(gap). That mismatch requires correction. It is distinct from the circular query-slope fitting in `simulation/resource_estimate.py::load_quantum_scaling`.
- Hardware summary provenance is unresolved, not demonstrated false. Preserve raw observations and seek saved job IDs, circuits and calibration/shot metadata before attributing them to a particular current implementation.

The previous revision’s code, derivation logs and generated results remain available. Necessary corrections can be reused after checking their scope; the previous broad literature rewrite need not be repeated.

### Quantum theorem mapping

Primary source: Ashley Montanaro, **Quantum-Walk Speedup of Backtracking Algorithms**, *Theory of Computing* 14(15), 1–24 (2018), https://doi.org/10.4086/toc.2018.v014a015. Read the preserved full primary text, particularly Theorems 1.1 and 1.2 and the distinction between detection and search.

For Theorem 1.1, source n maps to the residual/core Boolean-variable count, source T to a valid bound B on the fixed detection tree, source failure δ to the allocated error of that individual call, source P to the node predicate, and source branching h to the deterministic next-variable rule. That h is not the manuscript’s LP-bound h. A source-query bound excludes arithmetic costs, preparation of a size certificate and full coherent walk-gate costs. A detector output alone does not supply a witness. Theorem 1.2 is a separate search result. No new central theorem is derived or approved here.

## What could support a distinct contribution?

Current priority status for each proposed extension: **UNRESOLVED**. The targeted search identifies overlap; it cannot certify that a method is the first of its kind.

| Candidate | Specific research question | What would count as progress | What would not establish novelty |
|---|---|---|---|
| Resource-aware reversible LP pruning (recommended practical investigation) | Does the tree reduction from a clean LP predicate offset its arithmetic, depth dispatch, walk-reflection and recovery costs, relative to a precisely matched simpler predicate? | A proved safe construction plus a new resource improvement or a reproducible regime map, with full coherent composition on tractable cases and comparable gate/resource models. | Merely using known adders/dividers, showing a tiny oracle circuit, or plotting sqrt(T) budgets constructed from T. |
| Knapsack-specific certified tree bound (strong theoretical target; higher uncertainty) | Can observable instance data yield a useful bound for this exact static threshold/recovery-tree family without enumerating the tree, with all certification costs counted? | A bound genuinely tighter in a stated regime and not an immediate corollary of existing reduced-cost tree bounds; a valid mapping to every detector and witness call. | Reusing the full binary-tree bound, assuming a small core from random data, or importing a best-bound-first random-IP theorem without its assumptions. |
| Integer gap counterexample and precision lemma | Are the corrected results absent from prior knapsack/core and reversible optimization literature, and do they provide a substantive new consequence? | Full proof, falsification checks, and precise comparison to closest existing lemmas/results. | Fixing an error in this manuscript or stating a standard dual bound under a new name. |
| Full small-instance walk | Does the full reversible walk act correctly, clean all workspace and recover a witness with the stated error control? | Exact small-case operator comparison plus a general construction and resource accounting. | Completing an already-known algorithm alone; this is implementation evidence, not automatic novelty. |

### Prior work that changes the novelty assessment

1. **A quantum algorithm for solving 0-1 Knapsack problems**, Wilkening et al., *npj Quantum Information* 11, 146 (2025), https://doi.org/10.1038/s41534-025-01097-8. The primary paper includes QTG, amplitude amplification/maximum finding, resource comparisons and COMBO benchmarks. “Knapsack-specific and gate-model” is not a sufficient distinguishing claim. Its hard-instance generator is also a relevant benchmark lead, rather than assuming small-coefficient Pisinger-style inputs are sufficient.
2. **Discrete optimization: A quantum revolution?**, Creemers and Pérez Armas, *European Journal of Operational Research* 323(2), 378–408 (2025), https://doi.org/10.1016/j.ejor.2024.12.016. Quantum binary search and hybrid branch-and-bound are existing context.
3. **Optimal solving of a binary knapsack problem on a D-Wave quantum machine and its implementation in production systems**, Bożejko et al., https://doi.org/10.1007/s10479-024-06025-1, online 2024 / issue 2026. Distinguish annealing from coherent gate-model tree walks without calling generic hybridization new.
4. **On the Integrality Gap of Binary Integer Programs with Gaussian Data**, Borst, Dadush, Huiberts and Tiwari, primary full text https://arxiv.org/html/2012.08346v2. Section 1.1, Theorem 1.2 relates best-bound-first tree size to a reduced-cost knapsack counting set and credits Dey–Dubey–Molinaro Corollary 2. Theorem 1.3 adds independent logconcave columns with identity covariance; the paper’s source m is the number of constraints, not this manuscript’s number of core items. Here A would be the row of item weights, c item values, b capacity and λ an LP-dual multiplier, but our static threshold/recovery trees are not automatically the source’s best-bound-first process. Discrete correlated benchmark generators do not automatically satisfy the distribution/covariance assumptions. **Do not transfer the theorem as a new bound for this paper.** Read the original Dey–Dubey–Molinaro source before proposing any extension based on its result.
5. **A Quantum-Classical Hybrid Branch & Bound Algorithm**, Czégel, Sipos and G.-Tóth, arXiv preprint https://arxiv.org/html/2511.19501v1 (23 November 2025). The abstract/introduction describe a hybrid method for equality-constrained binary linear programs, classical bounds and variational quantum optimization, with set-partitioning tests. This is broad hybridization overlap, not proof that the manuscript’s exact LP predicate is already implemented there. Preprint status is kept explicit.
6. **Universal Quantum Speedup for Branch-and-Bound, Branch-and-Cut, and Tree-Search Algorithms**, Chakrabarti et al., https://arxiv.org/abs/2210.03210. Abstract-level discovery identifies a relevant incremental-search comparison. Its theorems have not been transferred into this manuscript; full theorem/source mapping is pending.
7. **Beyond Worst-Case Branching: Quantum Tree Search via Amplitude Amplification**, Wichert, https://arxiv.org/abs/2606.28452. A 2026 preprint discovery lead only. The abstract is not sufficient to accept its complexity claims or reject a proposed contribution; full verification is pending.

### Feasibility gates before rewriting

1. Reconcile research correctness first: witness recovery, per-call error, tree-size information, integer counterexample, exact safe node pruning and data provenance. Use the preserved corrected code where appropriate; do not discard legitimate literature.
2. Search for overlap with the specific proposed result. Write the claimed difference and its assumptions in one sentence before implementing a new method.
3. Derive any new lemma before code, attempt counterexamples, and keep failed attempts. Do not approve the central claim in the derivation pass.
4. Run matched ablations only after semantics are fixed: fixing/no fixing; simple/LP predicate; exact/safely rounded predicate; include witness recovery, certificate computation, arithmetic width and failures/caps. Count classical solver time and quantum resources separately; do not equate their units.
5. Include difficult large-coefficient/hard-generator cases and an appropriate specialized classical baseline such as COMBO where available. Do not announce a win in advance. Compare QTG under an explicit compatible cost model.
6. If pruning overhead defeats the tree saving, retain the negative finding and reassess the paper’s contribution rather than changing the metric. If the certificate follows immediately from prior work, do not call it a new theorem.
7. Only after those decisions, patch the original paper locally. Preserve its structure, relevant reference coverage, original data and archival versions. Log each corrected sentence/table and its supporting evidence.

## QIP acceptance-rate check

Official journal homepage checked: https://link.springer.com/journal/11128. Official submission instructions checked: https://link.springer.com/journal/11128/submission-guidelines. The current official homepage reports **32 days median submission to first decision**; this is a publisher-reported process metric, not our experiment and not an acceptance probability.

No verified public journal acceptance percentage or desk-rejection percentage was found in the checked official pages or the targeted search. Third-party metric aggregators have acceptance-rate headings without a substantiated journal denominator, and some search hits concern the separate QIP conference. **Acceptance rate: UNRESOLVED / not verified. Desk-rejection rate: UNRESOLVED / not verified.** No numeric estimate should be given.

A genuine and significant new result can address an originality concern; it cannot guarantee external review or acceptance. Correctness, significance, scope, clarity, documentation and editorial judgment still matter. A complete small quantum circuit is not a stated universal requirement for theoretical QIP papers.

## Collection record and limits

Graph-tool discovery again returned no graph methods, so targeted filesystem reads were used. Firecrawl searches and primary-source snapshots are under `.firecrawl/`, including QIP home, old-reference identifier checks, current hybrid work and the reduced-cost tree-bound source. All search leads and failed/no-result searches are retained. Search-feedback windows expired while processing the source audit; no late claim of feedback success was made.

No full 45-entry bibliography verification, independent approval of every proof, full walk implementation, new circuit synthesis, hardware run or baseline experiment was completed in this turn. These must not be implied by “line-by-line review”.
