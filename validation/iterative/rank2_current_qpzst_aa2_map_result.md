# Real map from the current three-residual AA(2) proposal

Date: 2026-08-17

Classification: `VALID_NOT_MET`.

Exactly one evaluation

\[
G_2(u),\qquad
u=0.60952347586151479p
 +0.31275948892760236z
 +0.07771703521088286t
\]

ran from source commit `16e4f64c151566d7e6128142160c19e8545c1f7e`.
There was no relaxation, damping, clipping, regularization, fitted
coefficient, retry or fallback.

| solve | `IEXTF` | `EEXT` | `EUNK` | `EINR` | FLU CPU |
|---|---:|---:|---:|---:|---:|
| radial plane 1 | 12 | `0` | `3.25848276e-7` | `3.87398956e-7` | 30 s |
| radial plane 2 | 16 | `0` | `3.22653960e-7` | `2.91130164e-7` | 47 s |
| radial plane 3 | 9 | `0` | `4.57069774e-7` | `4.57069774e-7` | 26 s |
| axial | 181 | `2.30564193e-10` | `4.81847906e-7` | `4.81847906e-7` | 139 s |

All four strict terminals passed before the 120/180-second process bounds.
At the unchanged \(5\times10^{-7}\) outer AND gate:

| quantity | raw value | tolerance multiple | gate |
|---|---:|---:|---|
| \(R_\rho\) | `0` | `0` | pass |
| \(R_L\) | `3.409196005788105e-4` | `681.839` | fail |
| \(R_a\) | `9.153803769526322e-7` | `1.830761` | fail |

The dimensional diagnostic is
\(D_L=4.995090421289206\times10^{-7}\ \mathrm{cm}^{-1}\); it is not compared
with the dimensionless outer tolerance. Relative to the preceding
\(s\mapsto t\) map,
\(R_L\) and \(D_L\) decreased by 56.28%, and \(R_a\) decreased by 65.19%.
Relative to the earlier direct \(p\mapsto z\) map, the decreases are 15.54%,
15.54%, and 73.67%, respectively. This is genuine componentwise progress,
but one map does not establish contraction or asymptotic convergence.

The `proposal-aa2` preflight passed. The independent Ganlib checker passed
the fixed POD package, live radial-operator change, radial positivity,
canonical layout, bitwise raw defects and restart archive. The global and
maximum-group balance diagnostics were `7.47540e-9` and `1.636811e-3`; they
are not stopping defects. The Git-ignored artifact has 22 regular files, no
symbolic links and a passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `3afecce30362c1be25d0ca3f8c6d448b6ac1df09507cc195c4c9f13f012b218d` |
| returned snapshots | `3da1e2402eae543504413387e04b8211052190e2a83ef31f1dd744f4b6e0a8f9` |
| receipt | `a70c8668d7722f325648c9e7ecc4c2a183fd5e045ae4cc176785a5839a250229` |

This is a valid physical map, not a converged rank-two fixed point. No retry,
fallback, empirical control or successor map was started.
