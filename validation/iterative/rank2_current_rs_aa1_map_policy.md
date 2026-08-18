# One map from the $r,s$ AA(1) proposal

Date: 2026-08-18

Status: `PREPARED_DEFAULT_OFF`.

Standard unregularized AA(1) uses only the genuine residuals $r-q_{10}$ and
$s-q_{11}$ and gives

$$
q_{12}=0.41267816249435374\,r+
0.58732183750564626\,s.
$$

Its exact denominator is `3.8071754534215003e-13`.  Its modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are
`0.30785297571708414`, `0.94676682054309913`, and
`0.98610570398914554`, all strictly below one.  These parameter-free screens
authorize one direction; they do not predict convergence.

One explicit activation permits exactly one physical map

$$
t=G_2(q_{12}).
$$

The unchanged fixed-rank-two host performs three online radial fixed-source
solves and one axial solve.  Acceptance uses only the original AND gate

$$
R_\rho\le5\times10^{-7},\qquad
R_L\le5\times10^{-7},\qquad
R_a\le5\times10^{-7}.
$$

Dimensional $D_L\,[\mathrm{cm}^{-1}]$ remains diagnostic only.  If valid,
the physical fixed-point residual is $t-q_{12}$; $t-s$ is not that residual.
The 120 s radial and 180 s axial limits are process-safety bounds, not model
coefficients.

One activation permits one attempt.  There is no retry, fallback, automatic
successor, relaxation, damping, clipping, fit, regularization, pseudoinverse,
condition cutoff, empirical parameter, mixed-unit objective, older-window
search, or AA(3).  This batch permits no second physical map.
