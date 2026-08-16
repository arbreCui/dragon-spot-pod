# One strict map from the standard rank-2 modal Anderson(2) proposal

Date: 2026-08-16

Status: `PREPARED_NOT_RUN`.

This default-off stage is limited to exactly one evaluation

\[
G_2(x_{\mathrm{AA2}}),
\]

where

\[
x_{\mathrm{AA2}}=
0.77664274528264354x_{\mathrm{next}}^+
-0.54521415283366947x_{\mathrm{roll}}^+
+0.76857140755102593x_{\mathrm{roll2}}^+.
\]

The negative coefficient is the unmodified result of the standard
unconstrained AA(2) problem. It is not an empirical coefficient and is not
altered or forced into a convex combination. The hash-locked parent has
already passed finite publication and 8880/8880 strict reconstructed-flux
positivity.

`AA2-RAW-FLUX` identifies the complete latest-returned
\(x_{\mathrm{roll2}}^+\) AX and snapshot carrier. It does not replace the
canonical proposal or enter a physical equation. The unchanged host
reconstructs each radial field from the proposal's fixed-rank coordinates,
uses the proposal eigenvalue in the frozen-fission source, performs three
online radial fixed-source solves and then one axial solve.

The fixed POD package, rank two, normalization, physical decks, strict inner
terminals and outer tolerance

\[
\varepsilon=5\times10^{-7}
\]

remain unchanged. The 120-second radial and 420-second axial limits are
operational process bounds, not physical or convergence parameters.

The wrapper is default-off. The proposal receipt, six parent hashes and exact
`PROPOSAL + AA2-RAW-FLUX` Ganlib preflight must pass before either Dragon
invocation. One activation permits one attempt and no retry, relaxation,
damping, clipping, fitted closure, regularization, pseudoinverse, fallback or
empirical coefficient.

Only three classifications are allowed:

- `INVALID_MAP`: a strict solve terminal, physical value, provenance check,
  fixed-basis check, independent audit or receipt fails; no candidate is
  published.
- `TOLERANCE_MET`: the map is valid and $R_\rho$, $R_L$ and $R_a$ all
  satisfy the unchanged tolerance.
- `VALID_NOT_MET`: the map is valid but at least one stopping defect exceeds
  the tolerance.

The dimensional leakage change, balances and offline AA(2) predicted modal
residual remain diagnostics. One map cannot establish asymptotic convergence,
stability, Anderson superiority, rank adequacy or physical accuracy, and it
starts no successor proposal or map. Preparing this host performs no Dragon,
assembly, transport or Picard calculation and produces no map result.
