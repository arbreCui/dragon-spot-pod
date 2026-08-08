#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)
B2L_DIR="$ROOT/validation/iterative/real64_phase_a9b_b2l_one_plane_real_asm"
B2K_DIR="$ROOT/validation/iterative/real64_phase_a9b_b2k_system_assembly"
B2M_DIR="$ROOT/validation/iterative/real64_phase_a9b_b2m_three_plane_real_asm_commit"
B2N_DIR="$ROOT/validation/iterative/real64_phase_a9b_b2n_real64_frozen_qfiss"
B2U_DIR="$ROOT/validation/iterative/real64_phase_a9b_b2u_same_call_asm_host"
B2M_RECEIPT="$B2M_DIR/phase_a9b_b2m_three_plane_real_asm_commit_receipt.sha256"
B2N_RECEIPT="$B2N_DIR/phase_a9b_b2n_real64_frozen_qfiss_receipt.sha256"
PARENT_RECEIPT="$B2U_DIR/phase_a9b_b2u_same_call_asm_host_receipt.sha256"
RECEIPT="$HERE/phase_a9b_b2v_one_real_continuation_receipt.sha256"

EXPECTED_PARENT_COMMIT=698d65b18be015c220db0cf8fc3db435b2127825
EXPECTED_PARENT_HASH=bed8b413c2c89fa15a87935686dc92e4d94890c28f6eed5045e034045f581c43
EXPECTED_B2M_HASH=8caa46c1af00e9dbe896123a6294dfa96b790e020c9592e0b76d13f093c09314
EXPECTED_B2N_HASH=06f9349e341a1bb3d07087e4f5236f8408b6fe67599a565d68c1b18ca7c51cc5
EXPECTED_BASE_DRAGON_HASH=257436c256aeed68e350cb958bda57d384cdc6845e1934842a1703dcbc5d86ec
EXPECTED_DRAGON_MAIN_HASH=1ef2ec69741bd0841c1250811b68170d46b96581d27d0c21cb00600c83ae32bb
EXPECTED_GANLIB_HASH=204d9f3aeaf4e06d8fbb62225e14859a767476cd845ba0096f166b5f9e14822c
EXPECTED_GANLIB_MOD_HASH=9ad2be2ae13310aa8273409d5cb3e70dfaa2201ada7bfc29a135bd566c4651d0
EXPECTED_UTILIB_HASH=a6c5cca8825691fd1da7554acabe542ba9986aabdbc935ecc46d1993240244ca
EXPECTED_TRIVAC_HASH=0b4dc12a834503223adb708751724cd1050b13b97cb8938dcf2ad7dafbde8002
EXPECTED_A9_OBJECT_HASH=c816a4e0415619221ac36357d356d770e0926e60b5dde10cdef0cd9837567c63
EXPECTED_SPOMOC_OBJECT_HASH=09f7d50a960ff11fb89fe116c50e8f37a9f351196b6e757208fe89449b62ca1a
EXPECTED_A9_MODULE_HASH=485c66a6f083d9c1a1cac39800acb110a1d4e82f559b3465e833150cd7ceaed8
EXPECTED_SPOMOC_MODULE_HASH=7e3754b1ae85c7d18ea123a387c4ecf80ce1439281ccebf315b215faa6609948
EXPECTED_SPOT_STEP_HASH=49a7cd59653cdb29f32a76b280ef32b81546ae9e4a757079c24ca10cc28e2634
EXPECTED_C2M_HELPER_HASH=5868da80b3646a0ce4b40594ad886103c5aa0e602b7b684c5110188ac9315fa2

FC=/opt/homebrew/bin/gfortran
EXPECTED_FC_BANNER='GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0'
CC=/usr/bin/cc
CPP=/usr/bin/cpp
AR=/usr/bin/ar
RUN_B2V=${RUN_B2V:-0}
PRESERVE_B2V_FAILURE=${PRESERVE_B2V_FAILURE:-0}

STATIC_CHECKER="$HERE/check_phase_a9b_b2v_one_real_continuation.py"
MUTATION_TEST=test_phase_a9b_b2v_one_real_continuation
BOUNDED="$HERE/run_bounded_b2v.py"
PREPARER="$B2L_DIR/prepare_b2l_projected.f90"
POSTERIOR="$HERE/check_b2v_real_returned.f90"
OBSERVER="$HERE/b2v_spor64t_observer.f90"
DECK="$HERE/one_real_continuation.x2m"
C2M_SOURCE="$ROOT/data/SpotStepR64.c2m"
C2M_HELPER="$B2K_DIR/compile_c2m.c"

