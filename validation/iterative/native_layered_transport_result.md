# Layered source and axial vacuum implementation calibration

The layered-source implementation calibration passes, including full replay,
24 independent raw audits and final artifact verification. Actual axial vacuum
entry and escape are verified in this declared calibration. This is not a
whole-native physical-source qualification or a coupled eigenproblem result.

The experiment implements the next part of the
[physical-boundary contract](native_oblique_physical_boundary_contract.md):
independent volume sources in each axial layer, independent radial inflow by
surface and layer, and actual zero incoming axial flux for every physical
volume/radial basis column. It uses the original track lengths, regions and
cross-section values. The previous
[complete zero-gradient result](native_oblique_full_response_result.md) remains
a separate, sealed result.

## Declared coverage

The artifact is
[`native-layered-kernel-20261001`](../artifacts/native-layered-kernel-20261001).
Its implementation and calibration plans freeze the gates before the
scientific runs. The 24 families cover four native polar nodes, heights 1 and
20, and 1, 2 and 4 axial layers. Each family retains groups 51, 61 and 98,
both planar orientations, both independent axial signs, and offset orders
8, 16 and 32.

Each state has `8*Nz` volume, `6*Nz` radial-inflow and eight active axial
boundary-control coordinates, plus two independently swept positive controls.
The axial controls are separate from the physical vacuum columns. No source
coordinate is fitted, merged or discarded.

For each family, the minimum, lower-median and maximum work tracks are chosen
deterministically, with the lowest original index breaking ties. All 864
ranked track/group/direction states have independent rectangle-clipping
references at orders 64 and 96. The largest contiguous 64-record batch in
each family provides additional mapping, conservation and resource evidence.
The union contains 204 distinct original tracks, not all 11,364 tracks.

The primary pass contains 57,888 transport configurations and 2,469,888 input
coordinate evaluations including controls and all three worker orders.
Ten implementation tests cover analytical homogeneous/void
escape, optically thin propagation, every layered coordinate, independent
adaptive integration, reflection, repeated regions, positive mixtures,
constant solutions, primitive witnesses and the manufactured white model.
The prior matched-inflow kernel is compared bit-for-bit on four critical
tracks, all three groups and both previous offset orders. The complete prior
matrix still needs regression through the new worker before a full-native
physical-stage claim.

## Precision failure and correction

The first independent reference used binary64 whole-track offsets. On track
51, polar 3, height 1 and four layers, its order-64/order-96 disagreement
reached `3.55e-13`, above the frozen `2e-13` reference gate. The reference now
clips each cell rectangle using 50-digit decimal coordinates and integrates
within each topology interval. Its flight coefficients use independent
`exprel` and hypergeometric identities.

That more accurate reference exposed a worker error. In group 98 with positive
planar and axial directions, a weak outgoing response was
`9.18139184350186e-9` rather than `9.181391843562663e-9`. The relative error,
`6.62e-12`, exceeded the unchanged `5e-12` field gate even though particle
balance passed. The artifact retains both failed calibration attempts,
their sources, binaries, input identities, results and logs.

Physical-mode geometry now uses 113-bit arithmetic for cumulative vertices,
offsets and intersections. Flight lengths are converted to binary64 after
subtraction; integration measures and all transported values remain binary64.
The exact-characteristic formula and tolerances are unchanged. The separate
matched-inflow regression mode retains the sealed original geometry.
The previously failing family now has maximum order-32 reference error
`6.14e-15`. Boost headers used by the build are frozen in the artifact; a
separate build from those headers is included for reproducibility controls.

The developmental reference estimator failure is also preserved. Its sum of
unrelated vector-component roundoff bounds was resolved by independent
component quadrature, retaining the original accuracy threshold. A failed
initial extraction of vendored header dependencies is recorded separately;
the successful numerical binary was preserved and the complete dependency
closure was subsequently frozen.

## Primary numerical results

