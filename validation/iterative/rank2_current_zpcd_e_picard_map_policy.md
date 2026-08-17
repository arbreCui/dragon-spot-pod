# One direct Picard map from the latest returned state $e$

Date: 2026-08-17

Status: `EXECUTED_ONCE_VALID_NOT_MET`.

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

## Frozen result

The stage was activated exactly once from source commit
`ce6be5b9c18201bd24af1c9318c830a6e0b8f6b3`.  All four strict terminals,
the independent `continued` checker, and the 21/21 receipt passed.  The
physical residual $f-e$ is

$$
(R_\rho,R_L,D_L,R_a)=
(1.284469730578053\times10^{-7},\,
8.318307793557387\times10^{-4},\,
1.218781108036637\times10^{-6}\ \mathrm{cm}^{-1},\,
1.505196532244700\times10^{-6}).
$$

Only $R_\rho$ passes the original AND gate, hence `VALID_NOT_MET`.  There
was no retry or automatic successor.

The next standard AA(1), formed only from $e-c_{\mathrm{next}}$ and $f-e$,
has modal, leakage height-$L_2$, and same-weight maximum-$|D_L|$ direction
ratios `0.059424727376440133`, `0.19596354669013863`, and
`0.28717479223258224`.  Thus `AA1_DIRECTION_PASS_AA2_SKIPPED`.  No durable
proposal is published and no second physical map is run.
