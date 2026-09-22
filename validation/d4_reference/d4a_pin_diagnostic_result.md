# Corrected D4-A pin-rate diagnostic (2026-09-23)

The static path is implemented and tested: saved geometry -> 217-pin
crosswalk, saved physical flux -> 75 regional rates, and conservative
expansion -> 651 pin/floor records. No tracking or transport was run.

This run reads the corrected **map 8, `VALID_NOT_MET`**, from
`validation/artifacts/d4a-corrected-material-rank2-series-from-map5-20260922/map-003.portable`.
Its `result.sha256` hash is
`d8ff71b79ce3eb326e5db770d500fe27d285d06bec19a8c97b71bc27eefffa98`;
the full input inventory verified before and after extraction. The canonical
Dragon hash is unchanged. These outputs are **DIAGNOSTIC_ONLY**, not final
power, convergence, or an independent SPOT–CE accuracy result.

## What was checked

- The three saved TRACK geometries agree. Only the 2268 active SAL elements
  are read; unused allocation capacity is not geometry. `NumMerge/VolMerge`
  are read from `TRACK/NXTRecords`.
- Inner and outer fuel boundaries identify 25 symmetry orbits and exactly
  217 unique CE lattice sites: 12 orbits of 12, 12 of 6, and the central pin.
  Translation comes from the saved central fuel topology; the stated
  coordinate convention then rotates by +90 degrees.
- Coordinate admission uses the frozen input's existing SAL EPS, interpreted
  as REAL32 (`9.999999747378752e-6 cm`), with exactly one candidate allowed.
  No fitted matching tolerance or nearest-neighbour fallback is used.
  Maximum center offset is `8.371592565024716e-8 cm`; lattice spacing is
  `1.07 cm`. This is admission within the declared geometry resolution, not
  a proof of coordinate bit equality.
- Independent saved-boundary area integration reproduces every fuel orbit's
  TRACK REAL32 area. Total saved fuel area and expanded per-pin area both
  equal `113.44341611862183 cm²`. The nominal CE area is separately reported
  as `113.44340159497953 cm²`; saved SAL geometry is not silently replaced
  with idealized circles or rescaled to force equality.
- The rate exporter checks all 396 physical regions, distinct `KEYFLX`,
  and fission support only in materials 4/10/16. It uses the same REAL32
  `FLUX` mirror, NUSIGF layout and REAL64 floor-accumulation order as SPORATE.
  Calling the existing SPORATE on the same read-only inputs gives identical
  printed floor fractions: `0.259763552 / 0.484196653 / 0.256039795`.
- Per-pin quantities are the orbit quantities divided by the number of pins
  in that orbit. There is no additional factor of 12 or renormalization.
  Exact-rational conservation differences are bounded solely by half-ULP
  division roundoff. The global fraction sum stays `0.9999999999999989`.

The output directory is
`validation/artifacts/d4a-map8-pin-diagnostic-20260923`:

| output | data rows | SHA-256 |
|---|---:|---|
| `pin_crosswalk.csv` | 217 | `5de3f42247f00fd2f998917bd0235fc5d25a8254811d836b69af36c21dc2e9f1` |
| `region_rates.csv` | 75 | `43750c14fc4ef950ada0614e1a6cd0f7dfddc9ff6d50b02d29e1e3f687aa8d93` |
| `pin_rates.csv` | 651 | `0c2d023dc56a4f9e277bc267549a86c8f19f110734b5eac11267475e459c8e97` |

`geometry_checks.json`, `conservation.json`, the saved-geometry text and
host logs contain the detailed checks. Same-orbit pins share one SPOT
solution; this is not a new solve for 217 independent radial fields.
The scored quantity is nu-fission production, not absolute thermal power.

## Reproduce without transport

