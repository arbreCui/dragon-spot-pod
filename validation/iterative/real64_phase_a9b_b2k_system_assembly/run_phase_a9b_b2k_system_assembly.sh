#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)
PARENT_RECEIPT="$ROOT/validation/iterative/real64_phase_a9b_b2j_archive_projection/phase_a9b_b2j_archive_projection_receipt.sha256"
RECEIPT="$HERE/phase_a9b_b2k_system_assembly_receipt.sha256"
EXPECTED_PARENT_COMMIT=8e7af9727432085bc757fd884707f1726a7ae9a8
EXPECTED_PARENT_HASH=289fe437c161ad977311fc9334bb8355022ab05e15882c0c3756adac6fe55a69
FC=/opt/homebrew/bin/gfortran
EXPECTED_FC_BANNER='GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0'
CC=/usr/bin/cc
CHECKER="$HERE/check_phase_a9b_b2k_system_assembly.py"
CONTRACT_TEST=test_phase_a9b_b2k_system_assembly_contract
B2J_SUPPORT="$ROOT/validation/iterative/real64_phase_a9b_b2j_archive_projection/b2j_fixture_support.f90"
B2K_SUPPORT="$HERE/b2k_fixture_support.f90"
HARNESS="$HERE/test_b2k_system_assembly.f90"
C2M_HELPER="$HERE/compile_c2m.c"
AX_ARTIFACT="$ROOT/validation/artifacts/iterative-map1/state1_axial.xsm"
ARCHIVE_ARTIFACT="$ROOT/validation/artifacts/iterative-map1/state1_snapshots.xsm"
TRACK_ARTIFACT="$ROOT/validation/artifacts/iterative-seed/initial_axial_track.xsm"
EXPECTED_AX_HASH=2323a256002f1e6f75f5af72c31479b0f6a7bff561d401cee363dcf9fc6ff484
EXPECTED_ARCHIVE_HASH=1b5a0c98aba0f5b4f366b64a8157f4a104df0f89f4cdeafc60eb6ce7811018e1
EXPECTED_TRACK_HASH=101ba0ad64c91723fdeb002e62c6226347fcfaeff188e125d699d70e113febc7
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-a9b-b2k.XXXXXX")
SOURCE_DIR="$BUILD_DIR/source"
OBJECT_DIR="$BUILD_DIR/objects"
CASE_DIR="$BUILD_DIR/case"
trap 'cd /; rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

LC_ALL=C
export LC_ALL

fail()
{
  printf '%s\n' "SPOR64 PHASE-A9b-B2k FAILURE: $*" >&2
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
  [ -f "$PARENT_RECEIPT" ] || fail "B2j parent receipt missing"
  [ "$(hash_of "$PARENT_RECEIPT")" = "$EXPECTED_PARENT_HASH" ] || \
    fail "B2j parent receipt changed"
  if [ -f "$RECEIPT" ]; then
    (
      cd "$ROOT"
      shasum -a 256 -c "$RECEIPT" >/dev/null
    ) || fail "B2k implementation receipt verification failed"
  fi
}

[ "$(uname -s)" = Darwin ] || fail "frozen platform is Darwin"
[ "$(uname -m)" = arm64 ] || fail "frozen architecture is arm64"
[ -x "$FC" ] || fail "frozen compiler missing"
[ -x "$CC" ] || fail "host C compiler missing"
FC_BANNER=$("$FC" --version | sed -n '1p')
[ "$FC_BANNER" = "$EXPECTED_FC_BANNER" ] || fail "unaudited compiler"
for source in SPOR64_B2C SPOR64_B2I SPOR64_B2H SPOR64_B2J SPOR64_B2K; do
  [ -f "$ROOT/src/$source.f90" ] || fail "production $source missing"
done
[ -f "$ROOT/src/ASM.f" ] || fail "production ASM missing"
[ -f "$ROOT/src/XDRTA2.f" ] || fail "production XDRTA2 missing"
[ -f "$ROOT/src/ASMDRV.f" ] || fail "production ASMDRV missing"
[ -f "$ROOT/src/KDRDRV.F" ] || fail "production dispatcher missing"
[ -f "$ROOT/data/SpotAsmR64.c2m" ] || fail "candidate ASM procedure missing"
[ -f "$CHECKER" ] || fail "independent static checker missing"
[ -f "$HERE/$CONTRACT_TEST.py" ] || fail "mutation tests missing"
[ -f "$B2J_SUPPORT" ] || fail "B2j real-XSM fixture support missing"
[ -f "$B2K_SUPPORT" ] || fail "B2k fixture support missing"
[ -f "$HARNESS" ] || fail "dynamic GANLIB harness missing"
[ -f "$C2M_HELPER" ] || fail "C2M compiler helper missing"
[ -f "$AX_ARTIFACT" ] || fail "frozen AX artifact missing"
[ -f "$ARCHIVE_ARTIFACT" ] || fail "frozen archive artifact missing"
[ -f "$TRACK_ARTIFACT" ] || fail "frozen axial-track artifact missing"
[ "$(hash_of "$AX_ARTIFACT")" = "$EXPECTED_AX_HASH" ] || \
  fail "frozen AX artifact changed"
