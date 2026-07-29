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
the original \(h\)-to-\(h/2\) Stage 4 remains `INVALID` and Stage 5 remains
`NOT-AUTHORIZED`. Exact values,
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
those records without misidentifying the preconditioner as physics.

The default-off same-sweep capture is now implemented. It records the
evaluated state, `QFR`, source-element vector and raw MOC response from the
first primary GMRES evaluation before ACA/SCR. It writes only to the fresh
`L_FLUX` audit directory; the instrumentation adds zero operator applications
and has no acceptance threshold. A bounded NATIVE/STATIONARY × OFF/ON replay
has now passed its independent log and Ganlib-only XSM checks. The scalar RAW
minus EVAL diagnostics are

\[
\begin{array}{c|cc}
 & D_{V,2} & D_{\max,\mathrm{input}}\\ \hline
\mathrm{NATIVE} & 5.7461264\times10^{-7} & 2.1306357\times10^{-6}\\
\mathrm{STATIONARY} & 5.7815536\times10^{-7} & 2.1902923\times10^{-6}
\end{array}
\]

These values classify the capture ledger, not an equation residual, transport
error, convergence gate or arm ranking. See
[radial_precision_result.md](validation/iterative/radial_precision_result.md)
and [raw_moc_capture_result.md](validation/iterative/raw_moc_capture_result.md).

The subsequent ULP bridge census is also complete and required no new Dragon
process, transport solve or operator application. For each of the 2960
positive finite scalar coordinates in each arm, `RAW-BRIDGE` compares one
IEEE binary64-to-binary32 round-to-nearest-even projection of the captured
RAW response with EVAL, while `PRODUCTION-STEP` compares the stored PRE and
OFF states:

\[
\begin{array}{c|c|rrrrr}
\text{arm} & \text{ledger} & \text{unchanged} & \text{up} & \text{down}
& \text{adjacent} & \max |{\rm steps}|\\ \hline
\text{NATIVE} & \text{RAW-BRIDGE} & 135 & 977 & 1848 & 248 & 877\\
\text{NATIVE} & \text{PRODUCTION-STEP} & 288 & 136 & 2536 & 265 & 17\\
\text{STATIONARY} & \text{RAW-BRIDGE} & 133 & 975 & 1852 & 251 & 878\\
\text{STATIONARY} & \text{PRODUCTION-STEP} & 272 & 88 & 2600 & 220 & 12
\end{array}
\]

There is no acceptance threshold or empirical parameter. The two ledgers
have different endpoints and must not be subtracted. No part of the
production step is attributed to binary32 rounding, GMRES, ACA, SCR,
rebalancing or acceleration; the census does not rank the two arms or
establish a residual, error bound, convergence or Stage-4/Stage-5
qualification. Its exact counts and evidence boundary are in
[raw_moc_ulp_bridge_result.md](validation/iterative/raw_moc_ulp_bridge_result.md).
It motivates only planning a minimal, default-off REAL64 radial
working-iteration experiment with the physical equation and frozen controls
unchanged; it does not predict that experiment will converge.

A subsequent passive control-flow census has now resolved where that
experiment must not be placed. In one frozen STATIONARY map, `MCGMRE`
entered and returned normally, and its PRIMARY MOC evaluation ran once for
all 370 active groups. The residual test immediately after the completed
PRIMARY evaluation then removed every group before the affine-RHS, Krylov
and correction sections:

```text
PRIMARY calls / active groups     1 / 370
AFFINE-RHS calls                  0
KRYLOV calls                      0
correction blocks / group-blocks 0 / 0
classification                   VALID-GMRES-UPDATE-INACTIVE
```

There are no per-group `KMAX` rows; in particular, this is not a census of
370 zero values. OFF reproduced the legacy XSM, the two ON runs reproduced
one another byte for byte, and the independent reader and artifact checker
closed all hashes and raw ledger identities. This proves only that a GMRES
correction-accumulation precision A/B would be empty for this locked path.
It neither explains the earlier nontermination nor establishes convergence.
The exact evidence and interpretation limits are in
[gmres_activity_result.md](validation/iterative/gmres_activity_result.md).

