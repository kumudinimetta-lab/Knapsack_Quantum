# Pruning study: protocol recorded before paired experiments

Date: 23 October 2026, Asia/Calcutta. User authorized research implementation and extensive necessary testing; manuscript changes follow research completion.

## Objective and integrity

Determine whether a cheap safe dual-bound predicate, an exact LP predicate and small banks of dual bounds occupy different useful quantum-resource/pruning regimes. A favorable outcome is not assumed. Cross multiplication, weak duality and the generic heuristic-cost tradeoff are known; priority of the precise construction/result remains unresolved.

Existing paper, bibliography, prior experiment outputs and deep-research prototypes are immutable inputs. New implementation lives in `simulation/pruning_study_20261023/`; new scripts, derivations and outputs live here. All failures, build caps, node caps, trivial cases and abandoned variants are retained. No IBM account or job access is needed or performed in this offline phase.

## Ownership

- Circuit agent: circuits module, width/cleanup derivation, bounded builds and circuit validation.
- Theory agent: canonical input registry, trees module, exact threshold/witness structural experiments and proof/certificate audit.
- Independent reviewer: separate proof/implementation/novelty review and paper-fit map.
- Parent: shared resource driver, paired summaries, statistical/metric audit, scope and final synthesis.

## Inputs and sampling policy

1. Pilot: five exact small inputs already in the deep-research circuit probe plus five generator inputs at n=12, seed=12000 (one per class).
2. Main structural set: existing five generators, n in {12,14,16,18,20,22,24}, 20 seeds 1000*n+t per class/size, t=0..19, R=100, capacity floor(sum weights/2): 700 cases, without favorable-outcome selection.
3. Resource representative set for expensive depth-wrapper architectures: first three seeds t=0,1,2 per class and size, selected before paired results: 105 cases. Cheaper single-scan families can be compiled on all 700 if the pilot meets budgets. A build that exceeds its budget is recorded, never silently removed.
4. High-bit-width stress: explicitly registered small item counts with large integer coefficients, independent exact MitM reference where applicable. Keep this set separate from the coefficient-small benchmark; do not call it an industrial advantage experiment.

No test-case optimum chooses an optimizer threshold, Grover count, predicate, or policy. Answer-known optimum+1 thresholds are permitted only as labeled unmarked diagnostics. Marked and unmarked conditions from the same instance are paired observations, not independent instances.

## Methods and controls

- Simple remaining-profit bound with prefix capacity rejection.
- One normalized root-dual bound, exact integer loss/cross-product comparison.
- Nominal two/four-entry compiled multiplier banks, with actual distinct count reported.
- Exact residual-LP bound via normalized integer cross products, coherent single scan.
- Exact residual-LP depth-wrapper architecture on the selected representative set.
- Preserved safe fixed-point LP depth wrapper on the same representative set.

Keep exact efficiency ordering and deterministic ties, identical original/residual problem inputs, quantum threshold register domains, prefix/depth encoding, strict pruning at bound<tau and clean XOR output semantics. Leaf acceptance must check actual feasible objective, not an upper bound. Report workspace and depth together with gate counts. Ratio normalization, dispatcher architecture and compile-time dead arithmetic are separate factors, not attributed to an invented new theorem.

## Work budgets

Initial per-circuit limits are HARDCODED configurations: 2,000,000 emitted gates, 150,000 wires, 60 seconds build/analysis time, with resource limits enforced or a monitored subprocess for constructors that cannot enforce them. Initial static-tree limits: 50,000 generated vertices and an explicit per-condition elapsed-time limit chosen in the tree driver. A limited cap escalation may follow only if capped conditions materially affect a conclusion; retain the initial capped outputs and label the rerun.

Pilot results determine whether broad gate-list compilation is affordable, not which instances have favorable scientific outcomes. The full raw input registry is saved before outcomes. Timing is diagnostic of this host and Python implementation, not a physical quantum runtime estimate.

## Validation

Derive new bank/width logic before circuit code. Independently review the derivation. Exhaust small prefix/depth/threshold/target domains on selected tiny cases; report mismatch and dirty-workspace counts on the same line as every checked-circuit claim. Include empty inputs, all-fit suffixes, ties, exact equality, zero capacity/residual, overweight prefixes, ignored suffix bits, invalid depth and both initial target bits. Perform an independent Qiskit statevector/operator check on a tractable tiny circuit; do not claim dense simulation of large workspace registers.

For larger inputs use exact rational reference predicates with recorded adversarial/sample encodings and circuit gate simulation. These are scoped samples, not exhaustive all-depth validation. Separately check bound safety, bank-vs-LP relation, fixing preservation and witness reconstruction against exact DP/MitM where feasible. Stop and log a research-integrity issue for unsafe pruning or a reference mismatch; do not fit around it.

## Metrics and interpretation

- MEASURED: classical generated vertices, solve outcomes, elapsed host times, build failures.
- DERIVED: exact rational values, safe certificate bounds, compiled X/CX/CCX lists/counts/depth, paired arithmetic and summary statistics.
- SIMULATED: circuit basis-column/statevector outputs or explicit quantum operators.
- SCHEDULED: chosen query/repetition budgets or model-based walk-use schedules.
- HARDCODED: seeds, caps, register policies and experimental configurations.

Primary offline observations are circuit resource vectors and static-tree node counts on the SAME input and threshold. Predicate-cost times sqrt(tree size) is a DERIVED work proxy, not a measured quantum runtime, an implemented full walk, an independent verification of square-root scaling, or a guaranteed quantum bound with an unexplained free tree-size input.

Report at least separate CCX, total-gate, depth and workspace comparisons. Assess sensitivity to a shared walk/reflection/acceptance overhead rather than treating predicate cost as the entire algorithm. Do not equate gates, physical seconds and classical nodes. A numerical full-walk/crossover claim requires an implemented/justified reflection and recovery cost model; otherwise label the omission.

Certificate-based theoretical bounds and enumerated-tree proxies are distinct analyses. A common valid dual certificate can bound a stronger LP tree, but may hide actual pruning differences. Certificate computation is counted and its looseness reported; pseudopolynomial counting is not free preprocessing. Witness queries require consistent original prefix penalties/order and retained feasible incumbent.

Use per-instance paired summaries with class/size breakdown and explicit capped-pair counts. Do not regress scheduled queries on their generating tree-size formula. Any uncertainty intervals must preserve dependence of conditions belonging to one input; do not manufacture p-values for deterministic algebra checks.

## Research gates and paper fit

1. Correctness and cleanup pass within stated scope; independent review addresses assumptions.
2. Same-input paired study finishes within budgets, retaining unfavorable cases and all caps.
3. An actual construction/resource result or explanatory negative regime survives fair baselines and overhead sensitivity. A small standalone oracle count is not automatically enough novelty.
4. Closest primary-source comparison identifies the exact supported contribution, with remaining priority uncertainty explicit.
5. Write a research results/limitations report and map it to the existing oracle, analysis and experiments sections. Only after these gates, edit the restored paper line by line while preserving legitimate citations.