[ "$(hash_of "$ARCHIVE_ARTIFACT")" = "$EXPECTED_ARCHIVE_HASH" ] || \
  fail "frozen archive artifact changed"
[ "$(hash_of "$TRACK_ARTIFACT")" = "$EXPECTED_TRACK_HASH" ] || \
  fail "frozen axial-track artifact changed"
git -C "$ROOT" cat-file -e "$EXPECTED_PARENT_COMMIT^{commit}" || \
  fail "B2j parent commit missing"
git -C "$ROOT" merge-base --is-ancestor "$EXPECTED_PARENT_COMMIT" HEAD || \
  fail "B2j parent commit is not an ancestor"
verify_receipts

PYTHONDONTWRITEBYTECODE=1 python3 "$CHECKER"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$HERE" python3 -m unittest -v \
  "$CONTRACT_TEST"

mkdir -p "$SOURCE_DIR" "$OBJECT_DIR" "$CASE_DIR"
for source in SPOR64_B2C SPOR64_B2I SPOR64_B2H SPOR64_B2J SPOR64_B2K; do
  copy_exact "$ROOT/src/$source.f90" "$SOURCE_DIR/$source.f90"
done
copy_exact "$ROOT/src/ASM.f" "$SOURCE_DIR/ASM.f"
copy_exact "$ROOT/src/XDRTA2.f" "$SOURCE_DIR/XDRTA2.f"
copy_exact "$ROOT/src/KDRDRV.F" "$SOURCE_DIR/KDRDRV.F"
copy_exact "$B2J_SUPPORT" "$SOURCE_DIR/b2j_fixture_support.f90"
copy_exact "$B2K_SUPPORT" "$SOURCE_DIR/b2k_fixture_support.f90"
copy_exact "$HARNESS" "$SOURCE_DIR/test_b2k_system_assembly.f90"
copy_exact "$C2M_HELPER" "$SOURCE_DIR/compile_c2m.c"
ln -s "$AX_ARTIFACT" "$CASE_DIR/ax.xsm"
ln -s "$ARCHIVE_ARTIFACT" "$CASE_DIR/archive.xsm"
ln -s "$TRACK_ARTIFACT" "$CASE_DIR/track.xsm"

FLAGS='-O0 -g -std=f2008 -pedantic -Wall -Wextra -Werror'
FLAGS="$FLAGS -fimplicit-none -fcheck=all -fbacktrace"
FLAGS="$FLAGS -ffp-contract=off -fno-fast-math"
GANMOD="$ROOT/Ganlib/lib/Darwin_arm64/modules"
FIXED_FLAGS='-O0 -g -std=legacy -ffixed-line-length-none -cpp'

for source in SPOR64_B2C SPOR64_B2I SPOR64_B2H SPOR64_B2J SPOR64_B2K; do
  "$FC" $FLAGS -I "$GANMOD" -I "$OBJECT_DIR" -J "$OBJECT_DIR" \
    -c "$SOURCE_DIR/$source.f90" -o "$OBJECT_DIR/$source.o"
done
"$FC" $FIXED_FLAGS -I "$GANMOD" -c "$SOURCE_DIR/ASM.f" \
  -o "$OBJECT_DIR/ASM.o"
"$FC" $FIXED_FLAGS -I "$GANMOD" -c "$SOURCE_DIR/XDRTA2.f" \
  -o "$OBJECT_DIR/XDRTA2.o"
"$FC" $FIXED_FLAGS -I "$GANMOD" -c "$SOURCE_DIR/KDRDRV.F" \
  -o "$OBJECT_DIR/KDRDRV.o"
"$FC" $FLAGS -I "$GANMOD" -I "$OBJECT_DIR" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/b2j_fixture_support.f90" \
  -o "$OBJECT_DIR/b2j_fixture_support.o"
