# One map from the latest admissible AA(1) proposal

Date: 2026-08-17

Status: `EXECUTED_ONCE_VALID_NOT_MET`.

The latest two genuine fixed-point residuals, $i-q_3$ and $j-q_4$, give
the standard unregularized full-Gram proposal

$$
q_5=1.1922339465680236\,i-0.19223394656802359\,j.
$$

Its denominator is `1.1217162258501826e-11`.  Its modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are
`0.064424480296712869`, `0.93186663298811390`, and
`0.97357313211276764`, all strictly below one.  The negative affine
coefficient is the unchanged result of standard unconstrained AA(1); it is
not clipped, damped, fitted, or replaced by an empirical parameter.  These
parameter-free screens authorize one direction; they do not predict
convergence.

One explicit activation permits exactly one physical map

$$
k=G_2(q_5).
$$

The unchanged fixed-rank-two host performs three online radial fixed-source
solves and one axial solve.  Acceptance uses only the original AND gate

$$
R_\rho\le5\times10^{-7},\qquad
R_L\le5\times10^{-7},\qquad
R_a\le5\times10^{-7}.
$$

Dimensional $D_L\,[\mathrm{cm}^{-1}]$ remains diagnostic only.  If the map
is valid, its physical fixed-point residual is $k-q_5$; $k-j$ is not that
residual.  The 120 s radial and 180 s axial limits are process-safety bounds,
not model coefficients.

One activation permits one attempt.  There is no retry, fallback, automatic
successor, relaxation, damping, clipping, fit, regularization, pseudoinverse,
condition cutoff, empirical parameter, mixed-unit objective, older-window
search, or AA(3).  This batch permits no second physical map.

## Post-run record

The stage was activated exactly once from source commit
`fbe6058300a93cc771bc050f81397aa2f563b9e7`.  All four strict terminals,
the independent `proposal-aa1` checker, and the 21/21 receipt passed.  The
physical residual $k-q_5$ is

$$
(R_\rho,R_L,D_L,R_a)=
(6.422348086676521\times10^{-8},\,
3.413471840828782\times10^{-4},\,
5.001347744837403\times10^{-7}\ \mathrm{cm}^{-1},\,
1.330790586136073\times10^{-6}).
$$

$R_\rho$ passes the original AND gate; $R_L$ and $R_a$ do not, so the map
is `VALID_NOT_MET`.  AA(1) on $j-q_4,k-q_5$ was tried first and failed only
the same-weight maximum-$|D_L|$ direction screen at
`1.0008704340662933`.  Only then, standard unregularized AA(2) on
$i-q_3,j-q_4,k-q_5$ was evaluated and also failed that screen at
`1.2201877109802688`.  The final offline classification is
`AA1_DIRECTION_FAIL_AA2_DIRECTION_FAIL`; no direction was published and no
second map was run.  The artifact's `continuation_policy.md` remains the
receipt-protected pre-run policy copy.  See
[rank2_current_ij_aa1_map_result.md](rank2_current_ij_aa1_map_result.md).
