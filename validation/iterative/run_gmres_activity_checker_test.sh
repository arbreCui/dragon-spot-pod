#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
FROZEN_FC=/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15
FROZEN_FC_SHA256=0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492
GANLIB_MOD="$ROOT/Ganlib/lib/Darwin_arm64/modules"
GANLIB_LIB="$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a"
GANLIB_MOD_SHA256=9ad2be2ae13310aa8273409d5cb3e70dfaa2201ada7bfc29a135bd566c4651d0
GANLIB_LIB_SHA256=204d9f3aeaf4e06d8fbb62225e14859a767476cd845ba0096f166b5f9e14822c
READER="$ROOT/validation/iterative/check_gmres_activity_xsm.f90"
FIXTURE="$ROOT/validation/iterative/make_gmres_activity_fixture.f90"
WORK=$(mktemp -d /tmp/spot-gmra-test.XXXXXX)
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

if test "${FC+x}" = x && test "$FC" != "$FROZEN_FC"
then
  echo "unfrozen FC override rejected" >&2
  exit 2
fi
FC=$FROZEN_FC
test "$(uname -sm)" = "Darwin arm64"

for path in "$FC" "$GANLIB_MOD/ganlib.mod" "$GANLIB_LIB" \
  "$READER" "$FIXTURE"
do
  test -f "$path"
  test ! -L "$path"
done
test "$(shasum -a 256 "$FC" | awk '{print $1}')" = "$FROZEN_FC_SHA256"
test "$(shasum -a 256 "$GANLIB_MOD/ganlib.mod" | awk '{print $1}')" = \
  "$GANLIB_MOD_SHA256"
test "$(shasum -a 256 "$GANLIB_LIB" | awk '{print $1}')" = \
  "$GANLIB_LIB_SHA256"
test "$("$FC" --version | head -1)" = \
  "GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0"

FC_FLAGS="-std=f2008 -O0 -Wall -Wextra -Werror
  -fcheck=all -ffp-contract=off -fno-fast-math -ffpe-summary=none"
"$FC" $FC_FLAGS -I "$GANLIB_MOD" -c "$READER" \
  -o "$WORK/reader.o"
"$FC" "$WORK/reader.o" "$GANLIB_LIB" -lstdc++ \
  -o "$WORK/reader"
"$FC" $FC_FLAGS -I "$GANLIB_MOD" -c "$FIXTURE" \
  -o "$WORK/fixture.o"
"$FC" "$WORK/fixture.o" "$GANLIB_LIB" -lstdc++ \
  -o "$WORK/fixture"

if grep -Ei \
  '(LCMPUT|LCMPTC|LCMPPD|LCMDID|LCMDIL|LCMLID|LCMLIL|LCMDEL|LCMEQU|LCMSIX)' \
  "$READER" >/dev/null
then
  echo "GMRES-ACTIVITY TEST FAIL: reader source contains LCM mutation" >&2
  exit 1
fi
if grep -Ei \
  '(use[[:space:]]+(SPOMOC|FLU|MCG|MOC)|call[[:space:]]+(DOORFV|FLU2DR|FLU2AC|FLUBAL|MCCGF|MCGFLX|MCGFL1|MCGMRE|MCGFCS|SPOMOC))' \
  "$READER" >/dev/null
then
  echo "GMRES-ACTIVITY TEST FAIL: reader source references solver code" >&2
  exit 1
fi
nm -u "$WORK/reader.o" >"$WORK/reader.object.nm"
if grep -Ei \
  'LCMPUT|LCMPTC|LCMPPD|LCMDID|LCMDIL|LCMLID|LCMLIL|LCMDEL|LCMEQU|LCMSIX|DOORFV|FLU2DR|FLU2AC|FLUBAL|MCCGF|MCGFLX|MCGFL1|MCGMRE|MCGFCS|SPOMOC' \
  "$WORK/reader.object.nm" >/dev/null
then
  echo "GMRES-ACTIVITY TEST FAIL: reader object has forbidden symbol" >&2
  exit 1
