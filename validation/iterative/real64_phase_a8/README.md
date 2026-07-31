# REAL64 Phase-A8 inner suffixed compile-only closure

## Purpose

Phase-A8 is the first validation-only implementation of the inner part of
the REAL64 lane frozen in Phase-A7.  It is deliberately outside `src/` and
is never linked or executed.  Its only scientific claim is narrower:

```text
validation-owned REAL64 active tail
  -> DOORFV64
  -> MCCGF64
     -> SPOMOC_MCCGF_BEGIN
  -> MCGFLX64
  -> MCGMRE64
  -> MCGFL164
     -> MCGFCS64
     -> MOCIK3
     -> MCGFCF
        -> MCGFFIR64_RANK_ADAPTER -> MCGFFIR
        -> MCGSCA
     -> MCGFST
     -> unresolved checked SPOMOC_CAPTURE64 seam
     -> MCGFCA64
        -> MCGFCR64
        -> MCGPRA64 -> MSRLUS1
        -> MCGABG64 -> MCGPRA64 -> MSRLUS1
```

All mutable source, flux, residual, correction and solver-control values in
this chain are `REAL64`.  Stored tracking, cross-section and ACA operator
records remain at their frozen `REAL32` kind and are promoted exactly only
when they enter a `REAL64` expression.  There is no mutable-state downcast.

## A8 addendum to the A7 blueprint

An independent pre-implementation audit found three details that A7 did
not freeze precisely enough for an exact compiler gate.  A8 therefore adds
the following small addendum before claiming implementation closure.

First, every state-owning layer from `DOORFV64` through `MCGABG64` has an
explicit `OK` result and an `integer(int64) CUTOFF_DELTA64` result.  Both
are initialized fail-closed.  A parent adds each child delta exactly once,
in call order.  Reaching an inherited iteration cap by a normal return is
not silently redefined as a structural failure; `DOORFV64` nevertheless
scatters state only after structural success and a finite-value check.

Second, `SPOMOC_CAPTURE64` is only an unresolved, checked interface in A8.
A8 compiles the four-`REAL64`-array call point, but it neither edits
`src/SPOMOC.f90` nor implements GANLIB writes.  The production audit
implementation and ON-arm wiring remain A9 work.

Third, the live `MCGABG` arithmetic uses legacy `DDOT`.  A8 freezes and
compile-checks that reuse, including the selected-toolchain proof that
`kind(0.0d0)==real64`; it does not replace `DDOT` with a different
reduction.

The machine-readable authority is
[`precision_manifest.json`](precision_manifest.json).

## Fixed numerical method

The branch remains exactly the frozen non-cyclic, isotropic 2-D MCCG path:

```text
NGRP=370, NREG=8, NSOUT=6, NLONG=KPN=14, NBMIX=8
NANI=NLIN=NFUNL=1, STIS=1, IDIR=0, ISCH=11
KRYL=10, IAAC=80, ISCR=0, PACA=4
MAXI=20, NSTART=10, MAXIT=19, MAXACC=200, LFORW=true
```

No Richardson, alternate BiCGSTAB transport solver, SCR, combined ACA/SCR,
multigroup ACA rebalancing or macrolib-scattering branch is represented.
The ACA corrective solve retains the inherited binary32 `1.0e-7` cutoff
by exact promotion.  A zero-cutoff Boolean counterfactual only counts when
one of the four existing live guard sites would differ; it cannot select a
branch, modify state, alter termination, or authorize publication.

The restarted GMRES is the inherited `GMRES(10)` structure: one primary
response per outer visit, one RHS response for the whole solve, two modified
Gram-Schmidt passes, stored Givens rotations, triangular back substitution
and a REAL64 iterate update. An input `NCONV=.false.` entry can never be
reactivated. Reaching `MAXIT=19` is reported through the inherited iteration
state and remains a normal solver return; non-finite values or invalid
structure fail closed.

