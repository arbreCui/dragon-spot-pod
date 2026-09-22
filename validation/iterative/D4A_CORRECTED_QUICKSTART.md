# Corrected D4-A minimal user path

This page is the shortest reproducible route from a clean checkout to the
corrected-material D4-A rank-two SPOD/Picard validation.  It does not change
the physics, rank, tolerances, or iteration method.

## Current release boundary

The corrected 132-region, 370-group snapshot archive is admitted for the
three frozen material states `(650,620,475)`, `(750,620,475)`, and
`(850,620,475)` degrees C.  Its SHA-256 is
`9c46b034a22235e1b410614579028f150588c17d9938f7591b3137327495d294`.
The admitted rank-two basis SHA-256 is
`b372e94165b68cc2ecf53768dfe5bb0c190b70908558e186ed74a297911aeab2`.

Bootstrap is admitted.  The axial seed and all three REAL64 fixed-source
radial refreshes completed, and the strict B2I seal published `CLOSED/0` with
`closed_axial.xsm`, `closed_snapshots.xsm`, and
`d4a_bootstrap_result.sha256`.  Corrected-material maps 1 through 8 completed
both half-steps and passed their independent audits.  Map 8 is `CLOSED/8` and
`VALID_NOT_MET`, with `R_rho=1.0492739930256789E-06`,
`R_L=3.1031397842917180E-06`, and `R_a=1.3106218716376795E-05`. The following
map-9 attempt was interrupted; its partial directory is not a restart parent.
A fresh series from frozen map 8 was stopped early on 2026-09-23 after its
implicit build changed the frozen executable identity. The original binary
was restored and runtime builds removed. A separately approved continuation
has now started from map 8 with the unchanged binary, bounded to maps 9–12,
first MET or failure. No new map has completed. The
[handoff](d4a_final_validation_handoff.md) records both attempts. No
corrected-material fixed point, final `k`/power result, or CE comparison may
yet be claimed.  Frozen evidence is in
[the map-1 result](d4a_corrected_map1_result.md),
[the map-2 result](d4a_corrected_map2_result.md),
[the map-3 result](d4a_corrected_map3_result.md),
[the map-4 result](d4a_corrected_map4_result.md),
[the map-5 result](d4a_corrected_map5_result.md),
[the map-6 result](d4a_corrected_map6_result.md),
[the map-7 result](d4a_corrected_map7_result.md), and
[the corrected map-8 result](d4a_corrected_map8_result.md).

## 1. Build and run the short gate

The current scripts are macOS/arm64-specific and expect `gfortran`, `gcc`,
Python 3, `rg`, `sha256sum`, and `shasum` on `PATH`.

This is a setup-only step, before restoring the canonical executable and
before starting any Picard series. Do not run these build/setup commands
while the main calculation is active. The safe order is: finish setup,
restore and verify the independent canonical binary, run the non-compiling
series/one-map route, stop at the first `VALID_MET`, then independently
accept the result.

The scientific acceptance receipt also pins the exact Dragon executable used
to build the corrected snapshots. A source rebuild is required for the local
libraries and tests, but it is not expected to reproduce that Mach-O file
byte-for-byte on another checkout path or toolchain. The corrected release
asset must therefore supply the 9,147,176-byte canonical Dragon with SHA-256
`2908cf383be163cb0534847fe7115d42c9deed97684c28abdd9c29f24c6722db`.
It requires the macOS arm64 Homebrew GCC 15.2.0 runtime at the standard
`/opt/homebrew/opt/gcc` prefix. The binary and large XSM inputs remain outside
Git; neither may be silently replaced by a locally different build.

```sh
cd /absolute/path/to/spot
make -C src -j2
make -C validation/iterative -j2
make spot-fast
```

The last command is transport-free.  Continue only after it ends with
`SPOT ACTIVE FAST PASS`.

## 2. Restore and verify the sealed CLOSED/0 runtime

