# Direct Picard map from the current AA(2) return

Date: 2026-08-16

Classification: `VALID_NOT_MET`.

Exactly one direct evaluation

\[
z=G_2(p),\qquad p=G_2(q_{\mathrm{AA2}})
\]

ran from source commit
`613eb436752c02091d2f10eaf4f136125e9480c1`. The complete preceding
returned AX/snapshot state was used directly. No affine proposal, mixing,
relaxation, damping, retry or fallback was used.

| solve | `IEXTF` | `EUNK` | `EINR` | FLU CPU |
|---|---:|---:|---:|---:|
| radial plane 1 | 4 | `2.83311778e-7` | `4.99506257e-7` | 17 s |
| radial plane 2 | 5 | `4.72452143e-7` | `4.88506544e-7` | 18 s |
| radial plane 3 | 11 | `4.35771540e-7` | `2.74241131e-7` | 30 s |
| axial | 228 | `3.64224150e-7` | `4.20307543e-7` | 139 s |

The axial `EEXT` was `6.05524630e-10`. All four strict terminals passed
before the frozen 120/180-second process bounds.

At the unchanged \(5\times10^{-7}\) outer gate:

| quantity | raw value | tolerance multiple | gate |
|---|---:|---:|---|
| \(R_\rho\) | `6.422348086676521e-8` | `0.128447` | pass |
| \(R_L\) | `4.036291023574800e-4` | `807.258` | fail |
| \(R_a\) | `3.476035708619729e-6` | `6.952071` | fail |

The dimensional leakage diagnostic is

\[
D_L=5.913898348808289\times10^{-7}\ \mathrm{cm}^{-1}.
\]

Relative to its current-AA(2) parent map, \(R_L\) and \(D_L\) decreased
by 35.15%, while \(R_a\) increased by 64.06%. Direct substitution therefore
continued the leakage improvement but did not restore the modal defect. This
single observation is not a proof of monotonicity, contraction or divergence.

The independent `--continued` Ganlib checker passed fixed POD identity,
live radial-operator change, radial positivity, canonical layout, bitwise raw
defects and restart lifecycle. The reported global and maximum-group balance
diagnostics were `7.71936e-9` and `1.63416e-3`; they are not stopping
defects.

The Git-ignored artifact contains 22 regular files, no symbolic links and a
passing 21/21 payload receipt.

| output | SHA-256 |
|---|---|
| returned AX | `38140efb4ac6a9e8bed40dbd026cb6b14172bca1a85d16f28580228cdf12736d` |
| returned snapshots | `ab1283957e066894037b1bf37832346b75c6cebbf1795bf6e938d8f96cc68c84` |
| receipt | `8fbb9d76c88cab7b6c6899a00d39f4f94556e77af20ba5aa7d8f78d6b4349f65` |

This is a valid map, not a converged rank-two fixed point. No retry,
successor proposal or successor map was started.
