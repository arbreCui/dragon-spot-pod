# One physical map from the latest-return AA(1) proposal

Date: 2026-08-17

Status: `PREPARED_NOT_RUN`.

The latest two genuine residuals $r-z$ and $s-r$ define the standard
unregularized full-Gram AA(1) state

\[
p=0.80686776173198704\,r+0.19313223826801298\,s.
\]

Its modal, leakage height-$L_2$, and leakage $D_L$ direction ratios are
`0.0551069`, `0.799194`, and `0.787927`.  AA(1) therefore passes the fixed
three-direction authorization screen; by the predeclared minimum-order
rule, AA(2) is not formed.  This default-off stage permits exactly one fresh
physical map

\[
p^+=G_2(p).
\]

The complete latest-return raw AX and snapshot payloads remain carriers;
only the verified published $(a,\rho,L)$ proposal enters the map.  The
unchanged fixed-rank-two host performs three online radial fixed-source
solves and one axial solve.  The POD basis, normalization, physical
equations, strict solve terminals, and original stopping gate remain
unchanged:

\[
R_\rho\leq5\times10^{-7},\qquad
R_L\leq5\times10^{-7},\qquad
R_a\leq5\times10^{-7}.
\]

Dimensional $D_L\,[\mathrm{cm}^{-1}]$ is not part of this outer gate.  The
120-second radial and 180-second axial limits are process-safety bounds, not
model or convergence parameters.  One activation permits one attempt.
There is no retry, fallback, automatic successor, relaxation, damping,
clipping, fitted closure, regularization, pseudoinverse threshold,
condition cutoff, older-window search, or empirical parameter.

After all strict terminals, the independent proposal-parent checker, and
the receipt checks pass, the unchanged host assigns exactly one
classification:

- `INVALID_MAP`: a physical, provenance, terminal, audit, or receipt check fails;
- `TOLERANCE_MET`: all three stopping defects pass;
- `VALID_NOT_MET`: the map is valid but at least one stopping defect fails.

Preparing and default-off checking this stage runs no Dragon or transport
calculation and creates no map-result artifact.

## Post-run record

The frozen host was activated exactly once from source commit
`6e7b6ecc3102bf76423807bb8908107b69e06bca`.  All four strict solve
terminals, the independent `proposal-x4` checker, and the 21/21 receipt
passed.  The returned raw defects are

\[
(R_\rho,R_L,D_L,R_a)=
(6.4223492\times10^{-8},\,4.8961883\times10^{-4},\,
7.1738032\times10^{-7}\ \mathrm{cm}^{-1},\,
2.6606584\times10^{-6}).
\]

Only $R_\rho$ passes the unchanged gate, so the result is
`VALID_NOT_MET`.  A cross-input comparison with the preceding direct map
shows smaller leakage and modal defects, but is not a contraction claim.
No retry, fallback, AA(2), or successor was started.  See
[rank2_current_zrs_aa1_map_result.md](rank2_current_zrs_aa1_map_result.md).
