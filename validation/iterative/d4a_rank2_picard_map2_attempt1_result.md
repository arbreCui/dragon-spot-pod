# D4-A rank-2 Picard map 2, attempt 1

This attempt has no scientific result. Plane 1 and plane 2 completed their
strict fixed-source solves, but the supervising foreground task disappeared
during the third solve of plane 3. The liveness watchdog correctly terminated
the Dragon process. No `candidate_radial.xsm` was published, so no partial
state is admitted or reused.

The interruption is operational, not evidence about physical convergence.
The next run uses the identical basis, operators, route contract, tolerances,
and direct Picard update (`alpha = 1`). Only the external process time cap is
raised from 21600 to 25200 seconds to leave non-physical scheduling margin.
