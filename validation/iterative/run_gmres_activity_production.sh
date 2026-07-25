#!/bin/sh
# Frozen, fail-closed bounded GMRES-activity production runner.
#
# With RUN_GMRES_ACTIVITY absent this performs only static, synthetic and
# compile/link preflight.  Exactly RUN_GMRES_ACTIVITY=1 authorizes the three
# frozen one-map Dragon processes; no other value is accepted.

set -eu
umask 077
export LC_ALL=C
PATH=/opt/homebrew/bin:/usr/bin:/bin
export PATH
FC_WAS_SET=${FC+x}
DRAGON_BIN_WAS_SET=${DRAGON_BIN+x}
ARTIFACT_WAS_SET=${ARTIFACT+x}

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd -P)
ITER="$ROOT/validation/iterative"
BUILD="$ROOT/validation/artifacts/gmres-activity-build"
CLEAN="$BUILD/source"
ARTIFACT_PARENT="$ROOT/validation/artifacts"
ARTIFACT="$ARTIFACT_PARENT/gmres-activity-census"
LOCK="$ARTIFACT_PARENT/.gmres-activity-census.lock"

PROTOCOL="$ITER/gmres_activity_run_protocol.json"
RUN_PROTOCOL_CHECKER="$ITER/check_gmres_activity_run_protocol.py"
REFERENCE="$ITER/gmres_activity_run_reference.sha256"
RUN_IMPLEMENTATION="$ITER/gmres_activity_run_implementation.sha256"
METHOD_IMPLEMENTATION="$ITER/gmres_activity_implementation.sha256"
METHOD_CHECKER="$ITER/check_gmres_activity_implementation.py"
METHOD_PREFLIGHT="$ITER/run_gmres_activity_preflight.sh"
DECK_TEMPLATE="$ITER/gmres_activity_probe.x2m.in"
BOUNDED_RUNNER="$ITER/run_bounded_gmres_activity.py"
BOUNDED_TESTS="$ITER/test_bounded_gmres_activity.py"
LOG_CHECKER="$ITER/check_gmres_activity_run_logs.py"
LOG_TESTS="$ITER/test_gmres_activity_run_logs.py"
LEDGER_SOURCE="$ITER/check_gmres_activity_xsm.f90"
PAIR_SOURCE="$ITER/check_gmres_activity_pair_xsm.f90"
ARTIFACT_CHECKER="$ITER/check_gmres_activity_artifact.py"
ARTIFACT_TESTS="$ITER/test_gmres_activity_artifact.py"
NORMALIZER="$ITER/normalize_gmres_activity_log.py"

DRAGON="$CLEAN/bin/Darwin_arm64/Dragon"
GANLIB_MOD="$CLEAN/Ganlib/lib/Darwin_arm64/modules"
GANLIB_LIB="$CLEAN/Ganlib/lib/Darwin_arm64/libGanlib.a"
UTILIB_LIB="$CLEAN/Utilib/lib/Darwin_arm64/libUtilib.a"
TRIVAC_LIB="$CLEAN/Trivac/lib/Darwin_arm64/libTrivac.a"
DRAGON_LIB="$CLEAN/lib/Darwin_arm64/libDragon.a"
FC=/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15
PYTHON=/Library/Developer/CommandLineTools/usr/bin/python3
PYTHON_FRAMEWORK_ENTRY=/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3
PYTHON_REAL=/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9
METHOD_PATH=/Library/Developer/CommandLineTools/usr/bin:/usr/bin:/bin

EXPECTED_RUN_IMPLEMENTATION_PATHS='validation/iterative/build_gmres_activity_overlay.sh
validation/iterative/check_gmres_activity_artifact.py
validation/iterative/check_gmres_activity_implementation.py
validation/iterative/check_gmres_activity_pair_xsm.f90
validation/iterative/check_gmres_activity_run_logs.py
validation/iterative/check_gmres_activity_run_protocol.py
validation/iterative/check_gmres_activity_xsm.f90
validation/iterative/gmres_activity_implementation.sha256
validation/iterative/gmres_activity_probe.x2m.in
validation/iterative/gmres_activity_run_protocol.json
validation/iterative/gmres_activity_run_reference.sha256
validation/iterative/normalize_gmres_activity_log.py
validation/iterative/run_bounded_gmres_activity.py
validation/iterative/run_gmres_activity_preflight.sh
validation/iterative/run_gmres_activity_production.sh
validation/iterative/test_bounded_gmres_activity.py
validation/iterative/test_gmres_activity_artifact.py
validation/iterative/test_gmres_activity_run_logs.py'

PRE="$ROOT/validation/artifacts/raw-moc-capture/stationary/pre.xsm"
LEGACY_OFF_XSM="$ROOT/validation/artifacts/raw-moc-capture/stationary/off.xsm"
LEGACY_ON_XSM="$ROOT/validation/artifacts/raw-moc-capture/stationary/on.xsm"
LEGACY_OFF_LOG="$ROOT/validation/artifacts/raw-moc-capture/stationary_off/probe.log"
LEGACY_ON_LOG="$ROOT/validation/artifacts/raw-moc-capture/stationary_on/probe.log"
LEGACY_OFF_DECK="$ROOT/validation/artifacts/raw-moc-capture/stationary_off/probe.x2m"
LEGACY_ON_DECK="$ROOT/validation/artifacts/raw-moc-capture/stationary_on/probe.x2m"
MACRO0="$ROOT/validation/artifacts/raw-moc-capture/common/restart_macro0.xsm"
SOURCE="$ROOT/validation/artifacts/raw-moc-capture/common/restart_source.xsm"
SYSTEM="$ROOT/validation/artifacts/raw-moc-capture/common/restart_system.xsm"
TRACK="$ROOT/validation/artifacts/raw-moc-capture/common/restart_track.xsm"
TRACK_BINARY="$ROOT/validation/artifacts/raw-moc-capture/common/initial_radial_track.bin"

