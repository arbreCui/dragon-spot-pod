# Current D4 scattering-data localization — updated 2026-09-29

The obstruction to a same-data multigroup reference is now localized to saved
microscopic scattering data, primarily Fe56 in the steel mixtures at groups
25/26. This diagnostic does not establish its effect on k or authorize a cross-section
correction. The active solver, snapshots and runtime were unchanged.

## Recovered prior result: do not repeat the GENDF audit

After the user pointed out duplicate work, the September 7 dragon-project
[production-physics audit](/Users/wen/dragon-5.1/Dragon/irena_core/colorset_rebuild_20260527/ce_compare/pnl_s30_production_physics_audit_v1_20260907/README.md)
was located. It already analyzes **this same original Fe56 GENDF**, including
G25/G26, rather than the later P3 lineage. The preceding search had missed
this more directly relevant report. The proposed new GENDF parser/audit is
therefore cancelled, not an outstanding task.

That report establishes that MF3/MT51 has ten dilution points while MF6/MT51
contains only the infinite-dilution matrix. GROUPR's inspected selection
retains dilution dependence for the scalar channel but not that matrix;
DRAGR broadcasts the single matrix over the elastic dilution grid. The
target-group contribution is MT2 + MT51, not real (n,2n) multiplication.
At 550 K and 2.5 barn, G25 MF3/MT51 is 0.324126 barn whereas the MF6 P0 sum
is 0.36025039992 barn. An independent native-printout sum is also retained.
The report separately records a smaller elastic-matrix integration discrepancy;
restoring MT51 alone is not proven to yield exact balance.

Read-only identity checks on September 29 reproduce **all seven** applicable
hashes declared by that report: GENDF, native printout, GROUPR source, DRAGR
source, audit script, tests and audit JSON. In particular:

- GENDF: `ae37d04f51154aa5275edd98a098519fdd9f640ed112f70337ab38e5763928a1`.
- Existing audit JSON: `a8c46e23b1e600b24be05554afa150614c19d8d278e3dddb7378151264853dfe`.

The existing 19-test result belongs to the September 7 audit; it was not
rerun or claimed as new work. No new script, GENDF analysis, processing or
solver run was started during this recovery. The preserved September 29
lookup artifact below adds only the **D4 saved-state connection**; its sealed
statement that the upstream origin was still unknown is historical and is
superseded by this recovered evidence, not silently rewritten.

The distinction for next work is **known cause versus validated replacement**.
The September 7 audit is not production-accepted. The September 10 Fe56 P3
pilot changes angular order, and is not evidence of an accepted MT51-dilution
repair. First locate any already qualified repair product in dragon; reuse it
if applicable, rather than repeating data-processing diagnosis. A new library
or D4 calculation requires separate validation scope/budget. None of this
quantifies the contribution to D4's k error.

### Existing products checked directly — 2026-09-29

The original library, the later chain-control P1 library, and the September 10
P3 pilot were checked through their retained GENDF section headers. Each has
five temperatures (293, 550, 900, 1200 and 2000 K), 370 groups and the following
same dilution coverage; 45 selected section headers were read, not recalculated:

| Retained product | MF3/MT51 scalar dilutions | MF6/MT51 matrix dilutions | Matrix angular orders |
| --- | ---: | ---: | --- |
| D4 original | 10 | 1 | P0–P1 |
| Later chain-control P1 | 10 | 1 | P0–P1 |
| Fe56 P3 pilot | 10 | 1 | P0–P3 |

MF6/MT2 (elastic) has ten dilutions in all three files. The P3 output therefore
**still lacks the MT51 matrix dilution dependence**: this is direct output
evidence, not just an inference from its input card. Its completion receipt
also says `production_accepted=false`, `completed_pilot_not_transport`.

The later P1 GENDF is
`/Users/wen/dragon-5.1/Dragon/irena_core/colorset_rebuild_20260527/lib_shem370_chain_control/shem370_control_mp_xsm/Fe56/gendf_neutron_Fe56`,
SHA-256 `fa831f91fec82f70406503fcd3e47d2d737694811996c3d06221aaaf2d6767e2`,
matching the P3 preparation manifest's old-GENDF pin. Its MF6/MT51 headers
are at lines 16202, 39721, 63303, 86950 and 110652.

The P3 GENDF is `groupr_p3/tape30` under
`/Users/wen/dragon-5.1/Dragon/irena_core/colorset_rebuild_20260527/ce_compare/mc2027_csd_rr_evidence_v1_20260909/paper_parallel_20260910/angular_tracking/p3_pilot/fe56_v2/attempt_Fe56/`,
SHA-256 `18c6678d50f58dc78652f0442b9028a123a7c47d61a621390527ecdffa6fd3bc`,
matching `groupr_p3/complete.json`. Its MF6/MT51 headers are at lines 21579,
56840, 92239, 127756 and 163404. GENDF HEAD fields L1/L2 give NL/NZ;
the next LIST header identifies temperature. A read-only 0.13-second scan
checked section transitions, HEAD sequence numbers, group counts, all five
temperatures and terminal TEND. It did not parse/reprove the old numerical
root-cause analysis or launch any native process.

