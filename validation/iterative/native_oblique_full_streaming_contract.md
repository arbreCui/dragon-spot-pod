# Full zero-gradient response: bounded streaming implementation

This continues the [complete native geometry contract](native_oblique_full_geometry_contract.md)
after the [full-path geometry and cost preflight](native_oblique_full_preflight_result.md).
The geometry inventory is complete. No full-track source response or common-white
reclosure was solved in the preflight.

## Preserve the scientific matrix

Retain all 11,364 original tracks, four polar nodes, both planar orientations,
both independent axial signs, heights 1/20 cm, grids 1/2/4, orders 8/16 and
groups 51/61/98. Physical reflection controls are not additional native rays.
There are 6,545,664 track/group configurations, 91,639,296 original-coordinate
evaluations and 329,935,769,856 primitive/column updates in one complete pass.
Keep all eight regional and six radial incoming coordinates per angular state.
These are the zero-gradient manufactured inputs defined in the parent contract.

Do not reduce the track set, energy groups, source coordinates or sign states
to meet an execution budget. Do not replace the oblique sweep by its exact
one-dimensional reference. Use the latter only to construct axial inflow and
to check the independently propagated oblique solution.

## Implementation and resource admission

Build a standalone streaming worker and qualify it against the existing
literal pilot recurrence, source maps, coefficient controls and independent
one-dimensional reference. Any compiled acceleration must use ordinary
double precision, disable fast-math/reassociation, preserve deterministic
ties and report differences on the original gates. Do not use shared builds,
production sources or live D4 inputs.

Use the complete preflight counts to size batches. Freeze a new execution plan
after an explicit performance calibration of the implementation. Calibration
must cover the smallest, median-work and maximum-work records plus the largest
planned batch for every height/grid family. These are timing and implementation
checks, not substitutes for the full scientific matrix. Keep every calibration
case and all failed results. Reuse none of its partial output as a claimed full
operator unless its exact original-index multiplicity is recorded.

The earlier conservative schedule is retained in the preflight. Its slowest
pilot rate includes startup on a one-segment path and produces an extremely
loose 162-day primary-plus-replay estimate. The pooled pilot extrapolation is
about 9.3 hours, but is not a benchmark of the new worker. Neither is sufficient
to launch an unimplemented response calculation. Measure actual worker and
serialization costs and publish the complete primary-plus-replay estimate.
The geometry-only scan itself takes about three minutes per pass.

Retain one numerical thread, 512 MiB and 600 seconds per process, with a live
watchdog. Budget the original fixture, accumulator arrays, temporary copies,
compression and allocator retention. The first whole-block geometry audit used
583 MiB. Merely releasing views still used 578.7 MiB on replay; both failed
approaches are preserved. A 512-record temporary-array bound reduced the final
audit's primary/replay peaks to 281.5/267.2 MiB. Do not infer memory solely from
array payload or the earlier pilot's 336.1 MiB peak.
Benchmark the final audit as well as the transport worker.

Preserve at least 1 GiB free disk. The preflight's complete two-pass response
output bound is 72,787,689,472 bytes, based on at most 32 float64 values per
source coordinate/track configuration and 1 MiB per scheduled aggregate batch.
This is a proposed schema bound, not measured response output. Revise it before
execution if the actual schema or batch schedule needs more space. Full
five-value primitive traces would require about 13.2 TB per pass and must be
regenerated on demand from original indices and archived code.

## Audit and comparison

Retain complete original-index receipts, source coordinates, raw directional
regional sums, radial outgoing currents, per-input minima and worst primitive
witnesses. Save the primitive incoming/outgoing/integral/defect/scale together
with enough geometry coordinates to independently reproduce each witness.
Keep raw cell/global balance and source-assembly checks before aggregation.
Declare the complete-track summation order. Verify that batching preserves the
same operator on noncancelling scales and never merges independent angular inputs.

Keep geometric volume/current measures separate from native stored normalizers.
The preflight measured their relative differences as approximately 7.44e-8 and
4.36e-8; do not fit those differences away or add native PJJ completion.

Recover the complete frozen exact directional operator, all 216 saved inputs
per group, and phi/Jx/Jz on the parent contract's induced-current scales. Only
after complete recovery passes may all polar nodes and both signs be mixed in
the six-surface common-white closure and the 67 saved reclosed cases per group.
Retain order-8 errors; gate quadrature-dependent assembled fields at order 16.
Keep every grid compared with the same independent zero-gradient reference.

Repeat the complete matrix from fresh copies, verify full numeric output and
all original-index receipts, and retain byte/hash evidence. Only verified
duplicate replay files may be discarded. Passing qualifies the manufactured
zero-gradient operator and its white algebra. Physical axial escape, the full
regional/axial source space, coupled scattering/fission/eigenproblems and POD
remain later stages; the failed native-table partition equality is unchanged.
