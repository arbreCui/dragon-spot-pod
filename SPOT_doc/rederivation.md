# Concise derivation of fixed-space Galerkin–SPOD

This document defines the SPOT equations used by the implementation. It keeps
the mathematics deliberately small: one fixed POD space, one online radial
fixed-source problem, one reduced axial problem, and direct Picard iteration.

## 1. Fixed radial space

For energy group $g$, collect normalized offline radial snapshots in $P_g$.
With radial volume matrix $W=\operatorname{diag}(w_i)$, compute

\[
W^{1/2}P_g=U_g\Sigma_gZ_g^T,
\qquad
B_g=W^{-1/2}U_{g,1:r_g}.
\tag{1}
\]

Thus $B_g^TWB_g=I$ in exact arithmetic. Stored finite-precision bases need
not be exactly orthonormal, so the implementation retains the Gram matrix

\[
M_g=B_g^TWB_g.
\tag{2}
\]

The rank $r_g$ is a spatial discretization order. The basis and rank remain
fixed during one convergence study.

## 2. Coupled state

Let $\mathcal R_s$ volume-restrict the axial scalar flux to radial plane $s$.
The POD coordinates satisfy

\[
M_g a_{s,g}=B_g^TW\mathcal R_s\Phi_g,
\qquad p_{s,g}=B_ga_{s,g}.
\tag{3}
\]

After one global fission-production normalization, define

\[
x=(a,\rho,L),\qquad \rho=1/k.
\tag{4}
\]

$L_{s,g}$ is the signed axial leakage coefficient for plane $s$ and group
$g$. No group-wise, plane-wise, or region-wise rescaling is allowed.

## 3. Online radial problem

Given $x$, reconstruct $p=Ba$. For every radial plane, solve

\[
[\mathcal A_{\perp,s}(L_s)-\mathcal S_{\perp,s}]u_s^+
=\rho\,\mathcal F_s p_s.
\tag{5}
\]

The right-hand-side fission term is frozen during this solve. Multigroup
scattering is converged, but fission is not reevaluated from $u_s^+$.

The source associated with the final radial field is

\[
q_{s,g}^+
=\sum_{h\ne g}\Sigma_{s0,h\to g}u_{s,h}^+
 +\rho(\mathcal F_s p_s)_g.
\tag{6}
\]

The radial response used by the axial equations is then

\[
d_{\perp,s,g}^+
=-\Sigma_{t,s,g}+\Sigma_{s0,g\to g}
 +\frac{q_{s,g}^+}{u_{s,g}^+}-L_{s,g}.
\tag{7}
\]

Equations (5)–(7) use the same frozen fission source. Replacing it with
$\mathcal F_su_s^+$ would define a different nonlinear map.

## 4. Reduced axial problem

Project the radial response into the fixed space:

\[
D_{s,g,ab}^+
=\langle B_{g,a},d_{\perp,s,g}^+B_{g,b}\rangle_W.
\tag{8}
\]

Use $D^+$ in the reduced 1D axial eigenproblem. Its solution gives
$\Phi^+$, $k^+$, and new coordinates through (3). The returned leakage is
the integrated axial current balance

\[
L_{s,g}^+
=
\frac{\displaystyle
 \sum_{f\mapsto s}\sum_i A_i^\perp
 (J^z_{g,i,f+1/2}-J^z_{g,i,f-1/2})}
{\displaystyle
 \sum_{f\mapsto s}\sum_i A_i^\perp\Delta z_f\Phi^+_{g,i,f}}.
\tag{9}
\]

This is a neutron-balance identity, not a closure coefficient.

## 5. Fixed-point equation

Equations (3)–(9) define

\[
G:(a,\rho,L)\mapsto(a^+,\rho^+,L^+).
\tag{10}
\]

The coupled solution satisfies

\[
G(x)-x=0.
\tag{11}
\]

The initial nonlinear method is direct Picard substitution:

\[
x^{m+1}=G(x^m).
\tag{12}
\]

No relaxation factor appears. If direct Picard is later shown not to
converge, another nonlinear solver may be studied against the same raw map;
it must not alter equations (5)–(10).

## 6. Three separate defects

For $x^+=G(x)$, use

\[
R_\rho=|\rho^+-\rho|,
\tag{13}
\]

\[
R_L=
\frac{\|L^+-L\|_\infty}
{\max(\|L^+\|_\infty,\|L\|_\infty)},
\tag{14}
\]

with an exact all-zero leakage branch, and

\[
R_a^2=
\frac{\displaystyle
 \sum_{s,g}H_s\Delta a_{s,g}^TM_g\Delta a_{s,g}}
{\displaystyle
 \sum_{s,g}H_s(a_{s,g}^+)^TM_ga_{s,g}^+}.
\tag{15}
\]

The three defects are checked independently. They are not fitted, weighted
together, or used to rescale the state.

## 7. Numerical versus physical choices

Fixed physical/discretization inputs are geometry, materials, tracks,
snapshot set, POD basis, and rank. Updated physical state is $(a,\rho,L)$,
the radial solution, and the radial response.

Inner and outer tolerances define when the discrete equations and fixed point
are considered numerically resolved. An iteration cap is only a safety bound.
If a radial or axial inner solve reaches its cap without satisfying the
declared strict predicate, $G(x)$ has not been evaluated and the program
fails closed.

The implementation is [data/SpotPicard.c2m](../data/SpotPicard.c2m).
