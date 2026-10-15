# SPOT: Synthesis Proper Orthogonal Decomposition

SPOT implements an iterative **2D/1D + POD neutron-transport method**: online
2D radial fixed-source transport, a reduced 1D axial solve, and axial-leakage
feedback. The target is a self-consistent, independently validated solution.
The current release target is one D4-A component case, not an IRENA full core.

Current axial-material validation status (2026-10-11):
[SPOT progress report](validation/axial_material/SPOT_CURRENT_PROGRESS_20261011_2250.txt).

**Validation in progress — not a validated production release.** The repaired
implementation has completed nine 12-cell coupled maps (and preserves a separate
old three-cell chain). The original convergence gate and final-output replay pass;
the independent CE k-accuracy comparison fails. Old maps 1–11 and their MET result
cannot validate the repaired scattering implementation.

## Method

The [validation plan](SPOT_doc/validation_plan.md) defines a finite sequence of
error-isolation and accuracy/cost experiments. The [saved-evidence report](validation/d4_reference/d4a_evidence_report.md)
puts completed-map convergence, CE differences and total cost side by side;
regenerate it with `make spot-evidence` without compilation or transport.
Live execution status remains in the [current handoff](validation/iterative/d4a_final_validation_handoff.md).

For each energy group, form one volume-weighted radial POD basis from offline
snapshots and keep it fixed during the convergence study:

$$
W^{1/2}P_g=U_g\Sigma_g Z_g^T,\qquad
B_g=W^{-1/2}U_{g,1:r_g},\qquad M_g=B_g^TWB_g.
$$

The rank $r_g$ is the number of retained radial modes, a discretization order.
The implementation retains the full Gram matrix $M_g$; it does not assume
stored finite-precision basis vectors are exactly orthonormal.

Each outer step has three operations:

1. Reconstruct the current flux and solve the online radial fixed-source problems.
2. Assemble and solve the axial problem in the same fixed POD space.
3. Return the new modal flux, eigenvalue and signed axial leakage.

The validation iteration is direct Picard, $x^{m+1}=G(x^m)$ (`alpha=1`). There
is no fitted closure, empirical coupling coefficient, damping, clipping, flux
floor or added CMFD correction. Negative layer leakage means net inflow and
is retained. See the [concise derivation](SPOT_doc/rederivation.md) for the
equations and approximation boundaries. Historical acceleration experiments
are not the active D4-A validation method.

## Convergence contract

The three separate coupled defects must all satisfy the original gate:

$$
R_\rho\le 5\times10^{-7},\qquad
R_L\le 5\times10^{-7},\qquad
R_a\le 5\times10^{-7}.
$$

Here the code's $\rho=1/k$; $R_L$ is the relative leakage change and $R_a$
the volume/Gram-weighted relative modal-flux change. An inner solver reaching
its iteration cap without passing its terminal test is rejected. A completed
map (`CLOSED/n`) is not necessarily a fixed point (`VALID_MET`). Neither a
MET result nor passing software tests alone establishes physical accuracy.

## D4-A status

Status checked **2026-09-29: CLOSED/9 independently verified VALID_MET; complete final-output replay PASS, independent CE k comparison FAIL.**
The current case has 370 energy groups, 132 radial regions representing a 217-pin
symmetric assembly, twelve axial numerical cells across three 50 cm physical
zones, fixed rank 2, SN 8 and declared SCAT 3. The old three-cell chain is preserved
separately and must not be spliced into the fine-mesh chain.

| Requirement | Evidence / remaining work |
| --- | --- |
| Corrected scattering implementation | Source repair, clean build and short regression/readback checks passed. |
| New initial state | Three repaired radial responses completed; CLOSED/0 admitted. |
| Online radial–axial coupling | Nine 12-cell maps independently replayed; CLOSED/9 is the first **VALID_MET**. |
| Coupled convergence | Map-9 defects are `2.91194e-8 / 2.98318e-7 / 3.64179e-7`; all satisfy the unchanged `5e-7` AND gate. Rrho increased but still passes; leakage/flux defects decreased 72.22%/59.76%. |
| Final outputs | Saved CLOSED/9 k and normalized nu-fission outputs sealed; full nine-map lineage/output replay PASS. No new transport solve. |
| Independent accuracy | CLOSED/9 differs from existing CE by −1095.56180 pcm, outside the unchanged 558.65111 pcm allowance. Same-state leakage excess +1.49629 percentage points; pin-zone nu-fission max/RMS differences 2.04726%/0.90509%, descriptive only. |
| Reproducible delivery | Real map-1 standalone copy/replay verified; complete release assets not yet published. |

