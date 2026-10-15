# Selected native oblique tracks: pilot qualified

The full declared matrix, independent replay and raw-field audit pass.

The oblique-cell construction now recovers original native paths, including
repeated visits to the same material region. All **16,896 configurations**
and **931,584 independent cell/boundary unit responses** pass the declared
gates. At order 16, the largest whole-track integral and radial
outgoing recovery differences from the frozen exact radial companion are
**2.53e-15** and **3.45e-15**, respectively, on the predeclared scales.

This is qualification of the selected paths and their explicit source mapping.
It is not whole-native geometry, common radial white return with physical
axial escape, native mesh convergence, or a coupled eigenreference.

## Evidence and selection

- [Original native-path contract](native_oblique_track_pilot_contract.md)
- [Separate compact-storage contract](native_oblique_track_compact_contract.md)
- [Original storage-blocked preflight](../artifacts/native-oblique-track-pilot-20260929/README.md)
- [Original-path inventory and selection](../artifacts/native-oblique-track-pilot-compact-20260929/preflight/selection.json)
- [Frozen compact plan](../artifacts/native-oblique-track-pilot-compact-20260929/plan.json)
- [Primary numerical summary](../artifacts/native-oblique-track-pilot-compact-20260929/analysis/result.json)
- [Final verification](../artifacts/native-oblique-track-pilot-compact-20260929/verification.json)
- [Archive schema and reproduction](../artifacts/native-oblique-track-pilot-compact-20260929/README.md)
- [Next complete-geometry contract](native_oblique_full_geometry_contract.md)

The inventory retains all 11,364 original planar paths. Selection takes the
minimum, lower-median value and maximum of each declared ordering, choosing
the lowest original zero-based index at every value tie. Multiplication by
each fixed positive ZMU does not change length/optical rankings.

| Ordering | Minimum path | Lower-median path | Maximum path |
|---|---:|---:|---:|
| Physical path length | 7575 | 6245 | 7398 |
| Interior segment count | 0 | 23 | 43 |
| Group-51 optical length | 7575 | 7747 | 5968 |
| Group-61 optical length | 7575 | 4791 | 5968 |
| Group-98 optical length | 7575 | 5888 | 4009 |

After deduplication there are eleven paths: 0, 23, 43, 4009, 4791, 5888,
5968, 6245, 7398, 7575 and 7747. They contain 1 to 15 original segments and
cover all eight material regions and six radial surfaces. This is deterministic
structural coverage, not a random sample or an error bound for untested paths.
No response was used to select or replace a path.

The matrix retains all four original polar factors, both independent axial
signs, both planar orientations, and a separately reflected physical layout.
The reflected layout is a symmetry control, not another native quadrature
weight. Groups are 51/61/98, heights are 1/20 cm, axial grids are 1/2/4/8,
and offset orders are 8/16. There are 352 separately bounded processes.

## Native source coordinates and exact matched recovery

Every original segment and material-region label is retained. Lengths are
the original `h2*ZMU`; the signed axial factor is `+/-sqrt(1-1/ZMU^2)` and
does not change when planar travel reverses. Native total-cross-section
precision, `wei*wzmu/2` half weights and planar moment factors remain fixed.

Each configuration sweeps every physical segment/axial-cell unit source,
every incoming radial-face unit and every incoming axial segment unit.
Additional inputs are the constant solution, a regional-weighted alternating
axial source, and all fourteen original regional-source/radial-surface inputs
with independent matched axial inflow. There are **1,201,920 input evaluations**
in total. Runtime batches of sixteen columns retain the complete input space.

The explicit source map has one row per physical segment/axial cell and
one column per original region/axial cell. Repeated region visits contribute
to the same original region but remain distinct geometric segments. Assembly
of the full unit response recovers independently swept constant and nonuniform
regional controls. Its maximum discrepancy is **6.75e-15**.

The one-dimensional native-path reference obtains B/D by independent scalar
quadrature and propagates original source/surface coordinates literally.
Its largest difference from the previously frozen exact whole-track action
is **5.37e-16**, below the 5e-12 calibration gate. This compares with the exact
companion; it does not reinstate equality with the distinct native table kernel.
No native PJJ completion is inserted.

The axial inflow is the independent exact 1D angular field at each actual
chord entry. It manufactures a zero axial gradient while allowing real axial
cell crossings. It is neither vacuum nor periodic top/bottom closure.

All following entries are relative fractions on the predeclared positive
reference scales. Matched cell/face comparisons use a per-input maximum
positive response; the frozen whole-track comparison uses the maximum over
the original fourteen-coordinate reference. Exactly zero reference responses
must remain exactly zero.

| Offset order | Matched cell-integral error | Matched face-current error | Frozen whole-track integral recovery | Frozen radial outgoing recovery |
|---:|---:|---:|---:|---:|
| 8 | 1.09834e-14 | 1.38802e-14 | 2.96292e-15 | 2.50456e-15 |
| 16 | 1.20926e-14 | 1.36049e-14 | 2.53049e-15 | 3.44585e-15 |

