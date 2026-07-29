# REAL64 Phase-A5 compile-only private host-shaped population

## Status

```text
IMPLEMENTED-COMPILE-ONLY-LOCKED-CONTEXT-POPULATION-PATH
POPULATION-SCOPE=STATIC-A5-PRIVATE-PATH-ONLY
CONTEXT-POPULATION-EXECUTIONS=0
REAL-RUNTIME-PROVENANCE=UNBOUND
PRODUCTION-ROUTE=UNCONNECTED
A5-OBJECT-LINKS=0
A5-OBJECT-EXECUTIONS=0
TRACKING-READS=0
TRANSPORT-SOLVES=0
DRAGON-RUNS=0
OUTER-CONVERGENCE=NOT-EVALUATED
```

This is Phase-A5 of the REAL64 implementation route. It is not the
project's numerical Stage-5, and it does not change the frozen Stage-4
qualification result.

## The one thing added here

Phase-A4 exposed a typed context but left its population to an arbitrary
caller. Phase-A5 adds one validation-only wrapper:

```text
MCGFL1R64_HOST_SHAPED_POPULATION_COMPILE_ONLY_LOCKED
```

Its context is private, local to one synchronous call, and never returned:

```text
A5 wrapper
  -> validate the exact locked branch
  -> populate a local disabled A4 context
  -> enable it only after every population check succeeds
  -> call the A4 wrapper exactly once
  -> disable it again before returning
```

The A5 wrapper calls A4 only. It does not call A2, A3, `MCGFCF`,
`MCGFST`, or any other legacy transport routine directly. It performs no
file or LCM operation and adds no link barrier. The single deliberate
unresolved barrier remains owned by Phase-A3.

## Field population definitions

The following values are copied into owned allocatable storage without a
kind conversion:

- `IFTRAK`, `NBTR`, `NBATCH`, and `N2MAX -> NMAX`;
- the borrowed `KPSYS(:)` C-address values;
- live binary64 `CAZ1(:)` and `CAZ2(:)`;
- live binary32 `ZMU(:)`, `WZMU(:)`, and `VOLUME(:)`.

The remaining context storage uses canonical defined values for three
formals proved unread on the locked `NDIM=2`, isotropic, `IDIR=0` branch,
and exact discrete identities for two index arrays:

- `CAZ0(:)=0.0_real64`: canonical storage because the 2D branch never
  reads `CAZ0`; the legacy 2D allocation is otherwise uninitialized;
- `CPO(:)=0.0_real32`: canonical storage; its length supplies `NMU`,
  while the locked
  isotropic 2D branch reads `ZMU/WZMU` and never reads `CPO` values;
- `XSI(:)=0.0_real64`: canonical storage because `MCGFFIR` reads `XSI`
  only when `IDIR>0`;
- `ISGNR(4,1)=1`: the exact `MOCIK3` result for order zero and `NMOD=4`;
- `PJJIND(1,1:2)=1`: the exact isotropic `MCGPJJ` index pair.

The three zeros are not claims about legacy data values; they are
canonical defined storage for observationally dead formals. The two
integer arrays are exact discrete index identities. None is a relaxation
factor, tolerance, fit, closure, empirical coefficient, or replacement
for live physical data. No physical equation is modified.

## What “host-shaped” proves

Strict Fortran interfaces check the kind, rank, shape, and contiguity of
the fields that a future locked `MCGFL1` host must supply. The private
population routine checks positive tracking counts, exact dimensions, and
non-null C addresses for active groups. The context owns its array
containers; the sequential file unit and objects referenced by `KPSYS`
remain borrowed.

This is a static source and compilation result. No A5 population routine,
A4 callback, or transport operator is executed by this gate.

## What remains unproved

An integer file unit and copied C addresses are not provenance evidence.
Phase-A5 does not establish:

- that `IFTRAK` is open on the intended tracking object or positioned at
  the first track record;
- that the `KPSYS` pointees are alive, in the required group order, or
  contain the matching `PJJ$MCCG` records;
- that `IFTRAK`, `KPSYS`, `NZON`, `SIGAL`, `SC`, and `VOLUME` describe
  one geometry, material state, and group ordering;
- that the hidden `/EXP1/` table was initialized by `XDRTA2` in the same
  process image;
- that the current production `QFR/PHIIN` host state is binary64;
- that the production tracking call can be replaced without consuming the
  stream twice.

In particular, `c_associated` proves only that an active handle is
non-null. It cannot inspect an LCM directory or prove a pointee lifetime.

## Short object-only gate

Run:

```sh
make spot-real64-phase-a5
```

The isolated target verifies the scoped receipt, frozen Phase-A4 receipt,
canonical manifest, static checker, and mutation tests. It then recompiles
the explicit Phase-A1 through Phase-A5 sources and a subroutine-only A5
anchor using object-only commands. Negative compilation checks reject
wrong mutable-state kind, wrong `KPSYS` type, wrong `CAZ` kind, promoted
operator data, noncontiguous population inputs, and global default-REAL
promotion.

Exact unresolved-symbol allowlists are checked for the A3, A4, A5, and
anchor objects. No object is linked, no executable is built, and no build
artifact is executed. The runner does not invoke older Phase-A runners, so
the total number of synthetic or transport executions in Phase-A5 is zero.

The exact diagnostics and symbol receipts are locked to GNU Fortran 15.2.0
(Homebrew GCC 15.2.0_1), locale `C`, on Darwin arm64. Another toolchain
requires a separate reviewed receipt.

## Next threshold

A later, separate gate must add a production-default-off callsite and
runtime preflight for tracking position, group directories, cross-object
identity, and `/EXP1/`, while retaining the Phase-A3 barrier. Only after
those obligations are independently closed can an explicit authorization
consider linking or one bounded transport execution.
