# Second-case contract: IRENA D4-A 1/12 assembly

## Status

`ACTUAL_TRACK_TOPOLOGY_ADMITTED_NO_D4_TRANSPORT`.

The accepted bounded Dragon run built only the radial tracking object from the frozen
geometry.  It performed no library processing, eigenvalue solve, radial
fixed-source solve, axial solve or Picard iteration.  No OpenMC process was
started.  The purpose of this record is to admit the real geometry topology
without changing the accepted SPOD equations or starting a long calculation.

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
  `3f7583449d279614eff3b1f1fe6b9a2ca0832612e3b90f4f68d1c2995ce71c03`;
- `rnr_interpol.c2m` SHA-256:
  `b09f93be0655d5ac017b3dc33a3b9d38c5dfb7f12ba70060ec2a050223895c6a`.

The bounded geometry-only TRACK build and its independent record checks are
recorded in [the D4-A TRACK result](d4a_track_geometry_probe_result.md).

Historical case specifications are recoverable from commit `470e0d7`:

- `data/Snap1Ring.c2m`, Git blob `8883a419...`, content SHA-256
  `64438d36624e7ec16a6ec8203c0e34498889a4e3073c719d1acfb08ec016943d`;
- `runs/irena_spot_d4a/d4a_converged_ac.x2m`, Git blob `1aef8355...`,
  content SHA-256
  `2c8ea2a2342ae54a78e5777858960190b8088c5fb6aa1865a1733285476b748b`.

Those historical files define geometry/material plumbing only.  They do
not validate the current method: their logs are absent, they use five
temperature snapshots, an `eps_pod=1e-3` cutoff, and an older scalar outer
criterion.  None of those numerical choices is imported here.

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
actual D4-A archive has not yet crossed the complete chain.  D4-A transport
therefore remains unauthorized; the current result is interface readiness,
not D4-A convergence.

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

1. generate one current, hash-locked set of three physical D4-A snapshots;
2. admit that archive through the existing lifecycle and freeze an independent
   D4-A reference with the unchanged convergence gate;
3. only then run one separately authorized, bounded physical convergence
   census with no empirical parameter or automatic retry.

The method remains the same 370-group, fixed rank-two basis, three-snapshot
Synthesis-POD iteration.  The historical five-temperature campaign is not
imported, and no D4-A reference currently exists.
