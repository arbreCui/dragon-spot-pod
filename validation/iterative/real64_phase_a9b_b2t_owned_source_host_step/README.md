# Phase-A9b B2t: owned-source host step

B2t is a narrow ownership boundary above the existing B2k, B2n, and B2s
production routines.  It adds no radial equation, empirical parameter,
relaxation factor, damping rule, clipping rule, or fitted coefficient.  Its
purpose is to keep the complete source-producing chain inside one subroutine
call:

```text
one PROJECTED/1 parent + three candidate SYSTEM objects
                         |
                         | private B2K commit
                         v
                 private ASSEMBLED/1

the same PROJECTED/1 parent
                         |
                         | private B2N builds, p=1,2,3
                         v
          three private (MACRO0, FROZEN-QFIS/1) pairs

private ASSEMBLED + the three still-live private pairs + TRACK_f
                         |
                         | B2S(enable=.true.)
                         v
                     RETURNED/1
```

No caller-produced `ASSEMBLED`, `MACRO0`, `FROZEN-QFIS`, or `SOLVED` object
enters this API.  The only physical-state inputs are one `PROJECTED/1` archive
and the three candidate radial SYSTEM objects.  `TRACK_f` remains one external
execution handle.

## Default-off API

The production API is

```fortran
call SPOR64_B2T_HOST_STEP(ipout,ipprojected,ipsystems,iptrack_file, &
    status,cutoff_by_plane,enable)
```

`enable` is optional.  If it is absent or false, B2t sets

```text
status = DISABLED
cutoff_by_plane = [0,0,0]
```

and returns before the first pointer-association test, LCM query, private
object creation, B2k call, B2n call, or B2s call.  Merely compiling or linking
B2t therefore cannot start assembly, source construction, or radial work.

When enabled, `ipout` must be one fresh memory-backed LCM root.  The output,
PROJECTED archive, TRACK_f handle, and all three SYSTEM objects must be
associated and mutually non-aliasing in every semantically meaningful pair;
the three SYSTEM objects must also be pairwise distinct.  B2t does not mutate
the caller LCM inputs.  It forwards the `TRACK_f` handle unchanged, but this
low-level routine does not verify the operating-system file mode or identity.

## Owned execution order

After complete public preflight, B2t opens exactly one private ASSEMBLED root,
three private MACRO0 roots, and three private source roots.  The production
calls then occur only in this order:

```text
B2K(PROJECTED,SYSTEM[1:3])
  require ARCHIVE_ASSEMBLED

for p = 1,2,3
  B2N(PROJECTED,p,MACRO0[p],SOURCE[p])
  require COMMITTED
end for

B2S(output,private-ASSEMBLED,private-MACRO0,private-SOURCE,TRACK_f,
    enable=.true.)
  accept only RETURNED
```

All three B2n pairs are committed before B2s is entered.  B2s then retains its
existing all-seal-first `B2O(3) -> B2B CONT(3) -> B2R(1)` ordering.  B2t never
accepts a detached result that a caller could substitute between source
construction and radial execution.

Every recoverable failure after private creation closes all private sources,
macros, and the ASSEMBLED root.  B2t itself performs no direct caller-visible
LCM publication.  The first possible `ipout` mutation remains the final B2r
publication owned by B2s.  This is a logical same-process boundary, not an
ACID, rollback, crash-safety, or `fsync` guarantee.

The three INT64 `cutoff_by_plane` values remain diagnostics owned by canonical
plane label.  They are initialized to zero, passed through from B2s, never
summed, never compared for acceptance, never fed into a solver, and never
written into `RETURNED/1`.

## Exact provenance scope

B2t proves same-call custody of these relations:

- the private ASSEMBLED archive is the B2k result admitted from this PROJECTED
  parent and these three candidate SYSTEM objects;
- every private MACRO0/source pair is produced by B2n from that same PROJECTED
  parent at the exact canonical plane index;
- those still-live private products are the products passed immediately to
  B2s; and
- caller-produced SOLVED, source, macro, or assembled objects cannot enter the
  chain.

The boundary deliberately does **not** prove that the three candidate SYSTEM
objects were historically produced by same-call host `ASM`.  It also does
**not** prove that the supplied `TRACK_f` handle names the binary tracking file
historically associated with the archived TRACK objects.  `FILUNIT>0` and
`LINK.FTRACK='TRACK_f'` are structural checks, not file-identity evidence.

Those two historical claims require a later outer host that is default-off
before any ASM call, creates all three candidate SYSTEM objects, and passes the
same still-live sequential-binary handle into B2t.  Its provenance receipt
must bind construction of the archived TRACK objects to that exact file.  A
bounded validation run must additionally use a private read-only copy and
verify its exact SHA-256 before and after execution.  The before/after hash
proves that the tested bytes did not change; it does not prove historical
TRACK identity by itself.  This evidence is not a physical coefficient or an
acceptance tolerance.

## Short validation boundary

The static checker and 49 targeted mutations freeze the API, zero-access OFF
prefix, alias and freshness rules, private object inventory, strict
`B2K -> B2N(1,2,3) -> B2S(.true.)` order, status predicates, cleanup paths,
and diagnostic-only cutoff.

The seconds-scale orchestration gate uses deterministic stubs solely to
witness call order, private pointer custody, status propagation, cleanup, and
output freshness.  A separate content gate executes production B2n exactly
three times from the same frozen PROJECTED parent while B2k and B2s remain
capture stubs.  A GANLIB-only posterior runs twice and checks 15,540 REAL64
QFISS values, their 15,540 REAL32 DSOUR projections, 1,110 QINT projections,
284,160 positive-zero NUSIGF values, and recursive bit identity of every other
MACRO record.

Neither gate is a true radial transport execution.  They cannot establish
candidate-SYSTEM ASM history, TRACK_f file identity, radial convergence,
outer Picard convergence, SPOD accuracy, eigenvalue accuracy, benchmark
agreement, or `CLOSED/1`.

No long calculation, Dragon process, real ASM call, production transport
solve, axial solve, or Picard map is authorized by this static phase.
