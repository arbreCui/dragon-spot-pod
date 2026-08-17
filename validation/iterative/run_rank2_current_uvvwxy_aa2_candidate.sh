#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
MANIFEST=${MANIFEST:-"$ROOT/validation/iterative/rank2_current_uvvwxy_aa2_candidate_inputs.tsv"}
ARTIFACT_DIR=${ARTIFACT_DIR:-"$ROOT/validation/artifacts/iterative-rank2-current-uvvwxy-aa2-candidate"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}

BUILDER="$ROOT/validation/iterative/build_rank2_modal_aa1_candidate.f90"
CHECKER="$ROOT/validation/iterative/check_rank2_modal_aa1_candidate.f90"
RUNNER="$ROOT/validation/iterative/run_rank2_current_uvvwxy_aa2_candidate.sh"
EXPECTED_AX_SHA=68cac6d4968785e7cfa5a0bc5c90a6619bf0d9d31d203b75b440894bf472c194
EXPECTED_SNAP_SHA=44e00f71215c64985b8ab8a60646830ff9b5b239d2f42c0f8f87d510f4f1360b

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

test "$(sed -n '1p' "$MANIFEST")" = \
  '# spot-rank2-current-uvvwxy-aa2-candidate-inputs-v1'
test "$(awk 'NF && $1 !~ /^#/ {n++} END {print n+0}' "$MANIFEST")" = 7
test "$(awk 'NF && $1 !~ /^#/ && NF != 3 {n++} END {print n+0}' \
  "$MANIFEST")" = 0
for role in u_aa2_pub v w x_aa2_pub y y_snapshots basis_reference
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

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-rank2-current-uvvwxy-aa2.XXXXXX")
STAGE="$(dirname "$ARTIFACT_DIR")/.rank2-current-uvvwxy-aa2.$$"
cleanup() {
  rm -rf "$WORK"
  if test -d "$STAGE"; then rm -rf "$STAGE"; fi
}
trap cleanup EXIT HUP INT TERM

for binding in u:u_aa2_pub v:v w:w x:x_aa2_pub y:y ys:y_snapshots \
  basis:basis_reference
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
  printf '%s\n' 'RANK2-CURRENT-UVVWXY-AA2 ERROR: forbidden solver symbol.' >&2
  exit 2
fi

(
  cd "$WORK"
  ./build_candidate --current-uvvwxy-aa2 u.xsm v.xsm v.xsm w.xsm \
    x.xsm y.xsm ys.xsm proposal_axial.xsm proposal_snapshots.xsm \
    >build.log
  ./check_candidate --current-uvvwxy-aa2 u.xsm v.xsm v.xsm w.xsm \
    x.xsm y.xsm ys.xsm basis.xsm proposal_axial.xsm \
    proposal_snapshots.xsm >check.log
)
rg -q '^RANK2-CURRENT-UVVWXY-AA2 PARAMETER-FREE DIRECTION GATE PASS$' \
  "$WORK/build.log" "$WORK/check.log"
rg -q '^RANK2-CURRENT-UVVWXY-AA2 CARRIER AA2-RAW-FLUX$' \
  "$WORK/build.log"
rg -q '^RANK2-CURRENT-UVVWXY-AA2 COMPLETE$' "$WORK/check.log"

for role in u_aa2_pub v w x_aa2_pub y y_snapshots basis_reference
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
cp "$RUNNER" "$STAGE/run_rank2_current_uvvwxy_aa2_candidate.sh"
printf '%s\n' 'MATERIALIZED_PROPOSAL_NOT_EVALUATED' \
  >"$STAGE/classification.txt"
(
  cd "$STAGE"
  shasum -a 256 proposal_axial.xsm proposal_snapshots.xsm build.log \
    check.log input_manifest.tsv build_rank2_modal_aa1_candidate.f90 \
    check_rank2_modal_aa1_candidate.f90 \
    run_rank2_current_uvvwxy_aa2_candidate.sh classification.txt \
    >result.sha256
  test "$(wc -l <result.sha256 | tr -d ' ')" = 9
  shasum -a 256 -c result.sha256 >/dev/null
)
mv "$STAGE" "$ARTIFACT_DIR"

cat "$ARTIFACT_DIR/build.log"
cat "$ARTIFACT_DIR/check.log"
printf '%s\n' \
  "RANK2-CURRENT-UVVWXY-AA2 AX-SHA256=$ax_sha" \
  "RANK2-CURRENT-UVVWXY-AA2 SNAP-SHA256=$snap_sha" \
  'RANK2-CURRENT-UVVWXY-AA2 INPUTS-READ-ONLY HASH PASS' \
  'RANK2-CURRENT-UVVWXY-AA2 RECEIPT 9/9 PASS' \
  'RANK2-CURRENT-UVVWXY-AA2 DRAGON/ASM/FLU/TRANSPORT=0' \
  'RANK2-CURRENT-UVVWXY-AA2 CLASSIFICATION=MATERIALIZED_PROPOSAL_NOT_EVALUATED' \
  "RANK2-CURRENT-UVVWXY-AA2 RESULT=$ARTIFACT_DIR"
