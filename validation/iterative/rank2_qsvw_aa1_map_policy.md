# One strict map from the current standard AA(1) state

Date: 2026-08-16

Status: `PREPARED_NOT_RUN`.

From the two consecutive evaluated pairs

\[
Q(s)\mapsto v,\qquad v\mapsto w,
\]

define \(p=v-Q(s)\) and \(q=w-v\). The unchanged full-Gram-height modal
AA(1) rule gives the unique scalar

\[
\beta=\frac{\lVert p\rVert^2-\langle p,q\rangle}
{\lVert q-p\rVert^2},\qquad
y=(1-\beta)v+\beta w.
\]

The coefficient is recomputed from the states and is not adjustable. The
same affine weights are applied to \(A\), \(\rho\), and \(L\). There is no
leakage fit, clipping, damping, relaxation or regularization. The two
same-coefficient leakage ratios are risk diagnostics only; they do not
accept the proposal and do not enter \(\beta\).

`X4-RAW-FLUX` is reused only as the existing latest-returned carrier-schema
route. The actual carrier is the complete hash-locked returned state \(w\).
The proposal is accepted for a map only by finite arithmetic, positive
\(\rho\), all 8880 positive reconstructed points, fixed-basis identity and
carrier/receipt checks.

This default-off stage permits exactly one evaluation \(G_2(y)\). The
unchanged host performs three online radial fixed-source transport solves
and then one axial solve. The sole convergence decision remains

\[
R_\rho\leq5\times10^{-7},\qquad
R_L\leq5\times10^{-7},\qquad
R_a\leq5\times10^{-7}
\]

as an AND gate. The 120/420 second bounds are external process limits.
There is no retry, fallback, empirical coefficient or automatic successor.

## Post-run record

The frozen host was activated exactly once from source commit `f421801`.
All strict solve terminals, the independent proposal/carrier/map audit and
the 21-entry receipt passed. The result is `VALID_NOT_MET`; no retry or
successor was started. See
[rank2_qsvw_aa1_map_result.md](rank2_qsvw_aa1_map_result.md).