The large XSM files and canonical Dragon are deliberately not stored in Git.
They must be published together as a hash-pinned project release asset before
this is a portable clean-checkout path. The locally verified replacement
archive is `d4a-corrected-closed0-runtime-repacked-20260923-9c59ef8.tar`,
with outer SHA-256
`2d50b1647184293657cff95c2b69ad5874e60622cb8d3ed136ef8dcc1fdc4649`.
It preserves the original payload and inner manifests; the old temporary
20260920 tar is no longer available, so its outer hash must not be used for
this new archive. The replacement contains 39 **flat top-level files**, not
an enclosing directory. Verify it before extracting into a fresh directory:

```sh
ARCHIVE=/absolute/path/to/d4a-corrected-closed0-runtime-repacked-20260923-9c59ef8.tar
ART=/absolute/path/to/fresh-closed0-runtime
(
set -eu
test "$(shasum -a 256 "$ARCHIVE" | awk '{print $1}')" = \
  2d50b1647184293657cff95c2b69ad5874e60622cb8d3ed136ef8dcc1fdc4649
test ! -e "$ART" && test ! -L "$ART"
mkdir "$ART"
tar -xf "$ARCHIVE" -C "$ART"
)
```

The release asset starts from the already sealed `CLOSED/0`; it does not
rebuild the three snapshots from a raw nuclear-data library.  It contains
exactly the 38 payload files named in
`d4a_closed0_release.sha256`, plus that receipt itself.  Verify it before
installing Dragon:

```sh
sh validation/iterative/check_d4a_closed0_release.sh --verify "$ART"
```

Release maintainers generate this inventory, without copying any data, from
the admitted local CLOSED/0 directory and the canonical Dragon with
`check_d4a_closed0_release.sh`:

```sh
sh validation/iterative/check_d4a_closed0_release.sh \
  "$LOCAL_CLOSED0" "$CANONICAL_DRAGON" > d4a_closed0_release.sha256
```

The frozen 38-payload manifest currently has SHA-256
`47652f10fd946473d39ff74384caaf977d56655f12ddfff727229038988e1eaf`.
Together with the manifest, the runtime bundle contains 39 regular files and
no symbolic links or subdirectories.  A public retrieval location is still
pending.

The replacement tar and checksum are currently local under
`validation/artifacts/d4a-runtime-restore-rehearsal-20260923/`.
The independent restore rehearsal verified all 39 files, separate inodes
without source hard links, and byte-identical read-only map-8 checker logs
from a separate checkout. Five prebuilt host tools were copied separately
for that rehearsal; they are not archive members and do not replace the
source-build setup in step 1. This proves local binary/data restoration on
the stated macOS/Homebrew environment, not a new clean-source build,
cross-platform portability, final convergence, or a public release. Detailed
evidence is in that directory's `restore_rehearsal.md` and `verification.log`.

The 769 MB `DLIB8R1_370` target and its absolute symbolic link are not release
payloads.  Its hash remains inside `executed_inputs.sha256` as inert upstream
provenance; the runtime manifest never dereferences it, and Picard and
acceptance do not read it.

Install and verify the release binary after the local source build and only
when no main calculation is running. The working binary must be an
independent regular copy, not a symbolic link or hard link to the release
copy. Use `install` (or an independent copy); never use `ln` for this restore.
The alias checks below fail closed if the destination is already linked to
the published binary:

```sh
(
set -eu
test "$(shasum -a 256 "$ART/Dragon" | awk '{print $1}')" = \
  2908cf383be163cb0534847fe7115d42c9deed97684c28abdd9c29f24c6722db
test ! -L bin/Darwin_arm64/Dragon
test ! "$ART/Dragon" -ef bin/Darwin_arm64/Dragon
install -m 755 "$ART/Dragon" bin/Darwin_arm64/Dragon
test ! -L bin/Darwin_arm64/Dragon
test ! "$ART/Dragon" -ef bin/Darwin_arm64/Dragon
test "$(shasum -a 256 bin/Darwin_arm64/Dragon | awk '{print $1}')" = \
  2908cf383be163cb0534847fe7115d42c9deed97684c28abdd9c29f24c6722db
)
```

