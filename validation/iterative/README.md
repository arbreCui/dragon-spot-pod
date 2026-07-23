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
claim. The systematic inner-tolerance sensitivity from the same \(x_0\) was
attempted next and failed its strict radial inner-solver gate. A second outer
return and any long Picard trajectory remain unauthorized.

## Inner-tolerance sensitivity

`inner_sensitivity_map.x2m` preserves the Stage-3 initializer tolerance
\(h=\mathtt{0x350637bd}\) and uses the exact binary32 half
\(h/2=\mathtt{0x348637bd}\) only for the three radial and one returned axial
solve in \(G\). `check_inner_sensitivity_contract.py` locks that schedule
before any refined result is observed.

The runner is

```sh
DRAGON_BIN=/absolute/path/to/Dragon \
GANLIB_LIB=/absolute/path/to/libGanlib.a \
GANLIB_MOD=/absolute/path/to/ganlib/modules \
SEED_DIR=/absolute/path/to/iterative-seed \
BASELINE_DIR=/absolute/path/to/iterative-map1 \
KEEP_WORK=1 \
  sh validation/iterative/run_inner_sensitivity.sh
```

It requires the frozen Stage-3 executable, seeds and five baseline XSM
objects. The basis and complete \(x_0\) archives must be byte identical. If
all five solves terminate strictly, independent Ganlib-only checks recompute
\(\mathcal D_{\rm out,h}\), \(\mathcal D_{\rm out,h/2}\) and
\(\mathcal D_{\rm in}\) component by component and compare the actual radial
leakage, fission-source and eigenvalue inputs bitwise. No scalar score,
relaxation or fitted factor is introduced.

The precise controls and scale-ordering rule are in
`inner_sensitivity_protocol.json`. A fresh \(h/2\) replay is required before
Stage 4 is finally qualified. `KEEP_WORK=1` preserves the first isolated
work directory so its five scientific hashes can be frozen. A replay
reference must contain exactly, in order, the hashes for
`basis_reference.xsm`, `state0_axial.xsm`, `state1_system.xsm`,
`state1_axial.xsm`, and `state1_snapshots.xsm`; arbitrary or partial checksum
lists fail closed.

The machine state is `UNRESOLVED` if any component fails the predeclared
ordering, `PENDING-REPLAY` if all four pass on the first capture, and
`QUALIFIED` only if all four pass again in a fresh isolated replay whose five
scientific files match the frozen reference. Only `QUALIFIED` authorizes
Stage 5.

The first capture did not reach that classification stage. All three radial
fixed-source solves exhausted `MAXOUT=500` with strict `STATE=2`; their final
unknown changes were \(5.03027\times10^{-7}\),
\(5.29329\times10^{-7}\), and \(6.19920\times10^{-7}\), above
\(h/2=2.5\times10^{-7}\). The initializer and returned axial solves passed,
but the written `state1` objects are invalid as \(G_{h/2}(x_0)\).

`check_inner_sensitivity_failure.py` recognizes only this complete,
normal-ending three-plane failure pattern and emits:

```text
CAPTURE INVALID-INNER-NONCONVERGENCE
STAGE4 INVALID
STAGE5 NOT-AUTHORIZED
OUTER-CONVERGENCE NOT-EVALUATED
```

The exact receipt and next short diagnostic are in
[inner_sensitivity_result.md](inner_sensitivity_result.md). Do not increase
`MAXOUT` or rerun the three-plane capture: the next step is to run the
frozen at-most-six-step, single-plane production-map diagnostic described
there.
Its machine-readable controls are
[radial_floor_protocol.json](radial_floor_protocol.json), and the runner is
[run_radial_floor_diagnostic.sh](run_radial_floor_diagnostic.sh).
The preflight reads only the real TRACK, SOURCE, SYSTEM and forensic CAP
objects; it does not fabricate solver outputs. The CAP flux carries
returned-axial \(L_1\) metadata written after its radial solve, whereas that
solve used the unchanged system \(L_0\). Thus only CAP leakage metadata is
excluded. The final audit still requires every newly produced arm/probe flux
to carry system \(L_0\) bit for bit before it reports either one-step defect.
