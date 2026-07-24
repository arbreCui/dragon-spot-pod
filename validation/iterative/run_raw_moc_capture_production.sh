#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
ITER="$ROOT/validation/iterative"
PROTOCOL="$ITER/raw_moc_capture_run_protocol.json"
REFERENCE="$ITER/raw_moc_capture_run_reference.sha256"
IMPLEMENTATION="$ITER/raw_moc_capture_run_implementation.sha256"
CAPTURE_IMPLEMENTATION="$ITER/raw_moc_capture_implementation.sha256"
DECK_TEMPLATE="$ITER/raw_moc_capture_probe.x2m.in"
PREPARE_DECK="$ITER/radial_floor_prepare.x2m"
BOUNDED_RUNNER="$ITER/run_bounded_dragon.py"
LOG_CHECKER="$ITER/check_raw_moc_capture_run_logs.py"
LOG_TESTS="$ITER/test_raw_moc_capture_run_logs.py"
PROCESS_TESTS="$ITER/test_bounded_dragon.py"
CONTRACT_CHECKER="$ITER/check_raw_moc_capture_run_contract.py"
XSM_SOURCE="$ITER/check_raw_moc_capture_xsm.f90"
RUNNER="$ITER/run_raw_moc_capture_production.sh"

PARENT=${PARENT:-"$ROOT/validation/artifacts/iterative-radial-floor"}
FAIL_PARENT=${FAIL_PARENT:-"$ROOT/validation/artifacts/iterative-sensitivity-h2-failed"}
DRAGON_BIN=${DRAGON_BIN:-"$ROOT/validation/artifacts/raw-moc-capture-build/Dragon"}
ARTIFACT=${ARTIFACT:-"$ROOT/validation/artifacts/raw-moc-capture"}
DIRNAME=$(uname -sm | sed 's/[ ]/_/')
FC=${FC:-gfortran}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/lib/$DIRNAME/modules"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/lib/$DIRNAME/libGanlib.a"}
UTILIB_LIB=${UTILIB_LIB:-"$ROOT/Utilib/lib/$DIRNAME/libUtilib.a"}
RUN_CAPTURE=${RUN_CAPTURE:-0}

case "$RUN_CAPTURE" in
  0|1) ;;
  *)
    echo "RAW-MOC-CAPTURE FAIL: RUN_CAPTURE must be 0 or 1" >&2
    exit 2
    ;;
esac

FROZEN_PATHS="
validation/iterative/raw_moc_capture_run_protocol.json
validation/iterative/raw_moc_capture_run_reference.sha256
validation/iterative/raw_moc_capture_run_implementation.sha256
validation/iterative/raw_moc_capture_probe.x2m.in
validation/iterative/run_bounded_dragon.py
validation/iterative/test_bounded_dragon.py
validation/iterative/check_raw_moc_capture_run_logs.py
validation/iterative/test_raw_moc_capture_run_logs.py
validation/iterative/check_raw_moc_capture_run_contract.py
validation/iterative/run_raw_moc_capture_production.sh
"

fail() {
  echo "RAW-MOC-CAPTURE FAIL: $*" >&2
  exit 2
}

expected_hash() {
  awk -v label="$1" '$2 == label { print $1 }' "$REFERENCE"
}

hash_of() {
  shasum -a 256 "$1" | awk '{ print $1 }'
}

require_hash() {
  label=$1
  path=$2
  expected=$(expected_hash "$label")
  test -n "$expected" || fail "missing reference label $label"
  actual=$(hash_of "$path")
  test "$actual" = "$expected" || fail "hash differs for $label"
}

verify_run_implementation() {
  (
    cd "$ROOT"
    shasum -a 256 -c \
      validation/iterative/raw_moc_capture_run_implementation.sha256
  ) >/dev/null
}

inode_of() {
  stat -f '%i' "$1" 2>/dev/null || stat -c '%i' "$1"
}

require_distinct_inodes() {
  seen=
  for path in "$@"
  do
    test -f "$path" || fail "missing inode input $path"
    test ! -L "$path" || fail "symlink input $path"
    inode=$(inode_of "$path")
    case " $seen " in
      *" $inode "*) fail "aliased input $path" ;;
    esac
    seen="$seen $inode"
  done
}

require_normal_end() {
  log=$1
  normal=$(grep -Ec \
    '^ normal end of execution for dragon 5  Version 5\.1\.0[[:space:]]*$' \
    "$log" || true)
  phrases=$(grep -c 'normal end of execution for dragon' "$log" || true)
  test "$normal" -eq 1 && test "$phrases" -eq 1 ||
    fail "normal-end census differs in $log"
  if grep -Ei 'XABORT|segmentation fault|floating invalid|NaN|Infinity' \
    "$log" >/dev/null
  then
    fail "abnormal text in $log"
  fi
}

