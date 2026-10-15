# Repaired D4-A Picard map 1 — 2026-09-24

**Independently verified: CLOSED/1, VALID_NOT_MET.** The repaired implementation
completed a full online radial → axial → leakage-feedback map. This is a valid
iteration result, not a coupled fixed point or a final accuracy result.

## Result and unchanged gate

Logged REAL64 eigenvalue: **1.2719027660185727**. The parent seed was
1.2718148126934201; neither number is a final converged eigenvalue.

| Coupled defect | Independently reproduced value | Gate | Result |
|---|---:|---:|---|
| Rrho | 5.4371895350291410e-5 | 5e-7 | NOT MET |
| Rleak | 4.7850057108391490e-3 | 5e-7 | NOT MET |
| Ra | 2.2933216671981128e-4 | 5e-7 | NOT MET |

All three must pass. Dleak=1.3167894255531392e-5 is diagnostic only.
The maximum relative out-of-span diagnostic is 7.0690177866573997e-8
(group 332, plane 1); it uses a different norm and is not evidence that
rank error is smaller than the outer defects or that rank 2 is sufficient.
These are the first repaired coupled defect values: no contraction factor,
remaining iteration count, or comparison to superseded-runtime residuals is
claimed.

The axial solve passed its existing solver gates in 6 outer iterations:
EEXT=2.92894077e-7; EUNK=EINR=1.63279224e-6, each below the declared 2e-6.
This inner solve convergence does not imply the coupled AND gate is met.
The existing log warning disables scalar transport correction for the explicit
SCAT3 axial path, consistent with the documented repair; no new correction or
empirical parameter was introduced.

## Scope and time

One map was authorized, with radial/axial caps 32400/180 seconds and no retry or
automatic map 2. It started at **15:43:28** and finished at **20:41:26**
Asia/Shanghai on September 24. Total elapsed time was **17877.9010 seconds
(4 h 57 min 58 s)**, within the conservative 32580-second overall limit.
Solver logs record 17834 radial CPU seconds and 8 axial CPU seconds; these are
not wall-clock stage timings or future runtime guarantees. All observed owner,
watchdog and Dragon processes have exited; launch session 68853 returned zero.

## Independent completion verification

The calculation directory is
`validation/artifacts/d4a-scattering-picard-map1-20260924`.
The control/status directory is
`validation/artifacts/d4a-scattering-picard-map1-control-20260924`.

- The 48-file result manifest, 12-item pre-run input/deck manifest, 8-item input
  manifest, 6-item output manifest and 11-file runtime manifest all verify.
- The original CLOSED/0 manifest and its 29 entries verify unchanged, as do
  the separately pinned prepared-runtime manifest and the one-map script.
- Three ordered radial plane entries and normal radial/axial completion are
  present. Admission passed; B2J reports CLOSED/0 → PROJECTED/1 and rejects the
  epoch-mismatch negative test. B2W reports CLOSE PASS and CLOSED/1.
- The independent checker verifies the fixed POD package, live radial-operator
  change, radial positivity, canonical layout, defects and restart archive.
- GANLIB-only read-only replay of `check_one_map_xsm --reencoded` and
  `check_convergence_gate` exactly reproduces both original logs byte for byte.
  Fresh replay logs are in
  `validation/artifacts/d4a-scattering-picard-map1-review-20260924`.
  Rechecking the entire result manifest after replay also passes. No solver
  was rerun, and no sealed log or status was rewritten.

Result-manifest SHA-256:
`d45a0ff43100b0f9ec9ce5be693650bcf771e30eb9577d56cb7fa309d943f7ed`.
Closed axial SHA-256:
`3dc9f351a934d77286881976eb3f8fbf25f5fc570206726918abeb218f6703bf`.
Closed snapshots SHA-256:
`ca17798660af2e0c3c09caf580d49dd03be6db19a13e07f0821152cfe76dce01`.
Repaired Dragon SHA-256:
`873ad14272a2f0765d95e6de067194a01708ccf9aa88d58cd782049e6d331fef`.

## Stop boundary and separately approved continuation

Map 1 stopped after independent review, without an automatic continuation.
No rank, closure, alpha=1 or threshold change is justified by this single result.
Final CE accuracy, mesh convergence and IRENA full-core validation remain
unestablished; the completed CE reference must not be rerun.

Second-map preparation: the unchanged one-map runner passed
`--preflight-only` against this CLOSED/1 and the same repaired runtime. The
control files in `validation/artifacts/d4a-scattering-picard-map2-control-20260924`
reuse the previous wrapper, changing only the parent/result paths and parent
manifest pin. After the explicit second-map budget proposal, the user asked to
continue toward this month's delivery objective. **Map 2 started at 2026-09-24
22:07:28 Asia/Shanghai**, with radial/axial caps 32400/180 seconds and a
32580-second overall cap: deadline **2026-09-25 07:10:28**, plus bounded cleanup.
It runs in `validation/artifacts/d4a-scattering-picard-map2-20260924`.
B2J completed `CLOSED/1 -> PROJECTED/2`; map 2 subsequently finished normally
at **2026-09-25 03:10:32**, elapsed 18183.981 seconds. Independent replay passed;
all three defects decreased, but the classification remains VALID_NOT_MET.
See the [map-2 result](d4a_scattering_picard_map2_result.md).
The parent result-manifest hash above and prepared runtime hash remain fixed.
The completed-attempt monitor is now PAUSED. No retry or automatic map 3
is authorized. This does not change the completed map-1 evidence or classification.

