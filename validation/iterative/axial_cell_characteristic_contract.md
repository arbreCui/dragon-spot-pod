# Positive cell-characteristic comparison on the analytic slab

The [analytic upwind result](analytic_axial_slab_result.md) found two false
admissions under the adjacent-grid 1% test, and 11.09% scalar error at 256
cells in its strongest conservative-scattering case. The next bounded step
compares an explicitly declared cell-characteristic discretization against
the **same analytic problem**, before any change to native axial coupling.

## Fixed comparison

Keep the 13 slab coefficients, height 20 cm, directions `+/-1/sqrt(3)`,
weights 1/2, unit isotropic external source, vacuum axial inflow and
8/16/32/64/128/256 meshes. Reuse the sealed analytic cell means and the upwind
results as comparisons. Add independent analytic spot checks so copied
reference data do not become an unchecked truth source. No native grid is
extended, and no radial operator, eigenvalue or POD calculation is included.

## Candidate equations

Within a cell of width h set path length `L=h/abs(mu)`. For its total cross
section define the exact nonnegative characteristic coefficients

```
T = exp(-sigma_t*L)
B = integral_0^L exp(-sigma_t*s) ds
D = integral_0^L (L-s)*exp(-sigma_t*s) ds
Q_i = sigma_s*phi_i + q_i

psi_out = T*psi_in + B*Q_i
cell_average_psi = (B*psi_in + D*Q_i)/L
phi_i = (cell_average_psi_plus + cell_average_psi_minus)/2
```

For a void use `T=1`, `B=L`, `D=L^2/2`. Evaluate thin-cell integrals stably,
without subtracting near-equal quantities or choosing fitted coefficients.
The cell source is constant and coupled through the **cell average** phi,
not a midpoint flux. Neighboring cells share the outgoing/incoming angular
face value. Use one coupled full-coordinate linear solve; no source-iteration
stopping error should enter the spatial comparison.

Check the segment identities `T+sigma_t*B=1` and `B+sigma_t*D=L`.
Local elimination has denominator `1-sigma_s*D/L`; retain it explicitly and
require it to stay positive for the prescribed coefficients. An alternative
global source-response formulation is acceptable if it is algebraically
calibrated against the face/cell equations. Do not substitute a scalar
regional inverse response for a directional transport generator.

## Controls and frozen gates

Before interpreting spatial errors, freeze a run plan with one numerical
thread, memory/time caps and the following limits:

- direct matrix residual and characteristic/cell consistency below `5e-12`
  relative to source/current scales;
- raw global balance below `1e-10` and disclosed local even/odd balance;
- nonnegative outgoing angles and cell means for the physical source and
  the volume-unit/boundary-unit response basis, without clipping;
- the pure-absorption uniform-source and void solutions reproduce analytic
  cell means and faces within `5e-12` on every declared grid;
- positive-absorption periodic constant-mode controls recover
  `phi=q/(sigma_t-sigma_s)` at `5e-12`. Conservative periodic transport with
  a positive source has no steady solution and must not be normalized into one.

Compare scalar, directional, current and bottom/top/total escape errors
against the analytic values on every mesh. Retain the same error norms as
the preceding experiment and report observed orders only above the declared
roundoff floor. Adjacent-grid changes remain descriptive; they cannot replace
the analytic error check.

The declared finest-grid accuracy target is **true scalar and total escape
errors below 1% for all 13 cases at 256 cells**. It may fail; retain failures
and do not add meshes or relax the target. Report comparison with upwind
and cost at each grid without requiring an invented uniform improvement
ratio. The added response-basis controls test positivity; distinguish their
count and purpose from the 78 uniform-source analytic comparisons.

## Admission boundary

Passing qualifies this one-dimensional candidate on the stated manufactured
problem only. It does not identify a unique native axial operator. A later
native bridge must preserve retained directional states, native zero-gradient
T/B/D action, common radial white return, and current balance under finite
axial variation. That bridge requires its own contract and calibration.
No accepted slab result authorizes inserting a new generator into the native
characteristic or the running D4 chain.

Archive input identities, source snapshots, all raw fields, failed controls,
runtime metadata and an independent fresh-directory replay. Keep all existing
native failures and production/runtime files unchanged.
