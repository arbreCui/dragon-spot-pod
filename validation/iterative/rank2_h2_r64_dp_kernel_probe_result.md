# REAL64 axial flux-kernel probe

Date: 2026-08-18

Status: `DP_KERNEL_VALIDATED_NEW_ROUTE`; not a map, not a boundary of the
suspended r32-kernel contract.

## Kernel conversion

Following the scoping audit
([r64_flux_kernel_scoping_audit.md](r64_flux_kernel_scoping_audit.md)),
the axial SPOT flux path was converted to REAL64 with no algorithm,
physics, or empirical-parameter change:

- `src/FLU2DR64.f`: SPOT-door-only twin of the generic driver — REAL64
  flux iterate and REAL64 `EEXT/EUNK/EINR` metrics; fail-closed entry
  guards (`SPOT` door, TYPE K, `ILEAK` 0/3, `REBA OFF`, `ACCE N 0`,
  forward only); the SIGS leakage source correction in double precision
  (`FLUSP64`); read-only helpers (`B1HOM/FLUKEF/FLULPN/FLUBLN`) staged
  through explicit REAL32 buffers; dual publication — legacy type-2
  `FLUX`/`SOUR`/`K-EFFECTIVE` mirrors plus type-4 `FLUX64` and
  `SPOT-KEFF64`.  `FLUDRV` dispatches to it for `CXDOOR='SPOT'`.
- `src/SPOF64.f` + `src/SPOT1P64.f90`: REAL64 door and solver egress —
  the modal SN solve was already computed internally in double
  precision and was only being demoted at its ABI.
- `src/SPOT_LEAKAGE.f90` `SPOLE1D` + `SPOLEAK`/`SPOSTATE`: REAL64
  leakage integration from `FLUX64`, bitwise mirror verification
  against the type-2 records, genuine REAL64 `SPOT-X-L`/`SPOT-X-RHO`,
  new type-4 `SPOT-X-KEFF`; the published `SPOT-LEAK1D` and
  `SPOT-L1-ERR` remain exact REAL32 mirrors so every existing reader
  and the B2W admission identities are unchanged.
- `src/SPOR64_B2W.f90`: the two frozen bit-identities accept the
  REAL64-era demote-direction (`SPOT-LEAK1D == real32(SPOT-X-L)`;
  `RHO == 1/SPOT-X-KEFF` with `real32(SPOT-X-KEFF) == K-EFFECTIVE`).
- `SPOXCONV` is unchanged: the stopping defects were already exact
  REAL64 arithmetic.

The previous binary is archived as
`validation/artifacts/frozen-binaries/Dragon.r32-flux-3474eddc`; the
new kernel binary hash is `e343d327e048...a88a344d`.

## Probe result

One warm axial solve of the hash-identical frozen epoch-5 window
(parent proposal `q_t`, radial staging bit-identical to the `aa1-z`
map), deck changes only `solver_eps = 5.0e-8`, `REBA OFF`, `ACCE 3 0`:

- The REAL32 kernel had exhausted `MAXOUT=500` in 131.7 s with the
  flux-update metric plateaued at `EUNK=5.79e-7`
  (`iterative-rank2-h2-r64-aa1-z-axial-eps5e8`).
- The REAL64 kernel reached the strict terminal in **8 outer
  iterations and 16.89 s**: `EEXT=6.57e-10`, `EUNK=EINR=4.26e-8`,
  `KEFF=1.3624113505066326`.  The binary32 flux-update floor is
  eliminated.

The independently recomputable REAL64 defect of the same input is

\[
(R_\rho,R_L,D_L,R_a)=
(1.1265761989953660\times10^{-7},
 5.3396710693148522\times10^{-6},
 7.8235889760451365\times10^{-9}\ {\rm cm}^{-1},
 3.9396660977955810\times10^{-7}).
\]

$R_\rho$ and $R_a$ pass the unchanged `5e-7` gate; $R_L$ is now the
*true* outer defect of `q_t`, about 10.7 gate multiples: the
r32-kernel value `2.48e-6` was a noise-quantized measurement, and the
state itself was never at the fixed point.  The dp lineage records
(`FLUX64`, `SPOT-KEFF64`, `SPOT-X-KEFF`, dp `SPOT-ITER-K`) are all
present and mirror-verified.

## Boundary

This probe validates the REAL64 route: the axial solve is now
deterministic and certifiable far below the `5e-7` gate, at ~2 s per
converged warm outer chain per this window.  Continuation under the
new route requires the predeclared new numerical-map contract (new
deck constants `REBA OFF ACCE 3 0`, new Dragon hash, restarted
residual history, one BOOT from a frozen best state) before any map is
produced.  No map, retry, or successor was run here.  Evidence:
`validation/artifacts/iterative-rank2-h2-r64-dp-kernel-probe/`.
