# Latest $Q(t)\to u$, $Q(s)\to v$ rank-2 modal AA(1) publication

Date: 2026-08-16

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

## Published proposal

The two hash-locked evaluated pairs are

$$
Q(t)\longmapsto u, \qquad Q(s)\longmapsto v,
$$

with residuals $p=u-Q(t)$ and $q=v-Q(s)$. Recomputed from the four
publication-aware states in the unchanged full Gram-height metric,

$$
\beta=
\frac{\lVert p\rVert_{HG}^{2}-\langle p,q\rangle_{HG}}
     {\lVert q-p\rVert_{HG}^{2}}
=3.43937066250607248,
$$

so this stage materialized the unique unrestricted affine state

$$
x_{\mathrm{AA1}}=
-2.43937066250607248u+3.43937066250607248v.
$$

The coefficient was recomputed, not accepted as an adjustable input. The
same weights were applied to $A$, $\rho$, and $L$. No relaxation, damping,
clipping, fitted coefficient, regularization, pseudoinverse threshold,
condition cutoff, fallback, or separate leakage coefficient was used.

## Publication arithmetic

| quantity | value |
|---|---:|
| modal denominator | `5.04823757210870257e-13` |
| weight on $v$ | `3.43937066250607248` |
| weight on $u$ | `-2.43937066250607248` |
| affine $\rho$ | `0.733993172511808067` |
| REAL32-published $k$ | `1.36241054534912109` |
| reciprocal published $\rho$ | `0.733993144293923150` |
| absolute $\rho$ publication delta | `2.82178849175807045e-8` |
| maximum leakage REAL32 round trip | `4.23491029570566280e-11` |
| minimum published REAL32 $B_2A$ | `1.75340245828789574e-15` |
| strictly positive reconstructed points | `8880 / 8880` |

Modal coordinates remain the exact REAL64 affine values. Leakage follows
the existing REAL64 affine calculation, REAL32 publication, and REAL64
storage convention. The effective eigenvalue is published in REAL32, and
stored $\rho$ is its REAL64 reciprocal.

## Carrier and independent audit

The latest valid returned state $v$ supplies the complete AX/raw-flux and
snapshot carrier. The proposal is marked `PROPOSAL + V2-RAW-FLUX`;
`V2-RAW-FLUX` distinguishes this lifecycle from the earlier unrelated
`V-RAW-FLUX` proposal. The marker records provenance and does not claim that
the copied raw flux is a solved flux for $x_{\mathrm{AA1}}$. Raw fluxes from
$u$ and $v$ were not mixed.

Only the declared publication fields changed. The fixed rank-two bundle,
normalization, state metadata, Gram error, lagged `SYSTEM`, and remaining
carrier payload from $v$ were preserved. Stale map-result records were
removed.

The separately compiled Ganlib checker independently recomputed the AA(1)
coefficient, required the `Z-RAW-FLUX` $Q(t)$ proposal and `U-RAW-FLUX`
$Q(s)$ proposal, verified the actual $Q(s)\to v$ snapshot lifecycle,
checked the complete $v$ AX/raw-flux and snapshot carrier bitwise,
reproduced the publication arithmetic, rejected two wrong-carrier cases,
and confirmed all 8880 positive points. The symbol census found
`DRAGON/ASM/FLU/TRANSPORT=0`.

## Frozen provenance and receipt

The six inputs are frozen in
[`rank2_latest_modal_aa1_qv_candidate_inputs.tsv`](rank2_latest_modal_aa1_qv_candidate_inputs.tsv),
whose SHA-256 is
`ec8d598b7902f6cfe0426d9bea2cec291a8cf0a0c654303ecce1e0ea0c429b27`.
The preceding four-state decision manifest remains frozen at
`8c062a10ad796c24beca7c17c6d62bed4873a08cb6ceaf98591ac208e97d347a`.

| implementation | SHA-256 |
|---|---|
| builder | `c5ca61daf463ccd5de1b01ecafd3dd1fc43d13aaf4d7d1f1518a44ed5b02e56d` |
| checker | `ecedafbb9a93aa86e15772099ffb625c570ce8193d68cac0be9cba569b5ec5a5` |
| runner | `3cf8499ea4bcf203a6d6e4bdc1354a6441087ab013b86001ac678b40461e4295` |

The Git-ignored artifact contains ten regular files, no symbolic links, and
a passing 9/9 receipt.

| artifact | SHA-256 |
|---|---|
| `proposal_axial.xsm` | `bdfc6f8c1a0e4c0d2eb02bffd218cace6bd263ad25bc5439f17751376417549f` |
| `proposal_snapshots.xsm` | `b6a92d2c553f535b0066a63e644423cae22848cd012492f89d0cbff535704490` |
| `build.log` | `4164ce3cf85ec38afcedbb37ed75de8a031752c350a80dc138d19146376cc113` |
| `check.log` | `6bbc2b28485a4822bf7322bffc9cf85760a2a48f7b2da7526682562a135681ac` |
| receipt | `de8c6fc2f0c42ba65223a80f01b9002edd70d00befe7ff53e2d623d5ecd7e0f3` |

Reproduce into a fresh artifact directory with:

```sh
ARTIFACT_DIR=/absolute/path/to/fresh-result \
  make spot-rank2-latest-modal-aa1-qv-candidate
```

The default artifact path refuses overwrite.

## Scientific boundary

This was deterministic publication and independent carrier checking only.
It ran no Dragon, radial solve, axial solve, transport, or nonlinear map. It
therefore created no new $R_\rho$, $R_L$, $D_L$, or $R_a$, did not test the
stopping AND gate, and establishes no convergence factor, contraction,
stability, monotonicity, AA(1) superiority, rank adequacy, or physical
accuracy.

The preceding adverse leakage screens remain warnings. Materialization does
not turn them into physical defects and does not authorize a map. No map
host was added or started; any evaluation $G_2(x_{\mathrm{AA1}})$ requires
a separate decision and authorization.
