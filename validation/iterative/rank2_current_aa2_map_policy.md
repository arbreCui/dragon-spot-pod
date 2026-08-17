# One strict map from the current-window standard AA(2) proposal

Date: 2026-08-16

Status: `PREPARED_NOT_RUN`.

This default-off stage permits exactly one evaluation

\[
G_2(q_{\mathrm{AA2}}),
\]

where

\[
q_{\mathrm{AA2}}=
0.72283238162036112x
-0.23768716180315402d
+0.51485478018279296e.
\]

These are the unique unmodified weights from the standard affine AA(2)
system. Anderson extrapolation naturally permits a negative weight; it is
not an empirical relaxation coefficient. No coefficient is clipped,
bounded, damped, regularized or refitted.

The proposal has already passed independent fixed-rank-two publication,
8880/8880 positivity and a 9/9 receipt. Its `AA2-RAW-FLUX` carrier is the
complete latest returned \(e\) AX and snapshot payload. No raw flux is
affinely mixed.

The unchanged host reconstructs the proposal's radial fields in the fixed
POD basis, performs three online radial fixed-source solves, and then one
reduced axial solve. Rank two, basis, normalization, physical decks, strict
inner predicates and the original outer tolerance

\[
\varepsilon=5\times10^{-7}
\]

remain unchanged. The 120-second radial and 180-second axial limits are
process-safety bounds based on recent valid runtimes; they do not enter the
physics or convergence test.

Before Dragon starts, the candidate receipt, all six parent hashes and the
exact `PROPOSAL + AA2-RAW-FLUX` preflight must pass. One activation permits
one attempt. There is no retry, fallback, relaxation, damping, clipping,
fitted closure, regularization, pseudoinverse or automatic successor.

The returned map is classified only by the existing rules:

- `INVALID_MAP`: a strict terminal, physical value, provenance check,
  independent audit or receipt fails.
- `TOLERANCE_MET`: the valid map satisfies
  \(R_\rho,R_L,R_a\le5\times10^{-7}\).
- `VALID_NOT_MET`: the map is valid but at least one of those three raw
  defects fails.

The dimensional \(D_L\), balance records and offline AA(2) predictions are
diagnostics only. This single map cannot by itself establish asymptotic
convergence, Anderson superiority, rank adequacy or physical accuracy, and
it starts no successor proposal or map.

## Post-run record

The frozen host was activated exactly once from source commit
`d6bf4365b04a4c3b9ffd41e112b44c8123f6c106`. All four strict solve
terminals, the independent audit and the 21/21 payload receipt passed. The
runtime classification is `VALID_NOT_MET`: \(R_\rho\) passes, while
\(R_L\) and \(R_a\) fail the unchanged gate. No retry or successor was
started. See [rank2_current_aa2_map_result.md](rank2_current_aa2_map_result.md).
