# Phase A9b-B2d: production-link closure

B2d closes one concrete gap found only when the complete Dragon executable
was linked after B2c. `SPOR64_A8` intentionally retained the checked external
interfaces frozen in Phase A8, but current GANLIB exports `LCMLEN`, `LCMGPD`
and `LCMGIL` as `LCMAUX` module procedures. Their linker names therefore did
not match.

[`src/SPOR64_GANLIB_ABI.f90`](../../../src/SPOR64_GANLIB_ABI.f90) is a narrow
ABI bridge. It defines exactly the three external names consumed by A8 and
forwards them to exactly the three GANLIB module procedures. It owns no state,
performs no numerical arithmetic, writes no GANLIB record, and contains no
solver or publication policy. The frozen A8 source is not changed.

Run the link gate with:

```sh
sh validation/iterative/real64_phase_a9b_b2d_link/run_phase_a9b_b2d_link.sh
```

The gate performs one production `make -C src`, verifies that the resulting
Dragon binary contains B2b, B2c, A8 and the three bridge symbols without an
unresolved GANLIB seam, and runs one GANLIB-only forwarding harness. It does
not execute Dragon, open tracking, or solve transport. The frozen receipt is
checked both before and after the production build, so a nested build cannot
silently change a library or build recipe used by the gate.

This also records a simplification: no multi-epoch object protocol is needed
for the next one-call gate. Object reuse must be designed only if a future
host actually reuses one published object across outer SPOD updates.

The shipped host is not yet allowed to execute this route. `SpotPlaneFS`
creates a fresh output `FLUX`, whereas B2b currently admits only a recovered
output that already contains `L_FLUX`, `FLUX`, `STATE-VECTOR` and
`EPS-CONVERGE`. Adding `R64` to the procedure call would therefore fail at
admission; it would not test transport or convergence. The next gate is a
zero-solve topology/lifecycle proof for a fresh output plus a read-only
`FLUX_OLD` input. Only after that contract is frozen may a bounded plane-1
execution be considered.

Passing B2d proves production link closure, not runtime provenance or
convergence. The authoritative result remains:

```text
DRAGON-EXECUTIONS=0
TRACKING-READS=0
TRANSPORT-SOLVES=0
RADIAL-CONVERGENCE=NOT-EVALUATED
OUTER-PICARD-CONVERGENCE=NOT-EVALUATED
```
