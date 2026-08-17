# One map from the post-$z^+$ AA(1) proposal

Date: 2026-08-17

Status: `EXECUTED_ONCE_VALID_NOT_MET`.

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

## Frozen result

The host was activated exactly once from source commit
`246a4cf48e7b2babbf04c089d9d09a0074f079e2`.  All four strict terminals,
the independent `proposal-aa1` checker, and the 21/21 receipt passed.  The
physical residual $d-c$ is

$$
(R_\rho,R_L,D_L,R_a)=
(6.422348086676521\times10^{-8},\,
4.958958534883100\times10^{-4},\,
7.265771273523569\times10^{-7}\ \mathrm{cm}^{-1},\,
1.309164007655304\times10^{-6}).
$$

Only $R_\rho$ passes the original AND gate, hence `VALID_NOT_MET`.  There
was no retry or automatic successor.

The next offline standard AA(1), formed only from $z^+-z$ and $d-c$, has
weights `0.48771444550122545` and `0.51228555449877455`.  Its modal,
leakage height-$L_2$, and same-weight maximum-$|D_L|$ ratios are
`0.99411674241637549`, `0.93884958302279575`, and
`0.79362266755606770`.  Thus `AA1_DIRECTION_PASS_AA2_SKIPPED`.  The next
proposal is not materialized and no second map is run.
