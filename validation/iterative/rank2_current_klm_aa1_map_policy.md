# One map from the latest admissible AA(1) proposal

Date: 2026-08-17

Status: `EXECUTED_ONCE_VALID_NOT_MET`.

The latest consecutive genuine residuals, $l-k$ and $m-q_6$, give the
standard unconstrained full-Gram proposal

$$
q_7=0.71958187611175339\,l+
0.28041812388824661\,m.
$$

Its denominator is `1.4220277430317252e-11`.  Its modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are
`0.089320649038882691`, `0.82454368960985658`, and
`0.56421285796347498`, all strictly below one.  These parameter-free screens
authorize one direction; they do not predict convergence.

One explicit activation permits exactly one physical map

$$
n=G_2(q_7).
$$

The unchanged fixed-rank-two host performs three online radial fixed-source
solves and one axial solve.  Acceptance uses only the original AND gate

$$
R_\rho\le5\times10^{-7},\qquad
R_L\le5\times10^{-7},\qquad
R_a\le5\times10^{-7}.
$$

Dimensional $D_L\,[\mathrm{cm}^{-1}]$ remains diagnostic only.  If valid,
the physical fixed-point residual is $n-q_7$; $n-m$ is not that residual.
The 120 s radial and 180 s axial limits are process-safety bounds, not model
coefficients.

One activation permits one attempt.  There is no retry, fallback, automatic
successor, relaxation, damping, clipping, fit, regularization, pseudoinverse,
condition cutoff, empirical parameter, mixed-unit objective, older-window
search, or AA(3).  This batch permits no second physical map.

## Post-run record

The stage was activated exactly once from source commit
`767fe7da92de238fdb7face911cf7e487c7e4901`.  All four strict terminals,
the independent `proposal-aa1` checker, and the 21/21 receipt passed.  The
physical residual $n-q_7$ is

$$
(R_\rho,R_L,D_L,R_a)=
(6.422348086676521\times10^{-8},\,
4.990742346753720\times10^{-4},\,
7.312337402254343\times10^{-7}\ \mathrm{cm}^{-1},\,
4.639312542887599\times10^{-7}).
$$

$R_\rho$ and $R_a$ pass the original AND gate; $R_L$ does not, so the map
is `VALID_NOT_MET`.  Standard AA(1) on $m-q_6,n-q_7$ fails the two leakage
direction screens.  Only then, standard unregularized AA(2) on
$l-k,m-q_6,n-q_7$ passes all three direction screens.  The offline
classification is `AA1_DIRECTION_FAIL_AA2_DIRECTION_PASS`; no durable
successor was published and no second map was run.  The artifact's
`continuation_policy.md` remains the receipt-protected pre-run policy copy.
See [rank2_current_klm_aa1_map_result.md](rank2_current_klm_aa1_map_result.md).
