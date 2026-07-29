# REAL64 Phase-A3 compile-only legacy ABI seam

## Status

Phase-A3 encodes a checked caller for the frozen legacy
`MCGFCF -> MCGFST` boundary:

```text
IMPLEMENTED-COMPILE-ONLY-LEGACY-ABI-SEAM
PRODUCTION-ROUTE=UNCONNECTED
PHASE-A3-LINKS=0
A3-EXECUTIONS=0
TRANSPORT-SOLVES=0
DRAGON-RUNS=0
ACTUAL-MOC-RESPONSE=NOT-VALIDATED
OUTER-CONVERGENCE=NOT-EVALUATED
```

The module remains under `validation/`; it is not selected by the
production build or any default runtime route.  Its scientific-use status
is therefore `NONE`.

## What this phase establishes

`MCGFCF_MCGFST_R64_COMPILE_ONLY_LOCKED` freezes the currently studied
two-dimensional isotropic branch:

```text
ISCH=11, NDIM=2, K=KPN=14, NREG=8, NSOUT=6
NANI=NLF=NFUNL=NLFX=NLIN=NFUNLX=1
NMOD=4, STIS=1, NPJJM=1, IDIR=0
CYCLIC=FALSE, LPRISM=FALSE, NG=370
```

The checked façade requires a nonempty arbitrary `NCONV` subset over a
strictly consecutive gathered-group tail ending at group 370.  It keeps
`SOURCE` and `RAW_RESPONSE` in REAL64, while preserving the stored REAL32
operator inputs `CPO`, `ZMU`, `WZMU`, `SIGAL`, and `VOLUME`.  It also
locks the legacy ABI details that are easy to change accidentally:

- `KPSYS` is rank-one `TYPE(C_PTR)`, with neither `VALUE` nor `BIND(C)`;
- `PJJIND` is rank two with shape `(NPJJM,2)`;
- the `NLIN=1` `KEYFLX` view passed to `MCGFST` is an explicit contiguous
  pointer rank remap, not a hidden array temporary;
- the legacy interface bodies leave `INTENT` unspecified and keep forwarded
  `SUBSCH` as implicit-interface `EXTERNAL`, exactly as in the definitions;
- global `-fdefault-real-8` promotion and mutable REAL32 callers are
  compile-time failures.

The source encodes exactly one `MCGFCF` call with procedure actuals
`MCGFFIR`, `MCGFFAR`, `MCGFFAL`, and `MCGSCA`, followed by exactly one
`MCGFST` call.  For the locked branch, the expected active legacy path is

```text
MCGFCF -> MCGFFIR -> MCGSCA -> MCGFST
```

`MCGFFAR` and `MCGFFAL` remain required procedure actuals but are inactive
on this branch.  This is a compile-time encoding of the path, not a runtime
observation.

An intentionally unresolved symbol,
`SPOR64_A3_COMPILE_ONLY_LINK_FORBIDDEN`, is called immediately before the
legacy sequence.  It is a link barrier: Phase-A3 objects must remain
unlinked and cannot be executed until a later, separately authorized gate
removes that barrier.

## Two legacy interface findings

The frozen `MCGFL1` call allocates `XSIXYZ(NSOUT,3)` but passes
`XSIXYZ(1,IDIR)`.  With the locked value `IDIR=0`, that actual designator
uses column zero even though the declared second-dimension lower bound is
one.  It is not standard-conforming Fortran.  The fact that locked
`MCGFFIR` does not read `XSI` when `IDIR=0` does not make the designator
conforming.  Phase-A3 instead requires legal, caller-owned, contiguous
`XSI(NSOUT)` storage.  It does not fix the production call or validate its
runtime safety.

The `MCGFFA_TEMPLATE` interface declared in `MCCGF.f` also does not match
the actual `MCGFFAR.f` procedure: the template contains additional
`NMOD`, `MODP`, and `MODM` arguments and different scratch/harmonic shapes.
Phase-A3 derives its `MCGFFAR` interface directly from `MCGFFAR.f`.
Because `MCGFFAR` is inactive for the locked isotropic path, this phase
records the mismatch without repairing or executing that legacy branch.

## Short compile-only gate

Run:

```sh
make spot-real64-phase-a3
```

The target first rechecks the Phase-A2 prerequisite, including its short
synthetic test, and then:

- verifies the scoped Phase-A3 receipt, manifest, and contract mutations;
- strictly compiles the Phase-A3 module and a subroutine-only positive
  anchor;
- requires wrong mutable kind, wrong `KPSYS` type, flat `PJJIND`, altered
  operator kind, and global default-kind promotion to fail compilation;
- compiles the six referenced legacy sources to independent object files;
- verifies the intended unresolved legacy symbols and link barrier, and
  rejects an executable entry point.

No Phase-A3 object is linked or executed.  The target performs no tracking
read, no transport application, and no Dragon run.  The Phase-A2 synthetic
prerequisite is compiled, linked, and executed inside the preceding A2
subgate; it is the only Fortran execution in this chained gate and is not a
MOC calculation.

## What is not yet proved

Passing this target is not evidence of a physical MOC response or radial
iteration convergence.  No real positioned tracking unit, `KPSYS`/PJJ
directory, geometry identity, `EXP1` table, or host-associated context has
been bound.  The Phase-A2 callback is not connected to this seam.
`MCGFCA`, live ACA correction, GMRES state, rebalancing, acceleration,
terminal norms, production gather/scatter, and the authoritative archive
boundary all remain open.

No empirical coefficient, relaxation parameter, clipping rule, fitted
closure, or new convergence tolerance is introduced here.

## Next static threshold

The next step is a compile-only, default-off context carrier and host
closure from the Phase-A2 callback to this Phase-A3 seam.  It must preserve
the unresolved link barrier, carry conforming caller-owned `XSI` and the
typed real-context identities, remain disconnected from production, and
perform no tracking read or transport execution.  Actual
`MCGFCF -> MCGFST` execution requires a later explicit gate after those
context and conformance obligations are closed.
