# Native radial / axial eigenreference and fixed POD comparison

Date: 2026-09-28. Artifact: `validation/artifacts/native-axial-coupling-20260928`.

Follow-up: [full-space axial refinement](native_axial_refinement_result.md)
now finds negative outgoing angles on all 4–64-cell grids. The coarse results
below remain valid for their stated meshes; they do not qualify this candidate
as a refined positive reference. Radial/angular source-current consistency
must be revisited before further POD development for this candidate.

Three independently defined, full-coordinate coupled eigenproblems pass the
declared positivity, normalization, residual, local-rank and current-ledger
checks. All 48 fixed-basis POD comparisons finish; full rank recovers each
reference. However, **25 reduced cases have negative outgoing angular flux**,
including cases with positive scalar flux and a small global balance defect.
This is a qualification of this candidate and these meshes, not D4 acceptance,
a replacement of the production ratio closure, or validation against 3D transport.

## Original data and the declared candidate

The radial operator is the previously verified, white-boundary raw MOC response
of the historical eight-region pin, with all 370 groups. The original seed
snapshot has an outer one-item `SNAP` list; its inner archive supplies plane 1's
`MICROLIB2/MACROLIB`. A read-only exporter recovers every original `NUSIGF` and
`CHI` component. All 3330 other checked group records match the frozen MACRO0
bit for bit: total, transport correction, self/packed scattering, packed indices
and CHI. MACRO0 itself has zero NUSIGF and cannot supply an eigenproblem.

There are 32 active fission components in each of regions 4–7, and none in
regions 1–3 or 8. All 128 components remain distinct in the factorized fission
operator. No coefficients, spectra or signed scattering entries are clipped,
renormalized or fitted. The initial exporter rejection due to the outer archive
wrapper is retained with its source and log; it produced no accepted data.

Let `H_g=R_g^-1` and `C_g=H_g-diag(total_g)`. The candidate equations are

\[
\pm\mu\partial_z\psi_g^\pm+\Sigma_{t,g}\psi_g^\pm
 +\tfrac12 C_g\phi_g
 =\tfrac12(S^{phys}\phi)_g+\tfrac\rho2(F\phi)_g,
\quad\phi_g=\psi_g^++\psi_g^-,\quad\mu=1/\sqrt3,\quad\rho=1/k.
\]

Axial streaming uses diamond difference, with vacuum inflow at both ends.
The native radial data are repeated uniformly over a manufactured 20 cm axial
extrusion. The predeclared meshes are `[20]`, `[10,10]` and `[8,12]` cm.
These are small discrete controls, not a mesh-converged physical benchmark.

Crucially, the diagonal of scattering is restored from `SPOT-S0-PHYS`.
The old binary32 leakage subtraction embedded in SYSTEM's used self coefficient
is removed; axial streaming now supplies the leakage. Off-group entries and
transport-corrected total remain unchanged. The native radial action is retained
as an isotropic P0 term; it is not an angular 3D transport operator.

One global volume-weighted nu-fission integral normalizes the scalar field to 1.
Actual birth is computed with the saved component spectra, so the ledger does
not assume their binary32 sums are exactly one.

## Full reference qualification

For each group, eliminate the two angular face fields exactly, retaining the
cell scalar field. The resulting removal matrix A has 2960 or 5920 unknowns.
Factor fission as `F=UV` and solve the smaller production eigenproblem
`V A^-1 U y = k y`. Select the largest-real-part mode before checking positivity;
it must also be real, positive, simple and dominant in magnitude. There is no
search among modes for one that merely passes the sign test.

| Axial mesh (cm) | k | Minimum scalar flux | Minimum outgoing angular flux | Raw balance / birth | Normalized production-Jacobian rank |
| --- | ---: | ---: | ---: | ---: | ---: |
| 20 | 0.279438470900328 | 1.18820e-13 | 1.18820e-13 | -5.35332e-7 | 129 / 129 |
| 10, 10 | 0.410444778690365 | 7.38720e-14 | 3.41040e-16 | -9.24237e-7 | 257 / 257 |
| 8, 12 | 0.406163292948924 | 7.48525e-14 | 3.59183e-16 | -9.11046e-7 | 257 / 257 |

Every scalar and non-vacuum outgoing angular entry is strictly positive. The
largest independently reconstructed angular-equation residual is 2.59e-13
relative to the fission term. Two positive production-space starts converge in
5–14 iterations and agree with the eigenvector solve within 3.78e-13 in flux.
Relative eigenvalue separation is at least 0.842.

The bordered Jacobian is checked in production coordinates, not presented as a
full angular Jacobian computation. A supplementary audit checks its removal-
matrix prerequisite: infinity-norm condition numbers are 8315, 17440 and 17218;
all-column inverse residual infinity norms are at most 7.26e-13. Together these
checks support a locally isolated normalized eigenmode of this discrete
candidate, including determined amplitudes in the non-fission regions. They do
not establish uniqueness of the original nonlinear ratio equations or D4.

The original gates were fixed before the eigenruns. The extra inverse-norm
audit was declared after the first solve to check the Schur reduction's
invertibility prerequisite; it did not change any case, basis or solution.

