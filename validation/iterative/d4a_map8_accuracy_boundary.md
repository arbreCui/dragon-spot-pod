# D4-A map-8 convergence and accuracy boundary

Date: 2026-09-04

## Legacy numerical SPOT result

The D4-A rank-two SPOD/Picard calculation reached its predeclared fixed-point
gate at map 8.  The update is direct Picard (`alpha = 1`); no relaxation,
damping, fitted closure, empirical coefficient, clipping, or model correction
is present.  A later material audit found that this run used the legacy
pre-2026-05-27 material procedures: bulk densities multiplied by thermal
volume expansion instead of dividing by it, and the old MOX/EM10 bookkeeping.
It is therefore retained only as a numerical convergence regression and is
not an admissible physical result or OpenMC comparison parent.

- `k = 1.2863778402485850`;
- `Rrho = 6.3952111273302137e-8`;
- `Rleak = 3.4898525208435340e-7`;
- `Ra = 3.4971804373678926e-7`;
- common gate: `5e-7`, classification `VALID_MET`.

The self-contained map-8 artifact is
`validation/artifacts/iterative-d4a-rank2-picard-map8`.  Its closed axial state
has SHA-256
`a55222ac7b2d4b25d27cd7c196ef8c4638c12037bf35410e02f87666bc647a9b`.

## Frozen SPOT observables

The read-only `SPORATE` extraction uses exactly

\[
P_s = \frac{\sum_g\sum_{i\in s}V_i\phi_{i,g}
                 \sum_f\nu\Sigma_{f,i,g,f}}
              {\sum_{s'}\sum_g\sum_{i\in s'}V_i\phi_{i,g}
                 \sum_f\nu\Sigma_{f,i,g,f}}.
\]

It performs no transport solve and changes no state.  For the three equal
50-cm floors (bottom, middle, top), map 8 gives

```text
0.256479949  0.485561517  0.257958535
```

The executable, deck, three inputs and log are frozen under
`validation/artifacts/iterative-d4a-rank2-map8-observables`; its
`result.sha256` rechecks all six files.

## Why the historical direct-3D ladder is not a D4-A reference

The recovered NXT deck is a single reflective pin cell with eight radial
regions and 24 axial mixtures.  D4-A is a 1/12 assembly sector with 132
radial regions and six physical media per floor; its `SPOLIB` axial
MACROLIB therefore contains 18 mixtures.  The two geometries are not the
same problem.

The historical 3D smoke additionally used
`validation/artifacts/iterative-seed/initial_axial_macrolib.xsm`
(`2e01e806683ce25b5771af055112dc86dcf147245abc5a5c3dceac4d9939373a`),
whereas D4-A map 8 uses
`1e77d078943c9bc0c8ad788e2f8a02a0235be97f07e66cbe5cf445fbd67bec97`.
Its smoke value `k = 1.2084794367395231` and the unfinished rung-2 value near
`1.314240` are consequently excluded from every D4-A comparison.  Rung 2
also failed its terminal and is `NO_RESULT`; rung 3 never ran; no accepted
3D flux was saved.

## Current scientific classification

The iteration claim is now closed:

```text
D4A_LEGACY_NUMERICAL_FIXED_POINT = VALID_MET
```

The accuracy claim remains deliberately open:

```text
D4A_PHYSICAL_FIXED_POINT = REBUILD_REQUIRED
D4A_ACCURACY = REFERENCE_MISSING
```

The next reference must reproduce the actual 132-region D4-A assembly
topology (or a demonstrably equivalent full-assembly representation), the
three material states, 0--50--100--150 cm axial interfaces, radial symmetry
conditions and vacuum axial boundaries.  It must export `k` and the same
globally normalized nu-fission production before any difference is formed.
No pin-cell value, partial iteration, fitted normalization, or result-chosen
threshold is admissible.