AX_ARTIFACT="$ROOT/validation/artifacts/iterative-map1/state1_axial.xsm"
ARCHIVE_ARTIFACT="$ROOT/validation/artifacts/iterative-map1/state1_snapshots.xsm"
AXIAL_TRACK_ARTIFACT="$ROOT/validation/artifacts/iterative-seed/initial_axial_track.xsm"
RADIAL_TRACK_ARTIFACT="$ROOT/validation/artifacts/iterative-seed/initial_radial_track.bin"
EXPECTED_AX_HASH=2323a256002f1e6f75f5af72c31479b0f6a7bff561d401cee363dcf9fc6ff484
EXPECTED_ARCHIVE_HASH=1b5a0c98aba0f5b4f366b64a8157f4a104df0f89f4cdeafc60eb6ce7811018e1
EXPECTED_AXIAL_TRACK_HASH=101ba0ad64c91723fdeb002e62c6226347fcfaeff188e125d699d70e113febc7
EXPECTED_RADIAL_TRACK_HASH=f7b27cb4a5d37f903b93e49610e2daa2290d55c164e2ca0e73ccb8d22fe486b8
EXPECTED_RADIAL_TRACK_BYTES=2275636
EXPECTED_PROJECTED_HASH=c010c0a860884a4e4d3842dffe45ffb4898f2aaca99557e0411ee8c66d60b90c
EXPECTED_PROJECTED_BYTES=225315452

BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-a9b-b2v.XXXXXX")
SOURCE_DIR="$BUILD_DIR/source"
OBJECT_DIR="$BUILD_DIR/objects"
HOST_DIR="$BUILD_DIR/host"
CASE_DIR="$BUILD_DIR/case"

cleanup()
{
  status=$?
  trap - EXIT HUP INT TERM
  if [ "$status" -ne 0 ] && [ -d "$CASE_DIR" ]; then
    for log in prepare.log dragon.log posterior_a.log posterior_b.log
    do
      if [ -f "$CASE_DIR/$log" ]; then
        printf '%s\n' "--- retained tail before cleanup: $log ---" >&2
        tail -n 200 "$CASE_DIR/$log" >&2
        printf '%s\n' "--- end retained tail: $log ---" >&2
      fi
    done
  fi
  if [ "$status" -ne 0 ] && [ "$PRESERVE_B2V_FAILURE" = 1 ]; then
    printf '%s\n' "B2V FAILURE ARTIFACTS PRESERVED: $BUILD_DIR" >&2
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
  printf '%s\n' "SPOR64 PHASE-A9b-B2v FAILURE: $*" >&2
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

runtime_count_exact()
{
  expected=$1
  pattern=$2
  file=$3
  found=$(grep -c -E "$pattern" "$file" || true)
  [ "$found" -eq "$expected" ] || \
    fail "$file: runtime census expected $expected matches for $pattern, found $found; INVALID-RUNTIME-EVIDENCE"
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

copy_exact()
{
  source_path=$1
  target_path=$2
  cp "$source_path" "$target_path"
  cmp "$source_path" "$target_path" || fail "copy differs: $target_path"
}

show_failure_log()
{
  log=$1
  if [ -f "$log" ]; then
    printf '%s\n' "--- bounded child log: $log ---" >&2
    tail -n 200 "$log" >&2
    printf '%s\n' '--- end bounded child log ---' >&2
  fi
}

verify_receipts()
{
  [ -f "$PARENT_RECEIPT" ] || fail "B2u parent receipt missing"
  require_hash "$PARENT_RECEIPT" "$EXPECTED_PARENT_HASH"
  [ -f "$B2M_RECEIPT" ] || fail "B2m receipt missing"
  require_hash "$B2M_RECEIPT" "$EXPECTED_B2M_HASH"
  [ -f "$B2N_RECEIPT" ] || fail "B2n receipt missing"
  require_hash "$B2N_RECEIPT" "$EXPECTED_B2N_HASH"
  git -C "$ROOT" cat-file -e "$EXPECTED_PARENT_COMMIT^{commit}" || \
    fail "B2u parent commit missing"
  git -C "$ROOT" merge-base --is-ancestor "$EXPECTED_PARENT_COMMIT" HEAD || \
    fail "B2u parent commit is not an ancestor"
  if [ -f "$RECEIPT" ]; then
    (
      cd "$ROOT"
      shasum -a 256 -c "$RECEIPT" >/dev/null
    ) || fail "B2v receipt verification failed"
  fi
}

verify_link_inputs()
{
  require_hash "$ROOT/lib/Darwin_arm64/libDragon.a" "$EXPECTED_BASE_DRAGON_HASH"
  require_hash "$ROOT/src/DRAGON.o" "$EXPECTED_DRAGON_MAIN_HASH"
  require_hash "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" "$EXPECTED_GANLIB_HASH"
  require_hash "$ROOT/Ganlib/lib/Darwin_arm64/modules/ganlib.mod" "$EXPECTED_GANLIB_MOD_HASH"
  require_hash "$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a" "$EXPECTED_UTILIB_HASH"
  require_hash "$ROOT/Trivac/lib/Darwin_arm64/libTrivac.a" "$EXPECTED_TRIVAC_HASH"
  require_hash "$ROOT/lib/Darwin_arm64/modules/spor64_a9.mod" "$EXPECTED_A9_MODULE_HASH"
  require_hash "$ROOT/lib/Darwin_arm64/modules/spomoc_audit.mod" "$EXPECTED_SPOMOC_MODULE_HASH"
  require_hash "$C2M_HELPER" "$EXPECTED_C2M_HELPER_HASH"
  found=$("$AR" -p "$ROOT/lib/Darwin_arm64/libDragon.a" SPOR64_A9.o | \
    shasum -a 256 | awk '{print $1}')
  [ "$found" = "$EXPECTED_A9_OBJECT_HASH" ] || \
    fail "frozen base SPOR64_A9 object differs"
  found=$("$AR" -p "$ROOT/lib/Darwin_arm64/libDragon.a" SPOMOC.o | \
    shasum -a 256 | awk '{print $1}')
  [ "$found" = "$EXPECTED_SPOMOC_OBJECT_HASH" ] || \
    fail "frozen base SPOMOC object differs"
}

require_normal_end()
{
  log=$1
  runtime_count_exact 1 \
    '^ normal end of execution for dragon 5  Version 5\.1\.0[[:space:]]*$' \
    "$log"
  runtime_count_exact 1 'normal end of execution for dragon' "$log"
  if grep -Ei \
    'XABORT|segmentation fault|floating invalid|NaN|Infinity|SIGKILL|SIGTERM' \
    "$log" >/dev/null
  then
    fail "abnormal Dragon text; FAILED-NO-RETURN"
  fi
}

case "$RUN_B2V" in
  0|1) ;;
  *) fail "RUN_B2V must be exactly 0 or 1" ;;
