# Radial inner-solver verifiability route

## Decision

The next SPOD validation step is a **continuous REAL64 radial working
lane**, limited to the already frozen `TYPE S + MCCG` case.  The current
freeze authorizes only implementation, compilation, static interface
closure, and synthetic unit tests.  It authorizes no Dragon process,
transport sweep, full Stage-4 map, or Picard trajectory.

This is a numerical solver-validation lane, not a new SPOD model.  The
online radial solve and its return to the axial problem remain part of the
map.

## Why an archived residual is not the next gate

The existing XSM objects contain the terminal flux, physical source data,
cross sections, geometry mappings, self-collision data, and ACA
preconditioner/correction records.  They do not contain the complete MOC
transport operator, which is applied by traversing the external sequential
tracking file.  In addition, the archived `SOUR` is the last sweep input
whereas the archived `FLUX` can already include ACA, rebalancing, and FLU
acceleration.  They are not a guaranteed same-point equation pair.

Consequently:

- using the ACA matrix or `PJJ` as \(A\) is invalid;
- reapplying the production sweep can give a solver-consistent fixed-point
  residual, but it is not implementation-independent;
- without a bound on the inverse discrete operator, a residual norm is not
  a bound on the flux-state error;
- no residual multiplier, ULP limit, balance cutoff, angle cutoff, or
  improvement factor is introduced as an acceptance rule.

The already captured raw-MOC observable remains useful diagnostic evidence,
but it cannot overturn the frozen Stage-4 \(R_a\) result.

## Minimal complete precision boundary

For the locked case, the mutable state must remain binary64 through

```text
FLU2DR source/state/update/norm
  -> DOORFV
  -> MCCGF
  -> MCGFLX
  -> MCGMRE
  -> MCGFL1
  -> MCGFCS + MCGFCA/MCGFCR + MCGABG + MCGPRA/MSRLUS1
  -> raw MOC response
  -> FLUBAL with ALSBD
  -> FLU2AC
  -> strict terminal decision
```

Every physical source, cross section, geometry, and tracking input retains
its frozen storage kind.  Binary32 inputs are promoted exactly when mixed
with the binary64 state; existing binary64 track lengths and angular data
remain binary64.  Nothing is refitted or modified.  Existing double-vector
kernels such as `MCGFCF`, `MCGFFIR`, `MCGFST`, `MCGPRA`, and `ALSBD` may
be reused.  `MCGSCA` is listed separately as a frozen mixed-precision
operator kernel, not as a binary64 mutable-vector kernel.  `MCGFMC`,
`MCGABGR -> MCGACA`, and `MCGSCR` are frozen inactive for this exact branch
and are not presented as required REAL64 implementation nodes.

The exact transport branch is also frozen: `IPHASE=1`, no double
heterogeneity, no prism reconstruction, initial `NGEFF=370`, and
`ISCH=11` (`NON CYCLIC - STIS 1 - SC SCHEME - TABULATED EXP`).  As
`IGDEB` advances, the direct-vector active set remains the ordered
contiguous range `IGDEB..370` and `NGEFF` decreases accordingly; it is not
artificially held at 370.  Inside each gathered set, `MCGMRE/NCONV` may
become a non-contiguous subset as individual groups meet the MCCG criterion;
that mask must also remain supported.  The operator tuple is

```text
MCGFCF -> MCGFFIR -> MCGSCA -> MCGFST
```

`MCGSCA` contains `TAU=REAL(TAUD)` and binary32 exponential-table
arithmetic.  Those operations belong to the unchanged mixed-precision
transport operator, not to the mutable iteration state, so the first lane
preserves them exactly.

The authoritative terminal audit records are GANLIB type 4.  Only after a
strict terminal decision may the lane round once into the existing type-2
`FLUX/SOUR` interface used by SPOD.  The claim is therefore a continuous
REAL64 **radial inner solve with one terminal public-output rounding**, not
an all-REAL64 Dragon or all-REAL64 SPOD map.

A local promotion of only `MCGFCS`, `MCGMRE`, or `MCGFLX` is rejected,
because it returns to binary32 mutable state within the iteration.
Changing an old unversioned F77 callee from four-byte to eight-byte `REAL`
without changing every caller is also rejected: that can compile while
misreading memory.  The implementation must use a separate default-off
route with checked interfaces and must fail closed outside the frozen
branch.

## Existing ACA cutoff

