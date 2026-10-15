# Concise derivation of fixed-space Galerkin–SPOD

This document defines the SPOT equations used by the implementation. It keeps
the mathematics deliberately small: one fixed POD space, one online radial
fixed-source problem, one reduced axial problem, and direct Picard iteration.

## 1. Fixed radial space

For energy group $g$, collect normalized offline radial snapshots in $P_g$.
With radial volume matrix $W=\operatorname{diag}(w_i)$, compute

\[
W^{1/2}P_g=U_g\Sigma_gZ_g^T,
\qquad
B_g=W^{-1/2}U_{g,1:r_g}.
\tag{1}
\]

Thus $B_g^TWB_g=I$ in exact arithmetic. Stored finite-precision bases need
not be exactly orthonormal, so the implementation retains the Gram matrix

\[
M_g=B_g^TWB_g.
\tag{2}
\]

The rank $r_g$ is a spatial discretization order. The basis and rank remain
fixed during one convergence study.

## 2. Coupled state

Let $\mathcal R_s$ volume-restrict the axial scalar flux to radial plane $s$.
The POD coordinates satisfy

\[
M_g a_{s,g}=B_g^TW\mathcal R_s\Phi_g,
\qquad p_{s,g}=B_ga_{s,g}.
\tag{3}
\]

After one global fission-production normalization, define

\[
x=(a,\rho,L),\qquad \rho=1/k.
\tag{4}
\]

$L_{s,g}$ is the signed axial leakage coefficient for plane $s$ and group
$g$. No group-wise, plane-wise, or region-wise rescaling is allowed.

## 3. Online radial problem

Given $x$, reconstruct $p=Ba$. For every radial plane, solve

\[
[\mathcal A_{\perp,s}(L_s)-\mathcal S_{\perp,s}]u_s^+
=\rho\,\mathcal F_s p_s.
\tag{5}
\]

The right-hand-side fission term is frozen during this solve. Multigroup
scattering is converged, but fission is not reevaluated from $u_s^+$.

The source associated with the final radial field is

\[
q_{s,g}^+
=\sum_{h\ne g}\Sigma_{s0,h\to g}u_{s,h}^+
 +\rho(\mathcal F_s p_s)_g.
\tag{6}
\]

The radial response used by the axial equations is then

\[
d_{\perp,s,g}^+
=-\Sigma_{t,s,g}+\Sigma_{s0,g\to g}
 +\frac{q_{s,g}^+}{u_{s,g}^+}-L_{s,g}.
\tag{7}
\]

Equations (5)–(7) use the same frozen fission source. Replacing it with
$\mathcal F_su_s^+$ would define a different nonlinear map.

## 4. Reduced axial problem

Project the radial response into the fixed space:

\[
D_{s,g,ab}^+
=\langle B_{g,a},d_{\perp,s,g}^+B_{g,b}\rangle_W.
\tag{8}
\]

Write the angular approximation as
\(\psi_{g,i}(z,\mu_n)=\sum_a B_{g,ia}A_{g,a,n}(z)\), and its modal
Legendre moments as \(a_{g,\ell}=\sum_n w_nP_\ell(\mu_n)A_{g,n}\).
With \(T_g=B_g^TW\Sigma_{t,g}B_g\),
\(S_{\ell,h\to g}=B_g^TW\Sigma_{s,\ell,h\to g}B_h\) and
\(F_{h\to g}=B_g^TW\chi_g\nu\Sigma_{f,h}B_h\) (summed over fission
components where required), the reduced angular equation is

\[
\mu_n M_g\frac{dA_{g,n}}{dz}+T_gA_{g,n}
+\frac12D^+_{s(z),g}a_{g,0}
=\sum_{h,\ell}\frac{2\ell+1}{2}P_\ell(\mu_n)
 S_{\ell,h\to g}a_{h,\ell}
+\frac{\rho^+}{2}\sum_hF_{h\to g}a_{h,0}.
\tag{8a}
\]

