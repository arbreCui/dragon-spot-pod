# Bounded map attempt from the latest modal AA(1) history proposal

Date: 2026-08-16

Classification: `INVALID_MAP`.

Reported reason: `TIMEOUT_BEFORE_TERMINAL`.

Scientific result: `NONE`.

## Frozen attempt

The separately authorized experiment attempted exactly one unchanged
fixed-rank map

$$
Q(t)^+=G_2(Q(t)),\qquad
t=0.223333969605448268x_4+0.776666030394551732z.
$$

The source tree and remote branch were frozen at commit
`da7f02ac9826ee6da04614486a9fa74c41a02729`. The parent proposal hashes
were:

| parent | SHA-256 |
|---|---|
| proposal AX | `e9e37246df25ef9afb449fad77e55b6ce21cd03f09e2f185d458aea4bd85d28c` |
| proposal snapshots | `8414fb2298bcd9797f5d1b0613d985413c7c87d533feb80e8f24360471c05b38` |

The nine-entry proposal receipt, all six map-parent hashes, and the strict
`PROPOSAL + Z-RAW-FLUX` Ganlib preflight passed before Dragon. The physical
rank, basis, normalization, decks, equations, and $5\times10^{-7}$ inner and
outer tolerances were unchanged. The radial wall bound was 120 seconds and
the axial wall bound was 80 seconds. These were process-safety bounds, not
physical or convergence parameters. There was one attempt and no retry.

## Completed radial stage

All three online frozen-fission radial solves reached the unchanged strict
terminal contract:

| plane | `IEXTF` | `EUNK` | `EINR` |
|---|---:|---:|---:|
| 1 | `4` | `2.02972799e-7` | `2.21422908e-7` |
| 2 | `21` | `4.03853818e-7` | `3.11236846e-7` |
| 3 | `6` | `3.91597467e-7` | `3.45966384e-7` |

The radial log contains exactly three outer PASS terminals, three inner
terminals, one `CONT-RADIAL-COMPLETE`, and one normal Dragon end. It reports
87 seconds of CPU time. The final radial contract record is

$$
(\mathrm{FIXB},\mathrm{FSN},\mathrm{RBAL},Q_{L2},Q_{\max})=
(1,3,3.9166317794\times10^{-7},
2.2412600644\times10^{-7},2.6345974681\times10^{-7}).
$$

These facts validate only the temporary radial stage; they do not constitute
a complete map or a successor state.

## Axial timeout

The axial log records `CONT-AXIAL-BEGIN`, the unchanged tolerance, and entry
into `FLU`. The bounded host terminated the process group after 80 seconds
with

```text
RAW-MOC-CAPTURE PROCESS FAIL: timeout after 80 seconds; no scientific result
SPOT-CONTINUATION INVALID_MAP: no candidate was published.
```

The partial log contains none of the required axial evidence:

- no `FLU2DR` strict terminal;
- no normal Dragon end;
- no `SPOGBAL`, `SPOSTATE`, or `SPOXCONV` result;
- no `CONT-RAW-DEFECT`, `CONT-CANDIDATE`, or
  `CONT-AXIAL-COMPLETE`;
- no `candidate_axial.xsm`, `candidate_snapshots.xsm`, independent check, or
  classification publication.

The formal result directory and lock are absent. A post-exit process census
found zero SPOT/Dragon processes. The parent hashes remained unchanged.
Temporary `candidate_system.xsm` and `candidate_radial.xsm` objects are
unpublished radial staging only and were not retained in the attempt
artifact.

## No stopping result

Because the axial solve never produced a strict terminal, the returned
$k^+$, $\rho^+$, $A^+$, and $L^+$ do not exist. Consequently none of
$R_\rho$, $R_L$, $D_L$, or $R_a$ exists, and the three-component AND gate
was not evaluated. This result is neither `VALID_NOT_MET` nor
`TOLERANCE_MET`.

The timeout shows only that the axial solve did not reach and publish its
strict terminal within the predeclared 80-second process bound. It is not
evidence of mathematical or physical nonconvergence.

## Frozen evidence

The separate Git-ignored attempt artifact is
`validation/artifacts/iterative-rank2-latest-modal-aa1-next-map-attempt/`.
It contains 11 regular files and no symbolic links. Its ten-entry receipt
passes 10/10; the receipt-file SHA-256 is
`96f9bc1eacba30a629f35feceb2177d77e3f0bba4ff9ddaaaa03ecb66e5205c3`.

| evidence | SHA-256 |
|---|---|
| `radial.log` | `a858af79fb0c97a9691d2d91056a0d613e1b28873e1793bb19e0078724c06cb5` |
| partial `axial.log` | `79c14be3a810f7d4e7e9cd33ffc1b0dbd829f8a4923cf0d1768eb70d6a4b1aaa` |
| `parent_preflight.log` | `818d15e93955911638ae2deda01f54f3731b9fde57c1141a5d962ea79af516c9` |
| `map_configuration.tsv` | `b406a8cdcd7f3dc18da3aebbaf252a60de1b9d4a6ccdebe3a503f59760d8f6eb` |

`attempt_host_observation.txt` explicitly labels its terminal block as a
host transcription because the interactive wrapper stream was not
redirected to a raw file. The Dragon-generated radial and partial axial logs
are retained verbatim.

## Scientific boundary

The complete $G_2(Q(t))$ map was not obtained. This attempt supplies no
fresh fixed-point defects and no evidence for convergence, divergence,
stability, contraction, convergence order, AA(1) superiority, rank
adequacy, or physical accuracy. The one-attempt authorization is consumed;
no retry or successor map was started.
