#!/bin/sh
set -eu

RUN_CONTINUATION=${RUN_CONTINUATION:-0}
case "$RUN_CONTINUATION" in
  0)
    echo "SPOT-CONTINUATION DEFAULT-OFF: no Dragon process started."
    exit 0
    ;;
  1) ;;
  *)
    echo "SPOT-CONTINUATION ERROR: RUN_CONTINUATION must be 0 or 1." >&2
    exit 2
    ;;
esac

fail() {
  printf 'SPOT-CONTINUATION ERROR: %s\n' "$1" >&2
  exit 2
}

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
DRAGON_BIN=${DRAGON_BIN:-"$ROOT/bin/Darwin_arm64/Dragon"}
PARENT_MANIFEST_SOURCE=${PARENT_MANIFEST:-"$ROOT/validation/iterative/current_parent.tsv"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}
RESULT_DIR=${RESULT_DIR:-}
RADIAL_TIMEOUT_SECONDS=120
AXIAL_TIMEOUT_SECONDS=80

test -n "$RESULT_DIR" || fail "RESULT_DIR is required when enabled."
case "$RESULT_DIR" in
  /*) ;;
  *) fail "RESULT_DIR must be an absolute path." ;;
esac
test ! -e "$RESULT_DIR" && test ! -L "$RESULT_DIR" ||
  fail "RESULT_DIR already exists."
RESULT_PARENT=$(dirname -- "$RESULT_DIR")
RESULT_NAME=$(basename -- "$RESULT_DIR")
LOCK_DIR="$RESULT_PARENT/.$RESULT_NAME.lock"
test -d "$RESULT_PARENT" && test -w "$RESULT_PARENT" ||
  fail "RESULT_DIR parent must exist and be writable."
test -f "$DRAGON_BIN" && test ! -L "$DRAGON_BIN" && test -x "$DRAGON_BIN" ||
  fail "Dragon must be an executable non-symlink file."
test -f "$GANLIB_LIB" || fail "Ganlib library is missing."
test -f "$GANLIB_MOD/ganlib.mod" || fail "Ganlib modules are missing."
test -f "$PARENT_MANIFEST_SOURCE" && test ! -L "$PARENT_MANIFEST_SOURCE" ||
  fail "parent manifest must be a regular non-symlink file."

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-continuation.XXXXXX")
HOST_WORK="$WORK/host"
RADIAL_WORK="$WORK/radial"
AXIAL_WORK="$WORK/axial"
mkdir -p "$HOST_WORK" "$RADIAL_WORK" "$AXIAL_WORK"
SUCCESS=0
MAP_STARTED=0
MAP_VALID=0
PUBLISH_DIR=
LOCK_HELD=0
classification=

cleanup() {
  status=$?
  if [ "$SUCCESS" != 1 ]; then
    if [ -n "$PUBLISH_DIR" ] && [ -d "$PUBLISH_DIR" ]; then
      rm -rf "$PUBLISH_DIR"
    fi
    if [ "$MAP_STARTED" = 1 ]; then
      if [ "$MAP_VALID" = 1 ]; then
        printf 'SPOT-CONTINUATION CLASSIFICATION: %s\n' \
          "$classification" >&2
        printf '%s\n' \
          "SPOT-CONTINUATION PUBLICATION FAIL: valid map retained only in workdir." >&2
      else
        printf '%s\n' \
          "SPOT-CONTINUATION INVALID_MAP: no candidate was published." >&2
      fi
    fi
    printf 'SPOT-CONTINUATION WORKDIR: %s\n' "$WORK" >&2
  elif [ "${KEEP_WORK:-0}" = 1 ]; then
    printf 'SPOT-CONTINUATION WORKDIR: %s\n' "$WORK"
  else
    rm -rf "$WORK"
  fi
  if [ "$LOCK_HELD" = 1 ]; then
    rmdir "$LOCK_DIR" 2>/dev/null || true
  fi
  return "$status"
}
trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

if ! mkdir "$LOCK_DIR"; then
  fail "another writer owns RESULT_DIR or left its lock."
fi
LOCK_HELD=1

cp "$PARENT_MANIFEST_SOURCE" "$HOST_WORK/current_parent.tsv"
cp "$ROOT/validation/iterative/continuation_policy.md" \
  "$ROOT/validation/iterative/continuation_radial.x2m" \
  "$ROOT/validation/iterative/continuation_axial.x2m" \
  "$ROOT/validation/iterative/check_one_map_xsm.f90" \
  "$ROOT/validation/iterative/run_bounded_dragon.py" \
  "$ROOT/validation/iterative/run_continuation_short.sh" \
  "$ROOT/data/SpotRefFS.c2m" "$ROOT/data/SpotPlaneFS.c2m" \
  "$HOST_WORK/"
PARENT_MANIFEST="$HOST_WORK/current_parent.tsv"

awk '
  NF && $1 !~ /^#/ {
    if (NF != 3) exit 1
    count++
  }
  END { if (count != 6) exit 1 }
' "$PARENT_MANIFEST" ||
  fail "parent manifest must contain exactly six three-field rows."
for role in axial_track axial_macrolib radial_track basis_reference \
  parent_axial parent_snapshots
do
  count=$(awk -v role="$role" '$1 == role { count++ } END { print count + 0 }' \
    "$PARENT_MANIFEST")
  test "$count" = 1 || fail "parent manifest role is missing or repeated: $role"
done

manifest_value() {
  awk -v role="$1" '$1 == role { print $2 }' "$PARENT_MANIFEST"
}

manifest_path() {
  awk -v role="$1" '$1 == role { print $3 }' "$PARENT_MANIFEST"
}

hash_file() {
  hash_output=$(shasum -a 256 "$1") || return 1
  digest=${hash_output%% *}
  printf '%s\n' "$digest" | rg -q '^[0-9a-f]{64}$' || return 1
  printf '%s\n' "$digest"
}

verify_hash() {
  role=$1
  path=$2
  expected=$(manifest_value "$role")
  actual=$(hash_file "$path") ||
    fail "cannot hash parent role: $role"
  test "$actual" = "$expected" ||
    fail "SHA256 mismatch for parent role: $role"
}

stage_parent() {
  role=$1
  target=$2
  expected=$(manifest_value "$role")
  rel=$(manifest_path "$role")
  printf '%s\n' "$expected" | rg -q '^[0-9a-f]{64}$' ||
    fail "invalid SHA256 for parent role: $role"
  case "$rel" in
    /*|.|..|../*|*/../*|*/..)
      fail "parent path must stay repo-relative: $role"
      ;;
  esac
  source_path="$ROOT/$rel"
  test -f "$source_path" && test ! -L "$source_path" ||
    fail "parent object is missing or is a symlink: $role"
  verify_hash "$role" "$source_path"
  cp "$source_path" "$RADIAL_WORK/$target"
  verify_hash "$role" "$RADIAL_WORK/$target"
}

