# Independent adversarial review and manuscript fit

23 October 2026. Independent reviewer of the circuit/theory agents' candidates. The manuscript, bibliography, existing experiment data and other agents' files were not edited. The reviewer saved isolated test programs and outputs only. This is not approval of novelty, a complete quantum optimizer, or journal readiness.

## Current conclusion

The selected production predicates and static structural optimizer survived a separate adversarial reference check. The proposed exact LP versus cheaper dual-bank study is coherent and executable. Its strongest plausible contribution is a knapsack-specific reversible construction and a carefully controlled resource/pruning comparison. The basic Lagrangian identity, rational cross multiplication, coherent depth indexing, and generic heuristic-depth/tree-size trade-off are prior knowledge.

The remaining major paper-quality gate is whether the resource result survives a **matched architectural baseline, shared walk overhead, a compact arithmetic control, and explicit cap/certificate accounting**. Passing toy correctness checks alone is insufficient. The current study does not establish an asymptotic quantum improvement or a practical speedup. The full walk is not implemented; that limits the resource claim, but is not a universal journal submission prerequisite.

Follow-up status: the compact control and every-input700 scoped gate checks subsequently completed. See `reviewer_followup_results.md` for independent fixing validation,534882 tested columns per family on all700 inputs (0mismatches/dirty/unsafe on stated sampled encodings), independent compact primitive/fixed-depth checks, a22-qubit dense example and paired-aggregator join/censoring review. The earlier sections below describe the initial review pass; they are retained rather than silently replacing its history.

## Independent test evidence

Pre-computation reasoning is in `reviewer_test_plan.md`. Prototype and production tests use an independent exact LP reference that enumerates integral subsets and fractional vertices; it does not call the candidates' greedy residual-LP scan. All clean-workspace encoded input columns are exhausted when input width is at most fourteen; the larger-width cases use 128 deterministic adversarial/random encodings, with both initial target bits. This is a selected fifteen-input test set, not the 700-instance benchmark and not arbitrary initial dirty workspace.

| Implementation scope | Families | Input-target columns per family | Predicate mismatches | Dirty-workspace columns |
|---|---:|---:|---:|---:|
| Preserved prototypes | exact single scan, exact depth wrapper, root dual | 24,432 | 0 for each family | 0 for each family |
| Production module | simple, root dual, bank2, bank4, exact single scan, fixed-point single scan, exact depth wrapper | 24,432 | 0 for each family | 0 for each family |

Circuit outputs and dirty-column counts are SIMULATED. Reference LP values are DERIVED exact rational enumerations. Input/configuration choices are HARDCODED. Production unsafe-pruning count: 0 for each of the seven families on the stated 24,432-column scope (SIMULATED comparison against independent exact LP reference). All-fit, empty, capacity-zero, duplicate ratios, equality, overweight prefixes, ignored suffix bits, invalid depths, large coefficient/gcd, large capacity, maximum encoded threshold and both target bits are represented.

The production structural optimizer was independently checked on those fifteen inputs for all five tree predicates: 75 completed method-input cases, 0 value mismatches, 0 invalid witnesses and 0 observed certificate violations on the checked adjacent threshold conditions (MEASURED classical execution with DERIVED exact enumeration references). All three intentionally tiny build limits triggered the correct cap reason (MEASURED build behaviour). No hardware job or regression was performed.

Raw results and exact source hashes: `reviewer_adversarial_probe.json` and `reviewer_production_probe.json`. These hashes scope this review. Later source changes require a targeted review of their effects; this result must not be silently attached to a different source version. The inherited BooleanCompiler and circuit simulator remain shared dependencies; these tests independently check the mathematical reference, and the circuit agent separately provides dense Qiskit checks where feasible.

## Mathematical and implementation assessment

### Exact node LP comparison

For positive integer weights, values and nonnegative capacity, exact ratio order fixes the residual fractional-knapsack LP. At a feasible prefix, U=P+r*a/b with reduced split ratio a/b and 0<=r<w_s. The comparison U<tau is exactly equivalent to P*b+r*a<tau*b for b>0. Equality remains alive. All-fit/no-split suffixes compare the integer total P<tau. This is an ordinary arithmetic identity; it does not represent a new theorem.

