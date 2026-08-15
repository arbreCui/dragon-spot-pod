# Latest rank-2 modal AA(1) proposal materialization

Date: 2026-08-15

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

## Purpose

This stage materializes the proposal already selected by the frozen read-only
history calculation. It runs no Dragon, radial solve, axial solve or map and
introduces no empirical parameter.

For the two actual evaluated pairs

\[
q=z-y_{\rm pub},\qquad r=v-w_{\rm pub},
\]

the full Gram-height modal least-squares scalar is recomputed from the XSM
inputs:

\[
\beta_v=\frac{\langle q,q-r\rangle_{HG}}
{\lVert q-r\rVert_{HG}^{2}}=0.956973882871698711,
\qquad
u=(1-\beta_v)z+\beta_v v.
\]

The same unique scalar is applied to the complete `(A,rho,L)` state. It is
not fitted, clipped, damped or relaxed.

## Publication and provenance contract

The AX output starts as an exact copy of the latest returned state \(v\).
Only `SPOT-X-A`, `K-EFFECTIVE`, `SPOT-X-RHO` and `SPOT-X-L` are published
from the affine state. The eight stale result/diagnostic records are removed,
and the only new lifecycle records are
`SPOT-X-STATE=PROPOSAL` and `SPOT-X-CARR=V-RAW-FLUX`. An independent Ganlib
checker recursively requires every other root record and payload, including
the raw `FLUX`, to remain bitwise \(v\).

The snapshot output starts as an exact copy of the returned \(v\) snapshot.
Root `SPOT-ITER-K` and plane `SPOT-LEAK1D` are published, while stale root
records `SPOT-L1-ERR`, `SPOT-PJ-PERP` and `SPOT-PROJECT` are removed. Every
other root, `TRACK`, `MICROLIB2`, `SYSTEM` and `FLUX` payload remains bitwise
\(v\). The input lifecycle check separately proves that its returned leakage
and root eigenvalue belong to \(v\), while `SPOT-FS-K` and the lagged `SYSTEM`
belong to the actual input \(w_{\rm pub}\).

## Frozen result

| Quantity | Value |
|---|---:|
| denominator | `1.0477795447002805e-7` |
| weight on \(v\) | `0.956973882871698711` |
| weight on \(z\) | `0.043026117128301289` |
| affine inverse eigenvalue | `0.73399330840146559` |
| published REAL32 \(k\) | `1.3624101877212524` |
| reciprocal published `rho` | `0.73399333696453450` |
| `rho` publication delta | `2.8563068910081313e-8` |
| maximum leakage REAL32 round trip | `5.7824184242910581e-11` |
| minimum published REAL32 \(B_2a\) | `1.7534197165841960e-15` |
| strictly positive \(B_2a\) points | `8880 / 8880` |

The hash-locked inputs are recorded in
[`rank2_modal_aa1_u_candidate_inputs.tsv`](rank2_modal_aa1_u_candidate_inputs.tsv).
The local Git-ignored outputs are frozen as:

| Output | SHA-256 |
|---|---|
| `proposal_axial.xsm` | `77a4bc3916db21064dc2bae73a0397faeb15fb8033de6f761fcaa4cfd0f6852b` |
| `proposal_snapshots.xsm` | `2f526c84f4ef42afd51178dde9481ff7336c0de5b0ff486135635a0b7fc79a81` |

The receipt at
`validation/artifacts/iterative-rank2-modal-aa1-u-candidate/result.sha256`
passes for both outputs, both logs, the manifest, builder, independent
checker, runner and classification. Builder/checker symbol audits report
`DRAGON/ASM/FLU/TRANSPORT=0`.

The historical materializers were rerun after adding the dedicated `--u`
mode. Their frozen AX/snapshot hashes remain exactly
`ae5f5b328fc6c5b181f40a4122b88771c857fd0200fc6e8351fc6b97d68d5c56` /
`c11f4641897288f355ba60fa05eb7081d3aedfd8078333735d5c85c219f47c75`
and
`c2df5e526aa9a0c0c3dc354d3ec539475814fe73c87af19ba04dde05c1475ff4` /
`530d23485baa006342b08815a9240d61fa4ec63810103307ead66104eb5bef9c`.
Negative carrier tests reject both an X2 proposal presented as the required Z
input and a Z proposal presented as the required V output.

Reproduction from a workspace containing the frozen local inputs is one
short no-transport command into a fresh artifact directory:

```sh
make spot-rank2-modal-aa1-u-candidate
```

The target refuses to overwrite the frozen artifact and contains no retry
loop.

## Scientific boundary

This result proves only deterministic publication, fixed rank-two
provenance, exact lifecycle binding, binary publication arithmetic and strict
positivity. It does not provide \(G_2(u_{\rm pub})\), a stopping defect,
convergence evidence, rank adequacy, transport accuracy or evidence that
AA(1) is superior to another iteration.

No map host or Dragon run was created or started in this stage. A future
evaluation of \(G_2(u_{\rm pub})\), if authorized, must be a separately
declared single map with the same physical equations and no empirical
controls.
