# Phase-A9b B2j: archive-wide REAL64 projection

B2j performs the first physically meaningful update after the B2i bootstrap
seal.  It is intentionally only the global-to-plane projection.  It does not
assemble a radial system, construct a fission source, run transport, or judge
convergence.

The controlled transition is

```text
AX CLOSED/0 + archive CLOSED/0 + three planes SOLVED/0
    -> fresh archive PROJECTED/1 + three planes PROJECTED/1
```

The AX root remains read-only `CLOSED/0`.  Projection does not create a new
axial solution, so copying AX and relabeling it as epoch 1 would be false.
The `RHO` carried by `PROJECTED/1` is still the exact parent value `rho0`; it
drives the work of iteration 1 and is not a claim about the future `rho1`.

## The complete formula

For energy group `g`, plane `p`, radial region `i`, and retained mode `a`,

```text
phi_hat[g,p,i] = sum_a real(B[g,i,a], binary64) * A[g,p,a]

B index = BOFF[g] + (a-1)*8 + i
A index = OFF[g]  + (p-1)*rank[g] + a
```

The loop order is group, mode load, plane, then the B2h region/mode
contraction.  It reproduces the fixed-space definition stored by `SPOSTATE`.
There is no additional normalization: the canonical coordinates already use
the one global `NUFISS-UNIT` normalization.  There is no tolerance, damping,
relaxation, clipping, floor, fit, or empirical coefficient.  A non-finite or
non-positive reconstructed region is rejected.

## Exact provenance boundary

The validation route calls production B2C three times, production B2i once,
and then B2j immediately on that fresh in-memory pair.  This
B2i-to-B2j direct in-memory lifecycle is part of the present contract.
Epoch zero is not a globally unique identifier, so arbitrarily combining
persisted `CLOSED/0` files is not admitted by this phase claim.

B2l later extends only the fresh **output** medium: production B2J may commit
directly to a new XSM root under the same empty-root and final-epoch rules.
The original B2j receipt remains the direct in-memory qualification and does
not claim persisted `CLOSED/0` input mixing.  B2l dynamically qualifies the
new output boundary with six close/reopen cases, including nonempty and
tombstoned targets plus early and late zero-write rejection paths.

Before any caller-visible write, B2j requires:

- exact `CLOSED/0`, `SOLVED/0`, `RHO`, `K`, and authority inventories;
- the frozen Synthesis-POD `DIMS/RANK/OFF/BOFF/BASIS/A/L` layout;
- plane track volume and key maps consistent with the axial radial ordering;
- same-index library, system and `SYSTEM/SPOT-L1-SNAP` structure;
- every plane `FLUX/SPOT-LEAK1D` to be the exact binary32-to-binary64
  promotion of its canonical AX `SPOT-X-L` slice.

The old SYSTEM leakage is checked only for finiteness.  It belongs to the
radial equation that produced the `SOLVED/0` state and therefore is not
equated to the newly returned canonical leakage.

## Private all-plane staging

B2j computes all 1,110 `(plane, group)` slices before publication.  It then
uses the real B2h publisher on three private fresh LCM roots.  B2h replaces
the eight region unknowns with the REAL64 projection and preserves the six
non-region unknowns from the REAL64 `SOLVED/0` seed.  B2j independently
checks each staged authority, its REAL32 mirror, lifecycle and canonical
leakage.

Only after all three stages pass does B2j create the caller's archive.  It
deep-copies `TRACK` and `MICROLIB2`, inserts the three complete fresh B2h FLUX
objects, closes the private stages, and finally writes archive-root
`STATE=PROJECTED` followed by `EPOCH=1`.  Root `EPOCH` is the final LCM
mutation.

## Why SYSTEM is absent

SYSTEM is deliberately absent from the projected archive.  The input SYSTEM
contains the lagged leakage used by the preceding radial solve.  Copying it
into epoch 1 would allow a continuation solve to use the wrong Picard map.

The next lifecycle gate must rebuild a fresh SYSTEM from each projected
FLUX object's canonical `SPOT-LEAK1D`.  Until that happens, the archive is
structurally unable to enter CONT.  B2j itself does not claim that ASM has
run or that an epoch-matched SYSTEM exists.  The plane root still carries
`LINK.SYSTEM='SYSTEM'` because B2h preserves the required future object name;
it does not mean that a SYSTEM object is present in this archive.

The successful output inventory is therefore

```text
archive: SIGNATURE, LISTDIM, SPOT-ITER-K, TRACK, MICROLIB2, FLUX, SPOT-R64
archive SPOT-R64: RHO, NPLANE, STATE=PROJECTED, EPOCH=1
plane SPOT-R64:   RHO, FLUX, STATE=PROJECTED, EPOCH=1
plane root:       one binary32 FLUX compatibility mirror and no SOUR/QFISS
SYSTEM:           absent, pending a fresh ASM lifecycle gate
```

Run the seconds-scale gate with:

```sh
sh validation/iterative/real64_phase_a9b_b2j_archive_projection/run_phase_a9b_b2j_archive_projection.sh
```

The gate compiles with strict floating-point and runtime checks, reads the
three frozen XSM files without modifying or fully copying the 218 MB archive,
and performs only small in-memory calculations.  It does not run Dragon,
read sequential tracking records, call transport, build QFISS, or execute
CONT.  `RADIAL-CONVERGENCE=NOT-EVALUATED` and
`OUTER-PICARD-CONVERGENCE=NOT-EVALUATED` remain authoritative.
