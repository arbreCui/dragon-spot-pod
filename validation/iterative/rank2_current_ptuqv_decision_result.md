# Minimum-order decision after $v=G_2(q)$

Date: 2026-08-17

Classification: `AA1_FAIL_AA2_PASS`.

The latest two actual residuals are $u-t$ and $v-q$; $v-u$ is not a
fixed-point residual.  Standard full-Gram AA(1) gives

$$
-0.10571997744112904\,u+1.10571997744112904\,v.
$$

Its modal ratio is `0.66672177530804910`, but the same-weight leakage
height-$L_2$ and $D_L$ ratios are `1.15375812119925825` and
`1.25785865829673038`.  AA(1) therefore fails and is not materialized.

The latest three genuine maps are $p\mapsto t$, $t\mapsto u$, and
$q\mapsto v$.  Standard unregularized full-Gram AA(2) gives

$$
w=0.19768585711059219\,t
 +0.21627230078843410\,u
 +0.58604184210097376\,v.
$$

The unmodified $2\times2$ determinant is
`2.7443289755626049e-25`.  The modal, leakage height-$L_2$, and $D_L$
ratios are `0.35609128006915597`, `0.58429312631281327`, and
`0.71221426364805607`; all pass.  No cutoff, regularization, fit, damping,
relaxation, clipping, empirical parameter, older-window search, or AA(3) is
used.  Therefore $w$ is the unique minimum-order candidate authorized for
one independently checked physical map.
