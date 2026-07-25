#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-s4v2-tests.XXXXXX")
cleanup() {
  rm -rf "$WORK"
}
trap cleanup EXIT HUP INT TERM

PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/check_inner_sensitivity_v2_protocol.py" \
  --public-only

(
  cd "$ROOT/validation/iterative"
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
    test_inner_sensitivity_v2_log.py \
    test_inner_sensitivity_v2_result.py \
    test_inner_sensitivity_v2_process.py \
    test_inner_sensitivity_v2_runner.py
)

"$FC" -std=f2008 -O0 -Wall -Wextra -Werror -Wno-compare-reals \
  -fcheck=all -ffp-contract=off -fno-fast-math \
  -I "$GANLIB_MOD" \
  "$ROOT/validation/iterative/check_one_map_xsm.f90" \
  "$GANLIB_LIB" -lstdc++ -o "$WORK/check_one"

"$FC" -std=f2008 -O0 -Wall -Wextra -Werror -Wno-compare-reals \
  -fcheck=all -ffp-contract=off -fno-fast-math \
  -I "$GANLIB_MOD" \
  "$ROOT/validation/iterative/check_inner_sensitivity_v2_balance_xsm.f90" \
  "$GANLIB_LIB" -lstdc++ -o "$WORK/check_balance"

"$FC" -std=f2008 -O0 -Wall -Wextra -Werror -Wno-compare-reals \
  -fcheck=all -ffp-contract=off -fno-fast-math \
  -I "$GANLIB_MOD" \
  "$ROOT/validation/iterative/check_inner_sensitivity_xsm.f90" \
  "$GANLIB_LIB" -lstdc++ -o "$WORK/check_pair"

(
  cd "$ROOT/validation/artifacts/iterative-map1"
  "$WORK/check_one" \
    basis_reference.xsm state1_system.xsm \
    state0_axial.xsm state1_axial.xsm state1_snapshots.xsm \
    > "$WORK/one.log"
)

(
  cd "$ROOT/validation/artifacts"
  "$WORK/check_balance" \
    iterative-seed/initial_axial_track.xsm \
    iterative-seed/initial_axial_macrolib.xsm \
    iterative-map1/state1_system.xsm \
    iterative-map1/state1_axial.xsm LEGACY-ANCHOR \
    > "$WORK/balance.log"
)

grep -Fqx \
  "INNER-SENSITIVITY-V2 BALANCE GLOBAL/GROUP/GALERKIN-BITS 3177D0FB 3B539AEF 351ECCBD" \
  "$WORK/balance.log"
grep -Fqx \
  "INNER-SENSITIVITY-V2 LEGACY-ANCHOR BITWISE PASS" \
  "$WORK/balance.log"

(
  cd "$ROOT/validation/artifacts/iterative-map1"
  "$WORK/check_pair" \
    state0_axial.xsm state1_axial.xsm \
    state0_axial.xsm state1_axial.xsm \
    state1_snapshots.xsm state1_snapshots.xsm V2-2H \
    > "$WORK/pair.log"
)

PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/check_inner_sensitivity_v2_result.py" \
  "$WORK/pair.log" \
  "$ROOT/validation/iterative/one_map_scientific.sha256" \
  "$ROOT/validation/iterative/inner_sensitivity_v2_protocol.json" \
  --artifact-dir "$ROOT/validation/artifacts/iterative-map1" \
  --mode capture > "$WORK/result.json"

PYTHONDONTWRITEBYTECODE=1 python3 -c \
  'import json,sys; data=json.load(open(sys.argv[1])); assert data["classification"] == "PENDING-REPLAY"; assert len(data["components"]) == 4' \
  "$WORK/result.json"

PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/check_inner_sensitivity_v2_implementation.py"

echo "INNER-SENSITIVITY-V2 TESTS PASS: DRAGON-RUNS=0"