The actual within-group solve moves self scattering to the left; off-group
scattering and fission enter its iterated source. The radial response acts
only in the P0 angular moment. `SPOT1P64` normalizes all radial integration
weights by the same total area, which scales every term above equally. It
retains the full mass/Gram matrix, uses S_N quadrature and diamond spatial
differencing, and solves the end-boundary problem. D4 has vacuum axial ends.
The three physical material/snapshot zones can contain more than three axial
numerical cells; numerical refinement does not create additional snapshots.

This eigenproblem gives $\Phi^+$, $k^+$, and new coordinates through (3).
The returned leakage is the integrated axial current balance

\[
L_{s,g}^+
=
\frac{\displaystyle
 \sum_{f\mapsto s}\sum_i A_i^\perp
 (J^z_{g,i,f+1/2}-J^z_{g,i,f-1/2})}
{\displaystyle
 \sum_{f\mapsto s}\sum_i A_i^\perp\Delta z_f\Phi^+_{g,i,f}}.
\tag{9}
\]

Equation (9) is an identity for the saved integrated current and scalar flux.
Using that one coefficient for every radial region of a physical plane/group
in (5) is a spatial closure approximation. Representing transverse transport
in (8a) by the scalar-balance response acting only on P0 is another closure
approximation. Neither coefficient is empirically fitted.

These approximations are distinct from POD truncation. Increasing to a full
physical radial basis removes the trial-space restriction but retains the
2D/1D closures. Full rank of the snapshot matrix need not be physical full rank.
An outer fixed point therefore establishes consistency of this discrete map,
not equivalence to the full three-dimensional transport equation. Rank, mesh,
angle and same-data 3D comparisons address different error sources.

There is an additional qualification for a **frozen-response** physical-basis
test. With the diagonal coordinate basis, all material, scattering, fission
and frozen radial-response matrices in (8a) are diagonal in radial region.
The axial streaming and vacuum boundary conditions also act within each
region. Thus this particular frozen eigenproblem splits into independent
radial-column blocks:

\[
  [\mathcal A_{z,i}(d_i)-\mathcal S_i]\psi_i
  =\rho\,\mathcal F_i\psi_i,\qquad i=1,\ldots,N_r.
\tag{8b}
\]

The global k, normalization and acceleration couple the numerical iteration,
but do not supply missing off-diagonal physical transport to (8b). A nonzero
solution in several fission-producing blocks requires a common eigenvalue
of those blocks. For a block with zero fission operator, an invertible
left-hand operator implies zero flux; a singular block instead requires a
nullspace analysis. Neither invertibility nor a common block spectrum follows
from the existence of the rank-restricted eigenpair.

This does not invalidate the declared reduced method. It limits the use of
an independently frozen full-coordinate eigenproblem as a physical reference
for it. Numerical rank sensitivity, when a terminal exists, remains a
property of that frozen operator. A coupled full-order reference must also
qualify how radial source exchange, block compatibility and positive active
flux are maintained when the response is updated through (5)–(7).

Refreshing that response is not by itself sufficient. An
[exact manufactured coupled check](../validation/iterative/coupled_reference_nullspace_result.md)
retains the ratio closure and shared leakage feedback in two-region S2 vacuum
models. Both the one-cell and two-cell cases admit a positive non-fission
amplitude family after global normalization, with identical k and leakage
but different physical balance defects. Their normalized residual Jacobians
have one null direction; explicit radial-exchange controls are locally regular.
This is a counterexample to assuming general full-coordinate admissibility,
not a calculation of the D4 Jacobian or proof that every configuration has
this degeneracy. The [reference contract](../validation/iterative/frozen_response_reference_contract.md)
therefore requires amplitude and physical-balance qualification before using
a complete-coordinate coupled result to assess POD error.

The [heterogeneous/multigroup extension](../validation/iterative/coupled_reference_heterogeneous_result.md)
retains that freedom in an asymmetric two-group exact example. Other small
configurations instead approach zero-reflector boundary roots with full
numerical Jacobian rank and finite physical balance defects. This is consistent
with (8b): zero angular flux in every group of a non-fission column satisfies
its homogeneous axial equations even when radial response coefficients are
updated. Thus full rank, positivity of a finite stopping iterate and a small
residual must not be mistaken for an admissible positive limiting reference.
Conservative explicit-exchange controls qualify the six manufactured networks;
their different closure has not been substituted into the production method.

