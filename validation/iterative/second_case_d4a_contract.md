# Second-case contract: IRENA D4-A 1/12 assembly

## Status

`CORRECTED_MATERIAL_EPOCH_PREFLIGHTED_REBUILD_REQUIRED`.

## Material epoch correction (2026-09-04)

A cross-code input audit found that the snapshot campaign still used the
pre-2026-05-27 material procedures.  Those procedures multiplied bulk mass
density by cubic thermal expansion, which makes a heated material denser.
The active D4-A input now uses the independently reviewed physical convention

```text
rho(T) = rho(20 C) / (1 + alpha * (T - 20 C))^3
```

together with the benchmark MOX O/M ratio `1.98`, fuel compaction `0.955`,
heavy-metal mass bookkeeping, the sodium-temperature interpolation fix and
the exactly normalized EM10 Fe mass fraction `0.8908`.  These are material
input corrections, not SPOD closure terms, convergence controls or fitted
coefficients.  Geometry, three temperatures, rank two and direct Picard are
unchanged.

Consequently, every older D4-A map, including the converged map 8, is
classified `LEGACY_MATERIAL_INPUT / NUMERICAL_REGRESSION_ONLY`.  The next
physical result must rebuild the three snapshots, basis and fixed point from
this material epoch before comparison with an independent reference.

The accepted bounded Dragon run built only the radial tracking object from the
frozen geometry.  A later first-state attempt reached the TONE self-shielding
iteration cap and was stopped before publishing a snapshot, so it is not an
accepted physical result.  Comparison with the historical successful builder
isolated an input-copy error: TONE/MERGMIX must retain tracking density `50.0`,
while the separate production radial track uses `100.0`.  That distinction is
now restored and the hash-locked static preflight passes.  A dedicated
TONE-only replay of the corrected 650 C state then converged at iteration 4
with error `4.453e-6 < 1.0e-5`, without an iteration-cap warning.  Its TONE
module took 326 s and Dragon ended normally.  No criterion, material state,
empirical coefficient or physical equation changed.  The gate contains no
MCCGT, ASM or FLU, so no radial archive, axial solve or Picard iteration has
been accepted.  The subsequently authorized three-state campaign was run once
with a 7200 s hard bound and no retry.  State 1 again passed TONE, but its
strict `FLU TYPE K` solve produced no terminal before the bound; the runner
cleaned up Dragon and published no snapshot, archive or success receipt.  No
OpenMC process was started. A 600 s passive trace located the cost inside the
first MCCGF/MCGMRE solve. Byte-identical 1300 s, 1500 s and final 1900 s
replays then completed seven MCGMRE solves at their unchanged local criterion.
The scheduled `IN(1..3)` free segment and `IN(4..6)` variationally accelerated
segment form one complete thermal cycle; the next free step reached
`IN(7)=0.0208`. Its value remains about `4.16e4` times the `5e-7` target, and
all records are still within `OUT(0)`. This proves neither FLU, eigenvalue nor
Picard convergence. See [the TONE gate
result](d4a_tone650_gate_result.md) and [the bounded snapshot campaign
result](d4a_three_snapshot_bounded_result.md), followed by [the FLU hierarchy
diagnostic](d4a_flu650_diagnostic_result.md).

The observable canonical `EDIT 1` route was subsequently executed once with
the same operator and three `5e-7` criteria, a 14400 s wall limit and no retry.
It completed 25 strict inner solves through `OUT(25)` and stabilized `keff`,
but its best printed outer flux residual was `1.69e-6`; no strict outer
terminal or snapshot was produced before timeout.  Its exact classification
is `TIMEOUT / NOT_RUN / NO_RESULT`.

A source/artifact audit then found no saved raw outer flux pair and no proof of
a REAL32 floor.  It did find that the production MCCG linear solve used
`EPSI=1e-5` while FLU required `5e-7`.  The current builder now takes MCCG
`EPSI` from the same `solver_eps=2e-6` as `EXTE`, `UNKT` and `THER`.  This is a
numerical consistency correction, not a material, operator or empirical-model
change.  TONE remains at `1e-5`.  Static preflight passes; the corrected
transport has not yet been run.

## Declared terminal correction (2026-08-26)

