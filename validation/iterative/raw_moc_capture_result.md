# Raw primary-MOC capture result

## Status

The corrected bounded replay completed from commit
`a011fd902398b47e06faa2b23d0682c9d01eef7f`. One preparation process
reconstructed the frozen restart without a transport solve. Four one-step
NATIVE/STATIONARY × OFF/ON probes then ended normally inside their declared
30-second process-group bounds.

The independent log comparison passed. For each arm, OFF and ON have the same
scientific FLU block after removing only the two printed CPU-time values. The
independent Ganlib-only checker also passed twice with byte-identical output:

- the old FROZEN and fresh OFF XSM objects are byte identical;
- OFF and ON are byte identical outside the single root `SPOT-MOC-AUD`
  directory;
- all 370 groups contain one complete write-once 14-unknown tuple;
- `EVAL` is the frozen PRE input bit for bit;
- the binary32 `MCGFCS` volume and boundary source arithmetic replays exactly;
- the captured payload is finite and the retained scalar flux is positive.

The machine classification is therefore `CAPTURE-VALID`. This classifies the
capture and its ledger, not the SPOT fixed point or an inner transport solve.

## Captured diagnostic

The payload is the first primary GMRES raw MOC response after STIS/volume
normalization and before ACA/SCR. The reported difference is

\[
\Delta\phi_{\mathrm{raw}}=\phi_{\mathrm{raw}}-\phi_{\mathrm{eval}}.
\]

| terminal | scalar relative two-norm | input-normalized scalar maximum | exact maximum location |
|---|---:|---:|---|
| NATIVE | \(5.74612642427124923\times10^{-7}\) | \(2.13063570538973194\times10^{-6}\) | group 100, region 2, key 2 |
| STATIONARY | \(5.78155360184452634\times10^{-7}\) | \(2.19029230865145395\times10^{-6}\) | group 100, region 2, key 2 |

The relative two-norm is volume weighted over 370 groups and eight scalar
regions. The maximum is the global absolute scalar change divided by the
global maximum input magnitude; it is not a pointwise relative error. All
2,220 current changes per arm are retained componentwise in the local
artifact, but they are not folded into the scalar norm.

## Interpretation boundary

`RAW - EVAL` is a same-sweep observable, not an independently assembled
\(A\phi-q\) residual, a backward-error estimate, or a transport-error bound.
The experiment has no independent truth for the finite RAW payload. The two
arms are parallel diagnostics and may not be ranked from the small difference
between their reported values.

No model term, empirical coefficient, relaxation, clipping, fitted factor or
post-result acceptance threshold was introduced. The result therefore retains
the following limits:

```text
TRANSPORT-ERROR-BOUND NOT-ESTABLISHED
ARM-RANKING NOT-AUTHORIZED
OUTER-CONVERGENCE NOT-EVALUATED
STAGE4 NOT-AUTHORIZED
```

The first production attempt is not counted as scientific evidence. Its five
processes ended normally, but the independent checker rejected legal negative
geometric `ICODE` before opening PRE, FROZEN, OFF or ON. No artifact was
published. The corrected checker follows the actual `MCGSIG`/`MCGFCS` path:
negative `ICODE` retains the TRACK albedo, positive physical indices override
only when group albedos exist, and each boundary albedo slot is selected by
`-NZON`.

The next minimal step is an offline ULP bridge audit of the already captured
scalar tuples: round each binary64 RAW value once to the production binary32
boundary and count exact unchanged/up/down representable steps from EVAL.
This requires no new transport solve, model term or threshold. It may scope a
later default-off REAL64 working-iteration experiment, but it cannot by itself
attribute the observed change to binary32 or authorize that experiment.

## Evidence

The tracked machine summaries are
[raw_moc_capture_status.txt](raw_moc_capture_status.txt) and
[raw_moc_capture_xsm_result.txt](raw_moc_capture_xsm_result.txt). The result
receipt binds them to the local artifact at
`validation/artifacts/raw-moc-capture/`.

The artifact contains 81 regular files (79 entries in its scientific
manifest), occupies about 81 MiB, and has no symlinks. It retains the four
rendered decks and logs, all PRE/FROZEN/OFF/ON objects, immutable common-input
receipts, the independent checker and symbol audit, two checker replays per
arm, and the external parent-manifest replay. The binary artifact is ignored
by Git; GitHub retains the protocol, implementation hashes, public result,
receipt and reproducible checker.

From the repository root, verify the complete local package with:

```sh
python3 validation/iterative/check_raw_moc_capture_result.py
shasum -a 256 -c \
  validation/iterative/raw_moc_capture_result_receipt.sha256
```

Use `--public-only` only when the ignored binary artifact is unavailable.
