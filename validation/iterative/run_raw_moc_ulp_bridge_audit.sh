#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
DIRNAME=$(uname -sm | sed 's/[ ]/_/')
FC=${FC:-gfortran}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/lib/$DIRNAME/modules"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/lib/$DIRNAME/libGanlib.a"}
INPUT="$ROOT/validation/artifacts/raw-moc-capture"
ARTIFACT="$ROOT/validation/artifacts/raw-moc-ulp-bridge"
ITER="$ROOT/validation/iterative"
READER="$ITER/check_raw_moc_ulp_bridge_xsm.f90"
LOG_CHECKER="$ITER/check_raw_moc_ulp_bridge_log.py"
FIXTURE_TEST="$ITER/run_raw_moc_ulp_bridge_checker_test.sh"
CONTRACT="$ITER/check_raw_moc_ulp_bridge_contract.py"
IMPLEMENTATION="$ITER/raw_moc_ulp_bridge_implementation.sha256"
PARENT_CHECKER="$ITER/check_raw_moc_capture_result.py"
WORK=$(mktemp -d /tmp/spot-ulp-run.XXXXXX)
PUBLISH=
LOCK=
LOCK_OWNED=0
cleanup()
{
  rm -rf "$WORK"
  if test -n "$PUBLISH" && test -e "$PUBLISH"
  then
    rm -rf "$PUBLISH"
  fi
  if test "$LOCK_OWNED" -eq 1 && test -d "$LOCK"
  then
    rmdir "$LOCK" 2>/dev/null || true
  fi
}
trap cleanup EXIT HUP INT TERM

IMPLEMENTATION_FILES="validation/iterative/raw_moc_ulp_bridge_protocol.json
validation/iterative/check_raw_moc_ulp_bridge_xsm.f90
validation/iterative/make_raw_moc_ulp_bridge_fixture.f90
validation/iterative/check_raw_moc_ulp_bridge_log.py
validation/iterative/run_raw_moc_ulp_bridge_checker_test.sh
validation/iterative/run_raw_moc_ulp_bridge_audit.sh
validation/iterative/check_raw_moc_ulp_bridge_contract.py
validation/iterative/raw_moc_ulp_bridge_implementation.sha256"

for path in "$GANLIB_MOD/ganlib.mod" "$GANLIB_LIB" "$READER" \
  "$LOG_CHECKER" "$FIXTURE_TEST" "$CONTRACT" "$IMPLEMENTATION" \
  "$PARENT_CHECKER" "$INPUT/artifact_manifest.sha256" \
  "$INPUT/check_capture"
do
  test -f "$path"
  test ! -L "$path"
done
test -d "$INPUT"
test ! -L "$INPUT"

for relative in $IMPLEMENTATION_FILES
do
  git -C "$ROOT" ls-files --error-unmatch "$relative" >/dev/null
  git -C "$ROOT" show "HEAD:$relative" >"$WORK/head-file"
  cmp "$WORK/head-file" "$ROOT/$relative"
done
test -z "$(git -C "$ROOT" status --porcelain --untracked-files=all -- \
  $IMPLEMENTATION_FILES)"

INPUT_FILES="common/restart_track.xsm
common/restart_system.xsm
check_capture
native/pre.xsm
native/frozen.xsm
native/off.xsm
native/on.xsm
native/check_a.log
stationary/pre.xsm
stationary/frozen.xsm
stationary/off.xsm
stationary/on.xsm
stationary/check_a.log"
seen_inodes=
for relative in $INPUT_FILES
do
  path="$INPUT/$relative"
  test -f "$path"
  test ! -L "$path"
  inode=$(stat -f '%d:%i' "$path" 2>/dev/null || stat -c '%d:%i' "$path")
  case " $seen_inodes " in
    *" $inode "*)
      echo "RAW-MOC-ULP RUN FAIL: aliased input $relative" >&2
      exit 1
      ;;
  esac
  seen_inodes="$seen_inodes $inode"
done

(
  cd "$ROOT"
  shasum -a 256 -c "$IMPLEMENTATION"
  python3 "$CONTRACT"
  python3 "$PARENT_CHECKER"
) >"$WORK/preflight.log"

"$FIXTURE_TEST" >"$WORK/fixture_test.log"

FC_FLAGS="-std=f2008 -O0 -Wall -Wextra -Werror
  -Wno-compare-reals -fcheck=all -ffp-contract=off
  -fno-fast-math -ffpe-summary=none"
"$FC" $FC_FLAGS -I "$GANLIB_MOD" -c "$READER" \
  -o "$WORK/reader.o"
nm -u "$WORK/reader.o" >"$WORK/reader.object.nm"
if rg -i \
  'LCMPUT|LCMPTC|LCMPPD|LCMDID|LCMDIL|LCMLID|LCMLIL|LCMDEL|LCMEQU' \
  "$WORK/reader.object.nm" >/dev/null
then
  echo "RAW-MOC-ULP RUN FAIL: reader object references LCM mutation" >&2
  exit 1