## Project the angular equations before eliminating angles

Both basis families are copied unchanged from the preceding 24 fixed-source
training snapshots: plain weighted POD and constant-enriched POD. They were
trained with the preceding prescribed-leakage problems, without any of these
eigenvectors. Each group uses rank 1–8; its basis is shared by every axial cell
and both directions.

Weighted Galerkin projection first gives the full Gram, total-collision,
scattering, radial-closure and fission matrices in the angular equations.
Only then are the axial face coefficients eliminated. Projecting an already
eliminated physical scalar operator would generally define a different method;
an independent two-cell test checks this distinction. Nonorthogonal coordinate
changes at ranks 3 and 8 preserve the physical solution.

The following errors are maxima over the three meshes at each rank. Negative
angle counts are counts of cases, out of three, not counts of entries.

| Rank | Plain scalar-flux error | Enriched scalar-flux error | Plain / enriched cases with negative angles |
| ---: | ---: | ---: | ---: |
| 1 | 6.87456% | 4.48828% | 0 / 0 |
| 2 | 6.82306% | 4.35364% | 2 / 3 |
| 3 | 3.88723% | 2.18669% | 2 / 2 |
| 4 | 1.73931% | 1.83675% | 2 / 2 |
| 5 | 1.38769% | 1.38777% | 2 / 2 |
| 6 | 1.18605% | 1.11005% | 2 / 2 |
| 7 | 0.71659% | 0.67399% | 2 / 2 |
| 8 | < 8e-13% | < 8e-13% | 0 / 0 |

All plain-POD scalar fields remain positive. Enriched rank 2 has negative scalar
entries in all three meshes, retained as signed output. In both two-cell cases,
both families have negative outgoing angles at every rank from 2 through 7.
These are not universally tiny roundoff effects: the worst plain rank-6 angle
is -7.49414e-4 in the equal-cell problem. Positive cell-averaged scalar flux is
therefore insufficient for angular admissibility.

The worst absolute inverse-k differences, expressed as
`1e5*(1/k_reduced-1/k_reference)`, remain about 1761 pcm (plain) and 1681 pcm
(enriched) at rank 7. These numbers concern this deliberately subcritical
manufactured extrusion; they are not D4 or CE discrepancies. No production rank
is selected from this table.

Full rank recovers scalar flux within 7.12e-15; the largest full-rank inverse-k
difference is 1.47e-9 pcm. Coordinate changes preserve flux within 7.48e-16.
The largest projected angular residual across the 48 cases is 1.11e-13.

## Current ledger, conservation and limits

With `V_zi=h_z W_i`, define

\[
b=\sum_{zgi}V_{zi}[\Sigma_t\phi-S^{phys}\phi
             +D_z\psi-\rho F\phi],\qquad
\delta_C=\sum_{zgi}V_{zi}(C\phi),\qquad
b=\sum V(R^++R^-)-\delta_C.
\]

Axial streaming telescopes to the two vacuum outflow currents. The native white
radial boundary has zero net current, while the raw radial flight's small
balance defect is retained in delta_C. This is a collision/scattering/current
ledger, not an independently audited capture/fission reaction balance.

Constant enrichment reduces the weighted angular equation residual below
1.76e-14. Its raw ledger still retains a defect up to 1.00e-6 of birth. Plain
rank 1 instead reaches a 9.90% raw balance defect. The ledger identity closes
within numerical roundoff. Thus equation conservation, current accounting,
scalar accuracy and angular positivity remain separate requirements.

The next bounded reference study should refine the full axial mesh before
claiming axial accuracy, keeping C, materials and source data fixed. Then test
angular-aware offline training or a separately specified positivity-preserving
projection against admitted references. Compare any new axial discretization
separately, retain negative cases, and do not repair them by clipping. Layered
material data and 3D comparisons remain later qualification steps.

## Reproduction and isolation

Ten standalone NumPy tests cover independent physical diamond-difference sweeps,
one-cell analytic removal/eigenvalues, component fission, group orientation,
unequal weights, nonorthogonal coordinates, the angular-before-scalar projection
distinction, balance and negative-angle rejection. The numerical study is
replayed from copied sources and original inputs with one numerical thread.
All 107 analysis files replay byte for byte, including recovered fission data;
all 102 saved numeric arrays are exactly equal. Both working and archived test
copies pass all ten tests. All 997 protected files, 22 source-input hashes and
561 entries from the nine previous artifact manifests remain unchanged.
Final replay, integrity and test receipts are linked below.

No production source, map, shared build, runtime control or D4 acceptance gate
is changed. This result extends the independent research-reference track only.

Files: [exporter](export_native_fission.f90),
[coupled solver](qualify_native_axial_coupling.py),
[invertibility audit](check_native_axial_invertibility.py),
[tests](test_native_axial_coupling.py),
[predeclared plan](../artifacts/native-axial-coupling-20260928/plan.json),
[numerical report](../artifacts/native-axial-coupling-20260928/analysis/result.json),
[verification receipt](../artifacts/native-axial-coupling-20260928/verification.json).
