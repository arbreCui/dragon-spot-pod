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

## Clean-source rebuild

The complete committed tree at `cf469c8` was exported with `git archive` to
`/private/tmp/spot-cf469c8-clean.xZIfZa`. The repository tracks no `.o`, `.a`
or `.mod` files. All solver/dependency libraries were built there from
source with `make -C src -j2`, followed by the lifecycle host tools and
`sh validation/run_fast.sh`. All three commands exited zero; the final
marker was `SPOT ACTIVE FAST PASS`, including the new angular-moment tests.
Logs are retained in
`validation/artifacts/d4a-scattering-clean-build-20260923`.
The working-tree and release canonical executables retain their old hash
shown above. No transport was launched and no binary was promoted.
This proves source-build/test reproducibility, not a validated replacement
runtime, a coupled fixed point, or CE accuracy.

## Approved 90-second probe: solver convergence, export failure (2026-09-24)

The user approved one corrected **3-cell** axial probe, capped at 90 seconds,
with no retry, radial solve or feedback. It used exactly the previous candidate
binary and frozen map-9 inputs. Only the time budget and log verbosity changed
(`FLU EDIT -3` to `1`, unbuffered output). Evidence is in
`validation/artifacts/d4a-scattering-fix-probe90-20260924`.

The solver reached its unchanged terminal gates in 14 outer iterations:

| Logged quantity | Value | Existing threshold |
|---|---:|---:|
| EEXT | 7.69394451e-10 | 1.99999999e-6 |
| EUNK | 1.68566906e-6 | 1.99999999e-6 |
| EINR | 1.68566906e-6 | 1.99999999e-6 |

The logged eigenvalue is `1.2718148126934201`; it is a frozen-radial axial
diagnostic, **not a new coupled fixed point or an accepted CE comparison**.
SPOGBAL completed (global balance diagnostic `3.17083e-7`, no nonpositive
scalar-flux entries). SPOSTATE also completed (`PERP=2.41155e-12`,
`GERR=7.34990e-8`). These do not substitute for all final validation gates.

The process then failed after 35.99 seconds at the second `SYS_OUT := SYS`:
`XSM_FILE *SYS_OUT* ALREADY EXISTS`. The diagnostic deck had added pre-FLU
assembly exports but retained the post-FLU copies. This is our probe-deck
export bug, not a solver-convergence failure. `AX_OUT := AX` was never reached,
so there is **no persisted axial state**. The original run status remains
`INCOMPLETE`; neither its deck, log nor status is rewritten. No retry occurred.

All protected binaries, libraries, sources and frozen inputs retained their
identities. The saved SYSTEM and TRACK hashes exactly match the 30-second
probe, whose physical XS and unchanged POD/radial records were independently
checked. No probe process remains. The separate `probe_export_fixed.x2m`
removes only the two duplicate post-FLU assembly exports. It was not run under
that authorization; the subsequently approved fresh run is recorded below.

## Export-fixed run and independent saved-state check (2026-09-24)

The user separately authorized one fresh run with the same 90-second cap.
`validation/artifacts/d4a-scattering-export-fixed-20260924` contains the complete
result. The driver verified that the only executable deck differences from the
previous run were removal of the two duplicate exports. No solver, input,
physics, rank, grid, threshold or coefficient changed. No automatic retry,
radial transport, online feedback or CE run occurred.

The run exited zero in **37.4604 seconds**, exported `axial.xsm`, and reached the
final deck marker. Its two terminal solver records are exactly the same text as
the previous run: 14 outer iterations, `k64=1.2718148126934201`, and all three
inner/outer solver gates passed at the existing `2e-6` thresholds.

Independent GANLIB-only readback, with no SPOT solver call, passed:

- The existing mesh checker read the saved SYSTEM/TRACK/AXIAL: 3 cells, correct
  material ordering and 150 cm total height; all 13 checked group records match
  the previously audited corrected assembly wordwise. SYSTEM and TRACK also
  match its complete file hashes, preserving the physical XS/POD/radial audit.
- `SPOT-KEFF64`, `SPOT-X-KEFF`, their REAL32 mirror and reciprocal rho agree.
  Every FLUX/FLUX64 value is finite and the mirrors agree bitwise.
- All **146520 active scalar flux entries are positive**, minimum
  `8.3861402596134438e-18`. Signed angular/current entries were not incorrectly
  subjected to scalar-flux positivity.
- Reintegrating volume × scalar flux × nu-fission XS reproduces the saved
  normalization **bitwise**: `1.2718148125469508`.
  Layer nu-fission fractions, at the production log's printed precision, are
  `0.259838086 / 0.484022293 / 0.256139621`, matching the saved-state readback.
- Input, output, canonical binary, library and source hashes are unchanged
  after checks; the complete `result.sha256` manifest verifies. No probe process
  remains. The old incomplete artifacts were neither altered nor promoted.

Classification: **SAVED_AXIAL_VERIFIED_NOT_COUPLED_FIXED_POINT**. This closes the
short corrected-axial persistence/readback test. The radial response is still
the frozen map-9 input, not a new response to this axial state. This therefore
does not establish a repaired online Picard fixed point, final power accuracy,
mesh convergence or a successful CE comparison.

## Old chain and shortest continuation

The old controller exited normally after map 11 reported `VALID_MET`:
`Rrho=2.1368370406449344e-9`, `Rleak=2.3298773338411653e-7`,
`Ra=2.7295793162486826e-7`, all below its unchanged `5e-7` gate. Its old
scattering implementation still disqualifies it as repaired-method evidence.
The former controller/supervisor/Dragon PIDs 17661/74248/74249 are gone;
do not issue signals using these stale identities. Old-chain acceptance stays
paused, and all sealed old receipts remain untouched.

The short axial test is complete; do not repeat it merely to obtain another
receipt. The raw TYPE-K guesses correctly failed B2I admission. The subsequently
authorized single three-plane TYPE-S bootstrap completed on 2026-09-24 at
04:24:33 Asia/Shanghai, in 8087.3168 seconds including B2I/B2J (10800-second cap,
no retry). All three radial plane terminals passed; B2I sealed `CLOSED/0`, and
B2J checked `PROJECTED/1` with no transport. Independent result/input manifest
checks passed and the inputs are unchanged; its monitor paused after review.
See [bootstrap preparation and result](d4a_scattering_bootstrap_preparation.md).
This establishes a new initial state, **not a repaired coupled fixed point**.
The separately budgeted repaired map 1 subsequently completed and passed
independent replay as `CLOSED/1 / VALID_NOT_MET`; map 2 is now running under a
separate single-map budget. See the [map-1 result and continuation](d4a_scattering_picard_map1_result.md).
The 6-cell mesh experiment remains unapproved. Do not
relabel old CLOSED states, promote this isolated axial state to a coupled
fixed point, or rerun the completed CE reference.
