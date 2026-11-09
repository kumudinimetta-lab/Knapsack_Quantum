# Quantum game theory and IBM hardware: feasibility review

Date: 23 October 2026, Asia/Calcutta. Research feasibility only. No manuscript changes, account access, QPU job submissions, new experiments, or claim of an established novel result.

## Recommendation

Investigate a controlled IBM-hardware study connected to the existing exact LP preprocessing and answer-agnostic threshold predicate. Do not add quantum game theory solely as a novelty label. A game-theoretic extension would change the research problem and require its own model, equilibrium analysis, literature audit and fair classical comparison.

Novelty of either proposed extension is **UNRESOLVED**. A positive experimental result, practical advantage or journal decision cannot be promised.

## Verified IBM access information

- Official plans overview: https://quantum.cloud.ibm.com/docs/en/guides/plans-overview. Open Plan allows up to 10 QPU minutes per rolling 28-day window, free, with Open instances in us-east.
- Official update: https://www.ibm.com/quantum/blog/open-plan-updates. A non-trial Open Plan user who has used 20 minutes of runtime within a 12-month period may opt into a one-time 180-minute allocation for the following 12 months. Eligibility, opt-in availability and remaining allocation for this user's account have not been checked.
- The announcement says ibm_kingston (Heron r2) was added to the Open fleet. This is not a statement that the device is currently operational or accessible to this particular account; check the account/backend before selecting it.
- These are publisher-reported access limits, not scientific measurements produced by this project. Queue waiting time, execution time and reproducibility across calibrations are different concerns.

## Literature overlap

1. Wilkening et al., *A quantum algorithm for solving 0-1 Knapsack problems*, npj Quantum Information 11, 146 (2025), https://doi.org/10.1038/s41534-025-01097-8. Previously checked primary paper: QTG, amplitude amplification/maximum finding, resource and classical-solver comparisons. A generic quantum knapsack circuit is not a sufficient originality claim.
2. Laurin Demmler and Maximilian Hess, *A Nested Amplitude Amplification Protocol for the Binary Knapsack Problem*, primary preprint https://arxiv.org/html/2604.05776v1. Abstract and relevant introduction/results inspected: nested amplification at a tunable tree depth, QTG preparation, classical amplitude tracking and comparisons with baseline GAS. Treat as a preprint; its complexity claims are not imported into our theorem. A simple proposal to split a knapsack search and amplify subsets must be compared with this work.
3. *Quantum Game Theory-Based Cloud Resource Allocation: A Novel Approach*, Mathematics 13(9), 1392 (2025), https://www.mdpi.com/2227-7390/13/9/1392. Its primary abstract discusses a quantum game-theoretic allocation model. This establishes topical prior work, not independent verification of its asserted advantages or relevance to every knapsack game.
4. *Quantum Game Theory meets Quantum Networks*, primary preprint https://arxiv.org/html/2306.08928v2. Its abstract and game-model sections discuss players, strategies, information, utility and equilibria in entanglement distribution. It does not establish a theorem for our single-decision-maker knapsack problem. Quantum/network performance claims in that paper are not adopted as our own findings.

Search snapshots and source text are preserved under `.firecrawl/` with `20261023` names. No-source and unrelated search results are retained in the original search files. No paper reference was deleted.

## Concrete IBM pilot proposal

Question: For the same knapsack inputs and objective threshold, when does exact classical LP fixing improve the probability of obtaining a valid improving assignment on noisy hardware, and how much of the improvement is due to classical fixing versus quantum amplification?

Use a matched two-by-two design:

| Method | Exact LP fixing | Amplitude amplification |
|---|---|---|
| Full-space sampling | No | No |
| Core-space sampling | Yes | No |
| Full-space threshold search | No | Yes |
| Core-space threshold search | Yes | Yes |

This controls for the possibility that the gain comes entirely from classical preprocessing. Comparisons must preserve the original problem through fixed-in values, residual capacities and reconstructed assignments. Shared thresholds must be transformed correctly after fixing.

Start with a small pilot only after exact ideal-simulation checks and backend-target compilation. Choose size, circuit count, shot counts, iteration policy and a hard execution budget from the compiled cost and available free quota; no numerical pilot outcome or resource count is currently claimed. All choices would be HARDCODED planned configurations until executed.

- The circuit must compute feasibility and value from the input, not mark a supplied optimal bitstring. Classical exact solutions may score outputs but must not secretly choose oracle answers or “optimal” iteration counts.
- Use thresholds obtained from an explicitly specified incumbent/threshold policy. If answer-known thresholds are chosen for component diagnostics, label them as such; they are not an optimization run.
- The primary fixed-threshold outcome is the probability of returning an assignment meeting that threshold, not the probability of finding the global optimum unless a complete optimizer is actually executed.
- If a full optimum-finding loop is added, account for all value-search/witness calls, failures and final reconstruction. A hardware Grover component is not the Montanaro backtracking walk.
- Report MEASURED shot counts, elapsed/QPU usage and empirical success proportions; DERIVED confidence intervals and compiled gate resources; SIMULATED ideal/noisy reference distributions; SCHEDULED job budgets and HARDCODED configurations separately.
- Match shot budgets for shot comparisons and actual QPU-time budgets for QPU-time comparisons. They are different experiments. Keep classical preprocessing cost and classical baseline times visible; do not equate QPU time, gates and classical nodes.
- Keep trials where no variables fix, the core is empty, circuits fail compilation, jobs fail, or outcomes are poor. Specify any mitigation, postselection and associated overhead.
- Retain backend/instance/plan identifiers, job IDs, input seeds, source/circuit hashes, transpilation seed and options, submitted circuit, calibration snapshot if accessible, shots and full counts. Repeat across execution windows if the quota permits; do not infer a universal hardware size limit.

An observed gain would be component/hardware evidence. It would not automatically be a new algorithm, a quantum speedup, or enough novelty for publication. A precise construction/resource improvement or a distinct, reproducible finding beyond existing studies would still need to be established. A negative result must be retained.

The clean LP-node predicate and coherent depth wrapper from the preserved revision are separate, potentially large components. Their full-walk feasibility must be checked rather than assumed. Start with classical fixing plus the small threshold predicate; add coherent node pruning only when its gate/qubit budget is demonstrated feasible. The existing hardware script should be reviewed before reuse; the earlier provenance problems should not be repeated.

## Genuine game-theory alternative

A possible separate problem is competitive allocation under a capacity constraint: multiple agents have defined actions/information/payoffs, and a specified allocation rule determines feasibility and utility. Quantum strategies might use entangled advice or another precisely defined resource, but novelty and any equilibrium/payoff advantage remain UNRESOLVED.

Required work includes the game specification, exact classical mixed/correlated baseline under the same information/communication rules, quantum strategy and equilibrium definition, exploitability or unilateral-deviation checks, and a proof or reproducible numerical result. A central optimizer's better knapsack solution is not by itself a Nash-equilibrium result. Adding entanglement or describing branching as a game is not sufficient.

This changes the question from solving one knapsack optimization problem to strategic interaction among agents. It is a larger departure from the current manuscript, so it is not the recommended immediate repair path.

## Decision boundary

Proceed from research question to offline pilot design and novelty comparison before consuming hardware allocation. Credentials should be configured locally; they should not be pasted into chat. No account eligibility or available quota is assumed. No account creation, paid plan, credential inspection or hardware execution was performed for this feasibility answer.
