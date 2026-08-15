#!/bin/sh
set -eu

RUN_RANK2_AXIAL_ONLY=${RUN_RANK2_AXIAL_ONLY:-0}
case "$RUN_RANK2_AXIAL_ONLY" in
  0)
    echo "SPOT-RANK2-AXIAL-ONLY DEFAULT-OFF: no Dragon process started."
    exit 0
    ;;
  1) ;;
  *)
    echo "SPOT-RANK2-AXIAL-ONLY ERROR: RUN_RANK2_AXIAL_ONLY must be 0 or 1." >&2
    exit 2
    ;;
esac

fail() {
  printf 'SPOT-RANK2-AXIAL-ONLY ERROR: %s\n' "$1" >&2
  exit 2
}

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
DRAGON_BIN=${DRAGON_BIN:-"$ROOT/bin/Darwin_arm64/Dragon"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}
RESULT_DIR=${RESULT_DIR:-}
PARENT_MANIFEST_SOURCE="$ROOT/validation/iterative/rank2_axial_only_parent.tsv"
POLICY_SOURCE="$ROOT/validation/iterative/rank2_axial_only_policy.md"
PRIOR_RESULT_SOURCE="$ROOT/validation/iterative/rank2_map_attempt_result.md"
RUNNER_SOURCE="$ROOT/validation/iterative/run_rank2_axial_only.sh"
STAGING_DIR="$ROOT/validation/artifacts/iterative-rank2-radial-staging"
AXIAL_TIMEOUT_SECONDS=420

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
for source_file in "$PARENT_MANIFEST_SOURCE" "$POLICY_SOURCE" \
  "$PRIOR_RESULT_SOURCE" "$RUNNER_SOURCE"
do
  test -f "$source_file" && test ! -L "$source_file" ||
    fail "tracked axial-only source is missing or is a symlink."
done
test -f "$DRAGON_BIN" && test ! -L "$DRAGON_BIN" && test -x "$DRAGON_BIN" ||
  fail "Dragon must be an executable non-symlink file."
test -f "$GANLIB_LIB" && test ! -L "$GANLIB_LIB" ||
  fail "Ganlib library is missing or is a symlink."
test -f "$GANLIB_MOD/ganlib.mod" && test ! -L "$GANLIB_MOD/ganlib.mod" ||
  fail "Ganlib module is missing or is a symlink."
test -z "$(git -C "$ROOT" status --porcelain --untracked-files=normal)" ||
  fail "tracked worktree must be clean before the one authorized run."
SOURCE_COMMIT=$(git -C "$ROOT" rev-parse HEAD) ||
  fail "cannot identify the source commit."

hash_file() {
  hash_output=$(shasum -a 256 "$1") || return 1
  digest=${hash_output%% *}
  printf '%s\n' "$digest" | rg -q '^[0-9a-f]{64}$' || return 1
  printf '%s\n' "$digest"
}

awk '
  NF && $1 !~ /^#/ {
    if (NF != 3) exit 1
    count++
  }
  END { if (count != 11) exit 1 }
' "$PARENT_MANIFEST_SOURCE" ||
  fail "parent manifest must contain exactly eleven three-field rows."
for role in staging_receipt runtime_provenance candidate_system \
  candidate_radial rank2_parent axial_track axial_macrolib basis_reference \
  axial_deck checker_source bounded_runner
do
  count=$(awk -v role="$role" '$1 == role { count++ } END { print count + 0 }' \
    "$PARENT_MANIFEST_SOURCE")
  test "$count" = 1 || fail "parent role is missing or repeated: $role"
done

manifest_value() {
  awk -v role="$1" '$1 == role { print $2 }' "$PARENT_MANIFEST_SOURCE"
}

manifest_path() {
  awk -v role="$1" '$1 == role { print $3 }' "$PARENT_MANIFEST_SOURCE"
}

source_path() {
  rel=$(manifest_path "$1")
  case "$rel" in
    /*|.|..|../*|*/../*|*/..)
      fail "parent path must stay repo-relative: $1"
      ;;
  esac
  printf '%s/%s\n' "$ROOT" "$rel"
}

