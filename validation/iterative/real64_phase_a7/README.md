# REAL64 Phase-A7 complete-lane ownership and ABI blueprint

## Status

```text
FROZEN-COMPLETE-SUFFIXED-REAL64-OWNERSHIP-ABI-BLUEPRINT
IMPLEMENTATION=NONE
PRODUCTION-SOURCE-CHANGES=0
DEFAULT-RUNTIME-ROUTE=UNCHANGED
FORTRAN-COMPILATIONS=0
OBJECT-LINKS=0
OBJECT-EXECUTIONS=0
TRACKING-READS=0
TRANSPORT-SOLVES=0
DRAGON-RUNS=0
RADIAL-CONVERGENCE=NOT-EVALUATED
OUTER-PICARD-CONVERGENCE=NOT-EVALUATED
```

Phase-A7 turns the already frozen
[`radial_real64_route_protocol.json`](../radial_real64_route_protocol.json)
into one complete implementation blueprint. It adds no numerical method,
physical term, solver parameter, production callsite, or executable code.

The purpose is to prevent one more locally correct but globally incomplete
precision adapter. Phases A1 through A6 establish a checked
source-to-response seam near `MCGFL1`. They do not own the mutable state
before that seam or after it. A continuous REAL64 radial lane must begin at
the eight-slice state in `FLU2DR` and remain REAL64 through the terminal
decision.

The machine-readable authority for this phase is
[`precision_ownership_manifest.json`](precision_ownership_manifest.json).

The freeze avoids a self-hash cycle by normalizing exactly the three
`hash_freeze` artifact fields
`precision_ownership_manifest_sha256`, `readme_sha256`, and
`canonical_json_sha256`. For the normalized formatted-file and canonical
JSON hashes, those three values are restored to the literal
`PLACEHOLDER`; the README and both upstream receipts are hashed directly.
The checker also verifies the parent protocol's 24-source hash map, the
complete A7 path scope against the Phase-A6 commit, and the explicit extra
source hashes.

## Hash-freeze semantics

The manifest avoids self-reference with one exact normalization rule. When
the checker computes the formatted-manifest digest and the canonical-JSON
digest, the three `hash_freeze` artifact fields
`precision_ownership_manifest_sha256`, `readme_sha256`, and
`canonical_json_sha256` are first restored to the literal `PLACEHOLDER`.
No other byte or value is normalized. The live README and both required
upstream receipt files are independently checked by their direct SHA-256
digests. A remaining placeholder fails closed.

The older radial-route receipt is historical evidence frozen at commit
`3162369d66287b3664a16c98cc03481e99d4e421`. Every one of its eight
entries is replayed against that commit. At the live worktree, only its
protocol JSON, checker, mutation tests, and runner remain hash
authorities. The four documentation targets
`radial_real64_route.md`, the root README,
`SPOT_doc/validation_plan.md`, and `validation/iterative/README.md`
have legitimately evolved and are an explicit, closed whitelist; their
historical hashes are not misrepresented as live hashes. The Phase-A6
receipt is still replayed completely against the live worktree.

The separate
[`phase_a7_implementation_receipt.sha256`](phase_a7_implementation_receipt.sha256)
has one exact ordered scope: the two upstream receipts, the two aggregate
READMEs, the top-level Makefile, and the five A7 authority/gate files. It
does not hash itself. The top-level Makefile must equal the Phase-A6
baseline plus only the isolated three-line `spot-real64-phase-a7` target;
that target has no prerequisite and is not part of `all`, `tests`, or
`spot-fast`.

## Two owners, not one

The design deliberately separates mutable state from immutable operator
data.

`FLU2DR64` is the unique mutable-state owner. It owns

```fortran
real(real64), allocatable :: FLUX64(:,:,:)
allocate(FLUX64(NUNKNO,NGRP,8))
```

with the unchanged legacy meanings:

| Slice | Meaning |
| --- | --- |
| 1 | old outer flux |
| 2 | present outer flux |
| 3 | new outer flux |
| 4 | outer source |
| 5 | old inner flux |
| 6 | present inner flux |
| 7 | new inner flux |
| 8 | inner source |

`QFR` and `PHIIN` in the inner solver are borrowed views or exact REAL64
copies of this state. They are not separate state owners. Creating an
owner only at `MCGFL1` would promote values that had already passed through
REAL32 and would return them to REAL32 afterward. That is explicitly
forbidden.

`MCCGF64` separately owns the complete immutable scattering bundle:

```fortran
real(real32), allocatable :: SC_BY_GROUP32(:,:,:)
allocate(SC_BY_GROUP32(0:NBMIX,1,NGEFF))
```

For every `II`, it requires an exact length `NBMIX+1`, type-2
`DRAGON-S0XSC` record and copies it from `KPSYS(II)` into
`SC_BY_GROUP32(:,1,II)` without numerical conversion. The tuple

```text
NGIND(II), KPSYS(II), SC_BY_GROUP32(:,1,II)
```

must describe the same admitted physical group. The bundle remains
read-only and lives for one complete `MCCGF64` call, including the source
and live ACA operations. No downstream routine and no Phase-A6 rendezvous
may gather it again.

This separation is important: REAL32 is the frozen storage kind of the
operator data, while REAL64 is the working kind of the mutable iteration
state. Promoting a frozen REAL32 coefficient when it participates in a
REAL64 expression is allowed. Rounding mutable state back to REAL32 is not.

`FLU2DR64` also owns the distinct frozen off-group source/rebalancing
bundle:

```fortran
integer :: NJJ_OFF(NMAT,NGRP), IJJ_OFF(NMAT,NGRP)
integer :: IPOS_OFF(NMAT,NGRP), NSCAT_OFF(NGRP)
real(real32) :: SCAT_OFF32(NMAT*NGRP,NGRP)
```

