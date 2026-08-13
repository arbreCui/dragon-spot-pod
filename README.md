# SPOT: Synthesis Proper Orthogonal Decomposition

SPOT is a reduced-order iterative 2D/1D neutron-transport method. A POD
basis represents radial dependence; online 2D fixed-source solves update the
radial response; a reduced 1D axial solve returns axial leakage. The two
parts are iterated to one self-consistent state.

The target method is **fixed-space Galerkin–SPOD with online radial
recalculation**.

It has no fitted closure, empirical relaxation coefficient, flux floor,
clipping, CMFD correction, or calibration to a reference result.

## Mathematics

For group $g$, construct one volume-weighted POD basis from offline radial
snapshots:

\[
W^{1/2}P_g=U_g\Sigma_g Z_g^T,
\qquad B_g=W^{-1/2}U_{g,1:r_g}.
\]

The fixed basis represents the restricted radial field as

\[
p_{s,g}=B_g a_{s,g}.
\]

The coupled state is

\[
x=(a,\rho,L),\qquad \rho=1/k,
\]

where $a$ is the POD coordinate vector and $L$ is the plane-wise axial
leakage. One complete online radial-plus-axial update defines $G$. SPOT
solves

\[
G(x)-x=0
\]

with direct Picard substitution,

\[
x^{m+1}=G(x^m).
\]

There is no adjustable α. Writing this update with α=1 would only restate
direct substitution.

`rank = r` is the number of retained radial basis functions. It is a
discretization order, not a temperature index or empirical coefficient.

The concise derivation is in
[SPOT_doc/rederivation.md](SPOT_doc/rederivation.md).

## One production iteration

[SpotPicard.c2m](data/SpotPicard.c2m) implements the whole outer loop. Each
iteration performs:

```text
Ba_m
  -> online 2D frozen-fission solves for every radial plane
  -> rebuild the radial response in the same fixed POD space
  -> solve the reduced 1D axial eigenproblem
  -> form (a_{m+1}, rho_{m+1}, L_{m+1})
  -> evaluate three raw defects
  -> return L_{m+1} and directly replace x_m by x_{m+1}
```

The radial equation is

\[
[\mathcal A_{\perp,s}(L_s)-\mathcal S_{\perp,s}]u_s^+
=\rho\,\mathcal F_s(Ba_s).
\]

Fission is frozen during this fixed-source solve. Final off-group scattering
and the stored radial response are built from the same equation. The POD
basis is not rebuilt inside the iteration.

`inner_eps` and `outer_eps` are numerical termination tolerances, and
`max_outer` is a safety limit. They do not modify the physical map. Reaching
an inner iteration cap is rejected for both radial `TYPE S` and axial
`TYPE K`; the last iterate is not accepted as a solution.

## Convergence quantities

For $x^+=G(x)$, SPOT reports three quantities separately:

\[
R_\rho=|\rho^+-\rho|,
\]

\[
R_L=
\frac{\|L^+-L\|_\infty}
{\max(\|L^+\|_\infty,\|L\|_\infty)},
\]

\[
R_a=
\frac{\|B(a^+-a)\|_V}{\|Ba^+\|_V}.
\]

All three must satisfy the declared outer tolerance. They are never combined
into a tuned scalar score. The dimensional quantity
$D_L=\|L^+-L\|_\infty$ is retained only as a diagnostic.

## Current verification status

The short, no-transport gate now verifies:

- volume-weighted POD construction and rank behavior;
- the frozen-fission radial source and response identity;
- leakage signs and radial balance algebra;
- canonical state construction and the three defect formulas;
- direct Picard replacement, the three-component AND stop, zero-leakage
  behavior, and finite-limit failure;
- C2M compilation of `SpotPicard` and Fortran compilation of the strict
  radial/axial termination path.

Run it with:

```sh
make spot-fast
```

It completes in a few seconds and launches no Dragon transport calculation.

A current real map from one hash-locked input also passes. It used three
online radial solves and one returned axial solve, with each process bounded
by a 75-second process timeout and a five-second termination grace, with no
parameter change or automatic retry:

\[
(R_\rho,R_L,R_a)=
(1.2812\times10^{-6},\,7.9229\times10^{-4},\,9.2283\times10^{-7}).
\]

Two direct continuations from that returned state also pass:

| map | \(R_\rho\) | \(R_L\) | \(R_a\) |
|---|---:|---:|---:|
| \(x_0\to x_1\) | \(1.2812\times10^{-6}\) | \(7.9229\times10^{-4}\) | \(9.2283\times10^{-7}\) |
| \(x_1\to x_2\) | \(0\) | \(3.9565\times10^{-4}\) | \(7.2378\times10^{-7}\) |
| \(x_2\to x_3\) | \(0\) | \(4.3249\times10^{-4}\) | \(2.3252\times10^{-6}\) |

The independent checker reproduced the fixed POD package, canonical states,
raw defects and restart physics. Details are in
[one_map_current_result.md](validation/iterative/one_map_current_result.md)
and
[map2_current_result.md](validation/iterative/map2_current_result.md). The
completed short-census result is in
[map3_current_result.md](validation/iterative/map3_current_result.md).

Physical outer convergence is **not established**. The second update
decreased all three defects, but the third increased both the leakage and
modal defects. The direct trajectory is therefore nonmonotone and \(x_3\) is
not accepted as a fixed point. Rank, mesh, angle, inner-tolerance, and
reference-solution studies remain separate validation questions.

A read-only, no-Dragon check of the frozen \(x_1,x_2,x_3\) states adds signed
information: the consecutive modal increments are obtuse in the fixed
Gram-height metric (cosine \(-0.8888508843\)) and the latter modal increment
has \(3.212598682\) times the norm of the former. This does not identify the
cause: the inner stopping gate is not a state-error bound, so physical map
behavior and numerical contamination remain unresolved. Exact definitions
and the separate leakage result are in
[map3_current_result.md](validation/iterative/map3_current_result.md).

A single follow-up attempt at half the inner tolerance timed out immediately
after the first-plane `ASM` step, before any solver terminal record. The
axial solve was not started and no scientific state was produced. It was not
retried, so the attempt does not classify inner convergence or explain the
update reversal.

The validation order is in
[SPOT_doc/validation_plan.md](SPOT_doc/validation_plan.md).

## Historical material

Earlier one-shot, precision-forensics, and B2 lifecycle experiments remain
under [validation/iterative](validation/iterative) as an archive. They are
not part of the active Picard interface or the fast acceptance gate. The
REAL64 work remains useful as a possible replacement for the radial numerical
solver; it does not change the seven-step SPOD coupling defined above.