Thus **none of these identified 370-group products is a ready MT51 repair**.
This is a scoped inventory, not a claim that every file on the machine was
searched. The separate 1962-group library is not a one-change replacement
for this 370-group D4 validation.

If a new repair experiment is authorized, reuse the September 7 diagnosis
and checks: in a private NJOY build retain D4's original Fe56 inputs and
P1 order, enable finite-dilution integration only for MF6/MT51, and compare
the scalar/matrix balance and angular/energy distribution at the declared
dilution grid. Do not copy or scale a scalar into a matrix. First test the
single isotope; do not automatically merge a library, rerun TONE, or restart
D4. The earlier P3 processing took about two minutes, but that does not
guarantee the modified work's runtime; an explicit hard budget is required.

### Static preparation (historical; subsequently authorized below)

The one-line candidate is retained as
[`fe56_mt51_candidate.patch`](fe56_mt51_candidate.patch): set `nz=nsigz` for
MF6/MT51 in GROUPR `init`. `git apply --check` passes against the pinned
`groupr.f90` hash `72c207415f53b6d242c9d81caea40ea6c6dc3900542499279bd4d524ab075dac`.
The patch hash is `848d0c650bc2549077bf97927fdad0addd96a3faf38afc4a7b8be922a3f9f8b0`.
**At this preparation checkpoint it had not been applied, compiled or executed.** It is a candidate
finite-dilution integration setting, not an accepted physical fix. Its
private executable must be used only for this Fe56 experiment.

A preparation check found why the P3 launcher cannot be run unchanged:
it binds the later chain-control inputs, excludes the SPOT tree, and waits
for natural exits without the proposed hard timeout. D4's original PENDF
has hash `717c347cc0902236965893834fe429a0b9b2d3c65f149b958f1152c134f2be30`,
not the later P1/P3 PENDF hash. Use the original cards unchanged:
GROUPR `0cc21aa077e5469b391de390cc30b1fd22a771af60a219fded7cfb7c60c499ea`,
DRAGR `bc74ad3c7b93bc1479df23f31acafbe56ca893e67f2096a99901efcadc0b5b7b`.
The evaluated Fe56 input is pinned at
`eca38d4ce177a463bbc872e50fef451dd4428adf86495ba69e71b4ebf65a7b19`.

The proposed 600-second ceiling must cover isolated compilation, an unpatched
control and the one-line candidate, and their checks, with no retries or
automatic follow-on. The control is needed to separate rebuilding/processing
differences from the one-line change. Existing production executables and
libraries must remain untouched. No execution-preparation tree or runner was
created in this static check; no new computational authorization was inferred
from automatic goal continuation.

### Authorized paired processing completed on 2026-09-29

The user subsequently approved the one-time 600-second experiment. Both private
builds and four processing stages finished; control reproduces all original
DRAGLIB records. The one-line candidate restores MF6/MT51's ten dilutions at all
five temperatures, with unchanged total/capture/flux records. Fixed-background
D4 lookup no longer clamps the scalar in the twelve selected Fe56 entries.
Processing/comparison took 232.90 s; independent read-only review ended at
299.95 s from launch. No empirical correction, production replacement or new
TONE/D4/CE solve was performed.

The controller's final stage-receipt write collided with the already produced
comparison JSON. Its FAILED status and traceback remain untouched; the native
results and read-only review pass are documented separately, not rewritten as
a successful controller run. There was no retry. See
[the paired result and limitations](fe56_mt51_candidate_result.md).

## Matched-library lookup completed — 2026-09-29

The new audit uses the actual **CLOSED/9** saved microlibs and backgrounds,
not a later dragon-project P3 library. D4's original DLIB370 resolves to
`/Users/wen/draglib_output/shem370_endfb8r1_v5p1/draglibshem370_endfb8r1_v5p1.xsm`.
Its SHA-256 is
`66b9a7b3e8534a54cf590db63a7c1dbd96b4a95c636f0e3a6eee5b219bbcc1e9`,
matching D4's executed-input receipt. All **641 Fe56 subtree records** match
the original isotope ASCII file (REAL32 numeric values and exact other fields).
The later Fe56 P3 processing and its P1 baseline are different library lineages;
only their readers/interpolation code were reused, not their numerical conclusions.