At present the only known copies are local to the development machine under
`validation/artifacts/`; no repository retrieval instruction exists yet. A
clean checkout therefore stops here until that bundle is supplied.
Verification of a supplied bundle is read-only:

```sh
(
  cd "$ART"
  sha256sum -c admitted_snapshot_archive.sha256
  sha256sum -c d4a_rank2_admitted.sha256
  sha256sum -c d4a_bootstrap_result.sha256
  test "$(sha256sum d4a_snapshots.xsm | awk '{print $1}')" = \
    9c46b034a22235e1b410614579028f150588c17d9938f7591b3137327495d294
  test "$(sha256sum d4a_rank2_basis.xsm | awk '{print $1}')" = \
    b372e94165b68cc2ecf53768dfe5bb0c190b70908558e186ed74a297911aeab2
  rg -q '^D4A-SNAPSHOT ARCHIVE GANLIB-ONLY PASS$' snapshot_check.log
  rg -q '^D4A-RANK2 GANLIB-ONLY PASS$' d4a_rank2_check.log
  rg -q '^SPOT-R64 B2I BOOTSTRAP COMMITTED CLOSED/0$' b2i_bootstrap.log
)
```

## 3. Select the sealed map parent

The runtime begins at the verified `CLOSED/0` state; no transport is rerun in
this step:

```sh
BOOT="$ART"
test -s "$BOOT/closed_axial.xsm"
test -s "$BOOT/closed_snapshots.xsm"
test -s "$BOOT/d4a_bootstrap_result.sha256"
rg -q '^SPOT-R64 B2I BOOTSTRAP COMMITTED CLOSED/0$' \
  "$BOOT/b2i_bootstrap.log"
(cd "$BOOT" && sha256sum -c d4a_bootstrap_result.sha256)
```

## 4. Run one direct Picard map

Only after the sealed `CLOSED/0` verification above:

```sh
MAP1=/absolute/path/to/fresh-d4a-map1
test ! -e "$MAP1"
: "${RADIAL_LIMIT_SECONDS:?set the authorized radial wall limit}"
: "${AXIAL_LIMIT_SECONDS:?set the authorized axial wall limit}"
RADIAL_TIMEOUT_SECONDS="$RADIAL_LIMIT_SECONDS" \
AXIAL_TIMEOUT_SECONDS="$AXIAL_LIMIT_SECONDS" \
  sh validation/iterative/run_d4a_rank2_picard_map.sh "$BOOT" "$MAP1"
```

The runner evaluates one unchanged direct map and then runs the independent
one-map checker and the three-defect convergence gate.  It introduces no
relaxation, damping, fitted coefficient, clipping, or empirical parameter.
It selects the required `--reencoded` audit for `CLOSED/0` and `--continued`
for later sealed epochs from the B2J receipt. The current one-map runner
checks the canonical binary and prebuilt host tools without compiling them.
Missing tools must be prepared during setup, not during an active series.

The historical `resume_d4a_rank2_picard_after_radial.sh` is not available for
this run and is not a recommended recovery entry point. Unlike the current
one-map runner, it still automatically builds `src` and the host tools and
can replace the hash-locked canonical executable. Its source is retained
for history only. If a run stops after the radial half-step, preserve its
partial directory as evidence; do not invoke that legacy script or use the
partial directory as a restart parent. This quickstart provides no new
partial-run recovery branch.

## 5. Check and continue

The result checker is already part of the one-map runner.  Accept a map only
if these checks pass:

```sh
(
  cd "$MAP1"
  shasum -a 256 -c input_manifest.sha256
  shasum -a 256 -c output_manifest.sha256
  rg -q '^ONE-MAP-XSM COMPLETE$' independent_check.log
  rg -q '^SPOT-GATE COMPLETE$' gate.log
  rg '^CLASSIFICATION=VALID_(MET|NOT_MET)$' gate.log
)
```

