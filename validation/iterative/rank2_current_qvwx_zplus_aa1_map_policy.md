# One map from the post-$z^+$ AA(1) proposal

Date: 2026-08-17

Status: `PREPARED_NOT_RUN`.

The genuine consecutive residuals $z-y$ and $z^+-z$ give the unique
standard full-Gram AA(1) proposal

$$
c=0.41511181447765411\,z+
0.58488818552234589\,z^+.
$$

Its modal, leakage height-$L_2$, and same-weight maximum-$|D_L|$ direction
ratios are `0.0933575730`, `0.4221465030`, and `0.6106565232`.  All three
are strictly below one, and all 8880 reconstructed points are positive.
These are authorization checks, not convergence evidence.  AA(2) is
skipped by the minimum-order rule.

One activation permits exactly one evaluation

$$
d=G_2(c).
$$

The unchanged fixed-rank-two host performs three online radial fixed-source
solves and one axial solve.  Rank, basis, equations, normalization, decks,
strict inner predicates, and the original outer AND gate remain unchanged:

$$
R_\rho\le5\times10^{-7},\qquad
R_L\le5\times10^{-7},\qquad
R_a\le5\times10^{-7}.
$$

Dimensional $D_L\,[\mathrm{cm}^{-1}]$ remains diagnostic only.  The 120 s
radial and 180 s axial limits are process-safety bounds.  There is no retry,
fallback, automatic successor, relaxation, damping, clipping, fit,
regularization, pseudoinverse, condition cutoff, empirical parameter,
mixed-unit objective, older-window search, or AA(3).

The host may return only `INVALID_MAP`, `TOLERANCE_MET`, or
`VALID_NOT_MET`.  If the map is valid, its physical residual is $d-c$.
Neither $d-z^+$ nor $d-z$ is a fixed-point residual.  This batch permits no
second physical map.
