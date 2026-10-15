# Next reference milestone: retain and qualify directional response

This is the next bounded research specification after the
[source/current audit](native_source_current_result.md). It is not a production
change or a claim that the proposed angular reference already exists.

## What the current scalar data establish

The saved native response R and outgoing-current functional describe a steady
P0 source-to-region-average problem. They have been checked against native MOC
flights and their raw balance defect has been retained. They do not identify a
unique angular or axial propagation law.

Two attempted uses are now insufficient as reference specifications:

- `C*phi/2` in both axial directions yields negative full-space angles under
  mesh refinement, while leaving the odd-moment equation without radial action.
- Replacing that term by `C*psi_plus` and `C*psi_minus` would add `C*J` to the
  odd equation, but the resulting source-free H propagation has certified
  negative outputs for nonnegative inputs in all 370 groups.

The next study must retain information discarded by scalar averaging. Do not
infer that information from R, fit it to a target eigenvalue, clip signed terms,
or replace native H by a graph generator as an undocumented repair.

## Native implementation facts to preserve

The read-only inspection identifies concrete extraction points:

- `MCGFFIR` carries `RP` and `RM` along the two orientations of an individual
  track, then accumulates their contributions into the regional scalar vector.
  These are track directions; they are not automatically the axial S2 signs.
- `OMEGA2` stores squared direction components. Squared components alone cannot
  recover a signed axial angular moment. The quadrature/track orientation and
  sign conventions must be established before assigning a signed axial label.
- With source-term isolation enabled, `F0=B*RP` is only the isolated accumulated
  contribution. `MCGFST` divides by the native volume/surface weights and adds
  the stored PJJ source contribution. An export of F0 alone is not the full
  segment or regional angular flux.
- The native TIBERE `IDIR`, `PJJZ` and related terms are potential sources of
  current-response information. Availability and their defining equations must
  be audited first; they must not be equated to a signed half-range response
  merely because a record name contains Z.

## First executable scope

Use private copies of the previously frozen pin, libraries and ray data.
Start with groups 51, 61 and 98, which provide retained angular-source or
generator counterexamples. No shared build, live D4 source, control or map is
changed. Before requesting any new eigenproblem:

1. Establish the exact mapping from a native track/quadrature sample to oriented
   direction components, physical segment, source normalization and integration
   weight. Record which independent angular inputs the current P0 interface can
   represent. Missing source directions require an explicit private extension,
   not an invented interpretation of the P0 field.
2. Retain source-to-track/segment and source-to-boundary information before
   regional angular summation, including the self-source contribution. Verify
   a single-segment analytical solution and both track orientations.
3. Aggregate the retained state back to the existing scalar R and boundary
   functional for all radial unit sources and the previous held-out sources.
   Require the existing action tolerance, preserve the native weights and keep
   the raw balance defect visible.
4. Specify paired directional excitations whose even parts agree and whose odd
   parts differ. Identify the native odd/current response from those data;
   do not choose it by setting an unmeasured operator equal to H or total.

This milestone ends with an audited directional response interface and its
aggregation tests. It need not solve the eventual coupled eigenproblem.

## Admission for a later coupled model

A subsequent coupled operator must declare its retained directional state,
source exchange and boundary-current functionals. Its zero-axial-variation,
steady isotropic limit must recover the native radial response. It need not
force the old `C*phi` action onto every nonuniform axial field: that would impose
the rejected closure in advance.

Qualify positive external unit-source and boundary-inflow response, even/odd
moment consistency and global current balance before introducing the signed,
transport-corrected multigroup scattering and original fission coefficients.
Then qualify the normalized full-coordinate eigenmode, local uniqueness and
mesh/angular refinement. The group-61 vacuum example and the group-51 fine-mesh
negative seeds remain mandatory counterexamples to revisit.

Only admitted full references may be used to measure POD error. No rank is
selected by agreement with CE or by global k alone. The direction of the live
SPOT method and its D4 acceptance requirements remain governed by their
existing definitions, independently of this reference-development track.
