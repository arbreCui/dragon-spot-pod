# Iterative SPOT validation

This directory contains the validation path for
`SPOT_doc/rederivation.md`. It starts from a clean qualification boundary.

## Implementation subgates

The labels 0A/0B/0C below are implementation subgates. They are not the
formal Stage numbers in `SPOT_doc/validation_plan.md`.

Stage 0A freezes the online radial source identity:

\[
q_{\rm FS}=F(Ba)/k+S_{\rm off}(u_\perp).
\]

The fixed fission source is stored on every refreshed radial flux object.
`SPOASM` uses that record for fixed-source snapshots and retains its
final-state eigenvalue source only for offline eigenvalue snapshots. Mixed
snapshot types fail closed.

Run the zero/short-compute check with

```sh
sh validation/iterative/run_stage0a.sh
```

Stage 0B adds the fixed-basis assembly contract:

```text
SYSTEM0 := ASM: MACROLIB3 TRACK_AX SNAP ::
  SPOD rank ;

SYSTEM1 := ASM: MACROLIB3 TRACK_AX SNAP BASIS_REF ::
  SPOD rank FIXB ;
```

`FIXB` copies only the validated POD package from the distinct read-only
`BASIS_REF`; material data and `RADIAL-OP` are rebuilt from the current
snapshot state. Run its static gate with

```sh
sh validation/iterative/run_stage0b.sh
```

The no-transport runtime fixture builds the basis once, enters `FIXB`, and an
independent Ganlib-only checker compares all 370 groups. `VOL2D`, POD basis,
coefficients, singular values, reconstruction/orthogonality records and the
same-snapshot `RADIAL-OP` are bit identical.

Stage 0C defines the canonical physical state variables and raw state
difference:

```text
AXFLUX := SPOSTATE: AXFLUX TRACK_AX SYSTEM_AX MACROLIB3 :: ;
CURRENT := SPOXCONV: CURRENT PREVIOUS :: ;
```

`SPOSTATE` uses one global nu-fission-production normalization, reproduces the
production binary32 plane restriction, solves the stored-basis Gram system,
and reconstructs leakage from face currents. Explicit `SPOPROJ FIXB`
reconstructs the next feedback from \(Ba\); its measured raw off-space
component is diagnostic and is not a hidden map input. `SPOXCONV` rejects a
changed basis bit and reports \(R_\rho\), \(R_L\), absolute \(\Delta L\), and
\(R_a\) separately.

Run the source and manufactured-algebra gate with

```sh
sh validation/iterative/run_stage0c.sh
```

Run all three no-transport executable paths with a Dragon binary built from
the current sources:

```sh
DRAGON_BIN=/absolute/path/to/Dragon \
  sh validation/iterative/run_stage0_runtime.sh
```

The runner verifies the six-file seed against `seed.sha256`, then makes fresh
byte-copies before adding state records. The two stored axial fields exercise
only the residual plumbing; their difference is not claimed to be a
fixed-space map defect.

## One corrected map

`one_corrected_map.x2m` freezes exactly one initializer and one evaluation

\[
x_1=G(x_0).
\]

The evaluated map contains three online radial fixed-source solves, one axial
eigenvalue solve, direct leakage feedback, fixed-basis response assembly and
the raw defect at \(x_0\). It contains no loop or relaxation. Its static
contract is below. The complete deck additionally performs the one archived
initializer axial solve, so the bounded runner executes two axial plus three
radial solves in total.

```sh
python3 validation/iterative/check_one_map_contract.py
```

The bounded runtime gate is

```sh
DRAGON_BIN=/absolute/path/to/Dragon \
GANLIB_LIB=/absolute/path/to/libGanlib.a \
GANLIB_MOD=/absolute/path/to/ganlib/modules \
SEED_DIR=/absolute/path/to/iterative-seed \
VERIFY_REFERENCE=1 \
  sh validation/iterative/run_one_map_runtime.sh
```

`VERIFY_REFERENCE=1` requires the five scientific XSM files to match
`one_map_scientific.sha256`. With an in-tree build, the two `GANLIB_*`
overrides may be omitted.

It verifies the frozen input hashes, runs one initializer plus exactly one
map, checks all five terminal records in that complete deck, and invokes two
independent postprocessors:

- `check_one_map_runtime.py` checks execution structure and declared solver
  termination without assigning an outer threshold;