fi
grep -i 'lcmop' "$WORK/reader.object.nm" >/dev/null
grep -i 'lcmget' "$WORK/reader.object.nm" >/dev/null

make_case()
{
  case_dir=$1
  mode=$2
  mkdir "$case_dir"
  "$WORK/fixture" "$case_dir" "$mode"
}

run_reader()
{
  case_dir=$1
  output=$2
  (
    cd "$case_dir"
    "$WORK/reader" track.xsm activity.xsm
  ) >"$output"
}

run_reader_clean()
{
  case_dir=$1
  output=$2
  run_reader "$case_dir" "$output" 2>"$output.err"
  if test -s "$output.err"; then
    cat "$output.err" >&2
    return 1
  fi
}

for pair in zero_a zero_b zerok_a zerok_b active_a active_b mixed_a mixed_b
do
  case "$pair" in
    zero_*) mode=zero-block ;;
    zerok_*) mode=zero-k ;;
    active_*) mode=active ;;
    mixed_*) mode=mixed ;;
  esac
  make_case "$WORK/$pair" "$mode"
done

cmp "$WORK/zero_a/track.xsm" "$WORK/zero_b/track.xsm"
cmp "$WORK/zero_a/activity.xsm" "$WORK/zero_b/activity.xsm"
cmp "$WORK/zerok_a/track.xsm" "$WORK/zerok_b/track.xsm"
cmp "$WORK/zerok_a/activity.xsm" "$WORK/zerok_b/activity.xsm"
cmp "$WORK/active_a/track.xsm" "$WORK/active_b/track.xsm"
cmp "$WORK/active_a/activity.xsm" "$WORK/active_b/activity.xsm"
cmp "$WORK/mixed_a/track.xsm" "$WORK/mixed_b/track.xsm"
cmp "$WORK/mixed_a/activity.xsm" "$WORK/mixed_b/activity.xsm"

shasum -a 256 "$WORK/mixed_a/track.xsm" \
  "$WORK/mixed_a/activity.xsm" >"$WORK/mixed.before.sha256"
run_reader_clean "$WORK/mixed_a" "$WORK/mixed_a.first.log"
shasum -a 256 "$WORK/mixed_a/track.xsm" \
  "$WORK/mixed_a/activity.xsm" >"$WORK/mixed.after.sha256"
cmp "$WORK/mixed.before.sha256" "$WORK/mixed.after.sha256"
run_reader_clean "$WORK/mixed_a" "$WORK/mixed_a.second.log"
cmp "$WORK/mixed_a.first.log" "$WORK/mixed_a.second.log"

run_reader_clean "$WORK/zero_a" "$WORK/zero_a.log"
run_reader_clean "$WORK/zero_b" "$WORK/zero_b.log"
run_reader_clean "$WORK/zerok_a" "$WORK/zerok_a.log"
run_reader_clean "$WORK/zerok_b" "$WORK/zerok_b.log"
run_reader_clean "$WORK/active_a" "$WORK/active_a.log"
run_reader_clean "$WORK/active_b" "$WORK/active_b.log"
run_reader_clean "$WORK/mixed_b" "$WORK/mixed_b.log"
cmp "$WORK/zero_a.log" "$WORK/zero_b.log"
cmp "$WORK/zerok_a.log" "$WORK/zerok_b.log"
cmp "$WORK/active_a.log" "$WORK/active_b.log"
cmp "$WORK/mixed_a.first.log" "$WORK/mixed_b.log"

grep '^GMRES-ACTIVITY CLASSIFICATION VALID-GMRES-UPDATE-INACTIVE$' \
  "$WORK/zero_a.log" >/dev/null
grep '^GMRES-ACTIVITY CLASSIFICATION VALID-GMRES-UPDATE-ACTIVE$' \
  "$WORK/zerok_a.log" >/dev/null
grep '^GMRES-ACTIVITY CLASSIFICATION VALID-GMRES-UPDATE-ACTIVE$' \
  "$WORK/active_a.log" >/dev/null
