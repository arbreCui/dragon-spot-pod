# D4-A 650 C FLU/MCGMRE bounded diagnostics

## Current status

`CANONICAL_EDIT1_TIMEOUT_OUT25 / NO_SCIENTIFIC_RESULT / NO_SNAPSHOT`.

The earlier bounded diagnostics below established the inner-solver behavior;
the current canonical outcome and next boundary are recorded at the end of
this file.

## Earlier bounded diagnostic result

`SEVEN_MCGMRE_SOLVES_ACCEPTED / FIRST_3_PLUS_3_CYCLE_DECREASED / FLU_TIMEOUT /
NO_SCIENTIFIC_RESULT`.

The frozen state is `(fuel,cladding,sodium)=(650,620,475) C`. All bounded
runs used `OMP_NUM_THREADS=1`, unbuffered output and zero retries. The staged
procedure changed production `FLU EDIT 0` to `EDIT 2` only, and the Dragon
binary contained passive `IPRINT>=2` MCGMRE writes. Those writes read existing
iteration, active-group and residual values; they change no arithmetic.

The first 600 s run established early GMRES decrease but ended with 338 active
groups. A second run used byte-identical scientific inputs and binary, changing
only the operational wall limit from 600 to 1300 s. Its child contract was an
exact one-line replacement and its frozen contract hash is
`e00a3c9f7c474814dea7f1a045e6a0cdf53ca88f154a529ea6f10053d2a18866`.
A third byte-identical run changed only that wall limit from 1300 to 1500 s;
its exact child-contract hash is
`189d21a200b47d8cb1657dc1c51b8b56ec0fd3a208ca5923cb71d0e8afcc50b2`.
A final byte-identical diagnostic changed only the wall limit from 1500 to
1900 s. Its frozen contract hash is
`45fec89fa782607a052ea457c8378df50ce87a94e072102679c746c7d1277acf`.

## Ordered inner-solve evidence

The final 1900 s log order was

```text
OUT(0) -> MCGMRE #1 -> IN(1) -> MCGMRE #2 -> IN(2)
       -> MCGMRE #3 -> IN(3) -> MCGMRE #4 -> IN(4)
       -> MCGMRE #5 -> IN(5) -> MCGMRE #6 -> IN(6)
       -> MCGMRE #7 -> IN(7) -> partial MCGMRE #8 -> timeout
```

The first solve passed the strict ordered-prefix check. Its residual-bearing
iterations were exactly 1 through 8, with the one RHS call between iterations
1 and 2. The active-group and maximum normalized residual sequences were:

| iteration | phase | active after test | maximum residual |
|---:|---|---:|---:|
| 1 | initial | 370 | `3.20979788e+1` |
| 2 | Krylov | 370 | `7.67969818e-1` |
| 3 | Krylov | 370 | `1.27950391e-1` |
| 4 | Krylov | 338 | `2.13965862e-2` |
| 5 | Krylov | 231 | `2.77530700e-3` |
| 6 | Krylov | 84 | `3.24902968e-4` |
| 7 | Krylov | 6 | `3.37822592e-5` |
| 8 | Krylov | 0 | `2.74101989e-6` |

The final value is below the unchanged MCGMRE
`EPSI=9.99999975e-6`. Only after this `ACTIVE-AFTER=0` record did `IN(1)`
appear. This excludes a silent `MAXIT=19` return with unconverged groups.

The next six solves also reached active zero before their corresponding FLU
records:

- solve 2: iteration 7, `1.18516299e-6 < EPSI`, then `IN(2)`;
- solve 3: iteration 6, `5.49372189e-6 < EPSI`, then `IN(3)`;
- solve 4: iteration 6, `1.74732673e-6 < EPSI`, then `IN(4)`;
- solve 5: iteration 6, `9.43269722e-7 < EPSI`, then `IN(5)`;
- solve 6: iteration 5, `5.91499964e-6 < EPSI`, then `IN(6)`;
- solve 7: iteration 5, `1.84668039e-6 < EPSI`, then `IN(7)`.

