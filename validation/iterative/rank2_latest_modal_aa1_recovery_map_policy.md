# One strict physical map from the published Q(s)

Date: 2026-08-16

Status: `PREPARED_NOT_RUN`.

This default-off stage permits exactly one evaluation

\[
v=G_2(Q(s)),\qquad
s=0.815637869982362540z+0.184362130017637404u.
\]

The coefficient is the already audited standard full-Gram modal AA(1)
coefficient. This stage does not recompute, fit, clip or tune it. The
hash-locked parent is the independently materialized publication $Q(s)$.
Its canonical `(A,rho,L)` fields are the map input. `U-RAW-FLUX` records only
that the complete raw AX/snapshot carrier came from the latest returned state
$u$; it does not claim that raw flux is a solved flux for $s$.

The existing host performs three online radial fixed-source solves followed
by one axial solve. Rank two, the POD basis, normalization, decks, physical
equations, strict inner termination and the original stopping tolerance
$5\times10^{-7}$ are unchanged. The decision remains the separate AND gate
on $R_\rho$, $R_L$ and $R_a$; $D_L$ and balances remain diagnostics.

The radial and axial process bounds are 120 and 420 seconds. They are external
safety bounds and do not enter the equations, AA(1), or convergence decision.
Before Dragon, the wrapper must verify the proposal receipt, all six parent
hashes and `PROPOSAL + U-RAW-FLUX` preflight.

There is no retry, fallback, damping, relaxation, clipping, fitted closure,
empirical coefficient or automatic successor. Only `INVALID_MAP`,
`TOLERANCE_MET` and `VALID_NOT_MET` are allowed. A valid map establishes only
this one stopping decision; it does not establish stability, contraction,
AA(1) superiority, rank adequacy or physical accuracy.