The `5e-7` four-channel strict terminal is **measured unreachable** on
this system.  A 17.5 h bounded state-1 run (86400 s authorized, 51
strict outers at ~19 min each) converged `keff` to `1.367864 +- 2e-6`
(~0.1 pcm jitter) while the raw outer-image residual oscillates on an
`~1e-5` envelope with occasional dips to `9.7e-7`/`2.4e-6`; later-half
inner residuals reach `8.4e-8`.  Together with both earlier eras'
attempts (25 outers to `1.69e-6`, then timeout; the `IN(7)=0.0208`
diagnostic), every `5e-7` campaign has ended the same way: eigenvalue
converged, flux-image channel on its floor, wall exhausted, nothing
published.  Following the campaign's floor discipline (the pincell
`UNKT` precedent), the snapshot terminal is **declared at `2e-6` with
all four channels moved consistently** (`EXTE`/`UNKT`/`THER` and MCCG
`EPSI`, preserving the EPSI-consistency correction).  No material,
operator, or empirical parameter changed.  Evidence:
`validation/artifacts/d4a-state1-outer-floor`;
`d4a_three_snapshots.x2m` re-sealed in `d4a_snapshot_inputs.sha256`.

## Why this case

The selected case is
`data/rnr_0burn_spot_proc/irena_assembly_tiso_1_12_1ring.dat`:

- 1/12 of an IRENA assembly;
- 132 radial regions instead of the current pin cell's 8;
- six physical media: sodium, AIM1 cladding, helium gap, MOX, central
  helium and the EM10 wrapper;
- multi-pin intra-assembly radial leakage and sector symmetry.

It is therefore physically complementary to the current reflective pin
cell, while remaining smaller than the available 207- and 688-region
assembly candidates.

## Frozen inputs

- geometry SHA-256:
  `ca46ef77ea769059ddc612f1a78e4b565c32990401b21652c822bf2e11497a3e`;
- `rnr_cc.c2m` SHA-256:
  `594e9e58aae950b003bd410440928c97b59cf67f70844033c69c05b78e8565b5`;
- `rnr_interpol.c2m` SHA-256:
  `255ddfc61a61026e0f36aefe5ad4cee0b41871fdbd25e2b77c540bd9bccb8ed2`.

The bounded geometry-only TRACK build and its independent record checks are
recorded in [the D4-A TRACK result](d4a_track_geometry_probe_result.md).

Historical case specifications are recoverable from commit `470e0d7`:

- `data/Snap1Ring.c2m`, Git blob `8883a419...`, content SHA-256
  `64438d36624e7ec16a6ec8203c0e34498889a4e3073c719d1acfb08ec016943d`;
- `runs/irena_spot_d4a/d4a_converged_ac.x2m`, Git blob `1aef8355...`,
  content SHA-256
  `2c8ea2a2342ae54a78e5777858960190b8088c5fb6aa1865a1733285476b748b`.

Those historical files define geometry/material plumbing only.  They do not
validate the current method: tracked run logs and physical archives are
absent, they use five temperature snapshots, an `eps_pod=1e-3` cutoff, and an
older scalar outer criterion.  None of those numerical choices is imported
here.

A separate local census found one untracked historical 750 C D4-A solve log,
SHA-256
`9f84d885de9526998409c498676aa89f12d60f1833039c5a79424dde1436b254`.
It records the canonical geometry, completed TONE/ASM/FLU modules and
`k=1.367208`, but its in-memory objects were deleted and no regional flux was
exported.  It is provenance only: it is neither a current snapshot nor an
acceptance reference.

## Frozen three-snapshot definition

The frozen D4-A archive recipe is defined to generate exactly three offline
radial flux fields:

| snapshot | fuel | cladding | sodium |
|---:|---:|---:|---:|
| 1 | 650 C | 620 C | 475 C |
| 2 | 750 C | 620 C | 475 C |
| 3 | 850 C | 620 C | 475 C |

Temperature is the prescribed offline material sampling coordinate: it changes
the microscopic-library temperature and, through `rnr_interpol/rnr_cc`, the
material densities.  It is not an online reduced unknown.  Each entry will
generate a complete 132-region, 370-group neutron-flux field, and POD is
applied to those spatial fields.  The three temperatures are frozen a priori
because they use the same thermophysical sampling schedule as the accepted
three-plane pin baseline.  This holds snapshot sampling fixed while testing
the assembly-scale D4-A radial configuration; it does not claim that geometry
is the only physical difference or that these states are a coupled
thermal-hydraulic prediction.  They are not adjusted from D4-A results and do
not act as relaxation, closure or convergence coefficients.

The remaining three media inherit those declared temperatures in the material
model: EM10 follows sodium, central helium follows fuel, and gap helium follows
cladding.  These assignments are frozen physical input assumptions, not fitted
coefficients.

The declared snapshot count is three, and the planned D4-A basis rank is fixed
at two before generating the archive.  The rank is a declared spatial
discretization order, not selected by a fitted singular-value cutoff.  The
builder uses the admitted D4-A tracking settings and `solver_eps=2e-6`; this
is the already declared numerical terminal for resolving each discrete radial
eigenproblem, not a physical parameter.

The minimal current inputs are:

