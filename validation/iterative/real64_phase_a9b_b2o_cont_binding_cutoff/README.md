# Phase-A9b B2o: sealed CONT predicates and cutoff observation

B2o closes two audit gaps immediately before a future bounded radial solve.  It
does not execute `FLU`, Dragon, transport, or a Picard map.

## Joint CONT admission

`SPOR64_B2B_INGRESS` previously checked the type-4 `FLUX` and `QFISS`
payloads independently.  A seed, frozen source, and response system from
different lifecycle states could therefore reach the REAL64 core together.
B2o keeps the public ABI unchanged and adds one read-only joint admission,
only for `R64 CONT`:

```text
seed/SPOT-R64:   RHO, PLANE, FLUX, STATE=PROJECTED, EPOCH=1
source/SPOT-R64: RHO, PLANE, STATE=FROZEN-QFIS, QFISS, EPOCH=1
system/SPOT-R64: RHO, STATE=ASSEMBLED, EPOCH=1
system root:     SPOT-L1-SNAP
```

All three authority inventories are exact.  The three positive finite `RHO`
values must be bit-identical binary64 values; all three epoch stage labels
must equal 1.  Seed and source `PLANE` must be identical, in `1:3`, and equal
`SYSTEM/SPOT-L1-SNAP`.  The 370 seed and SYSTEM `SPOT-LEAK1D` binary32 values
must also be bit-identical.  No tolerance, repair, fallback, fitted
coefficient, relaxation, clipping, or normalization is available.  A failure
returns the existing admission-failed token, leaves the fresh output empty,
keeps the cutoff count zero, and cannot call `XDRTA2` or the core.

BOOT's numerical and admission path retains its one-time legacy promotion and
is not broadened by this gate; it does gain the same host audit line.

### Sealed same-index pair

The old PROJECTED seed authority contains no `PLANE` record.  Production
`SPOR64_B2O_SEAL_CONT_PAIR` therefore accepts one committed `ASSEMBLED/1`
archive and one frozen source, reads `PLANE` only from the source, selects the
seed and SYSTEM at that same archive-list index, and publishes two fresh
objects.  It adds the derived plane to the seed and rewrites each object's
`EPOCH` as its final authority mutation.  The API accepts no independent
caller plane, `RHO`, or epoch scalar, coefficient, or tolerance; the committed
source authority owns the selected plane.

This proves same-index selection inside the supplied archive and all stated
cross-object predicates.  `EPOCH=1` is a local pipeline stage label, not a
globally unique transaction or parent identifier.  Distinct external runs
with coincidentally identical labels are not distinguished by the object
schema; the validation receipt pins the concrete parent evidence used here.

The current B2C terminal authority also contains only `FLUX` and `SOUR`, not
`RHO/PLANE/STATE/EPOCH`.  Its output therefore cannot be fed directly into a
second strict CONT call.  B2o proves one sealed, same-index predicate-satisfying
ingress, not a repeated continuation chain or Picard convergence.

## ACA cutoff observation

The inherited ACA cutoff is still the exact promotion of Dragon's binary32
`1.0e-7`; B2o adds no cutoff and changes no physical branch.  Along the live
trajectory, existing instrumentation compares each reached local predicate
with an exact-zero-cutoff counterfactual.  The returned integer is the number
of local Boolean outcomes that differ.  It is **not** the total number of guard
evaluations and is not a complete zero-cutoff rerun.

The count already propagates as `INT64` through A8, A9, and B2B.  B2o adds one
unconditional host observation in `FLU`, after B2B returns and before status
dispatch:

```text
SPOR64 R64 MODE=.. STATUS=.. ACA-CUTOFF-LOCAL-PREDICATE-DIFFERENCES=....................
```

The count does not participate in a physical, acceptance, or convergence
criterion and is never written into a physical LCM/XSM authority.  A9 retains
only fail-closed nonnegative/`INT64`-overflow integrity checks before addition;
the count is otherwise diagnostic evidence.  The FLU observation is also
present when a core returns normally with a non-accepted or failed status.

## Short validation

Run:

```sh
make spot-real64-phase-a9b-b2o-cont-binding-cutoff
```

The target performs strict free-form and fixed-form compilation, 25 mutation
tests, static data-flow checks, and one small GANLIB-backed synthetic harness.
The harness executes the production B2o sealer and production B2B/B2C
boundaries but replaces the transport core and `XDRTA2` with narrow stubs.
Seven direct sealer calls include two positive source-selected planes and five
fail-closed inputs; rejected calls publish no partial seed or SYSTEM.  One of
the two sealed pairs continues through B2B and returns the `INT64` sentinel
`4294967311`, deliberately above the 32-bit range.  Thirty-two negative
lifecycle cases—including zero,
negative, infinity, and NaN for every `RHO` owner—must all stop before the
stub boundary.  Every one of the 10,360 type-4 seed/source values has a
deterministic REAL64-only low-bit witness and is checked at the core ABI both
for exact identity and against an R64-to-R32-to-R64 round trip.  The three
synthetic archive planes additionally carry distinct exact-ULP multipliers;
the plane-2 sealer case checks every selected type-4 FLUX value, so a wrong
seed-list index cannot pass by payload coincidence.

The controlled inventory is:

```text
REAL-B2B-CALLS=33
SEALER-CALLS=7
SEALER-POSITIVES=2
SEALER-REJECTIONS-BEFORE-PUBLICATION=5
SEALED-B2B-INGRESS-POSITIVES=1
REJECTIONS-BEFORE-CORE=32
STUB-XDRTA2-CALLS=1
STUB-CORE-CALLS=1
STATIC-CONTRACT-TESTS=25
PRODUCTION-FLU-EXECUTIONS=0
DRAGON-EXECUTIONS=0
TRANSPORT-SOLVES=0
PICARD-MAPS=0
```

The strongest B2o claim is:

```text
ONE SEALED SAME-INDEX CONT INGRESS AND INT64 CUTOFF OBSERVABILITY CLOSED
```

It does not establish a radial solution, radial balance, radial or outer
convergence, response-matrix accuracy, SPOD truncation accuracy, eigenvalue or
power accuracy, or comparison with an independent transport code.  Radial and
outer convergence remain `NOT-EVALUATED`.