EXPECTED_REFERENCE_SHA256=42d21c49139ec93c272fba4a9dfb1ec304acd583abf31e6939db90548fdd01db
PARENT_COMMIT=4d7abb23ac7975d4146beaa3b0049e36cdad8776
SOURCE_IMPLEMENTATION_COMMIT=5816c8aad4fbb43542514d5bd571ebccecdb6d72
METHOD_PROTOCOL_SHA256=7fedbdf3fd5ae26a709dc1785d9d2bebf4648599d4aa1ccd999c6fbc93c9cac1
RUN_PROTOCOL_SHA256=9d22c63b2678e78867fd4bea0b801388ebc943d81b1f5eaa3a80fda052c9e23f
METHOD_IMPLEMENTATION_SHA256=19098f8f4bc4c75dc94c829472b44d4553de6992b03dc965b9f726b2018ee736
DRAGON_SHA256=df83931c4ba0e5f5a7dfa534438967536a71d82e62e77ba4fc6bcb2e8f19f84a

fail()
{
  echo "GMRES-ACTIVITY PRODUCTION FAIL: $*" >&2
  exit 2
}

hash_of()
{
  shasum -a 256 "$1" | awk '{print $1}'
}

require_regular()
{
  test -f "$1" && test ! -L "$1" ||
    fail "invalid regular file: $2"
}

expected_hash()
{
  label=$1
  value=$(awk -v wanted="$label" '
    $2 == wanted { count += 1; digest = $1 }
    END {
      if (count == 1) print digest
      else exit 1
    }
  ' "$REFERENCE") || fail "missing or duplicate reference label: $label"
  printf '%s\n' "$value"
}

require_hash()
{
  label=$1
  path=$2
  require_regular "$path" "$label"
  expected=$(expected_hash "$label")
  actual=$(hash_of "$path")
  test "$actual" = "$expected" || fail "SHA256 differs: $label"
}

require_frozen_python()
{
  test -L "$PYTHON" ||
    fail "frozen Python command-line-tools entry is not a symlink"
  test "$(readlink "$PYTHON")" = \
    "../../Library/Frameworks/Python3.framework/Versions/3.9/bin/python3" ||
    fail "frozen Python outer symlink target differs"
  test -L "$PYTHON_FRAMEWORK_ENTRY" ||
    fail "frozen Python framework entry is not a symlink"
  test "$(readlink "$PYTHON_FRAMEWORK_ENTRY")" = python3.9 ||
    fail "frozen Python inner symlink target differs"
  require_regular "$PYTHON_REAL" "toolchain/python3 resolved executable"
  expected=$(expected_hash toolchain/python3)
  test "$(hash_of "$PYTHON")" = "$expected" &&
    test "$(hash_of "$PYTHON_REAL")" = "$expected" ||
    fail "SHA256 differs: toolchain/python3"
}

inode_of()
{
  stat -f '%d:%i' "$1"
}

require_distinct_inodes()
{
  seen=
  for path in "$@"
  do
    require_regular "$path" "distinct-inode input"
    inode=$(inode_of "$path")
    case " $seen " in
      *" $inode "*) fail "input files alias one inode: $path" ;;
    esac
    seen="$seen $inode"
  done
}

copy_exact()
{
  source_path=$1
  target_path=$2
  cp "$source_path" "$target_path"
  cmp "$source_path" "$target_path" ||
    fail "copy differs: $target_path"
  test ! -L "$target_path" || fail "copy became a symlink: $target_path"
}

render_deck()
{
  mode=$1
  target=$2
  if test "$mode" = OFF
  then
    control=
  elif test "$mode" = ON
  then
    control="MOCA 2 GMRA"
  else
    fail "invalid deck mode: $mode"
  fi
  sed -e 's/@ARM@/STATIONARY/g' \
    -e "s/@MODE@/$mode/g" \
    -e "s/@AUDIT_CONTROL@/$control/g" \
    "$DECK_TEMPLATE" >"$target"
  if grep '@ARM@\|@MODE@\|@AUDIT_CONTROL@' "$target" >/dev/null
  then
    fail "unresolved deck placeholder"
  fi
  if test "$mode" = OFF
  then
    cmp "$target" "$LEGACY_OFF_DECK" ||
      fail "OFF deck differs from frozen legacy deck"
  else
    sed 's/ GMRA//' "$target" >"$target.without-gmra"
    cmp "$target.without-gmra" "$LEGACY_ON_DECK" ||
      fail "ON deck differs outside the GMRA token"
    rm -f "$target.without-gmra"
    test "$(grep -c ' MOCA 2 GMRA ;' "$target")" -eq 1 ||
      fail "ON deck GMRA census differs"
  fi
}

write_input_receipt()
{
  target=$1
  (
    cd "$ROOT"
    shasum -a 256 \
      validation/artifacts/raw-moc-capture/common/initial_radial_track.bin \
      validation/artifacts/raw-moc-capture/common/restart_macro0.xsm \
      validation/artifacts/raw-moc-capture/common/restart_source.xsm \
      validation/artifacts/raw-moc-capture/common/restart_system.xsm \
      validation/artifacts/raw-moc-capture/common/restart_track.xsm \
      validation/artifacts/raw-moc-capture/stationary/off.xsm \
      validation/artifacts/raw-moc-capture/stationary/on.xsm \
      validation/artifacts/raw-moc-capture/stationary/pre.xsm \
      validation/artifacts/raw-moc-capture/stationary_off/probe.log \
      validation/artifacts/raw-moc-capture/stationary_on/probe.log
  ) >"$target"
}

