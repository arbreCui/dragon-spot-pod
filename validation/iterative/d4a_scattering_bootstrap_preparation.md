# Repaired D4-A bootstrap preparation and result — 2026-09-24

Bootstrap status: **CLOSED0_SEALED_PROJECTABLE_NOT_FIXED_POINT**. The preparation
itself started no transport; the separately authorized single radial refresh
has now completed and passed independent completion checks.

## Authorized run completed

`validation/artifacts/d4a-scattering-bootstrap-run-20260924` is a fresh copy of
the 15-file prepared payload. Its `run_once.py` started the sole approved
three-plane refresh at **2026-09-24 02:08:41 Asia/Shanghai** (18:08:41 UTC on
September 23), capped at 10800 seconds. It finished normally at
**2026-09-24 04:24:33 Asia/Shanghai**, before the 05:08:41 deadline.
Radial elapsed time was **8081.7064 seconds**; total elapsed time including
sealing and projection was **8087.3168 seconds (2 h 14 min 47 s)**.
No retry occurred and no subsequent coupled map was started or authorized.

The driver checked all three plane terminals, the bridge terminal, normal exit,
and unchanged input hashes, then invoked existing B2I sealing and a no-transport
B2J projection check and stopped. `run_status.json` and `radial.log` retain the
execution record. Completion-time process inspection found no supervisor or
run children at the recorded PIDs 57432/57445/57446/57447; these are stale IDs,
not permission to signal any later process.

Independent read-only completion verification passed:

- All **29 entries** in `result.sha256` and **15 entries** in
  `input_manifest.sha256` verify. The input manifest is byte-identical to the
  prepared `prepared_inputs.sha256`; the runtime, decks and inputs are unchanged.
- Exactly three ordered plane results, each with R64 `MODE=1 STATUS=8` and
  `ACA-CUTOFF-LOCAL-PREDICATE-DIFFERENCES=0`, plus the bridge completion and normal
  Dragon terminal, are present.
- B2I reports `BOOTSTRAP COMMITTED CLOSED/0`.
- B2J reports `CLOSED/0 -> PROJECTED/1`, rejects the epoch-mismatch negative
  test with empty output, and finishes `NO-TRANSPORT`. Its
  `projected_check_only.xsm` is a projection check, not a completed map 1.
- The existing `spot-d4-a` follow-up was set to **PAUSED** after verification.
  No solver, closure, threshold, rank or empirical parameter was changed.

The sealed result-manifest SHA-256 is
`acab72a87521339f9eb0540130d0fc4ea1946b59df6bb5db4fcb83cd3528eb1c`.
The seed eigenvalue remains `1.2718148126934201`; these TYPE-S radial solves
do not produce a new coupled eigenvalue.

Plane response diagnostics are retained below. The L2 column measures the
old-to-new radial shape change, **not** the outer Picard convergence defect.

| Plane | SPOFCHK L2 shape change | RBAL |
|---|---:|---:|
| 1 | 1.945116e-3 | 1.459324e-8 |
| 2 | 6.942444e-3 | 2.179801e-8 |
| 3 | 1.966448e-3 | 5.327160e-8 |

## Preparation provenance (retained)

The working package is
`validation/artifacts/d4a-scattering-bootstrap-prepared-20260924`.
Its 15-file `prepared_inputs.sha256` verifies. All payload copies have separate
inodes; canonical/release executables, libraries, and source evidence are
unchanged. The runtime is the tested isolated repaired binary, SHA-256
`873ad14272a2f0765d95e6de067194a01708ccf9aa88d58cd782049e6d331fef`.

- Seed: the exported, independently checked corrected axial state from
  `d4a-scattering-export-fixed-20260924`, `k64=1.2718148126934201`.
  It has no old lifecycle epoch and is not relabelled from an old CLOSED state.
- Geometry, macrolib and fixed POD basis: byte-identical to that verified case.
- Initial guesses: the original admitted three TYPE-K snapshots, archive hash
  `9c46b034a22235e1b410614579028f150588c17d9938f7591b3137327495d294`.
  They remain numerical guesses, not new fixed-source responses.
- Radial tracking and route contract: original admitted copies. The contract
  keeps all three solver tolerances at `2e-6`, caps 500/740, ACCE 3/3 and B0.
- Procedures: unchanged `d4a_refresh_r64.x2m`, `SpotRefR64` and `SpotPlaneR64`.
  The B2I/B2J host tools are copied from the complete clean-source `cf469c8`
  build. No build is performed during transport and no old hash pin is bypassed.

## Work performed

The preparation deck calls **SPOLEAK only** on a private in-memory copy of the
raw archive and saves `d4a_seed_snapshots.xsm`. It makes no FLU or ASM call.
The existing current-divergence calculation supplies the seed leakage directly,
with no damping, clipping, empirical parameter or threshold change.

Postprocessing plus checks took 3.43 seconds; the postprocessor had a 10-second
cap. Independent GANLIB-only readback verifies:

- the archive's iteration k is bitwise the seed's REAL64 k;
- all 1110 REAL32 leakage entries are the exact demotion of the seed's canonical
  REAL64 leakage entries;
- all 1110 raw snapshot flux vectors and the TYPE-K state vectors are unchanged;
- neither archive nor plane roots carry old R64 authority.

A negative B2I test deliberately tried to seal these still-unsolved guesses.
It returned admission failure and created neither requested output. No guard
was modified to make them acceptable. Logs and source hashes are retained in
`check_seed.log`, `b2i_raw_guess_refusal.log` and `preparation.json`.

## Approved calculation scope (completed; not a rerun instruction)

