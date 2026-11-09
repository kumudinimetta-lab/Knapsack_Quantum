# Hardware feasibility pilot: assumptions before computation

23 October 2026. Read-only use of existing research code; no manuscript edits or hardware jobs.

Graph tools were searched first and no code-review-graph tools were available. Targeted file reads were used. Existing research-integrity stops remain in force: current code and the restored manuscript differ; no current hardware provenance or old hardware-table claim is approved by this pilot.

## Quantities and derivation

For an n-item input and integer threshold tau, define marked set M = {x: w.x <= W and v.x >= tau}. An exact enumeration here is evaluation ground truth only, never advice to an implemented optimizer. Let t = |M| and p = t / 2^n. Uniform sampling has probability p. Under an ideal clean phase predicate and uniform reflection, j Grover iterations yield sin^2((2j+1) arcsin(sqrt(p))). This is the standard amplitude-amplification diagnostic, not a new result, and neither a hardware-noise prediction nor a certified optimization run.

The existing hardware runner uses t to choose j. The feasibility pilot instead lists j=0,1,2 without making any policy selection from t. It separately records t for diagnostic scoring. No noisy model or regression is fitted.

For exact fixing from feasible incumbent L, the code only fixes an item when an exact upper bound on the opposite branch is < L. Therefore, any feasible assignment of value >= L must agree with every fixed item. Conversely, an assignment of the residual problem reconstructs to a feasible original assignment with value offset by the fixed-in profit. Thus, when tau >= L, the original and residual marked assignments are in bijection, with residual threshold tau' = tau - sum(fixed-in values). If f=n-m, the uniform marked fraction changes from t/2^n to t/2^m=2^f p. This is a hypothesis about the audited strict-fixing implementation, not a priority claim. Exhaustive selected-input checks will attempt to falsify it; thresholds below L are deliberately outside this claim.

Counterexample attempt to a stronger claim: increasing p does not always improve one-iteration Grover success. For p=1/4 the ideal one-iteration success is 1; for p=1/2 it is 1/2. Thus retaining the same number of iterations after reducing the search space can be harmful even under ideal arithmetic. This motivates policy control, rather than announcing a hardware benefit.

## Bounded compilation probe

Use the eight literal inputs already in simulation/run_ibm_hardware.py, parsed from the AST without importing its account/network code. Compile one Grover iteration around the existing arithmetic predicate to the abstract basis {rz, sx, x, cx}, with optimization level 1 and seed 23, under all-to-all and path connectivity. These are DERIVED compiler outputs for a specified abstract target, not IBM-target calibration metrics or measured QPU execution times. The backend, quota and physical calibration have not been accessed. Existing circuits are not edited.

Record failures, input hashes, dimensions, full count diagnostics, exact-fixing equivalence checks, and all compiler outputs. No statevector of the large arithmetic workspace is required for these static compiler metrics. This pilot cannot establish that the full backtracking walk fits hardware.

## Collection failures retained

- Initial firecrawl --status detected stored authentication but account info fetch failed; primary-source search succeeded after approved network execution. No account credential was read.
- Two initial Python attempts to read Firecrawl JSON without an explicit UTF-8 encoding failed with Windows cp1252 UnicodeDecodeError. Retried with UTF-8; source files unchanged.
- The first broad noisy-Grover search returned mostly introductory/non-primary pages; retained in .firecrawl/hardware_noise_grover_search.json. Targeted search found Vrana et al., Fault-ignorant Quantum Search, primary arXiv1307.0771v2 and DOI10.1088/1367-2630/16/7/073033.
