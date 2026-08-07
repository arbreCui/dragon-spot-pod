#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)
PARENT_RECEIPT="$ROOT/validation/iterative/real64_phase_a9b_b2k_system_assembly/phase_a9b_b2k_system_assembly_receipt.sha256"
RECEIPT="$HERE/phase_a9b_b2l_one_plane_real_asm_receipt.sha256"
EXPECTED_PARENT_COMMIT=3952353927161e36f243a7b38f7ba46cd6cd5192
EXPECTED_PARENT_HASH=fcff04068a61c7ff98785788a8202a1b4a87b8ad12d820a9922afd18de08c962
FC=/opt/homebrew/bin/gfortran
EXPECTED_FC_BANNER='GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0'
CPP=/usr/bin/cpp
AR=/usr/bin/ar
RUN_B2L=${RUN_B2L:-0}
PRESERVE_B2L_FAILURE=${PRESERVE_B2L_FAILURE:-0}

STATIC_CHECKER="$HERE/check_phase_a9b_b2l_one_plane_real_asm.py"
CONTRACT_TEST=test_phase_a9b_b2l_one_plane_real_asm_contract
BOUNDED="$HERE/run_bounded_b2l.py"
BOUNDED_TEST=test_run_bounded_b2l
PREPARER="$HERE/prepare_b2l_projected.f90"
POSTERIOR="$HERE/check_b2l_real_asm.f90"
DECK="$HERE/one_plane_real_asm.x2m"
B2J_SUPPORT="$ROOT/validation/iterative/real64_phase_a9b_b2j_archive_projection/b2j_fixture_support.f90"
XSM_HARNESS="$HERE/test_b2j_xsm_target.f90"

AX_ARTIFACT="$ROOT/validation/artifacts/iterative-map1/state1_axial.xsm"
ARCHIVE_ARTIFACT="$ROOT/validation/artifacts/iterative-map1/state1_snapshots.xsm"
AXIAL_TRACK_ARTIFACT="$ROOT/validation/artifacts/iterative-seed/initial_axial_track.xsm"
RADIAL_TRACK_ARTIFACT="$ROOT/validation/artifacts/iterative-seed/initial_radial_track.bin"
EXPECTED_AX_HASH=2323a256002f1e6f75f5af72c31479b0f6a7bff561d401cee363dcf9fc6ff484
EXPECTED_ARCHIVE_HASH=1b5a0c98aba0f5b4f366b64a8157f4a104df0f89f4cdeafc60eb6ce7811018e1
EXPECTED_AXIAL_TRACK_HASH=101ba0ad64c91723fdeb002e62c6226347fcfaeff188e125d699d70e113febc7
EXPECTED_RADIAL_TRACK_HASH=f7b27cb4a5d37f903b93e49610e2daa2290d55c164e2ca0e73ccb8d22fe486b8

BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-a9b-b2l.XXXXXX")
SOURCE_DIR="$BUILD_DIR/source"
OBJECT_DIR="$BUILD_DIR/objects"
HOST_DIR="$BUILD_DIR/host"
CASE_DIR="$BUILD_DIR/case"
XSM_CASE_DIR="$BUILD_DIR/xsm-target"

