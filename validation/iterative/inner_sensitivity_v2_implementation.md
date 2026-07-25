# Stage-4 v2 implementation boundary

This implementation evaluates one coarse map

\[
x_{1,2h}=G_{2h}(x_0),\qquad 2h=10^{-6},
\]

from the frozen Stage-3 state and rank-one POD basis.  The fine map
\(x_{1,h}\), with \(h=5\times10^{-7}\), is archival evidence and is never
rerun by this implementation.

The coarse deck contains exactly three online radial fixed-source solves and
one returned axial solve.  It contains no initializer, basis rebuild, outer
iteration, relaxation, fitting, clipping, flux floor, or empirical
coefficient.  It also does not call `SPOGBAL`: the frozen executable contains
a legacy 13-character Ganlib record literal, while Ganlib record names are
limited to twelve characters.  Balance is therefore reconstructed offline
without changing the frozen transport executable or the map physics.

## Default behavior

The production entry point defaults to preflight:

```sh
python3 validation/iterative/run_inner_sensitivity_v2.py \
  --dragon /absolute/path/to/frozen/Dragon
```

Preflight verifies all frozen hashes, compiles and scans all three Ganlib-only XSM
checkers, and prints `DRAGON-RUNS 0`.  It cannot accept an output path,
authorization, or replay evidence.  The execution ledger is not a command-line
option: it has the single fixed repository path
`validation/artifacts/inner-sensitivity-v2-execution-ledger`.

No run authorization is committed with this implementation.

## Separate execution authorization

A future capture or replay requires a separately reviewed and committed
canonical JSON file with exactly this schema:

```json
{
  "schema": "spot-inner-sensitivity-v2-run-authorization-1",
  "protocol_sha256": "8a870a85ffe7fd4eb53d9494bcf28acea2025f8f3d022579312cd34a22a1d88c",
  "implementation_commit": "<full implementation commit>",
  "ledger_relative_path": "validation/artifacts/inner-sensitivity-v2-execution-ledger",
  "mode": "capture",
  "maximum_dragon_processes": 1,
  "wall_clock_limit_seconds": 120,
  "automatic_replay": false
}
```

`mode` is either `capture` or `replay`; the two modes require different
authorization commits.  A replay authorization additionally contains the
exact committed capture commit, scientific-manifest SHA-256, and
capture-receipt SHA-256.  It must first appear after that capture commit, so a
generic replay authorization cannot be prepared before the
`PENDING-REPLAY` evidence exists.  The runner rejects an untracked, dirty, or
noncanonical authorization file, and it compares every implementation blob in
the authorized commit with the current implementation receipt.

The additional replay fields, placed immediately after `mode`, are:

```json
{
  "capture_commit": "<full committed capture commit>",
  "capture_scientific_manifest_sha256": "<64 lowercase hex digits>",
  "capture_receipt_sha256": "<64 lowercase hex digits>"
}
```

Immediately before starting Dragon, the runner atomically creates a permanent
`capture-spent.json` or `replay-spent.json` tombstone.  Timeout, signal,
abnormal exit, or checker failure still consumes that one process budget.
Replay also requires the capture tombstone to bind the authorization hash in
the committed capture receipt.  There is no automatic retry.

Published artifacts are direct children of `validation/artifacts`, use a
mode-specific `inner-sensitivity-v2-{capture,replay}-...` name, and are
disjoint from the fine, seed, capture, and ledger directories.  Publication
uses the operating system's atomic no-replace primitive.  Final verification
and ledger-lock release occur before success is reported; a failure withdraws
only the artifact inode owned by the current invocation.

## Independent evidence

The raw-log checker requires exactly three radial plus one axial strict
terminal pair with:

- `MAXOUT=500`, `MAXINR=740`;
- `STATE=1` for every solve;
- binary32 tolerance bits `0x358637bd`;
- one normal Dragon end and no failure marker.

One Ganlib-only checker audits the canonical coarse map, direct raw radial
scalar-flux positivity, fixed-source identity, leakage return, and radial
balance.  A separate Ganlib-only balance checker reconstructs the multigroup
fission and scattering source directly from the final flux, immutable
macrolib, axial track, and returned system.  It then evaluates positive axial
scalar flux, group/global transport balance, and the rank-one Galerkin
residual.  These diagnostics must be finite and nonnegative, but no empirical
magnitude threshold is applied.  On the frozen fine artifact, the independent
reconstruction must bit-match its three legacy balance records; the coarse
lane neither creates nor reads those records.

The pairwise Ganlib-only checker compares the fine and coarse XSM states and
emits exact binary64 bits for:

1. \(D_{\rm out,h}=D(x_{1,h},x_0)\);
2. \(D_{\rm out,2h}=D(x_{1,2h},x_0)\);
3. \(D_{\rm in}=D(x_{1,h},x_{1,2h})\).

The four components are, in order, \(R_\rho,R_L,D_L,R_a\).  There is no fifth
component: “five-file manifest” means the five XSM files
`basis_reference.xsm`, `state0_axial.xsm`, `state1_system.xsm`,
`state1_axial.xsm`, and `state1_snapshots.xsm`.

The exact component rule is applied to stored bits:

```text
D_out,2h > 0 and D_in < D_out,2h -> RESOLVED
D_out,2h = 0 and D_in = 0        -> RESOLVED
otherwise                         -> UNRESOLVED
```

No decimal tolerance, aggregation, weighting, or fit is used.

## Capture/replay state machine

- A valid unresolved capture publishes `UNRESOLVED` and forbids replay.
- Four resolved components publish `PENDING-REPLAY`.
- Replay is a separate invocation.  It requires both the capture manifest and
  `capture_receipt.json` in the same named Git commit, the original capture
  artifact, a different artifact directory and different file inodes.  The
  receipt binds the raw log, both XSM checks, exact result bits, authorization,
  input manifest, and one-process record.
- Only byte-identical reproduction of all five files can publish
  `QUALIFIED-ON-2H-TO-H-SCALE`.
- Qualification permits freezing a short Stage-5 protocol; it does not itself
  authorize a trajectory.

Every Dragon process is run in a fresh isolated directory with a fixed
120-second wall-clock limit.  On timeout or a managed external signal, its
exact process group receives `SIGTERM`, followed by `SIGKILL` after five
seconds if necessary.
