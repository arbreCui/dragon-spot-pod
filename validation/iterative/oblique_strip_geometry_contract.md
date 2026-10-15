# Actual axial crossings in an extruded ray strip

The [exact full-flight comparison](exact_native_flight_result.md) qualifies a
complete zero-gradient exact-kernel companion and measures its difference
from the native table operator. The next step introduces **actual geometric
crossings of axial cells**, initially in manufactured one-/two-material ray
strips. No full native geometry or multigroup problem is admitted by this step.

## Transport geometry and measures

Let `s` be physical path-scaled distance along an oriented planar ray, with
`0<=s<=S`, and let `0<=z<=H`. Native usage will later retain
`s=planar_distance*ZMU`. The signed axial direction is `mu`; transport obeys

```
dpsi/ds + mu*dpsi/dz + sigma_t(s,z)*psi = q(s,z)
u = z - mu*s                  # invariant along an oblique characteristic
```

Use the full source cell coordinate `(radial segment, axial cell)` and keep
the two axial signs independent of planar orientation. Reverse planar travel
by reversing material/source segment order; do not reverse the axial sign.

For positive mu, incoming chords have `-mu*S <= u <= H`. Chords with `u>=0`
enter at `s=0,z=u`; those with `u<0` enter at `s=-u/mu,z=0`. The exit is the
first intersection with `s=S` or `z=H`. Negative mu uses the corresponding
top-incoming/bottom-outgoing construction. Handle mu=0 explicitly.

Split each chord at every radial material interface and axial plane. On each
piece apply the qualified positive exact T/B/D integrals with the declared
constant cell source. Share the same angular amplitude at each internal
crossing; retain the signed contribution on both neighboring cell ledgers.
Do not exponentiate a regional scalar inverse or insert a finite-difference
axial generator into the radial characteristic.

The mapping `(s,u)->(s,z)` has unit Jacobian. Volume integration uses
`du * integral(psi ds)`. Radial boundary current uses `du=dz`; axial boundary
current uses `abs(du)=abs(mu)*ds`. These measures must arise from geometry,
without a fitted area, current or flux correction.

## Positive quadrature with known topology changes

For radial interfaces `s_k` and axial planes `z_j`, construct and sort all
offset breakpoints `u=z_j-mu*s_k`, including domain corners. Within each
offset interval the chord topology is fixed. Apply Gauss-Legendre quadrature
with positive weights separately on every interval, at fixed orders
2, 4, 8 and 16. Retain interval endpoints, nodes, weights, entry/exit identities,
piece lengths and source-cell indices; discard only exactly zero-length
geometric pieces. Coincident-interface conventions must be deterministic.

This is an explicit new spatial quadrature. The older native transverse-ray
weights are not adjusted to absorb axial quadrature error. The first experiment
uses unit strip weight; the future native bridge must retain the original
radial weights and compare geometric and stored-normalizer ledgers separately.

## Fixed manufactured controls

Use strip lengths S=1 and 3 cm, heights H=1 and 20 cm, axial signs
`+/-1/sqrt(3)` plus a mu=0 limit, and axial grids 1/2/4/8/16 cells. Include
one material and two equal radial segments. Keep all prescribed input and
comparison cases enumerated in a frozen plan before running.

1. **Geometry and constant solution.** Verify every cell's accumulated volume
   against its rectangular area and each boundary measure against its
   geometric length/current measure. Boundary psi=1 and cell source
   q=sigma_t must give psi=1 for any chosen positive piecewise material,
   including void cells. Reversing signs/material order must preserve the
   expected geometric reflection.
2. **Homogeneous vacuum source.** Totals 0, 0.02, 0.2 and 2 per cm, q=1.
   For positive mu, the incoming-flight distance at a point is
   `ell=min(s,z/mu)`; replace z by H-z for negative mu and use ell=s for
   mu=0. The exact angular field is `(1-exp(-sigma*ell))/sigma`, with the
   void limit ell. Derive independent cell and boundary integrals by splitting
   at `z=abs(mu)*s`; do not use the candidate offset quadrature as its own
   accuracy reference. Compare every cell mean and each outward face current.
3. **Zero-gradient full-flight control.** In the one-/two-material ray, use
   incoming axial values supplied by its independently computed 1D exact
   flight at that s. Constant axial source/inflow then reproduces the
   complete 1D flight across all axial cells. This is manufactured matched
   inflow, not a vacuum or periodic axial boundary claim.
4. **Input response cone and nonuniform source.** Apply every cell-unit
   source and each declared piecewise-constant incoming radial/axial boundary
   unit. Check all amplitudes, integrals and outgoing face currents without
   clipping. Also use a fixed alternating 0/1 source across axial cells in
   the two-material strip (totals 0.2 and 2 per cm). Record its 8→16 quadrature
   changes separately from analytic true errors. No scattering feedback or
   white-return closure is added in this first geometry test.

## Predeclared gates and scope

Freeze the full finite case matrix, source/current scales and zero-output
handling before computation. Geometry/constant-solution, independent 1D
recovery, reflection and shared-face checks use `5e-12`; raw per-cell and
global exact balance use `1e-10`; physical responses require strict
nonnegativity. At order 16, the homogeneous analytic cell-mean and outward
current errors must be below `1e-8` on the declared source-induced scales.
Report all quadrature orders; retain failures without adding more orders or
relaxing limits. The heterogeneous last-pair change is a quadrature diagnostic,
not a true-error bound or an axial mesh-convergence claim.

Use one numerical thread, a 512 MiB cap and 600 seconds per process. Batch
offset nodes or source columns while retaining every coordinate. Archive
source snapshots, geometry/response fields, primitive and shared-face ledgers,
failed controls, resource measurements and a fresh-directory replay.

Passing qualifies this geometric prototype only. A subsequent native-track
bridge must still recover the qualified exact full-flight companion, retain
native radial measures and all angular/sign states, solve common radial white
return, and revisit the recorded finite-axial-mesh failures. Original native
table partition equality remains failed. Live D4 inputs, production sources,
shared libraries, multigroup/fission eigenproblems and POD training remain
outside this experiment.
