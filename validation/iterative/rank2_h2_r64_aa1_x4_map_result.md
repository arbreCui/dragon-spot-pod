# Rank-two REAL64 standard AA(1) map from x4

Date: 2026-08-18

Status: `VALID_NOT_MET`.

The standard unregularized full-Gram AA(1) proposal formed from `x3-x2`
and `x4-x3` is

\[
y=0.27113387220513907\,x_3+
  0.72886612779486093\,x_4.
\]

It was independently materialized and checked in the fixed rank-two POD
space.  The checker reproduced the full-Gram calculation and plane-height
weighting, verified all 8880 published radial scalar-flux values were
strictly positive, and found direction ratios
`(0.90050274164755406, 0.97466155455276116,
0.95749961400361316)`.

Exactly one bounded physical map completed without retry through
`PROPOSAL -> PROJECTED/4 -> RETURNED/4 -> CLOSED/4`.  Production admission
and the independent one-map checker passed.  The raw defect is

\[
(R_\rho,R_L,D_L,R_a)=
(0,
 2.9199537002606746\times10^{-6},
 4.2782630771398544\times10^{-9}\ {\rm cm}^{-1},
 5.2477432212649936\times10^{-7}).
\]

At the unchanged `5e-7` AND gate, only `Rrho` passes.  `DL` remains
diagnostic only.  This is a physically valid map, but it is not a converged
rank-two fixed point.

No relaxation, damping, clipping, fitting, regularization, empirical
coefficient, fallback, dynamic rank, or model correction was introduced.
The full receipt is frozen under
`validation/artifacts/iterative-rank2-h2-r64-aa1-x4-map/`.
