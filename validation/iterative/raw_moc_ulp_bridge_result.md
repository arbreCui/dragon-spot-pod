# Raw-MOC binary32 ULP bridge result

## Result

The frozen capture was audited entirely offline from commit
`0a7e0e3fa951bcb12a5cd29dbffbe4fb3de44618`. No Dragon process, transport
solve, operator application, model term, relaxation, clipping or empirical
coefficient was added.

For each arm, group and radial region, two distinct ledgers were formed:

1. `RAW-BRIDGE` is
   \(K(\operatorname{RN}_{32,\mathrm{RNE}}(\mathrm{RAW}_{64}))
   -K(\mathrm{EVAL}_{32})\). It is a declared direct projection of the
   captured post-STIS, pre-ACA/SCR response, not an assertion that the
   production path actually stores RAW at that point.
2. `PRODUCTION-STEP` is
   \(K(\mathrm{OFF}_{32})-K(\mathrm{PRE}_{32})\), the complete stored
   one-step change already audited independently.

Here \(K\) is the monotone IEEE binary32 encoding key. All released scalar
values are positive and finite, so the signed difference is exactly the
number and direction of adjacent representable binary32 values crossed.

| arm | ledger | unchanged | upward | downward | adjacent | maximum absolute steps |
|---|---|---:|---:|---:|---:|---:|
| NATIVE | RAW-BRIDGE | 135 | 977 | 1848 | 248 | 877 |
| NATIVE | PRODUCTION-STEP | 288 | 136 | 2536 | 265 | 17 |
| STATIONARY | RAW-BRIDGE | 133 | 975 | 1852 | 251 | 878 |
| STATIONARY | PRODUCTION-STEP | 272 | 88 | 2600 | 220 | 12 |

No captured scalar RAW value is exactly equal to its EVAL input in
binary64. Nevertheless, direct round-to-nearest-even projection returns to
the EVAL binary32 encoding at 135 of 2960 NATIVE coordinates and 133 of
2960 STATIONARY coordinates. These are classified separately as
`ROUND-COLLAPSED-NONZERO`; neither arm contains a projected zero or
subnormal.

The NATIVE RAW-BRIDGE maximum is `-877` at group 345, region/key 4. The
STATIONARY maximum is `-878` at the same indexed coordinate. The complete
production-step maxima remain the previously reproduced `-17` NATIVE tie
at group 142, regions 6--8 and the `-12` STATIONARY tie at group 102, all
eight regions.

The tracked [summary](raw_moc_ulp_bridge_result.txt) retains exact counts and
all maxima. The ignored local artifact contains the complete signed
histograms and 11,840 per-coordinate rows, including RAW64 bits, both
binary32 encodings, ordered keys, signed/absolute steps and classifications.
Its manifest SHA-256 is
`c8aacee484a5afdf3684cad4f87c5150093ee7fd1afda232ab6f7265f869b31c`.

## Evidence

The two arm readers were each run twice with byte-identical output. A
separate Python checker was run twice and independently replayed every one
of the 5920 binary64-to-binary32 round-to-nearest-even conversions. It also
reconstructed all four ledgers, histograms and maximum-tie sets from the
printed bits. Input hashes were unchanged before and after extraction.

The synthetic XSM gate independently exercised permuted region keys and
group/region/unknown sentinels, both halfway-rounding parities, binade and
subnormal boundaries, gradual underflow, overflow, nonpromotion, missing
and malformed records, nonfinite/nonpositive values, cross-arm layout
mismatch, non-scalar isolation and one-bit RAW/OFF changes.

## Interpretation boundary

The two ledgers must not be subtracted. Their endpoints belong to different
algorithmic phases, and the complete production path includes GMRES, ACA,
SCR, rebalancing and FLU acceleration after the captured RAW response.
Therefore the difference between the displayed maxima is not a measured
rounding loss, cancellation, correction, or contribution from any named
algorithm.

This census is not an \(A\phi-q\) residual, backward-error bound, transport
error, physical error, convergence test or comparison of NATIVE with
STATIONARY. The two arms start from different states. There is no acceptance
threshold and this result does not authorize Stage 4 or Stage 5.

What the result does establish is narrower: a direct binary32 projection of
the captured primary RAW response is nonidentical to EVAL at 2825 of 2960
NATIVE coordinates and 2827 of 2960 STATIONARY coordinates, often by more
than one representable step. That is sufficient motivation to define a
minimal, default-off REAL64 radial working-iteration experiment while
retaining the same physical equation and all frozen solver controls. It
does not predict that the experiment will converge.
