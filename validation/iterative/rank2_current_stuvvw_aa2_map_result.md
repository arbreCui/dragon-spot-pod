# Real map from the chronological AA(2) proposal

Date: 2026-08-17

Classification: `VALID_NOT_MET`.

Exactly one evaluation

\[
G_2(x),\qquad
x=0.31289249339137026\,t
 +0.34535495185011489\,v
 +0.34175255475851485\,w
\]

ran from source commit
`90dce89d7d14f2c35a92137f63c2b7a33983c138`. There was no relaxation,
damping, clipping, empirical coefficient, regularization, retry, fallback,
or automatic successor.

| solve | `IEXTF` | `EEXT` | `EUNK` | `EINR` | FLU CPU |
|---|---:|---:|---:|---:|---:|
| radial plane 1 | 5 | `0` | `3.13219829e-7` | `4.20414977e-7` | 20 s |
| radial plane 2 | 4 | `0` | `4.54414391e-7` | `2.55825540e-7` | 16 s |
| radial plane 3 | 7 | `0` | `3.94446403e-7` | `3.94446403e-7` | 21 s |
| axial | 217 | `4.24525332e-10` | `4.88895239e-7` | `4.88895239e-7` | 144 s |

All strict terminals passed below `4.99999999e-7` before the frozen
120/180-second process bounds. At the unchanged outer AND gate:

| quantity | raw value | tolerance multiple | gate |
|---|---:|---:|---|
| \(R_\rho\) | `6.422348086676521e-8` | `0.128447` | pass |
| \(R_L\) | `6.222282784229706e-4` | `1244.456557` | fail |
| \(R_a\) | `2.472116032661110e-6` | `4.944232` | fail |

The dimensional diagnostic is

\[
D_L=9.116774890571833\times10^{-7}\ \mathrm{cm}^{-1};
\]

it is not compared with the dimensionless stopping tolerance. Relative to
the parent map \(v\mapsto w\), \(R_L\) decreased by 20.533264%, dimensional
\(D_L\) decreased by 20.533245%, and \(R_a\) increased by 63.795202%.
\(R_\rho\) changed from zero to a value still within tolerance, so no
percentage is assigned to that component.

The real map therefore improves leakage locally but is not componentwise
contractive and does not satisfy the original AND gate. This one map proves
neither asymptotic convergence nor global divergence. The offline direction
screen was an authorization diagnostic, not a prediction of the nonlinear
return.

The independent `proposal-aa2` Ganlib checker passed proposal/carrier
identity, fixed POD identity, live radial-operator change, raw radial
positivity, canonical layout, bitwise raw defects, and restart archive. The
global and maximum-group balance diagnostics were `7.427854e-9` and
`1.634292e-3`; they are not stopping defects.

The Git-ignored artifact has 22 regular files, no symbolic links, and a
passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `59969203d2bd1d63bb2546d4c2e5d5eb73b34d85b4b343034042173b83a4a850` |
| returned snapshots | `68bcf1c4887cad4dc2fcfd06ed7d52b7d2191ab2fe4a0a8dddc40e6705bb97b6` |
| receipt | `511ff747823bd5c66ba5cc381d0ab20c5c71ded244b4d98bbb6edfa12f4d0c87` |

This is a valid physical map, not a converged fixed point and not an
inner-solver failure. No retry or successor was started.
