#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)
B2L_DIR="$ROOT/validation/iterative/real64_phase_a9b_b2l_one_plane_real_asm"
B2K_DIR="$ROOT/validation/iterative/real64_phase_a9b_b2k_system_assembly"
PARENT_RECEIPT="$B2L_DIR/phase_a9b_b2l_one_plane_real_asm_receipt.sha256"
RECEIPT="$HERE/phase_a9b_b2m_three_plane_real_asm_commit_receipt.sha256"
EXPECTED_PARENT_COMMIT=66e12bdd39162f8f25f80b86f2384b1260f4f30e
EXPECTED_PARENT_HASH=2eb0b3c201757395abeaf2ebc83e4863d26b3e3c67acbb6d7dc5c5cb5167ca38
FC=/opt/homebrew/bin/gfortran
EXPECTED_FC_BANNER='GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0'
CC=/usr/bin/cc
CPP=/usr/bin/cpp
AR=/usr/bin/ar
RUN_B2M=${RUN_B2M:-0}
PRESERVE_B2M_FAILURE=${PRESERVE_B2M_FAILURE:-0}

STATIC_CHECKER="$HERE/check_phase_a9b_b2m_three_plane_real_asm_commit.py"
CONTRACT_TEST=test_phase_a9b_b2m_three_plane_real_asm_commit_contract
BOUNDED="$HERE/run_bounded_b2m.py"
BOUNDED_TEST=test_run_bounded_b2m
PREPARER="$B2L_DIR/prepare_b2l_projected.f90"
POSTERIOR="$HERE/check_b2m_three_plane_assembled.f90"
DECK="$HERE/three_plane_real_asm_commit.x2m"
C2M_SOURCE="$ROOT/data/SpotAsmR64.c2m"
C2M_HELPER="$B2K_DIR/compile_c2m.c"
EXPECTED_C2M_SOURCE_HASH=31ec89036bbd2ea62b27fbd4dff5aa1054f3f24997e383f05389e1dda91e364d

AX_ARTIFACT="$ROOT/validation/artifacts/iterative-map1/state1_axial.xsm"
ARCHIVE_ARTIFACT="$ROOT/validation/artifacts/iterative-map1/state1_snapshots.xsm"
AXIAL_TRACK_ARTIFACT="$ROOT/validation/artifacts/iterative-seed/initial_axial_track.xsm"
RADIAL_TRACK_ARTIFACT="$ROOT/validation/artifacts/iterative-seed/initial_radial_track.bin"
EXPECTED_AX_HASH=2323a256002f1e6f75f5af72c31479b0f6a7bff561d401cee363dcf9fc6ff484
EXPECTED_ARCHIVE_HASH=1b5a0c98aba0f5b4f366b64a8157f4a104df0f89f4cdeafc60eb6ce7811018e1
EXPECTED_AXIAL_TRACK_HASH=101ba0ad64c91723fdeb002e62c6226347fcfaeff188e125d699d70e113febc7
EXPECTED_RADIAL_TRACK_HASH=f7b27cb4a5d37f903b93e49610e2daa2290d55c164e2ca0e73ccb8d22fe486b8
EXPECTED_PROJECTED_HASH=c010c0a860884a4e4d3842dffe45ffb4898f2aaca99557e0411ee8c66d60b90c
EXPECTED_PROJECTED_BYTES=225315452

BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-a9b-b2m.XXXXXX")
SOURCE_DIR="$BUILD_DIR/source"
OBJECT_DIR="$BUILD_DIR/objects"
HOST_DIR="$BUILD_DIR/host"
CASE_DIR="$BUILD_DIR/case"

