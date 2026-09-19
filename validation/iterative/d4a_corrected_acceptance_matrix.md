# Corrected D4-A end-to-end acceptance matrix

This is the minimum usability gate for the corrected-material D4-A SPOD
route. It adds no transport model, fitted coefficient, relaxation, damping or
rank choice. The gate only reads archived results, verifies their hashes and
replays the existing Ganlib-only checkers. Missing evidence is a failure.

The legacy-material D4-A map sequence is never an admissible substitute. Each
Picard map must be hash-linked to the corrected snapshot-derived rank-two
basis and to the immediately preceding corrected `CLOSED/n` pair.

| stage | required evidence | acceptance condition | current state (2026-09-20) |
|---|---|---|---|
| material epoch | reviewed audit, frozen and executed `rnr_cc`/`rnr_interpol` hashes | both hashes equal the reviewed corrected epoch | **PASS** |
| three snapshots | `admitted_snapshot_archive.sha256`, snapshot checker log | all hashes verify; `(NSNAP,NGRP,NREG)=(3,370,132)`; Ganlib-only PASS; three strict FLU terminals | **PASS** |
| fixed rank two | `d4a_rank2_admitted.sha256`, rank checker log | manifest binds the admitted snapshots; `NMODE=2`; stored diagnostics and Ganlib-only checks pass | **PASS** |
| bootstrap | `d4a_bootstrap_result.sha256`, B2I log | three TYPE-S refreshes; B2I commits the canonical corrected `CLOSED/0`; basis/track/macrolib hashes remain fixed | **PASS**: the existing three TYPE-S responses were admitted without recomputation; B2I committed `CLOSED/0` and the 14-file manifest verifies |
| Picard maps | ordered map directories, input/output manifests and lifecycle logs | exact `CLOSED/(n-1) -> PROJECTED/n -> RETURNED/n -> CLOSED/n` lineage; hashes chain from corrected `CLOSED/0`; live one-map checker replay matches its receipt | **RUNNING**: corrected map 1 has no accepted result yet |
| final residuals | live replay of `check_convergence_gate` on final `closed_axial.xsm` | unchanged AND gate: `Rrho`, `Rleak`, `Ra` all `<=5e-7`; final classification `VALID_MET`; no later map | **FAIL** |
| final k and power | sealed read-only observables directory | manifest binds final axial state/track/macrolib; one `D4A-CORRECTED-K-EFFECTIVE`; three normalized bottom/middle/top `SPORATE NU-FISSION-FRACTIONS`; normal Dragon end | **FAIL** |

Overall current classification: **`FAIL-CLOSED`**. The corrected offline
snapshot/basis construction and coupled bootstrap are accepted; corrected
map 1 is running, so a coupled fixed point has not yet been produced.

## Short deterministic check

The checker never launches Dragon. Build the existing host-side read-only
checkers once, then list corrected maps in epoch order:

```sh
make -C validation/iterative check_one_map_xsm check_convergence_gate
D4A_OBSERVABLES_DIR=/absolute/path/to/final-observables \
  sh validation/iterative/check_d4a_corrected_acceptance.sh \
  /absolute/path/to/corrected-build \
  /absolute/path/to/map1 \
  /absolute/path/to/map2
```

Until map 1 has an accepted result, omit the map and observables options. The
checker then reports the accepted upstream stages through `CLOSED0` and exits
nonzero at maps, which is the intended current-state audit.

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
