# Latest three-pair AA(2) proposal

Date: 2026-08-17

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

The standard full-Gram AA(2) proposal is

$$
w=0.19768585711059219\,t
 +0.21627230078843410\,u
 +0.58604184210097376\,v.
$$

The builder and separately compiled checker reproduced the unchanged
$2\times2$ system, all three direction ratios, REAL64 modal publication,
REAL32 $k$ and leakage publication, the fixed rank-two basis, and the latest
$v$ raw carrier.  The determinant is `2.7443289755626049e-25`; no numerical
cutoff or regularization was applied.  All 8880 reconstructed points are
positive, with minimum `1.7533999171890540e-15`.

The proposal hashes are:

- AX: `0be2f39496fb5de7f4c942ec2e249d484492218e1376a9331b3ec19e7427a2d0`
- snapshots: `cdd6893892c5ba0140a3f5d3ce82bfef476c9a6537a939f41ecd53b2825e14e0`

The artifact has a passing 9/9 receipt and contains no transport solve or
map result.  The proposal was subsequently evaluated exactly once; see
[rank2_current_ptuqv_aa2_map_result.md](rank2_current_ptuqv_aa2_map_result.md).
