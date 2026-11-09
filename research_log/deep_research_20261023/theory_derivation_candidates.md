# Theory-track derivation pass (23 October 2026)

Status: candidate derivations, NOT independent approval of a new central claim.
The restored manuscript and existing code/raw data are unchanged. Graph tools
were discovered first; no relevant graph tool was exposed, so targeted reads
were used. This pass uses the Firecrawl and Firecrawl Research Papers skills.

## Root dual certificate, from weak duality rather than a desired result

Assume positive integer weights w_i, nonnegative integer profits v_i, capacity
W >= 0, and arbitrary fixed variable order pi. A prefix fixes x_i for i in S.
Reject overweight prefixes separately. The residual optimization LP is the
ordinary fractional 0/1 knapsack on the unassigned items.

Choose ANY nonnegative rational multiplier lambda=a/b, with a>=0 and b>0.
Define signed integer reduced costs r_i=b*v_i-a*w_i, preferred bit
z_i=1[r_i>0] (zero-cost ties may choose either bit), costs c_i=abs(r_i),
and root dual numerator A=a*W+sum_i max(r_i,0). Define prefix penalty
D_S=sum_{i in S} c_i*1[x_i != z_i].

For every feasible completion x of the prefix,

1. b*sum_i v_i*x_i = a*sum_i w_i*x_i + sum_i r_i*x_i.
2. a*sum_i w_i*x_i <= a*W since a>=0.
3. sum_i r_i*x_i <= sum_i max(r_i,0)-D_S; unassigned terms are independently
   bounded by their better endpoint, while assigned terms incur exactly the
   stated nonnegative penalty.
4. Therefore total profit <= (A-D_S)/b. The argument also applies to fractional
   residual completions because the unassigned variables lie in [0,1].
5. For integer target tau, safe reject iff A-D_S < b*tau, equivalently
   D_S > A-b*tau. Equality must remain alive. The product is all integer;
   there is no fixed-point loss or variable division in this predicate.

If lambda is a root LP-optimal multiplier (a split-item density; lambda=0
if all items fit), A/b equals the root LP upper bound. Optimality of lambda
is useful for tightness but NOT required for correctness. Efficiency ties do
not affect validity. This is a standard Lagrangian/reduced-cost identity, not
a new theorem. See Dey--Dubey--Molinaro, arXiv:2007.15192v4, Section 3,
equations (2)--(3), and Section 4 equation (6), for the directly overlapping
classical reduced-cost construction.

## Candidate exact state-count certificate for a STATIC prefix tree

Fix target tau, multiplier lambda, variable order pi and budget
H=A-b*tau. For depth d define
N_d(H)=#{Y subset of {pi(1),...,pi(d)}: sum_{i in Y} c_i <= H}.
This counts surviving prefixes of the dual-budget predicate before any capacity
pruning. For H<0 it is zero at every depth, including the root. For H>=0,
N_0=1. Each prefix corresponds bijectively to its set of deviations from z.
The pure dual-budget tree has sum_{d=0}^n N_d(H) nodes. Its capacity-pruned tree
has at most this many, and an exact-LP-pruned tree with the same order has at
most this many, since residual LP <= (A-D_S)/b. If an implementation retains
a rejected child as an explicitly represented leaf, count it consistently:
1+2*sum_{d=0}^{n-1} N_d(H) is a conservative bound for the generated binary
tree INCLUDING those rejected child leaves. It is at most the full-tree bound
2^(n+1)-1, so take the minimum. This distinction is essential when mapping to
a quantum tree oracle.

N_d can be computed with integer subset-sum counting DP after dividing all
positive c_i and H by their gcd where applicable. This is pseudopolynomial
in H (and O(n*H) arithmetic operations in the unscaled recurrence), not free
polynomial preprocessing in the bit length. Counts have O(n) bits. Large H
can make this an impractical certificate; a cheap envelope is needed before
claiming quantum benefit.

For a cheap but looser deterministic envelope, choose a positive cutoff t.
Let s_d(t)=#{i among first d: c_i<t}; every other deviation costs at least t,
so there are at most floor(H/t) such deviations. Consequently
N_d(H) <= 2^s_d(t) * sum_{j=0}^{min(d-s_d(t), floor(H/t))} binom(d-s_d(t),j).
For H>=0 choose t from the finitely many positive costs plus 1, optimize by
enumerating these t, and cap by 2^d. Zero-cost variables are always in s_d.
Computing this envelope uses only counts, binomial coefficients and integers;
it may be exponentially loose and must be tested rather than praised.

