# Native radial flight response and boundary-current qualification

Completed on 2026-09-28. A nonlocal scalar response can be recovered directly
from the native radial MOC sweep and verified on independent sources, before
ACA or global rebalancing. Boundary elimination reproduces fresh native sweeps
to 7.39e-15 relative error. The raw current balance is only approximately
conservative: its measured defect is of order 1e-7 and is retained unchanged.

This qualifies a **collision/flight response on one historical pin mesh**.
It does not qualify a full multigroup fixed-source problem, the coupled axial
closure, a D4 reference, or a production replacement. The mathematical network
studies and this native extraction answer different questions.

## Inputs and native path

The historical `raw-moc-capture/common` bundle supplies the read-only TRACK,
SYSTEM and binary rays. Their hashes match the earlier capture protocol.
There are eight physical regions, six boundary surfaces and 370 stored groups.
Groups 1, 185 and 370 were declared before execution. The original boundaries
are unit white albedo with identity return mapping.

A private Fortran host links copies of the four sealed libraries from the
physical-column diagnostic. It calls the same native sequence as the raw stage
of `MCGFL164` in [SPOR64_A8.f90](../../src/SPOR64_A8.f90): initialize the
exponential tables with `XDRTA2`, recover coefficients with `MCGSIG`, establish
isotropic harmonics with `MOCIK3`, then call `MCGFCF` with
`MCGFFIR64_RANK_ADAPTER`/`MCGSCA`, followed by `MCGFST` source isolation.
`MCGFST` divides by the saved native volume/surface weights and adds the saved
PJJ self-source contribution. Neither ACA nor `FLUBAL64` is called.

Native total coefficients, polar quadrature, weights and PJJ are binary32;
sources and responses are binary64. The tabulated exponential route is retained.
Stored self-scattering coefficients are exported for provenance but are **not
used** in this collision-only experiment. No fission source, scattering iteration
or axial leakage feedback is included.

The runtime and D4 inputs were untouched. Compilation is confined to the new
artifact directory, with one thread and a 30-second cap per private invocation.

## Response and boundary equations

With physical-region order followed by physical-boundary order, the native
linear action is

\[
\begin{pmatrix}\phi\\j_o\end{pmatrix}
=T\begin{pmatrix}q\\j_i\end{pmatrix},\qquad
T=\begin{pmatrix}T_{vv}&T_{vb}\\T_{bv}&T_{bb}\end{pmatrix}.
\]

Here q is prescribed volumetric source density. Boundary unknowns are native
incoming/outgoing amplitudes; multiplication by their saved surface weights
gives the integrated currents. They are not already net leakage.

Fourteen coordinate sources identify T. Four held-out patterns per group
(mixed positive, signed, boundary-only and volume-only) are then independently
swept. For boundary return matrix B, retaining the saved permutation,

\[
j_i=Bj_o,\quad J=(I-T_{bb}B)^{-1}T_{bv},\quad
R=T_{vv}+T_{vb}BJ,\quad \phi=Rq,\quad j_o=Jq.
\]

The experiment uses B equal to zero, half the saved albedo, and the saved
albedo. These are declared diagnostic boundary closures on unchanged tracks.
They are not three production pin runs.

Each closure is checked with five sources: uniform anchor, positive linear
ramp, first-region-only, last-region-only, and alternating signed perturbation.
Each source has unit volume-weighted absolute integral. Positive and signed
perturbations have separate interpretations; signed fields are algebra probes.
For all 45 cases, q and the eliminated incoming boundary field are sent back
through a fresh native sweep. Agreement is not inferred solely from multiplying
the extracted matrix.

The scalar loss and radial action are

\[
H=R^{-1},\qquad C=H-\operatorname{diag}(\Sigma_t).
\]

The native current ledger is evaluated before any balancing correction:

\[
\delta=\mathbf1^TWq+\mathbf1^TW_bj_i
       -\mathbf1^TW\Sigma_t\phi-\mathbf1^TW_bj_o.
\]

The primary relative defect divides by the volume-weighted absolute source
plus absolute incoming current. Volume-source-only normalization is also
reported, so a large reflected inflow cannot hide the accumulated defect.
The corresponding arbitrary-field row identity is checked as

\[
\mathbf1^TWC\simeq\mathbf1^TW_b(I-B)JH.
\]

