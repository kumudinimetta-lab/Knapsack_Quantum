# Circuit/algorithm research track: checkpoint and implementation report

Date: 23 October 2026. Scope: research code, primary-literature comparison and offline feasibility. No manuscript/bibliography/historical data were edited. No IBM job was submitted. Graph MCP discovery returned no graph tools; targeted file reads were used as the documented fallback.

## Recommendation

Rank 1: an explicitly verified, resource-aware portfolio of simple, root-dual, small fixed dual-bank and exact LP pruning predicates. The scientific question is whether a weaker predicate's gate savings compensate for its larger search tree, and in which instance/bit-width regimes. Combine the parent's matched tree/resource study with the theory track's certificates and overhead sensitivity. The algebra and the generic cost tradeoff are known. A publishable addition would have to be the concrete construction, rigorous correctness/encoding, reproducible same-instance Pareto evidence and explanatory limits; novelty/acceptance is not certified by this track.

Rank 2: division-free exact LP predicate and a controlled comparison against safe fixed-point arithmetic. This is a feasible construction already implemented and checked in limited scopes. The identity P+r*a/b<tau iff P*b+r*a<tau*b is elementary. Eliminating precision bits may help gate count but can lose on particular ratios and compiler representations. Include this as a controlled engineering result, not a new mathematical theorem.

Rank 3: coherent single-depth scan and space/depth tradeoff. The preserved implementation computes each fixed-depth predicate twice and reuses one work pool. The new alternative scans once, under a quantum depth index. This can reduce gate depth but increase ancillas because the transparent Boolean compiler stores intermediates. Coherent depth selection and space optimization already have predecessors. Treat it as an architecture control, not the entire novelty claim.

Do not make quantum-game theory or a new IBM experiment a prerequisite for this project. These additions are not needed for the computational question, and successful hardware execution alone would not establish originality. An offline complete dataset is feasible even when the positive improvement does not occur. The substantive result remains unknown until the parent's matched study is assessed.

## Primary-source evidence and overlap boundaries

1. Vedral, Barenco and Ekert, "Quantum networks for elementary arithmetic operations," Physical Review A 54, 147 (1996), DOI https://doi.org/10.1103/PhysRevA.54.147 ; primary full preprint https://arxiv.org/html/quant-ph/9511018v1 . Sections III.1 and III.3 explain subtraction/comparison and constant multiplication via controlled additions. This grounds implementation feasibility. Our compiler is generic X/CX/CCX Boolean arithmetic, not an implementation of VBE's exact optimized network.
2. Cuccaro, Draper, Kutin and Moulton, "A new quantum ripple-carry addition circuit," arXiv:quant-ph/0410184 (2004), https://arxiv.org/abs/quant-ph/0410184 . Exact author/title metadata were verified in prior cached primary material. Its single-ancilla linear-depth design cautions that our out-of-place compiler's qubit counts are not best-known arithmetic counts. No theorem from it is invoked in the current result.
3. Hou and Perkowski, "Quantum-based algorithm and circuit design for bounded Knapsack optimization problem," Quantum Information and Computation 20(9-10),766-786 (2020), DOI https://doi.org/10.26421/QIC20.9-10-4 ; full publisher paper https://www.rintonpress.com/xxqic20/qic-20-910/0766-0786.pdf . Sections 4-8 supply knapsack feasibility/threshold-oracle components with constant arithmetic; Sections 9-11 discuss costs and testing. Thus merely designing a knapsack decision circuit or counting its gates is not new.
4. Martiel and Remaud, "Practical implementation of a quantum backtracking algorithm," primary preprint https://arxiv.org/html/1908.11291v1 (2019; later SOFSEM 2020). Section 3 explicitly compares heuristic overhead against tree reduction, and Section 4 uses a coherent depth index and comparisons to fixed constants. This overlaps with both the generic portfolio rationale and depth-dispatch mechanism. Our potential delta must be specific construction/evidence, not the generic tradeoff.
5. Montanaro, "Quantum speedup of branch-and-bound algorithms," Physical Review Research 2,013056 (2020), DOI https://doi.org/10.1103/PhysRevResearch.2.013056 ; full primary preprint https://arxiv.org/html/1906.10375v1 . Theorem 1 counts calls to branching/cost procedures for an adaptive minimization algorithm with integer bounded cost, depth d and optimal truncated-tree size T_min. Our circuit cost is one local component, not the full adaptive algorithm or an implementation of that theorem. The parent's sqrt(tree) work proxies are separately DERIVED and cannot be called measured quantum runtime. This track does not instantiate Theorem 1.
6. Campbell, Khurana and Montanaro, "Applying quantum algorithms to constraint satisfaction problems," Quantum 3,167 (2019), https://quantum-journal.org/papers/q-2019-07-18-167/ . The primary abstract/publisher material shows detailed resource-aware comparisons and hardware overhead dependence for SAT/colouring. It establishes that generic resource estimation and unfavorable overhead conclusions are established practice, not our innovation.
7. Wilkening et al., "A quantum algorithm for solving 0-1 Knapsack problems," npj Quantum Information 11,146 (2025), https://www.nature.com/articles/s41534-025-01097-8 . The main paper supplies a QTG construction, maximum-finding/amplification, resource estimates and COMBO comparisons, and explicitly benchmarks QBnB in Supplementary F. Main text was read. Exact overlap with all supplementary details remains a priority-review question, not proof of absence. Primary supplement link: https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41534-025-01097-8/MediaObjects/41534_2025_1097_MOESM1_ESM.pdf . Parent was alerted to this highest-priority source comparison.
8. Bucher, Stein, Feld and Linnhoff-Popien, "Penalty-free approach to accelerating constrained quantum optimization," Physical Review A 112,062605 (2 December 2025), https://doi.org/10.1103/fb5m-cl9m . Publisher abstract discusses constraint-indicator QAOA for knapsack and solution-quality/circuit-depth tradeoffs. This is a different algorithmic setting, but overlaps with broad claims of improved constraint circuits or 'smaller search space is always better.' Only the publisher abstract is used here; no theorem is borrowed.
9. Sankar et al., "A benchmarking study of quantum algorithms for combinatorial optimization," npj Quantum Information (22 June 2024), https://www.nature.com/articles/s41534-024-00856-3 . Primary abstract compares MaxCut algorithms including Durr-Hoyer minimum finding under explicit resource/time-to-solution models. It supports the need for a precise cost model rather than gate/node-unit mixing; it does not establish anything about our knapsack performance.

