#!/bin/sh
set -eu

RUN_ANDERSON1_MAP=${RUN_ANDERSON1_MAP:-0}
case "$RUN_ANDERSON1_MAP" in
  0)
    printf '%s\n' \
      'ANDERSON1-MAP DEFAULT-OFF: no Dragon process started.'
    exit 0
    ;;
  1) ;;
  *)
    printf '%s\n' \
      'ANDERSON1-MAP ERROR: RUN_ANDERSON1_MAP must be 0 or 1.' >&2
    exit 2
    ;;
esac

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
DRAGON_BIN=${DRAGON_BIN:-"$ROOT/bin/Darwin_arm64/Dragon"}
ARTIFACTS=${ARTIFACTS:-"$ROOT/validation/artifacts"}
SEED_DIR=${SEED_DIR:-"$ARTIFACTS/iterative-seed"}
BASIS_DIR=${BASIS_DIR:-"$ARTIFACTS/iterative-map1"}
CANDIDATE_LOCK=${CANDIDATE_LOCK:-\
"$ROOT/validation/iterative/anderson1_trial_scientific.sha256"}
SEED_LOCK=${SEED_LOCK:-"$ROOT/validation/iterative/seed.sha256"}
BASIS_LOCK=${BASIS_LOCK:-\
"$ROOT/validation/iterative/one_map_scientific.sha256"}
ARTIFACT_OUT=${ARTIFACT_OUT:-\
"$ARTIFACTS/iterative-anderson1-returned-120-80s"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}

# Historical direct-map timings require a wider radial bound than the axial
# bound. Each process is launched once; the helper permits at most five more
# seconds for TERM cleanup before KILL. There is no retry.
RADIAL_TIMEOUT_SECONDS=120
AXIAL_TIMEOUT_SECONDS=80

test -x "$DRAGON_BIN"
test -f "$GANLIB_LIB"
test -f "$GANLIB_MOD/ganlib.mod"
test -f "$CANDIDATE_LOCK"
test -f "$SEED_LOCK"
test -f "$BASIS_LOCK"
test ! -e "$ARTIFACT_OUT"

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-anderson1-map.XXXXXX")
RADIAL_WORK="$WORK/radial"
AXIAL_WORK="$WORK/axial"
mkdir -p "$RADIAL_WORK" "$AXIAL_WORK"
SUCCESS=0
STARTED=0
cleanup() {
  if [ "$SUCCESS" = 1 ] && [ "${KEEP_WORK:-0}" != 1 ]; then
    rm -rf "$WORK"
  else
    printf 'ANDERSON1-MAP WORKDIR: %s\n' "$WORK"
    if [ "$STARTED" = 1 ] && [ "$SUCCESS" != 1 ]; then
      printf '%s\n' \
        'ANDERSON1-MAP INVALID-NO-SCIENTIFIC-RESULT; no retry.'
    fi
  fi
}
trap cleanup EXIT HUP INT TERM

verify_locked() {
  lock=$1
  source_dir=$2
  name=$3
  expected=$(awk -v file="$name" '$2 == file { print $1 }' "$lock")
  actual=$(shasum -a 256 "$source_dir/$name" | awk '{ print $1 }')
  test -n "$expected"
  test "$actual" = "$expected"
}

verify_candidate() {
  relative=$1
  expected=$(awk -v file="$relative" '$2 == file { print $1 }' \
    "$CANDIDATE_LOCK")
  actual=$(shasum -a 256 "$ARTIFACTS/$relative" | awk '{ print $1 }')
  test -n "$expected"
  test "$actual" = "$expected"
}

verify_inputs() {
  verify_locked "$SEED_LOCK" "$SEED_DIR" initial_axial_track.xsm
  verify_locked "$SEED_LOCK" "$SEED_DIR" initial_axial_macrolib.xsm
  verify_locked "$SEED_LOCK" "$SEED_DIR" initial_radial_track.bin
  verify_locked "$BASIS_LOCK" "$BASIS_DIR" basis_reference.xsm
  verify_candidate iterative-map4-axial-80s/state4_axial.xsm
  verify_candidate iterative-map5-axial-80s/state5_axial.xsm
  verify_candidate iterative-map6-axial-80s/state6_axial.xsm
  verify_candidate iterative-map6-axial-80s/state6_snapshots.xsm
}

static_hashes() {
  shasum -a 256 \
    "$ROOT/data/SpotRefFS.c2m" \
    "$ROOT/data/SpotPlaneFS.c2m" \
    "$ROOT/validation/iterative/prepare_anderson1_trial.f90" \
    "$ROOT/validation/iterative/check_anderson1_trial_xsm.f90" \
    "$ROOT/validation/iterative/anderson1_radial.x2m" \
    "$ROOT/validation/iterative/anderson1_axial.x2m" \
    "$ROOT/validation/iterative/run_bounded_dragon.py"
}