grep '^GMRES-ACTIVITY CLASSIFICATION VALID-GMRES-UPDATE-ACTIVE$' \
  "$WORK/mixed_a.first.log" >/dev/null
grep '^GMRES-ACTIVITY NONZERO-K-GROUP-BLOCKS 0$' \
  "$WORK/zero_a.log" >/dev/null
grep '^GMRES-ACTIVITY NONZERO-K-GROUP-BLOCKS 322$' \
  "$WORK/zerok_a.log" >/dev/null
grep '^GMRES-ACTIVITY SUM-K 2920$' "$WORK/zerok_a.log" >/dev/null
grep '^GMRES-ACTIVITY MAX-K 10$' "$WORK/zerok_a.log" >/dev/null
grep '^GMRES-ACTIVITY NONZERO-K-GROUP-BLOCKS 94$' \
  "$WORK/active_a.log" >/dev/null
grep '^GMRES-ACTIVITY NONZERO-K-GROUP-BLOCKS 261$' \
  "$WORK/mixed_a.first.log" >/dev/null
grep '^GMRES-ACTIVITY SUM-K 431$' "$WORK/mixed_a.first.log" >/dev/null
grep '^GMRES-ACTIVITY MAX-K 3$' "$WORK/mixed_a.first.log" >/dev/null
grep '^GMRES-ACTIVITY THRESHOLD NONE$' "$WORK/mixed_a.first.log" \
  >/dev/null
test "$(grep -c '^GMRES-ACTIVITY RAW ROLE-ACTIVE ' \
  "$WORK/zero_a.log")" -eq 370
test "$(grep -c '^GMRES-ACTIVITY RAW ROLE-ACTIVE ' \
  "$WORK/zerok_a.log")" -eq 7400
test "$(grep -c '^GMRES-ACTIVITY RAW ROLE-ACTIVE ' \
  "$WORK/active_a.log")" -eq 1480
test "$(grep -c '^GMRES-ACTIVITY RAW ROLE-ACTIVE ' \
  "$WORK/mixed_a.first.log")" -eq 3330
test "$(grep -c '^GMRES-ACTIVITY RAW BLOCK-GROUP ' \
  "$WORK/zero_a.log" || true)" -eq 0
test "$(grep -c '^GMRES-ACTIVITY RAW BLOCK-GROUP ' \
  "$WORK/zerok_a.log")" -eq 1110
test "$(grep -c '^GMRES-ACTIVITY RAW BLOCK-GROUP ' \
  "$WORK/mixed_a.first.log")" -eq 740

TAMPERS="
tamper-track-kryl
tamper-track-maxi
tamper-track-epsi
tamper-status
tamper-state-sum
tamper-added-operator
tamper-ngind
tamper-reordered-event
tamper-duplicate-event
tamper-role
tamper-event-iter
tamper-event-iter-high
tamper-event-block
tamper-event-active-count
tamper-role-mask
tamper-event-sequence
tamper-affine-mask
tamper-global-mask-rise
tamper-empty-primary
tamper-call-exit
tamper-call-event-count
tamper-call-block-count
tamper-call-last-iter
tamper-reordered-block
tamper-duplicate-block
tamper-block-mask
tamper-inactive-k
tamper-k-range
tamper-k-reconstruct
tamper-first-mask
tamper-monotone
tamper-histogram
tamper-role-groups
tamper-extra
tamper-missing-role-active
tamper-wrong-role-type
tamper-wrong-role-length
tamper-missing-block-active
tamper-wrong-block-type
tamper-wrong-block-length
tamper-zero-role
tamper-unexpected-block
"
for mode in $TAMPERS
do
  make_case "$WORK/$mode" "$mode"
  if run_reader "$WORK/$mode" "$WORK/$mode.log" \
      2>"$WORK/$mode.err"
  then
    echo "GMRES-ACTIVITY TEST FAIL: tamper passed: $mode" >&2
    exit 1
  fi
  test -s "$WORK/$mode.err"
  grep -q '^GMRES-ACTIVITY CHECK FAIL: ' "$WORK/$mode.err"
  if grep -E 'Fortran runtime error|Program received signal|SIGBUS|SIGSEGV' \
       "$WORK/$mode.err" >/dev/null
  then
    echo "GMRES-ACTIVITY TEST FAIL: tamper crashed: $mode" >&2
    exit 1
  fi
