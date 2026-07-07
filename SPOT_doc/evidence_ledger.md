# SPOT-POD evidence ledger

One row per accepted experiment run. All values from logs present in
this tree (`runs/<case>/<log>`), SHEM-370 library
(`draglibshem370_endfb8r1_v5p1.xsm`), Variant III′ binary
(branch `variant3-prime`) unless noted. Pre-SHEM-370 ("old-tree")
numbers are recorded only as historical context; they are not
citable references.

| run_id | date | deck / binary | K_iter1 | K_converged | errspo_final | status | notes |
|---|---|---|---|---|---|---|---|
| `d3_sanity` | 2026-07-03 | d3_sanity.x2m, eps=0 | 1.384711 | **1.411218** | 6.52e-05 | PASS | no-POD pincell baseline; bit-identical to 2026-05-13 run (LPOD gate intact after Variant III′) |
| `d3_sanity_pod` | 2026-07-03 | d3_sanity_pod.x2m, eps=1e-3 | 1.384703 | **1.411206** | 6.16e-05 | PASS | Δρ vs baseline −0.6 pcm; ERR_PRE flat ~2.0e-6 across ASM calls 1–3; ranks 1–3 of 5 |
| `d4a_baseline` | 2026-07-05 | d4a_het_baseline.x2m, eps=0 | — (stage-1) | **1.163271** (stage-1 final) | — | PASS | 132-region 1/12-hex 1-ring assembly, 5-T Doppler ladder; ~9.2 h wall; 0 warnings |
| `d4a_converged_ac` PASS A | 2026-07-07 | d4a_converged_ac.x2m, eps=0 | 1.163271 (=baseline, bit-identical) | **1.183264** | 8.71e-05 | PASS | converged=1 in 5 outer iters; axial leakage ≈ +2000 pcm |
| `d4a_converged_ac` PASS C | 2026-07-07 | d4a_converged_ac.x2m, eps=1e-3 | 1.163123 | **1.183274** | 8.15e-05 | PASS | converged=1 in 4 outer iters; **Δρ(A→C) = +1.03 pcm**; iter-1 offset −13 pcm washes out in the converged loop; ERR_PRE flat 1.39e-5 median across all 5 ASM passes; ranks 1–3 of 5 |
| `d4b_dry` | 2026-07-08 | d4b_dry_snapMring.x2m, single 750 °C snapshot | — | **K_TYPEK_radial = 1.367221** | — | PASS | 4-ring SnapMring end-to-end validation; +0.9 pcm vs 1-ring 1.367208 (ring refinement nearly neutral); all 3 gates pass; clean exit |

## Reference values (this tree)

- Pincell (D3): K_A = 1.411218 (no-POD), K_B = 1.411206 (POD 1e-3).
- 1-ring assembly (D4-A): stage-1 K = 1.163271; converged K_A = 1.183264,
  K_C = 1.183274, Δρ_AC = +1.03 pcm.
- Snap1Ring radial K_TYPEK ladder (from d4a_converged_ac.log):
  600 °C → 1.368250, 700 °C → 1.367513, **750 °C → 1.367208**,
  800 °C → 1.366938, 900 °C → 1.366500.
  The 750 °C value is the comparison point for the D4-B SnapMring
  dry run (old-tree value 1.365886 is superseded; ~+100 pcm SHEM-370
  library shift, same direction as the D3 pincell shift).

## Historical / superseded

- Old-tree (pre-SHEM-370, logs not on disk): pincell K_A = 1.410130,
  K_B = 1.409777; 1-ring stage-1 K_A/K_B = 1.163428 / 1.163425;
  radial K@750 = 1.365886. Superseded by the 366→370 migration
  (commit fe651a8) and the Variant III′ revision (commit 8ea0937).
- 2026-05-21 `d3_sanity_pod` attempt: killed externally mid-solve
  (empty .err); first completed in-tree POD run is 2026-07-03.
