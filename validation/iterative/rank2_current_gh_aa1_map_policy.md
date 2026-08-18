# One map from the latest admissible AA(1) proposal

Date: 2026-08-17

Status: `EXECUTED_ONCE_VALID_NOT_MET`.

The latest two genuine residuals, $g-q_1$ and $h-q_2$, give the standard
unregularized full-Gram proposal

$$
q_3=0.92198482219461153\,g+
0.078015177805388483\,h.
$$

Its denominator is `7.3007449964465324e-13`.  Its modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are
`0.11971305975561962`, `0.47525043616253554`, and
`0.70441518119387303`, all strictly below one.  These parameter-free
screens authorize one direction; they do not predict convergence.

One activation permits exactly one physical map

$$
i=G_2(q_3).
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
cutoff, empirical parameter, mixed-unit objective, older-window search, or
AA(3).

The host may return only `INVALID_MAP`, `TOLERANCE_MET`, or
`VALID_NOT_MET`.  If valid, the physical residual is $i-q_3$; $i-h$ is not
a fixed-point residual.  This batch permits no second physical map.

## Post-run record

The stage was activated exactly once from source commit
`a802ba1031414c4e25c74791f1043d453b5387c1`.  All four strict terminals,
the independent `proposal-aa1` checker, and the 21/21 receipt passed.  The
physical residual $i-q_3$ is

$$
(R_\rho,R_L,D_L,R_a)=
(6.422348086676521\times10^{-8},\,
4.699542341368844\times10^{-4},\,
6.885675247758627\times10^{-7}\ \mathrm{cm}^{-1},\,
1.040590980549194\times10^{-6}).
$$

$R_\rho$ passes the original AND gate; $R_L$ and $R_a$ do not.  The map is
therefore `VALID_NOT_MET`, with no retry or automatic successor.  AA(1) on
$h-q_2$ and $i-q_3$ fails only its leakage height-$L_2$ direction screen at
`1.0001541854604454`.  Only then, standard unregularized AA(2) on the latest
three genuine residuals gives direction ratios `0.085602787687317231`,
`0.50064418931908561`, and `0.44048518991529284`, all strictly below one.
Thus `AA1_DIRECTION_FAIL_AA2_DIRECTION_PASS`.  No durable proposal is
published and no second physical map is run.  The artifact's
`continuation_policy.md` remains the receipt-protected pre-run policy copy.
See [rank2_current_gh_aa1_map_result.md](rank2_current_gh_aa1_map_result.md).
