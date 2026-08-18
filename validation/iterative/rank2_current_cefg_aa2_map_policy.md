# One map from the latest admissible AA(2) proposal

Date: 2026-08-17

Status: `PREPARED_NOT_RUN`.

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
