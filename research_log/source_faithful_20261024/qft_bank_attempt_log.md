# QFT bank implementation attempt log

25 October 2026. The separate QFT bank was derived and independently reviewed
before implementation. The reviewer identified the legacy positive-value
validator mismatch; the new bank module alone was extended with its own
nonnegative-value validator before its first executable test. No earlier
production module was modified.

The first full-gate bank pilot completed 18/18 method cases, 296/296 columns,
0 predicate/phase/cleanup failures and 0 exact-rational bank-versus-LP predicate
disagreements. Its raw JSON also contains a reserved field named
`exact_rational_bank_predicate_disagreements` initialized to zero and never
updated. That field is HARDCODED/UNUSED, is NOT a measured validation result,
and must not be reported as an additional independent check. The genuinely
evaluated reference check is `exact_rational_LP_predicate_disagreements`:
it compares the exact rational bank predicate against the independently
computed fractional LP predicate for every tested prefix/threshold.
The raw JSON is preserved unmodified; the unused field is removed from
future script runs.

The supplied-bank gate target is computed from the independent rational
minimum of its multipliers, then compared to actual full compiled MPS
amplitudes and norm. Thus the gate simulation is an independent check of
the circuit's supplied-bank action, not a resource-based or arithmetic-only
surrogate. Large resource cohorts remain outside this simulation scope.

Before the merged-control run, input validation was tightened to reject
noninteger/bool depth and bool numerator/denominator pairs explicitly.
This changes no arithmetic or tested integer-domain netlist. The forthcoming
merged validation records its own source hashes rather than overwriting the
earlier raw pilot's hashes.

Snapshot recovery first encountered a Windows path-separator KeyError before
writing any snapshot. Its lookup now normalizes path separators only. A
recovered initial snapshot is accepted ONLY if its complete byte SHA256
matches the pre-recorded original raw pilot hash. This is source recovery,
not reconstruction or modification of numerical raw results.
