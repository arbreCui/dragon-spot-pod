# One map from the $r,s$ AA(1) proposal

Date: 2026-08-18

Status: `EXECUTED_ONCE_VALID_NOT_MET`.

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

## Post-run record

The stage was activated exactly once from source commit
`3f3df1d58f03bfc7fb990e476d2f9358089f484c`.  All four strict terminals,
the independent `proposal-aa1` checker, and the 21/21 receipt passed.  The
physical residual $t-q_{12}$ is

$$
(R_\rho,R_L,D_L,R_a)=
(0,\,4.684047945454728\times10^{-4},\,
6.862974260002375\times10^{-7}\ \mathrm{cm}^{-1},\,
5.179951998082914\times10^{-7}).
$$

$R_\rho$ passes the original AND gate; $R_L$ and $R_a$ do not.  The map is
therefore `VALID_NOT_MET`.  AA(1) on $s-q_{11}$ and $t-q_{12}$ has direction
ratios `0.72586264533733025`, `0.72631617652927194`, and
`0.90812221320053177`, all strictly below one.  Thus
`AA1_DIRECTION_PASS_AA2_SKIPPED`; AA(2) is not calculated.  No durable
proposal is published and no second physical map is run.  The artifact's
`continuation_policy.md` remains the receipt-protected pre-run policy copy.
See [rank2_current_rs_aa1_map_result.md](rank2_current_rs_aa1_map_result.md).
