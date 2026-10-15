# Oblique strip geometry: manufactured prototype qualified

Actual radial/axial cell crossings now pass the frozen geometry experiment.
Across 5,760 material/direction/quadrature configurations, all 101,632
independent cell-source and incoming-boundary unit responses are nonnegative.
At order 16, the maximum independent analytic cell-mean error is **3.89e-15**
relative and the maximum outward face-current error is **1.11e-14**.
All shared-face contributions match exactly between neighboring cells.

This qualifies the manufactured strip prototype. It does not yet qualify
the original native tracks, common radial white return with axial crossings,
finite-axial-mesh convergence, or a coupled eigenreference.

## Evidence and scope

- [Frozen geometry contract](oblique_strip_geometry_contract.md)
- [Predeclared finite matrix and gates](../artifacts/oblique-strip-geometry-20260929/plan.json)
- [Numeric summary and worst-case identities](../artifacts/oblique-strip-geometry-20260929/analysis/result.json)
- [Independent verification](../artifacts/oblique-strip-geometry-20260929/verification.json)
- [Artifact schema and reproduction](../artifacts/oblique-strip-geometry-20260929/README.md)
- [Preceding complete radial flight](exact_native_flight_result.md)
- [Next native-track pilot contract](native_oblique_track_pilot_contract.md)

The matrix uses lengths 1/3 cm, heights 1/20 cm, 1/2/4/8/16 axial cells,
both planar orientations, axial directions +/-1/sqrt(3), and an explicit
zero-axial-direction limit. One radial cell uses totals 0, 0.02, 0.2 and 2
per cm. Two equal radial cells use those four homogeneous controls and
the ordered pairs (0.2,2), (0,2), (2,0), and (2,0.2).

Every configuration keeps the full physical cell-source basis, one incoming
radial-face unit per axial cell, and, for nonzero axial direction, one
incoming axial-face unit per radial cell. Four additional inputs test the
constant solution, uniform vacuum source, matched one-dimensional inflow,
and alternating 0/1 axial source. There are **124,672 input evaluations**
in total. No source coordinates are truncated or fitted.

## Geometry and independent reference

For each signed characteristic, `u=z-mu*s` is constant. The offset interval
is split at every `u=z_j-mu*s_k`, so its topology is fixed within each
quadrature interval. Positive Gauss-Legendre rules of orders 2, 4, 8 and 16
integrate those intervals. Every chord is split at its actual material and
axial-plane crossings. The exact exponential T/B/D coefficients propagate
one angular amplitude across each shared face.

Volume contributions use `du*integral(psi ds)`. Radial face currents use
`du=dz`; axial currents use `abs(du)=abs(mu)*ds`. The experiment uses unit
strip weight. No native normalization factor, fitted volume or flux repair
is inserted. Per-cell source birth uses the independently known rectangular
area, so geometry errors cannot disappear into a fitted source measure.

For homogeneous vacuum source q=1, the Cartesian reference is
`psi=F(min(s,z/abs(mu)))`, with reflected z for negative mu, where
`F(l)=(1-exp(-sigma*l))/sigma` and the void limit is l. Independent Cartesian
integrals split at `z=abs(mu)*s`; they do not reuse candidate chord nodes or
weights. Unit tests additionally check the unit-square void volume 1/3,
each outgoing face current 1/2, and an independently integrated absorbing
square tail distribution.

The matched control supplies axial inflow from a direct one-dimensional
piecewise-material flight with incoming value 0.4 and physical radial
sources [1] or [1,0.3]. Pointwise incoming/outgoing recovery is tested at
every quadrature order. Its quadrature-dependent cell and face integrals
are gated at order 16, as declared in the run plan before computation.
This is manufactured inflow, not vacuum or periodic axial closure.

## Conservation does not establish integration accuracy

All entries below are relative fractions, not percentages. The analytic
errors compare each cell or outgoing face with its own positive independent
reference response; exactly zero reference currents must remain exactly zero.