esac
case "$PRESERVE_B2V_FAILURE" in
  0|1) ;;
  *) fail "PRESERVE_B2V_FAILURE must be exactly 0 or 1" ;;
esac

[ "$(uname -s)" = Darwin ] || fail "frozen platform is Darwin"
[ "$(uname -m)" = arm64 ] || fail "frozen architecture is arm64"
[ -x "$FC" ] || fail "frozen Fortran compiler missing"
[ -x "$CC" ] || fail "host C compiler missing"
[ -x "$CPP" ] || fail "host preprocessor missing"
[ -x "$AR" ] || fail "host archive tool missing"
[ "$($FC --version | sed -n '1p')" = "$EXPECTED_FC_BANNER" ] || \
  fail "unaudited compiler"

for path in "$STATIC_CHECKER" "$HERE/$MUTATION_TEST.py" "$BOUNDED" "$PREPARER" "$POSTERIOR" \
  "$OBSERVER" "$DECK" "$C2M_SOURCE" "$C2M_HELPER" \
  "$AX_ARTIFACT" "$ARCHIVE_ARTIFACT" "$AXIAL_TRACK_ARTIFACT" \
  "$RADIAL_TRACK_ARTIFACT" "$ROOT/lib/Darwin_arm64/libDragon.a"
do
  [ -f "$path" ] || fail "required input missing: $path"
done
for source in SPOR64_B2C SPOR64_B2B SPOR64_B2O SPOR64_B2R SPOR64_B2S \
  SPOR64_B2K SPOR64_B2N SPOR64_B2T SPOR64_B2U
do
  [ -f "$ROOT/src/$source.f90" ] || fail "production $source missing"
done
for source in ASM.f KDRDRV.F
do
  [ -f "$ROOT/src/$source" ] || fail "production $source missing"
done

verify_receipts
verify_link_inputs
require_hash "$C2M_SOURCE" "$EXPECTED_SPOT_STEP_HASH"
require_hash "$AX_ARTIFACT" "$EXPECTED_AX_HASH"
require_hash "$ARCHIVE_ARTIFACT" "$EXPECTED_ARCHIVE_HASH"
require_hash "$AXIAL_TRACK_ARTIFACT" "$EXPECTED_AXIAL_TRACK_HASH"
require_hash "$RADIAL_TRACK_ARTIFACT" "$EXPECTED_RADIAL_TRACK_HASH"
[ "$(stat -f '%z' "$RADIAL_TRACK_ARTIFACT")" -eq \
  "$EXPECTED_RADIAL_TRACK_BYTES" ] || fail "radial TRACK byte count differs"

PYTHONDONTWRITEBYTECODE=1 python3 "$STATIC_CHECKER"
if ! (
  cd "$HERE"
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$HERE" \
    python3 -m unittest -v "$MUTATION_TEST" \
    >"$BUILD_DIR/mutations.log" 2>&1
); then
  sed -n '1,300p' "$BUILD_DIR/mutations.log" >&2
  fail "B2v mutation suite rejected"
