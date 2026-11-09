# Independent preparation/readout triage, 2026-10-25

The original `circuit_vertex_adversarial.json` phase failure is retained unchanged.
Its raw direct-QFT ties/zero-profit fixture had amplitude error
0.21540057075978067, workspace leakage 0 and normalization error about 2e-12.
Those are SIMULATED amplitudes and DERIVED residuals, not measured hardware.
The present controls do not approve the oracle; they isolate a failure of the
input-preparation/backend path before any oracle gates are applied.

## Scope and unchanged acceptance rule

Weights [2,4,1], profits [1,2,0], capacity 3, depth 1, bank {0,1/2},
five logical wires including target, 22 total wires. The random complex input
has 32 amplitudes and seed 2026102529. Every comparison keeps the original
1e-8 amplitude tolerance. No oracle, old source, or original raw data was edited.
Host time is MEASURED; amplitudes are SIMULATED; norms, overlaps and errors are
DERIVED; seed, tolerance and controls are HARDCODED.

## Controls and falsified explanations

`theory_phase_preparation_triage_v2.py/json` runs each readout in a separate
circuit. This removes possible interference between multiple saves.

* On five wires, opaque `initialize` matches the desired complex vector to
  5.68e-13 with all three readouts: contracted saved MPS, native Aer saved
  amplitudes, native Aer saved statevector.
* On 22 wires with the same five-wire opaque initialization and no oracle,
  custom saved-MPS contraction and native Aer saved statevector agree on
  malformed norm 118.9813321417693 and maximum amplitude error 3.41439769234.
  Thus the custom tensor contraction alone cannot explain the failure.
  Native saved-amplitudes results are also inconsistent; they are retained.
* `enable_truncation=False` does not repair this control.
* The phase-aligned error remains about 3.4144, so global phase does not repair
  the observed malformed state.
* Decomposing the same initialization into gates before the MPS run gives
  maximum amplitude error 2.119e-11, norm error below 3e-15, for all three
  separate readouts. Decomposed unitary StatePreparation agrees.
* A separate dense Statevector calculation of the 22-wire initialize-only
  circuit returns the desired input exactly in this control, with zero
  workspace probability.

`theory_phase_threshold_controls.py/json` repeats the no-oracle preparation on
22 wires with default threshold (1e-16), 0, 1e-20 and 1e-16. All four opaque
initialize controls have the same malformed MPS state; all four decomposed
initializations pass at the original tolerance. This does not support a claim
that zero truncation threshold is the specific cause.

## Retained failed diagnostic

`theory_phase_preparation_triage.py/json` is the first diagnostic. It combined
save types and then stopped on an unsupported opaque `StatePreparation`
instruction. It is preserved, not counted as a completed comparison. The v2
separate-save controls resolve the ambiguity introduced by that attempt.

## Defensible conclusion and remaining boundary

For these installed versions (Qiskit 2.4.2, Qiskit Aer 0.17.2), this fixture's
opaque partial-register initialize-to-MPS path is unreliable. The exact
backend implementation defect remains UNRESOLVED. No claim is made that a
specific upstream issue or cutoff explains it. Primitive-gate input preparation
is an independently checked alternative for a new retained oracle run, while
the original failure must stay in the audit ledger. The current evidence alone
does not certify an oracle's superposition action; the parent/circuit agent's
separate dense-oracle control and fresh primitive-preparation oracle run are
required for that narrower conclusion. The original amplitude tolerance must
not be loosened.
