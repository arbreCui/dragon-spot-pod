# SPOT: Synthesis Proper Orthogonal Decomposition

SPOT is a reduced-order, iterative 2D/1D neutron-transport method.
Offline two-dimensional snapshots define a compact radial POD trial space.
Online two-dimensional fixed-source solves update the radial response, while
a reduced axial transport solve returns the axial leakage. The two parts are
iterated to one self-consistent physical state.

The target method is **self-consistent Galerkin–SPOD with a fixed offline POD
space and online radial response**.

It contains no fitted closure, empirical relaxation coefficient, flux floor,
clipping, CMFD correction, or calibration to reference results.

## Method in one line

For each group,

\[
W^{1/2}P_g=U_g\Sigma_gZ_g^T,\qquad
B_g=W^{-1/2}U_{g,1:r_g},\qquad B_g^TWB_g=I .
\]

The fixed basis \(B_g\) represents the radial dependence of the axial
angular flux,

\[
\psi_{g,i}(z,\mu_n)
\approx\sum_{a=1}^{r_g}B_{g,ia}A_{g,a,n}(z).
\]

The coupled state is

\[
x=(a,\rho,L),\qquad \rho=1/k,
\]

where \(a\) contains the restricted axial flux coordinates and \(L\) is the
plane-wise axial leakage. One complete radial-plus-axial update defines
\(G(x)\). The SPOT solution satisfies

\[
\boxed{G(x)-x=0}.
\]

The initial nonlinear solver is direct Picard substitution,

\[
x^{(m+1)}=G(x^{(m)}).
\]

There is no adjustable \(\alpha\). An \(\alpha=1\) written around this update
would only restate direct substitution; it is not a physical coefficient.

The complete concise derivation is in
[SPOT_doc/rederivation.md](SPOT_doc/rederivation.md).

## One outer update

```text
restrict the axial field into the fixed POD space
  -> form F p / k and solve all 2D radial fixed-source planes
  -> build radial response from that same fixed-source equation
  -> project the response into the fixed POD space
  -> solve one reduced 1D axial eigenproblem
  -> integrate the new axial leakage
```

The radial response and leakage are updated online. Only the POD trial space,
rank, geometry and material data remain fixed.

`rank = r` is the number of retained radial trial functions. It is a reduced
discretization order, not a temperature order or empirical coefficient.
`rank = 0` retains the full numerical snapshot rank during offline basis
construction. Online `FIXB` iteration uses an explicit positive frozen rank.

## Why the POD basis is fixed first

Freezing \(B\) does not remove 2D/1D feedback. It isolates physical coupling
from basis motion:

- rank convergence can be studied independently;
- the outer state and residual are unambiguous;
- SVD sign changes and singular-value crossings cannot mimic convergence;
- a later nonlinear solver acts on one fixed discretized equation.

A dynamic-POD iteration is a possible later variant, but it is not mixed into
the first formal method.

## Convergence

For one raw map evaluation \(x^+=G(x)\), SPOT reports separately

\[
R_\rho=|\rho^+-\rho|,
\]

\[
R_L=
\frac{\|L^+-L\|_\infty}
{\max(\|L^+\|_\infty,\|L\|_\infty)},
\]

and the volume-weighted physical change of the restricted flux,

\[
R_a=\frac{\|B(a^+-a)\|_V}{\|Ba^+\|_V}.
\]

Exactly one global eigenvector normalization is removed if needed. There is
no group-wise, plane-wise or region-wise fit, and the three residuals are not
combined into a tuned score.

Outer convergence does not replace strict inner-solver termination, radial
and axial equation residuals, global balance, positivity, or discretization
refinement.

## Current evidence and status

The project has been restarted from the equations above. Previous one-shot
and dynamic-basis trajectories are not imported as evidence for this method.

Online radial flux objects now store
the exact frozen \(F(Ba)/k\); `SPOASM` combines it only with final off-group
scattering and builds `RADIAL-OP` from the same fixed-source equation.
`FIXB` reuses the offline POD package bit for bit while rebuilding the live
radial response.

