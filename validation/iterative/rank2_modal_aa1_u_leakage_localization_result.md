# Leakage-residual localization after the direct Picard continuation

Date: 2026-08-15

Classification: `OFFLINE_LOCALIZATION_COMPLETE`.

## Scope

This read-only Ganlib calculation used the three frozen canonical states

\[
x_1=u_{\rm pub},\qquad x_2=G_2(u_{\rm pub}),\qquad x_3=G_2(x_2).
\]

It ran no Dragon, transport, assembly, SPOT map, proposal publication or
model update. The checker independently recomputed both maps' saved defects
bit for bit before examining the REAL64 `SPOT-X-L` fields.

| state | AX SHA-256 |
|---|---|
| \(x_1\) | `77a4bc3916db21064dc2bae73a0397faeb15fb8033de6f761fcaa4cfd0f6852b` |
| \(x_2\) | `046a4ff0cd5bd87af59688ba6a01d5de6155e9a71da82d3c97c57ac17abb3bba` |
| \(x_3\) | `8db8a8d3c1d9c3c0085b2e106f8a5bbbab3899bbccfbfa073fa801c6d33d67b5` |

The strict checker was compiled with no fast-math contraction. Its source
SHA-256 was
`fd93451890494909b5fc78f14032191e377e014507e7d4e15bf0454b31343665`.

## Exact leakage quantities

For each adjacent pair,

\[
D_L=\lVert L_{j+1}-L_j\rVert_\infty,\qquad
R_L=\frac{D_L}{\max(\lVert L_j\rVert_\infty,
\lVert L_{j+1}\rVert_\infty)}.
\]

The state maxima are:

| state | \(\lVert L\rVert_\infty\) (`cm^-1`) | first snapshot/group | ties | sign |
|---|---:|---:|---:|---:|
| \(x_1\) | `1.46513560321182013e-3` | `2 / 1` | `1` | positive |
| \(x_2\) | `1.46519986446946859e-3` | `2 / 1` | `1` | positive |
| \(x_3\) | `1.46517378743737936e-3` | `2 / 1` | `1` | positive |

Therefore both adjacent \(R_L\) denominators are exactly the same middle-state
value, `1.46519986446946859e-3 cm^-1`. Algebraically, the \(R_L\) ratio is the
\(D_L\) ratio before floating-point rounding; the stored ratios agree to
roundoff:

\[
\frac{D_L^{23}}{D_L^{12}}=1.29152325695741954.
\]

The 29.1523% rebound is therefore caused by the larger absolute leakage
increment, not by a normalization-scale change.

## Hotspots and signs

| map | unique hotspot | left \(L\) | right \(L\) | signed increment (`cm^-1`) |
|---|---|---:|---:|---:|
| \(x_1\to x_2\) | snapshot 1, group 328 | `4.78945876238867640e-4` | `4.79537789942696691e-4` | `+5.91913703829050064e-7` |
| \(x_2\to x_3\) | snapshot 1, group 326 | `3.97603202145546675e-4` | `3.96838731830939651e-4` | `-7.64470314607024193e-7` |

At the new snapshot-1/group-326 hotspot, the preceding increment was
`+5.56348823010921478e-7 cm^-1`; the next increment is larger and has the
opposite sign. At the old group-328 hotspot, the next increment is
`-6.95581547915935516e-9 cm^-1`, also opposite in sign. Positive leakage
denotes net axial loss, so these signs are physical signed changes, not
absolute-value labels.

The height-weighted leakage-update cosine is `-0.359139282908113755` and its
successive norm ratio is `0.453564277917984426`. This non-production
diagnostic says that the overall leakage update shrank in that auxiliary norm
even while the worst infinity-norm component grew. It cannot be described as
uniform leakage deterioration. The indices above are stored snapshot indices,
not claims about individual physical axial floors.

## Scientific boundary

The direct Picard leakage response is not componentwise monotone, its maximum
change moved from group 328 to group 326, and the new hotspot reversed sign.
This is evidence of a local oscillatory tendency. It does not establish an
exact two-cycle, convergence, divergence, stability, the physical or
numerical cause, rank adequacy or physical accuracy. No new map or candidate
was created.
