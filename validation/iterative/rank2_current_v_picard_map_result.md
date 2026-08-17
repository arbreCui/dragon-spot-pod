# Direct Picard map from the latest returned state

Date: 2026-08-17

Classification: `VALID_NOT_MET`.

Exactly one direct evaluation

\[
w=G_2(v),\qquad v=G_2(u)
\]

ran from source commit
`073f54ba826a745eb498b27d66cc759b7693a93f`. The complete returned
AX/snapshot state \(v\) was used directly. There was no affine proposal,
mixing, relaxation, damping, empirical coefficient, retry, fallback, or
automatic successor.

| solve | `IEXTF` | `EEXT` | `EUNK` | `EINR` | FLU CPU |
|---|---:|---:|---:|---:|---:|
| radial plane 1 | 4 | `0` | `4.27578982e-7` | `2.85403644e-7` | 16 s |
| radial plane 2 | 10 | `0` | `4.31685123e-7` | `4.53413520e-7` | 30 s |
| radial plane 3 | 12 | `0` | `4.75304745e-7` | `4.20048934e-7` | 28 s |
| axial | 168 | `6.83497980e-10` | `4.20306321e-7` | `4.81847337e-7` | 139 s |

All strict terminals passed below `4.99999999e-7` before the frozen
120/180-second process bounds. At the unchanged outer AND gate:

| quantity | raw value | tolerance multiple | gate |
|---|---:|---:|---|
| \(R_\rho\) | `0` | `0` | pass |
| \(R_L\) | `7.830047040270425e-4` | `1566.009408` | fail |
| \(R_a\) | `1.509272560716544e-6` | `3.018545` | fail |

The dimensional diagnostic is

\[
D_L=1.147243892773986\times10^{-6}\ \mathrm{cm}^{-1};
\]

it is not compared with the dimensionless stopping tolerance. Relative to
the parent map \(u\mapsto v\), \(R_\rho\) remains exactly zero,
\(R_L\) and \(D_L\) increased by 129.6743%, and \(R_a\) increased by
64.8793%. Thus ordinary Picard is not componentwise contractive at this
observed state. This one map does not prove global Picard divergence, infer a
spectral radius, or rule out the fixed-rank-two SPOD formulation.

The independent `continued` Ganlib checker passed fixed POD identity, live
radial-operator change, raw radial positivity, canonical layout, bitwise raw
defects, and restart archive. The global and maximum-group balance
diagnostics were `7.658218e-9` and `1.635178e-3`; they are not stopping
defects.

The Git-ignored artifact has 22 regular files, no symbolic links, and a
passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `00066b1bf2314b4bda3c435cb687a07deab41829268b69ab3337aefbfb0dbddc` |
| returned snapshots | `2f99d188dd0d36cd980b2731dcef325508e91382dadbd4e3bacd34e10f706485` |
| receipt | `4224a78074c05eef3dbaaa56552bc3011c5af217a23723aa275f3d1d1075e4d2` |

This is a valid physical map, not a converged fixed point and not an
inner-solver failure. No retry or successor was started.
