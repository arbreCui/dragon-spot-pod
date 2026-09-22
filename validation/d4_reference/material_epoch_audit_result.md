# D4-A material-epoch audit

Date: 2026-09-04

## Result

`PASS_REVIEWED_MATERIAL_INPUT_NO_TRANSPORT`.

The SPOT material procedures now match the independently reviewed production
copies byte for byte:

- `rnr_cc.c2m`:
  `594e9e58aae950b003bd410440928c97b59cf67f70844033c69c05b78e8565b5`;
- `rnr_interpol.c2m`:
  `255ddfc61a61026e0f36aefe5ad4cee0b41871fdbd25e2b77c540bd9bccb8ed2`.

The corrected physics consists of decreasing bulk density with thermal volume
expansion, MOX O/M `1.98`, fuel compaction `0.955`, heavy-metal mass
bookkeeping, sodium-temperature interpolation for `a_AIM1_Na`, and EM10 Fe
mass fraction `0.8908`.  No SPOD equation, rank, Picard update, convergence
threshold or fitted parameter changed.

A standalone Dragon calculation called only `rnr_interpol` and `rnr_cc` at
fuel/clad/sodium temperatures `750/620/475 C`.  It reproduced the reviewed
printed atom-density anchors exactly:

```text
N_Na          = 2.237345e-02
N_U8          = 1.881861e-02
N_Pu39        = 2.747854e-03
N_O           = 4.719196e-02
N_Fe56_AIM1   = 5.000890e-02
```

No cross-section library or transport module was invoked.  Reproduce with:

```sh
OPENMC_PYTHON=/path/to/openmc-python sh validation/d4_reference/run_material_epoch_audit.sh
```

## Three-temperature comparison (2026-09-22)

The material-only deck now evaluates `650/620/475`, `750/620/475` and
`850/620/475 C`. The bounded canonical Dragon run and comparator both passed;
no cross-section library, tracking or transport module was invoked. The
canonical Dragon and reviewed production material-source hashes are unchanged.

All 59 material/nuclide densities actually used by the six-medium CE model
are reported at each temperature (177 comparisons). The unused fertile
outputs `N_U5_f/N_U8_f/N_O_f` are excluded explicitly. The CE builder agrees
exactly with its independent static-checker formulas for this inventory.
The five reviewed 750 C printed SPOT anchors above remain unchanged.

| fuel temperature (C) | maximum relative SPOT-print/CE difference | maximum absolute difference (atoms/b-cm) |
|---|---:|---:|
| 650 | `6.02742707e-7` | `6.89356893e-9` |
| 750 | `6.02742707e-7` | `6.52396441e-9` |
| 850 | `6.02742707e-7` | `6.52396441e-9` |

The largest relative difference is `N_Cr52_AIM1` in each state. These are
REAL32 calculated/printed SPOT values versus binary64 CE formula values,
not bitwise-equal quantities. Differences are **REPORTED_ONLY**, with no new
material-agreement tolerance or pass threshold. The printed half-quantum is
shown per value but does not bound the preceding REAL32 arithmetic. PASS
covers complete valid inventory, CE formula consistency and preserved legacy
anchors; it does not assert a new all-temperature numerical-equivalence proof.

The comparator self-test also rejects missing/duplicate values, incomplete
or incorrect states, invalid densities, altered legacy anchors and duplicate
normal terminations. The full 177-row local report is
`validation/artifacts/d4a-three-temperature-material-audit-20260922.log`,
SHA-256 `c354a046da0deb2117ab566c8cd5344bfbd05baf440364a4f7a8652af33b60c6`.
