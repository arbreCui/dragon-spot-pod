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
src/SPOR64_B2H.f90                    fresh REAL64 projected-state boundary
src/SPOR64_B2I.f90                    archive-wide bootstrap lifecycle seal
src/SPOR64_B2J.f90                    archive-wide REAL64 projection commit
src/SPOR64_B2K.f90                    fresh radial SYSTEM archive commit
src/SPOR64_B2N.f90                    REAL64 frozen-fission source builder
src/SPOR64_B2O.f90                    source-selected same-index CONT sealer
src/SPOR64_B2R.f90                    label-bound RETURNED archive collector
src/SPOR64_B2S.f90                    default-off immediate three-plane bridge
src/SPOR64_B2T.f90                    owned PROJECTED-to-RETURNED host step
data/SpotAsmR64.c2m                   default-off three-plane ASM host
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

Phase-A9a owns the eight-slice `REAL64` state, consumes an already admitted
fixed fission source, forms each inner-sweep source as that fixed contribution
plus off-group scattering, and implements the A8 `DOORFV64` call,
`FLUBAL64`/`ALSBD`, `FLU2AC64`, the inner and outer norms, and the strict
terminal Boolean. It does not construct the outer `F phi/k` source. It adds no
relaxation, fit, clipping, floor or tolerance. It does not yet connect the
production parser or GANLIB archive, and therefore cannot establish a
continuous production lane or radial convergence. Those host and archive
lifetimes are reserved for Phase-A9b.

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

It originally added a one-pass `R64` selector that defaulted false on every
`FLUGPI` call and was independent of `MOCA`; B2g below later tightened that
selector to require an explicit `BOOT` or `CONT` mode. `FLUGPI` is
record-write-free and
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

B2g makes the previously implicit epoch choice explicit. `FLUGPI` now accepts
only `R64 BOOT` or `R64 CONT`; a bare `R64`, an unknown mode, a duplicate
selector, or a mode token without `R64` fails closed. The mode is reset to
OFF on every parser call and is never inferred from LCM contents. The shipped
`SpotPlaneR64` procedure says `R64 BOOT` explicitly and remains unselected by
all shipped top-level decks.

The seven-entry ownership split is unchanged. In `BOOT`, B2B accepts only a
legacy seed without `SPOT-R64` and performs the one documented binary32 to
binary64 promotion. In `CONT`, B2B refuses both compatibility payloads as
iteration inputs: it reads the initial iterate only from
`FLUX_OLD/SPOT-R64/FLUX` type 4 and the fixed fission source only from
`FSOURCE/SPOT-R64/QFISS` type 4. Missing, malformed or mixed-mode authority
fails before `XDRTA2` or the solver core; there is no presence-based mode
selection and no fallback to root `FLUX` or `DSOUR`.

`QFISS` and the published `FLUX/SPOT-R64/SOUR` have distinct ownership and
meaning. `QFISS` is the fixed fission contribution admitted at the start of a
radial solve; `SOUR` is the core's terminal inner-sweep total source, which
also contains off-group scattering. B2g verifies that B2C publishes a
synthetic terminal `SOUR` distinct from `QFISS` and never republishes `QFISS`
inside the output-flux authority.

The seconds-scale gate exercises the production parser and real B2B/B2C host
against deterministic stubs and real read-only XSM metadata. It proves that
10,360 deliberately added REAL64 low-bit witnesses survive the CONT ingress
while poisoned root type-2 mirrors are ignored:

```sh
sh validation/iterative/real64_phase_a9b_b2g_explicit_continuation/run_phase_a9b_b2g_explicit_continuation.sh
```

This is deliberately a host contract, not yet a continuous Picard result.
The present `SPOFSRC` still computes `F phi/k` through its legacy binary32
path and therefore cannot construct the required type-4 `QFISS`. No shipped
procedure selects `CONT`. A later suffixed REAL64 checker/lifecycle gate is
also required:
the legacy `SPOFCHK` reads type-2 compatibility records and cannot serve as
REAL64 convergence evidence. Radial and outer Picard convergence remain
`NOT-EVALUATED`.
See
[real64_phase_a9b_b2g_explicit_continuation/README.md](validation/iterative/real64_phase_a9b_b2g_explicit_continuation/README.md).

