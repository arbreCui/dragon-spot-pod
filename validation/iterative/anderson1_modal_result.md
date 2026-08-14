# Offline modal-residual Anderson(1) check

This check reads the frozen strict \(x_4,x_5,x_6\) states and does not call
Dragon or write a candidate state. With fixed-basis modal coordinates
\(a_i\), define

\[
f_4=a_5-a_4,\qquad f_5=a_6-a_5,
\]

and use the existing Gram-height inner product. The single coefficient is
the unique, unclipped least-squares value

\[
\gamma=
\frac{\langle f_5-f_4,f_5\rangle_{HG}}
     {\lVert f_5-f_4\rVert_{HG}^2},\qquad
a_A=\gamma a_5+(1-\gamma)a_6.
\]

There is no fitted damping or relaxation coefficient. Depth one and the
modal metric are declared algorithm choices.

The frozen data give

```text
gamma                              0.7868687504961641
weight on x6                       0.2131312495038359
||f4||_HG                          1.544886893195163e-7
||f5||_HG                          5.062288215163166e-7
linearized residual norm           7.393723863024349e-8
linearized residual / ||f5||       0.1460549765001090
```

The coefficient is a convex combination. Direct reconstruction of
\(B a_A\) is finite and strictly positive at all 8,880 group/plane/radial
points, without a floor or tolerance. The minimum is
\(1.750004465980173\times10^{-15}\) at group 370, plane 3, radial region 2.

This establishes only a strictly positive fixed-space radial-feedback
candidate and a reduction of the affine modal residual model. It does not
evaluate \(G(x_A)-x_A\), construct the complete state
\((a_A,\rho_A,L_A)\), establish axial balance, or establish convergence.

Reproduce the read-only check with

```sh
sh validation/iterative/run_anderson1_modal_check.sh
```

The input hashes are frozen in `anderson1_modal_scientific.sha256`.
