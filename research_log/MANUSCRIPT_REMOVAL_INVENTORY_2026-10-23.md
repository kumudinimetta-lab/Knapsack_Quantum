# Inventory of manuscript removals and replacements

Prepared 23 October 2026 at the user’s request. Restoration is paused. This report changes neither manuscript nor bibliography.

The before-revision LaTeX and bibliography preserve the exact prior text. The saved PDF is the PDF present when that backup was made; its build correspondence to the saved LaTeX has not been re-established.

## Saved files

- Earlier source: `C:\CBP\HybridQuantumKnapsack\paper\backups\2026-10-22_before_revision\main.tex`
- Earlier bibliography: `C:\CBP\HybridQuantumKnapsack\paper\backups\2026-10-22_before_revision\references.bib`
- Earlier PDF: `C:\CBP\HybridQuantumKnapsack\paper\backups\2026-10-22_before_revision\main.pdf`
- Current source: `C:\CBP\HybridQuantumKnapsack\paper\main.tex`
- Full line-by-line source and bibliography diff: `C:\CBP\HybridQuantumKnapsack\research_log\MANUSCRIPT_EXACT_CHANGES_2026-10-23.diff`

## Substantive changes

“Replaced” means the earlier wording/numbers were removed from the current manuscript and different content was inserted. It does not mean the entire subject disappeared. Reasons below describe the revision; this inventory is not a new independent verification of every technical conclusion.

| Area | Removed or replaced | Current treatment |
|---|---|---|
| Title, abstract, contributions | Replaced the long abstract, shortened the contribution list, changed “Spectral Validation” to “Spectral Checks”, and removed broad uniqueness, general advantage and hardware-validation statements. | A short abstract and a more limited contribution list remain. This was more extensive rewriting than minimal word changes. |
| Introduction and literature review | Removed the paragraph about subset-sum exponents, Heuristic 2 and QRAQM; replaced most of the literature review, including classical subset-sum work, quantum search limits, quantum walks, other quantum optimization methods, and quantum-inspired methods. | A shorter classical/tree-search review and three newly added close quantum knapsack comparisons remain. This substantially reduced literature coverage; removal is not evidence a source is false. |
| Prior-work tables | Removed the capability checklist and the separate table of knapsack/subset-sum algorithm complexities. | A narrower method-comparison table remains. Original table content is in the saved source and exact diff. |
| Preliminaries | Replaced the Montanaro theorem statement/attribution; revised amplitude amplification assumptions, core interpretation and meet-in-the-middle cost wording. | The concepts remain, with different statements and qualifications. |
| LP bounding oracle h | Replaced the old fixed-precision formula, resource table and claims about the earlier small circuit, including the old 96-qubit result. | A new safe pruning formula, Boolean circuit construction, gate-list resources and explicitly scoped simulations replace them. |
| Threshold predicate V | Removed the old logical-resource and analytical T-count table and its associated discussion. | The predicate construction and a scoped dense-statevector check remain. Full original resource discussion is recoverable. |
| Optimization and correctness | Replaced the threshold-search pseudocode, repetition-based correctness statement/proof and composed query bound. | Explicit witness recovery, allocation of decision error and a certified-tree-bound assumption replace the earlier statements. |
| Core analysis | Replaced the marginal-loss lemma explanation/proof and rational-valued spacing counterexample; corrected the full binary-tree vertex count. | Core containment and spacing bounds remain, with a dual proof and an integer fixed-gap counterexample. |
| Experimental setup and fixing results | Replaced the setup description and mean fixing-ratio values in the old table. | Exact-arithmetic rerun results and metric classifications replace them; historical data were retained. |
| Spectral experiment | Replaced the original spectral-validation narrative and taxonomy table. | A fresh Schur-based audit, capped/trivial/bypassed status counts and explicitly scoped acceptance checks replace them. |
| Runtime and memory | Condensed the old runtime/memory discussion and revised interpretation of the baseline. | Archived timings are still reported as archived implementation results; the OR-Tools timing and cutoff tables remain with revised captions/wording. |
| Regression | Removed the old fitted coefficients/statistics and the interpretation of the response as a reduced-core threshold tree. | A new exploratory regression of actual classical core-solver nodes replaces it, with explicit zero-gap exclusions. |
| Instance-dependent discussion | Replaced the original discussion of near-constant cores, instance-dependent query behavior and hard regimes. | A shorter discussion based on revised data and conditional query costs remains. |
| IBM hardware | Removed the Hardware Validation Insights subsection, IBM-versus-simulator success-probability table, noise-boundary conclusions and corresponding IBM acknowledgment sentence. | A limitations paragraph states that archived summaries do not establish execution provenance for the revised algorithm. The old table/text remain in backups; no new hardware run was performed. |
| Fault-tolerant crossover | Removed the Resource-Estimation Crossover Analysis subsection, per-query T-cost/crossover table and numerical hardware-crossover conclusions. | A limitation explains why component estimates are not full algorithm costs or a demonstrated crossover. |
| Conclusion, availability and limitations | Rewrote the conclusion and availability statement, replaced parts of the limitations, and added pending declarations and AI-use disclosure. | These reflect the revised claims and reproducibility scope. |
| Journal layout | Replaced IEEE conference formatting with the Springer Nature class, reformatted authors/affiliation and reduced keywords. | Author order was preserved; Madhavi is provisional corresponding author. |

