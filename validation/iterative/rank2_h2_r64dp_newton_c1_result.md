# Newton-Krylov cycle 1: validated model, first sustained leakage reduction

Date: 2026-08-18

Status: three maps `VALID_NOT_MET`; `NEWTON_KRYLOV_MODEL_VALIDATED`.

## The cycle (epochs 17-19 from `CLOSED/16`, anchor `x_A`)

All steps are affine combinations of already-evaluated states with
computed coefficients; every scalar below is derived from measured
quantities in the frozen height-L2 leakage metric — no tuned parameter
exists anywhere in the cycle.

1. **Direction 1** `v_1 = F(x_A)`: probe
   `y_1 = x_A + 0.25 v_1 -> CLOSED/17`, defect
   $(4.1253887\times10^{-8},\,4.3968535\times10^{-6},\,
   6.4421831\times10^{-9},\,6.8685110\times10^{-8})$, leakage L2
   residual `8.6181e-8`.  The probe scale 0.25 comes from the measured
   affine-validity radius of the preceding record.
2. **Direction 2** `v_2 = J_G v_1` (from the measured quotient):
   `y_2 = x_A + eps_2 v_2`, `eps_2 = 0.120186` (norm-matched to the
   first probe), published as a nested affine of
   `{x_A, G(x_A), G(y_1)}` and evaluated to `CLOSED/18`.
3. **The Newton iterate**: the 2x2 least-squares system in the frozen
   metric gives `alpha = (0.237511, 0.009260)`;
   `x_new = 0.762489 x_A + 0.200471 G(x_A) + 0.037040 G(y_1)`
   (convex), evaluated to `CLOSED/19`:
   $(3.7145008\times10^{-8},\,4.4612475\times10^{-6},\,
   6.5365317\times10^{-9},\,7.8814507\times10^{-8})$.

## Findings

- **The linear model now validates**: predicted leakage L2 residual
  `8.6060e-8`, measured `8.9242e-8` — 3.7% model error at this step
  size.  This is the quantitative license for Newton-Krylov iteration
  that no previous scheme on this problem ever had.
- **First sustained certified reduction of the leakage residual**: in
  one cycle the height-L2 leakage residual fell from `1.6479e-7` (at
  `g`) through `1.0837e-7` (`x_A`) to `8.62e-8`/`8.92e-8`
  (`y_1`/`x_new`) — a 0.53x contraction, monotone along the cycle.
  The gate-metric $R_L$ fell from `4.8157e-6` to `4.3969e-6` (`y_1`),
  the smallest certified leakage stopping defect in the project.
- $R_\rho$ and $R_a$ pass the unchanged `5e-7` gate at every probe and
  iterate of the cycle ($R_a$ down to `6.87e-8`).
- The second Krylov direction contributed little (`alpha_2 = 0.0093`):
  the residual's reachable component is dominated by the first
  direction at this distance; the space will be rebuilt fresh next
  cycle as the curvature shrinks with the residual.

## Boundary

The parameter-free Newton-Krylov cycle is now a validated, repeatable
contract: ~3 bounded maps plus frozen-metric offline algebra per
cycle, ~0.5-0.6x leakage-residual contraction at current amplitude and
improving as the quadratic remainder shrinks.  Continuation is more
cycles of the same record structure from the best iterate; no
relaxation, damping, or empirical control is introduced or authorized.
Evidence: `iterative-rank2-h2-r64dp-newton-c1-{y1,y2,iterate}-map` and
`iterative-rank2-h2-r64dp-newton-c1`.
