#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
MANIFEST=${MANIFEST:-"$ROOT/validation/iterative/rank2_current_aa2_candidate_inputs.tsv"}
ARTIFACT_DIR=${ARTIFACT_DIR:-"$ROOT/validation/artifacts/iterative-rank2-current-aa2-candidate"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}
CANDIDATE_MODE=${CANDIDATE_MODE:---current-aa2}
REPORT_PREFIX=${REPORT_PREFIX:-RANK2-CURRENT-AA2}
MANIFEST_HEADER=${MANIFEST_HEADER:-'# spot-rank2-current-aa2-candidate-inputs-v1'}

BUILDER="$ROOT/validation/iterative/build_rank2_modal_aa1_candidate.f90"
CHECKER="$ROOT/validation/iterative/check_rank2_modal_aa1_candidate.f90"
RUNNER="$ROOT/validation/iterative/run_rank2_current_aa2_candidate.sh"
EXPECTED_AX_SHA=dc2251e13fa473ceebee7839c32bd5b3244498134a8acfab93b39c55b1e79469
EXPECTED_SNAP_SHA=87ed9359809608c838991d2743914a47d96741fc94cedc07d06d512735970b63
expected_ax_sha=$EXPECTED_AX_SHA
expected_snap_sha=$EXPECTED_SNAP_SHA

case "$CANDIDATE_MODE" in
  --current-aa2)
    test "$REPORT_PREFIX" = 'RANK2-CURRENT-AA2'
    test "$MANIFEST_HEADER" = \
      '# spot-rank2-current-aa2-candidate-inputs-v1'
    ;;
  --current-ghi-aa2)
    test "$REPORT_PREFIX" = 'RANK2-CURRENT-GHI-AA2'
    test "$MANIFEST_HEADER" = \
      '# spot-rank2-current-ghi-aa2-candidate-inputs-v1'
    expected_ax_sha=${EXPECTED_AX_SHA_OVERRIDE:-}
    expected_snap_sha=${EXPECTED_SNAP_SHA_OVERRIDE:-}
    for expected_sha in "$expected_ax_sha" "$expected_snap_sha"
    do
      printf '%s\n' "$expected_sha" | rg -q '^[0-9a-f]{64}$'
    done
    ;;
  *)
    printf '%s\n' 'AA2 candidate mode must be current or GHI.' >&2
    exit 2
    ;;
esac

for file in "$MANIFEST" "$BUILDER" "$CHECKER" "$RUNNER" \
  "$GANLIB_LIB" "$GANLIB_MOD/ganlib.mod"
do
  test -f "$file" && test ! -L "$file"
done
test ! -e "$ARTIFACT_DIR" && test ! -L "$ARTIFACT_DIR"
mkdir -p "$(dirname "$ARTIFACT_DIR")"

hash_file() {
  output=$(shasum -a 256 "$1")
  digest=${output%% *}
  printf '%s\n' "$digest" | rg -q '^[0-9a-f]{64}$'
  printf '%s\n' "$digest"
}

manifest_value() {
  awk -v role="$1" '$1 == role {print $2}' "$MANIFEST"
}

manifest_path() {
  awk -v role="$1" '$1 == role {print $3}' "$MANIFEST"
}

test "$(sed -n '1p' "$MANIFEST")" = "$MANIFEST_HEADER"
test "$(awk 'NF && $1 !~ /^#/ {n++} END {print n+0}' "$MANIFEST")" = 8
test "$(awk 'NF && $1 !~ /^#/ && NF != 3 {n++} END {print n+0}' \
  "$MANIFEST")" = 0
for role in w x c d y e e_snapshots basis_reference
do
  test "$(awk -v role="$role" '$1 == role {n++} END {print n+0}' \
    "$MANIFEST")" = 1
  expected=$(manifest_value "$role")
  relative=$(manifest_path "$role")
  printf '%s\n' "$expected" | rg -q '^[0-9a-f]{64}$'
  case "$relative" in
    /*|.|..|../*|*/../*|*/..) exit 2 ;;
  esac
  test -f "$ROOT/$relative" && test ! -L "$ROOT/$relative"
  test "$(hash_file "$ROOT/$relative")" = "$expected"
done

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-rank2-current-aa2.XXXXXX")
STAGE="$(dirname "$ARTIFACT_DIR")/.rank2-current-aa2.$$"
cleanup() {
  rm -rf "$WORK"
  if test -d "$STAGE"; then rm -rf "$STAGE"; fi
}
trap cleanup EXIT HUP INT TERM

for role in w x c d y e e_snapshots basis_reference
do
  ln -s "$ROOT/$(manifest_path "$role")" "$WORK/$role.xsm"
done

