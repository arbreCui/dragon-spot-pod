# Phase A9b-B2-ABI: SPOMOC external seam closure

This deliberately small production gate closes the four ordinary-external
SPOMOC symbols already called by the promoted A8 module:

```text
SPOMOC_MCCGF_BEGIN
SPOMOC_SET_ROLE
SPOMOC_PUBLISH
SPOMOC_CAPTURE64
```

`src/SPOMOC_R64_BRIDGE.f90` defines those four global Fortran symbols. Each
routine only forwards to the checked `SPOMOC_AUDIT` module procedure. The
new module procedure `SPOMOC_CAPTURE64` receives QFR, EVAL, source and raw
response directly as `REAL(real64)`, applies the existing capture identity
and finite-value checks, and writes the four existing type-4 diagnostic
records without a REAL64-to-REAL32 conversion.

The legacy `SPOMOC_CAPTURE` routine is byte-for-byte unchanged. When the
existing audit is not armed, all four calls remain no-ops through the
existing module behavior. The bridge contains no arithmetic, GANLIB call,
I/O, saved state, solver control or empirical parameter.

## Why this precedes the selector

The current host writes `SIGNATURE`, `LINK.*` and `IMERGE-LEAK` before or
during `FLUGPI` parsing. Adding a production `R64` keyword now would therefore
create a selected path that can fail only after public mutation, contradicting
the frozen accepted-only contract. This gate does not touch `FLUGPI`, `FLU`,
`FLUDRV`, `FLU2DR` or `XDRTA2`, and does not expose a selector.

The remaining host work stays split:

1. B2a defers all early writes and adds one default-OFF, one-pass selector.
2. B2b performs read-only ingress, validates lifetimes, calls the unchanged
   zero-argument `XDRTA2` exactly once and reaches the REAL64 core without
   publication.
3. B2c performs type-4 authority, the single type-2 compatibility mirror and
   layered host writes only after strict acceptance.

## Short gate

```sh
make spot-real64-phase-a9b-spomoc-abi
```

The gate first copies and compiles the seven frozen GANLIB interface-module
sources in its temporary directory. It then compiles temporary copies of the
four production sources, so ignored or prebuilt `.mod` files in the worktree
cannot influence the result. Before any compilation it changes the working
directory to that fresh temporary directory and uses the frozen absolute
compiler path `/opt/homebrew/bin/gfortran`. It checks exact dependency and symbol
inventories, runs negative compile fixtures and mutation tests, then removes
the temporary directory. It does not link or execute an object, read a
tracking file, invoke transport or run Dragon.

Passing means only:

```text
A8-SPOMOC-EXTERNAL-SYMBOLS-DEFINED-COMPILE-ONLY
PRODUCTION-ROUTE-CONNECTED=false
CONTINUOUS-REAL64-LANE=false
RADIAL-CONVERGENCE=NOT-EVALUATED
OUTER-PICARD-CONVERGENCE=NOT-EVALUATED
```
