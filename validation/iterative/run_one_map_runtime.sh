#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
DRAGON_BIN=${DRAGON_BIN:?set DRAGON_BIN to an executable built from the current sources}
SEED_DIR=${SEED_DIR:-"$ROOT/validation/artifacts/iterative-seed"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}
VERIFY_REFERENCE=${VERIFY_REFERENCE:-0}

test -x "$DRAGON_BIN"
test -f "$GANLIB_LIB"
test -f "$GANLIB_MOD/ganlib.mod"
case "$VERIFY_REFERENCE" in
  0|1) ;;
  *) echo "set VERIFY_REFERENCE to 0 or 1" >&2; exit 2 ;;
esac
PYTHONDONTWRITEBYTECODE=1 python3 -m json.tool \
  "$ROOT/validation/iterative/one_map_protocol.json" >/dev/null
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/check_one_map_contract.py" >/dev/null

for name in initial_snapshots.xsm initial_axial_track.xsm \
  initial_axial_macrolib.xsm initial_radial_track.bin
do
  expected=$(awk -v file="$name" '$2 == file { print $1 }' \
    "$ROOT/validation/iterative/seed.sha256")
  test -n "$expected"
  actual=$(shasum -a 256 "$SEED_DIR/$name" | awk '{ print $1 }')
  test "$actual" = "$expected"
done

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-one-map.XXXXXX")
cleanup() {
  if [ "${KEEP_WORK:-0}" = 1 ]; then
    printf 'ONE-MAP WORKDIR: %s\n' "$WORK"
  else
    rm -rf "$WORK"
  fi
}
trap cleanup EXIT HUP INT TERM

for name in initial_snapshots.xsm initial_axial_track.xsm \
  initial_axial_macrolib.xsm initial_radial_track.bin
do
  cp "$SEED_DIR/$name" "$WORK/$name"
done
cp "$ROOT/data/SpotRefFS.c2m" "$ROOT/data/SpotPlaneFS.c2m" "$WORK/"

"$FC" -std=f2008 -O0 -Wall -Wextra -Werror -Wno-compare-reals \
  -ffp-contract=off -fno-fast-math \
  -I "$GANLIB_MOD" \
  "$ROOT/validation/iterative/check_one_map_xsm.f90" \
  "$GANLIB_LIB" -lstdc++ -o "$WORK/check_one_map_xsm"

if rg -i '\b(LCMPUT|LCMPTC|LCMPPD|LCMLID|LCMLIL|LCMEQU|LCMDEL)\b' \
  "$ROOT/validation/iterative/check_one_map_xsm.f90" >/dev/null
then
  echo "ONE-MAP RUNTIME FAIL: checker source contains LCM mutation." >&2
  exit 1
fi
nm "$WORK/check_one_map_xsm" > "$WORK/checker_nm.txt"
if rg -i 'SPOASM|SPOPOD|SPOT1P|SPOFSRC|SPOFCHK|SPOGBAL|SPOPROJ|SPOSTATE|SPOXCONV|Dragon' \
  "$WORK/checker_nm.txt" >/dev/null
then
  echo "ONE-MAP RUNTIME FAIL: checker links production solver symbols." >&2
  exit 1
fi
rg -i 'lcmop' "$WORK/checker_nm.txt" >/dev/null

shasum -a 256 \
  "$DRAGON_BIN" \
  "$ROOT/validation/iterative/one_corrected_map.x2m" \
  "$ROOT/validation/iterative/one_map_protocol.json" \
  "$ROOT/validation/iterative/one_map_scientific.sha256" \
  "$ROOT/validation/iterative/seed.sha256" \
  "$ROOT/validation/iterative/check_one_map_contract.py" \
  "$ROOT/validation/iterative/check_one_map_runtime.py" \
  "$ROOT/validation/iterative/check_one_map_xsm.f90" \
  "$ROOT/validation/iterative/run_one_map_runtime.sh" \
  "$WORK/check_one_map_xsm" \
  "$WORK/SpotRefFS.c2m" \
  "$WORK/SpotPlaneFS.c2m" \
  "$WORK/initial_snapshots.xsm" \
  "$WORK/initial_axial_track.xsm" \
  "$WORK/initial_axial_macrolib.xsm" \
  "$WORK/initial_radial_track.bin" \
  > "$WORK/input_manifest.sha256"

(
  cd "$WORK"
  "$DRAGON_BIN" < "$ROOT/validation/iterative/one_corrected_map.x2m" \
    > one_corrected_map.log 2>&1
)

PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/check_one_map_runtime.py" \
  "$WORK/one_corrected_map.log" > "$WORK/runtime_check.log"

(
  cd "$WORK"
  ./check_one_map_xsm basis_reference.xsm state1_system.xsm \
    state0_axial.xsm state1_axial.xsm state1_snapshots.xsm \
    > one_map_xsm_check.log
)

if [ "$VERIFY_REFERENCE" = 1 ]; then
  (
    cd "$WORK"
    shasum -a 256 -c \
      "$ROOT/validation/iterative/one_map_scientific.sha256"
  ) > "$WORK/replay_check.log"
else
  echo "ONE-MAP SAME-INPUT REPLAY NOT REQUESTED" \
    > "$WORK/replay_check.log"
fi

shasum -a 256 \
  "$WORK/input_manifest.sha256" \
  "$WORK/basis_reference.xsm" \
  "$WORK/state0_axial.xsm" \
  "$WORK/state1_system.xsm" \
  "$WORK/state1_axial.xsm" \
  "$WORK/state1_snapshots.xsm" \
  "$WORK/one_corrected_map.log" \
  "$WORK/runtime_check.log" \
  "$WORK/one_map_xsm_check.log" \
  "$WORK/replay_check.log" \
  "$WORK/checker_nm.txt" \
  > "$WORK/artifact_manifest.sha256"

for name in initial_snapshots.xsm initial_axial_track.xsm \
  initial_axial_macrolib.xsm initial_radial_track.bin
do
  expected=$(awk -v file="$name" '$2 == file { print $1 }' \
    "$ROOT/validation/iterative/seed.sha256")
  source_actual=$(shasum -a 256 "$SEED_DIR/$name" | awk '{ print $1 }')
  work_actual=$(shasum -a 256 "$WORK/$name" | awk '{ print $1 }')
  test "$source_actual" = "$expected"
  test "$work_actual" = "$expected"
done
for name in SpotRefFS.c2m SpotPlaneFS.c2m
do
  source_actual=$(shasum -a 256 "$ROOT/data/$name" | awk '{ print $1 }')
  work_actual=$(shasum -a 256 "$WORK/$name" | awk '{ print $1 }')
  test "$source_actual" = "$work_actual"
done

cat "$WORK/runtime_check.log"
cat "$WORK/one_map_xsm_check.log"
cat "$WORK/replay_check.log"
cat "$WORK/input_manifest.sha256"
cat "$WORK/artifact_manifest.sha256"
if [ "$VERIFY_REFERENCE" = 1 ]; then
  echo "ONE-MAP SAME-INPUT REPLAY PASS"
else
  echo "ONE-MAP SAME-INPUT REPLAY NOT EVALUATED"
fi
echo "ONE-MAP RUNTIME PASS: one raw fixed-space map was evaluated; outer convergence was not assessed."