render_deck() {
  arm=$1
  mode=$2
  code=$3
  target=$4
  if [ "$mode" = OFF ]; then
    audit_control=
  elif [ "$mode" = ON ]; then
    audit_control="MOCA $code"
  else
    fail "invalid render mode $mode"
  fi
  sed -e "s/@ARM@/$arm/g" \
    -e "s/@MODE@/$mode/g" \
    -e "s/@AUDIT_CONTROL@/$audit_control/g" \
    "$DECK_TEMPLATE" > "$target"
  if grep '@ARM@\|@MODE@\|@AUDIT_CONTROL@' "$target" >/dev/null
  then
    fail "incomplete deck rendering"
  fi
  if [ "$mode" = OFF ]; then
    if grep -w MOCA "$target" >/dev/null; then
      fail "OFF deck contains MOCA"
    fi
  else
    test "$(grep -Ec "MOCA[[:space:]]+$code" "$target")" -eq 1 ||
      fail "ON deck audit control differs"
  fi
}

copy_verified() {
  source=$1
  target=$2
  label=$3
  require_hash "$label" "$source"
  cp "$source" "$target"
  cmp "$source" "$target"
  require_hash "$label" "$target"
}

WORK=$(mktemp -d "/tmp/moca.XXXXXX")
STAGE=
cleanup() {
  if [ -n "$STAGE" ] && [ -e "$STAGE" ]; then
    rm -rf "$STAGE"
  fi
  if [ "${KEEP_WORK:-0}" = 1 ]; then
    printf 'RAW-MOC-CAPTURE WORKDIR: %s\n' "$WORK"
  else
    rm -rf "$WORK"
  fi
}
trap cleanup EXIT HUP INT TERM

for path in "$PROTOCOL" "$REFERENCE" "$IMPLEMENTATION" \
  "$CAPTURE_IMPLEMENTATION" "$DECK_TEMPLATE" "$PREPARE_DECK" \
  "$BOUNDED_RUNNER" "$LOG_CHECKER" "$LOG_TESTS" "$PROCESS_TESTS" \
  "$CONTRACT_CHECKER" "$XSM_SOURCE" "$RUNNER" "$DRAGON_BIN" \
  "$GANLIB_MOD/ganlib.mod" "$GANLIB_LIB" "$UTILIB_LIB"
do
  test -f "$path" || fail "missing preflight file $path"
  test ! -L "$path" || fail "symlink preflight file $path"
done
test -x "$DRAGON_BIN" || fail "Dragon is not executable"
test -d "$PARENT" || fail "missing compact parent artifact"
test -d "$FAIL_PARENT" || fail "missing failure parent artifact"

for path in $FROZEN_PATHS
do
  git -C "$ROOT" ls-files --error-unmatch "$path" >/dev/null 2>&1 ||
    fail "untracked frozen file $path"
  git -C "$ROOT" diff --quiet -- "$path" ||
    fail "unstaged change in frozen file $path"
  git -C "$ROOT" diff --cached --quiet -- "$path" ||
    fail "staged change in frozen file $path"
done

PYTHONDONTWRITEBYTECODE=1 python3 -m json.tool "$PROTOCOL" >/dev/null
PYTHONDONTWRITEBYTECODE=1 python3 "$CONTRACT_CHECKER"
PYTHONDONTWRITEBYTECODE=1 python3 "$PROCESS_TESTS" >/dev/null
PYTHONDONTWRITEBYTECODE=1 python3 "$LOG_TESTS" >/dev/null
verify_run_implementation

require_hash Dragon "$DRAGON_BIN"
require_hash raw_moc_capture_implementation.sha256 "$CAPTURE_IMPLEMENTATION"
require_hash radial_floor_result_receipt.sha256 \
  "$ITER/radial_floor_result_receipt.sha256"
require_hash minimal_manifest.sha256 "$PARENT/minimal_manifest.sha256"
require_hash full_artifact_manifest.sha256 \
  "$PARENT/full_artifact_manifest.sha256"
require_hash prepared_manifest.sha256 "$PARENT/prepared_manifest.sha256"
require_hash radial_floor_prepare.x2m "$PREPARE_DECK"
require_hash check_raw_moc_capture_xsm.f90 "$XSM_SOURCE"

