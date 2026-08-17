# One direct Picard map from the latest returned state $z$

Date: 2026-08-17

Status: `EXECUTED_ONCE_VALID_NOT_MET`.

The latest standard AA(1) and AA(2) directions both fail the predeclared
leakage screens and are not materialized.  This default-off stage therefore
permits exactly one direct continuation

$$
z^+=G_2(z).
$$

The complete returned AX and snapshot archives of $z$ are the sole parent;
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
checker, and the receipt checks.  Default-off preparation runs no Dragon.

## Frozen result

The stage was activated once from source commit
`3a30ffd94100df023bfb446487a44311a05a181f` and returned

$$
(R_\rho,R_L,D_L,R_a)=
(0,\,5.324646091595354\times10^{-4},\,
7.801572792232037\times10^{-7}\ \mathrm{cm}^{-1},\,
1.309957085222539\times10^{-6}).
$$

Only $R_\rho$ passes the original AND gate, so the classification is
`VALID_NOT_MET`.  The independent checker and 21/21 receipt pass.  There
was no retry or automatic successor.

The next offline standard AA(1), formed only from the genuine residuals
$z-y$ and $z^+-z$, has modal, leakage height-$L_2$, and same-weight
maximum-$|D_L|$ direction ratios
`0.093357573037484751`, `0.42214650302136536`, and
`0.61065652318148245`.  All three are strictly below one, hence
`AA1_DIRECTION_PASS_AA2_SKIPPED`.  This policy records only that direction
decision: the proposal is not materialized and no second map is run.
