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

An earlier legacy-inner-path census produced three hash-locked updates. It is
retained as historical evidence:

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
raw defects and restart physics for those archived objects. Details are in
[one_map_current_result.md](validation/iterative/one_map_current_result.md)
and
[map2_current_result.md](validation/iterative/map2_current_result.md). The
completed short-census result is in
[map3_current_result.md](validation/iterative/map3_current_result.md).

The current replacement evaluation enforces strict inner termination in all
three online radial plane solves and then performs one fresh axial solve. All
four numerical solves passed their declared \(5\times10^{-7}\) gates and the
Ganlib-only independent checker passed. The resulting complete map from the
same frozen \(x_2\) has

\[
(R_\rho,R_L,R_a)=
(0,\,4.3252643\times10^{-4},\,3.2409694\times10^{-7}).
\]

Physical outer convergence is therefore **not established**: \(R_\rho\) and
\(R_a\) pass, but \(R_L\) is about 865 times the declared outer tolerance.
The dimensional \(D_L=6.3417247\times10^{-7}\) is diagnostic only and is not
a fourth stop component. The complete result and immutable local hashes are
in [map3_strict_result.md](validation/iterative/map3_strict_result.md).
The replacement three-state direction check finds a smaller, acute modal
increment (cosine `+0.4969`, norm ratio `0.4478`).  The leakage increment is
obtuse in a non-production height-weighted \(L_2\) diagnostic (cosine
`-0.1551`, norm ratio `0.7312`), while the production dimensional infinity
change grows by the factor `1.0932`.  This is not a simple whole-state reverse
oscillation and does not distinguish physical-map behavior from numerical
state error. Both infinity maxima occur uniquely at plane-list index 1,
energy-group index 326: the local update changes from
`+5.8010e-7` to `-6.3417e-7`. This is a localized rebound, not proof of a
two-cycle. A focused raw-XSM balance audit reproduces all 1110 leakage values
bit for bit. A separate binary64 endpoint decomposition assigns `98.695%` and
`98.323%` of the hotspot numerator changes to the high-\(z\) face. The
production denominator's relative change is about 45–50 times smaller than the
numerator's and has the opposing ratio effect. This locates the contribution
within the archived balance but does not yet identify a physical cause. The
high-face split closes bit for bit across the eight track radial indices: all
eight reverse sign together, while the unique largest index contributes only
about `51.08%` of the L1 sum. It is therefore an exact multi-region change,
not a single-region anomaly. At that same face, the adjacent-floor audit uses
only the normalization-invariant pair

\[
R_\phi=\phi_{21}/\phi_{20},\qquad
q_J=2J_{21}/(\phi_{20}+\phi_{21}).
\]

All eight rows have \(\Delta R_{\phi,12}<0\),
\(\Delta R_{\phi,23}>0\), \(\Delta q_{J,12}>0\), and
\(\Delta q_{J,23}<0\). All 24 face currents remain negative in the common
\(+z\) convention: the update reverses, not the current direction. Therefore
the high-face rebound cannot be explained solely by an arbitrary common flux
normalization. These are adjacent cell-average fluxes and one signed face
current; no Fick coefficient, physical cause, two-cycle, or convergence claim
is inferred.

The next direct continuation, \(x_4=G(x_3)\), is defined by two
CLE-2000 decks. Its parent hashes bind the strict `state3_axial.xsm`
and `state3_snapshots.xsm`; it does not reuse `state3_system.xsm`, rebuild the
basis, or add mixing. Both decks pass the seconds-scale compiler and static
direct-Picard contract. The runtime entry is default-off and exits before any
Dragon or artifact access unless `RUN_MAP4=1` is supplied. One authorized
activation reached the 75 s radial bound after plane 1 had terminated strictly
and plane 2 had begun. The wrapper killed the process group; the axial deck was
not started. A separately authorized radial-only run with the identical deck
and inputs then completed all three planes within a 120 s safety bound; every
inner and outer terminal passed the unchanged \(5\times10^{-7}\) threshold.
A separately authorized axial-only process then terminated strictly within its
80 s bound, and the independent Ganlib-only checker reproduced the complete
map bitwise. The raw \(x_4=G(x_3)\) defects are

\[
(R_\rho,R_L,R_a)=
(0,\,5.6855251\times10^{-4},\,1.4817206\times10^{-6}).
\]

Leakage and modal defects fail the same three-component AND gate, so \(x_4\)
is not a fixed point. No \(x_5\) has been run.

Rank, mesh, angle, inner-tolerance, and reference-solution studies remain
separate validation questions.

Two separately authorized radial attempts at half the inner tolerance, with
75 s and 120 s bounds, timed out at the same logged point immediately after
the first-plane `ASM` step and before any solver terminal record. The axial
solve was not started and no scientific state was produced. These attempts
do not classify inner convergence or explain the update reversal. A short
print-only trace confirmed that the first-plane FLU solve was active, but its
inner and outer residuals fluctuated around and above the target through 27
outer iterations instead of satisfying both strict gates together. A matched
trace with FLU variational acceleration disabled still rebounded and did not
reach the target, so acceleration is not the sole cause.

The follow-up removes one legacy numerical shortcut only from the
legacy-`FLU2DR` online SPOT radial path: `EINN < 10*EPSINR` can no longer
return the current SPOT solve as `NEARLY`; it must reach the declared
`EPSINR` or the existing iteration cap. No tolerance, relaxation coefficient
or fitted parameter was added, and unrelated FLU paths retain their legacy
behavior. The seconds-scale static/compile gate passes. One bounded radial
process subsequently completed all three planes strictly, and one bounded
axial process completed the corresponding fresh map; both ended normally and
the independent complete-map check passed. This establishes a trustworthy
raw \(x_3=G_h(x_2)\), but not a Picard fixed point because its leakage defect
fails the outer gate. The optional REAL64 solver lane remains disabled by
default.

The validation order is in
[SPOT_doc/validation_plan.md](SPOT_doc/validation_plan.md).

## Historical material

Earlier one-shot, precision-forensics, and B2 lifecycle experiments remain
under [validation/iterative](validation/iterative) as an archive. They are
not part of the active Picard interface or the fast acceptance gate. The
REAL64 work remains useful as a possible replacement for the radial numerical
solver; it does not change the seven-step SPOD coupling defined above.