The production `_build_exact` uses explicit nonoverflowing widths for feasible branches and masks irrelevant modular arithmetic on overweight branches. Its active flag stops after the first fractional item; assigned prefix positions are excluded from the suffix scan. Invalid depth encodings explicitly prune. Compute-copy-uncompute returns workspace to zero on the tested clean-workspace subspace. I found no sign, equality, order, split-selection or relevant-overflow failure in the reviewed derivation/code and selected tests.

The fixed-point single-scan control is now present. It uses the same coherent scan and final integer comparison as the exact single-scan construction; this removes the initial comparison's major architecture confound. The safe fixed-point pruning decision must be distinguished from exact numerical representation of U. Both variants already avoid quantum division of unknown variable data; do not describe the comparison as removing an actually implemented variable divider from the preserved fixed-point code.

### Dual and bank predicates

For lambda=a/b>=0, reduced costs r_i=b*v_i-a*w_i, constant N0=a*W+sum(max(r_i,0)) and prefix disagreement loss L, weak duality yields b*value<=N0-L for every feasible completion. The code tests N0<L+b*tau. This is a sufficient safe rejection rule, not an iff test for the absence of a good integer completion. The equality case must remain alive, and prefix capacity rejection remains separate.

The bank ORs independently safe rejection flags, equivalent to comparing the minimum of its valid upper bounds with tau. Separate denominators avoid a common-denominator overflow/precision problem. Circuit and tree bank ordering differ but their multiplier sets agree; order does not change the predicate. Default banks are data-only, nested and deduplicated; actual bank size must accompany nominal q. A selected small bank is generally weaker than exact residual LP, so mismatch against exact LP is not necessarily an error. Its correct reference is its own Lagrangian envelope, with an independent safety check.

All item densities plus zero recover the exact fractional LP envelope, but this known dual characterization does not prove that a small bank is generally tight. Tied-density/subset-sum cases can have zero reduced costs and negligible bound-driven pruning. These are required negative regimes, not failures to hide.

### Static trees, witness recovery and certificates

The reviewed tree module uses the same exact item order, includes generated rejected children, checks leaf objective and capacity explicitly, and retains original-instance prefix losses during restricted witness calls. `structural_optimize` obtains a feasible incumbent, performs value decisions and then zero-prefix witness decisions. It does not use the separately computed optimum to choose those decisions. Capped undecided calls remain undecided. The observed small-case correctness therefore supports this classical structural implementation, not quantum execution.

The original-root certificate at target floor initial incumbent+1 covers all greater value targets and original-prefix witness subtrees; recovery when optimum equals the incumbent keeps the incumbent witness. A suffix that is re-sorted or reinitialized with a new reduced-cost budget is not automatically covered. The bound counts generated rejected leaves as specified; omitting those leaves would mismatch the current tree semantics.

The cutoff envelope is a deterministic reduced-cost counting bound. Its Python implementation uses exact integer/binomial arithmetic; O(n^3) should describe arithmetic-operation scaling, not constant-cost bit operations. Exact subset-sum counting is pseudopolynomial and cannot be silently treated as free polynomial preprocessing.

The shared root certificate is safe for banks and exact LP, but its schedules can be identical across those methods. A data-only refinement `min_j B_j`, where B_j is a valid bound for bank member j, is also safe because the bank tree is a subtree of every member tree. This is an elementary control, not a proposed original theorem. Its preprocessing and exact original-prefix/target semantics still need accounting.

## Resource-comparison requirements

