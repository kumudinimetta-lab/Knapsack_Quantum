# What advance is demonstrated?

24 October 2026. Additional source audit and controlled analysis requested by the user. No manuscript, bibliography, old raw data or prior checkpoint was changed.

## Verdict

The present evidence demonstrates an explicit reversible construction family and reproducible internal resource/pruning differences. It does **not yet demonstrate superior performance over the closest authors' implementation under a shared cost model**, establish global priority, or determine that journal editors will regard the advance as substantial. These are separate questions. More correctness test counts alone cannot close the latter gaps.

The largest dispatch improvement (single scan versus the earlier depth wrapper) is an architectural control, not the headline new algorithm. The exact-versus-fixed-point single-scan result and dual-versus-LP result survive matched architecture, and the five-case compact arithmetic control supports a real construction-level difference. Neither compiler is best-known arithmetic. Prior LP-QBnB, arithmetic networks and generic pruning-cost tradeoffs must be credited.

## Stronger same-cohort test

Previous per-method descriptive summaries correctly used their own complete-pair denominators. Those summaries cannot by themselves rank every portfolio method on a single shared cohort. `common_cohort.py` now uses identical inputs, thresholds, costs and completed tree conditions for all compared candidates. Capped and classically resolved conditions remain in an exclusion ledger. Results are DERIVED conditional work proxies; tree sizes are MEASURED classical enumerations, not executed quantum queries.

For the 492 original initial-incumbent+1 conditions where root dual, bank2, bank4 and exact LP all have complete resource/tree records and require detection:

| Shared overhead | Unique root-dual wins | Unique bank2 wins | Unique bank4 wins | Unique exact-LP wins | Tied conditions |
|---|---:|---:|---:|---:|---:|
| 0 | 384 | 107 | 0 | 0 | 1 |
| Exact-LP predicate cost | 43 | 219 | 79 | 111 | 40 |
| Ten times exact-LP predicate cost | 8 | 22 | 56 | 366 | 40 |

Metric: (predicate CCX cost + common overhead) * sqrt(observed full tree size). Winner labels use observed T after the fact. They do not define a deployable selection algorithm. The selected overheads are HARDCODED model sensitivities, not measured walk costs or physical timings. These cases are a complete-case subset of 700 inputs, not the entire benchmark.

Including the simple profit-only control gives a stricter 371-condition common cohort. At zero shared overhead its unique winners are root dual 245, profit only 81, and bank2 45. Thus the four-method counts above cannot be advertised as wins over every cheap alternative. This important control prevents overstating the portfolio's value.

## Attempt to eliminate hindsight: negative result

After deriving a data-only rule, `certificate_selector.py` selected a method by minimizing (C+h)*sqrt(B), using compiled C and valid cheap upper certificate B, never observed T. Only evaluation uses T. The certificate upper bounds remain safe, but need not rank methods accurately.

On the same 492 conditions at overhead ten times exact-LP predicate cost, the rule chooses root dual on 462, bank2 on 17 and bank4 on 13, and never chooses exact LP. Its median observed-tree proxy is **1.541 times always-exact LP**, worse than that baseline. Median regret relative to hindsight selection is 1.548; maximum is 4.942. This is a retained unfavorable result, not a practical improvement claim.

Reason: the valid certificate supplied to exact LP is the same four-member upper bound available to bank4. Because exact LP costs more, this certificate model cannot recognize its stronger actual pruning. Cheap valid bounds on T do not automatically supply a useful policy. This simple selector cannot be presented as a substantial new optimization algorithm. Candidate compilation and certificate preprocessing are additional classical setup, recorded separately and excluded from quantum gate units.

## Closest implementation comparison

The primary source and release audit is `source_implementation_audit.md`; its pinned artifact and function-level mapping are the authority for implementation details. The existing published-supplement comparison is `../pruning_study_20261023/WILKENING_SUPPLEMENT_OVERLAP.md`.

The paper-linked Zenodo R1 archive was downloaded and its published MD5 verified. The audited call path is evaluation script 04 -> `execute_qbnb` (including a COMBO optimum reference) -> classical `branch_and_bound` / `bnb_greedy` -> scalar quantum resource estimation and a dyadic sqrt(T*n) schedule. No complete clean LP-pruning gate-list interface was found in this audited path; the authors do provide real simulator/estimator code and published QFT arithmetic designs. Our explicit clean predicate artifact is an implementation-level difference. It is not a verified performance win. Their tree counter and our root-plus-rejected-children counter also differ, so raw T values are not interchangeable. The archive and selected source hashes are recorded in `qtg_R1_source_manifest.json`; no upstream build was attempted.

Wilkening et al. already include fractional-greedy LP pruning in quantum BnB estimates. Their QFT arithmetic/cycle conventions and our X/CX/CCX networks do not share a cost model. It is invalid to call our 14.2% internal median CCX ratio a speedup over that paper, to invent an expensive variable divider as their baseline, or to infer that an implementation is absent merely because no matching circuit is described in one subsection. The source archive is inspected explicitly to distinguish the authors' simulator, resource estimator and any actual gate construction.

## What would close the substantive-advance gap

1. A source-faithful comparison on a matching node-pruning interface: same input/threshold/depth semantics, correctness/error budget, uncomputation, arithmetic precision and logical gate accounting. Start with a small fixed-depth reference before allocating a large benchmark. If the source only supplies cycle estimates, label a reconstruction as a reconstruction and document every added choice.
2. Demonstrate a construction/resource benefit that survives this comparison and a justified allowance for marking, branching and reflections. A hypothetical zero-overhead advantage is insufficient for an end-to-end claim. A full optimized quantum computer implementation is not a universal journal requirement, but the omitted costs cannot be treated as zero evidence.
3. Either supply an input-only policy that realizes a useful portfolio regime, or present the portfolio explicitly as a resource landscape with hindsight choices. The tested cheap-certificate policy fails in an important regime; do not silently substitute the hindsight winner.

These obligations identify concrete evidence to obtain; they do not promise a favorable outcome. A narrow construction/resource paper may still be worthwhile. Current evidence does not justify asserting that a substantial cross-source advance has already been established or that QIP desk rejection is resolved.

## Reproducibility

`PROTOCOL.md` and `SELECTOR_DERIVATION.md` precede the new computations. `common_cohort_results.json` and `certificate_selector_results.json` pin their inputs; per-condition outputs are retained. Independent adversarial review and a separate recomputation audit are saved in this directory. All prior study outputs and the 24 October checkpoint remain intact. No empirical regression was performed on a dependent variable calculated from its predictor.
