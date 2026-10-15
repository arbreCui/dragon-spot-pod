# Repaired D4-A: current minimal path

This guide selects the repaired scattering implementation explicitly. It is
not permission to start another calculation. The new 12-cell route has a verified
CLOSED/0 and a sealed matching runtime. Its first separately approved coupled
map completed at 2026-09-26 01:54:13 Asia/Shanghai, producing independently
verified CLOSED/1 / NOT_MET in 15980.988 seconds. Its separately approved second
map completed at 2026-09-26 06:32:28 in 14722.078 seconds, with independently
replayed CLOSED/2 / NOT_MET. The user then separately approved map 3, started
at Sep 26 20:01:50 and completed at Sep 27 00:11:03 Asia/Shanghai in
14953.590 seconds. Its CLOSED/3 is independently verified NOT_MET; no retry
occurred. Map 4 was then separately approved and started at Sep 27 01:08:47
Asia/Shanghai, with total deadline 10:20:47. It completed at 05:13:37 in
14690.031 seconds; CLOSED/4 is independently verified NOT_MET. A separately
approved map 5 ran at Sep 27 16:55:29–21:01:11 in 14742.366 seconds;
its CLOSED/5 / NOT_MET was independently reviewed.
A separately approved sixth map started at Sep 27 22:57:58 with the same
32400/600/120 s caps and total deadline Sep 28 08:09:58. It completed Sep 28
03:00:54 in 14576.428 seconds, producing independently reviewed CLOSED/6 / NOT_MET.
A separately approved seventh map ran Sep 28 03:43:21–07:53:17 with the same caps,
taking 14995.955 seconds. A separately approved eighth map ran Sep 28
14:56:15–19:02:56 with the same caps, taking 14801.073 seconds.
The user subsequently approved one ninth map with the same caps, started Sep 28
21:23:56 and completed Sep 29 01:33:41 Asia/Shanghai in 14984.975 seconds.
Independently reviewed CLOSED/9 / VALID_MET is the latest completed state:
Rrho/Rleak/Ra=2.91194120e-8/2.98318115e-7/3.64179298e-7, all <=5e-7.
Monitoring is paused. Final saved-output replay now passes; the independent
CE k comparison fails its original criterion. Physical validation remains incomplete.
No retry or automatic tenth map is authorized. The preserved
3-cell chain has CLOSED/2 / NOT_MET. This guide never grants compute permission. See the
[current status and handoff](d4a_final_validation_handoff.md).

Do not rebuild, replace executables, or change an active deck, contract or
parent state. Build/fast tests belong in a separate, inactive checkout.
The large sealed artifacts below are local release inputs, not files restored
by cloning Git. A complete distribution remains to be delivered.

## 1. Select the repaired inputs

From the repository root, set the existing local artifact paths:

```sh
A="$PWD/validation/artifacts"
ORIGINAL_SNAPSHOT_BUILD="$A/d4a-corrected-closed0-runtime-release-20260920"
REPAIRED_BOOTSTRAP="$A/d4a-scattering-mesh12-bootstrap-run-20260925"
REPAIRED_RUNTIME="$A/d4a-scattering-mesh12-picard-runtime-20260925"
REPAIRED_MAP1="$A/d4a-scattering-mesh12-picard-map1-20260925"
REPAIRED_MAP2="$A/d4a-scattering-mesh12-picard-map2-20260926"
REPAIRED_MAP3="$A/d4a-scattering-mesh12-picard-map3-20260926"
REPAIRED_MAP4="$A/d4a-scattering-mesh12-picard-map4-20260927"
REPAIRED_MAP5="$A/d4a-scattering-mesh12-picard-map5-20260927"
REPAIRED_MAP6="$A/d4a-scattering-mesh12-picard-map6-20260927"
REPAIRED_MAP7="$A/d4a-scattering-mesh12-picard-map7-20260928"
REPAIRED_MAP8="$A/d4a-scattering-mesh12-picard-map8-20260928"
REPAIRED_MAP9="$A/d4a-scattering-mesh12-picard-map9-20260928"
FINAL_OBSERVABLES="$A/d4a-scattering-mesh12-map9-final-observables-20260929"
```

