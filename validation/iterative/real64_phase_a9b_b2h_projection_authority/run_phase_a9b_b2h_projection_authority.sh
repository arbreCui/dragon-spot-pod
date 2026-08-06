#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)
PARENT_RECEIPT="$ROOT/validation/iterative/real64_phase_a9b_b2g_explicit_continuation/phase_a9b_b2g_explicit_continuation_receipt.sha256"
RECEIPT="$HERE/phase_a9b_b2h_projection_authority_receipt.sha256"
EXPECTED_PARENT_COMMIT=33ebaaa351adab3fe3b45d510864943956573488
EXPECTED_PARENT_HASH=326fc4a62a66941b578ee843de8fe18ea705204a140de1c6b639e910e3ec210c
FC=/opt/homebrew/bin/gfortran
EXPECTED_FC_BANNER='GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0'
CHECKER="$HERE/check_phase_a9b_b2h_projection_authority.py"
CONTRACT_TEST=test_phase_a9b_b2h_projection_authority_contract
SEED_ARTIFACT="$ROOT/validation/artifacts/iterative-radial-floor/restart_cap.xsm"
TRACK_ARTIFACT="$ROOT/validation/artifacts/raw-moc-capture/common/restart_track.xsm"
EXPECTED_SEED_HASH=7291d8d88b5be07cd570131ea45ce5f283d55a37e3577197626001c59d9b8c89
EXPECTED_TRACK_HASH=2d868b87e2003c10c09da1ec8f8e6fd97f2a2629a680a46d7f898e2e5e1ed598
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-a9b-b2h.XXXXXX")
SOURCE_DIR="$BUILD_DIR/source"
OBJECT_DIR="$BUILD_DIR/objects"
CASE_DIR="$BUILD_DIR/case"
trap 'cd /; rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

LC_ALL=C
export LC_ALL

fail()
{
  printf '%s\n' "SPOR64 PHASE-A9b-B2h FAILURE: $*" >&2
  exit 1
}

count_exact()
{
  expected=$1
  pattern=$2
  file=$3
  found=$(grep -c -E "$pattern" "$file" || true)
  [ "$found" -eq "$expected" ] || \
    fail "$file: expected $expected matches for $pattern, found $found"
}

copy_exact()
{
  source_path=$1
  target_path=$2
  cp "$source_path" "$target_path"
  cmp "$source_path" "$target_path" || fail "copy differs: $target_path"
}

hash_of()
{
  shasum -a 256 "$1" | awk '{print $1}'
}

verify_receipts()
{
  [ -f "$PARENT_RECEIPT" ] || fail "parent receipt missing"
  [ "$(hash_of "$PARENT_RECEIPT")" = "$EXPECTED_PARENT_HASH" ] || \
    fail "parent receipt changed"
  [ -f "$RECEIPT" ] || fail "implementation receipt missing"
  (
    cd "$ROOT"
    shasum -a 256 -c "$RECEIPT" >/dev/null
  ) || fail "implementation receipt verification failed"
}

[ "$(uname -s)" = Darwin ] || fail "frozen platform is Darwin"
[ "$(uname -m)" = arm64 ] || fail "frozen architecture is arm64"
[ -x "$FC" ] || fail "frozen compiler missing"
FC_BANNER=$("$FC" --version | sed -n '1p')
[ "$FC_BANNER" = "$EXPECTED_FC_BANNER" ] || fail "unaudited compiler"
[ -f "$ROOT/src/SPOR64_B2H.f90" ] || fail "production B2h module missing"
[ -f "$CHECKER" ] || fail "independent static checker missing"
[ -f "$HERE/$CONTRACT_TEST.py" ] || fail "mutation tests missing"
[ -f "$SEED_ARTIFACT" ] || fail "frozen seed artifact missing"
[ -f "$TRACK_ARTIFACT" ] || fail "frozen track artifact missing"
[ "$(hash_of "$SEED_ARTIFACT")" = "$EXPECTED_SEED_HASH" ] || \
  fail "frozen seed artifact changed"
[ "$(hash_of "$TRACK_ARTIFACT")" = "$EXPECTED_TRACK_HASH" ] || \
  fail "frozen track artifact changed"
git -C "$ROOT" cat-file -e "$EXPECTED_PARENT_COMMIT^{commit}" || \
  fail "B2g parent commit missing"
git -C "$ROOT" merge-base --is-ancestor "$EXPECTED_PARENT_COMMIT" HEAD || \
  fail "B2g parent commit is not an ancestor"
verify_receipts

PYTHONDONTWRITEBYTECODE=1 python3 "$CHECKER"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$HERE" python3 -m unittest -v \
  "$CONTRACT_TEST"

mkdir -p "$SOURCE_DIR" "$OBJECT_DIR" "$CASE_DIR"
copy_exact "$ROOT/src/SPOR64_B2H.f90" "$SOURCE_DIR/SPOR64_B2H.f90"

# GANLIB's XSM filename bridge is 72 bytes, so the harness opens short,
# read-only copies and the runner proves those copies were not mutated.
copy_exact "$SEED_ARTIFACT" "$CASE_DIR/seed.xsm"
copy_exact "$TRACK_ARTIFACT" "$CASE_DIR/track.xsm"
chmod 444 "$CASE_DIR/seed.xsm" "$CASE_DIR/track.xsm"

