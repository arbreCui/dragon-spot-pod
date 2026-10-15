# One private temperature-interpolation comparison — material result available

## Latest result: independently reviewed, not production accepted

After a new explicit approval, the corrected-basename attempt ran in
`validation/artifacts/d4a-linear-temperature-namefix-tone650-run-20260929/`.
It started at 16:33:51.765406 Beijing time on 2026-09-29 and completed normally
after 341.408388 seconds, within the shared 900-second deadline 16:48:51.765406.
The unmodified control reproduces the repaired Dragon **whole-file hash exactly**.
The private candidate changes only `LIBDRA NOTX=3` to `NOTX=1`; no production
source, runtime, archive or library was replaced. The earlier failed attempt
remains unchanged. There was no retry or transport/CE solve.

TONE converged at iteration 4 with printed error 4.400e-6 (original limit 1e-5).
All 59 isotope identities, densities, temperatures and groups match saved D4.
The two Fe56 P0 negative counts changed 206→0 and 637→0. Across all six mixtures,
the macroscopic P0 negative count changed 6054→0. Signed P1 values were retained;
there was no clipping or scalar renormalization. The strict Fe56 check passed.

| Quantity | Cubic material | Linear material |
|---|---:|---:|
| Macro P0 minimum | −3.20529762e-6 | 0 |
| Max P0 column-sum/scalar absolute gap | 1.000590002e-5 | 1.15395e-5 |
| Location of max P0 gap | mix4/G240 | mix4/G240 |
| Max P1 column-sum/scalar absolute gap | 1.188910200e-7 | 8.539702e-8 |

For the new worst P0 entry the scalar is 65.0957336 and the matrix sum is
65.0957451395, relative difference about 1.77e-7. This is about 1.5 REAL32 ULPs
of that scalar, making floating-point accumulation a sensible next diagnostic,
**not proof of its cause or a new acceptance tolerance**. The actual-temperature
interpolation accuracy is also unqualified; the offline holdout warning below
still applies. This result therefore remains a material diagnostic candidate,
not a production interpolation change, a new eigenvalue or a CE accuracy pass.

Independent review completed at 16:39:50, before the shared deadline, checking
129 protected-file entries before/after, separate sparse-index reconstruction,
original TONE criteria, material identity and unchanged inputs. All run/review
manifests verify and the original supervisor/worker/Dragon/watchdogs have exited.
Review: `validation/artifacts/d4a-linear-temperature-namefix-tone650-review-20260929/review.json`.
Run manifest SHA-256: `6dbcf7a175ef03f07f73621c1c194eff8d1cf0642f2d9edbdb88f943348e12cf`.
Review manifest SHA-256: `51cb02a67359b71ab869ac2aae7856c7d1362b4ed3cd20f12ed8b3f86f500efa`.
The original controller receipt is preserved as `COMPLETE_PENDING_INDEPENDENT_REVIEW`;
the review verdict is separate. All prior approval/status statements below are historical.

### Saved-data roundoff follow-up (no additional native run)

The maximum P0 difference was recomputed after recovering the stored REAL32
values, rather than treating the printed decimals as exact binary64 data.
It is exactly `3087/268435456`, or 1.14999711513519e-5, at mix4/G240; its
relative value is 1.7666244e-7, or 1.50732421875 scalar ULPs. The cubic case
has 1.3154296875 ULPs at its worst column. Thus decimal export is not the cause.

Exact rational nearest-rounding intervals do not overlap for either worst
column. This **rules out only one final independent REAL32 rounding** of an
otherwise exactly conserved sum, not earlier accumulated arithmetic errors.
Neither fixed ascending nor descending REAL32 summation of the saved column
matches its saved scalar. These checks do not add a physical tolerance.

`LIBDEN.f:368` and `:371` accumulate scalar and matrix data separately in REAL.
The worst mixture is nine-isotope MOX fuel and contains no Fe56. The executed
material deck exported only Fe56 microscopic arrays, then deleted the complete
MICROLIB; the new fuel microscopic inputs needed for exact density-weighted
replay are not saved. Historical CLOSED/9 microdata cannot stand in for the
new linear-interpolation self-consistent state. The cause is therefore not
fully proved, and there is no additional production acceptance claim.

