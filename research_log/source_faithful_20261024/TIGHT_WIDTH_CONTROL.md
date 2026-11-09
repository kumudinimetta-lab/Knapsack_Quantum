# Reduced-denominator width control

The cross-product predicate has already been derived and independently checked: U=P+r*a_i/b_i rejects iff P*b_i+r*a_i<tau*b_i. The old global width covered unreduced maxima S*wmax+W*vmax and tau_max*wmax, despite using reduced constants in each product. This is safe but potentially inflated.

Before implementing the control, the parent derived the sharper common bound max_i(max(S*b_i+W*a_i,tau_max*b_i)); every feasible P<=S and residual r<=W, with nonnegative a_i,b_i. Taking its bit length plus a padding bit covers every exact numerator and threshold product. No signed arithmetic or predicate changes result. This is a competent-baseline width correction, not a new theorem. The explicit standalone note was recorded immediately after the code change; the formula was derived in the parent analysis before that change. No claim of earlier external preregistration is made.

The original rounding.py source is preserved as rounding_before_tight_exact.py, matching the existing upper-control records' module hash. Adding the exact-mode branch does not alter the previously tested upper-mode arithmetic. New exact-mode tests are separate; earlier raw outputs are not edited or reattached to a new hash. Production circuits.py and compact/QFT sources remain pinned unless a separately labelled new control is created.
