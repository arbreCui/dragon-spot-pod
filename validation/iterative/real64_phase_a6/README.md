# REAL64 Phase-A6 compile-only host-rendezvous readiness

## Status

```text
FROZEN-HOST-RENDEZVOUS-CONTRACT
IMPLEMENTED-COMPILE-ONLY-HOST-RENDEZVOUS-READINESS
PRODUCTION-ADMISSION=BLOCKED
DEFAULT-RUNTIME-ROUTE=UNCHANGED
REAL-RUNTIME-PROVENANCE=UNBOUND
PRODUCTION-QFR-PHIIN-REAL64=FALSE
COMPLETE-ORDERED-SC-BUNDLE-AVAILABLE=FALSE
HOST-RENDEZVOUS-EXECUTIONS=0
TRACKING-READS=0
TRANSPORT-SOLVES=0
DRAGON-RUNS=0
OUTER-CONVERGENCE=NOT-EVALUATED
```

This is Phase-A6 of the REAL64 implementation route. It freezes and
compile-checks the only admissible future rendezvous between the real
`MCGFL1` host and the validation-only Phase-A5 path. It does not connect
that path to production and it does not authorize a runtime preflight,
tracking read, transport application, Dragon process, or Picard
trajectory.

“Implemented” here means that the validation tree contains the typed,
fail-closed rendezvous-readiness contract. It does **not** mean that the
production admission conditions have been met.

## The only future seam

For the locked regular, non-cyclic 2D branch, the only future insertion
point is inside `MCGFL1`:

```text
form the group sources
  -> generate ISGNR with MOCIK3
  -> [one mutually exclusive default-off rendezvous]
       OFF: execute the existing MCGFCF then MCGFST response region
       ON and admitted: execute the A5 path, which already covers both
  -> rejoin only after the existing MCGFST response region
  -> continue with the unchanged post-response/acceleration path
```

The rendezvous must be after both source construction and `MOCIK3`, and
immediately before the existing regular non-cyclic `MCGFCF` call. The ON
and OFF response regions are alternatives, never consecutive operations.
The A5 path already contains the ordered `MCGFCF -> MCGFST` response, so
an admitted ON visit must skip both the host's existing `MCGFCF` and its
later `MCGFST`, and rejoin only after that response region. This is
essential because one `MCGFCF` traversal consumes the complete `NBTR`
tracking stream; running both arms would consume the stream twice, and
running the host `MCGFST` after A5 would apply STIS twice. Neither would
be a valid comparison or iteration.

The default is OFF, so an unmodified caller remains on the legacy arm.
Once a future caller explicitly selects the ON arm, `route_selected`
becomes true before any further admission check. Any later failure must
stop that selected visit; it may not fall back to the legacy arm, because
the caller must never risk a second response traversal. An inadmissible
state must not be repaired by conversion, copying, gathering, an LCM read,
or a guessed value. Phase-A6 itself remains under `validation/` and is not
included by the production `src/*.f` build.

## Why production admission is blocked

Two upstream facts prevent a truthful production call today.

First, the current `MCGFL1` interface declares both mutable iteration
inputs as default `REAL`:

```fortran
REAL QFR(KPN,NGEFF), PHIIN(KPN,NGEFF)
```

Phase-A5 requires the corresponding `QN` and `FI` matrices to be REAL64.
A conversion at the rendezvous would only promote values that had already
been rounded to REAL32 and would return the next iteration to REAL32. It
would not establish the continuous REAL64 mutable-state lane that this
route is intended to test. Such a conversion is therefore forbidden.

Second, `MCGFL1` does not own a complete scattering bundle. For each
active group it obtains one borrowed `DRAGON-S0XSC` pointer from the
corresponding `KPSYS` directory and passes that one-group view directly to
legacy `MCGFCS`. No persistent, ordered
`SC(0:M,1,NGEFF)` bundle exists at the future rendezvous. Gathering that
bundle inside Phase-A6 would add LCM access and a second data assembly
route whose identity and lifetime have not been proved. It is therefore
also forbidden.

