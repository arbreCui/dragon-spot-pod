# Native segment composition: exact kernel passes, native partition equality fails

The next bridge prerequisite is now resolved. Exact physical T/B/D can be
subdivided and recombined to roundoff. Repeated use of the native tabulated
coefficients changes the original response: the largest relative change
across the frozen native fixture is **2.96177e-5 (0.00296177%)**. All declared
native segment/partition/direction comparisons fail the strict `5e-12`
unchanged-action gate. Their amplitudes remain nonnegative and their raw
balance stays within the earlier `1e-6` context limit.

This is a failure of numerical operator equivalence, not a new determination
of whole-model physical accuracy. The discrepancy is small at the primitive
level; its propagation through complete tracks and common white return has
not yet been measured. Native spatial convergence and the coupled reference
remain unqualified.

## Frozen evidence

- [Predeclared composition contract](native_segment_composition_contract.md)
- [Compact execution plan](../artifacts/native-segment-composition-compact-20260929/plan.json)
- [Complete numeric summary](../artifacts/native-segment-composition-compact-20260929/analysis/result.json)
- [Verification](../artifacts/native-segment-composition-compact-20260929/verification.json)
- [Artifact and reproduction](../artifacts/native-segment-composition-compact-20260929/README.md)
- [Preserved resource-limited attempt](../artifacts/native-segment-composition-20260929/README.md)
- [Prior analytic slab success](axial_cell_characteristic_result.md)

The three groups are 51, 61 and 98. Each contains 439,344 positive-length
ray/polar/interior-segment records, for 1,318,032 original records in total.
Identical `(total, length, native B, native D)` tuples are deduplicated
losslessly to 244,233 per group. The saved inverse maps recover every
original record and its track, polar node, region and weight.

Native total precision and physical lengths `h2*ZMU` are unchanged. A private
probe links the sealed original libraries and calls `XDRTA2`, `MCGSCA` and
`MCGDSCA`. Every unsplit B and D is **bitwise equal** to its saved native
coefficient. Native D is extracted from its actual own-source routine,
not reconstructed from a balance identity.

Each record is partitioned into 2, 4 or 8 equal pieces and an asymmetric
1/3 + 2/3 pair. Both travel orders retain the physical source indices.
Inputs are a boundary unit, uniform unit source, each individual piece-source
unit and the fixed alternating 0/1 pattern. These are local composition
experiments; they do not define a quadrature of oblique axial crossings.

## What changes under partitioning

For one piece, outgoing amplitude and integrated amplitude are

```
out = T*in + B*q
integral = B*in + D*q
```

Exact two-piece composition requires

```
T12 = T2*T1
B_out12 = T2*B1 + B2
B_integral12 = B1 + B2*T1
D12 = D1 + D2 + B2*B1
```

The two B roles are kept separate. Direct flights use the original native
recurrence `out=in+B*(q-sigma*in)` for native coefficients and exact T/B
propagation for the exact companion. Independently multiplied augmented
3-by-3 transition matrices check both outgoing and integrated actions.
Their largest scaled difference on the native fixture is 1.35e-15.

The following maxima are **parts per million of the corresponding unsplit
response**, over all original segments and both travel orders. One ppm is
1e-6 relative. The frozen unchanged-action limit is 0.000005 ppm.

| Group | 2 equal pieces | 4 equal pieces | 8 equal pieces | 1/3 + 2/3 |
|---:|---:|---:|---:|---:|
| 51 | 15.7979 | 15.7529 | 15.9647 | 15.7508 |
| 61 | 15.7975 | 15.7524 | 15.9650 | 15.7505 |
| 98 | 27.8604 | 29.6177 | 29.5997 | 27.7809 |

Every one of the 5,861,592 unique record/partition/direction comparisons
fails that strict gate. They map to 10,544,256 comparisons over the original
records. A comparison fails when at least one of T, B_out, B_integral or D
exceeds the threshold; this does not say every component exceeds it.

Separating the components explains which quantity controls the maximum:

| Group | T change (ppm) | B_out change (ppm) | B_integral change (ppm) | D change (ppm) |
|---:|---:|---:|---:|---:|
| 51 | 0.190826 | 0.204517 | 0.204517 | 15.9647 |
| 61 | 0.201427 | 0.202902 | 0.202902 | 15.9650 |
| 98 | 29.6177 | 0.203433 | 0.203433 | 15.9642 |

