# Source-primitive QFT reconstruction: bounded pilot

Date:24October2026. This is OUR reconstruction using published Draper/Wilkening arithmetic primitives, not the authors’ released fractional-LP oracle or their optimized full parallel schedule. Existing production code, historical results and manuscript remain unchanged.

## Outcome and scope

The gate-level pilot is feasible. It generated full fixed-depth clean LP-prefix predicates with quantum prefix and threshold inputs, then simulated the actual complete gate lists. No opaque arithmetic reference was substituted for the circuit. The common-basis comparison also shows why a favorable result against our old Boolean arithmetic compiler cannot establish superiority to prior work.

SIMULATED dense arithmetic kernels:93kernel cases,1,848basis columns,0columns failing tolerance1e-8. Maximum dense-kernel amplitude error 1.44e-15.

SIMULATED independent tensor-readout cross-check:3random complex-superposition circuits,168amplitudes compared with dense statevectors,0failures; maximum amplitude disagreement 1.29e-11.

SIMULATED complete compiled predicates: 28method-cases on7listed fixed-depth fixtures,608basis columns,0output/phase/cleanup failures at tolerance1e-8. Maximum expected-output amplitude error 5.38e-13; maximum normalization error 1.08e-12; maximum complementary probability 4.44e-16. All28conditions completed;0natural size/time caps and0simulator exceptions in the final tensor run.

These figures apply only to the listed 1–3item fixtures, fixed depths and all their encoded prefix/threshold/target inputs with zero initial workspace. They are not all700benchmark inputs, a full quantum backtracking walk, hardware execution, an asymptotic speedup or a priority result.

## Sources versus declared reconstruction choices

Primary sources were read before derivation/code: ThomasG.Draper, Addition on a Quantum Computer, arXiv:quant-ph/0008033v1(2000), Sections3(Eqs1–2) and5, https://arxiv.org/html/quant-ph/0008033v1 ; Wilkeninget al.2025SupplementE.3–E.5, https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41534-025-01097-8/MediaObjects/41534_2025_1097_MOESM1_ESM.pdf . Cached primary text was used; the rejected direct-download access-page PDF was not evidence.

| Component | Attribution and choice |
|---|---|
| Full no-SWAP QFT, phase additions |DraperSecs3/5; ideal rotations, no AQFT truncation.|
| Merged rotations for a known constant, inverse phases for subtraction |WilkeningE.3/E.4; serial control strategy, with no copied-control parallelization claimed.|
| Classical constant comparison |WilkeningE.5EqsS.27–S.30 orthogonal lexicographic clauses; explicit negative-control flips and clean multi-control decomposition.|
| Multi-control decomposition |Both a literal generic clean-AND-to-CX policy and a direct-small-control/serial-chain policy are retained after independent review flagged a weak-baseline risk. Neither reproduces the authors’ optimized parallel cycle schedule.|
| Quantum versus quantum comparison |OUR explicit extra-sign-bit QFT subtraction, copy high bit, reverse; prevents interpreting unsigned wrap as a sign.|
| FractionalLP completion |OUR declared reduced cross-product comparison P*b+r*a<tau*b and same prefix/suffix scan as the compact control. The scalar arithmetic identity is elementary. No authors’ divider is claimed or eliminated.|
| Global cleanup and interface |OUR compute/copy/uncompute assembly with classical fixed depth, quantum prefix and tau, arbitrary target, zero workspace; all work restored in checked columns.|

The two QFT methods and compact-exact implement the same strict LP pruning predicate on identical inputs. Compact-dual implements a weaker safe bound and is therefore a resource/pruning portfolio comparator, not an equal Boolean-function baseline.

## Same logical gate model

Every method is decomposed with Qiskit2.4.2 into arbitrary-angle{u,cx},optimization_level0,all-to-all connectivity. Counts and depths below are DERIVED from actual decomposed gate lists. u gates are treated as logical unit primitives; there is no Clifford+T rotation synthesis, device calibration or physical-duration interpretation. Native counts are retained in the raw JSON. Comparing these numbers with the paper’s analytic cycles still requires reconciling its optimized scheduling and full-algorithm model.

