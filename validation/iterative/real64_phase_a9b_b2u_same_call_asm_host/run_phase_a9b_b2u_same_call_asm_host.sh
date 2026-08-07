#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)
CHECKER="$HERE/check_phase_a9b_b2u_same_call_asm_host.py"
MUTATION_TEST=test_phase_a9b_b2u_same_call_asm_host
PROBES="$HERE/b2u_adapter_probes.f90"
STUBS="$HERE/b2u_adapter_stubs.f90"
HARNESS="$HERE/test_spor64t_adapter.f90"
C2M_HELPER="$ROOT/validation/iterative/real64_phase_a9b_b2k_system_assembly/compile_c2m.c"
B2S_CAPTURE_STUB="$ROOT/validation/iterative/real64_phase_a9b_b2s_immediate_host_bridge/b2s_capture_stubs.f90"
PARENT_RECEIPT="$ROOT/validation/iterative/real64_phase_a9b_b2t_owned_source_host_step/phase_a9b_b2t_owned_source_host_step_receipt.sha256"
B2M_RECEIPT="$ROOT/validation/iterative/real64_phase_a9b_b2m_three_plane_real_asm_commit/phase_a9b_b2m_three_plane_real_asm_commit_receipt.sha256"
RECEIPT="$HERE/phase_a9b_b2u_same_call_asm_host_receipt.sha256"
TRACK_ARTIFACT="$ROOT/validation/artifacts/iterative-seed/initial_radial_track.bin"

EXPECTED_PARENT_COMMIT=1251f3a5eff95384f83d98d460ca430288736db7
EXPECTED_PARENT_RECEIPT_HASH=08d539c973a4881bbc3e431ddb4dace3da836a245fab9a7d19303c44a823e8af
EXPECTED_B2T_HASH=ee77bb076c1b6239017067a32ead8a95c45a0cf49cd1426ef51aca30bac79816
EXPECTED_B2M_RECEIPT_HASH=8caa46c1af00e9dbe896123a6294dfa96b790e020c9592e0b76d13f093c09314
EXPECTED_SPOT_ASM_HASH=31ec89036bbd2ea62b27fbd4dff5aa1054f3f24997e383f05389e1dda91e364d
EXPECTED_TRACK_HASH=f7b27cb4a5d37f903b93e49610e2daa2290d55c164e2ca0e73ccb8d22fe486b8
EXPECTED_TRACK_BYTES=2275636

FC=/opt/homebrew/bin/gfortran
CC=/usr/bin/cc
CPP=/usr/bin/cpp
EXPECTED_FC_BANNER='GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0'

BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-a9b-b2u.XXXXXX")
SOURCE_DIR="$BUILD_DIR/source"
ACTUAL_OBJECT_DIR="$BUILD_DIR/actual-objects"
ADAPTER_OBJECT_DIR="$BUILD_DIR/adapter-objects"
HOST_OBJECT_DIR="$BUILD_DIR/host-objects"
C2M_DIR="$BUILD_DIR/c2m"
trap 'cd /; rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

LC_ALL=C
export LC_ALL