There is no relaxation coefficient, fitted parameter, new tolerance,
clipping rule or model term.

## Exact ABI points

`KEYFLX_BASE1` remains rank one.  The tracking record is mapped directly as
`KEYFLX_TRK3(NREG,1,1)`.  `MCGFST` and `MCGFCA64` receive the direct
rank-two section `KEYFLX_TRK3(:,1,:)`; the global callback adapter receives
the legacy rank-three callback dummy and passes only
`KEYFLX_TRK3(:,:,1)` to checked `MCGFFIR`.  `PJJIND$MCCG` is mapped directly
as `PJJIND_TRK2(NPJJM,2)`.  Flat mappings and sequence association are not
accepted.

The adapter is a global external explicit-shape subroutine.  It is not a
module procedure, `BIND(C)` procedure or descriptor ABI, and it performs no
numerical work.

The PACA=4 path requires `IM(NLONG+1)` and `CF32(LC)`.  Local one-element
`IM0_INACTIVE` and `MCU0_INACTIVE` are used only with `LC0=0` assumed-size
inactive formals.  Explicit-shape inactive real formals receive complete,
defined `LUCF_INACTIVE32(LC)` and `DIAGF_INACTIVE32(NLONG)` storage.
The direct pre-`MCGABG64` application uses inactive `DIAGF`; every
`MCGABG64` call uses the active `DIAGF$MCCG` view.
Before either `MSRLUS1` call, every sparse row must satisfy
`IM(I)+1 <= JU(I) <= IM(I+1)+1`.  In the BiCGSTAB update, a finite negative
`DDOT` rho remains valid; only a non-finite or exact-zero denominator is a
structural breakdown.  Neither rule introduces a numerical threshold.

## Record admission

The compile-only source encodes the same fail-closed ordering required for
future runtime use: `LCMLEN` type and extent checks precede every LCM payload
mapping.  `MCCGF64` owns one complete ordered
`SC_BY_GROUP32(0:NBMIX,1,NGEFF)` copy and no downstream routine gathers SC
again.  The regular tracking identity is fixed at 8 regions, 6 surfaces
and 14 unknowns; `MATALB_TRK` has bounds `(-6:8)`.  Keys form a duplicate-
free permutation, zone and boundary indexes are in range, volumes are
finite and positive, and active PJJ and PACA=4 records have their exact
types and extents.

`ICODE<=0` is a valid legacy geometry code and keeps the tracking `ALBEDO`
for that surface.  Only a positive `ICODE>NALBP` is rejected before
`MCGSIG`; no negative code is reclassified as an invalid group-albedo
index.

Each `MCGFL164` visit reproduces the legacy stream entry sequence:
rewind, header and comments, the nine-integer geometry header, then exactly
six skipped records before `MCGFCF` consumes the first track.  This freezes
the lexical lifecycle without claiming that a real file is at the promised
runtime epoch.

These checks are compiled but not executed in A8.  Consequently they do
not establish that a real `IPTRK`, `KPSYS`, file position or LCM epoch has
the promised runtime identity.

## Gate

The isolated gate is:

```sh
make spot-real64-phase-a8
```

It verifies the scoped receipt and manifest, compiles only relocatable
objects with strict checked interfaces, requires targeted ill-typed or
wrong-rank fixtures to fail, and compares exact defined and unresolved
symbol inventories.  It invokes none of the A1-A7 runners because earlier
synthetic runners may link or execute test programs.  It does not run
Dragon, read tracking data, apply transport, link an A8 object or execute
one.

## Claim boundary

Even after this gate passes, A8 does **not** establish a continuous radial
REAL64 lane.  It does not implement `FLU2DR64` ownership, `FLUBAL64`,
`FLU2AC64`, terminal norms, archives, the type-2 compatibility mirror,
production dispatch, runtime provenance, a real MOC response, radial
convergence or Picard convergence.  Those claims require later, separately
authorized gates.
