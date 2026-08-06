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

Phase-A2 now adds an isolated full-matrix active-mask façade from the
Phase-A1 source to the exact post-STIS/pre-ACA raw-response boundary.  It
uses one typed REAL64 callback, enumerates all 31 nonempty masks over its
five-column synthetic fixture, rejects incomplete/nonfinite/illegal writes
atomically, and compile-time rejects REAL32 mutable state:

```sh
make spot-real64-phase-a2
```

The Phase-A2 callback is a signed-permutation test oracle, not a transport
model.  It executes no real `MCGFCF`, `MCGFFIR`, `MCGSCA`, `MCGFST`,
tracking-file, or ACA operation.

Phase-A3 now adds a compile-only checked legacy-ABI seam for the exact
frozen branch.  It encodes
`MCGFCF(MCGFFIR,MCGFFAR,MCGFFAL,MCGSCA,...)->MCGFST` with the real legacy
argument kinds, ranks, procedure identities, and call order:

```sh
make spot-real64-phase-a3
```

A deliberate unresolved link barrier keeps the Phase-A3 objects
non-linkable and non-executable.  Its gate therefore performs zero
Phase-A3 links, zero Phase-A3 executions, zero transport solves, and zero
Dragon runs.
It also records an existing legacy defect: `MCGFL1` passes
`XSIXYZ(1,IDIR)` with the frozen `IDIR=0`, which is a nonconforming actual
designator.  The validation seam uses a legal caller-owned `XSI` vector;
this does not repair or validate the production path.

Phase-A4 now closes that validation-only, compile-only host call shape from
the Phase-A2 façade into the Phase-A3 seam:

```sh
make spot-real64-phase-a4
```

Its caller-owned context storage schema is closed, but population from the
real host and cross-object provenance remain unbound.  The Phase-A4 objects
are linked zero times and executed zero times.  The recursive short gate
does link and execute the already-frozen Phase-A1 and Phase-A2 synthetic
programs once each; neither is a tracking or MOC calculation.  The whole
gate performs zero transport solves and zero Dragon runs.

The first four subgates remain outside the production call graph.  Phase-A4 does
not validate MOC behavior, ACA, rebalancing, acceleration, the full mutable
radial state, terminal norms, physical accuracy, solver convergence, or
Picard convergence.  Phase-A5 below adds only a static, host-shaped private
population path while preserving the unresolved link barrier and performing
no transport.  See
[real64_phase_a1/README.md](validation/iterative/real64_phase_a1/README.md)
and
[real64_phase_a2/README.md](validation/iterative/real64_phase_a2/README.md)
and
[real64_phase_a3/README.md](validation/iterative/real64_phase_a3/README.md)
and
[real64_phase_a4/README.md](validation/iterative/real64_phase_a4/README.md).

Phase-A5 now encodes the validation-only private population path for the
locked 2D isotropic host shape:

```sh
make spot-real64-phase-a5
```

It copies only the live host inputs and immediately consumes a local
Phase-A4 context.  `CAZ0`, `CPO`, and `XSI` receive canonical zero storage
only because the locked branch does not read those formal arguments;
`ISGNR` and `PJJIND` use their exact single-mode isotropic definitions.
None is a fitted or empirical coefficient.

Phase-A5 is still object-only and outside `src/`.  It does not prove the
tracking unit position, `KPSYS/PJJ$MCCG` contents or lifetime, `/EXP1/`
initialization, cross-object material/geometry identity, a production
REAL64 host state, or any solver convergence.  No A5 object is linked or
executed, and the Phase-A3 barrier remains unresolved.  See
[real64_phase_a5/README.md](validation/iterative/real64_phase_a5/README.md).

Phase-A6 now freezes the only admissible future `MCGFL1` rendezvous and a
default-off, validation-only host adapter:

```sh
make spot-real64-phase-a6
```

