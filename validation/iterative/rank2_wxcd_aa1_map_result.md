# One strict map from the w-x / c-d standard AA(1) state

Date: 2026-08-16

Classification: `VALID_NOT_MET`.

Exactly one frozen evaluation $G_2(y)$ ran from source commit
`9ee142798ade28742f3b7b2cbaa818b02c4a949d`, with

\[
y=1.6615840721007848x-0.66158407210078485d.
\]

No coefficient was adjusted after the candidate was frozen, and there was no
retry or fallback. The commit identity is established by the clean, aligned
pre-run HEAD and byte-identical frozen sources; the artifact receipt itself
does not contain a separate source-commit entry.

| solve | `IEXTF` | `EUNK` | `EINR` |
|---|---:|---:|---:|
| radial plane 1 | 9 | `4.99505120e-7` | `4.05886340e-7` |
| radial plane 2 | 5 | `4.63383572e-7` | `4.09440162e-7` |
| radial plane 3 | 10 | `4.26356650e-7` | `4.93058792e-7` |
| axial | 199 | `4.81847451e-7` | `4.81847451e-7` |

The axial `EEXT` was `4.38968089e-12`. Radial FLU CPU times were 26, 21 and
29 seconds; axial FLU CPU time was 140 seconds.

At the unchanged tolerance $5\times10^{-7}$:

| quantity | raw value | tolerance multiple | gate |
|---|---:|---:|---|
| $R_\rho$ | `0` | `0` | pass |
| $R_L$ | `1.285177921858958e-3` | `2570.356` | fail |
| $R_a$ | `4.607432352912023e-7` | `0.921486` | pass |

$D_L=1.883017830550671\times10^{-6}\,\mathrm{cm}^{-1}$ is diagnostic only.
Relative to the preceding $c\mapsto d$ map, $R_L$ and $D_L$ increased by
about 60.27%, while $R_a$ decreased by about 83.07% and entered tolerance.
The modal update improved, but leakage remains the sole failed gate.

The independently recompiled checker passed proposal/carrier identity, fixed
POD identity, live radial-operator change, radial positivity, canonical
layout, bitwise raw defects and restart lifecycle. The artifact contains 22
regular files, no symlinks and a passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `96cb06444bfca395b1765b907944aa2d32c4e877af41dbd58dee258b49025e45` |
| returned snapshots | `608b4ae084d7c5fdebbe3eaad30e82a453cd81fca160419eed4a7e73be288c91` |
| receipt | `637230a172fcf8aacf2120e8c80dea7042c8e0efc87007ab8b1ea07d5f1d9651` |
