#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
DRAGON_BIN=${DRAGON_BIN:?set DRAGON_BIN to the frozen Stage-4 executable}
FAIL_DIR=${FAIL_DIR:-"$ROOT/validation/artifacts/iterative-sensitivity-h2-failed"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}

ITER="$ROOT/validation/iterative"
REFERENCE="$ITER/radial_floor_reference.sha256"
PROTOCOL="$ITER/radial_floor_protocol.json"
PREPARE_DECK="$ITER/radial_floor_prepare.x2m"
ARM_TEMPLATE="$ITER/radial_floor_arm.x2m.in"
PROBE_TEMPLATE="$ITER/radial_floor_probe.x2m.in"
CONTRACT_CHECKER="$ITER/check_radial_floor_contract.py"
STATUS_CHECKER="$ITER/check_radial_floor_status.py"
XSM_SOURCE="$ITER/check_radial_floor_xsm.f90"
STATUS_TESTS="$ITER/test_radial_floor_status.py"
RUNNER="$ITER/run_radial_floor_diagnostic.sh"

FROZEN_PATHS="
validation/iterative/radial_floor_protocol.json
validation/iterative/radial_floor_reference.sha256
validation/iterative/radial_floor_prepare.x2m
validation/iterative/radial_floor_arm.x2m.in
validation/iterative/radial_floor_probe.x2m.in
validation/iterative/check_radial_floor_contract.py
validation/iterative/check_radial_floor_status.py
validation/iterative/test_radial_floor_status.py
validation/iterative/check_radial_floor_xsm.f90
validation/iterative/run_radial_floor_diagnostic.sh
"

test -x "$DRAGON_BIN"
test -d "$FAIL_DIR"
test -f "$GANLIB_LIB"
test -f "$GANLIB_MOD/ganlib.mod"
for path in "$REFERENCE" "$PROTOCOL" "$PREPARE_DECK" "$ARM_TEMPLATE" \
  "$PROBE_TEMPLATE" "$CONTRACT_CHECKER" "$STATUS_CHECKER" "$STATUS_TESTS" \
  "$XSM_SOURCE" "$RUNNER"
do
  test -f "$path"
  test ! -L "$path"
done
for path in $FROZEN_PATHS
do
  if ! git -C "$ROOT" ls-files --error-unmatch "$path" >/dev/null 2>&1
  then
    echo "RADIAL-FLOOR FREEZE FAIL: untracked protocol file $path" >&2
    exit 1
  fi
  if ! git -C "$ROOT" diff --quiet -- "$path" ||
     ! git -C "$ROOT" diff --cached --quiet -- "$path"
  then
    echo "RADIAL-FLOOR FREEZE FAIL: uncommitted protocol file $path" >&2
    exit 1
  fi
done

expected_hash() {
  awk -v file="$1" '$2 == file { print $1 }' "$REFERENCE"
}

require_hash() {
  label=$1
  path=$2
  expected=$(expected_hash "$label")
  test -n "$expected"
  actual=$(shasum -a 256 "$path" | awk '{ print $1 }')
  if [ "$actual" != "$expected" ]; then
    echo "RADIAL-FLOOR INPUT HASH FAIL: $label" >&2
    exit 1
  fi
}

inode_of() {
  stat -f '%i' "$1" 2>/dev/null || stat -c '%i' "$1"
}

require_normal_end() {
  log=$1
  count=$(grep -Ec \
    '^ normal end of execution for dragon 5  Version 5\.1\.0[[:space:]]*$' \
    "$log" || true)
  phrase_count=$(grep -c 'normal end of execution for dragon' "$log" || true)
  if [ "$count" -ne 1 ] || [ "$phrase_count" -ne 1 ]; then
    echo "RADIAL-FLOOR FAIL: missing unique Dragon normal end in $log" >&2
    exit 1
  fi
  if grep -E 'XABORT|segmentation fault|floating invalid|NaN|Infinity' \
    "$log" >/dev/null
  then
    echo "RADIAL-FLOOR FAIL: abnormal text in $log" >&2
    exit 1
  fi
}

