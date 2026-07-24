# Read-only radial working-precision audit

## Result

The completed radial-floor probes were re-read without running Dragon or
calling a transport routine. For each of the 370 groups and eight active
radial regions, the checker used `KEYFLX$ANIS` and counted the exact signed
distance between the pre- and post-probe IEEE binary32 encodings. For
positive finite binary32 values, this integer difference is exactly the
number of adjacent representable values crossed; no floating-point division
or fitted threshold is involved.

| arm | total | unchanged | upward | downward | adjacent | largest absolute step |
|---|---:|---:|---:|---:|---:|---:|
| NATIVE | 2960 | 288 | 136 | 2536 | 265 | 17 |
| STATIONARY | 2960 | 272 | 88 | 2600 | 220 | 12 |

The NATIVE maximum is tied at group 142, regions 6--8, with signed step
`-17`. The STATIONARY maximum is tied at group 102, all eight regions, with
signed step `-12`. Neither stored map is bitwise fixed. The complete signed
histograms are in
[radial_precision_result.txt](radial_precision_result.txt); the ignored
local evidence contains all 5920 rows with group, region, flux key, both
binary32 encodings, and signed and absolute step counts.
The separate
[radial_precision_receipt.sha256](radial_precision_receipt.sha256) binds
that full ledger, its parent radial-floor receipt, the checker and runner,
this result, and the next frozen protocol.

The two arms start from different terminal states. Their histograms are
therefore parallel diagnostics, not a controlled comparison of acceleration
schemes.

## What this establishes

The remaining stored-field motion is expressed in small integer numbers of
binary32 representable levels: at most 17 in this probe. This makes the
binary32 working-state path relevant to the failed tighter gate, but it does
not identify one unique numerical floor or prove that binary64 alone will
converge.

The current path combines several numerical mechanisms:

- `FLU2DR`, `FLUBAL`, the public MCCG door, and all stored `FLUX/SOUR`
  records use binary32 working values;
- MCCG ray integration and parts of GMRES use binary64 internally, then
  return through binary32 state updates;
- the frozen MCCG control uses `EPSI 1E-5`;
- the ACA correction contains an independent `1E-7` cutoff;
- the returned flux may be changed after the raw sweep by ACA, rebalancing,
  and FLU acceleration.

Consequently, this result is a representation audit only. It is not an
\(A\phi-q\) residual, a backward-error bound, an inner convergence proof, a
physical error estimate, or an authorization for Stage 4 or Stage 5.

## Why an archived \(A\phi-q\) checker is not valid

The frozen `SYSTEM/GROUP` records contain ACA corrective matrices and
preconditioners (`DIAGF`, `CF`, `DIAGQ`, `CQ`, `ILUDF`) plus self-collision
coefficients (`PJJ`). They do not contain the full MOC transport operator.
That operator is applied by traversing the external sequential tracking
file.

The archived `SOUR` is also the last sweep input, whereas the archived
`FLUX` may already include rebalancing and acceleration. Since the terminal
states did not converge strictly, they cannot be treated as a consistent
same-point equation pair. Replacing the unavailable transport matrix with
the ACA matrix would produce a preconditioner residual and is rejected.

## Frozen next step

The next bounded change is diagnostic instrumentation, not a longer solve:

1. behind a default-off `TYPE S + MCCG` diagnostic switch, capture the
   frozen terminal flux, same-call `QFR`, post-`MCGFCS` source-element vector
   and raw MOC response only for GMRES global iteration 1's primary
   fixed-point evaluation; explicitly exclude the affine-RHS, Krylov-basis
   and later primary calls;
2. write only beneath an `INCOMPLETE` audit directory in the fresh writable
   `L_FLUX` output, never into the read-only `SYSTEM`, and publish `COMPLETE`
   only after the locked 370-group tuple is present;
3. preserve `QFR` and the terminal binary32 input by exact promotion and
   preserve the production source-element vector and raw response in their
   binary64 storage;
4. execute one production-map update from each frozen terminal, with the
   instrumentation adding zero operator applications, relaxation, model
   terms, or empirical thresholds;
5. let a Ganlib-only checker replay the binary32 source construction and
   recompute the raw-sweep difference
   \(\phi_{\rm raw}-\phi_{\rm eval}\), positivity, metadata and census,
   while separately retaining the post-rebalancing production-map defect.

This adds the raw-primary fixed-point defect at the frozen terminal to the
existing terminal production-map defect. It does not decompose or assign the
difference to GMRES, ACA, `FLUBAL`, `FLU2AC`, or rounding. The pair of
observables is used only to scope the minimal default-off REAL64
working-iteration lane. The final method remains iterative online 2D/1D
Picard coupling; no physical feedback is removed.

The audit is replayed with:

```sh
validation/iterative/run_radial_precision_audit.sh
```

When the ignored local evidence is present, its receipt is checked from the
repository root with:

```sh
shasum -a 256 -c validation/iterative/radial_precision_receipt.sha256
```
