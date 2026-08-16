# One strict map from the latest rank-2 modal AA(1) proposal

Date: 2026-08-16

Status: `PREPARED_NOT_RUN`.

This default-off stage is prepared to evaluate exactly one unchanged
fixed-rank physical map

\[
G_2(Q(y)),\qquad
y=0.66364214132573696x_3+0.33635785867426299x_4.
\]

The coefficient is the unique, already audited standard modal AA(1)
coefficient. This stage does not recompute, fit, clip or tune it. The
hash-locked parent is the independently materialized publication \(Q(y)\).
Its canonical `(A,rho,L)` fields are the published proposal. The marker
`X4-RAW-FLUX` identifies only the complete raw AX/snapshot carrier used to
materialize that proposal; it does not identify \(Q(y)\) as \(x_4\).

The unchanged host reconstructs the rank-two radial fields from the proposal
coordinates, uses its published eigenvalue in the frozen-fission source,
performs three online radial fixed-source solves, and then performs one axial
solve. The POD basis, rank two, normalization, physical decks, strict inner
termination, and outer stopping tolerance

\[
\varepsilon=5\times10^{-7}
\]

remain unchanged. The outer decision is the original AND gate
\(R_\rho\le\varepsilon\), \(R_L\le\varepsilon\), and
\(R_a\le\varepsilon\). The dimensional leakage change and balances remain
diagnostics. The 120-second radial and 420-second axial limits are process
bounds, not physical or convergence parameters.

Before either Dragon invocation, the wrapper must verify the proposal
receipt, all six parent hashes, and the strict
`PROPOSAL + X4-RAW-FLUX` Ganlib preflight. A mismatch publishes nothing.
Activation permits exactly one attempt and no retry, relaxation, damping,
clipping, fitted closure, empirical coefficient, fallback, or successor map.

Only three classifications are allowed:

- `INVALID_MAP`: a strict solve terminal, physical value, provenance check,
  fixed-basis check, independent audit, or receipt fails; no valid candidate
  is published.
- `TOLERANCE_MET`: the map is valid and all three stopping defects satisfy
  the unchanged AND gate.
- `VALID_NOT_MET`: the map is valid but at least one stopping defect exceeds
  the unchanged tolerance.

One map cannot establish asymptotic convergence, stability, AA(1)
superiority, rank adequacy, or physical accuracy. Preparing this host performs
no Dragon, assembly, transport, or Picard calculation and produces no map
result.