Groups 51 and 61 attain their largest D change near optical length 0.02244.
The native own-source routine changes from its thin-layer polynomial branch
at 0.02 to its tabulated branch; subdivision places these pieces in the thin
branch. This is consistent with the observed D discrepancy. In group 98,
the largest T change occurs at optical length 5.98162, where the remaining
transmission is small and a small absolute B approximation error has a larger
relative effect on `T=1-sigma*B`. These are implementation-based explanations
supported by the saved worst-case traces, not fitted correction formulas.

## Mathematical controls and raw balance

Exact composition passes for every fixture partition. The largest relative
outgoing/integral recovery defect is **1.26e-15**; raw global balance is
**1.11e-15** on the declared incoming-plus-source scale. Exact and native
kernels, intermediate amplitudes and integrated responses are nonnegative.
No clipping, rescaling or redistribution of the PJJ remainder is applied.

Native raw global balance is at most **1.82e-7**, below the unchanged 1e-6
context limit. Small balance defects therefore coexist with failed strict
partition equivalence. The raw local and global defects remain available
for every prescribed input.

Independent controls span optical lengths 0, 1e-12, 1e-6, 0.001, 0.7, 10 and
100. Exact partition recovery is within 1.42e-14. Native void coefficients
are supported and exactly match the void limit. The largest native relative
change in these extra controls is 4.88817e-4 (0.0488817%); these deliberately
broader optical cases are reported separately from the native-fixture maximum.

## Resource-limited attempt and reproduction

The first 8,192-record implementation exceeded the frozen 512 MiB cap while
entering the group-51 eight-piece comparison: 524.64 MiB at 18.52 seconds.
It stopped before groups 61/98 were analyzed. Its plan, sources, native
extractions and completed partial outputs are sealed as an **incomplete**
artifact. It is not a failed physics result and is not presented as completed.

The compact continuation uses 1,024-record batches, computes exact coefficients
in those batches and releases coefficient-only scratch. The equations, source
cases, partitions, tolerances and 512-MiB/600-second per-process limits are
unchanged. All available numerical arrays from the preceding partial analysis
are compared with matching compact slices.

Primary group calculations take about 42 seconds each and peak at no more
than 293.80 MiB. Ten mathematical/source-interface tests pass from maintained
and archived code. A fresh-directory replay recompiles the private probe,
re-extracts the native coefficients and repeats every analysis from real copied
inputs. The initial list-input unit-test error is also preserved in the first
artifact; accepting array-like input fixed that helper before the full runs,
without changing any tolerance.

Raw endpoint amplitudes, integrated amplitudes, signed global defects,
intermediate minima, local-balance maxima and independent matrix outputs are
saved for every input and order. All subpiece T/B/D and primitive balance
coefficients are retained; the worst preservation/balance witnesses additionally
contain every intermediate incoming/outgoing amplitude, integral and local
defect. This is a complete endpoint-response audit, not a claim that every
intermediate trace of every case was materialized.

The verification record checks original-record mapping, exact coefficients,
raw endpoint ledgers, matrix comparison, gate counts, witness traces, replay,
protected files and all preceding seals. Running D4 inputs and production
source/runtime files remain unchanged.

The replay reproduces **2,897 analysis files byte for byte**. Verification
checks 161,776 numeric arrays and recovers all 3,416 available arrays from
the resource-limited partial run. It also checks 997 protected files, 45
copied-input hashes and 2,658 sealed-file entries in 20 preceding artifacts.
Replay group processes peak at no more than 303.80 MiB and take about
42 seconds each, within the unchanged limits.

## Next bounded step

The [exact-kernel full-flight contract](exact_native_flight_contract.md) now
specifies the next comparison. Reproduce the original native signed flights,
then evaluate an explicitly separate exact-exponential companion with the
same retained states. Measure fixed-input changes first, then rebuild common
white return and measure its effect separately. Exact whole-flight partition
recovery must pass before actual axial-crossing geometry is introduced.

The failed native equality gate remains failed. Using exact exponentials is
a declared kernel change requiring its own calibration; it is not silently
inserted into the original native operator or the production D4 chain.