Every `NJJS00/IJJS00/IPOS00/SCAT00` record is admitted once with exact
type, extent, index bounds, and finite values. Padding in `SCAT_OFF32` is
defined positive zero and never read. Source construction and `FLUBAL64`
receive the same immutable `OFFGROUP32` bundle through explicit read-only
rectangular dummies; neither may perform a later off-group `LCMGET` or
`LCMGPD`.

## Complete route

The only admissible ON route is

```text
FLU common one-pass FLUGPI parse
  -> independent default-false R64 selector
  -> FLU/FLUDRV guarded default-off dispatch
  -> admitted ON: unchanged XDRTA2 exactly once
  -> ON audit arm: SPOMOC_BEGIN64
  -> FLU2DR64
     -> SPOMOC_FLU_PATH
     -> first eligible door: SPOMOC_FLU_CONTEXT
        -> SPOMOC_DOOR_BEGIN
     -> DOORFV64
        -> MCCGF64
           -> MCGSIG
           -> SPOMOC_MCCGF_BEGIN
           -> MCGFLX64
              -> PRINDM (IPRINT>5 diagnostic only)
              -> MCGMRE64
                 -> SPOMOC_SET_ROLE before each response
                 -> MCGFL164
                    -> MCGFCS64
                    -> MOCIK3
                    -> MCGFCF
                       -> MCGFFIR64_RANK_ADAPTER
                          -> MCGFFIR
                       -> MCGSCA
                    -> MCGFST
                    -> SPOMOC_CAPTURE64
                    -> MCGFCA64
                       -> MCGFCR64
                       -> MCGPRA64
                          -> MSRLUS1
                       -> MCGABG64
                          -> MCGPRA64
                             -> MSRLUS1
                 -> SPOMOC_PUBLISH after the first primary response
     -> FLUBAL64
        -> ALSBD
     -> FLU2AC64
     -> REAL64 inner and outer terminal norms
     -> authoritative GANLIB type-4 FLUX/SOUR
     -> one terminal GANLIB type-2 compatibility mirror
  -> FLUDRV accepted host-metadata writes
  -> FLU deferred LINK.MACRO/LINK.TRACK/LINK.SYSTEM and SPOT-LEAK1D
  -> SPOMOC_FINISH
```

`XDRTA2` initializes the unchanged `/EXP1/` operator table after ON
admission and before the first `MCGSCA` use. It is frozen operator state,
not mutable solver state: omission, duplication, or replacement is
forbidden.

The existing double-vector kernels `MCGFCF`, `MCGFFIR`, `MCGFST`,
`PRINDM`, `MSRLUS1`, and `ALSBD` may be reused only after the selected
A8 toolchain proves `kind(0.0d0)==real64`.
All suffixed interfaces are explicit and checked except one precisely
bounded legacy callback seam inside `MCGFCF`. There,
`MCGFFIR64_RANK_ADAPTER` is a global external subroutine with
explicit-shape dummies and no descriptor ABI. Legacy `MCGFCF` calls it
through its existing implicit `EXTERNAL` seam; the adapter itself calls
`MCGFFIR` through a checked interface. This exception is object- and
call-list-audited and is not described as an explicit procedure
interface.
The ON arm uses a suffixed `MCGPRA64`, not legacy `MCGPRA`, because the
legacy dummy is declared `IM(NLONG)` although its loop reads
`IM(NLONG+1)`. `MCGPRA64` changes that checked extent only and preserves
the matrix-vector, preconditioner, and call order. `MCGSCA` remains the
frozen mixed-precision operator: its
`TAU=REAL(TAUD)` and binary32 exponential-table arithmetic are not
reclassified as mutable state.

The A1–A6 validation modules are evidence and specifications for the
future suffixed implementation. Production code must not acquire a build
dependency on the validation tree.

The locked `KRYL=10` route uses `MCGMRE64` only. Every call from
`MCGMRE64` to `MCGFL164` has `LAST=false`; together with `ISCR=0`, this
fixes `MACFLG=false`, `COMBFLG=false`, and the `MCGFCA64` rebalancing flag
to false. The live ACA path is the existing one-group path:

```text
MCGFCA64
  -> MCGFCR64
  -> MCGPRA64
     -> MSRLUS1
  -> MCGABG64
     -> MCGPRA64
        -> MSRLUS1
```

Richardson, BiCGSTAB, SCR, combined ACA-SCR, `MCGABGR`, `MCGACA`, and
macrolib-scattering ACA branches are outside the first lane.
`LREBAL=true` refers to the separate `FLUBAL64` call after the inner door.

## Exact index ranks

The checked interfaces do not use legacy sequence association to hide
rank changes. The outer `FLU2DR64` array has shape
`KEYFLX(NREG,NLIN,NFUNL)`; after the frozen
`NLIN=NFUNL=1` guard it passes the contiguous rank-1 actual
`KEYFLX(:,1,1)` as `KEYFLX_BASE1(NREG)` to `DOORFV64` and `MCCGF64`.

The tracking index is a different object. `MCCGF64` first requires
`KEYFLX$ANIS` to have exact length `NREG*NLIN*NFUNL` and GANLIB integer
type `ITYLCM=1`, then maps it directly as
`KEYFLX_TRK3(NREG,NLIN,NFUNL)`. That rank-3 view passes unchanged through
`MCGFLX64` and `MCGMRE64` to `MCGFL164`. After checking `NLIN=1` and the
exact shape, `MCGFL164` passes the direct contiguous rank-2 section
`KEYFLX_TRK3(:,1,:)` to `MCGFST` and `MCGFCA64`.

