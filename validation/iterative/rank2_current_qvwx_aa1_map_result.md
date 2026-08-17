# Physical map from the current $qvwx$ AA(1) proposal

Date: 2026-08-17

Classification: `VALID_NOT_MET`.

The standard full-Gram proposal

$$
y=0.88057313037525409\,v
 +0.11942686962474590\,x
$$

was evaluated exactly once.  The map performed three fresh online radial
fixed-source solves and one axial solve.  It returned

$$
(R_\rho,R_L,D_L,R_a)=
(0,\,
3.779851170520331\times10^{-4},\,
5.538167897611856\times10^{-7}\ \mathrm{cm}^{-1},\,
1.841719645535316\times10^{-6}).
$$

At the unchanged $5\times10^{-7}$ three-component AND gate, $R_\rho$
passes.  $R_L$ and $R_a$ fail at `755.970234` and `3.683439` tolerance
multiples.  Dimensional $D_L$ is diagnostic only and is not part of that
gate.  SPOT therefore still has no accepted rank-two fixed point.

Compared with the preceding evaluated residual $x-w$, $R_L$ and $D_L$
decreased by `20.0529685%` and `20.0529367%`, while $R_a$ increased by
`32.1654259%`; the stored raw $R_\rho$ changed to zero, which by itself is
not evidence of an exact fixed point.  Because the inputs $w$ and $y$
differ, this is a cross-input nonlinear response, not a contraction,
divergence, or cycle measure.  The offline AA(1) direction screen is an
authorization test, not a prediction of the realized nonlinear defect.

## Strict solver terminals

| solve | IEXTF | EUNK | ITERF | EINR | FLU time |
|---|---:|---:|---:|---:|---:|
| radial snapshot 1 | 4 | `4.65098708e-7` | 3 | `4.32411440e-7` | 15 s |
| radial snapshot 2 | 2 | `4.85760609e-7` | 4 | `1.98957736e-7` | 14 s |
| radial snapshot 3 | 10 | `2.79664505e-7` | 4 | `2.09778577e-7` | 27 s |
| axial | 174 | `4.13013311e-7` | 1 | `4.35567586e-7` | 135 s |

The axial eigenvalue terminal has `EEXT=2.70215045e-10`.  The independent
Ganlib checker passed the proposal lifecycle, fixed POD package, live radial
operator, raw radial positivity, canonical layout, all four raw defects,
and restart archive.  The global balance diagnostic is `7.28486e-9`; it is
separate from the outer fixed-point gate.

## Reproducibility

The default-off host was activated once from source commit
`523d5adcbf2deb5c951c5c56634ff86fc7fcac83`.  It made no retry, fallback,
or automatic successor.  The artifact contains 22 regular files, no
symbolic links, and a passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `2c2649c4317cc98fb84b0fa441d14d62834736db9dd1b52857004b34804761cb` |
| returned snapshots | `685a4433acca6f1402df58b373308d5c7e4ccd0d13cda7dd2ca475394999e815` |
| radial log | `11c70706f44b95cdd3c987608623e2e80f2ebc841d22609c66a7d959b83faef1` |
| axial log | `3dddf414e1dd8dcf7e264df7652235c27ff2ac320cce0278a6cce74b67bc1a1f` |
| independent check | `852969d74c0664055c23a42ca49dbc2608c05ce18ca2e95cac46bc3cdb32bb75` |
| receipt | `792fec91990e3792c04adaf7600544dded848a4b3391ae07f73d973e243f8e04` |

This stage introduced no empirical parameter, relaxation, damping,
clipping, fit, regularization, condition cutoff, mixed-unit objective, or
model correction.  No further map is authorized by this result.
