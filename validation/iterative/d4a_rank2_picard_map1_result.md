# D4-A rank-2 Picard map 1

This is the first complete D4-A 2D/1D map obtained with the frozen rank-2
SPOD basis and the unmodified radial and axial transport operators. The map
uses the direct Picard update (`alpha = 1`); no relaxation, damping, empirical
coefficient, or closure correction is present.

The radial response, axial solve, lifecycle close, and independent Ganlib
audit all completed. The convergence gate classified the map as
`VALID_NOT_MET`:

| quantity | value |
|---|---:|
| `Rrho` | `4.1571025436368814e-03` |
| `Rleak` | `5.7880183472862237e-02` |
| `Ra` | `1.4615029127716599e-02` |
| `Dleak` (diagnostic) | `1.5443581378951274e-04` |
| maximum relative out-of-span diagnostic | `7.4361542432073856e-08` |

The out-of-span diagnostic is many orders of magnitude below the three outer
fixed-point defects. Rank-2 representation error is therefore not the active
convergence bottleneck after this map. The next admissible action is another
map with the same basis, operators, route contract, and direct Picard update.

Frozen artifacts are stored locally under
`validation/artifacts/iterative-d4a-rank2-picard-map1/`. Their byte hashes are
recorded in that directory's manifests; the lifecycle outputs are:

| artifact | SHA-256 |
|---|---|
| `candidate_axial.xsm` | `5489299132d770b3d44a46b6409431f8f4d2a399ea8bcea25861106e5e39560b` |
| `candidate_snapshots.xsm` | `865c97167ebd0583e3f4e83fbf4f890bb936fb81bb08e59862038c60ba3c0da0` |
| `closed_axial.xsm` | `a67ebcfbcebd7b9d3afc9444c17c03490e17bbde8710a0e3c6969abc83f87d08` |
| `closed_snapshots.xsm` | `8e751757b7b9708920d8a3e47d83e60016c4185578385740189e62fb5ed03d05` |