For solves 5 through 7 the active sequences were respectively
`363,353,261,27,3,0`, `359,346,217,14,0`, and `353,333,177,5,0`.
Each RHS record lay strictly between iterations 1 and 2; each sequence was
nonincreasing and reached zero before its corresponding `IN`. Solve 8 contains
only its initial record (`345` active groups, residual `2.21795429e-2`), so it
is excluded.

## FLU thermal evidence

The seven accepted-inner FLU records were:

| thermal iteration | PRC | target | first unconverged group | ACCE |
|---:|---:|---:|---:|---:|
| 1 | `5.17e8` | `5.0e-7` | 1 | `1.0` |
| 2 | `4.07` | `5.0e-7` | 2 | `1.0` |
| 3 | `7.94e-1` | `5.0e-7` | 3 | `1.0` |
| 4 | `1.04e-1` | `5.0e-7` | 3 | `1.36578` |
| 5 | `5.58e-2` | `5.0e-7` | 3 | `1.08394` |
| 6 | `4.14e-2` | `5.0e-7` | 3 | `1.19025` |
| 7 | `2.08e-2` | `5.0e-7` | 21 | `1.0` |

The first three are the declared free thermal iterations; iterations 4 through
6 are the existing variationally accelerated segment. That complete declared
`3 free + 3 accelerated` cycle is finite and decreasing. The next free step,
`IN(7)`, also decreases. Across `IN(4..7)`, PRC is
`0.104 -> 0.0558 -> 0.0414 -> 0.0208`, a fivefold decrease at the printed
precision. There is no no-acceleration counterfactual, however, and neither a
fixed contraction rate nor guaranteed final convergence may be inferred.
`IN(7)` remains about `4.16e4` times the FLU target.

The existing `(3 free, 3 accelerated)` FLU cycle first calls `FLU2AC` at
thermal iteration 4. A separate source review shows that `FLU2AC` computes its
scalar by one-factor variational residual minimization; it is not a user-fitted
relaxation input. The timeout occurred just after the initial iteration of the
eighth fixed-source solve.

## Reproducibility and boundary

The retained final diagnostic artifact is
`validation/artifacts/d4a-flu650-cycle1900-20260824/`. All three manifests pass
`sha256sum -c`, and no Dragon process remained after cleanup. Principal hashes:

- diagnostic log:
  `b758d13060c7c5b4f4a557bf1a8303bcfa087ffbec362cebbdf8d9eb57d7132f`;
- bounded-runner error:
  `c4b8f383e79b42d10733159bd5e79c6252daa7ae7dce20e4585d3a89a7d8269e`;
- diagnostic-result manifest:
  `b71c33da12d50f5d1550a4cb472fd88a8c58bc66543c62847e946d03bf0025fe`.

The run returned 51 MCGFL1 integrations with 1500 s of reported integration
time. Seven MCGMRE solves were complete; the last integration belonged to the
incomplete eighth solve. It ended by the external 1900 s bound, with no Dragon abnormal terminal,
normal end, FLU terminal, `OUT(1)`, snapshot or trustworthy keff/flux result.
MCGMRE's approximately `1e-5` criterion and FLU's `5e-7` criterion remain
separate.

## Earlier EDIT 0 four-hour outcome

One unchanged canonical `EDIT 0` run was started at
`2026-08-24T19:42:05-0700`, with the declared 14400 s wall limit and zero
retries. TONE converged at iteration 4 with printed error `4.453e-6`, and FLU
began. At the contractual deadline the log contained no `FLU2DR-TERM`, deck
completion marker, normal Dragon end or snapshot archive. Because the native
supervisor did not produce its own timeout receipt, the result is strictly
`FAILED / NOT_RUN / NO_RESULT`; it is not evidence that the physical
iteration diverged or could never converge.

The host supervisor was lost before the deadline and left Dragon PID 62061
orphaned. The orphan was sent `TERM` at `23:42:17 PDT`, 12 s after the declared
deadline, exited without `KILL`, and was not retried. This recovery is recorded
explicitly rather than attributed to the missing helper. The sealed artifact is
`validation/artifacts/d4a-flu650-canonical-20260824/`; all four input, executable,
capture and result manifests pass `sha256sum -c`. Principal hashes are:

