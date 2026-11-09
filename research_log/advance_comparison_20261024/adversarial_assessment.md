# Adversarial assessment of a substantial advance

24 October 2026. Independent review of the completed predicate study and new common-cohort/selector diagnostics. No manuscript, production circuit, old raw result or previous summary was changed. This file distinguishes a correct internal engineering result from a demonstrated advance over an actual predecessor.

## Verdict

**A substantial cross-source performance advance has not yet been demonstrated.** The current work has real implementations, scoped correctness evidence, and useful internal resource/pruning results. Its strongest numerical improvements are comparisons among constructions implemented in this project. None is presently a verified head-to-head improvement over the released Wilkening implementation, Hou–Perkowski's decision circuit, or another optimized implementation of the same prefix-bound function.

The gains are not all artifacts: the matched fixed-point/exact single-scan comparison survives the dispatcher control, and the cheaper dual/exact ordering survives a separate fixed-depth compact arithmetic control. However, the largest ratio is mainly architectural, the fixed-point baseline is a sufficient worst-case precision construction rather than a best-known implementation, and the compact control covers a limited slice. These facts support a candid construction study; they do not establish priority or substantial superiority over the closest published implementation.

## What each observed gain actually establishes

All ratios below are DERIVED from the saved compiled gate lists; they are not hardware measurements.

| Observation on original inputs | What it establishes | Main remaining adversarial concern |
|---|---|---|
| Median exact-single/exact-wrapper CCX ratio about0.059 on105 preselected inputs | Single coherent scan avoids substantial depth-dispatch work in our wrapper | The wrapper computes multiple depth-specific circuits; this is not evidence of a new pruning algorithm or superiority over a predecessor already using a direct depth index. Martiel–Remaud already discusses coherent indexing. |
| Median exact-single/fixed-point-single CCX ratio about0.546 on700 inputs | An exact rational representation can be cheaper than this safe fixed-point construction with the same scan architecture | Both baselines are ours; the fixed-point construction uses a uniform sufficient precision bound. Need normalization and simple exact-efficiency/dyadic controls before calling this an arithmetic advance over strong alternatives. |
| Median root-dual/exact-single CCX ratio about0.142 on700 inputs | This weaker predicate costs less coherently in our compiler | The functions differ: less pruning is exchanged for cheaper arithmetic. Predicate cost alone cannot show better search or a source-level algorithmic advance. |
| Compact root/exact controls retain the cheaper-dual ordering on five n12,d6 classes | The qualitative ordering is not confined to the out-of-place compiler | This is a small fixed-depth control, not a700-input compact coherent-depth implementation; simple Cuccaro Section2 arithmetic is not the optimized published Section3 variant. |
| Shared-overhead curves reverse method rankings | The cost/pruning trade-off matters in the chosen model | The generic trade-off is already prior work. Much of the reversal follows algebraically from tree/cost ratios; it is not an independently executed quantum speedup. |

The out-of-place compiler is transparent and valid, but it carries numerous intermediate Boolean values until global uncomputation. The compact implementation's large workspace reduction and increased depth expose a different resource frontier. Thus no single scalar improvement should be advertised as a compiler-independent reduction or lower bound.

## Closest source obligations

### Wilkening et al., published article and Supplementary F.2