The subsequent [same-operator POD study](../validation/iterative/exchange_projection_result.md)
uses the conservative network operator as both reduced and full target.
Including the constant radial test function in every group makes the weighted
sum of physical equations a linear combination of projected equations, so
their global neutron balance follows from the projected residual. Ordinary
truncated POD need not contain that test function. This conservation property
does not guarantee local accuracy; full-coordinate recovery and flux errors
are checked separately. These network projection results do not alter (5)–(9)
or establish the corresponding native transport operator.

The [native radial flight study](../validation/iterative/native_radial_response_result.md)
subsequently extracts the pre-ACA, pre-rebalance response T mapping volumetric
source and incoming boundary amplitudes to regional flux and outgoing currents.
For a boundary return B, its scalar response is
`R = Tvv + Tvb B (I - Tbb B)^(-1) Tbv`, with radial action
`C = R^(-1) - diag(total)`. Independent sources and fresh boundary-closed native
sweeps recover this action on a historical eight-region pin mesh. Current
balance retains a measured defect of order 1e-7; it is not forced to zero.
Single-anchor diagonal response misses independent source action. This result
qualifies collision response and boundary elimination only. It does not replace
equations (5)–(9).

The [native multigroup/POD extension](../validation/iterative/native_multigroup_pod_result.md)
now checks self/off-group scattering and prescribed leakage on all 370 groups
of that pin. Its legacy self coefficient already contains the saved leakage;
the verified raw fixed-source matrix is `blockdiag(H_g) - S_used + lambda I`,
where lambda is only the extra prescribed leakage. Full coordinates and full
POD spaces agree. A constant test function preserves the weighted equation
residual, but the intrinsic raw-flight balance defect remains; low-rank local
positivity also requires a separate check. These are fixed-source results,
not qualification of the candidate coupled axial eigenproblem.

The subsequent [native axial candidate](../validation/iterative/native_axial_coupling_result.md)
uses the original component-wise fission data and restores physical self
scattering, removing the old prescribed leakage. Its frozen equations are
`+-mu*d_z(psi) + total*psi + C*phi/2 = S_phys*phi/2 + rho*F*phi/2`,
with vacuum S2 diamond difference. Three full-coordinate small meshes pass
positivity, current-ledger and normalized local-rank checks. Angular Galerkin
projection precedes exact angular elimination; full radial spaces recover the
references. Twenty-five of 48 reduced solutions have negative outgoing angular
flux, including cases whose scalar flux is positive. Constant enrichment
preserves the weighted equation but cannot guarantee angular admissibility.
This linear candidate has a different closure from equations (5)–(9); neither
its coarse axial accuracy nor its equivalence to 3D transport is established.

The [full-space axial-refinement check](../validation/iterative/native_axial_refinement_result.md)
now rejects that candidate on all five grids from 4 through 64 cells. An exact
nodal reformulation of the same S2-DD equations recovers the three earlier
dense solutions, then exposes negative outgoing angles under refinement.
Scalar flux remains positive. The offending directions have nonnegative DD
attenuation coefficients; negative effective sources
`S_phys*phi + rho*F*phi - C*phi` at vacuum inflows provide explicit seeds.
Native R remains verified, but inserting its scalar C isotropically into the
axial equations is not thereby a qualified positive angular coupling. Resolve
that candidate source/current consistency before using it as a POD reference.

The [source/current audit](../validation/iterative/native_source_current_result.md)
now verifies the declared even and odd identities and the native scalar/current
replay on all seven meshes. The even equation contains H while the odd equation
contains total. A direction-wise C lift would add C J to the odd equation, but
this is not a qualified repair: every group has a significant positive
off-diagonal H entry, yielding a negative entry of exp(-tau H) for sufficiently
small positive tau. Finite remainder bounds confirm all 370 witnesses, and an
exactly conservative three-region positive-response example has the same
obstruction. Steady scalar R and global balance do not determine a positive
angular generator. The [directional-response contract](../validation/iterative/native_angular_reference_contract.md)
specifies the missing native information and recovery checks before a revised
coupled reference is introduced.