The ON arm is defined as a mutually exclusive replacement for the existing
`MCGFCF`-through-`MCGFST` response visit; it can never be an additional
tracking traversal.  Once selected, a failed admission cannot fall back to
the legacy arm.  This prevents both a second consumption of the sequential
tracking stream and a second STIS application.

The static host audit also records two current production blockers:
`MCGFL1` still receives borrowed REAL32 `QFR/PHIIN`, and it has only a
transient one-group `DRAGON-S0XSC` view rather than the complete ordered
`SC(0:M,1,NGEFF)` bundle required by A5.  Phase-A6 deliberately performs
neither a kind conversion nor an LCM gather, and it does not modify `src/`.
See
[real64_phase_a6/README.md](validation/iterative/real64_phase_a6/README.md).

Phase-A7 freezes the complete ownership and checked-interface blueprint:

```sh
make spot-real64-phase-a7
```

The unique mutable-state owner is the future `FLU2DR64` eight-slice
REAL64 array.  `QFR/PHIIN` are views or exact REAL64 tail copies of that
state, not new owners.  A separate future `MCCGF64` owns one complete,
ordered, read-only REAL32 `DRAGON-S0XSC` bundle.  The blueprint permits one
entry promotion, no mutable-state REAL32 round trip, and one type-2
compatibility mirror only after the strict terminal decision.
An independent local `R64` keyword, parsed once and defaulting OFF,
selects the lane without coupling it to `MOCA`.  The first lane admits
only the frozen `FSOURCE/DSOUR` source with finite zero `NUSIGF`, so it
does not read `CHI` or invent a fission term.  `FLU2DR64` also owns one
validated immutable `OFFGROUP32` bundle shared with `FLUBAL64`, and calls
the unchanged `XDRTA2` initialization exactly once.
It also freezes explicit `KEYFLX/PJJIND` ranks, active `CF(LC)`,
`IM(NLONG+1)` in `MCGPRA64`, REAL64-only diagnostics through `PRINDM`,
and a no-downcast `SPOMOC_CAPTURE64` audit interface.  Publication and
host writes use layered child/driver/host success gates; no listed record
changes before strict acceptance, and no rollback claim is made after
accepted writes begin.  Before the first accepted write, a machine-only
preflight requires finite type-4 values and compatibility values within
the finite REAL32 range; it adds no convergence threshold.

Phase-A7 contains no production Fortran and performs no Fortran
compilation, tracking read, transport application, or Dragon run.  It
separates the next implementation into an inner compile-only A8 closure
and an outer-owner A9 closure; neither runtime provenance nor convergence
has been evaluated.  See
[real64_phase_a7/README.md](validation/iterative/real64_phase_a7/README.md).

The implemented Phase-A1 through A6 gates and the A7 design gate remain
static evidence, not a continuous REAL64 radial lane or a convergence
result.

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
    norms (protocol frozen; Phase-A1 source arithmetic and the Phase-A2
    typed post-STIS/pre-ACA façade implemented; Phase-A3 legacy-ABI seam and
    Phase-A4 compile-only A2-to-A3 host closure implemented; Phase-A5-A7
    host context, rendezvous and ownership contracts frozen; Phase-A8 inner
    suffixed REAL64 closure implemented and compile-checked; Phase-A9a owns
    the outer REAL64 core, B2b connects its default-off source route,
    B2c closes accepted-only publication, B2d closes the production link,
    B2e identifies the two real-input ownership blockers, and B2f closes the
    default-off fresh-output/read-only-seed bootstrap with real XSM inputs
    and a deterministic test core; runtime provenance, REAL64 continuation
    and actual MOC remain open);
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
validation/iterative/real64_phase_a8/
                                      compile-only inner REAL64 closure
validation/iterative/real64_phase_a9/
                                      compile-only outer REAL64 math closure
validation/iterative/real64_phase_a9b_promotion/
                                      byte-identical production promotion
validation/iterative/real64_phase_a9b_b2d_link/
                                      production-link closure, no Dragon run
validation/iterative/real64_phase_a9b_b2e_plane1_admission/
                                      real-input admission census, zero solve
