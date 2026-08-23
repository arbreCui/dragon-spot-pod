# Second-case contract: IRENA D4-A 1/12 assembly

## Status

`ASSEMBLED_TO_CLOSE_RUNTIME_GEOMETRY_PASSED_NO_TRANSPORT`.

No Dragon or OpenMC process was started for this case.  The purpose of this
record is to choose the next independent geometry without changing the
accepted SPOD equations or starting a long calculation prematurely.

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

- `SPOR64_B2B` obtains `NREG`, `NMAT` and `NUNKNO` from the actual TRACK
  object and independently checks the long-vector records;
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

The remaining strict lifecycle is not yet D4-A ready:

- `SPOR64_B2H/B2I/B2J`, which form or bootstrap the next PROJECTED epoch,
  still retain pin-specific geometry assumptions;
- historical validation builders also assume the pin-cell dimensions.

Consequently D4-A must not be run with the current strict chain.  A failure
would be an interface-dimension failure, not a physical convergence result.

## Completed vertical slices

`SPOR64_B2C` now derives `NREG`, `NMAT` and `NUNKNO` from its actual arrays
and allocates its publication staging accordingly.  The group count remains
the declared 370-group problem.  No tolerance, gate, equation, snapshot
count or physical parameter changed.

The no-transport manufactured test uses

- `FLUX64(138,370)` and `SOUR64(138,370)`;
- `KEYFLX(132)=1,...,132`;
- `IMERGE(6)=1`.

Here 138 is deliberately only a structural test dimension.  It is not a
claim about D4-A's real number of transport unknowns; that value must later
come from the actual `TRACK/STATE-VECTOR`.

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
`NZON$MCCG` and `KEYCUR$MCCG` extents to agree.  The current legacy MCCG
kernels genuinely support six outer surfaces, so this route retains the
strict relation

```text
NUNKNO = NLONG = NREG + 6
```

rather than claiming unsupported arbitrary surface counts.  `SPOR64_A9`
and `SPOR64_A8` now derive the remaining geometry dimensions from their
actual arrays and TRACK records.  They do not change the 370-group operator,
iteration order, physical coefficients, tolerances or terminal predicates.

A seconds-scale no-transport test admits both `(8,8,14)` and manufactured
`(132,6,138)` shapes through the A8/A9 interfaces and verifies fail-closed
entry with null transport handles:

```sh
make spot-a89-dimensions
```

The result is recorded in
[the A8/A9 runtime-geometry result](a89_runtime_geometry_result.md).

The connected `B2K/B2N/B2S/B2R/B2W` sources compile under the strict
REAL64 flags with runtime region, material and unknown extents.  A frozen
pin-cell no-Dragon replay independently admits RETURNED (`STATUS=3`) and
closes epoch 69 (`STATUS=2`); both CLOSED XSM files retain their exact
SHA-256 hashes.  This proves backward compatibility and lifecycle/write
ordering, not D4-A transport or D4-A convergence.

## Remaining work before a physical run

The remaining code work is dimension generalization and one structural
fixture only:

1. pass the same authoritative dimensions through `B2H/B2I/B2J` without
   changing their equations;
2. keep the current 370-group equations, fixed rank two, strict REAL64
   leakage lifecycle and unchanged three-defect `5e-7` gate;
3. keep the current method's three snapshots for this second case; the
   historical five-temperature campaign is not imported;
4. complete a full-chain no-transport 132-region admission and retain the
   existing pin-cell regression before any physical run.

Only after those four checks pass may a separately authorized D4-A physical
run be prepared.  A new independent OpenMC reference will also be required;
none currently exists for this case.
