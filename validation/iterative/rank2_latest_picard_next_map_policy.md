# One further direct Picard map from the latest returned state

Date: 2026-08-16

Status: `PREPARED_NOT_RUN`.

Let the latest valid returned state be

\[
x_3=G_2(x_2).
\]

This default-off stage is limited to exactly one direct Picard evaluation

\[
x_4=G_2(x_3).
\]

The complete returned AX and snapshot archives of \(x_3\) are the sole map
parent. The unchanged host reconstructs the radial fields in the same fixed
rank-two POD space, uses the parent eigenvalue in the frozen-fission source,
performs three online radial fixed-source solves and then one axial solve.
There is no proposal, state selection, combined norm or raw-carrier mixing.

The physical decks, normalization, fixed basis, rank two, strict inner
terminals and separate outer gate remain unchanged at

\[
R_\rho\leq5\times10^{-7},\qquad
R_L\leq5\times10^{-7},\qquad
R_a\leq5\times10^{-7}.
\]

The 120-second radial and 420-second axial bounds are operational process
limits, not model or convergence parameters. Before either Dragon invocation,
the wrapper must pass the preceding 21-entry receipt and the six parent
hashes. The continued-state independent checker must pass before publication
to a new dedicated result directory.

One activation permits one attempt. There is no retry, relaxation, damping,
Anderson mixing, clipping, fitted closure, regularization, pseudoinverse,
fallback or empirical coefficient. Only these classifications are allowed:

- `INVALID_MAP`: a strict terminal, physical value, provenance, fixed-basis,
  independent-audit or receipt check fails; no candidate is published.
- `TOLERANCE_MET`: the map is valid and all three raw stopping defects pass.
- `VALID_NOT_MET`: the map is valid but at least one raw stopping defect
  fails.

The dimensional leakage change, balances and direction ratios remain
diagnostics. One map cannot establish contraction, convergence order, rank
adequacy or physical accuracy. It starts no retry or further successor.
Preparing this host performs no Dragon, transport, assembly or Picard
calculation and produces no map result.

## Post-run record

The frozen host was subsequently activated exactly once from source commit
`95dd9204d1010b1583d8d4e4de530b094a80ee98`. All strict solve terminals,
the independent continued-state audit and the 21-entry receipt passed. The
runtime classification is `VALID_NOT_MET`; \(R_L\) and \(R_a\) exceed the
unchanged tolerance. No retry or further map was started. See
[rank2_latest_picard_next_map_result.md](rank2_latest_picard_next_map_result.md).
