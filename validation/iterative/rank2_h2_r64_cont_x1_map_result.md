# First rank-two REAL64 CONT map from the h/2 return

Date: 2026-08-18

Status: `VALID_NOT_MET`.

## What was done

The work was deliberately limited to three steps.

1. The frozen h/2 state $x_1$ and its BOOT archive were admitted by B2I and
   projected by B2J as `PROJECTED/1`.  This staging performed no transport.
2. Exactly one REAL64 CONT map was evaluated: three online radial
   fixed-source solves through `SpotStepR64`, followed by one warm-started
   axial solve.  The bounds were 40 s and 80 s; observed times were about
   22.13 s and 14.46 s.  There was no retry.
3. The result was independently checked and classified.  A Ganlib-only
   checker verified uniform rank two, the fixed POD package bit for bit, a
   live radial operator, positive raw radial scalar fluxes, the canonical
   layout, and recomputed the four defects bit for bit.  Separately, the
   production B2W gates admitted the exact nested REAL64 authority/mirror
   schema and closed a validation copy as `CLOSED/1`, without another solve.

No relaxation, damping, clipping, fit, regularization, empirical parameter,
or model correction was introduced.

## Result

For the validation-only map $x_2=G_{\rm CONT}(x_1)$,

\[
(R_\rho,R_L,D_L,R_a)=
(6.4223480866765215\times10^{-8},
 6.3067022188547633\times10^{-6},
 9.2404661700129509\times10^{-9}\ {\rm cm}^{-1},
 1.2853320235833834\times10^{-6}).
\]

At the unchanged $5\times10^{-7}$ AND gate, $R_\rho$ passes while $R_L$
and $R_a$ fail.  $D_L$ is diagnostic only.  The calculation is valid, but
the coupled iteration is not converged.

The previous warm h/2 map had much larger leakage and modal defects, but it
was the one-time REAL64 BOOT ingress.  This new residual is the first pure
REAL64 CONT residual.  That cross-ingress comparison is descriptive only;
it is not a contraction estimate.

## Why AA(1) was not formed

The available residuals are $x_1-x_0$ from BOOT and $x_2-x_1$ from CONT.
BOOT promotes the compatibility seed into REAL64, whereas CONT consumes the
REAL64 authority directly.  Their numerical maps are not proven bitwise
identical.  Combining them as a stationary-map Anderson history would be
academically unjustified, so `AA1=NOT_FORMED`.

At the time of this first-map result, the remaining boundary was the
rank-one close procedure and fixed `0 -> 1` lifecycle.  That boundary has
since been removed and independently gated; the second consecutive CONT
map is documented in
[rank2_h2_r64_cont_x2_map_result.md](rank2_h2_r64_cont_x2_map_result.md).

The complete local evidence is frozen under
`validation/artifacts/iterative-rank2-h2-r64-cont-x1-map/`.
