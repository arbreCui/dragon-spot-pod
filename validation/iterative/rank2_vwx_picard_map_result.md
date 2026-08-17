# Direct continuation from w

Date: 2026-08-16

Classification: `VALID_NOT_MET`.

Exactly one frozen evaluation $x=G_2(w)$ ran from source commit `8067954`.
The parent AX and snapshots were locked at
`defdee0cf442470eb623ebb83c8bed59b8c20308121951ef0c72073ddba3c243`
and `661fa88ed1a8a08907d5a31d90a367565a5c3dbcd0e50a8c3ccecc866436f1ca`.
There was no proposal, coefficient, retry or fallback.

| solve | `IEXTF` | `EUNK` | `EINR` |
|---|---:|---:|---:|
| radial plane 1 | 5 | `3.97515890e-7` | `3.81725727e-7` |
| radial plane 2 | 9 | `4.95075994e-7` | `3.11236505e-7` |
| radial plane 3 | 6 | `4.74305409e-7` | `2.99253685e-7` |
| axial | 216 | `3.78594706e-7` | `4.50328145e-7` |

The axial `EEXT` was `4.66514161e-10`. Radial FLU CPU times were 19, 27 and
21 seconds; axial FLU CPU time was 146 seconds.

At the unchanged tolerance $5\times10^{-7}$:

| quantity | raw value | tolerance multiple | gate |
|---|---:|---:|---|
| $R_\rho$ | `0` | `0` | pass |
| $R_L$ | `4.599429150357613e-4` | `919.886` | fail |
| $R_a$ | `1.143767569467111e-6` | `2.28754` | fail |

$D_L=6.738991942256689\times10^{-7}\,\mathrm{cm}^{-1}$ is diagnostic only.
Relative to $v\mapsto w$, $R_L$ and $D_L$ increased by approximately
`1.74498`, while $R_a$ fell to `0.60946`. Thus direct continuation is no
longer componentwise decreasing.

The checker passed fixed POD identity, live radial-operator change, radial
positivity, canonical layout, bitwise raw defects and restart lifecycle. The
artifact contains 22 regular files, no symlinks and a passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `b693b310ae8f499a869254cee77b1b787f9fa66813c24321dbfe5b00994c7196` |
| returned snapshots | `8a5a9f7171a4029a25d6a55cedfb64d114f3fe57db112c688c88786e6ce0c9e8` |
| receipt | `9bf91c65eff960ab9903079e76408175e2febffa73bfae674423ca9da252ad08` |
