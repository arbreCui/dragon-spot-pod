# The Gram era: declaration and re-anchor

Date: 2026-08-25

## What changed and why every prior receipt is void

The core corrections landed on `variant3-prime` (computed `B^T W B`
mass matrix in `SPOT1P`/`SPOT1P64`, `B1HOM64` replacing the defective
`B1HOM` copy pattern, the strict raw-Picard terminal gate with
accelerate-nonterminal `FLU2AC64`, the full-rank lifecycle admission,
the `SPOASM` fixed-basis allocation fix) change floating-point
arithmetic on every solve path.  By construction, **no bitwise receipt
from any earlier era replays** under this code.  This document declares
the era boundary instead of pretending continuity.

## Rank-2 re-anchor (the new baseline)

Six pure-Picard CONT maps from the frozen old-era fixed point, run on
the freshly built canonical binary, closed-parent deck pattern
(`DEL SPOT-X-STATE/EPOCH` and the four defect records), certified
`SPOXCONV` defect each map, `B2W` close each map, gate evaluated by
`check_convergence_gate`:

|                | old era             | Gram era            |
|----------------|---------------------|---------------------|
| k              | 1.3624113219204230  | 1.3624113283013846  |
| R_rho          | 3.12e-8 (floor)     | 3.28e-12            |
| R_L            | 4.33e-10            | 1.65e-10            |
| R_a            | 2.63e-9             | 3.77e-9             |
| PERP           | 1.856e-7            | 1.856e-7            |

The era shift is **+0.34 pcm**: the corrections are precision repairs,
not physics changes.  The old r32 rho-quantizer floor (`3.1e-8`,
deliberately left open in the old era) is **gone** — R_rho now sits four
decades below it; the keff64 channel work in `SPOSTATE`/`B2J`/`B2W`
closed that quantizer as a side effect.

Evidence: `validation/artifacts/iterative-rank2-gram-era-anchor`
(anchor decks, per-map defect table, gate verdict, closed state,
binary hash).

## New conventions of this era

- **Closed-parent decks.**  A continuation map parents directly on the
  closed state; the private solver copy deletes `SPOT-X-STATE`,
  `SPOT-X-EPOCH` and the four defect records.  The proposal-era decks
  (`DEL SPOT-X-CARR`) fail on closed parents and are historical.
- **Terminal-gate channels are per-channel floors.**  Measured on the
  full-rank axial solve: the per-unknown successive change (`EUNK`)
  plateaus at `3.71e-7` (~3x the REAL32 epsilon) while `EEXT` reaches
  `7.7e-11`.  Lanes that need it predeclare `UNKT` above that floor
  (the full-rank lane uses `1e-6`); k and `EEXT` keep `5e-8`.
- **Acceleration is legal, acceptance is raw.**  `ACCE n m` with
  `m > 0` accelerates only nonterminal outers; the strict gate accepts
  only an unmodified Picard image.

## Open front carried across the boundary

The physical-full-rank lane
(`validation/iterative/run_full_rank_physical_map.sh`) runs the whole
lifecycle without bypassing any guard.  Its axial solve **passes all
three declared terminals** (gate-pass at outer 1790,
k = 1.3767473539713819, EEXT 9.0e-10) and is then **refused by
`SPOSTATE`: the converged full-rank dominant mode contains nonpositive
active scalar flux.**  A physical transport operator has a positive
fundamental mode, so this k (+1400 pcm from rank-2) is *not* a
reduction-error measurement; the guard is right to refuse it.  The
frozen-L1d mechanism is excluded by measurement (only 9/1110 negative
entries, worst 0.7% of NTOT0).  The open question is whether the
negativity is an assembly defect in the complement directions or an
intrinsic property of the 2D/1D closure evaluated away from its
consistency point — the flux census decided it
(`validation/artifacts/full-rank-radial-reducibility`): the refused mode
is a **radial collapse onto one fuel-ring column** — non-fissile columns
underflowed to exact zero, the other MOX rings are decaying
power-iteration remnants (two slightly negative).  SPOT1P64's separable
path was verified bit-exact against a dense reference: no solver defect.
The cause is method-level: **the full-rank axial operator has no radial
coupling at all** (fission, scattering, and the B1 correction are
region-local; the frozen leakage is a diagonal removal), so the TYPE-K
eigenproblem is block-diagonal over the radial columns and correctly
converges to the most reactive column in isolation.  Radial coupling in
this 2D/1D scheme exists *only through the rank-2 projection*: the
reduction is not an approximation bolted onto the closure, it **is** the
closure's radial coupling.  A full-rank oracle posed on this closure is
ill-posed by construction; the −174 pcm must be decomposed against an
independent 3D direct-transport reference, or the closure upgraded to an
off-diagonal radial exchange matrix.