cleanup()
{
  status=$?
  trap - EXIT HUP INT TERM
  if [ "$status" -ne 0 ] && [ -d "$CASE_DIR" ]; then
    for log in prepare.log assembly.log posterior_a.log posterior_b.log
    do
      if [ -f "$CASE_DIR/$log" ]; then
        printf '%s\n' "--- retained tail before cleanup: $log ---" >&2
        tail -n 160 "$CASE_DIR/$log" >&2
        printf '%s\n' "--- end retained tail: $log ---" >&2
      fi
    done
  fi
  if [ "$status" -ne 0 ] && [ "$PRESERVE_B2M_FAILURE" = 1 ]; then
    printf '%s\n' "B2M FAILURE ARTIFACTS PRESERVED: $BUILD_DIR" >&2
    exit "$status"
  fi
  cd /
  rm -rf "$BUILD_DIR"
  exit "$status"
}

trap cleanup EXIT HUP INT TERM

LC_ALL=C
export LC_ALL

fail()
{
  printf '%s\n' "SPOR64 PHASE-A9b-B2m FAILURE: $*" >&2
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

require_hash()
{
  path=$1
  expected=$2
  [ "$(hash_of "$path")" = "$expected" ] || fail "hash differs: $path"
}

verify_receipts()
{
  [ -f "$PARENT_RECEIPT" ] || fail "B2l parent receipt missing"
  require_hash "$PARENT_RECEIPT" "$EXPECTED_PARENT_HASH"
  if [ -f "$RECEIPT" ]; then
    (
      cd "$ROOT"
      shasum -a 256 -c "$RECEIPT" >/dev/null
    ) || fail "B2m receipt verification failed"
  fi
}

require_normal_end()
{
  log=$1
  count_exact 1 \
    '^ normal end of execution for dragon 5  Version 5\.1\.0[[:space:]]*$' \
    "$log"
  count_exact 1 'normal end of execution for dragon' "$log"
  if grep -Ei \
    'XABORT|segmentation fault|floating invalid|NaN|Infinity|SIGKILL|SIGTERM' \
    "$log" >/dev/null
  then
    fail "abnormal Dragon text; INVALID-NO-SCIENTIFIC-RESULT"
  fi
}

show_failure_log()
{
  log=$1
  if [ -f "$log" ]; then
    printf '%s\n' "--- bounded child log: $log ---" >&2
    tail -n 160 "$log" >&2
    printf '%s\n' '--- end bounded child log ---' >&2
  fi
}

case "$RUN_B2M" in
  0|1) ;;
  *) fail "RUN_B2M must be exactly 0 or 1" ;;
esac
case "$PRESERVE_B2M_FAILURE" in
  0|1) ;;
  *) fail "PRESERVE_B2M_FAILURE must be exactly 0 or 1" ;;
esac

[ "$(uname -s)" = Darwin ] || fail "frozen platform is Darwin"
[ "$(uname -m)" = arm64 ] || fail "frozen architecture is arm64"
[ -x "$FC" ] || fail "frozen compiler missing"
[ -x "$CC" ] || fail "host C compiler missing"
[ -x "$CPP" ] || fail "host preprocessor missing"
[ -x "$AR" ] || fail "host archive tool missing"
FC_BANNER=$("$FC" --version | sed -n '1p')
[ "$FC_BANNER" = "$EXPECTED_FC_BANNER" ] || fail "unaudited compiler"

for source in SPOR64_B2C SPOR64_B2I SPOR64_B2H SPOR64_B2J SPOR64_B2K
do
  [ -f "$ROOT/src/$source.f90" ] || fail "production $source missing"
done
for source in ASM.f ASMDRV.f XDRTA2.f KDRDRV.F DOORAV.f MCCGA.f MCGASM.f
do
  [ -f "$ROOT/src/$source" ] || fail "production $source missing"
done
for path in "$STATIC_CHECKER" "$HERE/$CONTRACT_TEST.py" "$BOUNDED" \
  "$HERE/$BOUNDED_TEST.py" "$PREPARER" "$POSTERIOR" "$DECK" \
  "$C2M_SOURCE" "$C2M_HELPER" \
  "$AX_ARTIFACT" "$ARCHIVE_ARTIFACT" \
  "$AXIAL_TRACK_ARTIFACT" "$RADIAL_TRACK_ARTIFACT"