The legacy `MCGFCF` callback needs a different rank normalization.
`MCGFL164` proves `NLF=NLIN=NFUNL=1`, names the fixed global
`MCGFFIR64_RANK_ADAPTER` symbol directly, and does not assign that symbol
to legacy rank-2 `MCGFFI_TEMPLATE`. The adapter has an explicit-shape
callback dummy

```fortran
integer :: KEYFLX_TRK3(NREG,1,1)
```

and passes the direct contiguous rank-2 section
`KEYFLX_TRK3(:,:,1)` to checked legacy `MCGFFIR(NREG,1)`. It forwards
the legacy `SUBSCH` external unchanged, performs no arithmetic, has no
`SAVE`, I/O, module state, assumed-shape dummy, or `BIND(C)`, and is safe
inside the existing OpenMP loop. Direct rank-3-to-rank-2 sequence
association and flat aliases are forbidden.

`PJJIND$MCCG` is narrower. Immediately before the one `MCGFST` call,
`MCGFL164` requires exact length `2*NPJJM` and GANLIB integer type, then
uses `LCMGPD` and `C_F_POINTER(...,[NPJJM,2])` to create the local
read-only `PJJIND_TRK2(NPJJM,2)` view. Only `MCGFST` receives it. It is
not added to the `MCCGF64`, `MCGFLX64`, `MCGMRE64`, or `MCGFCA64`
interfaces, and its descriptor expires on return from the same response
call. Flat rank-1 `KEYFLX`/`PJJIND` mappings and implicit rank adaptation
are forbidden.

The remaining live tracking records are admitted before mapping or
reading:

```text
XMU$MCCG       length NMU,          type 2
WZMU$MCCG      length NMU,          type 2
ZMU$MCCG       length NMU,          type 2
V$MCCG         length NLONG,        type 2
NZON$MCCG      length NLONG,        type 1
KEYCUR$MCCG    length NLONG-NREG,   type 1
BC-REFL+TRAN   length NLONG-NREG,   type 1
PJJ$MCCG       length NREG*NPJJM,   type 2 for each active group
```

Before the `MATALB` payload, the regular header must prove
`NREG_TRACK=NBREG=N2REG=8`, `NSOU=N2SOU=NSOUT=6`,
`NFI=NLONG=K=KPN=NUNKNO=14`, and
`NLONG=NFI=NREG_TRACK+NSOU`. The owner allocates
`MATALB_TRK(-NSOUT:NREG)` and reads its payload in that same lower-to-upper
index order.

The checked `MCGSIG` reuse likewise preflights `IPTRK/ICODE` as
integer length 6, `IPTRK/ALBEDO` as type-2 length 6, every
`DRAGON-TXSC` as type-2 length `NBMIX+1`, and every positive-length group
`ALBEDO` as type 2 with the same `NALBP`; `NALBP=0` requires absence in
every group.

Length and type are followed by the already frozen capture-layout value
guards: `PJJIND_TRK2(1,:)=[1,1]`; scalar and current keys are
duplicate-free and together form a permutation of `1..KPN`;
boundary/zone indices are in range; volumes are finite and positive; and
the admitted scattering, total-cross-section, and albedo payloads are
finite. These are memory-safety and provenance checks, not empirical
thresholds.

## DOORFV64 active-tail ownership

`DOORFV64` borrows the full REAL64 source and flux matrices from
`FLU2DR64`, then owns two contiguous matrices for the admitted tail:

```fortran
real(real64), allocatable :: QFR_TAIL64(:,:), PHIIN_TAIL64(:,:)
allocate(QFR_TAIL64(NUN,NGEFF), PHIIN_TAIL64(NUN,NGEFF))
```

Before copying anything, it checks

```text
NGIND(1)     = NG-NGEFF+1
NGIND(II)    = NG-NGEFF+II
NGIND(NGEFF) = 370
NPSYS(IG)    = 0 before the tail and IG on the tail
KPSYS_TAIL(II) = LCMGIL(IPSYS,NGIND(II))
length(KPSYS(II)/FUNKNO$USS) = 0 for every II
```

The `KPSYS_TAIL` identity follows from `LBIHET=false`; it binds the local
column to the same physical group as `NPSYS` and `NGIND`. Bundle arrays
are always indexed by local `II`; `NGIND(II)` is never used as a local
array subscript.

The final check is required because legacy `DOORFV` can otherwise read a
type-2 `FUNKNO$USS` record into mutable flux on every door visit. The first
locked REAL64 lane does not read that optional payload. A nonzero record
length fails closed before `LCMGET` and cannot fall back to the legacy arm.

The input source tail is never scattered back. The output flux tail is
scattered into `FLU2DR64` storage only after an admitted, structurally
valid, finite normal return. Structural failure, non-finite state, or
abnormal return leaves the parent state unchanged. No REAL32 gather buffer
is permitted.

The same rule covers diagnostic output. For `IMPX>3`, region source and
flux formatting uses `FGAR64(NREG)`, initialized with `+0.0_real64` and
filled from `QFR_TAIL64` or `PHIIN_TAIL64` without conversion. For
`IMPX>4`, full-unknown output reads `PHIIN_TAIL64(:,II)` directly. A
REAL32 `FGAR` capture is forbidden even though printing does not feed back
into the solve.

This scatter rule does not add an inner numerical-convergence test.
Legacy `MCGMRE` reaching `MAXIT` and `MCGABG` reaching `MAXINT` both
return normally, so cap exhaustion by either routine alone does not veto
the REAL64 scatter. Their existing iteration and residual records are
retained where available. Publication is decided later, only by the
unchanged strict `FLU2DR64` terminal rule.

The `KPSYS_TAIL` array storage is owned by `DOORFV64`; its `C_PTR`
pointees remain borrowed and may not outlive the synchronous call.
Within the consecutive `NGIND` tail, `NCONV` may still be any nonempty
non-contiguous active mask.

