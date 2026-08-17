# One physical map from the current-window AA(1) proposal

Date: 2026-08-17

Status: `PREPARED_NOT_RUN`.

The latest actual residuals $t-p$ and $u-t$ give the standard
unregularized full-Gram AA(1) proposal

\[
q=0.41546155012473063\,t+0.58453844987526937\,u.
\]

Its modal, leakage height-$L_2$, and leakage $D_L$ direction ratios are
`0.092304347566644032`, `0.66391212983258452`, and
`0.56107589029972316`.  All three pass the fixed direction screen, so the
minimum-order rule skips AA(2).  This default-off stage permits exactly one
fresh physical map

\[
q^+=G_2(q).
\]

The verified proposal uses the latest returned (u) raw AX and snapshot
payloads as carriers.  The unchanged fixed-rank-two host performs three
online radial fixed-source solves and one axial solve.  The fixed POD basis,
normalization, physical equations, strict inner terminals, and original
stopping gate remain unchanged:

\[
R_\rho\leq5\times10^{-7},\qquad
R_L\leq5\times10^{-7},\qquad
R_a\leq5\times10^{-7}.
\]

Dimensional (D_L\,[\mathrm{cm}^{-1}]) is not part of this dimensionless
outer gate.  The 120-second radial and 180-second axial limits are process
safety bounds, not model or convergence parameters.  One activation permits
one attempt.  There is no retry, fallback, automatic successor, older-window
search, AA(2), AA(3), relaxation, damping, clipping, fitted closure,
regularization, pseudoinverse threshold, condition cutoff, or empirical
parameter.

After all strict terminals, the independent proposal-parent checker, and the
receipt checks pass, the unchanged host assigns exactly one classification:

- `INVALID_MAP`: a physical, provenance, terminal, audit, or receipt check fails;
- `TOLERANCE_MET`: all three stopping defects pass;
- `VALID_NOT_MET`: the map is valid but at least one stopping defect fails.

Preparing and default-off checking this stage runs no Dragon or transport
calculation and creates no map-result artifact.
