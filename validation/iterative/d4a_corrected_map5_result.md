# Corrected D4-A direct-Picard map 5

The fifth corrected-material rank-two map completed all three online radial
responses and the reduced axial solve with the unchanged `alpha=1` update.
On 2026-09-22 the existing freezer replayed the independent XSM checker and
convergence gate, required byte-identical logs, and produced a portable copy.

| item | exact value |
|---|---|
| lifecycle | `CLOSED/4 -> PROJECTED/5 -> RETURNED/5 -> CLOSED/5` |
| classification | `VALID_NOT_MET` |
| portable role | `NEXT_MAP_PARENT_ONLY` |
| `R_rho` | `1.2008320856993215E-04` |
| `R_L` | `1.0779227410496446E-04` |
| `R_a` | `3.4736134630042396E-04` |
| SHA-256 of `result.sha256` | `d826307de3690130a54621b2d123773d4c9e900c567ead4c3fcb278bf63f4fbd` |

Portable evidence:
`validation/artifacts/d4a-corrected-material-rank2-map5-portable-detached-20260922`.
Its complete `result.sha256`, eight-input manifest and six-output manifest
verify. The basis, route contract, tracks and axial macrolib match the admitted
corrected bootstrap. All three outer defects remain above `5e-7`.

The raw map is `map-001.raw` in
`validation/artifacts/d4a-corrected-material-rank2-series-from-map4-20260921`.
It ended normally on 2026-09-21 at 23:12 local time. Radial CPU time was
17927 seconds; axial CPU time was 7 seconds. The former series process and
tool session were absent when inspected on 2026-09-22. Its result table had
only a header and no portable copy existed. The exact cause of the series
exit was not captured; the numerical result passed direct read-only replay.
The raw directory and old table were left intact, and no transport was rerun.

The next unchanged serial continuation starts from this portable `CLOSED/5`
under `validation/artifacts/d4a-corrected-material-rank2-series-from-map5-20260922`.
Its full console output is retained in the adjacent `.runner.log` file.
The seven-map operational bound covers maps 6 through 12, preserving the
original total map budget. It stops at the first `VALID_MET` or any failure;
the cap itself never establishes convergence.

There is still no corrected fixed-point claim, final k/power result or
independent CE comparison.