1. **Architecture versus arithmetic.** Compare fixed-point and exact single scans under the same input/depth/threshold semantics. Compare exact single scan against exact depth dispatch separately. Keep ratio/gcd normalization separate. A best single-scan row versus an intentionally inefficient legacy wrapper can establish a total implementation difference but cannot isolate a division/precision contribution.
2. **One compact arithmetic control.** The current out-of-place BooleanCompiler has transparent gate lists but large workspace, even for trivial cases. Add one bounded root-dual/simple or exact-scan arithmetic control using a documented compact in-place adder/comparator, on the pilot inputs or a fixed-depth slice with matching semantics. This tests whether headline resource differences are artifacts of the compiler. It is unnecessary to optimize every family or implement a full walk before drawing a scoped circuit conclusion. Label architectural differences if the compact control has a fixed depth or classical threshold.
3. **Shared overhead sensitivity.** For weak/strong predicate costs Cw,Cs and actual tree sizes Tw>=Ts, the model `(C+h)*sqrt(T)` favours the weak predicate only when h < (sqrt(Ts/Tw)*Cs-Cw)/(1-sqrt(Ts/Tw)), if the right side is positive. If the trees have equal size, it reduces to comparing predicate costs. Report overhead ranges across CCX, total-gate and depth cost views; workspace remains a separate coordinate. This sensitivity is algebra on a model, not an executed quantum timing claim.
4. **Actual T versus certified B.** A post-hoc enumerated T proxy is not a free known input to a detector. The certified schedule should use its valid B and include certification cost. The actual-T proxy can compare potential regimes, explicitly conditional on obtaining tree-size information/adaptive search. Do not combine the favorable actual-T factor with an uncounted certificate or call it a guaranteed gate/runtime bound.
5. **Caps and paired summaries.** Retain every preselected method/input. A capped node count is a lower bound on actual T, and a failed build has unknown complete resource cost. Full-case ratios are selected-case summaries, not whole-benchmark wins. Report complete-pair denominators and class/size cap rates. When one bound is stronger, monotonic tree inclusion can supply safe inequalities, but not an invented exact ratio.
6. **Normalization.** Uniformly scaling all weights/values/capacity is an encoding-invariance control, not a hard large-coefficient generator. Dividing weights by gcd(weights) requires capacity floor division; dividing profits by gcd(values) requires ceil division of objective thresholds. In scaled inputs, L+1 and the mapped F*(Lbase+1) accept the same integer assignments but can produce different raw LP pruning unless the profit lattice is exploited. Treat these as normalization effects. Independently generated high-bit coefficients and MitM references are separate stress tests.
7. **Provenance.** Pin the circuit module, shared BooleanCompiler, tree module, registry/generator, build driver and Python version. A module-only hash is insufficient if an imported compiler changes. Report host build time separately from physical quantum execution.

## Closest primary-source comparison