- `check_one_map_xsm.f90` links only Ganlib, checks the fixed POD package,
  requires a live radial-operator change, and independently recomputes the
  three outer residuals plus \(D_L=\|L^+-L\|_\infty\) bit for bit. It also
  verifies the three-plane restart leakage time ordering.

The first calculation and one fresh replay pass. Their five scientific XSM
containers are byte identical. The frozen controls and evidence boundary are
in `one_map_protocol.json`; exact values and hashes are in
`one_map_result.md`.

This is one deterministic point evaluation of \(G\), not a convergence
claim. The systematic inner-tolerance sensitivity from the same \(x_0\) was
attempted next and failed its strict radial inner-solver gate. A second outer
return and any long Picard trajectory remain unauthorized.

## Inner-tolerance sensitivity

`inner_sensitivity_map.x2m` preserves the Stage-3 initializer tolerance
\(h=\mathtt{0x350637bd}\) and uses the exact binary32 half
\(h/2=\mathtt{0x348637bd}\) only for the three radial and one returned axial
solve in \(G\). `check_inner_sensitivity_contract.py` locks that schedule
before any refined result is observed.

The runner is

```sh
DRAGON_BIN=/absolute/path/to/Dragon \
GANLIB_LIB=/absolute/path/to/libGanlib.a \
GANLIB_MOD=/absolute/path/to/ganlib/modules \
SEED_DIR=/absolute/path/to/iterative-seed \
BASELINE_DIR=/absolute/path/to/iterative-map1 \
KEEP_WORK=1 \
  sh validation/iterative/run_inner_sensitivity.sh
```

It requires the frozen Stage-3 executable, seeds and five baseline XSM
objects. The basis and complete \(x_0\) archives must be byte identical. If
all five solves terminate strictly, independent Ganlib-only checks recompute
\(\mathcal D_{\rm out,h}\), \(\mathcal D_{\rm out,h/2}\) and
\(\mathcal D_{\rm in}\) component by component and compare the actual radial
leakage, fission-source and eigenvalue inputs bitwise. No scalar score,
relaxation or fitted factor is introduced.

The precise controls and scale-ordering rule are in
`inner_sensitivity_protocol.json`. A fresh \(h/2\) replay is required before
Stage 4 is finally qualified. `KEEP_WORK=1` preserves the first isolated
work directory so its five scientific hashes can be frozen. A replay
reference must contain exactly, in order, the hashes for
`basis_reference.xsm`, `state0_axial.xsm`, `state1_system.xsm`,
`state1_axial.xsm`, and `state1_snapshots.xsm`; arbitrary or partial checksum
lists fail closed.

The machine state is `UNRESOLVED` if any component fails the predeclared
ordering, `PENDING-REPLAY` if all four pass on the first capture, and
`QUALIFIED` only if all four pass again in a fresh isolated replay whose five
scientific files match the frozen reference. Only `QUALIFIED` authorizes
Stage 5.

The first capture did not reach that classification stage. All three radial
fixed-source solves exhausted `MAXOUT=500` with strict `STATE=2`; their final
unknown changes were \(5.03027\times10^{-7}\),
\(5.29329\times10^{-7}\), and \(6.19920\times10^{-7}\), above
\(h/2=2.5\times10^{-7}\). The initializer and returned axial solves passed,
but the written `state1` objects are invalid as \(G_{h/2}(x_0)\).

`check_inner_sensitivity_failure.py` recognizes only this complete,
normal-ending three-plane failure pattern and emits:

```text
CAPTURE INVALID-INNER-NONCONVERGENCE
STAGE4 INVALID
STAGE5 NOT-AUTHORIZED
OUTER-CONVERGENCE NOT-EVALUATED
```

The exact failure receipt and bounded-diagnostic rationale are in
[inner_sensitivity_result.md](inner_sensitivity_result.md). Do not increase
`MAXOUT` or rerun the three-plane capture. The frozen at-most-six-step,
single-plane production-map diagnostic has now been completed.
Its machine-readable controls are
[radial_floor_protocol.json](radial_floor_protocol.json), and the runner is
[run_radial_floor_diagnostic.sh](run_radial_floor_diagnostic.sh).
The preflight reads only the real TRACK, SOURCE, SYSTEM and forensic CAP
objects; it does not fabricate solver outputs. The CAP flux carries
returned-axial \(L_1\) metadata written after its radial solve, whereas that
solve used the unchanged system \(L_0\). Thus only CAP leakage metadata is
excluded. The final audit still requires every newly produced arm/probe flux
to carry system \(L_0\) bit for bit before it reports either one-step defect.

