# D4-A independent-reference route

## Current decision

The converged map-8 state is not an accuracy parent.  It used the legacy
material procedures and is retained only as a numerical SPOD/Picard
regression.  The corrected physical epoch has now admitted its three radial
snapshots, fixed rank-two basis and `CLOSED/0` bootstrap, but it has not yet
published a corrected fixed point or an accepted independent CE result.
The separately approved early CE run completed on 2026-09-23 in 111.22 s,
but its identity audit rejects a missing statepoint Git attribute in this
OpenMC build. The result is retained, not admitted or rerun; see the
[production result and failure record](d4a_ce_production_result_20260923.md).

The direct `MGXEXP` route is also fail-closed for the present D4-A MACROLIB.
The export is complete and deterministic (`DIM 370 18 3 32`), but the P0
compressed scattering sum differs from `SIGS00` by as much as
`7.2032378e-4` absolute and `3.2405989e-3` relative.  This is too large to
treat as serialization noise.  No renormalization, threshold relaxation or
cross-section correction is allowed, so this export may be kept only as a
diagnostic.

The corrected procedures and a no-transport atom-density check are frozen in
[material_epoch_audit_result.md](material_epoch_audit_result.md).  Run it with

```sh
OPENMC_PYTHON=/path/to/openmc-python sh validation/d4_reference/run_material_epoch_audit.sh
```

The short audit covers all three fuel temperatures and all 59 model
material/nuclide densities per state. It preserves the 750 C legacy anchors
and reports SPOT REAL32 printed values against CE binary64 formulas without
adding a fitted agreement threshold. It needs the existing OpenMC Python
package for material construction only; it does not launch OpenMC transport.

## Shortest admissible reference after the rebuild

Use a continuous-energy OpenMC model of the equivalent complete assembly:

- 217 pins on the exact 1.07 cm hexagonal lattice;
- pin radii 0.11, 0.4225, 0.435 and 0.485 cm;
- frozen wrapper/outer hexagon side lengths 9.2155980, 9.7352133 and
  9.9950209 cm;
- six outer faces with white boundary, equivalent to the TISO 12-fold
  unfolding; no artificial white boundary is placed on wedge planes;
- axial planes at 0, 50, 100 and 150 cm, with vacuum at both ends;
- fuel temperatures 650/750/850 C and clad/sodium temperatures 620/475 C;
- exactly the corrected SPOT material composition, with no fitted parameter.

The first reference smoke will prove geometry construction, particle
tracking and tally readability only.  It will not be reported as an accuracy
result.  A statistical `k` and globally normalized floor/radial nu-fission
comparison is authorized only after the corrected SPOT fixed point exists.

## Repo-local corrected CE driver

The reference path is deliberately limited to four source files:

- [audited_rnr_assembly_base.py](audited_rnr_assembly_base.py): the
  repository-local, hash-locked audited assembly base;
- [build_d4a_ce_reference.py](build_d4a_ce_reference.py): the corrected
  three-floor, 217-pin continuous-energy model builder;
- [check_d4a_ce_static.py](check_d4a_ce_static.py): the independent static
  checker for materials, geometry, boundaries, tallies and source hashes;
- [run_d4a_ce_production.py](run_d4a_ce_production.py): the sole frozen
  production supervisor and process-group wall-cap owner.

The safe default is an input-only build.  It exports and checks the XML model
but does not start OpenMC particle transport:

```sh
python3 validation/d4_reference/build_d4a_ce_reference.py \
  --output /absolute/path/to/fresh-no-run-output \
  --cross-sections /absolute/path/to/cross_sections.xml \
  --no-run
```

The output path must be new.  A successful check ends with both
`D4A CE STATIC PASS` and `D4A CE NO-RUN PASS`; it is not a physics result.
The manifest stores repository sources and neutron-library entries as logical
paths plus SHA-256, not checkout-specific absolute paths.  A moved input or
production directory can replay the static audit against an equivalent local
data installation with

```sh
/path/to/openmc-python validation/d4_reference/check_d4a_ce_static.py \
  /absolute/path/to/moved-ce-directory \
  --cross-sections /local/path/to/cross_sections.xml
```

The supplied index and every model HDF5 must match the original hashes.

Production execution is intentionally separate. The only authorized
production entry is [run_d4a_ce_production.py](run_d4a_ce_production.py), as
documented in
[d4a_ce_production_protocol.md](d4a_ce_production_protocol.md). Its CLI accepts
only a fresh output directory, the nuclear-data index and the OpenMC
executable. It fixes the statistical protocol and 900-second process-group
wall cap internally, so production users do not invoke the builder's `--run`
mode directly. No corrected CE production result has yet been accepted.

Before transport starts, the driver resolves the real OpenMC executable and
seals its resolved path identifier, file SHA-256, exact `--version` text and
text hash, parsed version and available Git SHA.  It also seals the OpenMC
Python package version, installation-root identifier, hashes of the critical
reader/executor modules and a relocation-stable hash of all package Python
sources.  These records live in the hash-sealed model contract.

An eventual result is admissible for comparison only when its reported
eigenvalue uncertainty satisfies

```text
sigma_pcm = 1e5 * sigma_k / k_CE^2 <= 50 pcm.
```

After the corrected SPOT fixed point also passes its own gate, compare the
two eigenvalues in reactivity using the frozen criterion

```text
1e5 * abs(1/k_SPOT - 1/k_CE) <= 500 pcm + 3*sigma_pcm.
```

