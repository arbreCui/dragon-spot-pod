# Next reference milestone: transport through radial segments and axial cells

The [signed-state experiment](native_signed_axial_result.md) qualifies an
explicit axial-sign extension at zero axial variation. It also shows that
separate sign returns can alter axial current by 44–181% while leaving scalar
flux unchanged to roundoff. The next private experiment must transport the
retained directional state across axial cells. It must not introduce a regional
inverse-H propagator or another reduced eigenproblem.

## Proposed full-state segment operator

For each ray, polar node, planar orientation and independent axial sign, retain
a vector Psi of axial-cell values as a function of distance ell along the
planar characteristic. Here ell equals planar distance times native ZMU.
Use the declared unit direction from the signed-state experiment.

At a fixed radial segment with physical total sigma, define the candidate

```
A = sigma*I + abs(mu_z)*D_up
dPsi/dell + A*Psi = q
```

`D_up` is the axial finite-volume upwind derivative: diagonal `1/h_i`, upstream
neighbor coefficient `-1/h_i`, and the upstream side selected by axial sign.
Top/bottom vacuum boundaries supply zero incoming flux. Positive prescribed
axial inflow is a separate boundary source. Use a periodic axial control to
test the constant mode `D_up*1=0`. Reversing the planar orientation reverses
radial segment order only.

Keep the axial vector inside the characteristic solve. Replacing its along-ray
variation by a single regional average before applying axial removal/source
terms can change the zero-gradient radial solution and must be rejected if it
fails the existing calibration.

## Exact and native-compatible coefficient controls

First implement a separate exact-exponential companion:

```
T(A,L) = exp(-L*A)
B(A,L) = integral_0^L exp(-s*A) ds
D(A,L) = integral_0^L (L-s)*exp(-s*A) ds

Psi_out = T*Psi_in + B*q
integrated_Psi = B*Psi_in + D*q
```

Use integral/block formulations that remain defined for zero total and singular
periodic streaming operators. Check segment balance and both directional
orders against independent scalar analytical cases. The exact companion is a
distinct numerical kernel; its difference from native tabulated coefficients
must remain visible.

The following native-compatible coefficient lift is a **candidate to test**.
Let `B_n,D_n` be the already extracted positive native scalar coefficients for
the same sigma and L, and `T_n=1-sigma*B_n`. Let `B_0,D_0` be the exact scalar
integrals at that sigma and L. Define

```
T_c = T_n * exp(-L*abs(mu_z)*D_up)
B_c = (B_n/B_0) * B(A,L)
D_c = (D_n/D_0) * D(A,L)
```

These factors are determined solely by native segment coefficients. They are
not fitted to k, source responses or target currents. For a periodic constant
axial mode they recover the native T, B and D. Positive scalar factors and
positive transport integrals provide a concrete positivity hypothesis to
check. The lift does change the finite-mesh kernel: disclose it explicitly and
measure its segment and global balance defects. Do not correct those defects
afterward or loosen the existing native-action tolerance to admit a failure.

Compare the exact and lifted operators before choosing either for a full
reference. Keep the known PJJ rounding remainder separate in zero-gradient
native calibration; do not distribute it among angles or infer additional
nonuniform-axial rounding corrections from the stored P0 record.

## Bounded execution and gates

Start with one- and two-region analytical segments, then the frozen groups
51, 61 and 98. Use small axial meshes (1, 2, 4 and 8 cells), vacuum axial
inflow and periodic constant-mode controls. Remain in the full retained
radial/directional state, without multigroup scattering, fission or POD.

For each boundary surface and axial cell, native radial white return must sum
all outgoing polar nodes, planar orientations and axial signs before setting
one common incoming amplitude. Test vacuum radial boundaries first, then this
coupled boundary solve. Preserve native volume/surface measures and their
known rounding discrepancy.

Require nonnegative external volume and boundary-input response, native
zero-gradient scalar and boundary recovery at 5e-12, even/odd moment ledgers,
axial current continuity, and disclosed raw balance defects. Freeze balance
and spatial-convergence thresholds before the first numerical run. Compare
exact versus lifted coefficient errors separately from axial mesh error.
Passing only a scalar or global-k check cannot admit the candidate.

Only after these prescribed-source checks may an eventual full-coordinate
multigroup/fission reference be proposed. The saved group-61 vacuum and
group-51 fine-mesh failures remain regression targets. Live D4 runs, production
source, shared libraries and rank choices remain outside this experiment.
