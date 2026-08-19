# Fifth rank-two REAL64 CONT map

Date: 2026-08-18

Status: `VALID_NOT_MET`; `AA1_DIRECTION_PASS_AA2_SKIPPED`.

## Three completed steps

1. Production B2J advanced the previously closed state without transport:
   `CLOSED/6 -> PROJECTED/7`.  A private archive-root epoch mismatch was
   rejected with an empty output, and all three physical input hashes were
   unchanged.
2. Exactly one physical map, `w = G_CONT(v)`, was evaluated.  The radial
   stage completed in 21.98 s under a 40 s hard bound; the warm axial stage
   completed in 14.63 s under a separate 40 s bound.  Neither stage was
   retried.  The warm parent was raw `v`, not its closed copy.
3. Production B2W admitted `RETURNED/7`; the Ganlib-only one-map checker
   passed and independently recomputed every defect bit for bit.  A
   validation copy closed as `CLOSED/7`.  The latest AA(1) direction was
   then evaluated read-only and passed all three fixed screens, so AA(2)
   was skipped by the predeclared minimum-order rule.

The map retained the fixed rank-two POD package, full Gram metric, plane
heights, normalization, tracks, axial macrolib, three fresh online radial
fixed-source solves, frozen fission source, warm axial equation, and direct
leakage return.  No relaxation, damping, clipping, fitting, regularization,
empirical coefficient, fallback, dynamic rank, or model change was used.

## Physical result

The independent checker obtained

\[
(R_\rho,R_L,D_L,R_a)=
(0,
 1.0408543268751368\times10^{-5},
 1.5250407159328461\times10^{-8}\ {\rm cm}^{-1},
 1.5351535557415451\times10^{-7}).
\]

At the unchanged `5e-7` AND gate, `Rrho` and `Ra` pass; only `RL` fails.
Relative to the preceding direct map, `RL` and `DL` decreased by about
7.83% and `Ra` by about 24.58%; `Ra` is again the smallest modal defect of
the REAL64 track.  These adjacent decreases are not a convergence factor.
`DL` remains diagnostic only.  The map is physically valid but the coupled
iteration is not converged.

The radial contract reported fixed-basis marker 1, three frozen sources,
and plane balance values below `6.59e-8`.  The independent checker also
verified the POD package bit for bit, a live radial operator, 8880 positive
raw radial scalar-flux values, canonical layout, and the feedback map
carrier.

## AA(1)-first decision

The latest genuine same-map residuals are `v-u` and `w-v`.  Standard
unregularized full-Gram AA(1) gives the unique unclipped affine direction

\[
q=0.0962047501787943737\,v+
  0.903795249821205626\,w,
\]

with denominator `9.82633432780853462e-15`.  Its modal,
leakage-height-L2, and same-weight maximum-DL direction ratios are

\[
(0.995646497516672779,
 0.855926138157315108,
 0.799420439751273193).
\]

All three are strictly below one and the geometry is convex.  Therefore
the decision is `AA1_DIRECTION_PASS_AA2_SKIPPED`.  This turn performed an
offline, read-only authorization only: no AA proposal was materialized and
no map was started from it.

The minimum next action is to materialize this one standard complete-state
AA(1) proposal, independently verify its fixed-space provenance and
positivity, and only then authorize one bounded physical map.

The complete local evidence is frozen under
`validation/artifacts/iterative-rank2-h2-r64-cont-v-map/`.
