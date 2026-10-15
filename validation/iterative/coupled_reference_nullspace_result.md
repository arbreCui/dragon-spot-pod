# Coupled full-coordinate reference: exact amplitude counterexample

Completed on 2026-09-28. **Refreshing the radial response and shared leakage
does not, by itself, guarantee a unique positive full-coordinate reference.**
Two manufactured S2 vacuum models have an exact positive one-parameter family
after global fission normalization. Their residual Jacobians have one null
direction. Explicit radial exchange removes that direction in the controls.
This is a small-model qualification of the declared closure equations, not a
native Dragon run, D4 Jacobian calculation, or POD-error measurement.

## Declared equations and controls

Each axial plane contains two radial regions: one with nu-fission coefficient
1 and one with coefficient 0. Both have total cross section 2, absorption 1,
and isotropic scattering 1. The radial exchange matrix is

\[
C=\begin{pmatrix}1&-1\\-1&1\end{pmatrix}.
\]

It transfers neutrons between regions without an exterior radial loss.
This is a manufactured radial network, not a discretized D4 MOC operator.
The full radial coordinate basis is used. Each axial cell is its own physical
restriction zone, so the radial source uses that cell's scalar flux directly.
S2 ordinates are mu = +/-1/sqrt(3), with weights 1; incoming angular flux is
zero at both ends. The axial discretization is diamond differencing.

For plane z and region r, the simultaneous radial equations are

\[
(2+L_z)u_{zr}-u_{z,1-r}=\rho f_r\phi_{zr},
\qquad f=(1,0),\qquad \rho=1/k.
\]

The ratio closure and axial equations are

\[
d_{zr}=-1+\frac{\rho f_r\phi_{zr}}{u_{zr}}-L_z,
\qquad
\mu_n\partial_z\psi_{rn}+2\psi_{rn}
+\tfrac12 d_{zr}\phi_{zr}
=\tfrac12\phi_{zr}+\tfrac\rho2 f_r\phi_{zr}.
\]

Scalar flux is the sum of the two cell-averaged angular fluxes. Leakage L is
recomputed from the signed current divergence summed over both radial regions,
divided by their summed scalar flux. There is one global normalization,
sum_z phi(z, fuel) = 1. All cell volumes are 1; an area of 1/h with cell height
h realizes this convention. These are two independently declared examples,
not a physical mesh-convergence comparison.

These definitions retain the source, ratio and leakage relationships in
[method equations (5)–(9)](../../SPOT_doc/rederivation.md). No radial field or
leakage coefficient is frozen during the residual or Jacobian evaluation.
The control changes only the transverse term from d*phi to C*phi, keeping
the same radial residuals, materials, quadrature, boundaries and normalization.
It is an explicit-exchange reference for this network, not a 3D transport
benchmark or a silently modified version of the current production map.

## Exact positive solution families

Let alpha be the non-fission/fission scalar-flux ratio. The closure equations
admit every alpha > 0 in the following families:

| Quantity | One axial cell | Two axial cells |
| --- | ---: | ---: |
| mu/h | 1/2 | 1 |
| Scalar flux in each cell | (1, alpha) | (1/2, alpha/2) |
| Radial field u in each plane | (1, 1/3) | (1/2, 3/16) |
| Shared leakage L in every plane | 1 | 2/3 |
| k | 3/8 | 24/55 |
| Unknowns, including rho | 7 | 13 |
| Ratio-closure Jacobian rank at each sampled alpha | 6 | 12 |
| Explicit-exchange reference alpha | 1/3 | 3/8 |
| Explicit-exchange Jacobian rank at its solution | 7 | 13 |

For the one-cell case the fuel outgoing angular fluxes are both 1. For the
two-cell case every non-vacuum fuel angular face value is 1/3. Multiply those
values by alpha for the non-fission column. Substitution verifies every
equation for arbitrary positive alpha; the implementation retains exact
rational residuals and Jacobians at alpha = 1/4, 1/2 and 1.