verify_source() {
  role=$1
  path=$(source_path "$role")
  expected=$(manifest_value "$role")
  printf '%s\n' "$expected" | rg -q '^[0-9a-f]{64}$' ||
    fail "invalid parent hash: $role"
  test -f "$path" && test ! -L "$path" ||
    fail "parent object is missing or is a symlink: $role"
  actual=$(hash_file "$path") || fail "cannot hash parent object: $role"
  test "$actual" = "$expected" || fail "parent hash mismatch: $role"
}

for role in staging_receipt runtime_provenance candidate_system \
  candidate_radial rank2_parent axial_track axial_macrolib basis_reference \
  axial_deck checker_source bounded_runner
do
  verify_source "$role"
done

WORK=
SUCCESS=0
MAP_STARTED=0
MAP_VALID=0
LOCK_HELD=0
classification=

cleanup() {
  status=$?
  if [ "$SUCCESS" != 1 ] && [ -n "$WORK" ] && [ -d "$WORK" ]; then
    if [ "$MAP_STARTED" = 1 ]; then
      if [ "$MAP_VALID" = 1 ]; then
        printf 'SPOT-RANK2-AXIAL-ONLY CLASSIFICATION: %s\n' \
          "$classification" >&2
        printf '%s\n' \
          "SPOT-RANK2-AXIAL-ONLY PUBLICATION FAIL: valid map retained in workdir." >&2
      else
        printf '%s\n' \
          "SPOT-RANK2-AXIAL-ONLY INVALID_MAP: no result was published." >&2
      fi
      printf 'SPOT-RANK2-AXIAL-ONLY WORKDIR: %s\n' "$WORK" >&2
    else
      rm -rf "$WORK"
    fi
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
WORK=$(mktemp -d "$RESULT_PARENT/.$RESULT_NAME.work.XXXXXX")

stage_input() {
  role=$1
  target=$2
  source=$(source_path "$role")
  cp "$source" "$WORK/$target"
  actual=$(hash_file "$WORK/$target") || fail "cannot hash staged input: $role"
  test "$actual" = "$(manifest_value "$role")" ||
    fail "staged input hash mismatch: $role"
}

stage_input staging_receipt source_staging.sha256
stage_input runtime_provenance runtime_provenance.tsv
stage_input candidate_system candidate_system.xsm
stage_input candidate_radial candidate_radial.xsm
stage_input rank2_parent rank2_parent_axial.xsm
stage_input axial_track initial_axial_track.xsm
stage_input axial_macrolib initial_axial_macrolib.xsm
stage_input basis_reference basis_reference.xsm
stage_input axial_deck axial.x2m
stage_input checker_source check_one_map_xsm.f90
stage_input bounded_runner run_bounded_dragon.py
cp "$PARENT_MANIFEST_SOURCE" "$WORK/parent_manifest.tsv"
cp "$POLICY_SOURCE" "$WORK/rank2_axial_only_policy.md"
cp "$PRIOR_RESULT_SOURCE" "$WORK/prior_attempt_result.md"
cp "$RUNNER_SOURCE" "$WORK/run_rank2_axial_only.sh"
printf '%s\n' "$SOURCE_COMMIT" >"$WORK/source_commit.txt"
printf '%s\n' \
  'attempt_number=2' \
  'mathematical_map=G2(C2(raw_x7))' \
  'radial_solve_count=0' \
  'axial_solve_count=1' \
  'retry_count=0' \
  "wall_bound_seconds=$AXIAL_TIMEOUT_SECONDS" \
  'solver_tolerance=5.0e-7' >"$WORK/attempt_config.txt"

(
  cd "$STAGING_DIR"
  shasum -a 256 -c staging.sha256
) >"$WORK/source_staging_check.log" ||
  fail "frozen radial staging receipt failed."

runtime_value() {
  awk -v role="$1" '$1 == role { print $2 }' "$WORK/runtime_provenance.tsv"
}

verify_runtime() {
  role=$1
  path=$2
  expected=$(runtime_value "$role")
  actual=$(hash_file "$path") || fail "cannot hash runtime object: $role"
  test "$actual" = "$expected" || fail "runtime hash mismatch: $role"
}

verify_runtime dragon "$DRAGON_BIN"
verify_runtime ganlib_archive "$GANLIB_LIB"
verify_runtime ganlib_module "$GANLIB_MOD/ganlib.mod"
DRAGON_HASH_BEFORE=$(hash_file "$DRAGON_BIN")
GANLIB_LIB_HASH_BEFORE=$(hash_file "$GANLIB_LIB")
GANLIB_MOD_HASH_BEFORE=$(hash_file "$GANLIB_MOD/ganlib.mod")

"$FC" -std=f2008 -O0 -Wall -Wextra -Werror -Wno-compare-reals \
  -ffp-contract=off -fno-fast-math -I "$GANLIB_MOD" \
  "$WORK/check_one_map_xsm.f90" "$GANLIB_LIB" -lstdc++ \
  -o "$WORK/check_one_map_xsm.bin"

MAP_STARTED=1
printf 'SPOT-RANK2-AXIAL-ONLY START: %s s host bound, no radial solve, no retry\n' \
  "$AXIAL_TIMEOUT_SECONDS"
if PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$WORK" python3 -c \
    'import sys; from pathlib import Path; from run_bounded_dragon import run; run(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), float(sys.argv[4]))' \
    "$DRAGON_BIN" "$WORK/axial.x2m" "$WORK/axial.log" \
    "$AXIAL_TIMEOUT_SECONDS" >"$WORK/bounded.stdout" 2>"$WORK/bounded.stderr"
then
  wrapper_status=0
else
  wrapper_status=$?
  printf 'wrapper_exit_status\t%s\nwall_bound_seconds\t%s\n' \
    "$wrapper_status" "$AXIAL_TIMEOUT_SECONDS" >"$WORK/wrapper_status.tsv"
  fail "bounded axial process failed; no scientific result."
fi
printf 'wrapper_exit_status\t0\nwall_bound_seconds\t%s\n' \
  "$AXIAL_TIMEOUT_SECONDS" >"$WORK/wrapper_status.tsv"
echo "SPOT-RANK2-AXIAL-ONLY DRAGON END"

expect_count() {
  pattern=$1
  expected=$2
  file=$3
  count=$(rg -c "$pattern" "$file" || true)
  test "$count" = "$expected" ||
    fail "unexpected log count for pattern: $pattern"
}

if rg -i \
  'FLU2DR-DIAG|CONVERGENCE NOT REACHED|XABORT|ABORT:|FATAL|SIG(SEGV|FPE|BUS|ILL|ABRT)|fortran runtime error' \
  "$WORK/axial.log" >/dev/null
then
  fail "axial log contains an abnormal marker."
fi
expect_count '^ FLU2DR-TERM OUTER-GATE=PASS ' 1 "$WORK/axial.log"
expect_count '^ FLU2DR-TERM INNER-TERMINAL ' 1 "$WORK/axial.log"
expect_count 'normal end of execution for dragon' 1 "$WORK/axial.log"
expect_count 'SPOGBAL GLOBAL/MAX-GROUP' 1 "$WORK/axial.log"
expect_count '^>\|CONT-RAW-DEFECT ' 1 "$WORK/axial.log"
expect_count '^>\|CONT-CANDIDATE ' 1 "$WORK/axial.log"
expect_count '^>\|CONT-AXIAL-COMPLETE ' 1 "$WORK/axial.log"
for file in candidate_axial.xsm candidate_snapshots.xsm
do
  test -s "$WORK/$file" && test ! -L "$WORK/$file" ||
    fail "candidate output is missing or is a symlink: $file"
done

(
  cd "$WORK"
  ./check_one_map_xsm.bin --reencoded basis_reference.xsm \
    candidate_system.xsm rank2_parent_axial.xsm candidate_axial.xsm \
    candidate_snapshots.xsm >independent_check.log
)
expect_count '^ONE-MAP-XSM COMPLETE$' 1 "$WORK/independent_check.log"

classification=$(
  PYTHONDONTWRITEBYTECODE=1 python3 -c '
import math
import re
import sys

token = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][+-]?\d+)?"