validation/iterative/real64_phase_a9b_b2f_fresh_host/
                                      fresh-output bootstrap host, zero solve
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

The implemented inner suffixed closure has its own isolated short gate:

```sh
make spot-real64-phase-a8
```

It compiles relocatable objects and checks exact symbol inventories and
negative ABI fixtures. It does not link or execute those objects, read a
tracking file, solve transport, run Dragon, or establish convergence.

The next outer step is intentionally split. Its first, mathematical subgate
is short and compile-only:

```sh
make spot-real64-phase-a9a
```

Phase-A9a owns the eight-slice `REAL64` state and implements frozen-source
construction, the A8 `DOORFV64` call, `FLUBAL64`/`ALSBD`, `FLU2AC64`, the
inner and outer norms, and the strict terminal Boolean. It adds no relaxation,
fit, clipping, floor or tolerance. It does not yet connect the production
parser or GANLIB archive, and therefore cannot establish a continuous
production lane or radial convergence. Those host and archive lifetimes are
reserved for Phase-A9b.

Before the host is allowed to select that lane, the frozen numerical modules
are promoted byte-for-byte into `src/` under a separate short gate:

```sh
make spot-real64-phase-a9b-promotion
```

This gate establishes only that the same A8/A9 module sources are available
to the production build and compile with the expected dependency and symbol
boundaries. It does not edit `FLUGPI`, `FLU`, `FLUDRV`, `FLU2DR`, `SPOMOC`,
`XDRTA2` or `src/Makefile`; it adds no selector or dispatch call site to any
existing host routine, performs no archive write and does not link or execute
the objects. The default route is therefore still unchanged. Host selection,
read-only admission and accepted-only publication form the next A9b subgate.

The next short subgate closes only the four promoted A8 calls into SPOMOC:

```sh
make spot-real64-phase-a9b-spomoc-abi
```

It adds four ordinary-external forwarding symbols and a direct
`REAL(real64)` `SPOMOC_CAPTURE64` diagnostic body. The legacy capture is
unchanged, and the bridge routines themselves have no arithmetic, solver
control or direct GANLIB access.
This is `A8-SPOMOC-EXTERNAL-SYMBOLS-DEFINED-COMPILE-ONLY`: it still does not
expose `R64`, implement `SPOMOC_BEGIN64`, connect a production route, link or
execute the objects. `PRODUCTION-ROUTE-CONNECTED=false`,
`CONTINUOUS-REAL64-LANE=false`, `RADIAL-CONVERGENCE=NOT-EVALUATED`, and
`OUTER-PICARD-CONVERGENCE=NOT-EVALUATED` remain authoritative. The selector
must wait until all public writes that currently precede admission have been
deferred.

That first host subgate is now implemented as B2a:

```sh
make spot-real64-phase-a9b-b2a-selector
```

It adds a bare, one-pass `R64` keyword that defaults false on every `FLUGPI`
call and is independent of `MOCA`. `FLUGPI` is now record-write-free and
returns an explicit logical `LIMERG` staging flag; `FLU` publishes the legacy
`SIGNATURE`, `LINK.*` and final `IMERGE-LEAK` records only after it knows the
legacy OFF route was selected. An R64-selected visit instead aborts and
returns before any output-record write, `XDRTA2`, `FLUGPT` or `FLUDRV`, and
`FLUDRV` has the same defensive no-fallback entry guard.

The short gate compiles the production host objects without linking them and
runs the real production parser against a synthetic read-only GANLIB surface.
It does not connect the REAL64 route or execute a solver. Therefore
`PRODUCTION-ROUTE-CONNECTED=false`, `CONTINUOUS-REAL64-LANE=false`,
`RADIAL-CONVERGENCE=NOT-EVALUATED`, and
`OUTER-PICARD-CONVERGENCE=NOT-EVALUATED` remain authoritative. B2b is the next
step: strict read-only live-topology admission, one exact zero-argument
`XDRTA2` epoch, and a no-publication rendezvous with the REAL64 core.