The post-B2g lifecycle audit found that source construction cannot safely be
the immediate next connection. Legacy `SPOPROJ` writes a new root type-2
plane `FLUX` but leaves the preceding radial result in
`SPOT-R64/FLUX`. A direct `CONT` would therefore ignore the current global
projection and use the stale type-4 radial state. Numerical correctness of
`F phi/k` would not repair that wrong Picard map.

B2h first closes the smaller projection-authority boundary:

```sh
make spot-real64-phase-a9b-b2h-projection
```

The new host-disconnected `SPOR64_B2H` module preserves the existing
fixed-space contraction order in REAL64 and publishes a fresh plane object
with explicit `SPOT-R64/STATE=PROJECTED`, caller-supplied positive finite
type-4 `RHO`, type-4 `FLUX`, and an incremented `EPOCH`. Region unknowns come
from the new REAL64 projection; non-region unknowns are retained only from the
preceding type-4 `SOLVED` state. The root type-2 flux is a compatibility
downcast written after the authority, while `SOUR`, `QFISS` and old
fixed-source diagnostics are not carried into the fresh object.

This module has no production caller. Current B2C does not yet publish
`SOLVED/EPOCH/RHO`, current `SPOPROJ` remains unchanged, and a per-plane helper
does not establish one atomic epoch across all planes. It also does not prove
that the supplied `RHO` and projected coordinates came from the same canonical
`SPOSTATE` object. The next lifecycle gate must bind that provenance and
connect the states archive-wide; only then may the REAL64 fission-source
builder consume `PROJECTED` and publish an epoch-matched `QFISS`. B2h therefore
does not execute `CONT` and does not establish radial or outer Picard
convergence. See
[real64_phase_a9b_b2h_projection_authority/README.md](validation/iterative/real64_phase_a9b_b2h_projection_authority/README.md).

B2i now establishes the missing archive-wide bootstrap lifecycle boundary:

```sh
make spot-real64-phase-a9b-b2i-bootstrap
```

`SPOR64_B2I` accepts one unsealed canonical `SPOSTATE` AX root, its axial
track, and a complete three-plane archive whose plane fluxes already contain
the exact B2C type-4 `{FLUX,SOUR}` authority. It derives `RHO` only from that
AX root, checks `RHO`, `K`, `L`, `H`, `GRAM`, `GERR`, plane volumes, list
indices and binary32 compatibility mirrors by exact identities, and copies
the complete four-list plane tuples into a fresh in-memory archive. No loose
basis, coefficient, epoch, plane pointer or empirical control enters the API.

Every copied plane is sealed `SOLVED/EPOCH=0` with the canonical type-4
`RHO`; the AX root and archive root are sealed `CLOSED/EPOCH=0`, and the
archive epoch is the final LCM mutation. Historical root transition
diagnostics are deliberately excluded from this new lifecycle schema because
they describe the preceding legacy transition. Admission rejection is
zero-write; an allocation/copy failure after publication begins is fail-closed
but not a rollback, so any pair without the final archive commit must be
discarded.

This phase checks structural closure only. It does not evaluate `B*A`, build
`QFISS`, call B2h, execute `CONT`, or solve transport; the B2h boundary remains
the sole owner of projection semantics. It also remains disconnected from all
shipped procedures, and epoch zero is a controlled data-flow label rather than
a globally unique persisted-state ID. Radial and outer Picard convergence are
still `NOT-EVALUATED`. See
[real64_phase_a9b_b2i_bootstrap_lifecycle/README.md](validation/iterative/real64_phase_a9b_b2i_bootstrap_lifecycle/README.md).

B2j now closes the next, strictly smaller transition:

```sh
make spot-real64-phase-a9b-b2j-projection
```

`SPOR64_B2J` consumes the controlled in-memory B2i pair
`AX CLOSED/0 + archive CLOSED/0 + planes SOLVED/0`.  It recovers `B`, `A`,
`RHO` and `L` only from the sealed AX root, evaluates all three planes with
the fixed binary64 contraction

