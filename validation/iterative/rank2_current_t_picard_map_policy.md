# One direct Picard map from the latest returned state

Date: 2026-08-17

Status: `PREPARED_NOT_RUN`.

The latest two evaluated residuals $s-r$ and $t-p$ give a standard AA(1)
whose modal direction improves but whose leakage height-$L_2$ and $D_L$
directions increase.  Only after that failure, standard unregularized AA(2)
was checked on $r-z$, $s-r$, and $t-p$; its two leakage directions also
increase.  Neither Anderson state is authorized or materialized.  This
default-off stage therefore permits exactly one direct continuation

\[
t^+=G_2(t).
\]

The complete returned AX and snapshot archives of $t$ are the sole parent;
there is no affine state mixing.  The unchanged fixed-rank-two host performs
three online radial fixed-source solves and one axial solve.  The fixed POD
basis, normalization, physical equations, strict solve terminals, and
original stopping gate remain unchanged:

\[
R_\rho\leq5\times10^{-7},\qquad
R_L\leq5\times10^{-7},\qquad
R_a\leq5\times10^{-7}.
\]

Dimensional $D_L\,[\mathrm{cm}^{-1}]$ is not part of this dimensionless
outer gate.  The 120-second radial and 180-second axial limits are process
safety bounds, not model or convergence parameters.  One activation permits
one attempt.  There is no retry, fallback, automatic successor, older-window
search, AA(3), relaxation, damping, clipping, fitted closure, regularization,
pseudoinverse threshold, condition cutoff, or empirical parameter.

After all strict terminals, the independent continued-state checker, and the
receipt checks pass, the unchanged host assigns exactly one classification:

- `INVALID_MAP`: a physical, provenance, terminal, audit, or receipt check fails;
- `TOLERANCE_MET`: all three stopping defects pass;
- `VALID_NOT_MET`: the map is valid but at least one stopping defect fails.

Preparing and default-off checking this stage runs no Dragon or transport
calculation and creates no result artifact.