| Fixture(w;v;W;d) | Method | Qubits | u | cx | Decomposed depth |
|---|---|---:|---:|---:|---:|
|[1];[1];0;1|qft_direct|23|731|433|418|
|[1];[1];0;1|qft_source_generic|25|749|447|418|
|[1];[1];0;1|compact_exact|23|871|797|1140|
|[1];[1];0;1|compact_dual|15|401|344|492|
|[1];[1];1;1|qft_direct|25|813|481|442|
|[1];[1];1;1|qft_source_generic|27|831|495|442|
|[1];[1];1;1|compact_exact|25|989|897|1284|
|[1];[1];1;1|compact_dual|18|709|604|884|
|[1, 2];[1, 1];1;0|qft_direct|40|4377|2641|2330|
|[1, 2];[1, 1];1;0|qft_source_generic|41|4449|2697|2377|
|[1, 2];[1, 1];1;0|compact_exact|38|4075|3689|5174|
|[1, 2];[1, 1];1;0|compact_dual|18|493|404|578|
|[1, 2];[1, 1];1;1|qft_direct|37|2932|1765|1616|
|[1, 2];[1, 1];1;1|qft_source_generic|38|2986|1807|1663|
|[1, 2];[1, 1];1;1|compact_exact|35|2824|2559|3606|
|[1, 2];[1, 1];1;1|compact_dual|19|785|668|972|
|[2, 3];[3, 2];2;1|qft_direct|47|6832|4229|2789|
|[2, 3];[3, 2];2;1|qft_source_generic|48|6904|4285|2845|
|[2, 3];[3, 2];2;1|compact_exact|43|4644|4255|6008|
|[2, 3];[3, 2];2;1|compact_dual|24|1229|1072|1542|
|[2, 4];[1, 2];3;1|qft_direct|48|5590|3469|2326|
|[2, 4];[1, 2];3;1|qft_source_generic|49|5644|3511|2373|
|[2, 4];[1, 2];3;1|compact_exact|44|3898|3515|4980|
|[2, 4];[1, 2];3;1|compact_dual|23|797|668|960|
|[2, 3, 1];[2, 1, 1];3;1|qft_direct|53|10371|6425|4026|
|[2, 3, 1];[2, 1, 1];3;1|qft_source_generic|54|10461|6495|4073|
|[2, 3, 1];[2, 1, 1];3;1|compact_exact|49|6965|6353|8970|
|[2, 3, 1];[2, 1, 1];3;1|compact_dual|25|1309|1132|1634|

The unfavorable controls matter: the QFT reconstruction frequently has lower decomposed depth than our compact exact circuit. On the three-item fixture QFTdirect gives53qubits,6,425cx,depth4,026 versus compact-exact49qubits,6,353cx,depth8,970. Root-dual is25qubits,1,132cx,depth1,634 on that same fixed-depth input, but this does not account for a different search tree.

Even root-dual is not uniformly cheaper in this gate model: on the one-item all-fit fixture QFTdirect uses481cx/depth442 versus compact-dual604cx/depth884, while using25rather than18qubits. This counterexample to an unqualified cheaper-bound claim is retained. These tiny results cannot select the best policy for large instances.

## Simulator readout failure and resolution

The first report-save attempt failed on a NumPy integer JSON counter before full jobs ran; it is logged. The next full-gate run returned15/16expected-amplitude failures on its first condition and stopped immediately. Original pilot_results.json,stdout/stderr and source snapshot are retained.

Independent triage reproduced a specific Aer0.17.2 disagreement: save_amplitudes([1,9])returned[0,0] for a compiled23-qubit circuit whose saved probabilities place all mass at9. Manual contraction of the same saved MPS tensors gives amplitude9=1+roundoff. This did not itself approve untested inputs. The final run uses explicit Gamma/lambda contraction, independently checked against dense statevectors on random complex superpositions, and checks normalization as well as expected amplitude and complementary probability. The final output is saved separately as pilot_results_mps_tensor.json; failed raw output was not edited.

Final MPS configuration: ideal/noiseless simulator, truncation_threshold0,maximum_bond_dimension18446744073709551615(default unbounded sentinel),single CPU thread. This records the actual configuration rather than treating a truncated MPS heuristic as an exact simulation. Numerical tolerance1e-8 is distinct from the ideal arithmetic definition and from a hardware/rotation synthesis error budget.

## Files and finite next gate

- Derivation before code: derivation_before_code.md; independent reviewer confirmed phase/endianness, sign/width logic and identified the comparator control improvement.
- New builder: simulation/source_faithful_20261024/qft_reconstruction.py .
- Pilot and explicit tensor readout: pilot.py,mps_readout.py .
- Final raw result: pilot_results_mps_tensor.json; attempted/readout failure artifacts and attempt_log.md retained.
- Rerun: python -B -X utf8 research_log/source_faithful_20261024/pilot.py .

Expansion should follow independent review of the assembled circuit and all model differences. A justified next bounded step would use fixed-depth slices of the preregistered five-class n12pilot, with the same interfaces and explicit build/simulation caps. Before making algorithm-level claims, compose coherent depth/reflections/recovery or retain the predicate-only scope and sensitivity analysis. A fair external performance comparison additionally needs a documented reconstruction of all missing upstream fractional-oracle choices and the same gate/error/scheduling convention. This successful pilot does not establish a substantial advance over the authors’ full QTG method or guarantee journal acceptance.