The [native planar extraction](../validation/iterative/native_directional_response_result.md)
now retains ray coefficients B and own-source integrals D before angular
summation. A separately disclosed regional PJJ rounding remainder recovers
the native completed scalar response; 93 independent native flights agree
within 1.59e-14 per source. Explicit paired x-odd sources produce a measured
planar current response. Native 2D harmonics omit axial odd modes, so this
result does not identify axial propagation. The
[signed axial-state contract](../validation/iterative/native_signed_axial_contract.md)
requires an explicit extra sign state, calibrated isotropic limit and
consistent white-boundary redistribution before a coupled extension.

The [signed-state experiment](../validation/iterative/native_signed_axial_result.md)
now checks that explicit zero-gradient extension against 648 native flights.
It recovers the original 93 P0 cases and measures an axial odd response with
both signs sharing a common white return. A separate-sign-return control
changes Jz by 44–181% while leaving scalar flux equal to roundoff. This
distinguishes directional boundary physics that scalar R does not determine.
The [axial-streaming experiment](../validation/iterative/native_axial_streaming_result.md)
retains an axial-cell vector within each radial characteristic. Its explicitly
declared native-coefficient lift passes constant-mode, positivity and raw
even/odd balance checks on 1/2/4/8 cells. However, the 4-to-8-cell axial escape
change is 1.88–6.11%, above the declared 1% gate. The subsequent
[same-operator 16/32/64-cell refinement](../validation/iterative/native_streaming_refinement_result.md)
also retains positivity and balance, but white-boundary escape still changes
by 2.64–5.03% between 32 and 64 cells. Scalar changes alone fall below 1%.
This remains an unqualified spatial reference. The
[independent analytic axial check](../validation/iterative/analytic_axial_slab_result.md)
now finds two adjacent-grid false admissions and substantial conservative
scalar error hidden by the escape balance. Its exact interior stencil
identity exposes the additional upwind diffusion term. The completed
[cell-characteristic slab comparison](../validation/iterative/axial_cell_characteristic_result.md)
passes the declared finest-grid analytic target: worst scalar and total-escape
errors are 0.565% and 0.270%, with positive source-basis responses and raw
balance. This qualifies the one-dimensional discretization only. A
[native segment-composition audit](../validation/iterative/native_segment_composition_result.md)
now confirms exact-exponential partition invariance, while native tabulated
responses change by up to 2.96e-5 relative and fail the strict equality gate.
The completed [exact-kernel full-flight comparison](../validation/iterative/exact_native_flight_result.md)
qualifies its zero-gradient companion through track aggregation and common
white return. Weighted scalar differences reach 2.488 ppm at fixed input and
1.194 ppm after reclosure; exact full-flight partition recovery is within
8.61e-16 on the declared induced scale. The completed
[oblique-strip geometry experiment](../validation/iterative/oblique_strip_geometry_result.md)
qualifies actual axial crossings with positive unit responses and exact
shared-face matching. Order-16 analytic mean/current errors are below
1.12e-14; order-2 face errors reach 2.54% despite near-roundoff conservation.
The completed [native-track pilot](../validation/iterative/native_oblique_track_pilot_result.md)
retains original path lengths, angular states, repeated-region mappings and
weights on eleven deterministically selected paths. All 931,584 unit responses
are nonnegative; zero-gradient whole-track integral/outgoing recovery is
within 3.45e-15, and geometry/reflection errors remain below 1.72e-12.
Thirty-one tests and complete byte-identical replay pass. The completed
[full-native geometry preflight](../validation/iterative/native_oblique_full_preflight_result.md)
now accounts for all 11,364 paths and 7.856 billion pieces. Local measure errors
stay below 1.88e-12; independent counts and full replay pass. Stored normalizer
differences remain separate from geometric measures. The
[bounded streaming implementation](../validation/iterative/native_oblique_streaming_calibration_result.md)
is calibrated, and the completed
[complete zero-gradient response](../validation/iterative/native_oblique_full_response_result.md)
recovers the original-coordinate operator and common-white fields across all
11,364 paths. Order-16 fixed/reclosed field differences stay below 1.03e-14;
eleven tests, six raw audits and 5,246 byte-identical replay files pass.
The [layered-source calibration](../validation/iterative/native_layered_transport_result.md)
now verifies actual vacuum entry and independent regional/axial sources on its
declared samples. A weak-leakage error required higher-precision geometric
intersections; order-32 independent response errors are below 1.19e-14.
Ten tests, 24 independent audits, 643 byte-identical replay files and
18 manufactured layer-local white cases pass. The
[physical-boundary experiment](../validation/iterative/native_oblique_physical_boundary_contract.md)
now has a [completed, sealed full-native result](../validation/iterative/native_layered_full_result.md).
All 2,191 scheduled jobs, 16,200 byte-identical replay files, 24 independent
audits and 288 full-field traces pass, including complete prior regression.
The fixed-source physical operator and 18 native geometric-white cases qualify
on the declared groups/grids: independent field error is below 1.68e-14 and
white physical balance defect below 2.66e-14. The separate stored-normalizer
closure retains a 1.56e-7 physical defect. This does not qualify coupled
eigenproblems, POD or production, or repair the failed native tabulated gate.
The native lift remains a tested extension choice, not an axial law uniquely
reconstructed from scalar data.

