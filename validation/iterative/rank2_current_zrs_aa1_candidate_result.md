# Latest-return standard AA(1) proposal

Date: 2026-08-17

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

The latest two genuine consecutive maps are

\[
z\mapsto r,\qquad r\mapsto s.
\]

Standard unregularized full-Gram AA(1), using only the residuals $r-z$ and
$s-r$, gives

\[
p=0.80686776173198704\,r+0.19313223826801298\,s.
\]

The denominator is `9.0242922572112097e-12`, finite and strictly positive
without a cutoff.  Relative to the current residual $s-r$, the modal,
leakage height-$L_2$, and leakage $D_L$ same-weight direction ratios are
`0.055106927228035521`, `0.79919414157585233`, and
`0.78792709968370800`.  All three are strictly below one, so AA(1) passes
the fixed parameter-free direction screen.  By the predeclared
minimum-order rule, AA(2) is not formed or searched.

The affine inverse eigenvalue is `0.73399300344327834`; publication gives
$k=1.3624107837677002$ and reciprocal
$\rho=0.73399301584690513$.  Leakage is published through the production
REAL32 round trip, whose maximum change is
`5.6959793652555657e-11`.  All 8880 reconstructed publication points are
strictly positive; the minimum is `1.7533958937825545e-15`.

The same two affine weights act explicitly on $(a,\rho,L)$; only afterward
are the existing REAL32 eigenvalue and leakage publication rules applied.

The latest returned $s$ AX/raw-flux and snapshot archives are the complete
carriers.  The internal `X4-RAW-FLUX` name is the existing carrier-protocol
marker; hashes and the bitwise checker bind its payload to $s$.  Only the
declared $(a,\rho,L)$ proposal fields and their
publication identities are replaced; raw fields are not affine-mixed.  The
independent Ganlib checker reproduced the coefficient, three direction
ratios, publication arithmetic, fixed rank-two bundle, raw carrier,
snapshot lifecycle, lagged `SYSTEM`, and positivity.

The artifact contains 10 regular files, no symbolic links, and a passing
9/9 receipt.

| output | SHA-256 |
|---|---|
| proposal AX | `d00a310cffb832cfec6ef2bdaa6cf27cfd51443904afd8d26ca57418e140d225` |
| proposal snapshots | `1e1ed5556c464ae319784ecab8ee408decba7392c419d45de796ab396f82d72d` |
| build log | `596463e5edeb58d28f7f631ad48f2a6c41bf59ffff2ae5256559e7b68a649a5e` |
| independent-check log | `251c002fb076621898c76f9f90e578bf6468d320d0b608debdec497374292389` |
| receipt | `573d7b6377c29bbd98303de9197597ed5b9905cf65ae717fb118ce6c335b9c45` |

This offline stage used no Dragon, radial solve, axial solve, transport map,
relaxation, damping, clipping, regularization, fitted coefficient, or
empirical parameter.  The three direction ratios are authorization
diagnostics, not new raw stopping defects and not a convergence result.
Exactly one fresh physical map is required before the original AND gate can
accept or reject the proposal.