do
  [ -f "$path" ] || fail "required input missing: $path"
done

require_hash "$AX_ARTIFACT" "$EXPECTED_AX_HASH"
require_hash "$ARCHIVE_ARTIFACT" "$EXPECTED_ARCHIVE_HASH"
require_hash "$AXIAL_TRACK_ARTIFACT" "$EXPECTED_AXIAL_TRACK_HASH"
require_hash "$RADIAL_TRACK_ARTIFACT" "$EXPECTED_RADIAL_TRACK_HASH"
require_hash "$C2M_SOURCE" "$EXPECTED_C2M_SOURCE_HASH"
git -C "$ROOT" cat-file -e "$EXPECTED_PARENT_COMMIT^{commit}" || \
  fail "B2l parent commit missing"
git -C "$ROOT" merge-base --is-ancestor "$EXPECTED_PARENT_COMMIT" HEAD || \
  fail "B2l parent commit is not an ancestor"
verify_receipts

PYTHONDONTWRITEBYTECODE=1 python3 "$STATIC_CHECKER"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$HERE" python3 -m unittest -v \
  "$CONTRACT_TEST" "$BOUNDED_TEST"

mkdir -p "$SOURCE_DIR" "$OBJECT_DIR" "$HOST_DIR" "$CASE_DIR"
for source in SPOR64_B2C SPOR64_B2I SPOR64_B2H SPOR64_B2J SPOR64_B2K
do
  copy_exact "$ROOT/src/$source.f90" "$SOURCE_DIR/$source.f90"
done
for source in ASM.f KDRDRV.F
do
  copy_exact "$ROOT/src/$source" "$SOURCE_DIR/$source"
done
copy_exact "$PREPARER" "$SOURCE_DIR/prepare_b2l_projected.f90"
copy_exact "$POSTERIOR" "$SOURCE_DIR/check_b2m_three_plane_assembled.f90"
copy_exact "$C2M_HELPER" "$SOURCE_DIR/compile_c2m.c"
copy_exact "$DECK" "$CASE_DIR/three_plane_real_asm_commit.x2m"

FLAGS='-O0 -g -std=f2008 -pedantic -Wall -Wextra -Werror'
FLAGS="$FLAGS -fimplicit-none -fcheck=all -fbacktrace"
FLAGS="$FLAGS -ffp-contract=off -fno-fast-math"
GANMOD="$ROOT/Ganlib/lib/Darwin_arm64/modules"
GANLIB="$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a"
UTILIB="$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a"

for source in SPOR64_B2C SPOR64_B2I SPOR64_B2H SPOR64_B2J SPOR64_B2K
do
  "$FC" $FLAGS -I "$GANMOD" -I "$OBJECT_DIR" -J "$OBJECT_DIR" \
    -c "$SOURCE_DIR/$source.f90" -o "$OBJECT_DIR/$source.o"
done
"$FC" $FLAGS -I "$GANMOD" -I "$OBJECT_DIR" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/prepare_b2l_projected.f90" \
  -o "$OBJECT_DIR/prepare_b2l_projected.o"
"$FC" $FLAGS -I "$GANMOD" -I "$OBJECT_DIR" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/check_b2m_three_plane_assembled.f90" \
  -o "$OBJECT_DIR/check_b2m_three_plane_assembled.o"

"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$OBJECT_DIR/SPOR64_B2C.o" "$OBJECT_DIR/SPOR64_B2I.o" \
  "$OBJECT_DIR/SPOR64_B2H.o" "$OBJECT_DIR/SPOR64_B2J.o" \
  "$OBJECT_DIR/prepare_b2l_projected.o" "$GANLIB" "$UTILIB" \
  -o "$BUILD_DIR/prepare_b2l_projected"
