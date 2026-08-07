# Phase-A9b B2l: bounded real one-plane ASM

B2l executes the smallest real radial-operator step needed after B2k.  It
materializes the complete three-plane `PROJECTED/1` archive from the frozen
state, then runs production `ASM: ... ARM LK1D 1` for plane 1 exactly once.
It does not call `FLU`, construct `QFISS`, invoke `SPOR64K`, enter `CONT`, or
perform a Picard update.

```text
frozen AX/archive/tracking
  -> production B2C x3 -> B2I -> B2J -> persistent PROJECTED/1
  -> production ASM, plane 1 only -> fresh L_PIJ SYSTEM
```

## Physical identities

The independent posterior checks the actual production `ASMDRV` result for
every group and material slot in the order used by the binary32 code:

```text
TXSC[0]   = +0
TXSC[m]   = NTOT0[m] - TRANC[m]

S0PHYS[0] = +0
S0PHYS[m] = SIGW00[m] - TRANC[m]

S0USED[0] = +0 - LEAK1D
S0USED[m] = S0PHYS[m] - LEAK1D
```

`S0USED` is the stored `DRAGON-S0XSC`.  The subtraction is checked as two
ordered binary32 operations; reassociation is not accepted.  No damping,
relaxation, clipping, floor, fitted closure, or empirical coefficient is
present.

## Real input, not a reduced fixture

The materializer deep-copies the full real `TRACK`, `MICROLIB2`, and lagged
`SYSTEM` objects into a private upstream candidate.  Historical binary32
`FLUX` and `SOUR` values are promoted exactly to binary64 and published
through production B2C; no ULP perturbation is added.  Production B2I seals
the epoch, and production B2J writes the final projected archive directly to
a new XSM file.  B2J is the final content-mutating owner; after it returns,
the materializer only closes the file.

GANLIB's `LCMINF` reports the storage medium separately from root freshness.
B2l therefore permits B2J to use either an in-memory LCM root or a persistent
XSM root while retaining the same strict requirements: the active object is
an empty associative-table root with length `-1` and name `/`.  The controlled
caller additionally requires a previously nonexistent output path and opens
it for modification.

This is a logical commit-marker transaction, not an ACID or power-failure
transaction.  `PROJECTED/EPOCH=1` is written last and is the only completion
marker.  A file without that marker is wholly invalid; no rollback, `fsync`,
or crash-recovery claim is made.

## Persistent-target lifecycle qualification

The default, no-Dragon preflight dynamically calls production B2J six times
against fresh or deliberately invalid XSM targets.  One fresh target commits;
five targets are rejected: a nonempty sentinel, a deleted-record tombstone,
an early invalid AX epoch, a plane-2 late B2H rejection, and a plane-3 late
B2H rejection.  Every target is closed and reopened read-only before its
persisted state is accepted.

The positive file must have the exact seven-entry projected inventory, no
`SYSTEM`, and exact `PROJECTED/1` authority.  It also checks six nested
`TRACK`/`MICROLIB2` deep copies and all 15,540 binary32 mirror downcasts.  The
three rejected fresh files must reopen strictly empty; the sentinel must
remain the sole logical record; and the tombstone must remain physically
nonfresh before and after reopen.  This bounded harness links production
B2C/B2I/B2H/B2J plus GANLIB/UTILIB only.  It links and runs no Dragon, ASM,
transport solver, B2K, FLU, or CONT and introduces no model coefficient.

## Independent posterior

The checker links only GANLIB and UTILIB.  It does not link ASM, a transport
solver, or any SPOR64 lifecycle module.  It reopens both XSM outputs and:

- recursively bit-compares the complete projected `TRACK` and `MICROLIB2`
  trees against the frozen source for all three planes;
- requires the exact projected lifecycle/root inventory and absence of the
  lagged `SYSTEM` list;
- requires the real plane-1 `L_PIJ` root plus 370 group directories, each
  with the exact five ACA, seven PJJ, and three cross-section records;
- requires all 59,940 response values to be finite and rejects an entirely
  zero response payload;
- checks 3,330 ordered binary32 values in each of `TXSC`, `S0PHYS`, and
  `S0USED`, including the plane-1 projected leakage.

The accepted run found 69,021 full-copy records containing 54,429,912
32-bit words.  All 59,940 response values were finite and 35,518 were
numerically nonzero with both `+0` and `-0` excluded.  The evidence hashes and
the transparent history of discarded and superseded
development attempts are frozen in [runtime_result.txt](runtime_result.txt).

These checks establish real ASM execution, complete finite response schema,
and compatibility with the B2k plane-1 formula contract.  They do **not**
establish response-matrix numerical accuracy, planes 2/3, the three-plane
`SPOR64K` commit, a radial flux solve, radial convergence, or outer Picard
convergence.

## Run

The default target performs strict compilation, symbol isolation, 47
mutation/resource tests, and the bounded no-Dragon XSM lifecycle qualification:

```sh
make spot-real64-phase-a9b-b2l-one-plane-real-asm
```

Its terminal claim remains `DRAGON-EXECUTIONS=0 ASM-EXECUTIONS=0`; the XSM
harness is lifecycle evidence, not a transport calculation.  The bounded real
smoke is an explicit opt-in:

```sh
RUN_B2L=1 make spot-real64-phase-a9b-b2l-one-plane-real-asm
```

One activation permits one materializer and one Dragon process.  The default
XSM harness and opt-in materializer each use the 30 s wall / 20 s CPU / 2 GiB
RSS profile; ASM has 15 s wall / 10 s CPU / 1 GiB RSS limits.  Both use a
fresh process group and single-thread
environment, and the runner contains no retry path.  `PRESERVE_B2L_FAILURE=1`
may retain a failed temporary case for read-only diagnosis; it defaults off
and has no effect on the calculation.
