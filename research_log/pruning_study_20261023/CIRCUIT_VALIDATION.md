# Scoped circuit validation

Compiled predicates only; no full walk or QPU execution.

Total SIMULATED basis columns: 422,144; predicate mismatches: 0; dirty columns: 0.

Independent dense Qiskit checks were completed only for the empty-instance circuits under the 18-qubit dense cap; all eight nonempty dense candidates were retained as skipped.

The exact inputs, sampled seeds, method resources, exceptions, cap controls and dense results are in circuit_validation_results.json. All 3 injected budget controls raised the expected cap. No unexpected exception occurred.

Run: python -B -X utf8 research_log/pruning_study_20261023/circuit_validation.py

Assumptions and width derivation: circuit_derivation_before_implementation.md.
