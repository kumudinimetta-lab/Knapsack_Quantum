# Quantum Information Processing: revision and submission guide

Checked 26 October 2026 against official journal and publisher pages. Working document for this project; not a submission confirmation. Journal-specific instructions take precedence over the universal template. Items marked OPEN need resolution; proposed editorial choices are not journal mandates.

## 1. Submission route and scope

Our proposed category is **Regular Article**. The reversible quantum-oracle work fits the journal's quantum-algorithm/computer-science scope; scope fit does not establish sufficient novelty or acceptance. Letters have a higher innovation emphasis, so they are not our default. [QIP scope](https://link.springer.com/journal/11128/aims-and-scope).

Use the live **Submit your manuscript** link on the [QIP homepage](https://link.springer.com/journal/11128), which currently points to Springer Nature's submission service. Do not rely on an old Editorial Manager bookmark. Portal-only fields, upload limits and declarations must be checked in the actual submission session; they have not been inspected behind login.

## 2. Compact journal rule sheet

This is a compact factual index; the linked official sections contain the full instructions and examples. [QIP submission guidelines](https://link.springer.com/journal/11128/submission-guidelines).

| Area | Rule |
|---|---|
| Article | Regular: arbitrary length; single-blind review |
| Delivery | Editable sources, styles, figures and compiled PDF; LaTeX preferred; Word accepted |
| Front matter | Title; authors; affiliations; corresponding-author contacts; ORCIDs if available |
| Abstract | Conflicting limits: 80–100 versus 150–250 words; no undefined abbreviations/references |
| Keywords | 4–6 |
| Headings | Decimal; at most three levels |
| Notation | Define abbreviations; SI units; standard mathematical typography |
| Notes | Footnotes, not endnotes; table notes below tables |
| References | Square-bracket numbers; consecutive list; DOI links; cited works only |
| Tables/figures | Arabic numbering; sequential mentions; captions; reused-material attribution/permissions |
| Artwork | Embedded fonts; lines ≥0.1 mm; raster line/halftone/combination ≥1200/300/600 dpi; RGB; legible lettering |
| Accessibility | Descriptive captions; distinguishable patterns; lettering contrast ≥4.5:1 |
| Supplements | Standard formats; file metadata/captions; manuscript citations; Online Resource numbering; PDF text; CSV/XLSX data |
| Declarations | Funding; interests; contributions; data/code; applicable ethics/consent |
| Interface | Contributions and interests supplied there; funding disclosed |
| Integrity | Originality; no simultaneous submission; coauthor approval; accurate evidence |
| Proofs | Correct production errors; substantial changes need editorial agreement |

### Matters requiring interpretation

**Abstract length: OPEN.** The two limits appear under different sections of the same guideline page; neither is labelled obsolete. Prepare a short version and a longer version from the final verified results, then resolve the applicable limit through the portal or [journal support](https://link.springer.com/journal/11128/contact-the-journal) before submission. Do not present a preference as a verified rule.

**Contributions.** Populate truthful per-author roles in the portal. Put a matching contribution statement in our manuscript as a project decision. A generic claim that everyone did everything is inappropriate without author confirmation.

**Preprints.** The general [Springer journal policy](https://link.springer.com/brands/springer/journal-policies#Preprint-sharing) explicitly permits reference-list citations to identifiable preprints. Accordingly, retain real arXiv sources with clear preprint labels and prefer verified published versions when available. Do not delete Cuccaro, Draper or another genuine source merely because it is a preprint. Disclose any preprint of our own manuscript and update its publication link if accepted.

**Acknowledgments and declarations placement.** Follow the journal's linked Acknowledgments and Summary-of-requirements sections when building the title/back matter. Keep the same funding and author facts across the PDF and portal; do not assume one automatically supplies the other. Placement conflicts with the universal sample should be logged rather than silently ignored.

## 3. LaTeX implementation decision

Use the downloaded official Springer journal package, not the IEEE conference template or a Springer conference-proceedings package. The existing file named `windows_latex_template` contains a conference template and must not determine this journal submission.

Proposed review configuration, based on the official package's manual and sample:

```latex
\documentclass[referee,lineno,pdflatex,sn-mathphys-num]{sn-jnl}
```

Here `sn-mathphys-num` selects numbered mathematical/physical-science references; `referee` supplies the manual's review spacing; `lineno` is our optional reviewer aid. Single-column is the package default. The manual distinguishes review layout from final production layout. It recommends semantic markup, standard fonts, few extra packages, one main `.tex` file and flat figure paths. [Official template/support page](https://www.springernature.com/gp/authors/campaigns/latex-author-support); the downloaded package and manual are indexed in `research_log/qip_submission_20261026/`.

**Margins:** retain the class defaults. No separately prescribed numerical QIP margin was found. Do not add `geometry`, squeeze the text block, shrink fonts or insert repeated negative spacing to mimic a published article. Wide whitespace in a review PDF can be a template effect; it is not evidence of a QIP-specific border measurement.

The manual mentions EPS in a generic LaTeX passage, while the selected build uses pdfLaTeX. Our technical choice is vector PDF for plots, with a successful clean pdfLaTeX compilation as the compatibility check. Keep original vector files too; do not claim QIP mandates PDF rather than its listed preferred artwork formats. Recheck the portal's accepted figure files.

Migration tasks for our source:

- Replace IEEE author blocks and ordinal labels with `\author`, `\affil` and corresponding-author markup.
- Replace the IEEE keyword environment with `\keywords`; build the abstract from verified findings.
- Remove the separate `cite` package if it conflicts with the class's citation handling. Use the template's numbered bibliography style and inspect rendered DOI links.
- Use numbered theorem/lemma/proposition environments and explicit proofs; retain exact source assumptions in theorem attributions.
- Adapt two-column `table*` layouts to the selected single-column document. Fix the existing bounding-oracle table overflow instead of scaling its text until unreadable.
- Use decimal section numbering, ordinary equations/labels and normal cross-references. Recheck every section/table/equation reference after restructuring.
- Flatten only the submission bundle's figure paths. Keep the research workspace and evidence hierarchy intact.

These are implementation choices for our paper, not additional journal requirements.

## 4. Full-rule navigation index

The official guideline page was inspected across all its substantive sections. Use its live Contents links for: Types of papers; Single-blind peer review; Manuscript Submission and permissions/source files; Title Page; Text; Scientific style; References; Tables; Artwork; Supplementary Information; Ethical Responsibilities; Authorship principles; Compliance with Ethical Standards; Competing Interests; Editing Services; After acceptance; Research Data Policy; Open Choice. [Complete authoritative rule page](https://link.springer.com/journal/11128/submission-guidelines).

For detailed figure-size classes, caption punctuation/lettering, print-color conditions, supplementary naming and multimedia parameters, use the Artwork and Supplementary sections directly when those assets are finalized. Do not guess whether QIP's production size is the universal page's large- or small-journal case. Size our plots to the actual template text width and preserve legibility. Our paper currently needs plots, tables and computational supplements; video/clinical/animal rules are conditional, not extra experiments we need to perform.

The publisher also provides [figure/table checks](https://link.springer.com/pre-submission/figures-and-tables?journalId=11128) and a [submission preparation checklist](https://link.springer.com/pre-submission?journalId=11128). Table units, readable labels, adequate spacing and caption/text consistency are useful final checks.

## 5. Data, code, AI and authorship

Use the [journal's data-policy section](https://link.springer.com/journal/11128/submission-guidelines#Instructions%20for%20Authors_Research%20Data%20Policy%20and%20Data%20Availability%20Statements) and the linked [publisher data policy](https://www.springernature.com/gp/authors/research-data-policy). Data availability is required for original research; repository sharing is encouraged.

Our implementation plan is a versioned release containing the code that actually generated the retained tables, raw result ledgers, instance IDs/seeds, environments, commands, failures/caps and a manifest. Freeze it after final checks. A public DOI is desirable for persistence, but do not invent one or claim that an unpublished local directory is public. Verify the currently claimed GitHub address and the precise release contents before writing the availability statement.

The [general AI policy](https://link.springer.com/brands/springer/journal-policies#Artificial-intelligence-(AI)) retains human accountability, requires transparent use, and distinguishes assistance from replacing scholarly judgment. Our work has involved AI assistance beyond surface proofreading. The declaration should identify the tools, purposes, affected research/code/writing tasks and the checks actually completed. It must not falsely claim the human authors independently verified everything. Human authors need to understand and approve the mathematical reasoning, implementation and interpretation. Do not list an AI system as an author. [Research-use guidance](https://www.springernature.com/gp/policies/editorial-policies/using-ai-in-research) and [writing guidance](https://www.springernature.com/gp/policies/editorial-policies/ai-manuscript-preparation) provide the current detailed framework.

The journal's copyediting exception does not describe this project's broader assistance. The current publisher-wide guidance is also broader about disclosure than that exception. A truthful full disclosure avoids relying on the narrow exception. Graphs should be generated from the recorded outputs; any AI-assisted visual processing must remain traceable to source evidence.

For authorship, establish real individual contributions and approval of the final version. Madhavi was previously suggested tentatively as corresponding author; that remains unconfirmed. Preserve the current author order until the authors settle it. Do not infer equal contribution, supervisory roles, funding or conflict declarations from names or affiliation.

## 6. Author facts still needed

| Fact | Current status | Action before submission |
|---|---|---|
| Full names and order | Seven names exist in the draft | Confirm exact spelling/order with every author |
| Corresponding author | Madhavi A. suggested, not definitive | Confirm responsibility and active email/contact details |
| Affiliations | VNR VJIET in draft | Confirm department, formal institution/address and any changed affiliation |
| ORCID | Not established | Supply existing IDs; do not invent IDs |
| Contributions | Not supplied | Provide truthful roles for each of the seven authors |
| Funding/in-kind support | Not established | Confirm grants, institutional support and computational resources |
| Competing interests | Not established | Obtain every author's disclosure, including relevant editorial roles |
| Ethics/consent | Computational scope suggests not applicable | Confirm no human/animal/private-data component before final wording |
| Prior publication/preprint | Not established | Identify earlier versions, overlapping submissions and licenses |
| Final approval | Not established | All authors approve the exact PDF, names/order and declarations |

Do not submit placeholders or convert missing facts into negative declarations. Institutional affiliation is not proof that no funding was received. No author has been contacted during this step.

## 7. Current manuscript versus the target

Local inspection on 26 October: `paper/main.tex` still uses IEEEtran conference format. Its abstract contains approximately **383 whitespace-delimited source tokens**, including LaTeX tokens; this is an editing diagnostic, not a journal word count. It exceeds both posted limits. The IEEE keyword list contains seven comma-separated items. The references and Literature Review were revised separately, but the rest of the manuscript is still the restored older version.

| Part | Required project revision |
|---|---|
| Title | Describe the actual scoped oracle contribution; avoid suggesting a demonstrated full quantum optimizer |
| Abstract | Problem, construction, evidence, tradeoff and limits from the final ledger; choose the confirmed length |
| Introduction | Remove unsupported best-known, universal memory-barrier and uniqueness assertions |
| Literature Review | Preserve the audited revision; make only changes needed to integrate later definitions/results |
| Definitions/theory | Exact density order, certified bank coverage, capacity rejection, finite integer thresholds and workspace contract |
| Pruning statement | Preserve integer-threshold LP decisions; do not claim exact integer-completion feasibility or numerical LP reproduction |
| Algorithm/circuits | Describe actual implemented builders; remove fictitious executed divider and unrelated arithmetic layout claims |
| Complexity | Separate query complexity, logical gate counts, compilation and physical runtime; map each cited theorem's assumptions |
| Experiments | Trace every retained number to code/raw evidence; include capped, failed and trivial cases appropriately |
| Comparison | Identify reconstructed baselines and matched interfaces; report depth tradeoffs alongside width/CX changes |
| Hardware | Remove unsupported IBM execution statements; include device results only if actual job evidence exists |
| Discussion/conclusion | Scope the contribution; acknowledge open priority and implementation limits without guarantees |
| Availability/acknowledgments | Actual public release and actual support only; no fabricated repository or IBM acknowledgment |

The evidence baseline is `research_log/claim_validation_20261025/VALIDATION_VERDICT.md`. The remaining claim/citation holds are in `research_log/references_literature_20261026/FINAL_AUDIT.md`. These project findings, not formatting compliance, determine what we can honestly claim.

## 8. Proposed article organization

This is our editorial plan, not a fixed QIP section template:

1. Title page, abstract and keywords.
2. Introduction and scoped contribution.
3. Related work, retaining the audited literature review.
4. Problem, LP predicate and computational model.
5. Certified affine-bank construction and correctness, with counterexample boundaries.
6. Reversible implementation and resource accounting.
7. Reproducible experiments and fair baseline comparison.
8. Limitations, interpretation and conclusion.
9. Relevant acknowledgments, statements/declarations and data/code availability, in the journal-consistent placement.
10. References; appendices for longer derivations and supplementary pointers.

Keep essential correctness assumptions in the main article. Move repetitive tables and extended derivations only when the main contribution remains understandable. Do not hide failures or conditions in supplementary material.

## 9. Submission package and process

Our planned source bundle is:

```text
qip_submission/
  main.tex
  sn-jnl.cls
  sn-mathphys-num.bst
  references.bib
  main.bbl
  Fig1.pdf ...
```

Maintain the `.bib` as the editable master. Choose one consistent bibliography workflow for the uploaded `.tex`; do not include two competing reference lists. The exact upload packaging must match the live portal. Test the ZIP after extraction into a clean directory, with relative paths and no dependency on this machine's absolute directories. Keep build logs, caches, credentials, `node_modules`, local backups and unrelated experimental scratch files out of the submission archive.

Prepare separately: final compiled PDF; cover letter; supplementary PDFs/data with captions; a release manifest; matching portal metadata and truthful declarations. A cover letter is our recommended preparation item, not a verified universal QIP mandatory file. Reviewer suggestions are optional; if requested, use genuinely independent qualified researchers and verifiable identities. Do not fabricate names or contact details.

The cover letter should explain the exact contribution over Wilkening, Hou--Perkowski, the classical-bound hybrid work and prior multiplier methods. It should state the actual limitations and any overlapping/preprint version. Do not promise quantum advantage or claim we are first without evidence.

Workflow: complete scientific revision; compile/render; independently audit; gather author facts/approval; freeze release and files; enter portal; inspect its generated PDF and metadata; resolve OPEN items; submit the approved version. Save a confirmation/manuscript ID only after the portal actually returns one. This task has not created a submission or made publication declarations on the authors' behalf.

## 10. Fees and decisions after acceptance

QIP offers subscription publication with **no APC**, or optional open access. The posted OA price checked on this date is **GBP2190 / USD3090 / EUR2490**, excluding applicable taxes; the applicable price is determined at acceptance. Check institutional/funder coverage and licensing obligations before choosing. Paid language editing is not required and does not guarantee review or acceptance. [Official publishing options and fees](https://link.springer.com/journal/11128/how-to-publish-with-us).

Do not pay a fee, choose a paid service or accept a publication license merely to prepare this guide. Those decisions depend on the authors, funding and actual acceptance terms.

## 11. Completion gates

- [ ] Resolve the abstract-limit conflict.
- [ ] Convert and compile using the selected journal template; inspect margins without overriding the class.
- [ ] Complete the line-by-line scientific revision and resolve the existing claim/citation holds.
- [ ] Reproduce every retained result and label measured, derived and simulated quantities accurately.
- [ ] Inspect every plot/table/equation and verify source-to-claim references and DOI rendering.
- [ ] Complete author facts, contributions, funding, interests and AI-use documentation.
- [ ] Freeze and verify a real code/data release and accurate availability statement.
- [ ] Clean-build the exact submission ZIP; inspect the final PDF.
- [ ] Confirm all authors approve that exact version and its submission.
- [ ] Verify portal-only requirements and the generated submission proof.
- [ ] Submit and save actual confirmation.

Formatting cannot resolve the existing scientific issues or guarantee peer review. The guide is complete as a preparation document; the manuscript and submission gates above remain open.