Both main arms reached the six-update cap. The NATIVE terminal probe gave
\(D_{V,2}=2.7679927\times10^{-7}\) and
\(D_{\max}=4.1416214\times10^{-7}\); the STATIONARY terminal probe gave
\(3.4298569\times10^{-7}\) and \(4.8318913\times10^{-7}\), respectively.
There is no acceptance threshold or acceleration-choice claim. The original
\(h\)-to-\(h/2\) Stage 4 remains `INVALID` and Stage 5 remains
`NOT-AUTHORIZED`. See
[radial_floor_result.md](radial_floor_result.md) and its tracked checksum
receipt for the exact result and evidence boundary.

## Read-only working-precision audit

The retained probes can be audited without another Dragon run:

```sh
validation/iterative/run_radial_precision_audit.sh
```

The runner first replays the complete radial-floor Ganlib checker, hashes the
five input XSM objects before and after, compiles a solver-free checker with
strict floating-point controls, runs its IEEE self-test, and requires two
byte-identical 5920-row ledgers.

For each positive retained scalar flux, the signed difference between the
two binary32 encodings is the exact number of adjacent representable values
crossed. NATIVE has 288 unchanged values and a maximum absolute step of 17;
STATIONARY has 272 unchanged values and a maximum of 12. Full histograms and
interpretation limits are in
[radial_precision_result.md](radial_precision_result.md).

This does not establish a unique binary32 floor. The active chain also
contains the MCCG `EPSI 1E-5` control, an ACA `1E-7` cutoff, binary32
rebalancing and FLU acceleration. Nor can `SYSTEM` provide a true archived
\(A\phi-q\): its matrices are ACA corrective/preconditioning data, and the
saved source precedes later flux transformations.

The capture design was frozen before implementation in
[raw_moc_residual_protocol.json](raw_moc_residual_protocol.json). It defines
a default-off `TYPE S + MCCG` diagnostic for the evaluated state, same-call
`QFR`, source-element vector and raw MOC response from only the first primary
GMRES evaluation, after STIS/volume normalization but before ACA/SCR. The
instrumentation adds zero operator applications and introduces no acceptance
threshold. The audit is published only in the fresh writable `L_FLUX` output
after all 370 group tuples are complete. The corrected bounded replay has
since captured and independently verified this observable; that completion
authorized only the offline ULP bridge audit below.

## Raw primary-MOC capture

The capture path is implemented and was enabled only for the bounded
corrected replay. It is explicitly enabled by `MOCA 1` for NATIVE or
`MOCA 2` for STATIONARY; absence of `MOCA` remains the unchanged default-off
path. The legacy `SPOT`/`IPICK` parser branch is unchanged.

The implementation accepts only the frozen one-step branch:

```text
TYPE S, MCCG, 370 groups, 8 regions, 14 unknowns
EXTE 1 2.5E-7
UNKT 2.5E-7
THER 740 2.5E-7
ACCE 1 0
INIT ON, direct solve, rebalancing on, ILEAK=0
KRYL=10, STIS=1, IAAC=80, ISCR=0, IDIFC=0, PACA=4, IDIR=0
```

Only the first primary GMRES evaluation may write. `MCGFL1` copies the
same-call `QFR`, evaluated binary32 state, binary64 source vector and
binary64 raw MOC response after STIS/volume normalization and before
ACA/SCR. The affine-RHS call, every Krylov-basis call and every later
primary call are excluded. The helper contains no transport call, and no
audit record is read into a solver array.

Run the short, no-Dragon state-machine gate with

```sh
validation/iterative/run_raw_moc_capture_state_test.sh
```

It checks default-off absence, the complete 370-by-14 schema, first-primary
write-once behavior and fail-closed duplicate, wrong-path, wrong-step,
partial-publication and overwrite cases.

Run the independent read-only checker gate with

```sh
validation/iterative/run_raw_moc_capture_checker_test.sh
python3 validation/iterative/check_raw_moc_capture_contract.py
```

