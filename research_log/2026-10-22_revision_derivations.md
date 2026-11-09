# Revision derivations and rejected claims

Date: 2026-10-22. The user's follow-up explicitly authorizes resolving the
previous integrity stop and correcting both code and manuscript. This document
records the derivation pass before implementation and before manuscript approval.
Historical data and logs are preserved. New results will use separate filenames.

## Sources inspected before circuit authoring

Primary sources retrieved through Firecrawl are cached in `.firecrawl/`.

- Ashley Montanaro, *Quantum-Walk Speedup of Backtracking Algorithms*, Theory
  of Computing 14(15), 1-24 (2018), DOI 10.4086/toc.2018.v014a015. Published
  Theorem 1.1: detection given an upper bound T, O(sqrt(T*n) log(1/delta))
  predicate/branching queries. Theorem 1.2: witness finding, with an additional
  n log n overhead in the general case. These are different statements.
- Ashley Montanaro, *Quantum speedup of branch-and-bound algorithms*, Physical
  Review Research 2, 013056 (2020), DOI 10.1103/PhysRevResearch.2.013056.
  The full primary text describes tree-size estimation and witness search;
  the previous manuscript's O(sqrt(T)*d*log d) detection attribution is rejected.
- Himanshu Thapliyal, T. S. S. Varun, Edgard Munoz-Coreas, *Quantum Circuit
  Design of Integer Division Optimizing Ancillary Qubits and T-Count*, arXiv
  1609.01241 (2016): verified as an actual preprint, not a journal publication.
  Its existence does not establish that the repository's divider matches it.
- The separately verified *Quantum Circuit Designs of Integer Division
  Optimizing T-count and T-depth*, arXiv:1809.09732 (2018), has four authors
  (Thapliyal, Munoz-Coreas, Varun, Humble) and must not be conflated with the
  similarly named 2017 iNIS proceedings contribution, DOI 10.1109/iNIS.2017.34.
- Thomas G. Draper, *Addition on a Quantum Computer*, arXiv quant-ph/0008033
  (2000); Vlatko Vedral, Adriano Barenco, Artur Ekert, *Quantum Networks for
  Elementary Arithmetic Operations*, Physical Review A 54, 147-153 (1996),
  arXiv quant-ph/9511018. Metadata verified from author-hosted arXiv records.
  Any new Boolean circuit is described as such, without claiming identity to
  an unverified implementation of one of these named arithmetic networks.

## Fixed-point lemma: derivation before new simulation code

Assume positive integer item weights/values and integer capacity. Sort item
efficiencies by exact rational comparison; truncation must not reorder items.
At any feasible node or forced-item LP subproblem, the bound is
U = P + r*v_s/w_s, where P is an integer and 0 <= r < w_s <= Wmax.
If no fractional split exists, U=P and no efficiency truncation is needed.
Let q_s=floor(2^k*v_s/w_s) and U_tilde=P+r*q_s/2^k.

1. 0 <= v_s/w_s - q_s/2^k < 2^(-k).
2. 0 <= U-U_tilde = r*(v_s/w_s-q_s/2^k) < Wmax*2^(-k).
   Thus epsilon(k)=Wmax*2^(-k) is a uniform strict error bound.
3. For integer threshold tau, if U<tau then tau-U is a positive rational
   multiple of 1/w_s, so tau-U >= 1/Wmax = g. Integral U has gap at least 1.
4. Use U_tilde <= tau-g to prune, not U_tilde<tau.
5. If U<tau, then U_tilde<=U<=tau-g and pruning occurs.
6. If U>=tau and epsilon(k)<g, then U_tilde>U-epsilon(k)>tau-g and pruning
   does not occur. Equality U=tau is therefore safe.
7. Therefore the robust predicate equals the exact U<tau predicate under
   2^k>Wmax^2. Apply it with tau=Z_LB for fixing and with each search threshold
   for node pruning. Forced-in integer values are included in P.
8. Integer implementation: A=2^k*P+r*q_s and
   H=floor((tau*2^k*Wmax-2^k)/Wmax); prune iff A<=H.
   Division in H is classical integer arithmetic; q_i are precomputed exactly
   from fixed problem data. Coherent arithmetic need not divide variable inputs.

The task addendum's requested "iff epsilon(k)<gap floor" is NOT asserted as
an instancewise necessity. Counterexample: all encountered efficiencies dyadic,
or all bounds integral. Truncation can be exact at a smaller k. The condition is
a sufficient uniform guarantee, not a necessary condition for every instance.
This failed necessity interpretation is retained here rather than fabricated.

Adversarial equality example retained from the earlier log: w=[4,7,6],
v=[5,6,2], W=7, Z_LB=6. Excluding item (7,6) gives U=5+3*(2/6)=6.
Floor truncation of 1/3 gives U_tilde<6 at every finite k; naive pruning is
unsafe. The robust threshold with adequate k avoids it. Lower precision can
fail: Wmax=5,k=2,r=3,v_s=2,w_s=5,P=tau-1 yields U=tau+1/5 but
U_tilde=tau-1/4. Both failures must be included in the new audit tests.

