# Independent compact-arithmetic review plan

23 October 2026. Read the primary Cuccaro et al. quant-ph/0410184v1 Sections2 and4.3, and the circuit agent's derivation before inspecting implementation. The simple MAJ/UMA and restored high-carry comparison match the stated algebra. No optimized Section3 counts or original arithmetic theorem is claimed.

Test primitives with an independent scalar computational-basis gate interpreter, rather than the shared bit-plane simulator. Exhaust all operands for widths1..5 for modular addition and strict comparison, both comparator targets; check unchanged left operand, correct right sum, clean carry, exact reversibility and all other bits unchanged. Test controlled constant addition/subtraction under both controls for widths1..4, all constants and accumulator values. Each such test starts with clean scratch/carry and does not assume an arbitrary-dirty-workspace implementation.

Then compare compact/out-of-place root-dual and exact-LP predicates on matching fixed-depth quantum-threshold interfaces, all d on selected tiny inputs, all encoded prefix/threshold columns and both target bits. Use the independent LP-vertex reference from the earlier reviewer audit, and a direct rational Lagrangian reference for root dual. Retain failures and stop the affected claim. Do not compare fixed-depth compact resources to a coherent-depth baseline as if they were the same function.

Outputs SIMULATED; exact references and circuit resources DERIVED; sample domains HARDCODED. This does not validate a full coherent depth dispatcher or a quantum walk. Production circuits.py and previous outputs remain unchanged.

An additional independent dense check will use w=[1,2],v=[1,3],W=2,d=1 and the compact dual predicate. Put independent complex random amplitudes on every encoded prefix/threshold/target basis input with clean workspace, seed2026102321, and compare Qiskit's dense evolution with direct rational-dual XOR action. Cap at20 total qubits; retain skip rather than allocating a larger statevector. This is a different, larger nonempty-input support than the circuit agent's sixteen-amplitude dense example.

The first build used22 qubits and was retained as SKIPPED_DENSE_QUBIT_CAP under the20-qubit policy. A separately named rerun permits22 qubits: each complex statevector is64MiB, a bounded local allocation. Keep the original skip JSON unchanged, and store the22-qubit run under a new filename. No larger cases or changed correctness metric are introduced.