Every completed raw map must be frozen before it can be used as a parent:

```sh
MAP1_PORTABLE=/absolute/path/to/fresh-portable-d4a-map1
sh validation/iterative/freeze_d4a_corrected_map.sh \
  "$BOOT" "$MAP1" "$MAP1_PORTABLE"
(cd "$MAP1_PORTABLE" && shasum -a 256 -c result.sha256)
```

Stop when the portable copy is labelled `CONVERGED_MAP`.  Only a
`VALID_NOT_MET` copy labelled `NEXT_MAP_PARENT_ONLY` may feed the next direct
Picard map.  The raw map directory must never be used as that parent:

```sh
rg -q '^MAP_CLASSIFICATION=VALID_NOT_MET$' \
  "$MAP1_PORTABLE/portable_classification.txt"
rg -q '^PORTABLE_ROLE=NEXT_MAP_PARENT_ONLY$' \
  "$MAP1_PORTABLE/portable_classification.txt"
MAP2_RAW=/absolute/path/to/fresh-d4a-map2-raw
RADIAL_TIMEOUT_SECONDS="$RADIAL_LIMIT_SECONDS" \
AXIAL_TIMEOUT_SECONDS="$AXIAL_LIMIT_SECONDS" \
  sh validation/iterative/run_d4a_rank2_picard_map.sh \
  "$MAP1_PORTABLE" "$MAP2_RAW"
MAP2_PORTABLE=/absolute/path/to/fresh-portable-d4a-map2
sh validation/iterative/freeze_d4a_corrected_map.sh \
  "$BOOT" "$MAP2_RAW" "$MAP2_PORTABLE"
```

Do not reuse a failed or partial directory, change the fixed basis, loosen a
gate, or add a coefficient to force acceptance.

### Recommended serial controller

The thin serial controller performs exactly the one-map, check, freeze and
continue sequence above, using the prebuilt tools and hash-locked canonical
binary. It does not compile at runtime; do not rerun setup while it is active:

```sh
SERIES_ROOT=/absolute/path/to/fresh-picard-series
: "${MAX_MAPS:?set a finite operational map bound}"
RADIAL_TIMEOUT_SECONDS="$RADIAL_LIMIT_SECONDS" \
AXIAL_TIMEOUT_SECONDS="$AXIAL_LIMIT_SECONDS" \
  sh validation/iterative/run_d4a_rank2_picard_series.sh \
  "$BOOT" "$BOOT" "$SERIES_ROOT" "$MAX_MAPS"
```

Its four arguments are `corrected-build`, `initial-parent`,
`fresh-output-root`, and `max-maps`.  The initial parent may be the corrected
`CLOSED/0` build or a sealed `NEXT_MAP_PARENT_ONLY` portable map.  `max-maps`
is only a finite execution guard; it does not alter the Picard map, physics,
rank, or convergence gate.  Exit status 3 means
`MAX_MAPS_REACHED / NO_CONVERGENCE_CLAIM`.  The controller never retries a
failed map and stops immediately at the first frozen `VALID_MET` map.

## 6. Extract and independently replay the final observables

Only the first frozen `VALID_MET` portable map is a final state. Extract its
eigenvalue and globally normalized bottom/middle/top nu-fission production
without another transport solve:

```sh
FINAL=/absolute/path/to/the-first-valid-met-portable-map
OBS=/absolute/path/to/fresh-corrected-observables
TIMEOUT_SECONDS=10 \
  sh validation/iterative/run_d4a_corrected_final_observables.sh \
  "$BOOT" "$FINAL" "$OBS"
```

Then rerun the complete lineage gate. Pass every map exactly once and in
epoch order; the example below has three maps:

```sh
D4A_OBSERVABLES_DIR="$OBS" \
  sh validation/iterative/check_d4a_corrected_acceptance.sh \
  "$BOOT" "$MAP1_PORTABLE" "$MAP2_PORTABLE" "$FINAL"
```

