# D4-A rank-2 Picard maps 3 to 5

Maps 3, 4, and 5 are complete continuations of the frozen D4-A rank-2 SPOD
route. Every map uses the same Dragon executable, decks, route contract,
rank-2 basis, radial and axial transport operators, and direct Picard update
(`alpha = 1`). No relaxation, damping, empirical coefficient, rank change, or
model correction is present.

For all three maps:

- the three radial fixed-source responses completed with fresh REAL64 true
  residual checks;
- production admission and the axial solve completed;
- B2W sealed `CLOSED/3`, `CLOSED/4`, and `CLOSED/5`;
- the independent continued-state checker passed POD identity, live radial
  change, positivity, canonical layout, raw defect, and restart archive;
- the complete input and output SHA-256 manifests rechecked byte-for-byte.

The fixed `5e-7` gate gives:

| map | `Rrho` | `Rleak` | `Ra` | classification |
|---:|---:|---:|---:|---|
| 2 | `1.1377286940830178e-3` | `7.5829611541736930e-3` | `2.6566931552983479e-3` | `VALID_NOT_MET` |
| 3 | `2.2103189776334631e-4` | `7.7771423654006248e-4` | `5.3982764055179259e-4` | `VALID_NOT_MET` |
| 4 | `3.8933101317195629e-5` | `1.3215411700758515e-4` | `1.1046835992980127e-4` | `VALID_NOT_MET` |
| 5 | `2.5073074546577701e-6` | `1.3528407829925955e-5` | `2.3977806631220546e-5` | `VALID_NOT_MET` |

Successive contraction ratios are:

| transition | `Rrho` | `Rleak` | `Ra` |
|---|---:|---:|---:|
| map 2 to 3 | `0.194274697397` | `0.102560757035` | `0.203195329304` |
| map 3 to 4 | `0.176142455958` | `0.169926318432` | `0.204636353590` |
| map 4 to 5 | `0.064400404022` | `0.102368417544` | `0.217055875967` |

All three independently gated physical defects decrease monotonically and by
large factors. From map 2 to map 5 they fall to `0.220%`, `0.178%`, and
`0.903%` of their map-2 values. The pure physical Picard route is therefore
stable and convergent over four consecutive validated maps. Map 5 is not yet
the fixed point: `Ra` remains the largest normalized gate defect at about 48
times the required threshold.

The non-gated maximum relative out-of-span diagnostic remains approximately
constant near `6e-8` (`5.79e-8`, `6.32e-8`, and `5.73e-8` for maps 3 to 5).
It remains far below the outer defects and supplies no evidence for changing
the rank.

The axial eigenvalues are `1.2864364243649271`, `1.2863719964753912`, and
`1.2863761454630884` for maps 3 to 5. Frozen artifacts and their manifests are
stored locally under:

- `validation/artifacts/iterative-d4a-rank2-picard-map3/`
- `validation/artifacts/iterative-d4a-rank2-picard-map4/`
- `validation/artifacts/iterative-d4a-rank2-picard-map5/`

The next physically justified action is to continue unchanged from
`CLOSED/5`; no numerical or modeling intervention is indicated by the data.
