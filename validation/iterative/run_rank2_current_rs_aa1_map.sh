#!/bin/sh
set -eu

RUN_RANK2_CURRENT_RS_AA1_MAP=${RUN_RANK2_CURRENT_RS_AA1_MAP:-0}
case "$RUN_RANK2_CURRENT_RS_AA1_MAP" in
  0)
    echo "SPOT-RANK2-CURRENT-RS-AA1-MAP DEFAULT-OFF: no Dragon process started."
    exit 0
    ;;
  1) ;;
  *)
    echo "SPOT-RANK2-CURRENT-RS-AA1-MAP ERROR: activation must be 0 or 1." >&2
    exit 2
    ;;
esac

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
PROPOSAL_DIR="$ROOT/validation/artifacts/iterative-rank2-current-rs-aa1-candidate"

test -d "$PROPOSAL_DIR" && test ! -L "$PROPOSAL_DIR"
test "$(sed -n '1p' "$PROPOSAL_DIR/classification.txt")" = \
  'MATERIALIZED_PROPOSAL_NOT_EVALUATED'
test "$(awk 'END {print NR}' "$PROPOSAL_DIR/result.sha256")" = 9
(
  cd "$PROPOSAL_DIR"
  shasum -a 256 -c result.sha256 >/dev/null
)

RUN_CONTINUATION=1 \
RESULT_DIR="$ROOT/validation/artifacts/iterative-rank2-current-rs-aa1-map" \
PARENT_MANIFEST="$ROOT/validation/iterative/rank2_current_rs_aa1_map_parent.tsv" \
CONTINUATION_POLICY_SOURCE="$ROOT/validation/iterative/rank2_current_rs_aa1_map_policy.md" \
RADIAL_DECK_SOURCE="$ROOT/validation/iterative/continuation_rank2_continued_radial.x2m" \
AXIAL_DECK_SOURCE="$ROOT/validation/iterative/continuation_axial.x2m" \
MAP_PARENT_FILE=parent_axial.xsm \
CHECKER_MODE=proposal-aa1 \
RADIAL_TIMEOUT_SECONDS=120 \
AXIAL_TIMEOUT_SECONDS=180 \
  sh "$ROOT/validation/iterative/run_continuation_short.sh"
