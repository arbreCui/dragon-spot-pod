# SPOT validation plan

Validation follows the dependencies of the method. A later benchmark cannot
repair an incorrect source, state, map, or unconverged inner solve.

## 1. Algebra and interface gate

Without transport execution, verify:

- volume-weighted POD construction, reconstruction and rank behavior;
- $p=Ba$ and the stored Gram metric;
- frozen fission source $\mathcal F(Ba)/k$;
- final off-group scattering with no second fission evaluation;
- radial-response and leakage signs;
- canonical state $x=(a,1/k,L)$;
- separate $(R_\rho,R_L,R_a)$ defects;
- direct substitution and the three-component AND stopping rule;
- fail-closed radial and axial inner iteration caps.

Status: PASS. Run with `make spot-fast`.

## 2. One real map

For one frozen input, evaluate $x^+=G(x)$. Require:

- strict radial and axial inner terminals;
- finite positive physical flux;
- radial source identity and balance;
- unchanged POD basis and rank;
- independently recomputed defects;
- consistent restart leakage ordering.

Status: PASS for the accepted real-map records through the final x8. The x8
classification is `VALID_NOT_MET`; its independent checker and publication
receipt both pass.

## 3. Fixed-point iteration

Run direct updates

$$
x_{m+1}=G(x_m)
$$

without relaxation or parameter changes. At every step report all three
defects. If any inner solve fails its strict terminal, $G(x_m)$ was not
evaluated and the run fails closed. If all three outer defects do not pass,
the last state is not a converged solution.

Status: DIRECT CENSUS COMPLETE, NOT CONVERGED through x8. The final result is

$$
(R_\rho,R_L,R_a)=
(6.4057635\times10^{-8},\,
3.7849612\times10^{-4},\,
2.6731298\times10^{-7})
$$

at an outer tolerance of $5\times10^{-7}$.

A single real leakage-Anderson candidate worsened the leakage and modal
defects relative to direct $x_6$; that rank-1 candidate is rejected. It does
not reject Anderson methods in general.

Next: stop direct Picard. The predeclared x8 endpoint was evaluated once and
no x9 is defined. The no-transport x6--x8 direction audit is complete: the
latest leakage residuals are nearly opposite in a separately labelled
height-$L_2$ diagnostic, and their unique production infinity hotspot stays
at plane 3/group 325 while reversing sign and growing. This motivates but
does not select a solver or prove a cycle. Any nonlinear-solver study must be
declared separately for the same $F(x)=G(x)-x$ and may not alter the physical
map.

The separately declared rank-2 sensitivity route has since produced two
valid maps. The second map reduced all three defects but remains
`VALID_NOT_MET`. Its full modal updates are strongly opposed and shrink only
to `0.864118`, while the leakage update shrinks to `0.024606`. These are
local two-update diagnostics, not convergence factors or cycle evidence, and
no third direct rank-2 map is defined.

The selected next study is therefore one offline modal-projected Anderson(1)
proposal in the full Gram-height metric. The unique minimizer of that stated
scalar least-squares problem gives latest-state weight
`0.5388643265136009`. The same scalar would
act on the complete state, but no mixed-unit whole-state norm is formed and
no empirical relaxation factor is prescribed. The publication-aware proposal
has now been materialized deterministically. Its independent Ganlib-only
audit passes the fixed-basis, binary publication, x2 carrier and 8880-point
strict-positivity checks. That publication stage remains correctly classified
`MATERIALIZED_PROPOSAL_NOT_EVALUATED`; it did not itself evaluate `G_2(y)`.
See
[../validation/iterative/rank2_solver_decision.md](../validation/iterative/rank2_solver_decision.md)
and
[../validation/iterative/rank2_modal_aa1_candidate_result.md](../validation/iterative/rank2_modal_aa1_candidate_result.md).

