# SPOT-POD: constraint-preserving rank-r POD compression for the SPOT transport eigenvalue problem

This repository contains the implementation, drivers, and supporting
documentation for a constraint-preserving Proper Orthogonal Decomposition
compression of the leakage current density in the **Synthesis Proper
Orthogonal Decomposition (SPOT)** transport synthesis method (Hébert, 2025),
referred to here as **Variant III**.

> *Naming note:* the in-tree Fortran source headers still carry the
> original development name "Synthesis Polytechnique Tracking"; the
> framework was later renamed by Hébert and the present author to
> "Synthesis Proper Orthogonal Decomposition." Use the current name
> in all prose and citations.

The SPOT framework itself (`SPOT.f`, `SPOT1P.f90`, `SPOF.f`, with the 1D
axial scattering-reduction direct solve in `SPOT1P.f90`) is by **A. Hébert**
(École Polytechnique de Montréal). The Variant III POD extension and
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
V_{i} \;=\; \text{region volume}
$$

The SPOT fundamental-mode constraint (volume-weighted zero-sum) reads

$$
\sum_{i=1}^{N} V_{i}\, L^{2D}_{g,i,k}\, \varphi^{k}_{g,i} \;=\; 0
\qquad \forall\, g,\, k .
$$

Variant III defines the volume-weighted leakage current density

$$
y_{g,i,k} \;:=\; V_{i}\, L^{2D}_{g,i,k}\, \varphi^{k}_{g,i} ,
$$

so the constraint becomes a column-sum-zero condition on the matrix
$$
\bigl[\mathbf{Y}_{g}\bigr]_{i,k} \;=\; y_{g,i,k}, \qquad
\mathbf{1}^{\top}\mathbf{Y}_{g}[\,:\,,k] \;=\; 0 \;\;\forall\,k.
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

### Theorem 1 (constraint-preserving rank-r POD truncation)

Let **Y**g be defined as above and let

$$
\widetilde{\mathbf{Y}}_{g} \;=\;
\sum_{\alpha=1}^{r_{g}} \sigma_{\alpha}\, \mathbf{u}_{\alpha}\, \mathbf{v}_{\alpha}^{\top}
$$

be its rank-rg SVD truncation, with rg ≤ rank(**Y**g). Define the
reconstructed leakage by reverse division,

$$
\widetilde{L}^{2D}_{g,i,k} \;:=\; \frac{\widetilde{y}_{g,i,k}}{V_{i}\, \varphi^{k}_{g,i}}
\qquad (\varphi^{k}_{g,i} > 0).
$$

Then the SPOT fundamental-mode constraint is exactly preserved at
every k and any rank rg:

$$
\sum_{i=1}^{N} V_{i}\, \widetilde{L}^{2D}_{g,i,k}\, \varphi^{k}_{g,i} \;=\; 0 .
$$

Furthermore, the truncation is Frobenius-optimal among all rank-rg
matrices (Eckart–Young, 1936):

$$
\bigl\lVert \mathbf{Y}_{g} - \widetilde{\mathbf{Y}}_{g} \bigr\rVert_{F}^{2}
\;=\; \sum_{\alpha > r_{g}} \sigma_{\alpha}^{2}.
$$

**Proof.** Substituting the definition of ỹ,

$$
\sum_{i} V_{i}\, \widetilde{L}^{2D}_{g,i,k}\, \varphi^{k}_{g,i}
\;=\; \sum_{i} \widetilde{y}_{g,i,k}
\;=\; \mathbf{1}^{\top}\widetilde{\mathbf{Y}}_{g}[\,:\,,k]
\;=\; \sum_{\alpha=1}^{r_{g}} \sigma_{\alpha}\,(\mathbf{1}^{\top}\mathbf{u}_{\alpha})\, v_{\alpha}(k).
$$

By the Lemma, every term with non-zero σα satisfies 1ᵀuα = 0, so
the sum vanishes. The Frobenius optimality is the standard
Eckart–Young theorem for SVD truncation. ∎

---

## Repository layout

```
src/                       Dragon main source (full vendor of upstream
                            `Version5_spot_ev3809/Dragon/src/`).
                            SPOT-specific files modified or authored
                            as part of this work:
  SPOT.f                   Hébert + Cui (KEYFLX$ANIS index fix,
                            EPSI -> SVDEPS write fix; see commit log)
  SPOT1P.f90               Hébert, 1D axial SN with scattering reduction
  SPOF.f                   Hébert
  SPOASM.f                 Hébert + Cui POD entry points
  SPODB2.f                 Hébert + Cui IPSNAP patch + FLU2 div-zero guard
  SPOPOD.f90               Cui — POD on Y_{i,k} = V_i L^{2D}_{i,k} φ^k_i
data/                      CLE-2000 driver procedures + Dragon multi-compo
  SpotPodEps.c2m           stage-1 POD wrapper (no outer iter)
  SpotPodItr.c2m           outer-iter POD wrapper (Variant III)
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

`-O3 -march=native` perturbs POD K by ~0.7 pcm Δρ via FMA / SIMD
reordering across the rank-cutoff in `ALSVDF`; use `-O2 -ffp-contract=off`
for science runs.

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
(see header notices in individual files). The Variant III contributions
(`SPOPOD.f90`, the `SPOASM` POD entry points, the `SPODB2` `IPSNAP`
patch, and content under `data/Spot*.c2m`, `data/Snap*.c2m`,
`runs/`) are Copyright © 2026 Bowen Cui, also under
LGPL-2.1-or-later.
