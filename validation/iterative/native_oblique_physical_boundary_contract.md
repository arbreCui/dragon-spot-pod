# Next experiment: physical axial boundaries with complete layered sources

This is a design contract, not execution admission or a result. Its prerequisite
is successful full replay and independent qualification of the
[complete zero-gradient response](native_oblique_full_response_result.md).
It advances the actual transport model beyond a manufactured invariant
subspace. Do not launch another zero-gradient-only path subset as a substitute.

## Model and source coordinates

Keep the original track fixture, repeated-region map, physical lengths,
cross-section precision, native polar/moment factors and two independent axial
signs. Continue using the qualified exact-characteristic primitive. Do not
claim equality to the distinct tabulated native kernel, or introduce PJJ
completion. Keep this implementation isolated from production and live D4.

For each retained angular state and an axial grid of Nz cells, retain every
regional/axial source coordinate q[r,j], r=0..7, j=0..Nz-1. Incoming radial data
must also resolve all six physical radial surfaces and all Nz axial intervals.
There are 8*Nz volume and 6*Nz radial-inflow coordinates per state. Distinct
regions, layers, polar nodes and signs cannot share one fitted source value.

Set actual incoming top and bottom data to zero for the physical vacuum runs.
A ray entering through an axial face then starts from zero, independent of the
one-dimensional radial companion. A ray entering radially uses its surface
and actual axial interval. Propagate through every subsequent intersection.
There must be no manufactured exact-flight injection at axial entries.

Keep separate axial-boundary input coordinates for control tests: for a fixed
axial sign only its entering top or bottom face is active, with eight regional
coordinates. They enable isolated boundary responses and a constant-solution
control with q[r,j]=Sigma[r] and all incoming angular values equal to one.
The physical vacuum runs set these coordinates identically to zero.

## Open boundaries before white return

First qualify the full open-boundary action. Retain regional/layer angular
integrals, radial outgoing current by surface/layer, top/bottom outgoing
current by region, source birth, collision and raw balance. Preserve incoming
and outgoing current separately. Top and bottom currents use their actual
normal cosine and offset measure; neither a net-current relative error nor
scalar mean recovery can replace these fields.

The physical radial white boundary is local to each axial interval. Mix every
polar node and both axial signs at each physical radial surface and interval;
do not average distant axial intervals into a six-number return. The return
unknown therefore has 6*Nz coordinates. Axial faces remain vacuum and do not
participate in the radial white solve.

Normalize this physical return by the incoming current measure computed from
the same discrete geometric rays and interval. This makes its conservation
identity explicit. The earlier zero-gradient companion uses stored native
surface normalizers, which differ slightly from geometric measures; retain a
separate stored-normalizer comparison and report the resulting boundary-model
change. Do not fit either measure to match a flux. Flux reporting with stored
native volume normalizers must likewise remain separate from raw geometric
collision and particle-balance ledgers.

Only admit white return after the open action is positive and independently
verified on every source coordinate in the admitted matrix. Verify the return
matrix, invertibility, nonnegative inverse/responses, solve residual and local
surface/layer closure. Include axial escape in the total particle balance.
Zero absorption with reflecting radial surfaces is a useful escape control;
do not assume a closed all-reflecting zero-absorption problem is invertible.

## Independent accuracy and implementation controls

Calibrate the new layered-source worker before freezing a full execution plan.
Required controls include void and optically thin primitives, isolated volume
and boundary sources, unequal positive mixtures, exact constant solution with
non-vacuum control inflow, sign reversal, axial reflection, repeated regions,
and exact matching on every shared face. Restore the entire prior manufactured
zero-gradient action as a regression test with its original matched inflow.

Check selected full traces with a separate literal recurrence and independent
integration of offset-dependent cell and face responses. Refine offset
quadrature on fixed topology and a fixed source field before interpreting any
axial-grid comparison. For a piecewise-constant layered source, ray crossing
and the segment solution are exact up to offset integration and roundoff;
changing Nz also changes the represented source unless the same profile is
explicitly prolonged. Distinguish these two effects.

The layer-local white return uses a piecewise-constant incoming field within
each axial interval. Refining Nz therefore changes its boundary approximation
even when the volume source is exactly prolonged. Keep the underlying physical
problem fixed and measure volume-source and boundary-approximation errors
separately. Exact segment propagation alone does not remove either error.

Use analytical void/homogeneous manufactured fields and independent scalar
quadrature wherever available. For nonuniform cases without a closed form,
retain a separate higher-accuracy integration reference with its own verified
error estimate. Agreement between two consecutive axial grids is insufficient.
Report errors on positive/induced scales, absolute defects for exact-zero
controls, and every failed comparison. Freeze tolerances and reference
accuracy before the physical calculation; do not relax the existing gates to
accept an unmeasured discretization error.

## Complete-matrix admission and limits

A small implementation calibration is allowed only as implementation evidence.
Before any whole-geometry claim, count all original tracks and all selected
groups, angles, signs, heights, grids, source columns and offset orders.
Publish the resulting process schedule, raw-witness schema, full primary and
replay storage bounds, and measured end-to-end cost. Retain one numerical
thread, 512 MiB and 600 seconds per process, with live own-child monitoring and
at least 1 GiB free storage. Redesign batching rather than dropping coordinates
or counting a pilot as full-native coverage.

Passing would qualify a fixed-source transport/physical-boundary reference for
the declared discretization and groups. It would still not admit coupled
scattering/fission eigenproblems, an axial closure inferred uniquely from
scalar data, POD training, a production solver change or a running D4 restart.
