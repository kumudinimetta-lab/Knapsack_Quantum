# Fixed-depth compact arithmetic sensitivity

Existing production module and broad-run artifacts were not edited. This is a separate fixed-depth quantum-prefix/threshold pilot, with arithmetic derivation recorded before code.

Primary primitive: Cuccaro, Draper, Kutin and Moulton, A new quantum ripple-carry addition circuit, arXiv:quant-ph/0410184v1 (2004), Sections2 and4.3: https://arxiv.org/html/quant-ph/0410184v1 . The simple MAJ/UMA adder is used; optimized Section3 counts are not claimed.

SIMULATED primitives: 5,456 basis columns, 0 mismatches. SIMULATED fixed-depth predicates: 128 method-cases, 2,645,200 basis columns, 0 predicate mismatches, 0 dirty columns.

Tiny tests cover every depth on8listed instances, including empty, zero capacity, all-fit, ties/gcd and overweight items; each fixed-depth test exhausts all prefix/threshold/target encodings. The pilot uses all5generator classes at n12, seed12000, depth6; each method-case checks131,072columns. No case was dropped;0unexpected exceptions and0build caps occurred.

Independent nonempty dense Qiskit check: weights[1],values[1],capacity0,depth1, compact root dual15qubits,16nonzero input amplitudes, maximum amplitude error0,0checks above1e-12. Other3methods exceeded the HARDCODED18-qubit dense cap and remain recorded as skipped.

All resource counts below are DERIVED from explicit X/CX/CCX gate lists. Quoted depth uses the same greedy gate-layer resource function as the out-of-place compiler. This is not a physical runtime, lower bound or best-known arithmetic circuit.

| Input | Method | Qubits | CX | CCX | Gate depth |
|---|---|---:|---:|---:|---:|
|tiny4 d=2|outplace_dual|86|171|50|69|
|tiny4 d=2|compact_dual|33|530|233|582|
|tiny4 d=2|outplace_exact|338|751|222|209|
|tiny4 d=2|compact_exact|65|2959|1199|3018|
|uncorrelated_n12_s12000_R100 d=6|outplace_dual|540|1179|404|215|
|uncorrelated_n12_s12000_R100 d=6|compact_dual|65|2314|989|2466|
|uncorrelated_n12_s12000_R100 d=6|outplace_exact|3540|8303|2636|1003|
|uncorrelated_n12_s12000_R100 d=6|compact_exact|132|23219|9287|23132|
|weakly_correlated_n12_s12000_R100 d=6|outplace_dual|466|999|352|225|
|weakly_correlated_n12_s12000_R100 d=6|compact_dual|65|2134|921|2278|
|weakly_correlated_n12_s12000_R100 d=6|outplace_exact|2829|6623|2052|883|
|weakly_correlated_n12_s12000_R100 d=6|compact_exact|132|18015|7271|18046|
|strongly_correlated_n12_s12000_R100 d=6|outplace_dual|537|1181|398|187|
|strongly_correlated_n12_s12000_R100 d=6|compact_dual|67|2558|1101|2724|
|strongly_correlated_n12_s12000_R100 d=6|outplace_exact|3929|9225|2954|1065|
|strongly_correlated_n12_s12000_R100 d=6|compact_exact|132|26591|10583|26430|
|subset_sum_n12_s12000_R100 d=6|outplace_dual|192|379|120|119|
|subset_sum_n12_s12000_R100 d=6|compact_dual|53|918|397|974|
|subset_sum_n12_s12000_R100 d=6|outplace_exact|1846|4289|1256|783|
|subset_sum_n12_s12000_R100 d=6|compact_exact|132|11651|4823|11926|
|inverse_strongly_n12_s12000_R100 d=6|outplace_dual|563|1237|422|201|
|inverse_strongly_n12_s12000_R100 d=6|compact_dual|68|2630|1129|2790|
|inverse_strongly_n12_s12000_R100 d=6|outplace_exact|3518|8245|2616|1043|
|inverse_strongly_n12_s12000_R100 d=6|compact_exact|134|22763|9079|22612|

The compact construction strongly reduces workspace but increases gate count and serial depth on this pilot. This unfavorable depth result is retained. Root dual remains less expensive than exactLP within each compiler on the5fixed-depth pilot inputs; this is a scoped ordering observation, not proof for all700instances or a universal advantage.

The fixed-depth comparison controls dispatcher architecture. It does not show that a coherent-depth compact circuit, root-weighted reflection, acceptance procedure or witness-recovery circuit has been synthesized. A small ancilla count alone cannot make the current entire optimizer hardware-ready.

Files: simulation/pruning_study_20261023/compact_sensitivity.py; research_log/pruning_study_20261023/compact_validation.py; compact_validation_results.json; compact_derivation_before_implementation.md.

Rerun: python -B -X utf8 research_log/pruning_study_20261023/compact_validation.py

Cost scaling and gate counts are construction-dependent. Further optimizing only one comparator would confound this control. The present result demonstrates a concrete space-versus-depth tradeoff and provides a check against attributing every resource advantage to an inflated out-of-place compiler.
