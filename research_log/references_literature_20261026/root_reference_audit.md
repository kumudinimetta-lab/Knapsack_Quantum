# Root primary-source audit

26 October 2026. Identity and scoped literature-use checks, not whole-paper correctness.

## ref8

[Primary source](https://arxiv.org/abs/quant-ph/9605043). Original STOC paper/abstract; ACM DOI10.1145/237814.237866.

Supports: Unstructured quantum search query scaling.

Limits: Query count excludes reversible implementation cost; not a structured knapsack lower bound.

## ref9

[Primary source](https://arxiv.org/html/quant-ph/9701001v1). Section3.1 and Theorem3.5.

Supports: Black-box and random-oracle lower-bound context.

Limits: Theorem3.5 concerns random-oracle NP and time o(2^(n/2)); it does not rule out structure-exploiting knapsack algorithms.

## ref11

[Primary source](https://arxiv.org/html/quant-ph/0005055v1). Section2, Theorem3; arXiv journal reference/related DOI; AMS volume305 cover.

Supports: Amplitude amplification using A and its inverse.

Limits: Theorem3 assumes measurement-free A, success probability a>0; expected O(1/sqrt(a)); zero-solution handling requires more than that statement. Publisher cover gives Quantum Computation and Information despite arXiv journal-reference title discrepancy.

## ref12

[Primary source](https://www.math.canterbury.ac.nz/research/ucdms2000n10.pdf). Author technical-report abstract; author-institution published record https://researchers.mq.edu.au/en/publications/implementing-pure-adaptive-search-with-grovers-quantum-algorithm/.

Supports: Grover-based implementation of pure adaptive search.

Limits: Conditional objective/domain assumptions; not unrestricted polynomial knapsack optimization. Published2003JOTA116(3)517--529, DOI10.1023/A:1023061218864.

## ref13

[Primary source](https://arxiv.org/abs/quant-ph/9607014). Abstract and original1996 submission/revision history.

Supports: Quantum minimum finding as optimization background.

Limits: Cited as original preprint, not an invented journal publication; no theorem transplanted into our oracle.

## ref16

[Primary source](https://eprint.iacr.org/2013/199). Author-posted abstract, metadata and official BibTeX.

Supports: Quantum subset-sum algorithms using Johnson-graph walks and representation methods.

Limits: The source describes heuristic cost; cite the verified expanded ePrint rather than guessing conference-version details. This is exact-target subset sum, not arbitrary weight/value optimization.

## ref17

[Primary source](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.TQC.2018.5). Publisher metadata, abstract and paper opening.

Supports: Quantum subset-sum algorithms under random-instance/heuristic assumptions.

Limits: No current-best claim and no worst-case general-knapsack exponent. Exact proceedings pagination5:1--5:15.

## ref18

[Primary source](https://quantum-journal.org/papers/q-2025-12-02-1922/). Published abstract and official BibTeX.

Supports: Active/passive QRAM assumptions and costs.

Limits: Does not prove all quantum-addressable memory impossible; circuit QRAM can help. Updated2023preprint to Quantum9,1922(2025).

## ref23

[Primary source](https://arxiv.org/abs/2411.00518v2). Abstract, accepted-at-QCE statement and related DOI.

Supports: QTG state preparation with Grover-mixer QAOA; finite-depth evidence and eventual optimal-sampling result.

Limits: Not all QTG uses are QAOA; do not claim no guarantees whatsoever. DOI10.1109/QCE65121.2025.00011; no unverified page range inserted.

## ref24

[Primary source](https://arxiv.org/html/1906.10375v1). Statement of results and oracle model.

Supports: Quantum branch-and-bound query framework.

Limits: Monotone cost/bounding oracle, depth and precision assumptions matter. The result is not a free-oracle runtime bound and is not simply sqrt(T)*d in all models. Old body theorem remains on hold.

## ref25

[Primary source](https://arxiv.org/html/1411.4028v1). Algorithm description and asymptotic-depth discussion.

Supports: QAOA variational framework.

Limits: Do not claim all QAOA lacks guarantees; source has specified approximation/limit results.

## ref26

[Primary source](https://quantum-journal.org/papers/q-2021-04-08-428/). Abstract and official BibTeX.

Supports: Grover adaptive search for constrained polynomial binary optimization.

Limits: Search is not variational QAOA. Source discusses oracle construction and conditional comparison with brute force, not blanket practical advantage. Quantum5,428(2021).

## ref31

[Primary source](https://preskill.caltech.edu/pubs/preskill-2018-NISQ.pdf). Author full text; Quantum2,79 metadata.

Supports: Noise/depth context.

Limits: No evidence for this project's device experiments, a four-item boundary or its implementation-specific mitigation claims.

## ref33

[Primary source](https://raw.githubusercontent.com/Qiskit/qiskit/refs/heads/main/CITATION.bib). Official Qiskit BibTeX; Aer README citation link.

Supports: Software attribution to Quantum computing with Qiskit,2024.

Limits: Citation is not evidence for device execution or experiment results. Actual package versions belong in later methods revision.

## bonnetain2020improved

[Primary source](https://arxiv.org/html/2002.05276v4). Section3.2 heuristic discussion, Sections4--5 alternative algorithms and memory tradeoffs; publisher DOI metadata.

Supports: Specific walk-update heuristic issue and subsequent alternatives.

Limits: Do not label every subset-sum method unsound or every variant QRAQM-dependent. Correct ASIACRYPT2020,LNCS12492,633--666, DOI10.1007/978-3-030-64834-3_22.

## ref35

[Primary source](https://theoryofcomputing.org/articles/v014a015/). Publisher full paper, Theorems1.1/1.2.

Supports: Quantum backtracking query framework.

Limits: Detection and witness recovery have distinct statements. No full gate-model LP walk follows merely from a citation. ToC14(15)1--24(2018), DOI10.4086/toc.2018.v014a015.

## ref36

[Primary source](https://www.mdpi.com/1099-4300/26/4/345). Article title/authors, abstract and hybrid model.

Supports: Classical B&B with quantum annealing for integer linear problems.

Limits: Correct authors Sanavio,Tignone,Ercolessi; Entropy26(4),345(2024), DOI10.3390/e26040345. Oldarxiv2403.09560 is a different DFT paper and is removed.

## bozejko2026

[Primary source](https://link.springer.com/article/10.1007/s10479-024-06025-1). Sections3.1/4, Eq16--20, floor-pruning rule; Section5 experimental scope; publisher CiteThisArticle.

Supports: Finite multiplier-set bounds and integer pruning are prior art; quantum annealing hybrid.

Limits: Their sign convention u<=0 maps to our nonnegative lambda=-u; local residual capacity maps to their subproblem W. No claim their model certifies our bank or circuit. Large instances ran root-bound calculations only. Online2024; actual issue is AnnalsOR364,2111--2126(2026).

## gabbassov2025

[Primary source](https://journals.aps.org/prresearch/abstract/10.1103/53gd-2374). Publisher abstract and bibliographic header.

Supports: Lagrangian duality in constrained quantum optimization, comparison with QUBO.

Limits: Different adiabatic/fault-tolerant framework; does not establish this bank's correctness or novelty. PRR7,023305(2025), authors EinarGabbassov,GiliRosenberg,ArturScherer.

## martiel2019

[Primary source](https://link.springer.com/chapter/10.1007/978-3-030-38919-2_49). Publisher abstract/metadata, arxiv1908.11291 author version.

Supports: Concrete implementation of quantum backtracking and resource accounting.

Limits: CSP graph coloring/SAT, not a full implementation of this LP oracle. Updated to SOFSEM2020,LNCS12011,597--606; key retains historical2019identifier only.

## Rejected mappings and limitations

- Cached .firecrawl/grover1996.md is actually BBHT Tight bounds on quantum searching, quant-ph/9605034; rejected for ref8. Correct Grover is quant-ph/9605043.
- Exploratory arxiv1802.07240 is CobaltBFT, not Preskill; rejected. Correct Preskill identifier1801.00862.
- Exploratory arxiv1898.11291 typo rejected in the preceding reference plan; correct Martiel1908.11291.
- Official AMS volume305 cover says Quantum Computation and Information; arXiv journal-reference field contains a different volume-title wording. Publisher title prevails.
- Firecrawl default network resolution failed; escalated scrape returned insufficient credits. No purchase/repeated credit retry; verified cached sources and web fallback used.
- Fresh primary metadata changes Bozejko from advance-online2024 to issue2026; original online date retained as note.
