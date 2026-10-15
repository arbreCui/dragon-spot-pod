# SPOT validation and research plan

The research question is: **what accuracy and total computational cost can a
fixed radial POD space achieve in an iterative 2D/1D neutron-transport method?**
The immediate case is the repaired D4-A component. Extending to a full core is
a later milestone. The method and its closure approximations are defined in
[rederivation.md](rederivation.md).

[Live execution status](../validation/iterative/d4a_final_validation_handoff.md),
[operator commands](../validation/iterative/D4A_CORRECTED_QUICKSTART.md), and
[release acceptance](../validation/iterative/d4a_corrected_acceptance_matrix.md)
have distinct owners. This plan does not duplicate their changing map numbers.
The [saved-evidence report](../validation/d4_reference/d4a_evidence_report.md)
provides a dated numerical baseline and can be regenerated without transport.

## Evidence already available

Weighted POD algebra, frozen-source identities, the Gram metric, source moments,
strict inner stopping, state lifecycle and the outer AND gate have software
checks. Real repaired coupled maps and independently replayed NOT_MET results
exist. The completed CE reference provides k, leakage and normalized nu-fission
fractions. It has no direct flux or heating tally.

Material and scattering repairs are prerequisites for the current chain.
Historical pin-cell fixed points and superseded D4 MET records cannot fill
current physical-validation gaps. A smaller update or projection residual is
not an eigenvalue-error bound.

## Finite experiment matrix

Run comparisons on isolated copies. Hold geometry, material state, nuclear data,
boundaries and all unlisted settings fixed. Each experiment produces differences
and a conclusion about its stated hypothesis, not a fitted correction.
Preparation and read-only analysis can proceed while the current baseline runs.

| Priority / question | Comparison and controlled change | What it resolves | Stop / decision |
| --- | --- | --- | --- |
| A. Does the declared coupled map have a reproducible fixed point? | Continue the existing bounded baseline with unchanged rank, runtime and thresholds. Independently replay all three defects. | Iteration error for this discretization. | Stop at the first MET or invalid inner solve/budget boundary; MET alone does not close accuracy. |
| B. Can the saved cross sections support a same-data reference? | Audit current raw `MGXEXP` P0 sums versus SIGS00 by mixture and incident group; then trace discrepant isotope records through the library/TONE/macrolib path. | Locates the obstacle to a matched multigroup reference before launching another transport study. | Do not normalize away mismatches or clip negative probabilities. If MC cannot represent the operator, use a deterministic same-operator reference. |
| C. Does the axial inner solve depend materially on the initial guess? | Same saved SYSTEM/TRACK/MACRO and executable; restart from a saved terminal and compare with a cold solve at the same tolerance. A later tolerance study changes only that tolerance. | Terminal repeatability and finite inner-solve effects. | Report k, normalized modal/physical flux and leakage changes; this is not a mesh experiment. Existing three-cell cold/warm difference is 0.48144 pcm. |
| D. How much is axial spatial/angular discretization contributing? | Frozen-radial 12 versus 24 cells at S8; separately S8 versus S16 at one fixed mesh and unchanged scattering order. | Local spatial or angular sensitivity, one factor at a time. | Existing 3/6/12 changes are 784.49/156.82 pcm; do not extrapolate an error correction. Carry a selected refinement through a separate coupled convergence study before claiming coupled mesh accuracy. |
| E. How much is POD truncation contributing? | First qualify a full-coordinate reference: positive active flux, determined amplitudes after normalization, physical radial exchange and balance. Then compare reduced and full states under declared identical equations/data. Scope frozen or rank-2/rank-3 comparisons as local sensitivities when admissible. | Separates reference-closure limitations from projection and coupled-rank differences. | Full coordinates and refreshed radial response alone do not guarantee a unique reference. Rank 3 of three snapshots is not physical full rank. Failed enrichment gives no truncation-error estimate. Do not select rank by matching CE. |
| F. Which approximation explains the remaining CE difference? | Compare a numerically resolved same-data full-order 2D/1D result with an independently resolved same-data 3D result, then examine MG/CE data-processing differences. | Separates POD, synthesis closure and reference-data effects along a declared comparison path. | No additive attribution of all CE error to POD. Report interactions and unavailable comparisons explicitly. |
| G. Is the reduced method computationally useful? | Measure total wall time, CPU/core-hours, peak memory, snapshot setup and online solve separately for reduced and full-order calculations at comparable observable accuracy. | End-to-end benefit and offline amortization. | Current radial cost dominates. Profile it and test inner precision only on isolated copies; do not change the active `1e-13` path. No speedup claim from unmatched thread counts or one axial solve. |