- `data/SpotD4Snap.c2m`, which builds one six-medium physical state;
- `data/SpotD4Tone.c2m` and `d4a_tone650_gate.x2m`, which reproduce only the
  first state's material/TONE prefix and stop before production transport;
- `d4a_three_snapshots.x2m`, which builds and persists exactly three list
  items (`TRACK`, `MICROLIB2`, `SYSTEM`, `FLUX`);
- `d4a_snapshot_inputs.sha256`, which freezes the builder, driver, geometry
  and material procedures;
- `run_d4a_three_snapshots.sh`, which is default-off and refuses to run
  unless both `RUN_D4A_SNAPSHOTS=1` and a new `RESULT_DIR` are supplied.

The seconds-scale preflight checks all frozen hashes, the exact three states,
the archive layout, absence of POD/coupling logic, the admitted TRACK settings
and the SHEM-370 library hash.  It executes no Dragon transport:

```sh
sh validation/iterative/preflight_d4a_three_snapshots.sh
```

Its result is recorded in
[the D4-A snapshot preflight result](d4a_snapshot_preflight_result.md).

## Frozen validation boundary

Three different questions must not be mixed:

1. **Iteration convergence.**  A D4-A rank-two result is converged only if it
   satisfies the existing raw strict residual gate with
   `EPSOUT=EPSUNK=EPSINR=5e-7`.  No external reference and no fitted
   coefficient enters that gate.
2. **POD truncation difference.**  After both solutions satisfy the same
   strict gate, compare rank two with a same-operator physical full-rank
   solution.  Freeze the reported quantities as
   `1e5*(1/k_full-1/k_rank2)` pcm and the RMS/maximum differences of normalized
   three-floor and radial-region nu-fission production.  This isolates the
   effect of the basis rank; it is not an independent physics validation.
   No D4-A shape PASS threshold will be selected after seeing the result.
3. **Independent physics comparison.**  An OpenMC reference must reproduce
   the same 132-region assembly, the three declared axial material states,
   axial mesh and boundary conditions.  Its frozen observables are `k` with
   Monte Carlo uncertainty, normalized three-floor nu-fission production and
   normalized radial-region nu-fission production.  The already predeclared
   Level-4 statistical/keff rule is inherited unchanged: reference uncertainty
   at most `50 pcm`, and absolute reactivity difference at most
   `500 pcm + 3 sigma`.  This is an external validation rule only; it is never
   used in SPOD, Picard iteration, basis construction or parameter selection.
   Radial and floor shape differences are reported without a fitted PASS
   threshold.

No artifact currently implements that D4-A OpenMC problem, and the historical
same-geometry `k=1.367208` is neither independent nor spatially complete.
Therefore D4-A remains `NO_GO_FOR_ACCURACY_CLAIM`.  The corrected 650 C
`LIB + SALT + TONE` prerequisite has passed.  The later observable canonical
run completed 25 strict inner solves but timed out after `OUT(25)` without the
outer gate or a snapshot.  This is a hard-bounded no-result, not a FLU
divergence proof.  The external reference is not part of the iteration and is
not required to test mathematical convergence; freezing its problem and
observables here prevents later result-driven choices.

## Current implementation boundary

The general core routines `SPOASM`, `SPOPOD` and `SPOT_LEAKAGE` already use
runtime dimensions.  The radial entrance, solver and publication boundary
now do as well:

- `SPOR64_B2B` obtains `NREG`, `NMAT`, `NSURF` and `NUNKNO` from the actual
  TRACK object and independently checks the long-vector records;
- `SPOR64_A9/A8` carry those extents through the unchanged REAL64 radial
  equations and MCCG call chain;
- `SPOR64_B2C` publishes using the runtime region, material and unknown
  counts.

The assembled-to-close strict lifecycle now uses the same runtime geometry:

- `SPOR64_B2K/B2N` derive and close the three TRACK tuples before committing
  the system archive or frozen fission source;
- `SPOR64_B2S/B2R/B2W` pass those extents through the host solve, RETURNED
  collection and epoch close without changing their public interfaces;
- `MCCG-STATE(5:6)` are the runtime `MXSEG` and ACA connection count `LC`.
  `LC` sizes `MCU$MCCG`, `CF$MCCG` and `CQ$MCCG`; the independent
  fission-isotope dimension remains `NIFIS=32`.

The next-epoch projection lifecycle now uses the same runtime geometry:

- `SPOR64_B2H` obtains the region, material, numerical-surface and unknown
  counts from its immutable radial TRACK;
- `SPOR64_B2I/B2J` require one common TRACK tuple across the three snapshots
  before bootstrap or CLOSED-to-PROJECTED publication;