fi
if rg -i \
  'SPOMOC|DOORFV|FLU2DR|FLU2AC|FLUBAL|MCCGF|MCGFLX|MCGMRE|SPOT1P' \
  "$WORK/reader.object.nm" >/dev/null
then
  echo "RAW-MOC-ULP RUN FAIL: reader object references solver symbols" >&2
  exit 1
fi
rg -i 'lcmop' "$WORK/reader.object.nm" >/dev/null

"$FC" "$WORK/reader.o" "$GANLIB_LIB" -lstdc++ \
  -o "$WORK/check_raw_moc_ulp_bridge_xsm"
{
  command -v "$FC"
  "$FC" --version
  uname -a
} >"$WORK/toolchain.txt"
shasum -a 256 "$GANLIB_LIB" "$GANLIB_MOD/ganlib.mod" \
  >"$WORK/dependency_hashes.sha256"
nm "$WORK/check_raw_moc_ulp_bridge_xsm" >"$WORK/reader.nm"
if rg -i \
  'SPOMOC|DOORFV|FLU2DR|FLU2AC|FLUBAL|MCCGF|MCGFLX|MCGMRE|SPOT1P' \
  "$WORK/reader.nm" >/dev/null
then
  echo "RAW-MOC-ULP RUN FAIL: reader binary links solver symbols" >&2
  exit 1
fi
rg -i 'lcmop' "$WORK/reader.nm" >/dev/null

"$WORK/check_raw_moc_ulp_bridge_xsm" SELFTEST \
  >"$WORK/selftest_a.log" 2>"$WORK/selftest_a.err"
"$WORK/check_raw_moc_ulp_bridge_xsm" SELFTEST \
  >"$WORK/selftest_b.log" 2>"$WORK/selftest_b.err"
test ! -s "$WORK/selftest_a.err"
test ! -s "$WORK/selftest_b.err"
cmp "$WORK/selftest_a.log" "$WORK/selftest_b.log"

(
  cd "$INPUT"
  shasum -a 256 $INPUT_FILES >"$WORK/inputs_before.sha256"
  ./check_capture common/restart_track.xsm common/restart_system.xsm \
    native/pre.xsm native/frozen.xsm native/off.xsm native/on.xsm 1 \
    >"$WORK/parent_native.log" 2>"$WORK/parent_native.err"
  ./check_capture common/restart_track.xsm common/restart_system.xsm \
    stationary/pre.xsm stationary/frozen.xsm stationary/off.xsm \
    stationary/on.xsm 2 \
    >"$WORK/parent_stationary.log" 2>"$WORK/parent_stationary.err"
  "$WORK/check_raw_moc_ulp_bridge_xsm" common/restart_track.xsm \
    native/pre.xsm native/off.xsm native/on.xsm 1 \
    >"$WORK/native_a.log" 2>"$WORK/native_a.err"
  "$WORK/check_raw_moc_ulp_bridge_xsm" common/restart_track.xsm \
    native/pre.xsm native/off.xsm native/on.xsm 1 \
    >"$WORK/native_b.log" 2>"$WORK/native_b.err"
  "$WORK/check_raw_moc_ulp_bridge_xsm" common/restart_track.xsm \
    stationary/pre.xsm stationary/off.xsm stationary/on.xsm 2 \
    >"$WORK/stationary_a.log" 2>"$WORK/stationary_a.err"
  "$WORK/check_raw_moc_ulp_bridge_xsm" common/restart_track.xsm \
    stationary/pre.xsm stationary/off.xsm stationary/on.xsm 2 \
    >"$WORK/stationary_b.log" 2>"$WORK/stationary_b.err"
  shasum -a 256 -c "$WORK/inputs_before.sha256" \
    >"$WORK/inputs_after.log"
)

for path in "$WORK"/parent_*.err "$WORK"/native_*.err \
  "$WORK"/stationary_*.err
do
  test ! -s "$path"
done
cmp "$INPUT/native/check_a.log" "$WORK/parent_native.log"
cmp "$INPUT/stationary/check_a.log" "$WORK/parent_stationary.log"
cmp "$WORK/native_a.log" "$WORK/native_b.log"
cmp "$WORK/stationary_a.log" "$WORK/stationary_b.log"

cat "$WORK/native_a.log" "$WORK/stationary_a.log" >"$WORK/full.log"
grep -v ' LEDGER ' "$WORK/full.log" >"$WORK/compact.log"
python3 "$LOG_CHECKER" "$WORK/full.log" >"$WORK/checker_a.log"
python3 "$LOG_CHECKER" "$WORK/full.log" >"$WORK/checker_b.log"
cmp "$WORK/checker_a.log" "$WORK/checker_b.log"
grep '^RAW-MOC-ULP LOG CHECK PASS: ARMS=NATIVE,STATIONARY;' \
  "$WORK/checker_a.log" >/dev/null
test "$(grep -c ' RAW-BRIDGE LEDGER ' "$WORK/full.log")" -eq 5920
test "$(grep -c ' PRODUCTION-STEP LEDGER ' "$WORK/full.log")" -eq 5920
test "$(grep -c ' COMPLETE$' "$WORK/full.log")" -eq 2

