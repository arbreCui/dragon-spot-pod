# Direction-1 campaign: new best R_L 2.12e-6, then the REAL32 radial-operator floor

Date: 2026-08-18

Status: two maps `VALID_NOT_MET`; `RADIAL_OP_R32_FLOOR_ESTABLISHED`.

> **Superseded in part (2026-08-18, same day):** the REAL32
> `RADIAL-OP` mechanism below was closed by the REAL64 radial feedback
> kernel, but the `6.55e-5` event **persists under exact arithmetic**
> and is now localized to a discrete branch in the
> publication/projection chain at plane 2, group 132.  The maps and
> defects recorded here are unchanged; only the causal reading is
> superseded.  See
> [rank2_h2_r64dp_radialop64_result.md](rank2_h2_r64dp_radialop64_result.md).

## The campaign (epochs 23-24 from `CLOSED/22`, anchor `z_1`)

Approved contract: direction-1 probes only (`x + 0.25 F(x)`, one bounded
map per step), full two-direction cycles only on model degradation.

1. `w_1 = z_1 + 0.25 F(z_1) -> CLOSED/23`:
   $(2.9309964\times10^{-8},\,2.1220190\times10^{-6},\,
   3.1091402\times10^{-9},\,8.0333565\times10^{-8})$ — $R_L$ at **4.24
   gate multiples**, the smallest certified leakage stopping defect of
   the project (0.70x of `z_1`, exactly the projected per-step rate).
2. `w_2 = w_1 + 0.25 F(w_1) -> CLOSED/24`:
   $(4.2820142\times10^{-8},\,6.5515774\times10^{-5},\,
   9.5992415\times10^{-8},\,1.0528869\times10^{-7})$ — $R_L$ jumped
   31x.  The campaign was stopped on this event and the event fully
   diagnosed.

## Diagnosis (frozen: `iterative-rank2-h2-r64dp-radialop-r32-diagnosis`)

The `w_2` residual and the cycle-2 `z_2` residual agree to five
significant figures ($6.5516\times10^{-5}$ vs $6.5515\times10^{-5}$,
$D_L$ likewise) for two states built from entirely different affine
combinations — not smooth dynamics.  The measured chain of custody:

- Both returns are **converged**: at `solver_eps = 5e-9` (10x tighter)
  both defects reproduce (`2.1249e-6` / `6.5516e-5`).
- Cross-swapping the radial half against the axial parent moves the
  event **with the radial half** in both directions
  (`1.619e-6` vs `6.550e-5`).
- In group 132 the two `candidate_system` files differ in **exactly one
  record**: `RADIAL-OP` (24 REAL32 values, max rel diff `2.1e-3`).
  Ranks, singular values, remainder diagnostics, and every other
  group-132 record are bitwise identical.  39 of 370 groups show
  `RADIAL-OP` rel diffs above `1e-5` — a resonance-group census.
- Mechanism: `SPOLE2` (src/SPOT_LEAKAGE.f90:98) evaluates
  `-total + scatter0 + qfixed/phi - leak1d` in REAL32.  At group 132,
  mix 1, $\Sigma_t = 6.62$ while the operator value is
  `~8.5e-3`: cancellation ratio $\Sigma_t/\mathrm{DB2} \approx 780$.
  `PHIRK`, `QREG`, and `DB2` in `SPOASM.f` are all REAL32, so
  REAL32-level input differences (~1.2e-7 relative, whether genuine or
  quantization) are amplified into `1e-4`-to-`1e-3`-relative jumps of
  the radial feedback operator, which the axial solve converts into a
  `~1.2e-6` (height-L2) / several-`1e-6`-to-`1e-5` (gate metric) jump
  of the returned leakage.

Two consequences:

1. **The cycle-2 `z_2` reading is superseded**: its `6.55e-5` residual
   was this event, not a linear-regime exceedance (addendum in
   [rank2_h2_r64dp_newton_c2_result.md](rank2_h2_r64dp_newton_c2_result.md)).
2. **The certified-`R_L` floor of the current binary is a few
   `1e-6`**: the map hops between adjacent REAL32 quantization buckets
   of the radial operator under state changes of order `1e-8`.  The
   unchanged `5e-7` gate is unreachable while the radial feedback chain
   is REAL32 — structurally the same verdict as the binary32
   flux-update floor of 2026-08-18, one level deeper in the loop.

## Boundary

Chain at `CLOSED/24`; best certified state `w_1`
(`R_L = 2.1220e-6`, epoch 23).  The parameter-free continuation is a
precision repair, not an algorithm change: promote the radial feedback
chain to REAL64 — dp `PHIRK`/`QREG`/`DB2` and a dp `SPOLE2` twin in
`SPOASM.f`, a dp `RADIAL-OP64` record with the bitwise REAL32 demote
mirror (the established dp-era record pattern), dp ingestion in
`SPOF64.f`, mirror checks in the B2W/B2J/checker ties — then resume
direction-1 steps from `w_1`.  No relaxation, damping, or empirical
control is introduced or authorized.  Evidence:
`iterative-rank2-h2-r64dp-d1-{w1,w2}-map`,
`iterative-rank2-h2-r64dp-radialop-r32-diagnosis`.
