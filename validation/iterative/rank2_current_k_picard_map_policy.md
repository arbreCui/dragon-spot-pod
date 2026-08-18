# One direct Picard map from the latest returned state $k$

Date: 2026-08-17

Status: `EXECUTED_ONCE_VALID_NOT_MET`.

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

## Post-run record

The stage was activated exactly once from source commit
`de35bc474fa5788acda9ce037d7a31721e07d34d`.  All four strict terminals,
the independent `continued` checker, and the 21/21 receipt passed.  The
physical residual $l-k$ is

$$
(R_\rho,R_L,D_L,R_a)=
(6.422348086676521\times10^{-8},\,
3.744499849949860\times10^{-4},\,
5.486363079398870\times10^{-7}\ \mathrm{cm}^{-1},\,
1.628119765098577\times10^{-6}).
$$

$R_\rho$ passes the original AND gate; $R_L$ and $R_a$ do not, so the map
is `VALID_NOT_MET`.  Standard AA(1) on $k-q_5,l-k$ has direction ratios
`0.81736979605403082`, `0.80173988821917219`, and
`0.90621455552995278`, all strictly below one.  Therefore the offline
classification is `AA1_DIRECTION_PASS_AA2_SKIPPED`; AA(2) was not
calculated, no direction was published, and no second map was run.  The
artifact's `continuation_policy.md` remains the receipt-protected pre-run
policy copy.  See
[rank2_current_k_picard_map_result.md](rank2_current_k_picard_map_result.md).