"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$OBJECT_DIR/check_b2m_three_plane_assembled.o" "$GANLIB" "$UTILIB" \
  -o "$BUILD_DIR/check_b2m_three_plane_real_asm_commit"

nm -g "$BUILD_DIR/check_b2m_three_plane_real_asm_commit" \
  >"$BUILD_DIR/posterior.nm"
if grep -Eiq \
  '(^|[[:space:]])_?(asm|asmdrv|doorav|doorpv|mccga|mcgasm|flu|fludrv|spor64k)_$|spor64_' \
  "$BUILD_DIR/posterior.nm"
then
  fail "independent posterior links a production solver or lifecycle gate"
fi
grep -i 'lcmop' "$BUILD_DIR/posterior.nm" >/dev/null || \
  fail "independent posterior lacks GANLIB read path"

"$CC" -std=c11 -pedantic -Wall -Wextra -Werror \
  -I "$ROOT/Ganlib/src" -c "$SOURCE_DIR/compile_c2m.c" \
  -o "$OBJECT_DIR/compile_c2m.o"
"$FC" "$OBJECT_DIR/compile_c2m.o" "$GANLIB" \
  -o "$BUILD_DIR/compile_c2m"
if ! (
  cd "$BUILD_DIR"
  ./compile_c2m "$C2M_SOURCE" SpotAsmR64.o2m >candidate_compile.log 2>&1
); then
  sed -n '1,240p' "$BUILD_DIR/candidate_compile.log" >&2
  fail "CLEPIL/OBJPIL compilation of SpotAsmR64.c2m failed"
fi
[ -s "$BUILD_DIR/SpotAsmR64.o2m" ] || fail "empty compiled SpotAsmR64"
if ! (
  cd "$BUILD_DIR"
  ./compile_c2m "$DECK" three_plane_real_asm_commit.o2m \
    >deck_compile.log 2>&1
); then
  sed -n '1,240p' "$BUILD_DIR/deck_compile.log" >&2
  fail "CLEPIL/OBJPIL compilation of B2m deck failed"
fi
[ -s "$BUILD_DIR/three_plane_real_asm_commit.o2m" ] || \
  fail "empty compiled B2m deck"
# kdrdpr.c requires the declared procedure's .c2m companion to exist even
# when its .o2m was compiled in advance.  Recursive cle2000_c first opens the
# existing .o2m, so the object remains the executed payload; the copied source
# is the exact, hash-frozen declaration/provenance companion.
C2M_OBJECT_HASH=$(hash_of "$BUILD_DIR/SpotAsmR64.o2m")
copy_exact "$C2M_SOURCE" "$CASE_DIR/SpotAsmR64.c2m"
copy_exact "$BUILD_DIR/SpotAsmR64.o2m" "$CASE_DIR/SpotAsmR64.o2m"
require_hash "$CASE_DIR/SpotAsmR64.c2m" "$EXPECTED_C2M_SOURCE_HASH"
require_hash "$CASE_DIR/SpotAsmR64.o2m" "$C2M_OBJECT_HASH"
[ ! -e "$CASE_DIR/SpotAsmR64.l2m" ] || \
  fail "unexpected pre-run procedure listing"

HOST_FLAGS='-fPIC -Wall -frecord-marker=4 -ffpe-summary=none'
HOST_FLAGS="$HOST_FLAGS -O2 -march=native -ffp-contract=off"
"$FC" $HOST_FLAGS -I "$GANMOD" -c "$SOURCE_DIR/ASM.f" \
  -ffixed-line-length-72 -o "$HOST_DIR/ASM.o"
"$CPP" -P -W -traditional -DLinux -DUnix "$SOURCE_DIR/KDRDRV.F" \
  "$HOST_DIR/KDRDRV.pp.f"
"$FC" $HOST_FLAGS -I "$GANMOD" -c "$HOST_DIR/KDRDRV.pp.f" \
  -ffixed-line-length-72 -o "$HOST_DIR/KDRDRV.o"
