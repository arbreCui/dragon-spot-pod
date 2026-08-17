# Direct Picard map from the newest returned state

Date: 2026-08-17

Classification: `VALID_NOT_MET`.

Exactly one direct continuation

\[
r^+=G_2(r)
\]

ran from source commit
`f3b3bdd10ac2e7d843621fff083c3d54808b1795`.  The parent $r$ was used
unchanged; there was no affine map parent, state mixing, relaxation,
damping, clipping, empirical coefficient, regularization, retry, fallback,
or automatic successor.

| solve | `IEXTF` | `EEXT` | `EUNK` | `EINR` | FLU CPU |
|---|---:|---:|---:|---:|---:|
| radial plane 1 | 11 | `0` | `3.76522820e-7` | `4.05885345e-7` | 28 s |
| radial plane 2 | 6 | `0` | `4.63729123e-7` | `2.40203605e-7` | 22 s |
| radial plane 3 | 7 | `0` | `4.46124005e-7` | `2.73050802e-7` | 23 s |
| axial | 180 | `3.19163890e-10` | `4.68292768e-7` | `4.81847621e-7` | 134 s |

All strict terminals passed below `4.99999999e-7` before the frozen
120/180-second process bounds.  At the unchanged outer AND gate:

| quantity | raw value | tolerance multiple | gate |
|---|---:|---:|---|
| $R_\rho$ | `6.422349219104007e-8` | `0.128447` | pass |
| $R_L$ | `7.479256400660744e-4` | `1495.851280` | fail |
| $R_a$ | `3.642420375064784e-6` | `7.284841` | fail |

The dimensional diagnostic is

\[
D_L=1.095846528187394\times10^{-6}\ \mathrm{cm}^{-1};
\]

it is not compared with the dimensionless stopping tolerance.  The previous
map ended at $r$, so the two maps are genuinely consecutive.  Relative to
the preceding residual $r-z$, $R_L$ decreased by 7.672597941%, dimensional
$D_L$ decreased by 7.672502575%, and $R_a$ increased by 307.717837061%.
The reported $R_\rho$ value was unchanged.  These are observed adjacent
residual ratios, not asymptotic contraction factors.

The direct map again shifts the leakage/modal tradeoff rather than
decreasing all defects, and it does not satisfy the original AND gate.  In
combination with the preceding direct map it shows alternating local defect
directions, but it proves neither a periodic orbit, asymptotic convergence,
nor global divergence.

The independent `continued` Ganlib checker passed fixed POD identity, live
radial-operator change, raw radial positivity, canonical layout, bitwise raw
defects, and restart archive.  The global and maximum-group balance
diagnostics were `7.822627e-9` and `1.634200e-3`; they are not stopping
defects.

The Git-ignored artifact has 22 regular files, no symbolic links, and a
passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `d8d74dd3e3b0910291df7a9d1b63976f8f9ac631a9bfdf9cb879327e5495bee3` |
| returned snapshots | `103ef77e094c3869d8b2ebca64d50b0ea38f6ef37e0b1d5f1356a963d349afd5` |
| receipt | `0caa7a26c39d67fe2c17270178594506691616c47244e6392d40ed22fc238b90` |

This is a valid physical map, not a converged fixed point and not an
inner-solver failure.  No retry or successor was started.
