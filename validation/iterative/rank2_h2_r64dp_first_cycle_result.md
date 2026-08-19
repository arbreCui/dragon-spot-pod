# REAL64-kernel route: first three maps and the exact-dynamics boundary

Date: 2026-08-18

Status: three maps `VALID_NOT_MET`; `LEAKAGE_CHANNEL_GROWTH_ESTABLISHED`.

## New numerical-map contract

Route `r64dp`: solves under the REAL64 axial kernel (`FLU2DR64` /
`SPOF64` / `SPOT1P64` / `SPOLE1D`); axial deck constants
`solver_eps = 5.0e-8`, `REBA OFF`, `ACCE 3 0`; radial half unchanged;
the `5e-7` outer AND gate unchanged; residual history restarted — no
old-route residual is mixed into any new AA(1).  The REAL64-era
lifecycle admissions were extended with demote-direction identities
(`SPOR64_B2J`/`B2W`, candidate builder/checker, map checker), keyed on
the presence of the REAL64 records and falling back to the frozen
legacy identities otherwise; the solver-iteration-control entries 9-10
of the axial STATE-VECTOR (`ACCE`,`REBA`) are declared route-contract
inputs and exempted from the fixed-package comparison.  Final binary
hash `07deb5209fe8...3174f544` (physics kernels identical to the
validated `e343d327...` build; only lifecycle admission modules were
patched afterwards).

## The three maps (epochs 12, 13, 14; all strict `5e-8` terminals in 9
outers, 15-16 s each)

1. `g = G(f)` from `CLOSED/11`:
   $(R_\rho,R_L,D_L,R_a)=(1.6761702\times10^{-7},\,
   4.8157300\times10^{-6},\,7.0559211\times10^{-9},\,
   2.5965667\times10^{-7})$.  AA(1) `NOT_FORMED` (single new-route
   pair).  See `iterative-rank2-h2-r64dp-cont-f-map`.
2. `h = G(g)`:
   $(5.1672714\times10^{-9},\,1.0697428\times10^{-5},\,
   1.5673663\times10^{-8},\,1.0244259\times10^{-7})$.  Under exact
   arithmetic the pure-Picard leakage defect **grew by 2.22x** while
   $R_\rho$ and $R_a$ fell.  The AA(1) direction on `g-f,h-g` passed
   all three screens `(0.976884, 0.917473, 0.917091)`, giving
   $q=0.0837464161121885819\,g+0.916253583887811418\,h$.  See
   `iterative-rank2-h2-r64dp-cont-g-map`.
3. `i = G_2(q)`:
   $(3.7365829\times10^{-8},\,6.5487670\times10^{-5},\,
   9.5951252\times10^{-8},\,1.0304539\times10^{-7})$.  The leakage
   defect **overshot 6.1x against a 0.917 screen prediction** — under
   exact REAL64 arithmetic, with strict terminals, and bitwise
   independent reproduction.  The next AA(1) on `h-g,i-q` passes its
   screens `(0.667290, 0.499930, 0.496267)` and is recorded but not
   materialized.  See `iterative-rank2-h2-r64dp-aa1-h-candidate` and
   `-map`.

## Supported boundary statement

The REAL64 kernel removes every numerical excuse: terminals are
certified at `5e-8`, defects are exact, and the map is deterministic.
What remains is genuine dynamics: **the leakage channel of the coupled
2D-1D + POD outer map expands under both direct Picard (factor ~2.2
per step) and depth-one Anderson mixing (overshoot despite passing
affine screens), while the eigenvalue and modal channels contract
monotonically** ($R_\rho$ down to $5.2\times10^{-9}$, $R_a$ down to
$1.02\times10^{-7}$, both passing the gate).  The r32-era oscillation
and screen failures are now explained as this same instability seen
through quantization noise.  Depth-one Anderson along a locally
expanding, nonlinear leakage direction is not a convergent scheme for
this map; no relaxation or empirical stabilization was introduced, and
none is authorized by this record.

The previously blocked Newton/JFNK route (`nonlinear_solver_contract`)
was rejected on binary32 publication-resolution grounds — a
finite-difference probe could not produce consistent directional
quotients.  The REAL64 kernel removes that obstruction: exact
directional derivatives of the leakage block are now measurable, and a
Newton-type treatment of the leakage channel (or deeper/windowed
Anderson) is the remaining parameter-free path to the unchanged
`5e-7` gate.  That choice is a new solver-contract decision and is not
made by this record.