def one(marker, count):
    lines = [line for line in open(sys.argv[1], errors="replace")
             if line.startswith(marker)]
    if len(lines) != 1:
        raise SystemExit(f"expected exactly one {marker} record")
    fields = re.findall(token, lines[0][len(marker):].split("|>", 1)[0])
    if len(fields) != count:
        raise SystemExit(f"unexpected field count for {marker}")
    return [float(item.replace("D", "E").replace("d", "e"))
            for item in fields]

defects = one(">|CONT-RAW-DEFECT", 4)
candidate = one(">|CONT-CANDIDATE", 3)
if not all(math.isfinite(item) and item >= 0.0 for item in defects):
    raise SystemExit("defects must be finite and nonnegative")
if (not all(math.isfinite(item) for item in candidate)
        or candidate[0] <= 0.0 or candidate[1] < 0.0
        or candidate[2] < 0.0):
    raise SystemExit("candidate state must be finite and physical")
eps = 5.0e-7
passed = defects[0] <= eps and defects[1] <= eps and defects[3] <= eps
print("TOLERANCE_MET" if passed else "VALID_NOT_MET")
' "$WORK/axial.log"
)
printf '%s\n' "$classification" >"$WORK/classification.txt"

for role in staging_receipt runtime_provenance candidate_system \
  candidate_radial rank2_parent axial_track axial_macrolib basis_reference \
  axial_deck checker_source bounded_runner
