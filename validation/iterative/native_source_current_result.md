# Native source/current audit: a steady scalar response is not an angular generator

Date: 2026-09-28. Artifact: `validation/artifacts/native-source-current-consistency-20260928`.

**The candidate's declared source/current identities are consistent, but its
scalar radial response does not supply a positive axial angular propagation
law.** A direct direction-wise use of `H=R^-1` also fails the positivity test in
all 370 groups, including exact matrix-exponential propagation. The next
reference milestone is to retain and qualify native directional information,
as specified in the [angular-reference contract](native_angular_reference_contract.md).

This audit uses the saved 1–64-cell fields and native response matrices. It
does not solve or modify a coupled eigenproblem. It does not identify H with
the native angular transport operator, and it makes no new D4 error claim.

## The source and current ledgers agree

Define the cell-average axial current and the unchanged corrected source as

\[
J=\mu(\bar\psi^+-\bar\psi^-),\qquad
p=S^{phys}\phi+\rho F\phi.
\]

The rejected candidate satisfies two separate moment equations:

\[
 D_zJ+H\phi=p,\qquad
 \mu^2D_z\phi+\Sigma_tJ=0.
\]

The audit rebuilds these from the saved angular faces and nodal scalar fields.
It separately computes `p-D_z J`, without using `H*phi` for that calculation,
and feeds it into the previously verified raw native flight matrices with the
stored white return. Across all seven meshes:

- The largest even-moment residual is 2.54e-13 relative to the source scale.
- Regional scalar flux replays within 1.78e-14 in weighted relative norm.
- The outgoing boundary relation replays within 4.22e-16.
- Axial current divergence telescopes to vacuum outflow within 2.23e-16.
- Raw radial balance retains the preceding defect, at most 9.25e-7 of birth.

This is matrix replay of already native-verified flights, not a claim of new
native sweeps in this artifact. White return has zero net radial boundary
current. Both its inferred outgoing boundary field and the replayed regional
scalar field remain nonnegative at the stored numerical precision.

The two effective sources are different objects:

\[
q_{rad}=p-D_zJ=H\phi,\qquad
q_{ax}=p-C\phi=\Sigma_t\phi+D_zJ.
\]

Both are retained signed. At 64 cells, 40560 entries of the inferred radial
source and 8694 entries of the effective axial source are negative. Even the
coarse admitted fields have negative inferred radial-source entries. These
counts alone are not a new admissibility criterion: effective leakage sources
and transport-corrected scattering can be signed. In particular p itself has
18 negative entries per cell from the unchanged corrected data. Angular
positivity must be checked on the reconstructed directional field, not inferred
from a blanket requirement that every effective source be positive.

There is no evidence here of a source/current sign mismatch or a missing
global balance term in the implemented candidate. The failed angular fields
solve the declared equations accurately; that fact does not validate the
closure used to define those equations.

## The even equation does not determine the odd equation

The existing isotropic radial insertion `C*phi/2` is identical in both axial
directions. It contributes C phi to the even equation and cancels from the odd
equation. A direction-wise insertion would instead be

\[
C\bar\psi^\pm=\tfrac12 C\phi\ \pm\ \frac{1}{2\mu}CJ.
\]

Its even sum is unchanged, while the odd equation acquires C J. The measured
weighted norm ratio `||CJ|| / ||total*J||` is about 67.36 on two cells,
400.29 on four cells and 468.97 on 64 cells. On the one-cell symmetric case the
cell-average current is zero at numerical precision, so the ratio is left
undefined. These are algebraic differences, not estimates of the correct
native odd operator.

Consequently, passing the global even/current ledger cannot select or verify
the odd radial response. Adding C J would be a substantial change to the
candidate, and the following test shows that it is insufficient as a general
positivity repair.

## Direct H propagation fails independently of diamond difference

For the direction-wise control, consider source-free propagation in one
direction, `d_z psi = -H psi / mu`. Its exact and backward-Euler maps are

\[
E(\tau)=\exp(-\tau H),\qquad
P(\tau)=(I+\tau H)^{-1},\qquad \tau=\Delta z/\mu.
\]

For nonnegative input in every regional coordinate to remain nonnegative,
these matrices must be entrywise nonnegative. But for i different from j,

\[
E_{ij}(\tau)=-\tau H_{ij}+O(\tau^2).
\]

Thus any positive off-diagonal H entry produces a negative output from a
nonnegative unit input for sufficiently small steps. This is a local derivative
argument, not an inference from a finite mesh failing to converge.

