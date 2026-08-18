#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
MANIFEST=${MANIFEST:-"$ROOT/validation/iterative/rank2_current_qvwx_zplus_aa1_candidate_inputs.tsv"}
ARTIFACT_DIR=${ARTIFACT_DIR:-"$ROOT/validation/artifacts/iterative-rank2-current-qvwx-zplus-aa1-candidate"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}

BUILDER="$ROOT/validation/iterative/build_rank2_modal_aa1_candidate.f90"
CHECKER="$ROOT/validation/iterative/check_rank2_modal_aa1_candidate.f90"
RUNNER="$ROOT/validation/iterative/run_rank2_current_qvwx_zplus_aa1_candidate.sh"
MODE=${MODE:---consecutive-qvwx-zplus-screened}
REPORT_PREFIX=${REPORT_PREFIX:-RANK2-QVWX-ZPLUS-AA1}
MANIFEST_HEADER=${MANIFEST_HEADER:-'# spot-rank2-current-qvwx-zplus-aa1-candidate-inputs-v1'}
PROPOSAL_ROLE=${PROPOSAL_ROLE:-y_aa1_pub}
PREVIOUS_ROLE=${PREVIOUS_ROLE:-z}
LATEST_ROLE=${LATEST_ROLE:-z_plus}
LATEST_SNAPSHOTS_ROLE=${LATEST_SNAPSHOTS_ROLE:-z_plus_snapshots}
BASIS_ROLE=${BASIS_ROLE:-basis_reference}

case "$MODE:$REPORT_PREFIX" in
  --consecutive-qvwx-zplus-screened:RANK2-QVWX-ZPLUS-AA1)
    test "$MANIFEST_HEADER" = \
      '# spot-rank2-current-qvwx-zplus-aa1-candidate-inputs-v1'
    EXPECTED_AX_SHA=${EXPECTED_AX_SHA:-5d462c634e7f909ff059d72ac8bb8d9240cb18c21232c682c99d8f34d791c67c}
    EXPECTED_SNAP_SHA=${EXPECTED_SNAP_SHA:-3c216fff2be1336c29e584e4b8b0d6d9eca537f80c6a5fc07bf08f4ad509eb84}
    ;;
  --consecutive-q5kl-screened:RANK2-CURRENT-KL-AA1)
    test "$MANIFEST_HEADER" = \
      '# spot-rank2-current-kl-aa1-candidate-inputs-v1'
    EXPECTED_AX_SHA=${EXPECTED_AX_SHA:-d223068dbabd5424762f6f73fb488a927cca94ca4db3cee7ef3bbf7f090d825d}
    EXPECTED_SNAP_SHA=${EXPECTED_SNAP_SHA:-c6c9546bb7807864aa2b0eaa56e289ee91ffa1ec4328b7889a5deb81d9b2cec6}
    ;;
  *) exit 2 ;;
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
test "$(awk 'NF && $1 !~ /^#/ {n++} END {print n+0}' "$MANIFEST")" = 5
test "$(awk 'NF && $1 !~ /^#/ && NF != 3 {n++} END {print n+0}' \
  "$MANIFEST")" = 0
for role in "$PROPOSAL_ROLE" "$PREVIOUS_ROLE" "$LATEST_ROLE" \
  "$LATEST_SNAPSHOTS_ROLE" "$BASIS_ROLE"
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

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-rank2-qvwx-zplus-aa1.XXXXXX")
STAGE="$(dirname "$ARTIFACT_DIR")/.rank2-qvwx-zplus-aa1.$$"
cleanup() {
  rm -rf "$WORK"
  if test -d "$STAGE"; then rm -rf "$STAGE"; fi
}
trap cleanup EXIT HUP INT TERM

for binding in y:"$PROPOSAL_ROLE" z:"$PREVIOUS_ROLE" zp:"$LATEST_ROLE" \
  zps:"$LATEST_SNAPSHOTS_ROLE" basis:"$BASIS_ROLE"
do
  short=${binding%%:*}
  role=${binding#*:}
  ln -s "$ROOT/$(manifest_path "$role")" "$WORK/$short.xsm"
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
  printf '%s\n' 'RANK2-QVWX-ZPLUS-AA1 ERROR: forbidden solver symbol.' >&2
  exit 2
fi

(
  cd "$WORK"
  ./build_candidate "$MODE" y.xsm z.xsm \
    zp.xsm zps.xsm proposal_axial.xsm proposal_snapshots.xsm >build.log
  ./check_candidate "$MODE" y.xsm z.xsm \
    zp.xsm zps.xsm basis.xsm proposal_axial.xsm \
    proposal_snapshots.xsm >check.log
)
rg -q "^$REPORT_PREFIX PARAMETER-FREE DIRECTION GATE PASS$" \
  "$WORK/build.log" "$WORK/check.log"
rg -q "^$REPORT_PREFIX CARRIER AA1-RAW-FLUX$" "$WORK/build.log"
rg -q "^$REPORT_PREFIX COMPLETE$" "$WORK/check.log"

for role in "$PROPOSAL_ROLE" "$PREVIOUS_ROLE" "$LATEST_ROLE" \
  "$LATEST_SNAPSHOTS_ROLE" "$BASIS_ROLE"
do
  test "$(hash_file "$ROOT/$(manifest_path "$role")")" = \
    "$(manifest_value "$role")"
done
ax_sha=$(hash_file "$WORK/proposal_axial.xsm")
snap_sha=$(hash_file "$WORK/proposal_snapshots.xsm")
test "$ax_sha" = "$EXPECTED_AX_SHA"
test "$snap_sha" = "$EXPECTED_SNAP_SHA"

mkdir "$STAGE"
cp "$WORK/proposal_axial.xsm" "$STAGE/proposal_axial.xsm"
cp "$WORK/proposal_snapshots.xsm" "$STAGE/proposal_snapshots.xsm"
cp "$WORK/build.log" "$STAGE/build.log"
cp "$WORK/check.log" "$STAGE/check.log"
cp "$MANIFEST" "$STAGE/input_manifest.tsv"
cp "$BUILDER" "$STAGE/build_rank2_modal_aa1_candidate.f90"
cp "$CHECKER" "$STAGE/check_rank2_modal_aa1_candidate.f90"
cp "$RUNNER" "$STAGE/run_rank2_current_qvwx_zplus_aa1_candidate.sh"
printf '%s\n' 'MATERIALIZED_PROPOSAL_NOT_EVALUATED' \
  >"$STAGE/classification.txt"
(
  cd "$STAGE"
  shasum -a 256 proposal_axial.xsm proposal_snapshots.xsm build.log \
    check.log input_manifest.tsv build_rank2_modal_aa1_candidate.f90 \
    check_rank2_modal_aa1_candidate.f90 \
    run_rank2_current_qvwx_zplus_aa1_candidate.sh classification.txt \
    >result.sha256
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
