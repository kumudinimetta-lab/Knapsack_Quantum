# Root-aware LP scan control — derivation before code

25 October 2026. Purpose: challenge the strength of our existing LP baseline,
not improve the bank. Existing sources/results/checkpoint remain unchanged.
The root agent independently reviewed the following elimination argument before
requesting this new control. It is an application of the already reviewed
root-tail lemma, not a new priority claim.

Assume positive integer weights, nonnegative integer profits, nonnegative
capacity W and the same static exact decreasing-density order pi. Let
`C_j=sum_{k<j} w_pi[k]`. Define s0 as the first position j for which
`C_j+w_pi[j]>W`, or n if all items fit. Fix a classical depth d, with quantum
prefix bits for positions k<d, quantum integer threshold tau, an arbitrary XOR
target, and initially zero workspace.

For an active feasible suffix scan at position j>=d, no earlier split occurred.
Its used capacity is exactly

`used_prefix + sum_{d<=k<j} w_pi[k] <= C_d + sum_{d<=k<j} w_pi[k] = C_j`.

If j<s0, then `C_j+w_pi[j]<=W`; the next item fits for every such input. Thus
the computed split flag is always zero on feasible active branches. On
infeasible prefixes, the independent bad-capacity flag rejects and the active
flag is zero. Removing the fractional-product/comparison output term at j<s0
therefore preserves every rejection decision, for every encoded prefix and
integer threshold. Keep the whole-item/take/residual/active logic unchanged.

Only positions `j>=max(d,s0)` can have a live fractional split. For their reduced
densities `a_j/b_j`, the original conservative valid-branch bounds still apply:

`P*b_j+r*a_j <= S*b_j+W*a_j`, and `tau*b_j <= tau_max*b_j`,

where S is the total input profit and tau_max is the largest encoded threshold.
Choose the common numerator/comparison width from

`max(S, tau_max, max_eligible(S*b_j+W*a_j, tau_max*b_j))`,

with one padding bit after bit_length. S and tau_max explicitly cover the final
integer comparison, including no eligible fraction positions. The weight and
profit widths and all interface bits are identical to the existing control.
Do not apply these smaller widths to arbitrary ratio positions that the new
control no longer evaluates. Inactive modular arithmetic is masked and exactly
reversed, as in the original factory.

Counterexample attempt: excluding an early prefix item only reduces used
capacity and makes pre-s0 items easier to fit, so cannot create an earlier
split. Selecting every prefix item maximizes used capacity and attains C_j;
the definition of s0 still guarantees fit for j<s0. Overweight prefixes are
already masked. Equal densities change neither cumulative-weight argument.
All-fit roots have no eligible fraction positions; empty inputs retain their
integer comparison. Negative weights or a non-static/different branch order
are outside scope.

This is only a stronger reconstruction control. It is not a released R1 gate
oracle or an optimal LP implementation. It does not add diagonal-angle merging,
copied-control parallelization, classical-threshold specialization, or physical
rotation synthesis. Allocate and count both raw and actually touched qubits
while retaining every interface wire.

Planned validation before the 105-input resource-only comparison: independent
LP-vertex references on tiny data, exact X/CX/CCX propagation using a parallel
ripple engine, and actual QFT gates on basis inputs plus unitary RY/P/CX-prepared
complex states. Do not use the diagnosed Aer MPS partial-initialize path.
Record explicit counts, seeds, tolerances, caps and failures. Do not overwrite
any previous raw result or manuscript file.
