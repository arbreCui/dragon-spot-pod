# REAL64 radial feedback kernel: pocket closed, event relocated

Date: 2026-08-18

Status: `RADIAL_OP64_KERNEL_VALIDATED`; `R32_RADIAL_OP_MECHANISM_SUPERSEDED`;
`G132_QUANTIZER_LOCALIZED_TO_PROJECTION_CHAIN`.

## 1. The kernel (built and validated)

The radial feedback chain is now REAL64 end to end.  Four source
changes, all precision-only, legacy path byte-identical:

- `SPOT_LEAKAGE.f90`: dp twins `SPOLE2D` (the cancellation site
  `-total+scatter0+qfixed/phi-leak1d` in dp) and `SPOQFSD` (dp ABI;
  the accumulation was already dp).
- `SPOASM.f`: when every snapshot carries the `SPOT-R64` REAL64
  authority, the flux/source/fission-source are ingested in dp with
  per-element `transfer()` mirror checks against the REAL32 roots;
  `QREG/PHIRK/DB2` become dp; the group record `RADIAL-OP64`
  (24 dp) is written with `RADIAL-OP` as its exact bitwise demote
  mirror.  Mixed REAL64/REAL32 snapshot sets are refused.
- `SPOT1P64.f90` + `SPOF64.f`: the dp operator is consumed directly
  (presence-gated, mirror-checked; absent record falls back to the
  promoted REAL32 mirror).

Validation, all frozen in `iterative-rank2-h2-r64dp-radialop64-kernel`:
mirrors bitwise across all 370 groups; the radial source-lag
diagnostic drops from `3.6e-8` (pure r32 quantization) to `~5e-16`;
the legacy fallback replays the frozen epoch-23 receipt **digit for
digit** on an old system without `RADIAL-OP64`.

## 2. The honest negative: the 6.55e-5 event survives exact arithmetic

Replaying both campaign maps with the dp kernel:
`w_1 -> R_L = 2.636e-6` (the `2.122e-6 -> 2.636e-6` shift is the old
r32 operator noise, now gone), but `w_2 -> R_L = 6.554e-5` — the event
**persists**.  The causal claim of
[rank2_h2_r64dp_d1_campaign_result.md](rank2_h2_r64dp_d1_campaign_result.md)
(REAL32 `RADIAL-OP` quantization) is **superseded**: that pocket was
real and is now closed, but it contributed only the `~5e-7`-scale
jitter, not the event.

Two further exact measurements
(frozen: `iterative-rank2-h2-r64dp-g132-quantizer-diagnosis`):

1. **The radial solves are exact.**  Instrumented tracing shows every
   radial fixed-source solve converging to `EUNK ~1e-15` in two outer
   iterations; the frozen `2.5e-7` radial terminal (bit-pinned twice,
   in `SPOR64_B2B` and `SPOR64_A9`) never binds.  Termination
   quantization is disproven too.
2. **The step is upstream of every solver.**  Scanning
   `w_1 + beta*F(w_1)`: `beta=0 -> 2.64e-6`; `beta = 0.0625, 0.125,
   0.25` all saturate at `6.553-6.555e-5` — a step function.  The
   projected radial seed at **plane 2, group 132** is violently
   non-affine in beta (`0.0625/0.125` sit `2.0e-6` relative from
   `beta=0` while `0.25` sits `2.9e-8`; planes 1/3 scale linearly),
   and the earlier fingerprint stands: proposals `z_2` and `w_2` —
   different affine combinations — carry bitwise-identical published
   g132 leakage.  A discrete branch in the
   publication/projection chain (builder staging, B2J plane-2
   projection, or B2N source build) quantizes the g132 content of
   proposals; the returns are correspondingly bimodal
   (`1.3453849e-4` vs `1.3463450e-4` at element 502, `7e-4`
   relative — `6.55e-5` in the gate metric).

## 3. Incident and recovery (recorded for provenance)

During terminal probing, `git checkout src/SPOR64_B2B.f90` destroyed
that file's uncommitted dp-era modifications (the working tree
deliberately carries the route's kernel as uncommitted state).  The
lost logic was reconstructed from the intact committed dp
architecture: the continuation-epoch guard made dynamic (the three
`SPOT-R64` authorities must agree among themselves; no pinned epoch)
and the seed guards extended to dp-era lineages (`EPS-CONVERGE`
accepting the axial `5e-8` bits `z'3356bf95'`; `IREBAL=0` under
`REBA OFF`).  The reconstructed tree rebuilds a binary that reproduces
the pre-incident binary's defect receipts **to all 16 printed digits
on both replay maps** plus the legacy-fallback receipt.  The full
uncommitted source set is now snapshotted in
`iterative-rank2-h2-r64dp-radialop64-kernel/src-snapshot/`.

## Boundary

Chain unchanged at `CLOSED/24`; best certified state `w_1`
(epoch 23).  Pinned route binary:
`1964e004d8fd65bc5d57e30a400bf5e85ad6eed9fde1acde7c25ef55fdd78ff5`
(tree-consistent; predecessor `ea0d6431...` archived with bitwise
equivalence evidence).  Continuation: locate and close the plane-2
g132 quantizer in the publication/projection chain — a
precision/fail-closed repair of the same kind as every prior era
change; no relaxation, damping, or empirical parameter is introduced
or authorized.  Direction-1 chain steps stay paused until that branch
is closed, because affine proposals randomly land on the remote
branch (as `w_2` and `z_2` did).
