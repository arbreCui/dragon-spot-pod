# Method erratum: the step scalar was damping, and the fixed point is four Picard maps away

Date: 2026-08-19

Status: `ERRATUM`; `PICARD_FIXED_POINT_REACHED`;
`L1RAW_FAIL_OPEN_CLOSED`; `RHO_QUANTIZER_IDENTIFIED`.

This record corrects two readings that ran through the whole `r64dp`
era, closes one fail-open hole, and identifies the remaining floor of
each gate channel.  Nothing here changes any previously recorded
measurement: those stand as era facts.  It changes what they mean.

## 1. The step scalar `beta = 0.25` was under-relaxation

`x_{n+1} = x_n + beta*F(x_n)` with `F = G(x) - x` and `beta < 1` **is**
damped Richardson iteration.  Every `r64dp`-era record that states "no
relaxation, damping, or empirical control is introduced" is therefore
wrong as written.  The accurate statement — and the one the protocol
actually held to — is: no *tuned* parameter, no physics change, no
relaxed acceptance criterion; the gate stayed at `5e-7` throughout.
But `beta` itself was a frozen Newton coefficient measured in the
quantizer era (`alpha_1 = 0.2212...0.2375`, cycles 1-2) and reused for
26 consecutive steps without re-derivation.  That is exactly the kind
of stale empirical constant the protocol forbids elsewhere.

Its cost was measured, not estimated.  The error map is
`M = (1-beta) + beta*J`; the campaign's contraction was `0.750` to
three or four digits for 26 straight steps, which is the signature of
`J ~ 0` — the "contraction" was almost entirely the `(1-beta)` decay
of the damping factor, not the map converging.

## 2. The Newton/JFNK route was built to fight a quantizer artifact

The measurement that motivated it — "the leakage channel of `G` is
expansive under Picard, growing `2.22x` per step" — was made while all
three quantizers were open.  With them closed, one pure-Picard map from
`w_41` gives a **`0.0372x`** contraction of the leakage residual.  The
1-D line search, the Krylov directions, the least-squares step
coefficients, and the depth-1 Anderson disproof are all era-local: the
numbers are correct, the dynamical conclusions drawn from them do not
survive the quantizer fixes.  The affected records carry a banner
pointing here.

## 3. The fixed point, reached in four maps

From `w_41` (`CLOSED/65`) with `beta = 1.0` (era `r64dp2-l1d-i13`
plus the guard of section 4, binary `3db907dc...`):

| epoch | $R_\rho$ | $R_L$ | $D_L$ | $R_a$ |
|---|---|---|---|---|
| `CLOSED/65` start | 3.1186e-8 | 1.9772e-7 | 2.897e-10 | 9.314e-10 |
| `CLOSED/66` | 3.1196e-8 | 7.3526e-9 | 1.077e-11 | 8.635e-10 |
| `CLOSED/67` | 3.1191e-8 | 1.1989e-9 | 1.757e-12 | 2.629e-9 |
| `CLOSED/68` | 3.1193e-8 | 4.3277e-10 | 6.341e-13 | 2.629e-9 |
| `CLOSED/69` | 3.1190e-8 | **4.3266e-10** | 6.339e-13 | 2.629e-9 |

The step-to-step leakage ratio at the last map is `0.9998`: the
iteration no longer moves.  This is the fixed point of the discrete
outer map, not merely a state inside the gate.  `keff = 1.36241132192`.
Margins to the unchanged gate: $R_\rho$ **16x**, $R_L$ **1156x**,
$R_a$ **190x**.

Four maps replaced the 23 damped maps that had barely crossed the gate,
and landed three orders of magnitude deeper.

## 4. The `SPOT-L1-RAW` fail-open is closed

The REAL64 leakage mode leaves the assembled radial system
*unreduced* (its self-scattering keeps the physical value; the leakage
is applied inside the solver core).  Until now that system carried no
marker, so any legacy consumer — `FLU.f`, `FLU2DR.f`, `SPOF.f` — fed
one would have silently dropped the axial leakage and returned a wrong
answer with no abort.  Closed by: `ASMDRV.f` writing `SPOT-L1-RAW` on
the unreduced system, guards in `FLU.f` and `FLU2DR.f`, and the five
system-root inventories widened to accept the marker.

Verified three ways (`iterative-rank2-h2-r64dp2-l1raw-guard`):
placement (marker on all three radial systems, absent on the axial
SPOD system, which is reduced by construction); a **negative control**
— injecting the marker into an axial system makes the legacy door
abort with `FLU: UNREDUCED SYSTEM REQUIRES THE REAL64 DOOR.`; and
bitwise neutrality — campaign, guarded and pre-guard binaries produce
the identical `SPOT-X-RLEAK` bits `3E8A89BA022B095D`, `0/1110` leakage
and `0/2220` modal differences.

Provenance note: the host tools `admit_candidate_radial` and
`close_r64_returned` were stale against the widened inventory and
**hard-rejected** the archive rather than passing it — the fail-closed
posture worked.  Both were rebuilt from current source before the
campaign resumed.  Host tools must be rebuilt whenever `src` changes.

## 5. What still floors each channel

- $R_\rho$ at `3.119e-8` is a **fourth quantizer, identified and left
  open**: the builder publishes `rho` through a REAL32 `K-EFFECTIVE`
  round trip (`build_rank2_modal_aa1_candidate.f90:562-566`) and B2J
  *enforces* the identity `rho64 == 1/promote(keff32)`.  The half-ULP
  of that grid mapped into `rho` is `3.2112e-8` analytically against
  `3.1190e-8` measured — a 3% agreement.  It is 16x below the gate and
  harmless today; closing it would need the same dp-authority +
  demote-mirror pattern and would open a new era.
- $R_a$ floors at `2.629e-9`, $R_L$ at `4.327e-10`; neither was chased.
- The inner terminal now pins the flight count at the tracked `MAXI=20`
  rather than converging to a tolerance.  That is deterministic and
  smooth, which is what the map needed, but it **redefines the discrete
  operator**: switching to it moved the fixed point by `3.49e-4` in the
  gate metric, ~700 gate widths.  The gate therefore certifies the
  outer iteration's **self-consistency**, not its accuracy.
- The ACA preconditioner records are still assembled by legacy
  `MCGASM.f` from the now-unreduced `DRAGON-S0XSC`, i.e. mismatched
  against the operator actually swept.  Preconditioner-only: it cannot
  move the fixed point, but those 20 inner iterations are less
  effective than they could be.
- Under `affine_beta_mode` several lineage ties are bypassed, which
  reduces verification coverage for exactly the states being certified.
- `SPOR64_B2B.f90` was reconstructed after the 2026-08-18 checkout
  incident and validated behaviourally (16-digit defect equality on two
  maps plus the legacy receipt).  That is strong evidence, not proof
  that no guard was lost.

## Boundary

Chain at `CLOSED/69`, at the fixed point of the discrete outer map.
Route binary `3db907dc62f8f5f2c6fe011cff662b79540173795d4109e33a6ba88174ff5794`.
The correct continuation contract is **`beta = 1.0`** — pure Picard —
until a measurement says otherwise; no damping, and no step scalar
carried across an era boundary without re-deriving it.  Evidence:
`iterative-rank2-h2-r64dp2-picard-fixedpoint`,
`iterative-rank2-h2-r64dp2-l1raw-guard`.
