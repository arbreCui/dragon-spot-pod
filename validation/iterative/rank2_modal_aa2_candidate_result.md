# Standard rolling rank-2 modal Anderson(2) proposal

Date: 2026-08-16

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

## Three real map residuals

The offline proposal uses exactly the three latest valid evaluations of the
same fixed-rank map:

\[
x_i^+=G_2(x_i),\qquad
(x_0,x_1,x_2)=(x_{\mathrm{next}},x_{\mathrm{roll}},x_{\mathrm{roll2}}).
\]

For the canonical modal coordinate, define

\[
f_i=A_i^+-A_i,
\]

and retain the existing Gram-height inner product. With
\(d_0=f_0-f_2\) and \(d_1=f_1-f_2\), standard AA(2) solves

\[
\begin{bmatrix}
\langle d_0,d_0\rangle & \langle d_0,d_1\rangle\\
\langle d_0,d_1\rangle & \langle d_1,d_1\rangle
\end{bmatrix}
\begin{bmatrix}\gamma_0\\\gamma_1\end{bmatrix}
=-
\begin{bmatrix}\langle d_0,f_2\rangle\\\langle d_1,f_2\rangle\end{bmatrix},
\]

then sets

\[
(\alpha_0,\alpha_1,\alpha_2)
=(\gamma_0,\gamma_1,1-\gamma_0-\gamma_1).
\]

The frozen matrix entries and determinant are:

| quantity | value |
|---|---:|
| \(H_{00}\) | `1.4560474354466529e-12` |
| \(H_{01}\) | `1.2271401167983124e-12` |
| \(H_{11}\) | `1.2324695537343101e-12` |
| \(\det H\) | `2.8866126672514724e-25` |

The determinant is finite and strictly positive. No condition threshold,
regularization, pseudoinverse or lower-depth fallback was used.

## Materialized proposal

The resulting returned-state combination is

\[
x_{\mathrm{AA2}}=
0.77664274528264354x_{\mathrm{next}}^+
-0.54521415283366947x_{\mathrm{roll}}^+
+0.76857140755102593x_{\mathrm{roll2}}^+.
\]

The weights sum to one. The negative middle weight is a direct result of the
unconstrained standard AA(2) problem; convexity was not imposed and the
coefficient was not modified. The same three weights were applied to the
canonical `(A,rho,L)` blocks, while the least-squares problem used only the
dimensionally consistent modal \(A\) residual.

The offline minimized residual square is
`6.3093775537668655e-14`. It is a proposal screen, not a stopping defect or
convergence test.

## Frozen provenance and publication

The generator was frozen at source commit
`ad1849f3940e08e48008239cdb16840cb59d09bd`. Its hash-locked inputs were:

| role | SHA-256 |
|---|---|
| \(x_{\mathrm{next}}\) | `58972931170d744f109550866b65a8d2cbf22204ef1fe99cef634c4187d59d89` |
| \(x_{\mathrm{next}}^+\) | `dfe9bc56a38c44799b63f5086aaecfbd24a9060d1dc45bbc6ca721d1c4c2c89d` |
| \(x_{\mathrm{roll}}\) | `a7166bdfff6a477542118e5f355eacd4e0018c496717cac845df0cd6233108ee` |
| \(x_{\mathrm{roll}}^+\) | `dbb333c8cd1a00a24de40d7b8685349fb83f63a7f0d92c0d2d225c8a25bc07a2` |
| \(x_{\mathrm{roll2}}\) | `5a40b39d7945cfd36c1f2b092c207b5cffb019c7a414ea8b84c478da5174e394` |
| \(x_{\mathrm{roll2}}^+\) | `e95e2a7577d82d9c9b8a28f938a121a4c8409e68764a8cdec9910fb3c1c6d70b` |
| latest returned snapshots | `bf08f193d745e1bbf66fc200f5fd8041b3b8eb37d1aa0e6b33757ca60f59eeb4` |
| rank-two basis | `2d7fc2bf36f65a203731c34dcea18a679fc0232b58c59caad828178a77ff45a8` |

Publication produced:

| quantity | value |
|---|---:|
| affine inverse eigenvalue | `0.73399288791831008` |
| published REAL32 \(k\) | `1.3624110221862793` |
| reciprocal published `rho` | `0.73399288739993207` |
| maximum leakage REAL32 round trip | `4.8611993120131758e-11` |
| minimum published REAL32 \(B_2A\) | `1.7533970584528570e-15` |
| strictly positive \(B_2A\) points | `8880 / 8880` |

The complete latest-returned \(x_{\mathrm{roll2}}^+\) AX/raw-flux and
snapshot payload was carried without affine mixing under the distinct
`AA2-RAW-FLUX` marker. Only the declared proposal publication fields changed.

## Independent check and receipt

The independently compiled Ganlib-only checker passed the standard
two-by-two system, fixed rank-two bundle, exact publication, latest returned
carrier, snapshot lifecycle, stale-record rejection and all-point positivity.
The builder/checker symbol audit reports `DRAGON/ASM/FLU/TRANSPORT=0`.

The local Git-ignored artifact contains 10 regular files and no symbolic
links. Its 9-entry receipt passes 9/9. The receipt-file SHA-256 is
`68edf666581f84e64e342f8e2229db8059ccaae730807f2b0b2af458041c2270`.

| output | SHA-256 |
|---|---|
| `proposal_axial.xsm` | `aaa0d6afa2883f5eb528c26c466833454629160e2fd1b2f1a2e53a69168183ed` |
| `proposal_snapshots.xsm` | `a6231acf84ed551e9144811c4bc775368c4a21132817ac757143a4c7e74d51dc` |
| `build.log` | `e5ec1cc70391bad2b912f0610832784948933ea9670f6c3bf148906270148572` |
| `check.log` | `5cccc5f718f2ae90e17358819c457963d94f2092b9a175e76e0c127e50092993` |

Reproduce this seconds-scale offline stage with:

```sh
make spot-rank2-modal-aa2-candidate
```

## Scientific boundary

This result establishes one finite, positive, provenance-checked standard
AA(2) proposal. It did not run Dragon or evaluate
\(G_2(x_{\mathrm{AA2}})\), and therefore created no raw stopping defect and
does not establish convergence, stability, contraction, Anderson superiority,
rank adequacy or physical accuracy. No map calculation or successor state was
produced.

## Subsequent one-map evaluation

A dedicated default-off host was later prepared for exactly one evaluation
of \(G_2(x_{\mathrm{AA2}})\). It keeps the fixed rank-two basis, physical
decks and three-component stopping gate unchanged, requires the exact
`AA2-RAW-FLUX` carrier and permits no retry or automatic successor. That host
was subsequently activated once. The map is valid but does not meet the
unchanged stopping rule; see
[rank2_modal_aa2_map_result.md](rank2_modal_aa2_map_result.md).
