# Independent axial discretization check before another native extension

The retained-state native refinement is limited to 64 cells. Its recorded
mesh failures must remain failures; no larger native grid or changed axial
scheme is implicitly admitted by this document. The next bounded experiment
isolates the existing first-order upwind error against an analytic transport
solution, before choosing a more expensive native calculation or a different
axial discretization.

## Analytic problem

Use a homogeneous slab of height H=20 cm, two axial directions
`mu=+/-1/sqrt(3)`, half-range weights 1/2, uniform source q=1 in each direction,
isotropic scattering, and vacuum incoming flux at both ends. Define

```
phi = (psi_plus + psi_minus)/2
J = mu*(psi_plus - psi_minus)/2
dJ/dz + sigma_a*phi = q
mu^2*dphi/dz + sigma_t*J = 0
sigma_a = sigma_t - sigma_s
```

For positive absorption, set `kappa=sqrt(sigma_t*sigma_a)/mu`. The analytic
scalar solution is

```
phi(z) = q/sigma_a * [1 - cosh(kappa*(z-H/2)) /
              (cosh(kappa*H/2) + mu*kappa/sigma_t*sinh(kappa*H/2))]
J(z) = -mu^2/sigma_t * dphi/dz
```

Use stable evaluations and analytic cell averages, not center samples as
surrogates for averages. For zero absorption and positive total, use

```
J(z) = q*(z-H/2)
phi(z) = q*H/(2*mu) + sigma_t*q*z*(H-z)/(2*mu^2)
```

For the void limit use the exact streaming solutions
`psi_plus=q*z/mu` and `psi_minus=q*(H-z)/mu`. Check the differential equations,
vacuum boundary conditions and global source/absorption/escape identity
independently of the finite-volume solver.

Prescribe total cross sections 0.02, 0.2 and 2 per cm; for each use scattering
fractions 0, 0.9, 0.99 and 1. Add the void case. These 13 manufactured cases
are not fitted to native response or leakage. They do not represent measured
group constants or reproduce the native radial white-boundary problem.

## Discrete controls and reported errors

Use exactly the signed first-order upwind axial operator of the retained-state
study. Solve the full two-direction linear system, with isotropic scattering
coupled explicitly through phi, on 8/16/32/64/128/256 cells. These are cheap
manufactured-slab grids, not an extension of the native 64-cell experiment.
Use one numerical CPU thread. Freeze the execution cap and memory budget
before running. No fission, eigenvalue, native radial operator or POD is used.

Before interpreting errors, require matrix residual below `5e-12`, raw global
balance below `1e-10`, and nonnegative flux without clipping. Evaluate analytic
identity checks against source/current scales at `5e-12`. Keep physical
boundaries and source conventions identical between discrete and analytic
solutions. Preserve signed currents.

For every case and mesh report cell-average flux and directional errors,
top/bottom and total escape errors, adjacent-grid changes, observed order
when defined, and the difference between adjacent-grid change and true
analytic error. Zero-absorption escape is constrained by balance and therefore
cannot alone test spatial accuracy. Do not infer full transport accuracy from
its small leakage error or discard its scalar error.

These error magnitudes are measurements, not pass targets to fit. Passing the
algebra/balance checks qualifies the implementation of this manufactured
problem only. It does not establish native mesh convergence.

## Decision and evidence boundary

If the controls show the expected diminishing upwind error but slow convergence
in strongly mixed cases, quantify the cost implication before proposing a
new native grid or positive higher-order discretization. Any new scheme must
separately retain native zero-gradient action, signed states, common radial
white return, positivity and current balance. If independent analytic checks
instead expose an implementation error, correct it in private diagnostics
before extending the reference.

Preserve the existing full-space angular failures, failed native mesh gates,
and resource-limited attempt. Archive prescribed inputs, source snapshots,
analytic references, all mesh results and a fresh replay. Do not alter live
D4 files or treat this slab experiment as a coupled multigroup reference.