The primary [2025 article](https://doi.org/10.1038/s41534-025-01097-8) already benchmarks quantum knapsack branch-and-bound. [Published supplementary F.2](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41534-025-01097-8/MediaObjects/41534_2025_1097_MOESM1_ESM.pdf) explicitly uses the fractional-greedy upper bound. Its closing paragraph refers to QTG arithmetic cycle calculations for implementing it. Sections E.3–E.5 cover constant QFT addition/subtraction/comparison and resource optimizations.

There is no fully specified cross-product LP-prefix gate list in F.2, but absence of our exact gate listing is not absence of LP-QBnB or resource analysis. In particular, **the source does not establish that its implementation uses a quantum variable divider**. We cannot claim to remove such a divider without identifying it in code. The preserved fixed-point construction also already compiles item efficiencies classically, so a similar divider claim is false for that baseline.

The article's Code/Data availability points to [Zenodo10.5281/zenodo.16895828](https://doi.org/10.5281/zenodo.16895828). Inspect that versioned author artifact before labelling any reconstructed baseline 'the Wilkening implementation'. If it exposes only resource formulas for this subsection, label a new circuit as an author-defined reconstruction from the published arithmetic, and state its choices.

Their ideal model treats single-qubit gates, singly controlled rotations and Toffoli gates as equal-cost elementary operations with all-to-all connectivity. Our CCX counts cannot be compared directly to their QFT cycles or treated as physical costs. A common cost/interface/accuracy model is necessary.

### Martiel–Remaud; Hou–Perkowski; Lagrangian precedents

- [Martiel and Remaud](https://arxiv.org/html/1908.11291v1), Sections3–4, already explicitly compare heuristic evaluation overhead with tree-size reduction, use a quantum depth index, and discuss workspace/depth trade-offs. The new claim cannot be the generic need to balance heuristic cost and tree size.
- [Hou and Perkowski](https://www.rintonpress.com/xxqic20/qic-20-910/0766-0786.pdf), Sections4–8 and10–11, already provide reversible complete-assignment feasibility/profit arithmetic, constant multiplication, cleanup and gate estimates. It is a useful kernel baseline; it is **not the same function** as a residual LP prefix bound. Claim superiority only on genuinely matched operations or account for the additional function.
- [Gabbassov, Rosenberg and Scherer](https://doi.org/10.1103/53gd-2374), Sections III–IV, already study circuit-model Lagrangian optimization and knapsack. Their digitized adiabatic construction differs from a safe deterministic prefix-pruning predicate; this distinction is legitimate, but 'first quantum Lagrangian knapsack' is unsupported.
- [Dey–Dubey–Molinaro](https://arxiv.org/html/2007.15192v4), Section3/Theorem3 and Section4, already connect reduced-cost disagreement to tree counts. Their best-bound optimization tree theorem is not our static threshold tree. Our direct specialization can clarify correct accounting, but does not create a new duality or reduced-cost principle.

These source comparisons identify possible narrower implementation differences, not proof of historical novelty. No theorem or complexity claim from these papers is imported without its assumptions.

## Bounded, testable fair-baseline obligations

1. **One source-faithful head-to-head kernel or predicate.** Inspect and pin the author artifact; identify an actual adder/comparison/fractional-bound kernel that can be recreated faithfully. Implement it and our alternative on identical tiny and medium fixed-depth interfaces first. Both need the same quantum/classical inputs, threshold domain, clean-output semantics, error allowance and ordering. A small faithful test is feasible; reproducing a full industrial optimizer should not become a prerequisite for every claim.
2. **Common gate accounting.** Compile both circuits to a declared common logical basis and report gate classes, depth and workspace. If arbitrary rotations remain, report them separately or synthesize them at the same stated global accuracy. Do not equate rotation counts, CCX, T gates, cycles, physical seconds or classical nodes. A direct T-cost claim requires a verified synthesis/error model; omit it if that mapping is unresolved.
3. **A competent same-function baseline.** Exploit data-only gcd normalization, profit-lattice threshold tightening, all-fit/zero-capacity constants, and known exact/dyadic efficiencies consistently. On a subset-sum instance all efficiencies are exactly1; forcing the general worst-case fixed-point precision is needlessly conservative. Keep the uniform-precision result as a documented baseline, not 'the necessary quantum cost'. Compare a compact exact-rational scan with a comparably engineered exact alternative where feasible.
4. **Separate architectural factors.** Keep fixed depth versus coherent depth, dispatch versus single scan, ratio normalization and arithmetic family as separate ablations. A fixed-depth compact circuit cannot replace a coherent-depth circuit in a whole-tree resource table without constructing/counting the missing dispatcher or direct coherent scan.
5. **Same-cohort pruning comparison, with the simple bound.** Compare all intended methods on exactly the same complete conditions; report the reduced denominator and all censored conditions. A small bank's lower median on a different easier cohort is not a portfolio advantage. Show resource-vector/model Pareto points, not just comparisons to the strongest and most expensive bound.
6. **Do not substitute optimized BnB trees.** Current trees branch to full assignments and mark leaves only. A source solver can terminate at a provably feasible integral LP completion, exploit all-fit suffixes, change variable order or update incumbents. If comparing tree sizes to that solver, align these semantics or explicitly study both. Integer LP *objective value* does not itself imply an integral LP solution; do not add unsafe early termination merely because a fractional bound happens to be an integer.
7. **Source-level acceptance gate.** Before calling the outcome a substantial implementation advance, obtain a non-dominated same-function resource result against a faithful and competently optimized baseline on more than one size/bit-width regime, and explain the mechanism beyond a generic dispatcher optimization. A useful negative result is a reproducible bottleneck or a demonstrated limitation of a claimed source cost model; failing to beat a straw baseline does not become publishable novelty automatically.

No result here guarantees those tests will show superiority. Their value is that a failed comparison can decisively narrow the claim before rewriting the paper.

## Common-cohort diagnostic: independently audited

`reviewer_common_cohort_audit.py` independently reconstructs every selected condition, normalized model ratio, hindsight winner, summary statistic and coverage count. Result:56,265 condition rows,240 summary groups and16 coverage groups checked;0 mismatches (DERIVED ledger/model verification). All source hashes matched. Detail: `reviewer_common_cohort_audit_result.json`.

On the492 identical complete original incumbent+1 conditions for the **four-member dual family**, h=0 has384 unique root-dual winners,107 bank2 winners and1 tie. At h=Cexact the winners are43 root,219 bank2,79 bank4,111 exact LP, with40 ties. These are hindsight optima of the declared model, **not deployable selection decisions**.

When the cheap simple bound is included, the matched original cohort shrinks to371 conditions. At h=0 the unique winners are245 root,81 simple and45 bank2; at h=Cexact they are31 root,68 simple,161 bank2,56 bank4 and55 exact LP, with0 ties. The two cohort denominators must never be mixed when asserting which portfolio member wins more often. Neither cohort represents all700 hard/unresolved conditions.

This closes a real comparison weakness and shows that several methods can occupy model-favourable regimes. It still compares our internal constructions, not a released predecessor, and it does not supply a deployable selector.

## Certificate-only selector: useful negative outcome

The separately predeclared rule minimizes `(C_j+h)*sqrt(B_j)` using only compiled cost, the supplied threshold and a valid input-derived certificate. It reads no observed tree size to select. This is a standard upper-bound minimization principle, not a new algorithmic theorem. The formal fact that its chosen proxy is no larger than the other supplied certificate proxies is tautological; actual tree work can rank differently because B can be loose.

I independently recomputed the selection using exact rational squared keys `(C_j+h)^2*B_j`, eliminating square-root/float tie ambiguity. All31,605 selector rows and120 summary groups match, with0 discrepancies (DERIVED verification). Source/timing accounting matched the corrected schema; result is `reviewer_selector_audit_result.json`.

On the492 complete original incumbent+1 CCX conditions, h=10*Cexact selects root462 times,bank2 seventeen times,bank4 thirteen times,and exact LP zero times. Its median observed-tree proxy ratio to always-exact is1.5413205151822835 and median hindsight regret is1.547982629700397. At h=Cexact, the median ratio is0.9644825822698595, which is not the best fixed portfolio-member median on that same cohort. This falsifies the easy hope that these cheap certificates automatically turn the observed portfolio into a strong practical selection policy.

The mechanism is transparent: exact LP and bank4 share the same supplied certificate, while exact LP has the larger compiled predicate cost. The selector cannot see exact LP's additional actual pruning and therefore can reject the method that becomes favourable when common overhead is large. This is conservative-certificate bias, not incorrect pruning. It provides a useful limitation to report; it is not evidence of a better quantum optimizer.

Recorded certificate setup now sums the separately executed bank1+bank2+bank4 host timings. A four-member reuse timing is separately labelled as a prospective reuse control. Compiling all candidate costs also has a classical setup cost; gate proxies do not include physical time for it. A first reviewer run met the parent's changing timing schema and stopped with KeyError; after the schema was finalized, the read-only audit was rerun and passed. No scientific result was altered to repair that audit failure.

## Research decision

The completed work demonstrates **correct scoped constructions and internal regimes**, and now explicitly demonstrates a limitation of a cheap certificate selector. It does **not** yet demonstrate a substantial performance advance over the closest actual published implementation. The next honest decision point is a bounded common-interface source-faithful comparison, not adding game theory, hardware decoration, or another broad novelty claim. Keep the current negative results and the original paper unchanged until that comparison resolves the intended contribution.
