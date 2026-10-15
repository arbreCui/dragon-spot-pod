# Exact-kernel full flight: zero-gradient companion qualified

The exact-exponential companion now passes the frozen complete-flight checks
for groups 51, 61 and 98, including common radial white return. Its largest
volume-weighted scalar change from the native table kernel is **2.48802 ppm
(0.000248802%)** at fixed input. After each kernel solves its own common white
boundary, the largest scalar difference is **1.19427 ppm (0.000119427%)**.
Reclosing the exact boundary adds at most 0.03981 ppm to the scalar change.

These are measured kernel differences on the specified zero-gradient
prescribed-source problem, not new physical-accuracy tolerances. The exact
companion is qualified as a separate operator. Original native partition
invariance, finite-axial-mesh convergence and the coupled eigenreference
remain unqualified. Actual oblique axial crossings are the next experiment.

## Evidence and scope

- [Frozen full-flight contract](exact_native_flight_contract.md)
- [Predeclared run plan](../artifacts/exact-native-flight-20260929/plan.json)
- [Numeric summary](../artifacts/exact-native-flight-20260929/analysis/result.json)
- [Verification](../artifacts/exact-native-flight-20260929/verification.json)
- [Artifact and reproduction](../artifacts/exact-native-flight-20260929/README.md)
- [Preceding native partition failure](native_segment_composition_result.md)
- [Next oblique-strip geometry contract](oblique_strip_geometry_contract.md)

All original ray paths, eight regions, six surfaces, four polar nodes, total
cross-section precision, physical lengths `h2*ZMU` and native normalization
weights remain fixed. Planar orientation and axial sign are independent.
There are 216 saved source/inflow pairs per group, including 214 nonnegative
inputs, two signed inputs, and the explicitly different separate-sign return
controls. All 648 original input pairs are retained.

The complete regional-source/surface-input basis has 8+6 coordinates for
each polar node and axial sign. Both planar orientations are swept explicitly.
This is the full input space of the frozen interface, with no source or
spatial truncation. The same Green action evaluates all saved inputs and
the newly reclosed cases. Nonnegative intermediate states for every unit
coordinate certify nonnegative responses to every nonnegative input; the
evaluated angular fields are also checked directly.

The fixed inputs are evaluated with the native unsplit kernel and the exact
kernel on whole, 2-/4-/8-piece and 1/3+2/3 segment partitions. Each of the
18 group/kernel/partition processes also recloses 64 directional volume-unit
sources and three paired source profiles through one common white boundary.
There are 3,240 exact fixed-input evaluations, 1,005 exact reclosed positive
evaluations, and 3,396 fixed/white comparisons against the unsplit exact flight.

## Native recovery and source isolation

The new full-coordinate action recovers the saved native half-sign/polar
integrals, isolated/own-source contributions, boundary outputs, scalar flux
and Jz. Including the 93 original P0 completed cases and reconstructed native
white inflows, the largest recovery defect is **5.57e-14**, below the fixed
5e-12 gate.

Splitting an original segment does not redefine its isolated/own-source
ledger: incoming attenuation and source generated within that original
segment are propagated separately through its pieces. Their sum equals the
actual integrated angular response. Small-fixture tests independently compare
all partitions against literal source flights with quadrature-derived B/D.

The original native PJJ completion is preserved only on its existing legacy
P0 cases. It is not inserted into the exact companion. Saved fields separate
the exact-minus-raw-native change, the native PJJ completion and the change
from completed native P0. Across the 31 legacy cases per group, the PJJ
completion contributes at most 0.03161 ppm on the declared weighted scale;
the largest exact-versus-completed-native legacy change is 2.18414 ppm.

## Fixed-input and common-white changes

All table entries are ppm relative to the declared source-induced response
scale (one ppm is 1e-6 relative). Scalar and outgoing-current comparisons use
native volume/surface weighted L2 norms. The worst scalar cases below are
nonnegative source-unit inputs, so their induced scalar scale is the actual
reference scalar response.

| Group | Fixed-input scalar | Reclosed white scalar | Scalar change from reclosure alone | Fixed-input outgoing current | Reclosed white outgoing current |
|---:|---:|---:|---:|---:|---:|
| 51 | 1.79855 | 0.452250 | 0.0391689 | 0.107564 | 0.0507207 |
| 61 | 1.91283 | 0.568830 | 0.0398102 | 0.108323 | 0.0551314 |
| 98 | 2.48802 | 1.19427 | 0.0319522 | 0.109199 | 0.139784 |