```text
phi_hat[g,p,i] = sum_a real(B[g,i,a],binary64) * A[g,p,a],
```

and uses the real B2h publisher on three private roots.  Only after all three
planes pass does it create a fresh archive and commit
`PROJECTED/EPOCH=1`.  The AX object remains read-only `CLOSED/0`; projection
does not create a new axial solution.  The projected `RHO` remains the exact
parent `rho0`, not a prediction of `rho1`.

The output intentionally contains only `TRACK`, `MICROLIB2` and the three
fresh projected `FLUX` objects.  The old `SYSTEM` is lagged: it belongs to the
radial equation that produced `SOLVED/0`.  Copying it would permit the next
continuation solve to use the wrong leakage.  A subsequent lifecycle gate
must therefore rebuild fresh SYSTEM objects from the projected canonical
`SPOT-LEAK1D` before constructing QFISS or admitting `CONT`.  The retained
plane `LINK.SYSTEM='SYSTEM'` is only the name of that future fresh object;
there is deliberately no SYSTEM list in the B2j output.

This phase remains host-disconnected and is limited to the direct B2i-to-B2j
in-memory lifecycle; epoch zero is not a globally unique identifier for
mixing persisted roots.  It performs no ASM, QFISS construction, CONT,
transport solve or convergence test.  See
[real64_phase_a9b_b2j_archive_projection/README.md](validation/iterative/real64_phase_a9b_b2j_archive_projection/README.md).

B2k closes the fresh radial-system boundary without advancing the nonlinear
iteration:

```sh
make spot-real64-phase-a9b-b2k-system-assembly
```

The default-off `SpotAsmR64` host recovers each projected plane's library and
track, exposes the library locally as `MACRO0`, and calls the public production
operator exactly three times with `ASM: ... ARM LK1D 1/2/3`.  It does not call
`FLU`, `SPOFSRC` or `CONT`.  `SPOR64K:` is registered as the suffixed commit
operator, but no shipped calculation deck selects this candidate host.

`SPOR64_B2K` accepts only the exact `PROJECTED/1` root/lifecycle, the required
TRACK/MICROLIB structure with frozen TRACK/MCCG/MACROLIB state vectors, and
the exact projected-FLUX schema.  The host supplies three fresh ASM results;
the commit boundary requires three distinct, authority-free ASM-shaped SYSTEM
objects.  For every plane, group and material, it checks the actual binary32
evaluation order

```text
TX       = NTOT0 - TRANC
S0phys   = SIGW00 - TRANC
S0used   = S0phys - SPOT-LEAK1D
```

including the mixture-zero slot, and admits the exact frozen MCCG response
schema rather than constructing a reduced surrogate.  All three complete
SYSTEM objects are deep-copied to private stages before publication.  The
plane fluxes remain `PROJECTED/1`; the SYSTEM and archive authorities become
`ASSEMBLED/1`, with the archive epoch written last.  No relaxation, damping,
clipping, fitted coefficient or model completion is introduced.

The seconds-scale gate compiles the production path and validates its archive
transaction with independent synthetic SYSTEM candidates and frozen XSM
cross sections.  It deliberately does not run Dragon, ASM, the sequential
tracking file, transport or CONT.  Consequently real ASM execution, radial
convergence and outer Picard convergence remain `NOT-EVALUATED`; a separately
bounded real-ASM smoke test was still required at the B2k boundary and is now
provided by B2l below.  See
[real64_phase_a9b_b2k_system_assembly/README.md](validation/iterative/real64_phase_a9b_b2k_system_assembly/README.md).

B2l now executes the separately bounded real-ASM smoke required by B2k:

```sh
make spot-real64-phase-a9b-b2l-one-plane-real-asm
RUN_B2L=1 make spot-real64-phase-a9b-b2l-one-plane-real-asm
```

