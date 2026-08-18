# One map from the latest admissible AA(1) proposal

Date: 2026-08-18

Status: `PREPARED_DEFAULT_OFF`.

Standard unregularized AA(1) uses only the two latest genuine residuals
$n-q_7$ and $o-q_8$ and gives

$$
q_9=0.14445266271586943\,n+
0.85554733728413057\,o.
$$

Its exact denominator is `3.8680130073227605e-14`.  Its modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are
`0.99405602856832498`, `0.78327883203609316`, and
`0.82926667695332601`, all strictly below one.  These parameter-free
screens authorize one direction; they do not predict convergence.

One explicit activation permits exactly one physical map

$$
p=G_2(q_9).
$$

The unchanged fixed-rank-two host performs three online radial fixed-source
solves and one axial solve.  Acceptance uses only the original AND gate

$$
R_\rho\le5\times10^{-7},\qquad
R_L\le5\times10^{-7},\qquad
R_a\le5\times10^{-7}.
$$

Dimensional $D_L\,[\mathrm{cm}^{-1}]$ remains diagnostic only.  If valid,
the physical fixed-point residual is $p-q_9$; $p-o$ is not that residual.
The 120 s radial and 180 s axial limits are process-safety bounds, not model
coefficients.

One activation permits one attempt.  There is no retry, fallback, automatic
successor, relaxation, damping, clipping, fit, regularization, pseudoinverse,
condition cutoff, empirical parameter, mixed-unit objective, older-window
search, or AA(3).  This batch permits no second physical map.
