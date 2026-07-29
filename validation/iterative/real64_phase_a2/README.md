# REAL64 Phase-A2 post-STIS raw-response façade

## Status

Phase-A2 adds one isolated, typed seam above the Phase-A1 source kernel:

```text
IMPLEMENTED-PARTIAL-SOURCE-TO-RAW-FACADE-ONLY
PRODUCTION-ROUTE=UNCONNECTED
ACTUAL-MOC-RESPONSE=NOT-IMPLEMENTED
DRAGON-RUNS=0
```

It remains under `validation/` and is not part of the production build.

## Exact boundary

For each gathered local group column \(j\) with `NCONV(j)=TRUE`,
Phase-A1 first constructs the binary64 source

\[
S_j=Q_j+\Sigma_{s,j}\Phi_j
\]

with the already frozen surface terms.  Phase-A2 then makes exactly one
full-matrix call through
`SPOR64_POST_STIS_RAW_RESPONSE_IFACE`.

That interface represents the future real sequence

```text
MCGFCS64
  -> MCGFCF (MCGFFIR -> MCGSCA)
  -> MCGFST
  -> post-STIS / pre-ACA raw response
```

It does not represent the value returned by legacy `MCGFL1`, because the
locked legacy path subsequently applies `MCGFCA`.  Phase-A2 does not call
any of these real transport routines; its callback is only a checked seam
for a later adapter.

`NGIND(j)` is the physical group label of local gathered column \(j\).  It
is never used as a direct array subscript.  The gathered labels must be the
strictly consecutive tail ending at `NG`; `NCONV` may select any nonempty,
noncontiguous subset of those local columns.

## Transactional rule

The caller works entirely in temporary binary64 matrices:

- active source columns are rebuilt; inactive source columns retain their
  caller bit patterns;
- active raw columns start as quiet-NaN sentinels, so every element must be
  written and finite;
- inactive raw columns start and must remain exact positive zero;
- the callback is invoked exactly once;
- any source, callback, completeness, finiteness, inactive-write, layout,
  or group-map failure leaves both caller output matrices unchanged;
- only a successful callback commits active source columns and the complete
  raw-response matrix.

These are exact structural checks, not fitted tolerances.

## Synthetic test operator

The unit test uses an exact signed permutation of each active source
column.  It has no cross section, fitting parameter, closure coefficient,
or physical interpretation.  Its sole purpose is to detect column
compression, active-mask mistakes, missing writes, and any binary32
round-trip at the interface.  All 31 nonempty masks over five gathered
columns are enumerated, including noncontiguous masks.

Run the short isolated gate with

```sh
make spot-real64-phase-a2
```

The runner first rechecks Phase-A1, then verifies the Phase-A2 receipt and
manifest, performs a strict explicit-source compile, runs the synthetic
test, requires two wrong-kind callers to fail compilation, checks link
isolation, and runs manifest mutation tests.  It starts no Dragon process
and reads no tracking file.

## What remains

This is still not a continuous REAL64 radial solve and gives no convergence
result.  The next static step is a compile-only checked adapter around the
real frozen `MCGFCF` through `MCGFST` response.  The tracking/KPSYS
context, ACA, GMRES state, rebalancing, acceleration, terminal norms, and
type-4 archive boundary all remain open.