Acceptance reruns the canonical read-only `GREP + SPORATE` extraction from
the sealed XSM state with the corrected-build Dragon identity. The saved and
replayed `k` and floor-power records must be byte-identical; a self-hashed
edited log is not evidence.

After that acceptance passes, export the sealed machine-readable result and
verify its receipt:

```sh
RESULT=/absolute/path/to/fresh-corrected-result
python3 validation/iterative/export_d4a_corrected_result.py \
  "$FINAL" "$OBS" "$RESULT"
(cd "$RESULT" && shasum -a 256 -c export_result.sha256)
```

`export_result.sha256` seals `result.json` and `power.csv`.  The exporter is
read-only and refuses a map that is not the frozen `VALID_MET/CONVERGED_MAP`.

## 7. Freeze a completed map for transfer

The map runner uses seven absolute input links to avoid duplicating large
files while it runs.  After a map has completed, make a portable copy without
rerunning either transport solver:

```sh
PORTABLE=/absolute/path/to/fresh-portable-map1
sh validation/iterative/freeze_d4a_corrected_map.sh \
  "$BOOT" "$MAP1" "$PORTABLE"
(cd "$PORTABLE" && shasum -a 256 -c result.sha256)
```

The freezer first verifies the corrected bootstrap receipt, requires exactly
the runner's eight input and six output receipt entries, and checks that the
basis, route contract, radial tracking, axial tracking, and axial macrolib are
byte-for-byte identical to that corrected bootstrap.  It also requires
complete independent-check and convergence-gate logs.  It then copies the
seven absolute linked inputs by value, refuses any remaining link, records
their original paths in `symlink_provenance.tsv`, and seals every regular file
in `result.sha256`.  The source map is read-only and the output directory must
not exist.

The freezer does not trust the copied checker text by itself.  With
`CHECKER_DIR` defaulting to `validation/iterative`, it reruns
`check_one_map_xsm` in the `--reencoded` or `--continued` mode sealed by the
B2J epoch receipt, then reruns `check_convergence_gate` on the packaged map
state and requires both outputs to match the source logs byte for byte.  It
also requires the canonical, unique termination records in `prepare.log`,
`admission.log`, and `close.log`.

`portable_classification.txt` states the role of the copy.  A
`VALID_NOT_MET` map is labelled `NEXT_MAP_PARENT_ONLY` and is not evidence of
final convergence; it may only feed the next unchanged Picard map.  Only a
`VALID_MET` map is labelled `CONVERGED_MAP`.

After the complete ordered lineage has already ended with
`D4A-CORRECTED-ACCEPT OVERALL PASS` and that first `VALID_MET` map has been
frozen as `CONVERGED_MAP`, its existing values may be formatted for downstream
tools without another solve:

```sh
FINAL_PORTABLE=/absolute/path/to/frozen-first-valid-met-map
RESULT_EXPORT=/absolute/path/to/fresh-result-export
python3 validation/iterative/export_d4a_corrected_result.py \
  "$FINAL_PORTABLE" "$OBS" "$RESULT_EXPORT"
(cd "$RESULT_EXPORT" && shasum -a 256 -c export_result.sha256)
```

This exporter only formats and seals the already accepted map and observables
receipts as `result.json` and `power.csv`. It does not run transport and does
not replace `check_d4a_corrected_acceptance.sh`.

## 8. Run the matching independent CE production

After the corrected SPOD lineage reaches its first independently accepted
`VALID_MET` map, use the sole production entry point. The wrapper owns the
frozen statistical controls and process-group wall cap; do not invoke the
builder's production mode directly:

```sh
CE_PRODUCTION=/absolute/path/to/fresh-ce-production
/path/to/openmc-python validation/d4_reference/run_d4a_ce_production.py \
  --output "$CE_PRODUCTION" \
  --cross-sections /absolute/path/to/cross_sections.xml \
  --openmc-exec /absolute/path/to/openmc
```

