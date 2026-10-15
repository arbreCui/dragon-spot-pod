# Same-operator conservative exchange and fixed-space POD comparison

Completed on 2026-09-28. Eight manufactured networks and forty reduced
eigenproblems now separate projection error from the earlier change in radial
closure. Full-coordinate spaces recover the explicit-exchange reference.
Including the constant radial test function preserves whole-domain neutron
balance at truncated rank, but consumes approximation capacity: a balanced
low-rank solution can still have a large flux error.

This is a candidate formulation study on the
[qualified conservative networks](coupled_reference_heterogeneous_result.md).
The production ratio response, D4 inputs, active runtime and coupled chain
were not changed. The results do not select a rank or quantify an error for D4.

## Operator and projection

Let W be the diagonal radial volume weights (proportional to area for the
equal-height cells used here). Radial exchange is defined by a graph
Laplacian K with symmetric nonnegative edge conductances:

\[
C=W^{-1}K,\qquad \boldsymbol 1^TWC=0.
\]

The full S2 vacuum/diamond-difference network is
A*y = rho*F*y, with rho=1/k and y the non-vacuum angular face unknowns.
A contains streaming, total loss, scattering and the conservative P0
radial transfer. F contains the same material fission production and spectrum
at every rank. There is one global weighted nu-fission normalization.

For group-dependent fixed radial bases B_g, P lifts modal angular face
unknowns into physical space. Q uses the same bases to test physical
cell/angle equations. Face ordering and equation ordering differ and are
handled separately. With the repeated cell/angle weights W_e, solve

\[
Q^T W_e A P\,a=\rho Q^T W_e F P\,a.
\]

This projection retains the full Gram/mass matrices. No identity-mass
substitution, altered transfer coefficient, positivity repair or balance
correction is used. Full coordinates, rotated full bases and nonorthogonal
full bases must represent the same physical eigenpair. Reduced nonorthogonal
coordinate changes are checked independently as well.

For the full physical residual R=A*y-rho*F*y, summing all weighted equations
gives absorption + axial boundary outflow - fission source, because internal
radial transfer cancels. If every B_g spans the constant radial vector, there
is a modal test vector eta satisfying Q*eta=1. Consequently,

\[
\boldsymbol 1^T W_e R=\eta^T Q^T W_e R=0.
\]

This is the discrete conservation argument. A small projected residual alone
does not imply that identity for an arbitrary POD test space. Conversely,
the identity says nothing by itself about local flux accuracy or positivity.

## Declared inputs and training data

Six cases reproduce the preceding two-region operators, materials, S2
quadrature and vacuum boundaries unchanged. Their independent earlier
references are recovered before the projection comparisons.

Two added cases have four radial regions, two axial cells and two energy
groups. Radial weights are (1, 2, 1.5, 1), with graph edges
(0,1,0.8), (1,2,0.6), (2,3,0.4), (0,2,0.15). Both use mu/h=2,
chi=(0.75,0.25), and nu-fission=(1,0.5)/(0.8,0.4)/(0,0)/(0,0)
by region. Group transfer factors are (1,0.7).

The uniform case has total=(2,2.5), self scattering=(0.5,0.75), downscatter
0.3 and upscatter 0.1 everywhere. The layered case has first-plane totals
(2,2.5)/(2.1,2.6)/(2.25,2.75)/(2.4,2.9), all increased by 0.25 in the
second plane. It retains self scattering, uses downscatter=0.3/0.4 and
upscatter=0.1/0.15 by plane, and multiplies second-plane exchange by 1.1.
The plan and output preserve every coefficient array and full operator matrix.

Training uses only radial fixed-source problems at the declared material
planes, with prescribed shared leakages 0.5, 1.5 and 3. Each fissile region
is excited separately by a source chi/w_region, with total source 1. Each
multigroup snapshot then receives one weighted nu-fission normalization.
There are 3 or 6 snapshots per two-region case and 12 per four-region case.
No axial reference eigenflux, reference k or observed error enters the basis
construction or rank selection.

Two nested families are fixed before each eigenproblem:

- **Plain POD:** leading modes from the weighted snapshot SVD.
- **Constant-enriched POD:** normalized constant first, then leading weighted
  SVD modes of snapshots after removing their constant component.

Both families use every rank from 1 to the number of radial regions, with
the same rank in each group. Comparing the families at equal rank therefore
exposes the approximation capacity used to represent conservation. These are
different fixed spaces of the same operator, not a change in physics between
the reduced and full runs.

## Results

