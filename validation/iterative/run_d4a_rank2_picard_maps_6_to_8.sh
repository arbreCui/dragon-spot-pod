#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../.." && pwd)
RUN_ONE="$HERE/run_d4a_rank2_picard_map.sh"
PARENT="$ROOT/validation/artifacts/iterative-d4a-rank2-picard-map5"

for epoch in 6 7 8
do
  OUTPUT="$ROOT/validation/artifacts/iterative-d4a-rank2-picard-map${epoch}"
  "$RUN_ONE" "$PARENT" "$OUTPUT"
  (
    cd "$OUTPUT"
    shasum -a 256 \
      ../../../bin/Darwin_arm64/Dragon \
      SpotStepR64.c2m radial.x2m axial.x2m checker_parent.x2m \
      ../../iterative/check_one_map_xsm \
      ../../iterative/check_convergence_gate \
      ../../iterative/run_d4a_rank2_picard_map.sh \
      > execution_manifest.sha256
  )
  if grep -q '^CLASSIFICATION=VALID_MET$' "$OUTPUT/gate.log"
  then
    echo "D4A RANK-2 PICARD CONVERGED AT MAP $epoch"
    exit 0
  fi
  PARENT=$OUTPUT
done

echo "D4A RANK-2 PICARD MAPS 6-8 COMPLETE; FINAL GATE NOT MET"