fi
count_exact 1 '^Ran 34 tests in [0-9.]+s$' "$BUILD_DIR/mutations.log"
count_exact 1 '^OK$' "$BUILD_DIR/mutations.log"

mkdir -p "$SOURCE_DIR" "$OBJECT_DIR" "$HOST_DIR" "$CASE_DIR"
for source in SPOR64_B2C SPOR64_B2B SPOR64_B2O SPOR64_B2R SPOR64_B2S \
  SPOR64_B2K SPOR64_B2N SPOR64_B2T SPOR64_B2U
do
  copy_exact "$ROOT/src/$source.f90" "$SOURCE_DIR/$source.f90"
done
copy_exact "$ROOT/src/ASM.f" "$SOURCE_DIR/ASM.f"
copy_exact "$ROOT/src/KDRDRV.F" "$SOURCE_DIR/KDRDRV.F"
copy_exact "$PREPARER" "$SOURCE_DIR/prepare_b2l_projected.f90"
copy_exact "$POSTERIOR" "$SOURCE_DIR/check_b2v_real_returned.f90"
copy_exact "$OBSERVER" "$SOURCE_DIR/b2v_spor64t_observer.f90"
copy_exact "$C2M_HELPER" "$SOURCE_DIR/compile_c2m.c"
copy_exact "$DECK" "$CASE_DIR/one_real_continuation.x2m"

STRICT_FLAGS='-O0 -g -std=f2008 -pedantic -Wall -Wextra -Werror'
STRICT_FLAGS="$STRICT_FLAGS -fimplicit-none -fcheck=all -fbacktrace"
STRICT_FLAGS="$STRICT_FLAGS -ffp-contract=off -fno-fast-math"
GANMOD="$ROOT/Ganlib/lib/Darwin_arm64/modules"
DRAMOD="$ROOT/lib/Darwin_arm64/modules"
GANLIB="$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a"
UTILIB="$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a"

# Compile the deterministic PROJECTED materializer and the independent
# GANLIB-only posterior before any possible runtime activation.
for source in SPOR64_B2C SPOR64_B2I SPOR64_B2H SPOR64_B2J
do
  if [ "$source" != SPOR64_B2C ]; then
    copy_exact "$ROOT/src/$source.f90" "$SOURCE_DIR/$source.f90"
  fi
  "$FC" $STRICT_FLAGS -I "$GANMOD" -I "$OBJECT_DIR" -J "$OBJECT_DIR" \
    -c "$SOURCE_DIR/$source.f90" -o "$OBJECT_DIR/$source.prepare.o"
done
"$FC" $STRICT_FLAGS -I "$GANMOD" -I "$OBJECT_DIR" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/prepare_b2l_projected.f90" \
  -o "$OBJECT_DIR/prepare_b2l_projected.o"
"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$OBJECT_DIR/SPOR64_B2C.prepare.o" "$OBJECT_DIR/SPOR64_B2I.prepare.o" \
  "$OBJECT_DIR/SPOR64_B2H.prepare.o" "$OBJECT_DIR/SPOR64_B2J.prepare.o" \
  "$OBJECT_DIR/prepare_b2l_projected.o" "$GANLIB" "$UTILIB" \
  -o "$BUILD_DIR/prepare_b2l_projected"

"$FC" $STRICT_FLAGS -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/check_b2v_real_returned.f90" \
  -o "$OBJECT_DIR/check_b2v_real_returned.o"
"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$OBJECT_DIR/check_b2v_real_returned.o" "$GANLIB" "$UTILIB" \
  -o "$BUILD_DIR/check_b2v_real_returned"
nm -g "$BUILD_DIR/check_b2v_real_returned" >"$BUILD_DIR/posterior.nm"
if grep -Eiq \
  '(^|[[:space:]])_?(dragon|asm|asmdrv|xdrta2|kdrdrv|doorav|doorfv|doorpv|mccga|mccgf|mcgasm|flu|fludrv|flu2dr|spomoc|spoasm|spostate|spoleak|spor64)_$|___spor64_' \
  "$BUILD_DIR/posterior.nm"
then
  fail "independent posterior links production lifecycle or solver code"
fi
grep -i 'lcmop' "$BUILD_DIR/posterior.nm" >/dev/null || \
  fail "independent posterior lacks GANLIB read path"

# Compile the procedure and wrapper deck with the real CLEPIL/OBJPIL path.
"$CC" -std=c11 -pedantic -Wall -Wextra -Werror \
  -I "$ROOT/Ganlib/src" -c "$SOURCE_DIR/compile_c2m.c" \
  -o "$OBJECT_DIR/compile_c2m.o"
