# Repaired D4-A, 12-cell bootstrap — independently verified

Completed 2026-09-25 **19:11:05 Asia/Shanghai**, starting at 17:00:55.
Status: **CLOSED0_SEALED_PROJECTABLE_NOT_FIXED_POINT**.
This is a new fine-mesh initial state, not a Picard map or final acceptance.

## Scope and actual cost

The user approved one three-plane TYPE-S radial refresh, capped at 32400 s,
followed by a shared 60 s sealing/check phase; no retry or next Picard map.
Actual radial time was **7807.364 s**, postprocessing **3.117 s**, total
**7810.758 s** (2 h 10 min 10.8 s). The managed session 87959 exited with code 0;
its supervisor, Dragon and watchdog PIDs were absent after completion.

The seed is the verified 12-cell axial state, with k64=1.2873232763835052,
three original physical zones, fixed rank 2, unchanged materials, signed-leakage
closure and solver contract. This seed k is not a newly converged coupled k.
No empirical coefficient, threshold relaxation, CE rerun or additional axial
solve was introduced. The failed background-shell launch before WORK creation
is documented separately; there was only one actual transport attempt.

## Evidence and independent replay

Run: `validation/artifacts/d4a-scattering-mesh12-bootstrap-run-20260925`.
Its **29-entry** result manifest verifies before and after independent replay:
`805c06e1ec873809a890be3a90afe1b8c16ec57272c3eaa5c315aa8feb64b32f`.
All **15** inputs are unchanged, and the working input manifest is byte-identical
to the prepared manifest:
`b59168704acb63e70c217868cc1896468a41ff6d0b8cb8cc8013d28782781216`.
The repaired Dragon remains
`873ad14272a2f0765d95e6de067194a01708ccf9aa88d58cd782049e6d331fef`.

Each plane has exactly one ordered start/result record, `MODE=1 STATUS=8`,
zero local cutoff difference, and the run has one completion marker and one
normal terminus. B2I seals CLOSED/0; B2J constructs PROJECTED/1 without transport
and rejects the epoch-mismatch negative case with an empty output.

Independent replay in
`validation/artifacts/d4a-scattering-mesh12-bootstrap-review-20260925`
used private input copies and existing host binaries, with 15 s per host call,
without transport or compilation. Both logs and all three reproduced XSM
outputs are **byte-identical** to the original:

| Output | SHA-256 |
| --- | --- |
| closed_axial.xsm | `5d051cba0986b680f83eec2c66330f323bb4bf7dec0724b1e37e32de912bb7b2` |
| closed_snapshots.xsm | `7d903cd63ba9f635cca186eb3b809ca1db6c0a8fb8b3a7a9264bb924b7d46400` |
| projected_check_only.xsm | `a6cadabbda2810c2813cb11e66ce6c1d3123db542a591b99bdf8218095d953d7` |

A second agent independently checked hashes, plane ordering, publication status,
logs and cost, with no P1/P2 found. The original evidence was never overwritten.
The `spot-d4-a` completion monitor is now paused.

## What the solver receipts establish

STATUS=8 is the existing strict accepted-publication path; the frozen code
requires its original EEXT/EUNK/EINR tests and strict inner completion. The BOOT
log does **not** print all three final scalar residual values, so this is not
an independent numerical reconstruction of those residuals. Printed MCCGF
subsolve endings and SPOFCHK diagnostics must not be substituted for them.

| Plane | Printed SPOFCHK L2 | Printed RBAL |
| --- | ---: | ---: |
| 1 | 3.042097e-3 | 1.137253e-7 |
| 2 | 5.167728e-3 | 4.568795e-8 |
| 3 | 2.973155e-3 | 1.085817e-7 |

These use the REAL32 mirror and compare with the prior radial field. They are
not the coupled Rrho/Rleak/Ra defects and do not prove the original 5e-7 AND gate.

## Next minimum step

Register this verified CLOSED/0 and the already-tested fine-mesh independent
checker as an explicit new runtime/acceptance identity, preserving the old
three-cell epoch and its NOT_MET results. Do not relabel an old parent or
replace a sealed runtime. Then perform a transport-free preflight for the first
12-cell coupled map. That map needs a new explicit compute budget; none has
been started or authorized by this bootstrap.

Final coupled convergence, mesh/angle and POD accuracy, same-mesh cold/warm
repeatability, and the final CE comparison remain open. Existing final shape
comparison covers three physical-zone nu-fission fractions, not 651-point
pinwise accuracy or thermal power. This is D4 component work, not IRENA full core.