The checker links only Ganlib. It recursively compares FROZEN with OFF and
OFF with ON while allowing only `SPOT-MOC-AUD`, verifies `EVAL` against the
frozen pre-update flux, independently replays the binary32 `MCGFCS` volume
and boundary source arithmetic, then reports the full 14-unknown ledger,
the scalar-only volume-weighted relative norm, the input-normalized scalar
maximum with exact ties, and six currents componentwise. A finite RAW
one-bit change remains structurally valid but changes the scientific
receipt; without an independent transport truth the checker does not
pretend otherwise.

`arm` and `plane` are protocol labels, not quantities inferable from the
captured flux. The production runner therefore binds each label to the
declared terminal input and plane through frozen input hashes.
`COMPLETE` certifies only that the write-once record structure is complete;
scientific acceptance additionally requires the independent checker to pass.

The first bounded production attempt completed its one no-transport
preparation process and four one-step probes with normal process exits. The
independent checker then rejected `ICODE exceeds group ALBEDO` before opening
PRE, FROZEN, OFF or ON, so fail-closed publication produced no artifact and
no scientific classification.

That rejection was a checker-contract error, not a transport result: geometric
negative `ICODE` is legal, and `MCGFCS` selects the boundary albedo through
`-NZON`, not the boundary-unknown ordinal. The checker and its fixtures now
cover negative `ICODE`, absent group albedos, non-identity `NZON`, boundary
source tampering and positive physical-albedo overflow.

The corrected replay completed from frozen commit `a011fd9`. Independent
OFF/ON log comparisons and two deterministic Ganlib-only XSM replays passed
for both arms. The scalar RAW-minus-EVAL diagnostics are
\(D_{V,2}=5.7461264\times10^{-7}\) and
\(D_{\max,\mathrm{input}}=2.1306357\times10^{-6}\) for NATIVE, and
\(5.7815536\times10^{-7}\) and \(2.1902923\times10^{-6}\) for STATIONARY.
They classify the capture ledger only; they are not a transport residual,
error bound, acceptance gate or arm comparison. Exact evidence is in
[raw_moc_capture_result.md](raw_moc_capture_result.md).

## Offline RAW-MOC ULP bridge census

The retained capture was then audited offline under the frozen
[raw_moc_ulp_bridge_protocol.json](raw_moc_ulp_bridge_protocol.json), with
zero Dragon processes, transport solves and operator applications. For every
positive finite scalar coordinate, `RAW-BRIDGE` compares one IEEE
binary64-to-binary32 round-to-nearest-even projection of RAW with EVAL.
`PRODUCTION-STEP` separately compares PRE with OFF.

| arm | ledger | unchanged | upward | downward | adjacent | maximum absolute steps |
|---|---|---:|---:|---:|---:|---:|
| NATIVE | RAW-BRIDGE | 135 | 977 | 1848 | 248 | 877 |
| NATIVE | PRODUCTION-STEP | 288 | 136 | 2536 | 265 | 17 |
| STATIONARY | RAW-BRIDGE | 133 | 975 | 1852 | 251 | 878 |
| STATIONARY | PRODUCTION-STEP | 272 | 88 | 2600 | 220 | 12 |

Each ledger has 2960 rows. The direct projection is nonidentical to EVAL at
2825 NATIVE and 2827 STATIONARY coordinates. There is no result threshold or
empirical parameter. Because the ledgers have different endpoints, they must
not be subtracted. No part of the production step is attributed to binary32
rounding, GMRES, ACA, SCR, rebalancing or acceleration.

This descriptive census is not an \(A\phi-q\) residual, backward-error or
transport-error bound, NATIVE/STATIONARY ranking, convergence test, or
Stage-4/Stage-5 authorization. Exact counts, maximum ties, the complete
interpretation boundary and the local-artifact manifest identity are in
[raw_moc_ulp_bridge_result.md](raw_moc_ulp_bridge_result.md). Check the
tracked evidence without Dragon or the ignored local artifact with

```sh
python3 validation/iterative/check_raw_moc_ulp_bridge_contract.py
python3 validation/iterative/check_raw_moc_ulp_bridge_result.py --public-only
```

## Passive GMRES activity result

The separately frozen version-2 runner was explicitly authorized for one
OFF and two independent ON processes. All three ended normally. OFF
reproduced the legacy OFF XSM byte for byte; ON-A and ON-B reproduced one
another in their XSM, normalized log and complete raw ledger.

The independently reconstructed control flow is:

