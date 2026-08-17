# One map from the latest admissible AA(2) proposal

Date: 2026-08-17

Status: `EXECUTED_ONCE_VALID_NOT_MET`.

The latest two actual residuals, $u-t$ and $v-q$, first gave standard
full-Gram AA(1).  Its modal direction ratio was `0.6667217753`, but its
leakage height-$L_2$ and $D_L$ ratios were `1.1537581212` and
`1.2578586583`; it was rejected and not materialized.

Only then, the latest three actual maps $p\mapsto t$, $t\mapsto u$, and
$q\mapsto v$ gave standard unregularized AA(2):

$$
w=0.1976858571\,t+0.2162723008\,u+0.5860418421\,v.
$$

Its modal, leakage height-$L_2$, and $D_L$ direction ratios are
`0.3560912801`, `0.5842931263`, and `0.7122142636`.  All 8880 reconstructed
points are positive.  These are authorization diagnostics, not stopping
defects or a convergence prediction.

One activation permits exactly one $G_2(w)$ evaluation.  The fixed rank-two
basis, physical equations, normalization, and online radial recomputation
remain unchanged.  Acceptance uses only the original AND gate

$$
R_\rho\le5\times10^{-7},\qquad
R_L\le5\times10^{-7},\qquad
R_a\le5\times10^{-7}.
$$

Dimensional $D_L\,[\mathrm{cm}^{-1}]$ remains diagnostic only.  The 120 s
radial and 180 s axial bounds are process-safety limits.  There is no retry,
fallback, relaxation, damping, clipping, fit, regularization, condition
cutoff, or automatic successor.

## Post-run record

The frozen host was activated exactly once from source commit
`9c1fe4b6109c2cd2c2fcfae8904d6aa9c1af190e`.  All four strict solver
terminals, the independent `proposal-aa2` checker, and the 21/21 receipt
passed.  The result is `VALID_NOT_MET`: $R_\rho$ passes, while $R_L$ and
$R_a$ fail.  Relative to the preceding evaluated map, $R_L$, $D_L$, and
$R_a$ increased by 18.57%, 18.57%, and 475.29%; this cross-input comparison
is not a contraction or divergence claim.  No retry or successor was
started.  See
[rank2_current_ptuqv_aa2_map_result.md](rank2_current_ptuqv_aa2_map_result.md).
