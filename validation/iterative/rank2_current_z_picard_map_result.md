# Direct Picard map from the latest returned state

Date: 2026-08-17

Classification: `VALID_NOT_MET`.

Exactly one direct continuation

\[
z^+=G_2(z)
\]

ran from source commit
`bd1a37ab9c3d4fbe38544f382769bfee90d4efc5`.  The parent \(z\) was used
unchanged; there was no affine proposal, relaxation, damping, clipping,
empirical coefficient, regularization, retry, fallback, or automatic
successor.

| solve | `IEXTF` | `EEXT` | `EUNK` | `EINR` | FLU CPU |
|---|---:|---:|---:|---:|---:|
| radial plane 1 | 5 | `0` | `4.68279552e-7` | `3.81167382e-7` | 20 s |
| radial plane 2 | 3 | `0` | `4.42996992e-7` | `4.42996992e-7` | 15 s |
| radial plane 3 | 7 | `0` | `3.34592556e-7` | `3.43544059e-7` | 24 s |
| axial | 229 | `5.30256339e-10` | `4.81848247e-7` | `4.81848247e-7` | 143 s |

All strict terminals passed below `4.99999999e-7` before the frozen
120/180-second process bounds.  At the unchanged outer AND gate:

| quantity | raw value | tolerance multiple | gate |
|---|---:|---:|---|
| \(R_\rho\) | `6.422349219104007e-8` | `0.128447` | pass |
| \(R_L\) | `8.100798066264695e-4` | `1620.159613` | fail |
| \(R_a\) | `8.933679235907245e-7` | `1.786736` | fail |

The dimensional diagnostic is

\[
D_L=1.186912413686514\times10^{-6}\ \mathrm{cm}^{-1};
\]

it is not compared with the dimensionless stopping tolerance.  The previous
map ended at \(z\), so the two maps are genuinely consecutive.  Relative to
the preceding residual \(z-q\), \(R_L\) increased by 105.430363%,
dimensional \(D_L\) increased by 105.430183%, and \(R_a\) decreased by
67.231352%.  These are observed adjacent residual ratios, not asymptotic
contraction factors.  \(R_\rho\) changed from zero to a value still within
tolerance, so no percentage is assigned to that component.

The direct map therefore shifts the leakage/modal tradeoff rather than
decreasing all defects, and it does not satisfy the original AND gate.  This
one map proves neither asymptotic convergence nor global divergence.

The independent `continued` Ganlib checker passed fixed POD identity, live
radial-operator change, raw radial positivity, canonical layout, bitwise raw
defects, and restart archive.  The global and maximum-group balance
diagnostics were `7.740291e-9` and `1.635778e-3`; they are not stopping
defects.

The Git-ignored artifact has 22 regular files, no symbolic links, and a
passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `b5134a53decba4a4ec1f0717d6632092a69c9e49919673bbb7d1debc70f5d996` |
| returned snapshots | `7cf0a9c87454d1185d4fdc21de521b563491c325949046b00bcaa457ec1874cb` |
| receipt | `5873aaf87c66f54622a39645f34435a5b22b2c664c05dbe3458de7c0c28220db` |

This is a valid physical map, not a converged fixed point and not an
inner-solver failure.  No retry or successor was started.
