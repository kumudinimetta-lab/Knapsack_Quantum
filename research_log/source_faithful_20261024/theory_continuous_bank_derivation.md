# Minimum rational pruning banks: derivation before implementation

24 October 2026. Independent algebra review PENDING. No circuits or broad
experiments may assume this candidate before that review. The finite-grid and
DP-free sufficient constructions remain separately preserved.

## Assumptions and existing ingredients

Use exactly the positive-integer-weight/nonnegative-integer-profit knapsack,
capacity W>=0 and static exact decreasing-efficiency prefix order from
`theory_compressed_bank_derivation.md`. Accrued prefix profit P is integer.
The residual LP dual F_d(R,lambda)=lambda*R+sum_suffix max(v_i-lambda*w_i,0)
is standard LP/Lagrangian duality (Dey--Dubey--Molinaro Section 3 is a primary
source already verified). Greedy interval stabbing is standard; author sources
and a finite-grid exchange proof are in the earlier derivation. No novelty is
claimed for those ingredients. The candidate is their use to compile one
static ALL-prefix/ALL-integer-threshold bank of arbitrary nonnegative rational
multipliers with the fewest entries. Minimum cardinality is NOT minimum gates.

## 1. Exact continuous coverage interval for one reachable state

At suffix start d and feasible residual R, let W_j,V_j be cumulative weights
and profits of the first j suffix items, including j=0 with W_0=V_0=0.
Exact density sorting ensures

F_d(R,lambda)=max_{j=0,...,n-d} [V_j+lambda*(R-W_j)], lambda>=0.

Reason: for any lambda, the positive reduced costs form an initial segment
of the sorted suffix; summing them equals the maximum initial-segment sum.
Tied zero reduced costs may extend that segment without changing the value.

Let U_d(R) be the exact fractional LP value and K=floor(U_d(R))+1. Because
U<K, the coverage set Gamma={lambda>=0:F_d(R,lambda)<K} is nonempty. It equals
the intersection of the following EXACT constraints for all suffix prefixes:

- D_j=R-W_j>0: lambda<(K-V_j)/D_j.
- D_j<0: lambda>(K-V_j)/D_j, with the inequality reversed.
- D_j=0: require V_j<K, otherwise the interval would be empty.
- Domain lambda>=0.

Thus Gamma is a rational interval: [0,u), (0,u), (l,u), [0,infinity) or
(l,infinity), with possible l>0. All finite upper bounds are OPEN. A positive
lower endpoint is OPEN. A zero lower endpoint is closed unless a strict
constraint excludes zero. R>0 implies a finite positive upper bound via j=0,
lambda<K/R; R=0 has no positive D_j and can have upper infinity. Empty suffixes
are handled by j=0 alone: [0,1/R) for R>0 and [0,infinity) for R=0.

Pruning preservation is exactly hitting every Gamma for every reachable
(d,R): since P is integer, a selected lambda in Gamma gives the same floor
as U; all other dual bounds are >=U. Prefix reachability still uses a declared
W-bit DP and must be charged. No optimum/tree/quantum outcome chooses a bank.

## 2. Finite exact candidate cells without losing arbitrary-rational minima

Collect all finite nonnegative interval endpoints, plus 0, into a sorted set E.
For each consecutive endpoints e<f, choose ANY rational strictly inside (e,f).
Also choose one rational larger than max(E). These points form a finite grid
of open cells. Point0 can be retained as an optional candidate.

Within an open cell no coverage membership changes. Any positive endpoint
itself belongs to no interval that has that endpoint as an OPEN boundary; all
intervals containing it also contain a small neighborhood, so an adjacent
cell point covers every interval it covers. If point0 occurs, every interval
containing it has a positive right endpoint and contains a small positive
neighborhood; finite many intervals permit replacing0 by a sufficiently small
positive cell point. Hence restricting to these cell points does not increase
the minimum number of arbitrary nonnegative rational multipliers.

Implementation can avoid a quadratic interval/cell incidence matrix. Process
coverage intervals by increasing finite upper endpoint, with infinity last.
For the first uncovered interval ending at u<infinity, take the cell immediately
LEFT of u, between u and its preceding GLOBAL endpoint in E. Its point is above
every lower endpoint <u, so it stabs every remaining interval with lower<u
(and upper>=u). Intervals with lower>=u cannot share any point with this open
earliest-ending interval. Repeat. If only upper-infinity intervals remain,
choose a point above all their lower endpoints. Track whether a chosen point
equals an open lower endpoint; the proposed cell construction is strictly
inside and therefore avoids such equalities, but explicit membership checks
are still required in code.

