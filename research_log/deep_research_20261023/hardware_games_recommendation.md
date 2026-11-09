# Hardware and game-theory research: independent feasibility recommendation

23 October 2026. No manuscript, bibliography, original data, account, credential or hardware job was changed. This is a research design and bounded offline feasibility probe, not a promise of originality, performance or acceptance.

## Decision

1. **GO for an offline matched pruning/circuit resource study.** Make a defensible construction and a resource/pruning trade-off the main contribution. It is feasible to obtain either a resource improvement or a useful negative regime map without depending on IBM quota or physical noise being favourable. Novelty still depends on the exact construction and literature delta.
2. **CONDITIONAL GO for a small IBM corroboration after compiling the new construction.** An IBM experiment can show what a specified small component actually does, with complete provenance. Running a known Grover circuit on tiny knapsacks is insufficient as the central advance. A full reversible LP-node predicate is not established feasible on the user's account, and no full walk requirement should be imposed on a theoretical paper.
3. **NO GO for appending quantum game theory to this manuscript.** A credible new Bayesian allocation game with fair correlated baselines is a different research problem. Making it substantive has much higher uncertainty than the controlled circuit/pruning study; a small entangled allocation demonstration does not meet the user's low-risk requirement.

## Offline evidence, with taxonomy

`hardware_compile_pilot.py` uses the eight existing literal hardware inputs, parsed without importing any IBM account code. It compiles one Grover iteration with the existing arithmetic phase predicate to {rz,sx,x,cx}, optimization level 1, transpilation seed 23, using Qiskit 2.4.2. Input sizes and compiler configuration are HARDCODED. Counts below are DERIVED compiler outputs; they are not hardware timings, IBM backend calibrations, error estimates or bounds on the best compiler.

| Input | Selection qubits | Residual core | Total qubits | 2Q gates all-to-all | 2Q gates path |
|---|---:|---:|---:|---:|---:|
| Core-3A | 3 | 0 | 15 | 377 | 1037 |
| Core-3B | 3 | 3 | 15 | 379 | 991 |
| Core-4A | 4 | 3 | 17 | 487 | 1366 |
| Core-4B | 4 | 4 | 18 | 555 | 1629 |
| Core-5A | 5 | 5 | 19 | 617 | 1889 |
| Core-5B | 5 | 5 | 19 | 617 | 1898 |
| Core-6A | 6 | 6 | 21 | 773 | 2324 |
| Core-6B | 6 | 6 | 22 | 847 | 2647 |

Compilation failures: 0 on these eight inputs (DERIVED). This proves only that these specific circuits compile under the abstract targets. It does not imply useful physical success probabilities.

The existing hand-written inputs are poor evidence for a preprocessing benefit: six of eight fix no items; one is solved entirely classically; one reduces from four items to three (DERIVED enumeration/fixing results). Their prose labels claiming to be cores 'after LP fixing' are not accompanied by a recorded parent-instance reduction.

All assignments meeting tau >= greedy incumbent were checked against reconstructed residual assignments at 133 input-threshold pairs: mismatch count 0 (DERIVED exact enumeration, eight supplied inputs). This scopes the fixed/core marked-set bijection; it is not a universal proof or priority claim. The pre-computation derivation, excluded stronger claim and counterexample are in `hardware_pilot_derivation.md`. For a uniform full/residual search, the same marked count occupies a larger fraction of the smaller cube. This fraction identity is not valid for arbitrary biased QTG state preparation without modifying the statement.

## Existing hardware-code hazards

The audited path is `run_ibm_hardware.main` -> `build_grover_circuit`/`run_simulator` -> `oracle_marked_set`, `build_knapsack_oracle` and `_diffuser`.

- The phase predicate computes a supplied threshold from problem coefficients, which is useful. But both hardware circuit and simulator select iteration count from the **exact number of marked assignments**, obtained by exhaustive enumeration. That is solution-count advice. A fair optimizer cannot use this count for free. It is acceptable only as an explicitly answer-count-assisted component diagnostic, or if counting cost is included.
- `greedy_threshold` returns incumbent L and the oracle marks value >= L, so returning the already-known incumbent counts as success. A strict-improvement stage must mark value >= L+1 for integer profits. The current component does not execute the full backtracking walk.
- Seven of the eight tested `>=L` marked sets include suboptimal assignments (DERIVED enumeration). The runner nevertheless labels membership in this set `OPTIMAL`, uses it for `hw_found_optimal`, and prints 'Optimal found'. These labels must be repaired before any new publication experiment. This is not evidence that the old observations themselves are false; their circuit/job provenance is unresolved.
- The `Core-3A` strict-improvement threshold has zero solutions (DERIVED), so it is a valuable negative/control condition, not an input to silently discard or assign fictitious t=1.
- All literal hardware inputs bypass actual parent-instance LP fixing. Full and reduced arms must record the original instance, fixed assignments, residual capacity and threshold offset.
- `save_results` retains only selected counts and not job IDs, full submitted circuits, source hashes, backend calibration/target or full shot distributions. Job IDs are printed but not persisted in the JSON. Retain all raw counts, including ancillary leakage and failed jobs.
- The failure call passes `(all_results, instance_meta, backend_name, hw_failed=True)` into a three-argument save function; that path itself fails. No failure run was attempted, but this static call mismatch should be fixed in a new runner.
- No new hardware run has been authorized or performed by this probe. Do not reuse the old hardware table as validation of newly constructed circuits.