## Routine precision and lifetime rules

| Owner or borrower | Required mutable REAL64 data | Frozen stored-kind data | Lifetime |
| --- | --- | --- | --- |
| `FLU2DR64` | eight-slice `FLUX64`, source accumulation, `AKEEP64`, all inner/outer terminal scalars | physical cross sections and geometry | complete radial-lane visit |
| `DOORFV64` | owned contiguous `QFR_TAIL64`, `PHIIN_TAIL64` | borrowed group directories and geometry | one door visit |
| `MCCGF64` | `REPS64`, `EPS64` and control-affecting norms | owned read-only `SC_BY_GROUP32`, `SIGAL32`; borrowed tracking | one MCCG visit |
| `MCGFLX64` | REAL64 source/response scratch and locked GMRES dispatch | borrowed SC, SIGAL and geometry | one inner-solver call |
| `MCGMRE64` | `QFR`, `PHIIN`, `RHS`, `GAR`, Krylov vectors, corrections and norms | borrowed SC, SIGAL and geometry | one GMRES call |
| `MCGFL164` | same-call source and post-STIS response | borrowed SC, SIGAL, KPSYS and tracking | one response call |
| `MCGFCS64` | REAL64 `QN`, `FI`, and inout source `S`; untouched elements preserve bits | borrowed REAL32 SC and SIGAL | one active-group source construction |
| `ACA64` | old state, response, REAL64 residual/right-hand-side/correction workspace and decision scalars | frozen REAL32 ACA matrices and records promoted when used | one ACA call |
| `FLUBAL64` | rebalancing matrix, right-hand side, solution, balance accumulators and flux update | frozen physical inputs | one rebalance call |
| `FLU2AC64` | flux history differences, dot products, `DMU` and accelerated state | unchanged acceleration schedule | one acceleration call |

`DOORFV64`, `MCCGF64`, and `MCGFLX64` replace the legacy REAL32
`SUNKNO/FUNKNO/FIMEM/QFR` interfaces with checked REAL64 interfaces.
`MCCGF64` also owns REAL64 `REPS/EPS` and passes the exact promotion of
the frozen binary32 `EPSI` value through the checked `MCGFLX64` interface.
Its convergence warning and printing use
`TEMP64=EPS64(II)`, compare `TEMP64>EPSI64`, and print `TEMP64` directly;
an implicit default-REAL `TEMP` may not capture the REAL64 norm.
For `IPRINT>5`, `MCGFLX64` likewise calls the existing double-precision
`PRINDM` directly on each REAL64 `PHIIN_TAIL64/FIMEM` group view. The ON
arm never calls REAL32 `PRINAM` for mutable state and never constructs a
REAL32 print adapter.
`MCGMRE64` then computes
`EPSINTO64=ERRTOL64/100.0_real64`; that value passes unchanged as
`MCGFL164` `EPSACC64`, `MCGFCA64` `EPSACA64`, and `MCGABG64` `EPSM64`.
It is never first rounded to a binary32 `EPSINTO`.
`MCGMRE64` must remove the current mutable-state downcasts represented by
`REAL(FLOUT)`, `REAL(V)` and REAL32 `RHS/GAR/PHIIN` updates.
`MCGFCS64` uses REAL64 `QN/FI`; `MCGFCA64/MCGFCR64` use REAL64
`PHIIN/FIOLD` and response. The locked `MACFLG=false` branch does not
consume `XSCAT`. `MCGFCA64` keeps `FLXN` in REAL64 and passes it
unchanged as `MCGABG64` `FAC`; `MCGABG64` uses REAL64 `EPSM/FAC` and
control arithmetic.

`MCGFLX64` initializes its whole `SOURCE64` matrix once to
`+0.0_real64` immediately after allocation and before any `MCGFCS64`
call. At the start of every `MCGFL164` response call it initializes the
whole `RESPONSE64` view to `+0.0_real64` before `MCGFCF` or `MCGFST`.
Inactive groups and unrepresented entries therefore retain a defined
positive-zero bit pattern instead of undefined storage.

For the locked regular 2D branch, `MCCGF64` preserves the exact stored
`CPO32(NMU)` values from `XMU$MCCG` even though the isotropic
`MCGFCF` branch does not read that formal. `MCGFL164` supplies defined
conforming `CAZ0_INACTIVE64(NANGL)=+0.0_real64` and
`XSI_INACTIVE64(NSOUT)=+0.0_real64`. `CAZ0` is unread for `NDIM=2`;
`MCGFFIR` reads `XSI` only for `IDIR>0`. The valid rank-1
`XSI_INACTIVE64` actual replaces the legacy illegal `XSIXYZ(:,0)`
expression without adding a physical coefficient.

At the existing post-`MCGFST`, pre-ACA audit point, the ON arm calls
`SPOMOC_CAPTURE64`, not legacy `SPOMOC_CAPTURE`. Its four rank-2 inputs
`QFR_TAIL64`, `PHIIN_TAIL64`, `SOURCE64`, and `RESPONSE64` are all
REAL64. It preserves the existing `SPOMOC_ACTIVE`, context, role,
iteration, group, `NCONV`, and finite checks, then writes
`SPOT-M-QFR/EVAL/SRC/RAW` directly as GANLIB type 4. There is no REAL32
QFR/EVAL staging and no re-promotion. These are validation-audit records,
not the terminal `SPOT-R64` authority or the type-2 compatibility mirror,
and the capture cannot change solver state or a convergence decision.
The legacy OFF arm continues to call the existing `SPOMOC_CAPTURE`.

The ON audit lifecycle is fixed and diagnostic-only:

1. `FLUDRV` calls `SPOMOC_BEGIN64` before REAL64 state mutation or
   tracking consumption.
