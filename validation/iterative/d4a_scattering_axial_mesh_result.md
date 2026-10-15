# Repaired D4-A: frozen-radial axial mesh comparison — 2026-09-25

## Current result: 3 / 6 / 12-cell comparison completed

The user subsequently approved **one 12-cell cold start, maximum 600 seconds,
no retry**. It completed at **15:03:35 Asia/Shanghai**, with **351.970 seconds**
in the bounded solve and **363.134 seconds** for the driver and checks.
No further transport was launched; the original coupled maps remain unchanged.

| Axial cells | Cell height | k64 | Physical reactivity change from preceding mesh |
| --- | ---: | ---: | ---: |
| 3 | 50 cm | 1.2719105545187395 | — |
| 6 | 25 cm | 1.2847296535189214 | +784.493197 pcm |
| 12 | 12.5 cm | 1.2873232763835052 | +156.822169 pcm |

The increments use `1e5*(1/k_coarse - 1/k_fine)`. The second increment is
**0.1999025223** of the first (an 80.01% reduction). This is evidence that
this further refinement changes the frozen-radial solution less. It does
**not** establish an asymptotic order, remaining error bound, pure POD error,
coupled fixed point or final CE accuracy. No extrapolated correction or fitted
coefficient has been applied to any solution. No 24-cell calculation is authorized
or started by this experiment.

Twelve cells terminated after 19 outer iterations with
`EEXT=6.20145345e-9`, `EUNK=1.99181925e-6`, `EINR=3.61997700e-7`;
all three unchanged 2e-6 solver thresholds pass. The saved-state checker
independently returns `NFLOOR=12, K64=1.2873232763835052`. SPORATE's
three physical-zone fractions are `0.261284364 / 0.482744307 / 0.255971329`,
using the same REAL32-mirror/REAL64-accumulation convention as the preceding
meshes. They are not twelve cell fractions or absolute thermal powers.

Evidence: `validation/artifacts/d4a-scattering-axial-mesh12-run-20260925`.
All **21** result entries and copied input identities verify; the 3-cell,
6-cell, map-1 and runtime manifests pass before and after the run. Result
manifest SHA-256:
`87e7b08ee7539baf3498f2677150a30d08df15e3a9e53f8115eeedd6dff32b8a`.
A second agent independently verified these identities, terminal tests,
existing GANLIB-only readback and the increment arithmetic. The four physical
inputs are byte-identical across the comparisons. No solver/controller remains.

### Minimum work before a fine mesh can enter the coupled chain

A parallel read-only check found no need to rewrite SPOSTATE, SPOLEAK, B2J or
B2W: they handle NFLOOR dynamically and retain three **physical** snapshot zones.
The direct checker mismatch was that `check_one_map_xsm.f90` demanded
the whole old-reference/new-SYSTEM STATE-VECTOR match, including NUNKN, while
`SPOASM.f:124–128` correctly permits a radial fixed basis on a different axial
mesh. This is now fixed in source: only the reference's positive NUNKN may
differ; all other state entries and radial bit comparisons remain unchanged.
Both actual map states must match the current SYSTEM NUNKN, and every FLUX
and optional FLUX64 group must match its declared size/type. No CLI or threshold
changed; canonical-only direction/history paths gain no raw-field dependency.

Strict isolated compilation and **49 synthetic cases** passed (7 test methods,
9.704 seconds including compilation), covering lawful cross-mesh radial-basis
reuse and rejection of coarse parents, false sizes, missing/truncated/wrong-type
fields, non-size state changes and basis-bit changes. Real repaired map-1 and
map-2 checker replays remain byte-identical and their 48-entry manifests verify.
The test is registered in the active fast gate. Evidence:
`validation/artifacts/d4a-fine-mesh-checker-20260925`.
No sealed runtime was replaced. This is stronger storage consistency, **not**
independent TRACK geometry certification or a new physical convergence result.

A true fine-mesh CLOSED/0 and matching sealed identities are also required:
the isolated result is not an authorized replacement for a coupled parent,
and changing TRACK underneath the old parent is invalid. Original basis
provenance remains useful; its coarse-grid-specific build checker need not
be generalized merely to retain that provenance.

