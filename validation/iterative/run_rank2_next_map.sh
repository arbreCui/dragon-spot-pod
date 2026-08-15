#!/bin/sh
set -eu

RUN_RANK2_NEXT_MAP=${RUN_RANK2_NEXT_MAP:-0}
case "$RUN_RANK2_NEXT_MAP" in
  0)
    echo "SPOT-RANK2-NEXT-MAP DEFAULT-OFF: no Dragon process started."
    exit 0
    ;;
  1) ;;
  *)
    echo "SPOT-RANK2-NEXT-MAP ERROR: RUN_RANK2_NEXT_MAP must be 0 or 1." >&2
    exit 2
    ;;
esac

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)

RUN_CONTINUATION=1 \
PARENT_MANIFEST="$ROOT/validation/iterative/rank2_next_parent.tsv" \
CONTINUATION_POLICY_SOURCE="$ROOT/validation/iterative/rank2_next_map_policy.md" \
RADIAL_DECK_SOURCE="$ROOT/validation/iterative/continuation_rank2_continued_radial.x2m" \
AXIAL_DECK_SOURCE="$ROOT/validation/iterative/continuation_axial.x2m" \
MAP_PARENT_FILE=parent_axial.xsm \
CHECKER_MODE=continued \
RADIAL_TIMEOUT_SECONDS=120 \
AXIAL_TIMEOUT_SECONDS=420 \
  sh "$ROOT/validation/iterative/run_continuation_short.sh"
