# D4 map-6: full-coordinate column trace and reference qualification

Completed diagnostic follow-up on 2026-09-28. The frozen full-coordinate
experiment reveals a reference-admissibility problem in addition to slow
iteration. Its 107 fission-free columns lose essentially all scalar flux.
At raw iteration 10 the original sealed Dragon explicitly rejects the saved
field with `SPOSTATE: NONPOSITIVE ACTIVE SCALAR FLUX.`
**There is still no accepted full-coordinate terminal or rank-error estimate.**

## Controlled diagnostic and equivalence

This is a private instrumented replay of the same full-coordinate map-6
SYSTEM, tracking, MACROLIB and initial field. The physical equations, EXTE /
UNKT / THER thresholds (2e-7), REBA OFF and ACCE 3 3 are unchanged. The outer
cap is deliberately 12, with a 900-second wall cap, one thread and no retry.
The original source files, shared libraries and active runtime are untouched.

The only solver-source addition is a call to a passive observer before the
outer gate and acceleration. It reads the input and raw output fields, the
fission data and the acceleration history. It changes no solver array or
LCM object. At iteration 10 it writes a binary explicitly labelled
`UNACCEPTED_COLUMN_TRACE_V1`; this is not a terminal or canonical SPOT state.

The private link uses the original repaired overlay objects and copies of
the original libraries. As a control, relinking the unmodified objects gives
all nine file-backed Mach-O sections identical to the sealed executable.
The instrumented run reproduces **2,615 native numerical IN/OUT log lines**
from the previous attempt exactly, including all matched inner residuals,
outer eigenvalue updates and applied acceleration factors. CPU times are
excluded from that comparison. Three analytic tests independently check
known reweighting, the raw defect and acceleration candidate, and passive
state/checkpoint handling.

The run reached the intentional native outer cap after
624.902 seconds. Its native strict rejection is preserved; no
final `axial.xsm` exists. The runner recorded generic `INCOMPLETE` because its
expected-cap classifier looked for a different log label. The independent
analysis verifies the actual `FLU2DR-DIAG OUTER IEXTF=12 MAXOUT=12` and strict
abort. This postprocessing distinction does not change the original receipt
or promote the calculation to a solution.

## What the trace measures

There are 132 radial columns, exactly 25 with nonzero nu-fission coefficients.
At outer 12:

| Diagnostic | Observed value |
| --- | ---: |
| Eigenvalue input/output defect EEXT | 7.10945557e-06 |
| Raw scalar-flux defect, native EUNK definition evaluated unconditionally | 3.70837293e-03 |
| Native inner EINR | 1.28427879e-07 |
| Global nu-fission-normalized physical flux update, volume L2 | 1.46274075e-03 |
| Sum of absolute changes in column nu-fission fractions | 1.18270717e-03 |
| Maximum within-fission-column shape change after its own normalization | 1.03607909e-04 |

The raw scalar-flux defect is about 18,542 times the declared 2e-7
threshold. The native program normally evaluates this outer defect only when
EEXT passes; the passive observer exposes it earlier without changing that
logic. Per-column normalization is used only to describe shape and amplitude
changes. It is never fed back to the solver.

The scheduled acceleration candidates at outer 10, 11 and 12 are respectively
-1.07845, -3.92401 and -8.03899. The existing REAL64 acceleration routine
applies an update only for a positive candidate. It therefore correctly
keeps an applied factor of 1 at these steps. The trace does not identify an
acceleration implementation bug. It shows continuing column-amplitude
redistribution that a small eigenvalue change would conceal.

## Fission-free flux collapse and direct rejection

The raw-10 binary is independently reread and its defect and physical L2
are reproduced. The following scalar integrals include all groups and cell
volumes, divided by each field's one global nu-fission production. They are
flux diagnostics, not power or source-normalized neutron leakage.

| Column partition | Count | Qualified rank-2 seed, reexpressed in full coordinates | Unaccepted raw iteration 10 |
| --- | ---: | ---: | ---: |
| Fission-producing | 25 | 46.10105798 | 46.1439749 |
| Fission-free | 107 | 59.21218105 | -4.91729331e-19 |

The signed fission-free integral is essentially zero; its tiny negative
remainder is retained. Among the 475,080 scalar entries in those columns,
267,394 are nonpositive in REAL64. The required REAL32 mirrors have
429,697 nonpositive entries, including underflowed values. All 25 fission-column
scalar fields remain positive at this checkpoint. The global update's squared
volume norm is dominated by the fission columns; the fission-free contribution
is only 1.13103e-19 of it after their flux has collapsed.

A separate no-transport probe encodes the raw field in a carrier explicitly
marked `TRACE-ONLY`, removes inherited canonical coordinate records, and supplies
consistent REAL32/REAL64 flux and k mirrors. The original sealed Dragon then
refuses SPOSTATE specifically for nonpositive active scalar flux. No FLU or
ASM module is called, and the carrier remains unchanged. This directly
confirms the checkpoint's inadmissibility under existing rules. It is not
proof that every possible later iterate must fail, nor a reason to floor,
clip or otherwise repair these values.

## Consequence for project direction

The full coordinate basis makes the frozen radial response, local material
terms, intergroup scattering and fission diagonal in radial region. With
axial streaming and vacuum boundaries also local to a column, the frozen
physical operator is a direct sum of column problems. Shared k and global
normalization do not restore off-diagonal radial transport. The implementation
explicitly exploits this exact separation in `SPOT1P64`; fission and
intergroup sources in `FLU2DR64` use the same region index on both sides.

For a fission-free block, zero flux follows if its homogeneous loss operator
is invertible; a singular block instead raises a nullspace question.
Nonzero amplitudes in several fission-producing blocks require compatible
block eigenvalues. This experiment does not compute those spectra or prove
all the relevant invertibility conditions. It does demonstrate loss of the
positive full-domain field while relative fission-column amplitudes continue
to evolve.

Therefore the next step is **reference qualification**, rather than assuming
that a longer frozen full-coordinate run yields the desired physical
benchmark. The [reference contract](frozen_response_reference_contract.md)
states the simultaneous coupled residual equations and a small-model
admissibility check. Its exact two-region example illustrates why a diagonal
response can reproduce an anchor and still lose radial exchange away from it.
The [method derivation](../../SPOT_doc/rederivation.md) now makes this limitation
explicit. None of these findings disproves the reduced coupled method or
attributes the CE gap to a particular approximation.

## Retained evidence

`validation/artifacts/d4a-map6-physical-column-trace-20260928/` preserves the
plan, private build and original-object identities, all numerical and column
logs, the explicitly unconverged checkpoint, independent analysis and the
sealed-Dragon positivity rejection. `result.sha256` seals the local files.
The original failed full-coordinate attempt and completed cold/warm and mesh
experiments retain their original manifests. No new coupled map or CE run
was launched, and the live chain's gates remain unchanged.
