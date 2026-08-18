# One direct Picard map from the latest returned state $k$

Date: 2026-08-17

Status: `PREPARED_NOT_RUN`.

Standard unregularized AA(1) and AA(2), evaluated in that order from genuine
fixed-point residuals, both fail the predeclared leakage direction screens.
Neither direction is materialized.  This default-off stage therefore permits
exactly one direct continuation

$$
l=G_2(k).
$$

The complete returned AX and snapshot archives of $k$ are the sole parent;
there is no affine mixing.  The unchanged fixed-rank-two host performs three online radial fixed-source solves and one axial solve.  Acceptance uses only
the original AND gate

$$
R_\rho\le5\times10^{-7},\qquad
R_L\le5\times10^{-7},\qquad
R_a\le5\times10^{-7}.
$$

Dimensional $D_L\,[\mathrm{cm}^{-1}]$ remains diagnostic only.  If the map is
valid, its physical fixed-point residual is $l-k$; a difference from any
older state or rejected proposal is not that residual.  The 120 s radial and
180 s axial limits are process-safety bounds, not model coefficients.

One activation permits one attempt.  There is no retry, fallback, automatic
successor, relaxation, damping, clipping, fit, regularization, pseudoinverse,
condition cutoff, empirical parameter, mixed-unit objective, older-window
search, or AA(3).  This batch permits no second physical map.  The unchanged
host may return `TOLERANCE_MET`, `VALID_NOT_MET`, or `INVALID_MAP` only after
all strict terminals, the independent `continued` checker, and receipt checks.
