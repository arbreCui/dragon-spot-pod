# Repaired D4-A delivery acceptance — 2026-09-29

The target is a physically consistent, reproducible **D4 component** calculation,
not an IRENA full-core release. Numerical convergence, physical/discretization
accuracy and reproducibility are separate requirements. No empirical coefficient
or weakened threshold is permitted.

Separately approved map 9 ran Sep 28 21:23:56–Sep 29 01:33:41 Asia/Shanghai,
with unchanged 32400/600/120 s one-attempt caps, taking 14984.975 s.
CLOSED/9 is independently verified VALID_MET: defects are
2.91194120e-8 / 2.98318115e-7 / 3.64179298e-7, all <=5e-7.
Rrho increased but passes; leakage/flux defects decreased 72.22%/59.76%.
All nine map lineages and independent replays pass. Subsequently authorized
saved-output extraction and full final replay pass; the separate CE k comparison
fails its unchanged criterion. Monitoring is paused;
no retry or automatic tenth map occurred. No physics parameter or threshold changed.

| Requirement | Current evidence | Remaining work |
|---|---|---|
| Corrected material and fixed POD | Three admitted 370-group, 132-region snapshots; fixed rank 2; original evidence linked to repaired CLOSED/0 | Complete for this input epoch; not a rank-error bound |
| Declared scattering | `cf469c8` repair, clean-source build and short kernel tests pass | Not by itself a physical accuracy result |
| New initial state | Three repaired TYPE-S responses; B2I CLOSED/0 and B2J independently verified | Complete; not convergence |
| Coupled iteration | Nine 12-cell maps independently replayed; CLOSED/9 first VALID_MET; old three-cell maps 1–2 retained separately | Original Rrho/Rleak/Ra AND gate `<=5e-7` met; not a physical accuracy certificate |
| Final observables | CLOSED/9 k and three normalized nu-fission shares extracted and sealed with existing read-only GREP/SPORATE | Complete; no transport or empirical conversion |
| Whole-chain final replay | Real CLOSED/1–9 lineage, FINAL-RESIDUALS and FINAL-K-POWER replay: OVERALL PASS | This is not a physical accuracy certificate |
| Physical accuracy | Existing CE provenance/statepoint replay PASS; k comparison FAIL: −1095.56180 pcm versus allowance 558.65111 pcm. CLOSED/9 leakage excess +1.49629 percentage points; pin-zone max/RMS nu-fission differences 2.04726%/0.90509%, REPORTED_ONLY | Isolate operator/data/discretization differences; mesh/angle and POD truncation accuracy remain unestablished |
| Direct flux / thermal-power reference | Saved CE statepoint has exactly one tally: 651 fuel-cell bins, total nu-fission, 200 realizations; no flux or heating score | Direct scalar-flux and thermal-power comparisons remain unverified; do not relabel nu-fission or invent a conversion |
| Angular/boundary signs | CLOSED/9 has 1642 negative end region/group currents; source-normalized negative magnitude 5.99978e-9. All 1110 leakage rows and 740 shared faces reproduce exactly | Cause remains open; small signed integral is not an eigenvalue-error bound; do not clip or treat MET as resolution |
| Reproducibility | Clean-source build passed; real repaired map-1 standalone package and relocation replay pass | Assemble the complete new initial-state/provenance/source release; old tar is not the repaired release |

The [final comparison record](d4a_mesh12_map9_final_comparison_result.md) links
the independently checked output, pin/current and CE evidence.

The existing tools have distinct scopes. `VALID_MET` certifies the three-defect
iteration gate only. `D4A-CORRECTED-ACCEPT OVERALL PASS` covers the archived
lineage, replayed map/gate and reproduced k/normalized nu-fission outputs; that
script does **not** run the independent CE comparison or certify angular
positivity, mesh/rank error or cold/warm reproducibility. The separate CE
comparison checks the declared k criterion and reports shape differences;
its PASS is not a pin-power accuracy qualification. None of these labels alone
means the complete physical validation target is finished. Final release must
state the unresolved rows above rather than turning a narrower PASS into a
broader claim. This clarification adds no numerical gate or changed tolerance.

