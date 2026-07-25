# Stage-4 v2: attainable tolerance sensitivity

The original Stage-4 experiment remains
`INVALID-INNER-NONCONVERGENCE`. All three online radial fixed-source
solves reached `MAXOUT=500` at
\(h/2=\mathtt{0x348637bd}\), so no valid \(G_{h/2}(x_0)\) exists.
Nothing in this amendment reuses or reclassifies those returned states.

The failed condition is evaluated in `FLU2DR`, whose eight stored
iteration fields, source construction, acceleration, balance and
`DOORFV` interface are binary32. A genuinely continuous REAL64 lane
would therefore have to begin at `FLU2DR` and propagate through the
complete radial solver. Changing only `MCGFCS`, `MCGMRE` or `MCGFLX`
would round back to binary32 inside every thermal update and would not
test the failed numerical boundary. That large solver fork is outside
the simple SPOD validation route.

The replacement is one predeclared, attainable factor-two comparison:

\[
x_{1,2h}=G_{2h}(x_0),\qquad
x_{1,h}=G_h(x_0),
\]

with

\[
2h=\mathtt{0x358637bd},\qquad
h=\mathtt{0x350637bd}.
\]

Binary32 arithmetic satisfies
\(\tfrac12(2h)=h\) exactly. The already released and replayed \(h\)
map is the fine lane. Only one \(2h\) candidate definition is permitted,
from the same frozen \(x_0\), basis, source identity and physical inputs.
It may be executed once for capture and once for the required fresh replay.

For

\[
\mathcal D_{\rm in}=\mathcal D(x_{1,h},x_{1,2h}),
\]

each of \(R_\rho,R_L,D_L,R_a\) is compared separately with the
corresponding coarse outer defect
\(\mathcal D_{\rm out,2h}=\mathcal D(x_{1,2h},x_0)\). A positive
component is resolved only when

\[
D_{{\rm in},i}<D_{{\rm out},2h,i}.
\]

If the coarse outer component is exactly zero, the corresponding
inner component must also be exactly zero. There is no scalar score,
cross-component weight, fitted factor or relaxation coefficient.

Every coarse radial solve and the returned axial solve must terminate
strictly. Input identity, source identity, positivity, balance,
Galerkin residual and independent replay remain mandatory. A first
valid result is only `PENDING-REPLAY`; a fresh byte-identical replay is
required for `QUALIFIED-ON-2H-TO-H-SCALE`.

Qualification means only that the map is stable over the tested
attainable interval \([h,2h]\). It is not an asymptotic order, an error
bound, a REAL64 result or an \(h/2\) qualification.

The complete machine-readable freeze is in
`inner_sensitivity_v2_protocol.json`. This protocol-only freeze authorizes
no Dragon process and no long trajectory. A later implementation freeze may
authorize at most one bounded capture process; only a valid
`PENDING-REPLAY` capture may authorize one separately invoked replay.
