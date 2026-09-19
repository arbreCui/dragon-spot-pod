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
sh validation/d4_reference/run_material_epoch_audit.sh
```
