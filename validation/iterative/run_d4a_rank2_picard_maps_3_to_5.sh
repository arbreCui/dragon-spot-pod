#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../.." && pwd)
RUN_ONE="$HERE/run_d4a_rank2_picard_map.sh"
PARENT="$ROOT/validation/artifacts/iterative-d4a-rank2-picard-map2-attempt2"

for epoch in 3 4 5
do
  OUTPUT="$ROOT/validation/artifacts/iterative-d4a-rank2-picard-map${epoch}"
  "$RUN_ONE" "$PARENT" "$OUTPUT"
  if grep -q '^CLASSIFICATION=VALID_MET$' "$OUTPUT/gate.log"
  then
    echo "D4A RANK-2 PICARD CONVERGED AT MAP $epoch"
    exit 0
  fi
  PARENT=$OUTPUT
done

echo "D4A RANK-2 PICARD MAPS 3-5 COMPLETE; FINAL GATE NOT MET"
