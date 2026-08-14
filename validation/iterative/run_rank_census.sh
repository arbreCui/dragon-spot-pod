#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
BASIS_XSM=${BASIS_XSM:-"$ROOT/validation/artifacts/iterative-map1/basis_reference.xsm"}
EXPECTED_SHA=dc65467731947901393f9fb7114b7cd2e956a9992bb97db18e665b47e7446504
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}

test -f "$BASIS_XSM" && test ! -L "$BASIS_XSM"
test -f "$GANLIB_LIB"
test -f "$GANLIB_MOD/ganlib.mod"

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-rank-census.XXXXXX")
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

hash_file() {
  hash_output=$(shasum -a 256 "$1")
  digest=${hash_output%% *}
  printf '%s\n' "$digest" | rg -q '^[0-9a-f]{64}$'
  printf '%s\n' "$digest"
}

test "$(hash_file "$BASIS_XSM")" = "$EXPECTED_SHA"
cp "$BASIS_XSM" "$WORK/basis_reference.xsm"
test "$(hash_file "$WORK/basis_reference.xsm")" = "$EXPECTED_SHA"

"$FC" -std=f2008 -O0 -g -pedantic -Wall -Wextra -Werror \
  -fcheck=all -ffp-contract=off -fno-fast-math -I "$GANLIB_MOD" \
  "$ROOT/validation/iterative/check_rank_census_xsm.f90" \
  "$GANLIB_LIB" -lstdc++ -o "$WORK/check_rank_census_xsm"

(
  cd "$WORK"
  ./check_rank_census_xsm basis_reference.xsm
)

test "$(hash_file "$BASIS_XSM")" = "$EXPECTED_SHA"
printf '%s\n' \
  'SPOT-RANK-CENSUS READ-ONLY HASH PASS' \
  'SPOT-RANK-CENSUS NO-DRAGON PASS'
