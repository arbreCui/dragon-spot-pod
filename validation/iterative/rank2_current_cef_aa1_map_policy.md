# One map from the latest minimum-order AA(1) proposal

Date: 2026-08-17

Status: `EXECUTED_ONCE_VALID_NOT_MET`.

The two genuine residuals $e-c_{\mathrm{next}}$ and $f-e$ give the standard
unregularized full-Gram proposal

$$
q_1=0.54317069088638781\,e+
0.45682930911361219\,f.
$$

Its modal, leakage height-$L_2$, and same-weight maximum-$|D_L|$ direction
ratios are `0.059424727376440133`, `0.19596354669013863`, and
`0.28717479223258224`, all strictly below one.  These parameter-free
screens authorize one direction; they do not predict convergence.

This default-off stage permits exactly one physical map

$$
g=G_2(q_1).
$$

The unchanged fixed-rank-two host performs three online radial fixed-source
solves and one axial solve.  Acceptance uses only the original AND gate

$$
R_\rho\le5\times10^{-7},\qquad
R_L\le5\times10^{-7},\qquad
R_a\le5\times10^{-7}.
$$

Dimensional $D_L\,[\mathrm{cm}^{-1}]$ remains diagnostic only.  The 120 s
radial and 180 s axial limits are process-safety bounds.  One activation
permits one attempt.  There is no retry, fallback, automatic successor,
relaxation, damping, clipping, fit, regularization, pseudoinverse, condition
cutoff, empirical parameter, older-window search, or AA(3).

The host may return only `INVALID_MAP`, `TOLERANCE_MET`, or
`VALID_NOT_MET`.  If valid, the physical residual is $g-q_1$; $g-f$ and
$g-e$ are not fixed-point residuals.  This batch permits no second physical
map.

## Frozen result

The stage was activated exactly once from source commit
`afbd273a52ac55cd2164b465f59eb94d7f110171`.  All four strict terminals,
the independent `proposal-aa1` checker, and the 21/21 receipt passed.  The
physical residual $g-q_1$ is

$$
(R_\rho,R_L,D_L,R_a)=
(6.422348086676521\times10^{-8},\,
3.858515151996695\times10^{-4},\,
5.653419066220522\times10^{-7}\ \mathrm{cm}^{-1},\,
1.741219010720005\times10^{-7}).
$$

$R_\rho$ and $R_a$ pass the original AND gate; $R_L$ does not.  The map is
therefore `VALID_NOT_MET`, with no retry or automatic successor.

The next standard AA(1), formed only from $f-e$ and $g-q_1$, fails because
its leakage direction ratios are `1.0164960989601337` and
`1.0021076380581850`.  The subsequently permitted standard AA(2), formed
from the latest three genuine residuals, has direction ratios
`0.33342566026806181`, `0.47696732762436056`, and
`0.39981312880450964`, all strictly below one.  Thus
`AA1_DIRECTION_FAIL_AA2_DIRECTION_PASS`.  No durable proposal is published
and no second physical map is run.
