# Corrected D4-A direct-Picard map 4

## Frozen result

The fourth corrected-material rank-two SPOD map completed one unchanged
online-radial/reduced-axial direct Picard update with `alpha=1`.  Its portable
receipt verifies, the independent one-map checker ends in `ONE-MAP-XSM
COMPLETE`, and the exact frozen result is:

| item | exact value | source |
|---|---:|---|
| lifecycle | `CLOSED/3 -> PROJECTED/4 -> RETURNED/4 -> CLOSED/4` | `prepare.log`, `admission.log`, `close.log` |
| classification | `VALID_NOT_MET` | `gate.log`, `portable_classification.txt` |
| portable role | `NEXT_MAP_PARENT_ONLY` | `portable_classification.txt` |
| `R_rho` | `3.8371606671805392E-04` | `gate.log` |
| `R_L` | `3.2229791058397219E-04` | `gate.log` |
| `R_a` | `1.0513386117938293E-03` | `gate.log` |
| SHA-256 of `result.sha256` | `f13bcb1c596ce870445ecb238cf09800b4895e8c1ab62113a3a752293598da55` | `shasum -a 256 result.sha256` |

The source is the frozen portable directory
`validation/artifacts/d4a-corrected-material-rank2-map4-portable-detached-20260921`.
Its `result.sha256` verifies all sealed files.

All three defects remain above the unchanged
`4.9999999999999998E-07` gate.  Map 4 is the only admitted parent for the next
unchanged `alpha=1` serial map.  It is not a corrected fixed point, final
`k`/power result, or CE comparison.