The production particle count, batches, inactive batches, seed, threads and
OpenMC executable are frozen in
`validation/d4_reference/d4a_ce_production_protocol.md`; they are execution
and statistical controls, not fitted SPOD parameters. A production result is not
accepted until its sealed statepoint, OpenMC runtime identity, continuous-
energy mode, final batch, realization count and 651-cell tally all pass the
independent receipt checker described in
`validation/d4_reference/README.md`.

## Files that must be published with the source revision

At minimum, the clean-checkout revision must contain:

- corrected snapshot inputs and guards: `data/SpotD4Snap.c2m`,
  `data/SpotD4Tone.c2m`, `data/rnr_0burn_spot_proc/rnr_cc.c2m`,
  `data/rnr_0burn_spot_proc/rnr_interpol.c2m`,
  `validation/iterative/d4a_snapshot_inputs.sha256`,
  `d4a_three_snapshots.x2m`, `preflight_d4a_three_snapshots.sh`,
  `run_d4a_three_snapshots.sh`, `run_d4a_snapshot_check.sh`, and the two D4-A
  snapshot/basis checker sources;
- the fixed-basis/seed route: `d4a_rank2_basis.x2m`,
  `run_d4a_rank2_basis.sh`, `d4a_axial_seed.x2m`, and
  `run_d4a_axial_seed.sh`;
- the bootstrap route: `data/SpotRefR64.c2m`,
  `data/SpotPlaneR64.c2m`, `SPOR64_RCONTRACT.f90`,
  `make_route_contract.f90`, `b2i_seal_bootstrap.f90`,
  `d4a_refresh_r64.x2m`, and `run_d4a_rank2_bootstrap.sh`;
- the one-map route: `data/SpotStepR64.c2m`,
  `d4a_rank2_picard_radial.x2m`, `d4a_rank2_picard_axial.x2m`,
  `d4a_rank2_checker_parent.x2m`, `run_d4a_rank2_picard_map.sh`,
  `run_d4a_rank2_picard_series.sh`, `freeze_d4a_corrected_map.sh`,
  `test_d4a_picard_series.py`, and
  the `prepare`, `admit`, `close`, one-map, and convergence checker sources;
- the final-result route: `d4a_corrected_final_observables.x2m`,
  `run_d4a_corrected_final_observables.sh`,
  `verify_d4a_corrected_observables.sh`,
  `test_d4a_corrected_observables_replay.sh`,
  `export_d4a_corrected_result.py`,
  `test_export_d4a_corrected_result.py`, and
  `check_d4a_corrected_acceptance.sh`, plus the runtime release checker
  `check_d4a_closed0_release.sh`;
- the independent CE route under `validation/d4_reference/`;
- all current SPOR64/REAL64 production-source changes used by those decks,
  the regenerated `src/.dragon_deps.mk`, the iterative `Makefile`, and every
  source/script newly referenced by `validation/run_fast.sh`.

The corrected D4-A source, decks, runners, host tools and fast-gate tests in
those groups are tracked.  A clean checkout still needs the separately
published sealed runtime asset described above; local historical diagnostics
and map outputs are not part of the release source.

The tracked `resume_d4a_rank2_picard_after_radial.sh` remains a historical
source file, not an enabled entry point in the current release route; its
automatic builds make it unavailable for the hash-locked run described here.

## Files that must remain outside Git

- the hash-pinned canonical Dragon executable, published as release data;
- locally compiled Dragon/Ganlib libraries and all other executables;
- compiled iterative host tools, including `b2i_seal_bootstrap` and
  `make_route_contract`;
- XSM databases, `TRACK_f`, copied CLE-2000 procedures, logs, and map output
  directories;
- the complete corrected artifact bundle under `validation/artifacts/`.

The first two new host-tool binaries need exact `.gitignore` entries; their
`.f90` sources must be tracked.  Do not add a broad `*.xsm` rule: the existing
`validation/artifacts/` rule is sufficient for the large validation bundle.
