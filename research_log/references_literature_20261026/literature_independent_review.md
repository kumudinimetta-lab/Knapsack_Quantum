# Read-only source-to-claim review of revised Literature Review

26 October 2026. Reviewed `literature_replacement.tex` and the arithmetic/
closest-source entries now saved in `paper/references.bib`. No main-paper,
bibliography, numerical raw data or simulation code edits made by this reviewer.
Graph tools were unavailable after discovery; targeted source reads used.
This is a circuit-reference/semantics review, not approval of unrelated old
body claims or every search theorem elsewhere in the paper.

## Fix before compile

1. **Separate Wilkening's main QTG algorithm from its QBnB benchmark.**
   LR line9 says their algorithm uses a quantum tree generator *and*
   fractional-greedy bounds. The primary article describes QTG with amplitude
   amplification; the fractional-greedy upper bound appears in the SEPARATE
   competitive QBnB benchmark, SupplementF.2. Current wording can incorrectly
   place that bound inside the main QTG search. Suggested replacement:

   > Wilkening et al. develop QTG-based amplitude-amplification search and,
   > separately, benchmark quantum B\&B using fractional-greedy bounds.

   [Primary article](https://www.nature.com/articles/s41534-025-01097-8),
   [SupplementF.2](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41534-025-01097-8/MediaObjects/41534_2025_1097_MOESM1_ESM.pdf).

2. **Keep the released implementation distinct from our reconstruction.**
   Table row29 calls R1 a versioned arithmetic implementation for comparison.
   R1 is real released software with a specialized QTG simulator and resource
   routines. The inspected QBnB call path does not supply the matched clean
   LP-prefix gate netlist compared in our new experiment. The table and prose
   should explicitly distinguish these, without making a universal absence
   claim. Suggested table cells:

   > QTG with amplitude amplification; fractional-greedy QBnB benchmarks

   > Published arithmetic primitives and released simulator/resource model;
   > our matched LP-oracle circuit is a declared reconstruction.

   The version DOI16895828 is correct; the citation itself is not the problem.
   Primary [release](https://zenodo.org/records/16895828),
   [audited bound path](https://github.com/SoerenWilkening/QTG_0-1Knapsack/blob/R1/src/simulation/quantum_branch_and_bound.c),
   [resource routine](https://github.com/SoerenWilkening/QTG_0-1Knapsack/blob/R1/src/simulation/qtgcount.c).

3. **Do not turn an LP upper-bound test into an integer-completion oracle.**
   LR line15 opens with deciding whether a prefix *can reach* an integer
   target. That can mean deciding existence of an actual integer completion.
   The implemented bank reproduces LP-threshold rejection, which can keep a
   prefix even when no integer completion reaches the target. The subsequent
   sentence is more precise, but the opening distinction should be fixed:

   > ...reversibly deciding whether the fractional LP upper bound for a
   > partial prefix falls below an integer target.

   A kept prefix is not a completion certificate. This follows directly from
   the LP relaxation versus integer problem distinction and matches the
   validated predicate's specified semantics.

## Small source-precision edits

* Identify Hou--Perkowski's problem as BOUNDED knapsack, as in its title and
  Section2, instead of silently treating its general integer-selection
  registers as the same binary-prefix encoding. The current statement that
  it tests complete candidates is otherwise supported by Sections4--8 and
  its Q\# simulator checks in Section10.
* Hamitouche et al.'s Algorithm1 step1 allows a classical upper bound,
  explicitly giving fractional knapsack as an example. Safer prose is
  “their node routine permits a classical fractional-knapsack bound,” rather
  than suggesting the experiments establish one particular bound at every
  node. The complete-assignment feasibility/improvement oracle and ancilla
  reuse are supported. It is a workshop/report citation, not a journal/LNAI
  publication. Primary [proceedings](https://www.cs.auckland.ac.nz/research/groups/CDMTCS/researchreports/download.php?selected-id=904),
  paper Sections4--5, Algorithm1; printed local pages1--14.

## Checks that pass within this review's scope

* Arithmetic attribution to VBE, Draper, Cuccaro and Barenco is appropriately
  general. It no longer turns one primitive's ancillary cost into a complete
  oracle resource theorem.
* The Thapliyal sentence explicitly says the constant-coefficient construction
  does not execute the divider. Retaining that real 2016 three-author preprint
  avoids breaking the staged body citations without certifying their old use.
* The bank scope includes positive integer weights, nonnegative integer
  profits, fixed exact-efficiency order, a coverage certificate, representable
  integer thresholds, separate capacity handling and clean workspace. These
  are the right mathematical restrictions. Implementation panels must still
  state their individual domains: the old Boolean builder accepts positive
  profits, while the new QFT bank additionally supports zero profits.
* The text rejects unrestricted historical-priority, complete-walk and
  hardware-advantage inferences. No fresh first/unique claim is established.
* All nine audited arithmetic/closest-source bibliographic identities match
  the primary evidence. Preprints are identified as such. Wilkening's article
  number146 and version-specific Zenodo DOI are correct.

The QAOA large-depth convergence wording and other agents' classical/search
theorem attributions are outside this circuit-source pass; they should use
their own primary-source audit. Nothing here certifies stale divider,
hardware, spectral or runtime statements elsewhere in the manuscript.

## Follow-up confirmation after parent corrections

26 October 2026. Read the saved replacement and corresponding main LR again.
All three requested semantic corrections are present:

* Wilkening's QTG/amplitude-amplification algorithm is explicitly separated
  from its fractional-greedy QBnB benchmarking comparison.
* The paragraph and comparison table distinguish published primitives and
  released simulator/resource models from a reconstructed matched LP oracle.
* The prefix predicate is described as the LP relaxation excluding an integer
  target, rather than certifying actual integer-completion existence.

The smaller Hou bounded-knapsack and Hamit optional-classical-fractional-bound
scope clarifications are also present. The internal pagination caveat has been
removed from Hamit's published bibliography note, which now simply identifies
it as a workshop paper. The no-executed-divider statement remains intact.

These deltas resolve this review's circuit-source/semantics findings. No new
blocking issue was found in that scope. This is not approval of untouched
main-body claims or an independent recertification of other agents' theorems.
