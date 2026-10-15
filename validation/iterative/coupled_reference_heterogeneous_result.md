# Heterogeneous and multigroup coupled reference qualification

Completed on 2026-09-28. The previous amplitude ambiguity is **not confined
to a homogeneous one-group example**. Axial material variation can retain
the free amplitude, and an asymmetric two-group example retains it exactly.
Other tested variations remove the null direction but lead the bounded solve
toward an inadmissible zero-reflector root. A full-rank Jacobian and a small
equation residual are therefore insufficient qualification on their own.

The explicit conservative-exchange control passes positive-flux, normalized
local-rank and physical-balance checks in all six declared networks. It is
qualified as a reference for these networks only. No D4 transport, production
solver change, or new active coupled map was performed.

## Equations, inputs and bounded procedure

All examples use two radial regions, S2 vacuum ends, diamond differencing,
unit cell volumes and one physical restriction plane per numerical cell.
Region 0 produces fission; region 1 has identically zero nu-fission. With
S[g,h] denoting scattering **from h to g**, the simultaneous radial equation is

\[
(\Sigma_{t,zrg}+L_{zg})u_{zrg}
+c_{zg}(u_{zrg}-u_{z,1-r,g})
-\sum_h S_{zrgh}u_{zrh}
=\rho\chi_g\sum_h\nu\Sigma_{f,zrh}\phi_{zrh}.
\]

The ratio response retains off-group radial scattering and the frozen
fission source:

\[
d_{zrg}=-\Sigma_{t,zrg}+S_{zrgg}-L_{zg}
+\frac{\sum_{h\ne g}S_{zrgh}u_{zrh}
+\rho\chi_g\sum_h\nu\Sigma_{f,zrh}\phi_{zrh}}{u_{zrg}}.
\]

The axial equation is mu*d(psi)/dz + total*psi + d*phi/2 =
sum_h S[g,h]*phi[h]/2 + rho*chi[g]*sum_h nu-fission[h]*phi[h]/2.
Shared L is recomputed for each plane/group from the signed current divergence
and scalar flux summed over both radial regions. One global nu-fission
normalization is imposed, with no regional/group normalization.

The explicit-exchange control replaces d*phi with
c*(phi(region 0) - phi(region 1)) in region 0 and the opposite in region 1.
Thus its radial transfer sums to zero. Its axial problem is a linear network
eigenproblem; the radial field is then solved with its returned L and source.
The control no longer feeds a scalar response derived from u into the axial
equation. **This changes the transverse closure**, not just the nonlinear
solver, and is not a native three-dimensional transport reference.

| Case | Declared variation |
| --- | --- |
| H1 | One group, two cells, mu/h=2; total=2, absorption=1, c=1 everywhere. |
| H2 | H1 with second-plane total=2.5; second-plane absorption=(1.2, 0.9) in fuel/reflector. Within-group scattering is total minus absorption. |
| H3 | H2 plus 0.25 to reflector total and self scattering, preserving absorption. |
| G1 | Two groups, one cell, mu/h=0.5; fuel total=(2, 2.5), reflector total=(2.25, 2.75); self scattering=(0.5, 0.5), downscatter=0.3, upscatter=0.1, c=(1, 0.75). |
| G2 | Two groups, two cells, mu/h=2; total by plane=(2, 2.5)/(2.25, 2.75), equal across radial regions; self scattering=(0.5, 0.75), downscatter=0.3/0.4 and upscatter=0.1/0.15 by plane; c=(1, 0.75). |
| G3 | G2 plus 0.25 to reflector total, retaining scattering. |

Fuel nu-fission is 1 for one group or (1, 0.5) for two groups; chi is 1 or
(0.75, 0.25). The full arrays, including the scattering orientation, are saved.
These inputs were declared before solving and are not fitted to D4 or CE.
They form controlled network examples, not an axial mesh-convergence study.

For each case, first solve the linear explicit-exchange eigenproblem. Then
start the ratio equations from that reference with reflector angular fields
scaled by 0.5, 1 or 2. Radial fields are simultaneous unknowns. The declared
nonlinear procedure permits at most 60 Newton least-squares steps, with at
most 20 step halvings, and requires positive u, rho and non-vacuum angular
fields at trial steps. No clipping, floor or matching constraint is used.
The residual stopping threshold is 1e-11. `RESIDUAL_MET` records only that
stopping condition; it is not an accepted physical reference.

Jacobians use complex-step differentiation. Numerical ranks are recorded at
relative singular-value thresholds 1e-8, 1e-10 and 1e-12; all three agree in
these results. An independent rational calculation supplies exact residuals,
Jacobian ranks and null vectors for G1. Numerical rank elsewhere is not an
exact theorem about all parameter choices.

## Positive amplitude families survive two extensions

H1 and H2 have numerical ranks 12/13 at their positive solutions. In H2,
all three seeds reach residuals below 9e-16 in three steps, with identical
k=0.29631391279359365 and plane leakage=(1.6488577193, 1.4714110592).
The reflector fluxes remain different. Scaling the reflector of a computed
solution again by 0.5 or 2 independently reproduces the zero residual and
unchanged leakage. Axial material variation has not determined this amplitude.

G1 has the exact eigenvalue

\[
k=\frac{7797115}{27866694}.
\]

