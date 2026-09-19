# D4-A rank-2 Picard map 2

Map 2 is a complete, independently checked continuation from the frozen
`CLOSED/1` state. It uses the same rank-2 SPOD basis, route contract, radial
and axial transport operators, and direct Picard update (`alpha = 1`) as map
1. No relaxation, damping, empirical coefficient, or model correction is
present.

The three radial fixed-source responses, production admission, axial solve,
`CLOSED/2` seal, continued-state Ganlib checker, and convergence gate all
completed. Input and output manifests recheck byte-for-byte. The gate result
is `VALID_NOT_MET`:

| quantity | map 1 | map 2 | map 2 / map 1 |
|---|---:|---:|---:|
| `Rrho` | `4.1571025436368814e-3` | `1.1377286940830178e-3` | `0.273683095892` |
| `Rleak` | `5.7880183472862237e-2` | `7.5829611541736930e-3` | `0.131011353095` |
| `Ra` | `1.4615029127716599e-2` | `2.6566931552983479e-3` | `0.181778163566` |
| `Dleak` (diagnostic) | `1.5443581378951274e-4` | `2.0309204170278596e-5` | `0.131505793067` |
| maximum relative out-of-span diagnostic | `7.4361542432073856e-8` | `5.9979171680865659e-8` | `0.806588590274` |

All three gated physical defects contract strongly and in the same direction.
The largest observed ratio is `0.2737`, while the rank-2 out-of-span diagnostic
remains below `6.0e-8`. This is direct evidence that the unchanged physical
Picard map is converging and that POD representation error is not the active
bottleneck at map 2. It is not yet evidence of convergence to the required
`5e-7` gate; the next action is map 3 with the identical method.

The map-2 axial solve reports `k = 1.2860707385301680`. Radial and axial CPU
times were 20573 seconds and 11 seconds, respectively.

Frozen artifacts are stored locally under
`validation/artifacts/iterative-d4a-rank2-picard-map2-attempt2/`. The sealed
lifecycle outputs are:

| artifact | SHA-256 |
|---|---|
| `candidate_axial.xsm` | `67ca2db36500c91caecd7b2064d0d75cbf4f5d44c1bcaaa0a488a55b215a44df` |
| `candidate_snapshots.xsm` | `cdcad824c95a59f28307b84d59066d73eb4d90d81f3e1dececada9f936b27b5b` |
| `closed_axial.xsm` | `987d94e72f6a234c56c6357861e6d38b98083f5e84aa5ec635400eb529d65a5f` |
| `closed_snapshots.xsm` | `ba8b101fa0672cb7327b77a573f6c4b8256ed47a4b68f4fd382e525a893bc1db` |

The first map-2 attempt is separately recorded as `NO_RESULT`: its foreground
supervisor disappeared during plane 3, and no candidate was published. No
partial state from that attempt was reused.