B now has a [current-input Fe56 localization](../validation/d4_reference/d4a_scattering_data_audit.md):
the selected steel/group discrepancies already exist in saved microscopic data.
The same note links the dragon project's completed Fe56 P3 and TONE-path
reviews. Reuse those records; the remaining extension is the D4 G25/G26
SCAT00/SIGS00 relation after matching library lineage, not another processing
or G140 capture audit.
C has a [12-cell terminal repeat](../validation/iterative/d4a_map6_axial_repeat_result.md):
one further inner solve moved modal flux by 5.61237e-7 with unchanged thresholds.
The subsequent [cold/warm and tighter-inner comparison](../validation/iterative/d4a_map6_axial_repeatability_result.md)
is complete: at 2e-7 the cold/warm reactivity difference is 0.02254 pcm, while the
modal and leakage differences still exceed the outer accuracy scale.
D now has a [map-6 frozen 12/24-cell comparison](../validation/iterative/d4a_map6_axial_mesh24_result.md):
at the same 2e-7 settings, refinement changes reactivity by +39.23943 pcm
and source-normalized axial leakage by -0.05186812 percentage points.
The old 3/6/12 study used a different frozen radial operator; do not combine
these increments to infer a convergence order.
E's [physical-coordinate attempt](../validation/iterative/d4a_map6_physical_basis_result.md)
passed operator and initial-field equivalence checks, but reached its
1,200-second cap without a terminal. It provides no rank-error estimate.
The [passive follow-up](../validation/iterative/d4a_map6_physical_column_trace_result.md)
reproduces 2,615 numerical log lines and shows collapse of the 107 fission-free
columns. The original runtime directly rejects the raw-10 checkpoint for
nonpositive active scalar flux. The frozen full-coordinate operator splits
into radial columns; its admissibility as a reference is therefore an open
question separate from its iteration budget.
The [exact coupled small-model check](../validation/iterative/coupled_reference_nullspace_result.md)
then retains radial and shared-leakage feedback and still finds one free
non-fission amplitude after global normalization in two S2 vacuum examples.
The exact Jacobian ranks are 6/7 and 12/13. Identical k can accompany different
physical balance defects; explicit-exchange controls remove this null direction.
This qualifies the reference question, not actual D4 Jacobian rank or CE error.
These findings do not repair cross sections or advance the D4 coupled chain.

The [six-case heterogeneous/multigroup extension](../validation/iterative/coupled_reference_heterogeneous_result.md)
is complete. Positive amplitude freedom survives axial material variation
and an asymmetric two-group exact check. Three other configurations approach
zero-reflector roots with full numerical rank and physical balance defects
of 19–21%. One has only 0.224 pcm k discrepancy from its explicit-exchange
control. All six conservative-exchange controls pass local reference checks;
none of these numbers estimates D4 error or proves absence of other roots.

The [same-operator POD comparison](../validation/iterative/exchange_projection_result.md)
now covers eight networks and forty reduced eigenproblems. Full spaces recover
the conservative references. Constant-enriched spaces preserve global balance
at truncated rank, but their coarsest approximations can still be inaccurate.
For the four-region layered example, enriched rank 3 has 0.096344% scalar-flux
error and balance at numerical precision; ordinary rank 3 has 0.037405% flux
error and a 0.021148% balance defect. These are descriptive network results,
not D4 criteria or a basis/rank selection for the live chain.

The [native flight-response study](../validation/iterative/native_radial_response_result.md)
now qualifies nonlocal collision response and boundary elimination in three
groups on an eight-region historical pin mesh. Independent and fresh
boundary-closed sweeps agree below 7.4e-15; raw current-balance defects remain
of order 1e-7. The native radial action must not be replaced with the toy graph
Laplacian or a diagonal ratio fitted to one field.

The [native multigroup/POD extension](../validation/iterative/native_multigroup_pod_result.md)
has completed that fixed-source comparison on all 370 groups. Embedded leakage
is applied once, signed scattering is retained, four full references are positive,
and full POD recovers the same operator. The 64 reduced cases distinguish weighted
equation conservation from raw native current balance and local positivity:
constant-enriched rank 2 has negative flux despite sub-1% global flux error.

The [small native radial/axial candidate](../validation/iterative/native_axial_coupling_result.md)
now passes its three full-coordinate eigenreference checks, with restored
physical self scattering and matched original fission data. All 48 fixed POD
comparisons recover the reference at full rank. Twenty-five reduced cases have
negative outgoing angles; positive scalar flux and weighted conservation are
insufficient.

