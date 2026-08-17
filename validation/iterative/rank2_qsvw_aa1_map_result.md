# Strict map from the current standard AA(1) state

Date: 2026-08-16

Classification: `VALID_NOT_MET`.

The frozen source at commit
`f4218015e18b588d0eab1e9e5e111d67622649b1` evaluated exactly one map

\[
G_2(y),\qquad
y=0.41386788806042374v+0.58613211193957626w.
\]

The standard full-Gram-height AA(1) coefficient was recomputed from the
actual \(Q(s)\mapsto v\) and \(v\mapsto w\) residuals. The same coefficient
acted on \(A,\rho,L\). There was no clipping, damping, relaxation, separate
leakage fit, empirical coefficient, retry or fallback.

## Strict terminals

| solve | `IEXTF` | `EUNK` | `EINR` |
|---|---:|---:|---:|
| radial plane 1 | 5 | `2.77198950e-7` | `3.70801047e-7` |
| radial plane 2 | 6 | `4.25336566e-7` | `2.92194386e-7` |
| radial plane 3 | 10 | `4.42302877e-7` | `4.81774237e-7` |
| axial | 216 | `4.13012316e-7` | `4.47430040e-7` |

The axial `EEXT` was `5.38676770e-10`. Radial FLU CPU times were 18, 23 and
30 seconds; axial FLU CPU time was 141 seconds. Both Dragon logs contain
exactly one normal termination and no failure marker.

## Original stopping gate

At the unchanged tolerance \(5\times10^{-7}\):

| quantity | raw value | tolerance multiple | gate |
|---|---:|---:|---|
| \(R_\rho\) | `6.422348086676521e-8` | `0.128447` | pass |
| \(R_L\) | `3.238169577271681e-4` | `647.634` | fail |
| \(R_a\) | `5.468734245606544e-7` | `1.09375` | fail |

The dimensional diagnostic is
\(D_L=4.744506441056728\times10^{-7}\,\mathrm{cm}^{-1}\). Relative to the
direct \(v\mapsto w\) map, \(R_L\) and \(D_L\) increased by factors
`1.22853120` and `1.22853160`, while \(R_a\) fell to `0.29140498` of its
previous value. Thus AA(1) nearly closes the modal gate but does not close
the leakage gate. The earlier affine leakage screens were diagnostics, not
predictions of this nonlinear defect.

## Independent evidence

The preflight accepted the exact materialized proposal and complete returned
\(w\) carrier. The post-map checker passed fixed POD-package identity, live
radial-operator change, raw radial positivity, canonical layout, bitwise
recomputation of all four defect fields and restart-archive lifecycle. The
artifact contains 22 regular files, no symlinks, and a passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `80108a5a1690d3f6f44ac68b25e9abf0726dbcd23ad15b54c16ba59dad29d22e` |
| returned snapshots | `5fb806f783afa9f71182da409f3f4d7671f625c4e516383f8e472cd648043f43` |
| receipt | `b41b0ebeea844728acd382cd68c3f39bb8e7ad1a07c09dfc0e3bae5f46682f31` |

Because \(R_L\) and \(R_a\) fail the original AND gate, the declared fixed
point is not yet reached. This three-step experiment stops here and starts no
automatic successor.