Build only the optional host tools; this does not rebuild Dragon. In a fresh
source checkout first build Ganlib alone with
`make -C Ganlib/src -j2 libGanlib.a`, then run `make -C validation/iterative pin-tools`.
The pin target now directly links the existing SPORATE source and Ganlib,
not `libDragon.a`. Use an isolated checkout for this setup while production
is running; do not rebuild shared production libraries.

```sh
set -eu
make -C validation/iterative pin-tools
R=/absolute/path/to/spot
MAP=/absolute/path/to/the/verified/portable/map
OUT=/absolute/path/to/a/new/diagnostic-directory
PY=/path/to/openmc-python
(cd "$MAP" && shasum -a 256 -c result.sha256)
mkdir "$OUT"
bounded() { python3 -c 'import subprocess,sys; subprocess.run(sys.argv[1:],check=True,timeout=10)' "$@"; }
(
  cd "$MAP"
  bounded "$R/validation/iterative/export_d4a_pin_geometry" \
    closed_snapshots.xsm "$OUT/saved_geometry.txt"
  bounded "$R/validation/iterative/export_d4a_region_rates" \
    closed_axial.xsm initial_axial_track.xsm initial_axial_macrolib.xsm \
    "$OUT/region_rates.csv" > "$OUT/region_export.log"
)
bounded "$PY" "$R/validation/d4_reference/build_d4a_pin_crosswalk.py" \
  --geometry-export "$OUT/saved_geometry.txt" --output-dir "$OUT"
bounded python3 "$R/validation/d4_reference/expand_d4a_pin_rates.py" \
  "$OUT/pin_crosswalk.csv" "$OUT/region_rates.csv" "$OUT/pin_rates.csv" \
  > "$OUT/conservation.json"
(cd "$MAP" && shasum -a 256 -c result.sha256)
```

The geometry builder uses the existing OpenMC Python package only to obtain
the fixed CE lattice definition; it starts no OpenMC executable. The
crosswalk does not infer a source iteration or convergence classification.
The caller must bind the diagnostic to its verified input, as above.

Short tests passed: 8 geometry positive/negative tests; region-rate integer
reference, 11 invalid-input cases and overwrite refusal; 3 expansion tests
(including invalid-input subcases and preservation of non-unit input scale).

```sh
python3 validation/iterative/test_d4a_region_rates.py
"$PY" validation/d4_reference/test_d4a_pin_crosswalk.py \
  --geometry-export "$OUT/saved_geometry.txt" -v
python3 validation/d4_reference/test_expand_d4a_pin_rates.py
```

## Independent clean-source replay and comparison readiness

A clean `git archive af24a1d` replay built all Ganlib routines and the sole
required Dragon library member, SPORATE, from that archive before building
both optional hosts. No old object, module or static library was reused,
and no Dragon executable was built. This is the tools' full dependency
closure, not a full-product rebuild. Build time was 2.703 seconds; each
extraction/test command was under 2 seconds. All eight outputs listed in the
diagnostic directory reproduced byte-for-byte, including the three CSV
hashes above; the source archive's 2016 tracked files remained unchanged.
The replay is in `/private/tmp/d4a-pin-clean-af24a1d.hb4Z1B`, with
`build.log` and `replay_verification.log`. Its observation of a changed main
Dragon hash exposed the independent main-runner build incident recorded in
[the handoff](../iterative/d4a_final_validation_handoff.md); it neither
compiled nor executed that binary.

The minimal dependency closure is now also the ordinary Makefile rule,
not merely an ad-hoc clean-build exercise. A fresh source export of
`a54ea87` plus the final Makefile/comment-only changes was tested in
`/private/tmp/d4a-pin-minimal-build.KwgxPQ`. Only Ganlib was built before
`make -C validation/iterative pin-tools`; no Dragon executable or Dragon
library existed in that tree. The integer-reference region test, all 11
invalid-input cases and overwrite refusal passed. Actual map-8 geometry,
regional CSV and both host logs reproduced byte-for-byte. The one unused
dummy-argument warning in SPORATE's unchanged CLE interface is explicitly
suppressed for this target; numerical checking/arithmetic flags are retained.

