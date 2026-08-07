# Phase-A9b B2k: fresh radial SYSTEM assembly commit

B2k closes exactly one lifecycle gap left intentionally by B2j.  B2j has
already projected the canonical Synthesis-POD flux and leakage into all three
planes.  The new, unselected candidate procedure wires that projected archive
to three real `ASM:` calls through `LK1D 1`, `LK1D 2`, and `LK1D 3`.  B2k
admits the three complete,
fresh `L_PIJ` results of those independent ASM calls and publishes them as one
archive-wide transaction.

```text
archive PROJECTED/1 + three fresh ASM SYSTEM candidates
    -> fresh archive ASSEMBLED/1
```

The projected FLUX objects remain `PROJECTED/1`; assembling a radial operator
does not solve a new flux.  The archive and every committed SYSTEM authority
become `ASSEMBLED/1`.  The parent `RHO` is copied bit-for-bit.  Archive-root
`EPOCH=1` is the final LCM mutation.

## Physical identities

For every plane `p`, group `g`, and material slot `m=1..8`, the fixture
constructs a fresh SYSTEM by the same ordered binary32 operations as
`ASMDRV` with the established transport correction:

```text
TXSC[p,g,0]   = +0
TXSC[p,g,m]   = NTOT0[p,g,m] - TRANC[p,g,m]

S0PHYS[p,g,0] = +0
S0PHYS[p,g,m] = SIGW00[p,g,m] - TRANC[p,g,m]

S0USED[p,g,0] = +0 - LEAK1D[p,g]
S0USED[p,g,m] = S0PHYS[p,g,m] - LEAK1D[p,g]
```

`S0USED` is stored as `DRAGON-S0XSC`.  It is deliberately evaluated in two
binary32 steps.  The rounding witness
`0x3d000000, 0x3c000000, 0x3c000001` produces `0x3c7fffff` for
`(x-y)-z`, while the forbidden reassociation `x-(y+z)` produces
`0x3c800000`.

There is no damping, relaxation, clipping, floor, fitted coefficient, or
empirical tolerance in this transition.

## Complete SYSTEM, not a surrogate

The dynamic gate does not execute ASM.  Instead it synthesizes three complete
fresh candidates with the exact root and response schemas observed at the real
ASM boundary: seven root entries, and the five ACA records, seven PJJ records,
and three cross-section families in every one of the 370 group directories.
No record is copied from the lagged B2i SYSTEM.  B2k deep-copies the complete
candidate and adds only its eighth root entry, the `SPOT-R64` lifecycle
authority; it does not reconstruct a smaller SYSTEM.  The gate proves this by
bit-checking all group payloads, checking distinct nested pointers, then
perturbing each of the 15 candidate record families after commit and proving
the already-committed output remains unchanged.

The synthetic ACA/PJJ values establish only exact schema, finiteness, and
deep-copy behavior.  They do not validate the numerical response matrices or
their transport physics; that requires a future execution of the real ASM
route.

The validation fixture starts from the same three frozen XSM inputs used by
B2j.  After `B2J_BUILD_CLOSED_PAIR`, it restores the real `NTOT0`, `SIGW00`,
and `TRANC` records from the same-index real library into the lightweight
closed archive, runs production B2j, and independently checks 1,110 leakage
slices plus 9,990 binary32 values in each of `TXSC`, `S0PHYS`, and `S0USED`.

The commit is all-or-nothing.  Collision, lifecycle mismatch, an extra input
SYSTEM list, candidate aliasing, old B2i sentinels, wrong plane/leakage or
cross-section bits, missing response records, non-finite data, and a late
plane-3 failure all leave the caller's fresh output completely empty.  The
same preflight also freezes the real MCCG control state and proves
`MATCOD/NZON$MCCG`, `VOLUME/V$MCCG`, and the scalar/current unknown maps are
coherent; dedicated mutations of those maps are rejected with zero writes.

Run the seconds-scale gate with:

```sh
sh validation/iterative/real64_phase_a9b_b2k_system_assembly/run_phase_a9b_b2k_system_assembly.sh
```

The runner compiles production B2c/B2i/B2h/B2j/B2k and the in-memory harness
with strict floating-point/runtime flags.  It also compiles the unselected
`SpotAsmR64.c2m` source to a temporary nonempty object with GANLIB's real
`clepil` and `objpil` routines, and object-compiles both the caller and the
zero-argument `XDRTA2` definition.  It never starts Dragon, `ASM`,
`ASMDRV`, a tracking-door routine, transport, QFISS construction, or CONT.
The candidate procedure, dispatcher registration, and ASM's zero-argument
`XDRTA2` ABI are inspected statically.  This removes the known host-wiring
blocker but does not constitute an execution of that route; therefore
`C2M-EXECUTION=NOT-EVALUATED`, `REAL-ASM-EXECUTION=NOT-EVALUATED`,
`RADIAL-CONVERGENCE=NOT-EVALUATED`, and
`OUTER-PICARD-CONVERGENCE=NOT-EVALUATED` are the only valid execution claims.