The existing SPOGBAL output is also diagnostic-only: it uses the REAL32
`FLUX`, `K-EFFECTIVE` and `RADIAL-OP` mirrors with REAL64 accumulation, not the
entire REAL64 authority chain. Its signed global reduction permits cancellation
and is not an independent full-3D conservation certificate or the outer AND gate.
The source matches repair commit `cf469c8`; no active implementation was changed.

A repository-only saved-reference inventory on Sep 28 found no replacement
for the missing direct flux/heating reference. The other saved OpenMC input
under `level4-rank2-fixedpoint-comparison/openmc` is a 24-cell concentric-ring
model with six reflective lateral surfaces and only three four-bin nu-fission
tallies. It is not the current 3267-cell D4 geometry with six white lateral
surfaces and 651 fuel-cell tally bins; neither tally input contains flux or
heating. The D4 XML hashes match the frozen source manifest. Historical rung
descriptions are not archived, geometry-matched D4 flux evidence. This check
does not rule out data outside this repository and does not authorize new
transport; the reference gap remains open.

The bottom-angle audit used existing CLOSED/1 data only: a 0.814-second binary
export and 0.083-second analysis, with unchanged source/runtime/input hashes.
Nonzero incoming samples were retained (264 entries, maximum absolute
`3.496498982434546e-30`), not rounded to zero. Bottom-current signs agree at all
region/group locations, ruling out a simple reader sign error; this does not
isolate POD, diamond spatial or angular/source error. Evidence:
`validation/artifacts/d4a-mesh12-map1-bottom-angle-audit-20260926/README.md`.

