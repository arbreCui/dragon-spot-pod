#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)
B2Z_DIR="$ROOT/validation/iterative/real64_phase_a9b_b2z_one_real_returned_staging"
B2V_DIR="$ROOT/validation/iterative/real64_phase_a9b_b2v_one_real_continuation"
B2X_DIR="$ROOT/validation/iterative/real64_phase_a9b_b2x_same_call_returned_close"
B2Z_RECEIPT="$B2Z_DIR/phase_a9b_b2z_one_real_returned_staging_receipt.sha256"
B2Z_RUNTIME_RESULT="$B2Z_DIR/runtime_result.txt"
B2V_RECEIPT="$B2V_DIR/phase_a9b_b2v_one_real_continuation_receipt.sha256"
PARENT_RECEIPT="$B2X_DIR/phase_a9b_b2x_same_call_returned_close_receipt.sha256"
RECEIPT="$HERE/phase_a9b_b2y_invalid_attempt_freeze_receipt.sha256"

EXECUTION_SNAPSHOT_COMMIT=5713f2eba8d267cb7eaaa36155b2888e07f19a32
EXECUTED_WRAPPER_HASH=c8e7905aac3d4e24e41602b6809d5a8e066690f9b523416bf77df0eefa4ad7b1
EXECUTED_RUNNER_HASH=148ee567be1ec3bedf4af5bf930595fa7f15ca72802f2ab1a40d4f964092b24c
EXECUTED_DECK_HASH=2e6755f87767f0c0bc357713d410dad280d5d66bd7a87264fa4dbb427d3e6b10
EXECUTED_SPOTCLOSE_HASH=9e7ffc250fa3eccb89edca7d0ece2caeb647ea8c1822fdb2415298540e62914c
EXECUTED_FLU2DR_HASH=26bc6dcaa464cc25d7f6c56c449f3dab004bb237494a9b5120618501b8c48188

EXPECTED_B2V_COMMIT=607eccf472dfb95fa24b0775f950e4e50eda5efa
EXPECTED_B2V_RECEIPT_HASH=af2b47504adcefc7d1e9fd2ae2ecf4517298e7b5b1be1cd75633ca0fa5482bcb
EXPECTED_PARENT_COMMIT=18a2e69a11867d71bdb22a7964e48422cd9d75f8
EXPECTED_PARENT_HASH=fae78e682c72a68e2acf10edebf065a69471722e64c971c9f0c840b39ff20f2c
EXPECTED_B2Z_RECEIPT_HASH=2f003d175a2ff7eea2feb73cc87e46d83c1c11e1e09f97ebe228472f7d741844
EXPECTED_B2Z_RUNTIME_HASH=6627924e8bed19e23537ede946c3c7c2cc7dcf2f53b84055a4b8e047fe444850
EXPECTED_B2Z_RUNTIME_BYTES=1735
EXPECTED_B2Z_ARTIFACT_MANIFEST_HASH=22949de59c8662c43ca7f7ec3293e27287571ae85b58ecddf24fc2148a67ca0f
EXPECTED_B2Z_ARTIFACT_MANIFEST_BYTES=483
EXPECTED_RETURNED_HASH=dd41a37d484b85612a495ff7b1f2233a53fbae1b462d89bd84db2a8809cef054
EXPECTED_RETURNED_BYTES=231572260
EXPECTED_TRACK_AX_HASH=101ba0ad64c91723fdeb002e62c6226347fcfaeff188e125d699d70e113febc7
EXPECTED_TRACK_AX_BYTES=13248
EXPECTED_MACROLIB3_HASH=2e01e806683ce25b5771af055112dc86dcf147245abc5a5c3dceac4d9939373a
EXPECTED_MACROLIB3_BYTES=27957124
EXPECTED_BASIS_REF_HASH=dc65467731947901393f9fb7114b7cd2e956a9992bb97db18e665b47e7446504
EXPECTED_BASIS_REF_BYTES=800220
EXPECTED_BASE_DRAGON_HASH=257436c256aeed68e350cb958bda57d384cdc6845e1934842a1703dcbc5d86ec
EXPECTED_DRAGON_MAIN_HASH=1ef2ec69741bd0841c1250811b68170d46b96581d27d0c21cb00600c83ae32bb
EXPECTED_GANLIB_HASH=204d9f3aeaf4e06d8fbb62225e14859a767476cd845ba0096f166b5f9e14822c
EXPECTED_GANLIB_MOD_HASH=9ad2be2ae13310aa8273409d5cb3e70dfaa2201ada7bfc29a135bd566c4651d0
EXPECTED_UTILIB_HASH=a6c5cca8825691fd1da7554acabe542ba9986aabdbc935ecc46d1993240244ca
EXPECTED_TRIVAC_HASH=0b4dc12a834503223adb708751724cd1050b13b97cb8938dcf2ad7dafbde8002
EXPECTED_A9_MODULE_HASH=485c66a6f083d9c1a1cac39800acb110a1d4e82f559b3465e833150cd7ceaed8
EXPECTED_SPOMOC_MODULE_HASH=7e3754b1ae85c7d18ea123a387c4ecf80ce1439281ccebf315b215faa6609948
EXPECTED_C2M_HELPER_HASH=5868da80b3646a0ce4b40594ad886103c5aa0e602b7b684c5110188ac9315fa2
EXPECTED_FLUGPI_HASH=4dfcfb7130d037eae155fac039ae7965b47f396407d17fa76022d5ca1c07bade
EXPECTED_FLUDRV_HASH=cb4fa2a1b4f6f07de6bbaa34d73f3c95279ba0c06e593fbb7cf5b10bafc8b746

FC=/opt/homebrew/bin/gfortran
CC=/usr/bin/cc
CPP=/usr/bin/cpp
AR=/usr/bin/ar
EXPECTED_FC_BANNER='GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0'
RUN_B2Y=${RUN_B2Y:-0}
B2Y_RETURNED_XSM=${B2Y_RETURNED_XSM:-}
PRESERVE_B2Y_FAILURE=${PRESERVE_B2Y_FAILURE:-0}
DRAGON_STARTED=0

STATIC_CHECKER="$HERE/check_phase_a9b_b2y_one_real_returned_close.py"
MUTATION_TEST=test_phase_a9b_b2y_one_real_returned_close
BOUNDED="$HERE/run_bounded_b2y.py"
POSTERIOR="$HERE/check_b2y_real_close.f90"
DECK="$HERE/one_real_returned_close.x2m"
HOST_SOURCE="$ROOT/data/SpotCloseR64.c2m"
C2M_HELPER="$ROOT/validation/iterative/real64_phase_a9b_b2k_system_assembly/compile_c2m.c"
PUBLISHER="$HERE/publish_b2y_artifact.py"
ATTEMPT_RESULT="$HERE/attempt_result.txt"

TRACK_AX_ARTIFACT="$ROOT/validation/artifacts/iterative-seed/initial_axial_track.xsm"
MACROLIB3_ARTIFACT="$ROOT/validation/artifacts/iterative-seed/initial_axial_macrolib.xsm"
BASIS_REF_ARTIFACT="$ROOT/validation/artifacts/iterative-map1/basis_reference.xsm"
ARTIFACT_PARENT="$ROOT/validation/artifacts"
B2Z_ARTIFACT_DIR="$ARTIFACT_PARENT/iterative-b2z"
B2Z_RETURNED="$B2Z_ARTIFACT_DIR/returned.xsm"
B2Z_ARTIFACT_RUNTIME_RESULT="$B2Z_ARTIFACT_DIR/runtime_result.txt"
B2Z_ARTIFACT_MANIFEST="$B2Z_ARTIFACT_DIR/artifact_manifest.sha256"
B2Z_ATTEMPT_DIR="$ARTIFACT_PARENT/.iterative-b2z-attempted"
ARTIFACT_DIR="$ARTIFACT_PARENT/real64-phase-a9b-b2y"
LOCK_DIR="$ARTIFACT_PARENT/.real64-phase-a9b-b2y.lock"
ATTEMPT_DIR="$ARTIFACT_PARENT/.real64-phase-a9b-b2y-attempted"
PUBLISH_STAGE=
PUBLISH_STAGE_ID=
LOCK_ID=
FINAL_OWNED_ID=

BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-a9b-b2y.XXXXXX")
SOURCE_DIR="$BUILD_DIR/source"
OBJECT_DIR="$BUILD_DIR/objects"
HOST_DIR="$BUILD_DIR/host"
C2M_DIR="$BUILD_DIR/c2m"
CASE_DIR="$BUILD_DIR/case"

cleanup()
{
  status=$?
  trap - EXIT HUP INT TERM
  owned_final_id=$FINAL_OWNED_ID
  if [ -z "$owned_final_id" ]; then
    owned_final_id=$PUBLISH_STAGE_ID
  fi
  if [ -n "$owned_final_id" ] && [ -d "$ARTIFACT_DIR" ] && \
     [ ! -L "$ARTIFACT_DIR" ] && \
     [ "$(stat -f '%d:%i' "$ARTIFACT_DIR")" = "$owned_final_id" ]; then
    rm -rf "$ARTIFACT_DIR"
  fi
  if [ -n "$PUBLISH_STAGE_ID" ] && [ -d "$PUBLISH_STAGE" ] && \
     [ ! -L "$PUBLISH_STAGE" ] && \
     [ "$(stat -f '%d:%i' "$PUBLISH_STAGE")" = "$PUBLISH_STAGE_ID" ]; then
    rm -rf "$PUBLISH_STAGE"
  fi
  if [ -n "$LOCK_ID" ] && [ -d "$LOCK_DIR" ] && [ ! -L "$LOCK_DIR" ] && \
     [ "$(stat -f '%d:%i' "$LOCK_DIR")" = "$LOCK_ID" ]; then
    rmdir "$LOCK_DIR"
  fi
  if [ "$status" -ne 0 ] && [ -d "$CASE_DIR" ]; then
    for log in dragon.log posterior_a.log posterior_b.log
    do
      if [ -f "$CASE_DIR/$log" ]; then
        printf '%s\n' "--- retained tail before cleanup: $log ---" >&2
        tail -n 200 "$CASE_DIR/$log" >&2
        printf '%s\n' "--- end retained tail: $log ---" >&2
      fi
    done
  fi
  if [ "$status" -ne 0 ] && [ "$PRESERVE_B2Y_FAILURE" = 1 ]; then
    printf '%s\n' "B2Y FAILURE ARTIFACTS PRESERVED: $BUILD_DIR" >&2
    exit "$status"
  fi
  cd /
  rm -rf "$BUILD_DIR"
  exit "$status"
}
trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

LC_ALL=C
export LC_ALL

fail()
{
  if [ "$DRAGON_STARTED" -eq 0 ]; then
    printf '%s\n' \
      "SPOR64 PHASE-A9b-B2y FAILURE: $*; INVALID-NO-SCIENTIFIC-RESULT DRAGON=0" >&2
  else
    printf '%s\n' "SPOR64 PHASE-A9b-B2y FAILURE: $*" >&2
  fi
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

require_bytes()
{
  path=$1
  expected=$2
  [ "$(stat -f '%z' "$path")" -eq "$expected" ] || \
    fail "byte count differs: $path"
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

run_limited()
(
  ulimit -c 0
  ulimit -t 20
  ulimit -f 262144
  "$@"
)

verify_lineage()
{
  [ -f "$B2V_RECEIPT" ] || fail "B2v receipt missing"
  require_hash "$B2V_RECEIPT" "$EXPECTED_B2V_RECEIPT_HASH"
  [ -f "$PARENT_RECEIPT" ] || fail "B2x parent receipt missing"
  require_hash "$PARENT_RECEIPT" "$EXPECTED_PARENT_HASH"
  git -C "$ROOT" cat-file -e "$EXPECTED_B2V_COMMIT^{commit}" || \
    fail "B2v commit missing"
  git -C "$ROOT" merge-base --is-ancestor "$EXPECTED_B2V_COMMIT" HEAD || \
    fail "B2v commit is not an ancestor"
  git -C "$ROOT" cat-file -e "$EXPECTED_PARENT_COMMIT^{commit}" || \
    fail "B2x parent commit missing"
  git -C "$ROOT" merge-base --is-ancestor "$EXPECTED_PARENT_COMMIT" HEAD || \
    fail "B2x parent commit is not an ancestor"
}

verify_b2z_frozen_evidence()
{
  [ -d "$B2Z_ARTIFACT_DIR" ] && [ ! -L "$B2Z_ARTIFACT_DIR" ] || \
    fail "canonical B2z artifact directory differs"
  [ -d "$B2Z_ATTEMPT_DIR" ] && [ ! -L "$B2Z_ATTEMPT_DIR" ] || \
    fail "B2z durable attempt evidence differs"
  for path in "$B2Z_RECEIPT" "$B2Z_RUNTIME_RESULT" \
    "$B2Z_ARTIFACT_MANIFEST" "$B2Z_ARTIFACT_RUNTIME_RESULT" "$B2Z_RETURNED"
  do
    [ -f "$path" ] && [ ! -L "$path" ] || \
      fail "B2z frozen evidence file differs: $path"
  done
  for file in returned.xsm prepare.log dragon.log posterior_a.log \
    posterior_b.log runtime_result.txt artifact_manifest.sha256
  do
    [ -f "$B2Z_ARTIFACT_DIR/$file" ] && \
      [ ! -L "$B2Z_ARTIFACT_DIR/$file" ] || \
      fail "B2z artifact inventory entry differs: $file"
  done
  [ "$(find "$B2Z_ARTIFACT_DIR" -mindepth 1 -maxdepth 1 | wc -l | tr -d ' ')" -eq 7 ] || \
    fail "B2z artifact inventory differs"
  require_hash "$B2Z_RECEIPT" "$EXPECTED_B2Z_RECEIPT_HASH"
  (
    cd "$ROOT"
    shasum -a 256 -c "$B2Z_RECEIPT" >/dev/null
  ) || fail "B2z frozen receipt verification failed"
  require_hash "$B2Z_RUNTIME_RESULT" "$EXPECTED_B2Z_RUNTIME_HASH"
  require_bytes "$B2Z_RUNTIME_RESULT" "$EXPECTED_B2Z_RUNTIME_BYTES"
  require_hash "$B2Z_ARTIFACT_RUNTIME_RESULT" "$EXPECTED_B2Z_RUNTIME_HASH"
  require_bytes "$B2Z_ARTIFACT_RUNTIME_RESULT" "$EXPECTED_B2Z_RUNTIME_BYTES"
  cmp "$B2Z_RUNTIME_RESULT" "$B2Z_ARTIFACT_RUNTIME_RESULT" || \
    fail "B2z tracked and artifact runtime results differ"
  require_hash "$B2Z_ARTIFACT_MANIFEST" \
    "$EXPECTED_B2Z_ARTIFACT_MANIFEST_HASH"
  require_bytes "$B2Z_ARTIFACT_MANIFEST" \
    "$EXPECTED_B2Z_ARTIFACT_MANIFEST_BYTES"
  (
    cd "$B2Z_ARTIFACT_DIR"
    shasum -a 256 -c artifact_manifest.sha256 >/dev/null
  ) || fail "B2z artifact manifest verification failed"
  require_hash "$B2Z_RETURNED" "$EXPECTED_RETURNED_HASH"
  require_bytes "$B2Z_RETURNED" "$EXPECTED_RETURNED_BYTES"
}

verify_b2z_staged_input()
{
  [ -n "$B2Y_RETURNED_XSM" ] || fail "B2Y_RETURNED_XSM is required"
  [ "$B2Y_RETURNED_XSM" = "$B2Z_RETURNED" ] || \
    fail "B2Y_RETURNED_XSM must be the canonical B2z staged RETURNED"
  verify_b2z_frozen_evidence
}

verify_receipt()
{
  if [ -f "$RECEIPT" ]; then
    grep -q '"receipt": "frozen"' "$HERE/precision_manifest.json" || \
      fail "receipt exists but manifest is not frozen"
    (
      cd "$ROOT"
      shasum -a 256 -c "$RECEIPT" >/dev/null
    ) || fail "B2y invalid-attempt freeze receipt verification failed"
    RECEIPT_STATE=FROZEN
  else
    grep -q '"receipt": "pending"' "$HERE/precision_manifest.json" || \
      fail "missing receipt without pending manifest"
    RECEIPT_STATE=PENDING-ATTEMPT-FREEZE
  fi
}

verify_execution_snapshot()
{
  git -C "$ROOT" merge-base --is-ancestor "$EXECUTION_SNAPSHOT_COMMIT" HEAD || \
    fail "B2y execution snapshot is not an ancestor"
  for item in \
    "validation/iterative/real64_phase_a9b_b2y_one_real_returned_close/run_bounded_b2y.py:$EXECUTED_WRAPPER_HASH" \
    "validation/iterative/real64_phase_a9b_b2y_one_real_returned_close/run_phase_a9b_b2y_one_real_returned_close.sh:$EXECUTED_RUNNER_HASH" \
    "validation/iterative/real64_phase_a9b_b2y_one_real_returned_close/one_real_returned_close.x2m:$EXECUTED_DECK_HASH" \
    "data/SpotCloseR64.c2m:$EXECUTED_SPOTCLOSE_HASH" \
    "src/FLU2DR.f:$EXECUTED_FLU2DR_HASH"
  do
    path=${item%:*}
    expected=${item##*:}
    actual=$(git -C "$ROOT" show "$EXECUTION_SNAPSHOT_COMMIT:$path" | \
      shasum -a 256 | sed -n '1s/[[:space:]].*//p')
    [ "$actual" = "$expected" ] || \
      fail "B2y execution snapshot blob differs: $path"
  done
}

verify_frozen_build_inputs()
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
  require_hash "$ROOT/src/FLUGPI.f" "$EXPECTED_FLUGPI_HASH"
  require_hash "$ROOT/src/FLUDRV.f" "$EXPECTED_FLUDRV_HASH"
}

require_normal_end()
{
  log=$1
  runtime_count_exact 1 \
    '^ normal end of execution for dragon 5  Version 5\.1\.0[[:space:]]*$' \
    "$log"
  runtime_count_exact 1 'normal end of execution for dragon' "$log"
  if grep -Ei \
    'XABORT|segmentation fault|floating invalid|NaN|Infinity|SIGKILL|SIGTERM|CONVERGENCE NOT REACHED|FLU2DR-DIAG' \
    "$log" >/dev/null
  then
    fail "abnormal Dragon text; FAILED-NO-CLOSED"
  fi
}

line_of()
{
  pattern=$1
  file=$2
  grep -n -E "$pattern" "$file" | sed -n '1s/:.*//p'
}

case "$RUN_B2Y" in
  0) ;;
  1) fail "B2y authorization was consumed; future B2y activation is forbidden" ;;
  *) fail "RUN_B2Y must be exactly 0 or 1" ;;
