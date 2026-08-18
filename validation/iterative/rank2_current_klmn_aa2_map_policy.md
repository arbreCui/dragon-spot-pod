# One map from the latest admissible AA(2) proposal

Date: 2026-08-18

Status: `EXECUTED_ONCE_VALID_NOT_MET`.

Standard AA(1) from $m-q_6$ and $n-q_7$ failed its two leakage direction
screens.  Only then, the three latest genuine residuals $l-k$, $m-q_6$, and
$n-q_7$ gave the standard unregularized full-Gram AA(2) proposal

$$
q_8=0.37973124035268829\,l+
0.10995812065327257\,m+
0.51031063899403917\,n.
$$

The exact unregularized $2\times2$ determinant is
`3.0970099337137395e-24`.

Its modal, leakage height-$L_2$, and same-weight maximum-$|D_L|$ direction
ratios are `0.16177043590261239`, `0.45458049672516687`, and
`0.46901724246492071`, all strictly below one.  These parameter-free screens
authorize one direction; they do not predict convergence.

One explicit activation permits exactly one physical map

$$
o=G_2(q_8).
$$

The unchanged fixed-rank-two host performs three online radial fixed-source
solves and one axial solve.  Acceptance uses only the original AND gate

$$
R_\rho\le5\times10^{-7},\qquad
R_L\le5\times10^{-7},\qquad
R_a\le5\times10^{-7}.
$$

Dimensional $D_L\,[\mathrm{cm}^{-1}]$ remains diagnostic only.  If valid,
the physical fixed-point residual is $o-q_8$; $o-n$ is not that residual.
The 120 s radial and 180 s axial limits are process-safety bounds, not model
coefficients.

One activation permits one attempt.  There is no retry, fallback, automatic
successor, relaxation, damping, clipping, fit, regularization, pseudoinverse,
condition cutoff, empirical parameter, mixed-unit objective, older-window
search, or AA(3).  This batch permits no second physical map.

## Post-run record

The stage was activated exactly once from source commit
`334d3eebddaef382ddedc4ba99457518a375d83d`.  All four strict terminals,
the independent `proposal-aa2` checker, and the 21/21 receipt passed.  The
physical residual $o-q_8$ is

$$
(R_\rho,R_L,D_L,R_a)=
(0,\,4.573608580149287\times10^{-4},\,
6.701156962662935\times10^{-7}\ \mathrm{cm}^{-1},\,
3.915463384152092\times10^{-7}).
$$

$R_\rho$ and $R_a$ pass the original AND gate; $R_L$ does not.  The map is
therefore `VALID_NOT_MET`.  AA(1) on $n-q_7$ and $o-q_8$ has direction
ratios `0.99405602856832498`, `0.78327883203609316`, and
`0.82926667695332601`, all strictly below one.  Thus
`AA1_DIRECTION_PASS_AA2_SKIPPED`; AA(2) is not calculated.  No durable
proposal is published and no second physical map is run.  The artifact's
`continuation_policy.md` remains the receipt-protected pre-run policy copy.
See [rank2_current_klmn_aa2_map_result.md](rank2_current_klmn_aa2_map_result.md).
