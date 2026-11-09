# Resume after this research milestone

Read `RESEARCH_ADVANCE_RESULTS.md` first, then `theory_construction_results.md`, the final QFT bank resource report, and `independent_new_controls_review.md` with its final audit appendices. Raw data and failed attempts are retained here. `ROOT_RUN_LOG.md` records integration failures and important scope restrictions.

The paper remains byte-identical to the restored 22 October backup, including 45 bibliography entries. Do not delete legitimate citations because they were not yet checked. Wrong citations need explicit repair. Original line audit: `research_log/RESTORED_PAPER_LINE_AUDIT_2026-10-23.csv`.

The candidate contribution is the all-prefix, all-integer-threshold LP-pruning compiler under static density order, reversible implementations, and scoped resource tradeoffs. Differentiate exact LP values from exact integer rejection. Minimum bank cardinality is not minimum gate cost. Capacity-DP preprocessing can cost more than solving the test inputs. DP-free banks avoid that barrier but offer no universal resource win. Global novelty/priority is UNRESOLVED; no guarantee of QIP acceptance is supported.

Completed new ledgers: 700 originals + 700 cores under four scan/bank families and 45 independent DP-free banks; exact sample-column and ledger counts are in the synthesis. The final 105-input same-engine QFT comparison has 840 resource-only rows with raw/cancelled forms and two control policies. Tiny phase-sensitive simulation is distinct from large resource compilation. No IBM device or full quantum walk was run.

Next manuscript pass should use the existing line audit, repair theorem/witness/spectral/schedule/citation errors, and rebuild the bounding-oracle and experimental sections around only verified results. Preserve author declarations pending actual facts. No need for more broad experiment sweeps without a specific unresolved scientific question. Global historical-priority review and any full-walk/runtime claim are separate unfinished work, not conclusions licensed by this checkpoint.

Reproduce the final aggregates from the project root with:

```
python research_log/source_faithful_20261024/analyze_compilation_extended.py
python research_log/source_faithful_20261024/analyze_qft_bank_resources.py --help
python research_log/source_faithful_20261024/make_research_figure.py
```

Inspect the QFT analyzer's arguments before running it; it supports multiple pilot/full cohorts. Existing analyses and manifests contain exact command scopes and hashes. Avoid rerunning drivers into preserved raw files. New runs should have distinct output paths and manifests.

The 25 October checkpoint contains this phase, simulation sources, unchanged paper source/bibliography/PDF, and the two hash-verified preceding checkpoints. Archive integrity and every member hash are checked by `save_checkpoint.py`; verification output is beside the ZIP.
