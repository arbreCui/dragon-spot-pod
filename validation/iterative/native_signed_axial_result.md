# Signed axial state: zero-gradient response and white-boundary mixing verified

An explicit, independent axial sign has been added to the retained native
ray/polar/planar-direction state in a private diagnostic. Its zero-gradient
source and boundary responses are verified against unchanged native transport
kernels. **This admits the declared zero-gradient interface, not axial
propagation or a new coupled eigenproblem.**

The important counterexample is a boundary model that returns the two axial
signs separately: it leaves scalar flux unchanged to roundoff but changes the
axial current response by 44–181%. Agreement in scalar flux alone cannot
establish correct directional transport.

Evidence: [artifact](../artifacts/native-signed-axial-state-20260929/README.md),
[predeclared plan](../artifacts/native-signed-axial-state-20260929/plan.json),
[numeric results](../artifacts/native-signed-axial-state-20260929/analysis/result.json),
[verification](../artifacts/native-signed-axial-state-20260929/verification.json).
The experiment implements the [signed-state contract](native_signed_axial_contract.md)
after the [planar extraction](native_directional_response_result.md).

## Declared extension

The state is `(ray, polar node, planar orientation, axial sign, segment)`.
The axial sign is independent of reversing the planar ray. Each sign receives
half the former planar integration weight, giving 181,824 oriented states and
1,757,376 interior segment samples per group. The source is constant inside a
radial segment at a specified angular state, with no axial spatial variation.

The direction convention is fixed before source generation:

```
Omega_x = planar_sign * CAZ1 / double(ZMU)
Omega_y = planar_sign * CAZ2 / double(ZMU)
Omega_z = axial_sign * sqrt(1 - 1/double(ZMU)**2)
```

This preserves the existing path length `ell=planar_length*ZMU` and unit
direction to 2.22e-16. The four positive axial magnitudes are approximately
0.183434286, 0.525532400, 0.796666501 and 0.960289831. They differ from the saved
CPO magnitudes by at most 3.50e-7. The saved negative CPO representatives are
preserved as input evidence; their sign is not treated as a missing physical
up/down degree of freedom.

The native `MCGFFAR` kernel receives explicit segment sources and boundary
inflows for each sign/polar state. Both planar orientations use the same
independently chosen axial sign. Native `MCGDSCA` independently recalculates
the own-source integral D. Its weighted contribution completes the native
isolated flux. The retained B/D recurrence supplies a separate calculation
for comparison with each native half-sign/polar result.

The unrounded directional state determines the axial moment
`Jz=sum(Omega_z*weighted_segment_integral)/V`. The known regional PJJ rounding
remainder is used only for the original P0 calibration. It is not assigned to
axial current or distributed over angular unit sources.

## Cases and checks

Each of groups 51, 61 and 98 has 216 prescribed flights:

| Cases per group | Purpose |
|---:|---|
| 31 | Previous isotropic open and white-return source patterns |
| 64 | Unit volume sources: 2 signs × 4 polar nodes × 8 regions, vacuum inflow |
| 48 | Unit angular boundary inflows: 2 signs × 4 polar nodes × 6 surfaces |
| 64 | The same unit volume sources with common white return |
| 3 + 3 | Opposite axial odd sources and their even anchor, vacuum and white |
| 3 | Same sources with deliberately separate sign returns |

Thus all 648 flights receive fresh native evaluation. Of these, 642 have
nonnegative prescribed volume sources and inflows, including the nine
different-boundary controls. All their retained incoming/outgoing amplitudes
and full segment integrals are nonnegative; native half-state integrals and
outgoing responses are nonnegative as well. The remaining six signed legacy
diagnostics are retained without clipping. There are 633 nonnegative cases
using the admitted boundary definitions and nine positive different-model
controls.

| Group | Maximum half-state action error per case | Original P0 calibration error per case | Raw even/odd balance error | White closure error |
|---|---:|---:|---:|---:|
| 51 | 1.47e-14 | 1.42e-14 | 1.31e-7 | 2.34e-15 |
| 61 | 1.55e-14 | 1.38e-14 | 1.34e-7 | 3.19e-15 |
| 98 | 2.53e-14 | 1.29e-14 | 1.50e-7 | 2.06e-15 |

