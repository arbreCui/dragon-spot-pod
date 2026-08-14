#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
MANIFEST=${MANIFEST:-"$ROOT/validation/iterative/residual_direction_inputs.tsv"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}

test -f "$MANIFEST" && test ! -L "$MANIFEST"
test -f "$GANLIB_LIB"
test -f "$GANLIB_MOD/ganlib.mod"

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-residual-direction.XXXXXX")
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

hash_file() {
  hash_output=$(shasum -a 256 "$1")
  digest=${hash_output%% *}
  printf '%s\n' "$digest" | rg -q '^[0-9a-f]{64}$'
  printf '%s\n' "$digest"
}

manifest_value() {
  awk -v role="$1" '$1 == role { print $2 }' "$MANIFEST"
}

manifest_path() {
  awk -v role="$1" '$1 == role { print $3 }' "$MANIFEST"
}

stage_state() {
  role=$1
  expected=$(manifest_value "$role")
  rel=$(manifest_path "$role")
  printf '%s\n' "$expected" | rg -q '^[0-9a-f]{64}$'
  case "$rel" in
    /*|.|..|../*|*/../*|*/..)
      printf 'RESIDUAL-DIRECTION ERROR: unsafe path for %s\n' "$role" >&2
      exit 2
      ;;
  esac
  source_path="$ROOT/$rel"
  test -f "$source_path" && test ! -L "$source_path"
  test "$(hash_file "$source_path")" = "$expected"
  cp "$source_path" "$WORK/$role.xsm"
  test "$(hash_file "$WORK/$role.xsm")" = "$expected"
}

rows=$(awk 'NF && $1 !~ /^#/ { count++ } END { print count + 0 }' "$MANIFEST")
test "$rows" = 3
for role in x6 x7 x8
do
  count=$(awk -v role="$role" '$1 == role { count++ } END { print count + 0 }' \
    "$MANIFEST")
  test "$count" = 1
  stage_state "$role"
done

"$FC" -std=f2008 -O0 -Wall -Wextra -Werror -Wno-compare-reals \
  -ffp-contract=off -fno-fast-math -I "$GANLIB_MOD" \
  "$ROOT/validation/iterative/check_one_map_xsm.f90" \
  "$GANLIB_LIB" -lstdc++ -o "$WORK/check_one_map_xsm"

(
  cd "$WORK"
  ./check_one_map_xsm --directions x6.xsm x7.xsm x8.xsm
)

for role in x6 x7 x8
do
  test "$(hash_file "$ROOT/$(manifest_path "$role")")" = \
    "$(manifest_value "$role")"
done

printf '%s\n' \
  'RESIDUAL-DIRECTION READ-ONLY HASH PASS' \
  'RESIDUAL-DIRECTION NO-DRAGON PASS'