**Overall: INCOMPLETE.** Nine fine-mesh maps now establish the original coupled
iteration gate, but not final accuracy. Two old three-cell maps remain separate. Superseded defective
maps 1–11/MET cannot fill these gaps. The old three-cell
map 2 finished at 2026-09-25 03:10:32 Asia/Shanghai in 18183.981 seconds,
within its approved caps. Rrho/Rleak/Ra are 1.12978e-5 / 6.54934e-4 /
5.83029e-5, all NOT_MET. Independent checker/gate replay is byte-identical;
all result/input/parent/runtime manifests verify unchanged. No retry or map 3
occurred, and the completed-run monitor is paused. The subsequently authorized
180-second 3-to-6-cell diagnostic ended in 134.49 seconds: 3-cell passed,
6-cell reached its 90-second cap. The user later approved a separate fresh
300-second six-cell attempt: it completed in 97.35 seconds with unchanged
inputs and thresholds. The frozen-radial 3-to-6 physical reactivity shift is
**+784.49 pcm**, independently checked. The separately approved 12-cell run
then completed in 351.97 seconds; its 6-to-12 shift is **+156.82 pcm**,
19.99% of the preceding increment. This establishes decreasing increments
in this frozen-radial study, not an error bound, coupled convergence or final
accuracy. No further mesh/transport run is authorized by these experiments.
The independent checker's old/new axial storage-size comparison is now fixed
in source and verified by 49 synthetic cases plus unchanged real map-1/2
replays. The separately sealed fine-mesh runtime now includes this checker;
the old runtime remains untouched. The
12-cell seed was prepared with 4.068 seconds of SPOLEAK-only processing and
checks; its raw guesses correctly failed B2I. The separately approved radial
refresh subsequently completed at 19:11 on Sep 25 (7807.364 s radial, 3.117 s
postprocessing). The true fine-mesh CLOSED/0 is now independently verified:
29 result/15 input entries pass, and B2I/B2J replay is byte-identical. The user subsequently approved one map with
32400/600/120 s caps (total 33120 s); it started at Sep 25 21:27:52 Asia/Shanghai,
with overall deadline Sep 26 06:39:52. It completed at Sep 26 01:54:13 in
15980.988 s, with independently verified CLOSED/1 / NOT_MET. Rrho/Rleak/Ra are
2.04332544e-3 / 1.13691143e-1 / 7.19512903e-3; all original manifests pass,
and independent checker/gate replays are byte-identical. Same-state pin-zone
and signed-current diagnostics are reported without an accuracy PASS.
The user then separately approved one second fine-mesh map with the same
32400/600/120 s caps. It started at Sep 26 02:27:05 Asia/Shanghai, with total
deadline 11:39:05. It completed at 06:32:28 in 14722.078 s, producing CLOSED/2
with defects 6.39763082e-4 / 1.49518030e-2 / 1.76807841e-3, all NOT_MET.
Independent checker/gate replay and manifests pass; two-map lineage passes
while final acceptance correctly refuses. Managed session exit 0 was observed;
OS process-tree reinspection is permission-limited, and monitoring remains paused.
The user subsequently approved one third map with the same single-attempt caps;
it started at Sep 26 20:01:50, with overall deadline Sep 27 05:13:50 Asia/Shanghai.
B2J CLOSED/2→PROJECTED/3 passed; CLOSED/3 completed at Sep 27 00:11:03 in
14953.590 s, with defects 2.01220735e-4 / 1.84425807e-3 / 5.72090075e-4.
These decrease by 68.55% / 87.67% / 67.64% but remain NOT_MET.
Independent replay and manifests pass; all three map lineages replay while
final acceptance correctly refuses. Known launch PID/PGID entries are absent
and the complete process census contains no Dragon. The monitor is paused.
No retry or automatic fourth map occurred in that third-map run. A separately
approved fourth map subsequently completed at Sep 27 05:13:37 in 14690.031 s:
Rrho/Rleak/Ra = 5.69383149e-5 / 3.72526523e-4 / 1.84938299e-4, all NOT_MET.
Independent replay/manifests and four-map lineage pass; final acceptance
correctly refuses. The subsequently approved fifth map completed at Sep 27
21:01:11 in 14742.366 s, with Rrho/Rleak/Ra =
1.19425845e-5 / 5.49844341e-5 / 6.04891652e-5, all NOT_MET.
Independent replay/manifests and five-map lineage pass; final acceptance
correctly refuses. The subsequently approved sixth map completed at Sep 28
03:00:54 in 14576.428 s, with defects 5.20952972e-7 / 1.63843853e-5 /
1.96005233e-5. Independent replay/manifests and six-map lineage pass; final
acceptance correctly refuses NOT_MET. The separately approved seventh map then
completed and was independently reviewed as described above.
Matched runtime/bootstrap identities are registered, and actual preflight passes; the runner
also binds the mesh TRACK and continuation runtime. Both cross-mesh combinations
are rejected before output. Fine-mesh CLOSED/8 has no coupled MET and therefore
cannot pass final acceptance. Four short software suites pass
74 test methods (synthetic orchestration, not physical validation). See the
[fine-mesh map-8 result](d4a_scattering_mesh12_picard_map8_result.md),
[fine-mesh map-7 result](d4a_scattering_mesh12_picard_map7_result.md),
[fine-mesh map-6 result](d4a_scattering_mesh12_picard_map6_result.md),
[fine-mesh map-5 result](d4a_scattering_mesh12_picard_map5_result.md),
[fine-mesh map-4 result](d4a_scattering_mesh12_picard_map4_result.md),
[fine-mesh map-3 result](d4a_scattering_mesh12_picard_map3_result.md),
[fine-mesh map-2 result](d4a_scattering_mesh12_picard_map2_result.md),
[fine-mesh map-1 result](d4a_scattering_mesh12_picard_map1_result.md),
[bootstrap result](d4a_scattering_mesh12_bootstrap_result.md) and
[mesh-attempt result](d4a_scattering_axial_mesh_result.md).

The same-mesh cold/warm axial comparison also differs by **0.48144 pcm**
despite both satisfying the declared inner stopping tests. This is a numerical
repeatability warning, not a certified error bound or evidence that the outer
gate is impossible. It must be resolved before final accuracy is claimed;
neither the original outer gate nor any physical parameter has been changed.

A separate [12-cell map-6 terminal repeat](d4a_map6_axial_repeat_result.md)
completed in 1.78 seconds with the same frozen operator and original inner
thresholds. It moved k by +0.01790 pcm and modal flux by 5.61237e-7. This is
an inner-repeatability diagnostic, not an additional coupled map or a measured
error floor; the running chain and original artifacts are unchanged.

