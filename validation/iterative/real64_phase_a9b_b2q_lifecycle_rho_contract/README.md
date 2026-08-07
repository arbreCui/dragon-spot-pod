# Phase-A9b B2q: lifecycle and `RHO` contract freeze

B2q freezes the meaning of the existing REAL64 lifecycle before another
iteration is implemented.  It changes no production source, public ABI,
equation, numerical control, or archive schema.  In particular, it does not
propagate `PLANE` into the archive-contained `PROJECTED` authority.

## Frozen generation convention

Let `CLOSED(n)` denote the accepted axial/archive state that owns `rho_n`.
Only a producer of a new complete `CLOSED` state may introduce a new `RHO`,
and that producer must prove its own frozen binary operation for
`rho_n = 1/k_n`.  The currently implemented bootstrap producer proves

```text
rho_0 = 1.0_real64 / real(K-EFFECTIVE_binary32, real64)
```

bit for bit.  No formula for a future `CLOSED(n+1)` producer is invented by
this phase.

Consequently a future `CLOSED/1` root may legitimately own `rho_1` while its
three child `SOLVED/1` results still carry `rho_0`, the coefficient of the
equations that produced them.  That difference is not a mismatch.  Closing
the next generation requires two separate provenance boundaries:

1. A returned-archive collector binds the three accepted `SOLVED/1` children
   to the same-index SYSTEM, TRACK, MICROLIB2, QFISS, and K inputs.  It emits
   an unclosed returned archive for SPOASM; it neither sees `AX_NEXT` nor
   commits `CLOSED/1`.
2. Only after `SPOASM -> axial FLU -> SPOSTATE -> SPOLEAK` may a separate
   close gate bind that returned archive to `AX_NEXT` and commit `CLOSED/1`.

Matching integer epochs or matching `RHO` values alone is not sufficient
provenance at either boundary.

The work generated from `CLOSED(n)` has the following labels:

```text
CLOSED(n), rho_n
    -> PROJECTED(n+1), rho_n
    -> ASSEMBLED(n+1), rho_n
    -> FROZEN-QFIS(n+1), rho_n
    -> SOLVED(n+1), rho_n
```

`PROJECTED`, `ASSEMBLED`, `FROZEN-QFIS`, and `SOLVED` therefore carry one
binary64 `RHO` value without a tolerance or recomputation.  For the only
implemented production generation this is

```text
CLOSED/0 -> PROJECTED/1 -> ASSEMBLED/1
         -> FROZEN-QFIS/1 -> SOLVED/1,
```

and every state carries the exact `rho_0` bits.  `FROZEN-QFIS/1` uses those
bits in the already frozen source formula.  The accepted radial terminal
state does not compute a new eigenvalue.

B2j's present plane/root `RHO` equality is specifically the bootstrap
`CLOSED/0` archive-projection invariant.  It must not be generalized into a
rule that a future `CLOSED(n)` root has the same `RHO` as its already solved
children; in particular, a future `CLOSED/1` root may carry `rho_1` while its
accepted `SOLVED/1` children retain `rho_0`.

Bootstrap `SOLVED/0` is a sealed archive seed aligned with `CLOSED/0`; it is
not evidence that the historical radial equation was solved with `rho_0`.

## Plane identity

`PLANE` has one owner in each representation.  Inside an archive, the
one-based list index is the sole plane identity and a child authority does not
repeat `PLANE`.  A detached `PROJECTED` seed, detached `SOLVED` result, or
detached `FROZEN-QFIS` source must carry an explicit type-1 `PLANE`; a radial
SYSTEM uses its existing `SPOT-L1-SNAP` record instead of a second authority
label.

The returned-archive collector must therefore admit exactly the label set
`{1,2,3}`, reject duplicates and omissions, bind every detached object to the
same-index SYSTEM/TRACK/MICROLIB2/QFISS/K provenance, and omit the redundant
`PLANE` record after insertion into the archive.  Propagating `PLANE` through
every contained child would create two competing owners without adding a
physical degree of freedom.

## The B2h boundary

The public B2h helper has a deliberately narrower claim.  It checks the seed
`RHO` as a finite positive completeness witness, but publishes the explicit
caller `RHO`.  Its direct output is not a canonical next Picard state.  Only
B2j, or a future archive-level successor, may make that claim after binding
the projected coordinates, axial state, seed, track, `RHO`, and epoch to one
canonical object.  This distinction is tested with two different binary64
`RHO` witnesses.

## Epoch meaning

`EPOCH` is a local generation and logical-commit label.  It is not a global
identifier, solver iteration counter, time step, eigenvalue certificate, or
convergence result.  Within generation 1, `PROJECTED`, `ASSEMBLED`,
`FROZEN-QFIS`, and `SOLVED` all retain epoch 1.  B2C preserves the accepted
seed epoch; it does not increment it.  The existing B2h helper performs the
local `SOLVED(n) -> PROJECTED(n+1)` increment, but its caller-supplied `RHO`
becomes canonical only at an archive-level provenance gate.

## Short validation

Run:

```sh
sh validation/iterative/real64_phase_a9b_b2q_lifecycle_rho_contract/run_phase_a9b_b2q_lifecycle_rho_contract.sh
```

The runner first proves that B2B, B2C, B2H, B2I, B2J, B2K, B2N, and B2O are
byte-identical to the B2p parent versions.  An independent static checker then
locks the cross-module `RHO` and epoch data flow, followed by mutation tests.

The dynamic gate directly rebuilds the existing B2h harness rather than
invoking its old receipt-bound runner.  It checks the explicit noncanonical
seed-RHO/caller-RHO boundary with distinct REAL64-only values.  The B2j and
B2p harness/source pairs and their real-XSM inputs are hash-pinned and audited
statically, but are not re-executed in this contract-only phase.  This keeps
the gate minimal, deterministic, and seconds-scale.

All XSM inputs are opened read-only and checked before and after execution.
The linked B2h executable is rejected if it contains a production transport,
FLU, Dragon, or ASM path.  B2J, B2K, B2N, B2O, B2B, and B2C remain
static-only in B2q; their already validated source contracts are frozen and
audited without executing their physical calculations.

This gate performs strict compilation and small in-memory calculations only.
It does not run Dragon, FLU, transport, ASM, a physical radial iteration, or
an outer Picard map.  The authoritative end state is therefore:

```text
LIFECYCLE/RHO CONTRACT = FROZEN
CURRENT GENERATION-1 DATA FLOW = BITWISE CONSISTENT
SECOND CLOSED ARCHIVE = NOT IMPLEMENTED
RADIAL CONVERGENCE = NOT EVALUATED
OUTER PICARD CONVERGENCE = NOT EVALUATED
```

No relaxation, damping, clipping, fitted tolerance, empirical coefficient,
fallback, or model completion is introduced.