2. `FLU2DR64` calls `SPOMOC_FLU_PATH`; on the first eligible
   `IT=JT=1` door visit it calls `SPOMOC_FLU_CONTEXT`, then
   `SPOMOC_DOOR_BEGIN`.
3. `MCCGF64` calls `SPOMOC_MCCGF_BEGIN` before `MCGFLX64`.
4. `MCGMRE64` calls `SPOMOC_SET_ROLE` before every response,
   `MCGFL164` calls `SPOMOC_CAPTURE64` at the post-STIS/pre-ACA point,
   and `MCGMRE64` calls `SPOMOC_PUBLISH` after the first primary return.
5. `FLUDRV` calls `SPOMOC_FINISH` after the selected route returns.

`SPOMOC_BEGIN64` admits the actual frozen controls
`MAXOUT=500`, `MAXINR=740`, `INITFL=1`, and `ACCE=(3,3)`; it does not
replace those values. Missing, duplicate, or reordered hooks fail the
audit without changing solver state, a terminal decision, or
publication.

The checked locked `MCGFCR64` interface is branch-specific: because the
`MACFLG=false` macrolib cross-group branch is disabled, it omits inactive
`NJJ/IJJ/IPOS/XSCAT` arguments.
The legacy practice of passing unallocated allocatables that happen not
to be read is not valid for the new explicit interface.

On the active `PACA=4` path, every live record is checked with `LCMLEN`
for exact length and GANLIB type before `LCMGPD` and `C_F_POINTER`:

| Record | Stored view |
| --- | --- |
| `IM$MCCG` | integer `IM(N1+1)` |
| `MCU$MCCG` | integer `MCU(LC)` |
| `PI$MCCG` | integer `IPERM(N1)` |
| `JU$MCCG` | integer `JU(N1)` |
| `DIAGQ$MCCG` | REAL32 `DIAGQ32(N1)` |
| `CQ$MCCG` | REAL32 `CQ32(LC)` |
| `ILUDF$MCCG` | REAL32 `ILUDF32(N1)` |
| `CF$MCCG` | REAL32 `CF32(LC)` |
| `DIAGF$MCCG` | REAL32 `DIAGF32(N1)` |

`IM0$MCCG`, `MCU0$MCCG`, and `ILUCF$MCCG` are inactive and may not be
mapped. In particular, `CF$MCCG` is not an `N1` vector. Before mapping it,
the owner requires

```text
LCMLEN(CF$MCCG) = LC
GANLIB record type = 2
```

and only then applies `LCMGPD` and `C_F_POINTER(...,[LC])` to obtain the
read-only `CF32(LC)` view used by `MCGPRA64`, `MCGABG64`, and
`MSRLUS1`. Mapping it with `[N1]`, as one legacy branch currently does,
is forbidden.

Likewise, the checked `MCGPRA64` dummy is
`IM(NLONG+1)`, matching the producer and `MSRLUS1`. The legacy declaration
`IM(NLONG)` is not wrapped behind an explicit interface because its loop
evaluates `IM(I+1)` through `I=NLONG`. This is a shape correction, not a
new solver: operator arrays remain REAL32, mutable vectors remain REAL64,
and every arithmetic expression and iteration order is unchanged.

The locked `PACA=4` route also replaces legacy one-element dummy actuals
with conforming defined storage:

```fortran
real(real32), allocatable :: LUCF_INACTIVE32(:)
real(real32), allocatable :: DIAGF_INACTIVE32(:)
allocate(LUCF_INACTIVE32(LC), DIAGF_INACTIVE32(N1))
LUCF_INACTIVE32 = +0.0_real32
DIAGF_INACTIVE32 = +0.0_real32
```

`LUCF_INACTIVE32` supplies the inactive ILUCF formal to the direct
pre-`MCGABG64` `MCGPRA64` call and to `MCGABG64`.
`DIAGF_INACTIVE32` is used only by that direct pre-`MCGABG64`
`MCGPRA64` call. `MCGABG64` and all `MCGPRA64` calls inside it receive
the active `DIAGF32(N1)` record. These arrays are not physical
coefficients and do not enter the operator.

The assumed-size inactive integer formals are a separate case. With
`LC0=0`, local defined `IM0_INACTIVE(1)` and `MCU0_INACTIVE(1)` are
conforming; no inactive record is mapped and no legacy `SAVE IDUMMY` is
used. This does not weaken the rule that explicit-shape REAL formals need
their full `LC` or `N1` storage.

The cutoff counterfactual has one explicit hierarchical owner. At entry,
`FLU2DR64` initializes

```fortran
integer(int64) :: CUTOFF_ACTIVE_VISIT64
CUTOFF_ACTIVE_VISIT64 = 0_int64
```

Each `MCGABG64` call returns a fresh nonnegative `integer(int64)` delta,
incremented by exactly one for every evaluated live guard whose production
and `EPSMAX=0` Boolean results differ. Each caller sums every normally
returned child delta exactly once in existing call order:

```text
MCGABG64 -> MCGFCA64 -> MCGFL164 -> MCGMRE64
          -> MCGFLX64 -> MCCGF64 -> DOORFV64 -> FLU2DR64
```

No lower routine resets or overwrites an ancestor total, and no `SAVE`,
`COMMON`, module singleton, or shared mutable leaf counter is permitted.
The visit total is diagnostic only and cannot change a live branch,
terminal decision, or publication. Under the frozen caps, the conservative
count bound is `555814000000`, safely within `integer(int64)`.

