# Second-case contract: IRENA D4-A 1/12 assembly

## Status

`INPUT_AUDIT_ONLY_NO_TRANSPORT`.

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

## Current incompatibility

The general core routines `SPOASM`, `SPOPOD` and `SPOT_LEAKAGE` already use
runtime dimensions.  The strict REAL64 lifecycle does not yet do so:

- `SPOR64_A8/A9` assume eight radial regions;
- `SPOR64_B2B/B2C/B2R/B2W` assume combinations of `NREG=8`, `NMAT=8`,
  `NSNAP=3` and `NUNKNO=14`;
- historical validation builders also assume the pin-cell dimensions.

Consequently D4-A must not be run with the current strict chain.  A failure
would be an interface-dimension failure, not a physical convergence result.

## Minimal next implementation

The next code step is dimension generalization only:

1. obtain region, material, unknown and snapshot counts from the existing
   LCM state records;
2. allocate the same fields with those runtime dimensions;
3. keep the current 370-group equations, fixed rank two, strict REAL64
   leakage lifecycle and unchanged three-defect `5e-7` gate;
4. compile and test manufactured 132-region admission without transport;
5. require the accepted pin-cell outputs to remain bitwise unchanged.

Only after those five checks pass may a separately authorized D4-A physical
run be prepared.  A new independent OpenMC reference will also be required;
none currently exists for this case.