verify_inputs
STATIC_BEFORE=$(static_hashes)

cp "$SEED_DIR/initial_axial_track.xsm" \
  "$SEED_DIR/initial_axial_macrolib.xsm" \
  "$SEED_DIR/initial_radial_track.bin" "$RADIAL_WORK/"
cp "$BASIS_DIR/basis_reference.xsm" "$RADIAL_WORK/"
cp "$ARTIFACTS/iterative-map4-axial-80s/state4_axial.xsm" \
  "$RADIAL_WORK/x4.xsm"
cp "$ARTIFACTS/iterative-map5-axial-80s/state5_axial.xsm" \
  "$RADIAL_WORK/x5.xsm"
cp "$ARTIFACTS/iterative-map6-axial-80s/state6_axial.xsm" \
  "$RADIAL_WORK/x6.xsm"
cp "$ARTIFACTS/iterative-map6-axial-80s/state6_snapshots.xsm" \
  "$RADIAL_WORK/snap6.xsm"
cp "$ROOT/data/SpotRefFS.c2m" "$ROOT/data/SpotPlaneFS.c2m" \
  "$RADIAL_WORK/"
cp "$ROOT/validation/iterative/anderson1_radial.x2m" \
  "$RADIAL_WORK/radial.x2m"
cp "$ROOT/validation/iterative/anderson1_axial.x2m" \
  "$AXIAL_WORK/axial.x2m"

"$FC" -std=f2008 -O0 -Wall -Wextra -Werror -Wno-compare-reals \
  -ffp-contract=off -fno-fast-math -fcheck=all -I "$GANLIB_MOD" \
  "$ROOT/validation/iterative/prepare_anderson1_trial.f90" \
  "$GANLIB_LIB" -lstdc++ -o "$RADIAL_WORK/prepare_anderson1_trial"
"$FC" -std=f2008 -O0 -Wall -Wextra -Werror -Wno-compare-reals \
  -ffp-contract=off -fno-fast-math -fcheck=all -I "$GANLIB_MOD" \
  "$ROOT/validation/iterative/check_anderson1_trial_xsm.f90" \
  "$GANLIB_LIB" -lstdc++ -o "$RADIAL_WORK/check_anderson1_trial_xsm"

(
  cd "$RADIAL_WORK"
  ./prepare_anderson1_trial x4.xsm x5.xsm x6.xsm snap6.xsm \
    trial_axial.xsm trial_snapshots.xsm
  ./check_anderson1_trial_xsm x4.xsm x5.xsm x6.xsm snap6.xsm \
    trial_axial.xsm trial_snapshots.xsm
)

run_bounded() {
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH="$ROOT/validation/iterative" \
  python3 -c \
    'import sys; from pathlib import Path; from run_bounded_dragon import run; run(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), float(sys.argv[4]))' \
    "$DRAGON_BIN" "$1" "$2" "$3"
}

reject_abnormal() {
  if rg -i \
    'FLU2DR-DIAG|CONVERGENCE NOT REACHED|XABORT|ABORT:|FATAL|SIG(SEGV|FPE|BUS|ILL|ABRT)|fortran runtime error' \
    "$1" >/dev/null
  then
    printf '%s\n' \
      'ANDERSON1-MAP FAIL: abnormal or nonconverged solver marker.' >&2
    exit 1
  fi
}

STARTED=1
printf '%s\n' \
  'ANDERSON1-MAP RADIAL START: 120 s hard wait + 5 s TERM grace; no retry'
run_bounded "$RADIAL_WORK/radial.x2m" "$RADIAL_WORK/radial.log" \
  "$RADIAL_TIMEOUT_SECONDS"
reject_abnormal "$RADIAL_WORK/radial.log"
test "$(rg -c '^ FLU2DR-TERM OUTER-GATE=PASS ' \
  "$RADIAL_WORK/radial.log")" = 3
test "$(rg -c '^ FLU2DR-TERM INNER-TERMINAL ' \
  "$RADIAL_WORK/radial.log")" = 3
test "$(rg -c 'normal end of execution for dragon' \
  "$RADIAL_WORK/radial.log")" = 1
test "$(rg -c '^SPOFSRC KEFF/QSUM/QMIN/QMAX ' \
  "$RADIAL_WORK/radial.log")" = 3
test "$(rg -c '^SPOFCHK L2/MAX/RBAL/MIN/QSUM ' \
  "$RADIAL_WORK/radial.log")" = 3
test "$(rg -c '^>\|ANDERSON1-RADIAL-COMPLETE' \
  "$RADIAL_WORK/radial.log")" = 1