esac
case "$PRESERVE_B2Y_FAILURE" in
  0|1) ;;
  *) fail "PRESERVE_B2Y_FAILURE must be exactly 0 or 1" ;;
esac

[ "$(uname -s)" = Darwin ] || fail "frozen platform is Darwin"
[ "$(uname -m)" = arm64 ] || fail "frozen architecture is arm64"
[ -x "$FC" ] || fail "frozen Fortran compiler missing"
[ -x "$CC" ] || fail "host C compiler missing"
[ -x "$CPP" ] || fail "host preprocessor missing"
[ -x "$AR" ] || fail "host archive tool missing"
[ "$($FC --version | sed -n '1p')" = "$EXPECTED_FC_BANNER" ] || \
  fail "unaudited compiler"
[ -d "$ARTIFACT_PARENT" ] && [ ! -L "$ARTIFACT_PARENT" ] || \
  fail "artifact parent is not a non-symlink directory"

for path in "$STATIC_CHECKER" "$HERE/$MUTATION_TEST.py" "$BOUNDED" \
  "$PUBLISHER" "$POSTERIOR" "$DECK" "$HOST_SOURCE" "$C2M_HELPER" \
  "$ATTEMPT_RESULT" \
  "$TRACK_AX_ARTIFACT" "$MACROLIB3_ARTIFACT" "$BASIS_REF_ARTIFACT" \
  "$HERE/README.md" "$HERE/precision_manifest.json" \
  "$B2Z_RECEIPT" "$B2Z_RUNTIME_RESULT" "$B2Z_ARTIFACT_MANIFEST" \
  "$B2Z_ARTIFACT_RUNTIME_RESULT" "$B2Z_RETURNED" \
  "$ROOT/lib/Darwin_arm64/libDragon.a"
do
  [ -f "$path" ] || fail "required input missing: $path"
done
for source in SPOR64_B2B SPOR64_B2C SPOR64_B2K SPOR64_B2N \
  SPOR64_B2O SPOR64_B2R SPOR64_B2S SPOR64_B2T SPOR64_B2U \
  SPOR64_B2W SPOR64_B2X SPOT_LEAKAGE SPOSTATE SPOLEAK
do
  [ -f "$ROOT/src/$source.f90" ] || fail "production $source missing"
done
for source in ASM.f FLU.f FLUGPI.f FLUDRV.f FLU2DR.f KDRDRV.F
do
  [ -f "$ROOT/src/$source" ] || fail "production $source missing"
done

verify_lineage
verify_receipt
verify_execution_snapshot
verify_frozen_build_inputs
verify_b2z_frozen_evidence
require_hash "$TRACK_AX_ARTIFACT" "$EXPECTED_TRACK_AX_HASH"
require_bytes "$TRACK_AX_ARTIFACT" "$EXPECTED_TRACK_AX_BYTES"
require_hash "$MACROLIB3_ARTIFACT" "$EXPECTED_MACROLIB3_HASH"
require_bytes "$MACROLIB3_ARTIFACT" "$EXPECTED_MACROLIB3_BYTES"
require_hash "$BASIS_REF_ARTIFACT" "$EXPECTED_BASIS_REF_HASH"
require_bytes "$BASIS_REF_ARTIFACT" "$EXPECTED_BASIS_REF_BYTES"
git -C "$ROOT" diff --check || fail "whitespace errors"

mkdir -p "$SOURCE_DIR" "$OBJECT_DIR" "$HOST_DIR" "$C2M_DIR" "$CASE_DIR"

if ! PYTHONDONTWRITEBYTECODE=1 python3 "$STATIC_CHECKER" \
  >"$BUILD_DIR/static.log" 2>&1
then
  sed -n '1,260p' "$BUILD_DIR/static.log" >&2
  fail "static one-real-returned-close contract rejected"
fi
count_exact 1 '^B2Y STATIC ONE-REAL-RETURNED-CLOSE PASS$' "$BUILD_DIR/static.log"