B2b now implements that source-level rendezvous behind the same default-OFF
`R64` selector:

```sh
make spot-real64-phase-a9b-b2b-ingress
```

The selected arm admits only the frozen six-entry topology: `FLUX`, `MACRO0`,
`TRACK`, `TRACK_f`, `SYSTEM` and `FSOURCE`.  Every LCM payload used by the ingress is
preceded by an exact length/type check; initial flux and frozen source are
promoted once from their stored binary32 values; geometry, material, source
and off-group identities are checked without fitting or correction.  Only
after this read-only admission does the arm initialize the unchanged
tabulated-exponential operator with one zero-argument `XDRTA2` call and meet
the production `FLU2DR64_CORE`.  It can never return to `FLUDRV` or the legacy
REAL32 route.

B2b deliberately has no scientific publication.  The terminal REAL64 arrays
remain private to the ingress, and even a strictly accepted core return ends
as `ACCEPTED_UNPUBLISHED`.  The short gate compiles the production connection
and exercises only synthetic dispatch/ABI checks; it does not call the real
core, read tracking, solve transport or run Dragon.  Thus
`PRODUCTION-R64-SOURCE-ROUTE-CONNECTED=true`, while
`CONTINUOUS-REAL64-LANE=false`, `RADIAL-CONVERGENCE=NOT-EVALUATED`, and
`OUTER-PICARD-CONVERGENCE=NOT-EVALUATED` remain authoritative.  The shipped
`SpotPlaneFS` procedure still contains no `R64` opt-in and creates a new flux
object, so its default scientific path is unchanged.  Accepted-only archive
and host publication belong to B2c.

This is a local B2b ABI claim, not a repository-wide `XDRTA2` cleanup:
`FLU`, `SPOR64_B2B` and the zero-argument procedure declaration agree, while
the pre-existing `src/ASM.f:101` actual-argument call remains explicitly
outside this subgate.  Consequently `GLOBAL-XDRTA2-ABI-CLEAN=false` is part of
the frozen receipt rather than being hidden by the compile-only result.

B2c closes the accepted-result publication boundary without changing the
solver equations or terminal Boolean:

```sh
make spot-real64-phase-a9b-b2c-publication
```

The accepted terminal arrays are published during the same synchronous B2b
ingress call in which they are owned. A complete no-write preflight first
checks the exact acceptance token, IEEE finiteness, binary32 representability,
the frozen `B0` option and the single-epoch collision policy. Publication is
then ordered as three status phases: the child-payload phase writes type-4
`SPOT-R64/FLUX,SOUR` scientific authority followed by one write-only binary32
staging pass into the legacy type-2 `FLUX,SOUR` compatibility mirror
(`status=6`); the driver-metadata phase commits `status=7`; and the host
links/cache phase commits `status=8`. Only the final `HOST_COMMITTED` status
may return normally from the selected arm.
There is no relaxation, clipping, fitted coefficient, fallback to `FLUDRV`,
completion marker or rollback claim.

This first publisher is intentionally single-epoch: an existing `SPOT-R64`,
root `SOUR`, `AFLUX`, `DFLUX` or `ADFLUX` causes a zero-write failure instead
of silently overwriting another result. On the integrated route, B2B rejects a
pre-existing collision as admission `status=1` before the core; B2C repeats
the no-write preflight at publication time. Any failure there returns
`status=5`, including a last-moment collision/schema drift, invalid terminal
representation or staging-allocation failure. A future online Picard route
that wants to reuse one object must define an explicit epoch protocol; B2c
does not guess that policy.

The B2c gate is seconds-scale and uses compile/static, mutation and synthetic
publication checks only. It does not run the production core, read tracking,
solve transport or run Dragon. Therefore B2c establishes the source-level
accepted publication path, but runtime provenance and the continuously
executed REAL64 lane remain unvalidated; radial convergence and outer Picard
convergence remain `NOT-EVALUATED`. The shipped `SpotPlaneFS` procedure still
does not opt into `R64`.

