# Level 2 — modal transport equivalence

A two-region manufactured problem is solved in a rotated two-mode POD basis.
The projected material matrices are genuinely coupled. The reconstructed
full-rank solution must equal two independent radial 1D SN channel solves.

The same level tests the offline balance-derived radial closure used by the
one-shot method. It verifies its loss/gain sign, normalization invariance,
reflective radial integral balance, and zero-divergence limit with imposed
axial leakage fixed identically to zero.

An independent two-material, three-group, two-fission-component hand
calculation also verifies the final-state P0 source evaluator: compressed
off-group scattering is mapped correctly, self scattering is excluded, and
the snapshot's own eigenvalue is used in the fission source.

Run:

```sh
sh validation/level2/run_level2.sh
```