"$FC" $FLAGS -I "$GANMOD" -I "$OBJECT_DIR" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/b2k_fixture_support.f90" \
  -o "$OBJECT_DIR/b2k_fixture_support.o"
"$FC" $FLAGS -I "$GANMOD" -I "$OBJECT_DIR" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/test_b2k_system_assembly.f90" \
  -o "$OBJECT_DIR/test_b2k_system_assembly.o"

"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$OBJECT_DIR/SPOR64_B2C.o" \
  "$OBJECT_DIR/SPOR64_B2I.o" \
  "$OBJECT_DIR/SPOR64_B2H.o" \
  "$OBJECT_DIR/SPOR64_B2J.o" \
  "$OBJECT_DIR/SPOR64_B2K.o" \
  "$OBJECT_DIR/b2j_fixture_support.o" \
  "$OBJECT_DIR/b2k_fixture_support.o" \
  "$OBJECT_DIR/test_b2k_system_assembly.o" \
  "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" \
  "$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a" \
  -o "$BUILD_DIR/test_b2k_system_assembly"

nm -g "$OBJECT_DIR/SPOR64_B2K.o" >"$BUILD_DIR/b2k.nm"
count_exact 1 \
  ' T ___spor64_b2k_MOD_spor64_b2k_commit_system_archive$' "$BUILD_DIR/b2k.nm"
count_exact 1 ' T _spor64k_$' "$BUILD_DIR/b2k.nm"
nm -g "$OBJECT_DIR/ASM.o" >"$BUILD_DIR/asm.nm"
count_exact 1 ' T _asm_$' "$BUILD_DIR/asm.nm"
count_exact 1 ' U _xdrta2_$' "$BUILD_DIR/asm.nm"
nm -g "$OBJECT_DIR/XDRTA2.o" >"$BUILD_DIR/xdrta2.nm"
count_exact 1 ' T _xdrta2_$' "$BUILD_DIR/xdrta2.nm"
nm -g "$OBJECT_DIR/KDRDRV.o" >"$BUILD_DIR/kdrdrv.nm"
count_exact 1 ' T _kdrdrv_$' "$BUILD_DIR/kdrdrv.nm"
count_exact 1 ' U _spor64k_$' "$BUILD_DIR/kdrdrv.nm"
nm -g "$BUILD_DIR/test_b2k_system_assembly" >"$BUILD_DIR/harness.nm"
if grep -Eiq \
  'asmdrv|doorav|doorpv|mccgf|mcgmre|flu2dr|fludrv|xdrkin|xdrexp|_dragon|spomoc|xdrta2' \
  "$BUILD_DIR/harness.nm"; then
  fail "B2k harness links ASM, transport, or Dragon code"
fi

"$CC" -std=c11 -pedantic -Wall -Wextra -Werror \
  -I "$ROOT/Ganlib/src" -c "$SOURCE_DIR/compile_c2m.c" \
  -o "$OBJECT_DIR/compile_c2m.o"
"$FC" "$OBJECT_DIR/compile_c2m.o" \
  "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" \
  -o "$BUILD_DIR/compile_c2m"
if ! (
  cd "$BUILD_DIR"
  ./compile_c2m "$ROOT/data/SpotAsmR64.c2m" SpotAsmR64.o2m \
    >c2m_compile.log 2>&1
); then
    sed -n '1,240p' "$BUILD_DIR/c2m_compile.log" >&2
    fail "CLEPIL/OBJPIL compilation of SpotAsmR64.c2m failed"
fi
[ -s "$BUILD_DIR/SpotAsmR64.o2m" ] || fail "empty compiled C2M object"

if ! (
  cd "$CASE_DIR"
  "$BUILD_DIR/test_b2k_system_assembly" ax.xsm archive.xsm track.xsm \
    >harness.log 2>&1
); then
  sed -n '1,240p' "$CASE_DIR/harness.log" >&2
  fail "dynamic system-assembly harness failed"
fi
count_exact 1 '^B2K SYSTEM-ASSEMBLY PASS$' "$CASE_DIR/harness.log"
count_exact 1 '^B2K CALLS=21 COMMITS=1 REJECTIONS=20$' "$CASE_DIR/harness.log"
count_exact 1 \
  '^B2K FRESH-ZERO-WRITE-REJECTIONS=19 COLLISION-NO-NEW-WRITES=1$' \
  "$CASE_DIR/harness.log"
count_exact 1 \
  '^B2K RESTORED-REAL-XS-BITS=26640 PROJECTED-LEAKAGE-BITS=1110$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2K TXSC-BITS=9990 S0PHYS-BITS=9990 S0USED-BITS=9990$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2K RESPONSE-DEEP-COPY-BITS=179820$' "$CASE_DIR/harness.log"