All 370 native groups have significant positive off-diagonal entries: 3452
entries in total. Each group's largest such entry is at least 0.0070712 times
that group's infinity norm. They are far larger than the measured raw balance
defect. No off-diagonal is clipped or replaced.

All columns are checked at the predeclared scaled steps
`theta=tau*||H_g||_inf`. The following minima are across groups and entries:

| theta | Groups with negative exact propagation | Minimum exact entry | Minimum backward-Euler entry |
| ---: | ---: | ---: | ---: |
| 1e-6 | 370 / 370 | -3.22640e-8 | -3.22639e-8 |
| 1e-3 | 370 / 370 | -3.22510e-5 | -3.22380e-5 |
| 0.1 | 370 / 370 | -0.00309890 | -0.00297985 |
| 1 | 370 / 370 | -0.0212880 | -0.0152742 |

Backward Euler also has negative entries in all 370 groups at every listed
step. The largest theta-0.1 exact witness is group 98, unit input in region 1,
negative output in region 3. Its physical step is 0.000300665 cm. This is a
propagation-control example, not a new coupled physical benchmark.

Every group also has a finite small-step certificate. With
`r=H_ij/||H||_inf` and `theta=min(1e-6,r/4)`, the exponential remainder is bounded
by `theta^2*exp(theta)/2`, and the inverse remainder by `theta^2/(1-theta)`.
Both upper bounds on the selected entry remain strictly negative. The saved
computed entries satisfy the same sign. Failure therefore persists even with
exact angular stepping for this proposed generator; changing the DD rule alone
does not give this direction-wise H control a positivity guarantee.

## Conservation and positive steady response are insufficient

The raw native response is retained exactly. It contains 12 tiny negative
entries in one group, with minimum -2.88e-20, or -6.14e-20 relative to that
matrix's infinity norm. These are disclosed rather than silently clipped or
used to explain the much larger generator counterexamples.

To separate the structural result from any native numerical defect, the audit
also constructs the symmetric, strictly positive three-region response

\[
R=\begin{bmatrix}1&0.3&0.01\\0.3&1&0.3\\0.01&0.3&1\end{bmatrix}.
\]

Its inverse has the exact entry `H_13=800/8217=0.0973591...>0`. Defining positive
`total=H*1=(70/83,41/83,70/83)` makes
`C=H-diag(total)` exactly conservative in the defining real-arithmetic model;
the recorded binary64 row/column sums are below 5.56e-17. R maps every nonzero
nonnegative source to positive flux, yet both exact and implicit H propagation
have negative entries. The native raw current defect is therefore not needed
for this obstruction to occur.

## What information is missing

The native implementation carries track-direction fields before summing them
into regional scalar flux. [MCGFFIR](../artifacts/native-source-current-consistency-20260928/inputs/MCGFFIR.f)
updates RP/RM along a track; those directions
are not automatically the axial S2 signs. Its `OMEGA2` argument contains squared
components, so it cannot by itself identify signed axial response.
[MCGFST](../artifacts/native-source-current-consistency-20260928/inputs/MCGFST.f)
also restores the self-source contribution isolated during the flight; an
accumulator captured before that step is not the complete angular field.

The next bounded task is therefore to audit a directional-response interface
on private copies, including direction/sign conventions and source isolation,
and show that its aggregation recovers the existing native R and current
functional. Then identify an odd/current response from independent excitations.
The [contract](native_angular_reference_contract.md) specifies the extraction
points and admission checks. It does not claim this response has already been
built or that a corrected coupled reference has been found.

No production source, live D4 map, shared build, basis or rank is changed.
Eight independent tests cover moment reconstruction, current telescoping,
odd/even splitting, positive controls and finite negative-propagation bounds.
Replay and integrity details are in the artifact's verification receipt.
All 18 analysis files replay byte for byte, including 107 exactly equal numeric
arrays. Both working and archived test copies pass all eight tests. All 997
protected files, 20 source inputs and 978 manifest entries from eleven previous
artifacts retain their hashes. No new coupled reference is marked qualified.

Files: [audit](audit_native_source_current.py),
[tests](test_native_source_current.py),
[predeclared plan](../artifacts/native-source-current-consistency-20260928/plan.json),
[results](../artifacts/native-source-current-consistency-20260928/analysis/result.json),
[generator witnesses](../artifacts/native-source-current-consistency-20260928/analysis/generator_audit.json),
[verification](../artifacts/native-source-current-consistency-20260928/verification.json).
