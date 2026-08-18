#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
MANIFEST=${MANIFEST:-"$ROOT/validation/iterative/rank2_current_qvwx_aa1_candidate_inputs.tsv"}
ARTIFACT_DIR=${ARTIFACT_DIR:-"$ROOT/validation/artifacts/iterative-rank2-current-qvwx-aa1-candidate"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}
CANDIDATE_MODE=${CANDIDATE_MODE:---next-x4aa2-screened}
REPORT_PREFIX=${REPORT_PREFIX:-RANK2-CURRENT-QVWX-AA1}
MANIFEST_HEADER=${MANIFEST_HEADER:-'# spot-rank2-current-qvwx-aa1-candidate-inputs-v1'}

BUILDER="$ROOT/validation/iterative/build_rank2_modal_aa1_candidate.f90"
CHECKER="$ROOT/validation/iterative/check_rank2_modal_aa1_candidate.f90"
RUNNER="$ROOT/validation/iterative/run_rank2_current_qvwx_aa1_candidate.sh"
EXPECTED_AX_SHA=012ccd8e428e7a819ce41cec70eab90745e92dc1bb95735a35631f3ef0e2057d
EXPECTED_SNAP_SHA=8942bf5ca0c2f551200dcf78508093a34da39636c5fe57f167a05b4d1da37504
expected_ax_sha=$EXPECTED_AX_SHA
expected_snap_sha=$EXPECTED_SNAP_SHA

case "$CANDIDATE_MODE" in
  --next-x4aa2-screened)
    test "$REPORT_PREFIX" = 'RANK2-CURRENT-QVWX-AA1'
    test "$MANIFEST_HEADER" = \
      '# spot-rank2-current-qvwx-aa1-candidate-inputs-v1'
    ;;
  --next-aa1aa2-screened)
    test "$REPORT_PREFIX" = 'RANK2-CURRENT-GH-AA1'
    test "$MANIFEST_HEADER" = \
      '# spot-rank2-current-gh-aa1-candidate-inputs-v1'
    expected_ax_sha=${EXPECTED_AX_SHA_OVERRIDE:-}
    expected_snap_sha=${EXPECTED_SNAP_SHA_OVERRIDE:-}
    for expected_sha in "$expected_ax_sha" "$expected_snap_sha"
    do
      printf '%s\n' "$expected_sha" | rg -q '^[0-9a-f]{64}$'
    done
    ;;
  --next-aa1aa2-no-screened)
    test "$REPORT_PREFIX" = 'RANK2-CURRENT-NO-AA1'
    test "$MANIFEST_HEADER" = \
      '# spot-rank2-current-no-aa1-candidate-inputs-v1'
    expected_ax_sha=${EXPECTED_AX_SHA_OVERRIDE:-}
    expected_snap_sha=${EXPECTED_SNAP_SHA_OVERRIDE:-}
    for expected_sha in "$expected_ax_sha" "$expected_snap_sha"
    do
      printf '%s\n' "$expected_sha" | rg -q '^[0-9a-f]{64}$'
    done
    ;;
  --next-aa2aa1-op-screened)
    test "$REPORT_PREFIX" = 'RANK2-CURRENT-OP-AA1'
    test "$MANIFEST_HEADER" = \
      '# spot-rank2-current-op-aa1-candidate-inputs-v1'
    expected_ax_sha=${EXPECTED_AX_SHA_OVERRIDE:-}
    expected_snap_sha=${EXPECTED_SNAP_SHA_OVERRIDE:-}
    for expected_sha in "$expected_ax_sha" "$expected_snap_sha"
    do
      printf '%s\n' "$expected_sha" | rg -q '^[0-9a-f]{64}$'
    done
    ;;
  --next-aa1aa1-screened)
    test "$REPORT_PREFIX" = 'RANK2-CURRENT-MN-AA1'
    case "$MANIFEST_HEADER" in
      '# spot-rank2-current-pr-aa1-candidate-inputs-v1'|\
      '# spot-rank2-current-rs-aa1-candidate-inputs-v1') ;;
      *) exit 2 ;;
    esac
    expected_ax_sha=${EXPECTED_AX_SHA_OVERRIDE:-}
    expected_snap_sha=${EXPECTED_SNAP_SHA_OVERRIDE:-}
    for expected_sha in "$expected_ax_sha" "$expected_snap_sha"
    do
      printf '%s\n' "$expected_sha" | rg -q '^[0-9a-f]{64}$'
    done
    ;;
  --next-aa1aa2-ij-screened)
    test "$REPORT_PREFIX" = 'RANK2-CURRENT-IJ-AA1'
    test "$MANIFEST_HEADER" = \
      '# spot-rank2-current-ij-aa1-candidate-inputs-v1'
    expected_ax_sha=27250a1b370d2cdbf83f35fbf1a380919261bb938890b2f3d04d7390afb72743
    expected_snap_sha=f7e351eab9c895c4b43023e37734f4675898fa39b70e07ca9c25c29eecd66f7c
    ;;
  *)
    printf '%s\n' 'AA1 candidate mode must be QVWX, GH, IJ, NO, OP, PR, or RS.' >&2
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
test "$(awk 'NF && $1 !~ /^#/ {n++} END {print n+0}' "$MANIFEST")" = 6
test "$(awk 'NF && $1 !~ /^#/ && NF != 3 {n++} END {print n+0}' \
  "$MANIFEST")" = 0
for role in q v w x x_snapshots basis_reference
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

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-rank2-current-qvwx-aa1.XXXXXX")
STAGE="$(dirname "$ARTIFACT_DIR")/.rank2-current-qvwx-aa1.$$"
cleanup() {
  rm -rf "$WORK"
  if test -d "$STAGE"; then rm -rf "$STAGE"; fi
}
trap cleanup EXIT HUP INT TERM

for binding in q:q v:v w:w x:x xs:x_snapshots basis:basis_reference
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
  printf '%s\n' "$REPORT_PREFIX ERROR: forbidden solver symbol." >&2
  exit 2
fi

(
  cd "$WORK"
  ./build_candidate "$CANDIDATE_MODE" q.xsm v.xsm w.xsm x.xsm \
    xs.xsm proposal_axial.xsm proposal_snapshots.xsm >build.log
  ./check_candidate "$CANDIDATE_MODE" q.xsm v.xsm w.xsm x.xsm \
    xs.xsm basis.xsm proposal_axial.xsm proposal_snapshots.xsm >check.log
)
rg -q "^$REPORT_PREFIX PARAMETER-FREE DIRECTION GATE PASS$" \
  "$WORK/build.log" "$WORK/check.log"
rg -q "^$REPORT_PREFIX CARRIER AA1-RAW-FLUX$" "$WORK/build.log"
rg -q "^$REPORT_PREFIX COMPLETE$" "$WORK/check.log"

for role in q v w x x_snapshots basis_reference
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
cp "$RUNNER" "$STAGE/run_rank2_current_qvwx_aa1_candidate.sh"
printf '%s\n' 'MATERIALIZED_PROPOSAL_NOT_EVALUATED' \
  >"$STAGE/classification.txt"
(
  cd "$STAGE"
  shasum -a 256 proposal_axial.xsm proposal_snapshots.xsm build.log \
    check.log input_manifest.tsv build_rank2_modal_aa1_candidate.f90 \
    check_rank2_modal_aa1_candidate.f90 \
    run_rank2_current_qvwx_aa1_candidate.sh classification.txt \
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
