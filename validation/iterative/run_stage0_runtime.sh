#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
DRAGON_BIN=${DRAGON_BIN:?set DRAGON_BIN to an executable built from the current sources}
SEED_DIR=${SEED_DIR:-"$ROOT/validation/artifacts/iterative-seed"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}

test -x "$DRAGON_BIN"
test -f "$GANLIB_LIB"
(
  cd "$SEED_DIR"
  shasum -a 256 -c "$ROOT/validation/iterative/seed.sha256"
)

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-iter-stage0.XXXXXX")
cleanup() {
  if [ "${KEEP_WORK:-0}" = 1 ]; then
    printf 'ITERATIVE STAGE0 WORKDIR: %s\n' "$WORK"
  else
    rm -rf "$WORK"
  fi
}
trap cleanup EXIT HUP INT TERM

for name in initial_snapshots.xsm initial_axial_track.xsm \
  initial_axial_macrolib.xsm initial_radial_track.bin \
  state8_axial.xsm state9_axial.xsm
do
  cp "$SEED_DIR/$name" "$WORK/$name"
done
cp "$ROOT/data/SpotRefFS.c2m" "$ROOT/data/SpotPlaneFS.c2m" "$WORK/"

before=$(shasum -a 256 \
  "$SEED_DIR/state8_axial.xsm" "$SEED_DIR/state9_axial.xsm")

(
  cd "$WORK"
  "$DRAGON_BIN" < "$ROOT/validation/iterative/fixed_basis_nosolve.x2m" \
    > fixed_basis.log 2>&1
  "$DRAGON_BIN" < "$ROOT/validation/iterative/state_residual_nosolve.x2m" \
    > state_residual.log 2>&1
  awk '
    /ECHO "ITERATIVE-MAP-BEGIN"/ { print "IF 0 1 = THEN" }
    /ECHO "ITERATIVE-MAP-COMPLETE"/ { print "ENDIF ;" }
    { print }
  ' "$ROOT/validation/iterative/one_corrected_map.x2m" |
    "$DRAGON_BIN" > one_map_syntax.log 2>&1
)

gfortran -std=f2008 -O0 -Wall -Wextra -ffp-contract=off -fno-fast-math \
  -I "$GANLIB_MOD" \
  "$ROOT/validation/iterative/check_fixed_basis_xsm.f90" \
  "$GANLIB_LIB" -lstdc++ -o "$WORK/check_fixed_basis_xsm"

(
  cd "$WORK"
  ./check_fixed_basis_xsm basis_reference.xsm fixed_system.xsm \
    > fixed_basis_check.log
)

nm "$WORK/check_fixed_basis_xsm" > "$WORK/checker_nm.txt"
if rg -i 'SPOASM|SPOPOD|SPOT1P|SPOPROJ|SPOSTATE|SPOXCONV|Dragon' \
  "$WORK/checker_nm.txt" >/dev/null
then
  echo "ITERATIVE STAGE0 RUNTIME FAIL: checker links production solver symbols." >&2
  exit 1
fi
rg -i 'lcmop' "$WORK/checker_nm.txt" >/dev/null

rg 'ITERATIVE-FIXB-NOSOLVE-COMPLETE' "$WORK/fixed_basis.log" >/dev/null
rg 'FIXED-BASIS-XSM COMPLETE' "$WORK/fixed_basis_check.log" >/dev/null
rg 'ITERATIVE-STATE-CANONICAL-PROJECTION' \
  "$WORK/state_residual.log" >/dev/null
rg 'ITERATIVE-HISTORICAL-STATE-DIFFERENCE' \
  "$WORK/state_residual.log" >/dev/null
rg 'ITERATIVE-STATE-NOSOLVE-COMPLETE' \
  "$WORK/state_residual.log" >/dev/null
rg 'ITERATIVE-MAP-COMPLETE' "$WORK/one_map_syntax.log" >/dev/null
rg 'normal end of execution' "$WORK/one_map_syntax.log" >/dev/null

after=$(shasum -a 256 \
  "$SEED_DIR/state8_axial.xsm" "$SEED_DIR/state9_axial.xsm")
test "$before" = "$after"

cat "$WORK/fixed_basis_check.log"
rg 'SPOSTATE NCOEF|SPOPROJ FIXED-SPACE|SPOXCONV RRHO' \
  "$WORK/state_residual.log"
echo "ITERATIVE STAGE0 RUNTIME PASS: no transport solve; fixed basis, canonical state, residual plumbing, and the one-map deck syntax are executable."
