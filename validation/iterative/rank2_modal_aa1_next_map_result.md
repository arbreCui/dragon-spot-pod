# Fresh map from the next rank-2 modal AA(1) proposal

Date: 2026-08-15

Classification: `VALID_NOT_MET`.

The separately authorized experiment evaluated exactly one unchanged map

\[
v=G_2(w_{\rm pub}),
\qquad
w_{\rm pub}=0.0697254493303232x_2+0.9302745506696768z.
\]

It reused the fixed rank-two basis, ran three online frozen-fission radial
solves and one axial solve, and used the explicit `Z-RAW-FLUX` carrier. There
was one attempt, no retry and no subsequent map. No relaxation, damping,
clipping, fitted closure or empirical coefficient was introduced.

## Strict validity evidence

The parent-only checker accepted the Z carrier before Dragon started. All
three radial fixed-source terminals then passed strictly:

| plane | `IEXTF` | `EUNK` | `EINR` |
|---:|---:|---:|---:|
| 1 | `2` | `4.66504872e-7` | `3.43577085e-7` |
| 2 | `10` | `4.16723623e-7` | `2.72048851e-7` |
| 3 | `6` | `3.99058592e-7` | `3.36309256e-7` |

The axial terminal also passed strictly:

| quantity | value | limit |
|---|---:|---:|
| outer iterations | `205` | `500` |
| outer error | `2.32599717e-10` | `5.0e-7` |
| unknown error | `4.81816016e-7` | `5.0e-7` |
| terminal inner error | `4.81816016e-7` | `5.0e-7` |

The terminal axial eigenvalue is `1.3624123852358114`; the canonical
REAL32-published value is `1.3624123334884644`. The separate Ganlib-only
checker passed the proposal lifecycle, Z-carrier identity, fixed POD package,
live radial operator, raw radial positivity, canonical layout,
bitwise-recomputed defects and returned archive checks.

The radial and axial logs report 70 and 138 CPU seconds, respectively. The
120-second and 420-second host bounds were operational process limits only.

## Fresh defects

For the unchanged tolerance

\[
\varepsilon=5\times10^{-7},
\]

the independently checked result is

| quantity | value | role | multiple of `epsilon` | passes? |
|---|---:|---|---:|---:|
| \(R_\rho\) | `8.349045215183537e-7` | stopping rule | `1.669809043` | no |
| \(R_L\) | `8.672730944580483e-4` | stopping rule | `1734.546189` | no |
| \(D_L\) (`cm^-1`) | `1.270847860723734e-6` | diagnostic | not applicable | not applicable |
| \(R_a\) | `4.441656115985480e-5` | stopping rule | `88.83312232` | no |

All three stopping components exceed the tolerance, so this valid map is not
a converged state. The global and maximum-group balance diagnostics are
`7.738672e-9` and `1.633527e-3`; they do not enter acceptance.

Relative to the preceding evaluated proposal map \(z=G_2(y_{\rm pub})\), the
new defects have the local ratios

| quantity | new / preceding proposal map |
|---|---:|
| \(R_\rho\) | `0.01269555797` |
| \(R_L\) | `0.3827907385` |
| \(D_L\) | `0.3827933235` |
| \(R_a\) | `0.09521884205` |

Thus every reported component is smaller for this one successive proposal.
These are cross-input ratios, not asymptotic convergence factors, and do not
establish Anderson superiority, stability, rank adequacy or physical
accuracy.

## Reproduction identity

The Git-ignored artifact is
`validation/artifacts/iterative-rank2-modal-aa1-next-map/`. Its 21-entry
checksum receipt passes in full. It was produced from source commit
`e5bb935129238b00e9ed062ecc7d132a95652b98`.

| object | SHA-256 |
|---|---|
| `candidate_system.xsm` | `66673e3cb71e57b443e0af47e0151195c52b8ae7f2f6342bd9095caa098fe577` |
| `candidate_radial.xsm` | `720eb7ab58541eeb512dced1e49edd9e405f5f5037ceff029fdcd6f0f2e7b067` |
| `candidate_axial.xsm` | `02f922cf157a0dde1b9d072f45cdb1e39c64fa1f8682ad3a1e4fe21fede12a62` |
| `candidate_snapshots.xsm` | `ff9b609268405223a045b3c427a29acff9b616aae4cfb611b6b832d2a4c7f8ed` |
| `radial.log` | `810bee36542c4fd43885c08fdc4496e47af15945707e75bed3933c5ffc87da6a` |
| `axial.log` | `65a67c7e7193d8a6abb684e82498732c5a309d0ff446ea26216a27f6bcc9eb55` |
| `parent_preflight.log` | `818d15e93955911638ae2deda01f54f3731b9fde57c1141a5d962ea79af516c9` |
| `independent_check.log` | `d866a4937a819c3ea9215d8d326794de3d2a9f9ccea48ebb7d2dd14830561cb9` |
| `result.sha256` | `5d19edfecabfae1d17d4d796929c5ea7ebd3b8343fc5d3a08f8d142338d50a73` |

The receipt also freezes the exact parent manifest, policy, decks, host,
checker and runtime-library identities. No Dragon process remained after
publication.

## Scientific boundary

This result closes the authorized one-map experiment. It supplies a second
valid rank-two AA(1) response with locally smaller defects, but it does not
meet the stopping rule. It authorizes neither acceptance nor another map. A
possible next step must begin with a separately reviewed, no-Dragon history
update from the two evaluated pairs \(y_{\rm pub}\to z\) and
\(w_{\rm pub}\to v\).
