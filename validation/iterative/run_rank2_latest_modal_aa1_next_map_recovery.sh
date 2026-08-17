#!/bin/sh
set -eu

RUN_RANK2_LATEST_MODAL_AA1_NEXT_MAP_RECOVERY=${RUN_RANK2_LATEST_MODAL_AA1_NEXT_MAP_RECOVERY:-0}
case "$RUN_RANK2_LATEST_MODAL_AA1_NEXT_MAP_RECOVERY" in
  0)
    echo "SPOT-RANK2-LATEST-MODAL-AA1-NEXT-MAP-RECOVERY DEFAULT-OFF: no Dragon process started."
    exit 0
    ;;
  1) ;;
  *)
    echo "SPOT-RANK2-LATEST-MODAL-AA1-NEXT-MAP-RECOVERY ERROR: activation must be 0 or 1." >&2
    exit 2
    ;;
esac

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
PROPOSAL_DIR="$ROOT/validation/artifacts/iterative-rank2-latest-modal-aa1-next-candidate"
ATTEMPT_DIR="$ROOT/validation/artifacts/iterative-rank2-latest-modal-aa1-next-map-attempt"
OLD_RESULT_DIR="$ROOT/validation/artifacts/iterative-rank2-latest-modal-aa1-next-map"

test -d "$PROPOSAL_DIR" && test ! -L "$PROPOSAL_DIR"
test "$(sed -n '1p' "$PROPOSAL_DIR/classification.txt")" = \
  'MATERIALIZED_PROPOSAL_NOT_EVALUATED'
test "$(awk 'END {print NR}' "$PROPOSAL_DIR/result.sha256")" = 9
(
  cd "$PROPOSAL_DIR"
  shasum -a 256 -c result.sha256 >/dev/null
)

test -d "$ATTEMPT_DIR" && test ! -L "$ATTEMPT_DIR"
test "$(find "$ATTEMPT_DIR" -mindepth 1 -maxdepth 1 -type f | wc -l | tr -d ' ')" = 11
test "$(find "$ATTEMPT_DIR" -mindepth 1 -maxdepth 1 -type l | wc -l | tr -d ' ')" = 0
test "$(sed -n '1p' "$ATTEMPT_DIR/classification.txt")" = 'INVALID_MAP'
test "$(sed -n '1p' "$ATTEMPT_DIR/reason.txt")" = \
  'TIMEOUT_BEFORE_TERMINAL'
test "$(awk 'END {print NR}' "$ATTEMPT_DIR/result.sha256")" = 10
test "$(shasum -a 256 "$ATTEMPT_DIR/result.sha256" | awk '{print $1}')" = \
  '96f9bc1eacba30a629f35feceb2177d77e3f0bba4ff9ddaaaa03ecb66e5205c3'
(
  cd "$ATTEMPT_DIR"
  shasum -a 256 -c result.sha256 >/dev/null
)
test ! -e "$OLD_RESULT_DIR" && test ! -L "$OLD_RESULT_DIR"

RUN_CONTINUATION=1 \
RESULT_DIR="$ROOT/validation/artifacts/iterative-rank2-latest-modal-aa1-next-map-recovery" \
PARENT_MANIFEST="$ROOT/validation/iterative/rank2_latest_modal_aa1_next_map_parent.tsv" \
CONTINUATION_POLICY_SOURCE="$ROOT/validation/iterative/rank2_latest_modal_aa1_next_map_recovery_policy.md" \
RADIAL_DECK_SOURCE="$ROOT/validation/iterative/continuation_rank2_continued_radial.x2m" \
AXIAL_DECK_SOURCE="$ROOT/validation/iterative/continuation_axial.x2m" \
MAP_PARENT_FILE=parent_axial.xsm \
CHECKER_MODE=proposal-z \
RADIAL_TIMEOUT_SECONDS=120 \
AXIAL_TIMEOUT_SECONDS=420 \
  sh "$ROOT/validation/iterative/run_continuation_short.sh"
