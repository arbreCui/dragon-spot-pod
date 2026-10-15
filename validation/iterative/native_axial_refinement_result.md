# Native axial refinement: full-space angular positivity fails

Date: 2026-09-28. Artifact: `validation/artifacts/native-axial-refinement-20260928`.

Follow-up: the [source/current audit](native_source_current_result.md) confirms
the implemented moment/current identities and shows that a direct direction-wise
H lift also lacks positivity. The next step is native directional-response
qualification, as specified in its [contract](native_angular_reference_contract.md).

**The frozen nonlocal P0 / axial S2-DD candidate does not qualify as a refined
positive reference.** All five finer full-space meshes, from 4 through 64 cells,
have negative outgoing angular flux, despite positive scalar flux, small true
equation residuals and a small current-ledger defect. No POD projection is used
in this study. Improving the reduced basis is therefore not the next reference
priority: the candidate's radial/angular coupling must be qualified first.

The earlier three coarse-mesh checks remain valid for their declared discrete
problems. Their positivity does not extend to axial refinement. This result
concerns the independently introduced candidate, not a measured failure of the
running D4 ratio closure or a comparison with continuous-energy/3D transport.

## Fixed physics and exact reformulation

The original 370-group, eight-region radial response, physical self scattering,
off-group scattering, 128 active fission components and global nu-fission
normalization are copied unchanged from the preceding artifact. The native
white radial boundary and vacuum axial boundaries are retained. The old
embedded leakage remains removed. No coefficient or flux is clipped.

Only the mesh of the uniform, manufactured 20 cm extrusion changes:
1, 2, 4, 8, 16, 32 and 64 equal cells. The previous unequal `[8,12]` cm case is
also used for independent solver calibration.

The previous angular S2 diamond-difference equations have an exact nodal scalar
form. Let f be scalar flux at axial faces, `K=H-S_phys`, and
`D=diag(mu^2/total)`, with `mu=1/sqrt(3)`. Then

\[
 (L\otimes D+M\otimes K+\mu B_\partial\otimes I)f
 =\rho(M\otimes F)f.
\]

For a cell of height h, the element matrices are

\[
L_e=h^{-1}\begin{bmatrix}1&-1\\-1&1\end{bmatrix},\qquad
M_e=\frac h4\begin{bmatrix}1&1\\1&1\end{bmatrix}.
\]

`B_partial` selects the two outer faces. Cell scalar flux is the average of its
two nodal values. The singular alternating mode of the midpoint mass matrix is
retained. There is no mass lumping, angular discretization change or spatial
mode truncation. At 64 cells this represents 192400 nodal unknowns.

All spatial modes are used in a simultaneous-diagonalization preconditioner,
with sparse energy-region factorizations and an exact two-end boundary Schur
correction. Original-equation GMRES residuals still govern each removal solve;
the preconditioner is not an alternative physical operator. Uniform grids use
both parity blocks; unequal grids use the full boundary matrix.

Two earlier preconditioner implementations and their successful coarse
calibrations are retained in `runs`. They needed hundreds of iterations.
The final boundary correction reduces this to one or two inner iterations,
without changing any physical parameter, selected mesh or accuracy threshold.
The additions were recorded before solving the fine meshes. The 64-cell run
takes about 127 seconds with one numerical thread, within its 240-second limit.

The final solver recovers the three previously sealed dense angular solutions:
maximum relative scalar-flux difference is 1.02e-14, and angular fields agree
within 1.33e-13. Small independent controls also compare the two formulations
on unequal four-cell meshes.

## Full-space refinement results

All meshes select the leading positive-real, largest-magnitude Ritz mode from
two independent initial vectors. All cell scalar flux entries remain positive.
The angular equations reconstructed from the saved faces have residuals at most
8.30e-13 relative to the fission term. The largest raw current-ledger defect is
9.25e-7 of birth. The finer cases fail only the declared angular sign gate.

| Cells | k | Minimum outgoing angular flux | Negative angular entries | Angular admission |
| ---: | ---: | ---: | ---: | --- |
| 1 | 0.279438470900329 | 1.18820e-13 | 0 | Pass |
| 2 | 0.410444778690364 | 3.41040e-16 | 0 | Pass |
| 4 | 0.408354576678305 | -0.0621872 | 1418 | Fail |
| 8 | 0.409069834982426 | -0.1003715 | 4104 | Fail |
| 16 | 0.410428624828537 | -0.0941466 | 8772 | Fail |
| 32 | 0.410828259418835 | -0.0740145 | 17516 | Fail |
| 64 | 0.410928575807130 | -0.0674718 | 36458 | Fail |

