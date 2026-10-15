# Native oblique streaming worker: implementation calibration passed

The standalone 16-column worker passes the frozen implementation and resource
checks. It retains all fourteen original regional/radial inputs and adds two
positive controls: an unequal coordinate mixture and the constant angular
solution. It traces actual axial crossings; the independent one-dimensional
flight supplies only matched boundary data and comparison fields.

Calibration covers the minimum, lower-median and maximum work records, choosing
the lowest original index for every tie, and the largest proposed contiguous
512-record batch for every polar/height/grid family. All signs, orientations,
orders and groups remain present. This is implementation/timing evidence, not
the completed full-native operator.

- 24 process families; 296,640 track/group configurations.
- 4,746,240 input evaluations, including the two controls.
- Eight tests per pass; 408 byte-identical replay files.
- Primitive/cell/global balance maxima: 5.03e-16 / 1.40e-14 / 1.28e-14.
- Independent primitive-witness quadrature discrepancy: 1.11e-15.
- Matched point/integral/outgoing-face maxima: 1.29e-14 / 1.30e-14 / 3.31e-13.
- Source assembly maximum: 8.35e-15; shared faces agree exactly.
- All physical basis/control responses remain nonnegative, without clipping.
- Measured maximum process: 8.44 seconds and 189.52 MiB.
- 2,304 weighted volume/Jx batching comparisons across chunk sizes 1, 64, 128,
  256 and 512 differ by at most 2.42e-15 on noncancelling scales.

The complete matrix with controls requires 377,069,451,264 primitive/column
updates per pass. A twofold measured timing margin plus child overhead gives
11,086.5 seconds for full primary plus replay worker processing. Reference
preparation, operator recovery, common-white closure and final audits need
their own allowance in the execution plan; this worker estimate alone is not
the total end-to-end forecast. Full source-response execution remains a separate
admission step. Scientific gates, source coordinates and original paths are
unchanged.

The separate sign-aware action evaluator also recovers all 648 frozen exact
inputs and 201 reclosed cases in three tests before the full native run. The
full run must first calibrate the independent flight on every original track,
then execute every oblique batch, recover all original operator coordinates,
and only then reclose the common white boundary across all polar/sign states.

Evidence: [frozen calibration plan](../artifacts/native-oblique-streaming-20260930/calibration_plan.json),
[raw audit and replay verification](../artifacts/native-oblique-streaming-20260930/verification/result.json),
[measured work costs](../artifacts/native-oblique-streaming-20260930/verification/measured_full_costs.json),
[batch partition check](../artifacts/native-oblique-streaming-20260930/verification/batch_partition_check.json).
The 997 protected files, 26 prior seals and their 68,916 entries remain unchanged.
Physical axial escape, coupled eigenproblems, POD and production changes are
not admitted by this calibration.
