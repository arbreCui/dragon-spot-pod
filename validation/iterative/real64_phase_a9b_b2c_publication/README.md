# Phase-A9b-B2c accepted-only publication gate

This seconds-scale gate closes one deliberately narrow boundary: an accepted
REAL64 terminal state can be published once, in the same `SPOR64_B2B_INGRESS`
lifetime, and only a fully completed publication (`status=8`) may return
normally from the selected `FLU` branch.

The preflight is fail-closed and precedes the first write.  It requires the
private accepted-unpublished token (`4`), finite terminal values, binary32
representability for the compatibility mirror, frozen input controls, a valid
existing 370-by-14 type-2 `FLUX` list, compatible root metadata schemas, and
an unused single-epoch namespace.  `SPOT-R64`, root `SOUR`, `AFLUX`, `DFLUX`,
and `ADFLUX` must be absent.  On the integrated route, a pre-existing collision
is rejected by the earlier B2B admission as status `1`, before the core runs.
B2C repeats the checks immediately before publication.  Any B2C no-write
preflight failure returns status `5`, including a last-moment collision or
schema drift, an invalid token/pointer/shape/frozen input, a non-finite or
non-representable terminal value, or staging-allocation failure.  Both paths
perform no listed mutation, and neither silently overwrites an earlier epoch.

After preflight, the fixed transaction order is:

1. write bit-preserving type-4 `SPOT-R64/FLUX` and `SPOT-R64/SOUR` authority;
2. perform exactly one write-only REAL64-to-REAL32 staging pass and write the
   root type-2 `FLUX`/`SOUR` compatibility mirror (`status=6`);
3. commit `STATE-VECTOR`, `EPS-CONVERGE`, `KEYFLX`, and `OPTION` (`status=7`);
4. commit `LINK.MACRO`, `LINK.TRACK`, `LINK.SYSTEM`, and `SPOT-LEAK1D`
   (`status=8`).

These three commit phases are the concrete A9b refinement of the three logical
publication owners frozen in A7: child payload, driver metadata, and host
links/leakage cache.  They remain separately ordered by statuses 6, 7, and 8,
but are implemented by one synchronous, same-lifetime publisher.  This
centralization does not merge their semantics or broaden publication
authority.

There is no completion marker and no crash-rollback claim once the first
accepted write has begun.  GANLIB write failures abort; intermediate statuses
6 and 7 are never accepted by `FLU`.  No fallback, fitted coefficient,
relaxation coefficient, or model completion is introduced.

The runner strictly compiles the production sources into a temporary
directory and freezes exact global-symbol inventories for `SPOR64_B2C`,
`SPOR64_B2B`, and `FLU`.  An explicit-interface positive/negative pair rejects
a REAL32 terminal payload.  A validation-owned state machine exercises wrong
tokens, all five collision classes, NaN, infinity, positive and negative
binary32 overflow, exact binary32 boundaries, normal event order, all status
transitions, REAL64 bit preservation, and one scalar compatibility conversion
per output value.

An additional in-memory LCM harness links and executes the real
`SPOR64_B2C.o` with GANLIB/UTILIB in five independent processes: valid,
wrong-token, existing-`SPOT-R64`, NaN, and out-of-binary32-range.  The valid
case reads back every authority and compatibility group plus all metadata and
an unrelated sentinel.  Each rejected case proves status 5, unchanged root
`FLUX` bits and sentinel, absent root `SOUR`, and no new authority child (the
collision case preserves its pre-existing empty authority).  The harness does
not link or execute B2B, the production solver, transport, tracking input, or
Dragon.  A repository-wide static enumeration additionally requires the sole
production `CALL SPOR64_B2C_PUBLISH` to remain in `SPOR64_B2B.f90`.

Run:

```sh
make spot-real64-phase-a9b-b2c-publication
```

This is publication evidence, not physical runtime evidence.  Production
transport execution remains zero, and radial and outer Picard convergence are
both `NOT-EVALUATED`.
