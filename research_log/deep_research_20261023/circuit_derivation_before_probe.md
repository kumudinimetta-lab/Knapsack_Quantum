# Circuit-track candidate derivations before feasibility code

Date: 2026-10-23. Status: candidate derivations; independent review is pending. Existing manuscript/code/raw data are unchanged. Graph MCP discovery returned no relevant tools, so targeted code reads were used.

## Source prerequisite
Primary source: Vlatko Vedral, Adriano Barenco, Artur Ekert, "Quantum networks for elementary arithmetic operations," Physical Review A 54, 147 (1996), DOI https://doi.org/10.1103/PhysRevA.54.147 ; author's primary preprint https://arxiv.org/html/quant-ph/9511018v1 . Sections III.1 and III.3 construct subtraction/comparison using overflow and constant multiplication by controlled additions. The preprint title capitalizes words differently; this is the same source. No divider is needed in the candidate. Cached full primary text `.firecrawl/vbe-full.md` was read. This establishes arithmetic feasibility, not a new complexity theorem or optimal gate count.

## Candidate A: exact rational comparison

Assumptions: positive integer item weights and values, nonnegative integer capacity, exact classical decreasing-ratio item order with deterministic ties, integer threshold tau encoded without overflow, coherent prefix and depth, initially zero workspace. Let P be the integer value of selected assigned items plus all whole suffix items that fit before the first split item s. Let r be the residual capacity at that first split, so 0 <= r < w_s. The fractional LP value is U = P + r*v_s/w_s.

Since w_s > 0, U < tau iff P*w_s + r*v_s < tau*w_s. This is an integer comparison; equality is not pruned. At an all-fit suffix, use P < tau. At an infeasible prefix, prune independently. Thus no fixed-point k, efficiency truncation, or reversible variable division is needed. The identity is elementary and is not proposed as an original theorem.

All-item coherent-depth scan: compute assigned-item sums under j < d; greedily process exactly j >= d while an active flag remains true; at the first split, record the cross-product comparison and deactivate; otherwise compare the whole-item total at the end. Invalid depth encodings d > m produce the same reject flag as the existing wrapper. Prefix bits beyond d are ignored. Compute-copy-uncompute gives a clean XOR predicate.

Width obligations: prefix weight <= sum(w); choose its arithmetic width above capacity + sum(w). Integer P <= S=sum(v). A safe numerator width covers S*wmax + capacity*vmax and (2^tb-1)*wmax, where tb is threshold width. Signed negative arithmetic is unnecessary for the chosen form. Underflow in infeasible-prefix residual registers is independently gated out; arithmetic is still reversible on that branch.

Adversarial cases to include: exact threshold equality (strict <), zero capacity/residual, all-fit suffix, no suffix, overweight prefix, repeated efficiencies, irrelevant prefix bits, invalid depth, both target-bit inputs, tau=0 and maximum encoded tau. A rejected alternative r*v_s < (tau-P)*w_s needs signed handling when tau-P < 0; the first probe will avoid that alternative.

## Candidate B: root-dual bound, loss form

Choose any nonnegative rational lambda=a/b with integers a>=0,b>0, preferably the root LP split ratio. Define r_i=b*v_i-a*w_i and N0=a*W+sum_i max(r_i,0). For a prefix assignment x, let L=sum_assigned_selected max(-r_i,0)+sum_assigned_excluded max(r_i,0). Its residual Lagrange bound numerator is N=N0-L.

Derivation: for feasible completion y of the suffix, b*value(x,y) = a*weight(x,y)+sum_assigned x_i*r_i+sum_suffix y_i*r_i <= a*W+sum_assigned x_i*r_i+sum_suffix max(r_i,0) = N0-L. Therefore N/b is an upper bound; N0 < L+b*tau is a safe strict pruning comparison. A stronger residual LP bound is <= this bound because it minimizes the same Lagrange expression over lambda. Root lambda=0 handles all-fit instances. No claim is made that any lambda produces a tight bound, or that this bound is historically new.

Each loss coefficient is a precomputed nonnegative integer. A coherent prefix-only implementation needs capacity sums, depth-controlled loss additions, one threshold constant multiplication, one comparator and uncomputation. It need not construct a split suffix or a quantum quotient. It can be incrementally maintained by adding/removing the chosen loss coefficient along a path, but a full walk with aggregate registers is NOT implemented by this probe.

Falsification attempts planned before accepting a scoped circuit claim: exhaustive feasible completions for small cases must never exceed N/b; exact bound <= N/b; search witnesses can survive even when weaker bound expands more nodes; compare all input encodings and retain every mismatch. Claim of global performance improvement is deliberately not made. Candidate can lose because the weaker tree expands too much.

## Attribution/novelty boundaries

Martiel and Remaud, "Practical implementation of a quantum backtracking algorithm," arXiv:1908.11291 (2019), Section 3 already explicitly trades heuristic circuit depth against search-tree reduction; Section 4 already uses a quantum depth index and constant/quantum comparisons. A root-dual/resource tradeoff paper must exceed this generic observation with knapsack-specific coherent circuits, actual gate lists, matched tree costs and negative regimes. Wilkening et al. 2025 already supplies a QTG construction, resource estimation and classical comparisons. Hou and Perkowski 2020 already supplies quantum knapsack decision circuits and gate costs. None of those facts demonstrates priority for these candidates.

## Failed/limited operations retained

- A first UTF-8 JSON inspection used the Windows default cp1252 decoder and failed with UnicodeDecodeError; rerun explicitly used UTF-8. No data were changed.
- One extra Firecrawl search for constraint-propagation cost returned HTTP 429; do not interpret a missing result as evidence of novelty.
- Existing exact-statevector circuit tests run on permutation-basis columns. This is exact for the X/CX/CCX gate set with clean workspace, not a demonstration that the full algorithm runs on a QPU.