In the preserved old three-cell chain, map 2 defects are `Rrho=1.12978e-5`, `Rleak=6.54934e-4`,
`Ra=5.83029e-5`: decreases of 79.2%, 86.3% and 74.6% from map 1, but all remain
above the gate. Map 2 completed in 5 h 3 min, within its approved caps.
No retry or map 3 occurred; the completed-run monitor is paused.

Saved-state diagnostics on repaired map 1 find source-normalized axial leakage
8.992% versus the existing CE reference's 6.230%; pin/floor production shape
differences have also been reported. These are **NOT_MET diagnostics**, not a
mesh-error decomposition or accuracy PASS. After an initial 90 s six-cell
timeout, a separately authorized fresh six-cell solve completed in **97.35 s**,
within its 300 s cap. With the same frozen radial response, the 3-to-6-cell
physical reactivity shift is **+784.49 pcm**. A subsequently authorized 12-cell
solve completed in **351.97 s**; the 6-to-12 shift is **+156.82 pcm**, about
20% of the preceding increment. Grid sensitivity is material and decreasing
in this study, but a mesh-error bound remains unproven; coupled convergence was subsequently established for the 12-cell route below.
The independent checker's old-reference axial storage-size coupling has now
been fixed in source, with 49 synthetic cases and unchanged real map-1/2
replays. It is now copied into a separately sealed 12-cell runtime; the old
runtime is unchanged. The 12-cell seed package was
prepared and checked without transport (4.07 s). The user subsequently approved
one three-plane radial refresh, started at **17:00:55 Asia/Shanghai on Sep 25**:
32400 s radial cap, followed by a shared 60 s sealing/check phase; no retry or
next Picard map. It completed at **19:11:05**: radial 7807.36 s and postprocessing
3.12 s. All 29 result entries and 15 inputs verify, and independent B2I/B2J
replay produces byte-identical logs and outputs. A genuine fine-mesh CLOSED/0
is now available. Its runtime/bootstrap pair passes transport-free preflight;
cross-mesh inputs are rejected before execution. The user separately approved
one complete fine-mesh map: it started at **21:27:52**, with a total deadline
of **Sep 26 06:39:52**, radial/axial caps of 32400/600 s and 120 s reserved for
checks. It completed at **Sep 26 01:54:13** in **4 h 26 min**, with
`k64=1.2839459587336686` and defects `2.04333e-3 / 1.13691e-1 / 7.19513e-3`.
All three remain above `5e-7`; independent checker/gate replay is byte-identical
and all original manifests verify. Saved-state pin-zone/current diagnostics
are reported, not final accuracy acceptance. The user subsequently approved
exactly one second fine-mesh map with the same 32400/600/120 s caps. It started
at **Sep 26 02:27:05 Asia/Shanghai**, with total deadline **11:39:05**;
CLOSED/2 completed at **06:32:28** in **4 h 5 min**, with k64=1.2850014862263228
and defects `6.39763e-4 / 1.49518e-2 / 1.76808e-3`. Independent checker/gate
replay is byte-identical and all checked manifests remain unchanged. The
managed session exited normally; final OS process-tree verification is limited
by denied process-inspection permission, and the monitor remains paused.
The user subsequently approved exactly one third map with the same caps. It
started at **Sep 26 20:01:50**, with total deadline **Sep 27 05:13:50**. The
CLOSED/3 completed at **Sep 27 00:11:03** in **4 h 9 min**, with
`k64=1.2846693106401121` and defects `2.01221e-4 / 1.84426e-3 / 5.72090e-4`.
All three remain above `5e-7`. Independent checker/gate replay is byte-identical,
all checked manifests pass, and the three-map lineage replays. Final acceptance
correctly refuses NOT_MET. Known tracked process IDs/groups are absent and a
complete process census contained no Dragon at that completed-run checkpoint.
The user then explicitly approved one fourth map: it started at **Sep 27
01:08:47 Asia/Shanghai**, with the same 32400/600/120 s caps and total deadline
**10:20:47**. It completed at **05:13:37**, in **4 h 4 min 50 s**, with
`k64=1.2847632870991244` and defects `5.69383e-5 / 3.72527e-4 / 1.84938e-4`.
CLOSED/4 is independently verified NOT_MET: all checked manifests pass,
checker/gate replay is byte-identical and the four-map lineage replays.
The user then separately approved one fifth map with the same caps. It ran at
**Sep 27 16:55:29–21:01:11 Asia/Shanghai**, taking **4 h 5 min 42 s**.
CLOSED/5 is independently verified NOT_MET, with `k64=1.2847435747721441`
and defects `1.19426e-5 / 5.49844e-5 / 6.04892e-5`. Five-map lineage,
sealed-input checks and byte-identical checker/gate replays pass. All defects
remain above `5e-7`. The user separately approved one sixth map with the same
32400/600/120 s caps. It started at **Sep 27 22:57:58 Asia/Shanghai**, with total
deadline **Sep 28 08:09:58**. It completed at **Sep 28 03:00:54** in
**4 h 2 min 56 s**, with `k64=1.2847427149054287` and defects
`5.20953e-7 / 1.63844e-5 / 1.96005e-5`. CLOSED/6 is independently verified
NOT_MET; all checked manifests and six-map lineage pass, and checker/gate
replays are byte-identical. That attempt did not retry or automatically start map 7.
The user subsequently approved exactly one seventh map with the same
32400/600/120 s caps. It started at **Sep 28 03:43:21 Asia/Shanghai**, with total
deadline **12:55:21**. It completed at **07:53:17** in **4 h 9 min 56 s**, with
`k64=1.2847437189313020` and defects `6.08292e-7 / 2.90850e-6 / 5.46714e-6`.
CLOSED/7 is independently verified NOT_MET; sealed inputs, seven-map lineage
and byte-identical checker/gate replay pass. That run stopped without a retry or
automatic eighth map. Leakage and flux defects decrease, but Rrho increases;
this is neither monotone three-defect convergence nor final accuracy acceptance.
The user then separately approved map 8 with the same 32400/600/120 s caps.
It started **Sep 28 14:56:15 Asia/Shanghai**, with total deadline **Sep 29 00:08:15**.
It completed at **Sep 28 19:02:56** in **4 h 6 min 41 s**, with
`k64=1.2847437095912226` and defects `5.65871e-9 / 1.07395e-6 / 9.04997e-7`.
CLOSED/8 is independently verified NOT_MET: eight-map lineage, input checks
and byte-identical checker/gate replay pass. That attempt stopped without retry
or automatic continuation. The user subsequently approved one ninth map with
the same 32400/600/120 s caps. It started **Sep 28 21:23:56 Asia/Shanghai**;
the total deadline was **Sep 29 06:35:56**. It completed at **Sep 29 01:33:41**
in **4 h 9 min 45 s**, with `k64=1.2847437576547476`. CLOSED/9 is independently
verified VALID_MET. All nine map lineages, sealed inputs and byte-identical
checker/gate replays pass. Subsequently authorized saved-output extraction and
complete final replay pass; the existing CE k criterion fails. Monitoring is paused;
no retry or automatic tenth map is authorized.
The runtime, rank, closure, alpha=1 and thresholds remain unchanged. See the
[final output and CE comparison](validation/iterative/d4a_mesh12_map9_final_comparison_result.md),
[fine-mesh map-9 result](validation/iterative/d4a_scattering_mesh12_picard_map9_result.md),
[fine-mesh map-8 result](validation/iterative/d4a_scattering_mesh12_picard_map8_result.md),
[fine-mesh map-7 result](validation/iterative/d4a_scattering_mesh12_picard_map7_result.md),
[fine-mesh map-6 result](validation/iterative/d4a_scattering_mesh12_picard_map6_result.md),
[fine-mesh map-5 result](validation/iterative/d4a_scattering_mesh12_picard_map5_result.md),
[fine-mesh map-4 result](validation/iterative/d4a_scattering_mesh12_picard_map4_result.md),
[fine-mesh map-3 result](validation/iterative/d4a_scattering_mesh12_picard_map3_result.md),
[fine-mesh map-2 result](validation/iterative/d4a_scattering_mesh12_picard_map2_result.md),
[fine-mesh map-1 result](validation/iterative/d4a_scattering_mesh12_picard_map1_result.md) and
[bootstrap result](validation/iterative/d4a_scattering_mesh12_bootstrap_result.md).
No physical closure changed; see the
[mesh-attempt result](validation/iterative/d4a_scattering_axial_mesh_result.md).

Read the [repaired map-2 result](validation/iterative/d4a_scattering_picard_map2_result.md),
[current handoff](validation/iterative/d4a_final_validation_handoff.md), and
[acceptance matrix](validation/iterative/d4a_corrected_acceptance_matrix.md).
Nu-fission fractions are not absolute thermal power. Mesh/rank accuracy,
multi-assembly coupling and IRENA full-core validation remain unestablished.

## Build and use

Build only in a **separate, inactive checkout** while a frozen calculation runs:

```sh
make -C src -j2
make -C validation/iterative -j2
make spot-fast
```

`SPOT ACTIVE FAST PASS` covers software contracts and algebra, not physical
convergence. This documentation update did not rebuild the active runtime.

Use the [current D4-A quickstart](validation/iterative/D4A_CORRECTED_QUICKSTART.md)
for explicit repaired-runtime preflight and read-only postprocessing. Do not
use the old default/series route or rebuild inside an active run. Large sealed
inputs and the exact runtime are not supplied by a source checkout alone;
complete clean-checkout D4 reproduction is still a delivery requirement.

The [development history](HISTORY.md) preserves the earlier experiments and
superseded results without presenting their commands as current instructions.
