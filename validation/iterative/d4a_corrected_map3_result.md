# Corrected D4-A direct-Picard map 3

## Frozen result

The third corrected-material rank-two SPOD map completed one unchanged
online-radial/reduced-axial direct Picard update with `alpha=1`.  Its portable
receipt verifies, the independent one-map checker ends in `ONE-MAP-XSM
COMPLETE`, and the exact frozen result is:

| item | exact value | source |
|---|---:|---|
| lifecycle | `CLOSED/2 -> PROJECTED/3 -> RETURNED/3 -> CLOSED/3` | `prepare.log`, `admission.log`, `close.log` |
| classification | `VALID_NOT_MET` | `gate.log`, `portable_classification.txt` |
| portable role | `NEXT_MAP_PARENT_ONLY` | `portable_classification.txt` |
| `R_rho` | `1.1768097152373702E-03` | `gate.log` |
| `R_L` | `1.2726421268638940E-03` | `gate.log` |
| `R_a` | `3.1762734075296063E-03` | `gate.log` |
| SHA-256 of `result.sha256` | `4b7d6312602e36dab1c1ee59473379b4dd0b55eaa68ee4a02bcb50da11a231ee` | `shasum -a 256 result.sha256` |

The source is the frozen portable directory
`validation/artifacts/d4a-corrected-material-rank2-map3-portable-detached-20260921`.
Its `result.sha256` verifies all sealed files.

All three defects remain above the unchanged
`4.9999999999999998E-07` gate.  This map is an admitted continuation parent,
not a corrected fixed point, final `k`/power result, or CE comparison.