## Current integration work

Post-map-2 delivery regression (2026-09-25): all six selected transport-free
suites pass in **37.75 seconds**: 62 unittest cases across final-observables,
repaired acceptance, packaging, export and map preflight, plus the existing
CE-receipt synthetic suite. No real Dragon/OpenMC transport, compilation or
runtime replacement occurred. Test/implementation hashes were checked before
and after. Evidence: `validation/artifacts/d4a-delivery-regression-20260925`.
This is a targeted software regression, not a rerun of all `spot-fast` tests
and not evidence of a physical fixed point or accuracy acceptance.

`run_d4a_corrected_final_observables.sh --repaired-runtime` explicitly selects
the sealed repair epoch. It verifies bootstrap/runtime/final manifests, requires
MET, uses only the existing GREP + SPORATE on private copies, and checks unchanged
inputs afterward. Its output contract stays at five files plus the manifest.
Twelve synthetic tests and the original observable-replay tests pass, including
exact manifest-name coverage (a lookalike filename cannot replace `gate.log`). Real
repaired CLOSED/1 is refused with `final map is not VALID_MET` before output or
process launch. No production final extraction ran. One initial synthetic
round-trip hit a 3-second test cap; subsequent suites pass with a 5-second
synthetic-process cap. No physics solve or production cap was changed.

`check_d4a_corrected_acceptance.sh` now accepts an explicit pair of
`--repaired-runtime` and `--repaired-bootstrap` arguments. The positional BUILD
remains original snapshot/rank provenance, not the new initial state. The new
branch pins both repair manifests, links the unchanged snapshots/basis/macrolib,
radial tracking and contract, and keeps the separately verified repaired axial
TRACK fixed throughout the map chain. It replays the original one-map and gate
checkers and verifies all map/parent/runtime manifests before and after reading.
The legacy entry is unchanged. The CE wrapper forwards the same explicit pair;
no CE runtime, material, uncertainty or accuracy criterion changed.

Fourteen isolated synthetic tests pass, including a complete MET extraction/
replay, two-map order and checker modes, NOT_MET, false saved PASS records,
wrong parents, changed material/geometry, different runtime, lookalike manifest
names and continuation after the first MET. The comparator's synthetic suite
also checks CLI forwarding, missing-option refusal and rejection propagation.
No real transport/CE run is part of these tests.

The actual repaired CLOSED/1 replay passes REPAIR-EPOCH, MATERIAL, SNAPSHOTS,
RANK2, CLOSED0 and MAP-REPLAY. Overall acceptance correctly exits **1** because
there is no final VALID_MET or final observable set. It launches only the two
GANLIB-only checkers, not Dragon or OpenMC. Logs and input/source identities are
under `validation/artifacts/d4a-repaired-acceptance-check-20260924`.
This is prefix verification and a real refusal test, not final acceptance.

The existing freezer now has the same explicit `--repaired-runtime` selection.
It accepts only a complete manifested repaired map, retains the original receipt
as `source_result.sha256`, materializes exactly seven parent links and copies the
nested runtime without hard links. It never runs a solver or edits the source.
The exporter accepts that exact nested-runtime inventory, verifies the retained
source receipt and still requires CONVERGED_MAP/VALID_MET. It now also checks the
original 5e-7 threshold and the three numerical defects, not only their PASS text.

Thirteen synthetic packaging tests and eight exporter tests pass, including the
legacy flat entry, preservation of NOT_MET, unsupported/unsealed nested files,
false PASS labels, changed thresholds and relocation with original synthetic
directories made unavailable. The actual map-1 package was independently moved
and rechecked using its own two GANLIB checkers. Both logs match the originals
byte for byte; all 51 portable manifest entries and 48 original receipt entries
verify. All 48 copied original files have distinct inodes, with no remaining
symlink. Its original real map/parents were left in place to protect active map 2;
physical source-inaccessibility was exercised only in the synthetic test.

