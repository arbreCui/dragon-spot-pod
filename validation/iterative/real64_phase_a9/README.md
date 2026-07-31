# REAL64 Phase-A9a outer mathematical compile-only closure

## What this phase closes

Phase-A9 was split after three independent source and host audits. A9a is
the smallest honest next step: it implements the outer radial iteration as
validation-owned `REAL64` mathematics and compile-checks its boundary. A9b
will later connect that mathematics to the production parser, live GANLIB
objects and accepted archive writes.

The A9a call graph is deliberately short:

```text
FLU2DR64_CORE
  -> A8 DOORFV64
  -> FLUBAL64 -> ALSBD
  -> FLU2AC64
  -> REAL64 inner and outer norms
  -> strict terminal Boolean
```

No A9a object is linked or executed. No tracking file is read, no transport
operator is applied and no Dragon process is started.

The first core handle is named `JPSYS_GROUP` deliberately: A8 `DOORFV64`
consumes the admitted `L_PIJ/GROUP` list, not the root `L_PIJ` object. A9a
compile-checks that typed boundary but cannot prove the live pointer or
tracking-stream epoch; A9b must establish both before selecting the route.

## Eight-slice owner

`FLU2DR64_CORE` uniquely owns
`FLUX64(14,370,8)`. The slices are old/present/new outer flux, current outer
source, and old/present/new inner flux plus current inner sweep source. The
owner first defines all storage as positive zero and promotes the initial
`REAL64` flux only into present outer slice 2. The inherited copy order fills
every other live history slice before use. Each outer iteration resets slice
4 to the admitted fixed source and slice 6 to the current outer flux.

For one inner visit, slice 7 first receives slice 6 and slice 8 first
receives slice 4. The frozen off-group scattering bundle is then applied in
the original group-region-packed order. Self scattering is excluded because
the frozen branch is `ITPIJ=1`; leakage and fission branches are absent.

One important physical distinction is now explicit: `XCSOU64` is the
volume integral of outer source slice 4. It is not the inner sweep source.
After the final inner visit, slice 7 becomes outer slice 3 and slice 8
becomes outer slice 4, so the terminal source is the final sweep input.
This is an A9a wording correction to the frozen A7 blueprint; A7 itself is
left immutable, while the legacy `FLU2DR` source is the authority.

## Rebalancing and acceleration

`FLUBAL64` builds its matrix and right-hand side in `REAL64`, reusing the
same admitted `REAL32` off-group operator bundle as source construction.
Stored volume, reaction, albedo, surface and scattering values are promoted
exactly at use. The linear system is the inherited one and is passed to
`ALSBD`; a solver error is structural failure, with no legacy fallback and
no publication.

`FLU2AC64` retains the inherited one-factor variational formula. It runs on
the inherited three-free/three-accelerated schedule. A mathematically exact
zero denominator produces no acceleration and `ZMU64=1`; no numerical
threshold is invented. There is no relaxation coefficient, fitted value,
clipping rule or tuned cutoff.

## Norms and acceptance

Inner and outer group norms use only the eight scalar-region flux keys, as
the legacy branch does, but all differences, maxima and divisions remain
`REAL64`. A zero norm denominator is a structural failure; it is not hidden
with a flux floor.

The legacy near-inner condition may schedule the next outer iteration, but
it can never accept. The only terminal condition is

```text
EEXT64 < EPSOUT64
and EUNK64 < EPSUNK64
and EINR_LAST64 < EPSINR64
and IINR_STATE == 1
and outer iteration >= 2
```

For the frozen type-S problem `EEXT64=0`. The three tolerances are exact
`REAL64` promotions of binary32 bits `0x348637bd`; their value is not tuned.
Reaching the inherited outer cap is a normal non-accepted return.

## Why this is not complete A9

A9a does not implement the production `FLUGPI/FLU/FLUDRV` route, runtime
pointer and tracking-stream provenance, `XDRTA2` lifecycle, the production
`SPOMOC_CAPTURE64` body, type-4 authority records, the terminal type-2
compatibility mirror or layered host publication. The small default-false
selector module in this directory proves only the abstract no-fallback
branch shape; it is not production wiring.

Consequently the status remains:

```text
FROZEN-IMPLEMENTED-COMPILE-ONLY-OUTER-CLOSURE
CONTINUOUS-REAL64-LANE=false
PRODUCTION-ROUTE-CONNECTED=false
RADIAL-CONVERGENCE=NOT-EVALUATED
OUTER-PICARD-CONVERGENCE=NOT-EVALUATED
```

The machine-readable authority is
[`precision_manifest.json`](precision_manifest.json).

## Short gate

```sh
make spot-real64-phase-a9a
```

The gate checks the A8 receipt identity, validates the source contract,
compiles relocatable objects only, requires deliberately wrong ABIs to fail,
and compares exact symbol inventories. It does not run any earlier synthetic
runner, link an object, execute an object, read tracking, solve transport or
run Dragon.

Only after A9a passes should A9b implement the default-off production host
and archive lifecycle. A bounded runtime convergence census remains later
work and requires its own authorization.
