# Rank-two REAL64 next standard AA(1) map

Date: 2026-08-18

Status: `VALID_NOT_MET`.

Using the genuine map pairs `x3 -> x4` and `y -> z`, the standard
unregularized full-Gram AA(1) proposal is

\[
t=0.252802215112331696\,x_4+
  0.747197784887668304\,z.
\]

Its three parameter-free direction ratios are
`(0.930191352745366906, 0.929883871343836987,
0.806313075857981731)`, all strictly below one.  It was independently
materialized in the fixed rank-two POD space, with 8880/8880 positive
published scalar-flux values.  AA(2) was not used.

Exactly one bounded physical map completed without retry through
`PROPOSAL -> PROJECTED/5 -> RETURNED/5 -> CLOSED/5`.  Its independently
reproduced raw defect is

\[
(R_\rho,R_L,D_L,R_a)=
(6.4223469764534968\times10^{-8},
 2.4829538267522743\times10^{-6},
 3.6379788070917130\times10^{-9}\ {\rm cm}^{-1},
 2.7689296270786060\times10^{-7}).
\]

At the unchanged `5e-7` AND gate, `Rrho` and `Ra` pass; only `RL` fails.
The map is physically valid and improves both `RL` and `Ra` over the
previous map, but rank two is not yet converged.

No relaxation, damping, clipping, fitting, regularization, empirical
coefficient, fallback, dynamic rank, or model correction was introduced.
The complete receipt is frozen under
`validation/artifacts/iterative-rank2-h2-r64-aa1-z-map/`.