(
  cd "$ROOT"
  shasum -a 256 -c "$IMPLEMENTATION"
  python3 "$CONTRACT"
  python3 "$PARENT_CHECKER"
) >"$WORK/postflight.log"

mkdir "$WORK/payload"
mkdir -p "$WORK/payload/implementation/validation/iterative"
cp "$WORK/check_raw_moc_ulp_bridge_xsm" \
  "$WORK/payload/check_raw_moc_ulp_bridge_xsm"
for name in reader.object.nm reader.nm selftest_a.log selftest_b.log \
  native_a.log native_b.log stationary_a.log stationary_b.log \
  parent_native.log parent_stationary.log full.log compact.log \
  checker_a.log checker_b.log inputs_before.sha256 inputs_after.log \
  preflight.log postflight.log fixture_test.log toolchain.txt \
  dependency_hashes.sha256
do
  cp "$WORK/$name" "$WORK/payload/$name"
done
cp "$IMPLEMENTATION" "$WORK/payload/implementation.sha256"
cp "$ITER/raw_moc_ulp_bridge_protocol.json" "$WORK/payload/protocol.json"
for relative in $IMPLEMENTATION_FILES
do
  case "$relative" in
    *raw_moc_ulp_bridge_implementation.sha256)
      continue
      ;;
  esac
  cp "$ROOT/$relative" "$WORK/payload/implementation/$relative"
done
git -C "$ROOT" rev-parse HEAD >"$WORK/payload/run_commit.txt"
(
  cd "$WORK/payload"
  shasum -a 256 check_raw_moc_ulp_bridge_xsm checker_a.log \
    checker_b.log compact.log fixture_test.log full.log \
    dependency_hashes.sha256 \
    implementation.sha256 inputs_after.log inputs_before.sha256 \
    implementation/validation/iterative/check_raw_moc_ulp_bridge_contract.py \
    implementation/validation/iterative/check_raw_moc_ulp_bridge_log.py \
    implementation/validation/iterative/check_raw_moc_ulp_bridge_xsm.f90 \
    implementation/validation/iterative/make_raw_moc_ulp_bridge_fixture.f90 \
    implementation/validation/iterative/raw_moc_ulp_bridge_protocol.json \
    implementation/validation/iterative/run_raw_moc_ulp_bridge_audit.sh \
    implementation/validation/iterative/run_raw_moc_ulp_bridge_checker_test.sh \
    native_a.log native_b.log parent_native.log parent_stationary.log \
    postflight.log preflight.log protocol.json reader.nm \
    reader.object.nm run_commit.txt selftest_a.log selftest_b.log \
    stationary_a.log stationary_b.log toolchain.txt \
    >artifact_manifest.sha256
  shasum -a 256 -c artifact_manifest.sha256 >/dev/null
)

verify_package()
{
  package=$1
  test -d "$package"
  test ! -L "$package"
  test -f "$package/artifact_manifest.sha256"
  test ! -L "$package/artifact_manifest.sha256"
  if find "$package" -type l | grep . >/dev/null
  then
    echo "RAW-MOC-ULP RUN FAIL: artifact contains a symlink" >&2
    exit 1
  fi
  expected_count=$((1 + $(wc -l <"$package/artifact_manifest.sha256")))
  actual_count=$(find "$package" -type f | wc -l | tr -d ' ')
  test "$actual_count" -eq "$expected_count"
  (
    cd "$package"
    shasum -a 256 -c artifact_manifest.sha256
    (
      cd implementation
      shasum -a 256 -c ../implementation.sha256
    )
  ) >/dev/null
}

verify_package "$WORK/payload"

LOCK="$ARTIFACT.lock"
if ! mkdir "$LOCK"
then
  echo "RAW-MOC-ULP RUN FAIL: artifact publication lock is busy" >&2
  exit 1
fi
LOCK_OWNED=1

if test -e "$ARTIFACT"
then
  verify_package "$ARTIFACT"
  cmp "$WORK/payload/artifact_manifest.sha256" \
    "$ARTIFACT/artifact_manifest.sha256"
  while read -r digest relative
  do
    test -n "$digest"
    test -f "$ARTIFACT/$relative"
    test ! -L "$ARTIFACT/$relative"
    cmp "$WORK/payload/$relative" "$ARTIFACT/$relative"
  done <"$WORK/payload/artifact_manifest.sha256"
else
  PUBLISH="$ARTIFACT.new.$$"
  test ! -e "$PUBLISH"
  mkdir -p "$(dirname "$ARTIFACT")"
  cp -R "$WORK/payload" "$PUBLISH"
  verify_package "$PUBLISH"
  test ! -e "$ARTIFACT"
  mv "$PUBLISH" "$ARTIFACT"
  PUBLISH=
fi
verify_package "$ARTIFACT"
rmdir "$LOCK"
LOCK_OWNED=0

cat "$WORK/compact.log"
