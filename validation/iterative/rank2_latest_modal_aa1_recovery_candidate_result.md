# Latest recovery-history rank-2 modal AA(1) publication

Date: 2026-08-16

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

## Published proposal

The two hash-locked evaluated pairs are

\[
Q(y)\mapsto z, \qquad Q(t)\mapsto u,
\]

with residuals $q=z-Q(y)$ and $r=u-Q(t)$. Recomputed in the unchanged
full Gram-height metric,

\[
\beta=\frac{\lVert q\rVert_{HG}^{2}-\langle q,r\rangle_{HG}}
{\lVert r-q\rVert_{HG}^{2}}
=0.184362130017637404,
\]

so this stage materialized

\[
Q(s)=Q(0.815637869982362540z+0.184362130017637404u).
\]

The coefficient was recomputed from the four frozen states, not supplied as
an adjustable number. The same weights were applied to $(A,\rho,L)$. No
relaxation, damping, clipping, fitted coefficient, regularization,
pseudoinverse threshold, fallback or separate leakage coefficient was used.

## Publication arithmetic

| quantity | value |
|---|---:|
| modal denominator | `9.14683788331648823e-12` |
| affine \(\rho\) | `0.733992899240309749` |
| REAL32-published \(k\) | `1.36241102218627930` |
| reciprocal published \(\rho\) | `0.733992887399932070` |
| absolute \(\rho\) publication delta | `1.18403776783182479e-8` |
| maximum leakage REAL32 round trip | `5.20275916533058380e-11` |
| minimum published REAL32 \(B_2A\) | `1.75340224652965893e-15` |
| strictly positive reconstructed points | `8880 / 8880` |

Modal coordinates remain REAL64 affine values. Leakage uses the existing
REAL32 publication round trip. The effective eigenvalue is published in
REAL32, and stored \(\rho\) is its REAL64 reciprocal.

## Carrier and independent audit

The latest valid returned state $u$ supplies the complete AX/raw-flux and
snapshot carrier. The proposal is marked `PROPOSAL + U-RAW-FLUX`. This marker
records carrier provenance; it does not claim that the copied raw flux is a
solved flux for $s$. Raw fluxes from $z$ and $u$ were not mixed.

Only the declared publication fields changed. The fixed rank-two bundle,
normalization, state metadata and lagged `SYSTEM` from $u$ were preserved,
and stale result records were removed.

The separately compiled Ganlib checker independently recomputed AA(1), bound
the two proposal carriers (`X4-RAW-FLUX` and `Z-RAW-FLUX`), verified the
actual `Q(t) -> u` snapshot lifecycle, checked the complete $u$ carrier,
publication arithmetic, stale-record absence and 8880-point positivity. The
symbol census found `DRAGON/ASM/FLU/TRANSPORT=0`.

## Frozen provenance and receipt

The six inputs are frozen in
[`rank2_latest_modal_aa1_recovery_candidate_inputs.tsv`](rank2_latest_modal_aa1_recovery_candidate_inputs.tsv),
whose SHA-256 is
`98a2f4a91130944398cb071c2de110644c0b54cd83fc222ab8329729ccddd1ed`.
The preceding four-state decision manifest remains frozen at
`28e83b947900b681780fb4b73bb07b81f148cbb7c17c05e5b9de956a33dbfa01`.

| implementation | SHA-256 |
|---|---|
| builder | `904306a75d027dcc5c53e1b0772bf7e487638db6d539307acd0e86a0fd21e3a0` |
| checker | `3a9425fc21482dedb53adf4b43f536daec52bad73d959073216f66edab02b0a7` |
| runner | `d904c8517c57784cf4f3a3ff3cb677545a6e343f445c3bf2a282a50c97d82c6c` |

The Git-ignored artifact contains ten regular files, no symbolic links, and
a passing 9/9 receipt.

| artifact | SHA-256 |
|---|---|
| `proposal_axial.xsm` | `53f6bb3e48ef583778e54ce0e21ff68f5f63d3d3857c3211c0803bc9a2ef0193` |
| `proposal_snapshots.xsm` | `3404d4295b8f71fa20d9b565fc88c0631184775dcac336be2f50e797999cefaa` |
| `build.log` | `c30924a4a8432568c33b8057b30873d1fd070063f8cc0ab8802205bebdd7dd64` |
| `check.log` | `32fede8eefbace8d81ccce4d45cbcd88503a9be1aeac0e77d1e9b23cb01d701d` |
| receipt | `33326758295453f6ab4d4d018d8830d119ceb5bc9ba4cc4b5e82ce1e66500b22` |

Reproduce into a fresh artifact directory with:

```sh
ARTIFACT_DIR=/absolute/path/to/fresh-result \
  make spot-rank2-latest-modal-aa1-recovery-candidate
```

The default artifact path refuses overwrite.

## Scientific boundary

This was deterministic publication and independent carrier checking only.
It ran no Dragon, radial solve, axial solve or nonlinear map. It therefore
created no new $R_\rho$, $R_L$, $D_L$ or $R_a$, did not test the AND
gate, and establishes no convergence factor, contraction, stability,
monotonicity, AA(1) superiority, rank adequacy or physical accuracy.

No map host was added or started. A future evaluation $G_2(Q(s))$ requires
a separate decision and authorization.