This derivation guarantees pruning decisions, not exact rational values, nor
correct sorting under rounded efficiencies, nor absence of register overflow,
nor correctness of an untested circuit, nor an end-to-end quantum speedup.

## Witness recovery and composition derivation

Let S=sum(core values), L=ceil(log2(S+1)), m=core size and M=L+m.
Binary search the maximum achievable integer value using at most L detections.
With target Z, recover an assignment in m steps: test whether the current
prefix extended by zero has any feasible completion of value >=Z; choose zero
if yes and one otherwise. Include the prefix's accrued value and weight in
each residual threshold/capacity. Handle infeasible and empty residual problems
classically, and validate the final witness against capacity and target.

If every detection is correct, induction keeps a target-achieving completion
under the chosen prefix, ending at an optimal witness. Give each call failure
probability delta/M (for M>0). The adaptive union bound is at most delta.
Independent repetition is not silently substituted for this allocation.

With a supplied certified bound B covering EVERY queried threshold tree and
prefix tree, Theorem 1.1 gives total
O(sqrt(B*max(1,m))*(L+m)*log((L+m)/delta)) oracle queries.
B=2^(m+1)-1 is always safe. Smaller B requires certification; obtaining that
certificate is not free. The simulator enumerates trees explicitly and its
classical construction cost is excluded from this conditional query bound.
This conservative expression is not Montanaro 2020's adaptive tree-counting
algorithm and makes no generic instance-adaptive advantage claim.

The simulator's K*(2^s-1) is SCHEDULED, since s is chosen from T and depth.
Regressing it on those same variables is CIRCULAR_VALIDATION; such a fit is
excluded from the revised paper. Analytical acceptance probabilities and
deterministic majority probabilities are SIMULATED, not hardware observations.

## Integer necessity-construction candidate (requires separate check)

The old rational values/capacity construction is rejected as outside the
defined integer problem class. No scaled variant is accepted without checking
its actual gap. A replacement will only be used after a separate exact check;
otherwise the stronger necessity claim will be removed, not presumed true.

First candidate checked w_i=2*n^2+i, v_i=2 and residual capacity n^2.
It has a bounded gap converging to one, but that alone does not disprove an
arbitrary function of the exact gap (a function could diverge near one).
Reject that stronger inference. This is a retained failed attempt.

Revised candidate: n>=2, q=floor(n/2), M=2*n^2,
w_i=2*(M+i), v_i=2, W=sum_{i=1}^q w_i+(M+q+1).
The remaining capacity is exactly half of w_(q+1), giving LP gap exactly one.
The difference between the heaviest and lightest q-subset weights is
2*q*(n-q)<=n^2/2 < M+q+1, so EVERY q-subset fits. The lightest (q+1)-subset
does not fit, since w_(q+1)=2*(M+q+1) exceeds that residual capacity.
Consequently Z*=Z_LB=2*q and each item can be both included and excluded in
some optimum; exact forced-item LP checks cannot fix any variable. Thus core
size n is unbounded at the SAME exact gap of one, with integer data and distinct
efficiencies e_i=1/(M+i). This proves failure of a bound depending on the gap
alone. It does not rule out bounds using weights, spacing or other structure.

## Additional audit findings and repairs

- The old benchmark correctness flag is hardcoded true above n=20. Its 700
  flags are not accepted as verification. A new exact-DP audit checks all 700.
- The old core-ratio table does not match regenerated seed-specific ratios.
  Replace it with new exact results; retain the historical file unchanged.
- The old tree-size regression fits T_full, not the reduced-core tree T_core,
  and silently adds 1e-6 to zero gaps. Any retained regression is regenerated
  against the specified dependent variable and explicitly counts zero gaps.
- The old spectral script uses np.linalg.eig without orthonormalizing degenerate
  eigenspaces. Replace the new audit path with orthogonal real Schur blocks and
  check spectral acceptance against direct walk iteration. No old raw file is
  overwritten. Historical 889-tree results are not silently called reverified.
- Archived IBM records lack job IDs/circuit hashes. They cannot independently
  establish execution of the current answer-agnostic circuit. Do not use them
  as validation of the proposed algorithm or infer a universal hardware boundary.
- A dense statevector is not required for a permutation-only X/CX/CCX circuit:
  exact sparse columns track basis labels and amplitudes through every gate.
  New oracle checks exhaust all prefix, threshold and target inputs at depth 3,
  with clean workspace, for all 700 benchmark instances. This does NOT check
  every depth on those 700 instances. Three explicitly listed small instances
  are additionally checked at every depth; a separate dense Qiskit statevector
  check uses a 25-qubit one-item circuit. The manuscript must keep these scopes.

## Journal instructions

Official QIP instructions at link.springer.com/journal/11128/submission-guidelines
were read. Journal-specific front matter says abstract 80-100 words and 4-6
keywords; generic title-page boilerplate elsewhere says 150-250. Use the
journal-specific 80-100 requirement and record the discrepancy. Editable LaTeX
and a PDF are requested. Author contributions and competing interests are
required through the submission interface. The user's reply names Madhavi as
the probable corresponding author; final designation and factual declarations
are pending. Do not invent funding, conflicts, or contributions.
