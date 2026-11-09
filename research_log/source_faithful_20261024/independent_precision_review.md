# Independent directed-rounding and QFT comparator review plan

24 October 2026. Independent derivation/counterexample pass before testing new builders. No old source, result or manuscript is changed.

## Upper-ceiling precision lemma

Assume positive integer weights/profits, exact rational order, integer P and threshold tau, feasible first-split residual0<=r<w, and reduced ratio a/b with b>0. Define q=ceil(2^k*a/b) and integer e=b*q-2^k*a, so0<=e<=b-1. The actual error is exactly r*e/(b*2^k).

- If r=0 or e=0, error is0. In particular, the strict expression 'error<r/2^k' is false at r=0 unless this zero case is stated separately. This edge-case wording was reported before implementation.
- If r>0 and e>0, error>=0 and error<r/2^k. If2^k>(w-1)*b, then error<1/b.
- Since b*(P+r*a/b) is an integer, U<tau implies tau-U>=1/b for integer tau. Therefore Uplus<tau whenever U<tau under the sufficient error condition. U>=tau implies Uplus>=tau at any precision because rounding is upward.
- Thus the exact integer-threshold pruning decision agrees under the sufficient precision. Lower precision can retain too many nodes but cannot introduce an unsafe objective rejection by upward error alone.
- Dyadic b=2^j is represented exactly at k=j, including b=1,k=0. The uniform precision inequality is sufficient, not a necessary minimum.

Independent counterexamples retained:

1. w3,v1,r2,tau1: k0 produces Uplus2, k1/k2 produce Uplus1; exact U2/3 rejects but all these retain. k3 gives Uplus3/4 and agrees. This is missed pruning, not unsafe pruning.
2. Necessity counterexample: w3,v2,r2,tau2 works at k2 (Uplus3/2<2) even though the sufficient inequality asks k3.
3. Integer-threshold assumption matters: w3,v1,r1,k3 gives U1/3 and Uplus3/8. A noninteger threshold7/20 lies between them; predicates differ despite the integer-threshold precision condition.
4. r0,nondyadic a/b=1/3: both bounds equal P, and0<r/2^k is false. Handle it as an exact case.
5. Sorting approximate efficiencies is unsafe: w=[10,10],v=[11,19],W10; rounding both ratios down to1 and preserving the original low-value-first order yields an apparent fractional bound11, rejecting threshold19 although the second item is a feasible good assignment. Keep exact order; compile approximation constants only after ordering.

The arithmetic is standard directed rounding and rational separation, not an independently established priority result. Register widths must cover the actual shifted products; this proof alone does not verify an emitted circuit.

## Adversarial QFT arithmetic obligations

The comparator is an author-defined reconstruction from Draper/Wilkening arithmetic unless an exact released LP-prefix circuit is identified. It must not be called the released Wilkening oracle by inference. Count and validate controlled additions, quantum-threshold comparisons, active/split history and cleanup on the same fixed-depth interface as all Boolean/ripple controls.

Independent counterexamples to naive implementations:

- A3-bit weight word wraps weight8 to0; w=[8],W1 must reject its selected prefix. Weight width must cover all prefix sums and capacity comparisons, not just W.
- A sign-bit comparison is valid only when the relevant mathematical subtraction fits its signed range. A modular value by itself is not a signed feasibility certificate.
- Enough-capacity comparison must retain equality: w=v=W=1 at its fitting step cannot be treated as fractional/infeasible by a strict-capacity test.
- All-fit suffix, empty suffix and first split with residual0 need their actual integer bound; they cannot dereference a nonexistent split or introduce a fractional rounding gap.
- Prefix profit already>=tau must remain objectively alive if capacity-feasible; a signed tau-P underflow must not become a large positive numerator.
- Ignored suffix bits, both initial output bits and all saved active/take/split flags must be restored. Agreement of measured flags alone does not certify a coherent phase oracle.

Test individual Fourier additions/subtractions/comparisons on arbitrary basis operands, controls and targets. Then test a bounded full predicate on independent exact LP-vertex references, with target XOR and clean workspace. Dense Qiskit tests should include complex amplitudes across both target states; a sparse numerical simulator must propagate joint amplitudes/entanglement, report any pruning error, and first agree with an independent dense simulator. The obsolete independent-per-qubit-phase simulator is not acceptable.

## Fairness and research acceptance gates

Use identical item order, fixed depth, quantum-prefix/threshold domains, capacity/invalid-input policy and zero-workspace semantics across all compared predicates. Compile to the same gate basis and declared connectivity; count rotations separately if exact arbitrary rotations remain. An approximate QFT or rotation synthesis must share a declared operator-error budget. No physical runtime or fault-tolerant T advantage follows from mixing equal-cost controlled rotations with CCX counts.

A substantial source-level claim needs a non-dominated same-function result against a faithful competently optimized comparator on more than one size/bit-width regime, with the gain mechanism isolated from dispatcher/normalization/precision artifacts. This is a research decision gate, not a guarantee or journal rule. Correctness alone, a known arithmetic identity, or a gain against an unnecessarily wide self-baseline is insufficient. Negative comparisons and stronger-baseline reversals remain results and must be retained.
