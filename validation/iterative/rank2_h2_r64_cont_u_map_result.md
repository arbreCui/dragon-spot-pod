# Fourth rank-two REAL64 CONT map

Date: 2026-08-18

Status: `VALID_NOT_MET`; `AA1_DIRECTION_FAIL_NOT_MATERIALIZED`.

## Three completed steps

1. Production B2J advanced the previously closed state without transport:
   `CLOSED/5 -> PROJECTED/6`.  A private archive-root epoch mismatch was
   rejected with an empty output, and all three physical input hashes were
   unchanged.
2. Exactly one physical map, `v = G_CONT(u)`, was evaluated.  The radial
   stage completed in 22.21 s under a 40 s hard bound; the warm axial stage
   completed in 14.44 s under a separate 40 s bound.  Neither stage was
   retried.  The warm parent was raw `u`, not its closed copy.
3. Production B2W admitted `RETURNED/6`; the Ganlib-only one-map checker
   passed and independently recomputed every defect bit for bit.  A
   validation copy closed as `CLOSED/6`.  The latest AA(1) direction was
   then evaluated read-only and rejected by its two leakage screens.

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
 1.1292474004069342\times10^{-5},
 1.6545527614653111\times10^{-8}\ {\rm cm}^{-1},
 2.0355057158034171\times10^{-7}).
\]

At the unchanged `5e-7` AND gate, `Rrho` and `Ra` pass; only `RL` fails.
`Ra` is the smallest modal defect of the REAL64 track so far, but `RL`
rebounded by a factor of about 4.55 relative to the preceding AA(1) map.
The unique `DL` hotspot moved from snapshot 3, group 370 to snapshot 3,
group 164 and reversed sign; the leakage update geometry is obtuse
(height-L2 cosine `-0.175249757722598432`).  This repeats the known local
leakage oscillation of the direct map and is not a divergence result.
`DL` remains diagnostic only.  The map is physically valid but the coupled
iteration is not converged.

The radial contract reported fixed-basis marker 1, three frozen sources,
and plane balance values below `4.0e-8`.  The independent checker also
verified the POD package bit for bit, a live radial operator, 8880 positive
raw radial scalar-flux values, canonical layout, and the feedback map
carrier.

## AA(1)-first decision

The latest genuine same-map residuals are `u-qt` and `v-u`.  Because the
first pair is a proposal-to-returned map, the audit extends the r64 checker
with the carrier-exact mode `--proposal-x4-directions`, patterned bit for
bit on the existing `--proposal-v-directions` host.  Standard unregularized
full-Gram AA(1) gives the unique unclipped affine direction

\[
w=-0.0685700633997792242\,u+
   1.06857006339977922\,v,
\]

with denominator `1.37639133397456289e-14`.  Its modal,
leakage-height-L2, and same-weight maximum-DL direction ratios are

\[
(0.998240212791472126,
 1.07969068838006654,
 1.07490239115437625).
\]

The modal ratio passes, but both leakage ratios exceed one and the
geometry is extrapolated.  Therefore the decision is
`AA1_DIRECTION_FAIL_NOT_MATERIALIZED`: no proposal was materialized and no
map may be run from this direction.  No standard r64 AA(2) host exists, so
AA(2) was not evaluated.  The parameter-free fallback is one further
direct CONT map from `CLOSED/6`.

The complete local evidence is frozen under
`validation/artifacts/iterative-rank2-h2-r64-cont-u-map/`.
