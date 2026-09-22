# Corrected D4-A CE production: completed, identity audit not admitted

2026-09-23. The user authorized moving the single frozen CE production run
ahead of SPOD convergence. Only execution order changed. The existing wrapper
ran once and exited 0; no transport retry, model change, sampling change or
checker relaxation was made. The SPOD continuation was not modified.

## Observed result and current classification

- OpenMC elapsed time: **111.22 s**, below the 900 s process-group cap.
- Log: one MPI process, 18 OpenMP threads; 20,000 particles, 300 batches,
  100 inactive batches, seed 731942; final statepoint has 200 realizations.
- Candidate combined `k = 1.3030848883933903`, one-standard-deviation
  `sigma_k = 0.0003319711641137808`.
- Diagnostic `sigma_pcm = 1e5*sigma_k/k^2 = 19.55036835978873`, below the
  unchanged 50 pcm limit. This alone does not admit the reference.
- The final file reports continuous-energy eigenvalue mode and 651 cell bins.
- Source/static checks and result-file hashes pass. The subsequent existing
  `read_ce()` audit stops at **statepoint Git SHA mismatch**. It has not passed
  its remaining complete statepoint/tally replay. No SPOT--CE comparison or
  physical-accuracy PASS is claimed.

The runner log contains an MPI TCP `bind() ... Operation not permitted`
warning. It is retained: the log subsequently identifies one MPI process,
completes all batches and writes the final statepoint; the wrapper exits 0.
This warning is not the reported identity-check failure.

## Identity-check failure: observed format, not a changed receipt

The sealed executable reports commit
`e542b2f035e397a647cc3ad0ae39946b1ad81e7b` and has SHA-256
`10a5d41fd8a1bf8dfed4c2779e3d782803e92c6a919f2a6acf4302878b2001af`.
Its final HDF5 file has OpenMC version `(0,15,4)` but no `git_sha1` attribute
or dataset. The API likewise returns no Git SHA. The existing check in
`check_d4a_spot_ce_receipts.py:539` therefore rejects it; this failure has
not been hidden or overridden.

Read-only inspection of the matching local source/build explains how that
format can arise:

- `/Users/wen/openmc-workspace/src/src/state_point.cpp:80` writes the Git
  attribute only inside `#ifdef GIT_SHA1`.
- `build/include/openmc/version.h:15` contains `VERSION_COMMIT_HASH` but no
  `GIT_SHA1` definition; the recorded statepoint compile command in
  `build/compile_commands.json:418` also has no such definition.
- `src/output.cpp:303` prints `VERSION_COMMIT_HASH` independently of that
  condition. Thus a printed commit does not imply a stored commit attribute.

This explains the missing metadata but is not, by itself, a substitute
identity acceptance rule. Next action requires approval of a bounded format
compatibility correction for the exact frozen runtime, with negative tests
still rejecting an explicit wrong SHA or missing SHA from an unknown build.
Then replay the saved result audit. Do not edit the HDF5/receipts, rebuild
OpenMC, rerun transport, or change the physics/statistical thresholds.

## Evidence

Artifacts are under `validation/artifacts/`:

- `d4a-corrected-ce-production-20260923/`: immutable production inputs,
  provenance, `statepoint.300.h5`, result JSON and receipts.
- `d4a-corrected-ce-production-20260923.runner.log`: full production log.
- `d4a-corrected-ce-production-20260923.ce-only-audit.log`: retained failed
  `read_ce()` audit. Frozen execution controls were checked against the
  production wrapper constants before this call.
- `d4a-corrected-ce-production-20260923.statepoint-diagnostic.log`: read-only
  metadata/k inspection, explicitly diagnostic-only after the audit failure.

SHA-256 of the production `result_receipt.sha256`:
`84b0a10c2ad4762344d205c601392b2017534e5e542a7e58c1500e8400a871fe`.
SHA-256 of the failed CE-only audit log:
`07334a91e8b1f7e98fe7d251fc79d3516da3bbb7774f79cbcc27667106903cf9`.

The SPOD canonical and release executables both retain SHA-256
`2908cf383be163cb0534847fe7115d42c9deed97684c28abdd9c29f24c6722db`.
The corrected SPOD chain remains accepted only through map 8, `VALID_NOT_MET`;
map 9 is still running at this handoff. The earlier instruction to wait for
SPOD convergence before launching CE is superseded by this explicit one-run
authorization, not by any change to final comparison acceptance.
