# B2C runtime-dimension admission result

## Classification

`VALID_NO_TRANSPORT_BOUNDARY_TEST`.

This result covers one deliberately small production boundary:
`SPOR64_B2C`, which publishes a completed radial plane.  It does not run
Dragon, solve radial transport, execute an axial solve or claim that the
full D4-A lifecycle is ready.

## Change

`SPOR64_B2C` now obtains the region, material and unknown counts from the
actual `KEYFLX`, `IMERGE-LEAK` and terminal arrays.  These counts control its
allocations and emitted record lengths.  The 370-group structure, frozen
tolerance bits, merge rule, option, link identities, lifecycle checks and
REAL64-to-REAL32 publication order are unchanged.

## Manufactured admission

The short host test publishes two independent memory objects:

| case | regions | materials | unknowns | groups |
|---|---:|---:|---:|---:|
| existing pin BOOT boundary | 8 | 8 | 14 | 370 |
| D4-A CONT structural boundary | 132 | 6 | 144 | 370 |

The 144-unknown extent is the real D4-A TRACK value: 132 region unknowns plus
12 surface-current unknowns.  The array values are manufactured and are not a
D4-A transport result.  They only ensure that the implementation does not
silently equate the region and unknown dimensions.

For every group and unknown the test requires:

- the type-4 `SPOT-R64/FLUX` and `SOUR` records to preserve the supplied
  REAL64 bits;
- the type-2 compatibility records to equal the exact REAL32 demotion bit
  pattern;
- `STATE-VECTOR`, `KEYFLX`, `IMERGE-LEAK` and all list-item lengths to carry
  the runtime dimensions;
- a duplicate region key or mismatched source shape to fail before the
  output root is modified.

The CONT case also supplies an exact five-record `PROJECTED` authority, so
the runtime-sized lifecycle-flux validator and `LEAK1D64` publication are
exercised rather than inferred from the BOOT result.

Command and result:

```text
$ make spot-b2c-dimensions
B2C RUNTIME-DIMENSION PASS: pin and D4-A 144-unknown structural publication only.
```

The same test is part of `make spot-fast`, which passes without starting a
Dragon process.

## Frozen first-case evidence

Both clean-replay manifests still pass.  A separately rebuilt no-transport
`SPOR64_B2W` close reproduced the two frozen CLOSED XSM files byte for byte;
the admission, close and independent-check logs were also byte-identical.
The convergence-gate numbers and classification were identical, with only
compiler-produced trailing blanks after the three `PASS` labels differing in
the regenerated text log.

This does not replace the eventual one-map transport regression required
after the complete radial dimension chain has been generalized.