stage_parent axial_track initial_axial_track.xsm
stage_parent axial_macrolib initial_axial_macrolib.xsm
stage_parent radial_track initial_radial_track.bin
stage_parent basis_reference basis_reference.xsm
stage_parent parent_axial parent_axial.xsm
stage_parent parent_snapshots parent_snapshots.xsm

cp "$HOST_WORK/SpotRefFS.c2m" "$HOST_WORK/SpotPlaneFS.c2m" \
  "$RADIAL_WORK/"
cp "$HOST_WORK/continuation_radial.x2m" \
  "$RADIAL_WORK/radial.x2m"
cp "$HOST_WORK/continuation_axial.x2m" \
  "$AXIAL_WORK/axial.x2m"

GANLIB_LIB_HASH_BEFORE=$(hash_file "$GANLIB_LIB") ||
  fail "cannot hash Ganlib library before checker compilation."
GANLIB_MOD_HASH_BEFORE=$(hash_file "$GANLIB_MOD/ganlib.mod") ||
  fail "cannot hash Ganlib module before checker compilation."
"$FC" -std=f2008 -O0 -Wall -Wextra -Werror -Wno-compare-reals \
  -ffp-contract=off -fno-fast-math -I "$GANLIB_MOD" \
  "$HOST_WORK/check_one_map_xsm.f90" \
  "$GANLIB_LIB" -lstdc++ -o "$AXIAL_WORK/check_one_map_xsm"

