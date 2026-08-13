# Current direct continuation result

This records exactly one continuation

\[
x_2=G(x_1)
\]

after the accepted current one-map result. It is a two-step trend diagnostic,
not an outer-convergence result.

## Frozen parent and controls

The parent state is the hash-locked `iterative-map1` package. The current
Stage-2 calculation reproduced its system and axial state byte for byte. Its
separately serialized snapshot and this parent snapshot both pass the same
independent restart-record identities; whole-container identity is not
claimed.

```text
dc65467731947901393f9fb7114b7cd2e956a9992bb97db18e665b47e7446504  basis_reference.xsm
fa693cbcc8a60f64521f6ad5be660c8d13414586f03da91506a01021ed5981c2  state1_system.xsm
2323a256002f1e6f75f5af72c31479b0f6a7bff561d401cee363dcf9fc6ff484  state1_axial.xsm
1b5a0c98aba0f5b4f366b64a8157f4a104df0f89f4cdeafc60eb6ce7811018e1  state1_snapshots.xsm
```

The source commit before adding this continuation was `a3a81e3`. The Dragon
SHA-256 was
`dabc549461c401a5d5806753b4cfd0db627e2def61f1938aceaf2432c3762e28`.
Rank remained one in every energy group and the inner tolerance remained
\(5\times10^{-7}\). Relaxation, damping, fitting, clipping, parameter
changes and automatic retries were absent.

The physical sequence was only

\[
(B a_1,k_1,L_1)
\longrightarrow 3\text{ radial fixed-source solves}
\longrightarrow \text{fixed-}B\text{ assembly}
\longrightarrow 1\text{ axial solve}
\longrightarrow x_2.
\]

## Strict inner termination

The three radial solves reached their strict terminal predicates after 25,
29 and 7 outer iterations; the radial process used 69 CPU seconds. The axial
solve reached its strict terminal predicate after 134 outer iterations; the
axial process used 46 CPU seconds. Every solve reported `EUNK-VALID=1`,
`STATE=1`, `IGDEB=371`, and residuals no greater than the declared tolerance.

Each process used a 75 s process timeout. Only if that timeout had fired would
the wrapper have allowed up to 5 s of TERM grace before KILL. No strict 80 s
total-wall-clock claim is made.

## Raw defects and observed trend

The independently checked continuation defect is

\[
\begin{aligned}
R_{\rho,2} &= 0,\\
R_{L,2}    &= 3.956455644583086\times10^{-4},\\
D_{L,2}    &= 5.800975486636162\times10^{-7},\\
R_{a,2}    &= 7.237783517966097\times10^{-7}.
\end{aligned}
\]

Compared component by component with \(x_0\to x_1\):

| defect | first map | continuation | ratio |
|---|---:|---:|---:|
| \(R_\rho\) | \(1.2811548\times10^{-6}\) | \(0\) | \(0\) |
| \(R_L\) | \(7.9228532\times10^{-4}\) | \(3.9564556\times10^{-4}\) | \(0.499373\) |
| \(D_L\) | \(1.1616503\times10^{-6}\) | \(5.8009755\times10^{-7}\) | \(0.499374\) |
| \(R_a\) | \(9.2282558\times10^{-7}\) | \(7.2377835\times10^{-7}\) | \(0.784307\) |

Thus all three dimensionless defects decreased in this one continuation.
The zero \(R_{\rho,2}\) means the stored binary32 eigenvalue, and therefore
its binary64 reciprocal, did not change; it is not an exact-arithmetic claim.
No contraction factor is fitted from these two steps.

The global balance norm was \(3.750150\times10^{-9}\). The separately
reported maximum Galerkin diagnostic was \(5.61745\times10^{-7}\); it is
reported directly and is not converted into an empirical acceptance factor.

## Independent check and artifacts

The Ganlib-only continuation checker passed the fixed POD package, live
radial response, positive radial flux, canonical layout, independently
recomputed raw defect and restart-archive time ordering. In particular, the
radial equations used \(L_1\) and frozen-source \(k_1\), while the returned
archive contains \(L_2\).

The accepted local artifacts are hash-frozen under
`validation/artifacts/iterative-map2-current`:

```text
6528228ccf1a75b7be490461e1e75a247af68e979ea79e4d25f203905fbcd7a6  radial.log
d6a5bfb84e81f1a7aad2219a3c69cb1b3835570246c71fa2abe59fee92fb7b0c  axial.log
6691a5750fbcbd5293f97d984b07382d82e96a0783174ce5d966e618bd1cf29d  state2_system.xsm
7bee7c9ff8cdfd657fa0a831a34ebe559dbe1035fd978af16c98738e992495b2  state2_axial.xsm
a0dc5417bf4a68762c642fa8c2001c7cee6a7d1a87ce2aa01d9d9ba8c576ce06  state2_snapshots.xsm
```

## Development-run note and boundary

The only radial calculation completed normally and passed all three strict
solver predicates. The first runner version then rejected its completion
marker because it omitted CLE-2000's `>|` output prefix. The check was fixed,
the same unchanged radial output was accepted, and the axial calculation was
launched exactly once. The radial calculation was not rerun.
The corrected two-part runner was not rerun end to end.

This proves a valid second direct update and shows a decreasing two-step
trajectory. It does not prove asymptotic contraction, exclude a later
oscillation, or establish outer convergence.