```text
MCGMRE entries / normal exits     1 / 1
PRIMARY calls / active groups     1 / 370
AFFINE-RHS calls                  0
KRYLOV calls                      0
correction blocks / group-blocks 0 / 0
classification                   VALID-GMRES-UPDATE-INACTIVE
```

No correction block means no per-group `KMAX` row exists; all histogram
bins, including `K=0`, therefore contain zero group-block rows. The result
does not say that the PRIMARY MOC evaluation was unused. It is limited to
this frozen restart and one map, does not explain earlier nontermination,
and does not establish inner or outer convergence.

For this locked restart and one-map execution, the absent GMRES correction
update is not a meaningful precision A/B target. The `MCGFCS` binary32/64
replay is now only an optional implementation unit test, not a scientific
gate: a nonempty local source difference would not establish a smaller
fixed-source defect or strict FLU termination.

The existing RAW-MOC capture is already a same-point primary-MOC defect at
the plane-1 six-update arm terminals derived from the cap-500 restart. A new
terminal sweep there would repeat that observable. The failed \(h/2\)
condition is evaluated from the binary32 `FLU2DR` working state, so a
continuous REAL64 treatment would have to propagate through the entire
radial solver. A partial promotion at `MCGFCS`, `MCGMRE` or `MCGFLX` is not
a valid test of that failure. At that point a full precision lane was
outside the simple Stage-4 v2 amendment. After v2 itself returned
`UNRESOLVED`, the project froze the separate solver-validation overlay
described below; it does not add mathematics to SPOD.

Exact counts, evidence hashes and interpretation limits are in
[gmres_activity_result.md](gmres_activity_result.md). Verify the tracked
result without Dragon, or include the ignored local artifact, with

```sh
python3 validation/iterative/check_gmres_activity_result_history.py \
  --public-only
python3 validation/iterative/check_gmres_activity_result_history.py
```

## Stage-4 v2 attainable tolerance freeze

The original \(h\)-to-\(h/2\) capture remains
`INVALID-INNER-NONCONVERGENCE`. Stage-4 v2 instead freezes exactly one
coarse-to-fine pair before any coarse result exists:

```text
coarse 2h = 0x358637bd = 1.0E-6 input
fine    h = 0x350637bd = 5.0E-7 input
```

The binary32 factor-two relation is exact. The released \(G_h(x_0)\) is
reused only with its exact executable, basis, state and scientific hashes.
The future coarse deck must consume the archived \(x_0\) and fixed basis
directly, so it adds no initializer solve. It may perform only the three
radial and one returned axial solves in \(G_{2h}\), under a process-group
wall-clock bound.

The four components of
\(\mathcal D(x_{1,h},x_{1,2h})\) are compared separately with the
corresponding coarse outer-map components. There is no weighted score,
fitting or relaxation. Strict solve termination and the existing physical
contracts remain mandatory, and a fresh exact replay is required before
qualification.

This can establish only `QUALIFIED-ON-2H-TO-H-SCALE`, meaning stability over
\([h,2h]\). It cannot establish a convergence order, error bound, REAL64
equivalence or \(h/2\) qualification. The protocol is frozen in
[inner_sensitivity_v2_protocol.json](inner_sensitivity_v2_protocol.json);
verify it without transport with

```sh
python3 validation/iterative/check_inner_sensitivity_v2_protocol.py \
  --public-only
```

No Dragon process is authorized by the freeze.

## Stage-4 v2 outcome and REAL64 route

The single authorized coarse capture has now completed.  All four transport
solves terminated strictly, but the axial-state component remained
unresolved:

```text
R_a D_out,2h  2.2557116628569681E-5
R_a D_in      2.2871261661792861E-5
relation      GREATER
classification UNRESOLVED
```

Replay and Picard are therefore not authorized.  The subsequent offline
Gram/height decomposition showed that the \(2h\)-to-\(h\) axial change is
almost antiparallel to the coarse update.  It localizes the returned-state
manifestation but does not identify a radial-plane cause, choose a group,
or change the result.

The next route is
[radial_real64_route.md](radial_real64_route.md).  A read-only archived
\(A\phi-q\) checker is rejected because the XSM archive does not contain the
complete MOC operator and its `SOUR/FLUX` records are not guaranteed to be a
same-point equation pair.  The chosen route is instead a default-off
continuous REAL64 radial working lane, limited to the frozen
`TYPE S + MCCG` branch.

