# One direct Picard map from the latest returned state $e$

Date: 2026-08-17

Status: `PREPARED_NOT_RUN`.

The latest standard AA(1) and AA(2) directions both fail the predeclared
leakage screens.  Neither direction is materialized.  This default-off
stage therefore permits exactly one direct continuation

$$
f=G_2(e).
$$

The complete returned AX and snapshot archives of $e$ are the sole parent;
there is no affine mixing.  The unchanged fixed-rank-two host performs three
online radial fixed-source solves and one axial solve.  Acceptance uses only
the original AND gate

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

The unchanged host returns `TOLERANCE_MET`, `VALID_NOT_MET`, or
`INVALID_MAP` only after all strict terminals, the independent `continued`
checker, and receipt checks.  The physical residual is $f-e$; $f-d$ and
$f-c_{\mathrm{next}}$ are not fixed-point residuals.
This batch permits no second physical map.