That census closes the local floating-point forensics. The existing RAW-MOC
capture is already a same-point primary-MOC defect at the plane-1
six-update arm terminals derived from the cap-500 restart, so another
terminal sweep there would repeat the same observable. A continuous
REAL64 experiment capable of addressing the failed \(h/2\) condition would
have to begin at the binary32 `FLU2DR` state and propagate through the full
radial solver; changing only `MCGFCS`, `MCGMRE` or `MCGFLX` would not test
that boundary.

Stage 4 was therefore amended without changing its failed history.  The
single authorized \(2h\)-to-\(h\) capture subsequently completed with strict
termination in all three radial solves and the returned axial solve.
\(R_\rho\), \(R_L\), and \(D_L\) were resolved, but \(R_a\) was not:

\[
D_{\mathrm{in},a}=2.2871261661792861\times10^{-5}
>
D_{\mathrm{out},2h,a}=2.2557116628569681\times10^{-5}.
\]

The result is permanently `UNRESOLVED`; replay and Picard remain
unauthorized.  The offline Gram-metric decomposition then showed that the
tolerance-induced axial change is almost antiparallel to the coarse update,
so the small fine-map update is a cancellation of two larger vectors.  This
explains the failed gate but does not identify a plane/group cause or
invalidate the SPOD equations.  See
[inner_sensitivity_v2_result.md](validation/iterative/inner_sensitivity_v2_result.md)
and
[inner_sensitivity_v2_ra_geometry_result.md](validation/iterative/inner_sensitivity_v2_ra_geometry_result.md).

The next route is now frozen as a default-off, continuous REAL64 radial
working lane for the exact `TYPE S + MCCG` branch.  The current freeze
authorizes only implementation, compilation, static precision closure, and
synthetic tests—no Dragon process.  A later single-plane feasibility
experiment must be separately authorized before any full Stage-4 restart.
The route and its no-empirical-parameter boundary are in
[radial_real64_route.md](validation/iterative/radial_real64_route.md) and
[radial_real64_route_protocol.json](validation/iterative/radial_real64_route_protocol.json).

Phase-A1 of that route is now implemented as an isolated validation-tree
slice.  It closes only the locked `MCGFCS` REAL64 source arithmetic and its
explicit entry/terminal conversion boundaries.  A strict compile,
sub-binary32-ULP probe, wrong-kind compile-fail test, link-isolation check,
and manifest mutation suite pass with zero Dragon runs:

```sh
make spot-real64-phase-a1
```

The production route is still untouched.  `MCGFL1`, the primary MOC
response, ACA, rebalancing, acceleration, the full mutable radial state,
and terminal norms remain open.  Consequently this is
`IMPLEMENTED-PARTIAL-SLICE-ONLY`, not a continuous REAL64 lane and not a
solver- or Picard-convergence result.  See
[real64_phase_a1/README.md](validation/iterative/real64_phase_a1/README.md).

A possible three-return legacy-binary32 Picard diagnostic was then examined
as a smaller alternative.  It is not currently executable: three returns are
a Picard trajectory regardless of whether they are called a census, and the
frozen `UNRESOLVED` branch forbids that trajectory.  Only its mathematical
design has been frozen, with `Dragon processes = 0`, in
[picard_three_return.md](validation/iterative/picard_three_return.md) and
[picard_three_return_protocol.json](validation/iterative/picard_three_return_protocol.json).

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
   and no acceptance threshold (completed and independently replayed);
7. round the retained RAW scalar tuples once to binary32 and publish an exact
   ULP bridge census without a new transport solve or attribution claim
   (completed);
8. passively census the existing GMRES control flow and reject an empty
   correction-accumulation precision experiment (completed);
9. retain the `MCGFCS` precision replay only as an optional implementation
   unit test, not a scientific gate; reject a partial REAL64 solver fork and
   freeze the unique attainable \(2h\)-to-\(h\) Stage-4 comparison
   (completed without transport);
10. evaluate the one coarse map under a strict process time bound
    (completed; `UNRESOLVED` in \(R_a\), so replay was forbidden);
