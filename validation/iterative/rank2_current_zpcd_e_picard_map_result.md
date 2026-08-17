# Direct Picard map from the latest returned state $e$

Date: 2026-08-17

Map classification: `VALID_NOT_MET`.

The latest returned state was evaluated exactly once from source commit
`ce6be5b9c18201bd24af1c9318c830a6e0b8f6b3`:

$$
f=G_2(e).
$$

Three fresh online radial fixed-source solves and one axial solve produced
the physical residual $f-e$

$$
(R_\rho,R_L,D_L,R_a)=
(1.284469730578053\times10^{-7},\,
8.318307793557387\times10^{-4},\,
1.218781108036637\times10^{-6}\ \mathrm{cm}^{-1},\,
1.505196532244700\times10^{-6}).
$$

At the unchanged $5\times10^{-7}$ three-component AND gate, $R_\rho$
passes at `0.256893946` tolerance multiples.  $R_L$ and $R_a$ fail at
`1663.661559` and `3.010393` multiples.  Dimensional $D_L$ is diagnostic
only.  SPOT therefore still has no accepted rank-two fixed point.

Against the preceding genuine residual $e-c_{\mathrm{next}}$, $R_\rho$
increased by `99.999982%`, $R_L$ by `6.957398%`, $D_L$ by `6.957321%`,
and $R_a$ by `18.813390%`.  This is one direct step, not an asymptotic
convergence or divergence rate.

## Strict solver terminals

| solve | `IEXTF` | `EEXT` | `EUNK` | `ITERF` | `EINR` | FLU CPU |
|---|---:|---:|---:|---:|---:|---:|
| radial plane 1 | 5 | `0` | `4.00482492e-7` | 5 | `3.51209792e-7` | 21 s |
| radial plane 2 | 5 | `0` | `3.22750651e-7` | 2 | `4.37859939e-7` | 18 s |
| radial plane 3 | 5 | `0` | `4.48904217e-7` | 5 | `2.31361469e-7` | 20 s |
| axial | 204 | `3.12178755e-10` | `4.81847792e-7` | 1 | `4.81847735e-7` | 137 s |

All strict terminals passed below `4.99999999e-7`.  The independent
`continued` checker passed the fixed POD package, live radial operator, raw
radial positivity, canonical layout, bitwise raw defects, and restart
archive.  The global balance diagnostic is `7.25189e-9`; it is separate
from the fixed-point gate.

The Git-ignored artifact has 22 regular files, no symbolic links, and a
passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `6e26d8dc40bf79c0dedad19912557dfed5ccd2c3bdb38ea719ce32b5cc9aba6c` |
| returned snapshots | `4e6ede5bb7253999850d8306c8f0683df9c6191e4dc5f19b2381b10f56fb0a2d` |
| radial log | `2c7074b84251eb64b7454763e45e254207c8a75b9f605ad5c5de73595bc6e583` |
| axial log | `2c721c5894040b70d649625590ef41b88836094bab05bdd8d9a6d03b75205e66` |
| independent check | `0db7dac519f882a1d6102ba00adf8fd102dc00c68aaea346c9dd8067e8715f02` |
| receipt | `9c34fc89118bdc4a6b7af373105bae75969c41f0b5e1725ce12ef2ed7606db67` |

## Minimum-order direction decision

The next standard full-Gram AA(1) uses only the genuine residuals
$e-c_{\mathrm{next}}$ and $f-e$.  Its affine output direction is

$$
q_1=0.54317069088638781\,e+
0.45682930911361219\,f,
$$

with denominator `3.3988810913576900e-12`.  The modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are

$$
(0.059424727376440133,\ 0.19596354669013863,\
0.28717479223258224).
$$

All three are strictly below one.  Independent builder and checker
arithmetic also confirms 8880/8880 positive reconstructed points, with
minimum `1.7533991760352251e-15`.  The classification is
`AA1_DIRECTION_PASS_AA2_SKIPPED`; AA(2) is not evaluated.

This direction decision is not convergence evidence.  No durable next
proposal is published and no second physical map is run.  No relaxation,
damping, clipping, fit, regularization, pseudoinverse, condition cutoff,
empirical parameter, mixed-unit objective, older-window search, or AA(3)
is used.
