# SPOT-POD: constraint-preserving POD filtering for the SPOT transport eigenvalue problem

This repository contains the implementation, drivers, and supporting
documentation for a constraint-preserving Proper Orthogonal Decomposition
filtering of the leakage current density in the **Synthesis Proper
Orthogonal Decomposition (SPOT)** transport synthesis method (Hébert, 2025),
referred to here as **Variant III′** (a corrected revision of the original
Variant III; see *History* note in the Math section).

> *Naming note:* the in-tree Fortran source headers still carry the
> original development name "Synthesis Polytechnique Tracking"; the
> framework was later renamed by Hébert and the present author to
> "Synthesis Proper Orthogonal Decomposition." Use the current name
> in all prose and citations.

The SPOT framework itself (`SPOT.f`, `SPOT1P.f90`, `SPOF.f`, with the 1D
axial scattering-reduction direct solve in `SPOT1P.f90`) is by **A. Hébert**
(École Polytechnique de Montréal). The Variant III′ POD extension and
associated outer-iteration support patch are by the present author.

---

## Math

### Setting

For each energy group g ∈ {1, …, G}, snapshot index k ∈ {1, …, K},
and radial region i ∈ {1, …, N}:

$$
\varphi^{k}_{g,i} \;=\; \text{radial scalar flux at snapshot } k
$$

$$
L^{2D}_{g,i,k} \;=\; \text{radial leakage equivalent cross section}
$$

$$
L^{1D}_{g,k} \;=\; \text{axial leakage cross section of snapshot } k
$$

$$
V_{i} \;=\; \text{region volume}
$$

From the SPOASM assembly,

$$
L^{2D}_{g,i,k} \;=\; -\Sigma_{t,g,i} + \Sigma_{s0,g,i} - L^{1D}_{g,k}
  + Q^{k}_{g,i}/\varphi^{k}_{g,i},
$$

the converged 2D MOC snapshot balance gives

$$
\sum_{i=1}^{N} V_{i}\, L^{2D}_{g,i,k}\, \varphi^{k}_{g,i}
 \;=\; -\,L^{1D}_{g,k} \sum_{i=1}^{N} V_{i}\,\varphi^{k}_{g,i},
$$

which vanishes **only when** L¹ᴰ = 0, i.e. only at the first outer
iteration.

> *History.* The original Variant III applied the POD to
> **Y** = V·L²ᴰ·φ and asserted the zero-column-sum constraint for all
> snapshots and iterations. Measured residuals in `d3_sanity.log`
> falsify that premise beyond the first outer iteration: the
> per-column balance |1ᵀY[:,k]| is ~10⁻¹¹ at ASM call 1 (L¹ᴰ = 0) but
> jumps to ~10⁻⁴ at calls 2–3. Variant III′ therefore shifts the
> compressed variable so the constraint is structural rather than
> incidental.

Variant III′ defines the volume-weighted **pure-radial** leakage
current density

$$
y'_{g,i,k} \;:=\; V_{i}\,\bigl(L^{2D}_{g,i,k} + L^{1D}_{g,k}\bigr)\,
  \varphi^{k}_{g,i} ,
$$

whose column sums equal the pure 2D radial balance of the converged
snapshots and stay at the assembly-rounding level (single-precision
DB2 assembly plus the 2D MOC convergence residual) at **every** outer
iteration, instead of growing with L¹ᴰ:

