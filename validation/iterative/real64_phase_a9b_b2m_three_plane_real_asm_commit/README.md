# Phase-A9b B2m: bounded three-plane real ASM commit

B2m is the next narrow production boundary after B2l.  It starts from the
same complete three-plane `PROJECTED/1` archive and executes the existing
default-off `SpotAsmR64` procedure once.  That procedure performs exactly
three production `ASM: ... ARM LK1D 1/2/3` calls and then one production
`SPOR64K:` call.

```text
PROJECTED/1
  -> real ASM(LK1D 1), real ASM(LK1D 2), real ASM(LK1D 3)
  -> one in-memory SPOR64K logical commit
  -> ASSEMBLED/1
  -> one whole-object XSM evidence copy
```

There is no `FLU`, fission-source construction, `CONT`, loop, Picard map,
relaxation, damping, clipping, fitted coefficient, model completion, or
automatic retry in this transition.  `FLU` is deliberately later: it consumes
an already assembled `L_PIJ` SYSTEM, so it is not a prerequisite for building
or committing these three operators.

## Scientific boundary

For every plane `p=1..3`, energy group `g=1..370`, and material slot
`m=1..8`, the independent posterior reproduces the production binary32
operation order:

```text
TXSC[p,g,0]   = +0
TXSC[p,g,m]   = NTOT0[p,g,m] - TRANC[p,g,m]

S0PHYS[p,g,0] = +0
S0PHYS[p,g,m] = SIGW00[p,g,m] - TRANC[p,g,m]

S0USED[p,g,0] = +0 - LEAK1D[p,g]
S0USED[p,g,m] = S0PHYS[p,g,m] - LEAK1D[p,g]
```

The two subtractions in `S0USED` are not reassociated or promoted.  Passing
requires 9,990 bit identities in each of the three families, 1,110 exact
leakage values, and the complete fixed response schema.  The 12 ACA/PJJ
response records contain 59,940 binary32 values per plane and 179,820 values
over all three planes.  Every value must be finite.  Each plane must contain
at least one response value whose magnitude bits are nonzero, treating both
signed zero encodings as zero.  This is only a categorical dead-output guard;
there is no empirical fraction, norm, distance, or tolerance, and it is not a
response-accuracy claim.

The committed archive must have the exact `ASSEMBLED/1` root inventory and
three exact `ASSEMBLED/1` SYSTEM authorities.  Across the three systems this
is 1,110 group directories and 16,650 exact group records.  Its `TRACK`, `MICROLIB2`, and
plane `FLUX` trees are recursively bit-identical to `PROJECTED/1`; every plane
FLUX therefore remains `PROJECTED/1`.  `RHO`, `SPOT-ITER-K`, plane identity,
and same-index leakage provenance are exact, and the read-only PROJECTED file
must retain its pre-run SHA-256.

If all checks pass, the strongest permitted claim is:

```text
REAL-ASM-PLANES1-3-EXECUTED
AND SPOR64K-ASSEMBLED1-COMMITTED
AND B2K-POSTERIOR-COMPATIBLE
```

It does **not** establish ACA/PJJ response-matrix numerical accuracy, a radial
flux solution, a balance residual, radial convergence, an outer Picard step or
convergence, SPOD truncation accuracy, eigenvalue or power accuracy, or
agreement with an independent transport code.

## Commit and persistence semantics

Production `SPOR64_B2K` currently accepts a fresh memory-backed LCM root.  The
`SpotAsmR64` result is therefore an in-memory logical commit: all semantic
admission and private staging precede publication, and root
`SPOT-R64/EPOCH=1` is its final LCM mutation on normal completion.

Only after `SpotAsmR64` returns does the B2m wrapper perform exactly one
whole-object assignment from the committed linked list to a previously
nonexistent XSM path.  That XSM is a persistent **evidence copy** of the
in-memory commit.  B2m does not claim that `SPOR64K` targeted XSM directly,
that EPOCH was the final physical XSM write, or that either object is ACID,
power-failure-safe, `fsync`-durable, or rollback-capable.  A missing or invalid
completion marker invalidates the entire evidence object.