if ! (
  cd "$HERE"
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$HERE" \
    python3 -m unittest -v "$MUTATION_TEST" \
    >"$BUILD_DIR/mutations.log" 2>&1
)
then
  sed -n '1,300p' "$BUILD_DIR/mutations.log" >&2
  fail "B2y mutation suite rejected"
fi
count_exact 1 '^Ran 81 tests in [0-9.]+s$' "$BUILD_DIR/mutations.log"
count_exact 1 '^OK$' "$BUILD_DIR/mutations.log"

for source in SPOR64_B2C SPOR64_B2B SPOR64_B2K SPOR64_B2N \
  SPOR64_B2O SPOR64_B2R SPOR64_B2S SPOR64_B2T SPOR64_B2U \
  SPOR64_B2W SPOR64_B2X SPOT_LEAKAGE SPOSTATE SPOLEAK
do
  copy_exact "$ROOT/src/$source.f90" "$SOURCE_DIR/$source.f90"
done
for source in ASM.f FLU.f FLUGPI.f FLUDRV.f FLU2DR.f KDRDRV.F
do
  copy_exact "$ROOT/src/$source" "$SOURCE_DIR/$source"
done
copy_exact "$HOST_SOURCE" "$SOURCE_DIR/SpotCloseR64.c2m"
copy_exact "$C2M_HELPER" "$SOURCE_DIR/compile_c2m.c"
copy_exact "$POSTERIOR" "$SOURCE_DIR/check_b2y_real_close.f90"
copy_exact "$DECK" "$CASE_DIR/one_real_returned_close.x2m"

STRICT_FLAGS='-O0 -g -std=f2008 -pedantic -Wall -Wextra -Werror'
STRICT_FLAGS="$STRICT_FLAGS -fimplicit-none -fcheck=all -fbacktrace"
STRICT_FLAGS="$STRICT_FLAGS -ffp-contract=off -fno-fast-math"
HOST_FLAGS='-fPIC -Wall -Wextra -Werror -frecord-marker=4 -ffpe-summary=none'
HOST_FLAGS="$HOST_FLAGS -O2 -march=native -ffp-contract=off"
GANMOD="$ROOT/Ganlib/lib/Darwin_arm64/modules"
DRAMOD="$ROOT/lib/Darwin_arm64/modules"
GANLIB="$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a"
UTILIB="$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a"

# Build the independent posterior before any possible Dragon activation.
"$FC" $STRICT_FLAGS -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/check_b2y_real_close.f90" \
  -o "$OBJECT_DIR/check_b2y_real_close.o"
"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$OBJECT_DIR/check_b2y_real_close.o" "$GANLIB" "$UTILIB" \
  -o "$BUILD_DIR/check_b2y_real_close"
nm -g "$BUILD_DIR/check_b2y_real_close" >"$BUILD_DIR/posterior.nm"
if grep -Eiq \
  '(^|[[:space:]])_?(dragon|asm|asmdrv|xdrta2|kdrdrv|doorav|doorfv|doorpv|mccga|mccgf|mcgasm|flu|fludrv|flu2dr|spostate|spoleak|spomoc|spoasm|spor64)_$|___spor64_' \
  "$BUILD_DIR/posterior.nm"
then
  fail "independent posterior links production lifecycle or solver code"
fi
grep -i 'lcmop' "$BUILD_DIR/posterior.nm" >/dev/null || \
  fail "independent posterior lacks GANLIB read path"

# Compile the production procedure and the one-call deck with CLEPIL/OBJPIL.
"$CC" -std=c11 -pedantic -Wall -Wextra -Werror \
  -I "$ROOT/Ganlib/src" -c "$SOURCE_DIR/compile_c2m.c" \
  -o "$C2M_DIR/compile_c2m.o"
"$FC" "$C2M_DIR/compile_c2m.o" "$GANLIB" -o "$C2M_DIR/compile_c2m"
if ! (
  cd "$C2M_DIR"
  run_limited ./compile_c2m "$SOURCE_DIR/SpotCloseR64.c2m" \
    SpotCloseR64.o2m >procedure_compile.log 2>&1
)
then
  sed -n '1,240p' "$C2M_DIR/procedure_compile.log" >&2
  fail "CLEPIL/OBJPIL compilation of SpotCloseR64 failed"
fi
if ! (
  cd "$C2M_DIR"
  run_limited ./compile_c2m "$DECK" one_real_returned_close.o2m \
    >deck_compile.log 2>&1
)
then
  sed -n '1,240p' "$C2M_DIR/deck_compile.log" >&2
  fail "CLEPIL/OBJPIL compilation of B2y deck failed"
fi
for object in SpotCloseR64.o2m one_real_returned_close.o2m
do
  [ -s "$C2M_DIR/$object" ] || fail "empty C2M object: $object"
done
C2M_OBJECT_HASH=$(hash_of "$C2M_DIR/SpotCloseR64.o2m")
copy_exact "$SOURCE_DIR/SpotCloseR64.c2m" "$CASE_DIR/SpotCloseR64.c2m"
copy_exact "$C2M_DIR/SpotCloseR64.o2m" "$CASE_DIR/SpotCloseR64.o2m"

# Build a private archive. Shared Dragon libraries and executables are never
# modified; the currently validated close path replaces same-name members.
"$FC" $HOST_FLAGS -I "$GANMOD" -I "$HOST_DIR" -I "$DRAMOD" \
  -J "$HOST_DIR" -c "$SOURCE_DIR/SPOR64_B2C.f90" \
  -o "$HOST_DIR/SPOR64_B2C.o"
"$FC" $HOST_FLAGS -I "$GANMOD" -I "$HOST_DIR" -I "$DRAMOD" \
  -J "$HOST_DIR" -c "$SOURCE_DIR/SPOR64_B2B.f90" \
  -o "$HOST_DIR/SPOR64_B2B.o"
for source in SPOR64_B2K SPOR64_B2N SPOR64_B2O SPOR64_B2R
do
  "$FC" $HOST_FLAGS -I "$GANMOD" -I "$HOST_DIR" -I "$DRAMOD" \
    -J "$HOST_DIR" -c "$SOURCE_DIR/$source.f90" \
    -o "$HOST_DIR/$source.o"
done
for source in SPOR64_B2S SPOR64_B2T SPOR64_B2U
do
  "$FC" $HOST_FLAGS -I "$GANMOD" -I "$HOST_DIR" -I "$DRAMOD" \
    -J "$HOST_DIR" -c "$SOURCE_DIR/$source.f90" \
    -o "$HOST_DIR/$source.o"
done
"$FC" $HOST_FLAGS -I "$GANMOD" -I "$HOST_DIR" -I "$DRAMOD" \
  -J "$HOST_DIR" -c "$SOURCE_DIR/SPOT_LEAKAGE.f90" \
  -o "$HOST_DIR/SPOT_LEAKAGE.o"
for source in SPOSTATE SPOLEAK
do
  "$FC" $HOST_FLAGS -Wno-unused-dummy-argument \
    -I "$GANMOD" -I "$HOST_DIR" -I "$DRAMOD" \
    -J "$HOST_DIR" -c "$SOURCE_DIR/$source.f90" \
    -o "$HOST_DIR/$source.o"
done
"$FC" $HOST_FLAGS -I "$GANMOD" -I "$HOST_DIR" -I "$DRAMOD" \
  -J "$HOST_DIR" -c "$SOURCE_DIR/SPOR64_B2W.f90" \
  -o "$HOST_DIR/SPOR64_B2W.o"
"$FC" $HOST_FLAGS -I "$GANMOD" -I "$HOST_DIR" -I "$DRAMOD" \
  -J "$HOST_DIR" -c "$SOURCE_DIR/SPOR64_B2X.f90" \
  -o "$HOST_DIR/SPOR64_B2X.o"

