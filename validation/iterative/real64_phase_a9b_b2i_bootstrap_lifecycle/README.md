# Phase-A9b B2i: archive-wide REAL64 bootstrap seal

B2i closes one narrow lifecycle gap before any online Picard continuation.
It binds one canonical axial `SPOSTATE` bundle to all three radial plane
tuples, then publishes a fresh in-memory AX/archive pair at bootstrap epoch
zero.  It remains disconnected from every shipped host procedure.

The input archive is not the historical binary32 `state1_snapshots.xsm`
alone.  Each input plane must already contain the B2C-style authoritative
binary64 payload

```text
SPOT-R64/FLUX = 370 list items x 14 binary64 values
SPOT-R64/SOUR = 370 list items x 14 binary64 values
```

and that directory must contain exactly those two records.  `RHO`, `STATE`,
`EPOCH` and `QFISS` must still be absent.  The historical artifact is used by
the gate only to supply real AX, axial-track, plane-track and terminal
plane-field data.  For each plane, the test promotes the real `FLUX/SOUR`
values with binary64-only witness bits and calls the production
`SPOR64_B2C_PUBLISH` routine on a fresh root.  Thus B2i consumes an object
created by its real upstream publisher, without running transport.  This also
avoids pretending that the historical 5e-7 solver-metadata bits are the
current B2C contract, whose exact numerical tolerance bits are 2.5e-7.

The admission uses exact schemas and bit identities together with finite and
physical-sign checks.  It uses no fitted or empirical coefficient:

- `RHO` is checked bit for bit against `1/real(K-EFFECTIVE, real64)`.
- Stored POD ranks and flat offsets must reproduce the exact `SPOSTATE`
  layout.  `B`, `A`, `L`, `GRAM`, `H`, `NORM`, `PERP` and `GERR` must have
  their declared kinds and finite values.
- `GRAM` and `GERR` are replayed in the frozen `SPOSTATE` loop order and
  compared bit for bit.  This is an arithmetic identity, not an
  orthogonality tolerance.
- `H` is replayed from `MAT1D/VOL1D`; every plane `VOLUME` equals axial
  `AREA2D` bit for bit.  These are the derived geometry identities retained
  by `SPOSTATE`, not a hash of every axial tracking row.
- Archive `SPOT-ITER-K` is the exact binary64 promotion of the AX
  `K-EFFECTIVE`; every returned plane leakage value is the exact binary64
  promotion stored in canonical `SPOT-X-L`.
- The four lists `TRACK/MICROLIB2/SYSTEM/FLUX` are complete at every common
  index.  Library macrolibs and radial systems have the frozen dimensions;
  `SYSTEM/SPOT-L1-SNAP` equals that index.
- Each legacy binary32 `FLUX/SOUR` value is exactly the downcast of its
  binary64 authority, with an explicit representable-range check before the
  conversion.

`SYSTEM/SPOT-LEAK1D` is required to be finite but is deliberately not equated
to the returned `FLUX/SPOT-LEAK1D`.  In the raw Picard map, `SYSTEM` records
the leakage used for the radial solve (the preceding state), whereas the
closing `SPOLEAK` call updates `FLUX` to the newly returned axial leakage.
The next radial system is rebuilt by `ASM`; treating these two records as one
epoch would erase the actual Picard ordering.

Likewise, the `RHO` stamped on a `SOLVED` plane is the lifecycle label of the
completed outer canonical state being closed.  It does not claim that the
preceding radial equation was solved with that `RHO`; that solve used the
previous Picard state.  Legacy `SPOT-FS-K` remains pass-through diagnostic
data and is never compared with the current AX eigenvalue.

B2i deliberately does not reconstruct `B*A`, solve a radial equation, build
`QFISS`, or judge convergence.  `A` is admitted as part of the finite,
same-root canonical bundle; B2h is the sole next-stage semantic gate that
evaluates `B*A`, checks the projected regional flux, and publishes
`PROJECTED`.  Thus `CLOSED` below means only that the bootstrap pair is
structurally closed, never that a radial or outer iteration converged.

On success, B2i writes only fresh in-memory LCM targets:

```text
each plane SPOT-R64/RHO   = canonical RHO, type 4
each plane SPOT-R64/STATE = SOLVED
each plane SPOT-R64/EPOCH = 0

AX/SPOT-X-STATE = CLOSED
AX/SPOT-X-EPOCH = 0

archive SPOT-R64/RHO    = canonical RHO, type 4
archive SPOT-R64/NPLANE = 3
archive SPOT-R64/STATE  = CLOSED
archive SPOT-R64/EPOCH  = 0        # final LCM mutation
```

The AX root is copied into one fresh target.  A new archive root is then
created and all four same-index lists are copied item by item into fresh
directories.  Historical root transition diagnostics such as
`SPOT-L1-ERR`, `SPOT-PJ-PERP` and `SPOT-PROJECT` are intentionally not
carried into the new epoch: they describe the preceding legacy transition,
not the newly sealed state.  The old one-map checker is therefore not a
sufficient checker for this new lifecycle schema.

All admission rejections occur before the first new write.  When both supplied
targets are fresh they remain empty; a freshness collision leaves its
pre-existing contents unchanged and leaves the other target empty.  GANLIB
allocation or copy failure after the first write is not claimed to roll back:
it aborts with an incomplete pair, and that pair must be discarded because
the archive root has no final `CLOSED/EPOCH`.
Consumers must require both the AX marker and the archive-root marker; the AX
marker alone is not a commit.  Bootstrap epoch zero is a controlled data-flow
label, not a globally unique identifier for arbitrarily mixed persisted
files.  Direct fresh-XSM output is also outside this API: a caller may persist
the validated in-memory pair only after the archive commit.

Run the seconds-scale gate with:

```sh
sh validation/iterative/real64_phase_a9b_b2i_bootstrap_lifecycle/run_phase_a9b_b2i_bootstrap_lifecycle.sh
```

The gate performs strict compilation, static mutation tests and real GANLIB
in-memory checks.  It does not execute Dragon, read the sequential tracking
file, call a transport kernel, construct a fission source, or run a long
calculation.  `RADIAL-CONVERGENCE=NOT-EVALUATED` and
`OUTER-PICARD-CONVERGENCE=NOT-EVALUATED` remain authoritative.
