# Independent exact-fixing audit result

23 October 2026. Audit of `simulation/exact_knapsack.py`, source SHA256 `49680352a2223d29283b2888549b078f005409c181a38f59de98d8250e1ad774`. Source unchanged during tests. No original code, manuscript, bibliography or historical experiment record was edited.

The implemented operation is strict exact **opposite-branch LP fixing**. It computes a feasible skip-overweight efficiency-greedy incumbent L, uses the root LP whole-prefix to choose the preferred bit, and fixes only when the exact LP bound for the opposite bit is `<L` (or that bit is capacity-infeasible). The greedy witness may include later items after skipping a split item. It is not necessarily the LP whole-prefix.

The explicit containment argument in `fixing_audit_before_tests.md` supports preservation of every feasible original assignment of value>=L, and consequently all optima. Residual capacity/value offsets and original-index reconstruction give a bijection. The scope does not include assignments below L; it does not require a nonempty core or a prefix-shaped greedy witness. It does require matching n/array lengths, positive integer coefficients and nonnegative capacity; this helper does not itself validate all such API preconditions.

Independent exact vertex enumeration and integral assignment enumeration produced:

| Set | Instances | Opposite LP checks | Original assignment encodings | Threshold-set bijection checks | Failure count |
|---|---:|---:|---:|---:|---:|
| Exhaustive n=0..3, coefficients1..3, W=0..sum(weights)+1 | 6,356 | 18,504 | 48,674 | 27,962 | 0 |
| Explicit adversarial inputs | 8 | 19 | 49 | 23 | 0 |
| Seeded random n=0..8 | 300 | 1,162 | 16,751 | 946 | 0 |
| Total | 6,664 | 19,685 | 65,474 | 28,931 | 0 |

All scientific counts/reference values in this table are DERIVED exact classical enumeration. Host execution/time is MEASURED; domains and seed2026102309 are HARDCODED. These are not quantum simulation or hardware measurements. The random cases use coefficients up to1009 on one-third of trials and up to19 otherwise; all arrays and capacities are retained in `fixing_bijection_rows.jsonl`.

The check includes 4,522 empty-core cases, 1,696 all-fit cases and 297 nonprefix greedy-witness cases (DERIVED). It checks partition coverage/disjointness, exact LP values, strict fixing decisions, every original good assignment's fixed bits, reconstruction and objective preservation, incumbent consistency, residual feasibility, all optimal objective values, and threshold-set bijection. Tiny cases check every integer tau>=L through sum(values)+1; larger random cases check each distinct attainable threshold boundary and its successor, which partition all possible threshold sets. No failed/capped/trivial test case was omitted.

Two stronger statements were rejected with retained counterexamples: preservation below L fails for w=v=W=1 at tau0; replacing strict `<L` by `<=L` can discard an optimal assignment for two identical items and capacity1. These are expected counterexamples to rejected variants, not failures of the audited implementation.

Source/code description should be corrected before publication: the function invokes a separately re-sorted LP problem per tested variable, rather than a single linear pass through reduced-cost coefficients. It does not support a total O(n log n) preprocessing claim merely because the first efficiency sort has that cost. Any optimized reduced-cost replacement would be a different implementation needing its own validation.

The cached Dantzig/Pisinger primary publisher pages verify source metadata and classical background, but no numbered theorem from those abstract pages is imported into this result. This is an independent implementation audit of a standard relaxation-containment argument, not a novelty claim.

Full raw scope, counts, hashes and rejected-variant counterexamples are in `fixing_bijection_summary.json`; the exact executable is `fixing_bijection_validation.py`. No new `RESEARCH_INTEGRITY_STOP` arose in this audit. The earlier manuscript integrity items remain separate and unresolved until the manuscript is repaired.
