# Phase-A9b B2r: label-bound returned archive

B2r implements the smallest archive boundary for three supplied committed
`SOLVED/1` radial-state objects.  It does not solve transport, assemble a
response matrix, update the axial eigenvalue, or close a Picard iteration.

The production module accepts only

```text
fresh output
+ one ASSEMBLED archive
+ three detached SOLVED objects
+ three detached FROZEN-QFIS source objects.
```

There is no caller-supplied plane, `RHO`, eigenvalue, epoch, tolerance,
relaxation factor, or fitted coefficient.  Both detached triples must carry
the exact plane-label set `{1,2,3}`.  The collector reads those labels and
binds by label; argument order has no meaning.  Duplicate, missing, out-of-
range, aliased, malformed, or cross-plane objects are rejected before the
first output write.

## Physical scope

For the currently implemented generation, the input relation is

```text
ASSEMBLED/1, rho_0
+ SOLVED(p)/1, rho_0
+ FROZEN-QFIS(p)/1, rho_0
          -> RETURNED/1, p = 1,2,3.
```

`RHO` is compared by its binary64 bits.  `EPOCH`, plane labels, the SYSTEM
`SPOT-L1-SNAP`, the solved leakage, the radial key map, and the frozen-source
eigenvalue representation must all agree with the same archive index.  No
numerical tolerance or repair path is used.

The collector proves exact label/index binding for the fields listed below,
bitwise binding for the admitted numerical fields, and recursive same-index
copying of `TRACK`, `MICROLIB2`, and `SYSTEM`.  It does not claim to validate
the full physical semantics of every recursively copied nested record.  The
detached `SOLVED` schema has no cryptographic or other sealed SYSTEM/QFISS
lineage digest, so B2r alone does **not** prove that an arbitrary solved object
was historically produced by those particular inputs.  That stronger causal
statement would be valid only when the collector is invoked on an immediate
integrated `B2O -> B2B -> B2R` host path, or after a future non-empirical
sealed tuple receipt is introduced.  This phase does not implement that host
integration.

## Returned schema

The returned archive root is exactly

```text
SIGNATURE, LISTDIM, TRACK, MICROLIB2, SYSTEM, FLUX, SPOT-R64
```

and its aggregate authority is exactly

```text
NPLANE=3, STATE=RETURNED, EPOCH=1.
```

The root intentionally has neither `RHO` nor `SPOT-ITER-K`.  The three radial
equations used the current outer-state `rho_0` and `k_0`, while a later axial
solve may produce `rho_1` and `k_1`.  Keeping the old value off the returned
root prevents the two scopes from being conflated.  `SPOLEAK` is the later
owner of the new root `SPOT-ITER-K`; only a separate close gate may publish
`CLOSED/1` and root `rho_1`.

`TRACK`, `MICROLIB2`, and `SYSTEM` are copied recursively from the single
`ASSEMBLED` archive by list index.  Each returned `FLUX` child is constructed
from the detached `SOLVED` object with the matching label.  Its authoritative
directory is exactly

```text
RHO, FLUX, SOUR, QFISS, STATE=SOLVED, EPOCH.
```

The detached `PLANE` record is removed after insertion because the archive
list index is then the sole plane identity.  The type-4 `QFISS` is preserved
from the matching frozen source.  The child also receives the compatibility
records required by the existing fixed-source branch of `SPOASM`:

```text
SPOT-FS-EQN = 1
SPOT-FS-K   = verified outer-state k_0 used by the radial equation, in binary32
SPOT-QFISS  = one prescribed binary64-to-binary32 projection of QFISS.
```

The source's type-2 `DSOUR` mirror must already be bit-identical to that
projection; the collector copies the verified mirror.  Terminal `SOUR` is
never used as `QFISS`.  In `SPOASM`, `QFISS` is the frozen fission contribution
and final off-group scattering is added separately, whereas terminal `SOUR`
is the completed radial right-hand side used for a lag diagnostic.  When
off-group scattering is nonzero, treating them as interchangeable would
double-count that contribution and erase the meaning of the frozen equation.
Their values are not required to be unequal; their roles and provenance are
distinct.

Within B2r, child `EPOCH` is rewritten after `QFISS` and `PLANE` changes, and
the root `EPOCH` is the final caller-visible collector mutation.  These are
logical in-process commits, not filesystem transactions.

## Short validation

Run:

```sh
make spot-real64-phase-a9b-b2r-returned-archive
```

The default gate uses deterministic in-memory LCM fixtures.  The successful
synthetic case deliberately supplies solved order `[3,1,2]` and source order
`[2,3,1]`, then verifies that the output is ordered by the labels.  Targeted
negative cases cover plane-set completeness, aliases, exact inventories,
`RHO`, epoch, SYSTEM snapshot/leakage, radial key maps, K provenance, type-4
`QFISS`, the type-2 `DSOUR` mirror, a forbidden `SOUR` fallback, and fresh
output semantics.

An independent posterior program does not link the B2r module.  It opens the
temporary output read-only and checks every type-4 and compatibility payload
bit, all three same-index copies, the absence of child `PLANE`, and the
absence of root `RHO`, `SPOT-ITER-K`, `AX_NEXT`, and `CLOSED`.  Its two reports
must be byte-identical.

The linked test executable is rejected if it contains `SPOASM`, ASM, FLU,
SPOSTATE, SPOLEAK, SPOMOC, XDRTA2, Dragon, or a production transport core.
No radial or axial solve, production ASM, Dragon run, or Picard map is
executed.  Therefore B2r does not claim `CLOSED/1`, `rho_1`, radial
convergence, outer convergence, or benchmark accuracy.