do
  verify_source "$role"
done
for binding in \
  'candidate_system candidate_system.xsm' \
  'candidate_radial candidate_radial.xsm' \
  'rank2_parent rank2_parent_axial.xsm' \
  'axial_track initial_axial_track.xsm' \
  'axial_macrolib initial_axial_macrolib.xsm' \
  'basis_reference basis_reference.xsm' \
  'axial_deck axial.x2m' \
  'checker_source check_one_map_xsm.f90' \
  'bounded_runner run_bounded_dragon.py'
do
  set -- $binding
  actual=$(hash_file "$WORK/$2") || fail "cannot rehash staged input: $1"
  test "$actual" = "$(manifest_value "$1")" ||
    fail "staged input changed during the attempt: $1"
done
verify_runtime dragon "$DRAGON_BIN"
verify_runtime ganlib_archive "$GANLIB_LIB"
verify_runtime ganlib_module "$GANLIB_MOD/ganlib.mod"
test "$(hash_file "$DRAGON_BIN")" = "$DRAGON_HASH_BEFORE"
test "$(hash_file "$GANLIB_LIB")" = "$GANLIB_LIB_HASH_BEFORE"
test "$(hash_file "$GANLIB_MOD/ganlib.mod")" = "$GANLIB_MOD_HASH_BEFORE"
MAP_VALID=1

printf '%s  Dragon\n' "$DRAGON_HASH_BEFORE" >"$WORK/dragon.sha256"
printf '%s  libGanlib.a\n' "$GANLIB_LIB_HASH_BEFORE" >"$WORK/ganlib.sha256"
printf '%s  ganlib.mod\n' "$GANLIB_MOD_HASH_BEFORE" >>"$WORK/ganlib.sha256"
rm "$WORK/check_one_map_xsm.bin"
(
  cd "$WORK"
  shasum -a 256 \
    attempt_config.txt axial.log axial.x2m basis_reference.xsm \
    bounded.stderr bounded.stdout candidate_axial.xsm candidate_radial.xsm \
    candidate_snapshots.xsm candidate_system.xsm check_one_map_xsm.f90 \
    classification.txt dragon.sha256 ganlib.sha256 independent_check.log \
    initial_axial_macrolib.xsm initial_axial_track.xsm parent_manifest.tsv \
    prior_attempt_result.md rank2_axial_only_policy.md \
    rank2_parent_axial.xsm run_bounded_dragon.py \
    run_rank2_axial_only.sh runtime_provenance.tsv source_commit.txt \
    source_staging.sha256 source_staging_check.log wrapper_status.tsv \
    >result.sha256
  shasum -a 256 -c result.sha256
)

test ! -e "$RESULT_DIR" && test ! -L "$RESULT_DIR" ||
  fail "RESULT_DIR appeared during the run."
mv "$WORK" "$RESULT_DIR"
WORK="$RESULT_DIR"
SUCCESS=1
printf 'SPOT-RANK2-AXIAL-ONLY CLASSIFICATION: %s\n' "$classification"
printf 'SPOT-RANK2-AXIAL-ONLY RESULT: %s\n' "$RESULT_DIR"
