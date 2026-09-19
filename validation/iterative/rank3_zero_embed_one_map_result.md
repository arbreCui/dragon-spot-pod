# Rank-3 zero-embedding bounded one-map result

Date: 2026-08-24

## Question

Does the certified rank-2 fixed point remain invariant when it is embedded
exactly in the complete three-snapshot POD space and evaluated by one
unchanged 2D/1D coupled map?

Here, rank 3 means full rank of the three-snapshot space. It is not the
physical full-rank radial oracle.

## 1. Common nested snapshot space

The production `SPOPOD` path was rerun from the frozen inputs:

- raw snapshots: `37656f3269c59db9a5df59ac3686a6da65bc07afa051e2473ffbefadcb2c2b95`
- rank-2 basis: `2d7fc2bf36f65a203731c34dcea18a679fc0232b58c59caad828178a77ff45a8`
- rank-3 basis: `21e22eb011ec194b5e60a133c5c69a288aa29ef86bc7744460adbb62f29c0f55`

The fresh rank-2 result reproduced the frozen rank-2 basis bitwise. The
first two modes and coefficients of rank 3 reproduced rank 2 bitwise.

## 2. Exact rank-2 to rank-3 state embedding

A locally gate-passing rank-2 CLOSED/69 pair was used:

- axial state: `616808e2a655dbf9748bdeba44d8d94e576184cb3fc96960650c65a2e20a077c`
- snapshot archive: `e181870e409c9668c809d05ab1b5a99bdfdb774982f426bf93f3ef55eb10325c`

This temporary pair passed its independent checker, close and convergence
gate, but its directory does not retain the producing Dragon binary, source
revision or complete input/result manifests.  It is therefore a valid local
probe input, not the canonical publication receipt.  The canonical rank-2
result remains `validation/artifacts/r2-leak64-clean-replay/`.

The first two coordinates were copied bitwise and the third coordinate was
set to positive zero. No projection, fitting, relaxation, transport solve,
or empirical parameter was used. The resulting rank-3 axial state is:

`06f005d108ccf16dc8bd25f0cf8d14bcb44656021dcab4408cfca22bdcca372c`

Production and independent Ganlib-only checks passed:

- all third-mode coordinates are positive zero;
- all 8 x 370 x 3 = 8880 reconstructed physical values are bitwise unchanged;
- rho, leakage, height, normalization, representation residual, and the raw
  axial flux carrier are unchanged;
- the old rank-2 map defects are absent;
- the snapshot archive remains read-only and has the same SHA-256;
- production B2J accepts `CLOSED/69 -> PROJECTED/70`.

## 3. One bounded unchanged coupled map

The current Dragon binary was used:

`c47d2a8d7b61f7e5e19680be49cdd3d2a0b1267e08a76fc1c3d25e43f31fcc28`

The radial half completed once in 67 seconds with `SPOD 3 FIXB`:

- fixed-basis marker: 1
- returned planes: 3
- radial balance: `5.887672128149170e-16`
- source L2: `1.147735948122973e-09`
- source max: `3.010176003055964e-09`

The axial half retained pure Picard `ACCE 3 0`, `REBA OFF`, and the declared
`5.0e-8` solver tolerance. It reached the single 600-second hard limit while
still inside `FLU`. The process group was terminated and no Dragon process
remained. There is no axial terminal, candidate, SPOSTATE, SPOXCONV defect,
CLOSED archive, or convergence gate for this attempt. It was not retried.

## Conclusion

This run does not prove a rank-3 fixed point and does not prove mathematical
nonexistence or divergence. It proves that the exact rank-enrichment map did
not produce one admissible next state within the declared bounded test.
Therefore no rank-2/rank-3 fixed-point error may be reported from this run.

The only canonical result for the precision-supported snapshot space remains
the clean-replay rank-2 fixed point. This diagnostic rank-3 attempt does not
supersede it. Repeating longer rank-3 Picard runs would target a third mode
near the REAL32 snapshot noise floor and is not the next minimal step.
