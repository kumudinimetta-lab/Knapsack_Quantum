# QFT static dual-bank predicate: derivation before implementation

24 October 2026. This is OUR reconstruction using the already inspected
Draper (2000), *Addition on a Quantum Computer*, Sections 3 and 5, and
Wilkening et al. (2025), Supplement E.3--E.5 arithmetic primitives. It is
not a released Wilkening bank circuit or an optimized reproduction of its
parallel schedule. No divider is assumed or removed. Exact LP pruning by
certified integer-threshold banks is covered by the independent theory
derivation `theory_compressed_bank_derivation.md`, especially Sections B/F;
the basic LP dual and reversible arithmetic are established prior work.

## Predicate and domain

Positive integer weights, nonnegative integer values and capacity W>=0;
fixed efficiency-sorted prefix depth d; quantum prefix bits x and the SAME
quantum threshold bit width as the normalized LP control. The output is
an arbitrary target bit, XORed with rejection; all work starts and ends zero.
Every nonnegative rational multiplier lambda=a/b is normalized by Fraction,
b>0. A supplied bank is a static, data-only list, deduplicated and sorted.
Its compiler certifies neither the bank's coverage nor its novelty.

Write c_i=b*v_i-a*w_i and

    A = a*W + sum_i max(c_i,0),
    D_d(x) = sum_{i<d} [(1-x_i)*max(c_i,0)+x_i*max(-c_i,0)].

Then A-D_d is exactly the b-scaled dual upper bound at this prefix:
the original positive reduced-cost term is removed when an item is fixed,
and its selected reduced cost is added. For integer threshold tau,

    (A-D_d)/b < tau  iff  A < D_d+b*tau.

Both comparison operands are nonnegative, including on infeasible prefixes.
This avoids an unsafe unsigned representation of potentially negative A-D.
The bank rejects iff ANY multiplier rejects, or prefix weight exceeds W.
With a separately certified floor-preserving bank this equals the fractional
LP rejection predicate for every integer tau. With an arbitrary supplied
bank it is only the valid bank upper-bound predicate; these are not conflated.

## Widths before code

Let tau_max=2^tb-1. For multiplier j,

    0 <= D_d+b*tau <= sum_{i<d}|c_i| + b*tau_max = M_j.

Use shared accumulator width

    cb=max(1, bit_length(max_j(max(A_j,M_j)))+1).

This is a conservative positive padding bit. The comparator is the existing
source E.5 constant comparison; it does not form a signed subtraction.
The weight register uses EXACTLY the shared normalized LP weight width
bit_length(W+sum_i w_i)+1. It covers every prefix, not only feasible ones.
The largest shared work width additionally covers the number of OR controls,
so a generic clean serial multi-control chain cannot run out of ancillas.

Accumulator construction begins with the constant
D0=sum_{i<d}max(c_i,0), set by computational X gates. For c_i>=0 subtract
c_i controlled on x_i; for c_i<0 add -c_i controlled on x_i. Every partially
processed loss remains nonnegative. The final threshold multiplication is
the SAME repeated shifted-add recurrence used by the LP control. Widths
cover the result, all nonnegative addition intermediates and all constants.

## Cleanup and overlapping reject flags

Compute prefix weight and bad-capacity flag once. For each bank entry:
compute its accumulator, compare A<accumulator into a fresh flag, and apply
the exact inverse of its accumulator computation. Thus the shared arithmetic
word returns to zero while each bank flag persists. The same temporary
multi-control workspace is reused and cleaned within each comparator.

Dual reject flags can overlap, so parity is WRONG. Compute their OR, including
the bad-capacity flag, into a fresh aggregate bit by 1 XOR AND(all flags=0).
This is a reversible negative-control construction. Copy the aggregate to
the arbitrary output target and reverse ALL forward gates. The arithmetic,
individual flags, capacity work and aggregate then return to zero; input
prefix/threshold and the XORed output remain. Inverse QFT phase signs are
reversed as in the pinned QFT primitive, not merely list-reversed.

## Adversarial checks required before resources

Test empty/all-zero-value data, W=0, maximum quantum threshold, all-fit,
capacity-infeasible prefixes, rational multipliers with gcd reduction,
ties, zero reduced costs, strict comparison equality, and overlapping flags.
Check BOTH output target values exhaustively in tiny full compiled circuits
using saved-MPS contraction already checked against dense statevectors.
An independent exact-rational reference must check bank and LP equivalence
on the certified tiny banks BEFORE the simulator comparison is accepted.

Budget caps/failures are retained. Tiny numerical gate simulation does not
test the 105 large circuits; large counts remain DERIVED, not hardware or
full-walk/runtime evidence. Arbitrary-angle u/cx costs are not fault-tolerant
rotation costs. Independent derivation/code review remains required.

## Independent review before testing

The independent reviewer approved A-D, the accumulator bounds, overlapping
OR flags and inverse cleanup. It identified that the old shared `_data`
validator excludes zero values. The NEW bank module therefore uses its own
explicit integer validator accepting nonnegative values and reproduces the
same weight/threshold formulas. No pinned production validator is modified.
The legacy LP comparison is restricted to its positive-value domain; zero
values are additional bank-kernel checks, not a shared-domain resource claim.