For G25/G26, all five temperature tables contain P0 matrices but no SIGS00,
including their nine finite-dilution correction tables. The infinite-dilution
outgoing sums are below NTOT0. At several finite-dilution nodes, however,
the sum of **infinite matrix + finite correction** exceeds the corresponding
total numerator, already **before dilution interpolation**. Examples at 293 K:

| Dilution (barn) | G25 sum-minus-total numerator | G26 sum-minus-total numerator |
| --- | ---: | ---: |
| 2.5 | +0.04366706765 | +0.04101338960 |
| 19.88179970 | +0.00603693091 | +0.00471058852 |
| 56.06769943 | +0.00060959418 | −0.00039527037 |

These are unnormalized reaction numerators, **not** finite-correction records
treated as standalone cross sections. The common positive flux normalization
does not reverse their ordering. The report retains all 90 node/group checks.

The source path is `LIBDRB.f`: missing SIGS00 + present SCAT00 selects
the matrix-derived scalar branch; line 609 stores
`SIGS = MIN(REAL(matrix sum), TOTAL)` without changing the matrix there.
Both are then divided by the reconstructed flux weight, and `LIBDRA.f`
combines the temperature contributions. This is an existing scalar cap,
not a new parameter or a correction introduced by this audit.

Using the **saved D4 temperatures, DSN and DSB**, offline REAL32 replay gives:

- All **12** selected rows: 3 planes × 2 steel mixtures × G25/G26.
- All **48** NTOT0/SIGS00/NWT0/NG values equal the saved values; an additional
  check verifies their REAL32 bit patterns.
- All **4440** selected outgoing matrix entries numerically equal the saved
  REAL32 entries; maximum absolute difference **0**.
- Every selected temperature contribution takes the scalar-cap branch in
  the replay. Top EM10 retains outgoing-sum minus SIGS00 of
  **0.0103030579085 barn (G25)** and **0.00870788203247 barn (G26)**.

Thus the original finite-dilution records plus the existing lookup path
reproduce the saved discrepancy completely. It is not introduced by POD,
MGXEXP, or dilution interpolation alone. This is a saved-state algebraic
reconstruction, not an instrumented trace of the historical execution; it
does not prove which original nuclear-data processing operation first created
the finite-table discrepancy. The pre-TONE microlib was deleted by the original
snapshot deck and is not claimed to have been recovered.

Two equality-only native exports took **0.383 s** and **0.531 s**. Six short
tests passed, including asymmetric signed sparse layout, rejection of missing
self-shielded payload, a scalar-cap fixture, a separate dense-matrix sum of the
saved records, and source/input hashes. No transport/TONE/CE solve, compilation,
library write, clipping, row normalization, or model/threshold change occurred.
Evidence and exact source hashes:
`validation/artifacts/d4a-fe56-library-path-audit-20260929/`.

**The contribution to the −1095.56 pcm k discrepancy remains unmeasured.**
This closes the lookup-localization question; it does not close the independent
accuracy requirement or justify replacing the library.

## Current-epoch raw export

The input is the actual repaired 12-cell map-6 `initial_axial_macrolib.xsm`,
SHA-256 `853003ab2a24279f1176ea6d668a827b45f09bdafde0aa030dfae6f9cabd24ab`.
A private copy and a copy of the sealed repaired executable were used for
`MGXEXP` only. The log contains no ASM or FLU call. The export took 2.81 seconds
including executable startup; the Python audit took under one second.

All 6660 mixture/incident-group rows were evaluated directly from signed P0
records, without clipping or row normalization. The maximum absolute difference
between the outgoing scattering sum and SIGS00 is **6.92907412e-4 cm^-1**, at
mixture 18, group 25. The maximum relative difference is **0.325280%**, at
mixture 18, group 26. These are new current-input measurements; they do not
replace the slightly different historical export numbers in the old records.

| Current mixture 18 (top-zone EM10) | Group 25 | Group 26 |
| --- | ---: | ---: |
| Energy interval (eV) | 950833.625–1050834 | 905365.8125–950833.625 |
| SIGS00 (cm^-1) | 0.217715606093 | 0.180039778352 |
| Outgoing P0 sum (cm^-1) | 0.218408513505 | 0.180625412017 |
| Difference (cm^-1) | 0.000692907412 | 0.000585633666 |
| Exported excess multiplicity | 0 | 0 |

Transposing the matrix makes the global maximum mismatch about 37.59 cm^-1;
it is not a remedy. Adding or subtracting the exported multiplicity cannot
remove these two discrepancies because the corresponding entries are zero.
Negative P0 channels are retained and reported, not made sampleable by this tool.

## Microscopic localization

