# One map from the minimum-order $qvwx$ AA(1) proposal

Date: 2026-08-17

Status: `EXECUTED_ONCE_VALID_NOT_MET`.

The genuine residuals $v-q$ and $x-w$ give standard full-Gram AA(1):

$$
y=0.8805731304\,v+0.1194268696\,x.
$$

Its modal, leakage height-$L_2$, and same-weight $D_L$ direction ratios are
`0.1097399419`, `0.7136503226`, and `0.8419194273`; all strictly pass.  By
the minimum-order rule, AA(2) is skipped.

One activation permits exactly one $G_2(y)$ evaluation.  The fixed rank-two
basis, physical equations, normalization, and online radial recomputation
remain unchanged.  Acceptance uses only the original AND gate

$$
R_\rho\le5\times10^{-7},\qquad
R_L\le5\times10^{-7},\qquad
R_a\le5\times10^{-7}.
$$

Dimensional $D_L\,[\mathrm{cm}^{-1}]$ is diagnostic only.  The 120 s radial
and 180 s axial limits are process-safety bounds.  There is no retry,
fallback, relaxation, damping, clipping, fit, regularization, cutoff, or
automatic successor.

## Post-run record

The frozen host was activated exactly once from source commit
`523d5adcbf2deb5c951c5c56634ff86fc7fcac83`.  All four strict solver
terminals, the independent `proposal-aa1` checker, and the 21/21 receipt
passed.  The result is `VALID_NOT_MET`: $R_\rho$ passes, while $R_L$ and
$R_a$ fail.  No retry or successor was started.  See
[rank2_current_qvwx_aa1_map_result.md](rank2_current_qvwx_aa1_map_result.md).