| Check | Maximum relative error |
| --- | ---: |
| Independent response, order 8 | 1.141e-14 |
| Independent response, order 16 | 1.120e-14 |
| Independent response, order 32 | 1.186e-14 |
| Independent reference, order 64 versus 96 | 1.328e-14 |
| Primitive balance | 4.380e-16 |
| Cell balance | 1.238e-14 |
| Whole-track balance | 7.950e-15 |
| Geometric measures and constant solution | 7.857e-15 |
| Independently swept positive-control assembly | 1.137e-14 |

Shared-face differences and physical axial incoming flux are exactly zero.
All retained responses are nonnegative. Conservation is checked together with
independent field accuracy; the precision failure demonstrates why a small
balance residual alone is insufficient.

## Independent audit and physical white controls

All 643 scientific files agree byte-for-byte in the complete replay. Ten tests
pass in both runs; the separate frozen-header build passes the same ten tests.
The 24 independent audits reconstruct
source birth, incoming current, collision and outgoing current from the saved
responses and original inputs, check every primitive witness by independent
flight quadrature, and adaptively integrate the worst ranked state in every
family. They also verify byte-exact reconstruction of every response and
witness using structural-zero storage. All 57,888 round trips are byte-exact.
The source coordinates remain recoverable, including inactive coordinates and
their original primitive/cell witness data.

The independent raw-balance maximum is `7.07e-15`; the independent primitive
quadrature maximum is `6.99e-16`. Adaptive references agree with the saved
order-96 references within `1.02e-14`, and their largest reported normalized
error estimate is `1.12e-14`, below the frozen `2e-13` reference gate.

The physical-white checks use a completely specified manufactured
three-chord, six-surface model. They retain all polar/sign/orientation states
and solve `6*Nz` surface/layer amplitudes using actual geometric incoming
measures, with top and bottom vacuum. Eighteen height/layer/absorption cases
include the void escape control, and all pass. The open operator is checked
before white closure. Its independent error is at most `2.94e-15`; closed
fields and currents agree with the independent operator within `1.63e-14`.
The source-minus-collision-minus-axial-escape relative defect is at most
`1.25e-14`, and local white closure is within `4.35e-16`. These checks do not
qualify native white closure or remove its difference from stored native
normalizers.

## Isolation, resources and full execution cost

The final verifier confirms all 997 protected inputs unchanged and validates
all 84,715 manifest entries in 28 prior sealed artifacts. Production source,
shared binaries and live D4 inputs are unchanged. Final evidence is in
[`verification/result.json`](../artifacts/native-layered-kernel-20261001/verification/result.json).
The successful primary/replay/audit pipeline and final verifier use 126
monitored processes. The highest sampled memory is 206.30 MiB; the maximum
recorded calibration-worker peak is 155.61 MiB. Including final verification,
the longest monitored process is 29.01 seconds. Every scientific process uses
one numerical thread, with 512 MiB and 600-second limits and a 1-GiB disk reserve.

The [full execution cost estimate](../artifacts/native-layered-kernel-20261001/verification/full_execution_preflight.json)
counts 3,272,832 track/group/direction states, 139,640,832 coordinate evaluations
including controls, and 1,635,906,401,280 piece/coordinate updates for one full
order-32 open-operator pass. Dense response/witness arrays would occupy
92,669,147,136 bytes per pass. The proposed lossless, batched uncompressed
schema bounds one pass at 36,779,904,000 bytes; primary, replay and a 1-GiB
reserve total 74,633,549,824 bytes, versus 82,129,301,504 bytes free at verification.

The measured kernel-work extrapolation is about 2.95 hours per full pass.
Scaling the entire three-order calibration elapsed time gives a conservative
estimate of about 5.98 hours per pass. These are estimates from the largest
64-record batches, not measured full runs. Complete prior regression,
native operator assembly, white closure and independent audits need additional
counted time and storage. The full physical run has not been admitted or launched.

## Remaining scope

Changing the axial layer count can change both the represented source and the
piecewise-constant white boundary field. This calibration does not claim
continuum axial-grid convergence. A full execution plan must retain every
original track and source coordinate, include the complete prior regression,
and qualify the open physical operator before native white return. Coupled
scattering/fission, POD training, production changes and D4 restarts remain
outside this result. The original tabulated native partition-equality failure
is unchanged.
