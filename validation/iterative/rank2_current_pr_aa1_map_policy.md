# One map from the $p,r$ AA(1) proposal

Date: 2026-08-18

Status: `PREPARED_DEFAULT_OFF`.

Standard unregularized AA(1) uses only the genuine residuals $p-q_9$ and
$r-q_{10}$ and gives

$$
q_{11}=0.21697843452735655\,p+
0.78302156547264345\,r.
$$

Its exact denominator is `2.1912767600921286e-12`.  Its modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are
`0.50304720552788507`, `0.87862793996767796`, and
`0.82134690926235421`, all strictly below one.  These parameter-free screens
authorize one direction; they do not predict convergence.

One explicit activation permits exactly one physical map

$$
s=G_2(q_{11}).
$$

The unchanged fixed-rank-two host performs three online radial fixed-source
solves and one axial solve.  Acceptance uses only the original AND gate

$$
R_\rho\le5\times10^{-7},\qquad
R_L\le5\times10^{-7},\qquad
R_a\le5\times10^{-7}.
$$

Dimensional $D_L\,[\mathrm{cm}^{-1}]$ remains diagnostic only.  If valid,
the physical fixed-point residual is $s-q_{11}$; $s-r$ is not that residual.
The 120 s radial and 180 s axial limits are process-safety bounds, not model
coefficients.

One activation permits one attempt.  There is no retry, fallback, automatic
successor, relaxation, damping, clipping, fit, regularization, pseudoinverse,
condition cutoff, empirical parameter, mixed-unit objective, older-window
search, or AA(3).  This batch permits no second physical map.