"$FC" $HOST_FLAGS -I "$GANMOD" -I "$OBJECT_DIR" -J "$HOST_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2K.f90" -o "$HOST_DIR/SPOR64_B2K.o"
cp "$ROOT/lib/Darwin_arm64/libDragon.a" "$HOST_DIR/libDragon.b2m.a"
"$AR" rcs "$HOST_DIR/libDragon.b2m.a" "$HOST_DIR/ASM.o" \
  "$HOST_DIR/KDRDRV.o" "$HOST_DIR/SPOR64_B2K.o"
"$AR" t "$HOST_DIR/libDragon.b2m.a" >"$HOST_DIR/archive-members.txt"
"$FC" -O2 -march=native -ffp-contract=off \
  "$ROOT/src/DRAGON.o" "$HOST_DIR/libDragon.b2m.a" \
  "$ROOT/Trivac/lib/Darwin_arm64/libTrivac.a" "$UTILIB" "$GANLIB" \
  -o "$BUILD_DIR/Dragon.b2m"

nm -g "$BUILD_DIR/Dragon.b2m" >"$BUILD_DIR/Dragon.nm"
for symbol in _asm_ _asmdrv_ _doorav_ _mccga_ _mcgasm_ _spor64k_ _xdrta2_
do
  count_exact 1 " T ${symbol}$" "$BUILD_DIR/Dragon.nm"
done
for member in ASM.o KDRDRV.o SPOR64_B2K.o
do
  count_exact 1 "^${member}$" "$HOST_DIR/archive-members.txt"
done

if [ "$RUN_B2M" = 0 ]; then
  printf '%s\n' 'SPOR64 PHASE-A9b-B2m PREFLIGHT PASS'
  printf '%s\n' \
    'ACTIVATION=DEFAULT-OFF; SET RUN_B2M=1 FOR ONE BOUNDED THREE-PLANE COMMIT'
  printf '%s\n' \
    'DRAGON-EXECUTIONS=0 ASM-EXECUTIONS=0 SPOR64K-EXECUTIONS=0 FLU=0 CONT=0'
  printf '%s\n' 'THREE-PLANE-REAL-ASM-COMMIT=NOT-EVALUATED'
  exit 0
fi
[ "$RUN_B2M" = 1 ] || fail "runtime activation is not exactly one"

ln -s "$AX_ARTIFACT" "$CASE_DIR/ax.xsm"
ln -s "$ARCHIVE_ARTIFACT" "$CASE_DIR/archive.xsm"
ln -s "$AXIAL_TRACK_ARTIFACT" "$CASE_DIR/axial_track.xsm"
ln -s "$RADIAL_TRACK_ARTIFACT" "$CASE_DIR/initial_radial_track.bin"
[ ! -e "$CASE_DIR/projected.xsm" ] || fail "PROJECTED output path exists"
[ ! -e "$CASE_DIR/assembled.xsm" ] || fail "ASSEMBLED output path exists"

if ! python3 "$BOUNDED" prepare "$BUILD_DIR/prepare_b2l_projected" - \
  "$CASE_DIR/prepare.log" ax.xsm archive.xsm axial_track.xsm projected.xsm
then
  show_failure_log "$CASE_DIR/prepare.log"
  fail "bounded PROJECTED preparation failed; INVALID-NO-SCIENTIFIC-RESULT"
fi
count_exact 1 '^B2L FULL PROJECTED PREPARATION PASS$' "$CASE_DIR/prepare.log"
count_exact 1 '^B2L PRODUCTION-B2C-CALLS=3 B2I-CALLS=1 B2J-CALLS=1$' \
  "$CASE_DIR/prepare.log"
count_exact 1 '^B2L FULL-TRACK-LIBRARY-SYSTEM-COPIES=9$' \
  "$CASE_DIR/prepare.log"
