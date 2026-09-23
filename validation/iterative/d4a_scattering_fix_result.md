# D4-A scattering repair — 2026-09-23

Status: source repair and short regressions pass; production convergence
and accuracy remain unverified. The old runtime is not a validation of the
declared SCAT3 method. No sealed evidence was rewritten.

## What was wrong

1. SPOASM allocated three radial scattering columns from the axial macrolib
   order, but the radial APOL-P0 record supplied only one. It copied the
   uninitialized remainder into the axial system.
2. FLU read TRACK fields 9/10 (spatial element/scheme) instead of 15/16
   (angular/scattering orders), omitting the higher cross-group moments.
3. Correcting that field mapping alone would have activated a second
   `(2*l+1)` factor in the generic source assembly. SPOT's kernel already
   applies `(2*l+1)/2` when reconstructing the angular source.

The saved map-8/map-9 evidence is in
`validation/artifacts/d4a-scattering-audit-20260923`. All 370 radial groups
have one 7-value P0 column, while the assembled axial records have three
19-value columns. Their P1 columns are zero; all 6660 corresponding
positive-material SIGW01 values are nonzero. P2 within-group diagonals are
zero in both, which does not excuse uninitialized reads or establish that
all P2 intergroup entries vanish. Both source manifests verify unchanged.

## Minimal repair and physical scope

For explicit axial anisotropy, use the existing macrolib NTOT0 and SIGW
moments, matching normal ASM's disabling of transport correction when
explicit anisotropy is used. The scalar axial path retains its original
transport-corrected radial coefficients. Unsupported anisotropic P0_TOTAL
(`NW>0`) is rejected; the audited D4 macrolib has `NW=0`.

Do not change the radial data or its balance-derived operator:

`D_r = Q_frozen/phi - (T_radial - s0_radial) - L`.

`SPOT-S0-PHYS` means before the axial-leakage subtraction, not before APOL.
The common APOL subtraction cancels in the real-number P0 removal identity;
the implementation preserves the actual stored values and rounding rather
than recomputing them from a different representation.

SPOT's source convention is

`q_l = sum(g' != g) Sigma_s,l(g' -> g) * phi_l(g')`,

followed once by `Q(mu) = sum_l (2*l+1)/2 * P_l(mu) * q_l` in the kernel.
Only SPOT's generic source branch changes; other doors retain their existing
convention. No empirical parameter, new closure, damping, clipping or
tolerance relaxation is introduced.

## Checks completed

- SPOASM synthetic assembly: nonzero P1, negative P2, differing physical and
  APOL totals, positive/negative imposed leakage, pre-subtracted and
  unsubtracted radial records; eight invalid-input cases rejected.
- Real FLU2DR/64 source routines on two groups: eight SPOT scalar/vector,
  downscatter/thermal cases; four non-SPOT cases retain their former factor.
  Sources compare exactly using binary-fraction fixtures. These tests stub
  normalization and the final transport call, not source assembly.
- Actual SPOT1P/64 manufactured angular solutions, reflective and periodic:
  maximum REAL32 moment error `2.1455e-9`; REAL64 errors `4.4409e-16` and
  `2.8866e-15`. Nonzero P1 is exercised with periodic boundaries; P2 and its
  negative scattering coefficient are exercised in both. Test bounds derive
  from machine precision and are not model coefficients.
- Full `sh validation/run_fast.sh` passes, including the new source and
  manufactured tests. The final log is in the isolated probe artifact.
- Independent source review found no remaining P1/P2 within this repair's
  scope. This is not a claim that all SPOT physics is validated.

## Real D4 assembly, bounded solve incomplete

`validation/artifacts/d4a-scattering-fix-probe-20260923` contains a separate
candidate linked from the four changed source objects. Its SHA-256 is
`873ad14272a2f0765d95e6de067194a01708ccf9aa88d58cd782049e6d331fef`.
The canonical and release executables remain
`2908cf383be163cb0534847fe7115d42c9deed97684c28abdd9c29f24c6722db`.
Libraries, source inputs and frozen map-9 inputs were unchanged.

The one 3-cell, rank-2, fixed-radial solve stopped at its 30-second cap
(30.12 s including cleanup). It has **no accepted k or flux** and was not
retried. No radial solve, feedback, new CE, or 6/12-cell solve was started.

Assembly outputs saved before FLU were independently read and checked:

- 370 groups of TXSC and all three S0XSC columns match their physical
  macrolib records bitwise; 1480 void entries are positive zero.
- Eleven POD/radial records per group, including RADIAL-OP64, retain all
  4070 reference records bitwise. Basis and radial closure were not changed.
- Macro NW is zero; input identities verify before and after the read.

These are structural facts, not evidence that the repaired D4 solve
converged or that the old CE discrepancy is explained.

## Next decision and shortest continuation

The old map-10 supervisor could not be terminated from the sandbox. The
controller subsequently completed old map 10 (NOT_MET) and started old
map 11; none is repaired-method evidence. PID 54771 is now gone and must
not be used. The last verified map-11 supervisor/Dragon PIDs were
74248/74249 under controller 17661; always recheck identity before any
operation. The user has an updated stop request. Old-chain automatic
acceptance is paused. Confirm stop status before touching the canonical
binary or active scripts.

A single new 90-second corrected **3-cell** axial probe has been requested,
not approved. It is distinct from the earlier unapproved 6-cell mesh probe;
neither may be launched without approval. Keep the existing snapshots,
macrolib and fixed POD basis: this defect does not justify recomputing
unchanged physical snapshots. After corrected axial validation, establish
an explicit new coupled lineage/runtime; do not silently relabel old
CLOSED states as repaired physics or rerun the completed CE reference.
