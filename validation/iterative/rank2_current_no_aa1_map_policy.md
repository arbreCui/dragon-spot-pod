# One map from the latest admissible AA(1) proposal

Date: 2026-08-18

Status: `EXECUTED_ONCE_VALID_NOT_MET`.

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

## Post-run record

The stage was activated exactly once from source commit
`8f1eb8fc19a3ee71a839f0661712910cac9b6a89`.  All four strict terminals,
the independent `proposal-aa1` checker, and the 21/21 receipt passed.  The
physical residual $p-q_9$ is

$$
(R_\rho,R_L,D_L,R_a)=
(6.422348086676521\times10^{-8},\,
6.792180645546773\times10^{-4},\,
9.951763786375523\times10^{-7}\ \mathrm{cm}^{-1},\,
1.761650656565653\times10^{-6}).
$$

$R_\rho$ passes the original AND gate; $R_L$ and $R_a$ do not.  The map is
therefore `VALID_NOT_MET`.  AA(1) on $o-q_8$ and $p-q_9$ has direction
ratios `0.12764993865086841`, `0.82141838136874701`, and
`0.89227926518865730`, all strictly below one.  Thus
`AA1_DIRECTION_PASS_AA2_SKIPPED`; AA(2) is not calculated.  No durable
proposal is published and no second physical map is run.  The artifact's
`continuation_policy.md` remains the receipt-protected pre-run policy copy.
See [rank2_current_no_aa1_map_result.md](rank2_current_no_aa1_map_result.md).