"$FC" "$OBJECT_DIR/compile_c2m.o" "$GANLIB" -o "$BUILD_DIR/compile_c2m"
if ! (
  cd "$BUILD_DIR"
  ./compile_c2m "$C2M_SOURCE" SpotStepR64.o2m >procedure_compile.log 2>&1
); then
  sed -n '1,240p' "$BUILD_DIR/procedure_compile.log" >&2
  fail "CLEPIL/OBJPIL compilation of SpotStepR64 failed"
fi
if ! (
  cd "$BUILD_DIR"
  ./compile_c2m "$DECK" one_real_continuation.o2m >deck_compile.log 2>&1
); then
  sed -n '1,240p' "$BUILD_DIR/deck_compile.log" >&2
  fail "CLEPIL/OBJPIL compilation of B2v deck failed"
fi
for object in SpotStepR64.o2m one_real_continuation.o2m
do
  [ -s "$BUILD_DIR/$object" ] || fail "empty C2M object: $object"
done
C2M_OBJECT_HASH=$(hash_of "$BUILD_DIR/SpotStepR64.o2m")
copy_exact "$C2M_SOURCE" "$CASE_DIR/SpotStepR64.c2m"
copy_exact "$BUILD_DIR/SpotStepR64.o2m" "$CASE_DIR/SpotStepR64.o2m"
[ ! -e "$CASE_DIR/SpotStepR64.l2m" ] || fail "unexpected procedure listing"

# Build one private Dragon.  The frozen base archive supplies the previously
# qualified A8/A9/SPOMOC/transport members; all post-B2m lifecycle objects,
# ASM, the dispatcher, and the validation-only observer are overlaid here.
HOST_FLAGS='-fPIC -Wall -Wextra -Werror -frecord-marker=4 -ffpe-summary=none'
HOST_FLAGS="$HOST_FLAGS -O2 -march=native -ffp-contract=off"
for source in SPOR64_B2C SPOR64_B2B SPOR64_B2O SPOR64_B2R SPOR64_B2S \
  SPOR64_B2K SPOR64_B2N SPOR64_B2T
do
  "$FC" $HOST_FLAGS -I "$GANMOD" -I "$HOST_DIR" -I "$DRAMOD" \
    -J "$HOST_DIR" -c "$SOURCE_DIR/$source.f90" \
    -o "$HOST_DIR/$source.o"
done
"$FC" $HOST_FLAGS -I "$GANMOD" -I "$HOST_DIR" -I "$DRAMOD" \
  -J "$HOST_DIR" -c "$SOURCE_DIR/b2v_spor64t_observer.f90" \
  -o "$HOST_DIR/SPOR64_B2U.o"
"$FC" $HOST_FLAGS -I "$GANMOD" -c "$SOURCE_DIR/ASM.f" \
  -ffixed-line-length-72 -o "$HOST_DIR/ASM.o"
"$CPP" -P -W -traditional -DLinux -DUnix "$SOURCE_DIR/KDRDRV.F" \
  "$HOST_DIR/KDRDRV.pp.f"
"$FC" $HOST_FLAGS -I "$GANMOD" -c "$HOST_DIR/KDRDRV.pp.f" \
  -ffixed-line-length-72 -o "$HOST_DIR/KDRDRV.o"

cp "$ROOT/lib/Darwin_arm64/libDragon.a" "$HOST_DIR/libDragon.b2v.a"
"$AR" rcs "$HOST_DIR/libDragon.b2v.a" \
  "$HOST_DIR/ASM.o" "$HOST_DIR/KDRDRV.o" \
  "$HOST_DIR/SPOR64_B2C.o" "$HOST_DIR/SPOR64_B2B.o" \
  "$HOST_DIR/SPOR64_B2O.o" "$HOST_DIR/SPOR64_B2R.o" \
  "$HOST_DIR/SPOR64_B2S.o" "$HOST_DIR/SPOR64_B2K.o" \
  "$HOST_DIR/SPOR64_B2N.o" "$HOST_DIR/SPOR64_B2T.o" \
  "$HOST_DIR/SPOR64_B2U.o"
"$AR" t "$HOST_DIR/libDragon.b2v.a" >"$HOST_DIR/archive-members.txt"
for member in ASM.o KDRDRV.o SPOR64_B2C.o SPOR64_B2B.o SPOR64_B2O.o \
  SPOR64_B2R.o SPOR64_B2S.o SPOR64_B2K.o SPOR64_B2N.o SPOR64_B2T.o \
  SPOR64_B2U.o
do
  count_exact 1 "^${member}$" "$HOST_DIR/archive-members.txt"
done
"$FC" -O2 -march=native -ffp-contract=off \
  "$ROOT/src/DRAGON.o" "$HOST_DIR/libDragon.b2v.a" \
  "$ROOT/Trivac/lib/Darwin_arm64/libTrivac.a" "$UTILIB" "$GANLIB" \
  -o "$BUILD_DIR/Dragon.b2v"