cleanup()
{
  status=$?
  trap - EXIT HUP INT TERM
  if [ "$status" -ne 0 ] && [ -d "$CASE_DIR" ]; then
    for log in prepare.log asm.log posterior_a.log posterior_b.log
    do
      if [ -f "$CASE_DIR/$log" ]; then
        printf '%s\n' "--- retained tail before cleanup: $log ---" >&2
        tail -n 160 "$CASE_DIR/$log" >&2
        printf '%s\n' "--- end retained tail: $log ---" >&2
      fi
    done
    if [ -f "$XSM_CASE_DIR/xsm_target.log" ]; then
      printf '%s\n' '--- retained tail before cleanup: xsm_target.log ---' >&2
      tail -n 160 "$XSM_CASE_DIR/xsm_target.log" >&2
      printf '%s\n' '--- end retained tail: xsm_target.log ---' >&2
    fi
  fi
  if [ "$status" -ne 0 ] && [ "$PRESERVE_B2L_FAILURE" = 1 ]; then
    printf '%s\n' "B2L FAILURE ARTIFACTS PRESERVED: $BUILD_DIR" >&2
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
  printf '%s\n' "SPOR64 PHASE-A9b-B2l FAILURE: $*" >&2
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
  [ -f "$PARENT_RECEIPT" ] || fail "B2k parent receipt missing"
  require_hash "$PARENT_RECEIPT" "$EXPECTED_PARENT_HASH"
  if [ -f "$RECEIPT" ]; then
    (
      cd "$ROOT"
      shasum -a 256 -c "$RECEIPT" >/dev/null
    ) || fail "B2l receipt verification failed"
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

case "$RUN_B2L" in
  0|1) ;;
  *) fail "RUN_B2L must be exactly 0 or 1" ;;
esac
case "$PRESERVE_B2L_FAILURE" in
  0|1) ;;
  *) fail "PRESERVE_B2L_FAILURE must be exactly 0 or 1" ;;
esac

[ "$(uname -s)" = Darwin ] || fail "frozen platform is Darwin"
[ "$(uname -m)" = arm64 ] || fail "frozen architecture is arm64"
[ -x "$FC" ] || fail "frozen compiler missing"
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
  "$B2J_SUPPORT" "$XSM_HARNESS" \
  "$AX_ARTIFACT" "$ARCHIVE_ARTIFACT" \
  "$AXIAL_TRACK_ARTIFACT" "$RADIAL_TRACK_ARTIFACT"
do
  [ -f "$path" ] || fail "required input missing: $path"
done

require_hash "$AX_ARTIFACT" "$EXPECTED_AX_HASH"
require_hash "$ARCHIVE_ARTIFACT" "$EXPECTED_ARCHIVE_HASH"
require_hash "$AXIAL_TRACK_ARTIFACT" "$EXPECTED_AXIAL_TRACK_HASH"
require_hash "$RADIAL_TRACK_ARTIFACT" "$EXPECTED_RADIAL_TRACK_HASH"
git -C "$ROOT" cat-file -e "$EXPECTED_PARENT_COMMIT^{commit}" || \
  fail "B2k parent commit missing"
git -C "$ROOT" merge-base --is-ancestor "$EXPECTED_PARENT_COMMIT" HEAD || \
  fail "B2k parent commit is not an ancestor"
verify_receipts

PYTHONDONTWRITEBYTECODE=1 python3 "$STATIC_CHECKER"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$HERE" python3 -m unittest -v \
  "$CONTRACT_TEST" "$BOUNDED_TEST"

mkdir -p "$SOURCE_DIR" "$OBJECT_DIR" "$HOST_DIR" "$CASE_DIR" \
  "$XSM_CASE_DIR"
for source in SPOR64_B2C SPOR64_B2I SPOR64_B2H SPOR64_B2J SPOR64_B2K
do
  copy_exact "$ROOT/src/$source.f90" "$SOURCE_DIR/$source.f90"
done
for source in ASM.f ASMDRV.f XDRTA2.f KDRDRV.F DOORAV.f MCCGA.f MCGASM.f
do
  copy_exact "$ROOT/src/$source" "$SOURCE_DIR/$source"
done
copy_exact "$PREPARER" "$SOURCE_DIR/prepare_b2l_projected.f90"
copy_exact "$POSTERIOR" "$SOURCE_DIR/check_b2l_real_asm.f90"
copy_exact "$B2J_SUPPORT" "$SOURCE_DIR/b2j_fixture_support.f90"
copy_exact "$XSM_HARNESS" "$SOURCE_DIR/test_b2j_xsm_target.f90"
copy_exact "$DECK" "$CASE_DIR/one_plane_real_asm.x2m"

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
  -c "$SOURCE_DIR/check_b2l_real_asm.f90" \
  -o "$OBJECT_DIR/check_b2l_real_asm.o"
