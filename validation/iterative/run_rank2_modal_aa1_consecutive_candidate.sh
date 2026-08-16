#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
MANIFEST=${MANIFEST:-"$ROOT/validation/iterative/rank2_modal_aa1_consecutive_candidate_inputs.tsv"}
ARTIFACT_DIR=${ARTIFACT_DIR:-"$ROOT/validation/artifacts/iterative-rank2-modal-aa1-consecutive-candidate"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}

BUILDER="$ROOT/validation/iterative/build_rank2_modal_aa1_candidate.f90"
CHECKER="$ROOT/validation/iterative/check_rank2_modal_aa1_candidate.f90"
RUNNER="$ROOT/validation/iterative/run_rank2_modal_aa1_consecutive_candidate.sh"
EXPECTED_AX_SHA=7094d4dc57156aae8f0d0180bcac24bf02640f5de0435b46635151ed975186f1
EXPECTED_SNAP_SHA=ebd0d7f0ca762f907f6d767273298b80262039f22cc4b36682d73a15d34065b2

for path in "$MANIFEST" "$BUILDER" "$CHECKER" "$RUNNER" \
  "$GANLIB_LIB" "$GANLIB_MOD/ganlib.mod"
do
  test -f "$path" && test ! -L "$path"
done
test ! -e "$ARTIFACT_DIR"
mkdir -p "$(dirname "$ARTIFACT_DIR")"

hash_file() {
  hash_output=$(shasum -a 256 "$1")
  digest=${hash_output%% *}
  printf '%s\n' "$digest" | rg -q '^[0-9a-f]{64}$'
  printf '%s\n' "$digest"
}

manifest_value() {
  awk -v role="$1" '$1 == role { print $2 }' "$MANIFEST"
}

manifest_path() {
  awk -v role="$1" '$1 == role { print $3 }' "$MANIFEST"
}

rows=$(awk 'NF && $1 !~ /^#/ { count++ } END { print count + 0 }' \
  "$MANIFEST")
test "$rows" = 5
test "$(sed -n '1p' "$MANIFEST")" = \
  '# spot-rank2-modal-aa1-consecutive-candidate-inputs-v1'
bad_width=$(awk 'NF && $1 !~ /^#/ && NF != 3 { count++ } \
  END { print count + 0 }' "$MANIFEST")
test "$bad_width" = 0
for role in x1_pub x2 x3 x3_snapshots basis_reference
do
  count=$(awk -v role="$role" \
    '$1 == role { count++ } END { print count + 0 }' "$MANIFEST")
  test "$count" = 1
  expected=$(manifest_value "$role")
  relative=$(manifest_path "$role")
  printf '%s\n' "$expected" | rg -q '^[0-9a-f]{64}$'
  case "$relative" in
    /*|.|..|../*|*/../*|*/..)
      printf 'RANK2-CONSECUTIVE-AA1 ERROR: unsafe path for %s\n' \
        "$role" >&2
      exit 2
      ;;
  esac
  source_path="$ROOT/$relative"
  test -f "$source_path" && test ! -L "$source_path"
  test "$(hash_file "$source_path")" = "$expected"
done

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-rank2-aa1-consecutive.XXXXXX")
STAGE="$(dirname "$ARTIFACT_DIR")/.rank2-modal-aa1-consecutive.$$"
cleanup() {
  rm -rf "$WORK"
  if test -d "$STAGE"; then rm -rf "$STAGE"; fi
}
trap cleanup EXIT HUP INT TERM

ln -s "$ROOT/$(manifest_path x1_pub)" "$WORK/x1.xsm"
ln -s "$ROOT/$(manifest_path x2)" "$WORK/x2.xsm"
ln -s "$ROOT/$(manifest_path x3)" "$WORK/x3.xsm"
ln -s "$ROOT/$(manifest_path x3_snapshots)" "$WORK/x3s.xsm"
ln -s "$ROOT/$(manifest_path basis_reference)" "$WORK/basis.xsm"
for binding in x1:x1_pub x2:x2 x3:x3 x3s:x3_snapshots basis:basis_reference
do
  short=${binding%%:*}
  role=${binding#*:}
  test "$(hash_file "$WORK/$short.xsm")" = "$(manifest_value "$role")"
done

FLAGS='-std=f2008 -O0 -g -pedantic -Wall -Wextra -Werror -Wno-compare-reals -fcheck=all -ffp-contract=off -fno-fast-math'
"$FC" $FLAGS -I "$GANLIB_MOD" "$BUILDER" \
  "$GANLIB_LIB" -lstdc++ -o "$WORK/build_candidate"
"$FC" $FLAGS -I "$GANLIB_MOD" "$CHECKER" \
  "$GANLIB_LIB" -lstdc++ -o "$WORK/check_candidate"

nm "$WORK/build_candidate" > "$WORK/builder.nm"
nm "$WORK/check_candidate" > "$WORK/checker.nm"
if rg -qi \
  '(_|[[:space:]])(asm|flu|dragon|spoasm|spoproj|spostate|spoxconv|spopod)(_|[[:space:]]|$)' \
  "$WORK/builder.nm" "$WORK/checker.nm"
then
  printf '%s\n' 'RANK2-CONSECUTIVE-AA1 ERROR: forbidden solver symbol.' >&2
  exit 2
fi

(
  cd "$WORK"
  ./build_candidate --consecutive x1.xsm x2.xsm x3.xsm x3s.xsm \
    proposal_axial.xsm proposal_snapshots.xsm > build.log
  ./check_candidate --consecutive x1.xsm x2.xsm x3.xsm x3s.xsm \
    basis.xsm proposal_axial.xsm proposal_snapshots.xsm > check.log
)

for role in x1_pub x2 x3 x3_snapshots basis_reference
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
cp "$RUNNER" "$STAGE/run_rank2_modal_aa1_consecutive_candidate.sh"
printf '%s\n' 'MATERIALIZED_PROPOSAL_NOT_EVALUATED' \
  > "$STAGE/classification.txt"
(
  cd "$STAGE"
  shasum -a 256 \
    proposal_axial.xsm proposal_snapshots.xsm build.log check.log \
    input_manifest.tsv build_rank2_modal_aa1_candidate.f90 \
    check_rank2_modal_aa1_candidate.f90 \
    run_rank2_modal_aa1_consecutive_candidate.sh classification.txt \
    > result.sha256
  shasum -a 256 -c result.sha256 >/dev/null
)
mv "$STAGE" "$ARTIFACT_DIR"

cat "$ARTIFACT_DIR/build.log"
cat "$ARTIFACT_DIR/check.log"
printf '%s\n' \
  "RANK2-CONSECUTIVE-AA1 AX-SHA256=$ax_sha" \
  "RANK2-CONSECUTIVE-AA1 SNAP-SHA256=$snap_sha" \
  'RANK2-CONSECUTIVE-AA1 INPUTS-READ-ONLY HASH PASS' \
  'RANK2-CONSECUTIVE-AA1 DRAGON/ASM/FLU/TRANSPORT=0' \
  'RANK2-CONSECUTIVE-AA1 CLASSIFICATION=MATERIALIZED_PROPOSAL_NOT_EVALUATED' \
  "RANK2-CONSECUTIVE-AA1 RESULT=$ARTIFACT_DIR"