verify_run_implementation()
{
  actual_paths=$(awk '
    NF != 2 ||
    length($1) != 64 ||
    $1 !~ /^[0-9a-f]+$/ ||
    $0 != $1 "  " $2 ||
    seen[$2]++ ||
    (NR > 1 && $2 <= previous) {
      bad = 1
    }
    {
      previous = $2
      print $2
    }
    END {
      if (NR != 18 || bad) exit 1
    }
  ' "$RUN_IMPLEMENTATION") ||
    fail "run implementation manifest grammar or ordering differs"
  test "$actual_paths" = "$EXPECTED_RUN_IMPLEMENTATION_PATHS" ||
    fail "run implementation path census differs"
  (
    cd "$ROOT"
    shasum -a 256 -c \
      validation/iterative/gmres_activity_run_implementation.sha256
  ) >/dev/null || fail "run implementation manifest replay failed"
}

verify_tracked_head()
{
  paths=$(awk '{print $2}' "$RUN_IMPLEMENTATION")
  paths="$paths
validation/iterative/gmres_activity_run_implementation.sha256"
  for relative in $paths
  do
    git -C "$ROOT" ls-files --error-unmatch "$relative" >/dev/null 2>&1 ||
      fail "run implementation path is untracked: $relative"
    git -C "$ROOT" diff --quiet -- "$relative" ||
      fail "run implementation path has an unstaged change: $relative"
    git -C "$ROOT" diff --cached --quiet -- "$relative" ||
      fail "run implementation path has a staged change: $relative"
    head_hash=$(git -C "$ROOT" show "HEAD:$relative" | shasum -a 256 |
      awk '{print $1}')
    test "$head_hash" = "$(hash_of "$ROOT/$relative")" ||
      fail "run implementation path differs from HEAD: $relative"
  done
}

freeze_run_head()
{
  RUN_COMMIT=$(git -C "$ROOT" rev-parse HEAD)
  printf '%s\n' "$RUN_COMMIT" | grep -Eq '^[0-9a-f]{40}$' ||
    fail "run commit grammar differs"
  verify_tracked_head
  test "$(git -C "$ROOT" rev-parse HEAD)" = "$RUN_COMMIT" ||
    fail "Git HEAD changed while freezing the bounded run"
}

verify_frozen_run_head()
{
  test "$(git -C "$ROOT" rev-parse HEAD)" = "$RUN_COMMIT" ||
    fail "Git HEAD changed during the bounded run"
  verify_tracked_head
  test "$(git -C "$ROOT" rev-parse HEAD)" = "$RUN_COMMIT" ||
    fail "Git HEAD changed during tracked-byte replay"
}

verify_reference_and_build()
{
  require_regular "$REFERENCE" "run reference"
  test "$(hash_of "$REFERENCE")" = "$EXPECTED_REFERENCE_SHA256" ||
    fail "run reference SHA256 differs"
  awk '
    NF != 2 || $1 !~ /^[0-9a-f]{64}$/ || seen[$2]++ { exit 1 }
    END { if (NR != 47) exit 1 }
  ' "$REFERENCE" || fail "run reference grammar or census differs"

  require_hash protocol/gmres_activity_run_protocol.json "$PROTOCOL"
  require_hash protocol/gmres_activity_protocol.json \
    "$ITER/gmres_activity_protocol.json"
  require_hash protocol/gmres_activity_implementation.sha256 \
    "$METHOD_IMPLEMENTATION"
  require_hash construction/gmres_activity_overlay_manifest.json \
    "$ITER/gmres_activity_overlay_manifest.json"
  require_hash construction/gmres_activity_overlay.patch \
    "$ITER/gmres_activity_overlay.patch"

  require_hash toolchain/gfortran-15 "$FC"
  require_hash toolchain/make /Library/Developer/CommandLineTools/usr/bin/make
  require_hash toolchain/ar /Library/Developer/CommandLineTools/usr/bin/ar
  require_hash toolchain/as /Library/Developer/CommandLineTools/usr/bin/as
  require_hash toolchain/cpp /Library/Developer/CommandLineTools/usr/bin/cpp
  require_hash toolchain/gcc /Library/Developer/CommandLineTools/usr/bin/gcc
  require_hash toolchain/ld /Library/Developer/CommandLineTools/usr/bin/ld
  require_frozen_python
  require_hash runtime/libgfortran.5.dylib \
    /opt/homebrew/opt/gcc/lib/gcc/current/libgfortran.5.dylib
  require_hash runtime/libquadmath.0.dylib \
    /opt/homebrew/opt/gcc/lib/gcc/current/libquadmath.0.dylib

  require_hash source/src/.dragon_deps.mk "$CLEAN/src/.dragon_deps.mk"
  require_hash source/src/FLU.f "$CLEAN/src/FLU.f"
  require_hash source/src/FLUDRV.f "$CLEAN/src/FLUDRV.f"
  require_hash source/src/FLUGPI.f "$CLEAN/src/FLUGPI.f"
  require_hash source/src/MCGMRE.f "$CLEAN/src/MCGMRE.f"
  require_hash source/src/SPOMGMR.f90 "$CLEAN/src/SPOMGMR.f90"
  require_hash source/src/SPOMOC.f90 "$CLEAN/src/SPOMOC.f90"

  require_hash build/instrumented_source_manifest.sha256 \
    "$BUILD/instrumented_source_manifest.sha256"
  require_hash build/source_identity.tsv "$BUILD/source_identity.tsv"
  require_hash build/build_receipt.tsv "$BUILD/build_receipt.tsv"
  require_hash build/toolchain.sha256 "$BUILD/toolchain.sha256"
  require_hash build/symbol_audit.txt "$BUILD/symbol_audit.txt"
  require_hash build/executable.sha256 "$BUILD/executable.sha256"
  require_hash build/Dragon.nm "$BUILD/Dragon.nm"
  require_hash build/Dragon.otool "$BUILD/Dragon.otool"
  require_hash build/Ganlib/lib/Darwin_arm64/modules/ganlib.mod \
    "$GANLIB_MOD/ganlib.mod"
  require_hash build/Ganlib/lib/Darwin_arm64/libGanlib.a "$GANLIB_LIB"
  require_hash build/Utilib/lib/Darwin_arm64/libUtilib.a "$UTILIB_LIB"
  require_hash build/Trivac/lib/Darwin_arm64/libTrivac.a "$TRIVAC_LIB"
  require_hash build/lib/Darwin_arm64/libDragon.a "$DRAGON_LIB"
  require_hash build/bin/Darwin_arm64/Dragon "$DRAGON"
  test -x "$DRAGON" || fail "frozen Dragon is not executable"

  require_hash input/PRE "$PRE"
  require_hash input/LEGACY_OFF_XSM "$LEGACY_OFF_XSM"
  require_hash input/LEGACY_ON_XSM "$LEGACY_ON_XSM"
  require_hash input/LEGACY_OFF_LOG "$LEGACY_OFF_LOG"
  require_hash input/LEGACY_ON_LOG "$LEGACY_ON_LOG"
  require_hash input/MACRO0 "$MACRO0"
  require_hash input/SOURCE "$SOURCE"
  require_hash input/SYSTEM "$SYSTEM"
  require_hash input/TRACK "$TRACK"
  require_hash input/TRACK_BINARY "$TRACK_BINARY"

  (
    cd "$CLEAN"
    shasum -a 256 -c ../instrumented_source_manifest.sha256
  ) >/dev/null || fail "instrumented source manifest replay failed"
  (
    cd /
    shasum -a 256 -c "$BUILD/toolchain.sha256"
  ) >/dev/null || fail "toolchain manifest replay failed"
}

compile_independent_tools()
{
  mkdir -p "$WORK/tools"
  flags="-std=f2008 -O0 -Wall -Wextra -Werror -Wno-compare-reals
    -fcheck=all -ffp-contract=off -fno-fast-math -ffpe-summary=none"
  "$FC" $flags -I "$GANLIB_MOD" "$LEDGER_SOURCE" \
    "$GANLIB_LIB" "$UTILIB_LIB" -lstdc++ -o "$WORK/tools/check_ledger"
  "$FC" $flags -I "$GANLIB_MOD" "$PAIR_SOURCE" \
    "$GANLIB_LIB" "$UTILIB_LIB" -lstdc++ -o "$WORK/tools/check_pair"

  nm "$WORK/tools/check_ledger" >"$WORK/tools/check_ledger.nm"
  nm "$WORK/tools/check_pair" >"$WORK/tools/check_pair.nm"
  for receipt in "$WORK/tools/check_ledger.nm" "$WORK/tools/check_pair.nm"
  do
    grep -i 'lcmop' "$receipt" >/dev/null ||
      fail "independent tool lacks Ganlib read path"
    if grep -Ei \
      'spomgmr|spomoc|doorfv|mccgf|mcgflx|mcgfl1|mcgmre|___flu_|_flu_' \
      "$receipt" >/dev/null
    then
      fail "independent tool references a forbidden production symbol"
    fi
  done
}

verify_binary_receipts()
{
  (
    cd "$ROOT"
    nm validation/artifacts/gmres-activity-build/source/bin/Darwin_arm64/Dragon
  ) >"$WORK/Dragon.nm"
  cmp "$WORK/Dragon.nm" "$BUILD/Dragon.nm" ||
    fail "Dragon nm receipt differs"
  (
    cd "$ROOT"
    otool -L \
      validation/artifacts/gmres-activity-build/source/bin/Darwin_arm64/Dragon
  ) >"$WORK/Dragon.otool"
  cmp "$WORK/Dragon.otool" "$BUILD/Dragon.otool" ||
    fail "Dragon otool receipt differs"
  strings "$DRAGON" >"$WORK/Dragon.strings"
  grep -F 'SPOT-GMR-AUD' "$WORK/Dragon.strings" >/dev/null ||
    fail "Dragon lacks SPOT-GMR-AUD schema text"
  for symbol in flu_reset parse_gmra require_moca begin mcgmre_enter \
    role block_begin block_end mcgmre_exit finish
  do
    grep -i "spomgmr_$symbol" "$WORK/Dragon.nm" >/dev/null ||
      fail "Dragon lacks SPOMGMR $symbol"
  done
}

verify_case_census()
{
  case_dir=$1
  actual=$(find "$case_dir" -mindepth 1 -maxdepth 1 -print |
    sed 's|.*/||' | sort)
  expected='deck.x2m
initial_radial_track.bin
restart_macro0.xsm
restart_source.xsm
restart_system.xsm
restart_track.xsm
result.xsm
run.log
tmp'
  test "$actual" = "$expected" || fail "case path census differs"
  test -d "$case_dir/tmp" && test ! -L "$case_dir/tmp" ||
    fail "invalid case-local tmp"
  test -z "$(find "$case_dir/tmp" -mindepth 1 -print -quit)" ||
    fail "case-local tmp is not empty after execution"
  for name in deck.x2m initial_radial_track.bin restart_macro0.xsm \
    restart_source.xsm restart_system.xsm restart_track.xsm result.xsm \
    run.log
  do
    require_regular "$case_dir/$name" "case payload"
  done
}

prepare_case()
{
  case_dir=$1
  mode=$2
  mkdir -p "$case_dir/tmp"
  copy_exact "$MACRO0" "$case_dir/restart_macro0.xsm"
  copy_exact "$SOURCE" "$case_dir/restart_source.xsm"
  copy_exact "$SYSTEM" "$case_dir/restart_system.xsm"
  copy_exact "$TRACK" "$case_dir/restart_track.xsm"
  copy_exact "$TRACK_BINARY" "$case_dir/initial_radial_track.bin"
  copy_exact "$PRE" "$case_dir/result.xsm"
  render_deck "$mode" "$case_dir/deck.x2m"
  chmod 400 "$case_dir/deck.x2m" \
    "$case_dir/restart_macro0.xsm" "$case_dir/restart_source.xsm" \
    "$case_dir/restart_system.xsm" "$case_dir/restart_track.xsm" \
    "$case_dir/initial_radial_track.bin"
  chmod 600 "$case_dir/result.xsm"
}

run_case()
{
  case_dir=$1
  "$PYTHON" "$BOUNDED_RUNNER" "$DRAGON" \
    "$case_dir/deck.x2m" "$case_dir/run.log" \
    >"${case_dir}.process.txt"
  test "$(cat "${case_dir}.process.txt")" = \
    "GMRES-ACTIVITY PROCESS PASS" ||
    fail "bounded wrapper receipt differs"
  rm -f "${case_dir}.process.txt"
  verify_case_census "$case_dir"
  cmp "$MACRO0" "$case_dir/restart_macro0.xsm"
  cmp "$SOURCE" "$case_dir/restart_source.xsm"
  cmp "$SYSTEM" "$case_dir/restart_system.xsm"
  cmp "$TRACK" "$case_dir/restart_track.xsm"
  cmp "$TRACK_BINARY" "$case_dir/initial_radial_track.bin"
}

write_result_from_ledger()
{
  ledger=$1
  target=$2
  blocks=$(awk '$1=="GMRES-ACTIVITY" && $2=="RAW" &&
    $3=="STATE" && $4=="17" {print $5}' "$ledger")
  nonzero=$(awk '$1=="GMRES-ACTIVITY" &&
    $2=="NONZERO-K-GROUP-BLOCKS" {print $3}' "$ledger")
  sum_k=$(awk '$1=="GMRES-ACTIVITY" && $2=="SUM-K" {print $3}' "$ledger")
  max_k=$(awk '$1=="GMRES-ACTIVITY" && $2=="MAX-K" {print $3}' "$ledger")
  classification=$(awk '$1=="GMRES-ACTIVITY" &&
    $2=="CLASSIFICATION" {print $3}' "$ledger")
  for value in "$blocks" "$nonzero" "$sum_k" "$max_k"
  do
    case "$value" in
      0|[1-9][0-9]*) ;;
      *) fail "noncanonical integer in independent ledger summary" ;;
    esac
  done
  case "$classification" in
    VALID-GMRES-UPDATE-ACTIVE|VALID-GMRES-UPDATE-INACTIVE) ;;
    *) fail "invalid ledger classification" ;;
  esac
  test "$(awk '$1=="GMRES-ACTIVITY" && $2=="RAW" &&
    $3=="K-HISTOGRAM" {count += 1} END {print count+0}' "$ledger")" -eq 11 ||
    fail "ledger histogram census differs"
  {
    echo "GMRES-ACTIVITY RESULT 1"
    echo "PROCESSES OFF=1 ON=2"
    echo "CORRECTION-BLOCKS $blocks"
    echo "GROUP-BLOCKS $((370 * blocks))"
    awk '$1=="GMRES-ACTIVITY" && $2=="RAW" &&
      $3=="K-HISTOGRAM" {print "K-HISTOGRAM " $4 " " $5}' "$ledger"
    echo "NONZERO-K-GROUP-BLOCKS $nonzero"
    echo "SUM-K $sum_k"
    echo "MAX-K $max_k"
    echo "THRESHOLD NONE"
    echo "CLASSIFICATION $classification"
    echo "COMPLETE"
  } >"$target"
  RESULT_CLASSIFICATION=$classification
}

