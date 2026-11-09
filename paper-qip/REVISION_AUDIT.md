# Full manuscript revision and scientific scope

27 October 2026. All edits are confined to `paper-qip`. The entire existing `paper` tree (467 files) is hash-manifested and preserved, including the previous PDF, bibliography, and figures. Copies of the previous manuscript, bibliography and PDF are also in `audit/original_*`.

## Changes and reasons

- Changed IEEE conference formatting to the supplied Springer Nature journal template, with numbered references and review spacing. Preserved the author order and email strings; Madhavi's corresponding-author designation is provisional. The title page prints the corresponding email; other contact strings remain in source comments and the original copy so the abstract stays together without changing margins.
- Replaced the title and abstract with the scoped reversible integer LP-pruning contribution. Abstract: 201 words; six keywords.
- Retained the audited literature-review prose and all 40 references. Changed its table layout for one column. Supplemented missing publisher locations from primary bibliographic sources; handled the stock BST's corruption of colon-delimited LIPIcs page identifiers by preserving the exact identifiers in a note. The official class/BST remain unchanged. See `audit/BIBLIOGRAPHY_FORMAT_CHANGES.json`.
- Replaced the old algorithm/theory sections with the fixed-prefix integer-threshold contract, dual identity, coverage criterion, grid and rational cardinality certificates, sufficient tied-group radius, linear cardinality limitation, integer arithmetic identity, width bounds and clean output semantics.
- Replaced old experiment claims and figures with auditable coverage results, explicitly scoped gate tests, the retained simulator failure, and the stronger root-aware 105-input resource comparison. Tables and the figure come from immutable raw ledgers; no raw outcomes were edited.
- Removed from the NEW manuscript the unsupported IBM hardware claims, uncertain composed quantum-query formula, inconsistent statements about synthesis of h, generic spectral-validation claims, untraced large-scale/regression headlines, and assertions of uniqueness. Their original wording and figures remain unchanged in `paper`, with a full original manuscript copy in this folder. This is not a finding that all historical spectral data are invalid; those results are outside the re-audited contribution developed here.
- Added limitations, provenance, truthful AI-assistance disclosure and pending declarations. Author contributions remain deferred at the user's request.

## Evidence-to-claim map

| Manuscript material | Evidence/source | Interpretation |
|---|---|---|
| LP contract, integer-floor criterion, root-tail lemma | `research_log/claim_validation_20261025/theory_claim_audit.md`; exact code/reference definitions | Mathematical integer/prefix contract, not rational thresholds or arbitrary branching |
| Grid, continuous and sufficient banks | `simulation/source_faithful_20261024/compressed_bank.py`, `continuous_bank.py`; preceding derivation files and theory audit | Minimum cardinality only in stated domain; sufficient constructor not actual-coverage minimum |
| Linear-cardinality family | `theory_adversarial_audit.py`, repaired family and 14 endpoint checks; fresh manuscript-indexing checks | Cardinality limitation, not search hardness |
| Loss identity and finite widths | `qft_bank.py`; `qft_bank_derivation_before_code.md` | No quantum division or efficiency truncation; supplied bank requires independent coverage |
| 5,204,456 states / 20,817,824 comparisons | `root_all_reachable_v2_rows.jsonl` and summary; separate primal reference | DERIVED arithmetic coverage, not statevector simulation |
| 1,888 inputs / 15,999 prefixes | `theory_adversarial_audit_v2.json` | Independent primal-vertex reference; overlapping checks not pooled |
| 24 QFT method-cases / 1,120 columns; Boolean 7 / 2,216 | original and resumed `circuit_vertex_adversarial` JSON, resumed summary | SIMULATED finite scope; failed initialization record retained; insufficient bank has 8 expected disagreements |
| root-aware control tests | `root_aware_validation.json`, `final_crosscheck.json` | 104 compact + 208 QFT columns and 16 coherent amplitudes; not large-circuit exhaustive testing |
| 105-input resource table and figure | `root_aware_resource105_rows.jsonl`; independently reaggregated in `assemble_evidence.py` | DERIVED u/CX netlist costs, all-to-all, fixed depth, no device timing or T synthesis |
| 40 cited works | previous complete primary-source citation audit, supplemented formatting metadata sources | Existing access limits remain recorded; no uncertain external theorem formula is quoted as established |

## Adversarial revision pass and retained mistakes

The first mathematical drafting pass incorrectly translated the saved zero-based family `4*(m-i)+1`, i=0..m-1, to a one-based formula without adding one. This moved the dummy's position and broke the drafted argument. The uncertainty was flagged before compilation; the proof was held and corrected against the saved code and derivation to `4*(m-i+1)+1`, i=1..m. The manuscript now has last main profit 5 and dummy profit 1. A separate fresh check reproduces all 14 primal/all-subset endpoint tests with zero mismatches. No research data were changed.

A source-level check also found that three named QFT fixtures use the FULL density grid plus zero, not a root-tail-selected bank. The fixture table was corrected. Error magnitudes from simulation are described as DERIVED comparisons of SIMULATED amplitudes. The new constant-comparison/width equations were separately checked on 1,376 tiny-domain combinations, with zero mismatches. These are manuscript checks and do not enlarge the published gate-test counts.

This revision's final audit is a separate pass by the same agent, not a new independent multi-agent review. The earlier recorded independent research audits remain evidence with their original scope. No universal absence-of-errors claim or guarantee of novelty/acceptance is supported.

## Remaining limitations and author decisions

The exact Aer partial-initialization implementation defect remains unresolved; independent dense/preparation evidence supports the specific oracle checks and the failed path is not trusted. Source priority, optimal-baseline performance, hardware advantage, end-to-end walk cost and editorial significance remain unestablished. Funding, competing interests, author contributions, author identity/contact confirmation, all-author approval and a public data/code release are pending. See `LATEX_SUBMISSION_CHECKLIST.md`.

The automatically generated checks in `audit/` document source preservation, arithmetic comparisons, reference linkage, abstract count, compilation and PDF layout inspection. These checks support a scientifically bounded review draft, not a submission-ready certification.