The largest individual-region scalar difference is 3.15333 ppm at fixed input
and 1.97063 ppm after common-white reclosure. The summary identifies the group,
input index and source label for each maximum. These componentwise values are
kept separate from the weighted norms in the table.

Jx uses the previously extracted native planar x harmonic and planar travel
sign. Jz uses the independent axial signs and `sqrt(1-1/ZMU^2)`. Both moments
come from retained directional integrals. To avoid dividing by cancellation,
current recovery gates use the absolute directional-current response to the
absolute input. Ordinary net-current relative errors are also reported when
the net-current norm exceeds 1e-10 of that induced scale; otherwise they are
marked unavailable rather than shown as zero accuracy error.

| Group | Fixed Jx change / induced scale (ppm) | Fixed Jz change / induced scale (ppm) | White Jz change / induced scale (ppm) |
|---:|---:|---:|---:|
| 51 | 0.0956697 | 1.79855 | 0.750920 |
| 61 | 0.0899108 | 1.91283 | 0.908964 |
| 98 | 0.0719522 | 2.48802 | 1.64568 |

The largest valid weighted net-Jz difference is 2.48802 ppm at fixed input
or common white return. Reclosing the boundary changes Jz only at roundoff
on the induced scale, consistent with a common return that mixes axial signs.
Separate-sign return remains a named different-model input control and is
never substituted for the common boundary.

## Gates, conservation and measures

All exact whole-flight partitions recover outgoing/integrated angular fields,
scalar flux and both current moments. The largest weighted/component
source-induced partition defect is **8.61e-16**, below the fixed 5e-12 gate.

| Check | Largest measured defect | Frozen limit |
|---|---:|---:|
| Native full-action recovery, including P0 | 5.57e-14 | 5e-12 |
| Exact partition recovery on induced scale | 8.61e-16 | 5e-12 |
| Exact piece balance | 4.74e-16 | 1e-10 |
| Exact whole-track balance | 4.50e-15 | 1e-10 |
| Independently aggregated exact basis balance | 2.34e-14 | 1e-10 |
| White inverse identity | 4.44e-16 | 5e-12 |
| White solve residual | 1.69e-15 | 5e-12 |
| White outgoing/incoming closure | 6.27e-16 | 5e-12 |

All unit-coordinate intermediate amplitudes/integrals and all nonnegative
fixed/reclosed responses remain nonnegative. The full common-boundary inverse
has no negative entries; its minimum over this experiment is 0.144924.
The six signed inputs retain signed negative responses. No clipping or
balancing multiplier is applied.

Geometric even/odd global balance defects are at most 2.20e-14 for fixed
inputs and 1.35e-14 for white inputs. These ledgers include actual geometric
incoming and outgoing measures. They do not assert that stored native surface
normalizers exactly equal their quadrature measures. Stored-white net current
is at roundoff, while the geometric incoming-minus-outgoing difference reaches
1.44e-7 in amplitude units. Both are retained. Diagnostic stored-normalizer
source ledgers preserve the measured polar proportions; they do not modify
the transport calculation.

## Reproduction and limits

Eight new independent mathematical tests and eight prior signed-state tests
pass from maintained, archived and fresh-replay source. The replay evaluates
the entire case matrix from real copied inputs in a fresh directory. All
**88 analysis files match byte for byte**; verification checks 2,487 numeric
arrays, 997 protected files, 44 copied-input hashes and 8,563 sealed-file
entries from 21 preceding artifacts.

Primary processes peak at 271.27 MiB; replay peaks at 287.84 MiB. The longest
process takes 2.13 seconds, within the frozen 512-MiB/600-second per-process
limits. Full-coordinate response reuse accounts for this small cost; it is
not a production benchmark or a reduced transport approximation.

The first native process completed its numerical fields but failed while
serializing a NumPy boolean into JSON. Its source, log, truncated JSON and
fields are preserved under `runs/initial_json_serialization`. Converting that
flag to a Python boolean fixed output serialization. All 76 previously saved
arrays match the completed rerun exactly; no mathematical rule or tolerance
changed. No physics or resource gate failed in the completed experiment.

## Next step

The [oblique-strip contract](oblique_strip_geometry_contract.md) now specifies
actual radial/axial intersection geometry, positive quadrature over incoming
chords, source-cell mapping, shared-face current and independent analytic
controls. It starts with manufactured one-/two-material strips before a
native-track bridge. This moves beyond algebraic segment subdivisions while
keeping geometric error separate from the measured kernel change.

The current success remains a zero-gradient full-flight qualification.
Production files, shared libraries and running D4 inputs were not changed.