render_arm() {
  arm=$1
  free=$2
  accelerated=$3
  target=$4
  sed -e "s/@ARM@/$arm/g" \
    -e "s/@FREE@/$free/g" \
    -e "s/@ACCEL@/$accelerated/g" \
    "$ARM_TEMPLATE" > "$target"
  if grep '@ARM@\|@FREE@\|@ACCEL@' "$target" >/dev/null; then
    echo "RADIAL-FLOOR FAIL: incomplete arm rendering" >&2
    exit 1
  fi
}

render_probe() {
  arm=$1
  target=$2
  sed -e "s/@ARM@/$arm/g" "$PROBE_TEMPLATE" > "$target"
  if grep '@ARM@' "$target" >/dev/null; then
    echo "RADIAL-FLOOR FAIL: incomplete probe rendering" >&2
    exit 1
  fi
}

copy_common_inputs() {
  target=$1
  for name in restart_macro0.xsm restart_source.xsm restart_system.xsm \
    restart_track.xsm initial_radial_track.bin
  do
    cp "$WORK/$name" "$target/$name"
    cmp "$WORK/$name" "$target/$name"
  done
  cp "$WORK/restart_cap.xsm" "$target/arm_flux.xsm"
  cmp "$WORK/restart_cap.xsm" "$target/arm_flux.xsm"
}

PYTHONDONTWRITEBYTECODE=1 python3 -m json.tool "$PROTOCOL" >/dev/null
PYTHONDONTWRITEBYTECODE=1 python3 "$CONTRACT_CHECKER"

require_hash Dragon "$DRAGON_BIN"
require_hash FLU2DR.f "$ROOT/src/FLU2DR.f"
require_hash FLU2AC.f "$ROOT/src/FLU2AC.f"
require_hash FLUGPI.f "$ROOT/src/FLUGPI.f"
require_hash FLU.f "$ROOT/src/FLU.f"
require_hash SPOFSRC.f90 "$ROOT/src/SPOFSRC.f90"
require_hash SPOPROJ.f90 "$ROOT/src/SPOPROJ.f90"
for name in initial_snapshots.xsm state0_axial.xsm \
  initial_axial_track.xsm initial_radial_track.bin \
  state1_snapshots.xsm inner_sensitivity.log
do
  test -f "$FAIL_DIR/$name"
  test ! -L "$FAIL_DIR/$name"
  require_hash "$name" "$FAIL_DIR/$name"
done
(
  cd "$FAIL_DIR"
  shasum -a 256 -c "$ITER/inner_sensitivity_failure_receipt.sha256"
) >/dev/null

WORK=$(mktemp -d "/tmp/spot-rf.XXXXXX")
cleanup() {
  if [ "${KEEP_WORK:-0}" = 1 ]; then
    printf 'RADIAL-FLOOR WORKDIR: %s\n' "$WORK"
  else
    rm -rf "$WORK"
  fi
}
trap cleanup EXIT HUP INT TERM
git -C "$ROOT" rev-parse HEAD > "$WORK/protocol_commit.txt"

for name in initial_snapshots.xsm state0_axial.xsm \
  initial_axial_track.xsm initial_radial_track.bin state1_snapshots.xsm
do
  cp "$FAIL_DIR/$name" "$WORK/$name"
  cmp "$FAIL_DIR/$name" "$WORK/$name"
done

"$FC" -std=f2008 -O0 -Wall -Wextra -Werror -Wno-compare-reals \
  -fcheck=all -ffp-contract=off -fno-fast-math -I "$GANLIB_MOD" \
  "$XSM_SOURCE" "$GANLIB_LIB" -lstdc++ \
  -o "$WORK/check_radial_floor_xsm"

if rg -i '\b(LCMPUT|LCMPTC|LCMPPD|LCMLID|LCMLIL|LCMEQU|LCMDEL)\b' \
  "$XSM_SOURCE" >/dev/null
then
  echo "RADIAL-FLOOR FAIL: XSM checker contains LCM mutation" >&2
  exit 1
