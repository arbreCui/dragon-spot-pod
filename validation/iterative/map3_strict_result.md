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
D_L=6.341724656522274\times10^{-7}\ {\rm cm}^{-1}
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

The infinity hotspot is unique in both updates and does not move.  It is at
plane-list index 1 and energy-group index 326.  At that same coordinate,

\[
L_1=3.3699741471\times10^{-4},\quad
L_2=3.3757751225\times10^{-4},\quad
L_3=3.3694333979\times10^{-4},
\]

so

\[
\Delta L_{12}=+5.8009754866\times10^{-7},\qquad
\Delta L_{23}=-6.3417246565\times10^{-7}.
\]

The largest coordinate therefore reverses sign and grows in magnitude by
9.32%.  This is one observed local rebound, not proof of a two-cycle.  Plane 1
is reported only as the stored list index.  In the frozen axial MACROLIB grid,
group 326 spans approximately `[1.02101195, 1.03499305] eV`; no physical cause
is inferred from that energy interval.

## Hotspot face-current decomposition

A second Ganlib-only mode then read the original axial unknowns.  It first
reconstructed all \(3\times370=1110\) canonical leakage values with the
production binary32 operation order and matched every promoted `SPOT-X-L`
value bit for bit.  For the unique hotspot it also evaluated the unfitted
balance

\[
L_s=\frac{N_s}{D_s},\qquad
N_s=\sum_{i,f\in s}A_i(J_{f+1,i}-J_{f,i}),\qquad
D_s=\sum_{i,f\in s}A_i\,\Delta z_f\,\phi_{f,i}.
\]

The stored face currents use one common signed \(+z\) convention.  Because
plane 1 is one contiguous floor interval, its binary64 diagnostic
decomposition is

\[
C_{\rm low}=-\sum_i A_iJ_{{\rm low},i},\qquad
C_{\rm high}=+\sum_i A_iJ_{{\rm high},i},\qquad
N=C_{\rm low}+C_{\rm high}.
\]

\(C\) and \(N\) are area-weighted face-current terms and \(D\) is a
volume-weighted scalar-flux integral; each scales with the arbitrary flux
normalization.  Their ratio \(L\), and hence \(\Delta L\), has unit
`cm^-1`; the percentages below are dimensionless.

| state | \(C_{\rm low}\) | \(C_{\rm high}\) | \(N\), face binary64 | \(N\), production binary32 | \(D\), production binary32 |
|---|---:|---:|---:|---:|---:|
| \(x_1\) | `1.7509067877e-15` | `-3.7699331665e-16` | `1.3739134711e-15` | `1.3739132750e-15` | `4.0769254292e-12` |
| \(x_2\) | `1.7509382750e-15` | `-3.7461155200e-16` | `1.3763267230e-15` | `1.3763270012e-15` | `4.0770694112e-12` |
| \(x_3\) | `1.7508939253e-15` | `-3.7721105683e-16` | `1.3736828684e-15` | `1.3736829879e-15` | `4.0768959389e-12` |

| update | \(\Delta C_{\rm low}\) | \(\Delta C_{\rm high}\) | \(\Delta N\), face binary64 | \(|\Delta C_{\rm high}|/|\Delta N|\) |
|---|---:|---:|---:|---:|
| \(x_1\to x_2\) | `+3.14873e-20` | `+2.38176e-18` | `+2.41325e-18` | `98.695%` |
| \(x_2\to x_3\) | `-4.43497e-20` | `-2.59950e-18` | `-2.64385e-18` | `98.323%` |

Thus the rebound is localized more narrowly: in this binary64 endpoint
decomposition, the **change in the plane-1 leakage numerator** is dominated in
both updates by the high-\(z\) face.  The production binary32 denominator
changes by only `+0.003532%` and `-0.004255%`, versus production binary32
numerator changes of `+0.175683%` and `-0.192106%`; in both cases it slightly
opposes the leakage change rather than drives it.  The directly observable
binary64 ratio \((|C_{\rm low}|+|C_{\rm high}|)/|N|\) stays between `1.544`
and `1.549`.

### Radial support of the high-z face change

The same read-only pass further decomposed only the dominant high-\(z\) term,

\[
H_r=A_rJ_{{\rm high},r},\qquad
\Delta H_r=H_r^{\rm new}-H_r^{\rm old},\qquad
\sum_{r=1}^{8}\Delta H_r=\Delta C_{\rm high}.
\]

The last identity closes bit for bit when accumulated explicitly in track
radial-index order.  No magnitude threshold is used.
In the frozen track, plane 1 is floors 1–20 with \(\Delta z=2.5\) cm, so
this high-\(z\) surface is axial face index 21, 50 cm above the lower boundary.

| track radial index | \(A_r\) (\(\mathrm{cm}^2\)) | \(\Delta H_{r,12}\) | L1 share 12 | \(\Delta H_{r,23}\) | L1 share 23 |
|---:|---:|---:|---:|---:|---:|
| 1 | `2.5253135e-1` | `+1.2166366e-18` | `51.0813%` | `-1.3278525e-18` | `51.0810%` |
| 2 | `1.4451326e-1` | `+7.5787071e-19` | `31.8197%` | `-8.2716100e-19` | `31.8199%` |
| 3 | `3.3673946e-2` | `+1.4926947e-19` | `6.2672%` | `-1.6291591e-19` | `6.2672%` |
| 4 | `2.6138989e-2` | `+4.3083503e-20` | `1.8089%` | `-4.7022451e-20` | `1.8089%` |
| 5 | `7.8417093e-2` | `+3.7227377e-20` | `1.5630%` | `-4.0630460e-20` | `1.5630%` |
| 6 | `1.5683433e-1` | `+5.5355409e-20` | `2.3241%` | `-6.0416967e-20` | `2.3242%` |
| 7 | `2.6139024e-1` | `+9.2490687e-20` | `3.8833%` | `-1.0094736e-19` | `3.8833%` |
| 8 | `3.8013272e-2` | `+2.9830898e-20` | `1.2525%` | `-3.2558211e-20` | `1.2525%` |