- canonical log:
  `145f9e9b18afa3f5eec8331f5dab1a09879e777905cd5cddf9f3d767a038adad`;
- orphan-recovery record:
  `64802f261dfc42cb434de7d39565e846641be29852779bbc75b04954625e27e8`;
- final result manifest:
  `a0a29cdc83fc996326fccf25aee72d0faf87a73a120c6f8bc3f69658297b5b9a`.

## Canonical EDIT 1 four-hour outcome

The prepared observable route was executed exactly once on 2026-08-25.  Its
frozen contract used `(fuel,cladding,sodium)=(650,620,475)` C, `EDIT 1`, one
OpenMP thread, all three `5e-7` criteria, a 14400 s wall limit and `RETRY=0`.
The retained artifact is
`validation/artifacts/d4a-flu650-canonical-edit1-20260825/`.

TONE converged at iteration 4 with error `4.453e-6`.  FLU then completed 25
inner solves, each with an `INTERNAL CONVERGENCE REACHED` terminal; the first
used 42 inner iterations and the remaining solves used 4--24.  From `OUT(2)`
onward, `keff` remained in `1.367861--1.367864`.  This eigenvalue stability is
not by itself full fixed-point convergence.

The smallest explicitly printed outer flux residual was `1.69e-6` at
`OUT(20)`, or 3.38 times the unchanged target.  It subsequently rose to
`1.82e-5` at `OUT(22)`.  The last completed record was `OUT(25)`, whose
eigenvalue residual was `1.32e-6 > 5e-7`.  There is no
`FLU2DR-TERM OUTER-GATE=PASS`, `INNER-TERMINAL`, normal Dragon end, deck
completion marker or snapshot receipt.

The bounded helper returned exactly:

```text
PROCESS_STATUS=TIMEOUT
SCIENTIFIC_STATUS=NO_RESULT
VALIDATION_STATUS=NOT_RUN
```

All five capture, result, executable, executed-input and frozen-repository
SHA-256 manifests pass, and no process associated with this run remains.  The
scientific classification is therefore `TIMEOUT / NOT_RUN / NO_RESULT`.
This establishes reliable inner solves and an unresolved outer full-flux
fixed-point boundary; it neither proves divergence nor proves that REAL32
precision is the cause.

## Offline audit and corrected next boundary

The retained artifact contains only the persistent tracking file and printed
scalars.  The in-memory `FLUX(:,:,2:3)` Picard input/image pair was lost at
timeout, so an exact offline REAL32/REAL64 norm comparison is impossible.
Fourteen outer flux defects were printed; none passed, the best was `1.69e-6`,
and the largest was `1.89e-5`, a spread of 11.18.  This is oscillatory evidence,
not a demonstrated constant precision floor.

The source trace instead found a definite nested-tolerance inconsistency.  The
production MCCG track supplied `EPSI=1e-5` to MCGMRE, whose convergence test is
that tolerance, while FLU required `EXTE=UNKT=THER=5e-7`.  The earlier passive
diagnostic observed accepted MCCG residuals from `9.43e-7` to `5.91e-6`.
Although the MCCG and outer norms are not identical, a linear solve permitted
to stop above the requested outer accuracy must be corrected before attributing
the result to REAL32.

The current `SpotD4Snap` builder therefore ties production MCCG
`EPSI <<solver_eps>>` to the same predeclared `solver_eps=5e-7` used by all
three FLU gates.  This introduces no new coefficient: it reuses one numerical
accuracy authority and only tightens the inner linear solve.  TONE retains
`EPS=1e-5`; the operator, material state, 3-free / 3-accelerated variational
schedule, REBA and GMRES/ACA are unchanged.  The frozen-input and canonical
default-off preflights pass; no transport was executed.

The next physical action is exactly one bounded canonical 650 C run with this
consistent tolerance chain.  Do not activate a REAL64 redesign unless that
corrected run still supplies evidence of a precision floor.  The three-snapshot
archive and rank-2/full-rank comparison remain closed until the strict terminal
is accepted.