Cached source files: `.firecrawl/vbe-full.md`, `.firecrawl/cuccaro.json`, `.firecrawl/circuit_circuit_search_bounds_0.md`, `.firecrawl/circuit_circuit_search_bounds_1.md`, `.firecrawl/circuit_circuit_search_cost_0.md`, `.firecrawl/circuit_circuit_search_cost_2.md`, `.firecrawl/wilkening2025.md`, `.firecrawl/circuit_penalty_free.md`, `.firecrawl/circuit_benchmarking2024.md`. One extra search returned HTTP429 and was not interpreted as a negative literature result. No 'first' claim is established.

## Derivation and adversarial process

Pre-prototype derivation: `circuit_derivation_before_probe.md`. Pre-production extension/width derivation: `../pruning_study_20261023/circuit_derivation_before_implementation.md`. Parent independently reviewed exact cross products and weak duality before production implementation. Finite-bank validity follows from a minimum of valid upper bounds; the bank circuit ORs the separate strict rejection comparisons. Register widths cover all unsigned live operands. The safe fixed-point control uses 2^k>Wmax^2 and a rational threshold gap at least 1/Wmax; exact efficiency ordering is preserved.

Rejected/risky alternative: r*a<(tau-P)*b needs signed arithmetic when tau-P<0; current implementation instead compares P*b+r*a<tau*b. Exact equality is not rejected. Infeasible prefixes are handled independently. No split means an integer bound. Empty inputs, zero capacity, all-fit, tied densities, gcd reduction, invalid depths, irrelevant suffix prefix bits, maximum encoded thresholds and both output targets are explicit checks.

A naive first exact depth-wrapper compiled dead arithmetic at already-assigned item positions. This was slower/larger than baseline. Both this failed attempt and later compile-time skip/gcd variants are preserved by code switches and generated raw results. They were not manually rewritten. The first UTF-8 inspection failed under Windows cp1252 and was rerun with explicit UTF-8; no data were changed.

## Completed feasibility results: limited scope, not full algorithm

Isolated prototype `circuit_feasibility_probe.py` and `circuit_feasibility_probe_results.json`: 6 variants x 5 small inputs, 17,920 SIMULATED basis columns per variant, total107,520; predicate mismatches0, dirty columns0. Added 3 resource-only inputs at n8/12 with coefficients100 and n8 with coefficients1,000,000. Resource-only circuits were not exhaustively simulated. No outcome was discarded.

After user authorization, production research module `../../simulation/pruning_study_20261023/circuits.py` was added separately. Validation `../pruning_study_20261023/circuit_validation.py` produced `circuit_validation_results.json`:
- SIMULATED exhaustive input domains on16listed small cases x8families:128method cases,406,080basis columns,0predicate mismatches,0dirty columns.
- SIMULATED sampled wider cases at recorded seeds20261100..20261103 (n6,8,12; final n8 coefficients up to10^6),8families:32method cases,16,064basis columns,0predicate mismatches,0dirty columns.
- Combined:160completed method-cases,422,144basis columns,0predicate mismatches,0dirty columns;0unexpected exceptions;0natural build caps in this validation set.
- SIMULATED independent Qiskit dense propagation on8empty-instance circuits, each random superposition with8nonzero input amplitudes: maximum amplitude error0;0checks above1e-12. Eight nonempty candidates were explicitly SKIPPED because they exceed the HARDCODED18-qubit dense cap. This does NOT constitute a dense check of nonempty large-workspace circuits.
- Three HARDCODED cap-injection controls hit the expected wire/gate/build-time reason; all retained. Limits protect construction, not physical device feasibility.

