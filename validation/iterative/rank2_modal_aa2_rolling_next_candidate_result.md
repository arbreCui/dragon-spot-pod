# Next rolling rank-2 modal Anderson(2) proposal

Date: 2026-08-16

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

## Shifted three-map window

The AA(2) window was shifted forward by one evaluated pair:

\[
(x_0,x_1,x_2)=(x_{\mathrm{roll}},x_{\mathrm{roll2}},x_{\mathrm{AA2}}),
\qquad x_i^+=G_2(x_i).
\]

The old \(x_{\mathrm{next}}\) pair left the window. For the canonical modal
coordinate, the unchanged method uses

\[
f_i=A_i^+-A_i,
\]

with the same Gram-height inner product. Defining
\(d_0=f_0-f_2\) and \(d_1=f_1-f_2\), the standard affine AA(2) system is

\[
\begin{bmatrix}
\langle d_0,d_0\rangle & \langle d_0,d_1\rangle\\
\langle d_0,d_1\rangle & \langle d_1,d_1\rangle
\end{bmatrix}
\begin{bmatrix}\gamma_0\\\gamma_1\end{bmatrix}
=-
\begin{bmatrix}\langle d_0,f_2\rangle\\\langle d_1,f_2\rangle\end{bmatrix},
\]

followed by

\[
(\alpha_0,\alpha_1,\alpha_2)
=(\gamma_0,\gamma_1,1-\gamma_0-\gamma_1).
\]

The frozen matrix is:

| quantity | value |
|---|---:|
| \(H_{00}\) | `1.0827190778255867e-13` |
| \(H_{01}\) | `-2.1398956298937145e-13` |
| \(H_{11}\) | `6.9621851997301167e-13` |
| \(\det H\) | `2.9589374322645231e-26` |

The determinant is finite and strictly positive. No condition threshold,
regularization, pseudoinverse or lower-depth fallback was used.

## Materialized proposal

The result is

\[
x_{\mathrm{rAA2}}=
-1.2827949098497831x_{\mathrm{roll}}^+
+0.23700413908563411x_{\mathrm{roll2}}^+
+2.0457907707641487x_{\mathrm{AA2}}^+.
\]

The weights sum to one. The negative coefficient and coefficient larger than
one are the unmodified standard AA(2) solution; they were not clipped or
forced into a convex combination. The least-squares problem used only the
dimensionally consistent modal \(A\) residual. The same affine weights were
then applied to the returned `(A,rho,L)` state blocks.

The offline predicted residual square is
`1.0388483301015066e-13`. It is a proposal diagnostic, not a stopping defect
or convergence test.

## Frozen provenance and publication

The generator was frozen at source commit
`81f09bdfd66889cc80730486a59fd6c79dbdbfee`. Its hash-locked inputs were:

| role | SHA-256 |
|---|---|
| \(x_{\mathrm{roll}}\) | `a7166bdfff6a477542118e5f355eacd4e0018c496717cac845df0cd6233108ee` |
| \(x_{\mathrm{roll}}^+\) | `dbb333c8cd1a00a24de40d7b8685349fb83f63a7f0d92c0d2d225c8a25bc07a2` |
| \(x_{\mathrm{roll2}}\) | `5a40b39d7945cfd36c1f2b092c207b5cffb019c7a414ea8b84c478da5174e394` |
| \(x_{\mathrm{roll2}}^+\) | `e95e2a7577d82d9c9b8a28f938a121a4c8409e68764a8cdec9910fb3c1c6d70b` |
| \(x_{\mathrm{AA2}}\) | `aaa0d6afa2883f5eb528c26c466833454629160e2fd1b2f1a2e53a69168183ed` |
| \(x_{\mathrm{AA2}}^+\) | `ebab72eb17b6b70e79fd8b48d0903b3dc9388ca417757efa90730bd3859acc17` |
| latest returned snapshots | `3f71736ec3a7b490f8635e9b0dcd7c365e7be05bc4a5af21232431954ac74f21` |
| rank-two basis | `2d7fc2bf36f65a203731c34dcea18a679fc0232b58c59caad828178a77ff45a8` |

Publication produced:

| quantity | value |
|---|---:|
| affine inverse eigenvalue | `0.73399300356650821` |
| published REAL32 \(k\) | `1.3624107837677002` |
| reciprocal published `rho` | `0.73399301584690513` |
| maximum leakage REAL32 round trip | `5.6988140768876594e-11` |
| minimum published REAL32 \(B_2A\) | `1.7533953643869625e-15` |
| strictly positive \(B_2A\) points | `8880 / 8880` |

The complete latest-returned \(x_{\mathrm{AA2}}^+\) AX/raw-flux and snapshot
payload was carried without affine mixing. The method-level
`AA2-RAW-FLUX` marker is reused; the shifted generation is uniquely bound by
the manifest, artifact path and SHA-256 values. Only the declared proposal
publication fields changed.

## Independent check and receipt

The independently compiled Ganlib-only checker passed the shifted history,
standard two-by-two system, fixed rank-two bundle, exact publication, latest
returned carrier, snapshot lifecycle, stale-record rejection and all-point
positivity. The symbol audit reports `DRAGON/ASM/FLU/TRANSPORT=0`.

The local Git-ignored artifact contains 10 regular files and no symbolic
links. Its 9-entry receipt passes 9/9. The receipt-file SHA-256 is
`741f7a46ff1294b1766e3a5e8cc9c5402b9ec6d9021aac956a11d78ce836b97a`.

| output | SHA-256 |
|---|---|
| `proposal_axial.xsm` | `ce9544e8f58b01d933f5937d781a0f1b70a58862468bbd380d5d2bc5c0e07715` |
| `proposal_snapshots.xsm` | `61604c1dfb586abe71115544aa73b4628f7528f5da32f6bce14ce8f7f8f30763` |
| `build.log` | `8b9fbc92f59e4ce469147915229747cbfe51c6d3f0dcd5017604bb8a0ccfee78` |
| `check.log` | `33bc6e2395c75383f215e701e274c335900c02f9e815625a276ad7635ff0ec7d` |

Reproduce this seconds-scale offline stage with:

```sh
make spot-rank2-modal-aa2-rolling-next-candidate
```

## Scientific boundary

This result establishes one finite, positive, provenance-checked rolling
AA(2) proposal. It did not run Dragon or evaluate
\(G_2(x_{\mathrm{rAA2}})\), and therefore created no raw stopping defect. It
does not establish convergence, stability, contraction, Anderson superiority,
rank adequacy or physical accuracy. No map host or successor calculation was
prepared as part of that offline stage.

## Subsequent real map

A separately frozen, default-off host was later activated exactly once to
evaluate \(G_2(x_{\mathrm{rAA2}})\). The map is valid but does not satisfy the
unchanged stopping gate; see
[rank2_modal_aa2_rolling_next_map_result.md](rank2_modal_aa2_rolling_next_map_result.md).
