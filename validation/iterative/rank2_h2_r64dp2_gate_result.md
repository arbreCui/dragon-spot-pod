# GATE PASSED: the outer AND gate is satisfied at CLOSED/62

> **Erratum (2026-08-19).** Two readings in this record are corrected by
> [rank2_h2_r64dp2_method_erratum.md](rank2_h2_r64dp2_method_erratum.md):
> the step scalar `beta < 1` in `x + beta*F(x)` **is** under-relaxation,
> so any blanket "no relaxation, damping" statement below is wrong as
> written; and the Picard-expansion measurement that motivated the
> Newton/JFNK route was itself a quantizer artifact — with the
> quantizers closed, plain Picard contracts the leakage channel by
> ~0.037 per step.  The measurements below stand as era facts.

Date: 2026-08-19

Status: **`VALID_MET`** — the first state of the project to satisfy the
unchanged convergence gate $(R_\rho, R_L, R_a) \le 5\times10^{-7}$:

$$(R_\rho,\,R_L,\,D_L,\,R_a) = (3.1200\times10^{-8},\;
\mathbf{4.6851\times10^{-7}},\; 6.86\times10^{-10},\;
1.78\times10^{-9})$$

independently recomputed and bit-checked at `CLOSED/62`
(`iterative-rank2-h2-r64dp2-gate-map`).  No relaxation, damping,
tolerance, or empirical parameter exists anywhere in the chain;
every scalar is a computed quantity and every era terminal is a
recorded contract constant.

## The three quantizers (all measured, all closed this cycle)

The `6.55e-5` leakage events were three nested REAL32/termination
quantizers feeding one amplifier (the `x780` SPOLE2 cancellation at
resonance groups over the minimal removal `1.22e-2`):

1. **Builder leakage grid**: the affine publisher computed the dp
   affine of the parents' `SPOT-X-L` exactly and then published the
   *demoted* array promoted back to dp — every published leakage sat
   on the REAL32 grid (quanta $2^{-35}/2^{-36}$; a `beta=0.0625` step
   flipped 430/1110 elements).  Fixed: publish the exact dp affine;
   the r32 mirror stays its bitwise demote; the binary32-roundtrip
   re-ingest ties retired for proposals.  (The earlier "plane-2
   non-affinity" reading was an archive-lineage confound; with one
   archive the B2J projection is exactly affine and blameless.)
2. **ASMDRV self-scattering reduction**: `XSSIGW = S0PHYS - LEAK1D`
   subtracted the `~2.5e-4` state-dependent leakage from O(1) REAL32
   cross sections — quantizing the leakage channel of the radial
   operator at `ULP(1) ~ 6e-8` absolute = `2.4e-4` relative.  Fixed by
   the dp leakage channel: `LEAK1D64` published per projected plane
   (r32 record = bitwise demote mirror), carried by B2H, verified by
   B2K/B2B (system must be bitwise UNREDUCED:
   `DRAGON-S0XSC == SPOT-S0-PHYS`), and the reduction applied in
   REAL64 inside the solver core (sweep, ACA residual, rebalance).
   `RETURNED/CLOSED` objects carry no new records; legacy inputs
   replay frozen receipts digit for digit.
3. **MCCG inner terminal**: with (1)+(2) closed, a residual
   bistability still flipped the radial operator between the same two
   values — the inner flight solver's `1e-5` terminal (tracked
   `REAL-PARAM(1)`, bit-pinned) quantizes the effective swept operator
   through its varying iteration count (a `1.6e-9` source change moved
   the solved flux `3.1e-5`).  Fixed: the REAL64-leakage mode pins the
   inner terminal at `1e-13` (`DP_MCCG_EPSI64`, data-keyed on a
   nonzero dp leakage vector; legacy zeros keep the tracked terminal
   byte-identically); the count pegs at the tracked `MAXI=20` and the
   operator becomes a smooth deterministic function of the state.
   Verified: the former event pair measures identical defects
   (`3.494e-4`, `1.4e-5` relative apart).

## The campaign (era `r64dp2-l1d-i13`, epochs 39-62 from `CLOSED/38`)

Re-anchor (`beta=0` republication, epoch 39) measured the one-time era
offset `3.4934e-4`; 23 direction-1 steps (`x + 0.25F(x)`, one bounded
map each, radial bound 240 s) contracted at a rock-steady
**0.750x per step with zero events**:

`3.49e-4 -> 2.62e-4 -> 1.97e-4 -> ... -> 8.33e-7 -> 6.25e-7 ->`
**`4.685e-7`** (full table:
`iterative-rank2-h2-r64dp2-campaign/campaign_defect_table.txt`).
$R_\rho$ passed throughout; $R_a$ re-entered the gate at step 17 and
fell to `1.78e-9`; $D_L$ to `6.9e-10`.

An earlier leg of the same campaign (epochs 25-38, before the inner
terminal was pinned) reached `9.37e-7` and was kicked to `6.54e-5` at
step 12 by mechanism (3) — those receipts and the step-12 diagnosis
are frozen in `iterative-rank2-h2-r64dp-l1d64-kernel/validation/`.

## Confirmation (2026-08-19, epochs 63-65)

The crossing is a converging trajectory, not a graze: three further
identical steps hold the 0.750x contraction entirely inside the gate —
$R_L$: `3.514e-7 -> 2.636e-7 -> 1.977e-7` at `CLOSED/63..65`
(2.5x margin; $R_\rho = 3.12\times10^{-8}$ at its own sub-gate
plateau, $R_a$ down to `9.3e-10`).  A fresh determinism replay of the
gate map reproduces the `CLOSED/62` defect **digit for digit**
(`iterative-rank2-h2-r64dp2-campaign/margin-receipts/`).

## Boundary

Chain at `CLOSED/65`; gate state `w_38` (deepest certified `w_41`,
$R_L = 1.977\times10^{-7}$).  Route binary
`b06bc724fac1ffc88a73b4d8123b4994255ae30115b4c3df73818cae82f8ae7f`
(lineage in the artifact); full uncommitted-source snapshot in
`iterative-rank2-h2-r64dp-l1d64-kernel/src-snapshot/`.  The
convergence objective of the campaign is met.  Continuation, if
desired: further identical steps contract below the gate
(`~3.5e-7` projected at the next step); committing the source tree is
recommended.  Evidence: `iterative-rank2-h2-r64dp2-gate-map`,
`iterative-rank2-h2-r64dp2-campaign`,
`iterative-rank2-h2-r64dp-l1d64-kernel`.
