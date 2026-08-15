# One strict map from the rank-2 modal AA(1) proposal

This stage evaluates exactly one fresh physical map

\[
z=G_2(y_{\rm pub}),
\]

where `y_pub` is the hash-locked materialized proposal.  It reuses the fixed
rank-2 basis and the unchanged three-plane frozen-fission radial solves plus
one axial solve.  The proposal is not re-encoded, and its missing old defect
and off-space records are not manufactured.

The outer tolerance remains

\[
\varepsilon=5\times10^{-7}.
\]

The 120-second radial and 420-second axial host limits are operational process
bounds inherited from the last completed rank-2 map.  They are not physical,
coupling or convergence parameters.  There is one attempt and no retry,
relaxation, damping, clipping, fitted closure or empirical coefficient.

Exactly one outcome is reported:

- **INVALID_MAP**: a strict inner terminal, physical value, provenance check,
  fixed-basis check, independent audit or receipt fails; no candidate is
  published.
- **TOLERANCE_MET**: the map is valid and the independent defects satisfy
  \(R_\rho\le\varepsilon\), \(R_L\le\varepsilon\), and
  \(R_a\le\varepsilon\).
- **VALID_NOT_MET**: the map is valid but at least one of those three defects
  exceeds \(\varepsilon\).

The dimensional leakage change, balance quantities and the earlier offline
AA(1) prediction remain diagnostics.  They cannot accept the state.  A valid
map evaluates only this one proposal; it does not establish rank adequacy,
physical accuracy or asymptotic convergence, and it starts no subsequent map.
