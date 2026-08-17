# Latest rank-2 modal AA(1) proposal publication

Date: 2026-08-16

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

## Published proposal

The two frozen evaluated pairs are

\[
x_3\mapsto x_4, \qquad Q(y)\mapsto z,
\]

with residuals \(p=x_4-x_3\) and \(q=z-Q(y)\). In the unchanged full
Gram-height metric, the unique standard depth-one coefficient gives

\[
\beta=0.776666030394551732,
\qquad
t=0.223333969605448268x_4+0.776666030394551732z.
\]

This stage deterministically materialized \(Q(t)\). The same weights were
applied to \((A,\rho,L)\). No relaxation, damping, clipping, fitted
coefficient, regularization, pseudoinverse threshold, fallback or separate
leakage coefficient was used.

## Publication arithmetic

| quantity | value |
|---|---:|
| modal denominator | `6.18132785403392786e-12` |
| affine \(\rho\) | `0.733992887399932070` |
| REAL32-published \(k\) | `1.36241102218627930` |
| reciprocal published \(\rho\) | `0.733992887399932070` |
| maximum leakage REAL32 round trip | `5.43286316542074266e-11` |
| minimum published REAL32 \(B_2A\) | `1.75340256416701415e-15` |
| strictly positive reconstructed points | `8880 / 8880` |

The modal coordinates remain REAL64 affine values. Leakage uses the existing
REAL32 publication round trip. The effective eigenvalue is published in
REAL32, and stored \(\rho\) is its REAL64 reciprocal.

## Carrier and independent audit

The complete returned \(z\) AX and snapshot objects supply the raw carrier.
The proposal is marked `PROPOSAL + Z-RAW-FLUX`; raw axial and plane fluxes
were not mixed. Only declared publication fields changed, stale result
records were removed, and the returned carrier's fixed basis, normalization,
state metadata and lagged `SYSTEM` history were preserved.

The separately compiled Ganlib checker independently recomputed AA(1) and
verified the fixed rank-two bundle, the actual
`Q(y) [X4-RAW-FLUX] -> z` lifecycle, complete \(z\) AX/snapshot carrier,
publication arithmetic, stale-record absence and 8880-point positivity.
The symbol census found `DRAGON/ASM/FLU/TRANSPORT=0`.

## Frozen provenance and receipt

The six inputs are frozen in
[`rank2_latest_modal_aa1_next_candidate_inputs.tsv`](rank2_latest_modal_aa1_next_candidate_inputs.tsv),
whose SHA-256 is
`4a814fbf19de8c6804fa41d6971eaf5c04fdc0d60c4f84107ed96fd8c1b7132b`.

| implementation | SHA-256 |
|---|---|
| builder | `fba31e67d27250665869feba7e7f539c2bc4e2767fdee2f25db4a75b52f6edff` |
| checker | `41fba47dfd1c2ccb1285d01ade3a472937e0ed4ba8ca42e2a36185a4f2dcbba9` |
| runner | `b0fcfedf6e9980c730cd6b0e5ea58f82c504f927fb417227ed07c249f6a981f0` |

The Git-ignored artifact contains ten regular files, no symbolic links, and
a passing 9/9 receipt.

| artifact | SHA-256 |
|---|---|
| `proposal_axial.xsm` | `e9e37246df25ef9afb449fad77e55b6ce21cd03f09e2f185d458aea4bd85d28c` |
| `proposal_snapshots.xsm` | `8414fb2298bcd9797f5d1b0613d985413c7c87d533feb80e8f24360471c05b38` |
| `build.log` | `96500bd387d3a8f0966bd4fd07c247aa84f5fdae65cdbc4aea9da17e2f3d1ad6` |
| `check.log` | `34405a0becd211a6938311cc98569fee50942324d07886358cdfaa519dbdd045` |
| receipt | `de0be838f43dc4a644480e47474d6f1667031259e8a402fc148db7a734716329` |

Reproduce into a fresh artifact directory with:

```sh
ARTIFACT_DIR=/absolute/path/to/fresh-result \
  make spot-rank2-latest-modal-aa1-next-candidate
```

The default artifact path refuses overwrite.

## Scientific boundary

This was only deterministic publication and carrier checking. It ran no
Dragon, radial solve, axial solve or nonlinear map. It therefore created no
new \(R_\rho\), \(R_L\), \(D_L\) or \(R_a\), did not test the AND gate, and
establishes no convergence factor, contraction, stability, monotonicity,
AA(1) superiority, rank adequacy or physical accuracy.

No map host was added or started. If separately authorized, exactly one
unchanged evaluation \(G_2(Q(t))\) is the next physical test.

## Subsequent authorized attempt

The publication result above remains the frozen no-map stage record. A later
default-off host was separately activated exactly once. Its `proposal-z`
preflight and three radial strict terminals passed, but the axial solve did
not produce a strict terminal before the predeclared 80-second process
bound. The attempt is `INVALID_MAP / TIMEOUT_BEFORE_TERMINAL`; it created no
candidate or stopping defect and was not retried. See
[rank2_latest_modal_aa1_next_map_attempt_result.md](rank2_latest_modal_aa1_next_map_attempt_result.md).
