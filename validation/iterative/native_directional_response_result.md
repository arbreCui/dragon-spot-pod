# Native directional response: planar extraction and aggregation qualified

The native ray/polar/orientation state has now been extracted for groups 51,
61 and 98. Its aggregate reproduces the saved radial response and boundary
functional, including the native source-isolation completion. An independently
excited planar x-current response is measured. **Axial odd response and a new
coupled reference remain unqualified.**

Evidence: [sealed artifact](../artifacts/native-directional-response-20260929/README.md),
[predeclared plan](../artifacts/native-directional-response-20260929/plan.json),
[numeric results](../artifacts/native-directional-response-20260929/analysis/result.json),
[verification](../artifacts/native-directional-response-20260929/verification.json).
This follows the [directional extraction contract](native_angular_reference_contract.md).

## What is retained

The historical fixture has 11,364 planar rays, 96 azimuths and four polar nodes.
Both orientations give 90,912 ray/polar/orientation states and 878,688 interior
segment samples per group. The export retains the physical segment sequence,
entrance/exit surface, native quadrature values, path lengths and two native
coefficients for every segment:

```
ell = H2D * ZMU
w = track_weight * WZMU
psi_out = psi_in + B * (q - total * psi_in)
segment_integral = B * psi_in + D * q
```

`B` comes directly from the frozen library's `MCGSCA`; `D` comes directly from
its `MCGDSCA` single-segment own-source calculation. The geometry plus these
coefficients are a factorized source-to-segment response, including boundary
inflow. They avoid storing an enormous dense matrix without discarding track
state. Saved examples also include segment source, incoming and outgoing
amplitudes for a white-return unit source in region 1, and weighted angular-bin
responses for all 31 source cases in each group. Bin entries are contributions
to an integral, not local angular flux values.

Both planar orientations carry weight `w`. Volume contributions are divided by
the native region weights; boundary contributions are divided by native surface
weights. Reintegrating the geometry differs from those stored weights by
7.19e-8 and 4.36e-8 respectively. These native discrepancies remain visible.

## Source isolation and precision

The unweighted coefficient `D` is the native own-source integral **per
orientation**. Reassembling `2*sum(w*D)/V` and applying `MCGDS6`'s binary32
rounding reproduces every stored PJJ value exactly in all three groups.

Before that rounding, summing the full directional integrals differs from the
native completed scalar response by up to 2.39e-8 relative. The export keeps
the known rounding remainder as a separate regional ledger:

```
delta_pjj = stored_pjj - 2*sum(w*D)/V
native_scalar = sum(w*segment_integral)/V + delta_pjj*q_even
```

This remainder is neither fitted nor allocated to arbitrary angular bins. The
unrounded directional state and the native rounded scalar state are explicitly
distinguished. In addition, `MCGDSCA` uses a small-optical-length Taylor branch
and a different table-evaluation precision from `MCGSCA`. Replacing native `D`
by `(ell-B)/total` would change the discretization; the maximum absolute
differences for these groups are 4.94e-6, 7.83e-6 and 1.02e-5 in integral/source
units. No such replacement or balance correction is made.

Single-segment controls at optical lengths 0.001, 0.7 and 100 exercise both
orientations against exact exponential solutions. Outgoing and full-integral
relative errors are below 1.30e-10/1.59e-7, 9.86e-8/1.12e-7 and roundoff/zero,
respectively, within the declared 2e-6 tabulation tolerance.

## Independent native comparisons

Each group uses 14 coordinate flights, the four previous independent open-flight
patterns, eight white-return unit sources, and the five previous normalized
closed-source patterns. Fresh, unmodified `MCGFCF` + `MCGFST` flights evaluate
all 93 sources. Stored operators are comparisons, not fitted extraction data.

| Group | Worst individual source action error | White-return R error | White-return outgoing error | Maximum raw balance defect |
|---|---:|---:|---:|---:|
| 51 | 1.31e-14 | 4.41e-15 | 4.24e-15 | 1.31e-7 |
| 61 | 1.58e-14 | 4.64e-15 | 2.54e-15 | 1.21e-7 |
| 98 | 1.19e-14 | 3.06e-15 | 2.91e-15 | 1.11e-7 |

Action errors pass the predeclared 5e-12 threshold. Balance is the absolute raw
source + inflow - collision - outflow defect, divided by absolute source plus
inflow; it passes 1e-6. All 87 nonnegative external-source cases have nonnegative
incoming amplitudes, outgoing amplitudes and full segment integrals. Every
sampled `B`, `D` and transmission `1-total*B` is nonnegative. The two signed
source patterns per group remain signed and are included in action checks.
This is a three-group transport-flight result, not a positivity claim for the
signed multigroup scattering/eigenproblem or all 370 groups.

## What the measured odd response means

The private host passes separate `SP` and `SM` segment sources to the native
`MCGFFAR` kernel and collects its scalar and x-harmonic moments. It uses the
actual binary32 x harmonic from `MOCCHR`. For each group, three vacuum-inflow
excitations have

```
q(r,Omega) = 1 + s * x_harmonic(Omega) * r/16,    s = -1, 0, +1
```

where `r=1..8`. The two planar orientations have opposite x harmonics; the
source's even part is exactly one in every case. The inputs remain positive.
The retained recurrence reproduces the independently executed native scalar,
x-current and boundary controls within 2.18e-14 relative. The midpoint identity
for opposite odd excitations holds at roundoff. The measured half-difference of
x-current has infinity norms 0.0706826, 0.0704398 and 0.0688134 in groups 51, 61
and 98. Its full regional vectors are archived. Pair-case raw balance defects
are at most 1.57e-8.

These are actual responses to explicitly extended angular inputs, not an odd
operator inferred from scalar `H` or assigned from `total`. They are planar
current responses. Native `MOCCHR` in two dimensions selects `l+m` even and
therefore omits the axial odd harmonic. The four saved CPO values are negative
half-range quadrature representatives; their sign does not supply independent
up/down track states. `RP/RM` reverse planar travel, not axial direction.

The native x harmonic and the planar component implied by `CAZ1/ZMU` differ by
up to 8.92e-8 because the records and harmonic generation use distinct binary32
operations. Both definitions are preserved; neither is silently substituted.

## Reproducibility and next step

Fresh native extraction and all 93 scalar flights were repeated in a separate
real input directory. Five native output/input files and all eight final
analysis files are byte-identical; all 86 numeric arrays agree exactly. Eight
analytical tests pass from both maintained and archived copies. The 997 protected
files, 30 source inputs, 54 copied inputs and 1,056 manifest entries from 12
earlier artifacts remain unchanged.

An initial test exposed an alias inside the synthetic test fixture; copying its
own-source sum fixed the fixture without changing the transport implementation.
An initial replay used a symlink for its working directory; the output-exists
guard rejected it before output creation. A separate real directory resolved
that path issue. Both logs and the earlier analysis are retained.

The next bounded step is the [signed axial-state contract](native_signed_axial_contract.md).
It must introduce axial signs explicitly, calibrate its zero-gradient limit to
these native flights, and test prescribed axial odd sources and boundary
redistribution before defining axial propagation. No shared build, live D4
control, production equation, POD rank or coupled eigenvalue has changed.
