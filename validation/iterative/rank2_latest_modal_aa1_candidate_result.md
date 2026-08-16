# Latest consecutive rank-2 modal Anderson(1) proposal

Date: 2026-08-16

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

## Latest consecutive history

The existing fixed-rank-two states form two consecutive direct Picard pairs:

\[
x_3=G_2(x_2),\qquad x_4=G_2(x_3).
\]

In the unchanged Gram-height modal metric, their modal residuals
\(f_{23}^a=A_3-A_2\) and \(f_{34}^a=A_4-A_3\) satisfy

| quantity | value |
|---|---:|
| \(\lVert f_{23}^a\rVert\) | `9.850448578597241e-7` |
| \(\lVert f_{34}^a\rVert\) | `1.934045083505154e-6` |
| cosine | `-0.9850841617639620` |
| norm ratio | `1.963408131186421` |

Thus the latest modal update is nearly opposite to, and larger than, its
predecessor. This geometry accompanies the local modal-defect rebound but is
not a cycle, divergence or stability result.

## Standard AA(1) choice

The standard depth-one coefficient is the unique minimizer of

\[
\left\lVert(1-\beta)f_{23}^a+\beta f_{34}^a\right\rVert^2
\]

and is computed directly as

\[
\beta=
\frac{\lVert f_{23}^a\rVert^2-
\langle f_{23}^a,f_{34}^a\rangle}
{\lVert f_{34}^a-f_{23}^a\rVert^2}
=0.33635785867426299.
\]

The denominator is `8.4642531275618504e-12`, which is finite and strictly
positive. No threshold, regularization, pseudoinverse, clipping, fallback or
prescribed relaxation is used. The pre-publication coupled proposal is

\[
y=0.66364214132573696\,x_3+
0.33635785867426299\,x_4.
\]

The same scalar weights are applied to the canonical \((A,\rho,L)\) blocks;
no mixed-unit full-state norm or separate block coefficient is introduced.
The affine modal residual prediction is `1.126786343888073e-7`, or
`0.05826060382449558` of the latest modal residual. This is an offline linear
diagnostic, not \(G_2(y)-y\), \(R_a\), or a stopping result.

The leakage updates have height-\(L_2\) cosine `-0.05837985650454977`, and
the production infinity-norm hotspot moves from snapshot 1/group 327 to
snapshot 3/group 325. Applying the same \(\beta\) gives an offline
height-\(L_2\) leakage prediction `0.8278580701177356` of the latest update.
Therefore this proposal is not claimed to solve the leakage defect.

## Publication and carrier

The materialized object is \(Q(y)\), not the unrounded affine state. The
modal coordinates remain the REAL64 affine values. Leakage is published
through the production REAL32 round trip; the eigenvalue is published in
REAL32 and stored \(\rho\) is its REAL64 reciprocal. The frozen results are:

| quantity | value |
|---|---:|
| affine \(\rho\) | `0.73399284477853100` |
| published REAL32 \(k\) | `1.3624111413955688` |
| reciprocal published \(\rho\) | `0.73399282317646231` |
| maximum leakage round trip | `5.3649504977437701e-11` |
| minimum published REAL32 \(B_2A\) | `1.7534012936175933e-15` |
| strictly positive points | `8880 / 8880` |

The \(x_4\) AX/raw-flux and snapshot objects are used as complete carriers
rather than affine-mixed raw fields; only the declared proposal and
publication fields are replaced. The checker independently verifies the
fixed rank-two bundle, publication arithmetic, axial and plane raw flux,
snapshot leakage and eigenvalue publication, lagged `SYSTEM` history, and
absence of stale result records. The proposal is explicitly marked
`X4-RAW-FLUX`.

## Frozen provenance and receipt

The source was frozen at commit
`0d9473f29707c7d9cb107aaa5612761d4235f948`. The five hash-locked inputs are:

| role | SHA-256 |
|---|---|
| \(x_2\) AX | `21e5f4e8660020aee9509a656993c45049deb9a01029d86e63801432c948ab67` |
| \(x_3\) AX | `154c707c0f21a1241fad0c887486867e9953af794fec0aa883220d669de74651` |
| \(x_4\) AX | `ee50a8cb438aba8bb36a30613975d92bdc93528b070bd61d1a43f2d17e53cc08` |
| \(x_4\) snapshots | `4b5deac64ec6ab50cd9c1c7a9e868f824bb2078895492eeb56c95863bd85e87a` |
| rank-two basis | `2d7fc2bf36f65a203731c34dcea18a679fc0232b58c59caad828178a77ff45a8` |

The builder and independent checker symbol census reports
`DRAGON/ASM/FLU/TRANSPORT=0`. The Git-ignored artifact contains 10 regular
files and no symbolic links. Its nine-entry receipt passes 9/9, with receipt
SHA-256
`0ab7e28a1f5924d5fc369ed6335abfdc02b4d8f6f2702c631e0dcebb0375e241`.

| output | SHA-256 |
|---|---|
| `proposal_axial.xsm` | `0c7d94c9df4b1a7f7f94b8a9d54eb51aacfcead8ab34d5f288c85351b1c0ab9d` |
| `proposal_snapshots.xsm` | `b5d03cb519ce54f0ade469288f70a50e303bb6a7bd7d4396c04558d38ffd108b` |
| `build.log` | `58969c296c9aeb10363c63a529b0de770d4ffa01598098a840ae9546068ae27d` |
| `check.log` | `950c2784394807ba4eaf7b42cbe644ad28452ac12c7f9eb651d16db64a3b7202` |

Reproduce this seconds-scale offline stage with:

```sh
make spot-rank2-latest-modal-aa1-candidate
```

## Scientific boundary

This stage materializes and verifies exactly one standard modal AA(1)
proposal. It performs no Dragon, radial solve, axial solve or map evaluation,
so it creates no new raw stopping defects and establishes no convergence,
stability, contraction, solver superiority, rank adequacy or physical
accuracy. No map host, retry, \(x_5\), or further proposal was prepared or
started. A later test, if separately authorized, must evaluate exactly one
unchanged \(G_2(Q(y))\) and use only the original three-component AND gate.
