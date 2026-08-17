# One direct Picard map from the current AA(2) return

Date: 2026-08-16

Status: `PREPARED_NOT_RUN`.

Let the latest valid returned state be

\[
p=G_2(q_{\mathrm{AA2}}).
\]

This default-off stage permits exactly one direct continuation

\[
z=G_2(p).
\]

The preceding AA(2) map reduced leakage but increased the modal defect.
Because its offline modal prediction did not survive the physical map, this
step adds no new extrapolation. Direct substitution is the parameter-free
control for the latest returned state, not a claim that Picard is contractive.

The complete returned AX and snapshot archives of \(p\) are the sole parent.
The unchanged fixed-rank-two host performs three online radial fixed-source
solves and one axial solve. The basis, normalization, physical equations,
strict inner terminals and original stopping gate remain unchanged:

\[
R_\rho\leq5\times10^{-7},\qquad
R_L\leq5\times10^{-7},\qquad
R_a\leq5\times10^{-7}.
\]

The 120-second radial and 180-second axial limits are process-safety bounds;
they are not model or convergence parameters. One activation permits one
attempt. There is no retry, mixing, relaxation, damping, clipping, fitted
closure, regularization, fallback or automatic successor.

The unchanged host assigns exactly one classification after all strict
terminals, the independent continued-state audit and the receipt checks pass:

- `INVALID_MAP`: a physical, provenance, terminal, audit or receipt check fails.
- `TOLERANCE_MET`: the valid return passes all three stopping defects.
- `VALID_NOT_MET`: the map is valid but at least one stopping defect fails.

Preparing this stage performs no Dragon or transport calculation and creates
no result artifact.
