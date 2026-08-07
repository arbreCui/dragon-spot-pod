# Phase-A9b B2u: deployment-default-off same-call ASM host

B2u freezes the smallest production route that closes the remaining
candidate-SYSTEM custody gap above B2t.  It adds no equation, coefficient,
relaxation rule, damping rule, clipping rule, fitted quantity, convergence
threshold, or retry policy.

The suffixed `SpotStepR64` CLE-2000 procedure has this external contract:

```text
RETURNED := SpotStepR64 PROJECTED TRACK_f :: ;
```

It is **deployment-default-OFF**: `SpotStepR64` is not selected by any shipped
calculation deck.  This is deliberately a deployment statement, not an
in-procedure Boolean switch.  Once a future deck explicitly selects the
procedure, its fixed route is active.

## Frozen route

The host recovers the same-index material library and tracking object for
each plane, creates three distinct local SYSTEM objects, and preserves them
until one immediate adapter call:

```text
same PROJECTED symbol + same TRACK_f symbol
  -> ASM(LK1D 1) -> SYSTEM1
  -> ASM(LK1D 2) -> SYSTEM2
  -> ASM(LK1D 3) -> SYSTEM3
  -> SPOR64T(PROJECTED,SYSTEM1,SYSTEM2,SYSTEM3,TRACK_f)
  -> production B2t
  -> RETURNED/1, if the later enabled route succeeds
```

`SYSTEM1`, `SYSTEM2`, and `SYSTEM3` are local to this procedure.  They are
not caller inputs, are not committed through a detached `SPOR64K` call, and
are deleted only after `SPOR64T` returns.  The caller therefore has no place
to substitute a persisted SYSTEM between ASM and B2t.

The thin `SPOR64T:` adapter admits exactly six entries:

```text
HENTRY = RETURNED, PROJECTED, SYSTEM1, SYSTEM2, SYSTEM3, TRACK_f
IENTRY = 1,        1,         1,       1,       1,       3
JENTRY = 0,        2,         2,       2,       2,       2
```

It consumes an exact empty option list, maps `KENTRY(3:5)` to the SYSTEM
array, forwards `KENTRY(6)` as the tracking-file handle, and calls
`SPOR64_B2T_HOST_STEP(...,.true.)`.  Only `SPOR64_B2T_RETURNED` is success.
The INT64 plane cutoffs remain unaggregated diagnostics and do not affect
acceptance or physics.  `KDRDRV` exposes exactly one `SPOR64T:` route between
the existing `SPOR64K:` and `FLU:` routes.

B2u introduces no numerical control of its own.  If the route is selected in
a later run, it inherits the already frozen downstream termination and
acceleration settings from B2t/B2S/B2B; this phase neither retunes nor replaces
them.

## Tracking-file lifetime boundary

The source-level route proves use of the same CLE `TRACK_f` symbol in all
three ASM expressions and in the final `SPOR64T` expression.  The validation
contract pins the intended future runtime artifact to
`f7b27cb4a5d37f903b93e49610e2daa2290d55c164e2ca0e73ccb8d22fe486b8`
(2,275,636 bytes).  The short gate verifies this artifact before and after but
does not open it through ASM or SPOR64T.

It does **not** prove one live `c_ptr` across ASM1, ASM2, ASM3, and SPOR64T.
DRAGON's `dramod` opens a sequential file before each module dispatch and
closes it when that dispatch returns.  The three ASM calls and SPOR64T therefore use separate
per-dispatch opens of the same CLE symbol/file bytes.  Inside the single
SPOR64T dispatch, however, `KENTRY(6)` remains live while the ordinary Fortran
call chain enters B2t, B2s, and all three B2B calls; that narrower same-live-
handle relation is inherited from the frozen B2t contract.

Neither the symbolic name nor the frozen hash proves that the binary file was
historically used to construct the archived TRACK objects.  That historical
claim remains outside B2u.

## Short gate and claim limit

The checker freezes the exact host order, common symbols, live local SYSTEM
scope, adapter ABI, dispatcher route, deployment selection census, DRAGON
`dramod` per-dispatch file lifetime, frozen tracking-file identity, and documentation
scope.  The accompanying suite contains 39 targeted mutations plus one
positive baseline.  The real CLEPIL/OBJPIL compiler accepts the production
procedure and the validation OFF/ON selection shapes.

The executable witness calls the production `SPOR64T` adapter seven times:
five ABI/option-list preflight rejections, one capture-stub B2t failure, and
one capture-stub success.  The two calls that reach B2t verify the ordered
three-SYSTEM slice and the current-dispatch `TRACK_f` pointer.  This is
adapter ABI and pointer-forwarding evidence only; the B2t implementation in
that executable is a deterministic capture stub.

Separately, the complete production B2C/B2B/B2O/B2R/B2S/B2K/B2N/B2T/B2U
interface chain, production `ASM.f`, and the preprocessed `KDRDRV.F` are
strictly compiled but never linked into the executable witness.

No Dragon, ASM, radial transport, or Picard execution is performed by this
gate.  Passing establishes only:

```text
SAME-CALL ASM-TO-B2T HOST ROUTE = STATICALLY FROZEN
DEPLOYMENT DEFAULT              = OFF
RUNTIME ASM / TRANSPORT / MAP   = NOT EXECUTED
```

It does not establish radial convergence, outer Picard convergence, response
accuracy, eigenvalue or power accuracy, SPOD truncation accuracy, or agreement
with an independent transport code.  A later separately authorized,
hard-bounded run is required for the first real continuation sweep.
