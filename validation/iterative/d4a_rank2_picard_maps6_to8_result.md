# D4-A rank-2 Picard maps 6 to 8

Maps 6, 7, and 8 continue the frozen D4-A rank-2 SPOD route from
`CLOSED/5`.  They use the same basis, cross sections, radial and axial
transport operators, route contract, and direct Picard update (`alpha = 1`).
No relaxation, damping, empirical parameter, rank change, or model correction
is present.

The fixed convergence threshold is `5e-7` for all three gated defects:

| map | `Rrho` | `Rleak` | `Ra` | classification |
|---:|---:|---:|---:|---|
| 6 | `8.5358311630034933e-7` | `2.9010277829192167e-6` | `5.5994551813715369e-6` | `VALID_NOT_MET` |
| 7 | `1.0664930039094855e-7` | `5.8768601502047976e-7` | `1.1249737924997042e-6` | `VALID_NOT_MET` |
| 8 | `6.3952111273302137e-8` | `3.4898525208435340e-7` | `3.4971804373678926e-7` | `VALID_MET` |

Map 8 is the first accepted fixed point.  Its axial eigenvalue is
`1.2863778402485850`.  The non-gated out-of-span diagnostic is
`6.3522525147971617e-8`; it remains below the gated physical defects and does
not indicate a rank bottleneck.

For every map, B2W produced the expected continued `CLOSED/n` state, the
independent checker passed POD identity, live radial change, positivity,
canonical layout, raw defect, and restart archive, and the execution, input,
and output SHA-256 manifests rechecked byte-for-byte.  The map-8 evidence is
stored under:

- `validation/artifacts/iterative-d4a-rank2-picard-map8/close.log`
- `validation/artifacts/iterative-d4a-rank2-picard-map8/independent_check.log`
- `validation/artifacts/iterative-d4a-rank2-picard-map8/gate.log`
- `validation/artifacts/iterative-d4a-rank2-picard-map8/execution_manifest.sha256`
- `validation/artifacts/iterative-d4a-rank2-picard-map8/input_manifest.sha256`
- `validation/artifacts/iterative-d4a-rank2-picard-map8/output_manifest.sha256`

The D4-A rank-2 physical Picard route is therefore converged under its frozen,
predeclared validation contract.  No further Picard map is justified for this
case.

## Self-contained freeze

On 2026-09-04 the seven absolute input links in the map-8 artifact were
materialized without changing their contents.  The exact production Dragon,
host tools, their Fortran sources, bounded runner, one-map runner, and maps
6-to-8 wrapper were copied into `frozen_runtime/`.  The artifact now contains
no symbolic links.  Re-running the frozen continued-state checker and gate
produced byte-identical logs.

The complete freeze receipt is:

- `result.sha256`: `85f308da73ea20efc7afc68a524db21368af4b5e6a9bde0a661b4e97f057f369`;
- `closed_axial.xsm`: `a55222ac7b2d4b25d27cd7c196ef8c4638c12037bf35410e02f87666bc647a9b`;
- `closed_snapshots.xsm`: `45b1d09ea8fffe9097d70b91410095341fc334f0fe426df27d4e415ef6721a88`.

`result.sha256` covers every regular file in the 880 MB self-contained
artifact except itself, including the original three manifests, all logs,
continued-state inputs and outputs, the saved link provenance, and the frozen
runtime files.
