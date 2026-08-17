# Minimum-order decision after $x=G_2(w)$

Date: 2026-08-17

Classification: `AA1_DIRECTION_PASS_AA2_SKIPPED`.

The latest two genuine fixed-point residuals are

$$
f_0=v-q,\qquad f_1=x-w.
$$

The difference $x-v$ is not used.  Standard full-Gram AA(1) gives

$$
y=0.88057313037525409\,v
 +0.11942686962474590\,x.
$$

The modal, leakage height-$L_2$, and same-weight $D_L$ direction ratios are
`0.10973994188609061`, `0.71365032258515559`, and
`0.84191942726698699`.  All are strictly below one, and all 8880
reconstructed points are positive.  AA(1) therefore passes.

By the fixed minimum-order rule, AA(2) is not formed or tested.  There is no
relaxation, damping, clipping, fit, regularization, cutoff, older-window
search, empirical parameter, fallback, or retry.  The unique authorized
candidate is $y$.