All pass the declared 5e-12 action/closure and 1e-6 raw balance thresholds.
The separately aggregated native Jz comparison is within 4.64e-14 relative.
The original 93 isotropic scalar and boundary cases are recovered, including
their separate scalar rounding completion; their axial current is zero.

For general angular sources, balance uses actual half-angle ray measures.
The even ledger is source + inflow - collision - outflow. The odd ledger
weights each term by Omega_z. Each defect is divided by the sum of absolute
angular source/inflow contributions, with the same angular weight in the odd
case. Native tabulation and stored-weight discrepancies are retained.

## White return and the current counterexample

At each radial surface, correct native white return sums the outgoing current
over all planar orientations, polar nodes and axial signs, then divides by the
stored surface weight. This sets **one incoming amplitude shared by every
angle**. A six-surface linear solve closes the boundary. Its common boundary
block independently reproduces the previously saved native Tbb.

The source pairs are

```
q(r,Omega) = 1 + s*Omega_z*r/16,     s=-1,0,+1; r=1..8
```

Their even source is identical, and every source remains positive. Common
white return has zero incoming axial odd moment. Consequently, at zero axial
variation its response to the source's odd part equals the vacuum odd
response. The measured identity holds within 6.70e-14 relative, with the
incoming odd boundary moment below 2.31e-16. These are checks of the declared
extension, not an axial law inferred from scalar H.

In the different-model control, each sign instead returns its own outgoing
current divided by half the stored surface weight. This preserves directional
memory that common white return discards. It is deliberately excluded from
the admitted boundary definition.

Let J denote half the difference between the responses to s=+1 and s=-1.
The reported change is `norm(J_separate-J_white,inf)/norm(J_white,inf)`.

| Group | Correct white J infinity norm | Separate-sign J infinity norm | Current change | Scalar flux difference |
|---|---:|---:|---:|---:|
| 51 | 0.115576 | 0.302034 | 181.02% | 2.54e-15 |
| 61 | 0.114872 | 0.257921 | 140.82% | 2.58e-15 |
| 98 | 0.110396 | 0.147214 | 44.20% | 3.42e-15 |

Full regional current vectors and boundary moment ledgers are archived. The
separate-sign return introduces incoming axial moments as large as 0.191675,
0.153164 and 0.055034 respectively. This is a controlled boundary-model
counterexample; it is not evidence that a live D4 routine uses that boundary.

The native stored-surface ledger closes within 4.45e-16 absolute. The actual
geometric boundary measure gives an uncorrected net-current discrepancy up to
1.44e-7, consistent with the earlier measured native surface-weight rounding.
The two ledgers remain separate. No balancing factor has been applied.

## Reproducibility and remaining work

The entire case preparation, all 648 native flights, and final analysis were
repeated in a separate real input directory. All six source/native files and
11 analysis files are byte-identical; all 102 numeric arrays agree exactly.
Eight analytical tests pass from both maintained and archived source copies.
All 997 protected files, 25 source inputs, 46 copied inputs and 1,175 manifest
entries from 13 earlier artifacts remain unchanged.

An initial symmetry test exposed avoidable floating-point cancellation in
computing an exactly symmetric zero current. The current is now computed as
the difference of matched axial-sign integrals before applying the polar
weight. The initial code and log are preserved. No field was clipped and no
physical acceptance tolerance was changed.

The next [axial-streaming contract](native_axial_streaming_contract.md) defines
a candidate characteristic solve that retains an axial-cell vector inside
each radial segment. It separates an exact-exponential control from a
native-compatible coefficient lift, both of which still require testing.
Top/bottom boundaries, axial spatial refinement, signed multigroup scattering,
fission and the full eigenmode remain outstanding. No production source,
shared build, live D4 input, POD rank or coupled eigenvalue has changed.
