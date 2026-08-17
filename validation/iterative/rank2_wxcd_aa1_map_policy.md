# One strict map from the w-x / c-d standard AA(1) state

Date: 2026-08-16

Status: `PREPARED_NOT_RUN`.

The two real residuals $p=x-w$ and $q=d-c$ uniquely give

\[
y=1.6615840721007848x-0.66158407210078485d.
\]

This is the unchanged full-Gram-height AA(1) least-squares solution. It is an
unclipped extrapolation, not a tuned relaxation. The same weights act on
$A$, $\rho$ and $L$. The adverse same-weight leakage screens are recorded as
risk diagnostics and do not enter the coefficient or acceptance gate.

This default-off stage permits exactly one $G_2(y)$. The fixed rank-two POD
basis, physical decks, normalization, online radial transport, axial solve,
strict terminals and original AND gate at $5\times10^{-7}$ remain unchanged.
The 120/420 second bounds are external process limits. There is no retry,
fallback, coefficient adjustment or automatic successor.

## Post-run record

The frozen host was activated exactly once from source commit `9ee1427`.
All strict solve terminals, the independent proposal/carrier/map audit and
the 21-entry receipt passed. The result is `VALID_NOT_MET`; no retry or
successor was started. See
[rank2_wxcd_aa1_map_result.md](rank2_wxcd_aa1_map_result.md).
