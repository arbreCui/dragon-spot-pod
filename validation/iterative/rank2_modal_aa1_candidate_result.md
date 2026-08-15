# Rank-2 modal AA(1) proposal materialization

Date: 2026-08-14

Status: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

The frozen modal-projected Anderson(1) scalar was applied once, offline, to
the complete published state:

\[
y=(1-\beta)x_1+\beta x_2,
\qquad \beta=0.53886432651360094.
\]

No Dragon, assembly, transport, axial solve or nonlinear-map evaluation was
run.  This stage therefore creates a proposal, not a new Picard iterate.

## Publication

The modal coordinates remain REAL64.  Leakage is rounded once to REAL32 and
promoted back to REAL64.  The inverse eigenvalue is published through the
production identity

\[
\rho_*=(1-\beta)\rho_1+\beta\rho_2,\qquad
k_{\rm pub}=Q_{32}(1/\rho_*),\qquad
\rho_{\rm pub}=1/\operatorname{REAL64}(k_{\rm pub}).
\]

The resulting values are:

- modal denominator: `6.6762694725360487e-5`;
- affine inverse eigenvalue: `0.73395259151331704`;
- published effective eigenvalue: `1.3624857664108276`;
- published inverse eigenvalue: `0.73395262148997154`;
- binary32 publication shift in rho: `2.9976654492003263e-8`;
- largest leakage publication round trip: `5.3633809199427063e-11`.

The output hashes are:

- AX proposal: `ae5f5b328fc6c5b181f40a4122b88771c857fd0200fc6e8351fc6b97d68d5c56`;
- snapshot carrier: `c11f4641897288f355ba60fa05eb7081d3aedfd8078333735d5c85c219f47c75`.

The AX object is explicitly marked `PROPOSAL` and `X2-RAW-FLUX`.  The copied
raw axial and radial fluxes remain x2 carrier data; they are not claimed to
be a transport solution at y.  The lagged `SYSTEM/SPOT-LEAK1D` history is
also retained unchanged.  Only the proposal state, published k/rho,
`FLUX/SPOT-LEAK1D`, and the required lifecycle records are changed.

## Independent checks

The separate Ganlib-only checker independently recomputed the AA(1) scalar
and publication arithmetic.  It established:

- fixed rank-2 layout, basis, Gram matrix and height are bitwise unchanged;
- the basis is bitwise tied to the frozen rank-2 reference;
- proposed A, k, rho and L match their declared arithmetic bitwise;
- AX and plane raw-flux carriers and fixed-source diagnostics are bitwise x2;
- the complete lagged SYSTEM payload is recursively bitwise x2;
- stale map, balance, projection and convergence records are absent;
- all `370 x 3 x 8 = 8880` REAL32-published `B*a` values are strictly
  positive, without a floor or tolerance.

The smallest published reconstruction is `1.75367700e-15` at group 370,
snapshot 3, region 2.  It is strictly positive in the actual publication
arithmetic, but its small magnitude is not presented as a robustness margin.

The local Git-ignored artifact contains the two XSM files, logs and a complete
checksum receipt at
`validation/artifacts/iterative-rank2-modal-aa1-candidate/result.sha256`.
The committed checker SHA-256 is
`4d9a3d458c49a4720b2e33535ec4bde9a469806eaa8e39ece0202ae1a793d6ff`.

Reproduce the offline materialization from the hash-locked local inputs with:

```sh
make spot-rank2-modal-aa1-candidate
```

The target intentionally refuses to overwrite an existing artifact directory.

## Scientific boundary

This result does not evaluate `G_2(y)`, a residual, balance closure,
convergence, rank adequacy or physical accuracy.  The next scientific step,
if separately authorized, is one fresh strict rank-2 map evaluation from this
published proposal.  It must retain the same physical map and introduce no
relaxation, damping, clipping, fitted closure or empirical coefficient.

That separate evaluation has since completed once and is documented in
[rank2_modal_aa1_map_result.md](rank2_modal_aa1_map_result.md). The proposal
artifact's own classification remains the correct historical classification
for this no-transport publication stage.