The original build is snapshot/POD provenance only, **not the new parent**.
The repaired bootstrap and each repaired map have their own sealed lineage.
Expected identities are:

| File | SHA-256 |
| --- | --- |
| Repaired runtime `Dragon` | `873ad14272a2f0765d95e6de067194a01708ccf9aa88d58cd782049e6d331fef` |
| 12-cell runtime `runtime.sha256` | `af7069315a59ae6de9c0bd3edd6f497bf4dcaef1140917b4239c32bcff8da12b` |
| 12-cell bootstrap `result.sha256` | `805c06e1ec873809a890be3a90afe1b8c16ec57272c3eaa5c315aa8feb64b32f` |
| 12-cell map 1 `result.sha256` | `1834b479020c9ad4f8f9f2e590b7f697ad258e3002f78d5e70fc65d3fa9530fb` |
| 12-cell map 2 `result.sha256` | `f9df698dcedba06db69501e490e550053392d05f0a1b4bb6fee1f13142e5f5a4` |
| 12-cell map 3 `result.sha256` | `4b2a6d45e3d65998a739252ef694b98c88e8e20b7e1d7bdedc007f2ee8c0917d` |
| 12-cell map 4 `result.sha256` | `33e2e5a077f92c38be5185ec9171a9fecd0f0ace0cda56375a3d4cac034b47ef` |
| 12-cell map 5 `result.sha256` | `75c1167c5c618099f81664be90209680d89274370491cd52a16d8d7c7398f622` |
| 12-cell map 6 `result.sha256` | `77c3f6b33cc3d5ccfd72afcef9dc5eca4f3d58dbbe5a16d2ac7a71f2bae40d5b` |
| 12-cell map 7 `result.sha256` | `7a872842564406ad138d11448d06394be10c3568a0084a96fa8e5ba15dcdc498` |
| 12-cell map 8 `result.sha256` | `20337979601e98312f7882360cb196908d8752cfbab374aebe4f3562d74399e7` |
| 12-cell map 9 `result.sha256` | `644a99cc7832fbcb9b1efa9b75b56b8cbf9fb430c1b07d245833c79c940ce16c` |

The runtime differs from the preserved 3-cell package only in its independently
tested mesh-aware checker. Dragon, all physics decks and all thresholds are
unchanged. The two registered runtime/bootstrap pairs are not interchangeable;
the runner also checks the exact axial TRACK and continuation-runtime identity.

## 2. Safe preflight, without transport

The destination must not exist. This command validates the selected runtime
and completed parent, then exits without creating it or invoking a solver:

Use historical NOT_MET map 8 for this optional preflight diagnostic. The latest
map 9 already meets the iteration gate; proceed to saved-output validation, not
automatic map 10. This example is not new compute authorization.

```sh
sh validation/iterative/run_d4a_rank2_picard_map.sh \
  --repaired-runtime "$REPAIRED_RUNTIME" --preflight-only \
  "$REPAIRED_MAP8" "$A/mesh12-preflight-no-output"
```

Expected: `D4A PICARD PREFLIGHT PASS NO-TRANSPORT NO-OUTPUT`.
Do not remove `--preflight-only` to start a duplicate run. Real transport needs
a fresh directory, explicit radial/axial/total budgets and its bounded
one-attempt supervisor. The seventh 12-cell map completed in
`d4a-scattering-mesh12-picard-map7-20260928`; do not duplicate or restart it.
The separately approved map 8 completed in
`d4a-scattering-mesh12-picard-map8-20260928`; do not duplicate or restart it.
The separately approved map 9 completed in
`d4a-scattering-mesh12-picard-map9-20260928`; do not duplicate or restart it.
Map 10 requires another explicit budget.
The separately approved caps remain radial 32400 s, axial 600 s, post-check
120 s, total 33120 s. The old 180-second axial cap is not reused.
Do not invoke old default or series commands for the repaired chain.

## 3. Independently check a completed chain

Supply **every completed repaired map in epoch order**. Do not include an
unfinished map. The new 12-cell route has eight NOT_MET maps followed by MET map 9.
The following checks provenance, residuals and the separately sealed final observables:

```sh
set -- "$REPAIRED_MAP1" "$REPAIRED_MAP2" "$REPAIRED_MAP3" "$REPAIRED_MAP4" "$REPAIRED_MAP5" "$REPAIRED_MAP6" "$REPAIRED_MAP7" "$REPAIRED_MAP8" "$REPAIRED_MAP9"
D4A_OBSERVABLES_DIR="$FINAL_OBSERVABLES" sh validation/iterative/check_d4a_corrected_acceptance.sh \
  --repaired-runtime "$REPAIRED_RUNTIME" \
  --repaired-bootstrap "$REPAIRED_BOOTSTRAP" \
  "$ORIGINAL_SNAPSHOT_BUILD" "$@"
```

For this completed nine-map chain, the result is `D4A-CORRECTED-ACCEPT OVERALL PASS`.
Without the separately sealed observables, final acceptance still refuses. Never bypass a refusal.
The original AND gate remains `Rrho, Rleak, Ra <= 5e-7`.

The observed `D4A-CORRECTED-ACCEPT OVERALL PASS` is the scope of this
lineage/replay/observable checker, not the entire physical-validation target.
Independent CE comparison, mesh/rank accuracy, cold/warm repeatability and the
saved angular/boundary-sign warning remain separate requirements. Do not call a
converged export a fully validated release; see the
[current acceptance matrix](d4a_corrected_acceptance_matrix.md).

To replay the old 3-cell evidence instead, use the preserved matching paths
`d4a-scattering-picard-runtime-20260924`, `d4a-scattering-bootstrap-run-20260924`,
and maps `d4a-scattering-picard-map1-20260924` followed by
`d4a-scattering-picard-map2-20260924`. Both maps remain NOT_MET; never append them
to the 12-cell chain or pass the old runtime with the new bootstrap.

## 4. Only after the first independently verified repaired MET

The map-9 extraction has already completed; use its sealed outputs for replay.
The command below documents that operation, not a request to repeat it.
For a separately authorized extraction, set `FINAL` to that completed map and
`FRESH_OBSERVABLES` to a new directory.
The extractor reads saved fields only; it does not perform transport:

```sh
TIMEOUT_SECONDS=10 sh validation/iterative/run_d4a_corrected_final_observables.sh \
  --repaired-runtime "$REPAIRED_RUNTIME" \
  "$REPAIRED_BOOTSTRAP" "$FINAL" "$FRESH_OBSERVABLES"
```

Then repeat the complete lineage acceptance above with
`D4A_OBSERVABLES_DIR="$FRESH_OBSERVABLES"` set for that command. The existing
CE comparator takes the same repaired-runtime/bootstrap flags, the original
snapshot build via `--corrected-build`, and every map via repeated `--spot-map`.
Read the already completed [CE reference](../d4_reference/d4a_ce_production_result_20260923.md);
**do not launch CE again**. The independent k criterion remains the previously
declared `500 + 3*sigma_pcm` budget; pin/floor nu-fission differences are
REPORTED_ONLY, not thermal-power qualification or IRENA full-core validation.
Real MET and final observable replay pass. The completed CE comparison fails:
absolute reactivity difference 1095.56180 pcm exceeds 558.65111 pcm. Same-state
pin/leakage diagnostics and evidence identities are in the
[final comparison result](d4a_mesh12_map9_final_comparison_result.md).

## 5. Copy a completed map without live parent links

After the original completed map's manifest verifies, set `COMPLETED_MAP` and
a nonexisting `FRESH_PORTABLE_MAP`:

```sh
sh validation/iterative/freeze_d4a_corrected_map.sh \
  --repaired-runtime "$REPAIRED_RUNTIME" "$REPAIRED_BOOTSTRAP" \
  "$COMPLETED_MAP" "$FRESH_PORTABLE_MAP"
```

This copies parent links by value, retains the exact runtime and original
`source_result.sha256`, and replays the independent checker/gate. NOT_MET is
only `NEXT_MAP_PARENT_ONLY`, never a final result. Do not replace the parent
of an already running map. Real map-1 relocation/replay passed; this is local
map portability, not a complete release or cross-platform verification.

The [acceptance matrix](d4a_corrected_acceptance_matrix.md) tracks the remaining
delivery requirements. The [previous quickstart](D4A_CORRECTED_QUICKSTART_HISTORY.md)
is retained solely as historical evidence; its old execution route is inactive.
