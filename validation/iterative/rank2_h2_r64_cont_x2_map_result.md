# Second consecutive rank-two REAL64 CONT map

Date: 2026-08-18

Status: `VALID_NOT_MET`; `AA1_DIRECTION_FAIL`.

## Three completed steps

1. The continuation lifecycle was made epoch-generic.  B2J is now the only
   increment, `CLOSED/e -> PROJECTED/(e+1)`, while B2K/B2N/B2O/B2B/B2R/B2W
   preserve that epoch.  On B2W close, transition-only authority `QFISS` is
   removed and each child is relabelled with the completed outer-state
   `RHO` before the epoch commit.  Strict Fortran compilation, the normal
   Dragon build, and `SpotCloseR64.c2m` compilation passed.
2. The frozen raw x2 pair was closed again without transport and passed the
   production B2J positive and negative gates: `CLOSED/1 -> PROJECTED/2`,
   while a private root-epoch mismatch was rejected with an empty output.
   All input hashes were unchanged.  A separate no-transport host test made
   three real ASM calls and B2K committed `ASSEMBLED/2`; its independent
   posterior passed.
3. Exactly one physical map, x3 = G_CONT(x2), was evaluated.  The radial
   stage completed in 21.73 s under a 40 s hard bound and the warm axial
   stage completed in 16.00 s under a separate 40 s bound.  There was no
   retry.  B2W admitted `RETURNED/2`, the Ganlib-only checker passed, and a
   validation copy closed as `CLOSED/2`.

The physical map used the same fixed rank-two POD package, tracks,
macrolib, three online radial fixed-source solves, frozen fission source,
warm axial equation, and direct leakage return as the preceding CONT map.
There was no relaxation, damping, clipping, fitted closure, regularization,
empirical coefficient, fallback, or model change.

## Result

The independent checker recomputed, bit for bit,

\[
(R_\rho,R_L,D_L,R_a)=
(0,
 1.0587314276061698\times10^{-5},
 1.5512341633439064\times10^{-8}\ {\rm cm}^{-1},
 1.1066465016594839\times10^{-6}).
\]

At the unchanged `5e-7` AND gate, only `Rrho` passes.  `DL` is diagnostic
only.  The map is valid, but the coupled iteration is not converged.

The radial contract reported fixed-basis marker 1, three frozen sources,
and plane balance values below `6.59e-8`.  The independent checker also
verified uniform rank two, the POD package bit for bit, a live radial
operator, 8880 positive raw radial scalar-flux values, canonical layout,
and the feedback map carrier.

## Parameter-free acceleration decision

There are now two genuinely consecutive residuals of the same finite-
precision CONT map: `x2-x1` and `x3-x2`.  Their saved defects and fixed POD
space passed bitwise checks.  Standard unregularized full-Gram AA(1) has the
unique affine direction

\[
y=0.37576785470366381\,x_2+
  0.62423214529633619\,x_3,
\]

with denominator `7.64084887424493118e-13`.  The unchanged modal,
leakage-height-L2, and same-weight maximum-DL authorization ratios are

\[
(0.89535614495056703,\ 1.1058125161297643,\
  0.56465919272136511).
\]

The second ratio is not strictly below one, so the predeclared componentwise
screen rejects AA(1).  No proposal was materialized and no physical map was
started from it.  AA(2) is not yet defined because it requires three
consecutive CONT residuals.

That minimum next action has since been completed.  The third consecutive
CONT map and its AA(1)-first decision are documented in
[rank2_h2_r64_cont_x3_map_result.md](rank2_h2_r64_cont_x3_map_result.md).

The complete local evidence is frozen under
`validation/artifacts/iterative-rank2-h2-r64-cont-x2-map/`.