The live locked path in `MCGABG` contains the inherited literal
`EPSMAX=1E-7` (`0x33d6bf95` in binary32).  (`MCGABGR` is outside this path
because `MCGMRE` calls `MCGFL1` with `LAST=.FALSE.`.)  This project does not
introduce, fit, or tune that value.  For every live Boolean guard derived
from `EPSMAX`, `EPSINF`, or `EPS2`, the REAL64 lane evaluates a diagnostic
counterfactual using the same finite operands with `EPSMAX=0`.
`cutoff_active` is incremented exactly when the two Boolean outcomes differ.
This includes zeroing, stopping, and the lucky-breakdown/\(W_I\) branches.
The counterfactual cannot alter the production action or state.

If `cutoff_active != 0` in the feasibility experiment, the result is
`INCONCLUSIVE-INHERITED-CUTOFF`, not evidence for or against REAL64.  The
project stops there instead of tuning the cutoff.  This preserves the rule
that an empirical solver constant cannot become a SPOD acceptance
coefficient.

## Two bounded gates

### A. Static closure

This is the only currently authorized work:

1. implement a default-off, suffixed path for the exact locked branch;
2. enumerate every mutable array, control-affecting norm, acceleration
   scalar, and call boundary in a machine-readable precision manifest;
3. prove that there is no binary32 round trip before terminal acceptance;
4. freeze the OFF-arm parser for ordered non-timing scientific log records;
5. compile with checked interfaces and run synthetic tests only;
6. prove that incomplete manifests and unsupported branches fail closed.

Passing this gate is implementation evidence only.  It says nothing about
transport or SPOD convergence.

The first subgate, Phase-A1, is now implemented only as an isolated
validation-tree slice.  It closes the locked `MCGFCS` source arithmetic,
the explicit binary32-entry to binary64-working conversion, and a
terminal-only binary32 adapter.  Its compile-fail, sub-binary32-ULP,
fail-closed, link-isolation, and manifest-mutation tests run with

```sh
make spot-real64-phase-a1
```

Phase-A1 is `IMPLEMENTED-PARTIAL-SLICE-ONLY`: it is not connected to
production and does not close the `MCGFL1` caller, primary MOC response,
the wider radial state, or any terminal norm.  It therefore does not pass
the complete static-closure gate above.  The implementation boundary and
its exact limitations are recorded in
[`real64_phase_a1/README.md`](real64_phase_a1/README.md) and
[`real64_phase_a1/precision_manifest.json`](real64_phase_a1/precision_manifest.json).

Phase-A2 is also implemented only inside the validation tree.  It adds one
typed, full-matrix active-mask callback between the Phase-A1 source and the
post-`MCGFST`, pre-`MCGFCA` raw-response boundary:

```sh
make spot-real64-phase-a2
```

The short gate enumerates all 31 nonempty masks over its five gathered
columns, checks exact inactive `+0`, complete finite active output and
failure atomicity, rejects REAL32 mutable arguments and callbacks at
compile time, and proves link isolation.  Its signed-permutation callback
is only an algebraic oracle.  Phase-A2 does not call `MCGFCF`, `MCGFFIR`,
`MCGSCA`, `MCGFST` or ACA and does not read a tracking file.  Thus
`IMPLEMENTED-PARTIAL-SOURCE-TO-RAW-FACADE-ONLY` is still not a continuous
REAL64 radial lane or a convergence result.  The exact boundary is in
[`real64_phase_a2/README.md`](real64_phase_a2/README.md) and
[`real64_phase_a2/precision_manifest.json`](real64_phase_a2/precision_manifest.json).

Phase-A3 is a compile-only checked legacy-ABI seam for the exact frozen
`MCGFCF`-through-`MCGFST` path:

```sh
make spot-real64-phase-a3
```

It encodes the ordered call
`MCGFCF(MCGFFIR,MCGFFAR,MCGFFAL,MCGSCA,...)->MCGFST` with the actual
legacy data kinds, ranks, procedure identities, and call boundaries.
A deliberate unresolved link symbol is part of the contract, so the gate
performs zero Phase-A3 links, creates no Phase-A3 executable, executes
zero Phase-A3 calls, and runs zero transport solves and zero Dragon
processes.  This is static ABI evidence only: it is disconnected from
production and does not validate MOC behavior or convergence.

