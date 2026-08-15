# One strict map from the next rank-2 modal AA(1) proposal

This default-off stage is prepared to evaluate exactly one fresh map

\[
v=G_2(w_{\rm pub}),
\qquad
w_{\rm pub}=0.0697254493303232x_2+0.9302745506696768z.
\]

The hash-locked parent is the independently materialized proposal with the
explicit `Z-RAW-FLUX` carrier. The old `X2-RAW-FLUX` proposal mode is not
accepted by this stage. The fixed rank-two basis, three frozen-fission radial
solves and one axial solve are unchanged; the parent is not re-encoded.

The outer tolerance remains

\[
\varepsilon=5\times10^{-7}.
\]

The 120-second radial and 420-second axial limits are operational process
bounds, not physical or convergence parameters. If separately activated,
there is one attempt and no retry, relaxation, damping, clipping, fitted
closure or empirical coefficient.

A parent-carrier or parent-artifact receipt mismatch rejects activation before
Dragon starts; it is not a map result and publishes nothing. Once those
preflights pass, exactly one outcome is allowed:

- **INVALID_MAP**: a strict inner terminal, physical value, provenance check,
  fixed-basis check, independent audit or runtime-result receipt fails; no
  candidate is published.
- **TOLERANCE_MET**: the map is valid and the independent defects satisfy
  \(R_\rho\le\varepsilon\), \(R_L\le\varepsilon\), and
  \(R_a\le\varepsilon\).
- **VALID_NOT_MET**: the map is valid but at least one of those defects
  exceeds \(\varepsilon\).

The dimensional leakage change and balance quantities remain diagnostics.
One valid map cannot establish rank adequacy, physical accuracy, asymptotic
convergence or Anderson superiority, and it starts no subsequent map.

Status when this policy was frozen: `PREPARED_NOT_RUN`. Freezing the policy
and its default-off host produced no map. The separately authorized single
attempt subsequently completed as `VALID_NOT_MET`; the frozen runtime copy of
this pre-run policy remains in the artifact receipt. See
[rank2_modal_aa1_next_map_result.md](rank2_modal_aa1_next_map_result.md).
