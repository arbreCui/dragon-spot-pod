# Real map from the latest chronological AA(2) proposal

Date: 2026-08-17

Classification: `VALID_NOT_MET`.

Exactly one evaluation

\[
G_2(q_2),\qquad
q_2=0.39248173027184491\,v
   +0.28907503340209423\,w
   +0.31844323632606092\,y
\]

ran from source commit
`9b23fd05e8359a381643839309e13a1b688afa57`.  There was no relaxation,
damping, clipping, empirical coefficient, regularization, retry, fallback,
or automatic successor.

| solve | `IEXTF` | `EEXT` | `EUNK` | `EINR` | FLU CPU |
|---|---:|---:|---:|---:|---:|
| radial plane 1 | 3 | `0` | `4.48594278e-7` | `2.99994838e-7` | 15 s |
| radial plane 2 | 5 | `0` | `4.30334268e-7` | `3.99002886e-7` | 20 s |
| radial plane 3 | 9 | `0` | `4.46329210e-7` | `3.43542808e-7` | 27 s |
| axial | 221 | `2.33117581e-10` | `4.16257961e-7` | `4.81848417e-7` | 143 s |

All strict terminals passed below `4.99999999e-7` before the frozen
120/180-second process bounds.  At the unchanged outer AND gate:

| quantity | raw value | tolerance multiple | gate |
|---|---:|---:|---|
| \(R_\rho\) | `0` | `0` | pass |
| \(R_L\) | `3.943330456018398e-4` | `788.666091` | fail |
| \(R_a\) | `2.726288639012558e-6` | `5.452577` | fail |

The dimensional diagnostic is

\[
D_L=5.777692422270775\times10^{-7}\ \mathrm{cm}^{-1};
\]

it is not compared with the dimensionless stopping tolerance.  Against the
preceding evaluated map \(x\mapsto y\), \(R_L\) decreased by 36.625663%,
dimensional \(D_L\) decreased by 36.625698%, and \(R_a\) increased by
10.281581%.  This is a cross-input defect comparison, not a contraction
factor.  \(R_\rho\) changed from a passing nonzero value to zero; no
percentage is assigned to that component.

The real map therefore improves leakage locally, but its defects are not
componentwise decreasing and it does not satisfy the original AND gate.
This one map proves neither asymptotic convergence nor global divergence.
The offline direction screen was an authorization diagnostic, not a
prediction of the nonlinear return.

The independent `proposal-aa2` Ganlib checker passed proposal/carrier
identity, fixed POD identity, live radial-operator change, raw radial
positivity, canonical layout, bitwise raw defects, and restart archive.  The
global and maximum-group balance diagnostics were `7.945596e-9` and
`1.639197e-3`; they are not stopping defects.

The Git-ignored artifact has 22 regular files, no symbolic links, and a
passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `bef525612a58ab3238f203b6aad30293bd1679c149e6c2ad304a08a489af039a` |
| returned snapshots | `4086ab801cda83ab251ece9f0acc3a59df1527c3abdb080400d2ebed6c9638d7` |
| receipt | `e52c83244ccd557e0510cf58e29a73b99961891fe9516b13d646166a6736b726` |

This is a valid physical map, not a converged fixed point and not an
inner-solver failure.  No retry or successor was started.
