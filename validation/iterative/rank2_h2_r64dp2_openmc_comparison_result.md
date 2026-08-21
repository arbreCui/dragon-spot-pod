# The rank-2 fixed point against the independent OpenMC reference

Date: 2026-08-20

Status: `PASS` on the inherited Level-4 acceptance gate;
`SELF_CONSISTENCY_AND_ACCURACY_DIVERGE_MEASURED`.

Until now this method had been compared with an external reference
exactly once, and that comparison used the **rank-1 one-shot baseline**
of 2026 — not the converged rank-2 solution.  The Level-4 comparison has
now been rerun, unchanged in protocol, against the fixed point of the
iterative route.

## Provenance: the reference is the same reference

The OpenMC model is built from a solver-neutral `MGXEXP` export of the
DRAGON macrolib; no SPOD quantity enters it.  Rebuilding that export
from the current tree reproduces the hash prefix recorded in the
Level-4 README, `d561c486`, and rerunning OpenMC under the frozen
protocol (370 groups, 24 snapshot material blocks, P2 without transport
correction, reflective hex boundary, three 50 cm floors at 650/750/850,
vacuum at `z = 0` and `150`, 200 batches / 50 inactive / 20 000
particles) reproduces the recorded eigenvalue to every printed digit:

| | recorded 2026 | rebuilt today |
|---|---|---|
| OpenMC `k` | `1.36565328` | `1.3656532819149128` |
| `sigma` | `0.00004588` | `4.588434424300107e-05` |
| reactivity `sigma` | `2.46 pcm` | `2.4602748 pcm` |

The comparison is therefore against the same physics and the same
reference, not a re-derived one.

## Result

The two SPOD observables are emitted by a read-only deck from the
`CLOSED/69` fixed-point state — the eigenvalue by `GREP` of
`SPOT-X-KEFF`, the axial shape by `SPORATE` — so nothing is transcribed
by hand:

| | `k` | `rho - rho_OpenMC` | max floor-fraction difference |
|---|---|---|---|
| rank-1 one-shot (2026) | `1.36417100` | `-79.56 pcm` | `4.876e-4` (0.189%) |
| **rank-2 fixed point** | **`1.362411321920423`** | **`-174.24 pcm`** | `8.131e-4` (0.302%) |

Predeclared acceptance limit `500 pcm + 3 sigma` = `507.38 pcm`.  All
four gates pass: frozen protocol, transfer audit, Monte Carlo
statistics, reactivity acceptance.

## The finding worth stating plainly

**Converging the outer iteration moved the answer away from the Monte
Carlo reference.**  The rank-2 fixed point sits `94.68 pcm` below the
rank-1 one-shot in reactivity, and the axial fission shape difference
grows from 0.189% to 0.302%.  Self-consistency and agreement with the
external reference are, on this problem, pulling in opposite
directions.

This is a measurement, not a verdict, and two things must be said with
it.  First, the comparison carries a known modelling difference —
OpenMC samples the exported P2 data without transport correction while
the SPOD solve uses the transport-corrected macrolib — which is
precisely why a `500 pcm` allowance was predeclared; `-174 pcm` sits
well inside it and does not by itself indicate an error in either
solver.  Second, the erratum already recorded that the gate certifies
the outer iteration's **self-consistency, not its accuracy**
([rank2_h2_r64dp2_method_erratum.md](rank2_h2_r64dp2_method_erratum.md),
section 5).  That statement now has a number attached to it: on this
problem, driving the residual from `1.98e-7` to the fixed point buys
`~95 pcm` of *disagreement* with the only external reference the
project has.

## The decomposition was attempted and is not executable

The obvious follow-up is to remove the modelling difference: give OpenMC
the transport-corrected data so that the Monte Carlo solves the same
approximate problem the deterministic route solves, and the remainder is
the SPOD method error alone.  It cannot be done.

Applying DRAGON's own correction to the export drives the P0
self-scatter diagonal negative in **2043 of 8880 entries (23.0%)**,
worst `-6.674e-02` at mixture 4, group 43, and Monte Carlo cannot sample
a negative scattering probability; `build_reference` refuses the file.
For scale, the raw export's own negative P0 mass is `8.0e-08` of the
positive mass — numerical noise, which the frozen protocol zeroes and
rescales.  The corrected data is negative by six orders of magnitude
more, across a quarter of its diagonal.  Zeroing that would fabricate a
third model belonging to neither solver.

