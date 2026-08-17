# Separately authorized recovery map from the latest modal AA(1) proposal

Date: 2026-08-16

Status: `PREPARED_NOT_RUN`.

The earlier, separately frozen 80-second attempt remains
`INVALID_MAP / TIMEOUT_BEFORE_TERMINAL / Scientific result NONE`. This new
default-off stage is authorized to evaluate exactly once the same unchanged
fixed-rank map

$$
Q(t)^+=G_2(Q(t)),\qquad
t=0.223333969605448268x_4+0.776666030394551732z.
$$

The parent AX and snapshot hashes, standard modal AA(1) coefficient,
published `(A,rho,L)`, complete `Z-RAW-FLUX` carrier, rank two, fixed basis,
normalization, radial and axial decks, equations, strict solver tolerances,
and original three-component stopping gate are unchanged. No intermediate
from the invalid attempt is reused; the full radial and axial chain starts
again from the hash-locked proposal.

The only operational difference from the invalid attempt is restoration of
the project's already exercised axial process cap:

- radial process cap: 120 seconds;
- axial process cap: 420 seconds.

These are external process-safety bounds. They do not enter Dragon, the
physical equations, the AA(1) formula, or the convergence criteria. The
420-second value is a historically successful cap, not an estimated runtime,
a fitted parameter, a minimum safe bound, or a completion guarantee.

Before Dragon, the wrapper must verify the nine-entry proposal receipt, the
ten-entry invalid-attempt receipt and its frozen SHA-256, the prior
classification and reason, absence of a prior formal result, and all six
map-parent hashes. The strict `PROPOSAL + Z-RAW-FLUX` preflight must then
pass. A mismatch publishes nothing.

Activation permits one attempt in this new stage. There is no loop, automatic
retry, fallback, relaxation, damping, clipping, fitted closure, empirical
coefficient, or automatic successor.

Only three classifications are allowed:

- `INVALID_MAP`: a provenance gate, strict solve terminal, normal end,
  physical check, independent audit, timeout, or receipt fails; no valid
  candidate is published.
- `TOLERANCE_MET`: the complete map is valid and $R_\rho$, $R_L$, and $R_a$
  all satisfy the unchanged $5\times10^{-7}$ AND gate.
- `VALID_NOT_MET`: the complete map is valid but at least one stopping
  component exceeds the unchanged tolerance.

Even a valid result establishes only the stopping status of this one
fixed-rank-two discrete map evaluation. It does not establish asymptotic
convergence, stability, contraction, convergence order, AA(1) superiority,
rank adequacy, or physical accuracy. A timeout remains an operational
failure, not proof of physical nonconvergence.
