# Closest-source comparison: Wilkening et al. (2025), Supplementary F

Date: 23 October 2026. Purpose: resolve concrete overlap before drafting novelty claims. This is source comparison, not endorsement of every theorem interpretation in the predecessor.

## Primary material actually read

- Published article: S. Wilkening, A.-I. Lefterovici, L. Binkowski, M. Perk, S. P. Fekete and T. J. Osborne, "A quantum algorithm for solving 0-1 Knapsack problems," npj Quantum Information11,146(2025), DOI https://doi.org/10.1038/s41534-025-01097-8 .
- Published supplementary PDF, full text extracted by Firecrawl: https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41534-025-01097-8/MediaObjects/41534_2025_1097_MOESM1_ESM.pdf . Cached authentic text `.firecrawl/circuit_wilkening2025_supplement_firecrawl.md`, 71,531characters. Read SectionE introduction/E.3/E.4/E.5 and all of F, especially F.2.
- Authors' primary preprint https://arxiv.org/html/2310.06623v2#A1.SS6.SSS2 , AppendixA.6.2, cross-checked for the fractional bound and benchmark assumptions. This version labels the same part A.6.2 rather than F.2. Primary full preprint cached `.firecrawl/circuit_wilkening_arxiv_full.md`.

Source integrity failure retained: direct Invoke-WebRequest download to `.firecrawl/circuit_wilkening2025_supplement.pdf` produced a3,038-byte one-page PDF containing only a JavaScript-disabled access page. It is NOT the supplement and was not used as evidence. Its extracted content is retained in `.firecrawl/circuit_wilkening2025_supplement.txt`. The successful Firecrawl extraction, not that access page, supplied the published supplement. No mathematical conclusion was drawn from missing content.

## Exact section/assumption mapping

### F.2 "Quantum branch-and-bound" (preprint A.6.2)

There is no numbered new theorem or numbered new algorithm in this subsection. It describes a benchmark model and cites existing quantum tree-size estimation, tree search and backtracking results. We do not manufacture a theorem number for it.

It identifies tree-size estimation and marked-node search as two ingredients. It explicitly adopts three favorable benchmark assumptions:
1. Optimal solution and its tree sizeT are known, so tree-size estimation is applied only once.
2. Quantum subroutine success probability is1.
3. Backtracking dominates; other quantum subroutines are treated as queried once.

It then sets beta=1, uses a sqrt(T*n) walk/phase-estimation-use model, and obtainsT by running the classical algorithm. This is their stated benchmark schedule/optimistic estimate. It is not an independently measured quantum runtime, and this report does not infer that a generic lower bound or rigorous universal success guarantee follows from their choice beta=1.

Most decisive overlap: F.2 expressly uses the fractional-greedy upper bound for knapsack. Items are sorted by density, whole items are packed through break indexh, and a fraction of the next item supplies:
U=sum_{j<=h}p_j+p_{h+1}*(c-sum_{j<=h}w_j)/w_{h+1}.
This formula is UNNUMBERED in F.2; no fabricated equation label is assigned here. The subsection closes by relating quantum fractional-greedy implementation cost to the previous QTG arithmetic cycle calculations.

Symbol mapping to this project:
- Theirp_i = ourv_i; theirw_i = ourw_i; theirc = ourW or residualcapacity after a prefix.
- Theirh = last whole suffix item; our firstsplit indexs corresponds toh+1 after adding the assigned-prefix integer valueP.
- Theirn = total selected problem item countm; theirT is a classically recorded benchmark tree count. Our paired structural study also enumerates static trees but labels those classical counts MEASURED and any sqrt(T) work model DERIVED.
- Their known optimum assumption is not used to choose our production predicate or optimization threshold; diagnostic optimum+1 conditions are labeled answer-known unmarked tests. Our cheap dual certificates and prefix reconstruction are distinct analyses, not free tree-size inputs.

### E "Resource estimation" and E.3-E.5

E defines qubit, gate and cycle counts for QTG exploration unitaries under explicit multi-controlled-gate/ancilla reuse assumptions. E.3 develops constant QFT addition from Draper's construction, merging rotations for known classical summands and using copied controls to parallelize. E.4 treats subtraction and records when intermediate QFTs cannot cancel because comparisons intervene. E.5 addresses capacity and profit comparisons. These precedents rule out a novelty claim based simply on constant-specialized knapsack arithmetic or reporting gates/cycles/ancillas.

Their QFT rotations/cycle conventions are different from our X/CX/CCX logical gate lists. Direct numerical comparison of their cycles to our CCX counts would mix cost models. Any direct performance comparison would require a shared gate/synthesis/connectivity/precision convention.

## What is already covered, and what is merely a candidate distinction

| Proposed broad claim | Assessment against this specific source |
|---|---|
| Quantum branch-and-bound for0/1knapsack |Already present in F.2 as a competitive algorithm benchmark.|
| Fractional/LPgreedy pruning within quantum knapsack tree search |Explicitly present in F.2. Cannot claim absence or first use.|
| Classical tree logs converted into a quantum search/resource schedule |Already present in this work. Our matched proxy study alone does not establish priority.|
| Resource estimation for knapsack arithmetic |Detailed precedent in E.3-E.5.|
| Static preprocessing can leave a smaller residual quantum problem |Main text's future improvements also mentions preprocessing branch-and-bound; this broad idea alone is not novel.|
| Exact threshold predicate via reduced rational cross products and explicit clean basis-level verification |Not presented in F.2's sketch or E's QTG arithmetic analysis in the form used here. This is a construction-level difference to compare, not proof of global priority.|
| Root-dual additive-loss predicate and nested2/4multiplier bank as cheaper alternatives to exact residualLP |These specific constructions are not described in the sections read; they remain candidate differences. Weak duality and multi-bound portfolios are themselves standard.|
| Same-instance matched arithmetic/dispatcher controls, weak/strong tree costs, certificate-aware limits and compiler-sensitivity Pareto data |A more specific study design than F.2's single fractional-greedy benchmark. Its significance depends on results and wider related-work review.|

## Defensible wording and limits

Useful positioning: build on established quantum knapsack tree search, and study how the cost of implementing safe bounds changes the pruning/resource tradeoff under explicit predicate circuits. Compare a fixed dual certificate/bank with recomputed fractionalLP and with a simple remaining-profit control; retain caps and negative regimes. Exact arithmetic and compactness are implementation controls, not invented new mathematical principles.

Do NOT use: first quantum knapsack BnB; first LP-pruned quantum knapsack; no previous resource analysis; first cost-versus-pruning tradeoff; measured quantum speedup from scheduled sqrt(T); universal guarantee of publication. This source does not establish our novelty and does not by itself negate every narrower construction-level contribution. Global priority remains UNRESOLVED pending broader source comparison.
