# Next rank-2 modal AA(1) proposal materialization

Date: 2026-08-14

## Purpose

This stage performs only the deterministic publication already authorized by
the frozen next-history decision. It runs no Dragon, assembly, transport,
axial solve or map evaluation and introduces no empirical parameter.

From the two evaluated pairs

\[
p=x_2-x_1,\qquad q=z-y_{\rm pub},
\]

the full Gram-height modal least-squares scalar is recomputed as

\[
\beta_z=\frac{\langle p,p-q\rangle_{HG}}
{\lVert p-q\rVert_{HG}^2}=0.9302745506696768,
\qquad
w_{\rm pub}=(1-\beta_z)x_2+\beta_z z.
\]

The same scalar is applied to the complete published state
`(A,rho,L)`. It is neither fitted nor clipped.

## Publication contract

The AX file is a copy of the audited `z` carrier. Its raw axial flux,
fixed rank-two basis package and matching normalization remain bitwise `z`.
Only the affine modal coordinates and canonical binary publication of
`K-EFFECTIVE`, reciprocal `SPOT-X-RHO` and leakage are written. The carrier is
explicitly marked `Z-RAW-FLUX`.

The snapshot file is likewise copied from `z`. Only root `SPOT-ITER-K` and
plane `SPOT-LEAK1D` are changed. The complete lagged `SYSTEM`, raw plane flux,
`SOUR`, `SPOT-QFISS` and every fixed-source diagnostic remain bitwise `z`.
In particular, `SPOT-FS-K` remains the historical value used to generate the
`z` carrier; it is not relabelled as a solve at `w_pub`.

All stale map defects, projection/off-space records and balance diagnostics
are absent. The independent checker compares the full carrier payload except
for the two explicitly published fields.

## Frozen result

| Quantity | Value |
|---|---:|
| denominator | `1.7664294562965954e-5` |
| weight on `z` | `0.9302745506696768` |
| weight on `x2` | `0.0697254493303232` |
| affine inverse eigenvalue | `0.73399301446018783` |
| published REAL32 `k` | `1.3624107837677002` |
| reciprocal published `rho` | `0.73399301584690513` |
| `rho` publication delta | `1.3867172965476016e-9` |
| maximum leakage REAL32 round trip | `5.2830902196390750e-11` |
| minimum published REAL32 `B2a` | `1.7533211431249593e-15` |
| strictly positive `B2a` points | `8880 / 8880` |

The hash-locked input manifest is
[`rank2_modal_aa1_next_candidate_inputs.tsv`](rank2_modal_aa1_next_candidate_inputs.tsv).
The materialized outputs are local, Git-ignored artifacts with frozen hashes:

| Output | SHA-256 |
|---|---|
| `proposal_axial.xsm` | `c2df5e526aa9a0c0c3dc354d3ec539475814fe73c87af19ba04dde05c1475ff4` |
| `proposal_snapshots.xsm` | `530d23485baa006342b08815a9240d61fa4ec63810103307ead66104eb5bef9c` |

The local receipt is
`validation/artifacts/iterative-rank2-modal-aa1-next-candidate/result.sha256`.
It covers both outputs, both logs, the input manifest, builder, independent
checker, runner and classification.

The final carrier audit was tightened after materialization to bind the AX
`STATE-VECTOR/GERR`, the input `y_pub -> z` snapshot lifecycle and the root
snapshot inventory. The two proposal files were not regenerated: the stronger
checker revalidated those same hashes, after which only its log/source receipt
was refreshed. The final checker SHA-256 is
`8a782159c23fc586d82f15b661ce12b00a32196e7c17df2e093da15f0fc79223`.

The historical six/seven-argument materialization path was also rerun: its
two output hashes remain exactly
`ae5f5b328fc6c5b181f40a4122b88771c857fd0200fc6e8351fc6b97d68d5c56`
and
`c11f4641897288f355ba60fa05eb7081d3aedfd8078333735d5c85c219f47c75`.

## Scientific boundary

The classification is exactly `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.
Materialization proves the formula, binary publication, provenance and
strict-positivity gates; it does not prove convergence, rank adequacy,
transport accuracy or Anderson superiority. There is still no value of
`G_2(w_pub)` and therefore no new outer residual.

The only meaningful next experiment is one separately authorized fresh map
`G_2(w_pub)`, with no retry. It has not been started by this stage.
