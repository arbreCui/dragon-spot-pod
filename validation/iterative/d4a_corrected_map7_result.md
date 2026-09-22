# Corrected D4-A direct-Picard map 7

The unchanged serial controller completed, independently checked and froze
global map 7, then started map 8. The method remains fixed rank two and
direct Picard (`alpha=1`); no physical or numerical controls changed.

| item | exact value |
|---|---|
| lifecycle | `CLOSED/6 -> PROJECTED/7 -> RETURNED/7 -> CLOSED/7` |
| classification | `VALID_NOT_MET` |
| portable role | `NEXT_MAP_PARENT_ONLY` |
| `R_rho` | `6.6053233140905832E-06` |
| `R_L` | `1.0785822056014212E-05` |
| `R_a` | `3.9279414674760791E-05` |
| SHA-256 of `result.sha256` | `5f4d1c9e49634ecf221f6003ca53344ff3bbd27c6b62a9fc48737a1242bde250` |

Portable evidence:
`validation/artifacts/d4a-corrected-material-rank2-series-from-map5-20260922/map-002.portable`.
The complete receipt and its eight-input/six-output manifests verify. Direct
replay of the independent XSM checker and convergence gate reproduces both
saved logs byte for byte. All three outer defects remain above `5e-7`.

Radial CPU time was 18130 seconds and axial CPU time was 2 seconds. The
largest outer defect decreased from map 6's `1.1538196291776131E-04` to
`3.9279414674760791E-05`. This is progress, not an accepted fixed point.

The subsequent global map 8 is recorded separately in
[its corrected-material result](d4a_corrected_map8_result.md). There is no
corrected final k/power or independent CE comparison yet.