`FLUBAL64` must not downcast `XCSOU` or solve a REAL32 balance system.
Its checked call uses only direct sections:
`KEYFLX(:,1,1)`, `MATALB(NNN+1:NNN+ICREB)`,
`V(NNN+1:NNN+ICREB)`, and `FLUX64(:,:,7)`.
`FLU2AC64` must not apply `REAL(DMU)` to a REAL32 flux array. Its inner
call receives `FLUX64(:,:,5:7)` with `AKEEP64(5:7)`; its outer call
receives `FLUX64(:,:,1:3)` with `AKEEP64(1:3)`. Element-actual sequence
association is forbidden at both outer boundaries.

All state, norm, acceleration and stopping arithmetic stays REAL64.
Immutable `SC`, `SIGAL`, volume, and quadrature inputs retain the frozen
kind declared in the manifest.

Existing REAL32 tolerances such as `EPSINR`, `EPSUNK`, `EPSOUT`, and
MCCG `EPSI` keep exactly their configured binary32 values and are promoted
to REAL64 for comparisons. Existing caps, schedules, `ERRTOL/100`, and the
ACA cutoff are unchanged; none is fitted or tuned.

No solver-state owner, operator owner, routine scratch object, or cutoff
counter may use `SAVE`, `COMMON`, or module-level mutable singleton
storage. The pre-existing `SPOMOC_AUDIT` module lifecycle is the one
narrow diagnostic exception: its flags, integer state vector, and
borrowed GANLIB handles may persist solely to order audit hooks. It stores
no solver REAL state or operator array and cannot feed a solver branch,
terminal decision, or authoritative/compatibility publication. Borrowed
file units, C addresses, LCM pointees, and array views otherwise do not
escape the synchronous call that admitted them.

`MCGFCS64` has two mutually exclusive formulas. For a represented volume
unknown it receives the rank-2 slice `SC_BY_GROUP32(:,:,II)` and evaluates

```text
S = QN + promoted(SC) * FI
```

in REAL64. For a represented boundary-current unknown it evaluates

```text
S = promoted(SIGAL) * FI
```

in REAL64. It never adds these into a three-term expression. `QN`, `FI`,
and `S` are REAL64; `SC` and `SIGAL` remain read-only REAL32 operator
inputs and are exactly promoted only where their respective branch uses
them.

## Host ingress and staged return

`R64` is the sole numerical-route selector. It defaults false, is local to
one `FLU` call, and is orthogonal to `MOCA`: `MOCA` can enable audit
diagnostics but can never enable the REAL64 solver. A common, read-only,
one-pass `FLUGPI` parse returns all existing controls plus `R64`; the input
stream is never parsed twice.

The admitted topology has exactly six entries:

```text
1 existing modifiable L_FLUX
2 read-only direct L_MACROLIB MACRO0
3 read-only L_TRACK TRACK
4 one read-only sequential-binary TRACK_f unit
5 read-only L_PIJ SYSTEM
6 read-only L_SOURCE FSOURCE
```

There is no `IPFLUP`, no library descent, and no additional entry. Before
any payload read, the five LCM objects require `SIGNATURE` length 3,
GANLIB type 3, and exact values `L_FLUX`, `L_MACROLIB`, `L_TRACK`,
`L_PIJ`, and `L_SOURCE`. The frozen state, tracking, source, and
cross-section records then prove `ITPIJ=1`, `ITRANC=2`, `INSB=1`,
`LEAKSW=false`, `NGRP=370`, `NMAT=8`, `NIFIS=32`, `NREG=8`,
`NUNKNO=14`, `IPHASE=1`, and inactive `ISPOD=0`, plus all remaining
locked dimensions and controls before a source or operator payload is
consumed.

The two optional initial-flux records `B2  HETE` and `B2  B1HOM` are
absent. `IPTRK/TITLE` has exact length 18, type 3, and the 72-character
blank-padded value `SAL TRACKING`; it is admitted diagnostic text, not a
solver input.

`FLU` owns conforming `KEYFLX_HOST3(NREG,NLIN,NFUNL)` storage. Its
`KEYFLX_BASE1` view is the same admitted value sequence as
`KEYFLX_TRK3(:,1,1)`; no rank-1-to-rank-3 sequence association is used.
For every region, `MATCOD=NZON$MCCG=MATALB_TRK` is in `1..NMAT`, while
`VOLUME` is finite, positive, and bitwise identical to `V$MCCG`.
The required finite `IPSYS/SPOT-LEAK1D` record is staged once in
read-only `LEAK1D_INPUT32(NGRP)` and never enters the solver.

Return status is deliberately layered. `FLU2DR64` returns `CHILD_OK` only
after strict acceptance and complete type-4/type-2 publication.
`FLUDRV` starts with `DRIVER_OK=false`, writes its host metadata only
after `CHILD_OK`, and returns true only after those writes finish. `FLU`
starts with `HOST_OK=false`, then writes deferred
`LINK.MACRO/LINK.TRACK/LINK.SYSTEM` and `SPOT-LEAK1D` only after
`DRIVER_OK`; only then can the outer call succeed. This is implementable
staged gating, not a claim of rollback or crash-atomic publication after
accepted writes begin.

## One entry promotion, exact frozen source, and one terminal mirror

After ON admission, `FLU2DR64` performs one entry-promotion event. The
existing `FLUX` container has exact length `NGRP`, type 10; every group
element has length `NUNKNO`, type 2, and finite values. Each group is read
into `REAL32(NUNKNO)` staging and promoted elementwise once into
`FLUX64(:,IG,2)`.

`FSOURCE` is mandatory and is the sole admitted source. Its state vector
is exactly `(370,14,1,0,...,0)`; `SPOT-FROZEN=1`; its positive finite
`SPOT-KEFF` is bitwise identical to `MACRO0/SPOT-KEFF`; `NBS` is absent.
`NORM-FS` is also absent, so the legacy terminal `NORM-FS` and `MATCOD`
writes are dead on this route.
`DSOUR` is a type-10 outer list of length 1 containing a type-10 inner
list of length 370, whose group records are length 14, type 2, finite,
and nonnegative. `SPOT-QINT` is finite provenance only and is never
substituted for the direct source integral.