write_artifact_manifest()
{
  root=$1
  target="$root/artifact_manifest.sha256"
  test ! -e "$target" || fail "artifact manifest already exists"
  (
    cd "$root"
    find . -type f ! -name artifact_manifest.sha256 -print |
      sed 's|^\./||' | sort |
      while IFS= read -r relative
      do
        shasum -a 256 "$relative" |
          awk -v label="$relative" '{print $1 "  " label}'
      done
  ) >"$target"
}

verify_candidate_artifact()
{
  root=$1
  expected=$2
  tag=$3
  "$PYTHON" "$ARTIFACT_CHECKER" "$root" \
    >"$WORK/$tag.out" 2>"$WORK/$tag.err" ||
    fail "artifact checker rejected $tag"
  test ! -s "$WORK/$tag.err" ||
    fail "artifact checker wrote stderr for $tag"
  test "$(cat "$WORK/$tag.out")" = "$expected" ||
    fail "artifact checker classification differs for $tag"
}

if test "${RUN_GMRES_ACTIVITY+x}" = x
then
  test "$RUN_GMRES_ACTIVITY" = 1 ||
    fail "RUN_GMRES_ACTIVITY must be absent or exactly 1"
  RUN=1
else
  RUN=0
fi
test "$FC_WAS_SET" != x || fail "FC override is forbidden"
test "$DRAGON_BIN_WAS_SET" != x || fail "DRAGON_BIN override is forbidden"
test "$ARTIFACT_WAS_SET" != x || fail "ARTIFACT override is forbidden"

