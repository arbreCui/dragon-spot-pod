# One direct Picard map from the latest returned state

Date: 2026-08-17

Status: `PREPARED_NOT_RUN`.

Let

\[
z=G_2(q)
\]

be the latest valid returned state.  Standard AA(1) on
\(x\mapsto y,q\mapsto z\) and standard unregularized AA(2) on
\(v\mapsto w,x\mapsto y,q\mapsto z\) both reduce the modal direction but
increase the leakage height-\(L_2\) and \(D_L\) directions.  They fail the
unchanged parameter-free direction gate and are not materialized.  This
default-off stage therefore permits exactly one direct continuation

\[
z^+=G_2(z).
\]

The complete returned AX and snapshot archives of \(z\) are the sole parent;
there is no affine proposal or state mixing.  The unchanged fixed-rank-two
host performs three online radial fixed-source solves and one axial solve.
The fixed POD basis, normalization, physical equations, strict solve
terminals, and original stopping gate remain unchanged:

\[
R_\rho\leq5\times10^{-7},\qquad
R_L\leq5\times10^{-7},\qquad
R_a\leq5\times10^{-7}.
\]

Dimensional \(D_L\,[\mathrm{cm}^{-1}]\) is a diagnostic and is not compared
with this dimensionless gate.  The 120-second radial and 180-second axial
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
