# Phase-A9b B2h: fresh REAL64 projected authority

This is a short, host-disconnected gate for the missing state transition ahead
of a REAL64 fission-source builder.  The post-B2g audit found that the current
`SPOPROJ` overwrites only each plane's root type-2 `FLUX`; an older
`SPOT-R64/FLUX` therefore survives and would be read by `R64 CONT` as though it
were the new global-to-plane projection.  That is the wrong Picard map even
when the later source formula is evaluated exactly.

`SPOR64_B2H` freezes two small operations without connecting that route:

- `SPOR64_B2H_RECONSTRUCT` evaluates one fixed-space slice in the explicit
  mode loop order, promoting each stored binary32 basis value at its use and
  accumulating against binary64 coordinates in binary64.
- `SPOR64_B2H_PROJECT` accepts an explicit `SOLVED` type-4 seed, constructs a
  fresh object, replaces only the eight region unknowns with the supplied
  binary64 projection, and preserves the six non-region unknowns directly
  from the seed authority.  It never reads the root type-2 `FLUX` as input.

The seed `RHO` and terminal `SOUR` are checked only as completeness witnesses
for the `SOLVED` state; neither enters the projection arithmetic.

The fresh authority is

```text
SPOT-R64/STATE = PROJECTED
SPOT-R64/RHO   = caller-supplied positive finite binary64 scalar
SPOT-R64/FLUX  = 370 list items, each 14 binary64 values
SPOT-R64/EPOCH = input epoch + 1
```

This boundary preserves and checks the supplied `RHO` bits, but it does not
read `SPOT-X-RHO` or prove that `RHO`, the fixed-space coordinates, the seed,
the tracking map and the plane belong to one canonical state. That same-object
provenance belongs to the archive-level host gate.

`STATE` and then `EPOCH` are written last as the two explicit commit records.
A root type-2 `FLUX` is emitted
only after the type-4 payload has been staged and written.  No `SOUR`,
`QFISS`, frozen-source diagnostic, relaxation parameter, clipping rule or
model completion is copied into the projected object.

The dynamic gate uses the frozen plane-1 `restart_cap.xsm` and
`restart_track.xsm` schemas through real GANLIB.  It creates a synthetic
`SOLVED` authority in memory, adds binary64-only low-bit witnesses, poisons the
root type-2 mirror, and checks the production publisher bit for bit.  Rejected
schema, state, epoch, mapping and numerical cases must leave a fresh output
empty.  Static and mutation checks independently lock the write order and the
absence of a production caller.

Run:

```sh
sh validation/iterative/real64_phase_a9b_b2h_projection_authority/run_phase_a9b_b2h_projection_authority.sh
```

The gate performs compilation and small in-memory calculations only.  It does
not run Dragon, read the sequential tracking file, execute `SPOPROJ`, build a
fission source, call a transport core, or solve transport.

The controlled inventory is:

```text
REAL-B2H-PROJECT-CALLS=14
PREFLIGHT-REJECTIONS=13
COMMITS=1
RECONSTRUCT-CALLS=6
RECONSTRUCT-REJECTIONS=5
REGION-TYPE4-BIT-CHECKS=2960
NONREGION-TYPE4-BIT-CHECKS=2220
ROOT-TYPE2-MIRROR-BIT-CHECKS=5180
RHO-TYPE4-BIT-CHECKS=2
STATIC-CONTRACT-TESTS=27
MUTATION-REGRESSION-CASES=26
PRODUCTION-CORE-CALLS=0
DRAGON-EXECUTIONS=0
TRANSPORT-SOLVES=0
```

This phase intentionally remains unreachable from every shipped C2M
procedure.  Production `B2C` does not yet publish the required explicit
`SOLVED/EPOCH/RHO` records, and legacy `SPOPROJ` remains type 2.  The next stages
must bind the canonical `SPOSTATE` provenance, connect this fresh projection
lifecycle, construct an epoch-matched type-4 `QFISS`, and make B2B compare both
states before any bounded `CONT` execution. The present per-plane publisher
also does not prove that all planes were preflighted and committed as one
archive epoch; that belongs to the future archive-level host gate. Because
`LCMEQU` is a merge-copy and does not delete stale records, that host must
replace a complete plane object or explicitly clear it before committing
`STATE+EPOCH`; merging this fresh object into an old plane is insufficient.
Radial and outer Picard convergence remain `NOT-EVALUATED`.
