# REAL64 Phase-A9b production-module promotion

## Purpose

This is the first, side-effect-free subgate of Phase-A9b.  It promotes the
already frozen A8 inner lane, its rank adapter and the A9a outer mathematical
owner into `src/` without changing a byte of their numerical implementation.
The production build can therefore discover and order the REAL64 module ABI
before any parser, dispatch or archive mutation is attempted.

The four production sources are exact copies:

```text
validation/iterative/real64_phase_a8/SPOR64_A8_ACA.f90
  == src/SPOR64_A8_ACA.f90
validation/iterative/real64_phase_a8/SPOR64_A8.f90
  == src/SPOR64_A8.f90
validation/iterative/real64_phase_a8/MCGFFIR64_RANK_ADAPTER.f90
  == src/MCGFFIR64_RANK_ADAPTER.f90
validation/iterative/real64_phase_a9/SPOR64_A9.f90
  == src/SPOR64_A9.f90
```

This is promotion, not a fork: byte equality is a release condition.  No
formula, kind, tolerance, cutoff, schedule or physical model is changed.

## What remains deliberately disconnected

`FLUGPI`, `FLU`, `FLUDRV`, `FLU2DR`, `SPOMOC`, `XDRTA2` and `src/Makefile`
remain unchanged in this subgate.  In particular:

- no `R64` keyword is parsed;
- the default production route is unchanged;
- no pre-existing production host or dispatch routine selects or calls the
  promoted REAL64 lane;
- the unresolved checked `SPOMOC_CAPTURE64` boundary is not implemented;
- the four A8 audit calls remain ordinary external symbols; the existing
  `SPOMOC_AUDIT` module procedures are not link-equivalent global wrappers;
- no GANLIB type-4 authority or type-2 compatibility mirror is written;
- no runtime pointer, tracking stream or `/EXP1/` epoch is claimed.

Those public side effects belong to the second A9b subgate.  Keeping them
separate makes a module-order or ABI failure distinguishable from a host
lifecycle or archive-order failure.

Accordingly, passing B1 does not authorize linking: B2 must either give the
four checked A8 audit seams exact global wrappers or replace them with an
equally explicit module interface while implementing the REAL64 capture.

One legacy detail is explicitly reserved for that next gate: `XDRTA2` is a
zero-argument routine.  The future selected ON route must call it exactly once
with no actual argument after admission and before the first `MCGSCA` use; this
promotion gate does not alter the existing host call.

## Short gate

```sh
make spot-real64-phase-a9b-promotion
```

The gate verifies byte identity, the generated module dependency edges,
strictly compiles relocatable objects, rejects default-REAL promotion and
compares exact defined/unresolved symbol inventories.  It does not link or
execute an object, build Dragon, read tracking, apply transport or run a
radial iteration.

An ordered scoped SHA-256 receipt freezes the parent receipt, both copies of
the four authorities, all protected host/build files, documentation and every
B1 gate artifact.  The runner verifies that receipt before compiling.

Passing this gate permits only the statement
`PRODUCTION-OBJECTS-AVAILABLE-COMPILE-ONLY`.  It does not establish a
continuous production REAL64 lane, radial convergence, physical accuracy or
outer Picard convergence.

The machine-readable contract is
[`precision_manifest.json`](precision_manifest.json).
