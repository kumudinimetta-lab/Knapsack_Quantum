# Abstract and literature review: sentence-level review

Scope: main.tex abstract (line 28), literature paragraphs (lines 46–58), and related-work table. Manuscript not edited in this pass. This is not approval of the rest of the manuscript or a fresh reproduction of all experiments.

Evidence: previously recorded primary-source audit in ../evidence/COMPLETE_REFERENCE_AUDIT.json, freshly inspected mathematical audit and raw result rows, and selected primary texts re-read this turn. `RETAIN` below means supported within the stated scope by that evidence; it does not mean every cited full text was newly re-read. Access limitations in the earlier source audit remain in force.

## Abstract, in sentence order

| ID | Claim | Assessment and evidence |
|---|---|---|
| A1 | Quantum tree-search frameworks require reversible bounding predicates; implementation costs can offset query reductions. | QUALIFY. General tree search need not use a numerical bounding oracle. Prefer “Quantum branch-and-bound frameworks use reversible bounding predicates, whose implementation costs can offset reductions in oracle queries.” This is motivation, not a measured result. |
| A2 | LP relaxation under fixed efficiency-ordered prefix branching. | RETAIN. Matches the stated model and saved theory audit; not arbitrary branching. |
| A3 | Certified rational affine-bound bank preserves every integer-target pruning decision without reproducing the fractional value. | RETAIN WITH CONTRACT. Positive integer weights, nonnegative integer profits, exact fixed order, certificate, and separate capacity rejection. Mathematical integer thresholds are distinct from the finite unsigned circuit interface. Example w=v=(1,1), W=1, bank={1/2}: LP=1 and bank=3/2 have the same floor; rational target 5/4 is deliberately outside scope. |
| A4 | Coverage certificates, grid/rational minimum cardinality, and construction avoiding capacity-reachability DP. | RETAIN. theory_claim_audit.md items 2–5. Minimum cardinality is not minimum gate count; the sufficient DP-free bank is not claimed minimum over the actual state coverage intervals. This pass checks the summary against recorded derivations, not a new full proof audit. |
| A5 | A linear number of multipliers can be necessary. | RETAIN. Recorded linear-cardinality family and 14 endpoint checks. This is a bank-cardinality limitation, not computational hardness or a quantum lower bound. |
| A6 | Constant-coefficient arithmetic, register bounds, compute-copy-uncompute. | RETAIN as a description of the construction. Global circuit correctness is not inferred from the finite checks. Implementation-level re-audit remains a later task. |
| A7 | 700 originals + 700 cores, 5,204,456 states, 20,817,824 floor comparisons, zero mismatches. | FRESH ROW REAGGREGATION PASS. All 1,400 rows in root_all_reachable_v2_rows.jsonl summed to exactly these counts, zero predicate-floor mismatches. DERIVED exact-arithmetic evidence, not statevector experiments. |
| A8 | 1,120 Fourier basis columns and 2,216 Boolean columns, zero gate mismatches; not large-instance simulation. | FRESH ROW REAGGREGATION PASS. Initial five completed rows total 544; resumed 19 rows total 576; 544+576=1,120. Seven Boolean rows total 2,216. Zero gate mismatches. SIMULATED. Prefer “Completed small-circuit basis tests…” to avoid suggesting every attempted simulator experiment passed. A failed superposition initialization path remains reported in the body; the eight expected insufficient-bank LP disagreements are not gate mismatches. |
| A9 | 105 instances; CX 0.4981, active qubits 0.4908, depth 1.0720 median ratios to root-aware reconstruction. | FRESH ROW REAGGREGATION PASS. All 105 rows complete. Unrounded medians 0.49812142250762775, 0.49079754601226994, 1.0720489143998004. DERIVED logical resources, not device timing or statistical speedup. |
| A10 | Scoped preservation and gate-count/depth tradeoff; no hardware or end-to-end speedup. | RETAIN. Consistent with increased median depth and limited comparison scope. Does not assert historical priority or journal acceptance. |

No invented numerical result was found in the abstract. Two precision edits are recommended (A1, A8). Its existing 201-word length is within the requested 150–250 range. “Bank”, “root-aware”, and “bank-floor comparison” are manuscript-defined descriptive terms, not alleged named external theorems.

## Literature review, in sentence order

Each row identifies the sentence by its opening/topic. Bibliography keys map to the existing primary-source ledger; no reference is recommended for deletion on the basis of unavailable full text.

