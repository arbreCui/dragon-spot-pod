# Phase-A9b B2g: explicit REAL64 continuation ingress

This directory is an independent, short validation gate for the two explicit
REAL64 ingress modes of `SPOR64_B2B_INGRESS`:

- `BOOT = 1` promotes the frozen REAL32 bootstrap records and requires the
  REAL64 continuation namespaces to be absent.
- `CONT = 2` reads the previous flux only from
  `FLUX_OLD/SPOT-R64/FLUX` and the new frozen fission source only from
  `FSOURCE/SPOT-R64/QFISS`.  Every group payload is GANLIB type 4.

The gate does not add a physical model, reconstruct a missing fission source,
apply relaxation, or choose an empirical coefficient.  It only proves that an
already supplied continuation state reaches the production REAL64 radial-core
call boundary/ABI without a REAL32 round trip.

## Positive poison proof

The Fortran harness opens the five frozen real XSM artifacts read-only, then
executes a clean `BOOT` success and proves bitwise that the two root type-2
inputs are promoted exactly once into the core-call ABI.  Using those same
artifacts, it copies the seed and source into temporary in-memory LCM objects
and manually creates
the two type-4 authority lists.  Each promoted value is shifted outward by one
REAL64 ULP, which remains below half a REAL32 ULP, so every authority value has
a deterministic low-bit witness that a REAL32 round trip destroys.  The
harness then overwrites the legacy root type-2 `FLUX` and `DSOUR` payloads with
finite, admissible poison values.  A stub with
the exact `FLU2DR64_CORE` ABI captures both REAL64 arrays.  The test requires
their bits to equal the type-4 authorities and to differ from the promoted
root poison.  Consequently the success path cannot be explained by an
accidental read of the compatibility mirrors.

The production `SPOR64_B2B` ingress and production `SPOR64_B2C` publisher are
linked.  The transport core and `XDRTA2` are narrow counters/capture stubs.
The positive call therefore exercises real GANLIB reads and the real host
admission/publication chain without running a transport solve.

The stub returns an exactly representable positive terminal `SOUR` sentinel
that is deliberately distinct from its admitted `QFISS`.  The harness checks
every published type-4 `SOUR` bit and requires `QFISS` to be absent from the
output authority.  This locks the physical ownership boundary: terminal
inner-sweep total source is not the next outer iteration's frozen fission
source.

## Rejection proof

Fresh output objects are used for every negative case.  Mode zero, missing or
wrong-type seed authority, missing or wrong-type source authority, wrong-type
type-4 list elements, and either BOOT input authority are required to return
the admission-failed token with zero cutoff visits and zero `XDRTA2`/core
calls.  The rejected output must remain empty.

## Parser/host contract

`check_phase_a9b_b2g_explicit_continuation.py` checks the fixed-form host path
statically.  It proves that `FLUGPI` owns a three-state integer selector,
requires `R64 BOOT` or `R64 CONT`, rejects duplicates/unknown modes, and passes
the selector through `FLU` into `SPOR64_B2B_INGRESS`.  The runner also compiles
the real production `FLUGPI` against a deterministic token/LCM shim and executes
OFF, BOOT, CONT, repeated-call reset, REC reset, and six rejection scenarios.

Run:

```sh
./validation/iterative/real64_phase_a9b_b2g_explicit_continuation/run_phase_a9b_b2g_explicit_continuation.sh
```

The runner uses a temporary directory, performs only compilation, static
checks, and a small deterministic synthetic harness.  It never executes
Dragon, never reads the sequential tracking file, and never invokes the
production transport core.  Its receipt pins the B2f parent, the production
host sources, both shipped legacy procedures, the explicit bootstrap
procedures, the five read-only artifacts, the compiler-facing libraries, and
every B2g validation source.  The gate rechecks that receipt before and after
execution.

The controlled inventory is:

```text
REAL-B2B-CALLS=13
REJECTIONS-BEFORE-CORE=11
BOOT-TYPE2-PROMOTIONS=2
CONT-TYPE4-AUTHORITY-CAPTURES=2
ROOT-TYPE2-POISONS=2
REAL32-ROUNDTRIP-BIT-LOSS-WITNESSES=10360
PARSER-EXECUTIONS=11
PARSER-CALLS=13
PARSER-NEGATIVES=6
STATIC-CONTRACT-TESTS=12
MUTATION-CASES=11
PRODUCTION-CORE-CALLS=0
DRAGON-EXECUTIONS=0
SEQUENTIAL-TRACKING-RECORD-READS=0
TRANSPORT-SOLVES=0
```

This closes only explicit mode selection and the read-only type-4 ingress.
`SPOFSRC` still cannot produce `SPOT-R64/QFISS`, so no shipped procedure
selects `CONT`; continuous radial or outer Picard convergence remains
`NOT-EVALUATED`.
