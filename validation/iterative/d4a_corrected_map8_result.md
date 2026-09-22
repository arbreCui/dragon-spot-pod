# Corrected D4-A direct-Picard map 8

This is the corrected-material map 8, not the historical legacy-material
map-8 regression. The unchanged serial controller completed, checked and
froze it before starting global map 9.

| item | exact value |
|---|---|
| lifecycle | `CLOSED/7 -> PROJECTED/8 -> RETURNED/8 -> CLOSED/8` |
| classification | `VALID_NOT_MET` |
| portable role | `NEXT_MAP_PARENT_ONLY` |
| `R_rho` | `1.0492739930256789E-06` |
| `R_L` | `3.1031397842917180E-06` |
| `R_a` | `1.3106218716376795E-05` |
| SHA-256 of `result.sha256` | `d8ff71b79ce3eb326e5db770d500fe27d285d06bec19a8c97b71bc27eefffa98` |

Portable evidence:
`validation/artifacts/d4a-corrected-material-rank2-series-from-map5-20260922/map-003.portable`.
The full manifest and eight-input/six-output manifests verify. Direct
independent XSM and convergence-gate replay reproduces both saved logs byte
for byte. Radial CPU time was 17736 seconds; axial CPU time was 1 second.
All three defects remain above `5e-7`, so no corrected fixed point is claimed.

The following map 9 (`map-004.raw`) is incomplete. Its supervising runner
recorded `KeyboardInterrupt` while waiting for Dragon; the serial owner and
Dragon processes were absent at inspection. This is an interrupted run, not
a failed convergence result, and its partial output is not a restart parent.
Maps 6–8 remain sealed and unaffected. A new long continuation from portable
`CLOSED/8` requires approval; none was started while doing the short material
audit. No physics, rank, Picard update or acceptance threshold changed.