In particular, the two-cell non-fission scalar flux can be 1/8 or 1/4 in
each cell, with identical k, radial fields and leakage, zero residuals and
positive scalar and non-vacuum angular fields. Thus positivity and one global
normalization do not remove the ambiguity. The exact Jacobian null vector
changes only non-fission angular amplitudes; it changes neither u, the fuel
angular field, nor rho. The global normalization has already removed the
usual common-amplitude freedom.

The mechanism is explicit: in the non-fission region d = -1 - L, independent
of that region's axial amplitude. Both columns have the same axial shape in
these examples, so the shared current/flux ratio L is also independent of
their relative amplitude. The radial equations determine u but supply no
remaining equation matching the non-fission axial amplitude to that u.

## Whole-domain neutron balance distinguishes the solutions

With no exterior radial loss, the explicit network requires absorption plus
axial boundary outflow to equal rho times normalized fission production.
At alpha = 1/2, the ratio-closure solutions instead give:

| Global quantity | One cell | Two cells |
| --- | ---: | ---: |
| Absorption | 3/2 | 3/2 |
| Axial boundary outflow | 3/2 | 1 |
| Fission source rho | 8/3 | 55/24 |
| Absorption + axial outflow - fission source | 1/3 | 5/24 |
| Summed ratio-closure transverse term | -1/3 | -5/24 |

The closure equations balance because their summed transverse term cancels
the discrepancy. Physical internal exchange C*phi always sums to zero and
cannot provide that net source. At the explicit-exchange reference alpha,
both the physical balance defect and net transverse term are exactly zero.
Hence identical k and even zero closed-equation residuals can conceal an
incorrect reflector amplitude and whole-domain balance in these examples.
This is not a measurement of D4's balance defect.

## What the controls establish

The explicit-exchange reference has positive scalar flux, zero residuals,
zero global physical balance defect and a nonsingular normalized Jacobian
at each reported solution. That establishes local regularity there, not
global uniqueness for arbitrary input data.

As a separate diagnostic, appending phi(non-fission) = u(non-fission) in
each plane also removes this null direction at the reference: the augmented
Jacobians have full column rank 7 and 13, with 8 and 15 equations respectively.
These extra constraints are absent from production. Their success in these
special examples is not justification for appending them to a general model;
they could be incompatible or overdetermine other configurations.

## Decision and remaining scope

The blanket assumption that a coupled full-coordinate solve necessarily
provides a unique physical truth is disproved by these examples. More
iterations, a Newton solver, or a different normalization cannot establish
the missing relative amplitude without addressing the equations.

Before another long D4 full-coordinate run, qualify a reference formulation
that retains radial exchange and determines active-region amplitudes. The
next bounded model checks should vary axial material shape and introduce
intergroup scattering, checking positivity, normalized Jacobian rank and
physical balance together. An explicit-exchange formulation changes the
closure and must be labelled accordingly; a same-closure reference remains
unqualified until its admissibility is established for the case in question.

The existing fixed-space reduced method and its running coupled chain keep
their scope and acceptance rules. These results do not prove a null direction
in actual multigroup D4, universal degeneracy, or attribution of the CE gap.
A POD space can constrain relative amplitudes in the examples, so increasing
rank is not automatically a clean measurement of truncation error.

## Reproduction and retained evidence

The standalone [qualification program](qualify_coupled_reference.py) uses
only Python's standard library: rational arithmetic, exact forward derivatives
and rational row reduction. There is no eigensolver stopping criterion, SVD
rank tolerance, fitted coefficient or positivity repair. Seven focused tests
check the positive families, null direction, both controls, physical balance
and the full two-cell Jacobian against independent central differences.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 validation/iterative/test_coupled_reference_qualification.py
PYTHONDONTWRITEBYTECODE=1 python3 validation/iterative/qualify_coupled_reference.py /tmp/spot-reference-new-output
```

The output directory must not already exist.
`validation/artifacts/coupled-reference-nullspace-20260928/` retains the
declared plan, exact residuals and matrices, source copies, test receipt and
file hashes. Protected source/runtime/input files and all four earlier map-6
diagnostic manifests are independently checked. No transport run or production
change was required.
