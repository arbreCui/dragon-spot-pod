# Native 370-group fixed-source and same-operator POD qualification

Completed on 2026-09-28. The historical eight-region pin now has four positive
full-space fixed-source references using **all 370 energy groups**, the native
MOC collision response, the saved scattering data and the saved white boundary.
Fresh native source construction and sweep reproduce these references. Both
POD families recover the full solution at rank 8.

This is a qualification of the **raw, pre-rebalance fixed-source equations**,
not a D4 result, a fission eigenproblem, or a coupled radial/axial reference.
It does not reproduce a `FLU2DR64` terminal after `FLUBAL64` rebalance.
The shared runtime, current maps and protected inputs remain unchanged.

## Source and leakage audit

The same TRACK, SYSTEM and rays as the
[native flight-response study](native_radial_response_result.md) are used.
The historical `restart_macro0.xsm` and `restart_source.xsm` supply the
off-group scattering and frozen external source. All five hashes match the
earlier raw-MOC capture protocol. MACRO0 has 32 fission components, all zero;
the prescribed source is fixed throughout, with no fission iteration.

For all 8 × 370 material/group pairs, the saved data satisfy exactly

\[
S_{gg}^{used}=\mathrm{float32}(S_{gg}^{physical}-L_g^{saved}).
\]

`SPOT-L1-RAW` is absent. This is the legacy embedded-leakage route in
[ASMDRV.f](../../src/ASMDRV.f), so the saved leakage must **not** be subtracted
a second time. The saved L ranges from 1.3411624e-4 to 1.1052049e-3 cm^-1.
The effective subtraction `float64(physical)-float64(used)` differs from the
saved L by as much as 1.4836260e-6 cm^-1 because the original subtraction was
binary32. The study preserves the actual used coefficient and that rounding.

The native total and self-scattering coefficients also include transport
corrections: their differences from the raw MACRO0 records reach 0.33102113
cm^-1. Consequently, the diagonal of packed `SCAT00` is not substituted for
`SYSTEM/DRAGON-S0XSC`. Off-group entries retain the native destination/source
orientation and all signs. There are 8,753 negative off-group entries and
701 negative used-self entries. None is clipped, rescaled or repaired.
Total minus the scatter column sum is described as operator net removal,
not independently established physical absorption.

A separate read-only export verifies the correction directly: all saved totals
equal `float32(NTOT0 - TRANC)` and all saved physical self coefficients equal
`float32(SIGW00 - TRANC)` bit for bit. Thus the macro/SYSTEM differences are
reconciled using the actual stored correction, not inferred from their size.

The read-only host independently evaluates `SPOQFSD` followed by `MCGFCS64`.
Their source arrays agree with the matrix construction within 5.26e-16.
Checks cover positive and signed analytic fields plus all four solved states.
The initial checker incorrectly assumed one fission component and rejected
the fixture before exporting data. That schema assumption was corrected to
read the actual count; both rejected audit logs are retained. No transport
result or input coefficient was adjusted in response.

## Full fixed-source operator

Fourteen coordinate flights are extracted for every group: 5,180 native sweeps.
The earlier matrices for groups 1, 185 and 370 are recovered bit for bit.
The scalar response R_g includes the saved white boundary return, as derived
in the preceding study. Define H_g=R_g^-1. The full scalar system is

\[
A(\lambda)\phi=q,\qquad
A(\lambda)=\operatorname{blockdiag}(H_g)-S^{used}+\lambda I.
\]

Off-group S comes from MACRO0 `SCAT00`; self-scattering comes from SYSTEM
`DRAGON-S0XSC`. The extra prescribed leakage lambda is distinct from the
saved leakage already embedded in S. No energy-group truncation, condensation,
scattering renormalization or fitted radial transfer is used.
The native route is isotropic with transport-corrected P0 coefficients; retaining
all energy groups does not introduce higher scattering moments.

Four held-out references combine lambda=0 and 0.05 cm^-1 with two sources:

- The archived frozen source, normalized to unit volume-integrated source.
- A positive regional ramp 1..8 times exp(-(g-1)/53), with the same single
  global source normalization.

The 2,960-unknown linear systems are solved directly. From each scalar field,
the eliminated outgoing boundary field is reconstructed. The native routines
then rebuild the full scattering/leakage/boundary source and sweep it again.
Together with the two analytic fields, this adds 2,220 independent native
flights. No ACA or global rebalance is applied.

| Qualification check | Measured maximum |
| --- | ---: |
| Full linear residual / prescribed source | 8.780e-13 |
| Source construction vs native callbacks | 5.257e-16 |
| Full scalar solution vs fresh native sweep | 4.382e-15 |
| Same comparison, worst separately normalized energy group | 2.918e-14 |
| Full-rank POD scalar-flux difference | 9.066e-15 |
| Nonorthogonal coordinate-change difference | 2.190e-14 |
| Projected residual across 64 reduced cases | 8.242e-13 |

All four full references have strictly positive regional scalar flux; the
minimum is 4.3915e-13. The maximum radial-response condition number is 1818.30.
These checks establish the meaning and numerical reproducibility of this
finite fixed-source operator. They do not establish a coupled eigenproblem's
positivity, uniqueness, or physical accuracy.

## Fixed POD spaces and held-out comparison

