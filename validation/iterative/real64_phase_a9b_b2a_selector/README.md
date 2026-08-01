# Phase A9b-B2a: default-OFF selector and write deferral

B2a adds exactly one numerical-route keyword to the common `FLUGPI` parse:

```text
R64
```

It is a bare keyword, defaults to false on every call, and a duplicate is an
error. `R64` and `MOCA` are independent: `MOCA` still controls only the
existing raw-MOC audit and can never select a numerical route.

The selected route is deliberately not executable in this subgate. After the
single parser return, `FLU` fails closed and returns before `SIGNATURE`,
`LINK.*`, `IMERGE-LEAK`, `XDRTA2`, `FLUGPT` or `FLUDRV`. `FLUDRV` also has an
entry guard before allocation or LCM access. There is no fallback to the
legacy solver.

## Why `LIMERG` is explicit

The old parser wrote `IMERGE-LEAK` while reading input. A final
`REC/NMERG/ILEAK` tuple cannot tell whether this invocation completed a new
`HETE` mapping or merely reused an existing one. `FLUGPI` therefore returns
the scalar logical `LIMERG` together with `LR64`. `LIMERG` is bookkeeping for
deferred record publication; it is not a physical or numerical parameter.

`FLUGPI` now performs no output-record write. On the legacy OFF path, `FLU`
commits the final records in this class order:

```text
SIGNATURE -> LINK.MACRO -> LINK.TRACK -> LINK.SYSTEM -> IMERGE-LEAK
```

The successful OFF path preserves each final record's name, GANLIB type,
length and payload, and it preserves the old numerical calls and floating
point statement order. Exact metadata mutation trace identity is not claimed:
a new object followed by one or more complete `HETE` mappings is committed
once with its final mapping. No event journal is introduced for an
unobservable, nonphysical write history.

## Exact boundary

Passing B2a means only that the production parser recognizes a local,
default-false selector and that a selected visit cannot reach an `IPFLUX`
record write or the legacy numerical route. It does not mean that the REAL64
route is connected.

The old `L_LIBRARY` branch can still navigate its `MACROLIB` cursor with
`LCMSIX` before parsing. This is not an output-record write, but it is why B2a
does not claim the complete A7 admission boundary. B2b must admit the direct
`L_MACROLIB` topology before solving.

`FLU` also retains the existing `CALL XDRTA2(IPTRK)` in the legacy OFF arm,
although `XDRTA2` is formally zero-argument. Correcting and validating the
selected route's exact single zero-argument epoch belongs to B2b. The existing
`FLUGPT`/`FLU2DR` argument-count debt is recorded but is not changed here.

## Short gate

```sh
make spot-real64-phase-a9b-b2a-selector
```

The gate compiles temporary copies of the production host objects. Separately,
it compiles the real production `FLUGPI.f` against a synthetic GANLIB module
that exposes read calls but no write API, then runs twelve fixed parser cases.
Those cases cover default OFF, one `R64`, duplicate rejection, a parameter
after `R64`, an illegal following keyword, both `MOCA` orders, per-call reset,
REC reuse and complete HETE staging. It never links or executes a production
solver object, reads tracking, invokes transport, or runs Dragon.

The authoritative result remains:

```text
R64-ROUTE-EXECUTABLE=false
PRODUCTION-ROUTE-CONNECTED=false
SPOMOC-BEGIN64-IMPLEMENTED=false
HOST-INGRESS-IMPLEMENTED=false
XDRTA2-EPOCH-VALIDATED=false
ARCHIVE-IMPLEMENTED=false
CONTINUOUS-REAL64-LANE=false
RADIAL-CONVERGENCE=NOT-EVALUATED
OUTER-PICARD-CONVERGENCE=NOT-EVALUATED
```
