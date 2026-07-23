# Self-consistent Galerkin–SPOD

This document defines the target SPOT method: an iterative 2D/1D coupling,
free of fitted or empirical coupling parameters, in a fixed POD radial trial
space. Two-dimensional transport is recomputed online, its radial response is
returned to the axial problem, and the axial leakage is returned to the
radial problems until the same physical state reproduces itself.

The concise name is **self-consistent Galerkin–SPOD with a fixed offline POD
space and online radial response**.

The POD rank and ordinary solver tolerances are numerical choices. There is
no fitted closure, empirical relaxation coefficient, flux clipping, CMFD
correction, or reference-data calibration.

## 1. Build one radial trial space

For energy group \(g\), let \(p_g^{(s)}\) be normalized offline radial
snapshots on a common geometry and let

\[
W=\operatorname{diag}(w_i),\qquad
\langle u,v\rangle_W=u^TWv .
\]

Compute

\[
W^{1/2}P_g=U_g\Sigma_g Z_g^T,\qquad
B_g=W^{-1/2}U_{g,1:r_g},\qquad B_g^TWB_g=I .
\tag{1}
\]

The basis \(B_g\) is fixed during the outer iteration. This separates two
questions that must not be mixed:

1. whether rank \(r_g\) resolves the radial trial space;
2. whether the radial and axial equations are self-consistent.

`rank = 0` retains the full numerical snapshot rank during offline basis
construction. Online fixed-basis iteration uses an explicit positive rank.
Rank is a reduced discretization order, not a fitted parameter.

## 2. Define the coupled state

Let \(\mathcal R_s\) be the volume restriction from the axial mesh to radial
plane \(s\). With scalar axial flux \(\Phi_g\), define

\[
a_{s,g}=B_g^TW\mathcal R_s\Phi_g,\qquad
p_{s,g}=B_ga_{s,g}.
\tag{2}
\]

Use inverse eigenvalue \(\rho=1/k\) and the plane-wise axial leakage
coefficient \(L_{s,g}\). After fixing one global
\(\nu\)-fission-production normalization, the outer state is

\[
\boxed{x=(a,\rho,L)} .
\tag{3}
\]

There is one global eigenvector normalization. No plane-wise or group-wise
rescaling is allowed.

In stored arithmetic \(B_g\) is binary32 and is not assumed to remain exactly
orthonormal. The implementation therefore solves

\[
(B_g^TWB_g)a_{s,g}=B_g^TW\mathcal R_s\Phi_g.
\]

The production restriction is first evaluated in the same binary32 operation
order used by the radial feedback path. The online source then explicitly
reconstructs \(p=B_ga\). Consequently any reported off-space roundoff is a
diagnostic, not an unrecorded input to the next map.

## 3. One online radial update

Given \(x=(a,\rho,L)\), solve every radial plane synchronously. Fission is a
fixed source formed from the restricted axial field \(p\):

\[
\left[\mathcal A_{\perp,s}(L_s)-\mathcal S_{\perp,s}\right]u_s^+
=\rho\,\mathcal F_s p_s .
\tag{4}
\]

Here \(\mathcal A_{\perp,s}(L_s)\) contains radial transport, collision and
the signed axial-leakage removal. Multigroup scattering is converged inside
the fixed-source solve; fission is not evaluated a second time.

For the converged radial scalar flux, the source belonging to exactly the
same equation is

\[
q_{s,g,i}^+
=\sum_{h\ne g}\Sigma_{s0,h\rightarrow g,i}u_{s,h,i}^+
 +\rho\left(\mathcal F_s p_s\right)_{g,i}.
\tag{5}
\]

The radial current-divergence coefficient is then reconstructed from that
same fixed-source balance:

\[
d_{\perp,s,g,i}^+
=-\Sigma_{t,s,g,i}
 +\Sigma_{s0,g\rightarrow g,i}
 +\frac{q_{s,g,i}^+}{u_{s,g,i}^+}
 -L_{s,g}.
\tag{6}
\]

Equation (6) must use the frozen fission source from (4), not a newly
evaluated \(F u_s^+\). This source identity is part of the method, not merely
a diagnostic. At finite inner tolerance its balance residual is measured
and reported.

## 4. One reduced axial update

Project the updated radial response into the fixed trial space:

\[
D_{s,g,ab}^+
=\left\langle B_{g,a},
d_{\perp,s,g}^+B_{g,b}\right\rangle_W .
\tag{7}
\]

All material and source terms use the same Galerkin test space. The angular
flux approximation is

\[
\psi_{g,i}(z,\mu_n)
\approx \sum_{b=1}^{r_g}B_{g,ib}A_{g,b,n}(z).
\tag{8}
\]

The projected multigroup axial eigenproblem is solved once with \(D^+\),
yielding \(A^+\), \(\Phi^+\), and \(\rho^+=1/k^+\). The new restricted
coordinates are