count_exact 1 '^B2K POST-COMMIT-INDEPENDENCE-WITNESSES=15$' \
  "$CASE_DIR/harness.log"
count_exact 1 \
  '^B2K PROJECTED-FLUX64-BITS=15540 PROJECTED-FLUX32-BITS=15540$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2K PRODUCTION-B2C-CALLS=3 B2I-CALLS=1 B2J-CALLS=1$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2K FRESH-SYSTEMS=3 OLD-SYSTEM-COPIES=0 FULL-SYSTEM-COPIES=3$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2K REAL-XSM-INPUTS=3 DRAGON=0 ASM=0 TRANSPORT-SOLVES=0$' \
  "$CASE_DIR/harness.log"
count_exact 1 \
  '^B2K QFISS=NOT-BUILT CONT=NOT-EXECUTED CONVERGENCE=NOT-EVALUATED$' \
  "$CASE_DIR/harness.log"
[ "$(wc -l <"$CASE_DIR/harness.log" | tr -d '[:space:]')" -eq 12 ] || \
  fail "unexpected harness output line count"

[ "$(hash_of "$AX_ARTIFACT")" = "$EXPECTED_AX_HASH" ] || \
  fail "frozen AX artifact mutated"
[ "$(hash_of "$ARCHIVE_ARTIFACT")" = "$EXPECTED_ARCHIVE_HASH" ] || \
  fail "frozen archive artifact mutated"
[ "$(hash_of "$TRACK_ARTIFACT")" = "$EXPECTED_TRACK_HASH" ] || \
  fail "frozen axial-track artifact mutated"
verify_receipts

printf '%s\n' 'SPOR64 PHASE-A9b-B2k SYSTEM-ASSEMBLY PASS'
printf '%s\n' 'CLAIM=PROJECTED1-PLUS-THREE-FRESH-SYSTEMS-TO-ASSEMBLED1'
printf '%s\n' 'B2K-CALLS=21 COMMITS=1 REJECTIONS=20 ZERO-WRITE=20'
printf '%s\n' 'LEAKAGE-BITS=1110 TXSC-BITS=9990 S0PHYS-BITS=9990 S0USED-BITS=9990'
printf '%s\n' 'RESPONSE-DEEP-COPY-BITS=179820 POST-COMMIT-WITNESSES=15'
printf '%s\n' 'PROJECTED-FLUX64-BITS=15540 PROJECTED-FLUX32-BITS=15540'
printf '%s\n' 'CANDIDATE-SYSTEM-ROOT=EXACT-7 COMMITTED-SYSTEM-ROOT=EXACT-8'
printf '%s\n' 'MCCG-STATE=FROZEN MAPS=BIT-COHERENT ROOT-EPOCH=FINAL-MUTATION'
printf '%s\n' 'STATIC-CONTRACT-TESTS=55 MUTATION-REGRESSION-CASES=54'
printf '%s\n' 'PRODUCTION-B2C-CALLS=3 B2I-CALLS=1 B2J-CALLS=1'
printf '%s\n' 'DRAGON-EXECUTIONS=0 ASM-EXECUTIONS=0 TRANSPORT-SOLVES=0'
printf '%s\n' 'REAL-ASM-STATIC-WIRING=PASS REAL-ASM-EXECUTION=NOT-EVALUATED'
printf '%s\n' 'C2M-COMPILE=CLEPIL+OBJPIL C2M-EXECUTION=NOT-EVALUATED'
printf '%s\n' 'HOST-OBJECT-COMPILE=ASM+XDRTA2+KDRDRV+B2K XDRTA2-ABI=ZERO-ARGUMENT'
printf '%s\n' 'RADIAL-RESPONSE-NUMERICS=NOT-EVALUATED'
printf '%s\n' 'QFISS=NOT-BUILT CONT=NOT-EXECUTED'
printf '%s\n' 'RADIAL-CONVERGENCE=NOT-EVALUATED OUTER-PICARD=NOT-EVALUATED'
printf '%s\n' 'SEQUENTIAL-TRACKING-RECORD-READS=0 LONG-CALCULATIONS=0'
if [ -f "$RECEIPT" ]; then
  printf '%s\n' 'RECEIPT=FROZEN PARENT=B2j'
else
  printf '%s\n' 'RECEIPT=PENDING-MAIN-AUDIT PARENT=B2j'
fi