The twelve-cell seed preparation is now complete in
`validation/artifacts/d4a-scattering-mesh12-bootstrap-prepared-20260925`:
4.068 seconds of SPOLEAK-only postprocessing and checks, no transport solve.
The verified AX/TRACK/macro/basis are unchanged copies; the original TYPE-K
archive remains an uncertified numerical guess. The existing checker verified
1110 leakage mirrors and 1110 unchanged raw flux vectors. B2I correctly refused
these unsolved guesses without outputs. All 15 prepared inputs verify; the
manifest hash is `b59168704acb63e70c217868cc1896468a41ff6d0b8cb8cc8013d28782781216`.
Status is **PREPARED_NOT_CLOSED0**, not a new coupled parent. A source review
confirms no new naming adapter or mesh-specific B2I branch is needed.

Next comes a separately authorized three-plane TYPE-S refresh for this new
source/leakage, then existing B2I/B2J sealing and projection checks. No repeated
axial seed solve is required, and no new physical controller was started.
Any new physical bootstrap/map needs explicit compute authorization. Further mesh/angle accuracy
and the same-mesh cold/warm repeatability warning remain unresolved. This checker
change followed the completed 12-cell experiment and did not alter its evidence.

## Earlier result: the separately approved six-cell run

After the first 90-second attempt below, the user explicitly approved one
fresh six-cell cold start, capped at 300 seconds, without automatic retry.
It completed at **14:07:47 Asia/Shanghai**: solve **97.349 seconds**, entire
driver/readback **102.618 seconds**. No new radial, Picard or CE run occurred.
The original three-cell baseline and unsuccessful six-cell attempt remain intact.

| Quantity | 3 cells, retained baseline | 6 cells, new completed run |
| --- | ---: | ---: |
| Cell height | 50 cm | 25 cm |
| k64 | 1.2719105545187395 | 1.2847296535189214 |
| Outer iterations | 13 | 14 |
| EEXT | 1.06019038e-8 | 7.35564463e-8 |
| EUNK / EINR | 1.90528769e-6 | 1.71107250e-6 |

Both meet the unchanged three inner solver thresholds of 2e-6. The physical
reactivity change is
`1e5 * (1/k3 - 1/k6) = +784.4931972562 pcm`.
Here physical reactivity is `1 - 1/k`; the code's stored inverse-k coordinate
has the opposite signed change. This is a **large frozen-radial mesh
sensitivity**, not a discretization-error bound, pure POD error, coupled
fixed-point shift or CE accuracy acceptance. It is much larger than the
observed 0.48144 pcm same-mesh cold/warm difference discussed below.

The three physical-zone nu-fission fractions change from
`0.259842915 / 0.484017676 / 0.256139409` to
`0.261673711 / 0.481642829 / 0.256683460`:
`+0.183080 / -0.237485 / +0.054405` percentage points. SPORATE aggregates
the six cells through MAT1D into the same three physical zones and reads the
REAL32 FLUX mirror with REAL64 accumulation; these are not absolute thermal
powers. The solver's balance diagnostic reports zero nonpositive scalar
values, minimum `5.00874e-18`; this diagnostic was not independently rebuilt.

New evidence: `validation/artifacts/d4a-scattering-axial-mesh6-run-20260925`.
All **19** result-manifest entries verify before and after independent readback;
the manifest hash is
`8abb49c26110f56b59349d21aa19c8aba916c9ed835c6e94557c51bafedddd89`.
The original 24-entry mesh experiment, 48-entry map-1 result, 11-entry runtime
and all copied input identities also verify unchanged. A second agent separately
checked the decks, terminal records, hashes and reactivity calculation and
ran the existing GANLIB-only checker. Both successful independent readbacks
returned `PASS NFLOOR=6 K64=1.2847296535189214`.
One additional main-agent reader invocation using absolute filenames trapped;
the established case-directory/relative-filename invocation passed unchanged.
No transport was repeated, and no evidence was overwritten.

