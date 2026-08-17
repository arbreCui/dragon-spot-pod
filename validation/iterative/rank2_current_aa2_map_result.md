# One strict map from the current-window standard AA(2) proposal

Date: 2026-08-16

Classification: `VALID_NOT_MET`.

Exactly one frozen evaluation \(G_2(q_{\mathrm{AA2}})\) ran from source
commit `d6bf4365b04a4c3b9ffd41e112b44c8123f6c106`, where

\[
q_{\mathrm{AA2}}=
0.72283238162036112x
-0.23768716180315402d
+0.51485478018279296e.
\]

The standard AA(2) weights were not changed after publication. There was no
clipping, damping, retry or fallback.

| solve | `IEXTF` | `EUNK` | `EINR` | FLU CPU |
|---|---:|---:|---:|---:|
| radial plane 1 | 10 | `3.04459064e-7` | `4.40753524e-7` | 27 s |
| radial plane 2 | 4 | `3.60752722e-7` | `3.80280937e-7` | 17 s |
| radial plane 3 | 4 | `4.56512737e-7` | `3.39667139e-7` | 19 s |
| axial | 181 | `4.81847849e-7` | `4.81847849e-7` | 135 s |

The axial `EEXT` was `5.68988523e-10`. All four strict terminal
predicates passed before their fixed 120/180-second process bounds.

At the unchanged \(5\times10^{-7}\) outer gate:

| quantity | raw value | tolerance multiple | gate |
|---|---:|---:|---|
| \(R_\rho\) | `6.422348086676521e-8` | `0.128447` | pass |
| \(R_L\) | `6.224270631088404e-4` | `1244.854` | fail |
| \(R_a\) | `2.118720252720744e-6` | `4.237441` | fail |

The diagnostic dimensional leakage defect is

\[
D_L=9.119685273617506\times10^{-7}\ \mathrm{cm}^{-1}.
\]

Relative to the preceding \(y\mapsto e\) map, \(R_L\) and \(D_L\)
decreased by 51.57%, while \(R_a\) increased by 359.85% to 4.598 times its
previous value. Thus AA(2) moved the only previously failed leakage direction
substantially downward, but lost modal convergence. The offline linear
leakage screen predicted the correct direction but overstated its magnitude;
the offline modal prediction did not survive the fresh nonlinear map.

The independent Ganlib checker passed the exact
`PROPOSAL + AA2-RAW-FLUX` parent, fixed POD identity, live radial-operator
change, radial positivity, canonical layout, bitwise raw defects and restart
lifecycle. The global balance diagnostics were `6.97123e-9` and
`1.63438e-3` for the reported global and maximum-group values; they are not
stopping defects.

The Git-ignored artifact contains 22 regular files, no symbolic links and a
passing 21/21 payload receipt.

| output | SHA-256 |
|---|---|
| returned AX | `86d2e3155ad9c41cc2ba62c87df40144399c74ba5a045c25e182e7f8a8ec3f9c` |
| returned snapshots | `dbadf350989ebb9d6137905a30ca023932560ed1bc927f064350f2c96231b45b` |
| receipt | `847d6cfe03e1af462986e406fcc7b9de74acd2f5edf2baf43b69c8b3dfbeeb07` |

This is a valid physical map, not a converged fixed point. No successor
proposal, map or retry was started.