WORK=$(mktemp -d "$ARTIFACT_PARENT/.gmres-activity-preflight.XXXXXX")
PUBLISH=
LOCK_HELD=0
FINAL_OWNED=0
FINAL_INODE=
cleanup()
{
  status=$?
  trap - EXIT HUP INT TERM
  if test "$status" -ne 0 && test "$FINAL_OWNED" -eq 1 &&
     test -d "$ARTIFACT" && test ! -L "$ARTIFACT"
  then
    current_inode=$(inode_of "$ARTIFACT" 2>/dev/null || true)
    if test -n "$current_inode" && test "$current_inode" = "$FINAL_INODE"
    then
      rm -rf "$ARTIFACT"
    fi
  fi
  if test -n "$PUBLISH" && test -d "$PUBLISH" && test ! -L "$PUBLISH"
  then
    rm -rf "$PUBLISH"
  fi
  if test -d "$WORK" && test ! -L "$WORK"
  then
    rm -rf "$WORK"
  fi
  if test "$LOCK_HELD" -eq 1 && test -d "$LOCK" && test ! -L "$LOCK"
  then
    rmdir "$LOCK" 2>/dev/null || true
  fi
  exit "$status"
}
trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

for path in "$PROTOCOL" "$RUN_PROTOCOL_CHECKER" "$REFERENCE" \
  "$RUN_IMPLEMENTATION" "$METHOD_IMPLEMENTATION" "$METHOD_CHECKER" \
  "$METHOD_PREFLIGHT" "$DECK_TEMPLATE" "$BOUNDED_RUNNER" "$BOUNDED_TESTS" \
  "$LOG_CHECKER" "$LOG_TESTS" "$LEDGER_SOURCE" "$PAIR_SOURCE" \
  "$ARTIFACT_CHECKER" "$ARTIFACT_TESTS" "$NORMALIZER"
