# REAL64 axial flux-kernel scoping audit

Date: 2026-08-18

Status: `READ_ONLY_SCOPING_AUDIT`; no code was changed.

Motivation: the frozen solver-floor boundary
([rank2_h2_r64_solver_floor_boundary.md](rank2_h2_r64_solver_floor_boundary.md))
shows the axial flux-update metric plateaus near `5.8e-7` (binary32)
and the certifiable $R_L$ floor is about `2.5e-6`, above the `5e-7`
gate.  This audit maps every binary32 site on the axial path and the
change surface for a genuine REAL64 axial flux/leakage chain.

## Where the binary32 floor lives

1. **Flux driver** `src/FLU2DR.f` (1538 lines): the entire flux
   iterate `FLUX(NUNKNO,NGRP,8)` is `REAL` (line 164); the
   convergence metrics `EINN/GINN/FINN/EEXT` are implicitly typed
   binary32 (no `IMPLICIT NONE`), the SPOT latches `EINR_LAST` and
   `EUNK_LAST` are `REAL` (line 147).  The `EUNK` plateau site is
   lines 1275-1289: it subtracts two binary32 iterates, so its floor
   is a few binary32 ulps — the observed `5.8e-7` is ~5 ulp and is
   structural.  Flux and source records are written with LCM type 2
   at lines 1457-1461; `K-EFFECTIVE` is demoted from the REAL64
   eigenvalue to binary32 at line 1478.  Only the eigenvalue path is
   already REAL64.
2. **Axial solver egress** `src/SPOT1P.f90` (lines 33-34): the modal
   SN solve is computed **in double precision internally** and demoted
   to `real, intent(out)` flux/current at the ABI.  `src/SPOF.f:49`
   declares the door vectors `REAL`.  This is the primary demotion
   point — the hard numerics already exist in REAL64.
3. **Leakage integration** `src/SPOT_LEAKAGE.f90` `SPOLE1`
   (lines 13-50): all-binary32 accumulation and division;
   `SPOT-LEAK1D` written type 2 (`SPOLEAK.f90:157`); `SPOSTATE.f90`
   rebuilds leakage in binary32 and widens it **after** rounding
   (line 218), so the type-4 `SPOT-X-L` record carries only binary32
   information; `SPOT-X-RHO` inherits the binary32 `K-EFFECTIVE`
   (line 100).
4. **Defect math** `src/SPOXCONV.f90` is already exact REAL64 on
   these binary32-valued operands (lines 140-184) and needs **no
   arithmetic change**: $R_L$, $D_L$, $R_\rho$ lift off the floor
   automatically once `SPOT-X-L` and `SPOT-X-RHO` hold genuine
   REAL64 values.
5. **Not on the path**: the Trivac linear-algebra chain
   (TRIFLV/MTLDLx/ALLDLx/ALVDLx, all REAL32 with only Utilib
   `ALDDLF/ALDDLM/ALDDLS` double twins) is *not engaged* — the axial
   deck uses TRACK-TYPE `SPOT`, so the solve goes through the SPOF
   door.  Trivac conversion is out of scope unless the axial solve is
   ever retracked.

## Existing REAL64 infrastructure (reusable)

The radial side is already fully REAL64: `SPOR64_A8` (REAL64 MOC
door), `SPOR64_A9` (`FLU2DR64_CORE` outer/inner driver), the
`SPOT-R64` authority schema with type-4 `FLUX/SOUR/QFISS` and
bitwise-checked type-2 mirrors, and the `SPOMOC_R64_BRIDGE` capture
layer.  The axial canonical state (`SPOT-X-*` on the axial root) is an
**open schema** — no `EXACT_INVENTORY` guards it — so new type-4
records can be added without breaking any existing checker.  Two
frozen bit-identities in `SPOR64_B2W` must be revised in lockstep if
genuine REAL64 leakage flows through an epoch:
`SPOT-X-L == promote(SPOT-LEAK1D_real32)` (lines 249-259) and
`SPOT-X-RHO == 1/real(keff32)` (lines 436-438).

## Change surface (phased)

**Phase 1 — REAL64 axial flux path** (moderate; numerics already
exist):
- `SPOT1P.f90`: REAL64 egress of flux and face currents (internal dp
  core unchanged);
- `SPOF.f`: REAL64 door variant or dual-write;
- `FLU2DR.f`: `FLUX` and metrics to `DOUBLE PRECISION` (~15 declaration
  and cast sites listed in the audit), REAL64 flux/source records via
  the established authority/mirror pattern (type-4 authority record +
  bit-exact type-2 mirror), full-precision `K-EFFECTIVE` carrier.

**Phase 2 — REAL64 leakage and state**:
- `SPOT_LEAKAGE.f90`: dp `SPOLE1` twin;
- `SPOLEAK.f90`/`SPOSTATE.f90`: dp work arrays, ingest the REAL64
  flux, publish genuine REAL64 `SPOT-X-L`/`SPOT-X-RHO`, keep the
  type-2 `SPOT-LEAK1D` as a bit-exact mirror so the radial ASM
  consumer and all ~15 existing readers are untouched;
- `SPOR64_B2W.f90`: revise the two frozen bit-identities;
- the independent map checker: update its type-2 expectations for the
  new authority records (~8 sites).

**Phase 3 — only if needed**: native REAL64 leakage feedback into the
radial ASM operator.  With the Phase-2 mirror pattern the feedback is
quantized at ~1 binary32 ulp (~`1.2e-7` relative), a factor ~4 below
the `5e-7` gate; Phase 3 becomes necessary only if the iteration
stalls between `1.2e-7` and `5e-7`.  It has the largest blast radius
(SYSTEM/child-root `EXACT_INVENTORY` ledgers in `SPOR64_B2B/C/J/K/N/O/R/W/X`).

## Contract consequences

A converted kernel is a new numerical route: new Dragon binary hash,
new fixed numerical-map contract, restarted residual history, one
BOOT ingress from the best frozen state (`u` or `b`), and a rerun of
the axial-terminal census to establish the new reachable terminal.
The unchanged `5e-7` gate remains the target, per the solver-floor
boundary record.

## Collateral finding

`src/DOORFV.f:273` calls `TRIFLV` with 14 arguments while
`src/TRIFLV.f` declares 12 (upstream dragon-5.1 passes 12): the
TRIVAC flux door is latently broken in this fork.  Not on the SPOT
axial path; flagged separately.
