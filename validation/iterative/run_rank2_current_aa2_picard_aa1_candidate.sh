#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
MANIFEST=${MANIFEST:-"$ROOT/validation/iterative/rank2_current_aa2_picard_aa1_candidate_inputs.tsv"}
ARTIFACT_DIR=${ARTIFACT_DIR:-"$ROOT/validation/artifacts/iterative-rank2-current-aa2-picard-aa1-candidate"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}

BUILDER="$ROOT/validation/iterative/build_rank2_modal_aa1_candidate.f90"
CHECKER="$ROOT/validation/iterative/check_rank2_modal_aa1_candidate.f90"
RUNNER="$ROOT/validation/iterative/run_rank2_current_aa2_picard_aa1_candidate.sh"
EXPECTED_AX_SHA=6a8527b62121e87c89d66b0d14893653aaaef5a902b4899307f995e4e63d1403
EXPECTED_SNAP_SHA=57c99aad12c36140790209a4d4992bc70f17a2d69f25a37328fbe14dd5c0a374

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
  '# spot-rank2-current-aa2-picard-aa1-candidate-inputs-v1'
test "$(awk 'NF && $1 !~ /^#/ {n++} END {print n+0}' "$MANIFEST")" = 5
test "$(awk 'NF && $1 !~ /^#/ && NF != 3 {n++} END {print n+0}' \
  "$MANIFEST")" = 0
for role in q_aa2_pub p z z_snapshots basis_reference
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

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-rank2-aa2-pz-aa1.XXXXXX")
STAGE="$(dirname "$ARTIFACT_DIR")/.rank2-aa2-pz-aa1.$$"
cleanup() {
  rm -rf "$WORK"
  if test -d "$STAGE"; then rm -rf "$STAGE"; fi
}
trap cleanup EXIT HUP INT TERM

for binding in q:q_aa2_pub p:p z:z zs:z_snapshots basis:basis_reference
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
  printf '%s\n' 'RANK2-AA2-PICARD-AA1 ERROR: forbidden solver symbol.' >&2
  exit 2
fi

(
  cd "$WORK"
  ./build_candidate --consecutive-current-aa2-picard q.xsm p.xsm \
    z.xsm zs.xsm proposal_axial.xsm proposal_snapshots.xsm >build.log
  ./check_candidate --consecutive-current-aa2-picard q.xsm p.xsm \
    z.xsm zs.xsm basis.xsm proposal_axial.xsm \
    proposal_snapshots.xsm >check.log
)
rg -q '^RANK2-AA2-PICARD-AA1 PARAMETER-FREE DIRECTION GATE PASS$' \
  "$WORK/build.log" "$WORK/check.log"
rg -q '^RANK2-AA2-PICARD-AA1 PROPOSAL COMPLETE NOT-EVALUATED NO-DRAGON NO-MAP$' \
  "$WORK/build.log"
rg -q '^RANK2-AA2-PICARD-AA1 COMPLETE$' "$WORK/check.log"

for role in q_aa2_pub p z z_snapshots basis_reference
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
cp "$RUNNER" "$STAGE/run_rank2_current_aa2_picard_aa1_candidate.sh"
printf '%s\n' 'MATERIALIZED_PROPOSAL_NOT_EVALUATED' \
  >"$STAGE/classification.txt"
(
  cd "$STAGE"
  shasum -a 256 proposal_axial.xsm proposal_snapshots.xsm build.log \
    check.log input_manifest.tsv build_rank2_modal_aa1_candidate.f90 \
    check_rank2_modal_aa1_candidate.f90 \
    run_rank2_current_aa2_picard_aa1_candidate.sh classification.txt \
    >result.sha256
  shasum -a 256 -c result.sha256 >/dev/null
)
mv "$STAGE" "$ARTIFACT_DIR"

cat "$ARTIFACT_DIR/build.log"
cat "$ARTIFACT_DIR/check.log"
printf '%s\n' \
  "RANK2-AA2-PICARD-AA1 AX-SHA256=$ax_sha" \
  "RANK2-AA2-PICARD-AA1 SNAP-SHA256=$snap_sha" \
  'RANK2-AA2-PICARD-AA1 INPUTS-READ-ONLY HASH PASS' \
  'RANK2-AA2-PICARD-AA1 DRAGON/ASM/FLU/TRANSPORT=0' \
  'RANK2-AA2-PICARD-AA1 CLASSIFICATION=MATERIALIZED_PROPOSAL_NOT_EVALUATED' \
  "RANK2-AA2-PICARD-AA1 RESULT=$ARTIFACT_DIR"
