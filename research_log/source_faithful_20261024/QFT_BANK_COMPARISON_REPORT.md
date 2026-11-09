# Same-function QFT bank / fractional-LP predicate comparison

25 October 2026, Asia/Calcutta. Circuit-track report. Manuscript, bibliography,
historical experimental data and pinned earlier production modules were not
edited. The primary resource claim is a comparison of TWO OUR constructions,
not a measured performance comparison against released Wilkening R1 code.

## What was completed

DERIVED: On the predeclared 105 representative positive-profit instances,
the exact-inverse-cancelled static bank construction used fewer qubits,
arbitrary-angle u gates and CX gates than our equally cancelled exact
fractional-LP scan in all 105 matched cases. The median bank/LP ratios were
0.4624 qubits, 0.4099 u gates, and 0.4091 CX gates. Depth was mixed: median
0.9433, lower in 57 cases and HIGHER in 48, with a worst ratio of 1.9165.
This supports a circuit construction/resource tradeoff; it does not establish
uniform depth savings, a full-optimizer speedup, device advantage, external
state-of-the-art superiority, or priority.

All 840 requested resource rows completed, with 0 capped and 0 error rows.
The five-input precursor completed all 40 rows, 0 caps/errors. The earlier
seven-method 105-input LP/compact sensitivity ledger is preserved separately:
735 completed rows, 0 caps/errors. These are distinct runs and are not pooled
as independent samples. Host compilation/profile elapsed times were MEASURED
283.12 s, 9.42 s and 268.77 s respectively; they are not quantum runtimes.

## Primary sources and scope of reconstruction

Primary sources read before circuit derivation/code:

* Thomas G. Draper, *Addition on a Quantum Computer*, arXiv:quant-ph/0008033v1
  (2000), Sections 3/5, equations (1)--(2):
  https://arxiv.org/html/quant-ph/0008033v1 . Full ideal QFT additions are used;
  approximate rotation omission is not used.
* Sören Wilkening, Andreea-Iulia Lefterovici, Lennart Binkowski, Michael Perk,
  Sándor P. Fekete and Tobias J. Osborne, *A quantum algorithm for solving
  0-1 Knapsack problems*, npj Quantum Information (2025), Supplement E.3--E.5
  and F.2: https://doi.org/10.1038/s41534-025-01097-8 ; supplement
  https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41534-025-01097-8/MediaObjects/41534_2025_1097_MOESM1_ESM.pdf .
  E.3 gives known-constant QFT additions and rotation/cancellation opportunities;
  E.4 subtraction reverses phase signs; E.5 equations S.27--S.30 give constant
  lexicographic comparison. F.2 already uses fractional greedy pruning in
  quantum knapsack branch-and-bound. That broad idea is prior work.

The released R1 audit remains `../advance_comparison_20261024/source_implementation_audit.md`.
Its archived source SHA256 is
`8f479e92a7fc8003df85e9e548052d2a7fe21ed7885ed64245e52203b0e3491e`.
The inspected QBnB call path uses classical fractional arithmetic and numerical
resource estimators; no same-interface clean LP gate list was found there.
That bounded finding is not proof of absence elsewhere and is not evidence
of a performance win. We did not execute or replace the authors' QTG solver.

Our LP scan completes the missing coherent predicate with reduced rational
cross products and an explicit quantum/quantum comparator. Those choices
are OUR reconstruction, not attributed to the released R1 implementation.
No quantum divider is assumed to exist in R1 and no claim of eliminating
the authors' divider is made. Both constructions use a quantum threshold
register; this is a matched internal interface, not necessarily the authors'
classical incumbent convention. Neither source parallel copied-control
schedules nor an optimal comparator/multiplier are reproduced.

## Interface, bank provenance and proof assumptions

Classical input: positive integer weights, nonnegative integer capacity,
fixed depth d, and a static data-only bank of nonnegative reduced Fractions.
The shared resource cohort has POSITIVE profits. The bank module additionally
accepts nonnegative/zero profits, checked separately on tiny circuits; no
zero-profit performance comparison to the older positive-only LP builder
is implied. Quantum inputs are d efficiency-sorted prefix bits and
tb=max(1,bit_length(sum(values)+1)) threshold bits, plus an arbitrary output
target. Work starts and ends zero. Invalid input data are rejected; the
compiled action is output XOR rejection.

The supplied-bank predicate is not automatically the LP predicate. It is
equal for ALL integer thresholds under the independently reviewed bank
floor-coverage certificate (`theory_compressed_bank_derivation.md`, B/F).
The DP-free bank conservatively covers adjacent density-breakpoint intervals;
it is not a minimum actual bank or a minimum arbitrary-rational bank. Its
construction does not enumerate reachable capacities, use an optimum or
select multipliers from observed quantum resource outcomes.