do
  require_regular "$path" "preflight implementation file"
done

verify_reference_and_build
test "$(hash_of "$PROTOCOL")" = "$RUN_PROTOCOL_SHA256" ||
  fail "run protocol constant differs"
test "$(hash_of "$METHOD_IMPLEMENTATION")" = \
  "$METHOD_IMPLEMENTATION_SHA256" ||
  fail "method implementation constant differs"

git -C "$ROOT" diff --quiet "$PARENT_COMMIT" -- src ||
  fail "tracked live src differs from the frozen parent"
test -z "$(git -C "$ROOT" status --porcelain=v1 \
  --untracked-files=all -- src)" ||
  fail "live src has a dirty or untracked path"
git -C "$ROOT" merge-base --is-ancestor \
  "$SOURCE_IMPLEMENTATION_COMMIT" HEAD ||
  fail "source implementation commit is not an ancestor of HEAD"

git -C "$ROOT" archive --format=tar --output="$WORK/parent.tar" \
  "$PARENT_COMMIT"
require_hash construction/parent_git_archive.tar "$WORK/parent.tar"
verify_run_implementation
if test "$RUN" -eq 1
then
  freeze_run_head
fi
verify_binary_receipts

"$PYTHON" "$RUN_PROTOCOL_CHECKER" >"$WORK/run_protocol.log"
"$PYTHON" "$RUN_PROTOCOL_CHECKER" --self-test \
  >"$WORK/run_protocol_self_test.log"
"$PYTHON" "$BOUNDED_TESTS" >"$WORK/bounded_tests.log"
"$PYTHON" "$LOG_TESTS" >"$WORK/log_tests.log"
"$PYTHON" "$ARTIFACT_TESTS" >"$WORK/artifact_tests.log"
env -u RUN_GMRES_ACTIVITY -u FC PATH="$METHOD_PATH" \
  PYTHONDONTWRITEBYTECODE=1 \
  sh "$METHOD_PREFLIGHT" >"$WORK/preflight.log"
"$PYTHON" "$METHOD_CHECKER" >"$WORK/implementation_replay.log"

compile_independent_tools
mkdir -p "$WORK/render"
render_deck OFF "$WORK/render/off.x2m"
render_deck ON "$WORK/render/on_a.x2m"
render_deck ON "$WORK/render/on_b.x2m"
cmp "$WORK/render/on_a.x2m" "$WORK/render/on_b.x2m" ||
  fail "ON deck replay differs"

if test "$RUN" -eq 0
then
  echo "GMRES-ACTIVITY PRODUCTION PREFLIGHT PASS"
  echo "GMRES-ACTIVITY PRODUCTION NOT-RUN; SET RUN_GMRES_ACTIVITY=1"
  exit 0
fi

verify_frozen_run_head
test ! -e "$ARTIFACT" && test ! -L "$ARTIFACT" ||
  fail "artifact path already exists"
mkdir "$LOCK" 2>/dev/null ||
  fail "artifact publication lock is busy"
LOCK_HELD=1

EVIDENCE="$WORK/evidence"
RUNS="$WORK/runs"
mkdir -p "$EVIDENCE/off" "$EVIDENCE/on_a" "$EVIDENCE/on_b" "$RUNS"
write_input_receipt "$WORK/inputs_before.sha256"

