# REAL64 Phase-A4 compile-only A2-to-A3 host closure

## Status

Phase-A4 encodes the missing synchronous call shape between the checked
Phase-A2 full-matrix façade and the Phase-A3 legacy ABI seam:

```text
IMPLEMENTED-COMPILE-ONLY-A2-A3-HOST-CLOSURE
CONTEXT-STORAGE-SCHEMA=CLOSED
REAL-CONTEXT-PROVENANCE=UNBOUND
A4-OBJECT-LINKS=0
A4-OBJECT-EXECUTIONS=0
PREREQUISITE-SYNTHETIC-LINKS=2
PREREQUISITE-SYNTHETIC-EXECUTIONS=2
TRACKING-READS=0
TRANSPORT-SOLVES=0
DRAGON-RUNS=0
OUTER-CONVERGENCE=NOT-EVALUATED
```

This is Phase-A4 of the REAL64 implementation route.  It is unrelated to
the project’s numerical Stage-4 qualification result.

## What is now encoded

The validation-only module defines a caller-owned `SPOR64_A4_CONTEXT` and
one outer procedure:

```text
MCGFL1R64_A2_A3_HOST_CLOSURE_COMPILE_ONLY_LOCKED
```

The exact static call chain is:

```text
A4 default-off wrapper
  -> MCGFL1R64_POST_STIS_RAW_FACADE_LOCKED
     -> internal host-associated callback
        -> MCGFCF_MCGFST_R64_COMPILE_ONLY_LOCKED
           -> unresolved Phase-A3 link barrier
           -> MCGFCF
           -> MCGFST
```

The internal callback is passed synchronously and never stored or returned.
This is the standard Fortran 2008 host-association mechanism: the callback
receives the Phase-A2 `NGEFF`, `KPN`, `NGIND`, `NCONV`, `SOURCE`, and
`RAW_RESPONSE`, while the remaining shared arrays retain one identity as
outer A4 dummies.

The context contains only data that Phase-A3 needs in addition to the
Phase-A2 interface:

- the default-off `enabled` switch and `IFTRAK`, `NBTR`, `NMAX`, `NBATCH`;
- owned allocatable `CAZ0/1/2`, `CPO`, `ZMU`, `WZMU`, `ISGNR`, `XSI`,
  `PJJIND`, `VOLUME`, and the `KPSYS` handle array.

It has no Fortran pointer component, procedure pointer, type-bound
execution, `SAVE`, `COMMON`, or module-level mutable singleton.  Its
allocatable containers are owned and contiguous.  The sequential file unit
and the external objects referenced by `KPSYS` remain borrowed resources.

## Why exactly two REAL64 staging matrices exist

The frozen Phase-A2 callback interface does not declare its `SOURCE` and
`RAW_RESPONSE` assumed-shape dummies `CONTIGUOUS`.  Adding that attribute
to the internal callback changes its procedure characteristics and fails
strict compilation.  Passing them directly to the Phase-A3 contiguous
interface creates compiler-generated temporaries.

Phase-A4 therefore makes the adaptation explicit:

```text
verify callback dimensions and host NGIND/NCONV identity
allocate source_a3 and raw_a3 as REAL64
source_a3 = local_source
raw_a3    = local_raw_response
call Phase-A3 with the two contiguous matrices
copy raw_a3 back only when Phase-A3 returns OK
```

There are exactly two staging arrays.  They keep the same REAL64 kind and
introduce no interpolation, relaxation, clipping, fit, tolerance, empirical
coefficient, or mathematical model.  `SOURCE` is never copied back by the
callback.  On an allocation, identity, or Phase-A3 status failure, the
callback does not copy `RAW_RESPONSE`; Phase-A2 then preserves its existing
caller-matrix transaction rule.

## What the carrier does not prove

Declaring typed storage is not provenance validation:

- `IFTRAK`, `NBTR`, and `NMAX` do not prove that the sequential tracking
  stream is open or positioned at the first track record;
- every future `MCGFCF` call consumes the complete `NBTR` stream, so an
  online iteration must reposition it before every call;
- associated `KPSYS` handles do not prove live `PJJ$MCCG` directories,
  group ordering, geometry identity, or lifetime;
- `PJJIND` is not yet proved to come from the same tracking object;
- `MCGSCA` still depends on the hidden legacy `/EXP1/` table initialized
  in the same process image;
- the legal context-owned `XSI` vector does not repair the production
  `XSIXYZ(1,IDIR)` expression at `IDIR=0`;
- public context components can be populated incorrectly, so their source
  kind and cross-object identity remain unchecked.

Legacy `MCGFCF` and `MCGFST` have no recoverable error status and may call
`XABORT`.  The matrix copy-back protocol is transactional for ordinary
nonzero callback returns; it cannot make the tracking-file position or
process state transactional after legacy entry.

## Short compile-only gate

Run:

```sh
make spot-real64-phase-a4
```

The isolated target first checks the frozen Phase-A3 scoped receipt and
runs the Phase-A2 prerequisite (which recursively runs Phase-A1), then:

- verifies the scoped receipt, canonical manifest, checker, and mutations;
- compiles Phase-A1, Phase-A2, Phase-A3, Phase-A4, and a subroutine-only
  anchor using explicit source lists and object-only commands;
- rejects REAL32 mutable state, a wrong context type, a noncontiguous
  mutable actual, and global default-REAL promotion;
- checks exact unresolved-symbol sets for the A3, A4, and anchor objects;
- rechecks that the Phase-A3 link barrier remains unresolved and that no
  object contains an executable entry point.

The older Phase-A3 runner is not invoked because its own historical
Makefile proof intentionally accepts only the pre-A4 Makefile.  Phase-A4
does not weaken or edit that frozen proof: it hash-locks the A1/A2/A3
receipts, checks the A3 receipt contents, recompiles the unchanged A3 source
with the strict object-only flags, and rechecks its exact unresolved
link-barrier set.

No Phase-A4 object is linked or executed.  The recursive prerequisite chain
runs the already-frozen Phase-A1 and Phase-A2 synthetic programs; each is
compiled, linked, and executed once, but neither is a tracking or MOC
calculation.

The exact diagnostic and unresolved-symbol receipt is intentionally locked
to GNU Fortran 15.2.0 (Homebrew GCC 15.2.0_1), locale `C`, on Darwin arm64.
Another compiler or platform needs a separately reviewed receipt; this gate
makes no cross-toolchain portability claim.  `-Warray-temporaries -Werror`
is compiler evidence for these checked A3/A4 object compilations, not a
language-level proof about every possible compiler.

## Next threshold

The next permitted step is a separate compile-only Phase-A5 population and
provenance contract.  It must map each context field to the real `MCGFL1`
host source, preserve legal `XSI`, specify exact tracking repositioning,
and bind the `KPSYS/PJJ`, geometry, material, group-order, and `/EXP1/`
identities without removing the Phase-A3 link barrier or executing
transport.  Actual MOC execution still requires a later explicit gate.
