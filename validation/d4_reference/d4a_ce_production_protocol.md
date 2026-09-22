# Corrected D4-A CE production protocol

This file freezes the single continuous-energy production run before any
corrected SPOD fixed-point value is available. The controls below determine
Monte Carlo sampling only; they do not change geometry, materials, nuclear
data, temperatures, boundaries, tallies, or the SPOD model.

## Frozen run

```text
particles per batch = 20000
batches             = 300
inactive batches    = 100
active batches      = 200
active histories    = 4000000
seed                = 731942
MPI processes       = 1
OpenMP threads      = 18
operational wall cap = 900 seconds
```

On 2026-09-23 the user explicitly authorized advancing this one production
run before the corrected SPOD lineage reaches `VALID_MET`, to overlap the
independent reference with the already running Picard continuation. This
supersedes only the earlier execution-order restriction. The physical model,
sampling controls, uncertainty gate and wall cap are unchanged. No
automatic retry is authorized. SPOT--CE comparison still requires the first
independently accepted corrected `VALID_MET` map and its complete lineage.

That one run has now completed; its identity audit remains rejected because
this OpenMC build omits the statepoint Git attribute. See the
[production result and failure record](d4a_ce_production_result_20260923.md).
Do not launch it again while resolving this metadata issue.

It is one production run, not a scan:
the seed, batch counts, result, or stopping point must not be selected using
the SPOD eigenvalue or power distribution. A timeout, nonfinal statepoint, or
reactivity uncertainty above 50 pcm is a rejected production result, not a
partial result to splice or tune.

The sole production entry point is the repository wrapper below. It invokes
the canonical builder with its own `sys.executable`; the frozen statistical
controls and wall cap are deliberately not command-line options.

```sh
/Users/wen/miniforge3/envs/openmc-dev/bin/python \
  validation/d4_reference/run_d4a_ce_production.py \
  --output /absolute/path/to/fresh-d4a-ce-production \
  --cross-sections \
  /Users/wen/openmc-workspace/data/endfb-viii.1-hdf5/cross_sections.xml \
  --openmc-exec /Users/wen/miniforge3/envs/openmc-dev/bin/openmc
```

The wrapper enforces the 900-second process-group wall cap. On timeout it
sends `TERM`, waits briefly, then sends `KILL` to any surviving group. A
timeout or nonzero builder exit leaves a `PRODUCTION_INCOMPLETE` marker and
removes any success receipt; no statepoint in that directory is admissible as
the final reference.

## Evidence and limits

The closest available timing/variance evidence is a prior 217-pin,
continuous-energy, white-boundary calculation made with the same OpenMC
commit (`e542b2f035e397a647cc3ad0ae39946b1ad81e7b`). It used 20,000 particles,
250 batches, 50 inactive batches, one MPI process, and 18 OpenMP threads. Its
log reports 171.55 seconds and `k = 1.36944 +/- 0.00034`, corresponding to
about 18.13 pcm under the frozen checker formula.

That historical case is not the present reference: it had one axial layer
and 217 tally bins, and its nuclear-data files were not hash-sealed. It is
used only to size the operational run. The corrected builder independently
hashes the current cross-section index and all 35 used HDF5 files, constructs
three axial floors and 651 unique fuel-cell bins, and seals the exact OpenMC
runtime before transport.

No entropy mesh or fitted source-convergence threshold is introduced. The
initial source is uniform over all fissionable regions and 100 inactive
batches are fixed a priori. The final statepoint retains the full generation
history for reporting; acceptance still requires the declared final batch,
200 active realizations, continuous-energy mode, exact runtime identity, and
the predeclared uncertainty gate.
