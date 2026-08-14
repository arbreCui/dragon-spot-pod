#!/bin/sh
set -eu

RUN_RANK2_MAP=${RUN_RANK2_MAP:-0}
case "$RUN_RANK2_MAP" in
  0)
    echo "SPOT-RANK2-MAP DEFAULT-OFF: no Dragon process started."
    exit 0
    ;;
  1) ;;
  *)
    echo "SPOT-RANK2-MAP ERROR: RUN_RANK2_MAP must be 0 or 1." >&2
    exit 2
    ;;
esac

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)

RUN_CONTINUATION=1 \
PARENT_MANIFEST="$ROOT/validation/iterative/rank2_parent.tsv" \
CONTINUATION_POLICY_SOURCE="$ROOT/validation/iterative/rank2_map_policy.md" \
RADIAL_DECK_SOURCE="$ROOT/validation/iterative/continuation_rank2_radial.x2m" \
AXIAL_DECK_SOURCE="$ROOT/validation/iterative/continuation_rank2_axial.x2m" \
MAP_PARENT_FILE=rank2_parent_axial.xsm \
CHECKER_MODE=reencoded \
  sh "$ROOT/validation/iterative/run_continuation_short.sh"