nm -g "$BUILD_DIR/Dragon.b2v" >"$BUILD_DIR/Dragon.nm"
count_exact 1 ' T _spor64t_$' "$BUILD_DIR/Dragon.nm"
for symbol in _asm_ _xdrta2_ _doorav_ _mccga_ _mcgasm_
do
  count_exact 1 " T ${symbol}$" "$BUILD_DIR/Dragon.nm"
done
for symbol in spor64_b2t_host_step spor64_b2s_host_bridge \
  spor64_b2b_ingress spor64_b2r_collect
do
  count_exact 1 " T .*${symbol}$" "$BUILD_DIR/Dragon.nm"
done
for symbol in spor64_a9_MOD_flu2dr64_core spor64_a8_MOD_doorfv64 \
  spomoc_audit_MOD_spomoc_active
do
  count_exact 1 " T .*${symbol}$" "$BUILD_DIR/Dragon.nm"
done

if [ "$RUN_B2V" = 0 ]; then
  printf '%s\n' 'SPOR64 PHASE-A9b-B2v PREFLIGHT PASS'
  printf '%s\n' \
    'ACTIVATION=DEFAULT-OFF; SET RUN_B2V=1 FOR EXACTLY ONE BOUNDED REAL RETURN'
  printf '%s\n' \
    'DRAGON=0 ASM=0 RADIAL-CONT=0 PICARD=0 LONG-CALCULATIONS=0'
  printf '%s\n' \
    'OBSERVER=COMPILE-ONLY PRODUCTION-SPOR64T=NOT-LINKED POSTERIOR=GANLIB-ONLY'
  printf '%s\n' 'ONE-REAL-THREE-PLANE-CONTINUATION=NOT-EVALUATED'
  exit 0
fi
[ "$RUN_B2V" = 1 ] || fail "runtime activation is not exactly one"

ln -s "$AX_ARTIFACT" "$CASE_DIR/ax.xsm"
ln -s "$ARCHIVE_ARTIFACT" "$CASE_DIR/archive.xsm"
ln -s "$AXIAL_TRACK_ARTIFACT" "$CASE_DIR/axial_track.xsm"
copy_exact "$RADIAL_TRACK_ARTIFACT" "$CASE_DIR/initial_radial_track.bin"
chmod 444 "$CASE_DIR/initial_radial_track.bin"
[ ! -L "$CASE_DIR/initial_radial_track.bin" ] || \
  fail "private radial TRACK is a symlink"
[ ! -e "$CASE_DIR/projected.xsm" ] || fail "PROJECTED path already exists"
[ ! -e "$CASE_DIR/returned.xsm" ] || fail "RETURNED path already exists"

if ! python3 "$BOUNDED" prepare "$BUILD_DIR/prepare_b2l_projected" - \
  "$CASE_DIR/prepare.log" ax.xsm archive.xsm axial_track.xsm projected.xsm
then
  show_failure_log "$CASE_DIR/prepare.log"
  fail "bounded PROJECTED preparation failed; INVALID-NO-SCIENTIFIC-RESULT"
fi
count_exact 1 '^B2L FULL PROJECTED PREPARATION PASS$' "$CASE_DIR/prepare.log"
[ -s "$CASE_DIR/projected.xsm" ] || fail "PROJECTED materialization missing"
[ ! -L "$CASE_DIR/projected.xsm" ] || fail "PROJECTED is a symlink"
[ "$(stat -f '%z' "$CASE_DIR/projected.xsm")" -eq \
  "$EXPECTED_PROJECTED_BYTES" ] || fail "PROJECTED byte count differs"
require_hash "$CASE_DIR/projected.xsm" "$EXPECTED_PROJECTED_HASH"
chmod 444 "$CASE_DIR/projected.xsm"

PROJECTED_BEFORE=$(hash_of "$CASE_DIR/projected.xsm")
TRACK_BEFORE=$(hash_of "$CASE_DIR/initial_radial_track.bin")
DRAGON_HASH=$(hash_of "$BUILD_DIR/Dragon.b2v")
DECK_HASH=$(hash_of "$CASE_DIR/one_real_continuation.x2m")

# This is the sole Dragon activation of the private B2v binary.  There is no
# retry, fallback, enlarged cap, altered tolerance, or second execution.
if ! python3 "$BOUNDED" dragon "$BUILD_DIR/Dragon.b2v" \
  "$CASE_DIR/one_real_continuation.x2m" "$CASE_DIR/dragon.log"
then
  show_failure_log "$CASE_DIR/dragon.log"
  fail "single bounded Dragon activation failed; NO-RETRY"
fi

require_normal_end "$CASE_DIR/dragon.log"
if grep -E \
  'COMPILING _MAIN\.c2m FILE|BAD OBJECTS _MAIN\.c2m FILE' \
  "$CASE_DIR/dragon.log" >/dev/null