DRAGON_HASH_BEFORE=$(hash_file "$DRAGON_BIN") ||
  fail "cannot hash Dragon before map execution."

run_bounded() {
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH="$HOST_WORK" \
  python3 -c \
    'import sys; from pathlib import Path; from run_bounded_dragon import run; run(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), float(sys.argv[4]))' \
    "$DRAGON_BIN" "$1" "$2" "$3"
}

expect_count() {
  pattern=$1
  expected=$2
  file=$3
  count=$(rg -c "$pattern" "$file" || true)
  test "$count" = "$expected"
}

reject_abnormal_log() {
  if rg -i \
    'FLU2DR-DIAG|CONVERGENCE NOT REACHED|XABORT|ABORT:|FATAL|SIG(SEGV|FPE|BUS|ILL|ABRT)|fortran runtime error' \
    "$@" >/dev/null
  then
    return 1
  fi
}

MAP_STARTED=1
echo "SPOT-CONTINUATION RADIAL START: 120 s bound, no retry"
run_bounded "$RADIAL_WORK/radial.x2m" "$RADIAL_WORK/radial.log" \
  "$RADIAL_TIMEOUT_SECONDS"
echo "SPOT-CONTINUATION RADIAL END"

reject_abnormal_log "$RADIAL_WORK/radial.log"
expect_count '^ FLU2DR-TERM OUTER-GATE=PASS ' 3 "$RADIAL_WORK/radial.log"
expect_count '^ FLU2DR-TERM INNER-TERMINAL ' 3 "$RADIAL_WORK/radial.log"
expect_count 'normal end of execution for dragon' 1 "$RADIAL_WORK/radial.log"
expect_count '^SPOFSRC KEFF/QSUM/QMIN/QMAX ' 3 "$RADIAL_WORK/radial.log"
expect_count '^SPOFCHK L2/MAX/RBAL/MIN/QSUM ' 3 "$RADIAL_WORK/radial.log"
expect_count '^>\|CONT-RADIAL-CONTRACT ' 1 "$RADIAL_WORK/radial.log"
expect_count '^>\|CONT-RADIAL-COMPLETE ' 1 "$RADIAL_WORK/radial.log"
for file in candidate_system.xsm candidate_radial.xsm
do
  test -s "$RADIAL_WORK/$file" && test ! -L "$RADIAL_WORK/$file"
done

for file in initial_axial_track.xsm initial_axial_macrolib.xsm \
  basis_reference.xsm parent_axial.xsm candidate_system.xsm \
  candidate_radial.xsm
do
  cp "$RADIAL_WORK/$file" "$AXIAL_WORK/$file"
done

echo "SPOT-CONTINUATION AXIAL START: 80 s bound, no retry"
run_bounded "$AXIAL_WORK/axial.x2m" "$AXIAL_WORK/axial.log" \
  "$AXIAL_TIMEOUT_SECONDS"
echo "SPOT-CONTINUATION AXIAL END"

