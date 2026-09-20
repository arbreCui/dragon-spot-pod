# Corrected D4-A direct-Picard map 2

## Classification

The second corrected-material rank-two SPOD map advanced the admitted state
from `CLOSED/1` to `CLOSED/2` with the unchanged online-radial/reduced-axial
map and direct Picard update (`alpha=1`).  Radial admission, the axial solve,
the B2W close, and the independent one-map audit all passed.  The unchanged
three-defect gate reported:

```text
R_rho = 3.6459412816532977e-3
R_L   = 9.0610645253661557e-3
R_a   = 9.6262337831960823e-3
gate  = VALID_NOT_MET
```

All three defects decreased from map 1, but none meets the predeclared
`5e-7` gate.  This is a valid Picard state, not a corrected-material fixed
point, and it must not be quoted as the final D4-A result.

## Lifecycle

The radial solve completed all three planes and published a production-
admitted `RETURNED/2` state.  The axial solve then ended normally, B2W
published `CLOSED/2`, and the independent checker reproduced the saved
state and defects.  No recovery route, repeated radial solve, relaxation,
damping, fitted coefficient, clipping, rank change, or tolerance change was
used.

The portable copy contains no symbolic links and is labelled
`NEXT_MAP_PARENT_ONLY`.  It is the only admitted parent for the unchanged
map-3 continuation.

## Frozen receipt hashes

```text
input_manifest.sha256       342ec20abe2e617f377d99bdf5b0496f403b0341d52dac05d40dc18c56fe973e
output_manifest.sha256      f7c1483e0933c9805413a853755eca40941d91cbb9c1db469221c701ea821072
admission.log               0c64ebbfbc1a390f04fb034deb2d063ebe70148abe72267938ee7335a004518e
close.log                   dee54429b89f9cc9aec4b7bb8299d64ce2d03e078eebbb799a77cda0902437a6
gate.log                    c8da53321e5d9a3a52233f31bb3c1dcd640957c7f1fa62cda6e7163bafaa9869
independent_check.log       0db7dac519f882a1d6102ba00adf8fd102dc00c68aaea346c9dd8067e8715f02
closed_axial.xsm            39982f406ceac23b74210be44fa90bd77f5c059042608802976a1ef6ec6fd5db
closed_snapshots.xsm        4b85becaaef135c079e94c5c05d061fbe512190533702025d00f6cd81a1821f6
portable result.sha256      aac3972114e0c9345d9e3e4ad996552c50503ac95f4830c3381808cabb348ee1
portable_classification.txt 5f8ec4bf3368cef2593e54d0f035ec9a84ae7bb9570feb8ad24a7dc058f709a5
```

The axial deck SHA-256 is
`04fa94bbc296c29ebbdf67a6e439ec33356ef254403deac2a4fa8c8351a1def0`.
The canonical Dragon SHA-256 remains
`2908cf383be163cb0534847fe7115d42c9deed97684c28abdd9c29f24c6722db`.