The [completed axial refinement](../validation/iterative/native_axial_refinement_result.md)
finds negative outgoing angles in the full space on every 4–64-cell grid.
The last k change is also above its declared convergence threshold. An exact
nodal reformulation is calibrated against the earlier dense problems; signed
source diagnostics identify negative effective angular sources with nonnegative
attenuation at vacuum inflows. The full candidate is therefore not a qualified
refined reference. Prioritize a consistent radial/angular source-current
coupling and test it against these failures before new POD training or rank
selection. Keep changes in axial discretization separate from projection comparisons.

The [source/current follow-up](../validation/iterative/native_source_current_result.md)
finds the implemented ledgers consistent, but a direction-wise H extension also
has negative exact propagators in every group. It therefore cannot be accepted
as a positivity repair from scalar data alone. The next bounded milestone is
the [native directional-response interface](../validation/iterative/native_angular_reference_contract.md):
audit direction/sign conventions and source isolation, recover the native
scalar and boundary response by aggregation, and identify the odd/current
response before a new coupled eigenproblem. Existing raw signed coefficients
and failures remain unchanged.
The [planar extraction](../validation/iterative/native_directional_response_result.md)
has now passed native aggregation and paired x-current checks for groups 51,
61 and 98. Its positive external-input track states, exact PJJ reconstruction
and independent native replay are verified. The 2D interface excludes axial
odd harmonics, requiring the explicit
[signed axial-state extension](../validation/iterative/native_signed_axial_contract.md)
with explicit sign weights and white-boundary mixing, initially at zero axial
variation. This result does not reopen POD training or admit an axial model.
That [signed-state experiment](../validation/iterative/native_signed_axial_result.md)
now passes 648 native flight checks and recovers all 93 previous P0 cases.
Separate-sign returns change axial current by 44–181% despite unchanged scalar
flux; common white return and the measured odd response must be preserved.
The [retained-state axial-streaming result](../validation/iterative/native_axial_streaming_result.md)
now passes positive prescribed-input, native constant-mode and raw even/odd
balance checks in 3,384 finite-mesh cases. It fails its 1% spatial gate:
4-to-8-cell axial escape changes by 1.88–6.11%. Exact-versus-native kernel
differences are much smaller than these mesh changes. The completed
[same-operator 16/32/64-cell refinement](../validation/iterative/native_streaming_refinement_result.md)
passes coarse recalibration, positivity and balance but still fails its
spatial gate: last-pair white-boundary escape changes by 2.64–5.03%, while
scalar changes are below 1%. The first resource-limited execution is sealed;
compact direct application completes under the unchanged memory cap.
The completed [analytic slab check](../validation/iterative/analytic_axial_slab_result.md)
now measures two false admissions under the adjacent-grid 1% comparison:
true fine-grid scalar errors remain 1.28–1.40%. At 256 cells, conservative
strong scattering retains 11.09% scalar error despite correct escape.
All 78 algebra/balance/positivity checks pass. The completed
[cell-characteristic comparison](../validation/iterative/axial_cell_characteristic_result.md)
passes the fixed 256-cell target for all 13 analytic slabs: scalar error is
at most 0.565% and total-escape error at most 0.270%. Its 13,260 additional
directional-volume/boundary unit responses are nonnegative; raw balance,
periodic controls, 22 tests and full replay pass. The completed
[native segment-composition audit](../validation/iterative/native_segment_composition_result.md)
recovers all native whole-segment B/D exactly, but subdivision changes the
tabulated response by up to 2.96e-5 relative. All strict unchanged-action
comparisons fail; exact composition, positivity and raw balance pass. The
first resource-limited attempt remains sealed; compact execution and full
replay complete under the unchanged caps. The completed
[exact-kernel full-flight comparison](../validation/iterative/exact_native_flight_result.md)
passes native recovery, full-flight partition, positivity, raw balance and
common-white checks. Its weighted scalar change is at most 2.488 ppm for
fixed input and 1.194 ppm after reclosure. Sixteen tests and full replay pass.
The completed [oblique-strip geometry experiment](../validation/iterative/oblique_strip_geometry_result.md)
passes real axial-plane crossing checks on manufactured strips: 101,632
unit responses are nonnegative, shared-face contributions match exactly,
and order-16 analytic errors are below 1.12e-14. Order-2 face-current errors
reach 2.54% despite near-roundoff balance. Nineteen tests and all 8,181 replay
files pass. The completed [native-track pilot](../validation/iterative/native_oblique_track_pilot_result.md)
qualifies eleven deterministic original paths with all polar/sign states and
931,584 nonnegative unit responses. Whole-track integral/outgoing recovery is
within 3.45e-15; geometry/reflection errors stay below 1.72e-12. Thirty-one
tests and all 39,777 replay files pass. A storage-blocked initial preflight
remains sealed; compact execution retains every case and source coordinate.
The completed [full-native geometry preflight](../validation/iterative/native_oblique_full_preflight_result.md)
audits every original path, with maximum local measure error 1.88e-12 and
complete independent count/replay agreement. Its first audit exceeded memory;
the failed output is preserved and the bounded audit passes. The
[streaming implementation calibration](../validation/iterative/native_oblique_streaming_calibration_result.md)
now passes. The completed
[full response stage](../validation/iterative/native_oblique_full_response_result.md)
qualifies all 91,639,296 original-coordinate responses in the zero-gradient
subspace. Complete recovery and common-white reclosure pass; eleven tests,
six independent raw audits and all 5,246 replay files agree. The maximum
order-16 field difference from the exact companion is 1.03e-14. No full-native
source response was solved in the earlier geometry preflight. The
[layered physical-source calibration](../validation/iterative/native_layered_transport_result.md)
now passes ten tests, 24 independent audits and 643 byte-identical replay files.
It retains every layered input coordinate on 204 selected original tracks and
checks 18 manufactured physical-white cases. A geometric precision failure
was corrected without changing the gates; independent order-32 errors are
below 1.19e-14. The [full physical-boundary stage](../validation/iterative/native_oblique_physical_boundary_contract.md)
has a [completed, sealed isolated result](../validation/iterative/native_layered_full_result.md)
covering the complete prior regression and all 11,364 native tracks. All 2,191
jobs and 16,200 scientific replay files pass, with 24 independent audits,
288 full-field traces and 18 layer-local geometric-white cases. The final
verifier and independent seal check pass; 303 frozen identities, 997 protected
inputs and 29 prior seals remain unchanged. Independent field error is below
1.68e-14 and physical white balance defect below 2.66e-14. The separate
stored-normalizer comparison retains a 1.56e-7 physical defect. Acceptance is
limited to the declared fixed-source operator and geometric white boundary;
coupled eigenproblem, POD and production qualification remain outside this stage.
Slab qualification does not qualify an axial bridge or erase the failed
native spatial gate. Do not use last-pair changes alone as a true-error bound.
No coupled reference, POD training or production readiness is admitted here.
Keep the measured raw balance defect and signed flux explicit, following the
[coupled-reference contract](../validation/iterative/frozen_response_reference_contract.md).
Do not insert an unqualified candidate into the running D4 chain. Compare any closure change
separately from projection error. Extra mean-matching constraints are not a production repair:
the layered one-group family would require different amplitudes in its two
planes. A longer budget or a new nonlinear solver alone does not qualify
the current full-coordinate reference.
B still needs matched library lineage; C's observable-repeatability
limit remains open; D still needs angular and separately coupled refinement.
These studies use standalone prepared inputs and do not splice into the
current chain. F depends on the operator audit and numerical qualification.
G starts with existing timing logs and later uses matched configurations.

