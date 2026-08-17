# Minimum-order decision after the map from $y$

Date: 2026-08-17

Classification: `AA1_DIRECTION_FAIL_AA2_DIRECTION_FAIL_NO_CANDIDATE_NO_MAP`.

The latest genuine fixed-point residuals are

$$
f_0=v-q,\qquad f_1=x-w,\qquad f_2=z-y,
$$

where $z$ denotes the returned state from the latest physical map.  No
output-to-unrelated-output difference is used.

Standard full-Gram AA(1) on $f_1,f_2$ gives

$$
1.9531696606115592\,x-0.95316966061155906\,z.
$$

Its denominator is `2.2162079420711167e-13`.  The modal, leakage
height-$L_2$, and same-weight $D_L$ direction ratios are

$$
(0.66245183553241582,\ 2.8228318539955719,\ 2.5387308020979624).
$$

The two leakage directions fail, so AA(1) is rejected and not materialized.

Only then, standard unregularized full-Gram AA(2) on $f_0,f_1,f_2$ gives
the formal affine weights

$$
(\alpha_v,\alpha_x,\alpha_z)=
(0.92125422555104919,-0.087299068768082078,
 0.16604484321703289).
$$

The unchanged $2\times2$ determinant is `1.7105793722062437e-25`.  The
modal, leakage height-$L_2$, and same-weight $D_L$ direction ratios are

$$
(0.063607294820461679,\ 1.2052138448555736,\
 1.0315766813341534).
$$

The two leakage directions again fail.  Although both formal affine fields
remain positive at 8880/8880 reconstructed points, positivity does not
override the three-direction AND gate.  AA(2) is rejected and not
materialized.

No cutoff, regularization, pseudoinverse, fit, damping, relaxation,
clipping, empirical parameter, older-window search, AA(3), fallback, or
retry is used.  No candidate, candidate runner, map wrapper, or physical
map was created; Dragon execution count is zero.  This result rejects only
the current minimum-order safeguarded window and is not a proof of global
nonconvergence.

The input states remain the previously hash-locked $q,v,w,x,y,z$ artifacts;
the latest returned AX and snapshots have SHA-256
`2c2649c4317cc98fb84b0fa441d14d62834736db9dd1b52857004b34804761cb`
and `685a4433acca6f1402df58b373308d5c7e4ccd0d13cda7dd2ca475394999e815`.
