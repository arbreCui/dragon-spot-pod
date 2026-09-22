# Corrected D4-A neutron-balance readiness

2026-09-23. Read-only source/field review, **not a neutron-conservation PASS**.
No transport, tracing, Dragon/OpenMC execution, production rebuild, or numerical
balance calculation was performed. The active continuation was not touched.

Subsequent numerical follow-up: the saved map-8 radial four-term calculation
has now been completed in [the balance diagnostic](d4a_radial_balance_result.md).
The readiness review below retains its original scope and limitations.

## Actual inspection

The short GANLIB-only inventory inspected map 8 (`map-003.portable`) of
`validation/artifacts/d4a-corrected-material-rank2-series-from-map5-20260922`.
Maps 6 and 7 were not independently inventoried in this bounded review.
Evidence is in
`validation/artifacts/d4a-neutron-balance-readiness-20260923/map8_inventory.log`;
the disposable `inventory.f90` and executable are alongside it. Compilation used
the existing GANLIB archive and the iterative Makefile's strict flags; compile
and each of 23 inventory processes had a 10-second timeout. No Dragon library
was linked. All six inspected XSM files have matching before/after SHA-256 hashes
in that log. The inventory is not a complete physical-XS validator.

| Saved location | Observed map-8 content | Meaning/scope |
| --- | --- | --- |
| `candidate_radial.xsm/TRACK[p]` | Each of 3 planes: 132 regions, 144 unknowns; `KEYCUR$MCCG=133..144`; `BC-REFL+TRAN=1..12`; six `ALBEDO=1`; `ICODE=-1..-6` | Twelve outer-boundary unknowns, with identity boundary pairing and no group-albedo substitution |
| `TRACK[p]/V$MCCG`, `NZON$MCCG` | 144 REAL32 weights; last 12 all 1.25068164; boundary material tags `-1..-6` repeated | Stored numerical surface weights and albedo lookup indices, not an assumed geometrical face area |
| `candidate_radial.xsm/FLUX[p]/SPOT-R64/{FLUX,SOUR,QFISS}` | Each list has 370 items of 144 REAL64 values, all finite, for all 3 planes | Authoritative returned flux and frozen-source receipt; do not substitute legacy REAL32 mirrors |
| `candidate_radial.xsm/FLUX[p]` | `LEAK1D64` has 370 REAL64 values; `SYSTEM[p]/SPOT-L1-RAW=1` | The axial loss used by this radial solve, applied separately in REAL64 |
| `candidate_snapshots.xsm/FLUX[1]/SPOT-R64` | `QFISS` still present | Returned feedback lifecycle retains the frozen source |
| `closed_snapshots.xsm/FLUX[1]/SPOT-R64` | `QFISS` absent | Closure deletes authority QFISS and relabels RHO; this is not the source object for replaying the preceding radial equation |
| `closed_axial.xsm/FLUX64` | 370 items of 2772 REAL64 values, all finite | Full stored axial unknown vector, not only cell scalar flux |
| `initial_axial_track.xsm` | 132 radial regions, 3 floors, `LL4=1188`, `LL5=528`, eight directions; `AREA2D`, `VOL1D=(50,50,50)`; `NCODE=(1,1)`, `ZCODE=(0,0)` | 132 × 4 signed face-current values and vacuum end boundaries in the current axial solver |

The source lifecycle conclusion also follows directly from
`src/SPOR64_B2W.f90:375`: closing deletes authoritative QFISS, updates child RHO,
and explicitly distinguishes the preceding fixed-source equation from the new
closed state. The table's lifecycle spot checks were plane 1; source code
performs closure for every plane.

## Radial boundary data: available, but not independent incoming/outgoing tallies

`src/MCGFFIR.f:78` takes incoming track values from the boundary source; at
line 125 it accumulates outgoing RP/RM times track weights into `KEYCUR`.
`src/MCGFST.f:93` divides those boundary entries by `V$MCCG` weights.
Thus saved `FLUX[KEYCUR]` is a normalized outgoing sweep unknown, **not Jnet**
and not an independently stored pair of incoming/outgoing angular tallies.
The final field also undergoes solver acceleration/rebalancing.

`src/SPOR64_A8.f90:684` forms the incoming boundary source as
`alpha[s] * outgoing[BC(s)]`. `src/MCGSIG.f:60` defines the albedo lookup and
optional group substitution. In this archive, every alpha is one and BC is
identity, so the declared conservative boundary condition implies zero net
radial boundary loss. Internal symmetry reconstruction does not introduce an
external loss. This is a **BC integral identity**, not a measurement proving
that every numerical ray/interface conserves particles.

The normalization link is explicit, with no guessed factor:
`src/SPOR64_B2B.f90:392` reads `V$MCCG`, and line 412 copies its final 12 values
directly into `surfac32`; `src/SPOR64_A9.f90:390` uses that exact array in the
global boundary term `(1-alpha)*FLUX[KEYCUR]*surfac32`.
No extra 2, 4, angular factor, or geometrical-area replacement is warranted.
For this identity-paired case this agrees with
`sum_s W_s*(jplus_s-alpha_s*jplus_BC(s))`. No generalization to arbitrary
nonidentity pairings or different track conventions was tested here.