11. decompose the frozen \(R_a\) geometry offline without changing the
    classification (completed);
12. freeze and statically close a default-off continuous REAL64 radial
    working lane, including ACA, rebalancing, acceleration, and terminal
    norms (protocol frozen; Phase-A1 source slice implemented, full static
    closure incomplete);
13. examine a fixed three-return legacy32 descriptive diagnostic as a
    smaller alternative (design frozen, but execution is `NO-GO` under the
    current Stage-4 result);
14. only after a separately authorized single-plane REAL64 feasibility pass
    and replay, restart Stage 4 with both \(h\) and \(h/2\) maps recomputed in
    the same lane;
15. only after Stage 4 passes study direct Picard convergence;
16. after convergence, repeat rank/mesh/angle refinement and independent 3D
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
src/SPOMOC.f90                        default-off raw primary-MOC capture
validation/iterative/                 active iterative contracts and fixtures
validation/iterative/check_radial_precision_xsm.f90
                                      exact stored binary32-step audit
validation/iterative/raw_moc_residual_protocol.json
                                      same-sweep diagnostic definition
validation/iterative/radial_real64_route_protocol.json
                                      static-only full working-lane contract
validation/iterative/picard_three_return_protocol.json
                                      no-run three-return design contract
validation/iterative/raw_moc_capture_run_protocol.json
                                      frozen four-probe production protocol
validation/iterative/run_raw_moc_capture_production.sh
                                      preflight and bounded production runner
validation/iterative/raw_moc_capture_result.md
                                      captured ledger result and limits
validation/iterative/check_raw_moc_capture_result.py
                                      public plus local-artifact replay
validation/iterative/raw_moc_ulp_bridge_protocol.json
                                      frozen offline ULP census definition
validation/iterative/raw_moc_ulp_bridge_result.md
                                      exact census and interpretation limits
validation/iterative/check_raw_moc_ulp_bridge_result.py
                                      public plus local-artifact replay
validation/iterative/gmres_activity_result.md
                                      exact passive activity result and limits
validation/iterative/check_gmres_activity_result.py
                                      public plus local-artifact replay
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

The original \(h\)-to-\(h/2\) capture returned `STAGE4 INVALID` because its
three radial solves did not meet \(h/2\). Do not use those written `state1`
files or launch a longer `MAXOUT` continuation. The bounded numerical-floor
diagnostic is complete; see
[radial_floor_result.md](validation/iterative/radial_floor_result.md). Its
read-only binary32-step follow-up is
[radial_precision_result.md](validation/iterative/radial_precision_result.md);
it does not change the Stage-4 status.

The raw-MOC production runner is deliberately inactive by default:

```sh
sh validation/iterative/run_raw_moc_capture_production.sh
```

That command performs identity, contract, unit-test, compiler and deck-render
preflight only. An explicit `RUN_CAPTURE=1` launches the one no-transport
preparation process and four bounded one-step probes. The corrected replay is
complete; verify its retained evidence with

```sh
python3 validation/iterative/check_raw_moc_capture_result.py
```

This `CAPTURE-VALID` result does not change the outer-convergence or Stage-4
status.

The published offline ULP census can be checked without the ignored local
artifact and without Dragon:

```sh
python3 validation/iterative/check_raw_moc_ulp_bridge_contract.py
python3 validation/iterative/check_raw_moc_ulp_bridge_result.py --public-only
```

Passing these checks certifies the declared census and its tracked evidence,
not causal attribution, arm ranking, convergence or Stage-4/Stage-5
qualification.

The current next-step contract is checked without Dragon by

```sh
sh validation/iterative/run_radial_real64_route_tests.sh
```

It rejects an incomplete precision path, any new empirical parameter, any
claim that archived ACA/PJJ data form the transport operator, and any
premature run authorization.

The alternative three-return design is also checked without Dragon:

```sh
sh validation/iterative/run_picard_three_return_protocol_tests.sh
```

Passing this checker means only that the design remains protocol-only and
execution remains `NO-GO`; it is not a Picard result.