These are admission blockers, not numerical failures and not convergence
observations.

## Direct host map

The frozen map below records the only direct production symbols that may
eventually feed the Phase-A5 interface. “Direct” means the same host
entity or a conforming view of it, with no change of kind and no
reconstruction.

| Phase-A5 field | Future `MCGFL1` host source | Current readiness |
| --- | --- | --- |
| `n` | `NLONG` | statically mapped |
| `ndim` | `NDIM` | statically mapped |
| `nzon` | `NZON` | borrowed conforming host view |
| `qn` | `QFR` | **blocked:** host object is REAL32 |
| `fi` | `PHIIN` | **blocked:** host object is REAL32 |
| `m` | `M` | statically mapped |
| `nani`, `nlin`, `nfunl` | `NANI`, `NLIN`, `NFUNL` | statically mapped |
| `sc` | complete ordered `DRAGON-S0XSC` bundle | **blocked:** only one borrowed group pointer exists at a time |
| `source` | `S` | direct REAL64 host matrix |
| `raw_response` | `PHIOUT` | direct REAL64 host matrix |
| `kpn`, `nreg` | `KPN`, `NREG` | statically mapped |
| `keyflx`, `keycur` | `KEYFLX`, `KEYCUR` | borrowed conforming host views |
| `ibc` | `IBC` associated from `BC-REFL+TRAN` | borrowed conforming host view |
| `sigal` | `SIGAL` | direct REAL32 operator data |
| `stis`, `cyclic`, `lprism`, `idir` | like-named host controls | direct, guarded |
| `ng`, `ngeff`, `ngind`, `nconv` | like-named host group state | direct, guarded |
| `iftrak` | `IFTRAK` | borrowed sequential-unit number |
| `nbtr` | tracking-header local `NBTR` | direct after header read |
| `n2max` | `N2MAX` | direct for `LPRISM=.FALSE.` |
| `nbatch` | `NBATCH` | statically mapped |
| `kpsys` | `KPSYS` | borrowed `TYPE(C_PTR)` handle array |
| `caz1`, `caz2` | `CAZ1`, `CAZ2` | direct REAL64 host arrays |
| `zmu`, `wzmu` | `ZMU`, `WZMU` | borrowed REAL32 tracking views |
| `volume` | `V` | borrowed REAL32 tracking view |

The A5-private canonical storage for `CAZ0`, `CPO`, and `XSI`, and the
exact order-zero identities for `ISGNR` and `PJJIND`, remain governed by
the Phase-A5 contract. Phase-A6 neither promotes those definitions to
runtime-provenance evidence nor introduces alternative values.

## Frozen branch and guards

The future rendezvous is admissible only for the already frozen branch:

```text
ISCH=11
NDIM=2
CYCLIC=FALSE
LPRISM=FALSE
STIS=1
NPJJM=1
K=KPN=NLONG=14
NREG=8
NSOUT=6
NG=370
NANI=NLIN=NFUNL=1
IDIR=0
```

`ISCH=11` identifies the non-cyclic source-term-isolation,
step-characteristics route with tabulated exponentials. `NPJJM=1` is the
exact isotropic PJJ mode count; it is not a fitted rank or a numerical
parameter.

For every gathered call, `NGIND` must be the strictly consecutive tail
ending at group 370:

```text
NGIND(1) = NG-NGEFF+1
NGIND(i) = NGIND(i-1)+1
NGIND(NGEFF) = NG
```

The initial call may contain all 370 groups. Later direct-vector gathers
may contain a shorter consecutive tail. Within that tail, `NCONV` may be
any nonempty, non-contiguous active mask. Phase-A6 must not force
`NGEFF=370` after the upstream gather has advanced.

All guards are exact structural predicates. No tolerance, relaxation
factor, fitted cutoff, interpolation, clipping rule, or empirical
coefficient is introduced.

