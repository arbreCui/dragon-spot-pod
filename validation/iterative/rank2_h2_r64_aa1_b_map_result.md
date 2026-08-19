# Rank-two REAL64 fourth standard AA(1) map

Date: 2026-08-18

Status: `VALID_NOT_MET`; next `AA1_DIRECTION_PASS_AA2_SKIPPED`.

Using the genuine map pairs `q -> r` and `r -> b`, the standard
unregularized full-Gram AA(1) proposal is

\[
c=0.489114497782001889\,r+
  0.510885502217998111\,b.
\]

Its three parameter-free direction ratios are
`(0.848686011945671837, 0.613945987255164471,
0.597652389054204813)`, all strictly below one — the strongest screens of
the REAL64 track.  It was independently materialized in the fixed
rank-two POD space, with 8880/8880 positive published scalar-flux values
and a passing `RETURNED/9` carrier and authority-strip audit.  AA(2) was
not used.

Exactly one bounded physical map completed without retry through
`PROPOSAL -> PROJECTED/10 -> RETURNED/10 -> CLOSED/10`.  The radial stage
completed in 21.64 s and the warm axial stage in 13.10 s, each under a
30 s hard bound.  Its independently reproduced raw defect is

\[
(R_\rho,R_L,D_L,R_a)=
(6.4223469764534968\times10^{-8},
 4.8010391379439250\times10^{-5},
 7.0343958213925362\times10^{-8}\ {\rm cm}^{-1},
 1.2924627215604308\times10^{-7}).
\]

At the unchanged `5e-7` AND gate, `Rrho` and `Ra` pass; only `RL` fails,
at about 96.0 gate multiples.  `Ra` is again the smallest modal defect of
the REAL64 track, but `RL` increased by a factor of about 17.5 relative
to the preceding direct map, although the same-coefficient affine screen
had predicted a 0.614 leakage reduction.  This is direct evidence that
the affine direction screen is not a reliable predictor of the mapped
leakage response at this amplitude; it is recorded as a local
observation, not a model conclusion.  The map is physically valid but
rank two is not converged.

No relaxation, damping, clipping, fitting, regularization, empirical
coefficient, fallback, dynamic rank, or model correction was introduced.

The following standard AA(1), using only `b-r,d-c`, gives the direction
`e = 0.460187880181553877 b + 0.539812119818446123 d` with ratios
`(0.924823979667296014, 0.544585032932459967, 0.532005871126909557)`.
All three pass the componentwise screen, so the decision is
`AA1_DIRECTION_PASS_AA2_SKIPPED` and exactly one further standard
proposal map is authorized.

The complete receipt is frozen under
`validation/artifacts/iterative-rank2-h2-r64-aa1-b-map/`.
