# Resume checkpoint

Date: 23 October 2026 (Asia/Calcutta).

Read `RECOMMENDATION.md` first, then `SAVED_PROBE_SUMMARY.json`.

## Current objective and constraints

Find feasible creative improvements to the restored quantum knapsack paper, with useful negative outcomes, before restructuring it for QIP. User explicitly authorized multiple agents. Do not modify the restored manuscript/bibliography yet. Preserve legitimate citations and all historical raw data. No guarantee of novelty, favorable outcome or acceptance. Follow `AGENTS.md` evidence-first process and metric taxonomy.

## Work completed

- Three tracks: reversible circuits, theory/certificates, IBM hardware/game-theory feasibility.
- Derivations saved before isolated probe code; parent independently checked core algebra and scope.
- Six circuit variants on five small inputs: each 17,920 clean-input basis columns, 0 mismatches and 0 dirty columns (SIMULATED), with differing resources.
- Exact bound/certificate checks: 120 instances, 7,012 feasible prefixes, no recorded failures within scope (DERIVED checks).
- Static-tree benchmark: 90 retained conditions, including caps; weak/strong bounds trade pruning against arithmetic.
- Finite dual-bank tree-only pilot: 90 conditions, bank circuit not yet built.
- Abstract compilation of eight old hardware inputs: no QPU/account usage; existing input/iteration-policy/provenance problems identified.
- Literature overlap checked and sources cached; novelty of the precise construction remains unresolved.
- No full quantum walk, fresh hardware run, full baseline comparison or paired net-resource improvement established.

## Main recommendation

One coherent project: cheap safe root-dual versus exact division-free LP predicates, coherent depth implementation and matched gate/workspace/tree/recovery analysis. Small dual banks and a static certificate are optional extensions. Hardware is optional corroboration. Do not pivot to game theory or an unproved asymptotic result as the critical path.

## Exact next action

Inspect the two derivation notes and probe scripts. Perform a SAME-INPUT paired circuit-and-tree pilot on the five small saved cases plus five n=12 seed12000 generator cases. This experiment was proposed but NOT completed when agent credits ran out. Do not combine first-case gate ratios with unrelated aggregate tree ratios. Ensure fair dispatch/cleanup/arithmetic baselines. Stop for any safety mismatch, retain failures/caps. Only then decide whether to expand.

## Files

- `circuit_derivation_before_probe.md`, `circuit_feasibility_probe.py`, `circuit_feasibility_probe_results.json`, console output.
- `theory_derivation_candidates.md`, `theory_probe.py`, `theory_probe_results.json`.
- `theory_bank_probe.py`, `theory_bank_probe_results.json`.
- `hardware_pilot_derivation.md`, `hardware_compile_pilot.py`, `hardware_compile_pilot.json`.
- `summarize_saved_probes.py`, `SAVED_PROBE_SUMMARY.json` (derived summary; raw data unmodified).
- `RECOMMENDATION.md` (parent's synthesis; agent final narrative reports were interrupted by the account limit).
- Primary sources and searches: `.firecrawl/circuit_*`, `.firecrawl/theory_*`, `.firecrawl/hardware_*` plus earlier named sources. Do not repeat completed searches without a specific unresolved question.

## Version state

The main paper is the exact restored backup at `paper/backups/2026-10-22_before_revision/`; current prior-revision simulation code was intentionally not rolled back. `RESEARCH_FIRST_REVIEW_2026-10-23.md` and the 777-line CSV record unresolved paper issues. The source SHA256 is 593c2b22a7aac7b8d0106dd6a804b40cb37634ed78395d4f1eb74ab8c5cf9dc1. Bibliography SHA256 is 2129e91caedb7322581d0333aae4af50d5126bfd6b02b6da7dba4ec1d694987b. PDF SHA256 is 2c26c61db6a2756d8cee0ab5d6851851f7ba0de0a61e0e3abca9373e6875e231.

## Account / tool status

No IBM login, API key access, paid plan or QPU job. Qiskit/Runtime/Aer/NumPy/SciPy/OR-Tools installed; Qrisp absent; no C compiler detected on PATH. IBM free quota/eligibility unknown. Agents hit account usage limit before final reports; use saved files rather than restarting their research. User's last steering was `continue`, revoking the brief pause; no automation or reminder was created.
