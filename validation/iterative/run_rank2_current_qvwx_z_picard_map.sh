#!/bin/sh
set -eu

RUN_RANK2_CURRENT_QVWX_Z_PICARD_MAP=${RUN_RANK2_CURRENT_QVWX_Z_PICARD_MAP:-0}
case "$RUN_RANK2_CURRENT_QVWX_Z_PICARD_MAP" in
  0)
    echo "SPOT-RANK2-CURRENT-QVWX-Z-PICARD-MAP DEFAULT-OFF: no Dragon process started."
    exit 0
    ;;
  1) ;;
  *)
    echo "SPOT-RANK2-CURRENT-QVWX-Z-PICARD-MAP ERROR: activation must be 0 or 1." >&2
    exit 2
    ;;
esac

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
PARENT_DIR="$ROOT/validation/artifacts/iterative-rank2-current-qvwx-aa1-map"

test -d "$PARENT_DIR" && test ! -L "$PARENT_DIR"
test "$(sed -n '1p' "$PARENT_DIR/classification.txt")" = 'VALID_NOT_MET'
test "$(awk 'END {print NR}' "$PARENT_DIR/result.sha256")" = 21
(
  cd "$PARENT_DIR"
  shasum -a 256 -c result.sha256 >/dev/null
)

RUN_CONTINUATION=1 \
RESULT_DIR="$ROOT/validation/artifacts/iterative-rank2-current-qvwx-z-picard-map" \
PARENT_MANIFEST="$ROOT/validation/iterative/rank2_current_qvwx_z_picard_map_parent.tsv" \
CONTINUATION_POLICY_SOURCE="$ROOT/validation/iterative/rank2_current_qvwx_z_picard_map_policy.md" \
RADIAL_DECK_SOURCE="$ROOT/validation/iterative/continuation_rank2_continued_radial.x2m" \
AXIAL_DECK_SOURCE="$ROOT/validation/iterative/continuation_axial.x2m" \
MAP_PARENT_FILE=parent_axial.xsm \
CHECKER_MODE=continued \
RADIAL_TIMEOUT_SECONDS=120 \
AXIAL_TIMEOUT_SECONDS=180 \
  sh "$ROOT/validation/iterative/run_continuation_short.sh"
