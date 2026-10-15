# CLOSED/9 final outputs and CE comparison — 2026-09-29

**Outer iteration: VALID_MET. Final saved-output replay: PASS. CE k accuracy: FAIL.**
This is the repaired D4-A component, fixed rank 2, alpha=1, 370 groups,
132 radial regions and 12 axial cells in three physical zones; not IRENA full core.

The user approved saved-state extraction and comparison after the ninth-map
review. Existing GREP/SPORATE and sealed pin/current readers were reused with
10-second per-invocation caps. No new transport, tenth map, CE simulation,
compilation, threshold change or empirical parameter was introduced.
All original inputs and new evidence manifests verified; prior sealed reviews
and controller status were preserved.

## Results from the same CLOSED/9

| Quantity | Result |
| --- | --- |
| Original outer defects Rrho / Rleak / Ra | 2.91194120e-8 / 2.98318115e-7 / 3.64179298e-7; all <=5e-7 |
| Nine-map lineage and final k/nu-fission replay | D4A-CORRECTED-ACCEPT OVERALL PASS |
| Existing CE static, runtime and statepoint replay | PASS; no CE rerun |
| SPOT saved k64 / CE k | 1.2847437576547476 / 1.3030848883933903 |
| Signed reactivity difference | −1095.56180284 pcm; original absolute allowance 558.65110508 pcm: FAIL |
| Source-normalized outward leakage, SPOT / CE | 0.07726458180671242 / 0.062301665075948254 |
| Leakage excess | +1.49629167308 percentage points |
| 651 pin-zone nu-fission shares, max / RMS relative difference | 2.04726203% / 0.90509201%; descriptive only |
| Bottom / middle / top SPOT shares | 0.261912626372 / 0.481646834853 / 0.256440538775 |

The k allowance is the existing 500 pcm + 3 sigma rule, with CE sigma
19.55036836 pcm. The signed difference is 1e5(1/k_CE − 1/k_SPOT).
Pin/floor quantities are globally normalized nu-fission fractions, not thermal
power; they include CE sampling noise, without a covariance-based shape verdict.

All 1110 stored leakage coefficients reproduce bitwise; 740 shared-face
integrals agree exactly. Negative end region/group currents remain in 1642
entries, with source-normalized negative magnitude 5.99977763e-9; none is clipped.
Small global negative magnitude is not an eigenvalue perturbation bound or a
resolution of the angular-sign warning. Currents use REAL64, while the saved
fission normalization and rates use the declared REAL32 flux mirror with
REAL64 accumulation; this is not a full-3D balance certificate.

## What this establishes, and the next discriminator

From map 6 to map 9, reactivity changes only +0.06317529 pcm and leakage excess
changes −0.00000142057 percentage points. The large CE discrepancy persists
after the original coupled stopping criterion is met. More Picard steps are
therefore not the current priority; this observation is not a rigorous error bound.

Existing isolated map-6 experiments show a +39.23943 pcm frozen-radial 12-to-24-cell
sensitivity and 0.02254 pcm tighter cold/warm sensitivity. These are not additive
corrections or map-9 error estimates. The unchanged axial macrolib connects this
state to the existing [scattering audit](../d4_reference/d4a_scattering_data_audit.md):
Fe56 G25/G26 SCAT00/SIGS00 differences are upstream of POD, but their cause and
contribution to k are not yet quantified.

The next cheap discriminator is read-only matching of the D4 library lineage
and scattering semantics, before choosing a same-data reference. Angular,
coupled mesh and POD-error experiments need separately declared compute budgets.
No map 10 is authorized; no fully validated production release is claimed.

## Preserved evidence

All paths below are under `validation/artifacts/`; manifests verify from their
own directories. The final comparison input manifest also binds source identities.

| Directory | Manifest SHA-256 |
| --- | --- |
| d4a-scattering-mesh12-map9-final-observables-20260929 | observables.sha256: `0dc169c548037cb37a0941c9174ed71e1b5c8a9fa67e3685d407a7fa34e4a46f` |
| d4a-mesh12-map9-pin-diagnostic-20260929 | result.sha256: `7cdfe528db142866662f9a10d8cefc677233bd5e2cfe29d40928d4e553e81493` |
| d4a-mesh12-map9-current-diagnostic-20260929 | result.sha256: `7ce39fc489a164b1c15f831ad8e420ec582fec2b86dec960685cd89b096589da` |
| d4a-mesh12-map9-final-comparison-20260929 | result.sha256: `6e36221830d388920bca31645e30105f1bb5666571bf1270d690ad382f577c40` |

The source CLOSED/9 result manifest is
`644a99cc7832fbcb9b1efa9b75b56b8cbf9fb430c1b07d245833c79c940ce16c`.
See the [original convergence review](d4a_scattering_mesh12_picard_map9_result.md)
and [generated nine-map report](../d4_reference/d4a_evidence_report.md).
