# Bounded radial numerical-floor result

## Status

The predeclared plane-1 diagnostic completed on 2026-07-24 from commit
`de4297cc4d1aeca63307191df70c6eeaef4b1e2a`. Both main arms reached the
six-update cap without satisfying the frozen strict FLU gate:

| arm | `ACCE` | terminal `EUNK` | terminal `EINR` | `IGDEB` | state |
|---|---:|---:|---:|---:|---:|
| NATIVE | `3 3` | \(4.61396212\times10^{-6}\) | \(1.42215981\times10^{-6}\) | 68 | 2 |
| STATIONARY | `1 0` | \(7.06307844\times10^{-7}\) | \(7.06307844\times10^{-7}\) | 50 | 2 |

The machine classification is therefore `BOTH-CAP`, not convergence. The
solver tolerance in both arms was the frozen binary32 value
\(h/2=2.5\times10^{-7}\).

Each terminal flux was then copied byte for byte to a fresh
`MAXOUT=1, ACCE 1 0` probe. The independent Ganlib-only checker obtained:

| terminal | \(D_{V,2}\) | \(D_{\max}\) | max-change location |
|---|---:|---:|---:|
| NATIVE | \(2.7679927314276433\times10^{-7}\) | \(4.1416213619307689\times10^{-7}\) | group 82, region 1 |
| STATIONARY | \(3.4298569286320643\times10^{-7}\) | \(4.8318912553881632\times10^{-7}\) | group 87, region 1 |

Here \(D_{V,2}\) is the volume-weighted relative two-norm over 370 groups
and eight radial regions. \(D_{\max}\) is the global maximum absolute
change divided by the global maximum input magnitude; it is not a
pointwise relative error.

## Interpretation boundary

The two defects show only that one fresh stationary production-map update
changes the two terminal scalar-flux fields by several \(10^{-7}\) in the
declared norms. They are not an independently assembled
\(A\phi-q\) residual, a transport-error bound, or a convergence proof.
Although both reported defects are smaller for the NATIVE terminal in this
one experiment, the result does not establish acceleration superiority or
causation.

The FLU successive-iterate quantities and the independent probe norms are
different observables and must not be ranked as if they were the same
residual. `BOTH-CAP` also does not prove divergence or determine a unique
floating-point floor.

No model term, relaxation, fitted factor, empirical coefficient, or
post-result acceptance threshold was introduced. Consequently:

```text
STAGE4 INVALID
STAGE5 NOT-AUTHORIZED
OUTER-CONVERGENCE NOT-EVALUATED
```

The next validation decision must be made before a long outer iteration:
either obtain a solver-independent inner equation/backward-error measure or
change the arithmetic so that the predeclared tighter solve can be resolved.
This diagnostic alone does not authorize choosing one arm or weakening the
gate.

## Evidence

The exact protocol is
[radial_floor_protocol.json](radial_floor_protocol.json). The tracked
[result receipt](radial_floor_result_receipt.sha256) binds the compact local
artifact at `validation/artifacts/iterative-radial-floor/`.
The public machine outputs are retained as
[radial_floor_status.txt](radial_floor_status.txt) and
[radial_floor_xsm_result.txt](radial_floor_xsm_result.txt).

The compact artifact is 7.6 MB and retains both arm terminals, all four
arm/probe logs and rendered decks, the four common XSM inputs needed by the
Ganlib checker, all four probe XSM objects, the checker executable and
symbol audit, and the complete-run receipts. Its dependency manifest points
to the five already preserved parent files in
`iterative-sensitivity-h2-failed`, avoiding another approximately 465 MB
(444 MiB) of logical file copies. Both `arm_flux.xsm == probe_pre.xsm`
terminal identities remain directly replayable.

The compact package and its parent artifact are intentionally ignored by
Git. Therefore the GitHub repository contains the protocol, result,
checksums, and reproducible tooling, but not the large binary evidence.
A complete rerun also requires the frozen Dragon executable
(`e4c61fa45ba0fe62be3a15e21785c5e27b9a3c10d727a02754d43d7c79ef2759`),
Ganlib, commit `de4297c`, and the local parent artifact.

From the repository root, the retained package is checked with:

```sh
shasum -a 256 -c validation/iterative/radial_floor_result_receipt.sha256
(
  cd validation/artifacts/iterative-radial-floor
  shasum -a 256 -c receipt.sha256
  shasum -a 256 -c minimal_manifest.sha256
  shasum -a 256 -c dependency_manifest.sha256
)
```