printf '%s\n' 'ANDERSON1-MAP RADIAL END'

for name in initial_axial_track.xsm initial_axial_macrolib.xsm \
  basis_reference.xsm x4.xsm x5.xsm x6.xsm snap6.xsm \
  trial_axial.xsm trial_snapshots.xsm returned_system.xsm \
  returned_radial.xsm check_anderson1_trial_xsm
do
  cp "$RADIAL_WORK/$name" "$AXIAL_WORK/$name"
done

printf '%s\n' \
  'ANDERSON1-MAP AXIAL START: 80 s hard wait + 5 s TERM grace; no retry'
run_bounded "$AXIAL_WORK/axial.x2m" "$AXIAL_WORK/axial.log" \
  "$AXIAL_TIMEOUT_SECONDS"
reject_abnormal "$AXIAL_WORK/axial.log"
test "$(rg -c '^ FLU2DR-TERM OUTER-GATE=PASS ' \
  "$AXIAL_WORK/axial.log")" = 1
test "$(rg -c '^ FLU2DR-TERM INNER-TERMINAL ' \
  "$AXIAL_WORK/axial.log")" = 1
test "$(rg -c 'normal end of execution for dragon' \
  "$AXIAL_WORK/axial.log")" = 1
test "$(rg -c '^>\|ANDERSON1-AXIAL-COMPLETE' \
  "$AXIAL_WORK/axial.log")" = 1
printf '%s\n' 'ANDERSON1-MAP AXIAL END'

CHECK_RESULT=$(
  cd "$AXIAL_WORK"
  ./check_anderson1_trial_xsm --returned \
    x4.xsm x5.xsm x6.xsm snap6.xsm \
    trial_axial.xsm trial_snapshots.xsm \
    returned_axial.xsm returned_snapshots.xsm
)
printf '%s\n' "$CHECK_RESULT"
printf '%s\n' "$CHECK_RESULT" >"$AXIAL_WORK/returned_check.log"
printf '%s\n' "$CHECK_RESULT" | grep -Fqx \
  'ANDERSON1-RETURNED FIXED-BUNDLE BITWISE PASS'
printf '%s\n' "$CHECK_RESULT" | grep -Fqx \
  'ANDERSON1-RETURNED RAW-DEFECT BITWISE PASS'
printf '%s\n' "$CHECK_RESULT" | grep -Fqx \
  'ANDERSON1-RETURNED STATE-CONTRACT PASS'
printf '%s\n' "$CHECK_RESULT" | grep -Fqx \
  'ANDERSON1-RETURNED RESTART-ARCHIVE BITWISE PASS'
printf '%s\n' "$CHECK_RESULT" | grep -Fqx \
  'ANDERSON1-RETURNED RAW-RADIAL-POSITIVITY PASS'
printf '%s\n' "$CHECK_RESULT" | grep -Fqx \
  'ANDERSON1-RETURNED COMPLETE'

verify_inputs
STATIC_AFTER=$(static_hashes)
test "$STATIC_AFTER" = "$STATIC_BEFORE"

mkdir -p "$ARTIFACT_OUT"
cp "$RADIAL_WORK/radial.log" \
  "$RADIAL_WORK/returned_system.xsm" \
  "$RADIAL_WORK/returned_radial.xsm" \
  "$AXIAL_WORK/axial.log" \
  "$AXIAL_WORK/returned_check.log" \
  "$AXIAL_WORK/trial_axial.xsm" \
  "$AXIAL_WORK/trial_snapshots.xsm" \
  "$AXIAL_WORK/returned_axial.xsm" \
  "$AXIAL_WORK/returned_snapshots.xsm" "$ARTIFACT_OUT/"
cp "$ROOT/validation/iterative/anderson1_radial.x2m" \
  "$ROOT/validation/iterative/anderson1_axial.x2m" "$ARTIFACT_OUT/"
(
  cd "$ARTIFACT_OUT"
  shasum -a 256 anderson1_radial.x2m anderson1_axial.x2m \
    radial.log axial.log returned_check.log \
    trial_axial.xsm trial_snapshots.xsm returned_system.xsm \
    returned_radial.xsm returned_axial.xsm returned_snapshots.xsm \
    > scientific.sha256
)

rg 'ANDERSON1-(RAW-DEFECT|RETURNED)|SPOGBAL GLOBAL/MAX-GROUP' \
  "$AXIAL_WORK/axial.log"
shasum -a 256 "$DRAGON_BIN"
printf 'ANDERSON1-MAP ARTIFACT: %s\n' "$ARTIFACT_OUT"
printf '%s\n' \
  'ANDERSON1-MAP PASS: one complete G(x_A); outer convergence not inferred.'
SUCCESS=1
