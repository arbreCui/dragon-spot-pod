#!/bin/sh
set -eu

# One physical-full-rank REAL64 direct-Picard map from the frozen rank-2
# fixed point, wired end to end:
#   reencode (SPOPHYS basis + same-rank parent) -> B2J projection ->
#   radial response + full-rank ASM -> warm axial FLU with certified
#   SPOXCONV defect -> B2W close -> independent --physical audit.
# Every Dragon execution uses the canonical bounded runner; every product
# is hash-receipted in RESULT_DIR.

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
RESULT_DIR=${RESULT_DIR:-/tmp/full-rank-physical-map}
DRAGON="$ROOT/bin/Darwin_arm64/Dragon"
SEED="$ROOT/validation/artifacts/iterative-seed"
BASIS="$ROOT/validation/artifacts/iterative-rank2-basis"
FIXED="$ROOT/validation/artifacts/iterative-rank2-h2-r64dp2-picard-fixedpoint/fixedpoint-map"
TOOLS="$ROOT/validation/iterative"
WALL=${WALL_LIMIT_SECONDS:-7200}

fail() {
  echo "FULL-RANK PHYSICAL MAP FAIL: $*" >&2
  exit 1
}

test -x "$DRAGON" || fail "canonical Dragon binary is missing"
for tool in close_r64_returned prepare_r64_next_projected check_one_map_xsm
do
  test -x "$TOOLS/$tool" ||
    fail "$tool is not built; run make in validation/iterative"
done

rm -rf "$RESULT_DIR"
mkdir -p "$RESULT_DIR"
cd "$RESULT_DIR"

cp "$SEED/initial_radial_track.bin" .
cp "$SEED/initial_axial_track.xsm" .
cp "$SEED/initial_axial_macrolib.xsm" .
cp "$BASIS/rank2_basis.xsm" basis_pod.xsm
cp "$FIXED/candidate_axial_closed.xsm" parent_axial.xsm
cp "$FIXED/candidate_axial_closed.xsm" parent_axial_closed.xsm
cp "$FIXED/candidate_snapshots_closed.xsm" parent_snapshots_closed.xsm
cp "$FIXED/SpotStepR64.c2m" .
cp "$TOOLS/run_bounded_dragon.py" .
cp "$TOOLS/full_rank_physical_reencode.x2m" .
cp "$TOOLS/full_rank_physical_radial.x2m" .
cp "$TOOLS/full_rank_physical_axial.x2m" .

run_deck() {
  deck=$1
  log=$2
  OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 - "$DRAGON" \
    "$deck" "$log" "$WALL" <<'PYEOF'
import sys
from pathlib import Path
sys.path.insert(0, '.')
import run_bounded_dragon as rbd
rbd.run(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]),
        timeout_seconds=int(sys.argv[4]))
PYEOF
}

echo "== stage 1: reencode the rank-2 parent in the physical basis =="
run_deck full_rank_physical_reencode.x2m reencode.log
rg -q "FULL-RANK-PHYSICAL-REENCODE-COMPLETE" reencode.log ||
  fail "reencode deck did not complete"
test -s basis_physical.xsm || fail "physical basis was not produced"

echo "== stage 2: B2J projection of the reencoded closed parent =="
"$TOOLS/prepare_r64_next_projected" parent_axial_closed.xsm \
  parent_snapshots_closed.xsm initial_axial_track.xsm \
  projected_parent.xsm > prepare.log 2>&1 ||
  { tail -3 prepare.log >&2; fail "projection was refused"; }
rg -q "PROJECT PREPARATION COMPLETE" prepare.log ||
  fail "projection did not complete"

echo "== stage 3: radial response and full-rank assembly =="
run_deck full_rank_physical_radial.x2m radial.log
rg -q "FULL-RANK-PHYSICAL-RADIAL-COMPLETE" radial.log ||
  fail "radial deck did not complete"

echo "== stage 4: warm full-rank axial solve with certified defect =="
run_deck full_rank_physical_axial.x2m axial.log
rg -q "FULL-RANK-PHYSICAL-AXIAL-COMPLETE" axial.log ||
  fail "axial deck did not complete"

echo "== stage 5: B2W close of the returned pair =="
"$TOOLS/close_r64_returned" candidate_axial.xsm candidate_snapshots.xsm \
  closed_axial.xsm closed_snapshots.xsm > close.log 2>&1 ||
  { tail -3 close.log >&2; fail "close was refused"; }
rg -q "CLOSE PASS" close.log || fail "close did not pass"

echo "== stage 6: independent --physical one-map audit =="
"$TOOLS/check_one_map_xsm" --physical basis_physical.xsm \
  candidate_system.xsm parent_axial.xsm candidate_axial.xsm \
  candidate_snapshots.xsm > independent_check.log 2>&1 ||
  { tail -5 independent_check.log >&2; fail "independent audit failed"; }

grep -E ">\|FULL-RANK-PHYSICAL-(RAW-DEFECT|CANDIDATE|LEAKAGE)" axial.log \
  > defect_receipt.txt || true
shasum -a 256 "$DRAGON" > dragon_executable.sha256
find . -maxdepth 1 -type f ! -name result.sha256 \
  -exec shasum -a 256 {} \; | sort -k2 > result.sha256

echo "FULL-RANK PHYSICAL MAP PASS"
cat defect_receipt.txt
