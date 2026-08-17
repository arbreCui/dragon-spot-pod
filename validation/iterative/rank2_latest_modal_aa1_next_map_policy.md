# One strict map from the latest modal AA(1) history proposal

Date: 2026-08-16

Status: `PREPARED_NOT_RUN`.

This default-off stage is prepared to evaluate exactly one unchanged
fixed-rank physical map

\[
Q(t)^+=G_2(Q(t)),\qquad
t=0.223333969605448268x_4+0.776666030394551732z.
\]

The coefficient is the unique, already audited standard modal AA(1)
coefficient. This stage does not recompute, fit, clip or tune it. The
hash-locked parent is the independently materialized publication \(Q(t)\).
Its canonical `(A,rho,L)` fields are the map input. The marker
`Z-RAW-FLUX` identifies only the complete raw AX/snapshot carrier inherited
from the latest returned state \(z\); it does not identify \(Q(t)\) as \(z\).

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
diagnostics. The 120-second radial and 80-second axial limits are process
bounds, not physical or convergence parameters.

Before either Dragon invocation, the wrapper must verify the proposal
receipt, all six parent hashes, and the strict
`PROPOSAL + Z-RAW-FLUX` Ganlib preflight. A mismatch publishes nothing.
Activation permits exactly one attempt and no retry, relaxation, damping,
clipping, fitted closure, empirical coefficient, fallback, or successor map.

Only three classifications are allowed:

- `INVALID_MAP`: a strict solve terminal, physical value, provenance check,
  fixed-basis check, independent audit, timeout, or receipt fails; no valid
  candidate is published.
- `TOLERANCE_MET`: the map is valid and all three stopping defects satisfy
  the unchanged AND gate.
- `VALID_NOT_MET`: the map is valid but at least one stopping defect exceeds
  the unchanged tolerance.

One map cannot establish asymptotic convergence, stability, contraction,
convergence order, AA(1) superiority, rank adequacy, or physical accuracy.
Preparing this host performs no Dragon, assembly, transport, or Picard
calculation and produces no map result.