A separate Ganlib-only reader opened a private copy of the saved map-6
`closed_snapshots.xsm` read-only. For all three physical planes it read each
isotope's density, NTOT0, SIGS00, IJJS00, NJJS00 and SCAT00 in base mixtures
2 (AIM1) and 6 (EM10), and independently summed groups 25/26.

For top-zone EM10/group 25, the saved Fe56 microscopic values are:

| Quantity | Value |
| --- | ---: |
| Density (atoms/barn-cm) | 0.0672528296709 |
| NTOT0 = SIGS00 (barn) | 2.478469610214 |
| Outgoing P0 sum (barn) | 2.488772668123 |
| Density-weighted difference (cm^-1) | 0.000692909799 |
| All-isotope weighted difference (cm^-1) | 0.000692909131 |
| Macrolib difference (cm^-1) | 0.000692907412 |

Fe56 dominates the selected discrepancies in both steel materials and all
three planes. The other isotope contributions largely cancel at much smaller
magnitudes. In every selected Fe56 row SIGS00 equals NTOT0 exactly while the
matrix production sum exceeds it. The macro and independently density-weighted
micro differences are close but not bitwise identical; the full differences
are retained in `localization.json`, with no new acceptance tolerance.

This puts the discrepancy **upstream of MGXEXP and the POD axial solve**.
`SPOLIB` copies the three six-mixture macrolibs into disjoint blocks without
homogenization. The reader directly observes the inconsistency in its saved
microlib inputs, so changing only the text exporter cannot restore consistency.

## Existing dragon-project evidence recovered on 2026-09-28

Fe56 processing and TONE lookup have already been studied in the dragon
project. The initial SPOT audit did not incorporate those records; the next
step below is narrowed accordingly.

- The [2026-09-10 Fe56 P3 review](/Users/wen/dragon-5.1/Dragon/irena_core/colorset_rebuild_20260527/ce_compare/mc2027_csd_rr_evidence_v1_20260909/paper_parallel_20260910/angular_tracking/p3_pilot/INDEPENDENT_REVIEW_Fe56.md)
  checks genuine SCAT02/03, five temperatures, nine finite dilutions, the
  signed compressed arrays and native finite-correction tails. It also reports
  small real changes in the lower moments. That work need not be repeated.
- The [2026-09-24 TONE-path audit](/Users/wen/dragon-5.1/Dragon/irena_core/colorset_rebuild_20260527/ce_compare/mc2027_csd_rr_evidence_v1_20260909/paper_parallel_20260910/single_int_tone_path_audit_v1_20260924/RESULTS.md)
  reconstructs the saved background cross sections and replays NG, NTOT0 and
  NWT0 for ten selected single-INT resonance entries, including Fe56 at G140
  and Cr52 at G137. The maximum table-replay relative difference is 1.86e-9.
  It finds no missed table, range violation or lookup implementation error
  for those entries. The nine files in its delivery receipt were hash-checked
  when this cross-reference was added; no native calculation was rerun.

These records do not contain the present D4 G25/G26 comparison of outgoing
SCAT00 against SIGS00. The TONE replay's selected fields omit both of those
scattering quantities, and the physical case and library lineage must be
matched before transferring a numerical conclusion. `TONCMI.f` is identical
across the two current project directories. The `LIBDRB.f` difference adds an
isotope-name argument to its diagnostic messages; the interpolation and P0
sum/clamp code are unchanged. This source comparison alone does not prove
equal libraries, binaries or saved isotope states.

## Remaining work, not another root-cause audit

Reuse the recovered September 7 GENDF diagnosis above. Check for an existing
qualified replacement before proposing any new processing. Any eventual
library change creates a new input epoch requiring validation; neither SIGS00
nor SCAT00 may be rescaled merely to pass the MC exporter. A new physical
bias experiment needs its own scope and computational budget.

This finding explains why the matched MG reference is blocked. It does **not**
explain a measured fraction of the approximately -1096 pcm SPOT–CE difference,
or show that fixing this inconsistency would resolve the 2D/1D closure error.

## Reproduction

Evidence: `validation/artifacts/d4a-scattering-data-audit-20260928/` contains
the raw `macrolib.mgx`, group CSV, summaries, microscopic reader source and
rows, executed export deck/log, input hashes and reproduction instructions.
The executed export deck retains its historical map8 filename internally;
`inputs.json` identifies its actual map-6 input. It never loaded a map-8 state.

Regenerate the raw-data analysis without Dragon or OpenMC:

```sh
python3 validation/d4_reference/audit_mgxexp.py \
  validation/artifacts/d4a-scattering-data-audit-20260928/macrolib.mgx \
  /absolute/path/to/new-audit-output
```

Eight analytic tests for the raw-scattering and saved-evidence tools run with
`make spot-evidence-test`. Existing transport acceptance and physical thresholds
are unchanged.
