# Manuscript review, 27 October 2026

Status: PARTIAL. Do not describe this as completed independent line-by-line certification.

The previous complete revision and its PDF are preserved in `../backups/before_line_audit_20261027/`. The original paper directory was checked against its 467-file manifest without conflicts. No raw experiment data were edited.

## Completed corrections

- Clarified that the denominator dividing the reduced density denominator belongs to the residual LP value, not the fractional item assignment. For weight 6, value 4, residual capacity 1, these are respectively 2/3 and 1/6. This repairs ambiguous terminology without changing the radius bound.
- Qualified the zero-capacity dual argument by nonempty suffix; the empty suffix is handled by multiplier zero.
- Qualified the Christiansen convergence statement by suitable parameters. The theory reviewer checked the cached primary text, section V-A, and its use of Binkowski et al., Theorem 12, Elementary Proof of QAOA Convergence (2024). This is an existence result, not an efficient parameter-finding or practical-depth guarantee.
- Replaced the IBM-specific and unrelated spectral/regression limitation checklist with the assumptions affecting the resource comparison: ideal arbitrary-angle gates, all-to-all connectivity, routing/synthesis/error costs, and missing complete-search operations. End-to-end runtime advantage remains unestablished.

## Figures and checks

Two explanatory vector figures were added. The coverage illustration is DERIVED, with five reachable states and 24 integer-threshold comparisons, zero mismatches. It is not additional benchmark evidence. The workflow is a conceptual compute-copy-uncompute diagram, not a literal gate diagram or hardware result. See FIGURE_EXAMPLE_CHECKS.json.

Fresh revision checks: 14 barrier endpoint checks and 1,376 arithmetic identity/width checks, zero mismatches; 40 references all cited; 201 abstract words. These checks do not establish absence of all errors.

## Outstanding review

The independent theory, implementation/evidence and hardware-value reviews were interrupted by an account usage limit before delivering their final audit documents. Preliminary mathematical findings above were applied, but the complete line inventory, implementation-to-claim reconciliation, and independent final adversarial review remain unfinished. Preserve this status on continuation.

No IBM jobs were submitted. A small hardware demonstration alone would not establish the general mathematical contract or the reported matched logical-resource comparison. Any hardware extension needs a defined, feasible question and comparable controls before it warrants inclusion.
