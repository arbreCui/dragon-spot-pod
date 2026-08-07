# Phase-A9b B2n: REAL64 frozen-fission source

B2n closes the missing source boundary between B2m assembly and a future
single-plane radial solve.  It does not run `FLU`.

B2m preserves every plane's `TRACK`, `MICROLIB2`, and `FLUX` subtree bit for
bit when it commits `ASSEMBLED/1`.  B2n therefore reads the exact frozen
`PROJECTED/1` parent used by B2m, selects plane 1, and constructs the source
authority that `R64 CONT` will later require:

```text
PROJECTED/1, plane 1
  -> one REAL64 frozen-fission calculation
  -> zero-live-fission MACRO0
  -> FSOURCE/SPOT-R64/QFISS
```

Using `PROJECTED/1` directly avoids repeating three production `ASM` calls.
The B2m parent posterior already proves that the three source-relevant
subtrees are recursively identical in `ASSEMBLED/1`.  The accepted input hash
is consequently both a B2l source-state identity and the B2m copied-subtree
identity.

## Physical definition

For region `r`, fissile component `j`, source group `g`, and previous-flux
group `h`, B2n evaluates only

```text
f[r,j] = sum_h NUSIGF[m(r),j,h] * phi_old[r,h]
q[r,g] = sum_j ((CHI[m(r),j,g] * f[r,j]) * rho)
```

where `rho=1/k` is read from the plane's type-4 authority and
`phi_old` is read only from `SPOT-R64/FLUX`.  The operation order is frozen as
region, fissile component, old group, then destination group.  For every
fissile component the binary64 update is exactly
`q <- q + ((real(CHI,REAL64)*f)*rho)`.  Each multiply and add is binary64;
compilation forbids contraction and fast-math
reassociation.  The six non-region unknowns remain positive zero.

There is no fitted term, relaxation, damping, clipping, floor, normalization,
fallback to the root binary32 `FLUX`, reused terminal `SOUR`, or model
completion.  The root type-2 `DSOUR` is only a one-time compatibility mirror
of the completed type-4 `QFISS`; it is not read to construct the authority.

The temporary `MACRO0` is a recursive copy of the selected physical
macrolib.  Its only physical-payload change is that all 94,720 `NUSIGF`
values are replaced by positive zero.  This prevents a later `TYPE S` solve
from adding a second live fission source.  `CHI`, scattering, total and
transport cross sections are not altered.

## Lifecycle contract

The production routine accepts one `PROJECTED/1` archive, one plane index,
and two distinct fresh memory roots.  It performs complete read-only
admission and stages all source values before its first output write.  On a
normal commit:

```text
FSOURCE root: SIGNATURE, STATE-VECTOR, SPOT-FROZEN, SPOT-KEFF,
              SPOT-QINT, DSOUR, SPOT-R64
SPOT-R64:     RHO, PLANE, STATE=FROZEN-QFIS, QFISS, EPOCH=1
```

`EPOCH=1` is the final normal source-authority mutation.  This is a logical
same-process commit, not an ACID, rollback, `fsync`, or crash-safety claim.
Only after the routine returns committed does the validation harness make
whole-object XSM evidence copies.

The independent checker links GANLIB/UTILIB only.  It recomputes all 5,180
type-4 source values bit for bit, checks all 5,180 compatibility values as one
binary64-to-binary32 conversion, checks all 370 integrated-source values, and
recursively verifies the macrolib copy plus the 94,720 positive-zero fission
cross sections.  It is run twice read-only and its outputs must be byte
identical.  No numerical distance or empirical acceptance tolerance is used.
This posterior is scoped to the hash-pinned `PROJECTED/1` input; it is not a
general replacement for the producer's broader input admission.  The runner
verifies that frozen input identity before invoking it.

## Execution policy

The default target compiles and runs only static, mutation, and bounded-runner
tests and verifies the frozen parent inputs.  B2n output artifacts are
constructed only after explicit activation:

```sh
make spot-real64-phase-a9b-b2n-real64-frozen-qfiss
RUN_B2N=1 make spot-real64-phase-a9b-b2n-real64-frozen-qfiss
```

One activation permits one bounded `PROJECTED` materializer, one bounded
source builder, and two bounded read-only posterior executions.  It permits
zero Dragon, `ASM`, `SPOR64K`, `FLU`, transport, `CONT`, or Picard execution,
and has no retry path.

The accepted activation completed the materializer, builder, and two
posterior processes in 1.186, 0.695, 0.654, and 0.167 seconds respectively.
The posterior reports were byte-identical.  It verified 5,180 REAL64
`QFISS` values, 5,180 REAL32 mirrors, 370 integrated-source mirrors, 2,960
strictly positive region fluxes, 2,220 positive-zero non-region sources, and
94,720 positive-zero `NUSIGF` values.  The accepted identities are:

```text
PROJECTED c010c0a860884a4e4d3842dffe45ffb4898f2aaca99557e0411ee8c66d60b90c 225315452 bytes
MACRO0    6430b5e43b03125f8bd94c350bae2d8fc97978f86b3a5bb25f2026fd10914ada   9878532 bytes
FSOURCE   37a3499742125db65fb51e505797e2890f6ae29461af9640bf14352aad898f2d    625560 bytes
```

The strongest permitted B2n claim is:

```text
PLANE1-SAME-EPOCH-REAL64-QFISS-BITWISE-VERIFIED
AND ZERO-LIVE-FISSION-MACRO0-VERIFIED
```

It does **not** establish a radial flux solution, a radial balance residual,
radial or outer convergence, a complete Picard map, response-matrix accuracy,
SPOD truncation accuracy, eigenvalue or power accuracy, or agreement with an
independent transport program.  Convergence remains `NOT-EVALUATED`.

The next gate must first make `R64 CONT` compare the source and seed
`RHO/STATE/EPOCH` and expose the inherited ACA-cutoff visit count.  Only then
is one bounded real `FLU` scientifically auditable.
