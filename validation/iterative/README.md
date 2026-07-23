# Iterative SPOT validation

This directory contains the validation path for
`SPOT_doc/rederivation.md`. It starts from a clean qualification boundary.

## Implementation subgates

The labels 0A/0B/0C below are implementation subgates. They are not the
formal Stage numbers in `SPOT_doc/validation_plan.md`.

Stage 0A freezes the online radial source identity:

\[
q_{\rm FS}=F(Ba)/k+S_{\rm off}(u_\perp).
\]

The fixed fission source is stored on every refreshed radial flux object.
`SPOASM` uses that record for fixed-source snapshots and retains its
final-state eigenvalue source only for offline eigenvalue snapshots. Mixed
snapshot types fail closed.

Run the zero/short-compute check with

```sh
sh validation/iterative/run_stage0a.sh
```

Stage 0B adds the fixed-basis assembly contract:

```text
SYSTEM0 := ASM: MACROLIB3 TRACK_AX SNAP ::
  SPOD rank ;

SYSTEM1 := ASM: MACROLIB3 TRACK_AX SNAP BASIS_REF ::
  SPOD rank FIXB ;
```

`FIXB` copies only the validated POD package from the distinct read-only
`BASIS_REF`; material data and `RADIAL-OP` are rebuilt from the current
snapshot state. Run its static gate with

```sh
sh validation/iterative/run_stage0b.sh
```

The no-transport runtime fixture builds the basis once, enters `FIXB`, and an
independent Ganlib-only checker compares all 370 groups. `VOL2D`, POD basis,
coefficients, singular values, reconstruction/orthogonality records and the
same-snapshot `RADIAL-OP` are bit identical.

Stage 0C defines the canonical physical state variables and raw state
difference:

```text
AXFLUX := SPOSTATE: AXFLUX TRACK_AX SYSTEM_AX MACROLIB3 :: ;
CURRENT := SPOXCONV: CURRENT PREVIOUS :: ;
```

`SPOSTATE` uses one global nu-fission-production normalization, reproduces the
production binary32 plane restriction, solves the stored-basis Gram system,
and reconstructs leakage from face currents. Explicit `SPOPROJ FIXB`
reconstructs the next feedback from \(Ba\); its measured raw off-space
component is diagnostic and is not a hidden map input. `SPOXCONV` rejects a
changed basis bit and reports \(R_\rho\), \(R_L\), absolute \(\Delta L\), and
\(R_a\) separately.

Run the source and manufactured-algebra gate with

```sh
sh validation/iterative/run_stage0c.sh
```

Run all three no-transport executable paths with a Dragon binary built from
the current sources:

```sh
DRAGON_BIN=/absolute/path/to/Dragon \
  sh validation/iterative/run_stage0_runtime.sh
```

The runner verifies the six-file seed against `seed.sha256`, then makes fresh
byte-copies before adding state records. The two stored axial fields exercise
only the residual plumbing; their difference is not claimed to be a
fixed-space map defect.

## One corrected map

`one_corrected_map.x2m` freezes exactly one initializer and one evaluation

\[
x_1=G(x_0).
\]

The evaluated map contains three online radial fixed-source solves, one axial
eigenvalue solve, direct leakage feedback, fixed-basis response assembly and
the raw defect at \(x_0\). It contains no loop or relaxation. Its static
contract is below. The complete deck additionally performs the one archived
initializer axial solve, so the bounded runner executes two axial plus three
radial solves in total.

```sh
python3 validation/iterative/check_one_map_contract.py
```

The bounded runtime gate is

```sh
DRAGON_BIN=/absolute/path/to/Dragon \
GANLIB_LIB=/absolute/path/to/libGanlib.a \
GANLIB_MOD=/absolute/path/to/ganlib/modules \
SEED_DIR=/absolute/path/to/iterative-seed \
VERIFY_REFERENCE=1 \
  sh validation/iterative/run_one_map_runtime.sh
```

`VERIFY_REFERENCE=1` requires the five scientific XSM files to match
`one_map_scientific.sha256`. With an in-tree build, the two `GANLIB_*`
overrides may be omitted.

It verifies the frozen input hashes, runs one initializer plus exactly one
map, checks all five terminal records in that complete deck, and invokes two
independent postprocessors:

- `check_one_map_runtime.py` checks execution structure and declared solver
  termination without assigning an outer threshold;
- `check_one_map_xsm.f90` links only Ganlib, checks the fixed POD package,
  requires a live radial-operator change, and independently recomputes the
  three outer residuals plus \(D_L=\|L^+-L\|_\infty\) bit for bit. It also
  verifies the three-plane restart leakage time ordering.

The first calculation and one fresh replay pass. Their five scientific XSM
containers are byte identical. The frozen controls and evidence boundary are
in `one_map_protocol.json`; exact values and hashes are in
`one_map_result.md`.

This is one deterministic point evaluation of \(G\), not a convergence
claim. The next gate is the systematic inner-tolerance sensitivity from the
same \(x_0\). A second outer return and any long Picard trajectory remain
unauthorized as qualification evidence until that gate is resolved.