Six short tests pass. Evidence:
`validation/artifacts/d4a-linear-material-roundoff-audit-20260929/analysis.json`.
Do not rerun the same material solely to chase this approximately 1e-7 relative
diagnostic. Prioritize an independent actual-temperature interpolation reference;
any future authorized material comparison should also preserve the full
MICROLIB so this mixing check can be completed without a separate replay run.

## Execution status, 2026-09-29

The user approved the proposed 900-second attempt. It started at 16:24:31.087709
Beijing time and stopped after 0.632997 seconds, `FAILED_NO_RETRY`, at the
unmodified-control full-file hash check. The private candidate was not compiled
and the material directory was not created. No material or transport engine ran.
The original attempt is immutable; this is not authorization for a retry.

Independent read-only inspection found all 11 section descriptions and all
file-backed code/data payloads bitwise identical. Before the code signature,
differences are confined to the UUID, LINKEDIT file size and code-signature
size. CodeDirectory identifiers are `Dragon_control` versus the original
`Dragon_scattering_probe`; only page 0 of 2218 signature page hashes differs.
The entire-file hash requirement was incompatible with the changed output
basename. This was a preparation error, not a physics/data failure.

For a **new separately authorized attempt**, retain the original control output
basename `Dragon_scattering_probe` in a new private directory. Keep the exact
full-file hash requirement; do not patch signatures/headers or relax the check.
This basename correction has not been relinked or executed. No new result is
claimed. Native candidate compilation, one material state and postchecks still
require a new single 900-second budget, without retries or transport/CE.

The corrected, syntax-checked preparation is
`validation/artifacts/d4a-linear-temperature-namefix-prepared-20260929/`.
It contains only the driver, private one-line LIBDRA candidate and their hashes.
Relative to the failed driver, executable behavior changes only in the two
control-basename references; the exact hash guard and all time/physics checks
remain unchanged. No build, attempt lock or material output exists there.
After a new explicit approval, copy the two prepared files into a fresh run
directory and execute once there; do not execute in the prepared or failed
directory. This preparation is not a repeat of the failed computation.

Failure evidence: `validation/artifacts/d4a-linear-temperature-tone650-run-20260929/`,
result manifest SHA-256 `065d97e991369d713d385e52967e2acff1decbc84270e3603258e9115e3ec667`.
Independent inspection: `validation/artifacts/d4a-linear-temperature-tone650-review-20260929/review.json`;
84 frozen/source files checked before and after, review completed at 16:26:59,
before the original shared deadline 16:39:31. No existing runtime, source or
nuclear library was modified. The inspection accounts for the signature blob's
zero alignment padding; it does not reinterpret the failed run as successful.

Purpose: test whether the existing first-order sqrt(T) interpolation removes
the reproduced P0 undershoot without corrupting the material data. This is a
numerical interpolation experiment, not a calibrated correction or production
acceptance. Nonnegativity alone does not establish interpolation accuracy.

**Offline accuracy warning (2026-09-29):** a leave-one-interior-temperature-out
check of the existing Fe56 nodes is complete. For the thermal incident columns
G282–370, unweighted matrix relative L1 errors are:

| Held-out temperature K | Linear sqrt(T) | Cubic sqrt(T) |
|---:|---:|---:|
| 550 | 3.90134% | 0.721994% |
| 900 | 2.11268% | 0.419399% |
| 1200 | 2.33948% | 0.664746% |

Linear interpolation has zero negative entries in these checks; cubic has
1009/1210/793 respectively. Thus linear positivity does not establish acceptable
accuracy. Held-out intervals are wider than the actual table intervals, so
these are **not error estimates or bounds at 748.15/893.15 K**, nor estimates of
k error. No tolerance is fitted from these numbers. The proposed native run
remains a **diagnostic material comparison**, not a production-fix acceptance.
An independent actual-temperature reference is still needed before adopting
an interpolation change as a validated physics-data solution.

Saved evidence: `validation/artifacts/d4a-fe56-temperature-holdout-20260929/analysis.json`
(SHA-256 `47b7383cca944df9c76c6dbbd5366332dda7d8940bc0b04d5381bebb15141eba`).
This used saved infinite-dilution Fe56 data only, with no native solve or writes
to existing inputs, source or libraries.