Every `MACRO0/GROUP/NUSIGF` record has exact length `NMAT*NIFIS`, type 2,
and finite numerical-zero values. The ON arm therefore lexically omits the
fission loop and does not read `CHI`; it never relies on `CHI*0`.
The branch-specific `FLU2DR64` interface omits dead `XSCHI/XSNUF`
formals: `FLUDRV` validates `NUSIGF` through per-group REAL32 staging,
does not allocate or read `CHI`, and passes neither array.
`FIXED_SOURCE64(NUNKNO,NGRP)` is populated once from `DSOUR`. The direct,
unchanged-order `XCSOU64(1)` sum must be strictly positive exactly—without
a threshold—which establishes the initial `IGDEB=1`, `NGEFF=370` tail.

Every outer iteration copies `FIXED_SOURCE64` into `FLUX64(:,:,4)`.
Every inner iteration copies slices 6 to 7 and 4 to 8, skips the
`ITPIJ=2/4` self-scattering addition, skips leakage source construction,
then adds only `JG!=IG` off-group terms from the admitted `OFFGROUP32`
bundle before `DOORFV64`. There is no no-`IPSOU` `FIXE` branch and no
later source or off-group LCM read.

Terminal printing is not another compatibility conversion. `IPRT>=3/4`
uses `FL_PRINT64(NREG)` or a direct REAL64 indexed view, and the
`ITYPEC=0` lane omits the dead `RKEFF=REAL(AKEFF)` assignment.
`DOORFV64` also requires every `FUNKNO$USS` record to be absent, so no
later REAL32 mutable-state ingress exists.

Only the unchanged strict Boolean

```text
EEXT < EPSOUT
and EINN < EPSUNK
and EINR_LAST < EPSINR
and IINR_STATE = 1
and IT >= 2
```

first authorizes a publication preflight, not a write. Before any
accepted-block creation or mutation, every selected REAL64
`FLUX64`/source value must be IEEE finite, and every value intended for
the compatibility mirror must lie within the finite REAL32 range:
`abs(x)<=real(huge(0.0_real32),real64)`. This is a machine-representation
limit, not an empirical parameter or a convergence threshold. Failure
stops the selected ON visit before all accepted writes.

Only after that preflight does the accepted block write the authoritative
GANLIB type-4
`SPOT-R64/FLUX` and `SPOT-R64/SOUR`, then exactly one write-only REAL32
adapter pass for legacy type-2 `FLUX/SOUR`, then the layered host writes
described above. Static checks reject preterminal `LCMLID`, `LCMDID`,
`LCMPUT`, `LCMPPD`, or `LCMPTC` targeting any of those records.
`SPOT-MOC-AUD` is the sole preterminal no-feedback diagnostic exception.

The type-2 mirror cannot affect acceptance and is never read back. A
structurally failed, invalid, non-finite, abnormal, or cap-exhausted visit
without the strict terminal Boolean publishes no accepted output. An
`MCGMRE` or `MCGABG` cap by itself is not a new rejection rule.

## Default OFF and fail closed

The legacy route remains the default and is unchanged:

```text
OFF -> existing FLU/FLUDRV/FLU2DR route only
```

The ON route is selected before legacy initial-`FLUX` creation, REAL64
state mutation, tracking consumption, or any authoritative,
compatibility, or host-metadata mutation. Once selected, every later
admission failure stops that visit. It may not fall back to the legacy
route. One visit can execute only one arm.

This preserves the Phase-A6 rule that a response uses exactly one tracking
traversal and exactly one STIS application. It also extends failure
gating to the scientific, compatibility, and host boundary: no listed
record changes before strict terminal acceptance. Once accepted writes
begin, A7 does not claim rollback or crash atomicity. `SPOT-MOC-AUD`
remains the sole explicitly incomplete diagnostic exception.

A9 must also prove with short synthetic tests that omitting `R64` leaves
the legacy arm's scientific output, public records, and call counts
byte-identical and adds no scientific log record.

## Frozen branch

The first lane remains limited to:

```text
TYPE S + MCCG
R64 explicitly present; otherwise legacy OFF
ITYPEC=0
IPHASE=1
ITPIJ=1, ITRANC=2, INSB=1, LEAKSW=false
2D regular non-cyclic direct-vector route
370 groups, 8 mixtures, 32 fissile spectra
8 regions, 14 unknowns per group
NANI=NLIN=NFUNL=1
ILEAK=0, IDIR=0
STIS=1, NPJJM=1, ISCH=11
KRYL=10, IAAC=80, ISCR=0, IDIFC=0, PACA=4
LPRISM=false, double heterogeneity=false
LREBAL=true
INITFL=1, MAXOUT=500, MAXINR=740, ACCE=(3,3)
IPSOU=FSOURCE required, IPFLUP absent
source=DSOUR with zero NUSIGF; NBS absent
h/2 solver tolerance bits=0x348637bd
LEXAC=false, LEXF=false, HDD_positive=false
MCGMRE MAXI=20, MAXIT=19, NSTART=10
MCGMRE ERRTOL=EPSI bits=0x3727c5ac
```

`MAXINR=740` is the FLU thermal-iteration cap; it is not the MCGMRE cap.

Any mismatch fails closed. The lane does not generalize to cyclic,
anisotropic, leakage, prism, SCR, BiCGSTAB, double-heterogeneity, or
another door.