The observed negative angular/endpoint values remain signed. Use the same
controlled D/E comparisons to locate their origin and measure their integrated
contribution; their existence does not by itself explain the CE discrepancy.

## Quantities and decisions

- Keep the original outer AND gate: Rrho, Rleak and Ra each <= 5e-7.
- Keep the existing CE k criterion: absolute reactivity difference <=
  500 + 3 sigma_pcm, with sigma_pcm = 1e5 sigma_k / k_CE^2 <= 50.
- Record three-zone and 651 pin-zone normalized nu-fission differences as
  descriptive shape data. Do not call them absolute thermal power or attach
  significance without the needed covariance.
- Use one normalization and one spatial mapping in each comparison. Report
  k, signed source-normalized leakage, shape differences and solve cost together.
- Preserve failed and incomplete experiments; an iteration cap is not a terminal.
- Specify each numerical comparison before execution. Do not derive tolerances,
  clipping or model coefficients from the desired reference answer.

## Delivery checkpoint

A distributable research release needs source and build instructions, the
repaired runtime identity, snapshot/basis/macrolib/tracking provenance, the
repaired initial state, the accepted map chain and observables, the existing
reference and comparison, and a fresh-location replay. Nuclear-data licensing
and availability must be stated rather than silently substituting data.

The existing standalone map-1 copy/replay proves a portion of this route.
Until the first repaired MET and accuracy studies are completed, packages must
be labelled diagnostic or continuation inputs. Final delivery must not inherit
physical validity from an older material/scattering epoch.

The [previous validation plan](validation_plan_HISTORY.md) preserves the old
rank-1/2 and Anderson development record. Its per-attempt next-step directions
are historical and are superseded by this finite experiment matrix.