FLAGS='-std=f2008 -O0 -g -pedantic -Wall -Wextra -Werror -Wno-compare-reals -fcheck=all -ffp-contract=off -fno-fast-math'
# shellcheck disable=SC2086
"$FC" $FLAGS -I "$GANLIB_MOD" "$BUILDER" \
  "$GANLIB_LIB" -lstdc++ -o "$WORK/build_candidate"
# shellcheck disable=SC2086
"$FC" $FLAGS -I "$GANLIB_MOD" "$CHECKER" \
  "$GANLIB_LIB" -lstdc++ -o "$WORK/check_candidate"

nm "$WORK/build_candidate" >"$WORK/builder.nm"
nm "$WORK/check_candidate" >"$WORK/checker.nm"
if rg -qi \
  '(_|[[:space:]])(asm|flu|dragon|spoasm|spoproj|spostate|spoxconv|spopod)(_|[[:space:]]|$)' \
  "$WORK/builder.nm" "$WORK/checker.nm"
then
  printf '%s\n' "$REPORT_PREFIX ERROR: forbidden solver symbol." >&2
  exit 2
fi

(
  cd "$WORK"
  ./build_candidate "$CANDIDATE_MODE" w.xsm x.xsm c.xsm d.xsm y.xsm \
    e.xsm e_snapshots.xsm proposal_axial.xsm proposal_snapshots.xsm \
    >build.log
  ./check_candidate "$CANDIDATE_MODE" w.xsm x.xsm c.xsm d.xsm y.xsm \
    e.xsm e_snapshots.xsm basis_reference.xsm proposal_axial.xsm \
    proposal_snapshots.xsm >check.log
)
if test "$CANDIDATE_MODE" = '--current-ghi-aa2'; then
  rg -q "^$REPORT_PREFIX PARAMETER-FREE DIRECTION GATE PASS$" \
    "$WORK/build.log" "$WORK/check.log"
fi
rg -q "^$REPORT_PREFIX CARRIER AA2-RAW-FLUX$" "$WORK/build.log"
rg -q "^$REPORT_PREFIX COMPLETE$" "$WORK/check.log"

for role in w x c d y e e_snapshots basis_reference
do
  test "$(hash_file "$ROOT/$(manifest_path "$role")")" = \
    "$(manifest_value "$role")"
done
ax_sha=$(hash_file "$WORK/proposal_axial.xsm")
snap_sha=$(hash_file "$WORK/proposal_snapshots.xsm")
test "$ax_sha" = "$expected_ax_sha"
test "$snap_sha" = "$expected_snap_sha"

mkdir "$STAGE"
cp "$WORK/proposal_axial.xsm" "$STAGE/proposal_axial.xsm"
cp "$WORK/proposal_snapshots.xsm" "$STAGE/proposal_snapshots.xsm"
cp "$WORK/build.log" "$STAGE/build.log"
cp "$WORK/check.log" "$STAGE/check.log"
cp "$MANIFEST" "$STAGE/input_manifest.tsv"
cp "$BUILDER" "$STAGE/build_rank2_modal_aa1_candidate.f90"
cp "$CHECKER" "$STAGE/check_rank2_modal_aa1_candidate.f90"
cp "$RUNNER" "$STAGE/run_rank2_current_aa2_candidate.sh"
printf '%s\n' 'MATERIALIZED_PROPOSAL_NOT_EVALUATED' \
  >"$STAGE/classification.txt"
(
  cd "$STAGE"
  shasum -a 256 proposal_axial.xsm proposal_snapshots.xsm build.log \
    check.log input_manifest.tsv build_rank2_modal_aa1_candidate.f90 \
    check_rank2_modal_aa1_candidate.f90 \
    run_rank2_current_aa2_candidate.sh classification.txt >result.sha256
  test "$(wc -l <result.sha256 | tr -d ' ')" = 9
  shasum -a 256 -c result.sha256 >/dev/null
)
mv "$STAGE" "$ARTIFACT_DIR"

cat "$ARTIFACT_DIR/build.log"
cat "$ARTIFACT_DIR/check.log"
printf '%s\n' \
  "$REPORT_PREFIX AX-SHA256=$ax_sha" \
  "$REPORT_PREFIX SNAP-SHA256=$snap_sha" \
  "$REPORT_PREFIX INPUTS-READ-ONLY HASH PASS" \
  "$REPORT_PREFIX RECEIPT 9/9 PASS" \
  "$REPORT_PREFIX DRAGON/ASM/FLU/TRANSPORT=0" \
  "$REPORT_PREFIX CLASSIFICATION=MATERIALIZED_PROPOSAL_NOT_EVALUATED" \
  "$REPORT_PREFIX RESULT=$ARTIFACT_DIR"
