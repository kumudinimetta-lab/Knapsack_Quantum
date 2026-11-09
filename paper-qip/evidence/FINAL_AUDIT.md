# Bibliography and Literature Review audit

26 October 2026. Authorized revision: references and Literature Review only.

## Result

The bibliography now contains **40 real, identifiable works/artifacts, all cited**. We removed16 saved entries and added11, including every addition in the preceding plan and the newly required Balas--Zemel core-origin reference. Four optional background references remain: Bulger adaptive search, Farhi QAOA, Preskill NISQ limitations, and Thapliyal reversible division as a comparison.

The revised review was checked against primary-source material and independently reviewed in separate classical/theory and circuit/source passes. This supports its scoped descriptions, not every claim in the old manuscript. Exact full-text access limitations remain below. No source was declared nonexistent merely because its saved record could not be verified.

**The whole paper is NOT scientifically certified or ready for submission by this audit.** The unchanged introduction, theorem statements, arithmetic descriptions and claimed IBM experiments retain problems requiring the next revision stage. The new review deliberately does not endorse those assertions.

## Files and recovery

- Edited: `paper/main.tex`, Literature Review section only, and `paper/references.bib`.
- Rebuilt: `paper/main.pdf` from the clean `latex_build/` directory in this audit folder.
- Exact pre-edit copies: `paper/backups/2026-10-26_before_references_literature/`. All three original SHA256 hashes still match the manifest.
- Every removed BibTeX entry is also preserved in `removed_entries.bib`; reasons are in `CHANGE_LEDGER.json`.
- `manuscript.diff` records the exact source change. The bytes before and after the Literature Review are identical to the backup. The document class, title, authors, abstract, introduction, theory, experiments and conclusions were not edited.
- Independent source evidence: `theory_reference_audit.md/json`, `circuit_reference_audit.md/json`, `root_reference_audit.md/json`.
- Consolidated record for every remaining key, its primary-source audit and its citation locations: `COMPLETE_REFERENCE_AUDIT.json`. All citation locations are also retained in `CITATION_LOCATIONS.json`.

## Removals

| Key | Saved work | Decision |
|---|---|---|
| ref6 | Helm--May, saved ESA2021 subset-sum title | Exact record unresolved; peripheral refinement discussion omitted. The verified Helm--May2018 paper remains. |
| ref7 | Plateau--Elkihel, saved packing-tree title | Exact record unresolved; replace background discussion with verified classical core/solver sources. |
| ref10 | Long, zero-failure Grover | Real but unused variant; discussion omitted. |
| ref14 | Ambainis, element distinctness | Peripheral walk background; backtracking/B&B sources retained. |
| ref15 | Magniez et al., search via quantum walk | Generic background omitted in favor of the frameworks actually discussed. |
| ref19 | Saved Jaques--Schanck lattice-sieving title | Exact record unresolved; not silently substituted with a different real paper. |
| ref20 | Saved Shi knapsack paper | Confirmed wrong arXiv identifier2006.09838, which is music generation. Verified Hou--Perkowski supplies the constructive-knapsack comparison. |
| ref21 | Dunjko--Ge--Cirac small-device speedup | Real 3-SAT paper, wrongly treated as a knapsack solver in the old review; peripheral context omitted. |
| ref22 | Saved Patvardhan et al. quantum-search title | Exact record unresolved; do not substitute quantum-inspired evolutionary work. |
| ref27 | Saved Ajagekar--You energy title/venue/year | Peripheral discussion omitted; conflated metadata not carried forward. |
| ref28 | Saved Norambuena genetic-knapsack title | Peripheral discussion omitted; exact record unresolved. |
| ref29 | Saved Geng wolf-pack title | Peripheral discussion omitted; exact record unresolved. |
| ref30 | Saved Li harmonic-oscillator title | Peripheral discussion omitted; exact record unresolved. |
| ref32 | Bravyi--Gosset--Koenig shallow circuits | Real but unrelated separation; does not establish this oracle's advantage. |
| ref34 | Ambainis adversary lower bounds | Generic background omitted; no structured-knapsack barrier inferred. |
| martello1988mtm | Martello--Toth1988 exact knapsack solver | Real historical solver; focused MINKNAP/COMBO context retained instead. |

## Additions

