#!/bin/sh
set -eu

RUN_RANK2_MODAL_AA1_U_MAP=${RUN_RANK2_MODAL_AA1_U_MAP:-0}
case "$RUN_RANK2_MODAL_AA1_U_MAP" in
  0)
    echo "SPOT-RANK2-MODAL-AA1-U-MAP DEFAULT-OFF: no Dragon process started."
    exit 0
    ;;
  1) ;;
  *)
    echo "SPOT-RANK2-MODAL-AA1-U-MAP ERROR: activation must be 0 or 1." >&2
    exit 2
    ;;
esac

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
PROPOSAL_DIR="$ROOT/validation/artifacts/iterative-rank2-modal-aa1-u-candidate"
test -d "$PROPOSAL_DIR" && test ! -L "$PROPOSAL_DIR"
test "$(sed -n '1p' "$PROPOSAL_DIR/classification.txt")" = \
  'MATERIALIZED_PROPOSAL_NOT_EVALUATED'
(
  cd "$PROPOSAL_DIR"
  shasum -a 256 -c result.sha256 >/dev/null
)

RUN_CONTINUATION=1 \
PARENT_MANIFEST="$ROOT/validation/iterative/rank2_modal_aa1_u_map_parent.tsv" \
CONTINUATION_POLICY_SOURCE="$ROOT/validation/iterative/rank2_modal_aa1_u_map_policy.md" \
RADIAL_DECK_SOURCE="$ROOT/validation/iterative/continuation_rank2_continued_radial.x2m" \
AXIAL_DECK_SOURCE="$ROOT/validation/iterative/continuation_axial.x2m" \
MAP_PARENT_FILE=parent_axial.xsm \
CHECKER_MODE=proposal-v \
RADIAL_TIMEOUT_SECONDS=120 \
AXIAL_TIMEOUT_SECONDS=420 \
  sh "$ROOT/validation/iterative/run_continuation_short.sh"