for source in ASM FLUGPI FLUDRV FLU2DR FLU
do
  "$FC" $HOST_FLAGS -Wno-unused-parameter -Wno-compare-reals \
    -Wno-unused-dummy-argument \
    -I "$GANMOD" -I "$HOST_DIR" -I "$DRAMOD" \
    -c "$SOURCE_DIR/$source.f" -ffixed-line-length-72 \
    -o "$HOST_DIR/$source.o"
done
"$CPP" -P -W -traditional -DLinux -DUnix "$SOURCE_DIR/KDRDRV.F" \
  "$HOST_DIR/KDRDRV.pp.f"
"$FC" $HOST_FLAGS -I "$GANMOD" -I "$HOST_DIR" -I "$DRAMOD" \
  -c "$HOST_DIR/KDRDRV.pp.f" -ffixed-line-length-72 \
  -o "$HOST_DIR/KDRDRV.o"

cp "$ROOT/lib/Darwin_arm64/libDragon.a" "$HOST_DIR/libDragon.b2y.a"
"$AR" rcs "$HOST_DIR/libDragon.b2y.a" \
  "$HOST_DIR/ASM.o" "$HOST_DIR/FLU.o" "$HOST_DIR/FLUGPI.o" \
  "$HOST_DIR/FLUDRV.o" "$HOST_DIR/FLU2DR.o" "$HOST_DIR/KDRDRV.o" \
  "$HOST_DIR/SPOR64_B2B.o" "$HOST_DIR/SPOR64_B2C.o" \
  "$HOST_DIR/SPOR64_B2K.o" "$HOST_DIR/SPOR64_B2N.o" \
  "$HOST_DIR/SPOR64_B2O.o" "$HOST_DIR/SPOR64_B2R.o" \
  "$HOST_DIR/SPOR64_B2S.o" "$HOST_DIR/SPOR64_B2T.o" \
  "$HOST_DIR/SPOR64_B2U.o" \
  "$HOST_DIR/SPOT_LEAKAGE.o" "$HOST_DIR/SPOSTATE.o" \
  "$HOST_DIR/SPOLEAK.o" "$HOST_DIR/SPOR64_B2W.o" \
  "$HOST_DIR/SPOR64_B2X.o"
"$AR" t "$HOST_DIR/libDragon.b2y.a" >"$HOST_DIR/archive-members.txt"
for member in ASM.o FLU.o FLUGPI.o FLUDRV.o FLU2DR.o KDRDRV.o \
  SPOR64_B2B.o SPOR64_B2C.o SPOR64_B2K.o SPOR64_B2N.o \
  SPOR64_B2O.o SPOR64_B2R.o SPOR64_B2S.o SPOR64_B2T.o SPOR64_B2U.o \
  SPOT_LEAKAGE.o SPOSTATE.o SPOLEAK.o \
  SPOR64_B2W.o SPOR64_B2X.o
do
  count_exact 1 "^${member}$" "$HOST_DIR/archive-members.txt"
done
"$FC" -O2 -march=native -ffp-contract=off \
  "$ROOT/src/DRAGON.o" "$HOST_DIR/libDragon.b2y.a" \
  "$ROOT/Trivac/lib/Darwin_arm64/libTrivac.a" "$UTILIB" "$GANLIB" \
  -o "$BUILD_DIR/Dragon.b2y"
nm -g "$BUILD_DIR/Dragon.b2y" >"$BUILD_DIR/Dragon.nm"
for symbol in _spor64k_ _spor64t_ _spor64v_ _spor64x_ _asm_ _flu_ \
  _spostate_ _spoleak_
do
  count_exact 1 " T ${symbol}$" "$BUILD_DIR/Dragon.nm"
done
for symbol in spor64_b2w_MOD_spor64_b2w_admit_returned \
  spor64_b2w_MOD_spor64_b2w_close
do
  count_exact 1 " T _*${symbol}$" "$BUILD_DIR/Dragon.nm"
done

if [ "$RUN_B2Y" = 0 ]; then
  printf '%s\n' 'SPOR64 PHASE-A9b-B2y PREFLIGHT PASS'
  printf '%s\n' \
    'ACTIVATION=CONSUMED; FUTURE-B2Y-ACTIVATION=FORBIDDEN'
  printf '%s\n' \
    'CURRENT-DEFAULT-OFF-CHECK DRAGON=0 SPOTCLOSE=0 ASM=0 FLU=0 AXIAL-SOLVE=0 PICARD=0'
  printf '%s\n' \
    'CURRENT-CHECK PRODUCTION-CLOSE=COMPILE/LINK-ONLY POSTERIOR=GANLIB/UTILIB-ONLY-COMPILE'
  printf '%s\n' \
    'HISTORICAL-B2Y-ATTEMPT DRAGON=1 ATTEMPTS=1 RETRIES=0 BOUNDED-WRAPPER-PASS=NO'
  printf '%s\n' \
    'SCIENTIFIC-CLASSIFICATION=INVALID-RUNTIME-EVIDENCE SCIENTIFIC-RESULT=NONE'
  printf '%s\n' \
    'SHELL-RUNTIME-CENSUS=NOT-REACHED POSTERIOR-EXECUTIONS=0 ARTIFACT-PUBLICATIONS=0 ACCEPTED-CLOSED=NO'
  printf '%s\n' \
    "ATTEMPT-FREEZE-RECEIPT=$RECEIPT_STATE INPUT-PARENT=B2z CLOSE-CONTRACT-LINEAGE=B2x"
  exit 0
fi

[ ! -e "$ARTIFACT_DIR" ] && [ ! -L "$ARTIFACT_DIR" ] || \
  fail "canonical B2y artifact target is not fresh"
[ ! -e "$ATTEMPT_DIR" ] && [ ! -L "$ATTEMPT_DIR" ] || \
  fail "B2y one-real activation authorization was already consumed"
if ! mkdir "$LOCK_DIR"; then
  fail "B2y activation lock is already held"
fi
LOCK_ID=$(stat -f '%d:%i' "$LOCK_DIR")
[ -d "$LOCK_DIR" ] && [ ! -L "$LOCK_DIR" ] || fail "B2y lock differs"
[ ! -e "$ARTIFACT_DIR" ] && [ ! -L "$ARTIFACT_DIR" ] || \
  fail "canonical B2y artifact target appeared after locking"
[ ! -e "$ATTEMPT_DIR" ] && [ ! -L "$ATTEMPT_DIR" ] || \
  fail "B2y activation attempt appeared after locking"

verify_b2z_staged_input
[ -n "$B2Y_RETURNED_XSM" ] || \
  fail "B2Y_RETURNED_XSM is required"
[ -f "$B2Y_RETURNED_XSM" ] || \
  fail "B2Y_RETURNED_XSM is not a file"
[ ! -L "$B2Y_RETURNED_XSM" ] || \
  fail "B2Y_RETURNED_XSM is a symlink"
require_hash "$B2Y_RETURNED_XSM" "$EXPECTED_RETURNED_HASH"
[ "$(stat -f '%z' "$B2Y_RETURNED_XSM")" -eq "$EXPECTED_RETURNED_BYTES" ] || \
  fail "B2Y_RETURNED_XSM byte count differs"

for output in ax_closed.xsm archive_closed.xsm
do
  [ ! -e "$CASE_DIR/$output" ] || \
    fail "nonfresh output path"
done
copy_exact "$B2Y_RETURNED_XSM" "$CASE_DIR/returned.xsm"
require_hash "$CASE_DIR/returned.xsm" "$EXPECTED_RETURNED_HASH"
[ "$(stat -f '%z' "$CASE_DIR/returned.xsm")" -eq "$EXPECTED_RETURNED_BYTES" ] || \
  fail "private RETURNED byte count differs"
