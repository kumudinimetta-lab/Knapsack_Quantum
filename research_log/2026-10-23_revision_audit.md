# Revision audit and evidence ledger

Date: 23 October 2026, Asia/Calcutta. This follows the user's explicit request
to resolve the discrepancies recorded in the 22 October integrity stop.

## Resolutions

1. **Missing witness:** `quantum_bb_optimize` now returns a recovered assignment,
   its validity flag, and recovery-call counts. Threshold and prefix decisions
   never use a classical optimum. DP checks only the final result. Empty marked
   roots are handled correctly. Algorithm 2, Theorem 1 and Proposition 1 now
   specify recovery and adaptive error allocation. The theorem is conditional
   on the cited detector and certified B, not a guarantee inferred from a
   calibrated simulation constant.
2. **Wrong query attribution:** the published primary source is Montanaro 2018,
   Theorem 1.1 for detection and Theorem 1.2 for witness finding. The previous
   O(sqrt(T)*m*log m) detector attribution was removed. B covers every queried
   value and recovery tree. The manuscript discloses tree-certificate cost.
   Montanaro 2020's adaptive tree-counting algorithm is not claimed implemented.
3. **Integer counterexample:** the rational family was replaced by the integer
   fixed-gap-one construction in the derivation log. It was separately checked
   exactly at n=2..100: no failures. The abandoned bounded-but-varying-gap
   candidate is retained in the log, including why it did not prove the desired
   impossibility statement.
4. **Rounding:** the manuscript derives the error, rational threshold gap and
   robust predicate for every integer threshold. It explicitly rejects naive
   truncation at equality and does not assert that the sufficient precision is
   necessary on each instance. The new separate exact falsification pass checked
   84,794 arithmetic cases with zero failures, plus 4,141 dual/containment checks
   across 1,000 generated instances with zero failures.
5. **Reversible node circuit:** a new explicit Boolean arithmetic circuit family
   uses X, CX and CCX gates, exact compiled coefficients, sufficient widths and
   compute-copy-uncompute. No unverified claim that it matches an optimized
   named divider is made. New sparse statevector tests exhaust all depth-three
   prefix/threshold/target inputs on the unchanged 700-instance generator set.
   This is not falsely described as all-depth testing on 700 instances or an
   end-to-end walk. Three small all-depth tests and an independent dense Qiskit
   check are separately identified. The old 96-qubit/clipped-input experiment
   is not used to validate the new circuit or an exact LP bound.
6. **Classical benchmark:** all 700 cases are rechecked against DP, rather than
   trusting the old hardcoded correctness flags for n>20. The fixing-ratio
   table and classical core node counts were replaced with the exact rerun.
   Subset-sum cases are not described as intrinsically hard merely because
   their core remains large.
7. **Spectra:** the new audit uses orthogonal real Schur blocks, not a possibly
   nonorthogonal degenerate eigenvector basis. Direct sparse walk iteration
   independently checks acceptance. All 1,200 R=50 conditions are recorded;
   889 complete, with zero endpoint violations and detection disagreements.
   Capped/trivial/bypassed conditions remain counted. No minimum-gap claim or
   empirical asymptotic optimization-complexity claim is inferred.
8. **Regression:** the previous fit used T_full while calling it a reduced-core
   LP tree, and inserted epsilon into zero gaps. The new fit uses actual exact
   core-solver node counts, explicitly counts the 141 zero gaps, and groups
   equal n/seed configurations across classes in CV. It is exploratory. Legacy
   query-budget regressions are CIRCULAR_VALIDATION and are excluded, not rerun
   as evidence for the paper.
9. **Large coefficients:** a new 45-case R=10^6 experiment adds independent exact
   meet-in-the-middle comparisons. Nine B&B caps are retained. COMBO is cited
   accurately as an untested specialized baseline, not claimed beaten.
10. **Hardware:** archived IBM summaries cannot establish circuit provenance.
    The revised paper excludes them from algorithm validation and removes the
    claimed universal size/noise boundary. No new hardware run is claimed.
11. **Crossover:** old heuristic T counts are not measured or certified lower
    bounds; controlled phases are not Toffolis, and T gates are not classical
    nodes. Unsupported numerical crossover claims were removed.
12. **Related work:** verified Wilkening 2025, Creemers--Perez Armas 2025, and
    Bozejko et al. (online 2024, issue 2026) were added with technical comparisons.
    QTG is not falsely labeled purely variational or without guarantees. Broad
    uniqueness/first/best claims were removed. Unused unverified references were
    excluded from the revised bibliography; their old text remains in backups.
13. **Journal form:** official Springer class/style; 89-word abstract; six keywords;
    supplied author order preserved. Madhavi is provisional corresponding author.
    Funding, interests and contributions are pending, explicitly stated. AI use
    beyond copy editing is disclosed. No facts about grants/contributions were
    invented. The source has not been uploaded to the public repository.

## Failures, revisions and unused attempts retained

- Graph-tool discovery returned no applicable tools. Filesystem fallback was
  necessary and announced, rather than claiming a graph audit occurred.
- Firecrawl initially failed under restricted network access (ENOTFOUND).
  Approved escalated access successfully retrieved primary sources.
- Console printing initially hit Windows cp1252 Unicode errors. UTF-8 output
  was selected; this did not alter any source or experimental input.
- The first node-resource JSON used the same `depth` key for prefix depth and
  gate depth. Copies ending `attempt1_metadata_collision.json` preserve those
  outputs. The schema was corrected to `gate_depth` and results regenerated
  from code. No raw values were manually patched.
- An initial fresh spectral run used R=100, not the old spectral R=50. Its full
  1,200-condition output is preserved as `spectral_R100_results.json`: 945
  completed, no checked endpoint violations/disagreements. The manuscript
  instead uses a separately regenerated R=50 run matching the original set.
