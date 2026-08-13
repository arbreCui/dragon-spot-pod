# Strict-inner map-3 result

This record replaces the earlier legacy-path evaluation of the same frozen
parent state.  It evaluates exactly one complete map

\[
x_3^{\mathrm{strict}}=G_h(x_2),\qquad h=5\times10^{-7}.
\]

No fourth Picard update was run.

## Fixed method and controls

The POD basis, rank-one space, physical data and frozen parent \(x_2\) were
unchanged.  The update used direct substitution: there was no relaxation,
fitting, clipping, flux floor, parameter change or automatic retry.  The only
solver change relative to the archived legacy run was that the online SPOT
radial path could no longer return through the legacy
`EINN < 10*EPSINR` shortcut.

One radial-only Dragon process performed the three plane solves.  A separate
axial-only process then consumed those newly returned radial objects.  Each
process had one 75 s process bound and no retry.  Their listings reported 65 s
and 46 s of CPU time, respectively.

The executable and axial-call provenance was frozen as follows:

```text
61673fa6ec3a2cbf25aa7ddfbda8acc5339c3392fd4888b9d9bb45e3ca1e0001  Dragon
101ba0ad64c91723fdeb002e62c6226347fcfaeff188e125d699d70e113febc7  initial_axial_track.xsm
2e01e806683ce25b5771af055112dc86dcf147245abc5a5c3dceac4d9939373a  initial_axial_macrolib.xsm
dc65467731947901393f9fb7114b7cd2e956a9992bb97db18e665b47e7446504  basis_reference.xsm
7bee7c9ff8cdfd657fa0a831a34ebe559dbe1035fd978af16c98738e992495b2  state2_axial.xsm
9dfdc65fee5cbed07b77e6649c64ac31bb3513a48373b34ddb310e9ef9bb128a  map3_axial.x2m
```

The axial deck contains exactly one axial `FLU` call and no radial transport,
mixing, relaxation or retry path.

## Numerical solver terminals

All returned FLU solves met the declared binary32 threshold
`4.99999999e-7` on both the outer unknown and final inner residual:

| solve | outer iterations | `EUNK` | final inner iterations | `EINR` |
|---|---:|---:|---:|---:|
| radial plane 1 | 5 | `4.31115978e-7` | 4 | `2.75581868e-7` |
| radial plane 2 | 3 | `4.57398869e-7` | 3 | `4.53212692e-7` |
| radial plane 3 | 6 | `3.65322109e-7` | 4 | `1.56248547e-7` |
| axial | 133 | `4.66254022e-7` | 1 | `4.66254022e-7` |

Every terminal has `EUNK-VALID=1`, `IGDEB=371` and `STATE=1`.  Both Dragon
processes ended normally.  These facts establish convergence of the four
numerical transport solves; they do not by themselves establish convergence
of the coupled Picard iteration.

## Independently reproduced map defect

The Ganlib-only continuation checker used no Dragon or transport routine.  It
passed the fixed POD package, live radial-operator change, positive radial
flux, canonical state layout, raw-defect recomputation and restart-archive
ordering.

For the predeclared outer tolerance \(5\times10^{-7}\), its independently
reproduced three-component AND gate is

| quantity | value | gate |
|---|---:|:---:|
| \(R_\rho\) | `0` | PASS |
| \(R_L\) | `4.325264323473080e-4` | **FAIL** |
| \(R_a\) | `3.240969394526228e-7` | PASS |

Thus \(R_L\) is about \(865.05\) times the declared outer tolerance.  The
dimensional leakage change

\[
D_L=6.341724656522274\times10^{-7}
\]

is retained only as a diagnostic.  It is not a fourth stop component and
cannot be compared directly with a dimensionless solver tolerance.

The axial balance diagnostics were a global norm of
`3.89306e-9` and a maximum per-group relative diagnostic of `3.23286e-3`.
The latter occurs in a very small-scale group and is recorded, not used as an
empirical acceptance override.