"$FC" $FLAGS -I "$GANMOD" -I "$OBJECT_DIR" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/b2j_fixture_support.f90" \
  -o "$OBJECT_DIR/b2j_fixture_support.o"
"$FC" $FLAGS -I "$GANMOD" -I "$OBJECT_DIR" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/test_b2j_xsm_target.f90" \
  -o "$OBJECT_DIR/test_b2j_xsm_target.o"

"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$OBJECT_DIR/SPOR64_B2C.o" "$OBJECT_DIR/SPOR64_B2I.o" \
  "$OBJECT_DIR/SPOR64_B2H.o" "$OBJECT_DIR/SPOR64_B2J.o" \
  "$OBJECT_DIR/prepare_b2l_projected.o" "$GANLIB" "$UTILIB" \
  -o "$BUILD_DIR/prepare_b2l_projected"
"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$OBJECT_DIR/check_b2l_real_asm.o" "$GANLIB" "$UTILIB" \
  -o "$BUILD_DIR/check_b2l_real_asm"
"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$OBJECT_DIR/test_b2j_xsm_target.o" \
  "$OBJECT_DIR/b2j_fixture_support.o" \
  "$OBJECT_DIR/SPOR64_B2C.o" "$OBJECT_DIR/SPOR64_B2I.o" \
  "$OBJECT_DIR/SPOR64_B2H.o" "$OBJECT_DIR/SPOR64_B2J.o" \
  "$GANLIB" "$UTILIB" -o "$BUILD_DIR/test_b2j_xsm_target"

nm -g "$BUILD_DIR/check_b2l_real_asm" >"$BUILD_DIR/posterior.nm"
if grep -Eiq \
  '(^|[[:space:]])_?(asm|asmdrv|doorav|doorpv|mccga|mcgasm|flu|fludrv)_$|spor64' \
  "$BUILD_DIR/posterior.nm"
then
  grep -Ei \
    '(^|[[:space:]])_?(asm|asmdrv|doorav|doorpv|mccga|mcgasm|flu|fludrv)_$|spor64' \
    "$BUILD_DIR/posterior.nm" >&2
  fail "independent posterior links a production solver or lifecycle gate"
fi
grep -i 'lcmop' "$BUILD_DIR/posterior.nm" >/dev/null || \
  fail "independent posterior lacks GANLIB read path"

nm -g "$BUILD_DIR/test_b2j_xsm_target" >"$BUILD_DIR/xsm-harness.nm"
for symbol in \
  ___spor64_b2c_MOD_spor64_b2c_publish \
  ___spor64_b2i_MOD_spor64_b2i_seal_bootstrap \
  ___spor64_b2h_MOD_spor64_b2h_project \
  ___spor64_b2j_MOD_spor64_b2j_project_archive
do
  count_exact 1 " T ${symbol}$" "$BUILD_DIR/xsm-harness.nm"
done
if grep -Eiq \
  '(^|[[:space:]])_?(dragon|asm|asmdrv|xdrta2|kdrdrv|doorav|doorfv|doorpv|mccga|mccgf|mcgasm|mcgmre|flu|fludrv|flu2dr|flugpi|xdrkin|xdrexp|spomoc|spor64k)_$|spor64_b2k_mod_' \
  "$BUILD_DIR/xsm-harness.nm"
then
  fail "XSM lifecycle harness links a solver, Dragon, or B2K"
fi

ln -s "$AX_ARTIFACT" "$XSM_CASE_DIR/ax.xsm"
ln -s "$ARCHIVE_ARTIFACT" "$XSM_CASE_DIR/archive.xsm"
ln -s "$AXIAL_TRACK_ARTIFACT" "$XSM_CASE_DIR/axial_track.xsm"
if ! python3 "$BOUNDED" prepare "$BUILD_DIR/test_b2j_xsm_target" - \
  "$XSM_CASE_DIR/xsm_target.log" ax.xsm archive.xsm axial_track.xsm