The current protocol authorizes static implementation and tests only:

```sh
sh validation/iterative/run_radial_real64_route_tests.sh
```

The first isolated implementation subgate is now present under
[`real64_phase_a1/`](real64_phase_a1/README.md).  It implements and tests
only the locked REAL64 source arithmetic and explicit conversion
boundaries:

```sh
make spot-real64-phase-a1
```

The second isolated subgate is under
[`real64_phase_a2/`](real64_phase_a2/README.md).  It adds a typed REAL64
full-matrix active-mask façade from the Phase-A1 source to the
post-`MCGFST`, pre-`MCGFCA` raw-response boundary:

```sh
make spot-real64-phase-a2
```

Phase-A2 uses only a synthetic signed-permutation callback.  It validates
all 31 nonempty masks over its five-column fixture, exact inactive `+0`,
complete finite active output, failure atomicity, and compile-time
wrong-kind rejection.  It does not execute the real MOC sequence or read a
tracking file.

The third isolated subgate is under
[`real64_phase_a3/`](real64_phase_a3/README.md).  It is a compile-only,
checked legacy-ABI seam for the frozen `MCGFCF`-through-`MCGFST` path:

```sh
make spot-real64-phase-a3
```

Phase-A3 encodes the ordered call
`MCGFCF(MCGFFIR,MCGFFAR,MCGFFAL,MCGSCA,...)->MCGFST` with the real legacy
data and procedure interfaces.  Its unresolved link barrier is mandatory:
the gate creates no Phase-A3 executable, performs zero Phase-A3 links,
executes zero Phase-A3 calls, and runs zero transport solves and zero
Dragon processes.  It is not connected to the production call graph and
does not validate MOC behavior.

The seam also makes one legacy limitation explicit.  The frozen
`MCGFL1` call forms `XSIXYZ(1,IDIR)` with `IDIR=0`, a nonconforming actual
designator.  Phase-A3 supplies a legal caller-owned `XSI` vector solely to
type-check the seam; it does not claim that the production caller is fixed
or validated.

The fourth isolated subgate is under
[`real64_phase_a4/`](real64_phase_a4/README.md).  It closes the
validation-only, compile-only host call shape from the Phase-A2 façade into
the Phase-A3 seam:

```sh
make spot-real64-phase-a4
```

Its caller-owned context storage schema is closed, but real-host population
and cross-object provenance remain unbound.  No Phase-A4 object is linked
or executed.  The recursive short gate links and executes the already-frozen
Phase-A1 and Phase-A2 synthetic programs once each; neither is a tracking
or MOC calculation.  The complete gate performs zero transport solves and
zero Dragon processes.

All four subgates remain outside `src/`.  ACA, rebalancing, acceleration,
the wider mutable radial state, terminal norms, real MOC operation, and
physical accuracy remain open.  This is not a continuous REAL64 lane and
is not evidence of MOC, solver, or Picard convergence.  The next authorized
work is a compile-only Phase-A5 contract for real-host context population
and provenance, with the unresolved link barrier retained and no execution.

It authorizes zero Dragon processes.  A later plane-1 feasibility capture,
full REAL64 Stage 4, replay, and Picard trajectory each require their own
gate.  No relaxation, fitted coefficient, cutoff tuning, residual multiplier
or ULP/angle threshold is introduced.

## Fixed three-return design

A three-return online legacy32 diagnostic was examined as a smaller
alternative:

\[
x^0\longrightarrow x^1\longrightarrow x^2\longrightarrow x^3.
\]

It is frozen only as a design in
[picard_three_return.md](picard_three_return.md) and
[picard_three_return_protocol.json](picard_three_return_protocol.json).
Execution is `NO-GO` under the current Stage-4 v2 result because three
returns are a Picard trajectory and `UNRESOLVED` forbids Picard.

The design has no full-state aggregate score, relaxation parameter or trend
threshold.  A possible future run would report \(D_\rho,D_L,D_a\)
separately and could not claim convergence even if all three decreased.
It would require nine radial and three returned axial transport solves, so
it is not represented as a short synthetic test.

Check only the no-run design contract with

```sh
sh validation/iterative/run_picard_three_return_protocol_tests.sh
```

The expected terminal status is
`PROTOCOL-ONLY; EXECUTION=NO-GO; DRAGON-RUNS=0`.
