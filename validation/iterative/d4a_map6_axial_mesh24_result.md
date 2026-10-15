# D4 map-6 frozen radial operator: 12 versus 24 axial cells

Completed 2026-09-28. Doubling the axial mesh changes reactivity by
**+39.23943 pcm** at the same tighter inner settings. This measures local
mesh sensitivity of one frozen radial operator; it does not establish mesh
convergence of the coupled method or explain the full SPOT–CE discrepancy.

## Controlled comparison

The twelve-cell baseline is the completed `cold_tight` case from the
[initial-guess study](d4a_map6_axial_repeatability_result.md). The new case
has 24 cells of 6.25 cm, eight cells in each of the same three material zones.
Both use map-6 radial data and basis, rank 2, SN8, SCAT3, vacuum ends and the
same MACROLIB. EXTE/UNKT/THER thresholds are all 2e-7, with EXTE 500,
REBA OFF and ACCE 3 3. Both start cold. The repaired Dragon executable is an
exact private copy; no active solver or runtime was rebuilt.

The 24-cell geometry, tracking and SYSTEM were built in isolation. A read-only
check verifies all 13 retained radial records in each of 370 groups word for
word against the map-6 SYSTEM, along with the material-zone and thickness
mapping. Building tracking/SYSTEM runs no new radial transport.
The solve had one thread, a 1,200-second cap and no retry.

| Quantity | 12 cells | 24 cells |
| --- | ---: | ---: |
| k64 | 1.2847459873766922 | 1.2853939891896877 |
| Outer iterations | 19 | 22 |
| Wall seconds for axial solve | 222.133 | 433.615 |
| Final EEXT | 1.42257e-8 | 6.28761e-10 |
| Final EUNK / EINR | 1.82633e-7 | 1.53572e-7 |
| Signed source-normalized outward leakage | 0.07726525658 | 0.07674657539 |
| Bottom-zone nu-fission fraction | 0.2619129355 | 0.2618946697 |
| Middle-zone nu-fission fraction | 0.4816459642 | 0.4817796703 |
| Top-zone nu-fission fraction | 0.2564411003 | 0.2563256600 |

Reactivity change is `1e5 * (1/k12 - 1/k24)`. Total leakage falls by
0.05186812 percentage points. Both solves pass all declared inner tests;
all fixed input hashes remain unchanged.

The physical FLUX64 relative volume L2 difference is **0.00127564985**
(0.127565%). Each field has one independently integrated global REAL64
nu-fission normalization. Fine-cell scalar flux is volume-averaged onto
the twelve-cell grid before comparison; variation within coarse cells is
not included in this norm. Three-zone modal summaries give Ra=4.20579e-4.
The maximum absolute leakage-coefficient difference is 2.40372e-4 cm^-1;
dividing it by the largest absolute coefficient across both states gives
Rleak=0.156304. This coefficient metric is distinct from integrated leakage.

## Signed boundary currents

An existing read-only current tracer independently reconstructs all 1,110
zone/group leakage coefficients bit for bit from FLUX64. Its summed boundary
current also agrees with the separate physical comparator to within 1e-14
after normalization. No value was clipped.

| Quantity | 12 cells | 24 cells |
| --- | ---: | ---: |
| Negative bottom outgoing region/group entries | 1,284 | 735 |
| Negative top outgoing region/group entries | 358 | 203 |
| Nonpositive cell scalar-flux entries | 0 | 0 |
| Source-normalized absolute sum of negative outgoing entries | 5.99974e-9 | 6.04848e-10 |
| Negative magnitude / signed net outward current | 7.76512e-8 | 7.88111e-9 |

Refinement reduces these negative endpoint contributions by about one decade
in this comparison. It does not remove every negative entry. Their integrated
magnitude is tiny compared with total leakage; this observation alone is not
an eigenvalue perturbation bound or an attribution of the CE discrepancy.

## Interpretation and retained evidence

The same-grid tight cold/warm difference was 0.02254 pcm; the mesh increment
is much larger. That observed initial-guess sensitivity is not a rigorous
error bar. The old 3/6/12-cell increments of 784.49/156.82 pcm used a different
frozen radial operator, so they cannot be combined with this increment to
infer an order of convergence or a Richardson correction.

`validation/artifacts/d4a-map6-axial-mesh24-20260928/` retains inputs, plans,
decks, native logs, structural and final-result checks, comparisons, signed
current records and `result.sha256`. The first build deck exceeded the CLE
line-length limit and was rejected before module execution; `case24/` is
preserved. The corrected deck only wraps that line, as recorded in
`setup_note.json`. One diagnostic invocation with an overly long XSM path
was also rejected before comparison. Neither failure reran transport.

The mesh checker accepts a `-` axial argument for structural checks and
verifies axial-state/tracking dimensions before examining a saved solution.
A deliberately mismatched twelve-cell state with 24-cell tracking is refused.
The physical comparator's analytic nested-grid tests pass.

A coupled refinement study remains separate future work. This result does
not change the running coupled chain, its gates or its selected mesh.