reject_abnormal_log "$RADIAL_WORK/radial.log" "$AXIAL_WORK/axial.log"
expect_count '^ FLU2DR-TERM OUTER-GATE=PASS ' 1 "$AXIAL_WORK/axial.log"
expect_count '^ FLU2DR-TERM INNER-TERMINAL ' 1 "$AXIAL_WORK/axial.log"
expect_count 'normal end of execution for dragon' 1 "$AXIAL_WORK/axial.log"
expect_count 'SPOGBAL GLOBAL/MAX-GROUP' 1 "$AXIAL_WORK/axial.log"
expect_count '^>\|CONT-RAW-DEFECT ' 1 "$AXIAL_WORK/axial.log"
expect_count '^>\|CONT-CANDIDATE ' 1 "$AXIAL_WORK/axial.log"
expect_count '^>\|CONT-AXIAL-COMPLETE ' 1 "$AXIAL_WORK/axial.log"
for file in candidate_axial.xsm candidate_snapshots.xsm
do
  test -s "$AXIAL_WORK/$file" && test ! -L "$AXIAL_WORK/$file"
done

(
  cd "$AXIAL_WORK"
  ./check_one_map_xsm --continued basis_reference.xsm \
    candidate_system.xsm parent_axial.xsm candidate_axial.xsm \
    candidate_snapshots.xsm >independent_check.log
)
expect_count '^ONE-MAP-XSM COMPLETE$' 1 \
  "$AXIAL_WORK/independent_check.log"

verify_hash axial_track "$RADIAL_WORK/initial_axial_track.xsm"
verify_hash axial_macrolib "$RADIAL_WORK/initial_axial_macrolib.xsm"
verify_hash radial_track "$RADIAL_WORK/initial_radial_track.bin"
verify_hash basis_reference "$RADIAL_WORK/basis_reference.xsm"
verify_hash parent_axial "$RADIAL_WORK/parent_axial.xsm"
verify_hash parent_snapshots "$RADIAL_WORK/parent_snapshots.xsm"
verify_hash axial_track "$AXIAL_WORK/initial_axial_track.xsm"
verify_hash axial_macrolib "$AXIAL_WORK/initial_axial_macrolib.xsm"
verify_hash basis_reference "$AXIAL_WORK/basis_reference.xsm"
verify_hash parent_axial "$AXIAL_WORK/parent_axial.xsm"

classification=$(
  PYTHONDONTWRITEBYTECODE=1 python3 -c '
import math
import re
import sys

marker = ">|CONT-RAW-DEFECT"
lines = [
    line
    for line in open(sys.argv[1], errors="replace")
    if line.startswith(marker)
]
if len(lines) != 1:
    raise SystemExit("expected exactly one raw-defect record")
token = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][+-]?\d+)?"
payload = lines[0][len(marker):].split("|>", 1)[0]
fields = re.findall(token, payload)
if len(fields) != 4:
    raise SystemExit("raw-defect record must contain four values")
values = [float(item.replace("D", "E").replace("d", "e")) for item in fields]
if not all(math.isfinite(item) and item >= 0.0 for item in values):
    raise SystemExit("raw-defect values must be finite and nonnegative")
candidate_marker = ">|CONT-CANDIDATE"
candidate_lines = [
    line
    for line in open(sys.argv[1], errors="replace")
    if line.startswith(candidate_marker)
]
if len(candidate_lines) != 1:
    raise SystemExit("expected exactly one candidate-state record")
candidate_payload = candidate_lines[0][len(candidate_marker):].split("|>", 1)[0]
candidate_fields = re.findall(token, candidate_payload)
if len(candidate_fields) != 3:
    raise SystemExit("candidate-state record must contain three values")
candidate = [
    float(item.replace("D", "E").replace("d", "e"))
    for item in candidate_fields
]
if (
    not all(math.isfinite(item) for item in candidate)
    or candidate[0] <= 0.0
    or candidate[1] < 0.0
    or candidate[2] < 0.0
):
    raise SystemExit("candidate state and balance must be finite and physical")
eps = 5.0e-7
passed = values[0] <= eps and values[1] <= eps and values[3] <= eps
print("TOLERANCE_MET" if passed else "VALID_NOT_MET")
' "$AXIAL_WORK/axial.log"
)
printf '%s\n' "$classification" >"$WORK/classification.txt"