This certificate is a transparent specialization/extension to a fixed prefix
tree of the known reduced-cost counting framework. PRIORITY UNRESOLVED.
Dey et al. Theorem 3 gives 2*n*|G|+1 for their best-bound-first optimization
tree. That theorem must NOT be directly substituted for a fixed threshold
tree or for arbitrary prefix recovery calls. The above direct counting is
being derived precisely because the tree semantics differ.

If all optimization calls use tau >= L+1 for a known feasible incumbent L,
H_max=A-b*(L+1) covers them. Prefix-restricted witness calls use the same
original costs and cumulative original-prefix penalty and are subtrees of
the root dual-budget tree at the weaker target L+1. This observation needs
independent review before changing an algorithm or theorem. A saved incumbent
witness handles the case optimum=L; it must not be discarded. Targets below
L+1 are NOT covered by this certificate.

## Attempts to falsify / limitation examples BEFORE pilot code

1. Invalid negative multiplier: a<0 reverses the use of the capacity inequality;
   the claimed bound can underestimate feasible profits. Restrict a>=0.
2. Equality pruning using >= instead of > for penalty: one item w=v=W=tau=1,
   lambda=1 yields A=1,D=0,H=0. Rejecting equality discards a valid optimum.
3. Ties / subset sum: v_i=w_i and lambda=1 imply every c_i=0. For tau<=W,
   the dual budget prunes NOTHING by objective, regardless of how small the
   root LP--integer gap is. Capacity checks and leaf objective checks remain
   necessary. This supplies a known hard regime for this certificate.
4. All-fit case: lambda=0 yields A=sum(v_i), and excluding an item subtracts
   v_i. This is valid and equivalent to the unconstrained remaining-profit
   bound; a nonexistent split item must not be dereferenced.
5. Infeasible prefix: a finite dual number is not an infeasibility certificate;
   reject weight>W explicitly before classifying a node feasible or marked.
6. Nonoptimal lambda: safe but possibly useless, e.g., lambda=0 with very small
   W allows sum(v_i) even when most items cannot fit. Tightness is empirical.
7. Stronger does not necessarily mean cheaper: evaluating several lambda
   values and taking min gives a valid tighter bound, but every additional
   accumulator and comparison increases reversible work. No net win assumed.
8. End-to-end benefit: fewer predicate gates alone does not imply fewer total
   gates if weaker pruning enlarges the tree. Compare the matched products
   involving certified/actual tree and full walk cost, not standalone oracles.

## Circuit-agent exact cross-product proposal: independent algebra audit

If residual LP scan produces exact integral P, residual 0<=r<w_s, and split
item positive w_s, its LP bound is U=P+r*v_s/w_s. For arbitrary integer target
tau, U<tau iff P*w_s+r*v_s<tau*w_s. This is an exact arithmetic identity,
NOT evidence of novelty; it bypasses fixed-point truncation entirely. It
requires sufficiently wide exact registers, a reversible correct scan,
correct split selection, and clean uncomputation. Ties need any deterministic
exact efficiency order; equality must not prune. For all-fit residuals compare
the integral bound P directly or use a flagged denominator-one representation.
Overweight prefixes and invalid encodings require explicit semantics. A finite
scan must ignore assigned suffix bits and handle depth in superposition.
I find no algebraic failure under those conditions, but this pass does not
approve the circuit implementation. Cross-product arithmetic itself is known.

## Candidate ranking before measurements

1. Root-dual versus exact LP oracle: low implementation risk, unknown result,
   useful negative outcome if cheaper predicates cause prohibitive tree growth.
   Creativity would lie in a principled quantum resource/pruning tradeoff and
   an improved construction, not inventing the Lagrangian identity.
2. Certified threshold/recovery envelope: feasible cheap integer bound above;
   its usefulness and nontriviality relative to existing work are uncertain.
   If vacuous, report where and why, instead of asserting a new advantage.
3. Multi-dual bank / depth-selected static certificate: optional extension only
   after candidate 1. Validity is straightforward; benefit may disappear under
   coherent evaluation, state loading and uncompute. Avoid premature work.

No manuscript edit, hardware run, regression or novelty approval occurred.
