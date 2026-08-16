#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
MANIFEST=${MANIFEST:-"$ROOT/validation/iterative/rank2_latest_modal_aa1_candidate_inputs.tsv"}
ARTIFACT_DIR=${ARTIFACT_DIR:-"$ROOT/validation/artifacts/iterative-rank2-latest-modal-aa1-candidate"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}

BUILDER="$ROOT/validation/iterative/build_rank2_modal_aa1_candidate.f90"
CHECKER="$ROOT/validation/iterative/check_rank2_modal_aa1_candidate.f90"
RUNNER="$ROOT/validation/iterative/run_rank2_latest_modal_aa1_candidate.sh"
EXPECTED_AX_SHA=0c7d94c9df4b1a7f7f94b8a9d54eb51aacfcead8ab34d5f288c85351b1c0ab9d
EXPECTED_SNAP_SHA=b5d03cb519ce54f0ade469288f70a50e303bb6a7bd7d4396c04558d38ffd108b

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
  '# spot-rank2-latest-modal-aa1-candidate-inputs-v1'
bad_width=$(awk 'NF && $1 !~ /^#/ && NF != 3 { count++ } \
  END { print count + 0 }' "$MANIFEST")
test "$bad_width" = 0
for role in x2 x3 x4 x4_snapshots basis_reference
do
  count=$(awk -v role="$role" \
    '$1 == role { count++ } END { print count + 0 }' "$MANIFEST")
  test "$count" = 1
  expected=$(manifest_value "$role")
  relative=$(manifest_path "$role")
  printf '%s\n' "$expected" | rg -q '^[0-9a-f]{64}$'
  case "$relative" in
    /*|.|..|../*|*/../*|*/..)
      printf 'RANK2-LATEST-AA1 ERROR: unsafe path for %s\n' "$role" >&2
      exit 2
      ;;
  esac
  source_path="$ROOT/$relative"
  test -f "$source_path" && test ! -L "$source_path"
  test "$(hash_file "$source_path")" = "$expected"
done

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-rank2-latest-aa1.XXXXXX")
STAGE="$(dirname "$ARTIFACT_DIR")/.rank2-latest-modal-aa1.$$"
cleanup() {
  rm -rf "$WORK"
  if test -d "$STAGE"; then rm -rf "$STAGE"; fi
}
trap cleanup EXIT HUP INT TERM

for binding in x2:x2 x3:x3 x4:x4 x4s:x4_snapshots basis:basis_reference
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
  printf '%s\n' 'RANK2-LATEST-AA1 ERROR: forbidden solver symbol.' >&2
  exit 2
fi

(
  cd "$WORK"
  ./build_candidate --consecutive-returned \
    x2.xsm x3.xsm x4.xsm x4s.xsm \
    proposal_axial.xsm proposal_snapshots.xsm > build.log
  ./check_candidate --consecutive-returned \
    x2.xsm x3.xsm x4.xsm x4s.xsm basis.xsm \
    proposal_axial.xsm proposal_snapshots.xsm > check.log
)
rg -q '^RANK2-LATEST-AA1 PROPOSAL COMPLETE NOT-EVALUATED NO-DRAGON NO-MAP$' \
  "$WORK/build.log"
rg -q '^RANK2-LATEST-AA1 COMPLETE$' "$WORK/check.log"

for role in x2 x3 x4 x4_snapshots basis_reference
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
cp "$RUNNER" "$STAGE/run_rank2_latest_modal_aa1_candidate.sh"
printf '%s\n' 'MATERIALIZED_PROPOSAL_NOT_EVALUATED' \
  > "$STAGE/classification.txt"
(
  cd "$STAGE"
  shasum -a 256 \
    proposal_axial.xsm proposal_snapshots.xsm build.log check.log \
    input_manifest.tsv build_rank2_modal_aa1_candidate.f90 \
    check_rank2_modal_aa1_candidate.f90 \
    run_rank2_latest_modal_aa1_candidate.sh classification.txt \
    > result.sha256
  shasum -a 256 -c result.sha256 >/dev/null
)
mv "$STAGE" "$ARTIFACT_DIR"

cat "$ARTIFACT_DIR/build.log"
cat "$ARTIFACT_DIR/check.log"
printf '%s\n' \
  "RANK2-LATEST-AA1 AX-SHA256=$ax_sha" \
  "RANK2-LATEST-AA1 SNAP-SHA256=$snap_sha" \
  'RANK2-LATEST-AA1 INPUTS-READ-ONLY HASH PASS' \
  'RANK2-LATEST-AA1 DRAGON/ASM/FLU/TRANSPORT=0' \
  'RANK2-LATEST-AA1 CLASSIFICATION=MATERIALIZED_PROPOSAL_NOT_EVALUATED' \
  "RANK2-LATEST-AA1 RESULT=$ARTIFACT_DIR"