count_exact 1 '^B2L POST-B2J-MUTATIONS=0 PROJECTED-SYSTEM=ABSENT$' \
  "$CASE_DIR/prepare.log"
[ "$(wc -l <"$CASE_DIR/prepare.log" | tr -d '[:space:]')" -eq 4 ] || \
  fail "materializer output inventory differs"
[ -s "$CASE_DIR/projected.xsm" ] || fail "PROJECTED materialization missing"
[ ! -L "$CASE_DIR/projected.xsm" ] || fail "PROJECTED output is a symlink"
PROJECTED_BYTES=$(stat -f '%z' "$CASE_DIR/projected.xsm")
[ "$PROJECTED_BYTES" -eq "$EXPECTED_PROJECTED_BYTES" ] || \
  fail "PROJECTED byte count differs from B2l evidence"
PROJECTED_HASH=$(hash_of "$CASE_DIR/projected.xsm")
[ "$PROJECTED_HASH" = "$EXPECTED_PROJECTED_HASH" ] || \
  fail "PROJECTED hash differs from B2l evidence"

if ! python3 "$BOUNDED" assemble3 "$BUILD_DIR/Dragon.b2m" \
  "$CASE_DIR/three_plane_real_asm_commit.x2m" "$CASE_DIR/assembly.log"
then
  show_failure_log "$CASE_DIR/assembly.log"
  fail "bounded three-plane assembly failed; INVALID-NO-SCIENTIFIC-RESULT"
fi
require_normal_end "$CASE_DIR/assembly.log"
if grep -E \
  'COMPILING _MAIN\.c2m FILE|BAD OBJECTS _MAIN\.c2m FILE' \
  "$CASE_DIR/assembly.log" >/dev/null
then
  fail "runtime procedure compilation error detected; INVALID-NO-SCIENTIFIC-RESULT"
fi
[ ! -e "$CASE_DIR/SpotAsmR64.l2m" ] || \
  fail "runtime procedure source-compilation branch detected; INVALID-NO-SCIENTIFIC-RESULT"
count_exact 3 '^->@BEGIN MODULE : ASM:[[:space:]]*$' "$CASE_DIR/assembly.log"
count_exact 3 '^->@END MODULE   : ASM:[[:space:]]*$' "$CASE_DIR/assembly.log"
count_exact 3 '^-->>MODULE ASM:[[:space:]]*: TIME SPENT=' "$CASE_DIR/assembly.log"
count_exact 1 '^->@BEGIN MODULE : SPOR64K:[[:space:]]*$' \
  "$CASE_DIR/assembly.log"
count_exact 1 '^->@END MODULE   : SPOR64K:[[:space:]]*$' \
  "$CASE_DIR/assembly.log"
count_exact 1 '^-->>MODULE SPOR64K:[[:space:]]*: TIME SPENT=' \
  "$CASE_DIR/assembly.log"
count_exact 1 \
  '^>\|B2M-THREE-PLANE-REAL-ASM-BEGIN[[:space:]]*\|>[0-9][0-9][0-9][0-9]$' \
  "$CASE_DIR/assembly.log"
count_exact 1 \
  '^>\|B2M-THREE-PLANE-REAL-ASM-COMPLETE[[:space:]]*\|>[0-9][0-9][0-9][0-9]$' \
  "$CASE_DIR/assembly.log"
if grep -E -- \
  '->@BEGIN MODULE : (FLU|SPOFSRC|SPOFCHK|CONT):' \
  "$CASE_DIR/assembly.log" >/dev/null
then
  fail "forbidden runtime module reached; INVALID-NO-SCIENTIFIC-RESULT"
fi
[ -s "$CASE_DIR/assembled.xsm" ] || fail "ASSEMBLED XSM output missing"
[ ! -L "$CASE_DIR/assembled.xsm" ] || fail "ASSEMBLED output is a symlink"
[ "$(stat -f '%z' "$CASE_DIR/assembled.xsm")" -le 536870912 ] || \
  fail "ASSEMBLED output cap exceeded"