## Scientific classification

The result is a complete, independently checked strict raw map.  It is **not**
an accepted fixed point because the leakage component fails the declared AND
gate.  The zero eigenvalue defect means only that the stored binary32 value of
\(\rho\) did not change.

Relative to the preceding \(x_1\to x_2\) update, \(R_L\) and \(D_L\) rise by
the factor `1.09321694`, while \(R_a\) falls to the factor `0.44778479`.  The
strict-inner replacement therefore removes the third step's modal gate
failure seen in the archived path, but it does not remove the leakage rebound
or leakage gate failure.  Because the archived and replacement third maps used
different inner termination behavior, their comparison is diagnostic only
and is not a convergence-rate estimate.  It neither identifies a physical
cause nor supplies an inner state-error bound.

## Consecutive-update direction

A subsequent read-only Ganlib check used the frozen \(x_1,x_2\) and this
strict \(x_3\).  It reproduced both saved raw defects and the fixed-space
package bit for bit before reporting the separate update geometries:

| component and metric | cosine | norm ratio \(23/12\) |
|---|---:|---:|
| modal, fixed Gram-height | `+0.4968937369` | `0.4477848149` |
| leakage, height-weighted \(L_2\) | `-0.1550583606` | `0.7312174322` |

Thus the modal increments are acute and the second modal increment is
smaller.  The leakage increments are obtuse in the explicitly non-production
height-weighted \(L_2\) diagnostic, while their aggregate \(L_2\) norm also
falls.  In contrast, the production dimensional infinity diagnostic grows:

\[
\frac{D_{L,23}}{D_{L,12}}
=1.0932169376.
\]

This is not evidence of a simple whole-state reverse oscillation: the maximum
leakage component grows even though its height-weighted aggregate norm falls,
and the modal update is smaller and acute.  No mixed-unit total-state angle is
defined; both stored \(\rho\) increments are zero.  These three-state
geometries prove neither convergence nor divergence and cannot separate
behavior of the physical map from inner-solver state error.

The strict read-only reproduction is

```sh
X3_DIR="$PWD/validation/artifacts/iterative-map3-strict-current" \
LOCK="$PWD/validation/iterative/picard_strict_direction_scientific.sha256" \
  sh validation/iterative/run_picard_direction_check.sh
```

It compiles one Ganlib-only checker, verifies all three hashes before and
after the read, and launches no Dragon process.

The next scientifically valid action is therefore not a blind \(x_4\).  Any
further run should first be justified by a predeclared test of the leakage
coupling; no empirical coefficient should be introduced.

## Hash-frozen local evidence

The ignored local evidence is split between
`validation/artifacts/iterative-map3-strict-radial/` and
`validation/artifacts/iterative-map3-strict-current/`.  Its manifest contains

```text
42b9a65fd54726df76bf6b587a7a4157bb8e61c09bb9604c2bc4aab1d452d93d  radial.log
12fcf8d406a72b2b20d98f0d372ff2c4ed1e4e9ae60be18fcbc932def837a77c  state3_radial.xsm
0ed25fe626af26e5e4425c45c7593aaa480b08300aea511b4ffc742c92f6e3dc  state3_system.xsm
966a416f176bf6d3d1a509a933dbe2fb65326813ca126496b42932fc991ac49b  axial.log
4b543cfd5d2b60727b0358adafe9057bb5859833744a3d58ad2f2d03d6feaf61  state3_axial.xsm
6d1ac081f17237bdc87e78d1d806c4f6127425e6f453f06a48451b278c1ab921  state3_snapshots.xsm
0db7dac519f882a1d6102ba00adf8fd102dc00c68aaea346c9dd8067e8715f02  independent_check.log
ae374a9721eac9e429f6ebfdf45e6235606f39ac5fb3e98c0888387b1607faa2  direction.log
```
