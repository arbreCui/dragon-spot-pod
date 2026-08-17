# One direct Picard map from the latest returned state

Date: 2026-08-17

Status: `PREPARED_NOT_RUN`.

Let $r=G_2(z)$ be the latest valid returned state.  Standard AA(1) on
$q\mapsto z,z\mapsto r$ and standard unregularized AA(2) on
$x\mapsto y,q\mapsto z,z\mapsto r$ both reduce the modal direction but
increase the leakage height-$L_2$ and $D_L$ directions.  They fail the
predeclared parameter-free direction screen and are not authorized or
published as production map parents.  This default-off stage therefore
permits exactly one direct continuation

\[
r^+=G_2(r).
\]

The complete returned AX and snapshot archives of $r$ are the sole parent;
there is no affine proposal or state mixing.  The unchanged fixed-rank-two
host performs three online radial fixed-source solves and one axial solve.
The fixed POD basis, normalization, physical equations, strict solve
terminals, and original stopping gate remain unchanged:

\[
R_\rho\leq5\times10^{-7},\qquad
R_L\leq5\times10^{-7},\qquad
R_a\leq5\times10^{-7}.
\]

Dimensional $D_L\,[\mathrm{cm}^{-1}]$ is not compared with this
dimensionless convergence gate.  The 120-second radial and 180-second axial
limits are process-safety bounds, not model or convergence parameters.  One
activation permits one attempt.  There is no retry, fallback, automatic
successor, relaxation, damping, clipping, fitted closure, regularization,
pseudoinverse threshold, condition cutoff, or empirical parameter.

After all strict terminals, the independent continued-state checker, and the
receipt checks pass, the unchanged host assigns exactly one classification:

- `INVALID_MAP`: a physical, provenance, terminal, audit, or receipt check fails;
- `TOLERANCE_MET`: all three stopping defects pass;
- `VALID_NOT_MET`: the map is valid but at least one stopping defect fails.

Preparing and default-off checking this stage runs no Dragon or transport
calculation and creates no result artifact.

## Post-run record

The frozen host was activated exactly once from source commit
`f3b3bdd10ac2e7d843621fff083c3d54808b1795`.  All strict solve terminals,
the independent `continued` checker, and the 21/21 receipt passed.  The valid
result is `VALID_NOT_MET`: $R_\rho$ passes, while $R_L$ and $R_a$ fail the
unchanged gate.  Against the preceding genuinely consecutive residual,
leakage decreased by 7.67% while the modal defect increased by 307.72%; these
observed adjacent ratios do not establish asymptotic contraction or a
periodic orbit.  No retry, fallback, or successor was started.  See
[rank2_current_zplus_picard_map_result.md](rank2_current_zplus_picard_map_result.md).
