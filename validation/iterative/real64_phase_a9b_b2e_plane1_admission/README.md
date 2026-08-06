# Phase A9b-B2e: real plane-1 admission census

B2e freezes a negative but decisive static-and-synthetic admission result:
the shipped plane-1 host cannot currently reach the REAL64 solver. This is a
host lifecycle result, not a convergence result.

The exact frozen `restart_cap.xsm` contains a legacy `SOUR` list, while B2b
requires `SOUR` to be absent on its recovered output. After removing only that
derived list from a temporary copy, the next incompatible B2b guard is the
real `MACRO0`: it stores three Legendre components
(`STATE-VECTOR(3)=3`), while B2b was locked to one. The schema census freezes
all earlier signature, collision, optional-record, state and tolerance guards
needed for that ordering. The real MCCG tracking activates one flux Legendre component,
so the legacy scalar branch uses order zero through
`0:MIN(NLF-1,NANIS)`. B2e records this distinction; it does not discard the
nonzero stored P1/P2 data or change a production equation.

The direct harness compiles the real `src/SPOR64_B2B.f90`, but replaces
`XDRTA2`, the REAL64 core and the publisher with ABI-identical counters. All
three cases stop with admission status 1 and zero post-boundary calls:

- the exact recovered real restart;
- a temporary clone with only legacy `SOUR` removed;
- the fresh output topology used by the shipped `SpotPlaneFS`.

The validation-only candidate therefore separates ownership:

```text
fresh FLUX target <- FLU(MACRO0, TRACK, TRACK_f, SYSTEM, FSOURCE,
                         read-only FLUX_OLD)
```

It has seven entries, one `R64`, `INIT ON`, `REBA`, `EXTE 500`, `THER 740`
and `ACCE 3 3`; its fresh target implies `REC=false, LIMERG=true`, whereas
the two recovered fixtures use `REC=true, LIMERG=false`. It is parsed
statically and is not registered or executed.
No epoch field is needed for this isolated one-call object lifetime.

Run the short gate with:

```sh
sh validation/iterative/real64_phase_a9b_b2e_plane1_admission/run_phase_a9b_b2e_plane1_admission.sh
```

The authoritative boundary is:

```text
CURRENT-HOST-ADMISSION-BLOCKED-BEFORE-SOLVER
PRODUCTION-XDRTA2-CALLS=0
PRODUCTION-CORE-CALLS=0
PRODUCTION-PUBLISHER-CALLS=0
DRAGON-EXECUTIONS=0
SEQUENTIAL-TRACKING-RECORD-READS=0
TRANSPORT-SOLVES=0
PRODUCTION-EXECUTION-AUTHORIZED=false
RADIAL-CONVERGENCE=NOT-EVALUATED
OUTER-PICARD-CONVERGENCE=NOT-EVALUATED
```
