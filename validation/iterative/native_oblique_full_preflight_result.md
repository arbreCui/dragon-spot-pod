# Complete native-path geometry: preflight and measure audit passed

All **11,364 original paths** have now been enumerated and audited across the
entire declared geometry matrix. The maximum local volume/face-measure error
is **1.88000e-12**, below the frozen **5e-12** gate. Independent interval-incidence
counts agree with every explicitly traced chord and piece count. Full fresh
replay reproduces every geometry output byte for byte.

This completes the geometry/counting part of the
[complete native geometry stage](native_oblique_full_geometry_contract.md).
**No full-path source responses, zero-gradient operator recovery or common-white
reclosure were computed.** The next step is the
[bounded streaming response implementation](native_oblique_full_streaming_contract.md).
The selected-path pilot remains the existing response evidence.

## Coverage and raw evidence

The matrix includes four original polar nodes, two planar orientations, two
independent axial signs, heights 1/20 cm, axial grids 1/2/4 and offset orders
8/16. Only the original physical layout is counted; pilot reflection controls
are not additional native rays. Every original index has multiplicity one in
each of the 192 geometry settings. No short segment, material region, surface,
sign or original record was dropped.

| Quantity, one complete geometry pass | Count |
|---|---:|
| Track/geometry configurations | 2,181,888 |
| Topology intervals, counted separately for each order | 75,386,112 |
| Quadrature chords | 904,633,344 |
| Primitive pieces | 7,855,613,568 |
| Largest chords in one track configuration | 1,264 |
| Largest pieces in one track configuration | 16,320 |
| Rounded-to-endpoint nodes / zero-length pieces | 0 / 0 |

The standalone compiled counter uses no transport or production code. It
retains the literal pilot construction's arithmetic and corner rules, with
fast-math disabled and floating-point contraction disabled. Seven tests cover
nonuniform widths, both signs/orientations, exact corner coincidences,
single-segment tracks, original-index inventory, native critical records,
batch independence and rejected zero axial cosine. Raw volume and individual
incoming/outgoing face arrays match the existing Python construction exactly
in these controls. The complete worst geometry is also independently rebuilt
by that Python construction with exactly matching raw arrays.

All 192 output files retain the complete per-original-track counts and all
local volume/incoming/outgoing face measures, including exact zero faces and
inactive padding. An independent auditor counts pieces by open offset-interval
incidence with internal planes, without constructing any quadrature chords.
Its counts match every original record at both orders.

The largest local error occurs on original path **8561**, polar node **0**,
height **20 cm**, one axial cell, negative axial sign, reversed planar travel
and order **16**. It is the incoming top-face measure of physical segment 7:
actual **0.0016554858959665355**, expected **0.0016554858959634232**. The absolute
difference is about **3.11e-15**. The complete raw witness and reconstruction
are retained; neither the gate nor the original width was adjusted.

## Geometric versus stored normalization

Geometric sums retain `h2*ZMU`, `wei*wzmu/2`, repeated region visits, both
orientations and both independent signs. The accumulator order is original
track, physical segment, then axial cell. Dividing the extruded measure by H
only recovers the original radial measure; it is not a fitted correction.

The largest volume-assembly difference from independently summed original
lengths is **5.31e-16**. Relative differences from the stored native volume and
surface normalizers are **7.44e-8** and **4.36e-8**, respectively. Both ledgers
are preserved separately. These normalizer differences do not justify adding
PJJ completion or modifying the exact companion.

## Complete response cost and next execution gate

Adding groups 51/61/98 and all fourteen original regional/radial coordinates
requires **6,545,664 track/group configurations**, **91,639,296 input evaluations**
and **329,935,769,856 primitive/column updates** per pass. None was solved here.

The frozen conservative scheduling calculation produces 12,335 contiguous
original-index batches, each estimated below 600 seconds and 512 MiB. It uses
the pilot's measured RSS, not its earlier optimistic structural estimate.
Retaining five float64 primitive values for every column/update would take
**13.20 TB per pass**. A proposed aggregate/receipt schema bounds complete
primary-plus-replay output at **72.79 GB**, plus a 1-GiB reserve; current disk
space admits that bound.

Timing still needs a new implementation benchmark. Pooling all observed pilot
work/time gives about **9.3 hours** for primary plus replay. The deliberately
conservative slowest-case schedule gives about **162 days**, because that rate
includes startup on a tiny one-segment path. Neither is a measured run time for
the future worker. The original conservative schedule and both estimates are
preserved; source-response execution remains explicitly unadmitted until a
qualified streaming worker and complete cost estimate exist. Scientific cases
and the original gates remain fixed.

The geometry workers used about three minutes total per pass and remain below
512 MiB/600 seconds per process. The first whole-block audit reached **583 MiB**,
exceeding the cap. Its code, complete outputs and failure status are preserved.
Releasing array views reduced one audit to 466.8 MiB, but its replay still used
578.7 MiB; both outputs are also preserved as an unsuccessful resource fix.
Bounding the temporary comparison arrays to **512 original records** then
reduced primary/replay peaks to **281.5/267.2 MiB**, with exactly the same raw
output and numerical result. Both bounded audits meet the original cap;
no resource limit was raised.

Full replay has **216 byte-identical analysis files** and four byte-identical
audit field/witness files. Primary and replay each pass all seven tests.
Production sources, shared binaries, live D4 inputs and prior sealed evidence
remain unchanged.

## Evidence and scope

- [Frozen plan](../artifacts/native-oblique-full-preflight-20260929/plan.json)
- [Complete geometry/count audit](../artifacts/native-oblique-full-preflight-20260929/preflight/result.json)
- [Cost and original-index batch receipts](../artifacts/native-oblique-full-preflight-20260929/preflight/response_costs_and_batches.json)
- [Separate normalizer ledgers](../artifacts/native-oblique-full-preflight-20260929/preflight/normalizer_ledgers.json)
- [Worst local measure](../artifacts/native-oblique-full-preflight-20260929/preflight/worst_geometry.json)
- [Preserved resource failure](../artifacts/native-oblique-full-preflight-20260929/preflight/resource_limited_audit/status.json)
- [Preserved failed view-release fix](../artifacts/native-oblique-full-preflight-20260929/preflight/resource_limited_view_release_audit/status.json)
- [Final verification](../artifacts/native-oblique-full-preflight-20260929/verification/result.json)
- [Archive and reproduction](../artifacts/native-oblique-full-preflight-20260929/README.md)

The next scientific comparison remains the complete exact zero-gradient
operator, its saved inputs, and then manufactured common-white reclosure.
Physical axial escape, finite-axial source completeness, coupled eigenproblems,
multigroup/fission, POD training and production changes remain outside this
result. The earlier failed native-table partition equality is unchanged.