| ID | Sentence/topic | Assessment and source |
|---|---|---|
| C1 | Historical fractional LP bounds | RETAIN broad context, ref1 publisher abstract. Full Dantzig text was not accessible; no precise theorem is asserted. |
| C2 | Horowitz–Sahni splitting and O(2^(n/2)) arithmetic baseline | RETAIN. Freshly re-read author full text, Section 5, cached line 1271: dominated weight/profit pairs discarded so sums and profits stay ordered. Source r maps to our n. Unit arithmetic/comparison model; no bit-cost or optimality claim. |
| C3 | Kellerer–Pferschy–Pisinger consolidation | RETAIN general book context, ref3 publisher contents. Internal exact theorem pages remain unverified. |
| C4 | Balas–Zemel core origin; Pisinger capacity/distribution caution | RETAIN, balas1980core and ref4 primary abstracts. No universal small-core assumption. |
| C5 | MINKNAP expanding-core DP; COMBO DP plus bounds | RETAIN, pisinger1997minimal and martello1999combo primary abstracts. |
| C6 | Stronger classical context than brute-force alone | RETAIN as methodological assessment, not a measured superiority result. |
| C7 | Beier–Vocking and Dey–Dubey–Molinaro distribution assumptions | RETAIN qualitative scope only. beier2004random abstract and dey2021random v4 Theorem 1/model; no transfer to our discrete cohorts. The journal Beier full theorem was not freshly inspected. |
| Q1 | Grover O(sqrt(N)) search | QUALIFY success model. Correct ref8 identity confirmed directly at https://arxiv.org/abs/quant-ph/9605043. Recommend “For a marked-item search with bounded error, Grover's algorithm uses O(sqrt(N)) oracle queries.” Avoid implying enumeration of the whole database or certainty. |
| Q2 | Amplitude amplification and adaptive/minimum finding | RETAIN, ref11/ref12/ref13. Fresh amplitude source Section 2 Theorems 2–3 requires measurement-free preparation and nonzero success probability. This is background, not a claim that a zero-solution search terminates without additional handling. |
| Q3 | “Searching all binary assignments therefore requires O(2^(n/2)) queries” | CHANGE. An upper bound should not be phrased as a necessity, and “all” can imply enumeration. Suggested: “Treating the 2^n assignments as an unstructured objective table gives an O(2^(n/2))-query minimum-finding baseline at constant success probability, before accounting for oracle cost.” Cite ref13. Fresh primary Theorem 1 gives probability at least 1/2; Section 3 permits constant repetitions. Map N=2^n, table value to a reversible feasibility/negative-profit score; infeasible assignments get a penalty above all feasible scores. This does not give a lower bound for structured knapsack or a complete runtime. |
| Q4 | BBBV lower-bound scope | RETAIN, ref9 Section 3.1/Theorem 3.5 in existing audit. No unrestricted knapsack lower bound is claimed. |
| S1 | BCJ representations and quantum subset-sum algorithms | RETAIN, ref5/ref16/ref17, primary audit. |
| S2 | Input models and heuristic assumptions distinguished | RETAIN. No exact-target subset-sum exponent is transplanted to general weight/value optimization. |
| S3 | Bonnetain walk-update issue and alternatives | RETAIN, bonnetain2020improved Section 3.2 and Sections 4–5 in existing audit. Scope explicitly avoids condemning every method. |
| S4 | QRAM architectures and assumptions | RETAIN, ref18 primary abstract/BibTeX audit. Readability: expand quantum random-access memory at first use. |
| S5 | Explicit memory cost accounting | RETAIN methodological caution; no assertion that QRAM is impossible. |
| G1 | Hou–Perkowski bounded-knapsack complete-candidate tests | RETAIN, hou2020 Sections 4–8 in existing audit; bounded-knapsack scope correctly stated. |
| G2 | Hamitouche Grover tests and classical optional fractional bound | RETAIN, hamitouche2025 Sections 4–5, Algorithm 1 step 1 in existing audit. Workshop/report status preserved. |
| G3 | Wilkening QTG/amplification vs separate fractional-bound QBnB benchmarks | RETAIN, wilkening2025 main text and Supplement F.2 in existing audit. |
| G4 | R1 software/data reference | RETAIN, wilkening2025code pinned version DOI and commit in existing audit. |
| G5 | Arithmetic and fractional bounds are prior art | RETAIN bounded conclusion from G1–G4, not an exhaustive priority survey. |
| G6 | Christiansen preparation with Grover-mixer QAOA/Farhi framework | RETAIN, ref23/ref25. Expand quantum approximate optimization algorithm on first use. |
| G7 | Arbitrarily high optimal sampling with sufficient depth and suitable parameters | RETAIN WITH ASSUMPTIONS. Fresh read of Christiansen Section V-A, cached lines 397–463: positive amplitudes on all feasible states, zero outside; feasible nonnegative irreducible projector mixer; diagonal objective; initial highest mixer eigenstate. Applies cited Binkowski Theorem 12. No efficient depth or angle-finding guarantee. The previous review inspected the underlying theorem; this pass re-read Christiansen's application, not the underlying full theorem again. |
| G8 | Grover adaptive search distinct from variational algorithm | RETAIN, ref26 primary audit. |
| L1 | Sanavio classical B&B plus annealing | RETAIN, ref36 publisher abstract/model. |
| L2 | Bozejko multiplier sets and integer pruning | RETAIN, bozejko2026 Sections 3.1/4, Eqs. 16–20 in existing audit; source multiplier u maps to -lambda. |
| L3 | Large-instance device experiments are root-bound evaluations | RETAIN with existing Section 5 source audit; not a statement about every experiment in that paper. |
| L4 | Gabbassov duality and QUBO comparison | RETAIN, gabbassov2025 primary abstract. Expand quadratic unconstrained binary optimization at first use. |
| L5 | Relaxation/floor operation not themselves new | RETAIN limited prior-art conclusion. |
| R1 | Montanaro query reductions with specified oracles | RETAIN, ref35 Theorems 1.1/1.2 and ref24 oracle-model audit. Broad framework context; no formula is imported into our implementation. |
| R2 | LP-oracle implementation cost not free | RETAIN distinction between oracle calls and gates. |
| R3 | Martiel–Remaud concrete backtracking circuits | RETAIN, martiel2019 primary abstract/author paper audit; no claim it implements our LP oracle. |
| R4 | VBE/Draper/Cuccaro arithmetic; Barenco gates | RETAIN primitive background, verified primary locations in existing audit. No assertion our full compiler is one of those exact networks. |
| R5 | Thapliyal divider as comparison, not executed here | RETAIN narrow existence statement; thapliyal2016 verified abstract, full text access unresolved in original audit. |
| R6 | Interval stabbing established; contribution in reduction/endpoints | RETAIN, erickson2019algorithms Chapter 4 exercise, printed p178. Own open-endpoint proof remains separate. |
| R7 | Preskill noise/depth context | RETAIN, ref31 author primary-text audit; not evidence of our hardware results. |
| R8 | Qiskit software does not establish device execution | RETAIN, ref33 software attribution. |
| P1 | Numerical bound vs complete-candidate test vs prefix predicate | RETAIN as definition of distinctions, not blanket absence-of-prior-work claim. |
| P2 | Our certified-bank prefix predicate | RETAIN conditional mathematical summary; see A3. |
| P3 | Positive weights/nonnegative profits/certificate/threshold/capacity/clean workspace | RETAIN; matches saved contract. |
| P4 | No numerical LP output/arbitrary branching/full walk | RETAIN scope exclusions. |
| P5 | Reconstructed comparison must identify semantics and costs | RETAIN; does not mislabel our circuit as released R1. |
| P6 | Table roles without priority or hardware claim | RETAIN; table is qualitative. |

