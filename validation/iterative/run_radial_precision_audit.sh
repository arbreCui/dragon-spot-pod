#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
DIRNAME=$(uname -sm | sed 's/[ ]/_/')
ARTIFACT="$ROOT/validation/artifacts/iterative-radial-floor"
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/lib/$DIRNAME/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/lib/$DIRNAME/modules"}
FC=${FC:-gfortran}
SOURCE="$ROOT/validation/iterative/check_radial_precision_xsm.f90"
PARENT_RECEIPT="$ROOT/validation/iterative/radial_floor_result_receipt.sha256"
PRECISION_RECEIPT="$ROOT/validation/iterative/radial_precision_receipt.sha256"
PUBLISHED_RESULT="$ROOT/validation/iterative/radial_precision_result.txt"
PUBLISHED_FULL="$ARTIFACT/radial_precision_xsm_full.log"

for path in "$SOURCE" "$PARENT_RECEIPT" "$PRECISION_RECEIPT" \
  "$PUBLISHED_RESULT" "$PUBLISHED_FULL" "$GANLIB_LIB" "$GANLIB_MOD/ganlib.mod"
do
  test -f "$path"
  test ! -L "$path"
done
test -d "$ARTIFACT"
test ! -L "$ARTIFACT"
for path in restart_track.xsm restart_source.xsm restart_system.xsm \
  restart_cap.xsm native/probe_pre.xsm native/probe_post.xsm \
  stationary/probe_pre.xsm stationary/probe_post.xsm \
  check_radial_floor_xsm radial_floor_xsm_check.log receipt.sha256 \
  minimal_manifest.sha256 dependency_manifest.sha256
do
  test -f "$ARTIFACT/$path"
  test ! -L "$ARTIFACT/$path"
done

inode_of() {
  stat -f '%d:%i' "$1" 2>/dev/null || stat -c '%d:%i' "$1"
}
seen_inodes=
for path in restart_track.xsm \
  native/probe_pre.xsm native/probe_post.xsm \
  stationary/probe_pre.xsm stationary/probe_post.xsm
do
  inode=$(inode_of "$ARTIFACT/$path")
  case " $seen_inodes " in
    *" $inode "*)
      echo "RADIAL-PRECISION FAIL: aliased scientific input $path" >&2
      exit 1
      ;;
  esac
  seen_inodes="$seen_inodes $inode"
done

(
  cd "$ROOT"
  shasum -a 256 -c "$PARENT_RECEIPT"
  shasum -a 256 -c "$PRECISION_RECEIPT"
) >/dev/null
(
  cd "$ARTIFACT"
  shasum -a 256 -c receipt.sha256
  shasum -a 256 -c minimal_manifest.sha256
  shasum -a 256 -c dependency_manifest.sha256
) >/dev/null

WORK=$(mktemp -d "/tmp/spot-rp.XXXXXX")
cleanup() {
  rm -rf "$WORK"
}
trap cleanup EXIT HUP INT TERM

FC_FLAGS="-std=f2008 -O0 -Wall -Wextra -Werror -Wno-compare-reals
  -fcheck=all -ffp-contract=off -fno-fast-math -ffpe-summary=none"
"$FC" $FC_FLAGS \
  -I "$GANLIB_MOD" -c "$SOURCE" \
  -o "$WORK/check_radial_precision_xsm.o"
nm -u "$WORK/check_radial_precision_xsm.o" \
  > "$WORK/check_radial_precision_xsm.object.nm"
if rg -i 'LCMPUT|LCMPTC|LCMPPD|LCMLID|LCMLIL|LCMEQU|LCMDEL' \
  "$WORK/check_radial_precision_xsm.object.nm" >/dev/null
then
  echo "RADIAL-PRECISION FAIL: checker object references LCM mutation" >&2
  exit 1
fi
if rg -i 'FLU2DR|FLU2AC|FLUBAL|DOORFV|MCCGF|MCGFLX|Dragon|SPOT1P' \
  "$WORK/check_radial_precision_xsm.object.nm" >/dev/null
then
  echo "RADIAL-PRECISION FAIL: checker object references solver symbols" >&2
  exit 1
fi
rg -i 'lcmop' "$WORK/check_radial_precision_xsm.object.nm" >/dev/null

"$FC" $FC_FLAGS "$WORK/check_radial_precision_xsm.o" \
  "$GANLIB_LIB" -lstdc++ \
  -o "$WORK/check_radial_precision_xsm"