## 5. Fixed-point equation

Equations (3)–(9) define

\[
G:(a,\rho,L)\mapsto(a^+,\rho^+,L^+).
\tag{10}
\]

The coupled solution satisfies

\[
G(x)-x=0.
\tag{11}
\]

The initial nonlinear method is direct Picard substitution:

\[
x^{m+1}=G(x^m).
\tag{12}
\]

No relaxation factor appears. If direct Picard is later shown not to
converge, another nonlinear solver may be studied against the same raw map;
it must not alter equations (5)–(10).

## 6. Three separate defects

For $x^+=G(x)$, use

\[
R_\rho=|\rho^+-\rho|,
\tag{13}
\]

\[
R_L=
\frac{\|L^+-L\|_\infty}
{\max(\|L^+\|_\infty,\|L\|_\infty)},
\tag{14}
\]

with an exact all-zero leakage branch, and

\[
R_a^2=
\frac{\displaystyle
 \sum_{s,g}H_s\Delta a_{s,g}^TM_g\Delta a_{s,g}}
{\displaystyle
 \sum_{s,g}H_s(a_{s,g}^+)^TM_ga_{s,g}^+}.
\tag{15}
\]

The three defects are checked independently. They are not fitted, weighted
together, or used to rescale the state.

## 7. Numerical versus physical choices

Fixed physical/discretization inputs are geometry, materials, tracks,
snapshot set, POD basis, and rank. Updated physical state is $(a,\rho,L)$,
the radial solution, and the radial response.

Inner and outer tolerances define when the discrete equations and fixed point
are considered numerically resolved. An iteration cap is only a safety bound.
If a radial or axial inner solve reaches its cap without satisfying the
declared strict predicate, $G(x)$ has not been evaluated and the program
fails closed.

The generic map is illustrated by [SpotPicard.c2m](../data/SpotPicard.c2m).
The active D4 REAL64 path uses [SpotStepR64.c2m](../data/SpotStepR64.c2m)
and the [D4 axial deck](../validation/iterative/d4a_rank2_picard_axial.x2m),
selected through the [current quickstart](../validation/iterative/D4A_CORRECTED_QUICKSTART.md).
Equation (8a) corresponds to the projected matrices and P0 radial term in
[SPOT1P64.f90](../src/SPOT1P64.f90); equation (9) is implemented by
`SPOLE1D` in [SPOT_LEAKAGE.f90](../src/SPOT_LEAKAGE.f90).

The original leakage-current-density POD variant and this flux-space Galerkin
method are different formulations. The former's constraint-preserving SVD
theorem does not by itself establish the latter's full-space conservation or
physical accuracy. See the [validation plan](validation_plan.md) for the
comparisons required by the current formulation.