All eight contributions are exactly nonzero.  They are all positive for
\(x_1\to x_2\) and all negative for \(x_2\to x_3\).  Radial index 1 is the
unique largest contributor in both updates, but it carries only about
`51.08%` of the L1 sum; indices 1 and 2 together carry about `82.90%`.
Moreover, \(|\Delta H_{r,23}/\Delta H_{r,12}|\) lies in the narrow reported
range `1.091413`–`1.091437` for every index.

The strict classification is therefore `EXACT-MULTI-REGION`: the high-face
pattern reverses coherently across all eight track radial indices and grows
slightly in magnitude.  It is concentrated in indices 1 and 2 but is not a
single-region or uniform change.  The track record supplies index and area,
not a pin/ring/material label, so no stronger geometric name is inferred.
Here `EXACT-MULTI-REGION` means only that the exact nonzero support has more
than one index; it is not a magnitude threshold or fitted physical class.

### Normalization-invariant adjacent-floor relation

The final no-solve check reads, at the same group and face, the floor-20 and
floor-21 cell-average scalar fluxes and the common signed face-21 current.
The three same-scale quantities contain two degrees of freedom after removal
of an arbitrary common state normalization.  The check therefore reports only
the minimal pair

\[
R_{\phi,r}=\frac{\phi_{21,r}}{\phi_{20,r}},\qquad
q_{J,r}=\frac{2J_{21,r}}{\phi_{20,r}+\phi_{21,r}}.
\]

Here the factor two only writes the current relative to the local arithmetic
mean scalar flux; it is not a fitted or empirical coefficient.  Both ratios
are dimensionless and unchanged by a common nonzero normalization of one
state.  The reader requires every adjacent scalar value to be finite and
strictly positive; it applies no floor, clipping, threshold, or fit.

| state | range of $R_\phi$, radial indices 1–8 | range of $q_J$, radial indices 1–8 |
|---|---:|---:|
| $x_1$ | `[1.0277273282, 1.0277275185]` | `[-2.6889540743e-3, -2.6889534766e-3]` |
| $x_2$ | `[1.0276808800, 1.0276810074]` | `[-2.6719403523e-3, -2.6719398969e-3]` |
| $x_3$ | `[1.0277326531, 1.0277328717]` | `[-2.6905163584e-3, -2.6905160075e-3]` |

The exact positive/negative/zero counts are `0/8/0` then `8/0/0` for
\(\Delta R_\phi\), and `8/0/0` then `0/8/0` for \(\Delta q_J\).  Thus both
normalization-invariant quantities reverse update sign at every radial index.
All 24 underlying face currents are negative in the common \(+z\) convention;
the current direction itself does not reverse.  The raw high-face rebound
therefore cannot be explained solely by arbitrary eigenvector normalization.

The two scalar values are adjacent cell averages, not an interface scalar
flux, and \(q_J\) is only a signed current-to-local-flux ratio.  It is not a
Fick coefficient or a fitted closure.  The eight radial-index rows of this
same rank-one field are also not eight independent physical experiments.  This
result identifies a coherent local shape-and-current update rebound, but
supplies no physical cause, two-cycle proof, or outer-convergence conclusion.

This identifies which archived balance term carries the hotspot change, not
its physical cause.  It does not establish a two-cycle or outer convergence
and introduces no model, fitted factor, relaxation coefficient, or fourth
Picard update.

Reproduce this focused audit with

```sh
SEED_DIR=/absolute/path/to/iterative-seed \
X1_DIR=/absolute/path/to/iterative-map1 \
X2_DIR=/absolute/path/to/iterative-map2-current \
X3_DIR=/absolute/path/to/iterative-map3-strict-current \
GANLIB_LIB=/absolute/path/to/libGanlib.a \
GANLIB_MOD=/absolute/path/to/ganlib/modules \
  sh validation/iterative/run_strict_leakage_faces.sh
```

The runner hash-locks the track and all three axial states before and after
the read, links only Ganlib, and launches no Dragon process.  With the local
development artifacts and in-tree Ganlib build, these overrides may be
omitted.

The strict read-only reproduction is

```sh
X3_DIR="$PWD/validation/artifacts/iterative-map3-strict-current" \
LOCK="$PWD/validation/iterative/picard_strict_direction_scientific.sha256" \
  sh validation/iterative/run_picard_direction_check.sh
```

It compiles one Ganlib-only checker, verifies all three hashes before and
after the read, and launches no Dragon process.

This completes the defensible no-solve localization available from the frozen
three-state sequence.  Further convergence evidence requires a separately
authorized new map or outer-solver study; the present diagnostic does not
select or tune such a method.

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
d1bf1a4462f3097fca7d44e49aa5cbda69e09b46999de0dbebc40d1b615c980d  direction.log
82058122fb471d1eaeba006c5132955f500c0bbd8298de66c62b9d325010e43d  leakage_faces.log
```
