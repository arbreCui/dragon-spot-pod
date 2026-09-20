# Corrected D4-A direct-Picard map 1

## Classification

The first corrected-material rank-two SPOD map completed one unchanged
online-radial/reduced-axial Picard update with `alpha=1`.  The independent
one-map checker passed every bitwise and provenance check.  The unchanged
three-defect gate reported:

```text
R_rho = 9.3496547129074958e-3
R_L   = 5.3754918589220380e-2
R_a   = 2.8817612252911608e-2
gate  = VALID_NOT_MET
```

This is a valid map, not a fixed point.  It must not be quoted as the final
corrected D4-A result.

## Recovery boundary

The radial half-step completed all three planes, ended normally, and passed
the production radial admission gate.  The original run then stopped before
the axial solve because its deck tried to delete an optional absent defect
record.  No failed-directory output was promoted.

The admitted radial products were hash-copied into a fresh directory.  Radial
admission was replayed, the corrected axial deck was run once, and B2W close,
the independent one-map audit, and the convergence gate all passed.  No
radial transport was repeated and no tolerance, rank, model term, relaxation,
or empirical coefficient was changed.

## Frozen receipt hashes

```text
input_manifest.sha256            9a350a40f569cf337313a8008c6ae61f3f7da8fe2a8bdd7b48f64eb10ad4513c
output_manifest.sha256           0ddcaf6724ea2e0cc0604db4aec7e235c812a166f7d6e062d559cfdb833347bb
upstream_radial_manifest.sha256  809fdabc3d21023ea20a2f7bc16c1a6adf4e021d670f82ee034d06a4ff8389b7
recovery_decks.sha256            587356cd9bfe8a19b0d03fa12ae2b2425396921c83c56de61533c7f00860e4e4
gate.log                          8301c9b46e743364e8151b6e45d0ed7c718c9e26f550eff961d477b6eb13ff91
independent_check.log             318ca9511eb2468268702f7e86b203003da6f63dd5381db8fb75300a04b16737
closed_axial.xsm                  a75a1771c47d10ad7a827f1e74fe1e5cd94499ac9d1dae703c293476c6568324
closed_snapshots.xsm              5f07eba1c597c36948ce8486792acdb14b65d0ba681271ab4b8f2c3fb01067f4
portable result.sha256            dca19c7c1deafe491801bd655da0bdd1f0d5c95d75820685d0c436de9002e661
portable_classification.txt       5f8ec4bf3368cef2593e54d0f035ec9a84ae7bb9570feb8ad24a7dc058f709a5
```

The axial deck SHA-256 is
`04fa94bbc296c29ebbdf67a6e439ec33356ef254403deac2a4fa8c8351a1def0`.
The canonical Dragon SHA-256 remains
`2908cf383be163cb0534847fe7115d42c9deed97684c28abdd9c29f24c6722db`.