This is precisely why the 2026 protocol compares raw-P2 Monte Carlo with
transport-corrected deterministic and predeclares a `500 pcm` allowance:
**there is no Monte-Carlo-samplable form of the deterministic solver's
own cross sections.**  So the `-174 pcm` cannot be decomposed from the
reference side at all.

Two by-products of the attempt are recorded with it
(`level4-transport-correction-decomposition`).  First, stripping `TRANC`
from `initial_axial_macrolib.xsm` and rerunning the fixed-point map
leaves `k` **bitwise unchanged** — that macrolib's `TRANC` is dead data
on this route, since the axial SPOD assembly reads `DRAGON-TXSC` and
`DRAGON-S0XSC` off the snapshot systems and never consults it, while the
OpenMC export is taken from that same macrolib's raw `NTOT0`.  Second,
the decomposition that remains open runs the other way — give the
*DRAGON* route the raw P2 data, where negativity is not a problem — but
that changes the method's configuration and needs a new era and a
re-convergence, so it was not started.

## Rank adequacy, the question this comparison left open

The Level-4 record says plainly that passing the rank-1 comparison "did
not by itself establish rank adequacy".  With three snapshots, rank
three is **full** rank: the basis spans the snapshot set exactly and the
out-of-span residual vanishes, so a converged rank-3 solution would
separate the POD truncation from everything else in the `-174 pcm`.

The rank-3 basis builds cleanly and passes both nesting checks of the
existing discipline — a fresh rank-2 rebuild reproduces the frozen
rank-2 reference bitwise, and rank three's leading two modes reproduce
fresh rank two bitwise.  **The rank-3 outer iteration then does not
converge.**  Five pure Picard steps oscillate in `k` by about `1e-3`
while the leakage residual stops contracting and begins to grow
(`4.35e-5 -> 1.21e-5 -> 1.44e-5 -> 1.83e-5`), where rank two on the same
map contracts `0.037` per step to a fixed point.

The POD spectrum says why:

| | median | |
|---|---|---|
| $\sigma_2/\sigma_1$ | `4.46e-05` | a real, small second mode |
| $\sigma_3/\sigma_1$ | `1.96e-07` | below `1e-07` in **182 of 370 groups** |

The snapshot fluxes and the POD basis are REAL32, whose relative
precision is `~6e-08`.  The third singular value is therefore about
three times the arithmetic noise floor of its own input data, and in
half the groups it sits on that floor.  **The third mode is not physics;
it is the single-precision noise of the snapshots**, and feeding a
noise-dominated coordinate through the outer feedback loop is what
destroys the contraction.

Three consequences.  Rank two is **not** a truncation compromise here —
it is the numerically supported rank of this snapshot set, and the
original design choice is vindicated by measurement.  The `-174 pcm`
therefore **cannot be attributed to POD truncation and cannot be reduced
by adding modes**: the modes are not there to add; what remains is the
2D/1D synthesis itself and the transport-correction modelling
difference.  And a genuine third mode would need REAL64 snapshot fluxes,
which is a different era and was not attempted.

These rank-3 numbers are **diagnostic, not certified**.  The iteration
runs through the B2W close and the B2J projection unchanged — both are
rank-generic — but `SPOXCONV` cannot compare states of different rank,
so no certified stopping defect exists, and the builder and checker are
hard-wired to rank two (`invalid frozen rank-two dimensions`).
Evidence: `level4-rank3-adequacy-probe`.

Nothing here is fitted.  The acceptance limit, the protocol and the
reactivity formula are imported from the 2026 checker
(`check_reference.py`) by the rank-2 variant so that the two
comparisons cannot drift apart.

## A blocker removed on the way

`SPOLIB`, `SPORATE` and `MGXEXP` are compiled into `libDragon.a` but had
**no dispatch branch in `KDRDRV.F`**, and `git log -S` shows they never
did.  No deck could call them, so Level 3, Level 4 and the Level-5 seed
could not run from this tree at all — the historical artifacts were
produced by a binary whose registry state is not in this repository.
The three branches are now registered; the addition is bitwise neutral
on the iterative route (`SPOT-X-RLEAK` bits `3DFDBB83122907D0`
unchanged, `0/1110` and `0/2220`).

## Boundary

One physical case remains the whole of this method's external
validation: the IRENA sodium-cooled hexagonal pin cell, now compared at
both rank-1 one-shot and rank-2 fixed point.  The assembly and colorset
geometries in `data/rnr_0burn_spot_proc/` are referenced by no deck and
have never been run.  Evidence:
`validation/artifacts/level4-rank2-fixedpoint-comparison`.