The first command is the default no-Dragon compile/contract gate.  It also
runs a bounded production-B2J lifecycle harness: six persistent XSM targets
are closed and reopened, with one exact `PROJECTED/1` commit and five strict
zero-commit rejections including a tombstone and plane-2/3 late failures.
This is storage/lifecycle evidence and runs no ASM or transport solve.  The
explicit activation materializes the complete real three-plane
`PROJECTED/1` archive, then runs exactly one production
`ASM: ... ARM LK1D 1` for plane 1.  B2J now admits either a fresh memory root
or a fresh persistent XSM root under the same empty-table contract, allowing
it to remain the final content-mutating owner instead of copying an archive
after its epoch commit.

The corrected accepted run completed one ASM in 0.973 s.  An independent GANLIB-only
posterior recursively compared 69,021 copied records, required all 59,940
response values to be finite, and reproduced 3,330 binary32 values in each of
`TX`, `S0phys`, and `S0used` bit for bit.  It found 35,518 nonzero response
values after treating both signed zeros as zero.  There was no `FLU`,
`SPOR64K`, `QFISS`, `CONT`, Picard map, empirical
coefficient, relaxation, damping, clipping, or model completion.

This proves only `REAL-ASM-PLANE1-EXECUTED` plus compatibility with the B2k
plane-1 formula/schema contract.  It does not validate response numerical
accuracy, planes 2/3, the three-plane commit, radial convergence, or outer
Picard convergence.  The XSM epoch is a logical completion marker, not an
ACID/crash-safe transaction.  Exact evidence and scope are in
[real64_phase_a9b_b2l_one_plane_real_asm/README.md](validation/iterative/real64_phase_a9b_b2l_one_plane_real_asm/README.md).

B2m closes the remaining three-plane operator-assembly boundary:

```sh
make spot-real64-phase-a9b-b2m-three-plane-real-asm-commit
RUN_B2M=1 make spot-real64-phase-a9b-b2m-three-plane-real-asm-commit
```

The default command runs 57 static, mutation, loader, and resource tests and
executes no Dragon process.  The explicit bounded activation copies the exact
`PROJECTED/1` XSM to an in-memory root, invokes the compiled `SpotAsmR64`
procedure once, performs production `ASM` for `LK1D 1/2/3`, and makes one
production `SPOR64K` in-memory `ASSEMBLED/1` logical commit.  Only after that
commit returns is the complete object copied once to a persistent XSM evidence
file; this is not claimed to be a direct-XSM or ACID transaction.

The accepted run used one Dragon process and completed the three ASM calls plus
the commit in 2.325 s.  A GANLIB-only posterior, repeated byte-identically,
validated all 179,820 finite response values, found 35,518 genuinely nonzero
values in each plane, checked 1,110 same-index leakage values, and reproduced
9,990 values in each of `TX`, `S0phys`, and `S0used` bit for bit.  There was no `FLU`, QFISS,
`CONT`, Picard map, empirical coefficient, relaxation, damping, clipping, or
model completion.

This establishes `REAL-ASM-PLANES1-3-EXECUTED`, the `SPOR64K`
`ASSEMBLED/1` logical commit, and B2k posterior compatibility.  It still does
not establish response-matrix numerical accuracy, a radial flux solution,
radial convergence, outer Picard convergence, or benchmark accuracy.  See
[real64_phase_a9b_b2m_three_plane_real_asm_commit/README.md](validation/iterative/real64_phase_a9b_b2m_three_plane_real_asm_commit/README.md).

B2n closes the next prerequisite without prematurely running `FLU`:

```sh
make spot-real64-phase-a9b-b2n-real64-frozen-qfiss
RUN_B2N=1 make spot-real64-phase-a9b-b2n-real64-frozen-qfiss
```

B2m's projected plane already carries type-4 `SPOT-R64/FLUX`, so it cannot
legitimately return through `R64 BOOT`.  The continuation route instead
requires a type-4 frozen `QFISS`, which the legacy binary32 `SPOFSRC` does not
provide.  B2n fills only that missing representation and lifecycle boundary.
It evaluates the unchanged frozen-fission formula in ordered binary64 from
plane 1's projected authority, creates a zero-live-fission `MACRO0`, and
publishes a same-plane, same-`RHO`, same-epoch
`FSOURCE/SPOT-R64/QFISS` authority plus a write-only compatibility mirror.

