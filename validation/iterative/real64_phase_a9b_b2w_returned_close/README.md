# Phase A9b / B2w returned-close validation

This directory validates the production `SPOR64_B2W_CLOSE` gate with a
bounded synthetic fixture. It does not run Dragon, FLU, ASM, transport, or
Picard. The harness does make one real call to `SPOLEAK`, using a one-region,
three-floor synthetic axial track and local `REDGET`/`REDPUT` parser stubs.
That call produces the returned child leakage, `SPOT-ITER-K`, and
`SPOT-L1-ERR`; no leakage result is injected after the call.

The pre-SPOLEAK child and `SYSTEM/SPOT-LEAK1D` values are both zero, matching
the B2R binding between the solved child and its lagged radial equation. The
real SPOLEAK call updates only the child to L1 values 0.125, 0.25, and 0.5.
Thus `SPOT-L1-ERR` is the exact binary32 maximum of `abs(L1-L0)`, namely 0.5.
The closing gate checks that identity but does not require lagged SYSTEM L0
to equal returned L1.

## Contract exercised

- `use SPOR64_B2W` and
  `SPOR64_B2W_CLOSE(ipaxout,iparchiveout,ipax,ipfeedback,status)`.
- Four distinct roots, two fresh outputs, and zero writes on every rejection.
- An unsealed canonical SPOSTATE `L_FLUX` AX bundle. Its ordinary FLUX record
  is permitted in addition to the prescribed `SPOT-X-*` bundle.
- `SPOT-X-RHO` is bitwise
  `1.0_real64/real(K-EFFECTIVE,real64)`, and every `SPOT-X-L` value is the
  exact binary32-to-binary64 promotion of the returned child leakage.
- The feedback root is exact nine records and `RETURNED/1`. Its three solved
  children retain a common `rho0`, common binary32 `SPOT-FS-K`, `QFISS`, and
  exact REAL64 authority plus REAL32 mirrors. `rho0` is deliberately unequal
  to the new AX `rho1`.
- The closed AX is a deep copy plus `CLOSED/1`. The output archive is exact
  eight root records (dropping `SPOT-L1-ERR`), has root `rho1`, `CLOSED/1`,
  and recursively copies all four indexed lists without changing child
  `SOLVED/1`, `rho0`, `SPOT-FS-K`, FLUX, SOUR, or QFISS.

The 25 dynamic rejections cover output aliasing/freshness; bad AX reciprocal,
layout and NaNs; feedback root schema/state/epoch; root K; returned leakage;
negative, NaN, and finite-but-wrong L1 error; SYSTEM L0 and SYSTEM rho;
child rho/state/epoch/QFISS/mirrors/forbidden PLANE; and child K consistency
and reciprocal binding. Each rejection checks both output roots for zero
writes (the nonfresh sentinel is preserved exactly).

The strongest production claim is deliberately content-scoped: given the
supplied canonical AX and returned-feedback objects, B2w proves the listed
schemas and bitwise identities and performs one logical `CLOSED/1` commit.
Because the public gate accepts detached objects, it does not prove that this
AX was historically produced from this exact archive by an immediate
`ASM -> FLU -> SPOSTATE -> SPOLEAK` call chain. That causal claim is reserved
for a later default-off wrapper that owns the complete sequence in one call.

This phase also does not claim an online axial solve, a complete real raw
Picard map, outer convergence, an independent radial or axial equation
residual, eigenvalue/leakage/power accuracy, rank-one truncation accuracy,
benchmark qualification, full-core validation, or cross-platform
reproducibility.

## Independent posterior

`check_b2w_returned_close.f90` is a standalone GANLIB-only reader. It neither
imports nor calls B2W, B2R, SPOLEAK, or a solver. It opens four XSM evidence
files read-only and verifies lifecycle, exact root inventories, K/RHO and
L1/L0 identities, all 1,110 leakage promotions, all 46,620 REAL64 authority
values and mirrors, and recursive separation/content of the four copied
lists. The runner executes it twice, compares its reports, and proves that
all four evidence hashes remain unchanged.

Run:

```sh
validation/iterative/real64_phase_a9b_b2w_returned_close/run_phase_a9b_b2w_returned_close.sh
```

The runner uses the frozen Darwin arm64 compiler, strict Fortran flags,
bounded CPU/file limits, static mutation checks, symbol audits, and a trap
that removes every temporary build and XSM product. Its receipt binds the
frozen B2v parent, production sources, validation inputs, dependencies, and
project documentation. This is synthetic interface/lifecycle validation,
not a transport or convergence claim.
