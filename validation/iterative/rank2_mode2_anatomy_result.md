# Rank-2 mode-2 anatomy

## Scope

This is a read-only decomposition of the valid but tolerance-not-met rank-2
map reported in
[rank2_axial_only_result.md](rank2_axial_only_result.md). It starts no Dragon
process, evaluates no radial or axial equation, advances no Picard state and
introduces no fitted, relaxation or empirical parameter.

For group $g$ and axial snapshot $s$, let
$\Delta a_{gs}=a^{\mathrm{current}}_{gs}-a^{\mathrm{parent}}_{gs}$.
The production coordinate defect is replayed exactly as

$$
R_a^2=\frac{N}{D},\qquad
N=\sum_{g,s}h_s\,\Delta a_{gs}^{T}G_g\Delta a_{gs},\qquad
D=\sum_{g,s}h_s\,a_{gs}^{T}G_ga_{gs}.
$$

For rank two, the checker only partitions this stored quadratic form:

$$
N=N_1+N_2+N_{12},
$$

where $N_1$ and $N_2$ are the two diagonal Gram terms and $N_{12}$ is the
sum of both signed off-diagonal terms. This is an algebraic identity, not a
new closure model.

## Independent checks

The Ganlib-only checker passed all of the following before reporting the
partition:

- rank-1 raw parent $\rho$, normalization, heights and leakage equal the
  rank-2 raw parent bit for bit;
- the rank-2 mode-1 basis, training coefficients and singular-value package
  reproduce the rank-1 prefix bit for bit;
- every rank-2 Gram entry recomputed from the stored volumes and basis equals
  the canonical state bit for bit;
- the production-order $R_a$ replay equals the stored defect bit for bit;
- $N_1+N_2+N_{12}$ closes to $N$ within a bound derived from binary64 machine
  epsilon. The observed absolute closure is `6.776263578034403e-21`, below
  the bound `3.029653286850545e-17`.

The height-volume weighted relative difference between the rank-1 and rank-2
representations of the same parent field is
`4.080123830400332e-8`.

## Exact partition of this one update

| term | value | fraction of $N$ |
|---|---:|---:|
| $N_1$ (mode-1 diagonal) | `4.604291767737819e-6` | `0.2247420627867173` |
| $N_2$ (mode-2 diagonal) | `1.588271320072229e-5` | `0.7752579348666966` |
| $N_{12}$ (signed coupling) | `4.807451805616416e-14` | `2.346585946426245e-9` |
| $N$ | `2.048700501653463e-5` | `1` |

The mode-2 diagonal term is `3.582010485840303e-5` (about `0.003582%`) of
the current state Gram-metric squared norm and
`1.664741047128487e-15` of the corresponding parent quantity. In this fixed
POD basis, the mode-2 diagonal term nevertheless accounts for about `77.53%`
of $N$. The net signed off-diagonal term is only `2.346585946426245e-9` of
$N$, so it does not explain the magnitude of $N$ within this algebraic
partition. These are basis-dependent algebraic shares, not a unique physical
energy attribution.

The largest coordinate changes for both modes occur at group 40, snapshot 2;
that cell supplies `6.762839505718414e-2` of $N$. The physical leakage
hotspot is separately at group 154, snapshot 2, with signed change
`3.716142964549363e-4 cm^-1`. The signed reactivity change is
`1.256333817507227e-3`. Leakage and reactivity are shared outputs of the
coupled map and are not assigned to either POD mode by this decomposition.

The production defect is reproduced as

$$
R_a=6.797330105507151\times10^{-3}.
$$

## Interpretation boundary

The narrow supported statement is:

> The mode-2 diagonal term is large in this one stored update despite its small
> diagonal share of the state Gram-metric squared norm. Leakage and reactivity
> also change in the same coupled map, but this decomposition does not
> attribute those changes to either mode.

This does not establish a large Jacobian eigenvalue, instability, divergence,
physical inaccuracy, rank-2 inferiority or a need for damping. It does not
select a nonlinear solver and it authorizes no next Picard map.

## Reproduction identity

The checker is
[`check_one_map_xsm.f90`](check_one_map_xsm.f90), invoked in `--mode2` mode
and compiled with binary64-preserving flags (`-ffp-contract=off` and
`-fno-fast-math`). Its SHA-256 in this result is
`8df9ef2056da34ca5eea597fa3f9b0a4c2a8a30d99939cf8356a6a7878a24586`.
The five read-only inputs are:

| role | local object | SHA-256 |
|---|---|---|
| rank-1 basis | `validation/artifacts/iterative-map1/basis_reference.xsm` | `dc65467731947901393f9fb7114b7cd2e956a9992bb97db18e665b47e7446504` |
| rank-1 raw parent | `validation/artifacts/iterative-x7-direct/candidate_axial.xsm` | `e7f7f4e8d7d296a943c10a419052cffe7970eeff017eb76428276d29124f0fee` |
| rank-2 system | `validation/artifacts/iterative-rank2-map-axial2/candidate_system.xsm` | `c2700e289ab98b1a26e4511f1fe988723d58804b674e4cde32d836d01d77acda` |
| rank-2 parent | `validation/artifacts/iterative-rank2-map-axial2/rank2_parent_axial.xsm` | `a464cc05a1d21f00c1edb1e1cc5451846a995cb67b08f0869d4709958f9e6e38` |
| rank-2 current | `validation/artifacts/iterative-rank2-map-axial2/candidate_axial.xsm` | `5ec5a3576fab3662cd5fabc18226d98e56fd9b936deabe6bd70a09623f596f61` |

The audited local Ganlib archive has SHA-256
`204d9f3aeaf4e06d8fbb62225e14859a767476cd845ba0096f166b5f9e14822c`.
The run used GNU Fortran 15.2.0 and completed in less than one second after
compilation.

From the repository root, the exact invocation is:

```sh
build_dir=$(mktemp -d "${TMPDIR:-/tmp}/spot-mode2.XXXXXX")
gfortran -O0 -g -std=f2008 -pedantic -Wall -Wextra -Werror \
  -Wno-compare-reals -ffp-contract=off -fno-fast-math \
  -I Ganlib/src validation/iterative/check_one_map_xsm.f90 \
  Ganlib/src/libGanlib.a -lstdc++ -o "$build_dir/check_one_map_xsm"
"$build_dir/check_one_map_xsm" --mode2 \
  validation/artifacts/iterative-map1/basis_reference.xsm \
  validation/artifacts/iterative-x7-direct/candidate_axial.xsm \
  validation/artifacts/iterative-rank2-map-axial2/candidate_system.xsm \
  validation/artifacts/iterative-rank2-map-axial2/rank2_parent_axial.xsm \
  validation/artifacts/iterative-rank2-map-axial2/candidate_axial.xsm
```