`compare_d4a_pin_rates.py` now joins SPOT and CE by unique `(floor,pin_index)`
and reports unmodified global-fraction differences. Its 14 synthetic tests
pass, including shuffled order, zero bins, missing/duplicate IDs and one-ULP
CE normalization inconsistencies. The tool does not authenticate either
input's provenance or convergence. CE raw tally standard deviation is not
converted into fraction uncertainty without the missing covariance.

## First real CE pin comparison (still provisional)

After the one authorized CE production completed, its unchanged files were
again replayed through `read_ce()` in `check_d4a_spot_ce_receipts.py`:
static inputs, nuclear-data/runtime identity, final statepoint, all 651 bins
and the existing sigma limit passed. The frozen execution controls were
checked separately (20,000 particles, 300 batches, 100 inactive, seed 731942,
18 threads). No transport was launched. The three saved SPOT CSV hashes
above were rechecked before using the existing comparator; its 14 synthetic
tests also passed again.

The new directory is
`validation/artifacts/d4a-map8-ce-pin-comparison-20260923`.
All 651 records join uniquely by `(floor,pin_index)`, not row position.
Fractions were used unchanged, with no rescaling, clipping, or fitted factor.
The reference is the accepted CE-only result under
`validation/artifacts/d4a-corrected-ce-production-20260923`; SPOT is still
the explicitly **nonconverged map 8** above.

| temperature zone | SPOT global fraction | CE global fraction | SPOT−CE, percentage points |
|---|---:|---:|---:|
| bottom | 0.25976355211228924 | 0.26192486508860197 | −0.21613130 |
| middle | 0.4841966529486634 | 0.4849344596237941 | −0.07378067 |
| top | 0.2560397949390463 | 0.2531406752876039 | +0.28991197 |

Maximum absolute global-fraction difference is `2.874340663687469e-5`
at floor 2, pin index 16 (zero-based); RMS is `1.1166553753187574e-5`.
For a second descriptive scale, define each relative difference as
`100*(SPOT_fraction-CE_fraction)/CE_fraction` (all CE bins are positive).
Its maximum magnitude is `1.8598648093461192%` at floor 3, pin 63;
its unweighted RMS across all 651 bins is `0.8752204904351076%`.
These are observed differences, including CE sampling noise, not proven
deterministic errors, uncertainty-adjusted values or a new accuracy gate.
Normalized-fraction covariance remains unavailable; no significance claim
or fraction sigma is inferred from the raw tally standard deviations.

Output SHA-256:

- `pin_comparison.csv`: `1eedf33ed7cbd2138ce90977379ef76ca8c9abf73e3bef3ef2bc5a67de522dab`
- `comparison_summary.json`: `d8be754bb3d64aed97a68d9e81d8e07a424aefb279ad3bce3cc414abdfb775c5`
- input CE `reference_result.json`: `d883cc06d8f2a8ca3c60b964ea295115ceb2cf892a32f0be94dd025fc972f154`

The comparator's summary honestly says `source_authentication=NOT_PERFORMED`:
authentication is supplied by the separate CE replay and manifested SPOT
extraction described above, not by the arithmetic comparator itself.
Overall status remains **DIAGNOSTIC_ONLY / REPORTED_ONLY**. This closes the
real-data postprocessing rehearsal, not convergence or pin-accuracy validation.
An independent read-only review recomputed every difference using exact
rational representations before rounding, confirmed max/RMS/floor summaries,
and matched all integer lattice/ring and cell identities against the CE pin
map. The maximum absolute difference is on the outermost pin ring (ring 8).

Remaining science boundary: rerun extraction on the first accepted fixed
point and compare that state against the same accepted CE observables.
The authoritative receipt comparison still reports floor differences only;
neither diagnostic tool adds or relaxes a pin-power accuracy criterion.
All quantities here are globally normalized nu-fission production, not
absolute thermal power.