$$
\bigl[\mathbf{Y}'_{g}\bigr]_{i,k} \;=\; y'_{g,i,k}, \qquad
\mathbf{1}^{\top}\mathbf{Y}'_{g}[\,:\,,k] \;=\; 0 \;\;\forall\,k.
$$

### Lemma (zero-column-sum SVD)

Let

$$
\mathbf{Y} \in \mathbb{R}^{N \times K}, \qquad
\mathbf{1}^{\top}\mathbf{Y} \;=\; \mathbf{0}^{\top}
\quad(\text{every column sums to zero})
$$

and let its thin SVD be

$$
\mathbf{Y} \;=\; \sum_{\alpha} \sigma_{\alpha}\, \mathbf{u}_{\alpha}\, \mathbf{v}_{\alpha}^{\top} .
$$

Then for every index α with non-zero singular value,

$$
\sigma_{\alpha} \neq 0 \;\Longrightarrow\; \mathbf{1}^{\top}\mathbf{u}_{\alpha} = 0 .
$$

**Proof.** For any fixed k,

$$
0 \;=\; \mathbf{1}^{\top}\mathbf{Y}[\,:\,,k]
\;=\; \sum_{\alpha} \sigma_{\alpha}\,(\mathbf{1}^{\top}\mathbf{u}_{\alpha})\, v_{\alpha}(k) .
$$

Define

$$
c_{\alpha} \;:=\; \sigma_{\alpha}\,(\mathbf{1}^{\top}\mathbf{u}_{\alpha}).
$$

The above gives

$$
\sum_{\alpha} c_{\alpha}\, \mathbf{v}_{\alpha} \;=\; \mathbf{0}
\quad \text{in } \mathbb{R}^{K}.
$$

The right singular vectors with non-zero singular values are
orthonormal in ℝᴷ, hence linearly independent, so cα = 0 for all
such α. Therefore σα ≠ 0 implies 1ᵀuα = 0. ∎

> *Remark.* This is an elementary column-space property of the SVD
> (1 ⊥ col(**Y**) and the uα with σα ≠ 0 form an orthonormal basis of
> col(**Y**); cf. Golub & Van Loan, §2.4), isomorphic to the familiar
> fact that PCA on mean-centred data yields mean-free components. It
> is stated and proved here for completeness, not claimed as new.

### Proposition (constraint-preserving POD filtering)

Let **Y**′g be defined as above with thin SVD
**Y**′g = Σα σα uα vαᵀ, let fα ∈ [0, 1] be arbitrary filter factors,
and let

$$
\widetilde{\mathbf{Y}}'_{g} \;=\;
\sum_{\alpha} f_{\alpha}\, \sigma_{\alpha}\, \mathbf{u}_{\alpha}\, \mathbf{v}_{\alpha}^{\top}
$$

be the filtered reconstruction. Define the recovered leakage by
reverse division and back-shift,

$$
\widetilde{L}^{2D}_{g,i,k} \;:=\;
\frac{\widetilde{y}'_{g,i,k}}{V_{i}\, \varphi^{k}_{g,i}} \;-\; L^{1D}_{g,k}
\qquad (\varphi^{k}_{g,i} > 0).
$$

Then the SPOT fundamental-mode constraint on the pure-radial balance
is exactly preserved at every k for **any** choice of filter factors
(hard rank-r truncation fα ∈ {0, 1} included):

$$
\sum_{i=1}^{N} V_{i}\,\bigl(\widetilde{L}^{2D}_{g,i,k} + L^{1D}_{g,k}\bigr)\,
\varphi^{k}_{g,i} \;=\; 0 .
$$

**Proof.** Substituting the definition of ỹ′,

$$
\sum_{i} V_{i}\,\bigl(\widetilde{L}^{2D}_{g,i,k} + L^{1D}_{g,k}\bigr)\, \varphi^{k}_{g,i}
\;=\; \mathbf{1}^{\top}\widetilde{\mathbf{Y}}'_{g}[\,:\,,k]
\;=\; \sum_{\alpha} f_{\alpha}\,\sigma_{\alpha}\,(\mathbf{1}^{\top}\mathbf{u}_{\alpha})\, v_{\alpha}(k).
$$

By the Lemma, every term with non-zero σα satisfies 1ᵀuα = 0, so the
sum vanishes term by term. ∎

### Choice of filter factors

The implementation (`SPOPOD.f90`) uses Tikhonov filter factors

$$
f_{\alpha} \;=\; \frac{\sigma_{\alpha}^{2}}
{\sigma_{\alpha}^{2} + (\varepsilon\,\sigma_{1})^{2}},
$$

with f = ½ exactly at the former hard cutoff σα = ε σ₁, plus an
optional hard cap fα = 0 for α > `rank_max`. Two remarks:

- Hard truncation (fα ∈ {0, 1}) is Frobenius-optimal at fixed rank
  (Eckart–Young, 1936), but the map **Y**′ → Ỹ′ is then discontinuous
  in the data: a 1-ulp perturbation of the spectrum near the cutoff
  flips an entire rank. This was observed as a ~0.7 pcm Δρ shift under
  `-O3` FMA/SIMD reordering (see Build notes). The Tikhonov filter
  makes the map Lipschitz in the data and removes that sensitivity,
  at the price of a slightly sub-optimal (but monotone and smooth)
  spectral attenuation.
- The S1 low-flux opt-out (cells with φ below the floor keep their
  original, unfiltered L²ᴰ) makes the written-back matrix a hybrid;
  the post-filter constraint residual is therefore **measured**
  (`POD-ERR-POST`), not asserted. It is machine-precision whenever no
  cell hits the floor.

---

## Repository layout

```
src/                       Dragon main source (full vendor of upstream
                            `Version5_spot_ev3809/Dragon/src/`).
                            SPOT-specific files modified or authored
                            as part of this work:
  SPOT.f                   Hébert + Cui (KEYFLX$ANIS index fix,
                            EPSI -> SVDEPS write fix; see commit log)
  SPOT1P.f90               Hébert + Cui (1D axial SN with scattering
                            reduction; defensive guard on singular
                            per-region systems, 2026-07)
  SPOF.f                   Hébert
  SPOASM.f                 Hébert + Cui POD entry points
  SPODB2.f                 Hébert + Cui IPSNAP patch + FLU2 div-zero guard
  SPOPOD.f90               Cui — POD on Y'_{i,k} = V_i (L^{2D}_{i,k} +
                            L^{1D}_k) φ^k_i with Tikhonov filtering
data/                      CLE-2000 driver procedures + Dragon multi-compo
  SpotPodEps.c2m           stage-1 POD wrapper (no outer iter)
  SpotPodItr.c2m           outer-iter POD wrapper (Variant III′)
  SpotPodMic.c2m           legacy stage-1 wrapper (kept for D2/D3 baselines)
  Snap1Ring.c2m            1-ring snapshot factory
  SnapMring.c2m            multi-ring snapshot factory
  SpotSnapBld.c2m          pincell snapshot factory
  rnr_0burn_spot_proc/     prepared multi-compo (rnr_cc, rnr_interpol,
                            irena_pincell.dat / irena_assembly_tiso_*.dat)
runs/                      experiment drivers and run scripts
Trivac/                    Hébert finite-element diffusion solver library
Utilib/                    Hébert utility library
Ganlib/                    Hébert generic asset network library (LCM)
Makefile                   top-level Dragon build entry
README.md                  this file
```

The repository is a complete buildable working tree of the
`Version5_spot_ev3809` Dragon distribution with the SPOT-POD
extension applied. All upstream Hébert files are present at their
expected paths; SPOT-POD modifications are concentrated in the
files annotated `Cui` above.

---

## Build & run (macOS, Apple Silicon)

Compiler flags (already set in each Makefile under `Trivac/src`,
`Utilib/src`, `Ganlib/src`, `src`):

```
opt = -O2 -march=native -ffp-contract=off -g
```

`-O3 -march=native` used to perturb POD K by ~0.7 pcm Δρ via FMA / SIMD
reordering across the former hard rank-cutoff; the Tikhonov filter
factors (see Math) remove that mechanism. `-O2 -ffp-contract=off`
remains the recommended science-run setting for bit-reproducibility.

```sh
# Build the three libraries first, then Dragon (dependency order):
(cd Utilib/src && make -j8)
(cd Ganlib/src && make -j8)
(cd Trivac/src && make -j8)
(cd src        && make -j8)

# macOS Gatekeeper requires re-signing after every rebuild:
codesign --force --deep --sign - bin/Darwin_arm64/Dragon
```

Run scripts under `runs/<case>/run_*.sh` expect `$DRAGON_ROOT` to
be the repository root and link the relevant `data/` procedures
into the case directory before launching Dragon.

### Notes on the outer iteration

The SPOT outer iteration in CLE-2000 requires two implementation
details that may be non-obvious:

1. `SALT/MCCGT` (MOC) tracks invalidate `IFTRAK` after `BACKUP/RECOVER`,
   so the original `LK1D` path through `DOORAV → MCCGA` is unreachable
   on a recovered track. `SpotPodItr.c2m` therefore drives the LK2D
   path through `CDOOR='SPOT'`, which avoids `MCCGA`.
2. CLE-2000 forces `DELETE` of the flux LCM each outer iteration, which
   would wipe the under-relaxation history for `SPOT-LEAK1D`. The
   `SPODB2.f` patch in this repository reads the previous
   `SPOT-LEAK1D` from `IPSNAP` (the snapshot archive, which persists
   across outer iterations) instead of from `IPFLUX`.

---

## Provenance

This work derives from the Dragon **`Version5_spot_ev3809`** branch
(Hébert et al., École Polytechnique de Montréal). Files in `src/`
that retain Hébert's authorship line are the upstream `ev3809` versions
or their direct descendants; the SPOPOD module, the SPOASM POD entry
points, the SPODB2 `IPSNAP` outer-iteration patch, and all `data/`
and `runs/` content are added or modified as part of this work.

This repository is part of the author's PhD at École Polytechnique de
Montréal.

---

## License

GNU Lesser General Public License, version 2.1 or later (LGPL-2.1-or-later),
inherited from the upstream Dragon framework. Full license text in
[`LICENSE`](LICENSE).

The Hébert source files (`SPOT.f`, `SPOT1P.f90`, `SPOF.f`, original
portions of `SPOASM.f` and `SPODB2.f`, plus the upstream Dragon
sources under `src/`, `Trivac/`, `Utilib/`, `Ganlib/`) are
Copyright © École Polytechnique de Montréal under LGPL-2.1-or-later
(see header notices in individual files). The Variant III/III′ contributions
(`SPOPOD.f90`, the `SPOASM` POD entry points, the `SPODB2` `IPSNAP`
patch, and content under `data/Spot*.c2m`, `data/Snap*.c2m`,
`runs/`) are Copyright © 2026 Bowen Cui, also under
LGPL-2.1-or-later.
