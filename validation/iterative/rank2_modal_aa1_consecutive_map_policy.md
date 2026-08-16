# One strict map from the consecutive rank-2 modal Anderson(1) proposal

Date: 2026-08-15

Status: `PREPARED_NOT_RUN`.

This default-off stage is prepared to evaluate exactly one unchanged
fixed-rank physical map

\[
G_2(x_{\mathrm{AA1}}),\qquad
x_{\mathrm{AA1}}=
0.327659203792738718x_2+0.672340796207261282x_3.
\]

The scalar is the already audited, unclipped modal Anderson(1) coefficient;
this stage does not recompute, fit or tune it. The hash-locked parent is the
independently materialized proposal. Its canonical `(A,rho,L)` fields are the
affine proposal, while `X3-RAW-FLUX` identifies the complete latest-returned
raw AX/snapshot carrier. It does not identify the proposal itself as \(x_3\).

The carrier does not replace any physical equation. If separately activated,
the unchanged host reconstructs the rank-two radial fields from the proposal
coordinates, uses the proposal eigenvalue in the frozen-fission source,
performs three online radial fixed-source solves, and then performs one axial
solve. The parent is not re-encoded. The POD basis, rank two, normalization,
physical decks, strict inner termination and outer tolerance

\[
\varepsilon=5\times10^{-7}
\]

remain unchanged. The 120-second radial and 420-second axial limits are
operational process bounds, not physical or convergence parameters.

The wrapper is default-off. The artifact receipt, six parent hashes and the
strict `PROPOSAL + X3-RAW-FLUX` Ganlib preflight must pass before the host can
begin map execution or reach either bounded Dragon invocation. A mismatch
publishes nothing. A future separately authorized run permits one attempt
and no retry,
relaxation, damping, clipping, fitted closure or empirical coefficient.

Only three classifications are allowed:

- `INVALID_MAP`: a strict solve terminal, physical value, provenance check,
  fixed-basis check, independent audit or receipt fails; no candidate is
  published.
- `TOLERANCE_MET`: the map is valid and \(R_\rho\), \(R_L\) and \(R_a\) all
  satisfy the unchanged tolerance.
- `VALID_NOT_MET`: the map is valid but at least one stopping defect exceeds
  the tolerance.

The dimensional leakage change and balances remain diagnostics. One map
cannot establish asymptotic convergence, stability, Anderson superiority,
rank adequacy or physical accuracy, and it starts no successor map. Preparing
this host performs no Dragon, assembly, transport or Picard calculation and
produces no map result.