The approximation sign is intentional. No coefficient fit, rebalancing,
symmetrization, diagonal repair or positivity clipping is applied.

## Results

The declared action tolerance is 5e-12; the declared raw current-balance
tolerance is 1e-6. The latter is a diagnostic criterion, not a D4 acceptance
gate or proof of a precision floor.

| Check | Measured maximum |
| --- | ---: |
| Held-out flight action, relative infinity norm | 6.814e-15 |
| Fresh boundary-closed native action | 7.383e-15 |
| Fresh boundary-return residual | 5.203e-15 |
| Raw flight balance / absolute source and incoming current | 1.438e-7 |
| Closed balance / absolute source and incoming current | 1.077e-7 |
| Closed balance / absolute volumetric source only | 4.080e-7 |
| Scaled arbitrary-field balance-row defect | 6.869e-8 |
| Scalar response condition number | 1818.30 |

All 36 nonnegative-source closure cases have strictly positive regional flux.
The smallest is 3.269e-4. Weighted scalar-response reciprocity defects are at
most 2.026e-16. These observations concern this fixture and these groups.

The 1e-7-scale current defects coexist with binary32 native coefficients and
weights, but this experiment does not isolate their cause or establish a
resolution-independent numerical floor. In particular, the much smaller global
balance previously measured after `FLUBAL64` cannot independently validate this
raw flight action: that routine explicitly solves a group rebalance system.

### A diagonal anchor does not retain nonlocal response

For the uniform-source anchor, set D=diag(q0/phi0). Equivalently,
`D = diag(total) + diag((C*phi0)/phi0)`: it retains the native radial action at
that field. It reproduces its anchor to roundoff.

Keeping D fixed, solve `D*phi=q` for the independent positive ramp. Against
the same boundary-closed native reference, its volume-weighted flux errors are:

| Group | Vacuum | Half albedo | Original white boundary |
| --- | ---: | ---: | ---: |
| 1 | 39.420% | 51.380% | 59.450% |
| 185 | 35.178% | 47.447% | 56.229% |
| 370 | 16.307% | 24.509% | 31.438% |

These are descriptive collision-response errors on a deliberately changed
source. They are not D4 flux errors and do not predict the error of a converged
nonlinear ratio iteration. They directly demonstrate what is lost when a
single field's diagonal ratio is treated as the whole native linear action.

The recovered C also has positive off-diagonal entries (8–18 of 56, depending
on group/boundary). It must not be silently replaced with the nonpositive
off-diagonal graph Laplacian used in the manufactured networks. Preserve the
native response and current functional when developing the next comparison.

## Verification and next step

Eight standalone NumPy tests pass. They include a separate joint-system oracle
for boundary elimination with unequal albedos and a noncommuting return map,
unequal-weight current accounting, signed-source normalization, held-out native
actions and the fresh closed-source evidence. The final private host repeats
all 54 initial flights byte for byte. There are 99 distinct flights plus those
54 replay flights. Archived analysis is replayed independently before sealing.
All 997 protected source/runtime/input files and all 233 manifest entries from
the seven preceding studies remain unchanged. This study does not modify the
shared fast-test runner or add NumPy to its required dependencies.

The next bounded study should qualify `H - S_self + L` together with the exact
off-group fixed-source definition on a small native multigroup problem. Trace
whether leakage is embedded in a saved scattering coefficient before using it;
do not count it twice. Then compare full coordinates and fixed POD spaces of
that **same** operator, retaining its actual boundary-current functional and
measured native balance defect. Only afterward assess a candidate axial coupling.

The one-group source-elimination algebra does not establish the reference's
coupled admissibility, physical reaction-rate accuracy or mesh convergence.
It supplies a native operator action with a verified meaning for that next step.

The subsequent [370-group fixed-source/POD study](native_multigroup_pod_result.md)
has now completed the scattering/leakage and same-operator projection checks.
It retains the raw native balance defect and exposes a separate low-rank
positivity issue. Coupled axial eigenreference qualification remains open.

Files: [native host](probe_native_radial_response.f90),
[analysis](qualify_native_radial_response.py),
[tests](test_native_radial_response.py),
[declared plan](../artifacts/native-radial-response-20260928/plan.json),
[full matrices and results](../artifacts/native-radial-response-20260928/analysis/result.json).
