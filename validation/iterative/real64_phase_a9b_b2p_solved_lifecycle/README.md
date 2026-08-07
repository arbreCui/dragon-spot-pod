# Phase-A9b B2p: accepted CONT publishes `SOLVED(n)`

B2p closes the publication boundary after one accepted REAL64 continuation
call. It changes no radial equation, convergence norm, cutoff, or numerical
algorithm, and the default gate executes no production transport solve.

## State transition

The intended local lifecycle is deliberately small:

```text
sealed PROJECTED(n)
        |
        | B2B joint CONT admission + unchanged A9 accepted result
        v
       SOLVED(n)
        |
        | existing B2H projection boundary
        v
     PROJECTED(n+1)
```

B2C copies the sealed seed's `RHO`, `PLANE`, and `EPOCH`; it does not invent
or increment them. Only B2H owns the existing per-plane authority
`n -> n+1` transition. Here, `n` describes the local copier contract.
Production admission and the short evidence are restricted to `n=1`; a
general multi-generation production flow is not yet implemented.

On the real B2B call path, `SOLVED(1)` has one narrow meaning: the local radial
fixed-source solver, under the already frozen `QFISS` and already assembled
SYSTEM admitted by B2B, returned `core_ok` and accepted under the unchanged A9
terminal predicates. It does not mean
that the outer 2D/1D Picard map, all three planes, a new eigenvalue, or a
benchmark comparison has converged.

The metadata are labels inherited from the admitted local state:

- `RHO` is copied bit-for-bit from the sealed PROJECTED seed. It labels the
  frozen equation; B2C does not recompute a terminal eigenvalue.
- `PLANE` is the local three-entry archive index in `1:3`, not a global
  spatial or run identifier.
- `EPOCH` is a local generation/commit label, not a globally unique lineage
  identifier.

The published `SOUR` is the terminal total radial right-hand side returned by
A9. It is not the frozen `QFISS` alone and is not claimed to be a newly
recomputed fission source.

## Production change

The old 16-argument `SPOR64_B2C_PUBLISH` entry point and BOOT route remain
unchanged. A separate `SPOR64_B2C_PUBLISH_CONT` entry point accepts the
sealed seed object; it accepts no caller-supplied `RHO`, `PLANE`, `EPOCH`,
relaxation factor, or tolerance.

Before its first caller-visible write, the CONT publisher requires the exact
seed authority

```text
RHO, PLANE, FLUX, STATE=PROJECTED, EPOCH
```

with finite positive binary64 `RHO`, a plane in `1:3`, a nonnegative
nonterminal integer epoch, and 370 finite type-4 FLUX list elements of length
14. It also repeats the fresh-output check immediately before publication.
Every recoverable rejection therefore precedes the first write.

After an accepted B2B core return, the CONT route publishes the exact
authority

```text
RHO, PLANE, FLUX, SOUR, STATE=SOLVED, EPOCH
```

where FLUX and SOUR are the returned terminal binary64 arrays. Existing root
FLUX/SOUR compatibility mirrors remain binary32. `EPOCH` is the final LCM
mutation and marks the logical object complete. It is not an ACID transaction
or global lineage proof. After the first write, only the pre-existing fatal
GANLIB/XABORT semantics remain; there is no recoverable partial commit.

B2C itself revalidates the sealed PROJECTED seed. The binding to the frozen
source and assembled SYSTEM is supplied by the immediately preceding
production B2B joint admission; the integer labels alone are not independent
physical proof. A direct caller can supply the public publisher's integer
accepted token, so only the integrated B2B path carries the stated `SOLVED`
physical meaning.

## Short validation

Run:

```sh
make spot-real64-phase-a9b-b2p-solved-lifecycle
```

The gate uses production B2O, B2B, B2C, and B2H, but replaces `XDRTA2` and the
A9 transport core with narrow capture stubs. The stub returns terminal FLUX
and SOUR arrays that differ from both inputs and retain deterministic
REAL64-only low bits. Its SOUR is a synthetic publication witness, not a
physical RHS evaluation. The ASSEMBLED and FROZEN-QFIS lifecycle authorities
are also synthesized around the five pinned base fixtures; they are not
production B2K/B2N outputs. The integrated control/interface path is

```text
B2O seal -> real B2B CONT -> accepted stub core
         -> B2C SOLVED/1 -> real B2H PROJECTED/2
```

It checks:

- all 10,360 SOLVED type-4 FLUX/SOUR values and all 10,360 binary32 mirrors;
- all 5,180 PROJECTED type-4 FLUX values and all 5,180 mirrors;
- bit-exact inheritance of a non-unit, REAL64-only `RHO`, `PLANE=2`, and
  `EPOCH=1`, followed by B2H's existing `EPOCH=2` publication;
- the exact SOLVED authority inventory and the unchanged legacy B2C authority
  `{FLUX,SOUR}`;
- 16 pre-publication lifecycle/fresh-output rejections, including wrong
  state, plane bounds/type, extra metadata, invalid `RHO`, epoch type/range,
  malformed type-4 FLUX, a type-4 NaN in the final group, and a nonempty
  output whose sentinel remains exact;
- one output/seed alias rejection, one nonaccepted-token rejection with an
  otherwise valid seed/output pair, and two real-B2B calls whose stub returns
  `core_ok=false` or `accepted=false`, all with empty outputs;
- five full sealed-seed checks over exact metadata and all 5,180 type-4 plus
  all 5,180 root-mirror FLUX bits, before and after the tested calls;
- 35 mutation tests over the ABI, admission, seed immutability, complete FLUX
  scanning, accepted-token and accepted-result publication, ordering, routing,
  and B2H increment;
- an old-object smoke test compiled against the B2o parent `SPOR64_B2C.mod`
  and linked and executed against the current legacy wrapper;
- byte-for-byte immutability of all five input fixtures; and
- absence of the production FLU, Dragon, transport, and A8/A9 implementations
  from the linked harness; its `FLU2DR64_CORE` symbol is supplied by the
  explicit capture stub.

The B2H call proves that the new SOLVED schema is consumable and that B2H's
existing epoch increment still works. Its projected regional field and `RHO`
are synthetic caller inputs; it does not run B2J or compute a real SPOD
projection. The resulting PROJECTED/2 object is not evidence of a canonical
next Picard state.

The gate normally completes in a few seconds. It does not execute or measure
a physical radial iteration, so radial convergence and outer Picard
convergence remain `NOT-EVALUATED`.

## Remaining boundary

B2p does not make a second CONT call possible. The current B2H output does
not carry `PLANE`, and its projected-region and `RHO` inputs are not yet bound
to one canonical SPOSTATE; B2J's exact SOLVED schema does not yet accept
`PLANE`; B2J, B2K, B2N, B2O, and B2B still contain first-generation
assumptions; and no boundary yet packages three accepted SOLVED planes plus
the updated axial state into the next closed archive. A valid next generation must rebuild
PROJECTED, SYSTEM, and QFISS at epoch 2 instead of reusing epoch-1 objects.
Those are the next lifecycle changes.

No empirical physical/coupling coefficient, relaxation, clipping, fitted
tolerance, normalization, fallback, or model completion is introduced by
B2p. Pre-existing A9 numerical controls are outside this change.