\[
a_{s,g}^+=B_g^TW\mathcal R_s\Phi_g^+ .
\tag{9}
\]

From the reconstructed axial face currents,

\[
L_{s,g}^+
=
\frac{
\displaystyle
\sum_{f\in s}\sum_i A_i^\perp
\left(J_{g,i,f+1/2}^z-J_{g,i,f-1/2}^z\right)}
{\displaystyle
\sum_{f\in s}\sum_i A_i^\perp\Delta z_f\,
\Phi_{g,i,f}^+}.
\tag{10}
\]

This is an integrated neutron-balance identity. It contains no tunable
coefficient.

## 5. Fixed-point equation

Equations (4)--(10) define one deterministic map

\[
G:(a,\rho,L)\longmapsto(a^+,\rho^+,L^+).
\tag{11}
\]

The coupled SPOT solution is not a prescribed number of returns. It is the
solution of

\[
\boxed{F(x)=G(x)-x=0}.
\tag{12}
\]

The first solver is direct Picard substitution,

\[
x^{(m+1)}=G(x^{(m)}).
\tag{13}
\]

There is no user-facing \(\alpha\). Writing (13) as
\(x^{(m+1)}=x^{(m)}+\alpha F(x^{(m)})\) merely gives \(\alpha=1\); it is an
identity, not a physical or empirical parameter.

If direct Picard is shown not to converge after the map itself is verified,
the next mathematical problem remains (12). A residual-based nonlinear
solver may then be introduced and validated separately. It must finally be
checked with the unmodified raw map defect \(G(x)-x\), never with a mixed or
fitted surrogate residual.

## 6. Convergence quantities

For one evaluated map \(x^+=G(x)\), report separately

\[
R_\rho=|\rho^+-\rho|,
\tag{14}
\]

\[
R_L=
\frac{\lVert L^+-L\rVert_\infty}
{\max(\lVert L^+\rVert_\infty,\lVert L\rVert_\infty)},
\tag{15}
\]

with an exact all-zero branch. Its stored dimensional companion is

\[
D_L=\lVert L^+-L\rVert_\infty.
\]

\(D_L\) is a diagnostic, not a fourth dimensionless convergence criterion.
Finally,

\[
R_a=
\frac{\left\|B(a^+-a)\right\|_V}
{\left\|Ba^+\right\|_V}.
\tag{16}
\]

For stored binary32 bases, the implementation does not assume exact
orthonormality. With \(M_g=B_g^TWB_g\) and
\(H_s=\sum_{f\mapsto s}\Delta z_f\), it evaluates

\[
\|\Delta a\|_V^2
=\sum_{s,g}H_s\,\Delta a_{s,g}^TM_g\Delta a_{s,g}.
\tag{17}
\]

Formal state records already use the declared single global normalization,
so no least-squares scale is fitted during convergence checking. No group,
plane or region may be rescaled independently.

The three outer defects are not combined into an empirical weighted score.
They also do not replace:

- strict convergence of every radial and axial inner solve;
- radial fixed-source equation balance;
- the axial Galerkin equation residual;
- global neutron balance and flux positivity;
- rank, mesh, angle and solver-tolerance refinement.

## 7. What is frozen and what is updated

```text
offline and fixed:
  geometry, material data, snapshot set, POD basis, rank

updated every outer map:
  restricted axial field, fixed fission source, radial transport solution,
  radial response operator, axial eigenpair, axial leakage
```

Freezing \(B\) does not remove radial feedback: the full 2D fixed-source
problems and their response are still recomputed online. It keeps the method
mathematically identifiable by preventing basis rotations and changing trial
spaces from being confused with physical convergence.

A dynamic-POD variant may be studied later. It is a different discretization
and must compare weighted projectors, handle singular-value crossings, and
repeat the rank study. It is not silently mixed into the first formal
iterative method.

## Current status

The project is qualifying equations (1)--(17) from a clean evidence boundary;
previous one-shot and dynamic-basis trajectories are not used to establish
this method. The active source tree has an explicit online branch:
`SPOT-QFISS` preserves the frozen fission source, `SPOQFS`
combines it with final off-group scattering, and `SPOASM` builds the radial
operator from that same equation.

The fixed-basis assembly, canonical state, binary32 restriction identity and
raw residual plumbing have passed no-transport runtime tests. One corrected
map \(x_1=G(x_0)\) has also been evaluated twice from the same frozen input.
The five scientific XSM outputs are byte identical between runs. An
independent Ganlib-only checker verified bitwise preservation of the POD
package, a live change in the radial response operator, and a bit-exact
recomputation of the three outer residuals \(R_\rho,R_L,R_a\) and the
accompanying \(D_L\) diagnostic.

This establishes a deterministic evaluation of \(G\) at one point. It does
not establish contraction or outer convergence. Inner-tolerance sensitivity,
the direct Picard trajectory, discretization qualification and independent
3D validation remain in that order.