if rg -i '\b(LCMPUT|LCMPTC|LCMPPD|LCMLID|LCMLIL|LCMEQU|LCMDEL)\b' \
  "$SOURCE" >/dev/null
then
  echo "RADIAL-PRECISION FAIL: checker contains LCM mutation" >&2
  exit 1
fi
nm "$WORK/check_radial_precision_xsm" \
  > "$WORK/check_radial_precision_xsm.nm"
if rg -i 'FLU2DR|FLU2AC|FLUBAL|DOORFV|MCCGF|MCGFLX|Dragon|SPOT1P' \
  "$WORK/check_radial_precision_xsm.nm" >/dev/null
then
  echo "RADIAL-PRECISION FAIL: checker links production solver symbols" >&2
  exit 1
fi
rg -i 'lcmop' "$WORK/check_radial_precision_xsm.nm" >/dev/null

"$WORK/check_radial_precision_xsm" SELFTEST \
  > "$WORK/selftest_a.log"
"$WORK/check_radial_precision_xsm" SELFTEST \
  > "$WORK/selftest_b.log"
cmp "$WORK/selftest_a.log" "$WORK/selftest_b.log"
grep '^RADIAL-PRECISION-XSM SELFTEST PASS$' \
  "$WORK/selftest_a.log" >/dev/null

(
  cd "$ARTIFACT"
  shasum -a 256 restart_track.xsm \
    native/probe_pre.xsm native/probe_post.xsm \
    stationary/probe_pre.xsm stationary/probe_post.xsm \
    > "$WORK/inputs_before.sha256"
  ./check_radial_floor_xsm restart_track.xsm restart_source.xsm \
    restart_system.xsm restart_cap.xsm \
    native/probe_pre.xsm native/probe_post.xsm \
    stationary/probe_pre.xsm stationary/probe_post.xsm \
    > "$WORK/radial_floor_replay.log"
  "$WORK/check_radial_precision_xsm" restart_track.xsm \
    native/probe_pre.xsm native/probe_post.xsm \
    stationary/probe_pre.xsm stationary/probe_post.xsm \
    > "$WORK/precision_a.log"
  "$WORK/check_radial_precision_xsm" restart_track.xsm \
    native/probe_pre.xsm native/probe_post.xsm \
    stationary/probe_pre.xsm stationary/probe_post.xsm \
    > "$WORK/precision_b.log"
  shasum -a 256 -c "$WORK/inputs_before.sha256" \
    > "$WORK/inputs_after.log"
)
cmp "$ARTIFACT/radial_floor_xsm_check.log" \
  "$WORK/radial_floor_replay.log"
cmp "$WORK/precision_a.log" "$WORK/precision_b.log"
cmp "$WORK/precision_a.log" "$PUBLISHED_FULL"

grep '^RADIAL-PRECISION-XSM DIMS 370 8 14$' \
  "$WORK/precision_a.log" >/dev/null
grep '^RADIAL-PRECISION-XSM NATIVE TOTAL 2960$' \
  "$WORK/precision_a.log" >/dev/null
grep '^RADIAL-PRECISION-XSM STATIONARY TOTAL 2960$' \
  "$WORK/precision_a.log" >/dev/null
grep '^RADIAL-PRECISION-XSM COMPLETE$' \
  "$WORK/precision_a.log" >/dev/null
test "$(grep -c ' LEDGER ' "$WORK/precision_a.log")" -eq 5920
test "$(grep -c ' NATIVE LEDGER ' "$WORK/precision_a.log")" -eq 2960
test "$(grep -c ' STATIONARY LEDGER ' "$WORK/precision_a.log")" -eq 2960

grep -v ' LEDGER ' "$WORK/precision_a.log" \
  > "$WORK/precision_compact.log"
cmp "$WORK/precision_compact.log" "$PUBLISHED_RESULT"
(
  cd "$ROOT"
  shasum -a 256 -c "$PARENT_RECEIPT"
  shasum -a 256 -c "$PRECISION_RECEIPT"
) >/dev/null
(
  cd "$ARTIFACT"
  shasum -a 256 -c receipt.sha256
  shasum -a 256 -c minimal_manifest.sha256
  shasum -a 256 -c dependency_manifest.sha256
) >/dev/null
grep -v ' LEDGER ' "$WORK/precision_a.log"
