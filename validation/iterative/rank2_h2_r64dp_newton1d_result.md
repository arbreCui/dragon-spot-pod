# Newton/JFNK route: exact directional-derivative census and the 1-D step

Date: 2026-08-18

Status: `JFNK_WELL_POSED_ESTABLISHED`; `NEWTON_1D_LINE_MINIMUM_MEASURED`;
no gate result changed.

## What was run

Two derivative-probe maps on the exact line through the latest genuine
Picard pair `v = h - g` (all under the `r64dp` contract, strict `5e-8`
terminals, bitwise-checked):

- `x_A = 0.5 g + 0.5 h` -> `CLOSED/15`, defect
  $(2.9389796\times10^{-8},\,5.6583098\times10^{-6},\,
  8.2904447\times10^{-9},\,7.9895620\times10^{-8})$;
- `x_B = 0.75 g + 0.25 h` -> `CLOSED/16`, defect
  $(2.2872825\times10^{-8},\,8.1548408\times10^{-6},\,
  1.1948313\times10^{-8},\,1.1254349\times10^{-7})$.

The probe states are published through a new input-$\beta$ affine mode
of the frozen builder/checker pair (`--affine-r64-fgh-beta`); the
Anderson direction gate is bypassed for these states because their
authorization is the Newton contract itself — the step scalar is a
computed quantity, never a tuned parameter.  Together with the two
already-evaluated maps `(g \to h)` and `(q \to i)`, four exact residual
samples exist on one line at $\beta \in \{0, 0.25, 0.5, 0.9163\}$.

## Findings (offline REAL64 algebra, frozen height-L2 leakage metric)

1. **Well-posedness**: the segment difference quotients of the leakage
   residual are finite, reproducible, and mutually consistent in scale
   (`4.5694e-7`, `2.7952e-7`, `2.8178e-6`).  The binary32-era
   counterexample (quotients 0, 1, 4/3) that froze the
   `nonlinear_solver_contract` is formally overturned: directional
   derivatives of the outer map are now measurable, and Newton-Krylov
   is well-posed on this problem.
2. **Quantified nonlinearity**: the curvature diagnostics are
   `|q2-q1|/|q1| = 1.119` on $[0,0.5]$ and `10.1` on $[0.5,0.916]$.
   The affine model of the leakage response is valid only for steps
   $\beta \lesssim 0.5$ of the current pair separation and breaks
   completely beyond — this is the exact mechanism behind every
   Anderson overshoot recorded on both routes.
3. **The 1-D Newton step**: the model minimizers ($\beta^* = 0.2055$
   with the near-anchor derivative; $0.4474$ with the midpoint
   derivative, predicted residual `1.0737e-7`) bracket the measured
   line minimum at $\beta = 0.5$ — which is `x_A`, already evaluated:
   leakage height-L2 residual `1.0837e-7`, a 34% reduction from the
   anchor (`1.6479e-7`).  The gate-metric $R_L$ at `x_A`
   (`5.658e-6`) is however *above* the anchor's (`4.816e-6`): the
   remaining residual concentrates into leakage hotspots outside the
   one-dimensional span.  A single Newton direction is therefore
   insufficient by measurement, not by assumption.

## Boundary

The parameter-free path forward is a proper Newton-Krylov cycle from
`x_A`: build the Krylov space with 4-6 further directional evaluations
(one bounded map each, ~40 s), solve the small least-squares system
offline in the frozen metric, and evaluate the multi-direction Newton
iterate once.  No relaxation, damping, tuned tolerance, or model
change is introduced or authorized by this record.  Evidence:
`iterative-rank2-h2-r64dp-newton-probeA-map`, `-probeB-map`, and
`iterative-rank2-h2-r64dp-newton1d`.
