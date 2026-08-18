# One map from the latest admissible AA(2) proposal

Date: 2026-08-17

Status: `PREPARED_NOT_RUN`.

AA(1) on $h-q_2$ and $i-q_3$ was tried first and failed because its
leakage height-$L_2$ direction ratio is `1.0001541854604454`.  Only then,
the latest three genuine residuals gave the standard unregularized
full-Gram proposal

$$
q_4=0.54656692430484066\,g+
0.22903224207636369\,h+
0.22440083361879565\,i.
$$

Its exact $2\times2$ determinant is `7.9724244756408422e-26`.  Its modal,
leakage height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are
`0.085602787687317231`, `0.50064418931908561`, and
`0.44048518991529284`, all strictly below one.  No regularization or
condition cutoff is applied.  These parameter-free screens authorize one
direction; they do not predict convergence.

One activation permits exactly one physical map

$$
j=G_2(q_4).
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
`VALID_NOT_MET`.  If valid, the physical residual is $j-q_4$; $j-i$ is not
a fixed-point residual.  This batch permits no second physical map.
