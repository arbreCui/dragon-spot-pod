# One strict map from the v-w-x standard AA(1) state

Date: 2026-08-16

Classification: `VALID_NOT_MET`.

Exactly one frozen evaluation $G_2(c)$ ran from source commit
`6c8129531f66791201da5abf582da76754748517`, with

\[
c=0.37810309349656490w+0.62189690650343510x.
\]

No coefficient was adjusted after the candidate was frozen, and there was no
retry or fallback.

The commit identity is established by the clean pre-run HEAD, aligned remote
HEAD and byte-identical frozen sources; the artifact receipt itself does not
contain a separate `source_commit.txt` entry.

| solve | `IEXTF` | `EUNK` | `EINR` |
|---|---:|---:|---:|
| radial plane 1 | 4 | `2.43054501e-7` | `4.05090901e-7` |
| radial plane 2 | 8 | `4.61654992e-7` | `3.91664798e-7` |
| radial plane 3 | 4 | `4.57228907e-7` | `3.40692139e-7` |
| axial | 240 | `4.16255915e-7` | `4.80351389e-7` |

The axial `EEXT` was `5.03582898e-10`. Radial FLU CPU times were 16, 27 and
18 seconds; axial FLU CPU time was 142 seconds.

At the unchanged tolerance $5\times10^{-7}$:

| quantity | raw value | tolerance multiple | gate |
|---|---:|---:|---|
| $R_\rho$ | `6.422349219104007e-8` | `0.128447` | pass |
| $R_L$ | `8.018947041737536e-4` | `1603.789` | fail |
| $R_a$ | `2.721935004163532e-6` | `5.44387` | fail |

$D_L=1.174921635538340\times10^{-6}\,\mathrm{cm}^{-1}$ is diagnostic only
and does not alter the AND gate. The map is therefore valid but not a
converged fixed point.

The independently recompiled checker passed proposal/carrier identity, fixed
POD identity, live radial-operator change, radial positivity, canonical
layout, bitwise raw defects and restart lifecycle. The artifact contains 22
regular files, no symlinks and a passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `4e1d50a42353a8d76e3796539746225de6f62857045275847b5049f28e542a48` |
| returned snapshots | `77c2f98ef473faba9e44c3de1b7c685466264e4ed6e5ddc5b4175bf1623316ca` |
| receipt | `f8c2542976183c294b50d73f188aecff34c8b04a622e6eaf1c1a0e76504f9352` |
