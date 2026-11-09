# Exact fixing audit: derivation and adversarial plan before tests

23 October 2026. Independently audit simulation/exact_knapsack.py without modifying it, historical data or the manuscript. Graph tooling was discovered earlier and unavailable; targeted source reads are used.

## Actual implementation and domain

Use n=len(weights)=len(values), positive integer weights and profits, and nonnegative integer capacity. `efficiency_order` sorts exact Fractions, with stable ties. `lp_bound` sorts its supplied item subset again and greedily fills fractional capacity. `reduced_cost_fixing` first obtains a feasible skip-overweight greedy incumbent L. A separate `before` set contains whole items before the first fractional root-LP split; it is not necessarily the greedy incumbent's support. For i in before, it tests the exact LP with x_i forced to zero. Otherwise, it tests x_i forced to one, with a separate impossible-overweight rejection. All tests use strict upper<L.

This is exact opposite-branch LP fixing, not merely evaluation of a closed-form reduced-cost approximation. It solves a new sorted fractional relaxation per tested variable. Do not attribute a linear-time implementation or just O(n log n) total preprocessing to this function without counting those calls and rational arithmetic. The broad name 'reduced_cost_fixing' does not change its actual call path.

## Self-contained safety derivation

For a capacity-feasible integral assignment, the relaxation containing that assignment has value at least its objective. The decreasing-efficiency fractional fill is an upper bound because an exchange of equal positive weight from a lower-efficiency selected item to a higher-efficiency unsaturated item never lowers profit; such exchanges yield the fractional prefix/split solution. This is standard fractional-knapsack reasoning, not a new theorem or an imported numbered source theorem.

If an opposite branch has bound U_i<L, no feasible assignment with profit>=L can use that opposite branch. Every retained good assignment therefore agrees with every fixed bit simultaneously. The greedy witness itself has profit L and is feasible, so it agrees with the fixed bits and demonstrates simultaneous consistency. Thus fixed-in weight<=W. For any assignment x of good objective, restriction to core coordinates yields y with residual weight<=W-sum(FI weights) and residual profit>=L-sum(FI profits). Conversely reconstructing any such residual y with the fixed bits produces a feasible original assignment of the same shifted objective. Restriction/reconstruction are inverse maps on these sets. Therefore all assignments at every threshold tau>=L are preserved, including every optimum because optimum>=L. The claim does not cover all assignments at thresholds below L.

Core index order returned by the function is original index order, whereas node branching later sorts the residual items by their own exact efficiency. A caller must map the recovered residual witness back through its own order before mapping through core indices. Wrongly treating original indices as residual efficiency positions can preserve the value while corrupting the witness.

## Counterexamples to overstrong claims

- Strictness: one item w=v=W=1, L=1; forcing the item to zero gives U=0<L and fixes it in. An equality example with two identical items w=v=1,W=1 has opposite bound U=L=1. Replacing '<' by '<=' can discard one of the two optimal assignments.
- Threshold scope: w=[1],v=[1],W=1 fixes x=1, but the feasible x=0 is lost at tau=0<L. No all-feasible-assignment preservation claim is valid.
- Greedy support: it can skip a fractional split item and accept a later item. The root whole-prefix set must not be treated as the greedy witness or its full value.
- Empty core and all-fit are valid outcomes, not failures to exclude. At L=0 with no fitting positive item, all nonempty overweight choices are infeasible.

## Independent exhaustive validation plan

Enumerate all n=0,1,2,3 instances with every weight/profit in {1,2,3}, and every capacity W from zero through sum(weights)+1. For each, independently enumerate integral feasible assignments and LP vertices (integral subset plus at most one fractional item) for opposite branches. Compare fixing decisions, strict inequality, partition, greedy witness, FI/FO consistency, residual reconstruction and all assignments of value>=L. Test every integer tau from L through sum(values)+1 via independently generated original and reconstructed sets. Retain all cases and any failures; stop the affected claim if found.

Then run fixed-seed random/adversarial cases up to eight items, including larger coprime coefficients, ties, capacity zero/all-fit, a nonprefix greedy witness and a known rounding-equality case. Exact enumeration remains the reference; no old raw records are modified. Expected inputs/configuration/seeds are HARDCODED, exact references and comparison counts DERIVED, host execution/time MEASURED. This is classical validation, not quantum simulation.

## Source boundary

The cached primary publisher pages identify Dantzig's Discrete-Variable Extremum Problems (Operations Research 5(2),266-288,1957; DOI10.1287/opre.5.2.266) and Pisinger's Core Problems in Knapsack Algorithms (Operations Research47(4),570-575,1999; DOI10.1287/opre.47.4.570). The latter explicitly credits Balas and Zemel for the core concept. Those metadata/abstract pages do not verify a numbered theorem for this exact implementation, so no such attribution or priority is asserted. The correctness check here rests on the explicit relaxation containment argument and independent exact vertex enumeration. The derivation is not a new contribution to advertise.