| Key | Work and purpose |
|---|---|
| balas1980core | Balas--Zemel1980: correct origin of the core concept. |
| wilkening2025 | Published npj Quantum Information algorithm; QTG with amplitude amplification, plus separate fractional-bound QBnB benchmarking. |
| wilkening2025code | Version-specific Zenodo R1 software/experiment artifact, DOI10.5281/zenodo.16895828. |
| cuccaro2004 | Real ripple-carry addition preprint; arithmetic primitive. |
| dey2021random | Dey--Dubey--Molinaro random binary-IP B&B; distribution-qualified context, arXivv4. |
| bozejko2026 | D-Wave knapsack B&B and multiplier-set prior art; first online2024, assigned journal issue2026. |
| hou2020 | Complete-candidate bounded-knapsack decision circuits. |
| gabbassov2025 | Lagrangian duality in constrained quantum optimization. |
| erickson2019algorithms | Standard interval-stabbing problem; no invented theorem/exercise number. |
| hamitouche2025 | Official PRICAI workshop-report contribution; classical bound and Grover completion tests. |
| martiel2019 | Practical backtracking implementation; now cited with verified SOFSEM2020 publication metadata. |

## Important retained-record repairs

Dantzig's pages are266--288. Bonnetain et al. is ASIACRYPT2020, not EUROCRYPT, with pages633--666. Sanavio's coauthors are Edoardo Tignone and Elisa Ercolessi; the real article is Entropy26(4),345, DOI10.3390/e26040345. The old arXiv2403.09560 is a different DFT paper. Gilliam is updated to Quantum5,428(2021), the QRAM survey to Quantum9,1922(2025), and Christiansen to QCE2025. Paul J. Christiansen's initial is visible in the primary full-paper header. Montanaro article identifiers and reversible-arithmetic metadata are completed. Qiskit uses its official2024 citation instead of a generic website entry. Bernstein's verified expanded ePrint is cited explicitly rather than guessing conference-version metadata. The AMS publisher cover gives *Quantum Computation and Information* for volume305, despite the differently worded arXiv journal-reference field.

## Source-to-claim changes in the review

- Replace unsupported uniqueness/capability claims with a descriptive table of methods and scope.
- Attribute cores to Balas--Zemel, with Pisinger for capacity/distribution cautions; include MINKNAP and COMBO without implying we benchmarked them.
- Separate generic quantum query counts, classical operation counts and runtime. The black-box lower bound is not a general structured-knapsack lower bound.
- Qualify subset-sum instance/heuristic/memory assumptions; omit strongest-known and universal hardware-impossibility assertions.
- Separate Grover adaptive search from variational QAOA and acknowledge Christiansen's asymptotic optimal-sampling result.
- Separate Wilkening's QTG algorithm, its QBnB benchmarking comparison and the released simulator/resource model. Our matched LP circuit is a reconstruction, not an attributed released LP netlist.
- Credit multiplier-set bounds, integer-floor pruning, reversible arithmetic and interval stabbing as prior tools.
- Describe the candidate construction as LP-based integer-threshold pruning for a certified fixed-order bank. LP rejection does not decide actual integer-completion feasibility. No full-walk, numerical-LP reproduction, first-in-literature or hardware-advantage claim is made in the new review.

Independent reports: `theory_literature_review.md` and `literature_independent_review.md`. The substantive wording findings were corrected before the final build. Earlier review snapshots and their hashes remain in those reports; later circuit confirmation records the applied corrections.

## Access limits and unresolved claims

Primary publisher metadata and accessible abstracts/contents verify source identities. Dantzig's full article, the exact internal KPP textbook passages, and the full journal theorem in Beier were not all available. The new review uses only broad historical/method statements supported by inspected material, without inventing theorem numbers or transferring distributional guarantees. Thapliyal2016 is a real preprint; its detailed layout is not certified here. These access limits remain **UNRESOLVED** for any more specific attribution outside the revised review.

Bozejko's floor rule is visible in the cached primary PDF extraction (`.firecrawl/claim_validation_dwave_knapsack2024.md`, line802, Fig1); Eq16--20 and Section5 were freshly checked in the publisher PDF. The web screenshot of PDFpage10 failed with a cache miss, and the figure-page fallback was inaccessible. Do not misreport that screenshot as inspected. Publisher HTML alone omits the figure's floor formula. No new theorem is derived from the source's sign conventions or potential typographical errors.