## Feasible design A: shallow, count-agnostic amplification after exact fixing

Question: on the same inputs and strict improvement thresholds, does classical fixing increase useful sample probability enough to offset arithmetic and noise cost, and is any residual gain attributable to amplification?

Use four arms: original-space sampling; fixed-core sampling; original-space shallow amplification; fixed-core shallow amplification. Preserve the problem exactly through reconstruction and threshold offsets. Add exact classical uniform sampling, a simple constructive randomized heuristic, and an exact classical reference for scoring; exact reference must not choose iteration counts or an input-specific threshold policy. Thresholds arise from a declared incumbent policy, not from the answer. Component diagnostics using optimum-adjacent thresholds must be labelled separately.

For a first hardware corroboration only, use a small predeclared collection with no-fixing, partial-fixing, fully solved and no-improvement controls. Determine j from a fixed shallow policy or training inputs, not marked counts on the evaluation inputs. Keep all j choices and training expenditure visible. Unknown-count search already has BBHT and fault-ignorant precedents; neither shallow restarts nor avoiding overshoot is a new result by itself.

Primary endpoint: probability of returning a **valid strict improvement** at a fixed threshold. Report reconstructed value distribution, feasible fraction, ancillary cleanup, 2Q gate counts, compiled duration when available, full shot counts and actual job QPU usage. An experiment of a fixed-threshold component cannot be called a complete optimizer or a classical runtime speedup. 'At least one success in thousands of shots' is a weak endpoint on tiny instances; report per-shot probabilities and confidence intervals.

A negative outcome is useful if it establishes a reproducible regime where arithmetic/noise overhead defeats the gain, with the classical fixing contribution isolated. This strengthens a serious resource/pruning paper; it is not automatically enough novelty for a standalone journal paper.

Feasibility gate: validate ideal action and cleanup; compile to an actual accessible target; estimate QPU usage; choose a bounded sample count and fixed analysis plan; only then consider hardware execution. If confidence intervals cannot distinguish the intended effect within available budget, keep the compilation/resource result and omit a forced hardware 'advantage' story.

## Feasible design B: arithmetic-precision boundary component, conditional on new circuits

If the main study yields an exact division-free pruning predicate, hardware can corroborate a minimal predicate/interference circuit on adjacent integer thresholds, comparing exact arithmetic to a deliberately truncated comparator under a clearly labelled approximation experiment. Select inputs near the pruning boundary by a declared diagnostic generator, not a solved-answer oracle. Record bit widths, signed ranges, overflow, workspace leakage and phase-action error. This is connected to the main correctness question, unlike adding a new application topic.

Gate: the smallest useful instance must fit a real target after routing. The existing large fixed-point LP construction is not thereby made hardware feasible. A tiny successful comparator does not validate every full-tree node or the complete quantum walk. New contribution would come from the exact construction, precision/resource trade-off and scope of correctness, with hardware as optional evidence.

## Why quantum games are a higher-risk diversion

The current paper has one decision maker and a deterministic objective. A game must define distinct players, private/public information, actions, payoff functions, admissible deviations, capacity violation handling and a resource model. Comparing an entangled strategy only with independent random play can mistake classical shared correlation for a quantum advantage.

For fixed public inputs, a central classical mediator can sample the same joint output distribution as a fixed quantum strategy. An equilibrium or computational separation requires an explicitly constrained information/deviation model; the bare distribution is not enough. For complete-information games, Dahl and Landsburg's *Quantum Strategies* primary manuscript discusses the relation between their quantum randomisation equilibria and classical correlated equilibria; its quantum-environment model must not be assumed to cover every joint EWL-style protocol. For private-input models, Bell-type/nonlocal resources can produce a genuine distinction, but implementing CHSH with a knapsack label is existing physics plus a relabelled payoff unless a substantive allocation result is established.

Abbott, Mhalla and Pocreau (Quantum 8, 1376, 2024) explicitly distinguish direct access to entangled states from classical access to quantum correlated advice, with different equilibrium classes (Definitions 5–9, Theorem 1). It demonstrates why the resource and allowed deviations matter. No theorem is transferred to this manuscript. Dey et al. and the 2025 cloud-allocation article establish topical overlap only; their abstract advantage claims were not adopted as facts about knapsack.