Phase-A3 also records that the frozen legacy `MCGFL1` caller forms
`XSIXYZ(1,IDIR)` with `IDIR=0`.  That is a nonconforming actual designator.
The validation seam uses a legal caller-owned `XSI` vector to make its own
interface conforming; it does not claim to repair or validate the
production caller.  The exact boundary is in
[`real64_phase_a3/README.md`](real64_phase_a3/README.md) and
[`real64_phase_a3/precision_manifest.json`](real64_phase_a3/precision_manifest.json).

Phase-A4 is the validation-only, compile-only host closure from the
Phase-A2 façade into the Phase-A3 seam:

```sh
make spot-real64-phase-a4
```

Its caller-owned context storage schema is closed.  Population from the real
`MCGFL1` host and the provenance of tracking, `KPSYS/PJJ`, geometry,
material, group-order, and `/EXP1/` identities remain unbound.  Phase-A4
objects are linked zero times and executed zero times.  Its recursive short
gate links and executes the frozen Phase-A1 and Phase-A2 synthetic programs
once each, but performs zero tracking reads, zero transport solves, and zero
Dragon processes.  The exact boundary is in
[`real64_phase_a4/README.md`](real64_phase_a4/README.md) and
[`real64_phase_a4/precision_manifest.json`](real64_phase_a4/precision_manifest.json).

The next static step is a compile-only Phase-A5 real-host population and
provenance contract, with the unresolved link barrier preserved and no
transport execution.  Until that and all later gates are separately passed,
ACA, rebalancing, acceleration, the wider mutable radial state, terminal
norms, real MOC operation, physical accuracy, and all solver/Picard
convergence claims remain open.

### B. Plane-1 feasibility

This gate is frozen but not authorized.  A later explicit authorization may
run one bounded capture process.  Both arms start from the same preserved
plane-1 cap state:

- the legacy-OFF arm performs the frozen six-update native cycle and must
  reproduce its existing standard output bit for bit and its ordered
  non-timing scientific records exactly under the pre-run frozen parser;
- the REAL64-ON arm uses the unchanged \(h/2\), `MAXOUT=500`,
  `MAXINR=740`, `ACCE 3 3`, rebalancing, and MCCG controls, with normal
  strict early termination;
- the wall-clock limit is a safety bound, not a scientific criterion;
- no retry, tolerance search, longer cap, or automatic replay is allowed.

Plane 1 is selected because the existing radial-floor and raw-MOC evidence
already bind that lane, not because it is assumed to be the worst plane or
the cause of the axial response.

The only positive feasibility condition is the existing strict FLU
terminal gate, reached before the unchanged iteration cap, with no
cutoff-active event and with the existing finite/positive/source/layout and
structural checks.  Balance diagnostics must be finite and nonnegative but
have no magnitude acceptance gate.  A first success is only
`PENDING-REPLAY`; a separate exact replay is required for
`REAL64-RADIAL-FEASIBLE`.

Classification is first-match and phase-specific.  For capture, legacy
identity failure precedes timeout, structural invalidity, `cutoff_active`,
cap exhaustion, and finally a strict `PENDING-REPLAY`.  After a pending
capture, replay applies the same early invalid/inconclusive checks, then
classifies a scientific mismatch as `INVALID-NONREPRODUCIBLE`; only exact
reproduction becomes `REAL64-RADIAL-FEASIBLE`.

`REAL64-RADIAL-FEASIBLE` means only reproducible attainment of the existing
FLU stopping rule in this locked lane.  It is not an independently evaluated
equation residual, a flux-error bound, a conservation-accuracy proof, or a
physical-solution accuracy claim.

## Later Stage 4

Only `REAL64-RADIAL-FEASIBLE` may lead to a separately frozen full map
comparison.  That comparison must recompute both

\[
G_h^{64}(x_0),\qquad G_{h/2}^{64}(x_0)
\]

from the same \(x_0\) and fixed POD basis.  It may not mix a new REAL64
\(h/2\) map with the archived binary32 \(h\) map.  The original four
component rule remains unchanged:

\[
D_{\mathrm{in},i}<D_{\mathrm{out},h,i},
\qquad
i\in\{R_\rho,R_L,D_L,R_a\}.
\]

If an outer component is exactly zero, the corresponding inner component
must be exactly zero.  There is no weighted score or fitted factor.  Only
an all-component pass plus exact replay can permit a separately frozen
direct Picard trajectory.

The complete machine-readable contract is
[`radial_real64_route_protocol.json`](radial_real64_route_protocol.json).
