# Rolling rank-2 modal Anderson(1) proposal

Date: 2026-08-15

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

## Two latest evaluated residuals

The rolling depth-one history uses exactly the two valid map pairs

\[
x_{\mathrm{AA1}}\longmapsto x_{\mathrm{AA1}}^+,
\qquad
x_{\mathrm{next}}\longmapsto x_{\mathrm{next}}^+.
\]

In the unchanged fixed-rank-two Gram-height metric, define

\[
p=x_{\mathrm{AA1}}^+-x_{\mathrm{AA1}},\qquad
q=x_{\mathrm{next}}^+-x_{\mathrm{next}}.
\]

The standard scalar is

\[
\beta=
\frac{\lVert p\rVert_{HG}^2-\langle p,q\rangle_{HG}}
     {\lVert p-q\rVert_{HG}^2}
=0.560779418805719687,
\]

with denominator `3.4541280335430955e-12`. The resulting proposal is the
affine combination of the two map outputs,

\[
x_{\mathrm{roll}}=
0.439220581194280313x_{\mathrm{AA1}}^+
+0.560779418805719687x_{\mathrm{next}}^+.
\]

The coefficient is naturally between zero and one. It was not clipped,
tuned, relaxed, damped or fitted. The same scalar was applied to canonical
`(A,rho,L)`; raw flux was not mixed. The minimized affine residual norm is
`3.6690574142532690e-7`, or `0.4099641217423281` of \(\lVert q\rVert_{HG}\).
This is only the offline AA(1) linear-combination diagnostic, not
\(\lVert G_2(x_{\mathrm{roll}})-x_{\mathrm{roll}}\rVert\) and not a
convergence factor.

## Publication and lifecycle

The deterministic binary publication produced:

| quantity | value |
|---|---:|
| affine inverse eigenvalue | `0.73399289520686861` |
| published REAL32 \(k\) | `1.3624110221862793` |
| reciprocal published `rho` | `0.73399288739993207` |
| publication shift in `rho` | `-7.8069365416766345e-9` |
| maximum leakage REAL32 round trip | `5.4336837546770100e-11` |
| minimum published REAL32 \(B_2a\) | `1.7533984348813963e-15` |
| strictly positive \(B_2a\) points | `8880 / 8880` |

The published \(k\) and reciprocal `rho` happen to occupy the same REAL32
quantization bin as the input \(x_{\mathrm{next}}\). This does not mean the
proposal is stale: its modal coordinates and leakage changed, and the
independent checker reproduced them bit for bit.

The proposal carries the complete latest-returned
\(x_{\mathrm{next}}^+\) AX/raw-flux payload under the distinct
`XNP-RAW-FLUX` marker. Its snapshot archive is likewise copied from that
returned map. Only the proposed root eigenvalue and `FLUX/SPOT-LEAK1D` are
published; the lagged `SYSTEM` remains the actual
\(x_{\mathrm{next}}\to x_{\mathrm{next}}^+\) solve history.

## Independent audit and receipt

The independently compiled Ganlib-only checker passed:

- both exact map-pair identities and the fixed rank-two bundle;
- bitwise affine publication of coordinates, leakage and eigenvalue;
- complete latest AX/raw-flux and snapshot carrier identity;
- the \(x_{\mathrm{next}}\to x_{\mathrm{next}}^+\) lagged lifecycle;
- absence of stale defect, balance and epoch records;
- strict positivity at all 8880 reconstructed points.

The builder/checker symbol audit reports
`DRAGON/ASM/FLU/TRANSPORT=0`. The Git-ignored artifact
`validation/artifacts/iterative-rank2-modal-aa1-rolling-candidate` contains
10 regular files and no symbolic links. Its 9-entry receipt passes 9/9; the
receipt-file SHA-256 is
`25607b65e39374d81b2994873292ba64a00f514d1edc26cc0801a5309edcf272`.

| output | SHA-256 |
|---|---|
| `proposal_axial.xsm` | `a7166bdfff6a477542118e5f355eacd4e0018c496717cac845df0cd6233108ee` |
| `proposal_snapshots.xsm` | `6762e58a75cc2bcbffae476187389797a9aebf95e8619355060b6de9c41b5102` |

Reproduce this seconds-scale offline stage with:

```sh
make spot-rank2-modal-aa1-rolling-candidate
```

## Scientific boundary

This result establishes one deterministic, positive and provenance-checked
rolling AA(1) proposal. It does not evaluate \(G_2(x_{\mathrm{roll}})\),
produce a new raw stopping defect or establish convergence, contraction,
stability, Anderson superiority, rank adequacy or physical accuracy. No
Dragon process, physical-map host or successor map was started.
