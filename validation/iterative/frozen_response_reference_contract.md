# Qualification of a full-coordinate SPOT reference

The frozen map-6 physical-coordinate experiment tests a particular diagonal
radial-response closure. It does not recover the nonlocal radial transport
operator by increasing the basis rank. This distinction is necessary before
using an enrichment result as the project's full-order accuracy reference.

## Exact two-region example

Consider one fission-producing region coupled to a non-fission region:

\[
 A=\begin{pmatrix}2&-1\\-1&2\end{pmatrix},\qquad
 F=\begin{pmatrix}1&0\\0&0\end{pmatrix},\qquad
 u=\begin{pmatrix}1\\1/2\end{pmatrix}.
\]

Here `A u = (3/2) F u`, so `k=2/3`. The second region has positive flux because
of exchange with the first. A coefficient obtained by dividing each component
of `A u` by the corresponding component of `u` gives

\[
 D(u)=\operatorname{diag}(3/2,0),\qquad D(u)u=Au.
\]

Freezing this diagonal coefficient preserves the equation at the anchor `u`.
It does not preserve the action on another vector: for example,
`A (1,1)^T=(1,1)^T`, whereas `D(u) (1,1)^T=(3/2,0)^T`.
In the unrestricted frozen eigenproblem, the second-region amplitude is now
arbitrary. Perturbing its diagonal coefficient from zero to any nonzero
`epsilon` instead forces that amplitude to zero. A rank-one space spanned by
`u` still fixes the amplitude ratio. Its inverse eigenvalue for the perturbed
diagonal problem is `3/2 + epsilon/4`.

This is an exact algebraic illustration, not a model of D4's measured
spectrum or an error estimate. It shows why coefficient equivalence at an
anchor and a larger trial space do not, by themselves, qualify a positive,
unique full-order transport reference.

## Required reference contract

The proposed *same-closure coupled* target is the simultaneous residual
system already implicit in the method, with a physical coordinate basis:

\[
\begin{aligned}
 R_r(u,\psi,\rho)
 &= [\mathcal A_\perp(L(\psi))-\mathcal S_\perp]u
       -\rho\mathcal F\overline\phi(\psi)=0,\\
 R_z(u,\psi,\rho)
 &=\mathcal T_z\psi+\Sigma_t\psi
       +\tfrac12d_\perp(u,\overline\phi,\rho,L)\phi
       -\mathcal S_\Omega\psi-\tfrac\rho2\mathcal F\phi=0,\\
 R_N(\psi)&=\sum_{i,f,g}V_{if}\nu\Sigma_{f,if,g}\phi_{if,g}-1=0.
\end{aligned}
\]

Here `d_perp` and `L` retain the definitions in equations (7) and (9) of the
[method derivation](../../SPOT_doc/rederivation.md), and `overline(phi)` is
the physical-zone average used by the radial problem. The radial fields,
axial angular fields and the one global inverse k are simultaneous unknowns.
The physical data and boundary conditions are held fixed. This definition
does not assert that the full-coordinate equations have a unique positive
solution, or prescribe an untested nonlinear solver.

The [first coupled check](coupled_reference_nullspace_result.md) is now
complete. Two radial-region S2 vacuum examples, with one and two axial cells,
retain simultaneous radial and shared-leakage feedback yet have a positive
one-parameter family after global normalization. Their exact Jacobian ranks
are 6/7 and 12/13. The free non-fission amplitude changes physical neutron
balance without changing k. Explicit-exchange controls have full normalized
Jacobian rank and zero physical balance defect at their solutions.

Thus the proposed same-closure target is a declared residual system, **not
yet a qualified unique reference**. This counterexample does not establish
the rank of the actual D4 Jacobian. Resolve the amplitude/exchange issue in
the reference specification and qualify more general small models before
scaling to D4. A Newton-type solver or a longer power iteration cannot by
itself establish uniqueness. Appending radial/axial mean-matching equations
removed the null direction in the examples only as a diagnostic control;
their compatibility in a general model is not established.

The [heterogeneous/multigroup extension](coupled_reference_heterogeneous_result.md)
is also complete. Axial material variation retains a positive amplitude family;
an asymmetric two-group one-cell example proves the same freedom with exact
rank 12/13. Three other configurations approach zero-reflector boundary roots
despite small residuals and full numerical rank. In one, k differs from the
explicit-exchange reference by only 0.224 pcm while the physical balance defect
is about 19%. All six explicit-exchange controls pass positive-flux, normalized
local-rank and physical-balance checks. These are network results, not D4
measurements, and do not rule out other positive roots of the ratio equations.

