#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)
PARENT_RECEIPT="$ROOT/validation/iterative/real64_phase_a9b_b2p_solved_lifecycle/phase_a9b_b2p_solved_lifecycle_receipt.sha256"
RECEIPT="$HERE/phase_a9b_b2q_lifecycle_rho_contract_receipt.sha256"
EXPECTED_PARENT_COMMIT=e9af085dfb73f1a69df4cbc3eacf989d3382e105
EXPECTED_PARENT_HASH=147d0c1ff95502344eb33234af4804be0e879bc3befae10699ddf8e9d3c642cc
FC=/opt/homebrew/bin/gfortran
EXPECTED_FC_BANNER='GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0'
CHECKER="$HERE/check_phase_a9b_b2q_lifecycle_rho_contract.py"
CONTRACT_TEST=test_phase_a9b_b2q_lifecycle_rho_contract
HARNESS="$ROOT/validation/iterative/real64_phase_a9b_b2h_projection_authority/test_b2h_projection_authority.f90"
SEED_ARTIFACT="$ROOT/validation/artifacts/iterative-radial-floor/restart_cap.xsm"
TRACK_ARTIFACT="$ROOT/validation/artifacts/raw-moc-capture/common/restart_track.xsm"
EXPECTED_SEED_HASH=7291d8d88b5be07cd570131ea45ce5f283d55a37e3577197626001c59d9b8c89
EXPECTED_TRACK_HASH=2d868b87e2003c10c09da1ec8f8e6fd97f2a2629a680a46d7f898e2e5e1ed598
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-a9b-b2q.XXXXXX")
SOURCE_DIR="$BUILD_DIR/source"
OBJECT_DIR="$BUILD_DIR/objects"
CASE_DIR="$BUILD_DIR/case"
trap 'cd /; rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

LC_ALL=C
export LC_ALL