## Smallest change

Apply `libdra_linear_temperature_candidate.patch` only to a private copy of
`src/LIBDRA.f`: `NOTX=3` becomes `NOTX=1`. Keep `LIBLEX`, dilution interpolation,
APOL, angular order, composition, density, temperatures and TONE criteria intact.
The same weights already feed TOTAL, NWT, fission, spectra, scalar scattering,
every scattering moment and extra reaction edits. This changes temperature
interpolation for **all nuclides read by LIBDRA**, not just Fe56. No P0-only
clipping, rescaling, mixture special case or fitted parameter is allowed.

The existing LIBLEX routine supports order 1. Positive convex weights apply to
points inside the temperature bracket, not arbitrary extrapolation; check the
actual temperature tables before claiming positivity preservation generally.
Exact-node lookup remains the existing identity branch. A one-node table is
constant under the existing routine, not a new fitted extrapolation rule.

## Reuse, do not rebuild the project or nuclear library

- Reuse the already verified Ganlib candidate binary from
  `validation/artifacts/d4a-fe56-ganlib-tone650-run-20260929/import/DLIB_370_bin`
  (SHA-256 `54a86e4a7b9dacfce6c94bf14c1ba506b6a8acaa6663b363c98ba5266e372bbe`).
  No NJOY rerun, import conversion or production library replacement.
- Reuse the exact material deck and procedure from
  `validation/artifacts/d4a-fe56-tone650-prepared-20260929/` and their helpers.
  One state only: fuel/cladding/sodium 650/620/475 C; original EPS=1e-5, MXIT=20.
- Private link inputs are the four repaired objects SPOASM/FLU/FLU2DR/FLU2DR64
  from `validation/artifacts/d4a-scattering-fix-probe-20260923/`, DRAGON.o and
  the same four library archives used there. Their current base-library hashes
  match the original probe input identity. Do not accidentally use the older
  canonical Dragon alone, or replace the shared archives.
- Before material execution, relink an unmodified control from these saved
  objects with the original link flags and output basename `Dragon_scattering_probe`
  (inside the new private directory), and require its hash to match the
  repaired runtime `873ad14272a2f0765d95e6de067194a01708ccf9aa88d58cd782049e6d331fef`.
  If this fails, stop; do not silently accept an unmatched runtime.
- Compile only the private LIBDRA copy using the recorded Fortran flags; link
  its object ahead of the unchanged libDragon archive and retain the four
  repaired objects. Source difference must be exactly the declared one line.
  The private output must not be promoted to any existing runtime directory.

## One bounded material test, only after separate approval

Proposed **900 seconds total**, including the private control/candidate build,
one material run and checks; reserve 120 seconds for postchecks. No retry,
second temperature, ASM/FLU, snapshot, Picard or CE. Last same-state material
attempt took 335.716 seconds including its import/reopen; this supports the
budget estimate but is not a runtime guarantee. Use the existing bounded
process-group runner and preserve failure/timeout evidence.

Reuse the strict material checker from the previous attempt: exactly one TONE
terminal, original tolerance, no forbidden modules, identical 59 isotope
identities/densities/temperatures, Fe56 P0 nonnegative, unchanged inputs. Report
the full macro P0 negative count/minimum, scalar/matrix consistency for P0/P1/P2,
and changes versus the frozen cubic material output. No invented tolerance may
turn the previously observed mix4/G240 discrepancy into a pass. Signed P1/P2
must not be clipped. A passed Fe56 guard is not complete material acceptance.

Use a new run directory. Existing failed attempts, receipts, CLOSED/9 and CE
remain immutable. The result must be described as an interpolation candidate
material comparison, never as a new k, a validated SPOD replacement or an IRENA
full-core result. Only after data and interpolation accuracy are justified can
a separately budgeted transport comparison be considered.

Historical preparation performed: source/one-line diff check and saved link-input
identity checks only. The subsequent authorized attempt linked only the unmodified
control and stopped at its hash check, as recorded at the top. No candidate
compilation, native-engine invocation, material run or runtime replacement occurred.
