# Continued rank-2 map result

## Classification

`VALID_NOT_MET`.

This is the separately authorized direct continuation

$$
x_0=C_2(\Phi_7),\qquad x_1=G_2(x_0),\qquad x_2=G_2(x_1).
$$

The previous valid rank-2 candidate is consumed directly as $x_1$; it is not
re-encoded. The run uses the same fixed rank-2 basis, equations, direct
substitution and $5.0\times10^{-7}$ tolerance. It performs all three online
radial solves and one axial solve, with no retry and no third map.

## Validity evidence

The run used source commit `e8bf199092c4a4ae08cb444a0a1d8d99155af111`.
The radial and axial Dragon processes each returned zero and reported 51 and
134 CPU seconds, respectively; no exact wall duration is claimed. The
120-second radial and 420-second axial bounds were host resource limits only.

All three radial terminals passed strictly. Their `(IEXTF, EUNK, EINR)`
records were

| plane | values |
|---:|---:|
| 1 | `(4, 3.36357630e-7, 4.05807270e-7)` |
| 2 | `(4, 4.75401663e-7, 2.27699019e-7)` |
| 3 | `(2, 4.97279075e-7, 1.99433416e-7)` |

The axial terminal also passed strictly:

| quantity | value | limit |
|---|---:|---:|
| outer iterations | `210` | `500` |
| outer error | `4.03366646e-11` | `5.0e-7` |
| unknown error | `4.22487261e-7` | `5.0e-7` |
| terminal inner error | `4.87475631e-7` | `5.0e-7` |

The independent Ganlib-only `--continued` checker passed the fixed POD
package, live radial response, positive raw radial flux, rank/layout,
bitwise-recomputed raw defects and returned-leakage/restart checks. The full
publication receipt passed before atomic publication.

## Raw second-map result

The axial FLU terminal eigenvalue is `1.3630393895609616`; the canonical
candidate stores its binary32 value as `1.3630393743515015`. The separate
defects are

| quantity | value | role | meets `5.0e-7`? | multiple of tolerance |
|---|---:|---|---:|---:|
| $R_\rho$ | `6.463824260144468e-4` | stopping rule | no | `1292.764852` |
| $R_L$ | `5.604853591664505e-3` | stopping rule | no | `11209.707183` |
| $D_L$ (`cm^-1`) | `8.213741239160299e-6` | diagnostic | not applicable | not applicable |
| $R_a$ | `5.863547015169775e-3` | stopping rule | no | `11727.094030` |

The global and maximum-group balance diagnostics are `4.089735e-8` and
`1.424116e-3`. They do not enter map acceptance.

All three stopping defects and diagnostic $D_L$ decreased relative to the
first rank-2 map:

| quantity | $x_0\rightarrow x_1$ | $x_1\rightarrow x_2$ | second/first |
|---|---:|---:|---:|
| $R_\rho$ | `1.256333817507227e-3` | `6.463824260144468e-4` | `0.5144989469` |
| $R_L$ | `2.534536480411694e-1` | `5.604853591664505e-3` | `0.02211391959` |
| $D_L$ | `3.716142964549363e-4` | `8.213741239160299e-6` | `0.02210286665` |
| $R_a$ | `6.797330105507151e-3` | `5.863547015169775e-3` | `0.8626250196` |

These are two-update ratios, not asymptotic convergence factors.

## Read-only direction audit

The current checker first replays $x_0\rightarrow x_1$ with the re-encoded
parent that intentionally carries no saved-defect records, then replays
$x_1\rightarrow x_2$ as a continued map. Both defect checks pass bit for bit
before any direction quantity is reported.

No angle is formed across the mixed-unit $(\rho,L,a)$ state:

| block | update-norm ratio | cosine | interpretation |
|---|---:|---:|---|
| full modal, height-Gram | `0.8641175966` | `-0.8749291465` | smaller, strongly anti-aligned |
| mode-2 $G_{22}$-restricted | `0.9325603959` | `-0.9159727398` | slightly smaller, strongly anti-aligned |
| leakage, height-$L_2$ | `0.02460553548` | `0.2712782652` | much smaller; auxiliary diagnostic |

The mode-2 ratio and cosine are a basis-dependent, $G_{22}$-restricted
coordinate diagnostic, not the full Gram partition or a unique physical
energy attribution. Separately, its diagonal term accounts for
`0.9029307791` of the second full modal update numerator. The production
leakage infinity ratio is
`0.02210286665`; its unique hotspot moves from plane 2/group 154 to plane
2/group 269. The signed inverse-eigenvalue updates are
`+1.256333817507227e-3` and `-6.463824260144468e-4`, so their signs oppose.

The supported local statement is therefore: the leakage update becomes much
smaller; the two full modal updates are strongly anti-aligned, with second to
first norm ratio `0.864118`; and the second $G_{22}$-restricted mode-2 norm is
`0.932560` of the first while its diagonal term is `0.902931` of the second
full modal numerator. This does not establish a two-cycle, Picard convergence
or divergence, a Jacobian eigenvalue, rank adequacy, physical accuracy or a
need for damping.

## Reproduction identity

The Git-ignored result is
`validation/artifacts/iterative-rank2-picard2/`. Its receipt validates with

```sh
cd validation/artifacts/iterative-rank2-picard2
shasum -a 256 -c result.sha256
```

Essential hashes are

| object | SHA-256 |
|---|---|
| `candidate_axial.xsm` | `bff9299595121b4b189f8b6d8e39c3b06bcefe0598d387f4aebf57861546ca02` |
| `candidate_snapshots.xsm` | `ec08ec18761585d0249f15f757830571c44ea80bdd3d4f4d822d775866c0c587` |
| `candidate_system.xsm` | `24f90f85ab6330d8cfdb59ce636cae20e044ec2f87ff9d1af670535f5e264820` |
| `radial.log` | `6c3a0376a04675b80dc520babd46457d24f38d76e40591d66344afafb7484cb4` |
| `axial.log` | `1fc71ccefefbb7150d94297db50b42ea1a3029d1223d2070d45a152201967eba` |
| `independent_check.log` | `0db7dac519f882a1d6102ba00adf8fd102dc00c68aaea346c9dd8067e8715f02` |
| `result.sha256` | `c837aa215a0f32a4677fbd75bc33dd28056e009c55cef2a3b6e9c556db4b116a` |

The read-only direction inputs are hash-locked as

| state | local object | SHA-256 |
|---|---|---|
| $x_0$ | `validation/artifacts/iterative-rank2-map-axial2/rank2_parent_axial.xsm` | `a464cc05a1d21f00c1edb1e1cc5451846a995cb67b08f0869d4709958f9e6e38` |
| $x_1$ | `validation/artifacts/iterative-rank2-map-axial2/candidate_axial.xsm` | `5ec5a3576fab3662cd5fabc18226d98e56fd9b936deabe6bd70a09623f596f61` |
| $x_2$ | `validation/artifacts/iterative-rank2-picard2/candidate_axial.xsm` | `bff9299595121b4b189f8b6d8e39c3b06bcefe0598d387f4aebf57861546ca02` |

The direction checker SHA-256 is
`8d8074246cf63d4afe745d85fab2d092c9492eeab2083ae30017599f260930b6`.
It is invoked after compilation as

```sh
check_one_map_xsm --rank2-directions \
  validation/artifacts/iterative-rank2-map-axial2/rank2_parent_axial.xsm \
  validation/artifacts/iterative-rank2-map-axial2/candidate_axial.xsm \
  validation/artifacts/iterative-rank2-picard2/candidate_axial.xsm
```

No third rank-2 map is defined or authorized by this result.