## Read-only axial-leakage diagnostic — 2026-09-25

The repaired CLOSED/1 saved fields were read with the existing GANLIB-only
current and regional-rate tools, without compilation or transport. Independent
CSV arithmetic reproduces all **1110/1110** `SPOT-X-L` entries bitwise from
REAL64 face-current divergence divided by the matching integrated scalar flux.
All 740 shared-face integral pairs agree; there are no nonpositive regional
scalar fluxes or negative outward end currents. The maximum absolute group
telescoping difference is `8.673617379884035e-19`. The 134 negative layer/group
divergences represent net inflow, remain signed, and were not clipped.

Use the same state's total nu-fission rate F and logged k64 to form k*L/F,
where L is the sum of the bottom and top outward currents. This normalization
is fixed by the eigenvalue source, not fitted to the reference.

| Quantity | Repaired CLOSED/1 value |
| --- | ---: |
| Bottom outward current | `0.04524514482659269` |
| Top outward current | `0.044678789735861923` |
| Same-state F | `1.271902766237405` |
| Source-normalized leakage k*L/F | `0.08992393454698311` |
| Existing CE native leakage | `0.062301665075948254` |
| CE leakage standard error | `0.00012926235482585316` |
| SPOT minus CE, percentage points | `2.7622269471034855` |

The existing CE-only static/runtime/statepoint audit and original uncertainty
gate passed again, reading the unchanged 200-batch statepoint. No CE transport
was launched. Both full result manifests and all directly used SPOT inputs
and reader binaries verify unchanged before/after extraction.

This is **DIAGNOSTIC_ONLY / REPORTED_ONLY**, not final accuracy acceptance.
It replaces reliance on the superseded implementation's leakage observation
with evidence from the repaired chain, and supports the proposed isolated
3-to-6-cell axial comparison. It does not prove a mesh-only cause or separate
POD, closure and multigroup-processing effects. CLOSED/1 is still NOT_MET.
Current uses REAL64; F deliberately uses the existing REAL32 flux mirror with
REAL64 accumulation. CE's native standard error is not an uncertainty bound
on the SPOT model discrepancy. The short mesh comparison still needs its own
budget authorization and cannot modify the running second map.

Evidence: `validation/artifacts/d4a-scattering-map1-leakage-diagnostic-20260925`
contains the two raw reader logs/CSVs, `read_saved.py`, `summary.json`, and
input/result hash manifests. No active runtime, source, deck or gate changed.

## Read-only pin/floor production comparison — 2026-09-25

The existing saved-geometry reader independently re-extracted all three
repaired CLOSED/1 TRACK geometries. They are identical and reproduce the
217-pin mapping (25 fuel symmetry orbits). The 75 regional rates from the
same-state diagnostic above expand conservatively into 651 pin/floor records;
no extra factor of 12, renormalization, transport solve, or new coefficient is
used. Each floor's volume, nu-fission rate and global fraction are conserved
within the existing exact-rational division-roundoff checks.

The unchanged CE result is joined by unique `(floor, pin_index)`, not row
position. Global fractions are compared without rescaling:

| Floor | SPOT fraction | CE fraction | SPOT minus CE, percentage points |
| --- | ---: | ---: | ---: |
| Bottom | `0.2598476611303741` | `0.26192486508860197` | `-0.2077203958` |
| Middle | `0.48401761528677156` | `0.4849344596237941` | `-0.0916844337` |
| Top | `0.2561347235828542` | `0.2531406752876039` | `+0.2994048295` |

Across the 651 bins, maximum absolute global-fraction difference is
`2.9423516682287876e-5` (floor 2, zero-based pin 16); RMS is
`1.1306055347104993e-5`. To avoid mistaking these small global fractions for
relative pin errors, also report `100*(SPOT-CE)/CE`: the largest magnitude
is `1.8985918934555213%` (floor 3, pin 63). Summing the three original
fractions for each pin before applying that same relative-difference formula
gives a maximum magnitude of `0.7263850443841919%` (pin 16, SPOT below CE).
No layer-wise fitting or normalization was applied. Axially aggregated
differences can cancel and do not bound the local 651-bin differences.

These are **DIAGNOSTIC_ONLY / REPORTED_ONLY**, not thermal power or accepted
pin-accuracy results. The SPOT parent is still NOT_MET. CE raw-bin standard
deviations cannot provide normalized-fraction uncertainties without the
shared-denominator covariance; no statistical-significance claim is made.
Neither this comparison nor the leakage comparison isolates the cause of the
eigenvalue discrepancy. The pending axial-mesh comparison remains a sensible
single-variable next check, not an authorized production change.

Evidence is in
`validation/artifacts/d4a-scattering-map1-pin-diagnostic-20260925`; its
18-entry result manifest has SHA-256
`520b9d0ef6e00b333b271664c1da81ca9fe63ce5d7fb2bc2b5f32771df1691ca`.
Map 1's complete manifest, prior diagnostic and CE result receipts, and all
directly used inputs/tools verify unchanged. No compilation was performed.