then
  show_failure_log "$XSM_CASE_DIR/xsm_target.log"
  fail "bounded no-Dragon B2J XSM lifecycle harness failed"
fi
count_exact 1 '^B2L B2J-XSM-TARGET PASS$' "$XSM_CASE_DIR/xsm_target.log"
count_exact 1 '^B2L B2J-XSM-CALLS=6 COMMITS=1 REJECTIONS=5$' \
  "$XSM_CASE_DIR/xsm_target.log"
count_exact 1 \
  '^B2L B2J-XSM-REOPEN-CHECKS=6 PROJECTED=1 SENTINEL-ONLY=1 TOMBSTONED=1 FRESH-EMPTY=3$' \
  "$XSM_CASE_DIR/xsm_target.log"
count_exact 1 \
  '^B2L B2J-XSM-ROOT-ENTRIES=7 AUTHORITY-ENTRIES=4 SYSTEM-ABSENT=1$' \
  "$XSM_CASE_DIR/xsm_target.log"
count_exact 1 \
  '^B2L B2J-XSM-LATE-B2H-REJECTIONS=2 EARLY-REJECTIONS=3$' \
  "$XSM_CASE_DIR/xsm_target.log"
count_exact 1 \
  '^B2L B2J-XSM-DRAGON=0 ASM=0 FLU=0 CONT=0 SPOR64K=0 EMPIRICAL-CONTROLS=0$' \
  "$XSM_CASE_DIR/xsm_target.log"
XSM_LOG_LINES=$(wc -l <"$XSM_CASE_DIR/xsm_target.log")
[ "$XSM_LOG_LINES" -eq 6 ] || fail "XSM lifecycle output inventory differs"
require_hash "$AX_ARTIFACT" "$EXPECTED_AX_HASH"
require_hash "$ARCHIVE_ARTIFACT" "$EXPECTED_ARCHIVE_HASH"
require_hash "$AXIAL_TRACK_ARTIFACT" "$EXPECTED_AXIAL_TRACK_HASH"

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
cp "$ROOT/lib/Darwin_arm64/libDragon.a" "$HOST_DIR/libDragon.b2l.a"
"$AR" rcs "$HOST_DIR/libDragon.b2l.a" "$HOST_DIR/ASM.o" \
  "$HOST_DIR/KDRDRV.o" "$HOST_DIR/SPOR64_B2K.o"
"$AR" t "$HOST_DIR/libDragon.b2l.a" >"$HOST_DIR/archive-members.txt"
"$FC" -O2 -march=native -ffp-contract=off \
  "$ROOT/src/DRAGON.o" "$HOST_DIR/libDragon.b2l.a" \
  "$ROOT/Trivac/lib/Darwin_arm64/libTrivac.a" "$UTILIB" "$GANLIB" \
  -o "$BUILD_DIR/Dragon.b2l"

nm -g "$BUILD_DIR/Dragon.b2l" >"$BUILD_DIR/Dragon.nm"
for symbol in _asm_ _asmdrv_ _doorav_ _mccga_ _mcgasm_ _spor64k_ _xdrta2_
do
  count_exact 1 " T ${symbol}$" "$BUILD_DIR/Dragon.nm"
done
for member in ASM.o KDRDRV.o SPOR64_B2K.o
do
  count_exact 1 "^${member}$" "$HOST_DIR/archive-members.txt"
done

if [ "$RUN_B2L" = 0 ]; then
  printf '%s\n' 'SPOR64 PHASE-A9b-B2l PREFLIGHT PASS'
  printf '%s\n' 'ACTIVATION=DEFAULT-OFF; SET RUN_B2L=1 FOR ONE BOUNDED ASM'
  printf '%s\n' 'DRAGON-EXECUTIONS=0 ASM-EXECUTIONS=0 FLU=0 CONT=0'
  printf '%s\n' 'REAL-ASM-EXECUTION=NOT-EVALUATED'
  exit 0
fi
[ "$RUN_B2L" = 1 ] || fail "runtime activation is not exactly one"

