# Exact integer-pruning bank construction results

25 October 2026. Manuscript and prior raw data unchanged. No hardware jobs.
Priority and publication significance remain UNRESOLVED. The constructions
preserve the Boolean predicate LP upper bound < integer threshold on a static
exact-efficiency prefix order; they do not return exact LP values, LP-integrality
flags, a greedy witness or a dynamic LP branching variable.

## What was constructed

1. **Root-tail exact bank:** ratios above the root fractional split are
   dominated for every such prefix. The remaining tail ratios plus0 reproduce
   exact fractional LP values. This requires no reachability DP.
2. **Minimum density-grid bank:** prefix weight reachability quotients all
   assignments into (depth, remaining capacity). Integer accrued profit cancels.
   Convex dual bounds turn each state's integer-floor coverage into an interval
   of candidate density indices; standard greedy interval stabbing gives the
   minimum number on that finite grid.
3. **DP-free sufficient bank:** adjacent density groups can share a multiplier
   under the strict radius |lambda-rho|<1/(denominator(rho)*total_group_weight).
   This has no capacity DP and is conservative, not a minimum actual bank.
4. **Minimum arbitrary-rational bank:** exact continuous coverage intervals
   come from suffix-prefix affine inequalities. Greedy predecessor-cell
   stabbing attains minimum cardinality among all nonnegative rational
   multipliers. Cell mediants keep representative coefficients modest; no
   minimum-bit-width/gate claim is made.

All derivations preceded their implementation, with separate parent/reviewer
algebra approval. Generic LP duality, convex interval geometry and greedy
stabbing are known; the proposed research delta is their precisely scoped
all-prefix integer-predicate compiler and its actual reversible resource result,
not an invention of those ingredients.

## Broad construction results

All counts of constructed banks/intervals are DERIVED exact outputs; work/time
counts are MEASURED classical preprocessing; configured caps are HARDCODED.
No number here is quantum runtime or a success probability.

| Panel | Cases | Median full density grid | Median root tail | Median minimum grid bank | Median minimum rational bank | Median DP-free sufficient bank |
|---|---:|---:|---:|---:|---:|---:|
| Original R=100 | 700 | 17 | 8 | 7 | 7 | 8 |
| Exact preprocessed cores | 700 | 11 | 6 | 5 | 5 | 6 |
| Independent R=1,000,000 | 45 | 25 | 10 | Not attempted beyond capacity cap | Not attempted beyond capacity cap | 10 |

The exact grid compiler improved beyond root-tail size on313 original and328
core inputs. Allowing arbitrary rational multipliers reduced cardinality below
the exact grid minimum on128 original and105 core inputs. Its largest bank was16;
all mediant numerator/denominator widths were at most10 bits on those R=100
panels. The DP-free sufficient construction shrank root-tail size on96 original,
75 core and0 independent inputs. Lack of compression is retained.

All original/core exact constructions finished within their declared caps.
The45 high-capacity cases explicitly fall back to safe root-tail banks for
reachability-based methods, with NO minimum-bank claim. The DP-free construction
handles all45 directly, but did not reduce their root-tail banks.

## Necessary negative findings

- **Preprocessing can solve the original optimization more cheaply.** On the
  original700 inputs, continuous compilation took37.42 aggregate host seconds,
  versus0.299 seconds for the local simple profit-DP reference. Core compilation
  took24.24 seconds versus0.206 seconds. These diagnostic timings are not a
  competitive solver benchmark, but decisively forbid treating the W-bit
  compilation as free evidence of end-to-end quantum optimization advantage.
- **Minimum grid is not minimum rational.** The gcd-normalized two-item input
  w=[1,1],v=[1,1],W=1 needs both density-grid multipliers0 and1, but the singleton
  off-grid multiplier1/2 preserves all integer pruning predicates.
- **No universal small bank.** A repaired gcd-one family with n main weights2,
  profits4(n-i)+1, capacity2*floor(n/2)+1 and a unit dummy has pairwise disjoint
  continuous coverage intervals. Its minimum rational bank has n-floor(n/2)+1
  entries. This is a linear certificate-cardinality barrier, not hardness of
  knapsack or a quantum-query lower bound; the family is easy classically.
- **Fewest multipliers need not mean fewest gates.** Different rational
  coefficients change accumulator widths and constant multiplication costs.
  Actual compiled comparisons against exact scans and stronger safe bounds
  are required before asserting a resource improvement.

## Checks and artifacts

Exact-grid/DP-free probe:207 instances,8,630 feasible prefixes,0 floor errors
for either construction;207 brute grid-minimum checks,0 mismatches;63 repaired
barrier sizes,0 mismatches. Continuous probe:127 instances,2,247 feasible
prefixes,0 floor errors;73,463 endpoint/cell checks,0 errors;112 brute finite-cell
minimum checks,0 errors,15 declared candidate-count caps;31 repaired barrier
sizes,0 mismatches. Independent reviewer tests use their own LP-vertex reference
and are retained separately. These scopes do not certify untested circuits.

Code: `simulation/source_faithful_20261024/compressed_bank.py` and NEW
`continuous_bank.py`. Raw construction JSONL and summary files:
`theory_banks_{main,core,independent}*`, `theory_banks_dp_free*`, and
`theory_banks_continuous_{main,core,independent}*` in this directory. Continuous
interval-frequency tables are retained as gzip sidecars with hashes in
`theory_continuous_interval_records/`; they were not discarded to shorten logs.
Pre-run manifests/source snapshots preserve which implementation produced each
version. Earlier failed inferences and all declared caps remain recorded.

Source/assumption mapping and proofs: `theory_compressed_bank_derivation.md`
and `theory_continuous_bank_derivation.md`. Circuit synthesis/testing/results
are a separate parent/circuit-agent phase and must not be inferred from this
construction report.
