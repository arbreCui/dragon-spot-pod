# Rank-2 axial-only result

## Classification

`VALID_NOT_MET`.

This second, separately authorized operational attempt completed the axial
half of the same mathematical map $G_2(C_2(\Phi_7))$ from the hash-locked
radial staging. It ran no radial equation and made no retry. The first
operational attempt remains `INVALID_MAP`; this result does not retroactively
change it.

## Validity gates

The run used source commit
`bb5a408247f76c695af08d4a184c659ebab4467f`, one Dragon process and the
predeclared 420-second host bound. Dragon returned zero and reported 137 CPU
seconds; no exact wall duration is claimed. The axial log contains exactly one
strict outer terminal, one strict inner terminal and one normal end:

| terminal quantity | value | limit |
|---|---:|---:|
| outer iterations | `215` | `500` |
| outer error | `6.00512640e-10` | `5.0e-7` |
| unknown error | `3.08506799e-7` | `5.0e-7` |
| terminal inner error | `4.58431856e-7` | `5.0e-7` |

The independent Ganlib-only `--reencoded` checker passed the frozen POD
package, live radial operator, positive raw radial flux, rank/layout,
independently recomputed raw defects and returned-leakage/restart checks. All
frozen inputs and Dragon/Ganlib hashes were unchanged, and `result.sha256`
passed before atomic publication.

## Raw one-map result

The candidate eigenvalue is `1.361840`. The separate raw defects are

| quantity | value | role | meets `5.0e-7`? |
|---|---:|---|---:|
| $R_\rho$ | `1.256333817507227e-3` | stopping rule | no |
| $R_L$ | `2.534536480411694e-1` | stopping rule | no |
| $D_L$ (`cm^-1`) | `3.716142964549363e-4` | diagnostic | not applicable |
| $R_a$ | `6.797330105507151e-3` | stopping rule | no |

The map is therefore valid, but the declared tolerance is not met. The global
and maximum-group balance diagnostics are `4.19131e-8` and `1.86008e-3`.
Their magnitudes, like $D_L$ and timing, are not acceptance thresholds or
physical-accuracy evidence.

## Rank sensitivity at the same raw x7 parent

The retained rank-1 x7-to-x8 map and this rank-2 map are both valid and both
classified `VALID_NOT_MET`:

| raw defect | rank 1 | rank 2 |
|---|---:|---:|
| $R_\rho$ | `6.405763486316829e-8` | `1.256333817507227e-3` |
| $R_L$ | `3.784961167028899e-4` | `2.534536480411694e-1` |
| $D_L$ | `5.549518391489983e-7` | `3.716142964549363e-4` |
| $R_a$ | `2.673129764390890e-7` | `6.797330105507151e-3` |

This establishes material sensitivity of the one-map response to retained POD
order at this frozen parent. It does not show that rank 2 is physically worse,
that either rank is adequate, or that the rank-2 iteration converges. No modal
coefficient is compared componentwise; $R_a$ is only a scalar in each rank's
own Gram metric. No 3D/reference accuracy result is claimed.

## Retained local result

The Git-ignored result is
`validation/artifacts/iterative-rank2-map-axial2/`. Its receipt validates with

```sh
cd validation/artifacts/iterative-rank2-map-axial2
shasum -a 256 -c result.sha256
```

Essential hashes are

| object | SHA-256 |
|---|---|
| `candidate_axial.xsm` | `5ec5a3576fab3662cd5fabc18226d98e56fd9b936deabe6bd70a09623f596f61` |
| `candidate_snapshots.xsm` | `f9c0b78073ba6da05c5e5912b4e5c45045ac2506e72465a33c007b545a667d4c` |
| `axial.log` | `fd3467fc36b19e81b5cbe4ffeac3e227b973e17a2c6fea36d66da08807317a36` |
| `independent_check.log` | `318ca9511eb2468268702f7e86b203003da6f63dd5381db8fb75300a04b16737` |
| `result.sha256` | `6c2000f5dedeabdd9476c0897fb27522d767f32869a06d7de0f79621e11bea6d` |

This single map is evidence for rank sensitivity only. It authorizes no next
Picard map automatically.
