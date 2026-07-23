# Stage-4 inner-tolerance capture

## Status

```text
CAPTURE INVALID-INNER-NONCONVERGENCE
STAGE4 INVALID
STAGE5 NOT-AUTHORIZED
OUTER-CONVERGENCE NOT-EVALUATED
```

This is an execution result, not a valid \(h/2\) map result. No
\(\mathcal D_{\rm in}\), scale ordering, or outer-convergence conclusion is
formed from the returned files.

## Frozen provenance

The complete protocol, checker, deck and classification rule were committed
and pushed as `a42795870e35f524fe6dacea4b5d417517e582ad` before this
calculation began. The capture used the frozen Dragon executable and the same
seed and baseline objects as Stage 3. Its pre-run input manifest was replayed
successfully after the failed calculation. The rebuilt basis and complete
\(x_0\) archive are byte identical to the Stage-3 objects.

The preserved log has SHA-256
`fb68de3f1cd345338e2e629170c9bcfd7b69b87be4766590e53aadf7c1ff1abf`.
The small tracked receipt is
`inner_sensitivity_failure_receipt.sha256`; the approximately 480 MB XSM
artifact directory remains local and is excluded from Git.

## Strict inner-solver outcome

The initializer remained at \(h\). The three radial solves and returned axial
solve used the exact binary32 half \(h/2\).

| Solve | tolerance | outer iterations | first unfinished group | final \(E_{\rm unk}\) | status |
|---|---:|---:|---:|---:|---|
| initializer axial | \(4.99999999\times10^{-7}\) | 134 | 371 | \(4.89227034\times10^{-7}\) | PASS |
| radial plane 1 | \(2.49999999\times10^{-7}\) | 500 | 50 | \(5.03026570\times10^{-7}\) | FAIL |
| radial plane 2 | \(2.49999999\times10^{-7}\) | 500 | 47 | \(5.29328702\times10^{-7}\) | FAIL |
| radial plane 3 | \(2.49999999\times10^{-7}\) | 500 | 29 | \(6.19920286\times10^{-7}\) | FAIL |
| returned axial | \(2.49999999\times10^{-7}\) | 193 | 371 | \(2.46326749\times10^{-7}\) | PASS |

Each radial solve exhausted the frozen `MAXOUT=500`, returned `STATE=2`,
and failed both the unknown and thermal successive-iterate gates. Dragon
continued to the end of the deck and wrote `state1`, but strict termination
failed before those objects were accepted. The independent failure checker
therefore does not print or classify their raw defect.

## What the failure means

For the radial fixed-source `TYPE S` solve, \(E_{\rm ext}=0\); the active
tests are the unknown and thermal changes. Both are maximum relative changes
between consecutive binary32 flux iterates, not an independently evaluated
equation residual \(\|A\phi-q\|\).

The Stage-3 radial solves crossed the \(h\) gate after 27, 6 and 2 outer
iterations. At \(h/2\), all three remained near
\(5\text{--}6\times10^{-7}\) after 500 iterations and their physical balance
diagnostics did not improve consistently. Since the flux, controls and
successive-iterate residuals are binary32, \(h\) is only about 8.39 unit
roundoffs and \(h/2\) about 4.19. The current evidence is consistent with a
REAL32-dominated, non-monotone numerical floor involving the default
three-free/three-accelerated cycle and rebalancing. The terminal log alone
does not separate those mechanisms.

Consequently:

- the failure does not prove that the physical SPOT fixed point diverges;
- the Stage-3 \(h\) crossing is not an error bound;
- increasing `MAXOUT` has no demonstrated contraction basis and is not the
  next experiment;
- the failed `state1` files are forensic artifacts, not
  \(G_{h/2}(x_0)\).

## Frozen bounded diagnostic

The numerical-only plane-1 protocol is frozen before another transport run:

1. restart both arms from the same preserved cap-500 plane-1 flux;
2. keep \(A\), \(q\), \(x_0\), rebalancing and all physical data identical;
3. run the production `ACCE 3 3` arm with normal strict early termination
   and a cap of six outer updates;
4. run the production `ACCE 1 0` arm with the same strict early termination
   and cap;
5. from each terminal state, apply exactly one `ACCE 1 0` stationary
   production-map probe;
6. record every \(E_{\rm unk}\), \(E_{\rm inr}\) and printed acceleration
   factor, and independently compute the probe's volume-weighted and maximum
   fixed-point defects in binary64.

Six is the native three-free/three-accelerated period, not a fitted stopping
parameter. A strict production termination before six is retained rather
than suppressed. The restart contains only the cap flux, so both solver
histories and the acceleration phase reset; the native arm is not a
continuation through iterations 501--506. Moreover `ACCE` controls inner as
well as outer `FLU2AC`, while rebalancing remains active.

The archived MCCG objects do not contain a complete materialized discrete
operator. The independently computed quantity is therefore
\(\|T_{h/2}(\phi)-\phi\|/\|\phi\|\), not a full \(A\phi-q\) backward
residual. It is reported without an acceptance threshold and cannot qualify
Stage 4 or authorize Stage 5. This diagnostic is much smaller than another
three-plane `MAXOUT=500` run and introduces no relaxation, calibration or
empirical coefficient. The exact predeclared controls are in
[radial_floor_protocol.json](radial_floor_protocol.json), with execution and
provenance gates in
[run_radial_floor_diagnostic.sh](run_radial_floor_diagnostic.sh).