then
  fail "runtime C2M compilation error/branch detected; INVALID-RUNTIME-EVIDENCE"
fi
runtime_count_exact 3 '^->@BEGIN MODULE : ASM:[[:space:]]*$' "$CASE_DIR/dragon.log"
runtime_count_exact 3 '^->@END MODULE   : ASM:[[:space:]]*$' "$CASE_DIR/dragon.log"
runtime_count_exact 1 '^->@BEGIN MODULE : SPOR64T:[[:space:]]*$' "$CASE_DIR/dragon.log"
runtime_count_exact 1 '^->@END MODULE   : SPOR64T:[[:space:]]*$' "$CASE_DIR/dragon.log"
runtime_count_exact 1 \
  '^>\|B2V-REAL-CONTINUATION-BEGIN[[:space:]]*\|>[0-9][0-9][0-9][0-9]$' \
  "$CASE_DIR/dragon.log"
runtime_count_exact 1 \
  '^>\|B2V-REAL-CONTINUATION-COMPLETE[[:space:]]*\|>[0-9][0-9][0-9][0-9]$' \
  "$CASE_DIR/dragon.log"
runtime_count_exact 1 \
  '^B2V-OBSERVER STATUS=2 CUTOFF-P1=[0-9]+ CUTOFF-P2=[0-9]+ CUTOFF-P3=[0-9]+$' \
  "$CASE_DIR/dragon.log"
if grep -E -- \
  '->@BEGIN MODULE : (SPOR64K|FLU|SPOFSRC|SPOFCHK|CONT|SPOSTATE|SPOLEAK):' \
  "$CASE_DIR/dragon.log" >/dev/null
then
  fail "forbidden CLE module reached; FAILED-NO-RETURN"
fi
[ ! -e "$CASE_DIR/SpotStepR64.l2m" ] || \
  fail "runtime source-compilation branch detected; FAILED-NO-RETURN"
[ -s "$CASE_DIR/returned.xsm" ] || \
  fail "RETURNED XSM missing; INVALID-RETURNED-EVIDENCE"
[ ! -L "$CASE_DIR/returned.xsm" ] || \
  fail "RETURNED XSM is a symlink; INVALID-RETURNED-EVIDENCE"
[ "$(stat -f '%z' "$CASE_DIR/returned.xsm")" -le 536870912 ] || \
  fail "RETURNED XSM exceeds file cap; INVALID-RETURNED-EVIDENCE"
chmod 444 "$CASE_DIR/returned.xsm"

[ "$(hash_of "$CASE_DIR/projected.xsm")" = "$PROJECTED_BEFORE" ] || \
  fail "PROJECTED changed during Dragon; INVALID-RETURNED-EVIDENCE"
[ "$(hash_of "$CASE_DIR/initial_radial_track.bin")" = "$TRACK_BEFORE" ] || \
  fail "radial TRACK changed during Dragon; INVALID-RETURNED-EVIDENCE"
RETURNED_HASH=$(hash_of "$CASE_DIR/returned.xsm")
RETURNED_BYTES=$(stat -f '%z' "$CASE_DIR/returned.xsm")

if ! python3 "$BOUNDED" posterior "$BUILD_DIR/check_b2v_real_returned" - \
  "$CASE_DIR/posterior_a.log" projected.xsm returned.xsm
then
  show_failure_log "$CASE_DIR/posterior_a.log"
  fail "first independent posterior failed; INVALID-RETURNED-EVIDENCE"
fi
if ! python3 "$BOUNDED" posterior "$BUILD_DIR/check_b2v_real_returned" - \
  "$CASE_DIR/posterior_b.log" projected.xsm returned.xsm
then
  show_failure_log "$CASE_DIR/posterior_b.log"
  fail "second independent posterior failed; INVALID-RETURNED-EVIDENCE"
fi
cmp "$CASE_DIR/posterior_a.log" "$CASE_DIR/posterior_b.log" || \
  fail "posterior reports differ; INVALID-RETURNED-EVIDENCE"
count_exact 1 '^B2V REAL RETURNED POSTERIOR PASS$' "$CASE_DIR/posterior_a.log"
sed -n '1,40p' "$CASE_DIR/posterior_a.log"
[ "$(hash_of "$CASE_DIR/projected.xsm")" = "$PROJECTED_BEFORE" ] || \
  fail "PROJECTED changed during posterior; INVALID-RETURNED-EVIDENCE"
[ "$(hash_of "$CASE_DIR/initial_radial_track.bin")" = "$TRACK_BEFORE" ] || \
  fail "radial TRACK changed during posterior; INVALID-RETURNED-EVIDENCE"
[ "$(hash_of "$CASE_DIR/returned.xsm")" = "$RETURNED_HASH" ] || \
  fail "RETURNED changed during posterior; INVALID-RETURNED-EVIDENCE"