The canonical state path is also executable. `SPOSTATE` applies the same
binary32 plane restriction used in production, removes one global
\(\nu\)-fission-production scale, and stores \(a,\rho,L\). Explicit
`SPOPROJ FIXB` reconstructs the next radial feedback as \(Ba\), so discarded
finite-precision off-space content cannot become a hidden state variable.

The no-transport runtime fixture passes, including an independent Ganlib-only
bitwise comparison over all 370 groups. One corrected map
\(x_1=G(x_0)\) has now been run twice from the same frozen input. Both runs
completed two axial and three radial solves, and their five scientific XSM
outputs are byte identical. A second Ganlib-only checker independently
verified that the POD package stayed fixed, the live radial operator changed,
and the three outer residuals plus the dimensional leakage-change diagnostic
are bit-exact recomputations.

This qualifies one deterministic map evaluation, not outer convergence. The
measured defect is

\[
(R_\rho,R_L,D_L,R_a)=
(1.28115\times10^{-6},\,7.92285\times10^{-4},\,
1.16165\times10^{-6},\,9.22826\times10^{-7}).
\]

Here \(D_L=\|L^+-L\|_\infty\) accompanies the dimensionless relative leakage
residual \(R_L\); it is a recorded diagnostic, not a fourth convergence
criterion.

The Stage-4 controls were frozen and pushed before evaluating \(h/2\). The
initializer reproduced the same basis and \(x_0\), but all three radial
fixed-source solves exhausted `MAXOUT=500` without satisfying
\(h/2=\mathtt{0x348637bd}\). The initializer and returned axial solves passed.
Therefore the capture is `INVALID-INNER-NONCONVERGENCE`: its returned
`state1` is not \(G_{h/2}(x_0)\), no inner-sensitivity vector is formed, and
Stage 5 is not authorized.

The failure is numerical, not evidence that the physical SPOT fixed point
diverges. The active FLU tests are binary32 successive-iterate changes, not
an independent equation residual. Simply increasing `MAXOUT` has no measured
contraction basis.

The frozen single-plane diagnostic has now completed. Both the native
`ACCE 3 3` and stationary `ACCE 1 0` arms reached the six-update cap without
strict termination (`BOTH-CAP`). Fresh one-step stationary probes gave

\[
\begin{array}{c|cc}
 & D_{V,2} & D_{\max}\\ \hline
\text{NATIVE} & 2.76799\times10^{-7} & 4.14162\times10^{-7}\\
\text{STATIONARY} & 3.42986\times10^{-7} & 4.83189\times10^{-7}
\end{array}
\]

These are production-map post-minus-pre defects, not \(A\phi-q\) residuals,
error bounds, or convergence proof. No result threshold was introduced, so
Stage 4 remains `INVALID` and Stage 5 remains `NOT-AUTHORIZED`. Exact values,
interpretation boundaries and evidence receipts are in
[radial_floor_result.md](validation/iterative/radial_floor_result.md); the
predeclared controls remain in
[radial_floor_protocol.json](validation/iterative/radial_floor_protocol.json).
The forensic cap flux carries the later returned-axial \(L_1\) metadata
written by `SPOLEAK`; the cap solve itself used the archived system's
\(L_0\). The checker therefore excludes only that stale cap metadata and
requires every newly solved pre/post flux to reproduce the actual system
leakage bit for bit.

A subsequent read-only arithmetic audit counted the exact binary32 encoding
steps at all \(370\times8\) retained scalar-flux values. NATIVE moved by at
most 17 representable levels and STATIONARY by at most 12; neither map was
bitwise fixed. This makes stored-state resolution relevant, but does not
prove one unique binary32 floor. The path also contains an independent MCCG
`EPSI 1E-5`, an ACA `1E-7` cutoff, rebalancing and acceleration.

The archived MCCG `SYSTEM` contains ACA corrective/preconditioning matrices,
not the complete MOC transport operator, and its final `SOUR`/`FLUX` records
are not a same-stage pair. An \(A\phi-q\) checker cannot be constructed from
those records without misidentifying the preconditioner as physics. The next
protocol is therefore a default-off, same-sweep capture of the evaluated
state, `QFR`, source-element vector and raw MOC response from the first
primary GMRES evaluation before ACA/SCR. It writes only to the fresh
`L_FLUX` audit directory; the instrumentation adds zero extra operator
applications and has no acceptance threshold. See
[radial_precision_result.md](validation/iterative/radial_precision_result.md)
and
[raw_moc_residual_protocol.json](validation/iterative/raw_moc_residual_protocol.json).

