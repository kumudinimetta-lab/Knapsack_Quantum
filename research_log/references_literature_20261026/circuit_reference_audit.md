# Arithmetic and closest-source reference audit

26 October 2026. Main manuscript and bibliography are READ-ONLY in this
circuit-track task. No simulations were run. Proposed entries are in
`circuit_proposed_entries.bib`; complete structured decisions and source
locations are in `circuit_reference_audit.json`. Source identity checks do
not certify the manuscript's existing arithmetic/resource claims.

Graph-tool discovery returned none before targeted reads. Cached primary
manuscripts were reused. Some targeted Firecrawl primary-record requests
completed before the parent reported exhausted credits; subsequent missing
records were checked with web fallback. Failed HTML/Drive/metadata endpoints
were not treated as paper contents, and no package was installed.

## Verified identities and permitted use

| Key | Verified publication | Decision |
|---|---|---|
|`draper2000`|Thomas G. Draper, *Addition on a Quantum Computer*, arXiv:quant-ph/0008033 (2000), DOI 10.48550/arXiv.quant-ph/0008033.|Retain; preprint, not an invented journal article.|
|`vedral1996`|Vlatko Vedral, Adriano Barenco, Artur Ekert, *Quantum networks for elementary arithmetic operations*, Physical Review A 54(1),147–153 (1996), DOI 10.1103/PhysRevA.54.147.|Retain; full names/page range verified by APS citation export.|
|`barenco1995`|Adriano Barenco, Charles H. Bennett, Richard Cleve, David P. DiVincenzo, Norman Margolus, Peter Shor, Tycho Sleator, John A. Smolin, Harald Weinfurter, *Elementary gates for quantum computation*, Physical Review A 52(5),3457–3467 (1995), DOI 10.1103/PhysRevA.52.3457.|Retain; add DOI and full page range.|
|`thapliyal2016`|Himanshu Thapliyal, T. S. S. Varun, Edgard Munoz-Coreas, *Quantum Circuit Design of Integer Division Optimizing Ancillary Qubits and T-Count*, arXiv:1609.01241 (2016), DOI 10.48550/arXiv.1609.01241.|Retain existing key during this staged revision; real source, current divider implementation attribution remains unsupported.|
|`cuccaro2004`|Steven A. Cuccaro, Thomas G. Draper, Samuel A. Kutin, David Petrie Moulton, *A new quantum ripple-carry addition circuit*, arXiv:quant-ph/0410184 (2004), DOI 10.48550/arXiv.quant-ph/0410184.|Add as arithmetic background; do not invent a journal venue.|
|`hou2020`|Wenjun Hou, Marek Perkowski, *Quantum-based algorithm and circuit design for bounded Knapsack optimization problem*, Quantum Information and Computation 20(9–10),766–786 (2020), DOI 10.26421/QIC20.9-10-4.|Add as constructive oracle prior work.|
|`hamitouche2025`|Monsef Hamitouche, Faicel Hnaien, Djamel Eddine Menacer, *Towards a Quantum Resolution of the Knapsack Problem*, in PRICAI 2025 Workshop on Quantum Computing for Search and Optimization Problems proceedings, CDMTCS Research Report CDMTCS-586, University of Auckland (2025).|Add as workshop/report work. Paper-local pp.1–14; no invented DOI or continuous proceedings page range.|
|`wilkening2025`|Sören Wilkening, Andreea-Iulia Lefterovici, Lennart Binkowski, Michael Perk, Sándor P. Fekete, Tobias J. Osborne, *A quantum algorithm for solving 0-1 Knapsack problems*, npj Quantum Information 11,article146 (2025), DOI 10.1038/s41534-025-01097-8.|Add as closest substantive prior work; published 26 August 2025.|
|`wilkening2025code`|Same six creators, same title, Zenodo software/experiment data, version R1,18 August 2025, DOI 10.5281/zenodo.16895828.|Add where the released implementation audit is discussed. Use pinned-version DOI, not all-version DOI16895827.|