**Historical next priority (now completed above):** one same-input 12-cell cold-start diagnostic to measure the
6-to-12 change before committing to another hours-long coupled map. A proposed
600-second cap, no retry, required new approval, subsequently granted; it was not covered by the
completed 300-second authorization. Do not silently
replace the coupled chain's three-cell mesh or declare mesh convergence from
two grids. The coupled original AND gate and the cold/warm repeatability issue
remain open.

The retained preparation deck `validation/artifacts/d4a-scattering-axial-mesh12-prepared-20260925/cells12.x2m`
has SHA-256
`8f5b13c8b4d6daae1e9aa4e3f0192c29d8fa1fe9e84aba0339e53618faa479ef`.
Two independent text reviews confirm that only CAR1D/MESHX/MIX and the comment
change from the verified six-cell deck: 12 cells of 12.5 cm, four cells per
original physical zone. It was copied unchanged into the authorized run above;
its historical preparation comment does not authorize any further run.

## Earlier 180-second paired attempt (preserved history)

**Result: 3-cell baseline verified; 6-cell timed out; no accepted mesh difference.**
The user explicitly approved one paired experiment: 180 seconds total,
90 seconds per solve, no retry. It ran at 04:06:30–04:08:44 Asia/Shanghai,
elapsed **134.488 seconds**. The 6-cell process group was stopped at its cap;
subsequent process inspection found no matching SPOT solver/controller left.
No Picard map, radial solve or CE calculation was started.

## What changed and what did not

The private cases use the same repaired map-1 radial response and the same
macrolib, rank-2 fixed POD basis, SN8, SCAT3, vacuum ends, 150 cm height and
original solver thresholds. Both start cold. The only active deck changes
are CAR1D/MESHX/MIX: three 50 cm cells become six 25 cm cells, with physical
zones `1,1,2,2,3,3`. An independent agent checked the decks and source mapping
before launch. No physics or numerical coefficient was fitted or added.

| Quantity | 3 cells | 6 cells |
| --- | ---: | --- |
| Solve wall time | 42.118 s | stopped at 90 s |
| Final k64 | 1.2719105545187395 | unavailable |
| Outer terminal EEXT | 1.06019038e-8 | no terminal PASS |
| EUNK / EINR | 1.90528769e-6 | no terminal PASS |
| Saved axial state | exported and independently read | not exported |

The 3-cell terminal passed the unchanged 2e-6 solver criteria. GANLIB-only
readback agrees with its k64, verifies all 146520 active scalar values positive
and the production norm bitwise, and reports fractions
`0.259842915, 0.484017676, 0.256139409`. The existing mesh checker verifies the
13 frozen radial records, physical-zone mapping and cell thicknesses. It is
not an independent reconstruction of all cross-group scattering matrices.

The 6-cell log records eight completed outer iterations; their recent EIG PRC
values are `2.26e-4, 2.07e-4, 1.32e-4, 5.96e-5`. After the eighth, another
18 inner iterations were recorded, last PRC `1.89e-5` versus `2e-6`.
This demonstrates continued iteration, not proven asymptotic convergence or
a bound on time remaining. Its last printed k is a transient diagnostic,
not k6. **Do not calculate a certified 3→6 reactivity shift from this attempt.**

## Evidence and next decision

Work: `validation/artifacts/d4a-scattering-axial-mesh-run-20260925`.
Its 24-entry result manifest verifies, SHA-256
`0650a62a20075a073fa199cff3f1678e1c476e425c4782f26bc7683ea3f174c9`.
All selected source/private inputs are unchanged. Full map-1, map-2 and runtime
manifests also verify after the attempt. Independent review logs are in
`validation/artifacts/d4a-scattering-axial-mesh-review-20260925`.
The incomplete 6-cell files and original failure status are preserved.

At the end of that first attempt, the proposed action was to retain this 3-cell baseline and, **only after new explicit
approval**, make one fresh 6-cell cold-start attempt with a 300-second cap,
unchanged inputs/deck/thresholds, no automatic retry. This is a requested new
budget, not use of the unused portion of the completed 180-second attempt.
No 12-cell run, new radial solve or Picard map is included. A completed pair
would measure frozen-radial mesh sensitivity, not full coupled mesh convergence,
pure POD error, CE accuracy acceptance, or IRENA full-core validation.

