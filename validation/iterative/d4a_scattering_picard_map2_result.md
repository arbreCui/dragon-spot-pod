# Repaired D4-A Picard map 2 — 2026-09-25

**Independently verified: CLOSED/2, VALID_NOT_MET.** All three coupled defects
decreased from map 1, but none meets the unchanged `5e-7` AND gate.

| Defect | Map 1 | Map 2 | Map 2 / map 1 | Remaining / gate |
| --- | ---: | ---: | ---: | ---: |
| Rrho | 5.4371895350291410e-5 | 1.1297807610666233e-5 | 0.207788 | 22.60 |
| Rleak | 4.7850057108391490e-3 | 6.5493434068397758e-4 | 0.136872 | 1309.87 |
| Ra | 2.2933216671981128e-4 | 5.8302936113966324e-5 | 0.254229 | 116.61 |

Logged k64 is **1.2718844894038088**, versus 1.2719027660185727 in map 1.
The conventional reactivity change `1e5*(1/k1 - 1/k2)` is **−1.1297807611 pcm**.
The table gives one observed step ratio, not an asymptotic convergence rate or
a forecast of remaining iterations. Dleak=1.8022368424625197e-6 is not gated.
Out-of-span=5.8768943392390130e-8 (group 176, plane 3) uses a different norm;
it is not a bound on rank error or evidence of final accuracy.

## Execution and independent review

The single authorized attempt ran from **2026-09-24 22:07:28** to
**2026-09-25 03:10:32 Asia/Shanghai**, elapsed **18183.981 seconds
(5 h 3 min 4 s)**. It stayed within radial/axial caps 32400/180 seconds and the
32580-second total cap. No retry or map 3 occurred. The original tool session
returned zero; the observed supervisor and child PIDs had exited at review.
The completed attempt's `spot-d4-a` monitor is now **PAUSED**.

Artifacts:

- Work: `validation/artifacts/d4a-scattering-picard-map2-20260924`.
- Control: `validation/artifacts/d4a-scattering-picard-map2-control-20260924`.
- Independent review: `validation/artifacts/d4a-scattering-picard-map2-review-20260925`.

Verification passed before and after GANLIB-only read-only replay:

- All 48 result entries, 12 pre-run parent/deck entries, 8 input entries,
  6 output entries and 11 runtime entries verify.
- All original map-1 and CLOSED/0 result entries verify unchanged; the
  prepared runtime and one-map runner still match their original pins.
- Radial plane entries are exactly 1, 2, 3 in order, followed by normal
  radial completion and production admission PASS.
- B2J reports CLOSED/1 → PROJECTED/2 and the expected epoch-mismatch rejection;
  B2W reports CLOSE PASS and CLOSED/2.
- The axial solve terminates normally in 5 outer iterations, with
  EEXT=2.88058608e-7 and EUNK=EINR=1.45177903e-6, below the existing 2e-6
  solver thresholds. This is not the coupled convergence test.
- `check_one_map_xsm --continued` and `check_convergence_gate` reproduce the
  sealed logs byte for byte. Each replay had a 10-second cap. New logs were
  written only to the independent review directory, not the sealed result.
- The full acceptance entry replays the real maps 1–2 prefix successfully,
  then correctly refuses final acceptance because no repaired MET exists.
  No final observables are fabricated. Map 2 also passes the existing
  next-parent preflight with NO-TRANSPORT / NO-OUTPUT; this starts no map 3.

Result-manifest SHA-256:
`ea5f32cbd983fe81d9d0f9bf60ab49853744763a1ab992fd0b536b1bb7398dea`.
Closed axial SHA-256:
`fdd615ddd8af9f34f501598637e5dbcd2967082a3ec208f48cb76a7a8a47d199`.
Closed snapshots SHA-256:
`a471e6a691b57bf41a9fd9aba0421bddf32ca0973769c6892f3544c6d7f14b76`.
The controller's original `VALID_NOT_MET_PENDING_INDEPENDENT_REVIEW` status is
preserved; this separate record supplies the completed independent review.

## Next decision — convergence is not accuracy

The repaired online coupling now has two complete maps with decreasing defects.
Nevertheless, map 2's diagnostic reactivity difference from the existing CE k
is −1882.52 pcm, much larger than the declared 558.65 pcm comparison budget.
This is an unconverged-state diagnostic, not final rejection or a decomposition
of mesh, closure, POD and nuclear-data processing errors.

The highest-value next check remains the already prepared isolated **3→6
axial-cell comparison**, using map 1's fixed radial response, the same cold
start, rank, angular order, material boundaries and solver thresholds. Proposed
budget: **180 seconds total, 90 seconds per solve, no retry**, with no feedback
into this chain and no CE rerun. The user subsequently approved it: 3-cell
passed, 6-cell timed out, and no retry occurred. See the
[separate mesh-attempt result](d4a_scattering_axial_mesh_result.md). A fresh
300-second 6-cell attempt is proposed and awaits approval. Prefer resolving
that accuracy-direction check before another five-hour radial map unless the
user chooses otherwise.

Any map 3 needs a separate explicit budget. No damping, empirical coefficient,
clipping, rank/closure change or relaxed gate is introduced. The target remains
a validated D4 component; neither this result nor CLOSED/2 is IRENA full-core
validation or a completed production release.
