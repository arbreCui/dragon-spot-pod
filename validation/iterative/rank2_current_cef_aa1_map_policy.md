# One map from the latest minimum-order AA(1) proposal

Date: 2026-08-17

Status: `PREPARED_NOT_RUN`.

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