fail()
{
  printf '%s\n' "SPOR64 PHASE-A9b-B2u FAILURE: $*" >&2
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

run_limited()
(
  ulimit -c 0
  ulimit -t 15
  ulimit -f 524288
  perl -e '$seconds=shift @ARGV; alarm $seconds; exec @ARGV' 15 "$@"
)

verify_parent()
{
  [ -f "$PARENT_RECEIPT" ] || fail "B2t parent receipt missing"
  [ "$(hash_of "$PARENT_RECEIPT")" = "$EXPECTED_PARENT_RECEIPT_HASH" ] || \
    fail "B2t parent receipt changed"
  grep -F -x "$EXPECTED_B2T_HASH  src/SPOR64_B2T.f90" \
    "$PARENT_RECEIPT" >/dev/null || fail "B2t parent source entry changed"
  [ "$(hash_of "$ROOT/src/SPOR64_B2T.f90")" = "$EXPECTED_B2T_HASH" ] || \
    fail "production B2t source changed"
  [ -f "$B2M_RECEIPT" ] || fail "B2m receipt missing"
  [ "$(hash_of "$B2M_RECEIPT")" = "$EXPECTED_B2M_RECEIPT_HASH" ] || \
    fail "B2m receipt changed"
  [ "$(hash_of "$ROOT/data/SpotAsmR64.c2m")" = "$EXPECTED_SPOT_ASM_HASH" ] || \
    fail "frozen SpotAsmR64 parent changed"
  git -C "$ROOT" cat-file -e "$EXPECTED_PARENT_COMMIT^{commit}" || \
    fail "B2t parent commit is missing"
  git -C "$ROOT" merge-base --is-ancestor "$EXPECTED_PARENT_COMMIT" HEAD || \
    fail "B2t parent commit is not an ancestor"
}

verify_receipt()
{
  if [ -f "$RECEIPT" ]; then
    (
      cd "$ROOT"
      shasum -a 256 -c "$RECEIPT" >/dev/null
    ) || fail "B2u receipt verification failed"
  fi
}

verify_track()
{
  [ -f "$TRACK_ARTIFACT" ] || fail "frozen radial tracking file missing"
  [ ! -L "$TRACK_ARTIFACT" ] || fail "frozen radial tracking file is a symlink"
  [ "$(stat -f '%z' "$TRACK_ARTIFACT")" -eq "$EXPECTED_TRACK_BYTES" ] || \
    fail "frozen radial tracking byte count changed"
  [ "$(hash_of "$TRACK_ARTIFACT")" = "$EXPECTED_TRACK_HASH" ] || \
    fail "frozen radial tracking hash changed"
}

[ "$(uname -s)" = Darwin ] || fail "frozen platform is Darwin"
[ "$(uname -m)" = arm64 ] || fail "frozen architecture is arm64"
[ -x "$FC" ] || fail "frozen Fortran compiler missing"
[ -x "$CC" ] || fail "host C compiler missing"
[ -x "$CPP" ] || fail "host preprocessor missing"
command -v perl >/dev/null 2>&1 || fail "wall-time limiter missing"
[ "$($FC --version | sed -n '1p')" = "$EXPECTED_FC_BANNER" ] || \
  fail "unaudited Fortran compiler"

for path in "$CHECKER" "$HERE/$MUTATION_TEST.py" "$PROBES" "$STUBS" \
  "$HARNESS" "$C2M_HELPER" "$B2S_CAPTURE_STUB" \
  "$ROOT/data/SpotStepR64.c2m" "$HERE/b2u_stub_off.c2m" \
  "$HERE/b2u_stub_on.c2m" "$ROOT/src/ASM.f" "$ROOT/src/KDRDRV.F"
do
  [ -f "$path" ] || fail "required input missing: $path"
done
for source in SPOR64_B2C SPOR64_B2B SPOR64_B2O SPOR64_B2R SPOR64_B2S \
  SPOR64_B2K SPOR64_B2N SPOR64_B2T SPOR64_B2U
do
  [ -f "$ROOT/src/$source.f90" ] || fail "production $source missing"
done
count_exact 1 '^SPOR64_B2U\.o: SPOR64_B2T\.o$' \
  "$ROOT/src/.dragon_deps.mk"
verify_parent
verify_receipt
verify_track

mkdir -p "$SOURCE_DIR" "$ACTUAL_OBJECT_DIR" "$ADAPTER_OBJECT_DIR" \
  "$HOST_OBJECT_DIR" "$C2M_DIR"

if ! PYTHONDONTWRITEBYTECODE=1 python3 "$CHECKER" \
  >"$BUILD_DIR/static.log" 2>&1
then
  sed -n '1,240p' "$BUILD_DIR/static.log" >&2
  fail "static same-call host contract rejected"
fi
count_exact 1 '^B2U STATIC SAME-CALL ASM HOST PASS$' "$BUILD_DIR/static.log"
count_exact 1 '^B2U DEPLOYMENT-DEFAULT=OFF SHIPPED-SELECTIONS=0$' \
  "$BUILD_DIR/static.log"
count_exact 1 '^B2U HOST=ASM\(1\)->ASM\(2\)->ASM\(3\)->SPOR64T LIVE-SYSTEMS=3$' \
  "$BUILD_DIR/static.log"
count_exact 1 '^B2U TRACK=SAME-CLE-SYMBOL HASH-PINNED-BYTES PER-DISPATCH-OPEN$' \
  "$BUILD_DIR/static.log"
count_exact 1 '^B2U SPOR64T-LIVE-HANDLE=B2T->B2S->B2B\(1,2,3\)$' \
  "$BUILD_DIR/static.log"
count_exact 1 '^B2U DRAGON=0 ASM-RUNTIME=0 TRANSPORT=0 PICARD=0$' \
  "$BUILD_DIR/static.log"
[ "$(wc -l <"$BUILD_DIR/static.log" | tr -d '[:space:]')" -eq 6 ] || \
  fail "unexpected static checker output"

if ! (
  cd "$HERE"
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$HERE" \
    python3 -m unittest -v "$MUTATION_TEST" \
    >"$BUILD_DIR/mutations.log" 2>&1
)
then
  sed -n '1,320p' "$BUILD_DIR/mutations.log" >&2
  fail "B2u mutation suite rejected"
fi
count_exact 1 '^Ran 40 tests in [0-9.]+s$' "$BUILD_DIR/mutations.log"
count_exact 1 '^OK$' "$BUILD_DIR/mutations.log"

FLAGS='-O0 -g -std=f2008 -pedantic -Wall -Wextra -Werror'
FLAGS="$FLAGS -fimplicit-none -fcheck=all -fbacktrace"
FLAGS="$FLAGS -ffp-contract=off -fno-fast-math"
FIXED_FLAGS='-O0 -g -std=legacy -ffixed-line-length-none -Wall -Wextra -Werror'
GANMOD="$ROOT/Ganlib/lib/Darwin_arm64/modules"
GANLIB="$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a"

# Compile the complete production interface chain.  B2S's numerical core is
# represented only by its established capture modules, so nothing is linked
# or executed here.
copy_exact "$B2S_CAPTURE_STUB" "$SOURCE_DIR/b2s_capture_stubs.f90"
for source in SPOR64_B2C SPOR64_B2B SPOR64_B2O SPOR64_B2R SPOR64_B2S \
  SPOR64_B2K SPOR64_B2N SPOR64_B2T SPOR64_B2U
do
  copy_exact "$ROOT/src/$source.f90" "$SOURCE_DIR/$source.f90"
done
"$FC" $FLAGS -Wno-unused-dummy-argument -I "$GANMOD" \
  -J "$ACTUAL_OBJECT_DIR" -c "$SOURCE_DIR/b2s_capture_stubs.f90" \
  -o "$ACTUAL_OBJECT_DIR/b2s_capture_stubs.o"
for source in SPOR64_B2C SPOR64_B2B SPOR64_B2O SPOR64_B2R SPOR64_B2S \
  SPOR64_B2K SPOR64_B2N SPOR64_B2T SPOR64_B2U
do
  "$FC" $FLAGS -I "$ACTUAL_OBJECT_DIR" -I "$GANMOD" \
    -J "$ACTUAL_OBJECT_DIR" -c "$SOURCE_DIR/$source.f90" \
    -o "$ACTUAL_OBJECT_DIR/$source.o"
done
nm -g "$ACTUAL_OBJECT_DIR/SPOR64_B2U.o" >"$BUILD_DIR/actual-b2u.nm"
count_exact 1 ' T _spor64t_$' "$BUILD_DIR/actual-b2u.nm"
count_exact 1 ' U ___spor64_b2t_MOD_spor64_b2t_host_step$' \
  "$BUILD_DIR/actual-b2u.nm"
count_exact 1 ' U _redget_$' "$BUILD_DIR/actual-b2u.nm"
count_exact 1 ' U _xabort_$' "$BUILD_DIR/actual-b2u.nm"

# Compile the two legacy host objects without linking or invoking them.
copy_exact "$ROOT/src/ASM.f" "$SOURCE_DIR/ASM.f"
copy_exact "$ROOT/src/KDRDRV.F" "$SOURCE_DIR/KDRDRV.F"
"$FC" $FIXED_FLAGS -cpp -I "$GANMOD" -c "$SOURCE_DIR/ASM.f" \
  -o "$HOST_OBJECT_DIR/ASM.o"
"$CPP" -P -W -traditional -DLinux -DUnix "$SOURCE_DIR/KDRDRV.F" \
  "$HOST_OBJECT_DIR/KDRDRV.pp.f"
"$FC" $FIXED_FLAGS -I "$GANMOD" -c "$HOST_OBJECT_DIR/KDRDRV.pp.f" \
  -o "$HOST_OBJECT_DIR/KDRDRV.o"
nm -g "$HOST_OBJECT_DIR/ASM.o" >"$BUILD_DIR/asm.nm"
nm -g "$HOST_OBJECT_DIR/KDRDRV.o" >"$BUILD_DIR/kdrdrv.nm"
count_exact 1 ' T _asm_$' "$BUILD_DIR/asm.nm"
count_exact 1 ' U _xdrta2_$' "$BUILD_DIR/asm.nm"
count_exact 1 ' T _kdrdrv_$' "$BUILD_DIR/kdrdrv.nm"
count_exact 1 ' U _spor64t_$' "$BUILD_DIR/kdrdrv.nm"

# Use the real CLEPIL/OBJPIL compiler for the production procedure and for
# both validation selection shapes.  Compiling these decks never dispatches
# ASM, SPOR64T, B2T, or Dragon.
copy_exact "$C2M_HELPER" "$SOURCE_DIR/compile_c2m.c"
"$CC" -std=c11 -pedantic -Wall -Wextra -Werror \
  -I "$ROOT/Ganlib/src" -c "$SOURCE_DIR/compile_c2m.c" \
  -o "$C2M_DIR/compile_c2m.o"
"$FC" "$C2M_DIR/compile_c2m.o" "$GANLIB" -o "$C2M_DIR/compile_c2m"
if ! (
  cd "$C2M_DIR"
  run_limited ./compile_c2m "$ROOT/data/SpotStepR64.c2m" \
    SpotStepR64.o2m >SpotStepR64.log 2>&1
)
then
  sed -n '1,240p' "$C2M_DIR/SpotStepR64.log" >&2
  fail "CLEPIL/OBJPIL compilation of SpotStepR64 failed"
fi
if ! (
  cd "$C2M_DIR"
  run_limited ./compile_c2m "$HERE/b2u_stub_off.c2m" \
    b2u_stub_off.o2m >b2u_stub_off.log 2>&1
)
then
  sed -n '1,240p' "$C2M_DIR/b2u_stub_off.log" >&2
  fail "CLEPIL/OBJPIL compilation of OFF deck failed"
fi
if ! (
  cd "$C2M_DIR"
  run_limited ./compile_c2m "$HERE/b2u_stub_on.c2m" \
    b2u_stub_on.o2m >b2u_stub_on.log 2>&1
)
then
  sed -n '1,240p' "$C2M_DIR/b2u_stub_on.log" >&2
  fail "CLEPIL/OBJPIL compilation of ON deck failed"
fi
for object in SpotStepR64.o2m b2u_stub_off.o2m b2u_stub_on.o2m
do
  [ -s "$C2M_DIR/$object" ] || fail "empty compiled C2M object: $object"
done

# Execute only the thin production SPOR64T adapter.  REDGET and the whole B2T
# boundary are deterministic capture stubs, so this cannot enter a solver.
copy_exact "$PROBES" "$SOURCE_DIR/b2u_adapter_probes.f90"
copy_exact "$STUBS" "$SOURCE_DIR/b2u_adapter_stubs.f90"
copy_exact "$HARNESS" "$SOURCE_DIR/test_spor64t_adapter.f90"
"$FC" $FLAGS -J "$ADAPTER_OBJECT_DIR" \
  -c "$SOURCE_DIR/b2u_adapter_probes.f90" \
  -o "$ADAPTER_OBJECT_DIR/b2u_adapter_probes.o"
"$FC" $FLAGS -I "$ADAPTER_OBJECT_DIR" -J "$ADAPTER_OBJECT_DIR" \
  -c "$SOURCE_DIR/b2u_adapter_stubs.f90" \
  -o "$ADAPTER_OBJECT_DIR/b2u_adapter_stubs.o"
"$FC" $FLAGS -I "$ADAPTER_OBJECT_DIR" -I "$GANMOD" \
  -J "$ADAPTER_OBJECT_DIR" -c "$SOURCE_DIR/SPOR64_B2U.f90" \
  -o "$ADAPTER_OBJECT_DIR/SPOR64_B2U.o"
"$FC" $FLAGS -I "$ADAPTER_OBJECT_DIR" -J "$ADAPTER_OBJECT_DIR" \
  -c "$SOURCE_DIR/test_spor64t_adapter.f90" \
  -o "$ADAPTER_OBJECT_DIR/test_spor64t_adapter.o"
"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$ADAPTER_OBJECT_DIR/b2u_adapter_probes.o" \
  "$ADAPTER_OBJECT_DIR/b2u_adapter_stubs.o" \
  "$ADAPTER_OBJECT_DIR/SPOR64_B2U.o" \
  "$ADAPTER_OBJECT_DIR/test_spor64t_adapter.o" \
  -o "$BUILD_DIR/test_spor64t_adapter"
nm -g "$BUILD_DIR/test_spor64t_adapter" >"$BUILD_DIR/adapter.nm"
count_exact 1 ' T _spor64t_$' "$BUILD_DIR/adapter.nm"
count_exact 1 ' T ___spor64_b2t_MOD_spor64_b2t_host_step$' \
  "$BUILD_DIR/adapter.nm"
if grep -Eiq \
  '(^|[[:space:]])_?(asm|asmdrv|dragon|flu|fludrv|xdrta2|spomoc)_$|___spor64_b2[bciknors]_' \
  "$BUILD_DIR/adapter.nm"
then
  fail "adapter witness links a production solver or downstream B2 module"
fi
if ! run_limited "$BUILD_DIR/test_spor64t_adapter" \
  >"$BUILD_DIR/adapter.log" 2>&1
then
  sed -n '1,240p' "$BUILD_DIR/adapter.log" >&2
  fail "production SPOR64T adapter witness rejected"
fi
count_exact 1 '^B2U SPOR64T ADAPTER STUB PASS$' "$BUILD_DIR/adapter.log"
count_exact 1 '^B2U NEGATIVES=NENTRY,HENTRY,IENTRY,JENTRY,REDGET,B2T-FAIL$' \
  "$BUILD_DIR/adapter.log"
count_exact 1 '^B2U SUCCESS B2T-STUB=1 SYSTEM-BINDINGS=3 TRACK-HANDLE=CURRENT-CALL$' \
  "$BUILD_DIR/adapter.log"
count_exact 1 '^B2U CUTOFF=INT64-PER-PLANE-DIAGNOSTIC-ONLY$' \
  "$BUILD_DIR/adapter.log"
count_exact 1 '^B2U REAL-ASM=0 REAL-B2T=0 FLU=0 TRANSPORT=0 PICARD=0$' \
  "$BUILD_DIR/adapter.log"
[ "$(wc -l <"$BUILD_DIR/adapter.log" | tr -d '[:space:]')" -eq 5 ] || \
  fail "unexpected adapter witness output"

verify_parent
verify_receipt
verify_track
git -C "$ROOT" diff --check

printf '%s\n' 'SPOR64 PHASE-A9b-B2u SAME-CALL ASM HOST PASS'
printf '%s\n' 'DEPLOYMENT-DEFAULT=OFF SHIPPED-SELECTIONS=0'
printf '%s\n' 'HOST=ASM-LK1D-1,2,3->SPOR64T->B2T STATIC+C2M-COMPILED'
printf '%s\n' 'SPOR64T-ADAPTER=PRODUCTION EXECUTIONS=7 B2T=CAPTURE-STUB'
printf '%s\n' 'TRACK-CONTRACT=SAME-CLE-SYMBOL HASH-PINNED-INTENDED-FILE PER-DISPATCH-REOPEN-SEMANTICS'
printf '%s\n' 'TRACK-RUNTIME-OPENS=0 CROSS-CALL-CPTR=NOT-CLAIMED'
printf '%s\n' 'STATIC-CONTRACT-TESTS=40 TARGETED-MUTATIONS=39'
printf '%s\n' 'PRODUCTION-CHAIN=B2C,B2B,B2O,B2R,B2S,B2K,B2N,B2T,B2U COMPILE-ONLY'
printf '%s\n' 'C2M-COMPILES=3 ASM-COMPILE=1 KDRDRV-COMPILE=1'
printf '%s\n' 'DRAGON=0 REAL-ASM=0 REAL-B2T=0 TRANSPORT=0 PICARD=0'
printf '%s\n' 'EMPIRICAL-COEFFICIENTS-ADDED=0 LONG-CALCULATIONS=0'
if [ -f "$RECEIPT" ]; then
  printf '%s\n' 'RECEIPT=FROZEN PARENT=B2t'
else
  printf '%s\n' 'RECEIPT=PENDING-MAIN-AUDIT PARENT=B2t'
fi