(
  cd "$ROOT"
  shasum -a 256 -c \
    validation/iterative/raw_moc_capture_implementation.sha256
  shasum -a 256 -c \
    validation/iterative/radial_floor_result_receipt.sha256
) >/dev/null
(
  cd "$PARENT"
  shasum -a 256 -c receipt.sha256
  shasum -a 256 -c minimal_manifest.sha256
  shasum -a 256 -c dependency_manifest.sha256
) >/dev/null

git -C "$ROOT" archive \
  d97a70225b118b2369c94e664b8e9028a1e4a704 \
  -o "$WORK/clean_git_archive.tar"
require_hash clean_git_archive.tar "$WORK/clean_git_archive.tar"

nm "$DRAGON_BIN" > "$WORK/Dragon.nm"
for symbol in spomoc_begin spomoc_capture spomoc_publish spomoc_finish
do
  grep -i "$symbol" "$WORK/Dragon.nm" >/dev/null ||
    fail "Dragon lacks $symbol"
done
strings "$DRAGON_BIN" > "$WORK/Dragon.strings"
grep 'FLUGPI: MOCA ARM 1 OR 2 EXPECTED.' "$WORK/Dragon.strings" >/dev/null ||
  fail "Dragon lacks MOCA parser text"
grep 'SPOT-MOC-AUD' "$WORK/Dragon.strings" >/dev/null ||
  fail "Dragon lacks audit schema text"

mkdir -p "$WORK/tools" "$WORK/render"
"$FC" -std=f2008 -O0 -Wall -Wextra -Werror -Wno-compare-reals \
  -fcheck=all -ffp-contract=off -fno-fast-math -I "$GANLIB_MOD" \
  "$XSM_SOURCE" "$GANLIB_LIB" "$UTILIB_LIB" -lstdc++ \
  -o "$WORK/tools/check_capture"
nm "$WORK/tools/check_capture" > "$WORK/tools/check_capture.nm"
if grep -Ei \
  'SPOMOC|DOORFV|MCCGF|MCGFLX|MCGMRE|MCGFL1|MCGFCS|MCGSIG|MCGFCF|MOCFCF' \
  "$WORK/tools/check_capture.nm" >/dev/null
then
  fail "independent checker references production solver symbols"
fi
grep -i 'lcmop' "$WORK/tools/check_capture.nm" >/dev/null ||
  fail "independent checker lacks Ganlib read path"

render_deck NATIVE OFF 1 "$WORK/render/native_off.x2m"
render_deck NATIVE ON 1 "$WORK/render/native_on.x2m"
render_deck STATIONARY OFF 2 "$WORK/render/stationary_off.x2m"
render_deck STATIONARY ON 2 "$WORK/render/stationary_on.x2m"

if [ "$RUN_CAPTURE" = 0 ]; then
  echo "RAW-MOC-CAPTURE PREFLIGHT PASS"
  echo "RAW-MOC-CAPTURE PRODUCTION NOT-RUN; SET RUN_CAPTURE=1"
  exit 0
fi

test ! -e "$ARTIFACT" || fail "artifact already exists: $ARTIFACT"
mkdir -p "$WORK/prepare" "$WORK/evidence/common"

for name in initial_snapshots.xsm state0_axial.xsm \
  initial_axial_track.xsm initial_radial_track.bin state1_snapshots.xsm
do
  source="$FAIL_PARENT/$name"
  test -f "$source" && test ! -L "$source" ||
    fail "missing parent preparation input $name"
  cp "$source" "$WORK/prepare/$name"
  cmp "$source" "$WORK/prepare/$name"
done
require_hash initial_radial_track.bin \
  "$WORK/prepare/initial_radial_track.bin"
cp "$PREPARE_DECK" "$WORK/prepare/prepare.x2m"
"$BOUNDED_RUNNER" "$DRAGON_BIN" "$WORK/prepare/prepare.x2m" \
  "$WORK/prepare/prepare.log"
require_normal_end "$WORK/prepare/prepare.log"
grep 'RADIAL-FLOOR-PREPARE-BEGIN' "$WORK/prepare/prepare.log" >/dev/null
grep 'RADIAL-FLOOR-PREPARE-COMPLETE' "$WORK/prepare/prepare.log" >/dev/null
if grep 'FLU2DR' "$WORK/prepare/prepare.log" >/dev/null; then
  fail "preparation unexpectedly entered FLU2DR"
fi
cp "$PARENT/prepared_manifest.sha256" \
  "$WORK/prepare/prepared_manifest.sha256"
(
  cd "$WORK/prepare"
  shasum -a 256 -c prepared_manifest.sha256
) > "$WORK/prepare/prepared_replay.log"
for name in restart_macro0.xsm restart_source.xsm restart_system.xsm \
  restart_track.xsm