- Martiel and Remaud, [Practical implementation of a quantum backtracking algorithm](https://arxiv.org/html/1908.11291v1), Sections 3–4: static/dynamic heuristic cost versus tree size, coherent depth index, constant-versus-quantum comparisons, reversible predicate cleanup and space/depth trade-offs already exist. Their graph-coloring/SAT constructions do not themselves supply this exact knapsack LP/dual-bank circuit. Candidate delta: the concrete knapsack predicate family and matched evidence, not the generic trade-off or depth register.
- Dey, Dubey and Molinaro, [Branch-and-Bound Solves Random Binary IPs in Polytime](https://arxiv.org/html/2007.15192v4), Section 3 equations (2)–(3), Theorem 3 and Section 4 equation (6): reduced-cost disagreement and counting are prior work. Theorem 3 assumes best-bound node selection for its optimization tree and states a 2*n*|G|+1 bound; it is not automatically this static threshold/recovery tree. No random-IP polynomial guarantee is imported.
- Borst et al., [On the Integrality Gap of Binary Integer Programs with Gaussian Data](https://arxiv.org/html/2012.08346v2), Theorems 1.2–1.3: strengthened reduced-cost/tree analyses have explicit algorithm/distribution assumptions. Discrete correlated benchmark classes and a source-symbol change do not satisfy those assumptions by analogy.
- Wilkening et al., [A quantum algorithm for solving 0-1 Knapsack problems](https://www.nature.com/articles/s41534-025-01097-8), npj QI 11,146 (2025): QTG, amplification/maximum finding, resource estimates and COMBO comparison already exist. Their ideal elementary gate assumptions use noiseless all-to-all gates and equal-cost rotations/Toffoli; they are not directly comparable with a physical IBM two-qubit count. A comparison needs a common cost model or explicit separate resource vectors.
- Gabbassov, Rosenberg and Scherer, [Lagrangian duality in quantum optimization: Overcoming QUBO limitations for constrained problems](https://doi.org/10.1103/53gd-2374), PRR 7,023305 (2025), Sections III–IV: circuit-model Lagrangian optimization and knapsack experiments already exist. The source constructs digitized adiabatic circuits; it is different from a deterministic clean prefix-pruning predicate. No claim of first quantum Lagrangian knapsack method is supportable. Its probabilistic Hamiltonian results are not a proof of this predicate's safety.
- Hou and Perkowski, [Quantum-based algorithm and circuit design for bounded knapsack optimization problem](https://www.rintonpress.com/xxqic20/qic-20-910/0766-0786.pdf), Sections 4–8 and 10–11: reversible decision arithmetic, constant multiplication, cleanup and gate analyses already exist. General arithmetic feasibility is not new. Exact residual fractional-LP node rejection has a different purpose from their complete-assignment feasibility/profit oracle.

These checks identify overlap and a possible distinction; they do not prove historical priority. No source theorem above is repurposed as a new theorem for this paper. A precise construction-level comparison is still required before using 'novel', 'first' or 'advantage'.

## Fit to the preserved 777-line manuscript

These are future edit locations only. The original source remains unchanged and all legitimate literature should be retained.

| Restored-source lines | Research-to-paper action after results settle |
|---|---|
| 52,69–83 | Replace uniqueness/advantage assertions with the supported construction and resource/pruning findings. Do not promise a generic small core. |
| 90–133 | Preserve the broad literature review; correct individual erroneous reference identifiers and add the closest implementation/duality papers. Compare claim by claim, not via a capability checklist that excludes real predecessors. |
| 184–195,249–305 | Repair detector/search attribution, witnessed optimization, per-call errors and known-B assumptions. Keep actual-T observations distinct from certified schedules. |
| 257–281 | Main new technical home: exact coherent LP comparison, root-dual loss/banks, register widths, cleanup semantics and scope. Replace the conflicting legacy resource table only with reproducible final tables. |
| 307–337 | Keep the complete-assignment threshold oracle separate from node pruning. Correct hardware marked-state/optimality wording and unknown-count iteration policy where relevant. |
| 339–375 | Reconstruct from a recovered core assignment; include retained-incumbent and capped/undecided branches. |
| 403–488 | Correct existing precision/counting/integer-family claims. If the certificate survives review, present it as a carefully scoped specialization with source credit. Cross multiplication alone is not the new theorem. |
| 496–566 | Add scoped circuit correctness, hierarchical bound safety and matched static-tree observations. Keep failed/capped/trivial condition counts visible. |
| 568–653 | Preserve archived classical evidence with its provenance. Add paired resource/tree summaries and overhead sensitivity. Remove circular scheduled-query regressions from evidentiary claims while retaining archives. |
| 667–731 | Preserve old hardware observations as archived/unreconciled unless job/circuit provenance is recovered. Present new IBM evidence only if actually executed. Avoid a universal NISQ boundary or mixing T gates with classical nodes as a crossover. |
| 733–775 | Rewrite conclusions and limitations around the final supported scope; complete truthful author declarations and reproduction instructions. |

## Acceptance gates for research, not a journal guarantee

**Gate 1:** final-source scoped circuit and independent reference checks have explicit zero/nonzero mismatch and dirty-workspace counts; no unsafe pruning remains unresolved. **Gate 2:** the paired benchmark and cap ledger use the same inputs/thresholds and survive normalization controls. **Gate 3:** the resource result remains explanatory against matched architecture and at least one compact arithmetic control; all limitations survive shared-overhead sensitivity. **Gate 4:** the precise delta against the primary constructions is substantial enough to state in one paragraph without 'first' by keyword absence. **Gate 5:** the old manuscript's known citation, witness, precision, metrics and provenance problems are repaired locally and adversarially reviewed before submission.

No new integrity-stop trigger was found in this selected circuit audit. The preserved manuscript's previously recorded `RESEARCH_INTEGRITY_STOP` items remain pending; none is cured by these experiments automatically. Research correctness and meaningful negative results are feasible. A substantial new result, favourable experimental outcome, external review or acceptance cannot be guaranteed.
