#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
DRAGON_BIN=${DRAGON_BIN:-"$ROOT/bin/Darwin_arm64/Dragon"}
DLIB370=${DLIB370:-/Users/wen/dragon-5.1/Dragon/irena_colorset_assembly_pin/pincell/DLIB_370}
RUN_D4A_SNAPSHOTS=${RUN_D4A_SNAPSHOTS:-0}

DLIB370="$DLIB370" sh "$ROOT/validation/iterative/preflight_d4a_three_snapshots.sh"

if [ "$RUN_D4A_SNAPSHOTS" != 1 ]; then
  echo "D4A SNAPSHOT BUILD DISABLED: set RUN_D4A_SNAPSHOTS=1 and an unused RESULT_DIR"
  exit 0
fi

test -x "$DRAGON_BIN"
test -f "$DLIB370"
test -n "${RESULT_DIR:-}"
case "$RESULT_DIR" in
  /*) ;;
  *) echo "RESULT_DIR must be an absolute path" >&2; exit 1 ;;
esac
test ! -e "$RESULT_DIR"
mkdir -p "$(dirname -- "$RESULT_DIR")"
mkdir "$RESULT_DIR"

cp "$ROOT/validation/iterative/d4a_three_snapshots.x2m" "$RESULT_DIR/"
cp "$ROOT/data/SpotD4Snap.c2m" "$RESULT_DIR/"
cp "$ROOT/data/rnr_0burn_spot_proc/rnr_cc.c2m" "$RESULT_DIR/"
cp "$ROOT/data/rnr_0burn_spot_proc/rnr_interpol.c2m" "$RESULT_DIR/"
cp "$ROOT/data/rnr_0burn_spot_proc/irena_assembly_tiso_1_12_1ring.dat" \
  "$RESULT_DIR/geometry.dat"
cp "$ROOT/validation/iterative/d4a_snapshot_inputs.sha256" \
  "$RESULT_DIR/frozen_repository_inputs.sha256"
ln -s "$DLIB370" "$RESULT_DIR/DLIB8R1_370"

(
  cd "$RESULT_DIR"
  sha256sum d4a_three_snapshots.x2m SpotD4Snap.c2m rnr_cc.c2m \
    rnr_interpol.c2m geometry.dat DLIB8R1_370 > executed_inputs.sha256
  sha256sum "$DRAGON_BIN" > dragon_executable.sha256
)

OMP_NUM_THREADS=1
export OMP_NUM_THREADS
(
  cd "$RESULT_DIR"
  "$DRAGON_BIN" < d4a_three_snapshots.x2m \
    > d4a_three_snapshots.log 2> d4a_three_snapshots.err
)

test ! -s "$RESULT_DIR/d4a_three_snapshots.err"
test -s "$RESULT_DIR/d4a_snapshots.xsm"
if grep -q 'MAXIMUM NUMBER OF SELF-SHIELDING ITERATIONS EXCEEDED' \
  "$RESULT_DIR/d4a_three_snapshots.log"
then
  echo "D4A snapshot build rejected: TONE did not converge" >&2
  exit 1
fi
test "$(grep -c 'CONVERGENCE REACHED AT TONE ITERATION' \
  "$RESULT_DIR/d4a_three_snapshots.log")" -eq 3
grep -q '^>|D4A-THREE-SNAPSHOT-ARCHIVE-COMPLETE' \
  "$RESULT_DIR/d4a_three_snapshots.log"
(
  cd "$RESULT_DIR"
  sha256sum d4a_snapshots.xsm > d4a_snapshots.sha256
)
echo "D4A THREE-SNAPSHOT ARCHIVE BUILT: $RESULT_DIR/d4a_snapshots.xsm"