The inherited `MCGABG` `EPSMAX=1E-7` value is unchanged. REAL64 control
arithmetic uses the exact promotion of its binary32 value
`0x33d6bf95`, namely `1.0000000116860974e-7` in REAL64. The already
frozen `EPSMAX=0` Boolean counterfactual is
diagnostic only: it never changes the live terminal decision, production
state, or publication boundary. If a counterfactual Boolean differs, the
later feasibility result is `INCONCLUSIVE-INHERITED-CUTOFF` and later
Stage-4 work is blocked; the accepted production output is not suppressed
and the cutoff is not tuned.

The diagnostic covers exactly four live `MCGABG` guards:
`RHSN<EPSINF`, `CN>EPSMAX*ASIN2`, and the two occurrences of
`FNORM<EPS2`. The `EPSM` convergence comparison is not a cutoff
counterfactual. Each comparison is counted only; it never chooses the live
branch.

No relaxation, damping, Aitken or Anderson mixing, fitting, clipping,
flux floor, new threshold, changed POD rank, or new physical source is
introduced.

## A8 and A9

Phase-A8 is the inner compile-only closure:

```text
DOORFV64 tail
  -> MCCGF64 SC/SIGAL owner
     -> MCGSIG
     -> MCGFLX64
        -> PRINDM
        -> MCGMRE64
           -> MCGFL164
              -> MCGFCS64
              -> MOCIK3
              -> MCGFCF
                 -> MCGFFIR64_RANK_ADAPTER
                    -> MCGFFIR
                 -> MCGSCA
              -> MCGFST
              -> SPOMOC_CAPTURE64 checked interface
              -> MCGFCA64
                 -> MCGFCR64
                 -> MCGPRA64 -> MSRLUS1
                 -> MCGABG64 -> MCGPRA64 -> MSRLUS1
```

It may use validation-owned REAL64 tail matrices and short synthetic
operators. It compiles every suffixed checked interface plus the one
object-audited legacy implicit `EXTERNAL` bridge. It rejects a
descriptor-based adapter, assignment to rank-2 `MCGFFI_TEMPLATE`,
rank-3/flat `KEYFLX` passage to `MCGFFIR`, and invalid
`XSIXYZ(:,0)` storage. It proves `kind(0.0d0)==real64`, exact tracking
header dimensions, all live tracking/MCGSIG/BC/PJJ record contracts, and
the frozen discrete-layout values.

A8 also proves that SC is gathered once by `MCCGF64`, requires
`FUNKNO$USS` to be absent, and requires direct rank-2
`KEYFLX_TRK3(:,1,:)` and `KEYFLX_TRK3(:,:,1)` sections. It validates all
nine active `PACA=4` records, distinguishes active `DIAGF32(N1)` from
`DIAGF_INACTIVE32`, and uses local `IM0_INACTIVE(1)` and
`MCU0_INACTIVE(1)` with `LC0=0`. It compiles `MCGPRA64` with
`IM(NLONG+1)`, rejects REAL32 `FGAR/TEMP` captures, requires `PRINDM`,
compiles the four-REAL64-array `SPOMOC_CAPTURE64` interface, propagates
exact cutoff deltas, and preserves arbitrary `NCONV` masks. It performs
no tracking read or transport execution.

Even after passing, A8 is not a continuous REAL64 radial lane because it
does not yet own `FLU2DR` state, rebalancing, FLU acceleration, terminal
norms, or archive output.

Phase-A9 adds the outer owner and completes the static lane:

```text
one-pass parse and independent default-off R64 dispatch
  -> unchanged XDRTA2 exactly once
  -> SPOMOC_BEGIN64 audit admission
  -> FLU2DR64 eight-slice owner, frozen DSOUR, and OFFGROUP32
  -> A8 inner route
  -> production SPOMOC_BEGIN64/SPOMOC_CAPTURE64 audit implementation
  -> FLUBAL64 with the same read-only OFFGROUP32 bundle
  -> FLU2AC64
  -> REAL64 terminal decision
  -> type-4 authority
  -> one type-2 mirror
  -> layered CHILD_OK/DRIVER_OK/HOST_OK writes
```

A9 also initializes the single `CUTOFF_ACTIVE_VISIT64` owner and adds
every normally returned `DOORFV64` delta exactly once. It does not use the
counter to change the frozen terminal rule. Every normal ON return emits
exactly one stable ASCII line
`SPOR64 CUTOFF-ACTIVE-VISIT64=<decimal-int64>` after the terminal
decision, without int32 narrowing; OFF emits none. Its compile gate rejects
a REAL32 `FL` diagnostic buffer and any locked-route
`RKEFF=REAL(AKEFF)` downcast. It locks the direct `FLUBAL64` and
`FLU2AC64` sections, the host ingress/explicit-success contract, and the
accepted-block-only `SPOT-R64` and type-2 publication calls.

Only a complete A9 static gate may claim
`COMPLETE-STATIC-REAL64-RADIAL-LANE-CLOSURE`. That label remains
implementation evidence only.

## What A7 proves and does not prove

A7 can freeze:

- the complete required call graph;
- the unique mutable-state and immutable-SC owners;
- every required kind, rank, lifetime and conversion boundary;
- default-OFF, no-fallback, pre-acceptance write gating, and honest
  post-acceptance failure scope;
- the exact A8/A9 boundary;
- absence of a new model term or empirical parameter from the design.

A7 cannot prove:

- live `IFTRAK`, `IPTRK`, `KPSYS`, `PJJ`, SC, geometry, material, or
  group-order identity;
- `/EXP1/` initialization in a real process;
- that any future suffixed routine compiles or executes;
- a real MOC response or `cutoff_active=0`;
- radial convergence, physical accuracy, Stage-4 qualification, or
  outer Picard convergence.

After A9, a separately authorized runtime provenance preflight must come
before any transport application. Only after that may the already frozen
bounded plane-1 feasibility capture and replay be considered. No long
calculation is authorized by Phase-A7.
