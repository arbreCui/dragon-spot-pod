#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
MANIFEST=${MANIFEST:-"$ROOT/validation/iterative/rank2_wxcd_aa1_candidate_inputs.tsv"}
ARTIFACT_DIR=${ARTIFACT_DIR:-"$ROOT/validation/artifacts/iterative-rank2-wxcd-aa1-candidate"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}

BUILDER="$ROOT/validation/iterative/build_rank2_modal_aa1_candidate.f90"
CHECKER="$ROOT/validation/iterative/check_rank2_modal_aa1_candidate.f90"
RUNNER="$ROOT/validation/iterative/run_rank2_wxcd_aa1_candidate.sh"
EXPECTED_AX_SHA=fded732054da400dc6000b492287e29f7ae88fa2e8c62f80c7dda972940af2d1
EXPECTED_SNAP_SHA=2952fda07917456c733863b7ce756acc2feaa52c8e913bf46ccfadda3b3d6636

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
  '# spot-rank2-wxcd-aa1-candidate-inputs-v1'
test "$(awk 'NF && $1 !~ /^#/ {n++} END {print n+0}' "$MANIFEST")" = 6
test "$(awk 'NF && $1 !~ /^#/ && NF != 3 {n++} END {print n+0}' \
  "$MANIFEST")" = 0
for role in x3 x4 qy_pub z z_snapshots basis_reference
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

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-rank2-wxcd-aa1.XXXXXX")
STAGE="$(dirname "$ARTIFACT_DIR")/.rank2-wxcd-aa1.$$"
cleanup() {
  rm -rf "$WORK"
  if test -d "$STAGE"; then rm -rf "$STAGE"; fi
}
trap cleanup EXIT HUP INT TERM

for role in x3 x4 qy_pub z z_snapshots basis_reference
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
  printf '%s\n' 'RANK2-WXCD-AA1 ERROR: forbidden solver symbol.' >&2
  exit 2
fi

(
  cd "$WORK"
  ./build_candidate --next-x4 x3.xsm x4.xsm qy_pub.xsm z.xsm \
    z_snapshots.xsm proposal_axial.xsm proposal_snapshots.xsm >build.log
  ./check_candidate --next-x4 x3.xsm x4.xsm qy_pub.xsm z.xsm \
    z_snapshots.xsm basis_reference.xsm proposal_axial.xsm \
    proposal_snapshots.xsm >check.log
)
rg -q '^RANK2-LATEST-AA1-NEXT CARRIER Z-RAW-FLUX$' "$WORK/build.log"
rg -q '^RANK2-LATEST-AA1-NEXT COMPLETE$' "$WORK/check.log"

for role in x3 x4 qy_pub z z_snapshots basis_reference
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
cp "$RUNNER" "$STAGE/run_rank2_wxcd_aa1_candidate.sh"
printf '%s\n' 'MATERIALIZED_PROPOSAL_NOT_EVALUATED' \
  >"$STAGE/classification.txt"
(
  cd "$STAGE"
  shasum -a 256 proposal_axial.xsm proposal_snapshots.xsm build.log \
    check.log input_manifest.tsv build_rank2_modal_aa1_candidate.f90 \
    check_rank2_modal_aa1_candidate.f90 run_rank2_wxcd_aa1_candidate.sh \
    classification.txt >result.sha256
  shasum -a 256 -c result.sha256 >/dev/null
)
mv "$STAGE" "$ARTIFACT_DIR"

cat "$ARTIFACT_DIR/build.log"
cat "$ARTIFACT_DIR/check.log"
printf '%s\n' \
  "RANK2-WXCD-AA1 AX-SHA256=$ax_sha" \
  "RANK2-WXCD-AA1 SNAP-SHA256=$snap_sha" \
  'RANK2-WXCD-AA1 INPUTS-READ-ONLY HASH PASS' \
  'RANK2-WXCD-AA1 DRAGON/ASM/FLU/TRANSPORT=0' \
  'RANK2-WXCD-AA1 CLASSIFICATION=MATERIALIZED_PROPOSAL_NOT_EVALUATED' \
  "RANK2-WXCD-AA1 RESULT=$ARTIFACT_DIR"