The minimum scalar flux on the 64-cell mesh is 3.90661e-14. Its negative angles
are consequently not equivalent to the earlier negative-scalar POD examples.
Their magnitude is far above the equation residual and floating-point noise.

![Measured mesh changes and angular signs](../artifacts/native-axial-refinement-20260928/mesh_refinement.png)

The mesh-change criterion is also unmet. From 32 to 64 cells:

- Relative k change is 2.44181e-4, above the declared 1e-4 threshold.
- Conservatively restricted scalar-flux change is 7.06660e-4, below 1e-3.
- Relative axial outflow-current change is 3.13926e-4, below 1e-3.
- The inverse-k difference is -59.4217 pcm, defined as
  `1e5*(1/k_fine-1/k_coarse)`.

The plan requires two successive passing refinements and admissible reference
fields. Neither condition is met. No extrapolated k or “converged reference”
is reported. These differences are properties of this manufactured extrusion,
not D4 reactivity errors.

## Negative source, not negative DD attenuation

The source seen by either axial direction is

\[
 q=S^{phys}\phi+\rho F\phi-C\phi.
\]

For each saved cell and direction, the independent signed reconstruction is

\[
 \psi_{out}=
 \frac{q/2+(\mu/h-\Sigma_t/2)\psi_{in}}
      {\mu/h+\Sigma_t/2}.
\]

Every negative angular entry on the 4–64 cell grids occurs where the incoming
coefficient `mu/h-total/2` is nonnegative. Thus the usual negative DD attenuation
coefficient on optically thick cells does not explain these negatives. They
originate from negative effective sources and can then propagate through a
negative incoming angular field.

For a concrete seed, on the 4-cell mesh at group 61, region 3, the lower vacuum
cell has zero incoming flux and the following signed terms:

| Quantity | Value |
| --- | ---: |
| Physical scattering source | +0.001065912541 |
| Fission source divided by k | 0 |
| Radial term C phi | +0.016444899716 |
| Effective source q | -0.015378987175 |
| Optical ratio `total*h/(2*mu)` | 0.0708462 |
| Reconstructed outgoing angle | -0.062187236473 |

The 64-cell grid still has 2178 negative outgoing entries with nonnegative
incoming flux and nonnegative attenuation; all 2178 are at vacuum inflows.
None of these seeds has a nonnegative effective source. The complete signed
source terms and DD reconstruction checks are saved for all seven meshes;
the largest reconstruction discrepancy is 2.52e-13 relative to the angular
field scale.

This diagnoses a failure of the **chosen isotropic insertion of C into this
axial candidate**. It does not invalidate the previously verified native radial
flight operator R itself. It also does not prove that every possible finer
grid or another angular closure fails. It does rule out treating the present
4–64-cell eigenfields as positive reference solutions or attributing this
failure solely to truncated POD spaces.

## Direction after this result

The immediate reference task is to revisit radial/angular source and current
coupling. Any revised candidate must reproduce the native radial limit and
pass the retained vacuum, optically thin negative-source examples under axial
refinement. Qualify the full-coordinate candidate before training new POD
spaces or choosing a reduced rank. A positive angular discretization alone
cannot make a genuinely negative prescribed source nonnegative; clipping it
would define another equation and conceal the present failure.

The live D4 chain, its rank, equations and acceptance gates are unchanged.
No new production input, shared build or transport map is launched here.

## Verification and reproduction

Twelve standalone tests cover the exact nodal/current identity, full-space
preconditioning and boundary correction, midpoint-mass nullspace, dense-angle
equivalence, fission orientation, global normalization, conservative mesh
restriction and separate negative-source/negative-attenuation controls.

The artifact contains copied sources and inputs, the predeclared mesh plan,
recorded solver-only additions, native dense calibration data and a complete
second numerical run. Final replay and protected-file counts are recorded in
the [verification receipt](../artifacts/native-axial-refinement-20260928/verification.json).
All 25 numerical analysis files replay byte for byte; all 52 numeric arrays
match exactly. Both working and archived test copies pass all twelve tests.
All 997 protected files, nine source inputs and 841 manifest entries from ten
prior artifacts remain unchanged. Verification passes while physical
refinement admission explicitly fails; these are separate outcomes.

Files: [solver](qualify_native_axial_refinement.py),
[source diagnostic](diagnose_native_axial_sources.py),
[mesh comparison](summarize_native_axial_refinement.py),
[tests](test_native_axial_refinement.py),
[plan](../artifacts/native-axial-refinement-20260928/plan.json),
[full results](../artifacts/native-axial-refinement-20260928/analysis/result.json),
[source audit](../artifacts/native-axial-refinement-20260928/analysis/source_audit.json).