The default path performs no real source build.  Explicit activation uses a
standalone bounded builder and a twice-repeated GANLIB-only posterior; it
executes zero Dragon, ASM, FLU, transport, CONT, or Picard processes.  B2n
therefore proves only the REAL64 frozen-source bits and zero-live-fission
macrolib preparation.  A later gate must bind `RHO/STATE/EPOCH` at the
`R64 CONT` ingress and expose the inherited cutoff census before one real
radial solve is scientifically auditable.  See
[real64_phase_a9b_b2n_real64_frozen_qfiss/README.md](validation/iterative/real64_phase_a9b_b2n_real64_frozen_qfiss/README.md).

The accepted short activation used one materializer, one source builder, and
two byte-identical read-only posteriors.  It checked all 5,180 REAL64 source
values and all 94,720 zeroed fission values; `MACRO0` and `FSOURCE` were
9,878,532 and 625,560 bytes.  No radial solve or convergence test occurred.

B2o now closes the next read-only audit boundary:

```sh
make spot-real64-phase-a9b-b2o-cont-binding-cutoff
```

For `R64 CONT`, production B2B requires exact `PROJECTED/1`,
`FROZEN-QFIS/1`, and `ASSEMBLED/1` authorities before `XDRTA2` or the REAL64
core can be called.  Their positive binary64 `RHO` values must be bitwise
identical, their local epoch stage labels must all be 1, sealed seed/source
plane must equal the SYSTEM snapshot, and seed/SYSTEM leakage must match in
all 370 binary32 bit patterns.  Production `SPOR64_B2O` derives the plane from
the source and selects seed plus SYSTEM from the same ASSEMBLED archive index;
it accepts no independent caller plane or `RHO` scalar.  The public B2B ABI and BOOT numerical and
admission route are unchanged, although BOOT also gains the audit line.

The inherited ACA `1e-7` diagnostic is also exposed once by `FLU` as an
`INT64` count of reached local live-cutoff predicates that differ from their
exact-zero-cutoff counterfactuals.  It is neither a count of all guard
evaluations nor a full zero-cutoff rerun.  It does not enter physical,
acceptance, or convergence criteria; only fail-closed integer integrity checks
remain in A9.  The default B2o gate runs 25 mutation tests, 7 direct production
sealer calls (2 positives and 5 pre-publication rejections), and a short
stub-core harness with 32 pre-core rejections and an above-32-bit sentinel;
it executes no production `FLU`,
Dragon, transport, or Picard map.

`EPOCH=1` remains a local pipeline label, not a globally unique lineage ID,
and the B2C terminal authority still has no lifecycle metadata.  B2o therefore
proves one sealed same-index, predicate-satisfying CONT ingress—not repeated
CONT or convergence.  See
[real64_phase_a9b_b2o_cont_binding_cutoff/README.md](validation/iterative/real64_phase_a9b_b2o_cont_binding_cutoff/README.md).

B2p closes the accepted-CONT publication boundary without running a real
transport solve:

```sh
make spot-real64-phase-a9b-b2p-solved-lifecycle
```

After the existing B2B joint admission and an accepted A9 return, production
B2C now publishes the exact authority
`{RHO,PLANE,FLUX,SOUR,STATE=SOLVED,EPOCH}`. `RHO`, `PLANE`, and `EPOCH` are
copied from the sealed PROJECTED seed; B2C neither recomputes an eigenvalue nor
increments the generation. `EPOCH` is the last mutation. The existing B2H
per-plane authority boundary alone advances `SOLVED(n)` to `PROJECTED(n+1)`.
The old 16-argument B2C publisher and the BOOT route remain unchanged.

