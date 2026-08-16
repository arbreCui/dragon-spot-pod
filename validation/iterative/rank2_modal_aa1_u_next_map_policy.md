# One direct Picard map after the latest evaluated proposal

Evaluate exactly one unchanged fixed-rank map

\[
x_{n+1}=G_2(x_n),
\]

where `x_n` is the valid returned state from the completed
`u_pub -> G_2(u_pub)` experiment. Use direct substitution, the fixed rank-two
POD basis, three online radial fixed-source solves and one axial solve.

No retry, relaxation, damping, clipping, fitted closure, empirical coefficient
or automatic successor is allowed. The 120-second radial and 420-second axial
limits are operational process bounds only.

For \(\varepsilon=5\times10^{-7}\), report exactly one classification:

- `INVALID_MAP` if a strict solve, provenance or independent audit fails;
- `TOLERANCE_MET` if the map is valid and
  \(R_\rho\leq\varepsilon\), \(R_L\leq\varepsilon\) and
  \(R_a\leq\varepsilon\);
- `VALID_NOT_MET` otherwise.

The dimensional \(D_L\) and balance values are diagnostics, not stopping
conditions. One adjacent map may establish only a local observed change; it
cannot by itself prove convergence, stability, rank adequacy or physical
accuracy.

The separately authorized single run subsequently completed as
`VALID_NOT_MET`; see
[rank2_modal_aa1_u_next_map_result.md](rank2_modal_aa1_u_next_map_result.md).
