# One map from the $z^+,d$ AA(1) proposal

Date: 2026-08-17

Status: `EXECUTED_ONCE_VALID_NOT_MET`.

The two genuine map residuals $z^+-z$ and $d-c$ give the standard
unregularized full-Gram AA(1) proposal

$$
c_{\mathrm{next}}=0.48771444550122545\,z^++
0.51228555449877455\,d.
$$

Its modal, leakage height-$L_2$, and same-weight maximum-$|D_L|$ direction
ratios are `0.99411674241637549`, `0.93884958302279575`, and
`0.79362266755606770`.  All are strictly below one, and all 8880
reconstructed points are positive.  These checks authorize only this
direction; they do not predict convergence.  AA(2) is skipped by the
minimum-order rule.

One activation permits exactly one evaluation

$$
e=G_2(c_{\mathrm{next}}).
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
`VALID_NOT_MET`.  If the map is valid, its physical residual is
$e-c_{\mathrm{next}}$.  Neither $e-d$ nor $e-z^+$ is a fixed-point
residual.  This batch permits no second physical map.

## Frozen result

The host was activated exactly once from source commit
`fa154ed421598c5f91fe9b5bd1878af46c993386`.  All four strict terminals,
the independent `proposal-aa1` checker, and the 21/21 receipt passed.  The
physical residual $e-c_{\mathrm{next}}$ is

$$
(R_\rho,R_L,D_L,R_a)=
(6.422349219104007\times10^{-8},\,
7.777215945396249\times10^{-4},\,
1.139502273872495\times10^{-6}\ \mathrm{cm}^{-1},\,
1.266857654692717\times10^{-6}).
$$

Only $R_\rho$ passes the original AND gate, hence `VALID_NOT_MET`.  There
was no retry or automatic successor.

The next standard AA(1), formed only from $d-c$ and
$e-c_{\mathrm{next}}$, fails because its leakage direction ratios are
`1.4891030102954350` and `1.5185498258021630`.  The subsequently permitted
standard AA(2), formed from the latest three genuine residuals, also fails:
its leakage direction ratios are `1.3654718014730096` and
`1.3434921133428195`.  Thus
`AA1_DIRECTION_FAIL_AA2_DIRECTION_FAIL`.  No proposal is published and no
second map is run.