fail()
{
  printf '%s\n' "SPOR64 PHASE-A9b-B2q FAILURE: $*" >&2
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

hash_of()
{
  shasum -a 256 "$1" | awk '{print $1}'
}

copy_exact()
{
  source_path=$1
  target_path=$2
  cp "$source_path" "$target_path"
  cmp "$source_path" "$target_path" || fail "copy differs: $target_path"
}

verify_receipts()
{
  [ -f "$PARENT_RECEIPT" ] || fail "B2p parent receipt missing"
  [ "$(hash_of "$PARENT_RECEIPT")" = "$EXPECTED_PARENT_HASH" ] || \
    fail "B2p parent receipt changed"
  git -C "$ROOT" cat-file -e "$EXPECTED_PARENT_COMMIT^{commit}" || \
    fail "B2p parent commit missing"
  git -C "$ROOT" merge-base --is-ancestor "$EXPECTED_PARENT_COMMIT" HEAD || \
    fail "B2p parent commit is not an ancestor"
  [ -f "$RECEIPT" ] || fail "B2q contract receipt missing"
  (
    cd "$ROOT"
    shasum -a 256 -c "$RECEIPT" >/dev/null
  ) || fail "B2q contract receipt verification failed"
}

[ "$(uname -s)" = Darwin ] || fail "frozen platform is Darwin"
[ "$(uname -m)" = arm64 ] || fail "frozen architecture is arm64"
[ -x "$FC" ] || fail "frozen compiler missing"
FC_BANNER=$("$FC" --version | sed -n '1p')
[ "$FC_BANNER" = "$EXPECTED_FC_BANNER" ] || fail "unaudited compiler"
[ -f "$CHECKER" ] || fail "static lifecycle/RHO checker missing"
[ -f "$HERE/$CONTRACT_TEST.py" ] || fail "mutation suite missing"
[ -f "$HARNESS" ] || fail "B2h distinct-RHO harness missing"
[ -f "$SEED_ARTIFACT" ] || fail "frozen seed artifact missing"
[ -f "$TRACK_ARTIFACT" ] || fail "frozen track artifact missing"
[ "$(hash_of "$SEED_ARTIFACT")" = "$EXPECTED_SEED_HASH" ] || \
  fail "frozen seed artifact changed"
[ "$(hash_of "$TRACK_ARTIFACT")" = "$EXPECTED_TRACK_HASH" ] || \
  fail "frozen track artifact changed"
verify_receipts

if ! PYTHONDONTWRITEBYTECODE=1 python3 "$CHECKER" \
  >"$BUILD_DIR/static.log" 2>&1
then
  sed -n '1,180p' "$BUILD_DIR/static.log" >&2
  fail "static lifecycle/RHO contract rejected"
fi
count_exact 1 '^B2Q STATIC LIFECYCLE-RHO CONTRACT PASS$' \
  "$BUILD_DIR/static.log"
count_exact 1 '^B2Q FLOW=CLOSED\(N\)/RHO_N->WORK\(N\+1\)/RHO_N$' \
  "$BUILD_DIR/static.log"
count_exact 1 \
  '^B2Q CURRENT=CLOSED/0->PROJECTED/1->ASSEMBLED/1->FROZEN-QFIS/1->SOLVED/1$' \
  "$BUILD_DIR/static.log"
count_exact 1 \
  '^B2Q PRODUCTION-SOURCE-CHANGES=0 EMPIRICAL-CONTROLS-ADDED=0$' \
  "$BUILD_DIR/static.log"

if ! (
  cd "$HERE"
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$HERE" \
    python3 -m unittest -v "$CONTRACT_TEST" \
    >"$BUILD_DIR/mutations.log" 2>&1
)
then
  sed -n '1,220p' "$BUILD_DIR/mutations.log" >&2
  fail "lifecycle/RHO mutation suite rejected"
fi
count_exact 1 '^Ran 34 tests in [0-9.]+s$' "$BUILD_DIR/mutations.log"
count_exact 1 '^OK$' "$BUILD_DIR/mutations.log"
verify_receipts

mkdir -p "$SOURCE_DIR" "$OBJECT_DIR" "$CASE_DIR"
copy_exact "$ROOT/src/SPOR64_B2H.f90" "$SOURCE_DIR/SPOR64_B2H.f90"
copy_exact "$HARNESS" "$SOURCE_DIR/test_b2h_projection_authority.f90"
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
  -c "$SOURCE_DIR/test_b2h_projection_authority.f90" \
  -o "$OBJECT_DIR/test_b2h_projection_authority.o"
"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$OBJECT_DIR/SPOR64_B2H.o" \
  "$OBJECT_DIR/test_b2h_projection_authority.o" \
  "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" \
  "$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a" \
  -o "$BUILD_DIR/test_b2h_projection_authority"

nm -g "$BUILD_DIR/test_b2h_projection_authority" >"$BUILD_DIR/harness.nm"
if grep -Eiq \
  'doorfv|mccgf|mcgmre|flu2dr|fludrv|flugpi|xdrkin|xdrexp|_dragon|spomoc|spoasm|spor64_b2k|spor64_b2n|_asm' \
  "$BUILD_DIR/harness.nm"
then
  fail "B2h harness links a production solver, FLU, Dragon, or ASM component"
fi

if ! (
  cd "$CASE_DIR"
  "$BUILD_DIR/test_b2h_projection_authority" seed.xsm track.xsm \
    >harness.log 2>&1
)
then
  sed -n '1,180p' "$CASE_DIR/harness.log" >&2
  fail "B2h distinct-RHO harness rejected"
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
  fail "unexpected B2h harness output line count"

cmp "$SEED_ARTIFACT" "$CASE_DIR/seed.xsm" || fail "seed copy mutated"
cmp "$TRACK_ARTIFACT" "$CASE_DIR/track.xsm" || fail "track copy mutated"
[ "$(hash_of "$CASE_DIR/seed.xsm")" = "$EXPECTED_SEED_HASH" ] || \
  fail "seed copy hash changed"
[ "$(hash_of "$CASE_DIR/track.xsm")" = "$EXPECTED_TRACK_HASH" ] || \
  fail "track copy hash changed"
verify_receipts
PYTHONDONTWRITEBYTECODE=1 python3 "$CHECKER" >/dev/null

printf '%s\n' 'SPOR64 PHASE-A9b-B2q LIFECYCLE-RHO-CONTRACT PASS'
printf '%s\n' 'CONTRACT=CLOSED(N)/RHO_N->PROJECTED-ASSEMBLED-FROZEN-QFIS-SOLVED(N+1)/RHO_N'
printf '%s\n' 'CURRENT=CLOSED/0->PROJECTED/1->ASSEMBLED/1->FROZEN-QFIS/1->SOLVED/1'
printf '%s\n' 'PRODUCTION-SOURCE-CHANGES=0 STATIC-CONTRACT-TESTS=34'
printf '%s\n' 'DYNAMIC=B2H-DISTINCT-SEED-RHO/CALLER-RHO CALLS=14 REJECTIONS=13'
printf '%s\n' 'B2J-B2P-EVIDENCE=HASH-PINNED-NOT-REEXECUTED'
printf '%s\n' 'PRODUCTION-SOLVER-EXECUTIONS=0 DRAGON-EXECUTIONS=0 ASM-EXECUTIONS=0'
printf '%s\n' 'RETURNED-ARCHIVE-COLLECTOR=SPECIFIED AX-NEXT-CLOSE-GATE=SPECIFIED'
printf '%s\n' 'SECOND-CLOSED-ARCHIVE=NOT-IMPLEMENTED RHO1=NOT-COMPUTED'
printf '%s\n' 'RADIAL-CONVERGENCE=NOT-EVALUATED OUTER-PICARD-CONVERGENCE=NOT-EVALUATED'
printf '%s\n' 'RECEIPT=FROZEN PARENT=B2p'
