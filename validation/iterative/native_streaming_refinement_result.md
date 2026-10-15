# Retained-state refinement: scalar change below 1%, white-boundary escape still unresolved

The 16/32/64-cell prescribed-source experiment is complete. All declared
positivity, balance and boundary checks pass, but the final spatial gate
**fails**. Between 32 and 64 cells, scalar-flux changes are below 1% in every
case, while common-white-boundary axial escape still changes by 2.64–5.03%.
Both exact and native-compatible kernels give the same gate outcome.
This is not a mesh-qualified coupled eigenreference.

The [completed artifact](../artifacts/native-axial-streaming-refinement-compact-20260929/README.md)
contains the [frozen run plan](../artifacts/native-axial-streaming-refinement-compact-20260929/plan.json),
[numeric results](../artifacts/native-axial-streaming-refinement-compact-20260929/analysis/result.json)
and [verification](../artifacts/native-axial-streaming-refinement-compact-20260929/verification.json).
The [preceding contract](native_axial_streaming_refinement_contract.md)
fixed the model, meshes, sources and gates before execution. No native mesh
above 64 was run and no physical threshold was relaxed.

## Same operator, smaller memory requirement

The calculation retains groups 51/61/98, height 20 cm, original radial tracks,
four polar nodes, independent axial signs, first-order upwind streaming and
common radial white return. Both planar ray orientations and all n powers of
the upstream shift are retained. Exact-exponential and native-compatible
coefficient lifts remain distinct controls, unchanged from the preceding
1/2/4/8-cell experiment.

The two volume sources are uniform and region index divided by eight, each
constant along z. Both radial vacuum and common-white cases use vacuum axial
inflow. The new meshes contain 72 prescribed solves; 96 further coarse
held-out solves provide 48 calibration comparisons before refinement.
This stage contains no scattering/fission eigenproblem or POD comparison.

An [initial execution](../artifacts/native-axial-streaming-refinement-20260929/README.md)
hit its declared 512 MiB peak-RSS cap at 515.25 MiB after 253.97 seconds.
Its 16/32-cell fields and first 64-cell vacuum field are sealed as incomplete
evidence. The resource cap was not raised. A separately declared compact
execution instead uses 128-line batches and directly applies every Green
shift to two right-hand sides; it expands only the common radial-boundary
matrix. Peak memory fell to 262.69 MiB, with a complete primary execution
time of 586.71 seconds. Numerical execution uses one CPU thread.

All 48 coarse comparisons pass the original `5e-12` criterion, with maximum
relative difference `9.921e-15`. They cover Green coefficients, half-state
flux, radial outgoing state, scalar flux, Jz, face moments and white inverse.
The compact implementation also agrees with all 73 retained expanded-matrix
fields from the resource-limited attempt within `4.265e-15`; this includes
the first 64-cell vacuum field. Changing summation order did not change the model.

## Final 32-to-64-cell changes

Scalar errors use native-volume/cell-height weighted L2 norms after averaging
each fine-cell pair. Escape is total outgoing top-plus-bottom current.
The finer result is the denominator. Every quantity for both sources, all
groups, both kernels and both radial boundaries had to change by less than 1%.

| Native-compatible group / radial boundary | Uniform flux | Ramp flux | Uniform escape | Ramp escape |
| --- | ---: | ---: | ---: | ---: |
| 51 / vacuum | 0.4929% | 0.4805% | roundoff level | roundoff level |
| 61 / vacuum | 0.4877% | 0.4761% | roundoff level | roundoff level |
| 98 / vacuum | 0.4573% | 0.4505% | roundoff level | roundoff level |
| 51 / white | 0.9099% | 0.9147% | 5.0021% | 5.0308% |
| 61 / white | 0.8566% | 0.8614% | 4.5928% | 4.6189% |
| 98 / white | 0.6602% | 0.6645% | 2.6687% | 2.6398% |

The white-boundary escape changes do not follow a settled factor-of-two
decrease over this range. For example, group 51's ramp-source changes are
6.111%, 7.125%, 6.607% and 5.031% for successive pairs from 4/8 through
32/64. Last-pair observed escape orders, using consecutive absolute escape
differences, are approximately 0.464, 0.419 and 0.172–0.177 for groups
51, 61 and 98. These are descriptive values, not reliable continuum-error
estimates. Vacuum escape differences are already at roundoff; their raw
order ratios must not be interpreted as a physical convergence order.

![Adjacent-grid changes for both observables](../artifacts/native-axial-streaming-refinement-compact-20260929/figures/mesh_changes.png)

The exact-versus-native differences over these two-source comparisons are
at most `5.811e-7` in scalar flux, `6.084e-7` in face current and `2.868e-7`
in escape. They are much smaller than the unresolved spatial changes.
Using only the scalar adjacent-grid threshold would have admitted cases whose
leakage is still changing by several percent. Vacuum scalar changes also grow
over these mesh pairs despite staying below 1%; a small last difference is
not, by itself, a validated bound on total spatial error.

## Positivity and raw ledgers

Every retained primitive/Green coefficient, white inverse and tested
half-state response is nonnegative. No coefficient pruning or clipping is
used. The explicit response's entrywise minimum follows from the normalized
Green coefficients and known structural zeros without allocating that matrix.

| Maximum over the two-source cases on all tested meshes | Exact | Native-compatible |
| --- | ---: | ---: |
| Even global relative balance defect | 2.612e-14 | 3.845e-8 |
| Even axial-cell relative defect | 6.027e-15 | 8.319e-8 |
| Odd axial-cell relative defect | 1.314e-16 | 1.253e-7 |
| Face-versus-streaming absolute defect | 2.221e-16 | 4.441e-16 |
| Common-return relative defect | 2.178e-15 | 2.056e-15 |

The unchanged exact balance limit is `1e-10`; native global and axial-cell
limits are `1e-6` and `1e-5`. Face and common-return limits are `1e-13`
absolute and `5e-12` relative. Cell ledgers sum all radial regions in an
axial slab. The sources are mirror symmetric in z, so global odd cancellation
near roundoff is not a strong standalone test; local odd ledgers remain explicit.

All-segment induced-infinity defects `||T+A B-I||` and `||B+A D-L I||/L`
reach `3.701e-7` and `8.740e-6` for the native lift; exact maxima are
`2.560e-15` and `4.540e-15`. These raw defects are reported without correction
or a new acceptance threshold. Fine-grid balance admission applies to the
two specified sources, not a newly executed exhaustive fine-grid source basis.

## Reproducibility and decision

Six implementation tests and the 13 frozen primitive tests pass. The initial
compact-application control failures at near-zero residuals are retained;
their roundoff comparisons now use incoming/source scale and the declared
maximum-field current norm. No physical gate was changed. Full source,
input, runtime, replay and prior-artifact checks are in the verification record.
A fresh-directory replay reproduces all 86 analysis files byte for byte and
all 1,428 arrays exactly. Its peak RSS is 265.91 MiB and elapsed time 586.55
seconds. All 997 protected files, 66 source-input hashes, 114 copied-input
hashes and 1,666 manifest entries from 16 prior artifacts verify unchanged.

The next [independent axial-discretization check](native_streaming_discretization_contract.md)
uses an analytic two-direction slab to measure true spatial errors and the
reliability of adjacent-grid changes. It is a diagnostic for deciding how to
improve axial accuracy, not a fitted replacement for the native model.
The native 64-cell gate remains failed. Do not extend its grid silently,
start POD training, or insert this candidate into the live D4 chain.