prepare_case "$RUNS/off" OFF
prepare_case "$RUNS/on_a" ON
prepare_case "$RUNS/on_b" ON
require_distinct_inodes \
  "$RUNS/off/restart_macro0.xsm" "$RUNS/off/restart_source.xsm" \
  "$RUNS/off/restart_system.xsm" "$RUNS/off/restart_track.xsm" \
  "$RUNS/off/initial_radial_track.bin" "$RUNS/off/result.xsm" \
  "$RUNS/on_a/restart_macro0.xsm" "$RUNS/on_a/restart_source.xsm" \
  "$RUNS/on_a/restart_system.xsm" "$RUNS/on_a/restart_track.xsm" \
  "$RUNS/on_a/initial_radial_track.bin" "$RUNS/on_a/result.xsm" \
  "$RUNS/on_b/restart_macro0.xsm" "$RUNS/on_b/restart_source.xsm" \
  "$RUNS/on_b/restart_system.xsm" "$RUNS/on_b/restart_track.xsm" \
  "$RUNS/on_b/initial_radial_track.bin" "$RUNS/on_b/result.xsm"

run_case "$RUNS/off"
"$PYTHON" "$NORMALIZER" --mode legacy "$LEGACY_OFF_LOG" \
  >"$WORK/legacy_off.normalized.log"
"$PYTHON" "$NORMALIZER" --mode legacy "$RUNS/off/run.log" \
  >"$WORK/actual_off.normalized.log"
cmp "$WORK/legacy_off.normalized.log" "$WORK/actual_off.normalized.log" ||
  fail "fresh OFF log differs from legacy OFF"
cmp "$RUNS/off/result.xsm" "$LEGACY_OFF_XSM" ||
  fail "fresh OFF XSM differs from legacy OFF"

run_case "$RUNS/on_a"
"$PYTHON" "$NORMALIZER" --mode legacy "$LEGACY_ON_LOG" \
  >"$WORK/legacy_on.normalized.log"
"$PYTHON" "$NORMALIZER" --mode gmra "$RUNS/on_a/run.log" \
  >"$WORK/actual_on_a.normalized.log"
cmp "$WORK/legacy_on.normalized.log" "$WORK/actual_on_a.normalized.log" ||
  fail "fresh ON-A log differs from legacy ON"

run_case "$RUNS/on_b"
"$PYTHON" "$NORMALIZER" --mode gmra "$RUNS/on_b/run.log" \
  >"$WORK/actual_on_b.normalized.log"
cmp "$WORK/legacy_on.normalized.log" "$WORK/actual_on_b.normalized.log" ||
  fail "fresh ON-B log differs from legacy ON"
cmp "$RUNS/on_a/result.xsm" "$RUNS/on_b/result.xsm" ||
  fail "ON XSM replay differs"
verify_frozen_run_head

"$PYTHON" "$LOG_CHECKER" "$LEGACY_OFF_LOG" "$LEGACY_ON_LOG" \
  "$RUNS/off/run.log" "$RUNS/on_a/run.log" "$RUNS/on_b/run.log" \
  >"$EVIDENCE/log_identity.txt"
"$PYTHON" "$NORMALIZER" --mode legacy "$RUNS/off/run.log" \
  >"$EVIDENCE/off/normalized.log"
"$PYTHON" "$NORMALIZER" --mode gmra "$RUNS/on_a/run.log" \
  >"$EVIDENCE/on_a/normalized.log"
"$PYTHON" "$NORMALIZER" --mode gmra "$RUNS/on_b/run.log" \
  >"$EVIDENCE/on_b/normalized.log"

for pair in on_a on_b
do
  compare_dir="$WORK/compare_$pair"
  mkdir "$compare_dir"
  copy_exact "$LEGACY_ON_XSM" "$compare_dir/legacy.xsm"
  copy_exact "$RUNS/$pair/result.xsm" "$compare_dir/candidate.xsm"
  before_legacy=$(hash_of "$compare_dir/legacy.xsm")
  before_candidate=$(hash_of "$compare_dir/candidate.xsm")
  (
    cd "$compare_dir"
    "$WORK/tools/check_pair" legacy.xsm candidate.xsm
  ) >"$EVIDENCE/$pair/non_audit_identity.txt" \
    2>"$WORK/check_pair_$pair.err"
  test ! -s "$WORK/check_pair_$pair.err" ||
    fail "pair comparator wrote stderr for $pair"
  rm -f "$WORK/check_pair_$pair.err"
  test "$before_legacy" = "$(hash_of "$compare_dir/legacy.xsm")" &&
    test "$before_candidate" = "$(hash_of "$compare_dir/candidate.xsm")" ||
    fail "pair comparator modified an XSM"
  before_track=$(hash_of "$RUNS/$pair/restart_track.xsm")
  before_result=$(hash_of "$RUNS/$pair/result.xsm")
  (
    cd "$RUNS/$pair"
    "$WORK/tools/check_ledger" restart_track.xsm result.xsm
  ) >"$EVIDENCE/$pair/ledger.txt" 2>"$WORK/ledger_$pair.err"
  test ! -s "$WORK/ledger_$pair.err" ||
    fail "ledger reader wrote stderr for $pair"
  rm -f "$WORK/ledger_$pair.err"
  (
    cd "$RUNS/$pair"
    "$WORK/tools/check_ledger" restart_track.xsm result.xsm
  ) >"$EVIDENCE/$pair/ledger_repeat.txt" \
    2>"$WORK/ledger_repeat_$pair.err"
  test ! -s "$WORK/ledger_repeat_$pair.err" ||
    fail "repeated ledger reader wrote stderr for $pair"
  rm -f "$WORK/ledger_repeat_$pair.err"
  test "$before_track" = "$(hash_of "$RUNS/$pair/restart_track.xsm")" &&
    test "$before_result" = "$(hash_of "$RUNS/$pair/result.xsm")" ||
    fail "ledger reader modified an XSM for $pair"
  cmp "$EVIDENCE/$pair/ledger.txt" "$EVIDENCE/$pair/ledger_repeat.txt" ||
    fail "reader replay differs for $pair"