fi
nm "$WORK/check_radial_floor_xsm" > "$WORK/check_radial_floor_xsm.nm"
if rg -i 'FLU2DR|FLU2AC|SPOFSRC|SPOFCHK|Dragon|MCCGF' \
  "$WORK/check_radial_floor_xsm.nm" >/dev/null
then
  echo "RADIAL-FLOOR FAIL: XSM checker links solver symbols" >&2
  exit 1
fi
rg -i 'lcmop' "$WORK/check_radial_floor_xsm.nm" >/dev/null

shasum -a 256 \
  "$DRAGON_BIN" "$REFERENCE" "$PROTOCOL" "$PREPARE_DECK" \
  "$ARM_TEMPLATE" "$PROBE_TEMPLATE" "$CONTRACT_CHECKER" \
  "$STATUS_CHECKER" "$STATUS_TESTS" "$XSM_SOURCE" "$RUNNER" \
  "$ROOT/src/FLU2DR.f" "$ROOT/src/FLU2AC.f" \
  "$ROOT/src/FLUGPI.f" "$ROOT/src/FLU.f" "$ROOT/src/SPOFSRC.f90" \
  "$ROOT/src/SPOPROJ.f90" \
  "$WORK/protocol_commit.txt" \
  "$WORK/check_radial_floor_xsm" \
  "$WORK/initial_snapshots.xsm" "$WORK/state0_axial.xsm" \
  "$WORK/initial_axial_track.xsm" "$WORK/initial_radial_track.bin" \
  "$WORK/state1_snapshots.xsm" \
  > "$WORK/input_manifest.sha256"

(
  cd "$WORK"
  "$DRAGON_BIN" < "$PREPARE_DECK" > prepare.log 2>&1
)
require_normal_end "$WORK/prepare.log"
grep 'RADIAL-FLOOR-PREPARE-BEGIN' "$WORK/prepare.log" >/dev/null
grep 'RADIAL-FLOOR-PREPARE-COMPLETE' "$WORK/prepare.log" >/dev/null
if grep 'FLU2DR' "$WORK/prepare.log" >/dev/null; then
  echo "RADIAL-FLOOR FAIL: preparation unexpectedly ran FLU2DR" >&2
  exit 1
fi
for name in restart_macro0.xsm restart_source.xsm restart_system.xsm \
  restart_track.xsm restart_cap.xsm
do
  test -s "$WORK/$name"
  test ! -L "$WORK/$name"
done
(
  cd "$WORK"
  shasum -a 256 \
    restart_macro0.xsm restart_source.xsm restart_system.xsm \
    restart_track.xsm restart_cap.xsm > prepared_manifest.sha256
)

(
  cd "$WORK"
  ./check_radial_floor_xsm restart_track.xsm restart_source.xsm \
    restart_system.xsm restart_cap.xsm PREPARED \
    > restart_xsm_check.log
  shasum -a 256 -c prepared_manifest.sha256 \
    > prepared_replay_preflight.log
)

mkdir -p "$WORK/native" "$WORK/stationary"
copy_common_inputs "$WORK/native"
copy_common_inputs "$WORK/stationary"

for name in restart_macro0.xsm restart_source.xsm restart_system.xsm \
  restart_track.xsm initial_radial_track.bin arm_flux.xsm
do
  cmp "$WORK/native/$name" "$WORK/stationary/$name"
  inode_native=$(inode_of "$WORK/native/$name")
  inode_stationary=$(inode_of "$WORK/stationary/$name")
  if [ "$inode_native" = "$inode_stationary" ]; then
    echo "RADIAL-FLOOR FAIL: A/B input aliases for $name" >&2
    exit 1
  fi
done

render_arm NATIVE 3 3 "$WORK/native/arm.x2m"
render_arm STATIONARY 1 0 "$WORK/stationary/arm.x2m"

(
  cd "$WORK/native"
  "$DRAGON_BIN" < arm.x2m > arm.log 2>&1
)
require_normal_end "$WORK/native/arm.log"
(
  cd "$WORK/stationary"
  "$DRAGON_BIN" < arm.x2m > arm.log 2>&1
)
require_normal_end "$WORK/stationary/arm.log"