copy_exact "$TRACK_AX_ARTIFACT" "$CASE_DIR/initial_axial_track.xsm"
copy_exact "$MACROLIB3_ARTIFACT" "$CASE_DIR/initial_axial_macrolib.xsm"
copy_exact "$BASIS_REF_ARTIFACT" "$CASE_DIR/basis_reference.xsm"
chmod 444 "$CASE_DIR/returned.xsm" "$CASE_DIR/initial_axial_track.xsm" \
  "$CASE_DIR/initial_axial_macrolib.xsm" "$CASE_DIR/basis_reference.xsm"

RETURNED_BEFORE=$(hash_of "$CASE_DIR/returned.xsm")
TRACK_BEFORE=$(hash_of "$CASE_DIR/initial_axial_track.xsm")
MACRO_BEFORE=$(hash_of "$CASE_DIR/initial_axial_macrolib.xsm")
BASIS_BEFORE=$(hash_of "$CASE_DIR/basis_reference.xsm")
EXTERNAL_BEFORE=$(hash_of "$B2Y_RETURNED_XSM")
DRAGON_HASH=$(hash_of "$BUILD_DIR/Dragon.b2y")
DECK_HASH=$(hash_of "$CASE_DIR/one_real_returned_close.x2m")

# The only close-profile launch site. Failure never reaches a second launch.
if ! mkdir "$ATTEMPT_DIR"; then
  fail "B2y one-real activation authorization could not be consumed"
fi
[ -d "$ATTEMPT_DIR" ] && [ ! -L "$ATTEMPT_DIR" ] || \
  fail "B2y durable attempt sentinel differs"
ATTEMPT_ID=$(stat -f '%d:%i' "$ATTEMPT_DIR")
DRAGON_STARTED=1
if ! python3 "$BOUNDED" close "$BUILD_DIR/Dragon.b2y" \
  "$CASE_DIR/one_real_returned_close.x2m" "$CASE_DIR/dragon.log"
then
  show_failure_log "$CASE_DIR/dragon.log"
  fail "single bounded Dragon close failed; NO-RETRY"
fi

require_normal_end "$CASE_DIR/dragon.log"
if grep -E 'COMPILING _MAIN\.c2m FILE|BAD OBJECTS _MAIN\.c2m FILE' \
  "$CASE_DIR/dragon.log" >/dev/null
then
  fail "runtime C2M compilation error/branch; INVALID-RUNTIME-EVIDENCE"
fi
runtime_count_exact 1 '^->@BEGIN MODULE : SPOR64V:' "$CASE_DIR/dragon.log"
runtime_count_exact 1 '^->@END MODULE   : SPOR64V:' "$CASE_DIR/dragon.log"
runtime_count_exact 1 '^->@BEGIN MODULE : ASM:' "$CASE_DIR/dragon.log"
runtime_count_exact 1 '^->@END MODULE   : ASM:' "$CASE_DIR/dragon.log"
runtime_count_exact 1 '^->@BEGIN MODULE : FLU:' "$CASE_DIR/dragon.log"
runtime_count_exact 1 '^->@END MODULE   : FLU:' "$CASE_DIR/dragon.log"
runtime_count_exact 1 '^->@BEGIN MODULE : SPOSTATE:' "$CASE_DIR/dragon.log"
runtime_count_exact 1 '^->@END MODULE   : SPOSTATE:' "$CASE_DIR/dragon.log"
runtime_count_exact 1 '^->@BEGIN MODULE : SPOLEAK:' "$CASE_DIR/dragon.log"
runtime_count_exact 1 '^->@END MODULE   : SPOLEAK:' "$CASE_DIR/dragon.log"
runtime_count_exact 1 '^->@BEGIN MODULE : SPOR64X:' "$CASE_DIR/dragon.log"
runtime_count_exact 1 '^->@END MODULE   : SPOR64X:' "$CASE_DIR/dragon.log"
runtime_count_exact 1 '^ FLU2DR-TERM OUTER-GATE=PASS ' "$CASE_DIR/dragon.log"
runtime_count_exact 1 '^ FLU2DR-TERM INNER-TERMINAL ' "$CASE_DIR/dragon.log"
runtime_count_exact 1 \
  '^>\|B2Y-REAL-RETURNED-CLOSE-BEGIN[[:space:]]*\|>[0-9][0-9][0-9][0-9]$' \
  "$CASE_DIR/dragon.log"
runtime_count_exact 1 \
  '^>\|B2Y-REAL-RETURNED-CLOSE-COMPLETE[[:space:]]*\|>[0-9][0-9][0-9][0-9]$' \
  "$CASE_DIR/dragon.log"
if grep -E -- '->@BEGIN MODULE : (SPOR64T|SPOR64K|SPOFSRC|SPOFCHK|SPOPROJ):' \
  "$CASE_DIR/dragon.log" >/dev/null
then
  fail "forbidden module reached; INVALID-RUNTIME-EVIDENCE"
fi

BEGIN_LINE=$(line_of '^>\|B2Y-REAL-RETURNED-CLOSE-BEGIN' "$CASE_DIR/dragon.log")
V_BEGIN=$(line_of '^->@BEGIN MODULE : SPOR64V:' "$CASE_DIR/dragon.log")
V_END=$(line_of '^->@END MODULE   : SPOR64V:' "$CASE_DIR/dragon.log")
ASM_BEGIN=$(line_of '^->@BEGIN MODULE : ASM:' "$CASE_DIR/dragon.log")
ASM_END=$(line_of '^->@END MODULE   : ASM:' "$CASE_DIR/dragon.log")
FLU_BEGIN=$(line_of '^->@BEGIN MODULE : FLU:' "$CASE_DIR/dragon.log")
OUTER_TERM_LINE=$(line_of '^ FLU2DR-TERM OUTER-GATE=PASS ' "$CASE_DIR/dragon.log")
INNER_TERM_LINE=$(line_of '^ FLU2DR-TERM INNER-TERMINAL ' "$CASE_DIR/dragon.log")
FLU_END=$(line_of '^->@END MODULE   : FLU:' "$CASE_DIR/dragon.log")
STATE_BEGIN=$(line_of '^->@BEGIN MODULE : SPOSTATE:' "$CASE_DIR/dragon.log")
STATE_END=$(line_of '^->@END MODULE   : SPOSTATE:' "$CASE_DIR/dragon.log")
LEAK_BEGIN=$(line_of '^->@BEGIN MODULE : SPOLEAK:' "$CASE_DIR/dragon.log")
LEAK_END=$(line_of '^->@END MODULE   : SPOLEAK:' "$CASE_DIR/dragon.log")
X_BEGIN=$(line_of '^->@BEGIN MODULE : SPOR64X:' "$CASE_DIR/dragon.log")
X_END=$(line_of '^->@END MODULE   : SPOR64X:' "$CASE_DIR/dragon.log")
COMPLETE_LINE=$(line_of '^>\|B2Y-REAL-RETURNED-CLOSE-COMPLETE' "$CASE_DIR/dragon.log")
[ "$BEGIN_LINE" -lt "$V_BEGIN" ] && [ "$V_BEGIN" -lt "$V_END" ] && \
  [ "$V_END" -lt "$ASM_BEGIN" ] && [ "$ASM_BEGIN" -lt "$ASM_END" ] && \
  [ "$ASM_END" -lt "$FLU_BEGIN" ] && \
  [ "$FLU_BEGIN" -lt "$OUTER_TERM_LINE" ] && \
  [ "$OUTER_TERM_LINE" -lt "$INNER_TERM_LINE" ] && \
  [ "$INNER_TERM_LINE" -lt "$FLU_END" ] && \
  [ "$FLU_END" -lt "$STATE_BEGIN" ] && [ "$STATE_BEGIN" -lt "$STATE_END" ] && \
  [ "$STATE_END" -lt "$LEAK_BEGIN" ] && [ "$LEAK_BEGIN" -lt "$LEAK_END" ] && \
  [ "$LEAK_END" -lt "$X_BEGIN" ] && [ "$X_BEGIN" -lt "$X_END" ] && \
  [ "$X_END" -lt "$COMPLETE_LINE" ] || \
  fail "runtime route is reordered or interleaved; INVALID-RUNTIME-EVIDENCE"

