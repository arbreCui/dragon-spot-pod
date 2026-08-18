# One map from the latest admissible AA(1) proposal

Date: 2026-08-17

Status: `PREPARED_NOT_RUN`.

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