rg '^>\|CONT-(RAW-DEFECT|CANDIDATE)|^SPOGBAL GLOBAL/MAX-GROUP' \
  "$AXIAL_WORK/axial.log"
DRAGON_HASH_AFTER=$(hash_file "$DRAGON_BIN") ||
  fail "cannot hash Dragon after map execution."
GANLIB_LIB_HASH_AFTER=$(hash_file "$GANLIB_LIB") ||
  fail "cannot hash Ganlib library after map execution."
GANLIB_MOD_HASH_AFTER=$(hash_file "$GANLIB_MOD/ganlib.mod") ||
  fail "cannot hash Ganlib module after map execution."
test "$DRAGON_HASH_AFTER" = "$DRAGON_HASH_BEFORE"
test "$GANLIB_LIB_HASH_AFTER" = "$GANLIB_LIB_HASH_BEFORE"
test "$GANLIB_MOD_HASH_AFTER" = "$GANLIB_MOD_HASH_BEFORE"
MAP_VALID=1

PUBLISH_DIR=$(mktemp -d "$RESULT_PARENT/.$RESULT_NAME.tmp.XXXXXX")
cp "$RADIAL_WORK/candidate_system.xsm" \
  "$RADIAL_WORK/candidate_radial.xsm" \
  "$RADIAL_WORK/radial.log" \
  "$AXIAL_WORK/candidate_axial.xsm" \
  "$AXIAL_WORK/candidate_snapshots.xsm" \
  "$AXIAL_WORK/axial.log" \
  "$AXIAL_WORK/independent_check.log" \
  "$PUBLISH_DIR/"
cp "$HOST_WORK/current_parent.tsv" \
  "$HOST_WORK/continuation_policy.md" \
  "$HOST_WORK/continuation_radial.x2m" \
  "$HOST_WORK/continuation_axial.x2m" \
  "$HOST_WORK/SpotRefFS.c2m" \
  "$HOST_WORK/SpotPlaneFS.c2m" \
  "$HOST_WORK/check_one_map_xsm.f90" \
  "$HOST_WORK/run_bounded_dragon.py" \
  "$HOST_WORK/run_continuation_short.sh" \
  "$PUBLISH_DIR/"
cp "$WORK/classification.txt" "$PUBLISH_DIR/classification.txt"
printf '%s  Dragon\n' "$DRAGON_HASH_BEFORE" >"$PUBLISH_DIR/dragon.sha256"
printf '%s  libGanlib.a\n' "$GANLIB_LIB_HASH_BEFORE" \
  >"$PUBLISH_DIR/ganlib.sha256"
printf '%s  ganlib.mod\n' "$GANLIB_MOD_HASH_BEFORE" \
  >>"$PUBLISH_DIR/ganlib.sha256"
(
  cd "$PUBLISH_DIR"
  shasum -a 256 \
    candidate_system.xsm candidate_radial.xsm candidate_axial.xsm \
    candidate_snapshots.xsm radial.log axial.log independent_check.log \
    current_parent.tsv continuation_policy.md continuation_radial.x2m \
    continuation_axial.x2m SpotRefFS.c2m SpotPlaneFS.c2m \
    check_one_map_xsm.f90 run_bounded_dragon.py \
    run_continuation_short.sh classification.txt dragon.sha256 \
    ganlib.sha256 \
    >result.sha256
  shasum -a 256 -c result.sha256
)
test ! -e "$RESULT_DIR" && test ! -L "$RESULT_DIR"
mv "$PUBLISH_DIR" "$RESULT_DIR"
SUCCESS=1
PUBLISH_DIR=

printf 'SPOT-CONTINUATION CLASSIFICATION: %s\n' "$classification"
printf 'SPOT-CONTINUATION RESULT: %s\n' "$RESULT_DIR"