OUTER_LINE=$(grep '^ FLU2DR-TERM OUTER-GATE=PASS ' "$CASE_DIR/dragon.log")
OUTER_VALUES=$(printf '%s\n' "$OUTER_LINE" | sed -E \
  's/^ FLU2DR-TERM OUTER-GATE=PASS IEXTF= *([0-9]+) MAXOUT= *([0-9]+).* EUNK-VALID=([0-9]+)$/\1 \2 \3/')
set -- $OUTER_VALUES
[ "$#" -eq 3 ] || fail "outer terminal parse failed; INVALID-RUNTIME-EVIDENCE"
IEXTF=$1
MAXOUT=$2
EUNK_VALID=$3
[ "$IEXTF" -ge 2 ] && [ "$IEXTF" -le 500 ] && \
  [ "$MAXOUT" -eq 500 ] && [ "$EUNK_VALID" -eq 1 ] || \
  fail "outer terminal census differs; INVALID-RUNTIME-EVIDENCE"

INNER_LINE=$(grep '^ FLU2DR-TERM INNER-TERMINAL ' "$CASE_DIR/dragon.log")
INNER_VALUES=$(printf '%s\n' "$INNER_LINE" | sed -E \
  's/^ FLU2DR-TERM INNER-TERMINAL ITERF= *([0-9]+) MAXINR= *([0-9]+).* IGDEB= *([0-9]+) STATE=([0-9]+) NGRP= *([0-9]+)$/\1 \2 \3 \4 \5/')
set -- $INNER_VALUES
[ "$#" -eq 5 ] || fail "inner terminal parse failed; INVALID-RUNTIME-EVIDENCE"
ITERF=$1
MAXINR=$2
IGDEB=$3
INNER_STATE=$4
NGRP=$5
[ "$ITERF" -ge 1 ] && [ "$ITERF" -le 740 ] && \
  [ "$MAXINR" -eq 740 ] && [ "$IGDEB" -eq 371 ] && \
  [ "$INNER_STATE" -eq 1 ] && [ "$NGRP" -eq 370 ] || \
  fail "inner terminal census differs; INVALID-RUNTIME-EVIDENCE"

for output in ax_closed.xsm archive_closed.xsm
do
  [ -s "$CASE_DIR/$output" ] || fail "$output missing; FAILED-NO-CLOSED"
  [ ! -L "$CASE_DIR/$output" ] || fail "$output is a symlink; INVALID-CLOSED-EVIDENCE"
  [ "$(stat -f '%z' "$CASE_DIR/$output")" -le 536870912 ] || \
    fail "$output exceeds file cap; INVALID-CLOSED-EVIDENCE"
  chmod 444 "$CASE_DIR/$output"
done

[ "$(hash_of "$CASE_DIR/returned.xsm")" = "$RETURNED_BEFORE" ] || \
  fail "private RETURNED changed; INVALID-CLOSED-EVIDENCE"
[ "$(hash_of "$CASE_DIR/initial_axial_track.xsm")" = "$TRACK_BEFORE" ] || \
  fail "TRACK_AX changed; INVALID-CLOSED-EVIDENCE"
[ "$(hash_of "$CASE_DIR/initial_axial_macrolib.xsm")" = "$MACRO_BEFORE" ] || \
  fail "MACROLIB3 changed; INVALID-CLOSED-EVIDENCE"
[ "$(hash_of "$CASE_DIR/basis_reference.xsm")" = "$BASIS_BEFORE" ] || \
  fail "BASIS_REF changed; INVALID-CLOSED-EVIDENCE"
[ "$(hash_of "$B2Y_RETURNED_XSM")" = "$EXTERNAL_BEFORE" ] || \
  fail "external RETURNED changed; INVALID-CLOSED-EVIDENCE"

AX_HASH=$(hash_of "$CASE_DIR/ax_closed.xsm")
ARCH_HASH=$(hash_of "$CASE_DIR/archive_closed.xsm")
AX_BYTES=$(stat -f '%z' "$CASE_DIR/ax_closed.xsm")
ARCH_BYTES=$(stat -f '%z' "$CASE_DIR/archive_closed.xsm")

if ! python3 "$BOUNDED" posterior "$BUILD_DIR/check_b2y_real_close" - \
  "$CASE_DIR/posterior_a.log" returned.xsm ax_closed.xsm archive_closed.xsm
then
  show_failure_log "$CASE_DIR/posterior_a.log"
  fail "first independent posterior failed; INVALID-CLOSED-EVIDENCE"
fi
if ! python3 "$BOUNDED" posterior "$BUILD_DIR/check_b2y_real_close" - \
  "$CASE_DIR/posterior_b.log" returned.xsm ax_closed.xsm archive_closed.xsm
then
  show_failure_log "$CASE_DIR/posterior_b.log"
  fail "second independent posterior failed; INVALID-CLOSED-EVIDENCE"
fi
cmp "$CASE_DIR/posterior_a.log" "$CASE_DIR/posterior_b.log" || \
  fail "posterior reports differ; INVALID-CLOSED-EVIDENCE"
count_exact 1 '^B2Y REAL RETURNED-CLOSE POSTERIOR PASS$' "$CASE_DIR/posterior_a.log"
sed -n '1,40p' "$CASE_DIR/posterior_a.log"

[ "$(hash_of "$CASE_DIR/returned.xsm")" = "$RETURNED_BEFORE" ] || \
  fail "RETURNED changed during posterior; INVALID-CLOSED-EVIDENCE"
[ "$(hash_of "$CASE_DIR/ax_closed.xsm")" = "$AX_HASH" ] || \
  fail "AX_CLOSED changed during posterior; INVALID-CLOSED-EVIDENCE"
[ "$(hash_of "$CASE_DIR/archive_closed.xsm")" = "$ARCH_HASH" ] || \
  fail "ARCH_CLOSED changed during posterior; INVALID-CLOSED-EVIDENCE"
[ "$(hash_of "$B2Y_RETURNED_XSM")" = "$EXTERNAL_BEFORE" ] || \
  fail "external RETURNED changed during posterior; INVALID-CLOSED-EVIDENCE"

require_hash "$CASE_DIR/SpotCloseR64.o2m" "$C2M_OBJECT_HASH"
require_hash "$TRACK_AX_ARTIFACT" "$EXPECTED_TRACK_AX_HASH"
require_hash "$MACROLIB3_ARTIFACT" "$EXPECTED_MACROLIB3_HASH"
require_hash "$BASIS_REF_ARTIFACT" "$EXPECTED_BASIS_REF_HASH"
verify_lineage
verify_receipt
verify_frozen_build_inputs
verify_b2z_staged_input

if [ ! -f "$RECEIPT" ]; then
  RECEIPT_STATE=PENDING-RUNTIME-FREEZE
fi

[ ! -e "$ARTIFACT_DIR" ] && [ ! -L "$ARTIFACT_DIR" ] || \
  fail "canonical artifact appeared before publication"
