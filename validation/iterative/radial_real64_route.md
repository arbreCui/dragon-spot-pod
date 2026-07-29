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