Training uses lambda=0.01, 0.1 and 1 cm^-1, exciting each of the eight regions
separately. Each source has unit volume integral and the energy spectrum of
the volume-integrated archived external source. These 24 multigroup solutions
are each normalized once by their full volume-weighted L2 norm. No groupwise
normalization or held-out reference flux enters the training. All training
fields are positive.

Each group has one radial basis fixed across the four tests. Plain POD uses
the weighted snapshot SVD. Constant-enriched POD reserves its first mode for
the constant radial vector, then uses the weighted SVD after removing that
component, with orthogonalization. Both families retain ranks 1 through 8.

For the groupwise lifting matrix B, every reduced solve uses exactly

\[
B^TWA(\lambda)Ba=B^TWq.
\]

All Gram matrices are retained, including the leakage term. Independent
nonorthogonal coordinate changes at ranks 3 and 8 preserve the physical field.
The reduced/full comparison therefore measures projection of the same native
operator, not a simultaneous change of closure.

The table gives the worst volume-weighted relative flux error over the four
held-out configurations at each rank. These are descriptive results, not rank
selection criteria for D4.

| Radial rank per group | Plain POD error | Constant-enriched error | Enriched cases with negative flux |
| ---: | ---: | ---: | ---: |
| 1 | 14.9070% | 0.80810% | 0 / 4 |
| 2 | 14.8416% | 0.71438% | 4 / 4 |
| 3 | 9.93535% | 0.35069% | 0 / 4 |
| 4 | 0.23856% | 0.09811% | 0 / 4 |
| 5 | 0.07378% | 0.05833% | 0 / 4 |
| 6 | 0.06596% | 0.03051% | 0 / 4 |
| 7 | 0.00755% | 0.01159% | 0 / 4 |
| 8 | < 1e-12% | < 1e-12% | 0 / 4 |

All 32 plain-POD solutions are positive. Constant-enriched rank 2 has
19/9/9/9 negative entries in the four configurations, all in region 8; the
minimum is -1.90793e-5. These are retained signed. Global flux error below
1% and a small projected residual do not establish local positivity.
The observed improvement at rank 3 does not authorize a production rank change.

## Equation conservation versus the native current defect

The original white boundary has zero net radial boundary current. Let
C_g=H_g-diag(total_g). For any lifted scalar field, define

\[
r=A\phi-q,\quad
\delta_C=\sum_g\mathbf1^TWC_g\phi_g,\quad
b=\sum_g\mathbf1^TW[\Sigma_{t,g}\phi_g-(S^{used}\phi)_g
                     +\lambda\phi_g-q_g].
\]

Then `b = sum(W*r) - delta_C`. The recorded identity agrees within 4.45e-16.
The current-based collision/scattering/leakage ledger b is distinct from an
independently audited capture/fission reaction balance.

The constant-enriched spaces keep `sum(W*r)` below 1.08e-14, as expected from
their test space. They **do not erase** the native raw-flight defect delta_C.
Their largest absolute ledger defect is 4.043e-6 of the unit external source;
the full references reach 4.030e-6. Multiple scattering can amplify the
collision-flight defect relative to the external source.

Plain POD does not generally contain the constant test vector. Its rank-1
weighted equation imbalance reaches 0.149626 of the external source and
decreases with enrichment in this experiment. Its full rank recovers the
native reference and the same small retained raw-flight defect.

Thus three properties remain separate: projected equation residual, raw
native current balance, and positivity/local flux accuracy. Exact conservation
of the manufactured graph networks is not silently imposed on native MOC.

## Reproducibility and remaining work

Eleven standalone NumPy tests pass. They include an independent explicit global
projection oracle, asymmetric group-transfer orientation, unequal weights,
nonorthogonal Gram handling, conservation with an intentionally imperfect
radial operator, and saved native/full-space evidence. These tests are not
added to the shared fast runner.

All analysis is replayed from archived sources. The audit, references,
projection results, final report data and source-field input are byte-identical;
all saved numeric arrays are exactly equal. The final native audit/source
host also replays its binary outputs byte for byte. The archived replay
explicitly sets the Accelerate, OpenBLAS and OpenMP thread limits to one.
All 997 protected files and all 303 entries of the eight preceding artifact
manifests remain unchanged.

The subsequent [coupled eigenreference study](native_axial_coupling_result.md)
has now completed this milestone on three declared small meshes, with 48 POD
comparisons and retained angular-positivity failures. Its scope and remaining
axial-refinement work are stated separately.

The candidate specified at the end of this fixed-source study was a small radial/axial model retaining this native
nonlocal action, full multigroup scattering and explicit current accounting.
First qualify its full-coordinate coupled eigenproblem, normalization and
positivity; then project that same operator into fixed POD spaces. Keep
the low-rank signed-flux counterexample as an admission test. This study alone
does not justify inserting C, a new basis, or another rank into the running
D4 chain, nor does it establish D4 error relative to a 3D reference.

Files: [native audit/source host](probe_native_multigroup.f90),
[analysis](qualify_native_multigroup_pod.py),
[tests](test_native_multigroup_pod.py),
[predeclared plan](../artifacts/native-multigroup-pod-20260928/plan.json),
[full result](../artifacts/native-multigroup-pod-20260928/analysis/result.json).
