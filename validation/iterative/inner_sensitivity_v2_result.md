# Stage-4 v2 coarse-map capture result

## Status

```text
CAPTURE UNRESOLVED
REPLAY NOT-AUTHORIZED
OUTER-CONVERGENCE NOT-EVALUATED
NEXT STOP-NO-TOLERANCE-SEARCH
```

The bounded capture was executed once from authorization commit
`0217749dd9857c86e8d4e5881919220a161bab72`.  The authorization binds
implementation commit `898ffc782c027fa6e024a55b441fedcc6f9abee7`,
one Dragon process, a 120-second wall-clock limit, and no automatic replay.
The frozen Dragon executable has SHA-256
`e4c61fa45ba0fe62be3a15e21785c5e27b9a3c10d727a02754d43d7c79ef2759`.

The single process ended normally.  All three radial fixed-source solves and
the returned axial solve reached their frozen strict terminal conditions.
The result is therefore a valid comparison of

\[
x_{1,2h}=G_{2h}(x_0),\qquad 2h=10^{-6},
\]

with the archived fine map \(x_{1,h}=G_h(x_0)\), \(h=5\times10^{-7}\).

## Exact component result

The checker applies the same exact rule to every stored binary64 component:

```text
D_out,2h > 0 and D_in < D_out,2h -> RESOLVED
D_out,2h = 0 and D_in = 0        -> RESOLVED
otherwise                         -> UNRESOLVED
```

| component | \(D_{\rm out,h}\) | \(D_{\rm out,2h}\) | \(D_{\rm in}\) | relation | status |
|---|---:|---:|---:|---|---|
| \(R_\rho\) | \(1.2811548254498817\times10^{-6}\) | \(1.2170971905867134\times10^{-6}\) | \(6.4057634863168289\times10^{-8}\) | less | resolved |
| \(R_L\) | \(7.9228531576958626\times10^{-4}\) | \(9.1551322692508480\times10^{-4}\) | \(5.1551941513884668\times10^{-4}\) | less | resolved |
| \(D_L\) | \(1.1616502888500691\times10^{-6}\) | \(1.3423268683254719\times10^{-6}\) | \(7.5585558079183102\times10^{-7}\) | less | resolved |
| \(R_a\) | \(9.2282558412815538\times10^{-7}\) | \(2.2557116628569681\times10^{-5}\) | \(2.2871261661792861\times10^{-5}\) | greater | unresolved |

For \(R_a\),

\[
D_{\rm in}-D_{\rm out,2h}
=3.1414503322318077\times10^{-7},
\qquad
\frac{D_{\rm in}}{D_{\rm out,2h}}
=1.0139266484451874.
\]

These descriptive values do not add a tolerance or replace the exact
component rule.

## Physical checks

The initial state, fixed rank-one trial space, and radial inputs are bitwise
identical between the two lanes.  The independent Ganlib-only checks confirm:

- the raw radial scalar flux is strictly positive;
- the returned axial scalar flux is strictly positive;
- the physical fission and scattering source is independently rebuilt;
- the radial operator, raw map defect, archive layout, and leakage return are
  internally consistent;
- the global, maximum-group, and rank-one Galerkin balance diagnostics are
  finite and nonnegative.

Their stored binary32 diagnostic bits are respectively
`318D102D`, `3B5420D2`, and `35470AC1`.  They are reported without an
empirical magnitude threshold and are not the cause of the classification.

The failure is confined to the axial POD state metric

\[
R_a=\frac{\lVert B(a^+-a)\rVert_V}{\lVert Ba^+\rVert_V}.
\]

The fine/coarse separation in this metric is larger than the entire coarse
map update.  Therefore the change from \(2h\) to \(h\) is not demonstrably
smaller than the coarse axial-state update, and the coupled map is not
tolerance-resolved on this scale.

This result does not prove physical fixed-point divergence, prove that rank
one is insufficient, or identify a transport-balance defect.  It does prove
that the present \(2h\)-to-\(h\) pair cannot qualify the map or authorize an
outer SPOD trajectory.

## Frozen boundary and next evidence

The one-shot ledger is permanently `UNRESOLVED`.  A second capture, replay,
tolerance search, Stage-5 protocol, and outer-convergence claim are all
forbidden by this result.

The shortest admissible next diagnostic is offline and uses only the two
already captured XSM states: decompose the \(R_a\) Gram/height norm by axial
plane, energy group, and the single retained mode, and report the two update
magnitudes and their Gram inner product.  This can distinguish a magnitude
change from a direction change or normalization effect.  It changes no
physics, adds no fitted parameter, and requires no Dragon process.  It must
not retroactively change the `UNRESOLVED` classification.

## Evidence

The complete local artifact is
`validation/artifacts/inner-sensitivity-v2-capture-898ffc7/` and is excluded
from Git because it is approximately 232 MB.  Its 20-file
`artifact_manifest.sha256`, five-XSM scientific manifest, capture receipt,
one-shot ledger tombstone, exact result, and five small checker logs are
preserved in
[`inner_sensitivity_v2_result/`](inner_sensitivity_v2_result/).
