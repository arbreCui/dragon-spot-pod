# First rank-2 sensitivity-map attempt

## Classification

`INVALID_MAP` (reported reason: `TIMEOUT_BEFORE_TERMINAL`); no scientific
rank-2 map result exists.

The attempt used the same raw x7 axial solution as the retained rank-1 x8
map.  Production `SPOSTATE` canonicalized that raw solution in the frozen
rank-2 basis before `SPOPROJ FIXB`.  No coefficient was fitted or manually
zero-filled.

## What completed

The radial half completed normally in 73 CPU seconds.  All three frozen-source
solves produced one strict outer pass and one strict inner terminal.  Three
finite records of each `SPOFSRC` and `SPOFCHK` diagnostic were present; they
have no separate predeclared acceptance threshold.  Fixed-rank assembly returned
`SPOT-FIXB=1`, `SPOT-FS-N=3`.

The re-encoded parent has 2220 coefficients, rank-2 volume-Gram defect
`6.63754e-8`, maximum stored off-space value `1.43736e-9`, and a fixed-space
projection diagnostic `9.10335e-8`.  The live radial diagnostics were

| quantity | value |
|---|---:|
| `SPOT-RBAL` | `3.647129195171330e-7` |
| `SPOT-Q-L2` | `2.125786480049067e-7` |
| `SPOT-Q-MAX` | `2.625565883291890e-7` |

These are staging diagnostics only, not a rank-2 convergence or accuracy
result.

## Where it stopped

The durable axial log proves that Dragon entered `FLU` but produced no
`FLU2DR-TERM` record or normal termination.  The host wrapper reported
`timeout after 80 seconds`; this line is preserved only as a clearly labelled
transcription of the Codex tool output, not as an independently captured raw
stderr/status log.  A separate post-exit process census found no remaining
SPOT Dragon process.  No `candidate_axial.xsm`, `candidate_snapshots.xsm`, raw
defect or independent one-map audit exists.  The requested result directory
was never created, and the runner made no retry.

The durable classification is therefore `INVALID_MAP`; the reported runtime
reason is consistent with the incomplete log but is not independently timed
by that log.  This is not evidence of axial nonconvergence or of rank-2
physics failure.  The historical rank-1 axial solve used 45 CPU seconds;
doubling the modal order changed the cost, but this interrupted run does not
measure the completed rank-2 cost.

## Retained local staging

The successful radial output is retained locally, Git-ignored, at
`validation/artifacts/iterative-rank2-radial-staging/`.  Its receipt validates
with

```sh
cd validation/artifacts/iterative-rank2-radial-staging
shasum -a 256 -c staging.sha256
```

The essential retained hashes are

| object | SHA-256 |
|---|---|
| `candidate_radial.xsm` | `091ed4cefbef9042dba0279dbd16f3bc3541eb7804039c8964d22357261fccd6` |
| `candidate_system.xsm` | `c2700e289ab98b1a26e4511f1fe988723d58804b674e4cde32d836d01d77acda` |
| `rank2_parent_axial.xsm` | `a464cc05a1d21f00c1edb1e1cc5451846a995cb67b08f0869d4709958f9e6e38` |
| `radial.log` | `b7aa9ffaf87b720338bd16a6a4f58505ac8f1b184eea0bfd7ef43b264e4b127d` |
| interrupted `axial.log` | `c45d325a0b36f95634f3e7b7f0b3326fbe29f353157fe7fb082dc0f3371ce24c` |

The staging receipt also locks the exact `SpotRefFS.c2m`, `SpotPlaneFS.c2m`
and runtime-source copies.  `runtime_provenance.tsv` records the Dragon,
Ganlib archive and Ganlib module hashes.  `attempt_host_observation.txt`
preserves the timeout report with its explicit transcription limitation.

No further Dragon run is automatic or authorized by this receipt.  A future
step, if separately chosen, would be a second operational attempt consuming
this hash-locked radial staging and running only the axial half under a newly
declared wall bound.  It cannot retroactively complete this attempt.  Changing
that operational bound does not change the physical equations or solver
tolerance.

That separately authorized second operational attempt later completed and is
reported in [rank2_axial_only_result.md](rank2_axial_only_result.md). Its valid
map does not alter this first attempt's `INVALID_MAP` classification.