done
cmp "$EVIDENCE/on_a/ledger.txt" "$EVIDENCE/on_b/ledger.txt" ||
  fail "ON ledger replay differs"

copy_exact "$PROTOCOL" "$EVIDENCE/gmres_activity_run_protocol.json"
copy_exact "$RUN_IMPLEMENTATION" \
  "$EVIDENCE/gmres_activity_run_implementation.sha256"
copy_exact "$BUILD/source_identity.tsv" "$EVIDENCE/source_identity.tsv"
copy_exact "$BUILD/build_receipt.tsv" "$EVIDENCE/build_receipt.tsv"
copy_exact "$BUILD/toolchain.sha256" "$EVIDENCE/toolchain.sha256"
copy_exact "$BUILD/symbol_audit.txt" "$EVIDENCE/symbol_audit.txt"
copy_exact "$BUILD/instrumented_source_manifest.sha256" \
  "$EVIDENCE/instrumented_source_manifest.sha256"
copy_exact "$BUILD/executable.sha256" "$EVIDENCE/executable.sha256"
copy_exact "$TRACK" "$EVIDENCE/track.xsm"
copy_exact "$WORK/preflight.log" "$EVIDENCE/preflight.log"
copy_exact "$WORK/implementation_replay.log" \
  "$EVIDENCE/implementation_replay.log"
copy_exact "$WORK/inputs_before.sha256" "$EVIDENCE/inputs_before.sha256"

for pair in off on_a on_b
do
  copy_exact "$RUNS/$pair/deck.x2m" "$EVIDENCE/$pair/deck.x2m"
  copy_exact "$RUNS/$pair/run.log" "$EVIDENCE/$pair/run.log"
  copy_exact "$RUNS/$pair/result.xsm" "$EVIDENCE/$pair/result.xsm"
done

(
  cd "$EVIDENCE"
  shasum -a 256 on_a/ledger.txt on_a/ledger_repeat.txt \
    on_b/ledger.txt on_b/ledger_repeat.txt
) >"$EVIDENCE/reader_replay.sha256"

write_input_receipt "$WORK/inputs_after.sha256"
cmp "$WORK/inputs_before.sha256" "$WORK/inputs_after.sha256" ||
  fail "frozen input identity changed"
copy_exact "$WORK/inputs_after.sha256" "$EVIDENCE/inputs_after.sha256"
verify_reference_and_build
verify_run_implementation
verify_frozen_run_head
env -u RUN_GMRES_ACTIVITY -u FC PATH="$METHOD_PATH" \
  PYTHONDONTWRITEBYTECODE=1 \
  sh "$METHOD_PREFLIGHT" >"$EVIDENCE/postflight.log"

write_result_from_ledger "$EVIDENCE/on_a/ledger.txt" \
  "$EVIDENCE/result.txt"
printf '%s\n' "$RESULT_CLASSIFICATION" \
  >"$EVIDENCE/artifact_check_a.log"
printf '%s\n' "$RESULT_CLASSIFICATION" \
  >"$EVIDENCE/artifact_check_b.log"

verify_frozen_run_head
printf '%s\n' "$RUN_COMMIT" >"$EVIDENCE/run_commit.txt"
RUN_IMPLEMENTATION_SHA256=$(hash_of "$RUN_IMPLEMENTATION")
{
  printf 'schema\t1\n'
  printf 'run_commit\t%s\n' "$RUN_COMMIT"
  printf 'source_implementation_commit\t%s\n' \
    "$SOURCE_IMPLEMENTATION_COMMIT"
  printf 'method_protocol_sha256\t%s\n' "$METHOD_PROTOCOL_SHA256"
  printf 'run_protocol_sha256\t%s\n' "$RUN_PROTOCOL_SHA256"
  printf 'method_implementation_manifest_sha256\t%s\n' \
    "$METHOD_IMPLEMENTATION_SHA256"
  printf 'run_implementation_manifest_sha256\t%s\n' \
    "$RUN_IMPLEMENTATION_SHA256"
  printf 'executable_sha256\t%s\n' "$DRAGON_SHA256"
  printf 'process_matrix\tOFF=1,ON=2\n'
  printf 'classification\t%s\n' "$RESULT_CLASSIFICATION"
} >"$EVIDENCE/run_receipt.tsv"

write_artifact_manifest "$EVIDENCE"
verify_candidate_artifact "$EVIDENCE" "$RESULT_CLASSIFICATION" work_a
verify_candidate_artifact "$EVIDENCE" "$RESULT_CLASSIFICATION" work_b
cmp "$WORK/work_a.out" "$EVIDENCE/artifact_check_a.log"
cmp "$WORK/work_b.out" "$EVIDENCE/artifact_check_b.log"

PUBLISH=$(mktemp -d "$ARTIFACT_PARENT/.gmres-activity-publish.XXXXXX")
cp -R "$EVIDENCE/." "$PUBLISH/"
verify_candidate_artifact "$PUBLISH" "$RESULT_CLASSIFICATION" publish
test ! -e "$ARTIFACT" && test ! -L "$ARTIFACT" ||
  fail "artifact path appeared before publication"
FINAL_INODE=$(inode_of "$PUBLISH")
FINAL_OWNED=1
mv "$PUBLISH" "$ARTIFACT"
PUBLISH=
test "$(inode_of "$ARTIFACT")" = "$FINAL_INODE" ||
  fail "published artifact inode differs"
verify_candidate_artifact "$ARTIFACT" "$RESULT_CLASSIFICATION" final

rmdir "$LOCK"
LOCK_HELD=0
FINAL_OWNED=0
echo "GMRES-ACTIVITY PRODUCTION PASS"
echo "$RESULT_CLASSIFICATION"
