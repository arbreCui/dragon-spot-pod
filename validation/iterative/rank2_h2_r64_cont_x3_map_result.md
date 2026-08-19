# Third consecutive rank-two REAL64 CONT map

Date: 2026-08-18

Status: `VALID_NOT_MET`; `AA1_DIRECTION_PASS_AA2_SKIPPED`.

## Three completed steps

1. Production B2J advanced the previously closed state without transport:
   `CLOSED/2 -> PROJECTED/3`.  A private archive-root epoch mismatch was
   rejected with an empty output, and all three physical input hashes were
   unchanged.
2. Exactly one physical map, `x4 = G_CONT(x3)`, was evaluated.  The radial
   stage completed in 22.12 s under a 40 s hard bound; the warm axial stage
   completed in 15.24 s under a separate 40 s bound.  Neither stage was
   retried.  The warm parent was raw x3, not its closed copy.
3. Production B2W admitted `RETURNED/3`; the Ganlib-only one-map checker
   passed and independently recomputed every defect bit for bit.  A
   validation copy closed as `CLOSED/3`.  The latest AA(1) direction was
   then evaluated read-only.  Because it passed all three fixed screens,
   AA(2) was skipped by the predeclared minimum-order rule.

The map retained the fixed rank-two POD package, full Gram metric, plane
heights, normalization, tracks, axial macrolib, three fresh online radial
fixed-source solves, frozen fission source, warm axial equation, and direct
leakage return.  No relaxation, damping, clipping, fitting, regularization,
empirical coefficient, fallback, dynamic rank, or model change was used.

## Physical result

The independent checker obtained

\[
(R_\rho,R_L,D_L,R_a)=
(6.4223469764534968\times10^{-8},
 2.8206357713028515\times10^{-6},
 4.1327439248561859\times10^{-9}\ {\rm cm}^{-1},
 7.4996305372338354\times10^{-7}).
\]

At the unchanged `5e-7` AND gate, only `Rrho` passes.  `DL` remains
diagnostic only.  The map is physically valid but the coupled iteration is
not converged.

The radial contract reported fixed-basis marker 1, three frozen sources,
and plane balance values below `6.59e-8`.  The independent checker also
verified uniform rank two, the POD package bit for bit, a live radial
operator, 8880 positive raw radial scalar-flux values, canonical layout,
and the feedback map carrier.

## AA(1)-first decision

The latest genuine same-map residuals are `x3-x2` and `x4-x3`.  Standard
unregularized full-Gram AA(1) gives the unique unclipped affine direction

\[
y=0.27113387220513907\,x_3+
  0.72886612779486093\,x_4,
\]

with denominator `6.42614306605438749e-13`.  Its modal,
leakage-height-L2, and same-weight maximum-DL direction ratios are

\[
(0.90050274164755406,
 0.97466155455276116,
 0.95749961400361316).
\]

All three are strictly below one.  Therefore the decision is
`AA1_DIRECTION_PASS_AA2_SKIPPED`.  This turn performed an offline,
read-only authorization only: no AA proposal was materialized and no map
was started from it.

The minimum next action is to materialize this one standard complete-state
AA(1) proposal, independently verify its fixed-space provenance and
positivity, and only then authorize one bounded physical map.

The complete local evidence is frozen under
`validation/artifacts/iterative-rank2-h2-r64-cont-x3-map/`.
