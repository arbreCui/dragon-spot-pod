# Phase-A9b B2s: default-off immediate host bridge

B2s adds one narrow orchestration boundary.  It does not change the radial
equation, the B2B acceptance predicates, the B2R returned schema, or the
outer 2D/1D iteration.  Its purpose is to remove the detached-`SOLVED`
provenance gap identified at B2r: when explicitly enabled, the three objects
given to B2R are the still-live private outputs of the immediately preceding
B2B calls, not objects supplied later by a caller.

## Default-off boundary

The final `enable` argument is optional.  If it is absent or false, the call
returns

```text
status = DISABLED
cutoff_by_plane = [0,0,0]
```

before the first object association test, LCM query, scratch-object creation,
or B2O/B2B/B2R call.  Thus merely linking B2s cannot start radial work or
touch a caller object.  This phase does not enable a production call site.

When enabled, the public input boundary is only

```text
fresh output
+ one ASSEMBLED/1 archive
+ three detached MACRO0 objects
+ three detached FROZEN-QFIS/1 objects
+ one shared TRACK_f handle.
```

There is no external `SOLVED` object and no caller-supplied plane, `RHO`,
eigenvalue, epoch, tolerance, relaxation factor, damping factor, or fitted
coefficient.  The numerical controls passed to B2B are the pre-existing
frozen controls of the admitted Phase-A path; B2s adds no empirical physical
or coupling parameter.

## Immediate causal order

The enabled state machine is exactly

```text
three same-slot (MACRO0, FROZEN-QFIS) inputs
                 |
                 | B2O seals all three source-selected pairs
                 v
       sealed PLANE labels must be exactly {1,2,3}
                 |
                 | canonical p=1,2,3
                 | B2B CONT; require HOST_COMMITTED each time
                 v
       three private, still-live SOLVED/1 objects
                 |
                 | one B2R call, only after all three commits
                 v
                    RETURNED/1
```

All three B2O calls and the complete label-set check occur before the first
B2B call.  A duplicate, missing, or out-of-range sealed plane therefore fails
without entering the radial core.  The source label selects its archive seed
and SYSTEM through B2O; the `MACRO0` in the same caller slot follows that
source into the corresponding canonical-plane B2B call.  B2S accepts only
`SPOR64_B2C_HOST_COMMITTED`.  A partial sequence never reaches B2R, and B2R is
called exactly once after the three accepted calls.

The caller output is not used as any radial workspace.  Seeds, systems, and
solved objects are private LCM scratch objects.  The first possible
caller-visible archive mutation remains inside the final B2R publication.

## Physical and provenance scope

This immediate custody proves a stronger local statement than B2r could make
from detached metadata alone: the collected `SOLVED/1` objects are exactly
the outputs committed by these three B2B invocations under these sealed
source/SYSTEM pairs in the same subroutine call.

The statement is deliberately not enlarged.  Current object schemas do not
encode a receipt proving that a detached `MACRO0` was historically derived
from the same-index `ASSEMBLED/MICROLIB2` payload, or that the same-slot
`MACRO0` and `FROZEN-QFIS` were historically generated as siblings.  Read-only
sharing between `MACRO0` slots is allowed and is not treated as lineage
evidence.  The shared `TRACK_f` handle likewise has no encoded historical
identity binding to the archived `TRACK` objects.  Same-slot use is an
explicit host contract, not a reconstructed history claim.

The per-plane INT64 `cutoff_by_plane(p)` values are diagnostics only.  They
are initialized to zero, written only by the corresponding canonical B2B
call, never summed, never compared for acceptance, never fed back to the
solver, and never written into `RETURNED/1`.

## Short validation boundary

Run the complete short gate with

```sh
make spot-real64-phase-a9b-b2s-immediate-host-bridge
```

Its static and mutation portion freezes the OFF-before-access ordering, the public ABI, the all-seal-first
label check, the same-slot mapping, canonical B2B order, strict
`HOST_COMMITTED` gate, final one-shot B2R collection, and diagnostic-only
cutoff.  Forty-five targeted mutations must be rejected.

The accepted seconds-scale linked gate uses production B2O, B2B, B2C, B2R,
and B2s orchestration with an explicit deterministic terminal-core stub.  It
does not link or execute the production A9 transport implementation, Dragon,
an axial solve, or a Picard map.  Such a stub proves interface, ordering,
status, publication, and REAL64 custody; it is not a true radial transport
solve and cannot prove radial convergence, outer convergence, or benchmark
accuracy.  `RETURNED/1` also remains unclosed.

The accepted run completed in under four seconds.  It checked omitted and
explicit OFF calls with null pointers, one duplicate-label rejection before
the core, one plane-2 core failure with an empty caller output, and one
successful source order `[2,3,1]` whose radial order was `[1,2,3]`.  Two
independent GANLIB-only posteriors agreed byte for byte.  REAL64 and REAL32
FLUX, SOUR, and QFISS were each checked for all 15,540 values.  No Dragon,
ASM, SPOASM, FLU, A8, production A9, true transport solve, or Picard map was
linked or executed.
