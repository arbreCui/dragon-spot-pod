#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
MANIFEST=${MANIFEST:-"$ROOT/validation/iterative/rank2_current_zrs_aa1_candidate_inputs.tsv"}
ARTIFACT_DIR=${ARTIFACT_DIR:-"$ROOT/validation/artifacts/iterative-rank2-current-zrs-aa1-candidate"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}

BUILDER="$ROOT/validation/iterative/build_rank2_modal_aa1_candidate.f90"
CHECKER="$ROOT/validation/iterative/check_rank2_modal_aa1_candidate.f90"
RUNNER="$ROOT/validation/iterative/run_rank2_current_zrs_aa1_candidate.sh"
EXPECTED_AX_SHA=d00a310cffb832cfec6ef2bdaa6cf27cfd51443904afd8d26ca57418e140d225
EXPECTED_SNAP_SHA=1e1ed5556c464ae319784ecab8ee408decba7392c419d45de796ab396f82d72d

for path in "$MANIFEST" "$BUILDER" "$CHECKER" "$RUNNER" \
  "$GANLIB_LIB" "$GANLIB_MOD/ganlib.mod"
do
  test -f "$path" && test ! -L "$path"
done
test ! -e "$ARTIFACT_DIR" && test ! -L "$ARTIFACT_DIR"
mkdir -p "$(dirname "$ARTIFACT_DIR")"

hash_file() {
  hash_output=$(shasum -a 256 "$1")
  digest=${hash_output%% *}
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
  '# spot-rank2-current-zrs-aa1-candidate-inputs-v1'
test "$(awk 'NF && $1 !~ /^#/ {n++} END {print n+0}' "$MANIFEST")" = 5
test "$(awk 'NF && $1 !~ /^#/ && NF != 3 {n++} END {print n+0}' \
  "$MANIFEST")" = 0
for role in z r s s_snapshots basis_reference
do
  test "$(awk -v role="$role" \
    '$1 == role {n++} END {print n+0}' "$MANIFEST")" = 1
  expected=$(manifest_value "$role")
  relative=$(manifest_path "$role")
  printf '%s\n' "$expected" | rg -q '^[0-9a-f]{64}$'
  case "$relative" in
    /*|.|..|../*|*/../*|*/..)
      printf 'RANK2-CURRENT-ZRS-AA1 ERROR: unsafe path for %s\n' "$role" >&2
      exit 2
      ;;
  esac
  source_path="$ROOT/$relative"
  test -f "$source_path" && test ! -L "$source_path"
  test "$(hash_file "$source_path")" = "$expected"
done

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-rank2-current-zrs-aa1.XXXXXX")
STAGE="$(dirname "$ARTIFACT_DIR")/.rank2-current-zrs-aa1.$$"
cleanup() {
  rm -rf "$WORK"
  if test -d "$STAGE"; then rm -rf "$STAGE"; fi
}
trap cleanup EXIT HUP INT TERM

for binding in z:z r:r s:s ss:s_snapshots basis:basis_reference
do
  short=${binding%%:*}
  role=${binding#*:}
  ln -s "$ROOT/$(manifest_path "$role")" "$WORK/$short.xsm"
  test "$(hash_file "$WORK/$short.xsm")" = "$(manifest_value "$role")"
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
  printf '%s\n' 'RANK2-CURRENT-ZRS-AA1 ERROR: forbidden solver symbol.' >&2
  exit 2
fi

(
  cd "$WORK"
  ./build_candidate --consecutive-returned-screened \
    z.xsm r.xsm s.xsm ss.xsm \
    proposal_axial.xsm proposal_snapshots.xsm >build.log
  ./check_candidate --consecutive-returned-screened \
    z.xsm r.xsm s.xsm ss.xsm basis.xsm \
    proposal_axial.xsm proposal_snapshots.xsm >check.log
)
rg -q '^RANK2-CURRENT-ZRS-AA1 PARAMETER-FREE DIRECTION GATE PASS$' \
  "$WORK/build.log" "$WORK/check.log"
rg -q '^RANK2-CURRENT-ZRS-AA1 PROPOSAL COMPLETE NOT-EVALUATED NO-DRAGON NO-MAP$' \
  "$WORK/build.log"
rg -q '^RANK2-CURRENT-ZRS-AA1 COMPLETE$' "$WORK/check.log"

for role in z r s s_snapshots basis_reference
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
cp "$RUNNER" "$STAGE/run_rank2_current_zrs_aa1_candidate.sh"
printf '%s\n' 'MATERIALIZED_PROPOSAL_NOT_EVALUATED' \
  >"$STAGE/classification.txt"
(
  cd "$STAGE"
  shasum -a 256 proposal_axial.xsm proposal_snapshots.xsm build.log \
    check.log input_manifest.tsv build_rank2_modal_aa1_candidate.f90 \
    check_rank2_modal_aa1_candidate.f90 \
    run_rank2_current_zrs_aa1_candidate.sh classification.txt \
    >result.sha256
  test "$(wc -l <result.sha256 | tr -d ' ')" = 9
  shasum -a 256 -c result.sha256 >/dev/null
)
mv "$STAGE" "$ARTIFACT_DIR"

cat "$ARTIFACT_DIR/build.log"
cat "$ARTIFACT_DIR/check.log"
printf '%s\n' \
  "RANK2-CURRENT-ZRS-AA1 AX-SHA256=$ax_sha" \
  "RANK2-CURRENT-ZRS-AA1 SNAP-SHA256=$snap_sha" \
  'RANK2-CURRENT-ZRS-AA1 INPUTS-READ-ONLY HASH PASS' \
  'RANK2-CURRENT-ZRS-AA1 RECEIPT 9/9 PASS' \
  'RANK2-CURRENT-ZRS-AA1 DRAGON/ASM/FLU/TRANSPORT=0' \
  'RANK2-CURRENT-ZRS-AA1 CLASSIFICATION=MATERIALIZED_PROPOSAL_NOT_EVALUATED' \
  "RANK2-CURRENT-ZRS-AA1 RESULT=$ARTIFACT_DIR"
