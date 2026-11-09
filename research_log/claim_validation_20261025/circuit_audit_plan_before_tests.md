# Fresh circuit falsification pass: plan before new tests

25 October 2026. This pass is by the QFT bank's author, after the previous
independent reviewer pass. It is a fresh adversarial check with a new LP
reference, not an assertion that the author has become an independent reviewer.
Old code, numerical raw data and manuscript files are read-only.
Graph discovery returned no structural graph tools before targeted reads.

## Questions, call paths and inspected semantics

1. `qft_bank.build_qft_bank -> bank_geometry -> QFTNetwork` creates explicit
   X/CX/CCX/H/P/CP gates. A=aW+sum positive reduced costs; loss is positive
   assigned reduced cost when excluded and negative cost magnitude when
   included. Compare A<loss+b*tau; OR all flags and capacity; copy target;
   invert the full forward gates. The output target is not used in forward
   controls, so arbitrary initial output must implement XOR, not overwrite.
2. `qft_normal_form` deletes exact inverse pairs only if the intervening gates
   are disjoint. The most recent live record on every gate wire must match;
   deleting a pair restores those wires' predecessor pointers. This preserves
   the full unitary, including phases. No approximate angle simplification.
3. `resource_profile` expands the actual primitive gate lists into opt0 u/cx
   skeletons and schedules their wire dependencies. It computes DERIVED costs;
   it never defines the LP answer or validates the gate action. Fresh full
   transpilation controls will check count/depth on the new test circuits.
4. `circuits.build_dual_bank -> _prefix_state -> BooleanCompiler` computes the
   SAME reduced-cost loss, quantum-threshold RHS and OR rejection including
   invalid depth/capacity. `BudgetCompiler.finish` copies the result into an
   arbitrary target and reverses all X/CX/CCX gates. Each has only +1 nonzero
   permutation amplitudes; exact gate-label propagation determines phase too.
   This builder requires strictly POSITIVE profits. Zero profits are supported
   only by the new QFT bank, not silently attributed to this older API.

No sign/width/OR/cleanup defect has been found in this code-reading pass.
That is not a passing experimental result.

## Independent LP-vertex reference, derived before tests

Fix prefix assignments (with a separately cross-multiplied, stable density
ordering), accrued profit P and residual R. If R<0, reject by capacity.
For the suffix box 0<=y_i<=1 with sum(w_i*y_i)<=R, a vertex has at most ONE
fractional coordinate: if at least two are fractional and capacity is tight,
a small two-coordinate perturbation along (w_j,-w_i) preserves capacity and
stays in the box in both directions, so the point is not extreme. If capacity
is slack, a small one-coordinate perturbation works instead. The polytope is
bounded and a linear objective attains an optimum at an extreme point.

Enumerate every feasible whole-item subset. For each omitted item i with
0<residual_after_subset<w_i, also enumerate its uniquely tight fractional
value residual_after_subset/w_i. Take the maximum exact Fraction objective.
No density-greedy bound, LP-dual value or bank formula is used to compute it.
This reference is exponential in tiny suffix size; no complexity gain is
claimed. The derivation is sent to the parent for separate review.

For the independently defined supplied-bank expectation, evaluate its
Lagrangian expression in exact Fractions. Compare it against the LP vertices,
then independently propagate actual circuit gates against that expectation.
Arbitrary nonnegative banks need only be safe upper bounds. An insufficient
bank SHOULD disagree with LP pruning; that is a recorded scope counterexample,
not a circuit failure. A certified/full-density/off-grid-valid bank must agree
on every encoded integer threshold under test.

## Predeclared adversarial fixtures and finite scope

Fresh QFT cases: denominator-17 near-integer split; equal ratios with a zero
profit item; multi-item all-fit; capacity zero; an off-grid singleton bank
that preserves integer floors but not exact rational bounds; an insufficient
singleton bank. Check all encoded quantum thresholds, all prefix bits and
both output targets on raw/cancelled, direct/generic complete gate networks.
Use noiseless MPS saved-tensor contraction (previously independently checked),
tolerance 1e-8, condition cap90s, native gate cap40,000, width cap128,
at most512 basis columns per method. Save caps/failures, do not drop them.
Add a fixed-seed complex superposition check to expose relative phases.

Boolean cases use only its declared positive-profit domain. Exhaust every
encoded depth (including invalid codes), all stored prefix bits, threshold
bits and both target bits on bounded small instances. Independently propagate
the emitted X/CX/CCX netlist into whole integer state labels and require the
ENTIRE output label to equal the expected inputs/output with zero workspace.
This checks stale prefix bits beyond depth as well as invalid-depth rejection.

Explicit limitations: thresholds are unsigned tb-bit integers, not arbitrary
precision/signed/fractional inputs. Probe rational-threshold and out-of-range
examples as limitations, not falsely simulated supported encodings. The
105-input comparison is a resource compilation, not exhaustive700 MPS testing
or a released-implementation/state-of-the-art benchmark.

If a real gate mismatch occurs, preserve its raw record and immediately
report RESEARCH_INTEGRITY_STOP. Do not patch the tested production code.
