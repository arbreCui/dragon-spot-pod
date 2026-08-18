# One map from the latest admissible AA(2) proposal

Date: 2026-08-17

Status: `EXECUTED_ONCE_VALID_NOT_MET`.

The standard full-Gram AA(1) from $f-e$ and $g-q_1$ failed because its
leakage direction ratios are `1.0164960989601337` and
`1.0021076380581850`.  Only then, the latest three genuine residuals gave

$$
q_2=0.37059923635358261\,e+
0.28970803656130206\,f+
0.33969272708511533\,g.
$$

Its modal, leakage height-$L_2$, and same-weight maximum-$|D_L|$ direction
ratios are `0.33342566026806181`, `0.47696732762436056`, and
`0.39981312880450964`, all strictly below one.  These parameter-free
screens authorize one direction; they do not predict convergence.

One activation permits exactly one physical map

$$
h=G_2(q_2).
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
`VALID_NOT_MET`.  If valid, the physical residual is $h-q_2$; $h-g$ is not
a fixed-point residual.  This batch permits no second physical map.

## Post-run record

The stage was activated exactly once from source commit
`1be7a4070d1083592e7e8f966e383ea44196c14a`.  All four strict terminals,
the independent `proposal-aa2` checker, and the 21/21 receipt passed.  The
physical residual $h-q_2$ is

$$
(R_\rho,R_L,D_L,R_a)=
(1.284469506313002\times10^{-7},\,
4.808395175515263\times10^{-4},\,
7.045164238661528\times10^{-7}\ \mathrm{cm}^{-1},\,
1.190590942018258\times10^{-6}).
$$

$R_\rho$ passes the original AND gate; $R_L$ and $R_a$ do not.  The map is
therefore `VALID_NOT_MET`, with no retry or automatic successor.  The next
standard AA(1), formed only from $g-q_1$ and $h-q_2$, has direction ratios
`0.11971305975561962`, `0.47525043616253554`, and
`0.70441518119387303`, all strictly below one.  Thus
`AA1_DIRECTION_PASS`; AA(2) is not calculated.  No durable proposal is
published and no second physical map is run.  The artifact's
`continuation_policy.md` remains the receipt-protected pre-run policy copy.
See [rank2_current_cefg_aa2_map_result.md](rank2_current_cefg_aa2_map_result.md).