Primary metadata links: [Draper](https://arxiv.org/abs/quant-ph/0008033),
[VBE APS export](https://journals.aps.org/pra/export/10.1103/PhysRevA.54.147?type=bibtex&download=true),
[Barenco APS](https://doi.org/10.1103/PhysRevA.52.3457),
[coauthor's primary page confirming Barenco pagination](https://math.mit.edu/~shor/elecpubs.html),
[Thapliyal2016](https://arxiv.org/abs/1609.01241),
[Cuccaro](https://arxiv.org/abs/quant-ph/0410184),
[Hou publisher record](https://doi.org/10.26421/QIC20.9-10-4),
[Auckland proceedings](https://www.cs.auckland.ac.nz/research/groups/CDMTCS/researchreports/download.php?selected-id=904),
[Wilkening publisher record](https://www.nature.com/articles/s41534-025-01097-8),
[R1 record](https://zenodo.org/records/16895828).

## Method evidence and its limits

**Draper.** Sections3/5 and equations(1)–(2) derive the QFT representation
and addition using mutually commuting phase rotations. The absence of a
temporary carry register is an ADDER property. It does not establish zero
workspace for comparison, flag aggregation, LP arithmetic or a complete
oracle. The approximate-QFT discussion is separate from the ideal full-QFT
engine used in this project. Primary full text:
[quant-ph/0008033v1](https://arxiv.org/html/quant-ph/0008033v1).

**VBE.** SectionIII.1/equation(9) gives reversible in-place addition with
explicit overflow and work registers. SectionIII.3 constructs a controlled
constant multiplier modulo N by shifted conditional additions. The full
arithmetic and uncomputation assumptions must accompany any use of its
resource constants. Our new repeated-addition compiler is not automatically
the same modular multiplier merely because the general strategy is related.
Primary [full text](https://arxiv.org/html/quant-ph/9511018v1).

**Barenco.** Lemma5.1 has an SU(2) condition; determinant phases need separate
treatment. Lemma6.1 chooses V with V²=U and implements doubly controlled U
using controlled-V/V† blocks and XOR gates. These are not three arbitrary
SINGLE-qubit synthesis rotations. Corollary6.2 counts elementary gates;
Section6.2 explicitly distinguishes relative-phase alternatives. This source
does not itself supply a Ross–Selinger precision/T-count estimate.
Primary [full text](https://arxiv.org/html/quant-ph/9503016v1).

**Thapliyal.** The real 2016 arXiv abstract describes a restoring integer
divider using conditional addition and subtraction in Clifford+T. This
supports a divider-background citation. The 2016 full HTML fetch failed,
so no detailed register-mapping lemma is certified here. The cached
2018 arXiv1809.09732 paper has a different title and four authors including
Travis S. Humble; it must not silently replace the 2016 three-author record.
Retaining a legitimate cited work is appropriate while its stale body use
awaits the separately authorized rewrite.

**Cuccaro.** Section2 gives the basic MAJ/UMA construction; Section3 optimizes
it, and Section4 gives variants. The compact control in this project was
derived from the simpler Section2 recurrence. Do not attach Section3's best
constants to that simpler implementation, or expand one adder's single
carry ancilla into a full-oracle one-ancilla assertion. Primary
[full text](https://arxiv.org/html/quant-ph/0410184v1).

**Hou–Perkowski.** Sections4–8 construct a bounded-knapsack decision oracle
from comparisons, in-place constant additions and constant multipliers.
Section10/Table10.1 describe local Q# simulator tests; Section11 analyzes
gate usage. This is concrete constructive prior work, not merely a proposal
to apply Grover abstractly. It is not our static prefix LP-pruning bank, and
the source's broad priority wording should not be repeated as an established
historical fact. [Publisher-linked primary PDF](https://www.rintonpress.com/xxqic20/qic-20-910/0766-0786.pdf).

**Hamitouche–Hnaien–Menacer.** The official proceedings paper spans PDF
pages19–32, with its own printed pages1–14. Section4 gives reversible
capacity/improvement oracles. Section5/Algorithm1 step1 computes a classical
upper bound, explicitly allowing a fractional-knapsack bound, before Grover
search; its enhanced variant reuses work registers. Section7 reports
noiseless simulation limits. Thus hybrid branching, fractional-bound pruning
and ancilla reuse are already relevant prior work. This is not a demonstrated
coherent LP-prefix bank. No DOI was identified in the primary PDF/program.
The cover's April2025 date and the official November2025 workshop schedule
differ, so cite year only. It is a university workshop-report proceeding,
not a journal article or an asserted Springer LNAI publication.

**Wilkening/R1.** The published QTG uses amplitude amplification; describing
all QTG approaches solely as QAOA would omit this work. SupplementE.3–E.5
gives QFT arithmetic and constant comparisons, and F.2 already uses the
fractional-greedy bound within QBnB benchmarking. Its benchmark assumptions
and modeled cycles are not measured hardware runtime. The inspected R1
QBnB call path uses a classical bound and numerical resource routines; the
separate specialized QTG simulator is real executable implementation. The
bounded absence of a clean LP-oracle netlist in that path does not prove
absence everywhere. Our serial quantum-threshold LP completion is OUR
reconstruction using published primitives, not the authors' released or
optimized oracle. Primary [supplement](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41534-025-01097-8/MediaObjects/41534_2025_1097_MOESM1_ESM.pdf)
and [R1 source](https://github.com/SoerenWilkening/QTG_0-1Knapsack/tree/R1).

## Stale body uses to flag, not certify or edit at this stage

Locations below refer to `paper/main.tex` as read before the parent's LR edits;
subsequent line numbers may shift.

* Line263: implemented Thapliyal divider/VBE multiplier and remainder-to-ancilla
  mapping do not describe the new bank construction. A real citation cannot
  substitute for implementing and testing those blocks.
* Line280: the claimed Barenco three-rotation T-cost convention requires its
  own decomposition/synthesis/error-budget derivation.
* Line310: no carry ancilla for QFT addition does not imply no extra workspace
  for the entire oracle.
* Lines98–103: any closest-work/uniqueness table must acknowledge published
  fractional-pruning QBnB benchmarking, constructive Grover decision oracles,
  and the workshop's classical-bound/Grover hybrid. No first/unique claim is
  established by this audit.

No bibliography-only correction resolves contradictory old h/V synthesis,
hardware, query/runtime or spectral claims elsewhere in the manuscript.
Those body claims remain outside this revision stage.

## Concise LR wording available to the parent

Constructive knapsack oracles precede this work: Hou and Perkowski give a
bounded-knapsack decision circuit and Q\# simulator tests, while Hamitouche
et al. combine classical upper-bound pruning with Grover-based completion
search and work-register reuse. Wilkening et al.'s QTG uses amplitude
amplification, and their QBnB benchmarks already employ fractional-greedy
bounds. These works motivate a narrower distinction: compiling a specified
integer-threshold LP-pruning predicate into a static affine bank and
comparing complete reversible predicates under a matched interface.

Standard reversible arithmetic is an ingredient, with addition and
multiplication constructions due to Vedral et al., QFT addition due to
Draper, ripple-carry addition due to Cuccaro et al., and controlled-gate
decompositions due to Barenco et al. Comparisons reconstructed from these
primitives should be identified as reconstructions, rather than performance
benchmarks of a released full LP-oracle implementation.
