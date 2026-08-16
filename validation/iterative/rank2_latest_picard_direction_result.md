# Latest rank-two Picard direction audit

Date: 2026-08-16

Classification: `OFFLINE_DIRECTION_COMPLETE`.

## Scope

This Ganlib-only audit reads the latest three fixed-rank-two axial states:

\[
x_1=x_{\mathrm{rAA2}},\qquad
x_2=G_2(x_1),\qquad
x_3=G_2(x_2).
\]

| state | role | SHA-256 |
|---|---|---|
| \(x_1\) | rolling-AA(2) proposal | `ce9544e8f58b01d933f5937d781a0f1b70a58862468bbd380d5d2bc5c0e07715` |
| \(x_2\) | returned rolling-AA(2) map | `21e5f4e8660020aee9509a656993c45049deb9a01029d86e63801432c948ab67` |
| \(x_3\) | returned direct Picard successor | `154c707c0f21a1241fad0c887486867e9953af794fec0aa883220d669de74651` |

The checker first reproduced both maps' four stored raw defects bit for bit
and required the fixed POD basis, Gram matrix, layout, height and
normalization to remain unchanged. It ran no Dragon, transport, assembly,
axial solve, map, proposal construction or state publication.

## Leakage result

The two adjacent leakage changes are:

| map | \(D_L\) (`cm^-1`) | \(R_L\) |
|---|---:|---:|
| \(x_1\to x_2\) | `1.71447754837572575e-6` | `1.170144756375341e-3` |
| \(x_2\to x_3\) | `9.21310856938362122e-7` | `6.288020914939620e-4` |

Both relative defects use the same denominator,
`1.46518414840102196e-3 cm^-1`, because the shared middle state \(x_2\)
has the largest leakage magnitude of all three states. Therefore the ratio

\[
\frac{D_L^{23}}{D_L^{12}}
=0.537371199646913045
\]

also explains the local reduction in \(R_L\); it is not a normalization-scale
effect.

Both infinity-norm changes have one unique hotspot at snapshot 1, group 327:

| state | leakage at the hotspot (`cm^-1`) |
|---|---:|
| \(x_1\) | `4.33473760494962335e-4` |
| \(x_2\) | `4.35188238043338060e-4` |
| \(x_3\) | `4.34266927186399698e-4` |

The signed update changes from `+1.71447754837572575e-6` to
`-9.21310856938362122e-7 cm^-1`: it reverses sign at the same location and
shrinks in magnitude. In the separate, non-production height-\(L_2\) view,
the leakage-update cosine is `-0.713235637254585053` and the norm ratio is
`0.542388165116233778`. This is local damped-oscillatory evidence, not a
two-cycle, contraction or future convergence factor.

## Other state blocks

The full modal Gram-height updates are acute, with cosine
`0.941946959765363023` and norm ratio `0.821356827803685685`. The
basis-dependent mode-two diagonal updates are instead obtuse, with cosine
`-0.791118671160926490` and norm ratio `0.697848238817061484`.
The inverse-eigenvalue updates keep the same sign and the second has
approximately half the magnitude of the first. These separate observations
are not combined into a mixed-unit norm.

## Cause boundary

The narrow supported classification is:

- `INNER_TERMINATION_PASS`: every radial and axial solve in the two maps met
  its declared strict terminal contract, so this is not an invalid map caused
  by an inner solver that failed to terminate. No operator inverse bound or
  same-parent tighter solve exists, so finite inner-error influence is not
  bounded by this audit.
- `OUTER_NOT_CLOSED`: \(R_L\) and \(R_a\) still fail the unchanged AND gate,
  directly proving \(G_2(x_2)\ne x_2\) at the declared tolerance. The
  structured same-hotspot sign reversal describes the outer response but
  does not identify its physical or numerical cause.
- `RANK_CAUSE_UNRESOLVED`: the fixed rank-two basis is unchanged, but this
  three-state audit contains no same-parent rank-three counterfactual. Frozen
  training-snapshot tail errors are different quantities and cannot be used
  to attribute the leakage defect to rank two.

Thus the evidence establishes outer nonclosure and records a locally damped
sign reversal in the leakage block. It does not strictly separate finite
inner error from POD truncation, establish rank adequacy, or authorize a new
map, rank increase, relaxation or empirical correction.

## Reproduction identity

The checker source SHA-256 is
`c80efbbb9204e4bc2c9665130a903ab9f269c57935f5be89a68cfea395a8ec05`.
It was compiled with GNU Fortran 15.2.0 using `-ffp-contract=off` and
`-fno-fast-math`, then invoked as:

```sh
check_one_map_xsm --proposal-aa2-directions x1.xsm x2.xsm x3.xsm
```

The three short names were temporary regular-file copies of the hash-locked
inputs above. The temporary directory was removed after the read-only audit.