for path in system1.xsm system2.xsm system3.xsm
do
  [ ! -e "$CASE_DIR/$path" ] || fail "unexpected raw SYSTEM artifact: $path"
done
[ "$(hash_of "$CASE_DIR/projected.xsm")" = "$PROJECTED_HASH" ] || \
  fail "PROJECTED input mutated during three-plane assembly"

if ! python3 "$BOUNDED" posterior \
  "$BUILD_DIR/check_b2m_three_plane_real_asm_commit" - \
  "$CASE_DIR/posterior_a.log" projected.xsm assembled.xsm
then
  show_failure_log "$CASE_DIR/posterior_a.log"
  fail "first independent posterior failed"
fi
if ! python3 "$BOUNDED" posterior \
  "$BUILD_DIR/check_b2m_three_plane_real_asm_commit" - \
  "$CASE_DIR/posterior_b.log" projected.xsm assembled.xsm
then
  show_failure_log "$CASE_DIR/posterior_b.log"
  fail "second independent posterior failed"
fi
cmp "$CASE_DIR/posterior_a.log" "$CASE_DIR/posterior_b.log" || \
  fail "read-only posterior output is not repeatable"
count_exact 1 '^B2M THREE-PLANE COMMIT POSTERIOR PASS$' \
  "$CASE_DIR/posterior_a.log"
count_exact 1 \
  '^B2M ROOT-ENTRIES=8 SYSTEMS=3 ROOT-STATE=ASSEMBLED/1$' \
  "$CASE_DIR/posterior_a.log"
count_exact 1 \
  '^B2M COPIED-LIST-ITEMS=9 FULL-COPY-RECORDS=[1-9][0-9]* FULL-COPY-32BIT-WORDS=[1-9][0-9]*$' \
  "$CASE_DIR/posterior_a.log"
count_exact 1 \
  '^B2M GROUPS=1110 EXACT-GROUP-RECORDS=16650$' \
  "$CASE_DIR/posterior_a.log"
count_exact 1 \
  '^B2M RESPONSE-FINITE-VALUES=179820 RESPONSE-NONZERO-VALUES=[1-9][0-9]*$' \
  "$CASE_DIR/posterior_a.log"
count_exact 1 \
  '^B2M PLANE1-NONZERO=[1-9][0-9]* PLANE2-NONZERO=[1-9][0-9]* PLANE3-NONZERO=[1-9][0-9]*$' \
  "$CASE_DIR/posterior_a.log"
count_exact 1 \
  '^B2M LEAKAGE-BITS=1110 TXSC-BITS=9990 S0PHYS-BITS=9990 S0USED-BITS=9990$' \
  "$CASE_DIR/posterior_a.log"
count_exact 1 \
  '^B2M SYSTEM-STATES=ASSEMBLED/1x3 FLUX-STATES=PROJECTED/1x3$' \
  "$CASE_DIR/posterior_a.log"
count_exact 1 \
  '^B2M THREE-PLANE-B2K-POSTERIOR=COMPATIBLE EMPIRICAL-CONTROLS=0$' \
  "$CASE_DIR/posterior_a.log"
count_exact 1 \
  '^B2M RESPONSE-ACCURACY=NOT-EVALUATED CONVERGENCE=NOT-EVALUATED$' \
  "$CASE_DIR/posterior_a.log"
[ "$(wc -l <"$CASE_DIR/posterior_a.log" | tr -d '[:space:]')" -eq 10 ] || \
  fail "posterior output inventory differs"