Scaling **both reflector energy groups together** by any positive multiplier
preserves its coupled equations, global normalization and leakage. The
rational checks at multipliers 1/2, 1 and 2 have exact zero residuals and
rank 12/13. The explicit-exchange reference has exact rank 13/13. Asymmetric
up/downscattering constrains the group relation but does not eliminate the
reflector's common amplitude freedom in this example.

## Other variations reach the zero-reflector boundary

All nine ratio attempts for H3, G2 and G3 meet the declared 1e-11 residual
threshold after 25–30 steps, with positive but tiny reflector flux. To resolve
whether these are usable positive solutions, a separately declared follow-up
sets reflector angular fields exactly zero in a **new diagnostic candidate**
and solves only the remaining equations. Original attempt states are retained.
The omitted reflector equations are checked as part of the final full residual.

All six such diagnostic candidates have full residuals below 9e-16. H3, G2
and G3 have full numerical Jacobian rank at this boundary. They are explicitly
labelled `INADMISSIBLE_ZERO_REFLECTOR_BOUNDARY_ROOT`: radial reflector u remains
positive, but its axial scalar flux is identically zero. They cannot satisfy
the existing positive active-domain requirement.

The table uses the seed multiplier 1 for the finite stopping receipts.
Physical balance defect is (absorption + vacuum outflow - rho*production)
divided by rho*production; negative means an apparent net loss through the
summed transverse closure in these radially closed networks.
Reactivity difference is 1e5*(1/k_reference - 1/k_ratio), in pcm.

| Case | Rank / unknowns near boundary | Minimum scalar flux at residual stop | Relative physical balance defect | Scalar-flux L2 difference from explicit exchange | Reactivity difference |
| --- | ---: | ---: | ---: | ---: | ---: |
| H3 | 13/13 | 7.83e-11 | -21.183% | 27.641% | -271.252 pcm |
| G2 | 25/25 | 5.07e-10 | -19.186% | 23.268% | -0.223779 pcm |
| G3 | 25/25 | 1.80e-10 | -19.474% | 22.161% | -218.584 pcm |

Each finite state is within 1.1e-9 in maximum component distance of its
separately solved zero-reflector boundary state. The G2 result is especially
instructive: k differs by only about 0.224 pcm while reflector flux is nearly
absent and physical neutron balance is wrong by about 19%. These percentages
describe the manufactured networks and **are not D4 error estimates**.

This behavior is compatible with the algebra: if every angular/group flux
in a non-fission region is zero, its local scattering, ratio*phi and streaming
terms all vanish. Updating the radial coefficients does not introduce an
additive inter-region source into that axial equation. Explicit exchange
does introduce such a source from the neighboring region. This explains why
the zero-reflector subspace can persist even with radial/leakage feedback.
The experiments do not prove that there are no other positive roots.

## Reference qualification and next decision

Every explicit-exchange control has positive u, scalar flux and non-vacuum
angular flux; maximum equation residual below 9e-16; relative physical-balance
defect below 5e-16; and full normalized Jacobian rank. The smallest/largest
singular-value ratios range from 0.0472 to 0.1025. G1 also has the exact
rational rank check. These are local qualifications of the six declared
networks, not a global uniqueness/positivity theorem.

Adding regional mean-matching constraints to the current closure is still
not justified. In the H2 family, matching reflector phi to radial u in each
plane would require two different reflector/fuel ratios, approximately
0.274058 and 0.296612. A common amplitude cannot satisfy both. This is a
concrete reason to derive compatible equations instead of appending the
constraint that happened to work in the previous uniform examples.

For the next reference milestone, keep conservative radial transfer explicit
and define its projection into the fixed POD space. Compare reduced and full
solutions of that **same** candidate operator to isolate projection error;
compare the candidate with the existing ratio formulation separately to
measure the change in closure. Mapping this network result to a native radial
transport operator still requires an operator derivation and verification.
The diagonal response at one anchor alone does not supply that operator.

The existing D4 chain, original acceptance thresholds and production method
remain unchanged. These checks neither invalidate every reduced configuration
nor quantify the actual D4 nullspace or CE gap. They establish why a larger
POD rank, a new nonlinear solver or k agreement alone cannot qualify the
desired full-coordinate reference.

## Reproduction and evidence

The [standalone program](qualify_coupled_reference_extended.py) needs Python
and NumPy; it reuses exact arithmetic helpers from the
[previous qualification](qualify_coupled_reference.py). Eight focused tests
pass: old-model equivalence, off-solution neutron balance, all six reference
checks, exact asymmetric multigroup control, independent finite-difference
Jacobian verification, axial amplitude freedom, boundary-root rejection and
invalid-input rejection. This standalone scientific check does not add a
NumPy dependency to the existing fast-test runner.

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 validation/iterative/test_coupled_reference_extended.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 validation/iterative/qualify_coupled_reference_extended.py /tmp/spot-heterogeneous-new
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 validation/iterative/qualify_coupled_reference_extended.py --boundary /tmp/spot-heterogeneous-new/summary.json /tmp/spot-boundary-new
```

Output directories must be new. Artifacts under
`validation/artifacts/coupled-reference-heterogeneous-20260928/` preserve the
original plan, follow-up plan, all 18 stopping receipts, exact control,
boundary diagnostics, comparison, source copies and test/replay receipts.
The 997 protected source/runtime/input files and all five earlier diagnostic
manifests are checked without modification. No shared build is required.
