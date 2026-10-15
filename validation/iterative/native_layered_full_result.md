# Full native layered-source operator and geometric white qualification

The full physical-source fixed-source operator, native layer-local geometric
white return and complete previous zero-gradient regression pass. All 2,191
scheduled jobs have successful watchdog receipts, including final verification.
The resumed scheduler completed its final job at 2026-10-03 06:10:58 China time
and exited. The artifact is sealed and every manifest entry has been
independently read and verified.

This result qualifies the declared groups and discretizations on all original
tracks. It does not qualify a coupled scattering/fission eigenproblem, POD,
continuum axial convergence or a production solver change. The original
tabulated-kernel subdivision failure remains unchanged.

## Frozen scope and coverage

The [physical-boundary contract](native_oblique_physical_boundary_contract.md)
and [execution record](native_layered_full_execution.md) define the experiment.
The artifact is
[`native-layered-full-20261001`](../artifacts/native-layered-full-20261001).
Its frozen plan covers all 11,364 original tracks, groups 51/61/98, four polar
ordinates, both planar orientations, independent axial signs, heights 1/20
and axial grids 1/2/4.

Every angular state retains `8*Nz` regional/layer volume sources and `6*Nz`
surface/layer radial-inflow coordinates. Physical top/bottom entry is vacuum.
Eight independent axial-entry controls and two separately swept positive
assembly controls remain separate from the physical source columns. No source
coordinate is fitted or removed.

| Coverage | Completed count |
| --- | ---: |
| Primary batches / complete replay batches | 1,080 / 1,080 |
| Physical configurations, orders 16 and 32 | 6,545,664 |
| Physical coordinate evaluations, including controls | 279,281,664 |
| Physical piece/column updates | 2,453,859,601,920 |
| Matched regression configurations, orders 8 and 16 | 6,545,664 |
| Previous original-coordinate regression evaluations | 91,639,296 |
| Byte-identical scientific replay files | 16,200 |
| Independent full-inventory audits / full-field traces | 24 / 288 |
| Native group/height/grid white cases | 18 |

Each full-inventory family covers every original index exactly once. The
order-32 raw candidate responses and primitive/cell/face witnesses use
lossless ragged storage. Replay recomputes and serializes all 15 scientific
files per batch, then checks their lengths and SHA256 values against primary
bytes without retaining a second large archive. The previous zero-gradient
regression compares all local cell and face fields byte-for-byte against the
sealed preceding kernel.

## Numerical results

The final verifier reports the following maxima from the full-inventory
checks and selected independent reference traces. Exact-zero controls are
listed separately from relative errors.

| Check | Maximum relative error |
| --- | ---: |
| Primitive balance | 5.177e-16 |
| Cell balance | 1.386e-14 |
| Whole-track balance | 9.593e-15 |
| Geometric measures / constant solution | 9.520e-15 |
| Represented width | 2.093e-14 |
| Independently swept source assembly | 1.378e-14 |
| Complete-coordinate order-16/order-32 difference | 1.302e-14 |
| Independent whole-flight reference | 8.681e-16 |
| Independent integrated response | 8.979e-15 |
| Independent full cell/face fields | 1.671e-14 |
| Geometric white physical balance, including axial escape | 2.654e-14 |
| Local surface/layer white closure | 1.160e-15 |

Shared-face differences and physical axial incoming flux are exactly zero.
The audits independently reconstruct all stored coordinates and check the
worst order-convergence track in every group/orientation/axial-sign combination:
12 full traces per family, 288 in total. Their independent geometry/integration
references check field accuracy in addition to conservation. All frozen gates
pass without tolerance changes.

## Native white return and the separate stored-normalizer model

Six height/grid assemblies each cover all three groups and both orders 16/32.
The radial return mixes polar and axial states at each surface and axial layer,
with `6*Nz` return amplitudes and `64*Nz` independent angular volume-source
coordinates. Top/bottom entry stays vacuum. Incoming geometric current measures
set the physical closure denominator; flux, both signed current components,
radial return and axial escape are checked between the two orders. The
admission controls also verify analytical cyclic white return and reject a
perturbed stored surface measure as geometric conservation.

The separate stored-native-normalizer comparison leaves a maximum physical
balance defect of **1.5560039535192466e-7**. It is retained as a different
boundary model and does not pass as geometric conservation. Neither surface
nor volume normalizers were fitted to erase this discrepancy.

## Completion, isolation and seal

The [final result](../artifacts/native-layered-full-20261001/verification/result.json)
sets `full_native_physical_operator_qualified`, `full_native_white_qualified`
and `full_previous_zero_gradient_regression_completed` to true. Its
[own watchdog receipt](../artifacts/native-layered-full-20261001/runs/final_verification_watchdog.json)
has return code zero and no resource failure. The 2,191-job schedule comprises
1,080 primary, 1,080 replay, 24 audit, six white and one final-verification job.
The verifier's separate `watchdog_processes=2218` includes 28 preflight jobs
and excludes its own then-unwritten receipt; 2,219 receipts exist including it.

The final verifier confirms 303 frozen identities and 997 protected project
inputs unchanged, and verifies 88,063 entries in 29 prior artifact seals.
The maximum sampled monitored memory is 485.91 MiB and the longest monitored
child is 63.13 seconds, within the 512-MiB and 600-second limits. Final
verification itself takes 40.02 seconds under its watchdog, with 76.71 MiB
sampled peak memory. Each numerical child used one thread.

The first scheduler's unexplained interruption and the authorized resumption
are retained under `resumption_20261003`; no scientific failure was recorded
at that interruption. The resumed scheduler's log ends with the successful
final-verification entry. Its process and numerical children were absent
before sealing, and the complete file inventory and metadata remained stable
through manifest generation. No numerical validator was rerun for this
report or sealing operation.

The [seal](../artifacts/native-layered-full-20261001/result.sha256) covers
**25,713 files / 12,224,064,357 bytes**, excluding the manifest itself.
An independent second pass verified every file digest, the exact path set,
all 2,191 scheduled receipt identities/results and final qualification flags.
Manifest SHA256:

`6ab0927cb9570715607c260873e907d6b6a429327773909ceb4b2e4f0af3ac2d`

## Scope limits

This is an exact-exponential fixed-source reference with actual axial vacuum
and layer-local geometric white return on the frozen native trajectory set.
Changing the axial grid changes the represented source and white-boundary
approximation; agreement across these grids is not a continuum error bound.
The native lift is an explicitly chosen extension, not an axial law uniquely
recovered from scalar data.

The original tabulated native kernel still fails strict spatial subdivision
equality at about **2.96e-5**. This candidate neither repairs that kernel nor
qualifies coupled eigenproblems, POD training, production, or a D4 restart.
Those require separate contracts and evidence.
