# Final independent aggregation and report review

24 October 2026, Asia/Calcutta. Read-only review of the completed paired analysis. No production code, raw data, paired summary or manuscript was edited. Executable independent reconstruction: `final_aggregation_audit.py`; detailed result: `final_aggregation_audit_result.json`.

## Verdict and exact scope

**No aggregation mismatch was found.** The audited `paired_summary.json` SHA256 is `80211bcf478d04e721e341ea5de02603bcb4f3daa9f74302ae150f42b1fefa43`. This review independently reads raw manifests, resource ledgers, input registries, aliases, fixed-tree records and the retry overlay; it does not import or rerun `analyze_paired.py`. All ledger/hash/statistical verification counts below are DERIVED. This is not an additional quantum experiment, proof of novelty, full-walk validation or journal-acceptance assessment.

| Verification | Independently checked result |
|---|---|
| Resource attempts and exact manifest key sets |6,732 expected/observed;6,696 complete,36 qubit-budget caps;0 missing/duplicate/unexpected keys |
| Resource panels |4,200 main singles;210 representative wrappers;1,866 changed-core singles;96 changed-core wrappers;270 independent-stress attempts;90 scaling attempts |
| Build-cap origin |33 independent-stress and3 scaling cases; all fixed-point single scans; no claim of an unavoidable lower bound |
| Input/tree panels |1,460 globally unique input IDs:700 main,700 core,45 independent stress,15 scaling controls |
| Core aliases |700 checked;389 reuse original records with identical arrays/capacity;0 invalid mappings |
| Retry selection |183 unique method/input/target keys, exactly the complete initial time-cap key set |
| Retry outcome |23 extra completed fixed-tree conditions,160 node-capped conditions; same50,000-node cap, five-second allowance;0 conflicts |
| Summary source hashes |21 current sources matched their recorded hashes; circuit and driver dependency hashes in every resource manifest also matched |
| Descriptive resource groups |1,524 groups independently reconstructed;0 discrepancies |
| Descriptive proxy groups |7,875 groups independently reconstructed;0 discrepancies |
| Proxy coverage groups |96 groups independently reconstructed;0 discrepancies |
| Certificate/tree groups |20 groups independently reconstructed;0 discrepancies |

Each overlay's retained old dictionary and target tau match its original record exactly. New counts do not contradict the originally processed prefix; method, target and node budget agree. The immutable original source hashes match. Only fixed-tree conditions are replaced in the analysis copy: structural optimizer calls, statuses, completion rates and initial diagnostic budgets remain unchanged. Initial cap counts are separately retained. The23 extra completions are **conditions**, not23 additional independent instances or successful quantum optimizer runs.

## Ratios, joins and censoring

Resource comparisons join the same immutable input and circuit interface; unchanged-core reuse is valid only through the verified identical-data aliases. Wrapper omissions outside the105 preselected original/core representatives are labelled `not_scheduled_representative_panel`, rather than failed builds. Existing raw caps remain visible.

I independently reconstructed the full set of resource ratio groups and conditional `(C+h)*sqrt(T)` proxy groups, including group membership, medians, empirical indexed quantiles, extrema and below/equal/above-one counts. This checks per-input ratios rather than ratios of unrelated medians. The two threshold conditions are kept separate. Complete-pair denominators, nontrivial subsets and classically-resolved exclusions match the code's stated policies. Capped processed-node counts are never substituted for exact T in a complete proxy pair.

The shared-overhead formula and break-even rearrangement are correct. Its costs remain abstract gate/CCX/depth units; h is a sensitivity parameter measured in the exact predicate's cost unit, not a physical walk-overhead estimate. Example independent reconstructions on uncorrelated n12,seed12000 at incumbent+1:

- Cweak=864 CCX, Cexact=5668 CCX, Tweak=65 and Texact=37.
- R(0)=0.20204109667639464.
- R(Cexact)=0.7637340529457232.
- R(100*Cexact)=1.3143043764176394.

These figures are DERIVED arithmetic on MEASURED classical tree counts and DERIVED compiled gate counts. They are not executed quantum times or speedups. Remaining example values are retained in the audit JSON.

The final headline root-dual/incumbent+1 subsets reproduce the report:492 main complete pairs and473 core complete pairs after excluding root-rejected and classically resolved cases. Main medians R(0),R(Cexact),R(10*Cexact) are0.2384616196578761,0.9706593563624939 and1.5671347121268815; core medians are0.22468507377449898,0.9010274951973112 and1.456537858894113. The full main/core denominators are700 inputs each; the smaller denominators are conditional descriptive subsets, not evidence of a whole-benchmark advantage.

## Report consistency

I inspected `RESEARCH_RESULTS.md` and its generator against the final summary. The resource medians and pair counts, unfavorable wrapper/single-scan cases, fixed-tree complete/cap counts, initial optimizer completion counts and displayed overhead medians agree with the audited summary. The report appropriately separates original/core/scaling dependence, source overlap, scoped circuit simulation, logical resources, classical enumeration, theoretical schedules and physical execution.

The broad overlap with Wilkening et al. (2025), published Supplementary F.2, is real: the primary supplement explicitly benchmarks quantum knapsack branch-and-bound with a fractional-greedy bound and an optimistic known-optimum/tree-size resource model. The possible contribution therefore cannot be 'first LP-pruned quantum knapsack', generic tree-resource estimation or a new duality identity. The current construction/portfolio/control results require their narrower positioning. I independently read the relevant cached primary subsection during this final review; no numbered theorem is fabricated for it.

Two minor wording recommendations were communicated to the parent:

1. Use **predeclared/recorded protocol**, rather than *preregistered protocol*, unless a public or otherwise independently registered preregistration actually exists. A local before-experiment protocol is useful but should not imply a registry that was not used.
2. Say **311 smaller cores, including11 empty cores** to make the subset relation unambiguous. The11 empty cases are part of the311 reduced cases.

Resolution before checkpoint: the parent corrected the report generator/report to explicitly say locally predeclared with no external preregistration claimed, and confirmed the311/11 subset wording. These wording items are closed; they do not change the independently audited numerical summary.

No report-facing numerical contradiction was found. The following interpretation limits remain essential:

- The work curves are conditional algebraic models on observed trees; their reversal is not independently measured quantum acceleration or confirmation of square-root scaling.
- Complete-pair summaries are censored by budget completion and must retain their denominators and cap ledger beside claims.
- Optimizer completion rates are initial-budget classical accounting. Retrying fixed-tree conditions does not improve those optimizer rates.
- The36 high-bit construction caps demonstrate this compiler's resource budget, not intrinsic quantum hardness. Uniform scaling is an encoding control, and normalization removes it.
- Classically solved/empty cores need no detection calls; their component circuits describe functions rather than incurred QPU work.
- The compact arithmetic control has matching fixed-depth semantics and useful workspace/gate/depth trade-offs; it is not a coherent-depth700-input compact implementation.
- The portfolio, cross-product and known-duality results do not by themselves establish historical priority or sufficient journal significance. The restored manuscript still needs its previously identified local repairs.

## Final integrity status

The final independent reconstruction completed with **0 failures**. No new `RESEARCH_INTEGRITY_STOP` trigger was found in the completed aggregation or this report-consistency pass. Previous manuscript integrity items are not automatically cured by these computations. No publication outcome, QIP external review, acceptance rate, practical quantum advantage or complete walk implementation is asserted.
