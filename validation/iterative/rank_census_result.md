# Frozen snapshot rank census

## Scope and input

This is a read-only, no-transport census of the snapshot set that built the
frozen rank-1 SPOT basis. The sole input is

`validation/artifacts/iterative-map1/basis_reference.xsm`

with SHA-256

`dc65467731947901393f9fb7114b7cd2e956a9992bb97db18e665b47e7446504`.

The 800,220-byte object is the `basis_reference` locked by
[current_parent.tsv](current_parent.tsv). It contains all three REAL64
singular values for each of 370 energy groups, even though it retains only
one spatial basis vector. Therefore this census does not read the 218 MiB raw
snapshot archive and does not reconstruct or invent a second mode.
The XSM object remains local and Git-ignored; a fresh clone needs a copy that
matches the recorded hash. The committed checker and result do not replace
that source artifact.

With the local hash-locked object present, run it with:

```sh
make spot-rank-census
```

The runner copies the hash-locked object, compiles a Ganlib-only checker and
opens the copy read-only. It neither links nor starts Dragon.

## Per-group quantities

Production `SPOPOD` normalizes each of the three radial snapshots by its
volume-weighted mean and applies the SVD to the volume-weighted snapshot
matrix. For each energy group $g$, the optimal snapshot-set reconstruction
error at rank $r$ is therefore

$$
e_{r,g}=
\sqrt{
\frac{\sum_{j>r}\sigma_{j,g}^2}
     {\sum_{j=1}^{3}\sigma_{j,g}^2}
},
$$

and its captured fraction is $1-e_{r,g}^2$. These are dimensionless
within-group quantities. No cross-energy-group score or acceptance threshold
is defined.

## Result

All 370 groups have production numerical snapshot rank 3. The descriptive
rank-1 and rank-2 errors are:

| retained rank | minimum $e_{r,g}$ | median $e_{r,g}$ | maximum $e_{r,g}$ | worst group | minimum captured fraction |
|---:|---:|---:|---:|---:|---:|
| 1 | 5.621065089993577e-8 | 4.541360836235422e-5 | 1.500397382849577e-2 | 251 | 9.997748807693538e-1 |
| 2 | 6.577286811389827e-9 | 1.050484534235874e-7 | 3.408482963639734e-4 | 241 | 9.999998838224389e-1 |

The worst rank-1 spectrum, in group 251, is

$$
(\sigma_1,\sigma_2,\sigma_3)=
(1.970896465734787,
 2.957435314406866\times10^{-2},
 1.227984452285345\times10^{-4}).
$$

The worst rank-2 spectrum, in group 241, is

$$
(\sigma_1,\sigma_2,\sigma_3)=
(1.752660020063699,
 1.979552173124150\times10^{-2},
 5.974293191510079\times10^{-4}).
$$

The spectral rank-1 formula agrees with the stored production rank-1
reconstruction diagnostic to a maximum absolute difference of
$2.801770664062835\times10^{-8}$, at group 39. The stored diagnostic also
contains the REAL32 basis and coefficient reconstruction effects, so this
difference is reported rather than forced to zero.

## Scientific decision

Classification: `DIAGNOSTIC_ONLY`.

Rank 1 is not a uniformly exact representation of its own frozen snapshot
set: the worst optimal within-group error is about 1.50%. Rank 2 reduces the
largest spectral tail to about 0.0341%, but all groups still have numerical
rank 3.

This does not prove that rank 1 caused the failed Picard census, that rank 2
will converge, or that either rank is accurate against a reference solution.
It also does not authorize changing the active fixed basis. A rank-2 study
would first have to reconstruct the second mode from the same original
frozen snapshots and validate that package without transport; qualification
would still require a reproducible fixed point and declared physical
observables.
