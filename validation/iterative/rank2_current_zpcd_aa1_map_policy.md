# One map from the $z^+,d$ AA(1) proposal

Date: 2026-08-17

Status: `PREPARED_NOT_RUN`.

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