The saved schema has no complete angle-resolved radial boundary history or
internal region-to-region face currents. `SOUR` is not such an independent
boundary record: `src/SPOR64_A9.f90:172` initializes slice 4 from the frozen
source, but line 281 replaces it with slice 8 after off-group source assembly.
The published terminal `SOUR` therefore includes the last off-group source
and is not generally equal to `QFISS`; `src/SPOR64_B2R.f90:241` explicitly
retains QFISS separately. Therefore an independent **local** radial current-divergence
test, or a sweep-level incoming-versus-outgoing conservation test, is not ready
from these saved fields alone. Do not reconstruct those missing currents from
the balance residual.

## Smallest calculable follow-up, not calculated here

For each returned plane and target group g, a faithful fixed-source **discrete
operator** residual can use the saved data without `RADIAL-OP64`:

```text
F_g = sum_i V_i * QFISS(i,g)
M_g = sum_i V_i * [(Tcorr(i,g)-Sself,corr(i,g))*u(i,g)
                   - sum_(h != g) S(i,h->g)*u(i,h)]
Z_g = sum_i V_i * LEAK1D64(g)*u(i,g)
B_g = sum_s W_s*(jplus(s,g)-alpha(s)*jplus(BC(s),g))  [this case: 0 by BC]
R_g = M_g + Z_g + B_g - F_g
```

Addresses: `u` and `jplus` are the returned authoritative `SPOT-R64/FLUX`;
`V`, material indices, and flux/current indices are in returned `TRACK[p]`;
`Tcorr`/`Sself,corr` are `SYSTEM[p]/GROUP[g]/{DRAGON-TXSC,SPOT-S0-PHYS}`;
off-group S comes from `MICROLIB2[p]/MACROLIB/GROUP[g]/SCAT00`, decoded with
`NJJS00/IJJS00/IPOS00` exactly as `src/SPOR64_A9.f90:205` does. Selected group-1
records were inventoried; all-group XS packing/finiteness still needs explicit
validation if this calculation is authorized later.

`QFISS` is the saved source formed from **parent projected Ba and parent 1/k**,
not from returned u or returned k (`src/SPOR64_B2N.f90:413`). Use the returned
authority receipt, not the closed archive's relabelled RHO or REAL32
`SPOT-QFISS` mirror. Use the radial solve's saved `LEAK1D64`, not newly returned
axial leakage. This is the forward radial fixed-source equation, not a claim
that the full coupled eigensystem has converged.

Important dependence: `src/SPOR64_A9.f90:236` calls `FLUBAL64`; lines 383–449
form and solve the group-integrated rebalance system and scale **all** unknowns.
A small R_g would establish archive/operator consistency with a solver that
already enforces that balance; it is not an external or wholly independent
physical conservation validation. Existing `SPOASM` radial diagnostics are
even less independent: `src/SPOT_LEAKAGE.f90:108` defines d_perp from q/u,
and `src/SPOASM.f:520` accumulates `V*d_perp*u`. Reusing that expression cannot
independently verify its own inferred leakage.

## Cross-section terminology and axial scope

The library procedure uses `CTRA APOL` and TONE self-shielding
(`data/SpotD4Snap.c2m:100`, `:187`). Saved macrolib group 1 includes `NTOT0`,
`SIGW00`, `TRANC`, compressed scattering, `NFTOT`, `NG`, and nonzero multiplying
reaction channels such as `N2N`/`N3N`. These are processed library data, not a
newly verified raw reaction balance. `src/ASMDRV.f:223` subtracts transport
correction from both total and self-scattering before saving
`SPOT-S0-PHYS` at line 314. “PHYS” here means before imposed axial leakage,
**not before APOL/TONE/transport correction**. M_g, including any multiplicative
scattering convention, must be called operator net removal, not unverified
capture-plus-fission absorption. No reaction-channel reconstruction was done.

Axial current is genuine discrete 1D SN output: `src/SPOT1P64.f90:488` sums
`w*mu*face` to modal currents, and line 506 reconstructs radial-region currents
in the fixed rank-2 basis. It is not obtained from q/u. Its saved index is
`LL4+(i-1)*(NFLOOR+1)+face`; `src/SPOLEAK.f90:178` reads this REAL64 slot.
`src/SPOT_LEAKAGE.f90:75` calculates floor leakage as
`sum_i AREA_i*(Jright-Jleft) / sum_i AREA_i*height*phi`.

The subsequent [saved axial-current audit](d4a_axial_current_result.md) checks
current telescoping, vacuum-end outflow, and the saved leakage coefficient:
all 1110 REAL64 coefficients reproduce bit for bit, without clipping signed
layer inflow. A separate check could examine
the projected axial discrete equation, but that operator contains radial
coefficients inferred from the previous radial balance. It cannot by itself
validate the full 3D local balance, missing radial interface currents, the POD
approximation, or original nuclear reaction-channel absorption. Full axial
face-angle arrays are transient; a left-boundary angular block is retained
at `LL4+LL5+1` (`src/SPOF64.f:180`),
which does not replace complete angle-resolved currents at every interface.

**Disposition:** field readiness and limitations established for map 8.
The later [radial budget](d4a_radial_balance_result.md) and
[axial current](d4a_axial_current_result.md) diagnostics provide numerical
archive/operator consistency results, retaining the dependence/BC distinctions
above. Neither introduces a tolerance or changes convergence/accuracy acceptance.
