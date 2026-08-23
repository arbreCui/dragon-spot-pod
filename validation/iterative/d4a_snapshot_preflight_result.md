# D4-A three-snapshot input preflight

## Result

`PASS_NO_TRANSPORT`.

The frozen D4-A snapshot inputs pass their seconds-scale preflight.  The
check executed no Dragon module and produced no physical flux.  Running the
default-off wrapper without explicit authorization repeated the same
preflight and exited before launching Dragon.

```text
D4A SNAPSHOT PREFLIGHT PASS
D4A PHYSICAL STATES C: (650,620,475) (750,620,475) (850,620,475)
D4A ARCHIVE: NSNAP=3 NGRP=370 NREG=132 NMAT=6 NSURF=12 NUNK=144
D4A DLIB SHA256=66b9a7b3e8534a54cf590db63a7c1dbd96b4a95c636f0e3a6eee5b219bbcc1e9
D4A TRANSPORT EXECUTED=0
D4A SNAPSHOT BUILD DISABLED: set RUN_D4A_SNAPSHOTS=1 and an unused RESULT_DIR
```

The frozen repository-input manifest SHA-256 is
`ffac9146159c7271ef51b70045c1ed045a560d8d3028d0a8abb0b142a44e873b`.
The preflight requires the canonical geometry and material procedure hashes
already declared by the D4-A case contract.

## Scope

This freezes and textually checks the declared states, material builder,
370-group library identity, geometry, tracking inputs and three-item archive
recipe before the expensive calculation.  It does not establish physical
compatibility by parsing the library or executing the material/transport
modules.  It also does not prove that TONE or FLU will terminate, that the
archive has physical values, that rank two is adequate for D4-A, or that the
coupled iteration converges.

A read-only census found no existing artifact that combines the canonical
132-region D4-A topology with recoverable 370-group regional flux.  A
historical 750 C log (12,872 bytes, SHA-256
`9f84d885de9526998409c498676aa89f12d60f1833039c5a79424dde1436b254`)
records a normal D4-A TONE/ASM/FLU completion and `k=1.367208`, but the deck
deleted its in-memory flux and exported no XSM.  It is not used as a snapshot
or convergence reference.