for arm in native stationary
do
  cp "$WORK/$arm/arm_flux.xsm" "$WORK/$arm/probe_pre.xsm"
  cp "$WORK/$arm/arm_flux.xsm" "$WORK/$arm/probe_post.xsm"
  cmp "$WORK/$arm/arm_flux.xsm" "$WORK/$arm/probe_pre.xsm"
  cmp "$WORK/$arm/probe_pre.xsm" "$WORK/$arm/probe_post.xsm"
  terminal_hash=$(shasum -a 256 "$WORK/$arm/arm_flux.xsm" | \
    awk '{ print $1 }')
  {
    printf '%s  arm_flux.xsm\n' "$terminal_hash"
    printf '%s  probe_pre.xsm\n' "$terminal_hash"
  } > "$WORK/$arm/terminal.sha256"
  (
    cd "$WORK/$arm"
    shasum -a 256 -c terminal.sha256 >/dev/null
  )
done

render_probe NATIVE "$WORK/native/probe.x2m"
render_probe STATIONARY "$WORK/stationary/probe.x2m"

(
  cd "$WORK/native"
  "$DRAGON_BIN" < probe.x2m > probe.log 2>&1
)
require_normal_end "$WORK/native/probe.log"
(
  cd "$WORK/stationary"
  "$DRAGON_BIN" < probe.x2m > probe.log 2>&1
)
require_normal_end "$WORK/stationary/probe.log"

PYTHONDONTWRITEBYTECODE=1 python3 "$STATUS_CHECKER" \
  "$WORK/native/arm.log" "$WORK/stationary/arm.log" \
  "$WORK/native/probe.log" "$WORK/stationary/probe.log" \
  "$PROTOCOL" > "$WORK/status.log"

(
  cd "$WORK"
  ./check_radial_floor_xsm restart_track.xsm restart_source.xsm \
    restart_system.xsm restart_cap.xsm \
    native/probe_pre.xsm native/probe_post.xsm \
    stationary/probe_pre.xsm stationary/probe_post.xsm \
    > radial_floor_xsm_check.log
)

(
  cd "$WORK/native"
  shasum -a 256 -c terminal.sha256 >/dev/null
)
(
  cd "$WORK/stationary"
  shasum -a 256 -c terminal.sha256 >/dev/null
)
for arm in native stationary
do
  for name in restart_macro0.xsm restart_source.xsm restart_system.xsm \
    restart_track.xsm initial_radial_track.bin
  do
    cmp "$WORK/$name" "$WORK/$arm/$name"
  done
done
seen_flux_inodes=
for path in "$WORK/restart_cap.xsm" \
  "$WORK/native/probe_pre.xsm" "$WORK/native/probe_post.xsm" \
  "$WORK/stationary/probe_pre.xsm" "$WORK/stationary/probe_post.xsm"
do
  inode=$(inode_of "$path")
  case " $seen_flux_inodes " in
    *" $inode "*)
      echo "RADIAL-FLOOR FAIL: aliased final flux input $path" >&2
      exit 1
      ;;
  esac
  seen_flux_inodes="$seen_flux_inodes $inode"
done
(
  cd "$WORK"
  shasum -a 256 -c prepared_manifest.sha256 \
    > prepared_replay_final.log
)
shasum -a 256 -c "$WORK/input_manifest.sha256" \
  > "$WORK/input_replay.log"

(
  cd "$WORK"
  if find . -type l -print | grep . >/dev/null
  then
    echo "RADIAL-FLOOR FAIL: artifact contains a symlink" >&2
    exit 1
  fi
  find . -type f ! -name artifact_manifest.sha256 \
    ! -name artifact_replay.log -exec shasum -a 256 {} \; |
    LC_ALL=C sort > artifact_manifest.sha256
  shasum -a 256 -c artifact_manifest.sha256 \
    > artifact_replay.log
)

cat "$WORK/status.log"
cat "$WORK/radial_floor_xsm_check.log"
cat "$WORK/protocol_commit.txt"
echo "RADIAL-FLOOR INPUT REPLAY PASS"
echo "RADIAL-FLOOR ARTIFACT REPLAY PASS"
echo "RADIAL-FLOOR DIAGNOSTIC COMPLETE"
