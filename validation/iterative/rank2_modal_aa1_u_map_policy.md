# One strict map from the latest rank-2 modal AA(1) proposal

This default-off stage is prepared to evaluate exactly one fresh physical map

\[
G_2(u_{\rm pub}),
\qquad
u_{\rm pub}=0.0430261171283013z+0.956973882871699v.
\]

The hash-locked parent is the independently materialized proposal with the
explicit `V-RAW-FLUX` carrier. The earlier `X2-RAW-FLUX` and `Z-RAW-FLUX`
proposal modes are not accepted. Carrier provenance does not replace a solve:
the unchanged map reconstructs the rank-two radial fields from the published
coordinates, uses the published eigenvalue \(k\) in the frozen-fission source,
performs three online radial fixed-source solves and then one axial
solve. The parent is not re-encoded.

The fixed POD basis, rank two, normalization, physical decks and strict inner
termination remain unchanged. The outer tolerance remains

\[
\varepsilon=5\times10^{-7}.
\]

The 120-second radial and 420-second axial limits are operational process
bounds, not physical or convergence parameters. If separately activated,
there is one attempt and no retry, relaxation, damping, clipping, fitted
closure or empirical coefficient.

A parent-carrier or artifact-receipt mismatch rejects activation before
Dragon starts. It is not a map result and publishes nothing. Once those
preflights pass, exactly one outcome is allowed:

- **INVALID_MAP**: a strict inner terminal, physical value, provenance check,
  fixed-basis check, independent audit or runtime-result receipt fails; no
  candidate is published.
- **TOLERANCE_MET**: the map is valid and the three independent raw stopping
  defects satisfy \(R_\rho\le\varepsilon\), \(R_L\le\varepsilon\), and
  \(R_a\le\varepsilon\).
- **VALID_NOT_MET**: the map is valid but at least one of those three defects
  exceeds \(\varepsilon\).

The dimensional leakage change, balances, the offline `0.882410` affine
screen and cross-map ratios remain diagnostics. They cannot accept a state.
One map cannot establish asymptotic convergence, stability, Anderson
superiority, rank adequacy or physical accuracy, and it starts no subsequent
map. Even `TOLERANCE_MET` would establish only the stated discrete rank-two
fixed-point stopping gate, not physical validation.

Status: `PREPARED_NOT_RUN`. Freezing this policy and its default-off host
produces no map.