The relocated real package remains **NEXT_MAP_PARENT_ONLY / NOT_MET**. The full
lineage prefix replays, while both final acceptance and JSON/power export reject
it; no rejected export directory is created. Evidence and the retained package:
`validation/artifacts/d4a-repaired-packaging-check-20260924/relocated-map1`.
Portable `result.sha256` hash:
`9173ab41db0e94d1ae438a2d39ae6ec2db157c1d2f8ac23d8b08961b9836dad4`.
Its retained source receipt still hashes to
`d45a0ff43100b0f9ec9ce5be693650bcf771e30eb9577d56cb7fa309d943f7ed`.
This proves local map portability, not final convergence, cross-platform
portability, a complete clean-checkout distribution or physical accuracy.

CE k acceptance remains the declared `500 + 3*sigma_pcm` budget. Layer fractions
are normalized **nu-fission production**, not absolute thermal power. Pin/floor
shape differences have no predeclared acceptance threshold and remain
REPORTED_ONLY. A k PASS is not pin-power or IRENA full-core validation.

Read-only coverage check on 2026-09-27 confirms the above missing-reference row
against both the sealed tallies.xml and statepoint.300.h5 (one tally, score_bins
contains only nu-fission). The source generator at build_d4a_ce_reference.py
lines 608–613 requests exactly that score; the CE checker at
check_d4a_spot_ce_receipts.py lines 597–602 enforces it. The CE result receipt
remains 84b0a10c2ad4762344d205c601392b2017534e5e542a7e58c1500e8400a871fe;
its two results, source manifest and generated model inputs reverify unchanged.
This is a data-coverage finding, not a new physics threshold. Existing k,
global leakage and normalized nu-fission comparisons remain useful within
their own scope. No new CE run, fitted conversion, or claim that integrated
nu-fission uniquely determines the multigroup scalar flux is authorized here.

See [map-2 evidence](d4a_scattering_picard_map2_result.md),
[current handoff](d4a_final_validation_handoff.md), and
[repaired entry](D4A_CORRECTED_QUICKSTART.md).

## Historical pre-repair matrix and interface — not current acceptance

The following is retained only to explain the previous interface. Its old
runtime, maps and executable commands are not the repaired release path.

This is the minimum usability gate for the corrected-material D4-A SPOD
route. It adds no transport model, fitted coefficient, relaxation, damping or
rank choice. The gate only reads archived results, verifies their hashes and
replays the existing Ganlib-only checkers. Missing evidence is a failure.

The legacy-material D4-A map sequence is never an admissible substitute. Each
Picard map must be hash-linked to the corrected snapshot-derived rank-two
basis and to the immediately preceding corrected `CLOSED/n` pair.

| stage | required evidence | acceptance condition | current state (2026-09-22) |
|---|---|---|---|
| material epoch | reviewed audit, frozen and executed `rnr_cc`/`rnr_interpol` hashes | both hashes equal the reviewed corrected epoch | **PASS** |
| three snapshots | `admitted_snapshot_archive.sha256`, snapshot checker log | all hashes verify; `(NSNAP,NGRP,NREG)=(3,370,132)`; Ganlib-only PASS; three strict FLU terminals | **PASS** |
| fixed rank two | `d4a_rank2_admitted.sha256`, rank checker log | manifest binds the admitted snapshots; `NMODE=2`; stored diagnostics and Ganlib-only checks pass | **PASS** |
| bootstrap | `d4a_bootstrap_result.sha256`, B2I log | three TYPE-S refreshes; B2I commits the canonical corrected `CLOSED/0`; basis/track/macrolib hashes remain fixed | **PASS**: the existing three TYPE-S responses were admitted without recomputation; B2I committed `CLOSED/0` and the 14-file manifest verifies |
| Picard maps | ordered map directories, input/output manifests and lifecycle logs | exact `CLOSED/(n-1) -> PROJECTED/n -> RETURNED/n -> CLOSED/n` lineage; hashes chain from corrected `CLOSED/0`; live one-map checker replay matches its receipt | **PASS THROUGH `CLOSED/8`; NOT FINAL**: maps 1 through 8 are frozen and independently checked; map 8 is `NEXT_MAP_PARENT_ONLY` |
| final residuals | live replay of `check_convergence_gate` on final `closed_axial.xsm` | unchanged AND gate: `Rrho`, `Rleak`, `Ra` all `<=5e-7`; final classification `VALID_MET`; no later map | **FAIL**: map 8 has `(Rrho,Rleak,Ra)=(1.0492739930256789E-06,3.1031397842917180E-06,1.3106218716376795E-05)` and `VALID_NOT_MET` |
| final k and power | sealed read-only observables directory | manifest binds final axial state/track/macrolib; one `D4A-CORRECTED-K-EFFECTIVE`; three normalized bottom/middle/top `SPORATE NU-FISSION-FRACTIONS`; normal Dragon end | **FAIL**: no corrected `VALID_MET` map, final observables, or CE comparison exists |