All forty projected residual maxima are below 1.43e-15. All reported physical
scalar fields and non-vacuum angular fields are positive without clipping.
For all complete spaces and nonorthogonal full-coordinate controls, maximum
absolute k error is 3.89e-16 and maximum relative weighted scalar-flux error
is 1.91e-15. Thus the implementation passes full-coordinate recovery without
relying on exact orthonormality of stored basis matrices.

All twenty constant-enriched calculations conserve to a relative physical
balance defect below 1.51e-15. Plain truncated POD does not generally conserve;
even its very small projection residual cannot supply the missing global test
function. In the two-region cases its rank-one flux errors range from 0.613%
to 2.645%, while absolute relative balance defects range from 0.746% to 2.361%.

For the four-region **layered** case, k_reference=0.2415921778891399:

| Fixed space | Rank per group | Weighted scalar-flux error | Reactivity difference | Relative physical balance defect |
| --- | ---: | ---: | ---: | ---: |
| Plain POD | 1 | 9.33445% | -1322.95 pcm | +1.37030% |
| Plain POD | 2 | 0.274626% | -5.56869 pcm | +0.308249% |
| Plain POD | 3 | 0.0374051% | -0.0712637 pcm | +0.0211479% |
| Plain POD | 4 | Numerical precision | Numerical precision | Numerical precision |
| Constant-enriched POD | 1 | 90.5326% | -358851 pcm | Numerical precision |
| Constant-enriched POD | 2 | 68.4725% | -41662.1 pcm | Numerical precision |
| Constant-enriched POD | 3 | 0.0963440% | -1.10974 pcm | Numerical precision |
| Constant-enriched POD | 4 | Numerical precision | Numerical precision | Numerical precision |

Flux error is the W-weighted volume L2 difference after the same global
nu-fission normalization. Reactivity difference is
1e5*(1/k_reference - 1/k_reduced). Physical balance defect is
(absorption + axial vacuum outflow - fission source)/fission source.
"Numerical precision" denotes the maxima stated above, not exact arithmetic.

The uniform four-region case confirms the pattern. At rank 3, plain POD has
0.0630716% flux error and 0.0319101% balance defect; constant-enriched POD has
0.171643% flux error and balance at numerical precision. Full rank recovers
the same reference in both families. Errors decrease with rank in these
measured sequences; this is not a monotonic-convergence theorem for transport
eigenproblems or a rank recommendation for another geometry.

The large rank-1/2 errors of the enriched family are retained. Conservation
does not make those solutions accurate. Its rank-3 layered solution also has
a nonzero full local residual (maximum 1.49e-3), despite its vanishing global
balance and projected residual. These three quantities answer distinct questions.

## Consequence for the project

There is now a reproducible same-operator route for measuring projection
error in the network candidate, with exact full-space recovery and an explicit
discrete conservation condition. It avoids treating a diagonal response that
matches one anchor as the action of a nonlocal transport operator on every
possible field. It does not validate the production ratio closure by substitution.

The next useful step is to return to the native radial transport interface:
derive how a conservative nonlocal operator or response can be applied, and
check its action on independent perturbations on a small native mesh. Include
the actual radial boundary current in the balance; the zero-net-transfer
identity here assumes no exterior radial loss. One-anchor coefficient agreement
is insufficient. Preserve the fixed-source/scattering definitions and weighted
normalization while making that comparison.

Only after that native operator check should a candidate be connected to the
existing reduced axial implementation. A constant-enriched space is one
qualified network option, not an instruction to alter the live POD basis.
The D4 chain retains its current purpose and gates. This study makes no D4
accuracy, convergence or speedup claim.

## Reproduction and evidence

[The program](qualify_exchange_projection.py) and
[nine focused tests](test_exchange_projection.py) require Python and NumPy.
Tests cover prior-operator recovery, unequal-volume balance, snapshot source
and normalization, representation of the balance functional, full recovery,
nonorthogonal reduced-coordinate invariance, positivity and projected residuals,
separation of conservation/accuracy, and invalid-input rejection. No native
transport or shared build is invoked, and the fast runner gains no dependency.

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 validation/iterative/test_exchange_projection.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 validation/iterative/qualify_exchange_projection.py /tmp/spot-projection-new
```

The output directory must be new. The artifact
`validation/artifacts/exchange-pod-projection-20260928/` retains the predeclared
plan, all forty comparisons, snapshots, bases, full/reduced matrices, test and
replay receipts, source copies and file hashes. The 997 protected input/runtime/
source files and six preceding diagnostic manifests are checked unchanged.