The short gate runs three real B2B control calls around configurable capture
stubs, including one accepted result and two rejected core results. It adds 16
fail-closed metadata cases, one alias rejection, one nonaccepted-token
rejection, 35 mutation tests, five full sealed-seed immutability sweeps, and a
caller compiled against the parent B2C module then linked against the current
wrapper. It checks all terminal and
projected type-4 values plus their compatibility mirrors and links no
production FLU, Dragon, or transport solver. Thus it proves the real
B2B-path publication `sealed PROJECTED(1) -> accepted SOLVED(1)` and separately
proves that existing B2H can consume the schema and perform its `1 -> 2`
mechanics. The synthetic B2H output is not a B2J/SPOD projection or canonical
next Picard state. There is no physical radial solve, second CONT call, or
outer Picard convergence result. B2q below establishes that B2H's omission of
`PLANE` and B2J's archive-member schema are intentional single-owner choices,
not blockers. The returned three-plane archive and subsequent axial closure
remain future work. See
[real64_phase_a9b_b2p_solved_lifecycle/README.md](validation/iterative/real64_phase_a9b_b2p_solved_lifecycle/README.md).

B2q freezes the lifecycle meaning of `RHO` before another return is wired:

```sh
make spot-real64-phase-a9b-b2q-lifecycle-rho-contract
```

For a canonical `CLOSED(n)` state, the root/AX `RHO` is
\(\rho_n=1/k_n\). The complete radial work generation produced from it carries
those same bits without recomputation:

```text
CLOSED(n), rho_n
  -> PROJECTED(n+1), rho_n
  -> ASSEMBLED(n+1), rho_n
  -> FROZEN-QFIS(n+1), rho_n
  -> SOLVED(n+1), rho_n.
```

The subsequent axial eigenproblem, not the radial solver, may produce a new
\(\rho_{n+1}\). A future `CLOSED(n+1)` root may therefore own
`RHO=rho_(n+1)` while its archived `SOLVED(n+1)` plane members retain the
radial-equation input `RHO=rho_n`. These are different scoped quantities;
the implementation must not force them equal with a tolerance, relaxation,
or empirical rule. Bootstrap `SOLVED/0` is the explicit initialization
exception: it is aligned with `CLOSED/0` and makes no claim about the unknown
historical radial-equation input.

This also resolves the apparent `PLANE` mismatch. An archive list index is
the sole plane identity for an archive-contained member; a detached
PROJECTED seed, SOLVED result, or FROZEN-QFIS source carries `PLANE` so its
index can be recovered, while a radial SYSTEM uses `SPOT-L1-SNAP`. There is
no physical reason to propagate a duplicate `PLANE` record through every
archive member.

The short B2q gate changes no production source and runs no production FLU,
ASM, Dragon, transport solve, or Picard map. It audits the current bitwise
`RHO` flow and executes the existing B2h distinction in which seed and caller
`RHO` deliberately differ. Direct B2h output is only a local projection
stage; canonical provenance requires B2j or a future archive-level gate.

The next implementation boundary is now precise. First, a returned-archive
collector accepts the three detached `SOLVED/1` results with the exact
`PLANE` set `{1,2,3}`, rejects duplicates, and binds each one to the
same-index `SYSTEM`, `TRACK`, `MICROLIB2`, and frozen `QFISS/K` provenance.
Terminal `SOUR` must not be substituted for `QFISS`. This collector does not
see `AX_NEXT` and does not commit `CLOSED/1`; it emits an unclosed archive for
`SPOASM FIXB`. Only after the axial eigenvalue solve, `SPOSTATE`, and
`SPOLEAK` may a separate close gate bind that archive to `AX_NEXT` and commit
`CLOSED/1`. See
[real64_phase_a9b_b2q_lifecycle_rho_contract/README.md](validation/iterative/real64_phase_a9b_b2q_lifecycle_rho_contract/README.md).

B2r implements that returned-archive collector without executing a solver:

```sh
make spot-real64-phase-a9b-b2r-returned-archive
```

It accepts one committed `ASSEMBLED/1` archive plus three detached
`SOLVED/1` and three detached `FROZEN-QFIS/1` objects. The two detached
triples must each carry the exact label set `PLANE={1,2,3}`; B2r binds by
those labels rather than argument order and rejects every duplicate,
omission, alias, schema mismatch, RHO/epoch mismatch, SYSTEM index/leakage
mismatch, key-map mismatch, K mismatch, or QFISS-mirror mismatch before its
first output write.

