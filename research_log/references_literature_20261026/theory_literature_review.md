# Independent revised-Literature-Review check — 26 October 2026

Read-only scope: `literature_replacement.tex` and the current
`paper/references.bib`. Classical/theoretical statements were checked against
the primary-source ledger `theory_reference_audit.md/json`. This review does
not approve the deliberately unchanged original body, recheck every quantum
paper, establish historical priority, or certify circuits/experimental results.

## Actionable wording

The closest-prior-work paragraph initially says that the task is reversibly
deciding whether a partial prefix can reach an integer target. This can be read
as an exact integer-completion feasibility oracle, which is stronger than the
LP-pruning predicate. Replace that clause with:

> reversibly deciding whether the LP relaxation of a partial prefix excludes an integer target

The following sentence already correctly specifies preservation of the
integer-threshold **LP-pruning** decisions. For example, a single residual item
of weight 2 and profit 3 with residual capacity 1 has LP value 3/2 but integer
optimum 0. An integer target 1 survives the LP test although no integer
completion reaches it. This is a direct algebraic scope counterexample, not a
new experiment or a defect in the correctly scoped predicate.

## Classical/theory sentence checks

* The corrected Dantzig record and weak historical LP statement fit the
  publisher metadata/abstract. No uninspected exact theorem is attributed.
* Horowitz–Sahni as an arithmetic-operation baseline fits the author's full
  text, especially Section 5. The former unqualified current-best/optimality
  claim is gone.
* KPP is used as a general monograph citation, not as a source for an invented
  theorem number or an uninspected numerical bound.
* Balas–Zemel receives the correct core-origin attribution. Pisinger1999 is
  correctly used to motivate testing over capacities and distributions.
* The descriptions of expanding-core DP (MINKNAP) and combined DP/strong
  bounds (COMBO) fit their publisher abstracts. The statement about substantive
  classical comparisons is acceptable as related-work context; if it is meant
  to imply completed empirical benchmarking of these solvers, that would need
  separate evidence. An optional ambiguity-free wording is: 'These methods
  provide stronger classical context than brute-force baselines alone.'
* The Beier–Vöcking and Dey–Dubey–Molinaro sentence preserves the necessary
  distributional qualification and does not transfer polynomial conclusions to
  the manuscript's benchmark classes. Beier's Pareto enumeration and Dey's
  best-bound B&B remain different methods from the static-prefix tree.
* The BCJ sentence identifies representation methods without calling all
  results heuristic or claiming a worst-case general-knapsack bound. This is
  consistent with its separate heuristic analysis and Section3.6 Theorem2.
* Treating Lagrangian relaxation, integer rounding of a valid upper bound,
  and interval stabbing as established tools is appropriately modest. The
  Erickson source poses minimum interval stabbing in Chapter4, printedp178;
  it does not supply the new strict-endpoint reduction proof. If maximum
  source precision is wanted, change 'an established greedy problem' to
  'an established combinatorial problem'; the source is an exercise, not a
  solved theorem presented there.
* The final positive-integer-weight/nonnegative-integer-profit, fixed-order,
  integer-threshold, coverage, capacity and workspace restrictions match the
  independently audited construction assumptions. The exclusions of numerical
  LP-value reproduction, arbitrary branching, and complete-walk implementation
  are appropriate. Capacity must remain within the construction's declared
  nonnegative integer input domain in the later formal definition.

## Bibliography check

The retained classical/theory entries match the audited real records:
`ref1`, `ref2`, `ref3`, `ref4`, `ref5`, `beier2004random`,
`pisinger1997minimal`, `martello1999combo`, `dey2021random`,
`erickson2019algorithms`, and `balas1980core`.
Dantzig now has pages266–288. The Dey citation explicitly identifies arXivv4
(16 September2021), preventing ambiguous transfer from another version.
Omission of the peripheral Martello–Toth1988 item does not break a surviving
classical/theory attribution in this revision. No genuine retained reference
was rejected merely because its full text was inaccessible.

## Decision

The classical/theoretical literature framing is supported within the stated
source-access limits. The parent corrected the integer-completion wording
during this review. A follow-up read of `literature_replacement.tex` confirms
the replacement now says that the LP relaxation excludes the target. That
resolves the substantive wording issue; the two alternative phrases remain
optional clarity edits. The original body remains outside this review and
retains the separate later-stage holds already recorded in the source audit.

Follow-up snapshot SHA256:
`literature_replacement.tex` =
`f6510a5bea0d8228604ffc7447c310c92d00a79d71f7e7f93434d7d885524465`;
`paper/references.bib` =
`a80e64f5f288e900a1a07bef25d90c35bff6fc50b4953c4cd17f8317c19c2018`.
