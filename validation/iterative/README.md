# Iterative SPOT validation

Use the [current D4-A quickstart](D4A_CORRECTED_QUICKSTART.md) for the repaired
runtime, initial state, completed-map replay and packaging. The
[current handoff](d4a_final_validation_handoff.md) owns live execution status;
this overview deliberately does not repeat map numbers or process state.

The method is fixed-space Galerkin SPOD with online radial fixed-source
transport, a reduced axial solve and direct Picard feedback. The next research
steps and decision rules are in the [validation plan](../../SPOT_doc/validation_plan.md).
The [acceptance matrix](d4a_corrected_acceptance_matrix.md) distinguishes
iteration convergence, physical accuracy and reproducible delivery.

## Maintained paths

| Task | Entry |
| --- | --- |
| Repaired-map preflight and execution | `run_d4a_rank2_picard_map.sh --repaired-runtime ...` via the quickstart |
| Completed-chain replay | `check_d4a_corrected_acceptance.sh` with the explicit repaired pair |
| Final fixed-point observables | `run_d4a_corrected_final_observables.sh --repaired-runtime ...` |
| Portable copy of a completed map | `freeze_d4a_corrected_map.sh --repaired-runtime ...` |
| Saved-data accuracy/cost report | `make spot-evidence` from the repository root |
| Software and algebra checks | `make spot-fast` in an inactive checkout |

Frozen map-6 diagnostics now include the
[cold/warm stopping comparison](d4a_map6_axial_repeatability_result.md) and
the [12/24-cell axial comparison](d4a_map6_axial_mesh24_result.md).
The [physical-coordinate comparison](d4a_map6_physical_basis_result.md) reached
its time cap without a terminal and supplies no rank-error estimate.
The [passive column trace](d4a_map6_physical_column_trace_result.md) then found
collapse of fission-free flux and direct positivity rejection. See the
[reference qualification contract](frozen_response_reference_contract.md)
before treating a full-coordinate frozen solve as a physical benchmark.
These isolated studies retain the original radial response and do not advance
the coupled chain.

The subsequent [exact coupled reference check](coupled_reference_nullspace_result.md)
retains radial and leakage feedback in manufactured S2 vacuum models. It
finds a free non-fission amplitude after normalization, with identical k but
different physical neutron balance. Explicit-exchange controls remove that
null direction. This is a small-model closure qualification, not a D4 result;
its seven standalone tests require no transport run or shared build.

The [heterogeneous/multigroup extension](coupled_reference_heterogeneous_result.md)
adds six declared networks and eight standalone NumPy tests. Amplitude freedom
survives some extensions; others approach inadmissible zero-reflector roots
despite full numerical rank. All six explicit-exchange controls pass local
reference checks. These remain manufactured operator comparisons, with no
change to the D4 chain or the fast runner's dependencies.

The [same-operator POD comparison](exchange_projection_result.md) covers those
six networks plus two four-region cases with unequal volumes. Forty reduced
solutions separate projection error from the change in closure. Full-space
recovery passes; constant-enriched spaces preserve global balance, while
accuracy remains a separate check. Nine standalone NumPy tests pass.

The [native radial response study](native_radial_response_result.md) now checks
the raw MOC flight on an eight-region historical pin mesh in three groups.
Held-out and freshly boundary-closed sources reproduce the nonlocal action;
raw balance defects of order 1e-7 are retained. Eight standalone NumPy tests
pass. This is collision-only qualification.

The subsequent [native multigroup/POD study](native_multigroup_pod_result.md)
retains all 370 groups and verifies the stored scattering/leakage semantics.
Four full fixed-source references are positive and pass fresh native sweeps.
Sixty-four same-operator POD comparisons recover the reference at full rank;
constant-enriched rank 2 nevertheless has negative flux. Eleven standalone tests
pass.

The [native radial/axial candidate](native_axial_coupling_result.md) now restores
the matched original fission data and physical self scattering, and couples the
native nonlocal action to vacuum axial S2 diamond difference. Three full-coordinate
references pass the declared checks. Forty-eight fixed POD comparisons recover
them at full rank, but 25 truncated cases have negative outgoing angles, sometimes
despite positive scalar flux and conserved weighted equations. Ten standalone
tests pass. This independently defined candidate does not replace the production closure.

The [axial-refinement follow-up](native_axial_refinement_result.md) now checks
1–64 cells in the same full space. All five meshes from 4 through 64 have
negative outgoing angles despite positive scalar flux and small equation
residuals. Signed source diagnostics identify negative effective sources at
vacuum inflows even with nonnegative DD attenuation. The candidate is therefore
not qualified as a refined positive reference. Revisit radial/angular source
and current coupling before improving its POD basis; twelve standalone tests
and dense-to-nodal calibration support this finding.

The [source/current audit](native_source_current_result.md) confirms that the
declared moment and native radial-current identities agree, despite those
negative angles. A direction-wise H lift also lacks positivity: all 370 groups
have certified negative exact-propagation outputs for nonnegative unit inputs.
Eight tests include an exactly conservative positive-response counterexample.
The [next angular-reference contract](native_angular_reference_contract.md)
therefore specifies native directional-state extraction and aggregation checks
before another coupled eigenproblem or POD change.

The [native directional extraction](native_directional_response_result.md)
now reproduces 93 native scalar/boundary flights for groups 51, 61 and 98,
including source isolation and its rounding ledger, and measures a planar
x-current response from paired angular sources. All 87 nonnegative source
cases have nonnegative track amplitudes and full segment integrals. Native
and analysis replays agree exactly; eight analytical tests pass. Axial odd
state is absent from the original 2D interface, motivating an
[explicit signed axial-state extension](native_signed_axial_contract.md).