All 105 bank lists come from `theory_banks_dp_free.jsonl`; the driver reproduces
each list with `build_dp_free_bank` and stops on any difference. Stored DP-based
comparison fields in that ledger are NOT used for choosing the bank. Data-only
preprocessing time is recorded separately in each row. Classical preprocessing
is not charged as quantum gates and must not be omitted in a future end-to-end
runtime study. The selected bank sizes in this cohort range from 2 to 16.

For lambda=a/b, c_i=b*v_i-a*w_i, define

    A = a*W + sum_i max(c_i,0),
    D = sum_assigned [(1-x_i)*max(c_i,0)+x_i*max(-c_i,0)].

Then the scaled node dual is A-D, so rejection is exactly A<D+b*tau.
The accumulator width covers max(A,sum_assigned|c_i|+b*tau_max), with one
padding bit. Capacity is checked independently. Each bank entry computes
its loss/threshold accumulator, copies its comparison flag, and reverses
the arithmetic. Flags are combined by OR, not parity; after output-copy,
the entire computation is reversed. The independent reviewer approved the
signs, widths, overlapping-flag OR and cleanup before the large compilation.

The LP product widths use reduced a_i/b_i consistently on BOTH engines:
max_i(max(S*b_i+W*a_i,tau_max*b_i)), plus a padding bit, S=sum(values).
Using unreduced item maxima could overcharge tied-density LP cases; that
conservative historical control remains separately preserved and is not
the primary comparison here.

## Gate validation: numerical scope and explicit counts

SIMULATED, with HARDCODED amplitude tolerance 1e-8:

| Actual complete compiled predicates | Cases | Basis columns | Predicate/phase/cleanup failures | Exact-rational bank-vs-LP predicate disagreements |
|---|---:|---:|---:|---:|
| Unmerged bank, direct/generic controls |18|296|0|0|
| Exact-inverse-cancelled bank AND LP, direct/generic controls |32|544|0|0|

Each row's basis columns exhaust its tiny declared prefix/threshold domain
and BOTH output target values, with zero initial workspace. Fixtures include
empty data, zero capacity, all-fit, real fractional splits, exact equality,
ties, overweight prefixes, maximum encoded threshold, and zero-valued items.
The unmerged bank checks contain 108 columns with overlapping dual reject
flags, so replacing OR by parity would not be hidden by mutually exclusive
test data. Maximum expected-amplitude errors were 1.33e-13 and 4.10e-13.

The actual complete gate networks were executed by noiseless Aer MPS with
truncation threshold 0 and no finite bond limit. Readout explicitly contracts
saved Gamma/lambda tensors; expected amplitude near +1, norm and complementary
probability test output, column phase and workspace cleanup. Numerical
tolerance is not fixed-point precision, rotation-synthesis error or QPU noise.
Aer's configured `zero_threshold` is recorded, including its default 1e-10.

Independent reviewer checks add a complex entangled-state test on
w=[5,2,3],v=[0,3,2],W=4,d=2, bank={0,1/2,2/3,4/6}: 64 logical amplitudes,
including 32 overlapping-reject and 16 overweight encodings; raw+cancelled
networks have 0 failures at 1e-8, maximum error 6.80e-10, workspace leakage
1.11e-16. This separately checks gcd deduplication and relative phases.
Raw record: `reviewer_qft_bank_probe.json`.

These are NOT exhaustive MPS/statevector tests of the 105 or 700 instances.
The larger resource netlists have DERIVED resources; symbolic correctness
arguments and the theory bank checks do not become large-circuit simulations.

Earlier primitive checks remain distinct: 1,848 dense adder/comparator columns,
0 failures; 608 original full LP/compact predicate columns, 0 failures; 564
normalized-width control columns, 0 failures. Exact resource profiling agreed
with full Qiskit transpilation on 55 prior/new method cases and 8 additional
independent cases, 0 discrepancies. These scopes are not summed into one
homogeneous validation sample.

## Resource protocol and cancellation sensitivity

Predeclared cohort: 5 instance classes x 7 sizes (12,14,16,18,20,22,24)
x trials (0,1,2) =105 inputs, depth floor(n/2). Full ID lists and input SHA256
are in the manifest. There are eight rows per input: LP/bank x direct/generic
controls x raw/cancelled netlist. No capped or failed case was removed.

All counts below are DERIVED in the same all-to-all arbitrary-angle {u,cx}
basis with optimization_level=0. Depth follows actual gate-wire dependencies.
Native netlists are expanded by actual installed-Qiskit local decomposition
skeletons, whose counts/depth were crosschecked against full transpilation.
There is no finite-rotation synthesis, hardware routing, T cost or wall-clock
QPU interpretation. HARDCODED per-condition caps are 150,000 wires, 2,000,000
native/expanded gates and 60 seconds per build/profile operation.