Exchange proof: first use the preceding finite positive-neighborhood argument
to replace any chosen point0 by a positive cell point without losing coverage.
Then any feasible bank has a positive point p inside the earliest uncovered
interval. Every remaining interval p hits has lower<p<u and upper>=u. The
chosen predecessor-cell point x is above ALL lower endpoints below u and below
u, so replacing p by x keeps those intervals hit. Greedy repetition therefore
achieves minimum cardinality. Its chosen critical intervals are pairwise
disjoint, providing a matching lower-bound certificate. This proves minimum
among ALL nonnegative rational multipliers, not only the item-density grid.

## 3. Rational representative policy and bit widths

An arithmetic midpoint is always a valid representative of a bounded cell.
A MEDIANT of nonnegative rational endpoints a/b<c/d,
(a+c)/(b+d), is also strictly inside because b,d>0. This may avoid the
artificial denominator multiplication introduced by the arithmetic midpoint;
no minimum-denominator/minimum-gate claim follows. Record the policy and actual
numerator/denominator widths. An unbounded final cell can use max(E)+1.
All finite coverage endpoints have numerator/denominator from integer suffix
profit/capacity differences. These bit widths and preprocessing are part of
the resource comparison, not erased by reporting only cardinality.

## 4. Adversarial checks required before a broad study

1. Strict endpoint: equality F=K is NOT coverage. A cell point must never be
   an open endpoint. Closed domain0 is the only special closed boundary.
2. R=0 has an unbounded coverage interval; sorting a fake finite sentinel
   could choose an invalid point. Represent infinity explicitly.
3. Empty/all-fit instances: a singleton0 is exact, and one is minimum for a
   nonempty collection of states. Empty item input still has its root state.
4. Brute-force tiny all-prefix coverage intervals against independently
   evaluated Fraction dual values, not only the endpoint-generation code.
5. Enumerate ALL subsets of a small endpoint-cell candidate set to verify
   minimum cardinality; include off-grid witnesses where density-grid minimum
   is strictly larger, notably w=[1,1],v=[1,1],W=1, lambda1/2 sufficient.
6. Ties, zero profits, capacity0, all-fit suffixes, infeasible prefixes and both
   finite/open/infinite endpoint cases must be retained.
7. A bank selected for this exact static order need not preserve another
   order or the exact rational LP values; only integer-threshold decisions.

## 5. Stronger barrier candidate: arbitrary rational banks

Use the repaired family from Section E of the earlier derivation: n main
items w_i=2,v_i=4*(n-i)+1, q=floor(n/2), W=2q+1, plus the last dummy w=1,v=1.
For every s=q,...,n-1, the all-zero prefix d=s-q has q whole items then half
of main item s. Its exact U is a half-integer, and around rho_s=v_s/2 the
dual slopes are -1 and +1 until the next distinct densities. Those adjacent
breakpoints are at least 3/2 away (2 between main items; the dummy is at1).
Therefore its EXACT continuous coverage interval is

Gamma_s=(rho_s-1/2,rho_s+1/2).

These n-q intervals are pairwise disjoint because main centers differ by2.
The all-zero complete leaf has Gamma_zero=[0,1/W), disjoint from all of them
because rho_last=5/2 and 1/W<=1/3. Every rational bank hitting all prefix
states needs at least n-q+1 points. Conversely {0,rho_q,...,rho_last} gives
exact LP values for every prefix in this family: a main split uses its retained
density, all-fit states use0, and the unit dummy cannot have a positive
fractional residual because capacities/weights are integer. Thus the lower
bound is attained. This is a linear worst-case cardinality barrier even for
ARBITRARY rational banks with gcd-normalized weights/profits.

This says nothing about knapsack hardness or quantum query lower bounds; the
family is easy to solve classically. Its purpose is to delimit how much one
static primal-dual predicate can compress. Independent review is required
before accepting this stronger barrier or implementing the continuous compiler.

## Independent review and implementation record, 25 October

The parent and hardware/games reviewer separately confirmed the max-affine
representation, strict endpoint arithmetic, global predecessor-cell exchange,
minimum-cardinality/disjoint-interval certificate and arbitrary-rational
repaired barrier. The reviewer required the explicit positive-neighborhood
replacement before the exchange argument's strict lower<p step; this wording
was clarified above. Their approval is a bounded algebra/implementation gate,
not priority, minimum gates, end-to-end advantage or publication approval.

Implementation was placed in NEW `simulation/source_faithful_20261024/continuous_bank.py`;
the earlier exact-grid and DP-free module was left unchanged. A separate
source snapshot and pre-run source hashes were saved. The tiny probe covered
127 instances/2,247 feasible prefixes with 0 floor mismatches, 73,463 exact
endpoint/cell membership checks with 0 mismatches, 112 brute finite-cell
minimum checks with 0 mismatches and 15 explicit candidate-count caps, plus
31 repaired barrier sizes with 0 mismatches. These are classical exact checks,
not quantum circuit verification. Broad construction output then retained all
700 original cases,700 exact-core cases and45 declared high-capacity fallbacks.