do
  copy_verified "$WORK/prepare/$name" "$WORK/evidence/common/$name" "$name"
done
copy_verified "$WORK/prepare/initial_radial_track.bin" \
  "$WORK/evidence/common/initial_radial_track.bin" \
  initial_radial_track.bin
cp "$WORK/prepare/prepare.x2m" "$WORK/evidence/prepare.x2m"
cp "$WORK/prepare/prepare.log" "$WORK/evidence/prepare.log"
cp "$WORK/prepare/prepared_manifest.sha256" \
  "$WORK/evidence/prepared_manifest.sha256"
cp "$WORK/prepare/prepared_replay.log" \
  "$WORK/evidence/prepared_replay.log"

run_case() {
  case_name=$1
  arm=$2
  mode=$3
  code=$4
  pre_source=$5
  pre_label=$6
  case_dir="$WORK/evidence/$case_name"
  mkdir -p "$case_dir"
  for name in restart_macro0.xsm restart_source.xsm restart_system.xsm \
    restart_track.xsm initial_radial_track.bin
  do
    cp "$WORK/evidence/common/$name" "$case_dir/$name"
    cmp "$WORK/evidence/common/$name" "$case_dir/$name"
  done
  copy_verified "$pre_source" "$case_dir/result.xsm" "$pre_label"
  render_deck "$arm" "$mode" "$code" "$case_dir/probe.x2m"
  (
    cd "$case_dir"
    shasum -a 256 restart_macro0.xsm restart_source.xsm \
      restart_system.xsm restart_track.xsm initial_radial_track.bin \
      > immutable_inputs.sha256
  )
  "$BOUNDED_RUNNER" "$DRAGON_BIN" "$case_dir/probe.x2m" \
    "$case_dir/probe.log"
  require_normal_end "$case_dir/probe.log"
  (
    cd "$case_dir"
    shasum -a 256 -c immutable_inputs.sha256
  ) > "$case_dir/immutable_replay.log"
}

native_pre="$PARENT/native/arm_flux.xsm"
native_frozen="$PARENT/native/probe_post.xsm"
stationary_pre="$PARENT/stationary/arm_flux.xsm"
stationary_frozen="$PARENT/stationary/probe_post.xsm"
require_hash native_pre.xsm "$native_pre"
require_hash native_frozen.xsm "$native_frozen"
require_hash stationary_pre.xsm "$stationary_pre"
require_hash stationary_frozen.xsm "$stationary_frozen"

run_case native_off NATIVE OFF 1 "$native_pre" native_pre.xsm
run_case native_on NATIVE ON 1 "$native_pre" native_pre.xsm
run_case stationary_off STATIONARY OFF 2 \
  "$stationary_pre" stationary_pre.xsm
run_case stationary_on STATIONARY ON 2 \
  "$stationary_pre" stationary_pre.xsm

for arm in native stationary
do
  mkdir -p "$WORK/evidence/$arm"
  cp "$WORK/evidence/common/restart_track.xsm" \
    "$WORK/evidence/$arm/track.xsm"
  cp "$WORK/evidence/common/restart_system.xsm" \
    "$WORK/evidence/$arm/system.xsm"
done
copy_verified "$native_pre" "$WORK/evidence/native/pre.xsm" native_pre.xsm
copy_verified "$native_frozen" "$WORK/evidence/native/frozen.xsm" \
  native_frozen.xsm
copy_verified "$stationary_pre" "$WORK/evidence/stationary/pre.xsm" \
  stationary_pre.xsm
copy_verified "$stationary_frozen" \
  "$WORK/evidence/stationary/frozen.xsm" stationary_frozen.xsm
cp "$WORK/evidence/native_off/result.xsm" \
  "$WORK/evidence/native/off.xsm"
cp "$WORK/evidence/native_on/result.xsm" \
  "$WORK/evidence/native/on.xsm"
cp "$WORK/evidence/stationary_off/result.xsm" \
  "$WORK/evidence/stationary/off.xsm"
cp "$WORK/evidence/stationary_on/result.xsm" \
  "$WORK/evidence/stationary/on.xsm"

require_distinct_inodes \
  "$WORK/evidence/native/track.xsm" \
  "$WORK/evidence/native/system.xsm" \
  "$WORK/evidence/native/pre.xsm" \
  "$WORK/evidence/native/frozen.xsm" \
  "$WORK/evidence/native/off.xsm" \
  "$WORK/evidence/native/on.xsm"