require_hash "$AX_ARTIFACT" "$EXPECTED_AX_HASH"
require_hash "$ARCHIVE_ARTIFACT" "$EXPECTED_ARCHIVE_HASH"
require_hash "$AXIAL_TRACK_ARTIFACT" "$EXPECTED_AXIAL_TRACK_HASH"
require_hash "$RADIAL_TRACK_ARTIFACT" "$EXPECTED_RADIAL_TRACK_HASH"
require_hash "$C2M_SOURCE" "$EXPECTED_C2M_SOURCE_HASH"
require_hash "$CASE_DIR/SpotAsmR64.c2m" "$EXPECTED_C2M_SOURCE_HASH"
require_hash "$CASE_DIR/SpotAsmR64.o2m" "$C2M_OBJECT_HASH"
[ ! -e "$CASE_DIR/SpotAsmR64.l2m" ] || \
  fail "procedure listing appeared during posterior"
[ "$(hash_of "$CASE_DIR/projected.xsm")" = "$PROJECTED_HASH" ] || \
  fail "PROJECTED input mutated during posterior"
verify_receipts

ASSEMBLED_HASH=$(hash_of "$CASE_DIR/assembled.xsm")
ASSEMBLED_BYTES=$(stat -f '%z' "$CASE_DIR/assembled.xsm")
FULL_COPY_LINE=$(grep '^B2M COPIED-LIST-ITEMS=' \
  "$CASE_DIR/posterior_a.log")
RESPONSE_LINE=$(grep '^B2M RESPONSE-FINITE-VALUES=' \
  "$CASE_DIR/posterior_a.log")
PLANE_NONZERO_LINE=$(grep '^B2M PLANE1-NONZERO=' \
  "$CASE_DIR/posterior_a.log")
FORMULA_LINE=$(grep '^B2M LEAKAGE-BITS=' \
  "$CASE_DIR/posterior_a.log")

printf '%s\n' 'SPOR64 PHASE-A9b-B2m THREE-PLANE-REAL-ASM-COMMIT PASS'
printf '%s\n' \
  'CLAIM=REAL-ASM-PLANES1-3-EXECUTED-AND-SPOR64K-ASSEMBLED1-COMMITTED-AND-B2K-POSTERIOR-COMPATIBLE'
printf '%s\n' \
  'MATERIALIZER-EXECUTIONS=1 DRAGON-EXECUTIONS=1 ASM-EXECUTIONS=3 SPOR64K-EXECUTIONS=1 XDRTA2-CALLS=3'
printf '%s\n' \
  'RADIAL-OPERATOR-ASSEMBLIES=3 FLU-FLUX-SOLVES=0 PICARD-MAPS=0 QFISS=NOT-BUILT CONT=NOT-EXECUTED'
printf '%s\n' 'PLANES-EXECUTED=3 THREE-PLANE-COMMIT=EXECUTED'
printf '%s\n' "$FULL_COPY_LINE"
printf '%s\n' "$RESPONSE_LINE"
printf '%s\n' "$PLANE_NONZERO_LINE"
printf '%s\n' "$FORMULA_LINE"
printf '%s\n' "PROJECTED-SHA256=$PROJECTED_HASH BYTES=$PROJECTED_BYTES"
printf '%s\n' "ASSEMBLED-SHA256=$ASSEMBLED_HASH BYTES=$ASSEMBLED_BYTES"
printf '%s\n' \
  'COMMIT=MEMORY-LOGICAL-ASSEMBLED/1 PERSISTENCE=WHOLE-OBJECT-XSM-EVIDENCE-COPY'
printf '%s\n' \
  'EMPIRICAL-CONTROLS=0 AUTOMATIC-RETRIES-WITHIN-ACCEPTED-RUN=0 LONG-CALCULATIONS=0'
printf '%s\n' 'RESPONSE-NUMERICAL-ACCURACY=NOT-EVALUATED'
printf '%s\n' \
  'RADIAL-CONVERGENCE=NOT-EVALUATED OUTER-PICARD=NOT-EVALUATED'
if [ -f "$RECEIPT" ]; then
  printf '%s\n' 'RECEIPT=FROZEN PARENT=B2l'
else
  printf '%s\n' 'RECEIPT=PENDING-MAIN-AUDIT PARENT=B2l'
fi