B2d then closes the narrow GANLIB ABI seam required to link the complete
production Dragon executable. The gate links Dragon once but never executes
it, and it performs no tracking read or transport solve. Its exact boundary
is recorded in
[real64_phase_a9b_b2d_link/README.md](validation/iterative/real64_phase_a9b_b2d_link/README.md).

B2e was the last blocked-input census. A read-only census of the frozen plane-1
objects and three direct calls to the real B2b ingress establish that the
then-current host could not enter the REAL64 solver. The exact recovered flux is
first rejected by its legacy root `SOUR` list. After deleting only that list
from a temporary clone, the next incompatible guard is
`MACRO0/STATE-VECTOR(3)=3`, while B2b then required one stored Legendre
component. The real MCCG track nevertheless activates only one flux Legendre
component, so the legacy solve uses only order zero; the stored P1/P2 arrays
are finite and nonzero and are not discarded or reinterpreted.

The shipped plane procedure also creates a fresh `FLUX`, implying
`REC=false, LIMERG=true`, but B2b then required a recovered object and
reads its initial state from that same output. The validation-only candidate
therefore uses a fresh publication target plus a distinct, read-only
`FLUX_OLD` seed. It has not been registered or executed. The B2e gate takes
seconds and executes no Dragon, `XDRTA2`, production core, publisher,
tracking record or transport solve:

```sh
sh validation/iterative/real64_phase_a9b_b2e_plane1_admission/run_phase_a9b_b2e_plane1_admission.sh
```

That result defines the B2f ownership split. See
[real64_phase_a9b_b2e_plane1_admission/README.md](validation/iterative/real64_phase_a9b_b2e_plane1_admission/README.md).

B2f now implements and validates the explicit seven-entry bootstrap:
`FLUX` is a fresh, empty, write-only target; `FLUX_OLD` is the distinct
read-only initial-flux seed; and `MACRO0`, `TRACK`, `TRACK_f`, `SYSTEM` and
`FSOURCE` retain their existing read-only roles. The suffixed procedures
`SpotPlaneR64` and `SpotRefR64` expose this path, while the unchanged
`SpotPlaneFS`/`SpotRefFS` path remains the default and no shipped top-level
deck selects `SpotRefR64`.

The real macrolib stores P0, P1 and P2, but the real track activates only P0.
B2f therefore verifies the stored P1/P2 shapes and loads only the same P0
records used by the active legacy solve; it deletes, zeros and models none of
the inactive data. Initial flux is promoted only from `FLUX_OLD/FLUX`, and
the fixed source only from `FSOURCE/DSOUR`. The fresh publisher writes the
complete type-4 authority, type-2 compatibility mirror and `L_FLUX` metadata.

The seconds-scale gate links the real B2B ingress and B2C publisher to a
deterministic copy oracle. It opens five frozen XSM objects read-only, covers
one successful publication, six blocked ingress cases and seven publisher
preflight rejections (including empty daughter-table targets), and performs
no Dragon run, production `XDRTA2`, real
core call, sequential tracking-record read or transport solve:

```sh
sh validation/iterative/real64_phase_a9b_b2f_fresh_host/run_phase_a9b_b2f_fresh_host.sh
```

This proves the first fresh-output REAL64 bootstrap contract only. A seed
already carrying `SPOT-R64` is rejected deliberately, so no hidden
REAL64-to-REAL32-to-REAL64 Picard continuation is claimed. The next gate must
assign explicit ownership to the previous type-4 state before any bounded
production plane execution. Radial and outer Picard convergence remain
`NOT-EVALUATED`. See
[real64_phase_a9b_b2f_fresh_host/README.md](validation/iterative/real64_phase_a9b_b2f_fresh_host/README.md).

The alternative three-return design is also checked without Dragon:

```sh
sh validation/iterative/run_picard_three_return_protocol_tests.sh
```

Passing this checker means only that the design remains protocol-only and
execution remains `NO-GO`; it is not a Picard result.
