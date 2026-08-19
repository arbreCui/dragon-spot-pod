# Rank-two REAL64 third standard AA(1) map

Date: 2026-08-18

Status: `VALID_NOT_MET`; next `AA1_DIRECTION_FAIL_NOT_MATERIALIZED`.

Using the genuine map pairs `u -> v` and `v -> w`, the standard
unregularized full-Gram AA(1) proposal is

\[
q=0.0962047501787943737\,v+
  0.903795249821205626\,w.
\]

Its three parameter-free direction ratios are
`(0.995646497516672779, 0.855926138157315108,
0.799420439751273193)`, all strictly below one.  It was independently
materialized in the fixed rank-two POD space, with 8880/8880 positive
published scalar-flux values and a passing `RETURNED/7` carrier and
authority-strip audit.  AA(2) was not used.

Exactly one bounded physical map completed without retry through
`PROPOSAL -> PROJECTED/8 -> RETURNED/8 -> CLOSED/8`.  The radial stage
completed in 21.35 s and the warm axial stage in 13.20 s, each under a
30 s hard bound.  Its independently reproduced raw defect is

\[
(R_\rho,R_L,D_L,R_a)=
(0,
 3.2259772467709291\times10^{-6},
 4.7266439651139081\times10^{-9}\ {\rm cm}^{-1},
 1.3439421010078249\times10^{-7}).
\]

At the unchanged `5e-7` AND gate, `Rrho` and `Ra` pass; only `RL` fails,
at about 6.45 gate multiples.  Relative to the preceding direct map, `RL`
and `DL` fell by about 69.0% and `Ra` by about 12.5%; `Ra` is the smallest
modal defect of the REAL64 track.  These adjacent decreases are not a
convergence factor.  The map is physically valid but rank two is not yet
converged.

No relaxation, damping, clipping, fitting, regularization, empirical
coefficient, fallback, dynamic rank, or model correction was introduced.

The following standard AA(1), using only `w-v,r-q`, gives the direction
`s = 0.297962433494916579 w + 0.702037566505083421 r` with ratios
`(0.965935617614250286, 0.754897743550166034, 1.16885968577921284)`.
The same-coefficient maximum-`DL` ratio exceeds one, so the existing
componentwise, no-leakage-fit screen rejects this direction.  No proposal
was materialized, no successor map was started, and no standard r64 AA(2)
host exists.

The complete receipt is frozen under
`validation/artifacts/iterative-rank2-h2-r64-aa1-w-map/`.
