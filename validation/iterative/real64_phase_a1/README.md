# REAL64 Phase-A1 locked-source slice

## Status

This directory contains the first isolated implementation slice of the
default-off REAL64 radial route:

```text
IMPLEMENTED-PARTIAL-SLICE-ONLY
PRODUCTION-ROUTE=UNCONNECTED
DRAGON-RUNS=0
```

It is deliberately outside `src/`.  The legacy production route and the
default build therefore do not call or compile this module.

## Implemented boundary

`SPOR64_PROMOTE_MUTABLE` explicitly promotes the binary32 entry arrays
`QN32` and `FI32` once into binary64 working arrays.  For the frozen
two-dimensional isotropic branch

```text
NDIM=2, NANI=1, NLIN=1, NFUNL=1, STIS=1
```

`MCGFCS64_LOCKED` evaluates

\[
S_k=Q_k+\operatorname{real64}(SC_{m,1})\,\Phi_k
\]

for a mapped volume unknown, and

\[
S_k=\operatorname{real64}(SIGAL_b)\,\Phi_{k'}
\]

for a mapped boundary unknown.  `QN`, `FI`, and `S` remain binary64
through this kernel.  The frozen binary32 operator data `SC` and `SIGAL`
are promoted exactly at their use sites; they are not refitted or
recomputed.

All metadata and array bounds are checked before `S` is changed.
Unsupported branch metadata or an invalid layout returns a nonzero status
without changing `S`.  Unmapped entries preserve the caller's bit pattern.
`SPOR64_TERMINAL_COPY` demonstrates the only allowed down-conversion:
one binary64-to-binary32 copy after an explicit terminal-acceptance flag.

No relaxation, fitted closure, clipping, empirical coefficient, or new
acceptance threshold is present.

## Short verification

Run

```sh
make spot-real64-phase-a1
```

The target uses an explicit source list in a temporary directory.  It:

- verifies the frozen implementation receipt before executing any checker;
- compiles with explicit interfaces, runtime checks, and no global
  default-kind promotion;
- verifies independent `QN` and `FI` increments smaller than one binary32
  ULP survive the source arithmetic;
- verifies exact promotion of an arbitrary stored binary32 `SC` bit
  pattern, key mappings, input immutability, and fail-closed behavior;
- requires a binary32 mutable-state caller to fail compilation;
- checks that the test executable has no unresolved transport symbols;
- runs the manifest mutation tests.

This target starts no Dragon process and performs no transport solve.

## Interpretation and next boundary

Passing the target is not evidence that the radial iteration converges.  It
does not provide a continuous REAL64 lane: `FLU2DR`, `DOORFV`, `MCCGF`,
`MCGFLX`, `MCGMRE`, `MCGFL1`, the primary MOC response, ACA,
rebalancing, acceleration, terminal norms, and the type-4 archive boundary
remain open.

The next static step is an isolated REAL64 `MCGFL1` caller plus a checked
primary-response façade.  It must remain disconnected from production and
must support the arbitrary active-group subset before the wider mutable
iteration state is implemented.