The [signed-state result](native_signed_axial_result.md) now verifies that
extension at zero axial variation against 648 native flights. All 93 original
isotropic cases are recovered, and common white return mixes the axial signs
correctly. Returning each sign separately leaves scalar flux unchanged but
changes the measured axial current by 44–181%. All 642 nonnegative prescribed
flight inputs, including nine different-boundary controls, have nonnegative
retained states. Full replay agrees exactly and eight analytical tests pass.
The subsequent [transport across axial cells](native_axial_streaming_result.md)
passes positive-response, native constant-mode and raw current-balance gates
in 3,384 prescribed-source cases. Its 4-to-8-cell axial escape changes by
1.88–6.11%, failing the declared 1% mesh gate. Full replay agrees exactly and
13 analytical tests pass. The [16/32/64-cell follow-up](native_streaming_refinement_result.md)
now also passes positivity and raw balance, but white-boundary escape still
changes by 2.64–5.03% in the last pair, despite scalar changes below 1%.
A compact implementation completes under the original memory cap; the
preceding resource-limited attempt is retained. The
[analytic axial-discretization check](analytic_axial_slab_result.md) now finds
two false admissions under the adjacent-grid 1% rule, and 11.09% scalar
error in a 256-cell conservative-scattering slab despite correct escape.
All 78 slab solves pass algebra, balance and positivity; 11 tests and full
replay pass. The completed [cell-characteristic comparison](axial_cell_characteristic_result.md)
passes the frozen 256-cell true-error target in all 13 slabs: maximum scalar
error is 0.565% and maximum total-escape error is 0.270%. All 13,260 unit
source/boundary responses remain nonnegative; periodic controls, 22 tests and
full replay pass. This qualifies the manufactured slab candidate only. The
completed [native segment-composition audit](native_segment_composition_result.md)
recovers all unsplit coefficients exactly and verifies exact-exponential
composition, but native subdivision changes responses by up to 0.00296%.
All strict native equality comparisons fail despite positivity and small raw
balance defects. The resource-limited first attempt is preserved; compact
execution and full replay pass. The next
[exact-kernel full-flight comparison](exact_native_flight_result.md)
now passes native recovery, positivity, raw balance, full-flight partition
and common-white checks. Its largest weighted scalar change is 2.488 ppm
at fixed input and 1.194 ppm after reclosure. Sixteen tests and full replay
pass. The completed [oblique-strip geometry experiment](oblique_strip_geometry_result.md)
qualifies actual axial crossings on manufactured strips: 101,632 independent
unit responses remain positive or zero, shared-face currents match exactly,
and order-16 analytic mean/current errors are below 1.12e-14. Order-2 currents
still have up to 2.54% error despite near-roundoff balance. Nineteen tests and
8,181 byte-identical replay files pass. The completed
[native-track pilot](native_oblique_track_pilot_result.md) qualifies eleven
deterministically selected original paths, retaining all polar/sign states
and 931,584 independent unit responses. Whole-track integral/outgoing recovery
is within 3.45e-15; local geometry/reflection defects remain below 1.72e-12.
Thirty-one tests and all 39,777 replay files pass. The storage-blocked initial
preflight is retained; compact storage preserves the full matrix. The completed
[full-path geometry preflight](native_oblique_full_preflight_result.md) now
audits all 11,364 tracks and 7.856 billion pieces, with maximum local measure
error 1.88e-12. Independent counts, seven tests and all 216 replay analysis
files pass. A 583-MiB audit failure is preserved; the bounded audit passes.
The [streaming implementation calibration](native_oblique_streaming_calibration_result.md)
now passes eight tests and 408 byte-identical replay files. The completed
[full-track source response](native_oblique_full_response_result.md) qualifies
all 91,639,296 original-coordinate evaluations and common-white recovery in
the manufactured zero-gradient subspace. Eleven tests, six independent raw
audits and 5,246 byte-identical replay files pass; order-16 recovered fields
differ from the exact companion by at most 1.03e-14. The
[layered physical-source calibration](native_layered_transport_result.md) now
passes 10 tests, 24 independent audits and 643 byte-identical replay files.
It verifies actual vacuum entry and escape in the declared samples and
18 manufactured layer-local white cases. A weak-leakage precision failure was
corrected in physical geometry; independent order-32 errors are below 1.19e-14.
The [full physical-boundary experiment](native_oblique_physical_boundary_contract.md)
now has a [completed, sealed full-inventory result](native_layered_full_result.md):
all 2,191 jobs, 16,200 byte-identical replay files, 24 independent audits,
288 full-field traces and 18 native geometric-white cases pass. Independent
full-field error is at most 1.68e-14 and physical white balance defect at most
2.66e-14. Complete prior-kernel regression also passes. The separate stored
normalizer leaves a 1.56e-7 physical defect; the native tabulated spatial gate
remains failed at 2.96e-5.
No coupled eigenproblem or production change is admitted by these results.

No old default or series wrapper selects the repaired chain implicitly.
Historical AA, pin-cell, coarse-mesh and superseded-scattering results remain
available as evidence for their own configurations. Their local PASS labels
are not repaired D4 validation.

`run_full_rank_picard_cycle.sh` exercises a manufactured four-region,
rank-four state lifecycle without transport. It proves neither full-rank D4
physical accuracy nor the adequacy of a three-snapshot rank-three basis.

The [previous overview](README_HISTORY.md) is retained as history. Its
continuation directions are inactive. Keep running inputs and sealed outputs
unchanged; diagnostics use completed states and private output directories.