The pointwise matched endpoint error is at most **1.56e-14**. These very small
differences establish the declared recovery controls; they are not general
heterogeneous finite-axial true-error bounds. The largest alternating-source
8-to-16 changes are 4.68e-15 for integrated response and 3.60e-15 for current,
on their declared maximum-response scales. No mesh-convergence conclusion is
drawn from those last-pair changes.

## Positivity, geometry and conservation

| Check across both quadrature orders | Largest relative defect | Frozen gate |
|---|---:|---:|
| Original segment length representation | 6.65e-15 | 5e-12 |
| Geometric cell/face measures | 1.69518e-12 | 5e-12 |
| Constant angular solution | 1.69530e-12 | 5e-12 |
| Planar/axial reflection | 1.71011e-12 | 5e-12 |
| Shared-face matching | exactly zero | 5e-12 |
| Primitive balance | 5.95e-16 | 1e-10 |
| Cell balance | 2.19e-14 | 1e-10 |
| Primary global balance | 2.11e-14 | 1e-10 |

All intermediate angular amplitudes, integrals and face currents are
nonnegative. All 16,896 reflection comparisons pass. Nothing is clipped or
rebalanced. Each source column retains its worst actual primitive witness
and minimum amplitude/integral over the complete traversal.

The largest measure defect is an axial entry-face measure on path 43,
polar 0, H=20 cm: the expected measure is 0.0019210359481857486 and its
absolute discrepancy is about 3.26e-15. The small face measure explains why
the relative geometry error is larger than the whole-track response errors.
It still passes the frozen 5e-12 gate; the measure is not fitted or repaired.
Full-native admission must continue checking every such local measure.

Weighted regional integrals and Jx/Jz contributions reconstruct from the
complete physical-segment response and original angular weights. Stored
whole-native normalizers remain a separate input ledger. Selected tracks are
never rescaled to match those full-native volumes or surfaces.

## Storage, reproduction and resource bounds

The first preflight passed its memory/time estimates but proposed a
26.42-GiB primary diagnostic expansion when the shared volume had about
5.8 GiB free. It is sealed as storage-blocked, with its inputs, source and
ten passing candidate tests; no native response matrix ran there.

The separately declared compact continuation preserves the entire scientific
matrix and every gate. Its primary uncompressed storage bound is 3.94 GiB,
plus at most 34.75 MiB for a fresh replay batch, copied inputs, metadata and
a 1-GiB free-space reserve. Later free-space readings increased; the compact
plan and its reserve remained unchanged. This task performed no unrelated
file cleanup.

Every cell-integrated response and physical face current is saved. Shared
faces are stored once only after exact reconstruction of both original
ledgers succeeds. Geometry retains exact float64 endpoints and checked integer
indices. Full primitive trace tensors are reconstructible from frozen inputs
and source; the compact archive instead retains per-input extrema and complete
worst witnesses. This diagnostic choice does not remove any transport inputs.

The independent replay compares every process output byte for byte, writes
hash/size receipts, and only then discards that process's duplicate temporary
NPZ files. Primary fields, replay result JSON files, logs and resources remain.
All **39,777 analysis files match byte for byte** across the complete replay;
352 receipts retain their hashes and sizes. Twelve new pilot/packing tests,
eight strip tests and eleven existing characteristic tests pass from maintained,
archived and replay source: **31 tests** in each environment. The audit checks
5,632 geometries, 596,992 numeric arrays, the complete native selection and
baseline mapping, 997 protected files and 25,475 sealed entries in 24 earlier
artifacts. No old artifact is changed.

Each input's worst actual primitive is independently checked using scalar
quadrature; its largest outgoing/integrated discrepancy is **7.30e-16** on
the declared input scales. Independently reconstructed cell and global
balance defects are 2.19e-14 and 2.11e-14. Every original region/axial input
coordinate, exact shared face and native angular weight is audited.

The primary analysis occupies **470,923,279 bytes**. Numerical processes peak
at **336.11 MiB** over primary and replay, and the longest takes **8.31 seconds**,
within the fixed 512-MiB/600-second caps. The final audit takes 79.15 seconds
and peaks at 379.72 MiB. The initial 215.98-MiB numerical memory estimate was
too low; actual monitored peaks, rather than that estimate, establish resource
admission. No cap was relaxed. Full primary/replay numerical elapsed sums
are 711.57/698.62 seconds, excluding launcher and receipt overhead; these are
selected-pilot timings, not a full-native performance estimate.

## Next step

The [complete-native geometry contract](native_oblique_full_geometry_contract.md)
requires all 11,364 paths, an explicit full-work cost preflight, accountable
original-index coverage, independent geometric measures, and recovery of the
complete exact radial operator in the manufactured zero-gradient subspace.
It then checks common-white recovery within that same subspace. Physical
axial escape and a general finite-axial source operator remain later gates.

Production sources, shared builds and running D4 inputs were not changed.