A low-cost small game can always be simulated, but a new useful separation cannot be guaranteed; the strategic model and baseline work would largely replace the existing paper. Therefore this track is NO GO for the immediate research-first repair.

## Primary sources and scope

1. IBM, [Plans overview](https://quantum.cloud.ibm.com/docs/en/guides/plans-overview), official current access: up to ten QPU minutes per rolling twenty-eight days. User eligibility/allocation has not been checked.
2. IBM, [Open Plan update](https://www.ibm.com/quantum/blog/open-plan-updates), official promotion conditions: non-trial eligible accounts using twenty minutes in twelve months may opt in to a one-time 180-minute allocation; this user's access is unknown.
3. IBM, [Workload usage](https://quantum.cloud.ibm.com/docs/en/guides/estimate-job-run-time) and [Maximum execution time](https://quantum.cloud.ibm.com/docs/en/guides/max-execution-time), distinguish QPU lock usage, active-session time, overhead, failures/cancellations and per-job limits. `max_execution_time` concerns QPU usage, not queue time. Planned shots alone do not establish a feasible quota.
4. Wilkening et al., [A quantum algorithm for solving 0-1 Knapsack problems](https://www.nature.com/articles/s41534-025-01097-8), npj Quantum Information 11, 146 (2025). QTG, amplification/maximum finding, detailed resources and COMBO benchmarking already exist. Its elementary equal-cost, noiseless, all-to-all model is not IBM physical execution.
5. Demmler and Hess, [A Nested Amplitude Amplification Protocol for the Binary Knapsack Problem](https://arxiv.org/html/2604.05776v1), preprint (2026), Sections III–V and Appendix A. Tunable tree split, QTG-biased preparation, inner iteration selection and GAS comparisons already exist. No source complexity theorem is adopted in this report.
6. Christiansen et al., [Quantum tree generator improves QAOA state-of-the-art for the knapsack problem](https://arxiv.org/html/2411.00518v2), primary preprint version inspected. Another reason to distinguish state preparation, classical reduction and the exact quantum routine; a generic knapsack QAOA demonstration is not new.
7. Vrana, Reeb, Reitzner and Wolf, [Fault-ignorant Quantum Search](https://arxiv.org/html/1307.0771v2), New Journal of Physics 16, 073033 (2014), DOI10.1088/1367-2630/16/7/073033. Section II.2 building blocks, Section II.4 Algorithm 1 and Theorem 3; restart/noise-adaptive search predates this project. Its general-channel/noise-hit assumptions and noiseless classical verification are not a model of measured IBM noise; lower-bound conclusions specifically rely on stronger depolarising assumptions (Section II.1, Theorems 2/5). No bound is transferred to IBM or the new pruning algorithm.
8. Boyer, Brassard, Hoyer and Tapp, [Tight bounds on quantum searching](https://arxiv.org/abs/quant-ph/9605034), primary abstract verified. It explicitly studies unknown numbers of solutions. Full theorem mapping is unnecessary for the fixed shallow pilot; no BBHT complexity claim is imported.
9. Abbott, Mhalla and Pocreau, [Improving social welfare in non-cooperative games with different types of quantum resources](https://quantum-journal.org/papers/q-2024-06-17-1376/), Quantum 8, 1376 (2024). Definitions 5–9 and Theorem 1 distinguish equilibrium/advice models. Read primary PDF snapshot; no game theorem is repurposed as a knapsack theorem.
10. Dahl and Landsburg, [Quantum Strategies](https://econweb.ucsd.edu/~gdahl/papers/quantum-strategies.pdf), authors' primary manuscript, Sections 3–7. Model-specific complete/private-information distinctions; publication metadata not independently checked here, so no unverified venue/year is asserted.

Additional overlap snapshots: [Quantum Game Theory meets Quantum Networks](https://arxiv.org/html/2306.08928v2) (Dey et al., primary preprint v2, 2024); [Quantum Game Theory-Based Cloud Resource Allocation: A Novel Approach](https://www.mdpi.com/2227-7390/13/9/1392) (Mathematics, 2025). These are not evidence of a general quantum allocation advantage.

## Failures and limits

All computation inputs, output, source hashes and compilation configuration are in `hardware_compile_pilot.json`; pre-computation reasoning is in `hardware_pilot_derivation.md`. UTF-8 read failures and a low-value broad search were retained in that derivation log. A PowerShell literal wildcard passed to rg produced a path-syntax error; subsequently explicit paths were used. No source data were manually modified. No hardware success probability, speedup, universal noise threshold or novelty priority has been established. Search feedback deadlines expired while evaluating full sources; no success is claimed for late feedback. The manuscript remains unchanged.