The CE floor and pin nu-fission tallies remain globally normalized
observables; they are not fitted to the SPOT result.

### Read-only pin-rate readiness

The final SPOT state already contains reconstructed physical-region flux.
`SPORATE` integrates `VOLUME * FLUX[KEYFLX] * NUSIGF` before combining regions
into floors. Retaining the radial-region index can therefore yield regional
nu-fission rates without a new transport solve. The present accepted output
uses the REAL32 `FLUX` mirror; a future extractor must state its precision
explicitly and must not silently change that comparison convention.

Source/topology inspection of the frozen 132-region geometry identifies
25 fuel symmetry orbits: 12 interior orbits of 12 pins, 12 boundary orbits
of 6 pins, and the central pin, totaling 217. SAL preserves region labels
when unfolding and accumulates expanded volumes by those labels. Do not
multiply the saved volume or regional rate by another uniform factor of 12.

This static crosswalk and conservative rate expansion are now implemented.
The saved SAL `GEOMETRY/IPAR/RPAR` and `NXTRecords/NumMerge` topology produce
217 unique CE lattice indices; the rate exporter reads 75 fuel-region/floor
rates and expands them to 651 pin/floor records without renormalization.
The corrected map-8 diagnostic reproduces the existing SPORATE floor output
and passes the static/short synthetic checks. It is not a converged result:
see [the diagnostic result and minimal commands](d4a_pin_diagnostic_result.md).
Nu-fission rates are not absolute thermal power. The saved-state tools also
reproduced all eight diagnostic outputs byte-for-byte from a clean-source
build of their actual dependency closure (Ganlib plus SPORATE, not a full
Dragon product build).

The read-only pin comparator is ready, with 14 synthetic tests passed:

```sh
python3 validation/d4_reference/compare_d4a_pin_rates.py \
  /absolute/path/to/pin_rates.csv \
  /absolute/path/to/reference_result.json \
  /absolute/path/to/new-pin-comparison-directory
python3 validation/d4_reference/test_compare_d4a_pin_rates.py
```

It joins all 651 records by `(floor,pin_index)` and reports absolute global
fraction differences, their maximum location and RMS without renormalizing.
Outputs are `DIAGNOSTIC_ONLY / REPORTED_ONLY`: the tool does not authenticate
receipts, establish convergence, or apply a pin-accuracy criterion. Raw CE
tally standard deviations do not supply normalized-fraction uncertainty,
because the common denominator introduces covariance. No fraction sigma or
sigma-based pin verdict is invented. Final-state extraction and a comparison
against an actual accepted CE production result remain to be completed.

Once both production receipts exist, perform the sealed, read-only comparison
with the full corrected SPOT lineage and an explicit local location for the
same hash-sealed CE nuclear-data index.  Repeat `--spot-map` in epoch order:

```sh
/path/to/openmc-python validation/d4_reference/check_d4a_spot_ce_receipts.py \
  --corrected-build /absolute/path/to/corrected-build \
  --spot-map /absolute/path/to/map1 \
  --spot-map /absolute/path/to/map2 \
  --spot-observables /absolute/path/to/sealed-corrected-observables \
  --ce-result /absolute/path/to/sealed-ce-production-result \
  --cross-sections /local/relocated/path/to/cross_sections.xml
```

The checker normally requires the executable at its sealed resolved path.  If
that executable was moved, pass `--openmc-exec /new/path/to/openmc`; this is
the only admitted executable relocation and is accepted only when the file
hash and complete version identity are unchanged.

The checker first calls the authoritative corrected acceptance script on the
build, every ordered map and the observables directory.  Therefore the
snapshot-derived basis, direct-Picard lineage, independent XSM checker,
three-defect `VALID_MET` gate and final observables must all pass again; a
self-hashed text file cannot substitute for an XSM database.

On the CE side it reruns the independent static model audit.  Repository
sources are located by manifest key in the current checkout and verified by
their original hashes.  `--cross-sections` may point to a relocated but
byte-identical index; all 35 referenced HDF5 files are resolved from that
index and checked against the manifest hashes.  The original machine's
absolute source and nuclear-data paths need not exist.

Finally, the checker opens the sealed final statepoint with the OpenMC Python
API, verifies its OpenMC version and exact Git-SHA presence/value against the
sealed executable, continuous-energy
mode, particles/batches/inactive/seed, final current batch, and realization
count against the production contract.  It also requires the named 651-cell
`nu-fission` tally to use the `tracklength` estimator and exactly the
`['total']` nuclide bin before reconstructing every result bin and all three
floor fractions using the declared global sum.  Every JSON floating value
must have the identical Python float round-trip (`float.hex`); no comparison
tolerance is added.  It then applies only the two criteria declared above. Three
floor-power differences are reported for diagnosis with
`status=REPORTED_ONLY`; no power-shape acceptance threshold is introduced.
Its small no-solver synthetic test covers exact reconstruction, one-ULP
rejection, duplicate cell/floor/pin-map rejection, text-XSM rejection and
text-statepoint rejection:

```sh
/path/to/openmc-python validation/d4_reference/test_d4a_spot_ce_receipts.py
```

The production supervisor has a separate transport-free synthetic test for
the exact frozen command and success, nonzero-exit and timeout cleanup paths:

```sh
/path/to/openmc-python validation/d4_reference/test_run_d4a_ce_production.py
```
