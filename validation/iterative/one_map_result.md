# One corrected fixed-space map

This receipt records the first bounded transport evaluation of the current
method,

\[
x_1=G(x_0),
\]

and one fresh replay from the same frozen input. It is evidence for one map,
not for outer convergence.

## Frozen calculation

- source commit: `c7c7b45027766aafba2481973d89c0cee3c3819d`;
- Dragon SHA-256:
  `e4c61fa45ba0fe62be3a15e21785c5e27b9a3c10d727a02754d43d7c79ef2759`;
- deck SHA-256:
  `4c8780b1739b5aaec0c78d0cbe2b23b6021f860d232af8e9c1767ed989c9720e`;
- `SpotRefFS.c2m` SHA-256:
  `db763e8c013d9f753ae6eb635dc5490c6bb34b9f23ea211dd3b282b6ec031742`;
- `SpotPlaneFS.c2m` SHA-256:
  `69a2931c817d298a3af36f5e1f55760c58dd55229c73002b4b01d3a4797e27b5`;
- rank: 1 in every one of 370 groups;
- planes: 3;
- inner tolerance: binary32 `0x350637bd`, equal to \(5\times10^{-7}\)
  at the deck interface;
- relaxation, fitting and clipping: absent.

The four seed hashes are the corresponding `initial_*` entries in
`seed.sha256`. Both runs verified them before calculation and used fresh
byte-copies.

## Result

Both axial solves and all three radial solves reached their declared FLU
terminal state without touching an iteration limit. The three radial
fixed-source solutions were strictly positive, their frozen fission sources
were nonnegative and nonzero, and the returned axial field had no nonpositive
active cell.

The independent Ganlib-only checker established:

- the complete POD package was bit identical before and after the map;
- at least one `RADIAL-OP` value changed, so the online radial response was
  actually rebuilt;
- the canonical state layout, basis, Gram matrix and plane heights were bit
  identical;
- the three outer residuals and the accompanying \(D_L\) diagnostic equal an
  independent recomputation bit for bit;
- the returned three-plane restart archive contains the current leakage in
  each flux state, the preceding leakage in each system, and the declared
  fixed-source equation identity, all bit for bit.

The four recorded map-change quantities at \(x_0\) are

\[
\begin{aligned}
R_\rho &= 1.2811548254498817\times10^{-6},\\
R_L    &= 7.9228531576958625\times10^{-4},\\
D_L    &= 1.1616502888500690\times10^{-6},\\
R_a    &= 9.2282558412815538\times10^{-7}.
\end{aligned}
\]

\(D_L=\|L^+-L\|_\infty\) is the dimensional companion to \(R_L\), not a
fourth convergence criterion.

The eigenvalues stored by the direct leakage return are

\[
k_0=1.3641711473464966,\qquad
k_1=1.3641735315322876.
\]

For the returned axial state, the reported global balance norm is
\(3.606202\times10^{-9}\), the maximum separately normalized group
diagnostic is \(3.228839\times10^{-3}\), and the maximum Galerkin residual is
\(5.91575\times10^{-7}\). All FLU terminal residuals satisfy the declared
binary32 solver tolerance. The independent postsolve Galerkin diagnostic is
reported separately and is retained for Stage-4 tolerance sensitivity; it is
not compared with an invented threshold. The group diagnostic is likewise
reported without an empirical acceptance threshold.

`SPOFCHK L2/MAX` is the radial response change, and `SPOT-Q-L2/MAX` is the
saved-RHS lag. Neither is relabeled as an outer residual or assigned an
ad-hoc threshold.

## Replay

The fresh replay produced byte-identical scientific XSM containers. These
five values are also stored in the machine-readable
`one_map_scientific.sha256` gate used by `VERIFY_REFERENCE=1`:

```text
dc65467731947901393f9fb7114b7cd2e956a9992bb97db18e665b47e7446504  basis_reference.xsm
0a54da1236f863a7574f17bc7d931f9a18629aceeb5f99ebfdb7dae29464fceb  state0_axial.xsm
fa693cbcc8a60f64521f6ad5be660c8d13414586f03da91506a01021ed5981c2  state1_system.xsm
2323a256002f1e6f75f5af72c31479b0f6a7bff561d401cee363dcf9fc6ff484  state1_axial.xsm
1b5a0c98aba0f5b4f366b64a8157f4a104df0f89f4cdeafc60eb6ce7811018e1  state1_snapshots.xsm
```

The raw log files differ only in runtime and memory telemetry. All scientific
markers and both independent checker results are identical.

## Qualification boundary

```text
map runtime structure : PASS
fixed-space XSM state : PASS
same-input replay     : PASS
inner sensitivity     : PENDING
outer convergence     : NOT EVALUATED
```

The next formal calculation is the predeclared inner-tolerance sensitivity
from the same \(x_0\). A second outer return or a long Picard trajectory is
not yet qualification evidence.
