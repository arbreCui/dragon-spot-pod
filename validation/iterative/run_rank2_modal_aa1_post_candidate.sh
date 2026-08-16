#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
MANIFEST=${MANIFEST:-"$ROOT/validation/iterative/rank2_modal_aa1_post_candidate_inputs.tsv"}
ARTIFACT_DIR=${ARTIFACT_DIR:-"$ROOT/validation/artifacts/iterative-rank2-modal-aa1-post-candidate"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}

BUILDER="$ROOT/validation/iterative/build_rank2_modal_aa1_candidate.f90"
CHECKER="$ROOT/validation/iterative/check_rank2_modal_aa1_candidate.f90"
RUNNER="$ROOT/validation/iterative/run_rank2_modal_aa1_post_candidate.sh"
EXPECTED_AX_SHA=58972931170d744f109550866b65a8d2cbf22204ef1fe99cef634c4187d59d89
EXPECTED_SNAP_SHA=0c22cc9748beb813757d154ca592f343654e61c710f9b852ad35270ae19e186c

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
test "$rows" = 6
test "$(sed -n '1p' "$MANIFEST")" = \
  '# spot-rank2-modal-aa1-post-candidate-inputs-v1'
bad_width=$(awk 'NF && $1 !~ /^#/ && NF != 3 { count++ } \
  END { print count + 0 }' "$MANIFEST")
test "$bad_width" = 0
for role in x2 x3 aa1_pub aa1_plus aa1_plus_snapshots basis_reference
do
  count=$(awk -v role="$role" \
    '$1 == role { count++ } END { print count + 0 }' "$MANIFEST")
  test "$count" = 1
  expected=$(manifest_value "$role")
  relative=$(manifest_path "$role")
  printf '%s\n' "$expected" | rg -q '^[0-9a-f]{64}$'
  case "$relative" in
    /*|.|..|../*|*/../*|*/..)
      printf 'RANK2-POST-AA1 ERROR: unsafe path for %s\n' "$role" >&2
      exit 2
      ;;
  esac
  source_path="$ROOT/$relative"
  test -f "$source_path" && test ! -L "$source_path"
  test "$(hash_file "$source_path")" = "$expected"
done

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-rank2-post-aa1.XXXXXX")
STAGE="$(dirname "$ARTIFACT_DIR")/.rank2-modal-aa1-post-candidate.$$"
cleanup() {
  rm -rf "$WORK"
  if test -d "$STAGE"; then rm -rf "$STAGE"; fi
}
trap cleanup EXIT HUP INT TERM

for binding in x2:x2 x3:x3 aa1:aa1_pub aa1p:aa1_plus \
  aa1ps:aa1_plus_snapshots basis:basis_reference
do
  short=${binding%%:*}
  role=${binding#*:}
  ln -s "$ROOT/$(manifest_path "$role")" "$WORK/$short.xsm"
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
  printf '%s\n' 'RANK2-POST-AA1 ERROR: forbidden solver symbol.' >&2
  exit 2
fi

(
  cd "$WORK"
  ./build_candidate --post-aa1 x2.xsm x3.xsm aa1.xsm aa1p.xsm \
    aa1ps.xsm proposal_axial.xsm proposal_snapshots.xsm > build.log
  ./check_candidate --post-aa1 x2.xsm x3.xsm aa1.xsm aa1p.xsm \
    aa1ps.xsm basis.xsm proposal_axial.xsm proposal_snapshots.xsm \
    > check.log
)

for role in x2 x3 aa1_pub aa1_plus aa1_plus_snapshots basis_reference
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
cp "$RUNNER" "$STAGE/run_rank2_modal_aa1_post_candidate.sh"
printf '%s\n' 'MATERIALIZED_PROPOSAL_NOT_EVALUATED' \
  > "$STAGE/classification.txt"
(
  cd "$STAGE"
  shasum -a 256 \
    proposal_axial.xsm proposal_snapshots.xsm build.log check.log \
    input_manifest.tsv build_rank2_modal_aa1_candidate.f90 \
    check_rank2_modal_aa1_candidate.f90 \
    run_rank2_modal_aa1_post_candidate.sh classification.txt \
    > result.sha256
  shasum -a 256 -c result.sha256 >/dev/null
)
mv "$STAGE" "$ARTIFACT_DIR"

cat "$ARTIFACT_DIR/build.log"
cat "$ARTIFACT_DIR/check.log"
printf '%s\n' \
  "RANK2-POST-AA1 AX-SHA256=$ax_sha" \
  "RANK2-POST-AA1 SNAP-SHA256=$snap_sha" \
  'RANK2-POST-AA1 INPUTS-READ-ONLY HASH PASS' \
  'RANK2-POST-AA1 DRAGON/ASM/FLU/TRANSPORT=0' \
  'RANK2-POST-AA1 CLASSIFICATION=MATERIALIZED_PROPOSAL_NOT_EVALUATED' \
  "RANK2-POST-AA1 RESULT=$ARTIFACT_DIR"