### Loader visibility and precompiled selection

GANLIB separates procedure discovery from procedure compilation.  `kdrdpr`
requires the exact `SpotAsmR64.c2m` source name to be visible when processing
the `PROCEDURE` declaration, and records `SpotAsmR64.o2m` as the executable
object name.  `cle2000` then probes that object first and enters its source
compilation branch only when the object is absent.

The bounded case therefore contains both an exact copy of the reviewed source
and the already compiled, nonempty `SpotAsmR64.o2m`.  Source visibility is a
loader requirement; it does not dynamically recompile the procedure.  The
runner requires `SpotAsmR64.l2m` to be absent before and after execution;
that listing is created only by the missing-object source-compilation branch.
Procedure-compilation error markers are also rejected.

## Execution policy

The default target is compile/static/mutation checking only and must execute
no Dragon or ASM process.  Real execution remains explicit and default-off:

```sh
make spot-real64-phase-a9b-b2m-three-plane-real-asm-commit
RUN_B2M=1 make spot-real64-phase-a9b-b2m-three-plane-real-asm-commit
```

The older candidate header's phrase “not selected by a shipped deck” refers
to default production calculation decks.  B2m is an explicit validation-only
wrapper; no default target or production calculation selects the candidate.

One activation permits one bounded PROJECTED materializer and one bounded
Dragon process.  The Dragon process invokes `SpotAsmR64` once, giving exactly
three ASM calls and one SPOR64K call.  It is single-threaded, has fixed wall,
CPU, output-file and core-dump limits, a 50 ms sampled ceiling on the leader
process RSS, and no retry path.  The RSS check is not a process-group aggregate
hard limit.  The
posterior links GANLIB/UTILIB only and cannot call ASM, SPOR64K, FLU, or a
transport solver.

## Accepted bounded execution

The accepted activation completed the materializer in 1.190 s and the one
Dragon process in 2.325 s.  Its runtime census was exactly three `ASM` calls,
one `SPOR64K` call, and zero `FLU`, `SPOFSRC`, `SPOFCHK`, `CONT`, or Picard
calls.  The independent posterior was run twice read-only and produced
byte-identical output.

All 179,820 response values were finite.  The signed-zero-safe nonzero counts
were 35,518 in each plane (106,554 total).  The posterior also checked 1,110
leakage values and 9,990 values in each of `TXSC`, `S0PHYS`, and `S0USED` bit
for bit.  It recursively compared 71,280 copied records containing 54,477,882
32-bit words.  The input `PROJECTED` hash remained
`c010c0a860884a4e4d3842dffe45ffb4898f2aaca99557e0411ee8c66d60b90c`;
the persistent `ASSEMBLED` evidence-copy hash is
`16f79f8fd97ff90ca9bd892cdeab27337fafb3ec6189d9b00b90375fcc596e79`.

One earlier activation was rejected before the B2m begin marker and before
any `ASM` or `SPOR64K` execution because the procedure loader's exact source
companion was not visible.  It contributes no scientific evidence.  The
accepted activation supplied both the hash-frozen source companion and the
precompiled object.  Under the frozen object-first loader path that object was
the selected payload; no procedure-compilation error marker appeared.
Exact evidence and scope are frozen in [runtime_result.txt](runtime_result.txt).

A normal return without the independent posterior is not scientific evidence.

## Development history

One prior invalid activation stopped in `kdrdpr` because the runtime case
contained the precompiled object but not the source name required for loader
visibility.  It stopped before the B2m begin marker and before every ASM call:

```text
prior invalid activations = 1
prior actual ASM executions = 0
```

That activation is diagnostic history only and contributes no scientific
evidence.