The proposal has now been followed by one separately authorized fresh strict
evaluation $z=G_2(y_{\rm pub})$. The physical chain and all independent
validity checks pass, but the result is `VALID_NOT_MET`:

\[
(R_\rho,R_L,R_a)=
(6.5763515\times10^{-5},\,2.2656585\times10^{-3},\,
4.6646819\times10^{-4}),
\]

so every stopping component remains above $5\times10^{-7}$. Each is smaller
than in the direct second rank-2 map for this one frozen comparison. That is
useful local response evidence, not an asymptotic factor, solver ranking,
rank qualification or physical-accuracy result. The run had no retry and
defines no next map. See
[../validation/iterative/rank2_modal_aa1_map_result.md](../validation/iterative/rank2_modal_aa1_map_result.md).

The next depth-one history update has now been checked offline using the two
actual evaluated pairs $x_1\to x_2$ and $y_{\rm pub}\to z$. The unique
full-Gram modal coefficient gives weight `0.9302745506696768` to $z$, and the
possible next raw affine state formula is
$(1-\beta_z)x_2+\beta_z z$. Its canonical publication preflight is finite and
all 8880 reconstructed points remain strictly positive. The proposal has now
been deterministically materialized and independently verified with the
audited `z` raw-flux/snapshot carrier. It is
`MATERIALIZED_PROPOSAL_NOT_EVALUATED`: no fresh map or stopping defect has
been generated. See
[../validation/iterative/rank2_modal_aa1_next_history_result.md](../validation/iterative/rank2_modal_aa1_next_history_result.md)
and
[../validation/iterative/rank2_modal_aa1_next_candidate_result.md](../validation/iterative/rank2_modal_aa1_next_candidate_result.md).

The separately authorized single map from that `Z-RAW-FLUX` proposal has now
completed without retry. The decks, rank, tolerance and physics remained
unchanged; the carrier preflight, strict terminals, independent audit and
receipt pass. Its classification is `VALID_NOT_MET`, with
\((R_\rho,R_L,R_a)=(8.34905\times10^{-7},8.67273\times10^{-4},
4.44166\times10^{-5})\). No subsequent map was started; see
[../validation/iterative/rank2_modal_aa1_next_map_result.md](../validation/iterative/rank2_modal_aa1_next_map_result.md).

The solver-independent proposal and acceptance contract is now frozen and
passes exact-arithmetic manufactured tests. A full exact-Newton step is used
only as a parameter-free algebraic reference. Real SPOT has no validated
exact Jacobian, so no Newton/JFNK production path or new transport run is
authorized by this result.

A no-transport finite-difference entry probe also passes. It shows that the
same linear manufactured direction can be hidden or distorted by binary32
state publication. This is a local counterexample to assuming a smooth
binary64 $Jv$, not a proof that JFNK is impossible; Krylov implementation
remains out of scope.

## 4. Numerical qualification

Only after a reproducible fixed point exists, vary one choice at a time:

1. POD rank;
2. radial and axial meshes;
3. angular quadrature;
4. energy groups;
5. inner solver tolerances.

Rank is accepted only when the self-consistent state and declared observables
are stable under rank increase. It is never calibrated to a desired answer.

Prequalification diagnostic: the frozen three-snapshot spectra have been
read without transport. The worst optimal within-group reconstruction error
is 1.5004% at rank 1 and 0.03408% at rank 2; all groups have numerical rank
3. This does not qualify rank 2 or identify the cause of Picard failure. It
only establishes that a later rank-increase study is scientifically
motivated.

## 5. Reference validation

Compare the numerically qualified SPOT fixed point with an independent
higher-fidelity transport reference using predeclared observables such as
eigenvalue, plane power, axial shape and reaction rates. Keep equation and
iteration errors separate from model-to-reference differences.

The concise current evidence is
[../validation/iterative/current_result.md](../validation/iterative/current_result.md).
Historical diagnostics are preserved at Git tag
`archive-pre-lean-20260814`.
