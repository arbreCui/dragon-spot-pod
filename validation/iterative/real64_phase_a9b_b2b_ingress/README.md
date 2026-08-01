# Phase-A9b-B2b read-only ingress gate

This is a seconds-scale, compile-only gate for the first production host
rendezvous of the default-OFF `R64` route.

It authorizes only the following structure:

1. `FLU` parses `R64` once, then its selected branch calls exactly one
   `SPOR64_B2B_INGRESS` and explicitly returns.  It cannot fall through to
   legacy `FLUDRV`, legacy writes, or a second transport path.
2. `SPOR64_B2B_INGRESS` admits the frozen live host snapshot read-only.  It
   contains no LCM mutation, `XABORT`, stream `READ`/`REWIND`, `SAVE`, audit
   publication, relaxation, fitted coefficient, or model completion.
3. Only after `admission_complete=.true.` may it call the unchanged,
   zero-argument `XDRTA2`; the next and only side-effecting call is the single
   `FLU2DR64_CORE` rendezvous.
4. The legacy branch retains one bare, zero-argument `CALL XDRTA2` at its old
   location before `FLUDRV`.

The runner compiles the real GANLIB modules, SPOMOC bridge, A8/A9 modules,
`SPOR64_B2B`, `FLUGPI`, `FLU`, and `XDRTA2` into temporary objects.  These
production objects are never linked or executed.  A separate four-case
synthetic dispatch executable checks OFF, selected, admission-failure, and
core-failure event flow; it contains no production core or transport symbol.
An explicit-interface positive/negative compile pair locks the zero-argument
`XDRTA2` ABI.

The claim is local to this route.  The known pre-existing
`src/ASM.f:101` call still supplies an actual argument to the zero-argument
procedure and is outside B2b, so this gate records
`GLOBAL-XDRTA2-ABI-CLEAN=false` rather than claiming a repository-wide repair.

Run:

```sh
make spot-real64-phase-a9b-b2b-ingress
```

This gate does **not** authorize a Dragon run, accepted-result publication,
physical transport claims, radial convergence, or outer Picard convergence.
The reported `TRACKING-READS=0` and `TRANSPORT-SOLVES=0` describe this
compile/static/synthetic validation run; a later real core execution will read
the frozen tracking stream inside the already-audited A8 transport operator.
Those physical executions and claims remain separate later gates.