Overall current classification: **`FAIL-CLOSED`**. The corrected offline
snapshot/basis construction, coupled bootstrap, and direct maps through
`CLOSED/8` are accepted.  Map 8 remains `VALID_NOT_MET`, so a corrected
coupled fixed point and final `k`/power/CE result have not been produced.

The former serial process ended after the complete map-5 raw outputs and
checks, before portable packaging and its series row.  The existing freezer
independently replayed and froze that map on 2026-09-22 without a transport
rerun.  See [the map-5 receipt](d4a_corrected_map5_result.md). The fresh serial
continuation completed and froze maps 6–8, then was interrupted in map 9.
Its incomplete `map-004.raw` does not count toward this matrix or serve as a
restart parent. See [the corrected map-8 receipt](d4a_corrected_map8_result.md).

## Short deterministic check

The checker never launches Dragon. Build the existing host-side read-only
checkers once, then list corrected maps in epoch order:

```sh
make -C validation/iterative check_one_map_xsm check_convergence_gate
sh validation/iterative/check_d4a_corrected_acceptance.sh \
  /absolute/path/to/corrected-build \
  /absolute/path/to/portable-map1 \
  /absolute/path/to/portable-map2 \
  /absolute/path/to/portable-map3 \
  /absolute/path/to/portable-map4 \
  /absolute/path/to/portable-map5 \
  /absolute/path/to/portable-map6 \
  /absolute/path/to/portable-map7 \
  /absolute/path/to/portable-map8
```

Because map 8 is `VALID_NOT_MET`, this current-state invocation must exit
nonzero at final-map acceptance.  Do not supply an observables directory
until the first frozen `VALID_MET` map exists.

The final observables directory has a deliberately small contract:

- `closed_axial.xsm`, `initial_axial_track.xsm`, and
  `initial_axial_macrolib.xsm` copied or linked from the final corrected map;
- `observables.x2m`, a read-only `GREP + SPORATE` deck;
- `observables.log`, containing `D4A-CORRECTED-K-EFFECTIVE`, one
  `SPORATE NU-FISSION-FRACTIONS` line and one normal Dragon end;
- `observables.sha256`, covering those five files.

This observables step evaluates no transport equation and cannot feed back
into the iteration.

After the ordered corrected map chain ends at its first `VALID_MET` state,
create that directory with the read-only runner:

```sh
TIMEOUT_SECONDS=10 \
  sh validation/iterative/run_d4a_corrected_final_observables.sh \
  /absolute/path/to/corrected-build \
  /absolute/path/to/final-map \
  /absolute/path/to/fresh-final-observables
```

The runner refuses a legacy basis/contract, a non-`VALID_MET` map, a broken
manifest, or an existing output directory. It copies the three frozen inputs,
runs only `GREP + SPORATE`, verifies that their hashes did not change, checks
one positive `k` and three nonnegative fractions summing to one, and then
publishes `observables.sha256`. It cannot run before a final accepted map
exists.

Final acceptance does not trust that self-signed listing.  It pins the
repository observables deck and bounded runner by SHA-256, requires the
repository Dragon to match the Dragon hash sealed by the corrected snapshot
bundle, reruns the same read-only extraction from copied XSM inputs, and
requires the two scientific records (`k` and three floor fractions) to match
the saved listing byte for byte.  `CHECKER_DIR` and `DRAGON_BIN` cannot replace
the repository paths.
