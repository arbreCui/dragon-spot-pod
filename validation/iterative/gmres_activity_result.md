# Passive GMRES activity result

## Result

The committed version-2 runner was explicitly authorized and executed from
commit `83e49163d36c4126fe6531500315c67a0162a78b`. All three bounded processes
ended normally:

| process evidence | exact count |
|---|---:|
| OFF processes | 1 |
| independent ON processes | 2 |
| `MCGMRE` entries / normal exits in each ON process | 1 / 1 |
| PRIMARY role calls / active groups | 1 / 370 |
| AFFINE-RHS role calls | 0 |
| KRYLOV role calls | 0 |
| correction blocks / group-block rows | 0 / 0 |

The PRIMARY MOC evaluation therefore ran for every active group in this
locked one-map path. The residual test immediately after the completed
PRIMARY evaluation then removed all groups from `NCONV` before the
affine-RHS and Krylov section was entered.
The ledger stores no correction block and hence no per-group `KMAX` row.
For that reason the bins `K=0,...,10` are all zero; the `K=0` bin is not
370. `SUM-K 0` and `MAX-K 0` are the frozen schema's empty-census aggregate
encodings; neither denotes an observed per-group `KMAX` value.

The exact classification is

```text
VALID-GMRES-UPDATE-INACTIVE
```

There is no activity threshold. This is an exact control-flow result, not a
preference ranking or a fitted numerical decision.

## Evidence closure

Fresh OFF reproduced the frozen legacy OFF XSM byte for byte. ON-A and ON-B
reproduced one another in their full XSM, normalized log and complete
787-line raw ledger. Their non-audit scientific XSM records reproduced the
legacy ON records. The four independent ledger reads (A, A-repeat, B and
B-repeat) were byte identical.

The independent checker reconstructed the call, role, 370-entry active mask,
empty block census, histogram and classification from raw rows. All 39
payload hashes replayed, inputs were unchanged before and after the run, and
the two artifact-checker passes agreed. The ignored local artifact contains
40 regular files and no extra path, symlink or special file. Its manifest
SHA-256 is
`aeb7d0b4952cea79ed4288ba8e6e27e82d69ae772054f9a0d9a64d57b5e49e22`.

The tracked [compact result](gmres_activity_result.txt) is byte identical to
the artifact result. The public result checker verifies the frozen
dependencies and tracked receipt without Dragon; when the local artifact is
present it also reruns the independent artifact checker.

## Interpretation boundary

This result proves only that the GMRES correction-accumulation path was
inactive for this frozen restart and one-map execution. It does not mean the
PRIMARY MOC evaluation was unused, does not apply automatically to another
restart or later thermal iteration, and does not establish inner, outer or
Picard convergence. It does not explain the earlier nontermination or
attribute it to precision, GMRES, ACA, SCR, rebalancing or acceleration.
Stage 4 remains invalid and Stage 5 remains unauthorized.

A precision A/B limited to the absent GMRES correction update would be an
empty experiment and is therefore abandoned.

## Next evidence step

The narrow next candidate is the `MCGFCS` source arithmetic that was reached
on this locked PRIMARY path for all 370 active groups. It is not assumed to
be unconditionally active for every possible state.

Before another Dragon run, the existing frozen inputs should be replayed
offline in two arithmetic arms:

1. the current binary32 source arithmetic;
2. the same formula after exact promotion of the same stored inputs to
   binary64.

The first question is only whether at least one source-vector element changes
at the retained representation. No improvement threshold, relaxation,
clipping, fit, flux floor or empirical coefficient is allowed. Only a
nonempty offline result can justify separately freezing one short
source-to-MOC runtime A/B; it will not be run automatically.