ln -s "$AX_ARTIFACT" "$CASE_DIR/ax.xsm"
ln -s "$ARCHIVE_ARTIFACT" "$CASE_DIR/archive.xsm"
ln -s "$AXIAL_TRACK_ARTIFACT" "$CASE_DIR/axial_track.xsm"
ln -s "$RADIAL_TRACK_ARTIFACT" "$CASE_DIR/initial_radial_track.bin"
[ ! -e "$CASE_DIR/projected.xsm" ] || fail "PROJECTED output path exists"
[ ! -e "$CASE_DIR/system1.xsm" ] || fail "SYSTEM output path exists"

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
[ -s "$CASE_DIR/projected.xsm" ] || fail "PROJECTED materialization missing"
[ ! -L "$CASE_DIR/projected.xsm" ] || fail "PROJECTED output is a symlink"
[ "$(stat -f '%z' "$CASE_DIR/projected.xsm")" -le 536870912 ] || \
  fail "PROJECTED output cap exceeded"
PROJECTED_HASH=$(hash_of "$CASE_DIR/projected.xsm")

if ! python3 "$BOUNDED" asm "$BUILD_DIR/Dragon.b2l" \
  "$CASE_DIR/one_plane_real_asm.x2m" "$CASE_DIR/asm.log"
then
  show_failure_log "$CASE_DIR/asm.log"
  fail "bounded one-plane ASM failed; INVALID-NO-SCIENTIFIC-RESULT"
fi
require_normal_end "$CASE_DIR/asm.log"
count_exact 1 '^->@BEGIN MODULE : ASM:[[:space:]]*$' "$CASE_DIR/asm.log"
count_exact 1 '^->@END MODULE   : ASM:[[:space:]]*$' "$CASE_DIR/asm.log"
count_exact 1 '^-->>MODULE ASM:[[:space:]]*: TIME SPENT=' "$CASE_DIR/asm.log"
count_exact 1 \
  '^>\|B2L-ONE-PLANE-REAL-ASM-BEGIN[[:space:]]*\|>[0-9][0-9][0-9][0-9]$' \
  "$CASE_DIR/asm.log"
count_exact 1 \
  '^>\|B2L-ONE-PLANE-REAL-ASM-COMPLETE[[:space:]]*\|>[0-9][0-9][0-9][0-9]$' \
  "$CASE_DIR/asm.log"
if grep -E -- \
  '->@BEGIN MODULE : (FLU|SPOR64K|SPOFSRC|SPOFCHK|CONT):' \
  "$CASE_DIR/asm.log" >/dev/null
then
  fail "forbidden runtime module reached; INVALID-NO-SCIENTIFIC-RESULT"
fi
[ -s "$CASE_DIR/system1.xsm" ] || fail "real ASM SYSTEM output missing"
[ ! -L "$CASE_DIR/system1.xsm" ] || fail "real ASM output is a symlink"
[ "$(stat -f '%z' "$CASE_DIR/system1.xsm")" -le 67108864 ] || \
  fail "real ASM output cap exceeded"
[ "$(hash_of "$CASE_DIR/projected.xsm")" = "$PROJECTED_HASH" ] || \
  fail "PROJECTED input mutated during ASM"

(
  cd "$CASE_DIR"
  "$BUILD_DIR/check_b2l_real_asm" projected.xsm system1.xsm archive.xsm \
    >posterior_a.log 2>&1
  "$BUILD_DIR/check_b2l_real_asm" projected.xsm system1.xsm archive.xsm \
    >posterior_b.log 2>&1
)
cmp "$CASE_DIR/posterior_a.log" "$CASE_DIR/posterior_b.log" || \
  fail "read-only posterior output is not repeatable"
count_exact 1 '^B2L REAL ASM POSTERIOR PASS$' "$CASE_DIR/posterior_a.log"
count_exact 1 '^B2L GROUPS=370 EXACT-GROUP-RECORDS=5550$' \
  "$CASE_DIR/posterior_a.log"