- The new dense cross-check used a 25-qubit circuit; it is not misrepresented
  as a dense simulation of the much wider main benchmark circuits.
- The first Springer compile failed on inherited `resizebox` wrappers nested
  inside the class's `threeparttable`. Those wrappers were removed. A later
  alignment failure exposed a leftover notes cell after reducing table columns;
  it was corrected. BibTeX initially found duplicate style commands because the
  class already selected its style; the redundant command was removed. These
  were layout/build failures, not suppressed mathematical failures.
- A first patch combining delete/add of the same path was rejected atomically;
  no partial edits from that patch were assumed. The edits were reapplied as
  ordinary updates. A build command initially used the wrong working directory
  for the editing script; the script was then run from the repository root.

## Primary-source map

| Claim/use | Exact source and assumptions | Implementation mapping / limit |
|---|---|---|
| Fixed-tree detection | Montanaro, Theory of Computing 14(15), 2018, Theorem 1.1; known tree-size upper bound, Boolean domain, coherent predicate/branching access, failure eta | Source n -> core m; source T -> supplied B; source delta -> per-call delta/(L+m). Source branching h -> next-item rule, distinct from our LP h. No free B certificate or runtime claim. |
| Witness distinction | Same source Theorem 1.2 and Section 2.3 | Paper gives an explicit conservative self-reduction using Theorem 1.1 instead of pretending detection returns a witness. |
| Spectral tests | Same source Lemma 2.1 and proof of Lemma 2.4 | W=R_B R_A; eigenphase phi=2 theta. mu(phi)<=phi^2*T*m/4 at specified cutoffs; marked phase-zero root weight >=1/2. This is not a minimum spectral gap. |
| Amplitude amplification | Brassard, Hoyer, Mosca, Tapp, Contemporary Mathematics 305, 53-74 (2002), Theorem 3 | Positive initial good-state probability; measurement-free preparation and inverse, supplied good-state predicate. Not a full optimum-recovery theorem. |
| Adaptive B&B | Montanaro, Physical Review Research 2, 013056 (2020) | Context/comparison only; not falsely equated to our simulator. |
| Reversible arithmetic | Vedral--Barenco--Ekert, Physical Review A 54, 147-153 (1996); Draper, arXiv quant-ph/0008033 (2000); Thapliyal--Varun--Munoz-Coreas, arXiv 1609.01241 (2016) | Existence/background, not inherited optimized resource guarantees. New Boolean network precomputes fixed division constants. |

Sources and official publisher instructions are cached in `.firecrawl/` and
linked through verified bibliography entries and the reproduction guide. A
primary source verifying an old related-work citation does not validate a
claim about that source's algorithm unless its content supports the claim.

## Remaining scope limits

The full walk circuit, a universal calibration guarantee, a tight automatically
certified small B, COMBO comparisons, and physical quantum acceleration are not
completed research achievements and are not claimed as such in the revised
paper. Factual author declarations still require author input. These limits
cannot be repaired by invented results or stronger wording.

## Final coherent-depth composition

After the fixed-depth checks, a clean depth-dispatch wrapper was implemented
and separately tested. It computes each fixed-depth flag into a private bit,
copies it to the output conditioned on the binary depth encoding, and applies
the same clean XOR predicate again to clear the private bit. Reused workspace
is clean between blocks. Depth-equality work bits are uncomputed at the end;
invalid depth encodings are explicitly rejected. Since the depth flags are
mutually exclusive, this composes coherently on superpositions of depth and
prefix assignments. It does not implement the walk reflections.

The three explicit small instances in the manuscript, at k=5,7,6, respectively,
were checked on all 8192,8192,1024 prefix/depth/threshold/target basis columns:
zero predicate mismatches and zero dirty-workspace columns (SIMULATED).
For the first four-item instance, the coherent circuit has 591 qubits, 9228
X/CX/CCX gates and depth 1622 (DERIVED gate-list counts). These replace no old
raw data; the new results are in `revision_20261023_coherent_h_results.json`.
The manuscript now states that depth dispatch is implemented on the tested
small instances. Only composition with the full walk remains future work.

The final binomial-tail calculation also uses a stable survival function and
separate logarithms, avoiding overflow at very small requested error budgets.
A 1e-300-budget two-item smoke check returned a valid optimum; this is a
numerical robustness check, not a universal detector error certificate.

## Delivery checks

The final source compiles to 19 pages with no undefined citations/references,
overfull boxes, duplicate destinations, or LaTeX errors. Every final page is
pixel-identical to the rendered pages inspected during PDF QA; extracted text
stays within the page boundaries. The abstract has 89 words, six keywords, and
15 cited bibliography entries. All 16 archived timing-table rows were checked
against the retained raw records. The final consistency JSON records these
counts and the exact manuscript source hash.

The full reproduction entry point completed successfully, including the new
coherent-depth tests. The recovery tests were rerun after aligning the precision
schedule's depth parameter with the root diffusion depth bound: 135 configurations,
zero value/witness mismatches and zero caps. Tests of the unchanged arithmetic
and walk-construction paths did not need different numerical claims.

No historical experimental JSON was manually modified. The broad `git diff
--check` command treated the tracked PDF as text and emitted irrelevant binary
whitespace diagnostics; the source-only check passes. Generated bytecode is
restored to its starting tracked contents without changing Git index state.
The working tree's existing uncommitted author changes were not reset.

A transient Windows invalid-argument error occurred while rewriting the LaTeX
source; the file remained present and a subsequent ordinary retry succeeded.
No failed write was assumed successful. The final source hash and compilation
were checked afterward.