PUBLISH_STAGE=$(mktemp -d "$ARTIFACT_PARENT/.real64-phase-a9b-b2y-publish.XXXXXX")
PUBLISH_STAGE_ID=$(stat -f '%d:%i' "$PUBLISH_STAGE")
[ -d "$PUBLISH_STAGE" ] && [ ! -L "$PUBLISH_STAGE" ] || \
  fail "publication stage differs"
copy_exact "$CASE_DIR/ax_closed.xsm" "$PUBLISH_STAGE/ax_closed.xsm"
copy_exact "$CASE_DIR/archive_closed.xsm" "$PUBLISH_STAGE/archive_closed.xsm"
copy_exact "$CASE_DIR/dragon.log" "$PUBLISH_STAGE/dragon.log"
copy_exact "$CASE_DIR/posterior_a.log" "$PUBLISH_STAGE/posterior_a.log"
copy_exact "$CASE_DIR/posterior_b.log" "$PUBLISH_STAGE/posterior_b.log"

DRAGON_LOG_HASH=$(hash_of "$CASE_DIR/dragon.log")
POSTERIOR_HASH=$(hash_of "$CASE_DIR/posterior_a.log")
{
  printf '%s\n' 'SPOR64 PHASE-A9b-B2y ONE-REAL-RETURNED-CLOSE PASS'
  printf '%s\n' 'CLASSIFICATION=ONE-REAL-SUPPLIED-RETURNED-TO-CLOSED-AXIAL-HALF-STEP'
  printf '%s\n' 'DRAGON-EXECUTIONS=1 SPOTCLOSE-CALLS=1 ASM=1 FLU=1 RETRIES=0 PICARD-LOOPS=0'
  printf '%s\n' 'SPOR64V=1 SPOSTATE=1 SPOLEAK=1 SPOR64X=1 CLOSED-PAIRS=1'
  printf '%s\n' "FLU-STRICT-PASS IEXTF=$IEXTF/$MAXOUT ITERF=$ITERF/$MAXINR STATE=$INNER_STATE IGDEB=$IGDEB NGRP=$NGRP"
  printf '%s\n' "RETURNED-SHA256=$RETURNED_BEFORE BYTES=$EXPECTED_RETURNED_BYTES"
  printf '%s\n' "AX-CLOSED-SHA256=$AX_HASH BYTES=$AX_BYTES"
  printf '%s\n' "ARCH-CLOSED-SHA256=$ARCH_HASH BYTES=$ARCH_BYTES"
  printf '%s\n' "DRAGON-SHA256=$DRAGON_HASH DECK-SHA256=$DECK_HASH"
  printf '%s\n' "DRAGON-LOG-SHA256=$DRAGON_LOG_HASH"
  printf '%s\n' "POSTERIOR-LOG-SHA256=$POSTERIOR_HASH REPORTS-IDENTICAL=YES"
  printf '%s\n' 'ATOMIC-PUBLISH=RENAMEATX_NP-RENAME_EXCL TARGET=validation/artifacts/real64-phase-a9b-b2y'
  printf '%s\n' "DURABLE-ATTEMPT-SENTINEL=$ATTEMPT_ID RETRY-AFTER-ANY-ATTEMPT=DISABLED"
  printf '%s\n' 'EMPIRICAL-COEFFICIENTS-ADDED=0 RELAXATION=0 DAMPING=0 CLIPPING=0 FITTING=0'
  printf '%s\n' 'B2v-SAME-PROCESS=NOT-CLAIMED OUTER-PICARD-CONVERGENCE=NOT-EVALUATED'
  printf '%s\n' 'INDEPENDENT-AXIAL-RESIDUAL/GLOBAL-BALANCE/RANK-ADEQUACY=NOT-EVALUATED'
  printf '%s\n' \
    "RECEIPT=$RECEIPT_STATE PARENT=B2z CLOSE-CONTRACT-LINEAGE=B2x HISTORICAL-CONTENT-REFERENCE=B2v"
} >"$PUBLISH_STAGE/runtime_result.txt"

(
  cd "$PUBLISH_STAGE"
  shasum -a 256 ax_closed.xsm archive_closed.xsm dragon.log posterior_a.log \
    posterior_b.log runtime_result.txt >artifact_manifest.sha256
  shasum -a 256 -c artifact_manifest.sha256 >/dev/null
)
for file in ax_closed.xsm archive_closed.xsm dragon.log posterior_a.log \
  posterior_b.log runtime_result.txt artifact_manifest.sha256
do
  [ -f "$PUBLISH_STAGE/$file" ] && [ ! -L "$PUBLISH_STAGE/$file" ] || \
    fail "staged evidence file differs: $file"
  chmod 444 "$PUBLISH_STAGE/$file"
done
[ "$(find "$PUBLISH_STAGE" -mindepth 1 -maxdepth 1 | wc -l | tr -d ' ')" -eq 7 ] || \
  fail "publication stage inventory differs"
require_hash "$PUBLISH_STAGE/ax_closed.xsm" "$AX_HASH"
require_hash "$PUBLISH_STAGE/archive_closed.xsm" "$ARCH_HASH"
[ "$(stat -f '%z' "$PUBLISH_STAGE/ax_closed.xsm")" -eq "$AX_BYTES" ] || \
  fail "staged AX_CLOSED byte count differs"
[ "$(stat -f '%z' "$PUBLISH_STAGE/archive_closed.xsm")" -eq "$ARCH_BYTES" ] || \
  fail "staged ARCH_CLOSED byte count differs"

if ! python3 "$PUBLISHER" "$PUBLISH_STAGE" "$ARTIFACT_DIR"; then
  if [ -d "$ARTIFACT_DIR" ] && [ ! -L "$ARTIFACT_DIR" ] && \
     [ "$(stat -f '%d:%i' "$ARTIFACT_DIR")" = "$PUBLISH_STAGE_ID" ]; then
    FINAL_OWNED_ID=$PUBLISH_STAGE_ID
  fi
  fail "INVALID-ARTIFACT-PUBLICATION NO-RETRY"
fi
FINAL_OWNED_ID=$(stat -f '%d:%i' "$ARTIFACT_DIR")
[ "$FINAL_OWNED_ID" = "$PUBLISH_STAGE_ID" ] || \
  fail "published directory identity differs"
[ "$(find "$ARTIFACT_DIR" -mindepth 1 -maxdepth 1 | wc -l | tr -d ' ')" -eq 7 ] || \
  fail "published artifact inventory differs"
(
  cd "$ARTIFACT_DIR"
  shasum -a 256 -c artifact_manifest.sha256 >/dev/null
)
cmp "$CASE_DIR/ax_closed.xsm" "$ARTIFACT_DIR/ax_closed.xsm" || \
  fail "published AX_CLOSED differs"
cmp "$CASE_DIR/archive_closed.xsm" "$ARTIFACT_DIR/archive_closed.xsm" || \
  fail "published ARCH_CLOSED differs"
cmp "$CASE_DIR/dragon.log" "$ARTIFACT_DIR/dragon.log" || \
  fail "published Dragon log differs"
cmp "$CASE_DIR/posterior_a.log" "$ARTIFACT_DIR/posterior_a.log" || \
  fail "published posterior differs"
require_hash "$ARTIFACT_DIR/ax_closed.xsm" "$AX_HASH"
require_hash "$ARTIFACT_DIR/archive_closed.xsm" "$ARCH_HASH"

rmdir "$LOCK_DIR"
LOCK_ID=
FINAL_OWNED_ID=
PUBLISH_STAGE_ID=
sed -n '1,80p' "$ARTIFACT_DIR/runtime_result.txt"
printf '%s\n' "ARTIFACT=$ARTIFACT_DIR"
