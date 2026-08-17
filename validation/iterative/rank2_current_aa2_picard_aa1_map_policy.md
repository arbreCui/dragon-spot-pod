# One strict map from the latest two-map AA(1) proposal

Date: 2026-08-16

Status: `PREPARED_NOT_RUN`.

This default-off stage permits exactly one evaluation

\[
G_2(s),\qquad
s=0.62153295893235927\,p+0.37846704106764067\,z,
\]

using the genuine consecutive maps
\(q_{\mathrm{AA2}}\mapsto p\) and \(p\mapsto z\). The weights are the
unique standard full-Gram AA(1) solution. They were not fitted, clipped,
damped or relaxed.

Before materialization, the same weights reduced the modal residual,
height-weighted leakage \(L_2\), and \(D_L\) relative to the latest map to
`0.0339984`, `0.534864`, and `0.720624`. All 8880 published reconstructed
points are strictly positive. These are offline authorization checks, not
convergence evidence.

The proposal carries the complete latest returned \(z\) raw AX and snapshot
payload as `Z-RAW-FLUX`; raw fluxes are not mixed. The unchanged host performs
three online radial fixed-source solves followed by one reduced axial solve.
Rank two, basis, equations, normalization, decks, strict inner predicates and
the original outer AND gate

\[
R_\rho,R_L,R_a\le 5\times10^{-7}
\]

remain unchanged. The 120-second radial and 180-second axial bounds are only
process-safety limits. One activation permits one attempt, with no retry,
fallback, empirical parameter or automatic successor.

The result is classified only as `INVALID_MAP`, `TOLERANCE_MET`, or
`VALID_NOT_MET` by the existing independent checker and the unchanged AND
gate. Offline predictions and \(D_L\) remain diagnostics.

## Post-run record

The default-off host was activated exactly once from source commit
`18170cca5fcd7ac30e3768e852ad25bd2ed2ebae`. All four strict solve terminals,
the independent checker and the 21/21 receipt passed. The result is
`VALID_NOT_MET`: \(R_\rho\) passes while \(R_L\) and \(R_a\) fail. No retry,
fallback or successor was started. See
[rank2_current_aa2_picard_aa1_map_result.md](rank2_current_aa2_picard_aa1_map_result.md).
