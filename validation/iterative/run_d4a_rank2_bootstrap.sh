#!/bin/sh
set -eu

# Build the initial D4-A CLOSED/0 pair from one admitted corrected-material
# snapshot directory.  This composes existing physical operators only:
# axial TYPE-K seed -> three radial TYPE-S responses -> B2I seal.

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TOOLS="$ROOT/validation/iterative"
DRAGON_BIN=${DRAGON_BIN:-"$ROOT/bin/Darwin_arm64/Dragon"}
AXIAL_TIMEOUT_SECONDS=${AXIAL_TIMEOUT_SECONDS:-900}
: "${RADIAL_TIMEOUT_SECONDS:?set an explicit bounded wall time for the three D4-A TYPE-S solves}"
EXPECTED_TRACK_SHA=d2bcd5c078e7b66772f44963039eb0505300e4d51d4661125823f6037d2d51d7

fail() {
  echo "D4A RANK2 BOOTSTRAP FAIL: $*" >&2
  exit 1
}

test -n "${RESULT_DIR:-}" || fail "set RESULT_DIR to the admitted rank-2 build"
case "$RESULT_DIR" in
  /*) ;;
  *) fail "RESULT_DIR must be an absolute path" ;;
esac
test -d "$RESULT_DIR" || fail "RESULT_DIR does not exist"
test -x "$DRAGON_BIN" || fail "Dragon executable is missing"

for input in d4a_snapshots.xsm admitted_snapshot_archive.sha256 \
  d4a_rank2_basis.xsm d4a_axial_track.xsm d4a_axial_macrolib.xsm \
  d4a_rank2_admitted.sha256 TRACK_f
do
  test -s "$RESULT_DIR/$input" || fail "$input is missing or empty"
done
test "$(sha256sum "$RESULT_DIR/TRACK_f" | awk '{print $1}')" = \
  "$EXPECTED_TRACK_SHA" || fail "radial tracking hash changed"

for output in d4a_seed_axial.xsm d4a_seed_snapshots.xsm \
  initial_radial_track.bin initial_axial_track.xsm \
  initial_axial_macrolib.xsm basis_reference.xsm route_contract.xsm \
  d4a_refreshed_snapshots.xsm closed_axial.xsm closed_snapshots.xsm \
  d4a_refresh_r64.log d4a_bootstrap_result.sha256
do
  test ! -e "$RESULT_DIR/$output" || fail "refusing to overwrite $output"
done

make -C "$ROOT/src" -j2 >/dev/null
make -C "$TOOLS" -j2 >/dev/null

cp "$RESULT_DIR/TRACK_f" "$RESULT_DIR/initial_radial_track.bin"
cp "$RESULT_DIR/d4a_axial_track.xsm" "$RESULT_DIR/initial_axial_track.xsm"
cp "$RESULT_DIR/d4a_axial_macrolib.xsm" \
  "$RESULT_DIR/initial_axial_macrolib.xsm"
cp "$RESULT_DIR/d4a_rank2_basis.xsm" "$RESULT_DIR/basis_reference.xsm"

(
  cd "$RESULT_DIR"
  "$TOOLS/make_route_contract" route_contract.xsm D4A-1RING \
    2e-6 2e-6 2e-6 500 740 3 3 B0 > route_contract.log
)

RESULT_DIR="$RESULT_DIR" TIMEOUT_SECONDS="$AXIAL_TIMEOUT_SECONDS" \
  sh "$TOOLS/run_d4a_axial_seed.sh"

cp "$ROOT/data/SpotRefR64.c2m" "$RESULT_DIR/SpotRefR64.c2m"
cp "$ROOT/data/SpotPlaneR64.c2m" "$RESULT_DIR/SpotPlaneR64.c2m"
cp "$TOOLS/d4a_refresh_r64.x2m" "$RESULT_DIR/d4a_refresh_r64.x2m"

OMP_NUM_THREADS=1
export OMP_NUM_THREADS
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$TOOLS" \
  python3 -c \
  'import sys; from pathlib import Path; from run_bounded_dragon import run; run(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), float(sys.argv[4]))' \
  "$DRAGON_BIN" "$RESULT_DIR/d4a_refresh_r64.x2m" \
  "$RESULT_DIR/d4a_refresh_r64.log" "$RADIAL_TIMEOUT_SECONDS"

LOG="$RESULT_DIR/d4a_refresh_r64.log"
test "$(rg -c '^>\|SPOT-REFRESH-R64-RESULT' "$LOG")" = 3 ||
  fail "did not complete exactly three TYPE-S plane responses"
rg -q '^>\|D4A-R64-REFRESH-COMPLETE' "$LOG" ||
  fail "TYPE-S bridge did not complete"
rg -q 'normal end of execution for dragon' "$LOG" ||
  fail "TYPE-S bridge has no normal Dragon terminal"
if rg -i \
  'CONVERGENCE NOT REACHED|XABORT|ABORT:|FATAL|SIG(SEGV|FPE|BUS|ILL|ABRT)|fortran runtime error' \
  "$LOG" >/dev/null
then
  fail "TYPE-S bridge log contains an abnormal terminal"
fi

(
  cd "$RESULT_DIR"
  "$TOOLS/b2i_seal_bootstrap" d4a_seed_axial.xsm \
    initial_axial_track.xsm d4a_refreshed_snapshots.xsm \
    route_contract.xsm closed_axial.xsm closed_snapshots.xsm \
    > b2i_bootstrap.log
  rg -q '^SPOT-R64 B2I BOOTSTRAP COMMITTED CLOSED/0$' b2i_bootstrap.log ||
    fail "B2I did not commit CLOSED/0"
  sha256sum -c admitted_snapshot_archive.sha256 >/dev/null
  sha256sum -c d4a_rank2_admitted.sha256 >/dev/null
  sha256sum d4a_seed_axial.xsm d4a_seed_snapshots.xsm \
    initial_radial_track.bin initial_axial_track.xsm \
    initial_axial_macrolib.xsm basis_reference.xsm route_contract.xsm \
    d4a_refreshed_snapshots.xsm closed_axial.xsm closed_snapshots.xsm \
    d4a_axial_seed.log d4a_refresh_r64.log route_contract.log \
    b2i_bootstrap.log > d4a_bootstrap_result.sha256
)

echo "D4A RANK2 BOOTSTRAP PASS: CLOSED/0"