## Related-work table

All six rows agree with the paragraph descriptions and existing primary-source ledger. The Montanaro row groups tree/branching/acceptance and bounding interfaces across two frameworks; it should not be read as saying every backtracking method requires a numerical LP bound. QTG and QBnB should be expanded in the table or prose for readability. No table row asserts measured superiority.

## Evidence hygiene finding

`.firecrawl/grover1996.md` actually contains the Boyer–Brassard–Hoyer–Tapp “Tight bounds on quantum searching” abstract, not Grover's original paper. It was not used as proof for ref8 in this review. The actual manuscript citation ref8 points to Grover's genuine paper; its title, author, arXiv ID and STOC publication were checked directly. Thus this is a cache-label problem, not an observed wrong-paper manuscript citation. Preserve the cached file; use verified content identities rather than its filename. No raw data were altered.

## Verdict

No fabricated abstract numbers or invented cited works were identified. Do not call both sections unconditionally “error-free”: A1, A8 and Q1–Q3 need the precision distinctions above, and some broad literature claims remain supported at primary-abstract/metadata level rather than inspected full texts. This pass identifies those limits explicitly instead of deleting genuine references or inventing theorem details. The current manuscript was left unchanged so the proposed small edits are reviewable.


## Corrections applied after user approval

Applied the abstract scope and completed-basis-test qualifiers, Grover success-model qualifier, minimum-finding upper-bound baseline with ref13, and first-use acronym expansions. Shortened the final abstract sentence without changing its claim so keywords remain on the title page. Final abstract: 199 words. Retained the existing title because it describes the scoped integer LP-pruning predicate rather than claiming full optimization or speedup. Changes are confined to the abstract and literature review; all 40 references retained. Source/PDF backup: ../backups/before_abstract_literature_fixes_20261027/. Build passed, 33 pages, no undefined references or overflow. The full-paper audit remains pending.
