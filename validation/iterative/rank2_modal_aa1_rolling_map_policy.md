# One strict map from the rolling rank-2 modal Anderson(1) proposal

Date: 2026-08-16

Status: `PREPARED_NOT_RUN`.

This default-off stage is limited to exactly one evaluation

\[
G_2(x_{\mathrm{roll}}),\qquad
x_{\mathrm{roll}}=
0.439220581194280313x_{\mathrm{AA1}}^+
+0.560779418805719687x_{\mathrm{next}}^+.
\]

The hash-locked parent is the independently materialized proposal. Its
canonical `(A,rho,L)` fields contain the standard, unclipped rolling AA(1)
state. `XNP-RAW-FLUX` identifies the complete latest-returned
\(x_{\mathrm{next}}^+\) AX and snapshot carrier; it does not replace the
proposal or any physical equation.

If separately activated, the unchanged host reconstructs the rank-two radial
fields from the proposal coordinates, uses its published eigenvalue in the
frozen-fission source, performs three online radial fixed-source solves and
then one axial solve. The fixed POD package, rank two, normalization, physical
decks, strict inner terminals and outer tolerance

\[
\varepsilon=5\times10^{-7}
\]

remain unchanged. The 120-second radial and 420-second axial limits are
operational process bounds, not physical or convergence parameters.

The wrapper is default-off. The proposal receipt, six parent hashes and exact
`PROPOSAL + XNP-RAW-FLUX` Ganlib preflight must pass before either Dragon
invocation. One activation permits one attempt and no retry, relaxation,
damping, clipping, fitted closure or empirical coefficient.

Only three classifications are allowed:

- `INVALID_MAP`: a strict solve terminal, physical value, provenance check,
  fixed-basis check, independent audit or receipt fails; no candidate is
  published.
- `TOLERANCE_MET`: the map is valid and $R_\rho$, $R_L$ and $R_a$ all
  satisfy the unchanged tolerance.
- `VALID_NOT_MET`: the map is valid but at least one stopping defect exceeds
  the tolerance.

The dimensional leakage change and balances remain diagnostics. The offline
AA(1) minimized residual is not an acceptance quantity. One map cannot
establish asymptotic convergence, stability, Anderson superiority, rank
adequacy or physical accuracy, and it starts no successor proposal or map.
Preparing this host performs no Dragon, assembly, transport or Picard
calculation and produces no map result.

## Post-run record

The frozen host was subsequently activated exactly once from source commit
`d8c87eaf70cace3e976ac1fe10d0c60eba35512f`. All strict terminals, the
independent audit and the 21-entry receipt passed. The runtime classification
is `VALID_NOT_MET`; \(R_L\) and \(R_a\) exceed the unchanged tolerance. No
retry, successor proposal or successor map was started. See
[rank2_modal_aa1_rolling_map_result.md](rank2_modal_aa1_rolling_map_result.md).