These checks support the listed instances/seeds/encodings with zero initial workspace only. They do not validate every700benchmark input, every possible instance, a full walk/reflection, witness recovery circuit, error correction or real hardware. No global 'h is correct' claim is made.

### Same small input resource vector

For w=[2,3,4,5],v=[3,4,5,8],W=8, all counts below DERIVED from actual X/CX/CCX lists in the production module (not hardware measurements):

| Predicate/architecture | Qubits | CCX gates | Gate depth |
|---|---:|---:|---:|
| Simple remaining profit |177|98|125|
| Root dual, reduced multiplier |190|108|137|
| Nominal bank2 |258|156|147|
| Nominal bank4 |414|270|179|
| Safe fixed-point single scan |1272|934|507|
| Exact rational single scan |881|598|433|
| Exact rational depth wrapper |510|1653|1722|
| Preserved fixed-point depth wrapper |591|2125|1622|

This is an implementation feasibility illustration, not a selected performance victory. Portfolio predicates have different tree sizes. Single-scan/wrapper rows differ in architecture. Even equal Boolean functions have different depth/ancilla Pareto vectors; no row is a best-known or optimal circuit. Fixed-point arithmetic is not uniformly worse: the subset-sum/gcd structure can make constant multiplications cheap. The parent's broad matched study must determine regimes.

## Production API for reruns

Import `simulation.pruning_study_20261023.circuits` from repo root (or `pruning_study_20261023.circuits` with simulation on sys.path).
`BUILDERS` keys: `simple`, `root_dual`, `bank2`, `bank4`, `fixedpoint_single`, `exact_single`, `exact_wrapper`.
All accept `(weights, values, capacity, budget=BuildBudget(max_qubits=150000,max_gates=2000000,max_seconds=60))`.
Direct functions: `build_simple`, `build_root_dual`, `build_dual_bank(q=1/2/4,multipliers=...)`, `build_fixedpoint_single_scan`, `build_exact_single_scan`, `build_exact_depth_wrapper`.
Bank policy root; root+0; root+0+min/maxdensity; exact Fraction deduplication. Choices depend only on problem data.
Input layout: m prefix bits in exact stable decreasing-density order; db=max(1,m.bit_length()) coherent depth bits; tb=max(1,(sum(values)+1).bit_length()) threshold bits. Target is `.output`, work qubits are all other noninput wires. `.num_inputs` excludes target/work. Invalid d>m rejects; ignored suffix bits remain untouched.
Return object exposes `.resources()`, `.metadata`, `.gates`, `.simulate_columns(inputs,output_bit=0)`, `.to_qiskit()`, `.depth_register_bits`, `.prefix_width`. Catch `CircuitBuildCap` and retain `.reason`/`.counters`; do not turn a capped build into a success row.

Commands:
`python -B -X utf8 research_log/pruning_study_20261023/circuit_validation.py`
`python -B -X utf8 research_log/deep_research_20261023/circuit_feasibility_probe.py`

## Finite success/failure criteria and valuable negatives

1. Zero unsafe-prune mismatches/dirty workspace within specified checked scopes; any violation stops the affected scientific claim and is logged.
2. Generate matched resource vectors and static-tree counts on preregistered inputs, including time/memory/node caps. A useful resource result must survive comparison with SIMPLE and matched fixed-point single-scan controls, not only an expensive old dispatcher.
3. Report class/size/bit-width breakdown and sensitivity to a shared walk/reflection overhead. Cost*sqrt(T) remains a DERIVED proxy; no empirical speedup theorem or hardware runtime.
4. If root dual/banks expand too much, quantify the regimes and counterexamples. If exact arithmetic wins gates but loses qubits, publish the tradeoff only at its actual strength. If all methods lose to simple remaining-profit after common overhead, that negative conclusion can still motivate a corrected/practical-resource study, but journal significance is not guaranteed.
5. Before a novelty claim, finish closest-source SupplementaryF comparison and compare optimized arithmetic where relevant. If a predecessor already supplies the same construction/regime, report overlap and narrow the claim; do not invent novelty through branding.

Main full700/static-tree/resource runs are owned by parent/theory agents and are not reported here as complete. Next steps: audit broad results and caps, review primary-source overlap, settle the strongest supported claim, then make minimal source-based manuscript changes preserving valid references. No acceptance percentage/desk-review guarantee follows from this work.