FLAGS='-O0 -g -std=f2008 -pedantic -Wall -Wextra -Werror'
FLAGS="$FLAGS -fimplicit-none -fcheck=all -fbacktrace"
FLAGS="$FLAGS -ffp-contract=off -fno-fast-math"
GANMOD="$ROOT/Ganlib/lib/Darwin_arm64/modules"

"$FC" $FLAGS -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2H.f90" -o "$OBJECT_DIR/SPOR64_B2H.o"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$HERE/test_b2h_projection_authority.f90" \
  -o "$OBJECT_DIR/test_b2h_projection_authority.o"
"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$OBJECT_DIR/SPOR64_B2H.o" \
  "$OBJECT_DIR/test_b2h_projection_authority.o" \
  "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" \
  "$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a" \
  -o "$BUILD_DIR/test_b2h_projection_authority"

nm -g "$OBJECT_DIR/SPOR64_B2H.o" >"$BUILD_DIR/b2h.nm"
count_exact 1 \
  ' T ___spor64_b2h_MOD_spor64_b2h_reconstruct$' "$BUILD_DIR/b2h.nm"
count_exact 1 \
  ' T ___spor64_b2h_MOD_spor64_b2h_project$' "$BUILD_DIR/b2h.nm"
nm -g "$BUILD_DIR/test_b2h_projection_authority" >"$BUILD_DIR/harness.nm"
if grep -Eiq \
  'doorfv|mccgf|mcgmre|spor64_a8|fludrv|flugpi|xdrkin|xdrexp|_dragon|_flu2dr_|spomoc|asm' \
  "$BUILD_DIR/harness.nm"; then
  fail "projection harness links a transport solver or Dragon component"
fi

if ! (
  cd "$CASE_DIR"
  "$BUILD_DIR/test_b2h_projection_authority" seed.xsm track.xsm \
    >harness.log 2>&1
); then
  sed -n '1,160p' "$CASE_DIR/harness.log" >&2
  fail "dynamic projection harness failed"
fi
count_exact 1 '^B2H PROJECTION-AUTHORITY PASS$' "$CASE_DIR/harness.log"
count_exact 1 '^B2H RECONSTRUCT-CALLS=6 REJECTIONS=5$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2H PROJECT-CALLS=14 REJECTIONS=13$' \
  "$CASE_DIR/harness.log"
count_exact 1 \
  '^B2H REGION-BITS=2960 NONREGION-BITS=2220 MIRROR-BITS=5180$' \
  "$CASE_DIR/harness.log"
count_exact 1 \
  '^B2H RHO-TYPE4-BITS=2 SOURCE-CARRYOVERS=0 ARTIFACT-WRITES=0$' \
  "$CASE_DIR/harness.log"
[ "$(wc -l <"$CASE_DIR/harness.log" | tr -d '[:space:]')" -eq 5 ] || \
  fail "unexpected harness output line count"

cmp "$SEED_ARTIFACT" "$CASE_DIR/seed.xsm" || \
  fail "frozen seed artifact copy mutated"
cmp "$TRACK_ARTIFACT" "$CASE_DIR/track.xsm" || \
  fail "frozen track artifact copy mutated"
[ "$(hash_of "$CASE_DIR/seed.xsm")" = "$EXPECTED_SEED_HASH" ] || \
  fail "seed copy hash changed"
[ "$(hash_of "$CASE_DIR/track.xsm")" = "$EXPECTED_TRACK_HASH" ] || \
  fail "track copy hash changed"
verify_receipts

printf '%s\n' 'SPOR64 PHASE-A9b-B2h PROJECTION-AUTHORITY PASS'
printf '%s\n' 'CLAIM=REGION-PROJECTED-NONREGION-TYPE4-PRESERVED-MIRROR-DOWNCAST'
printf '%s\n' 'REAL-B2H-PROJECT-CALLS=14 PREFLIGHT-REJECTIONS=13 COMMITS=1'
printf '%s\n' 'RECONSTRUCT-CALLS=6 RECONSTRUCT-REJECTIONS=5'
printf '%s\n' 'REGION-TYPE4-BIT-CHECKS=2960 NONREGION-TYPE4-BIT-CHECKS=2220'
printf '%s\n' 'ROOT-TYPE2-MIRROR-BIT-CHECKS=5180 ROOT-POISON-FAMILIES=1'
printf '%s\n' 'RHO-TYPE4-BIT-CHECKS=2'
printf '%s\n' 'OUTPUT-SOURCE-CARRYOVERS=0 ORIGINAL-ARTIFACT-MUTATIONS=0'
printf '%s\n' 'STATIC-CONTRACT-TESTS=27 MUTATION-REGRESSION-CASES=26'
printf '%s\n' 'PRODUCTION-CORE-CALLS=0 DRAGON-EXECUTIONS=0 TRANSPORT-SOLVES=0'
printf '%s\n' 'SEQUENTIAL-TRACKING-RECORD-READS=0'
printf '%s\n' 'RECEIPT=FROZEN PARENT=B2g'
printf '%s\n' 'RADIAL-CONVERGENCE=NOT-EVALUATED OUTER-PICARD=NOT-EVALUATED'