1. **Declare the equations being compared.** Distinguish the frozen diagonal
   closure, the self-consistent 2D/1D equations with refreshed radial response,
   and an independently discretized 3D transport operator. Their differences
   answer different questions.
2. **Qualify radial communication and admissibility.** A physical-coordinate
   frozen closure splits into columns. Identify fission-free columns, any
   nullspaces and incompatible block eigenvalues. A small global k change
   does not certify a positive full-domain eigenfunction. Retain the existing
   active-flux requirements; do not insert a floor to make an export pass.
3. **Define a coupled full-order solve before running one.** If the target is
   the self-consistent equations, include the radial response update and
   physical source exchange in that definition, and demonstrate that their
   amplitudes are determined after normalization. Check physical balance
   as well as closed-equation residuals. Choose an iteration strategy
   that can handle the qualified equations; do not assume repeated exact
   eigen-solves of an independently frozen diagonal operator form a valid
   positive map on the whole domain.
4. **Keep enrichment studies honestly scoped.** An admissible rank-2/rank-3
   comparison can measure sensitivity to that snapshot-space extension.
   It cannot replace a qualified full physical reference or certify an error
   bound. No rank is selected by matching CE.

The [same-operator projection study](exchange_projection_result.md) is complete
on the six previous networks and two four-region unequal-volume extensions.
Forty reduced eigenproblems use bases trained only on prescribed radial
fixed-source snapshots. Full spaces and nonorthogonal coordinates recover the
references. Constant-enriched test spaces preserve whole-domain balance at
truncated rank; ordinary truncated POD need not do so. Conservation alone is
insufficient: the enriched rank-1/2 four-region solutions have large flux
errors, while rank 3 has much smaller errors and full rank recovers the reference.

The [native flight-response check](native_radial_response_result.md) now extracts
the nonlocal action from an eight-region pin mesh for three declared groups.
Four held-out sources per group and 45 fresh boundary-closed sweeps reproduce
the matrix action below 7.4e-15. Raw current-balance defects remain of order
1e-7 before rebalance. A single-anchor diagonal response fails to reproduce
independent sources; the native radial operator also differs from a simple
graph Laplacian. This qualifies collision response and boundary elimination,
not a complete scattering/leakage or coupled eigenproblem.

The [native multigroup/POD study](native_multigroup_pod_result.md) now verifies
that milestone on the same historical pin with all 370 groups. Saved self
scattering already includes binary32 leakage subtraction; the study uses it
once, with off-group scattering and signed coefficients unchanged. Four positive
full fixed-source references pass fresh native source/sweep checks. Sixty-four
POD comparisons recover the reference at full rank. Constant-enriched spaces
preserve the weighted equation residual but retain the native raw balance
defect; enriched rank 2 also develops negative flux in all four configurations.

The [small coupled native candidate](native_axial_coupling_result.md) now
qualifies three full-coordinate meshes using restored physical self scattering,
matched original fission and vacuum axial S2 diamond difference. The normalized
production Jacobians have full numerical rank, with a separately checked
invertible removal matrix; all full scalar and outgoing angular fluxes are
positive. Full-rank angular projection recovers the same references. Nevertheless,
25 of 48 truncated solutions have negative outgoing angles, including cases with
positive scalar flux and conserved weighted equations.

The [subsequent full-space refinement](native_axial_refinement_result.md) now
finds negative outgoing angular flux at every 4–64-cell mesh. At 64 cells,
2178 negative seeds arise at vacuum inflows with nonnegative DD attenuation;
the effective isotropic source is negative. This is a candidate coupling failure
before POD reduction, not solely a reduced-space positivity issue. Its coarse
checks remain scoped to those meshes; the candidate is not a qualified refined
reference. Revisit the radial/angular source-current formulation before new
training or positivity constraints. The candidate remains a frozen nonlocal
P0 closure, not the live ratio closure, and does not authorize a production
basis/rank change.

The [source/current consistency audit](native_source_current_result.md) then
verifies the candidate's declared ledgers. It also establishes that a direct
direction-wise H propagation has no general positivity guarantee: all 370
groups have certified negative small-step outputs from nonnegative inputs.
An exactly conservative positive steady-response control shows that the
native raw balance defect is not required for this obstruction. The next
reference specification must include independently identified directional
information, following the [angular-response contract](native_angular_reference_contract.md),
rather than infer an odd/current operator from scalar R alone.
Changes in closure remain separate from same-operator projection error. These
independent studies do not authorize a new live basis or D4 rank.

The current same-closure full-coordinate reference remains unqualified for
D4. The network control is not a replacement production map or a 3D benchmark.
A larger frozen-run budget does not resolve the issue. The running rank-2
coupled chain and its original acceptance gates retain their unchanged purpose.