| Offset quadrature order | Largest analytic cell-mean error | Largest analytic face-current error | Largest matched-1D integral error | Largest matched-1D face-current error |
|---:|---:|---:|---:|---:|
| 2 | 6.45610e-3 | 2.53618e-2 | 2.45902e-3 | 1.13593e-2 |
| 4 | 1.78902e-5 | 7.02790e-5 | 5.16844e-7 | 1.21220e-5 |
| 8 | 8.24161e-13 | 3.23959e-12 | 2.70803e-15 | 5.59070e-13 |
| 16 | 3.88764e-15 | 1.11305e-14 | 2.80541e-15 | 1.37114e-14 |

Order 2 has up to **0.646% cell-mean error and 2.536% face-current error**
while retaining near-roundoff balance and exact shared-face matching.
Thus positivity and conservation alone still cannot admit a reference.
All predeclared order-16 analytic errors pass the 1e-8 gate; matched-1D
integrated errors pass the separate 5e-12 gate. No higher quadrature order
or relaxed tolerance was introduced after observing results.

Across all orders, the largest matched pointwise error is 1.25e-15.
The alternating heterogeneous source's largest 8-to-16 change is 1.52e-15
for integrated response and 1.75e-15 for face current, on the declared
maximum-response scales. Those are quadrature diagnostics; they are not
independent heterogeneous true-error bounds or axial mesh-convergence claims.

## Geometry, positivity and raw ledgers

| Check, over every applicable configuration | Largest relative defect | Frozen gate |
|---|---:|---:|
| Cell volume and face measures | 6.73e-15 | 5e-12 |
| Constant angular solution | 6.73e-15 | 5e-12 |
| Planar/axial reflection | 2.39e-14 | 5e-12 |
| Shared-face continuity | exactly zero | 5e-12 |
| Exact primitive balance | 4.07e-16 | 1e-10 |
| Cell balance | 6.84e-15 | 1e-10 |
| Independently assembled global balance | 2.52e-15 | 1e-10 |

All intermediate amplitudes, integrated responses and currents are
nonnegative, including void-containing profiles. No clipping is applied.
All 4,800 reflection comparisons pass. Axial reflection permutes physical
source cells and radial inflow pieces; planar reflection also reverses
material order. The asymmetric matched-1D source is tested independently
rather than incorrectly treated as invariant under planar reflection.

Source, incoming current, outgoing current and absorption are retained for
every cell and input. Primitive records retain coefficients, intermediate
minima, and the largest normalized signed defect with its input identity and
scale. Complete primitive states can be reconstructed from the archived
geometry, source coordinates and inflows. No global balance multiplier or
postprocessing correction is used.

## Reproduction and resource bounds

Eight new geometry tests and eleven existing characteristic tests pass from
maintained, archived and fresh-replay source. The fresh replay starts from
real copied inputs and source snapshots. All **8,181 analysis files match
byte for byte**. Verification audits 960 geometry files, 175,680 numeric
arrays, 997 protected files, and 8,886 sealed entries in 22 earlier artifacts.

The largest measured process memory is **138.83 MiB** and the longest
numerical process takes **3.25 seconds**, within the frozen single-thread,
512-MiB and 600-second per-process limits. Resource telemetry is separate
from deterministic results. These are small-prototype timings, not a native
full-track performance estimate.

Two launch issues are preserved under `runs`: the sandbox initially denied
the process-memory monitor, and the first archived dependency test lacked
an unchanged transitive import. The authorized monitor and copied dependency
resolved them before numerical matrix execution. No numerical equations,
case selections or gates were changed. The completed matrix has no failed
scientific or resource gates.

## Next step

The [native-track pilot](native_oblique_track_pilot_contract.md) starts with
an inventory and cost estimate on the existing sealed native rays, followed
by a deterministically selected, bounded path sample. It must preserve
original segment lengths, material labels, polar factors and ray weights,
and recover the qualified exact radial flight under matched axial inflow.
Whole-native geometry aggregation and common white return remain subsequent
gates; a selected-ray success cannot qualify them.

Production code, shared libraries and live D4 inputs remain unchanged.
