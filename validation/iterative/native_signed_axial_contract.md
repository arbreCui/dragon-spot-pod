# Next reference milestone: explicit signed axial state

The [planar directional extraction](native_directional_response_result.md)
recovers the native scalar and boundary responses and identifies a planar
x-current response. It does not recover an axial odd mode from the original
P0 data. This specification defines the next private extension, without
claiming it already exists or admitting another coupled eigenproblem.

## State and calibration

1. Keep the retained ray, polar node, planar orientation and segment as state.
   Introduce an independent axial sign `zeta=+1/-1`. Reversing planar travel
   must not reverse `zeta` by definition.
2. Split each existing planar-state quadrature weight equally between the two
   axial signs. Preserve native B, D, source normalization and the separately
   disclosed PJJ rounding ledger. In the zero-axial-gradient, isotropic-source
   limit, summing both axial signs must reproduce the qualified native planar
   response and the native rounded scalar response to its existing tolerance.
3. Specify the axial direction magnitude and precision convention before
   computing sources or moments. The native CPO magnitude and
   `sqrt(1-1/ZMU**2)` differ by rounding. A convention must be documented and
   its relation to path length and direction normalization checked; do not
   silently mix them or treat the sign of stored CPO as the missing state.

## First experiment: prescribed sources, no axial propagation

Use the same frozen groups 51, 61 and 98. At zero axial variation, exercise
nonnegative pairs of directional sources with equal even parts and opposite
axial odd parts. Use the native two-orientation characteristic kernel with
the declared extra sign state; measure the axial current moment from actual
retained amplitudes. Compare direct segment flights with aggregation and
check linear parity, units, positive unit-source response and raw balance.

Specify radial white-boundary redistribution on the full angular state. A
diffuse white boundary uses the total outgoing current to set an isotropic
incoming amplitude; its return must mix axial signs consistently. Closing each
axial sign independently would preserve directional information that a white
boundary discards and would define a different boundary model. Check vacuum
and white cases independently. Axial odd amplitudes and even scalar averages
must remain separately observable throughout the calculation.

The result is a response of an explicitly declared signed-state extension.
It must not be described as a uniquely reconstructed axial law from the saved
P0 matrix. Distinguish native-kernel checks from assumptions introduced by the
new source/sign/boundary interface.

## Conditions before adding axial variation

After these checks, declare how positive transport along a physical direction
crosses both radial segments and axial cells, including top/bottom vacuum
boundaries and the region/angle averages used for source exchange. The axial
odd response just measured is a calibration target, not by itself an axial
generator. Do not exponentiate the scalar regional inverse H or equate the
odd operator with H or total by assumption.

Test nonnegative volume and boundary inputs, zero-gradient native recovery,
even/odd moments, current continuity and raw balance in the full retained
space. Only then introduce the original signed multigroup scattering and
fission coefficients. Revisit the saved group-61 vacuum and group-51 fine-mesh
counterexamples, and qualify full-coordinate mesh/angular refinement before
POD error or rank selection. Live D4 calculations remain a separate workstream.