## Validation route

1. freeze the fixed-space state, source identity and raw map residual;
2. unit-test POD projection, radial closure and leakage signs;
3. replay one complete map twice and require identical scientific records
   (passed for the first corrected map);
4. compare one production map with one tighter-tolerance map from the same
   input (attempted; invalid because the radial inner solves did not
   terminate strictly);
5. audit the completed probes in exact binary32 representable steps and
   reject an invalid ACA-matrix surrogate for \(A\phi-q\) (completed);
6. capture the first primary GMRES raw-sweep difference per frozen terminal,
   before ACA/SCR, with zero operator applications added by instrumentation
   and no acceptance threshold;
7. use that additional observable to scope a default-off REAL64
   working-iteration lane,
   retaining the same physical equation and direct Picard map;
8. only after a predeclared inner gate passes study direct Picard
   convergence;
9. after convergence, repeat rank/mesh/angle refinement and independent 3D
   comparison for the iterative solution.

See [SPOT_doc/validation_plan.md](SPOT_doc/validation_plan.md) for the
predeclared gates and evidence boundaries.

## Main files

```text
SPOT_doc/rederivation.md              target iterative equations
src/SPOPOD.f90                        weighted snapshot POD
src/SPOASM.f                          projected-system assembly
src/SPOPROJ.f90                       axial-to-radial restriction
src/SPOFSRC.f90                       frozen radial fission source
src/SPOLEAK.f90                       axial leakage integration
src/SPOSTATE.f90                      canonical fixed-space state
src/SPOXCONV.f90                      complete raw state difference
src/SPOT1P.f90                        axial modal transport solve
validation/iterative/                 active iterative contracts and fixtures
validation/iterative/check_radial_precision_xsm.f90
                                      exact stored binary32-step audit
validation/iterative/raw_moc_residual_protocol.json
                                      next same-sweep diagnostic freeze
validation/level1/                    POD algebra tests
validation/level2/                    fixed-operator algebra unit tests
```

Run the existing fast algebra tests with

```sh
sh validation/run_fast.sh
```

These tests plus `validation/iterative/run_stage0_runtime.sh` qualify the
zero/short-compute implementation plumbing. The bounded transport runner

```sh
DRAGON_BIN=/absolute/path/to/Dragon \
GANLIB_LIB=/absolute/path/to/libGanlib.a \
GANLIB_MOD=/absolute/path/to/ganlib/modules \
SEED_DIR=/absolute/path/to/iterative-seed \
VERIFY_REFERENCE=1 \
  sh validation/iterative/run_one_map_runtime.sh
```

`VERIFY_REFERENCE=1` requires the five outputs to match the published
same-input replay hashes. An in-tree build may omit the two `GANLIB_*`
overrides. This runner verifies one raw map when its independent runtime and
XSM checks pass. It does not qualify outer convergence.

The failed Stage-4 capture command is retained for provenance. It is not the
next calculation to repeat:

```sh
DRAGON_BIN=/absolute/path/to/Dragon \
GANLIB_LIB=/absolute/path/to/libGanlib.a \
GANLIB_MOD=/absolute/path/to/ganlib/modules \
SEED_DIR=/absolute/path/to/iterative-seed \
BASELINE_DIR=/absolute/path/to/iterative-map1 \
KEEP_WORK=1 \
  sh validation/iterative/run_inner_sensitivity.sh
```

The current frozen solver returns `STAGE4 INVALID` because its three radial
solves do not meet \(h/2\). Do not use the written `state1` files or launch a
longer `MAXOUT` continuation. The bounded numerical-floor diagnostic is
complete; see
[radial_floor_result.md](validation/iterative/radial_floor_result.md). Its
read-only binary32-step follow-up is
[radial_precision_result.md](validation/iterative/radial_precision_result.md);
it does not change the Stage-4 status.