count_exact 1 '^B2L RESPONSE-FINITE-VALUES=59940 RESPONSE-NONZERO-VALUES=[1-9][0-9]*$' \
  "$CASE_DIR/posterior_a.log"
count_exact 1 '^B2L TXSC-BITS=3330 S0PHYS-BITS=3330 S0USED-BITS=3330$' \
  "$CASE_DIR/posterior_a.log"
count_exact 1 '^B2L B2K-PLANE1-POSTERIOR=COMPATIBLE EMPIRICAL-CONTROLS=0$' \
  "$CASE_DIR/posterior_a.log"
count_exact 1 '^B2L RESPONSE-ACCURACY=NOT-EVALUATED CONVERGENCE=NOT-EVALUATED$' \
  "$CASE_DIR/posterior_a.log"

require_hash "$AX_ARTIFACT" "$EXPECTED_AX_HASH"
require_hash "$ARCHIVE_ARTIFACT" "$EXPECTED_ARCHIVE_HASH"
require_hash "$AXIAL_TRACK_ARTIFACT" "$EXPECTED_AXIAL_TRACK_HASH"
require_hash "$RADIAL_TRACK_ARTIFACT" "$EXPECTED_RADIAL_TRACK_HASH"
[ "$(hash_of "$CASE_DIR/projected.xsm")" = "$PROJECTED_HASH" ] || \
  fail "PROJECTED input mutated during posterior"
verify_receipts

SYSTEM_HASH=$(hash_of "$CASE_DIR/system1.xsm")
SYSTEM_BYTES=$(stat -f '%z' "$CASE_DIR/system1.xsm")
PROJECTED_BYTES=$(stat -f '%z' "$CASE_DIR/projected.xsm")
FULL_COPY_LINE=$(grep '^B2L FULL-COPY-RECORDS=' "$CASE_DIR/posterior_a.log")
RESPONSE_LINE=$(grep '^B2L RESPONSE-FINITE-VALUES=' "$CASE_DIR/posterior_a.log")

printf '%s\n' 'SPOR64 PHASE-A9b-B2l ONE-PLANE-REAL-ASM PASS'
printf '%s\n' 'CLAIM=REAL-ASM-PLANE1-EXECUTED-AND-B2K-POSTERIOR-COMPATIBLE'
printf '%s\n' 'DRAGON-EXECUTIONS=1 ASM-EXECUTIONS=1 XDRTA2-CALLS=1'
printf '%s\n' 'RADIAL-OPERATOR-ASSEMBLIES=1 FLU-FLUX-SOLVES=0 PICARD-MAPS=0'
printf '%s\n' 'PLANES-EXECUTED=1 QFISS=NOT-BUILT CONT=NOT-EXECUTED SPOR64K=NOT-EXECUTED'
printf '%s\n' "$FULL_COPY_LINE"
printf '%s\n' "$RESPONSE_LINE"
printf '%s\n' 'TXSC-BITS=3330 S0PHYS-BITS=3330 S0USED-BITS=3330'
printf '%s\n' "PROJECTED-SHA256=$PROJECTED_HASH BYTES=$PROJECTED_BYTES"
printf '%s\n' "SYSTEM1-SHA256=$SYSTEM_HASH BYTES=$SYSTEM_BYTES"
printf '%s\n' 'EMPIRICAL-CONTROLS=0 RETRIES=0 LONG-CALCULATIONS=0'
printf '%s\n' 'RESPONSE-NUMERICAL-ACCURACY=NOT-EVALUATED'
printf '%s\n' 'PLANES2-3=NOT-EVALUATED THREE-PLANE-COMMIT=NOT-EVALUATED'
printf '%s\n' 'RADIAL-CONVERGENCE=NOT-EVALUATED OUTER-PICARD=NOT-EVALUATED'
if [ -f "$RECEIPT" ]; then
  printf '%s\n' 'RECEIPT=FROZEN PARENT=B2k'
else
  printf '%s\n' 'RECEIPT=PENDING-MAIN-AUDIT PARENT=B2k'
fi
