# Rank-two REAL64 axial-terminal probe at 5e-8

Date: 2026-08-18

Status: `NO_MAP_RESULT`; `AXIAL_TERMINAL_UNREACHABLE_AT_5E-8`.

This same-parent axial tolerance sensitivity extends the existing
`2.5e-7` and `1.25e-7` points of the epoch-5 window with a third
terminal, `solver_eps = 5.0e-8`.  The parent proposal, radial response,
reduced system, basis, tracks, and macrolib are hash-identical to the
frozen `aa1-z` map; the only deck change is the terminal value.  No
radial solve was repeated.

Two bounded attempts were made, each exactly once:

1. Under an external 120-second process bound, the warm axial solve
   produced no strict terminal before the bound.  That attempt is
   `TIMEOUT_BEFORE_TERMINAL` and carries no scientific content beyond
   the missing terminal.
2. Under the established 420-second external axial cap and fresh
   staging, the solve ran to the internal iteration limit in 131.7 s.
   The final solver diagnostic is

   ```
   FLU2DR-DIAG OUTER IEXTF=500 MAXOUT=500 KEFF=1.3624110816069912
     EEXT=1.30974936e-11 EUNK=5.79228015e-07 EPSUNK=5.00000006e-08
   FLU2DR: CONVERGENCE NOT REACHED
   FLU2DR: SPOT TYPE-K STRICT TERMINATION REQUIRED.
   ```

   The eigenvalue converged to `1.3e-11`, but the flux-unknown
   successive change plateaued near `5.8e-7`, above the requested
   `5e-8`, and the strict-termination contract refused publication.
   No candidate, defect, or map result exists.

## Supported conclusion

Together with the two existing points --- `2.5e-7` terminal giving
$R_L=2.4829538\times10^{-6}$ and `1.25e-7` giving
$R_L=2.9994077\times10^{-6}$ (a 20.80% increase) --- this probe
establishes that the warm axial solver cannot certify a flux terminal
of `5e-8`: its flux-update floor under the unchanged TYPE K B1 SIGS
EXTE 500 configuration sits near `5.8e-7`, consistent with the
binary32 flux-update representation, while tightening the terminal
within the reachable range does not reduce $R_L$.  The
tolerance-tightening route to the `5e-7` outer leakage gate is
therefore closed with the present single-precision flux kernel.  This
is an operational solver-floor result, not a physical-model statement;
the exact floor value is bounded only by the `MAXOUT=500` census.  No
empirical parameter or model correction was introduced.

The evidence is frozen under
`validation/artifacts/iterative-rank2-h2-r64-aa1-z-axial-eps5e8/`.