require_distinct_inodes \
  "$WORK/evidence/stationary/track.xsm" \
  "$WORK/evidence/stationary/system.xsm" \
  "$WORK/evidence/stationary/pre.xsm" \
  "$WORK/evidence/stationary/frozen.xsm" \
  "$WORK/evidence/stationary/off.xsm" \
  "$WORK/evidence/stationary/on.xsm"

PYTHONDONTWRITEBYTECODE=1 python3 "$LOG_CHECKER" \
  "$WORK/evidence/native_off/probe.log" \
  "$WORK/evidence/native_on/probe.log" \
  "$WORK/evidence/stationary_off/probe.log" \
  "$WORK/evidence/stationary_on/probe.log" \
  > "$WORK/evidence/run_log_check.txt"

cp "$WORK/tools/check_capture" "$WORK/evidence/check_capture"
cp "$WORK/tools/check_capture.nm" "$WORK/evidence/check_capture.nm"
(
  cd "$WORK/evidence"
  ./check_capture native/track.xsm native/system.xsm native/pre.xsm \
    native/frozen.xsm native/off.xsm native/on.xsm 1 \
    > native/check_a.log
  ./check_capture native/track.xsm native/system.xsm native/pre.xsm \
    native/frozen.xsm native/off.xsm native/on.xsm 1 \
    > native/check_b.log
  cmp native/check_a.log native/check_b.log
  ./check_capture stationary/track.xsm stationary/system.xsm \
    stationary/pre.xsm stationary/frozen.xsm stationary/off.xsm \
    stationary/on.xsm 2 > stationary/check_a.log
  ./check_capture stationary/track.xsm stationary/system.xsm \
    stationary/pre.xsm stationary/frozen.xsm stationary/off.xsm \
    stationary/on.xsm 2 > stationary/check_b.log
  cmp stationary/check_a.log stationary/check_b.log
)
grep '^RAW-MOC-XSM CAPTURE-VALID$' \
  "$WORK/evidence/native/check_a.log" >/dev/null
grep '^RAW-MOC-XSM CAPTURE-VALID$' \
  "$WORK/evidence/stationary/check_a.log" >/dev/null

require_hash Dragon "$DRAGON_BIN"
require_hash clean_git_archive.tar "$WORK/clean_git_archive.tar"
verify_run_implementation
(
  cd "$ROOT"
  shasum -a 256 -c \
    validation/iterative/raw_moc_capture_implementation.sha256
  shasum -a 256 -c \
    validation/iterative/radial_floor_result_receipt.sha256
) > "$WORK/evidence/external_replay.log"
(
  cd "$PARENT"
  shasum -a 256 -c receipt.sha256
  shasum -a 256 -c minimal_manifest.sha256
  shasum -a 256 -c dependency_manifest.sha256
) >> "$WORK/evidence/external_replay.log"
git -C "$ROOT" rev-parse HEAD > "$WORK/evidence/run_commit.txt"
cp "$PROTOCOL" "$REFERENCE" "$IMPLEMENTATION" "$CAPTURE_IMPLEMENTATION" \
  "$DECK_TEMPLATE" "$BOUNDED_RUNNER" "$LOG_CHECKER" "$CONTRACT_CHECKER" \
  "$RUNNER" "$WORK/evidence/"

(
  cd "$WORK/evidence"
  if find . -type l -print | grep . >/dev/null; then
    fail "evidence contains a symlink"
  fi
  find . -type f ! -name artifact_manifest.sha256 \
    ! -name artifact_replay.log -exec shasum -a 256 {} \; |
    LC_ALL=C sort > artifact_manifest.sha256
  shasum -a 256 -c artifact_manifest.sha256 > artifact_replay.log
)

artifact_parent=$(dirname "$ARTIFACT")
artifact_name=$(basename "$ARTIFACT")
mkdir -p "$artifact_parent"
STAGE="$artifact_parent/.$artifact_name.staging.$$"
test ! -e "$STAGE" || fail "artifact staging path exists"
cp -R "$WORK/evidence" "$STAGE"
(
  cd "$STAGE"
  shasum -a 256 -c artifact_manifest.sha256 > artifact_replay.log
)
test ! -e "$ARTIFACT" || fail "artifact appeared during publication"
mv "$STAGE" "$ARTIFACT"
STAGE=

cat "$ARTIFACT/run_log_check.txt"
grep '^RAW-MOC-XSM SCALAR-' "$ARTIFACT/native/check_a.log"
grep '^RAW-MOC-XSM SCALAR-' "$ARTIFACT/stationary/check_a.log"
echo "RAW-MOC-CAPTURE PRODUCTION COMPLETE"
