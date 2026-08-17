# Direct map from the latest returned state v

Date: 2026-08-16

Classification: `VALID_NOT_MET`.

Exactly one frozen evaluation

\[
w=G_2(v)
\]

ran from source commit `2243d63`. The parent AX and snapshots were locked at
`0842ea931a0b53babb7ea7cde6af459ad86d219ea70e83f1242b7b86ce2bf737`
and `a701f41dfc42fb31043befad8c3607d669bbba456c1dda663a6c6a1873d1f9ed`.
The unchanged host performed three online radial fixed-source transport
solves and one axial solve. There was no proposal, mixing, empirical
coefficient, retry or fallback.

## Strict terminals

| solve | `IEXTF` | `EUNK` | `EINR` |
|---|---:|---:|---:|
| radial plane 1 | 16 | `4.29631740e-7` | `3.64848432e-7` |
| radial plane 2 | 5 | `4.99307419e-7` | `4.37952252e-7` |
| radial plane 3 | 5 | `4.06389290e-7` | `4.54336089e-7` |
| axial | 198 | `3.44177010e-7` | `4.68291660e-7` |

The axial `EEXT` was `2.88277069e-10`. Radial FLU CPU times were 39, 22 and
20 seconds; axial FLU CPU time was 139 seconds. Each Dragon log contains one
normal termination and no failure marker.

## Original stopping gate

For the unchanged tolerance \(5\times10^{-7}\):

| quantity | raw value | tolerance multiple | gate |
|---|---:|---:|---|
| \(R_\rho\) | `6.422349219104007e-8` | `0.128447` | pass |
| \(R_L\) | `2.635805720887253e-4` | `527.161` | fail |
| \(R_a\) | `1.876678378894124e-6` | `3.75336` | fail |

The dimensional leakage diagnostic is
\(D_L=3.861932782456279\times10^{-7}\,\mathrm{cm}^{-1}\). Relative to the
preceding \(Q(s)\mapsto v\) map, the ratios for
\((R_\rho,R_L,D_L,R_a)\) are respectively
`0.500000044`, `0.626392660`, `0.626392560`, and `0.707341888`.
This is local componentwise improvement, not a contraction proof.

## Independent evidence

The checker passed fixed POD-package identity, live radial-operator change,
raw radial positivity, canonical layout, bitwise recomputation of all four
defect fields and restart-archive lifecycle. The artifact contains 22 regular
files, no symlinks, and a passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `defdee0cf442470eb623ebb83c8bed59b8c20308121951ef0c72073ddba3c243` |
| returned snapshots | `661fa88ed1a8a08907d5a31d90a367565a5c3dbcd0e50a8c3ccecc866436f1ca` |
| receipt | `848eaaa1fb440c077382940774f1b281417eb95bb50a75408554f64deb512916` |

Only \(R_\rho\) passes the AND gate, so this map is valid but not converged.
