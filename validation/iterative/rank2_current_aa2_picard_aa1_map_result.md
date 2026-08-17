# Real map from the latest two-map AA(1) proposal

Date: 2026-08-16

Classification: `VALID_NOT_MET`.

Exactly one evaluation

\[
G_2(s),\qquad
s=0.62153295893235927\,p+0.37846704106764067\,z
\]

ran from source commit `18170cca5fcd7ac30e3768e852ad25bd2ed2ebae`.
There was no relaxation, damping, clipping, fitted coefficient, retry or
fallback.

| solve | `IEXTF` | `EEXT` | `EUNK` | `EINR` | FLU CPU |
|---|---:|---:|---:|---:|---:|
| radial plane 1 | 4 | `0` | `4.70068073e-7` | `2.15294335e-7` | 18 s |
| radial plane 2 | 6 | `0` | `3.56175974e-7` | `4.25450679e-7` | 22 s |
| radial plane 3 | 4 | `0` | `3.04985804e-7` | `3.55782078e-7` | 18 s |
| axial | 228 | `2.15551854e-10` | `3.64224832e-7` | `4.39231798e-7` | 144 s |

All four strict terminals passed before the 120/180-second process bounds.
At the unchanged \(5\times10^{-7}\) outer AND gate:

| quantity | raw value | tolerance multiple | gate |
|---|---:|---:|---|
| \(R_\rho\) | `0` | `0` | pass |
| \(R_L\) | `7.797262126893837e-4` | `1559.452` | fail |
| \(R_a\) | `2.629799345866008e-6` | `5.259599` | fail |

The dimensional diagnostic is
\(D_L=1.142441760748625\times10^{-6}\ \mathrm{cm}^{-1}\). Relative to the
preceding direct \(p\mapsto z\) residual, \(R_L\) and \(D_L\) increased by
93.18%, while \(R_a\) decreased by 24.34%. Thus the offline affine screen
did not predict the nonlinear map's componentwise outcome; it was correctly
used only as an authorization diagnostic, never as convergence acceptance.

The `proposal-z` preflight passed. The independent Ganlib checker passed the
fixed POD package, live radial-operator change, radial positivity, canonical
layout, bitwise raw defects and restart archive. The global and maximum-group
balance diagnostics were `7.64893e-9` and `1.63417e-3`; they are not stopping
defects. The Git-ignored artifact has 22 regular files, no symbolic links and
a passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `d2d16f3b003c6f6f32c3fba4452dca18540302c29c02c7f25a4df1d9be1de696` |
| returned snapshots | `95515fd413fc89d19f522cea8b56b1e43de9c55aa6e054ecbdad5facaeaa3be6` |
| receipt | `2fb2df2ed908ad3628d2c13a6746042f7924f740b31b9705bb1624802a64f93b` |

This is a valid physical map, not a converged rank-two fixed point. No retry,
fallback, empirical control or successor map was started.
