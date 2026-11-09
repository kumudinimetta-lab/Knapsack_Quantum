# QIP LaTeX review package

Prepared 27 October 2026. This is a review draft, not a submitted manuscript.

## Files to supply for the LaTeX manuscript

- `main.tex`: one self-contained manuscript source, including editable tables; no external TeX subfiles.
- `references.bib`: all 40 audited references, all cited.
- `main.bbl`: compiled bibliography, included for submission-system compatibility.
- `sn-jnl.cls` and `sn-mathphys-num.bst`: unchanged official Springer template files.
- `resource_ratios.pdf`: vector figure generated from saved result rows, with embedded fonts.
- `integer_coverage_example.pdf` and `oracle_workflow.pdf`: explanatory vector figures.
- `main.pdf`: compiled manuscript for reading and submission-system comparison.

These are included at the top level of `qip_latex_review_bundle.zip`. The checklist itself is for author use; it need not be uploaded as an article attachment. Upload file designations and archive handling must be checked in the actual submission portal. No authenticated submission form was inspected.

The main file uses the Springer `referee` option (double-spaced review text), single-column defaults, and the numbered physical-sciences reference style. Margins and class files are not modified. Only the corresponding email is printed; other original contact strings are preserved in TeX comments and the original snapshot. Tables are in the main TeX file and remain editable. No separate table files are required to compile. The bibliography URL command is mapped to `url` for line breaking; `xurl` is used if installed. No shell escape or automatic package installation is needed by the build script.

## Rebuild

From the project root, run `python paper-qip/build_pdf.py`. This uses installed `pdflatex` and `bibtex`, a clean separate `paper-qip/build` directory, and copies the resulting PDF and BBL back here. On this Windows installation MiKTeX requires access to its normal user registry/configuration; the restricted first attempt could not read it. An approved normal-context build succeeded.

For another machine, unzip the review bundle and run `pdflatex main`, `bibtex main`, then `pdflatex main` twice. Standard packages used by the Springer class must be installed. Avoid mixing old IEEE auxiliary files with this build.

## Journal rules and author decisions

The official [QIP submission guidelines](https://link.springer.com/journal/11128/submission-guidelines) describe Regular Articles as being of arbitrary length; no page maximum is specified for this type. They request LaTeX source, style files, figures, and the compiled PDF. The current PDF's review spacing does not predict the published page count.

The abstract has 199 whitespace-delimited words and six keywords. The requested 150–250-word limit is followed. The same official page also has a conflicting 80–100-word instruction under single-blind review; that conflict remains flagged for checking before upload, not represented as resolved by our choice.

Author contributions are intentionally deferred, as requested. They are not invented or filled in the draft. The journal requires contributions and competing interests in the submission interface. The visible funding and competing-interest statements are explicitly pending. Madhavi is provisionally marked corresponding author following the user's earlier preference; this designation and every author's name, affiliation, contact, name parsing, and order still require confirmation.

Before actual submission, complete funding/interests, contributions, corresponding-author confirmation, author approval, originality/exclusivity declarations, final AI-use wording and human review, and the data/code release decision and persistent link. No unsupported 'no funding', 'no conflicts', public DOI, or author-consent declaration has been inserted. The two pending declaration sentences and pending-review wording must be replaced with author-approved facts.

The evidence directory is an internal provenance and review aid. It is not yet a complete independently runnable public software release. Source snapshots preserve their original imports and refer to the project tree. Select and package supplementary files only after checking reproducibility, licensing, and author-approved release scope; do not upload the entire internal audit folder as-is.

No manuscript has been uploaded, no journal fee or publishing license has been selected, and no acceptance claim is made.