## Static lifetime facts

The selected location makes the following source-order facts available:

- `MCGFL1` has already rewound `IFTRAK`, read its headers and comments,
  and left the sequential stream immediately before the track records;
- `NBTR` and the non-prismatic `NMAX=N2MAX` value have already been
  established;
- `IBC`, `NZON`, `KEYFLX`, `KEYCUR`, `SIGAL`, `KPSYS`, angular arrays,
  quadrature arrays, and `V` are visible for the synchronous host call;
- `S` and `PHIOUT` are REAL64 host matrices whose storage remains live
  throughout that call;
- `ISGNR` has been allocated and filled by `MOCIK3`, and remains allocated
  until the existing end-of-`MCGFL1` deallocation;
- the A5 context is local to one synchronous call and does not retain the
  borrowed sequential unit, C addresses, or host views after return.

These are lexical and Fortran-scope facts only. They do not prove that a
file unit is open on the expected file, that its physical record position
matches the source text, that an LCM pointee remains alive, or that
separately borrowed objects describe the same physical state.

The current one-group `XSSC` association ends conceptually with each
active-group source calculation. Reusing its last pointer as if it were a
full-group `SC` bundle is forbidden.

## What Phase-A6 does not prove

All runtime-provenance claims remain false. In particular, Phase-A6 does
not establish:

- the open identity or actual first-track position of `IFTRAK`;
- the identity, contents, ordering, or lifetime of `KPSYS` pointees and
  their `PJJ$MCCG` records;
- common geometry, material, group-order, and epoch identity across
  `IFTRAK`, `IPTRK`, `KPSYS`, `NZON`, `SIGAL`, `SC`, and `V`;
- initialization of the hidden `/EXP1/` exponential table in the same
  process image;
- a continuous REAL64 `QFR/PHIIN` state before or after the rendezvous;
- availability or provenance of the required complete ordered SC bundle;
- execution of A5, A4, A3, `MCGFCF`, `MCGFST`, or any transport operator;
- a physical MOC response, numerical accuracy, radial convergence,
  outer/Picard convergence, or a qualified SPOD map;
- safety of removing the deliberate Phase-A3 unresolved link barrier;
- readiness of ACA, SCR, GMRES/BiCGSTAB, rebalancing, acceleration,
  terminal norms, or the final type-4/type-2 archive boundary.

A successful object compilation proves only that the frozen rendezvous
shape and its fail-closed admission logic remain type-correct.

## Short compile-only gate

The isolated Phase-A6 gate is intended to:

- verify its scoped receipt, canonical manifest, checker, and mutations;
- recheck the frozen Phase-A5 receipt and the unchanged legacy source
  hashes;
- compile A1 through A6 and a subroutine-only anchor with explicit
  object-only commands;
- reject REAL32 admission to the REAL64 mutable lane, an incomplete SC
  bundle, nonconforming group tails, any enabled-by-default route, and
  any host control flow that can execute legacy `MCGFCF` or `MCGFST`
  after the A5 response;
- prove that all compiler commands use `-c`;
- inspect exact unresolved-symbol allowlists without linking an object;
- execute no object, prerequisite runner, synthetic program, tracking
  read, transport solve, or Dragon process.

The hashes and object-symbol receipts are frozen only after the complete
short gate and an independent review pass.

## Next threshold

Do not add a production callsite yet. The next engineering step is
upstream:

1. establish a continuous REAL64 owner for `QFR/PHIIN` across the radial
   iteration, with no REAL32 round trip before the terminal decision;
2. establish one complete, ordered, lifetime-bounded
   `SC(0:M,1,NGEFF)` bundle for the same gathered tail and physical
   state, without asking the rendezvous to perform LCM I/O or gathering;
3. only then re-evaluate the fail-closed Phase-A6 production admission.

A later, separately authorized runtime-preflight gate may validate object
identity and lifetime. Transport execution remains beyond that gate.
