# D4-A bounded three-snapshot attempt

## Result

`NO_RESULT_TIMEOUT_IN_STATE1_FLU`.

The frozen 650/750/850 C three-snapshot campaign was executed once with
`OMP_NUM_THREADS=1`, a fixed 7200 s process bound and `RETRY=0`.  The first
650 C state passed the unchanged TONE terminal at iteration 4 with error
`4.453e-6 < 1.0e-5`; TONE used 319 s.  Radial assembly then completed in
25 s and the run entered the unchanged `FLU TYPE K` solve with
`solver_eps=5.0e-7`.

The first FLU solve produced no strict `FLU2DR` terminal before the 7200 s
wall bound.  The bounded runner terminated the process group and returned

```text
RAW-MOC-CAPTURE PROCESS FAIL: timeout after 7200 seconds; no scientific result
```

No `D4A-SNAPSHOT-COMPLETE` marker was executed, no state-2 or state-3 solve
started, and no XSM archive, build receipt or admission receipt was
published.  A post-run process census found no remaining SPOT Dragon process.
This is therefore neither a converged result nor evidence that the discrete
FLU problem mathematically diverges.  It establishes only that the first
strict full-rank radial solve did not terminate inside this declared short-run
budget.

## Reproducibility

The retained local diagnostic artifact is
`validation/artifacts/d4a-three-snapshots-a770aa2-20260824/`.  Its executed
input manifest and the repository's frozen input manifest both pass
`sha256sum -c` after the run.  Relevant SHA-256 values are:

- partial Dragon log:
  `7ed585b21dea2bb7551b07c85e1a419995007dc7fe8dce9e7a45e95266485689`;
- bounded-runner error:
  `2750969cbddc3adee4005ca5ee79a68a2eedd319f22dc4bd6afe3a61b09cefd8`;
- run contract:
  `c09d34dbd691051f9c2f665661fee8f61ce58ee22acb3667d3605d6d4a650ab8`;
- executed-input manifest:
  `223fd828b6337de6300ac79ccaf2889344c6f5131f20ae14f0cbda0eb65d11c0`.

The run contract freezes the three material states, `NSNAP=3`, TONE tracking
density `50.0`, `MXIT=20`, TONE `EPS=1.0e-5`, FLU
`solver_eps=5.0e-7`, one OpenMP thread, the 7200 s process boundary and zero
retries.  The process boundary is operational metadata; it does not enter the
transport or POD equations.

## Consequence

The snapshot-admission gate correctly remains closed, so no rank-two D4-A
basis may be constructed from this attempt.  The next validation action must
target the single-state full-rank FLU path and obtain its real iteration
terminal or an internal failure diagnostic before spending time on the other
two material states.  It must retain the same operator and declared numerical
criterion; changing the POD rank cannot repair a missing offline snapshot.

## Minimal root-cause boundary

The current and historical snapshot builders use the same physical route,
`SALT -> MCCGT -> ASM:ARM -> FLU TYPE K`, but their FLU problems are not
numerically equivalent.  The historical completed 750 C calculation used
`EXTE 30 1.0e-4` with default unknown and thermal criteria of `5.0e-5`.
The current calculation uses `EXTE 500 5.0e-7`, `UNKT 5.0e-7` and
`THER 5.0e-7`, and its terminal requires all three residuals to pass.  The
historical 671 s FLU time therefore cannot predict the current strict solve.

This D4-A `MCCG` system currently follows ordinary `FLU2DR`, not the separate
SPOT REAL64 online route.  `EDIT 0` suppresses its intermediate group, inner
and outer residual reports, although strict success/failure terminals remain
unconditional.  The timeout log consequently cannot distinguish slow
progress from a particular stalled iteration level.

That minimal follow-up has now been executed.  With the same operator and
three `5.0e-7` criteria, raising only FLU output from `EDIT 0` to `EDIT 2`
showed five 40--41 s full-group MCGFL1 applications inside the first MCCGF
GMRES solve.  The first FLU2DR thermal iteration had not returned before
the 600 s diagnostic bound.  See [the FLU hierarchy diagnostic
result](d4a_flu650_diagnostic_result.md).  No state 2/3, archive or POD
construction was performed.