The existing TYPE-S bootstrap bridge recomputed the three radial responses
to the **new** seed source and leakage. The old map-11 radial response belongs
to the old state and cannot be substituted as this new response. The corrected
axial seed itself does not need to be solved again.

The fresh work directory was copied from the 15-file prepared manifest and
verified before execution. After explicit budget approval, the bounded driver
ran the copied repaired `Dragon` and `d4a_refresh_r64.x2m` with one thread.
It required all three plane-result markers, the bridge completion marker and
normal solver termination before calling existing `b2i_seal_bootstrap` on the
seed, track, refreshed archive and route contract, then checked B2J projection
without transport.

The analogous completed bootstrap log records **8052 CPU seconds (2.24 h)**.
That is historical CPU time, not a promised elapsed time. The user has now
approved **10800 seconds / 3 hours hard cap for the three-plane refresh, no retry**;
the single run above completed within that cap. No CE, snapshot generation, axial refinement or
subsequent coupled map is included in that budget.

## After initial-state admission

Next comes a separately identified repaired Picard chain, with alpha=1 and the
existing three-defect `5e-7` acceptance gate. The default one-map/series route
still pins the superseded canonical hash; it must not be run or have that guard
bypassed for this package. No full fixed point, mesh convergence, final
power accuracy or CE agreement is established by CLOSED/0 admission. Any new
Picard calculation requires a separately approved time budget. This remains a
D4 component case, not an IRENA full-core validation.

### Repaired one-map entry and authorized first run

`run_d4a_rank2_picard_map.sh` now has an explicit `--repaired-runtime` option;
the old default hash is unchanged. The option requires the repaired Dragon
hash, a complete runtime manifest and a sealed parent manifest identifying
that same runtime. It privately copies the runtime into the fresh map directory,
checks immutable inputs before/after, executes exactly the existing one-map
sequence, and records the result manifest. There is no build, retry or map loop.
The radial/axial decks, contract, fixed basis and convergence gate are unchanged.

Prepared runtime: `validation/artifacts/d4a-scattering-picard-runtime-20260924`.
Its 11-file `runtime.sha256` hash is
`8888d5772c39472fe4d4895120737370fd471200c4ace9e7bf41ed8c7e74db1b`.
Dragon is the exact completed-bootstrap executable. The five host tools come
from the already-tested clean `cf469c8` build at
`/private/tmp/spot-cf469c8-clean.xZIfZa`; the B2J executable matches the bootstrap
copy bitwise. Decks and the bounded subprocess runner are unchanged source
copies. The clean-build Dragon is not substituted for the pinned bootstrap
Dragon (different build-path binary identity).

All 15 transport-free runner tests passed, including old-route preflight,
tampered runtime/parent rejection, old-runtime parent rejection, explicit-budget
enforcement, and a fully stubbed one-map/manifest round trip. The real package
also passed `--preflight-only` against the new CLOSED/0 without creating a map
directory or calling a host/solver. These tests establish orchestration, not
physical convergence.

**Authorized 2026-09-24:** the user accepted the stated budget by replying
"继续" to the explicit budget question. One radial half-step is
capped at **32400 seconds (9 h)**, then one axial half-step capped at
**180 seconds**, stop on failure or after this single map, no retry or map 2.
This reuses the previous half-step caps. The historical first D4 Picard map
records 21477 CPU seconds radially (about 6 h) and 14 seconds axially; it used
the superseded implementation and is only a cost reference, not a new-runtime
timing promise or scientific acceptance. The completed 2.24 h bootstrap is a
different solve path and cannot establish the new map's duration.

The single attempt started at **2026-09-24 15:43:28 Asia/Shanghai**. Control is
in `validation/artifacts/d4a-scattering-picard-map1-control-20260924`
(`run_once.py`, `launch.sh`, `run_status.json`, `controller.log`); actual map
outputs are in `validation/artifacts/d4a-scattering-picard-map1-20260924`.
The wrapper uses the existing tested process-group timeout/liveness helper,
with a conservative **32580-second total cap including orchestration**, in
addition to the original radial/axial caps. Overall timeout triggers at
**2026-09-25 00:46:28 Asia/Shanghai**; bounded process-group cleanup may follow.
There is no loop, retry or second map. The wrapper's logs and mutable status
are outside the map directory so they cannot alter its completed manifest.

Startup checks passed and B2J reports `CLOSED/0 -> PROJECTED/1` plus the expected
epoch-mismatch rejection. The radial process started at 15:43:36. Observed
identities were supervisor 1836, shell owner 1850, radial owner 1935, Dragon
1936, with matching executable paths and parent relationships. These are
observations, not permanent PID identities. Tool session at launch: 68853.
The existing 15-minute follow-up `spot-d4-a` was active for this one attempt only,
quiet on ordinary progress; it is now paused after independent terminal review.
No active code, deck, contract, runtime or parent
input may be changed during the calculation. Six existing timeout/liveness
tests passed immediately before launch; no rebuild was performed.

The attempt completed normally at **2026-09-24 20:41:26 Asia/Shanghai** in
17877.9010 seconds. Independent review confirms **CLOSED/1, VALID_NOT_MET**:
Rrho=5.4371895350291410e-5, Rleak=4.7850057108391490e-3,
Ra=2.2933216671981128e-4, all above the unchanged 5e-7 AND gate.
All manifests and unchanged-parent checks passed. Read-only checker/gate
replay exactly reproduced both logs, with a further complete manifest check
afterward. The result is a complete repaired map, not a coupled fixed point.
No map 2 or retry occurred. See [map-1 result and independent review](d4a_scattering_picard_map1_result.md).