## Bibliography accounting

- Earlier bibliography: 45 entries; earlier manuscript: 41 unique cited keys.
- Current bibliography: 15 entries; current manuscript: 15 unique cited keys.
- Old entries retained: 12. Old entries omitted: 33. New entries added: 3.

The omitted sources were not all individually established to be false. Blanket exclusion of unverified sources was not a substitute for an individual citation audit.

### Every omitted bibliography entry

Titles below are transcribed from the earlier bibliography; they are not certified bibliographic metadata.

| Old key | Old title | Cited in earlier manuscript? |
|---|---|---|
| `ref5` | Improved generic algorithms for hard knapsacks | Yes |
| `ref6` | Subset sum algorithms: improved classical and quantum algorithms | Yes |
| `ref7` | Analysis and optimisation of the packing tree search algorithm for the knapsack problem | Yes |
| `ref9` | Strengths and weaknesses of quantum computing | Yes |
| `ref10` | Grover algorithm with zero theoretical failure rate | Yes |
| `ref12` | Implementing pure adaptive search with Grover's quantum algorithm | Yes |
| `ref13` | A quantum algorithm for finding the minimum | Yes |
| `ref14` | Quantum walk algorithm for element distinctness | Yes |
| `ref15` | Search via quantum walk | Yes |
| `ref16` | Quantum algorithms for the subset-sum problem | Yes |
| `ref17` | Subset sum quantumly in $1.17^n$ | Yes |
| `ref18` | QRAM: A survey and critique | Yes |
| `ref19` | Quantum lattice sieving with reduced memory requirements | Yes |
| `ref20` | A quantum algorithm for the solution of the 0-1 knapsack problem | Yes |
| `ref21` | Computational speedups using small quantum devices | Yes |
| `ref22` | A quantum search method for quadratic and multidimensional knapsack problems | Yes |
| `ref23` | Quantum tree generator improves {QAOA} state-of-the-art for the knapsack problem | Yes |
| `ref25` | A quantum approximate optimization algorithm | Yes |
| `ref26` | Grover adaptive search for constrained polynomial binary optimization | Yes |
| `ref27` | Quantum computing assisted optimization for energy systems | Yes |
| `ref28` | Hybrid quantum genetic algorithm for the 0-1 knapsack problem | Yes |
| `ref29` | Quantum-inspired wolf pack algorithm to solve the 0-1 knapsack problem | Yes |
| `ref30` | A binary multi-scale quantum harmonic oscillator algorithm for 0-1 knapsack problem | Yes |
| `ref31` | Quantum computing in the NISQ era and beyond | Yes |
| `ref32` | Quantum advantage with shallow circuits | Yes |
| `ref33` | Qiskit: An open-source framework for quantum computing | Yes |
| `ref34` | Quantum lower bounds by quantum arguments | Yes |
| `bonnetain2020improved` | Improved classical and quantum algorithms for subset-sum | Yes |
| `ref36` | Hybrid classical-quantum branch-and-bound algorithm for solving integer linear programs | Yes |
| `beier2004random` | Random knapsack in expected polynomial time | No |
| `pisinger1997minimal` | A minimal algorithm for the 0-1 knapsack problem | No |
| `martello1988mtm` | A new algorithm for the 0-1 knapsack problem | No |
| `barenco1995` | Elementary gates for quantum computation | Yes |

### Added bibliography keys

`wilkening2025`, `creemers2025`, `bozejko2026`

## Snapshot hashes

SHA-256 hashes identify the exact versions compared.
- `C:\CBP\HybridQuantumKnapsack\paper\backups\2026-10-22_before_revision\main.tex`: `593c2b22a7aac7b8d0106dd6a804b40cb37634ed78395d4f1eb74ab8c5cf9dc1`
- `C:\CBP\HybridQuantumKnapsack\paper\backups\2026-10-22_before_revision\references.bib`: `2129e91caedb7322581d0333aae4af50d5126bfd6b02b6da7dba4ec1d694987b`
- `C:\CBP\HybridQuantumKnapsack\paper\backups\2026-10-22_before_revision\main.pdf`: `2c26c61db6a2756d8cee0ab5d6851851f7ba0de0a61e0e3abca9373e6875e231`
- `C:\CBP\HybridQuantumKnapsack\paper\main.tex`: `196a36632d5920f26e870b765d8d649dce3f5e1c43037c2ad0d063f0a82a3a86`
- `C:\CBP\HybridQuantumKnapsack\paper\references.bib`: `8e6240bb7a0fa4fb45e956c479b1aa24efea05cb01570284da03d0f8ea7515fe`
- `C:\CBP\HybridQuantumKnapsack\paper\main.pdf`: `d7a5f0b0fef09df7eae579c5bd309c0dde0bd62eacb9311aeb32b3b2e5461d99`
