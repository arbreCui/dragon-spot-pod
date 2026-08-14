# Frozen-snapshot rank-2 basis reconstruction

## Scope

This is a short offline reconstruction of the rank-2 SPOD trial space from
the same three raw radial snapshots that produced the frozen rank-1 basis.
It does not use x7 or x8, assemble a system, solve transport, execute Dragon,
or perform a Picard iteration.

The two read-only inputs are:

| role | bytes | SHA-256 |
|---|---:|---|
| `validation/artifacts/iterative-seed/initial_snapshots.xsm` | 227,725,476 | `37656f3269c59db9a5df59ac3686a6da65bc07afa051e2473ffbefadcb2c2b95` |
| `validation/artifacts/iterative-map1/basis_reference.xsm` | 800,220 | `dc65467731947901393f9fb7114b7cd2e956a9992bb97db18e665b47e7446504` |

Both are local, Git-ignored artifacts. A fresh clone therefore needs copies
matching these hashes.

## Construction

The builder descends through the seed archive's one-item `SNAP` wrapper,
reads three `TRACK`/`FLUX` pairs, and maps each scalar flux by its own
`KEYFLX`:

$$
\phi_{rkg}=\mathrm{FLUX}_{kg}(\mathrm{KEYFLX}_{rk}).
$$

For every one of 370 energy groups, it calls the production
`SPOPOD`/`ALSVDF` path once at rank 1 and once at rank 2. No second SVD
implementation is used to create the basis. The rank-1 replay is a control;
the rank-2 file is retained only if that control reproduces the locked
rank-1 POD records bitwise.

The local output is

`validation/artifacts/iterative-rank2-basis/rank2_basis.xsm`

with 832,780 bytes and SHA-256

`2d7fc2bf36f65a203731c34dcea18a679fc0232b58c59caad828178a77ff45a8`.

The output is also Git-ignored. It is not the active continuation basis and
is not read automatically by any iteration runner.

## Independent checks

The Ganlib-only checker does not link `SPOPOD`, `ALSVDF`, ASM, FLU, Dragon,
or a transport solver. It reads the raw snapshots, locked reference, fresh
rank-1 control and rank-2 candidate and verifies:

- 370 groups, 8 radial regions and 3 snapshots;
- all groups retain two numerical modes under the existing production rank
  rule;
- the fresh rank-1 POD fields reproduce the locked reference bitwise;
- volumes, all three singular values, radial operators and cross sections are
  unchanged bitwise between rank 1 and rank 2;
- the rank-2 first basis vector and its three coefficients reproduce the
  fresh rank-1 prefix bitwise;
- stored reconstruction and volume-Gram diagnostics are reproduced bitwise
  from the original snapshots;
- two repeated builds produce bitwise-identical XSM files.

No empirical acceptance tolerance is introduced. Floating residuals caused
by storing the basis and coefficients in REAL32 are reported rather than
used as adjustable gates:

| diagnostic | value | group |
|---|---:|---:|
| maximum rank-2 volume-Gram defect | `6.637536276166145e-8` | 114 |
| maximum relative coefficient-projection defect | `8.256954693429560e-8` | 254 |
| minimum ideal spectral tail | `6.577286811389827e-9` | -- |
| maximum ideal spectral tail | `3.408482963639734e-4` | 241 |
| minimum stored reconstruction error | `2.421745014403484e-8` | -- |
| maximum stored reconstruction error | `3.408483000025015e-4` | 241 |
| maximum stored/spectral absolute difference | `5.973055078085415e-8` | 8 |

Reproduce the result with:

```sh
make spot-rank2-basis
```

The complete target takes about three seconds on the recorded workstation.

## Scientific boundary

Classification: `OFFLINE_RECONSTRUCTION_ONLY`.

This establishes that a genuine, production-convention rank-2 trial space
can be reconstructed reproducibly from the original frozen snapshots. It
retains mode 1 bitwise and adds a second production-numerical mode. It does
not show that rank
2 will make Picard converge, improve an eigenvalue or power distribution, or
provide a separately interpretable second physical mode. No rank-2 transport
map has been evaluated.
