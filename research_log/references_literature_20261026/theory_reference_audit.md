# Classical and theoretical reference audit — 26 October 2026

This is a read-only source audit for the bibliography and Literature Review revision. No manuscript or bibliography edits were made. All listed works are real; limited full-text access is recorded, not treated as grounds for deletion. No new experiments or performance measurements were made.

The full structured ledger is `theory_reference_audit.json`. Suggested complete records are in `theory_proposed_classical_entries.bib`, an audit artifact rather than a manuscript edit.

## Main decisions

* Correct Dantzig's page range from 266–277 to **266–288**.
* Attribute the core concept to **Balas and Zemel (1980)**. Retain Pisinger (1999) for its important caution about core distributions, capacities and test design.
* Describe Horowitz–Sahni as a classical meet-in-the-middle baseline. Its paper does not establish a lower bound or certify a blanket current-best claim.
* Keep general knapsack optimization separate from cryptographic subset-sum input models.
* Preserve the distinction between average-case Pareto enumeration, best-bound B&B, and our static-prefix tree.
* Treat interval stabbing and reduced-cost dual identities as established tools. Novelty of their particular oracle use remains separate and UNRESOLVED by bibliography verification.

## `ref1` — Discrete-Variable Extremum Problems

**Verified record:** George B. Dantzig (1957). Operations Research, 5(2):266--288. DOI 10.1287/opre.5.2.266. [Primary source](https://pubsonline.informs.org/doi/10.1287/opre.5.2.266).

**Source passage:** Publisher Cite as confirms 5(2):266–288; abstract discusses LP for discrete-variable optimization.

**Supports:** Historical LP context; retain this genuine reference and fix pages.

**Limits:** The inspected abstract does not establish a named precision lemma, tightness for every integer instance, or that every modern exact solver uses precisely this bound.

**Access boundary:** UNRESOLVED: full paper access; publisher PDF redirects to abstract. No theorem number invented.

**LR action:** Use 'fractional LP bounds' without 'tight' or universal solver claims.

**Local evidence:** `.firecrawl/dantzig1957.md:333-372,7857`; `.firecrawl/theory_refs_20261026_dantzig_citation.md`; `.firecrawl/theory_refs_20261026_primary_web_5.json`.

## `ref2` — Computing Partitions with Applications to the Knapsack Problem

**Verified record:** Ellis Horowitz and Sartaj Sahni (1974). Journal of the ACM, 21(2):277--292. DOI 10.1145/321812.321823. [Primary source](https://www.cise.ufl.edu/~sahni/papers/computingPartitions.pdf).

**Source passage:** Section 3 Algorithm 2(b) splits into two lists; its enumeration time includes output term rQ. Section 5 eliminates dominated weight/profit pairs and gives a splitting implementation taking O(2^(r/2)).

**Supports:** Classical meet-in-the-middle baseline in the arithmetic/comparison operation model.

**Limits:** No lower bound proving worst-case optimality of the algorithm; no current-best claim. A separate binary search per half-subset incurs an additional logarithmic list-size factor unless using soft-O or a different merge.

**Symbol mapping:** Source r→item count n; source si→weights wi; pi→values vi; M→capacity W; delta→binary decision.

**LR action:** Call it a classical O(2^(n/2)) baseline, not the best provable algorithm without scope.

**Local evidence:** `.firecrawl/horowitz-sahni-doi.md:148-158`; `.firecrawl/theory_refs_20261026_hs.json:data.web[0]`; `.firecrawl/theory_refs_20261026_hs_author_full.md:1129-1280`.

## `ref3` — Knapsack Problems

**Verified record:** Hans Kellerer and Ulrich Pferschy and David Pisinger (2004). Springer, . DOI 10.1007/978-3-540-24777-7. [Primary source](https://link.springer.com/book/10.1007/978-3-540-24777-7).

**Source passage:** First edition copyright2004. Ch2 Basic Algorithmic Concepts pp15–42; Ch3 Advanced Algorithmic Concepts pp43–72; Ch5 Exact Solution pp117–160.

**Supports:** General reference for exact knapsack methods.

**Limits:** Publisher metadata/TOC alone does not verify any exact theorem/page for O(nW), assumptions about typical cores or our benchmark generator.

**Access boundary:** UNRESOLVED: exact internal subsection/page; paywall. No guessed theorem number.

**LR action:** A broad review citation is appropriate; avoid assigning a precise uninspected theorem.

**Local evidence:** `.firecrawl/theory_refs_20261026_kpp_primary.md:223-274,408-430`.

## `ref4` — Core Problems in Knapsack Algorithms

**Verified record:** David Pisinger (1999). Operations Research, 47(4):570--575. DOI 10.1287/opre.47.4.570. [Primary source](https://pubsonline.informs.org/doi/10.1287/opre.47.4.570).

**Source passage:** Abstract credits Balas and Zemel with introducing cores in the1980s, challenges uniform weights within cores, and identifies difficult capacities and inadequate testing.

**Supports:** Core methods can fail under naive typical-instance assumptions; capacity and instance class matter.

**Limits:** Pisinger1999 introduced core, universally small/easy core, or attribution of all exact reduced-cost fixing to this article.

**Access boundary:** Publisher abstract and bibliography read; full article not accessed.

**LR action:** Retain as a caution and testing source; cite Balas–Zemel for origin.

**Local evidence:** `.firecrawl/theory_refs_20261026_pisinger_core.json:data.web[0]`.

## `ref5` — Improved Generic Algorithms for Hard Knapsacks

**Verified record:** Anja Becker and Jean-S{\'e}bastien Coron and Antoine Joux (2011). Advances in Cryptology -- EUROCRYPT 2011, 6632:364--385. DOI 10.1007/978-3-642-20465-4_21. [Primary source](https://link.springer.com/content/pdf/10.1007/978-3-642-20465-4_21.pdf).

**Source passage:** Section3 extends representations using {-1,0,+1}. Section3.4 treats heuristic/random behavior. Section3.6 Theorem2 gives a probabilistic guarantee for a large fraction of equibalanced densityD<1 instances.

**Supports:** Representation-based subset-sum advances under specified input models; not general optimization of arbitrary weight/value pairs.

**Limits:** Every representation algorithm is merely heuristic, or softO(2^.291n) is a worst-case general 0/1 optimization guarantee.

**Exact theorem scope:** Theorem2: any epsilon>0, fraction at least1−140*2^(−epsilon*n) of equibalanced densityD<1 instances, existing balanced solution, modified algorithm finds it in softO(2^((.291+3epsilon)*n)).

**Symbol mapping:** Source ai→subset-sum input coefficient; targetS→exact sum; not separate manuscript wi/vi optimization instance.

**LR action:** Separate subset-sum input models from our knapsack optimization problem; no exact-best label.

**Local evidence:** `.firecrawl/theory_refs_20261026_bcj.json:data.web[0],data.web[2]`; `.firecrawl/theory_refs_20261026_primary_web_3.json`; `.firecrawl/theory_refs_20261026_primary_web_5.json`.

## `beier2004random` — Random knapsack in expected polynomial time

**Verified record:** Ren{\'e} Beier and Berthold V{\"o}cking (2004). Journal of Computer and System Sciences, 69(3):306--329. DOI 10.1016/j.jcss.2004.04.004. [Primary source](https://www.sciencedirect.com/science/article/pii/S0022000004000431).

**Source passage:** Publisher abstract: average-case Pareto-optimal filling counts imply expected polynomial enumeration by Nemhauser–Ullmann; adversarial weights and random profits or conversely, under their probability-distribution conditions.

**Supports:** Instance distributions and correlations can change exact classical difficulty; average-case results need input assumptions.

**Limits:** Polynomial deterministic worst-case knapsack, polynomial static-prefix branch-and-bound trees, or automatic transfer to our discrete five benchmark classes.

**Access boundary:** 2004 journal full theorem not read; institutional2003 TR abstract corroborates scope but is not substituted for journal theorem numbers.

**LR action:** Keep qualitative and distribution-qualified; no unverified explicit complexity bound.

**Local evidence:** `.firecrawl/theory_refs_20261026_beier.json:data.web[0]`; `.firecrawl/theory_refs_20261026_primary_web_1.json`; `.firecrawl/theory_refs_20261026_primary_web_2.json`.

## `pisinger1997minimal` — A Minimal Algorithm for the 0-1 Knapsack Problem

**Verified record:** David Pisinger (1997). Operations Research, 45(5):758--767. DOI 10.1287/opre.45.5.758. [Primary source](https://pubsonline.informs.org/doi/10.1287/opre.45.5.758).

**Source passage:** Abstract says exact core cannot be identified before solving KP; describes dynamic programming with core extended as needed and lazy sorting/reduction.

**Supports:** Strong practical expanding-core DP baseline; adaptive classical preprocessing already exists.

**Limits:** Cheap prior exact-core identification, a provably fixed small core on all inputs, or optimality of preprocessing/gate cost.

**LR action:** Describe lazy expanding-core DP and retain experimental strength as source-specific, not global superiority.

**Local evidence:** `.firecrawl/theory_refs_20261026_minknap_primary.md:360-368,2451`.

## `martello1999combo` — Dynamic Programming and Strong Bounds for the 0-1 Knapsack Problem

**Verified record:** Silvano Martello and David Pisinger and Paolo Toth (1999). Management Science, 45(3):414--424. DOI 10.1287/mnsc.45.3.414. [Primary source](https://pubsonline.informs.org/doi/10.1287/mnsc.45.3.414).

**Source passage:** Abstract combines prior exact approaches, valid inequalities/surrogate relaxation, and a new initial core.

**Supports:** COMBO is a strong combined exact baseline using more than a plain static binary tree.

**Limits:** A plain DFS on our chosen tree represents COMBO, old machine timings establish current runtime superiority, or asymptotic quantum advantage over COMBO.

**LR action:** Retain as strong classical solver context without transplanting historical timings.

**Local evidence:** `.firecrawl/combo1999.md:460-464`.

## `martello1988mtm` — A New Algorithm for the 0-1 Knapsack Problem

**Verified record:** Silvano Martello and Paolo Toth (1988). Management Science, 34(5):633--644. DOI 10.1287/mnsc.34.5.633. [Primary source](https://pubsonline.informs.org/doi/10.1287/mnsc.34.5.633).

**Source passage:** Abstract describes a core problem, a heuristic incumbent with optimality proof in suitable cases, improved upper bounds and reduction procedures.

**Supports:** Established exact core/bounding/reduction methods.

**Limits:** No proof every instance has a small/easy core or that a heuristic incumbent is always optimal.

**LR action:** Retain for exact classical solver history; avoid universal empirical claims.

**Local evidence:** `.firecrawl/theory_refs_20261026_mtm.json:data.web[2]`.

## `dey2021random` — Branch-and-Bound Solves Random Binary IPs in Polytime

**Verified record:** Santanu S. Dey and Yatharth Dubey and Marco Molinaro (2021). undefined, . [Primary source](https://arxiv.org/html/2007.15192v4).

**Source passage:** Section3 Lagrangian reduced costs Eq2–3; Theorem3 bounds best-bound tree by2*n*|G|+1. Corollary3 gives geometric counting bound. Theorem1 random polynomial guarantee assumes iid continuousuniform coefficient/objective data, fixed constraint count, proportional RHS.

**Supports:** Known reduced-cost loss/duality and counting ideas; distinction between deterministic tree certificate and random-instance theorem.

**Limits:** Transfer best-bound node-count theorem to arbitrary static-prefix DFS or random theorem to five discrete benchmark classes; newness of reduced-cost identity.

**Symbol mapping:** n source=number of variables; m source=number constraints(ours1), not manuscript core itemcountm; A_1i=wi,c_i=vi,b_1=W,lambda scalar; G binary points with reduced-cost loss≤IPGap.

**LR action:** Reference established dual/counting context with explicit node-selection/input-model qualifications.

**Local evidence:** `.firecrawl/theory_search_dey_0.md:11-26,180-246,614-626`; `.firecrawl/theory_refs_20261026_primary_web_2.json`.

## `erickson2019algorithms` — Algorithms

**Verified record:** Jeff Erickson (2019). Self-published, . [Primary source](https://jeffe.cs.illinois.edu/teaching/algorithms/book/04-greedy.pdf).

**Source passage:** First edition June2019. Chapter4 exercises printedp178 explicitly poses minimum point stabbing of intervals; extracted exercise number illegible, so none supplied.

**Supports:** Interval stabbing is an established combinatorial problem; not a new general optimization principle.

**Limits:** Book exercise proves our half-open/open rational-cell adaptation, supplies our exact endpoint construction, or certifies minimum gates.

**LR action:** Cite as standard problem background; retain separate proof of strict-boundary adaptation.

**Local evidence:** `.firecrawl/theory_erickson_stabbing_20261024_0.md`; `.firecrawl/theory_erickson_stabbing_20261024_2.md`; `.firecrawl/theory_refs_20261026_primary_web_6.json`.

## `balas1980core` — An Algorithm for Large Zero-One Knapsack Problems

**Verified record:** Egon Balas and Eitan Zemel (1980). Operations Research, 28(5):1130--1154. DOI 10.1287/opre.28.5.1130. [Primary source](https://pubsonline.informs.org/doi/10.1287/opre.28.5.1130).

**Source passage:** Publisher abstract introduces core as equivalent KP on subset variables and says exact core cannot be identified without solving KP; LP gives a satisfactory approximation.

**Supports:** Historical origin of core-based methods and LP-guided approximate core identification.

**Limits:** A uniformly small exact core is discoverable at negligible cost for every instance.

**LR action:** Add alongside Pisinger1997/1999 when discussing core methods.

**Local evidence:** `.firecrawl/theory_refs_20261026_primary_web_1.json`; `.firecrawl/theory_refs_20261026_primary_web_2.json`.

## Mathematical source boundaries

Dey et al. version 4, Theorem 1 assumes independently uniform [0,1] entries of the coefficient matrix and objective, fixed number of constraints m, n≥m+1, and right-hand sides b_j=β_j n with β_j∈(0,1/2). Nodes use best-bound selection and branch on fractional variables. Theorem 3 and Corollary 3 are deterministic counting statements under their stated B&B setting; the polynomial random-instance conclusion is not a consequence for arbitrary discrete correlated benchmarks. In the manuscript's one-row knapsack, source m=1; source n is the item count, not the manuscript's use of m for core size. The bound is on nodes, not runtime or quantum gates.

The BCJ2011 Theorem 2 is a fractional-population probabilistic subset-sum guarantee with balanced solutions and density D<1. It is not a worst-case guarantee for optimization with separate weights and profits. Its presence also prevents describing the entire paper as only heuristic.

Erickson's minimum-stabbing exercise is in Chapter 4, printed p.178. It states the established problem but does not provide the manuscript's strict-open-interval proof. The illegible extracted exercise number was not guessed.

## Outside-LR holds — no edits in this pass

| Original line | Existing statement | Later action |
|---|---|---|
|61|Horowitz–Sahni is 'the best classical exact algorithm'|Remove unscoped optimality/current-best implication; cite as a baseline.|
|176|Core concept introduced by Pisinger1999|Correct origin to Balas–Zemel1980.|
|199|Reduced-cost variable fixing 'due to Pisinger1999'|Inspected paper does not support the attribution; revise attribution independently of the correct mathematical fixing condition.|
|203|Independent binary search per half-list entry, but exactO(2^(n/2)) total|Include logarithmic factor, use soft-O, or describe monotone merge/sorted dominance implementation.|

Line numbers identify the version read at audit start and may move during the parent's authorized Literature Review edit.

## Retrieval failures retained

Firecrawl was used under its research-paper skill, then began returning insufficient-credit errors for later scrapes. A bounded web-tool fallback supplied missing primary pages. Dantzig's PDF route redirected to its abstract. The KPP internal chapters and exact journal-version Beier theorem numbers remain uninspected, explicitly UNRESOLVED, while their genuine metadata and qualitative abstracts remain usable. IACR PDF and HAL-document routes failed; the BCJ full publisher PDF was accessible and used instead. Secondary indexes were discovery aids, not the mathematical evidence. Existing caches and all new retrieval records remain preserved.