CUTOFF_LINE=$(grep '^B2V-OBSERVER STATUS=2 ' "$CASE_DIR/dragon.log")
CUTOFF_VALUES=$(printf '%s\n' "$CUTOFF_LINE" | sed -E \
  's/^B2V-OBSERVER STATUS=2 CUTOFF-P1=([0-9]+) CUTOFF-P2=([0-9]+) CUTOFF-P3=([0-9]+)$/\1 \2 \3/')
set -- $CUTOFF_VALUES
[ "$#" -eq 3 ] || \
  fail "cutoff census parse failed; INVALID-RETURNED-EVIDENCE"
CUTOFF_P1=$1
CUTOFF_P2=$2
CUTOFF_P3=$3
if [ "$CUTOFF_P1" = 0 ] && [ "$CUTOFF_P2" = 0 ] && \
   [ "$CUTOFF_P3" = 0 ]; then
  CUTOFF_CLASS=NO-REACHED-LOCAL-PREDICATE-DIFFERENCE-OBSERVED
else
  CUTOFF_CLASS=INHERITED-ACA-CUTOFF-LOCAL-PREDICATE-DIFFERENCE-OBSERVED
fi

require_hash "$AX_ARTIFACT" "$EXPECTED_AX_HASH"
require_hash "$ARCHIVE_ARTIFACT" "$EXPECTED_ARCHIVE_HASH"
require_hash "$AXIAL_TRACK_ARTIFACT" "$EXPECTED_AXIAL_TRACK_HASH"
require_hash "$RADIAL_TRACK_ARTIFACT" "$EXPECTED_RADIAL_TRACK_HASH"
require_hash "$CASE_DIR/SpotStepR64.c2m" "$EXPECTED_SPOT_STEP_HASH"
require_hash "$CASE_DIR/SpotStepR64.o2m" "$C2M_OBJECT_HASH"
verify_receipts
verify_link_inputs

printf '%s\n' 'SPOR64 PHASE-A9b-B2v ONE-REAL-CONTINUATION PASS'
printf '%s\n' \
  'CLASSIFICATION=ONE-REAL-THREE-PLANE-CONTINUATION-RETURNED'
printf '%s\n' \
  'CLAIM=THREE-REAL-ASM-AND-PRODUCTION-CONT-INTERNAL-ACCEPTANCE-AND-PUBLICATION-PATH-RETURNED-3-PLANES'
printf '%s\n' \
  'DRAGON-EXECUTIONS=1 ASM-EXECUTIONS=3 RADIAL-CONT-RETURNS=3 RETRIES=0'
printf '%s\n' \
  'VALIDATION-OBSERVER-SPOR64T-EXECUTIONS=1 PRODUCTION-SPOR64T-EXECUTIONS=0'
printf '%s\n' \
  'PRODUCTION-B2T/B2S/B2B/A9/B2R=EXECUTED POSTERIOR=GANLIB-ONLYx2'
printf '%s\n' \
  "CUTOFF-P1=$CUTOFF_P1 CUTOFF-P2=$CUTOFF_P2 CUTOFF-P3=$CUTOFF_P3"
printf '%s\n' "CUTOFF-CLASS=$CUTOFF_CLASS"
printf '%s\n' "PROJECTED-SHA256=$PROJECTED_BEFORE BYTES=$EXPECTED_PROJECTED_BYTES"
printf '%s\n' "TRACK-SHA256=$TRACK_BEFORE BYTES=$EXPECTED_RADIAL_TRACK_BYTES"
printf '%s\n' "RETURNED-SHA256=$RETURNED_HASH BYTES=$RETURNED_BYTES"
printf '%s\n' "DRAGON-SHA256=$DRAGON_HASH DECK-SHA256=$DECK_HASH"
printf '%s\n' \
  'EMPIRICAL-COEFFICIENTS-ADDED=0 RELAXATION=0 DAMPING=0 CLIPPING=0 MODEL-COMPLETION=0'
printf '%s\n' \
  'AXIAL-SOLVE=0 OUTER-PICARD-CONVERGENCE=NOT-EVALUATED CLOSED/1=NOT-PUBLISHED'
printf '%s\n' \
  'INDEPENDENT-A9-RESIDUAL/NORM-VALIDATION=NOT-EVALUATED INTERNAL-TERMINATION-PATH=PROVENANCE-ONLY'
printf '%s\n' \
  'REPRODUCIBILITY=NOT-EVALUATED TRACK-HISTORICAL-IDENTITY=NOT-CLAIMED'
if [ -f "$RECEIPT" ]; then
  printf '%s\n' 'RECEIPT=FROZEN PARENT=B2u'
else
  printf '%s\n' 'RECEIPT=PENDING-MAIN-AUDIT PARENT=B2u'
fi