Graph tools were unavailable after discovery; targeted file reads were the fallback. Firecrawl lacked usable credits; no purchase occurred. Verified cache material and primary web sources supplied the audit. Rejected URL/cache mappings are explicitly recorded in `root_reference_audit.json`.

## Outside-scope integrity holds for the next stage

**RESEARCH_INTEGRITY_STOP on certifying the following original claims.** This is the audit outcome for those claims, not an endorsement caused by fixing their references. No further experiment, theorem derivation or body edit was attempted in this bibliography/LR stage.

Locations below are current `paper/main.tex` line numbers; all citation occurrences are preserved in the machine-readable ledger.

| Lines | Citation/claim | Status and required later action |
|---|---|---|
| 61 | Horowitz--Sahni is the best classical exact algorithm | Unsupported unrestricted current-best claim; qualify the baseline. |
| 63 | Grover versus classical runtime comparison | Separate query count from oracle and classical-operation costs. |
| 65 | Blanket heuristic unsoundness and QRAQM feasibility claims | Replace with source-specific assumptions and variants. |
| 143 | Specific Dantzig closed-form attribution | Retain genuine source, but exact primary passage not inspected; full attribution remains unresolved. |
| 171 | Pisinger introduced cores | Contradicted by the verified Balas--Zemel origin. |
| 175--177 | Amplitude-amplification theorem | State measurement-free A, success probability assumptions and success/error convention. |
| 181--189,246,281 | Montanaro theorem and composed bound | Exact theorem/assumptions and implementation mapping require the next theory revision. The revised review avoids this unsupported formula. |
| 194 | Specific fixing technique is due to Pisinger1999 | Exact attribution not established from the inspected source. |
| 198 | Per-subset binary search yet O(2^(n/2)) total | Reconcile the extra factor, soft-O notation or merge implementation. |
| 258 | Thapliyal divider/VBE multiplier implemented, exact ancilla layout | Does not describe the new bank implementation; do not call this citation-backed implementation evidence. |
| 275 | Barenco three-rotation Ross--Selinger T estimate | Barenco controlled-V decomposition does not supply this synthesis/error-budget calculation. |
| 305--310 | Zero-ancilla arithmetic extrapolation | No carry ancilla for an adder does not imply zero workspace for the full predicate. |
| 477 | Blanket Heuristic2 table footnote | Restrict to the algorithm/assumptions actually criticized. |
| 496 | Benchmark distributions attributed to KPP | Exact generator/class mapping must be checked against code in the later methods audit. |
| 697 | Heron hardware boundary supported by Preskill | No source support for project-specific executions; verified project record has no such IBM jobs. |
| 702 | Newly measured T-count and VBE citation | Logical/derived resources are not hardware measurements; rewrite using the validated ledger. |

Additional non-citation problems remain in the original abstract, contributions, hardware discussion, data-availability statement and conclusion. For example, the unchanged source simultaneously claims a synthesized m=4 LP oracle and says h is not synthesized. The current research checkpoint is `research_log/claim_validation_20261025/VALIDATION_VERDICT.md`; the body must be reconciled with that evidence in the next stage. The bibliography cannot supply missing experiments or repair those contradictions.

## Verification

Document-inventory counts are **DERIVED**, not scientific measurements:40 entries,40 distinct cited keys,0 missing keys,0 uncited entries,0 duplicate keys,40 source-audit records. Every retained source is used in the new review. All11 planned additions are present. Three original backup hashes match. Bytes outside the Literature Review are unchanged.

Five final build passes succeeded; BibTeX warnings0, undefined citations0, undefined references0, no remaining cross-reference rerun warning. The compiled PDF has13 pages. Pages2--4 (review and related-work table) and12--13 (references) were rendered and visually inspected: no clipping or overlap in the revised material. The untouched bounding-oracle table still produces a33.33115pt overflow warning; a float placement is adjusted by LaTeX. Those old-body layout issues are recorded rather than silently changing other sections.

No code, raw data or experiment results were altered. No new experiment or quantitative advantage result was produced. Compilation and source-identity checks do not establish novelty, scientific validity of untouched sections, or likelihood of journal acceptance.

See `FINAL_CHECKS.json` for final source/PDF hashes and reproducible checks, `BUILD_RESULTS.json` for compiler results, and `BUILD_ATTEMPTS.md` for the failed initial build attempts and clean-build resolution.