## Read-only cost check after the stopped attempt

Counting the existing `SPOF: PROCESSING GROUP` and `IN(...) FLX` log records:

| Recorded work | 3-cell complete run | 6-cell at timeout |
| --- | ---: | ---: |
| Single-group solver entries | 181090 | 226922 |
| Inner-iteration records | 671 | 847 |

The stopped 6-cell attempt had already entered 25.3% more group solves than
the entire 3-cell run. Source review also confirms that the normal non-TRAN
path uses a block-tridiagonal boundary solve: generic coupled rank-2/SN8 blocks
remain 16-dimensional; the number of face blocks grows from 4 to 7.
This is not an eightfold dense-global-system scaling claim. Exact mode
separability, when present, can split blocks further; no claim is made that
all 370 groups have identical block structure. The existing factor cache is
restricted to physical full-rank diagonal bases and is not active for rank 2.

Sources: `SPOF64.f:180`, `SPOT1P64.f90:410–428,539,703–724`, and
`FLU2DR64.f:592–606`. The inspected SPOT1P64 source is byte-identical to the
already-built clean cf469c8 source. These are log counts and algorithmic
structure, **not a runtime profile, predicted completion time, or a proof of
convergence**. No solver, cache, parameter or logging level was changed.
That fresh 6-cell attempt was subsequently approved and completed as recorded above.

## Same-mesh cold/hot-start cross-check — read-only

The new cold 3-cell run and repaired map 1's warm axial half-step use the same
saved radial response, basis and macrolib. Their TRACK files are byte-identical
(SHA-256 `6e90eda20bc4807f80467c54127ea33065ea60eca59800a57c61a77206e64589`).
Their SYSTEM files differ in **only 16 bytes**, all inside the three 12-byte
name records beginning at zero-based byte 776: `MACROLIB3/TRACK_AX/BASIS_REF`
versus `MAC/TRK/BASIS`. Every other byte agrees. These are the LINK names
written by `ASM.f:84,86,131`, not numerical coefficients. Source review finds
EDIT -3/1 changes output verbosity, not the SPOT equations or stopping tests.

| Three-cell solve | Warm map 1 | Cold diagnostic |
| --- | ---: | ---: |
| k64 | 1.2719027660185727 | 1.2719105545187395 |
| Outer iterations | 6 | 13 |
| EEXT | 2.92894077e-7 | 1.06019038e-8 |
| EUNK / EINR | 1.63279224e-6 | 1.90528769e-6 |

Both satisfy their declared 2e-6 inner solver tests. The observed absolute
inverse-k difference is **4.814413082976365e-6**, or **0.4814413083 pcm**,
9.63 times the outer Rrho gate. This is a same-mesh numerical-repeatability
warning, **not a mesh shift**, certified error bound, noise-floor measurement,
or proof that the coupled gate is unattainable. The cold/hot comparison is
not substituted for the cold/cold mesh comparisons, subsequently completed
for 3, 6 and 12 cells above.

`FLU2DR64.f:364–373` initializes a warm solve from the saved REAL32 `FLUX`
mirror, then promotes it to REAL64; it does not initialize from `FLUX64`.
Cold initialization uses scalar 1 and other components 0. The iteration itself
remains REAL64. Initial-state quantization and finite stopping tolerance are
possible contributors, but their individual effects have not been isolated.
Warm-start inherited leakage metadata has not been independently read from
XSM; no exact all-parser-state equivalence is claimed. A follow-up source
check excludes a change of the effective SPOT operator through **legal**
inherited leakage metadata on this plain TYPE-K path: `FLU2DR64.f:316,322–327`
zeros the working DIFHET and B2, and the source correction at `1630–1642`
requires nonzero B2. TYPE K does not itself erase ILEAK/NMERG/IMERG.
`FLUKEF.f:103–105` may still index these arrays, but its added leakage term
is zero here. This is not a validation of malformed or out-of-range metadata.
No restart handling, tolerance or runtime was changed. Final convergence
validation must not silently equate one terminal PASS with start-independent
accuracy.
