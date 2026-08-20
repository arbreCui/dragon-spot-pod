# Newton-Krylov cycle 2: R_L at 3.03e-6, six gate multiples

> **Erratum (2026-08-19).** Two readings in this record are corrected by
> [rank2_h2_r64dp2_method_erratum.md](rank2_h2_r64dp2_method_erratum.md):
> the step scalar `beta < 1` in `x + beta*F(x)` **is** under-relaxation,
> so any blanket "no relaxation, damping" statement below is wrong as
> written; and the Picard-expansion measurement that motivated the
> Newton/JFNK route was itself a quantizer artifact — with the
> quantizers closed, plain Picard contracts the leakage channel by
> ~0.037 per step.  The measurements below stand as era facts.

Date: 2026-08-18

Status: three maps `VALID_NOT_MET`; contraction sustained.

## The cycle (epochs 20-22 from `CLOSED/19`, anchor `y_1`)

Identical recipe to cycle 1; every coefficient computed from measured
quantities in the frozen height-L2 leakage metric.

1. `z_1 = y_1 + 0.25 F(y_1) -> CLOSED/20`:
   $(3.2224836\times10^{-8},\,3.0280941\times10^{-6},\,
   4.4367035\times10^{-9},\,6.7499134\times10^{-8})$ — $R_L$ at
   **6.06 gate multiples**, the smallest certified leakage stopping
   defect of the project.
2. `z_2 = y_1 + 0.117462\,q_1` (nested affine) `-> CLOSED/21`.  Its own
   residual is large (`6.55e-5`): the norm-matched step along $q_1$
   exceeded the local linear regime — recorded as a measured fact and
   used only as the Jacobian action sample.
   **Addendum (2026-08-18, superseding the reading above):** the
   direction-1 campaign reproduced this residual to five significant
   figures from an unrelated affine state and traced it to REAL32
   quantization of the radial feedback operator (`RADIAL-OP`),
   amplified ~780x by catastrophic cancellation in `SPOLE2` at
   resonance groups — not a linear-regime exceedance.  See
   [rank2_h2_r64dp_d1_campaign_result.md](rank2_h2_r64dp_d1_campaign_result.md).
3. Iterate `alpha = (0.221201, -0.000139) -> CLOSED/22`:
   $(3.0694100\times10^{-8},\,3.1725251\times10^{-6},\,
   4.6483209\times10^{-9},\,8.4668083\times10^{-8})$; measured leakage
   L2 residual `7.7759e-8` against predicted `7.1624e-8` (8.6% model
   error).

## Trajectory and measured structure

- Best certified $R_L$: `4.8157e-6` (g) → `4.3969e-6` (y_1, cycle 1)
  → `3.0281e-6` (z_1, cycle 2).  Leakage L2 residual:
  `1.648e-7` → `8.618e-8` → `7.776e-8`.  $R_\rho$ and $R_a$ pass the
  unchanged gate at every state of both cycles.
- In both cycles the second Krylov direction contributed essentially
  nothing (`alpha_2` of `9.3e-3` then `-1.4e-4`) while the direction-1
  probe (`anchor + 0.25 F`) captured the gain.  The measured
  (I-J)-action on the residual is nearly scalar at current amplitude;
  the marginal value of the second direction map is, at present,
  below its cost.  This is a measured property of the map, recorded
  for the next contract decision; no recipe change is made here.

## Boundary

Chain at `CLOSED/22`; best state `z_1` (`R_L = 3.0281e-6`).
Continuation: further cycles from `z_1`.  At the observed per-cycle
contraction (0.69-0.72x on $R_L$) the unchanged `5e-7` gate is
approximately 5-6 cycles away; if the next contract adopts the
measured fact above (direction-1 probes only, one map per step until
the linear model degrades), the same progress costs one map per step.
No relaxation, damping, or empirical control is introduced or
authorized.  Evidence:
`iterative-rank2-h2-r64dp-newton-c2-{z1,z2,iterate}-map`,
`iterative-rank2-h2-r64dp-newton-c2`.
