# D4-A three-snapshot input preflight

Date: 2026-09-04

## Result

`PASS_STATIC_CORRECTED_MATERIAL_EPOCH_NO_TRANSPORT`.

The seconds-scale preflight passes after synchronizing the reviewed D4-A
material model.  It verifies the three prescribed states, archive layout,
geometry and library identity, and the common radial numerical terminal.  It
does not execute Dragon transport or publish a snapshot.

```text
D4A SNAPSHOT PREFLIGHT PASS
D4A PHYSICAL STATES C: (650,620,475) (750,620,475) (850,620,475)
D4A ARCHIVE: NSNAP=3 NGRP=370 NREG=132 NMAT=6 NSURF=12 NUNK=144
D4A NUMERICAL CONTRACT: MCCG_EPSI=FLU_EXTE=FLU_UNKT=FLU_THER=2e-6
D4A DLIB SHA256=66b9a7b3e8534a54cf590db63a7c1dbd96b4a95c636f0e3a6eee5b219bbcc1e9
D4A TRANSPORT EXECUTED=0
```

The frozen input-manifest SHA-256 is
`32f81d3333e83b8d7c64f0c03d9031469686bcf2e90a258aebcadfecca7097bb`.
The material procedures are pinned to
`594e9e58aae950b003bd410440928c97b59cf67f70844033c69c05b78e8565b5`
and
`255ddfc61a61026e0f36aefe5ad4cee0b41871fdbd25e2b77c540bd9bccb8ed2`.

This is permission to rebuild the three physical snapshots under the corrected
material epoch.  It is not a snapshot result, a fixed-point result or an
accuracy result.  Earlier D4-A snapshots and map 8 remain
`LEGACY_MATERIAL_INPUT / NUMERICAL_REGRESSION_ONLY`.