The output is `RETURNED/1`, not `CLOSED/1`. Its archive root has neither
`RHO` nor `SPOT-ITER-K`: the outer-state `rho_0/k_0` used by the radial
equations remain scoped to the children, and only a later axial solve plus
`SPOLEAK` may provide root `k_1`. Each archive-contained child retains
authoritative type-4 `FLUX`, terminal
`SOUR`, and frozen `QFISS`, drops detached `PLANE`, and receives only the
fixed-source compatibility records required by `SPOASM`. `SOUR` is never
substituted for `QFISS`.

This proves exact binding of the listed fields and recursive same-index
copying of the supplied committed objects. Because detached `SOLVED`
presently carries no sealed SYSTEM/QFISS lineage digest, B2r alone does not
prove their historical causal pairing; that stronger same-call statement is
the separate B2s `B2O -> B2B -> B2R` host boundary below. The short B2r gate
runs no ASM, SPOASM, FLU,
Dragon, transport, axial solve, or Picard map. See
[real64_phase_a9b_b2r_returned_archive/README.md](validation/iterative/real64_phase_a9b_b2r_returned_archive/README.md).

B2s closes that immediate in-process custody gap while remaining default-off:

```sh
make spot-real64-phase-a9b-b2s-immediate-host-bridge
```

Production `SPOR64_B2S` accepts no caller-produced `SOLVED`, plane, `RHO`,
eigenvalue, epoch, tolerance, or relaxation input. Unless its optional enable
flag is explicitly true, it returns before inspecting any object or creating
scratch storage. When enabled, it first seals all three source-selected B2O
pairs and requires the exact label set `{1,2,3}`. It then calls the existing
B2B CONT boundary in canonical plane order and accepts only three
`HOST_COMMITTED` results before immediately passing those still-live private
outputs to one B2R collection.

The short gate links the production B2O/B2B/B2C/B2R/B2S boundaries but
replaces only the radial core and `XDRTA2` with deterministic witnesses. It
therefore verifies the same-call control/data lifecycle, not a physical radial
transport execution or convergence. Detached `MACRO0` and `TRACK_f` history
also remains outside the object schema: B2s proves use of the supplied tuple,
not historical derivation of `MACRO0` from the archived `MICROLIB2` or file
identity of `TRACK_f`. No production call site is enabled by this phase.

B2t removes the remaining caller-supplied source pair from that immediate
path:

```sh
make spot-real64-phase-a9b-b2t-owned-source-host-step
```

Production `SPOR64_B2T` accepts one `PROJECTED/1` parent, three candidate
SYSTEM objects, and one shared `TRACK_f` handle. Unless explicitly enabled it
returns before any object access or subcall. When enabled, it privately calls
B2K once to create `ASSEMBLED/1`, calls B2N in canonical order to create all
three still-live `MACRO0/FROZEN-QFIS` pairs from the same PROJECTED parent,
and only then enters B2s. The caller can no longer substitute detached
ASSEMBLED, MACRO0, source, or SOLVED objects.

This is an ownership and lineage boundary, not a new equation or convergence
rule. It adds no empirical coefficient, relaxation, damping, clipping, or
retry. Candidate-SYSTEM history and the binary identity of `TRACK_f` remain
outside this low-level API; a later outer host must be default-off before its
three ASM calls, retain one read-only tracking-file handle through B2t, and
cryptographically bind that file to construction of the archived TRACK
objects. A before/after file hash proves unchanged tested bytes, not historical
identity on its own.

The B2t short gate runs the complete production ABI as a strict compile-only
check and executes production B2N for all three planes. An independent
GANLIB-only posterior checks the REAL64 QFISS construction and its exact
REAL32 projections twice. B2K/B2S are capture stubs in that content branch;
there is still no ASM, transport solve, Picard step, or enabled production host
call site.

The alternative three-return design is also checked without Dragon:

```sh
sh validation/iterative/run_picard_three_return_protocol_tests.sh
```

Passing this checker means only that the design remains protocol-only and
execution remains `NO-GO`; it is not a Picard result.