The primary control safely removes literal inverse gates across only disjoint
intervening gates, identically on BOTH LP and bank. In particular this cancels
serial adjacent inverse-QFT/QFT pairs rather than charging avoidable source
assembly overhead. It preserves widths/interfaces, uses no approximate angle
test, and does not merge diagonal angles or implement copied-control source
parallelization. The helper's independent dense unitary controls had 30
conditions, 0 failures, max difference 6.94e-16. Complete merged predicates
were then independently tested as above.

| Form, bank/LP median ratio | Qubits | u | CX | Depth | Depth worse |
|---|---:|---:|---:|---:|---:|
|Cancelled, direct (PRIMARY)|0.4624|0.4099|0.4091|0.9433|48/105|
|Cancelled, generic|0.4652|0.4146|0.4146|0.9771|52/105|
|Raw, direct control|0.4624|0.8073|0.7999|1.4878|81/105|
|Raw, generic control|0.4652|0.8088|0.8018|1.5034|81/105|

Uncancelled bank circuits were WORSE in CX on 32/105 direct-control cases,
and worse in u on 35/105. Those negative controls remain in the raw ledger.
Cancellation substantially changes comparisons and benefits the bank's long
accumulation sums, so its policy must accompany any reported resource ratio.
The raw controls are sensitivity evidence, not an optimized source baseline.

Primary direct cancelled bank/LP ratio ranges: qubits [0.3974,0.5000],
u [0.0942,0.7517], CX [0.0933,0.7506], depth [0.0798,1.9165]. The bank is
lower in all four metrics on 57/105 cases. On the other 48 it trades lower
qubits/gates for higher serial depth; a scalar 'cost advantage' would hide
that tradeoff.

| Class (21 inputs each), cancelled direct bank/LP median | Qubits | u | CX | Depth | Depth worse |
|---|---:|---:|---:|---:|---:|
|uncorrelated|0.4677|0.4203|0.4188|0.9953|10|
|weakly correlated|0.4688|0.4997|0.4995|1.1243|17|
|strongly correlated|0.4545|0.3282|0.3280|0.7860|0|
|subset sum|0.4189|0.1212|0.1212|0.1832|0|
|inverse strongly correlated|0.4840|0.6273|0.6267|1.5048|21|

Depth regressions occur on EVERY inverse-strongly-correlated instance here.
This is a material negative result, not noise to remove. The theory's linear
bank-cardinality barrier and off-grid counterexamples further rule out claims
of uniformly small or globally minimum rational banks.

## Files, failures and reproducibility

* API: `simulation/source_faithful_20261024/qft_bank.py::build_qft_bank(...)`;
  explicit bank geometry and rational normalization are exposed separately.
* Derivations: `qft_bank_derivation_before_code.md`,
  `normalized_width_derivation_before_code.md`, `derivation_before_code.md`.
* Primary raw resource ledger/manifest/analysis:
  `qft_bank_full105_rows.jsonl`, `qft_bank_full105_manifest.json`,
  `qft_bank_full105_analysis.json`; five-input versions use `pilot5`.
* Validation: `qft_bank_pilot_results.json`, `qft_bank_merged_validation.json`,
  reviewer files named above. Source/runtime inputs are hashed.
* Current completed-run source bytes are preserved in
  `source_snapshot_qft_bank105/`, verified against the PRE-RECORDED completed
  run source hashes before copying. The snapshot manifest is
  `qft_bank105_source_snapshot_manifest.json`. The shared LP width builder,
  QFT engine and profiler hashes also match the preserved earlier 105 run.
* The first pilot's source versions were recovered only after their complete
  byte hashes matched the PRE-RECORDED raw hashes. See
  `qft_bank_initial_source_snapshots.json`; no raw numerical result was edited.
* `qft_bank_attempt_log.md` records the input-domain correction, an unused
  HARDCODED reserved zero field in the initial raw JSON (not reported as a
  measured validation), and a path-separator snapshot-recovery failure.
* Earlier failed Aer `save_amplitudes` readout remains untouched in the
  original pilot files and attempt log. Independent probability/MPS/dense
  tests identified that readout discrepancy; the replacement tensor readout
  was checked independently before the present bank experiments. This is
  not silent deletion of a failed circuit test.

No experiments beyond the predeclared 105-input expansion were performed
for this report. A substantial improvement over released full quantum
algorithms, best possible source assembly, or physical runtime remains
UNRESOLVED. The strongest supported result is a reproducible same-function,
same-interface gate-construction tradeoff under explicit compiler choices.