done

grep 'TRACK NSTART differs' "$WORK/tamper-track-kryl.err" >/dev/null
grep 'TRACK MAXI differs' "$WORK/tamper-track-maxi.err" >/dev/null
grep 'TRACK ERRTOL bits differ' "$WORK/tamper-track-epsi.err" >/dev/null
grep 'AFFINE-RHS event is not immediately after PRIMARY' \
  "$WORK/tamper-event-sequence.err" >/dev/null
grep 'AFFINE-RHS mask differs from block-entry mask' \
  "$WORK/tamper-affine-mask.err" >/dev/null
grep 'ROLE-ACTIVE globally changes from zero to one' \
  "$WORK/tamper-global-mask-rise.err" >/dev/null
grep 'ROLE-EVENTS cannot be empty on the MCGMRE path' \
  "$WORK/tamper-empty-primary.err" >/dev/null
grep 'ROLE-EVENTS ITER is outside the frozen range' \
  "$WORK/tamper-event-iter-high.err" >/dev/null
grep 'first Krylov mask differs from block mask' \
  "$WORK/tamper-first-mask.err" >/dev/null
grep 'ROLE-ACTIVE globally changes from zero to one' \
  "$WORK/tamper-monotone.err" >/dev/null
grep 'KMAX does not reconstruct from Krylov masks' \
  "$WORK/tamper-k-reconstruct.err" >/dev/null
grep 'inactive group has nonzero KMAX' \
  "$WORK/tamper-inactive-k.err" >/dev/null
grep 'at least one PRIMARY role event is required' \
  "$WORK/tamper-zero-role.err" >/dev/null
grep 'AUDIT ROOT census differs' \
  "$WORK/tamper-unexpected-block.err" >/dev/null

# Exact asymmetric sentinels prove event/block-major then physical-group
# storage rather than merely reproducing the aggregate summaries.
grep '^GMRES-ACTIVITY RAW ROLE-ACTIVE 4 1 1$' \
  "$WORK/mixed_a.first.log" >/dev/null
grep '^GMRES-ACTIVITY RAW ROLE-ACTIVE 4 3 0$' \
  "$WORK/mixed_a.first.log" >/dev/null
grep '^GMRES-ACTIVITY RAW ROLE-ACTIVE 5 1 1$' \
  "$WORK/mixed_a.first.log" >/dev/null
grep '^GMRES-ACTIVITY RAW ROLE-ACTIVE 5 301 0$' \
  "$WORK/mixed_a.first.log" >/dev/null
grep '^GMRES-ACTIVITY RAW ROLE-ACTIVE 8 297 1$' \
  "$WORK/mixed_a.first.log" >/dev/null
grep '^GMRES-ACTIVITY RAW BLOCK-GROUP 1 1 1 3$' \
  "$WORK/mixed_a.first.log" >/dev/null
grep '^GMRES-ACTIVITY RAW BLOCK-GROUP 1 2 0 0$' \
  "$WORK/mixed_a.first.log" >/dev/null
grep '^GMRES-ACTIVITY RAW BLOCK-GROUP 1 301 1 2$' \
  "$WORK/mixed_a.first.log" >/dev/null
grep '^GMRES-ACTIVITY RAW BLOCK-GROUP 2 1 1 2$' \
  "$WORK/mixed_a.first.log" >/dev/null
grep '^GMRES-ACTIVITY RAW BLOCK-GROUP 2 5 1 1$' \
  "$WORK/mixed_a.first.log" >/dev/null
grep '^GMRES-ACTIVITY RAW BLOCK-GROUP 2 297 1 2$' \
  "$WORK/mixed_a.first.log" >/dev/null

echo "GMRES-ACTIVITY CHECKER TEST PASS"