- their POD contraction order, 370-group equations, three snapshots,
  lifecycle states and bitwise REAL64/REAL32 boundary remain unchanged.

Historical full-lifecycle builders still assume pin-cell dimensions, so an
actual D4-A archive has not yet crossed the complete chain.  The standalone
strict 650 C transport has now been exercised, but it did not reach its outer
terminal; D4-A snapshot publication therefore remains unauthorized.  The
current result is transport evidence and interface readiness, not convergence.

## Completed vertical slices

`SPOR64_B2C` now derives `NREG`, `NMAT` and `NUNKNO` from its actual arrays
and allocates its publication staging accordingly.  The group count remains
the declared 370-group problem.  No tolerance, gate, equation, snapshot
count or physical parameter changed.

The no-transport manufactured test uses the actual D4-A extents

- `FLUX64(144,370)` and `SOUR64(144,370)`;
- `KEYFLX(132)=1,...,132`;
- `IMERGE(6)=1`.

The value 144 comes from the real `TRACK/STATE-VECTOR`; the values carried by
this particular host test remain manufactured.  It proves structural shape
propagation, not D4-A transport physics.

The test verifies the runtime state records, all 370 REAL64 list items, their
bit-exact REAL32 mirrors and fail-before-write rejection of duplicate keys or
mismatched arrays.  It repeats the same contract at the old pin dimensions
`(NREG,NMAT,NUNKNO)=(8,8,14)`.  Run it with:

```sh
make spot-b2c-dimensions
```

The result is recorded in
[the B2C runtime-dimension result](b2c_runtime_dimension_result.md).

At the radial solve boundary, `SPOR64_B2B` now treats `TRACK/STATE-VECTOR`
as the geometry authority and requires the independently stored `V$MCCG`,
`NZON$MCCG` and `KEYCUR$MCCG` extents to agree.  The MCCG route retains the
strict relation

```text
NUNKNO = NLONG = NREG + NSURF
```

For D4-A, `NSURF=12`.  These 12 numerical surfaces reference six physical
boundary/albedo code slots, so their `MATALB/NZON` values remain in
`[-6,-1]`; `ICODE`, `ALBEDO` and `SIGAL` retain their legacy six-slot
semantics.  `SPOR64_A9` and `SPOR64_A8` derive the remaining geometry
dimensions from their actual arrays and TRACK records.  They do not change
the 370-group operator, iteration order, physical coefficients, tolerances
or terminal predicates.

A seconds-scale no-transport test admits the pin tuple and the manufactured
D4-A tuple `(NREG,NMAT,NSURF,NUNKNO)=(132,6,12,144)` through the A8/A9
interfaces and verifies fail-closed entry with null transport handles:

```sh
make spot-a89-dimensions
```

The result is recorded in
[the A8/A9 runtime-geometry result](a89_runtime_geometry_result.md).

At the projection boundary, a seconds-scale no-transport test admits the old
pin shape and manufactured D4-A `(132,6,12,144)` shape through `SPOR64_B2H`. It
checks all 370 REAL64 projected list items and their exact REAL32 mirrors:

```sh
make spot-b2h-dimensions
```

The B2I bootstrap retains its historical result of one commit and twelve
fail-before-write rejections.  The B2J pin replay advances CLOSED/5 to
PROJECTED/6, rejects an epoch mismatch, leaves its inputs unchanged and is
byte-identical to the frozen pre-generalization output.  These are
no-transport regressions, not a manufactured full D4-A lifecycle.  The
permanent target above strictly compiles B2H/B2I/B2J and runs B2H; the B2I
replay uses the historical harness at Git object `891e67c` and the B2J replay
uses `prepare_r64_next_projected.f90` with the frozen pin artifacts.

The connected `B2K/B2N/B2S/B2R/B2W` sources compile under the strict
REAL64 flags with runtime region, material and unknown extents.  A frozen
pin-cell no-Dragon replay independently admits RETURNED (`STATUS=3`) and
closes epoch 69 (`STATUS=2`); both CLOSED XSM files retain their exact
SHA-256 hashes.  This proves backward compatibility and lifecycle/write
ordering, not D4-A transport or D4-A convergence.

## Remaining work before a convergence census

1. rebuild and independently verify the three snapshots with the corrected
   material epoch and the declared common `2e-6` radial terminal;
2. build the fixed rank-two basis and converge direct Picard under the unchanged
   `5e-7` outer three-defect gate;
3. compare that physical fixed point with the separately specified full-rank
   and continuous-energy references.

The method remains the same 370-group, fixed rank-two basis, three-snapshot
Synthesis-POD iteration.  The historical five-temperature campaign is not
imported.  The separately frozen D4-A OpenMC reference must be implemented
before making an accuracy claim, but it does not feed back into convergence.
