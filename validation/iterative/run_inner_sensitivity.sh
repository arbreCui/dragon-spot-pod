#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
DRAGON_BIN=${DRAGON_BIN:?set DRAGON_BIN to the frozen Stage-3 executable}
SEED_DIR=${SEED_DIR:-"$ROOT/validation/artifacts/iterative-seed"}
BASELINE_DIR=${BASELINE_DIR:-"$ROOT/validation/artifacts/iterative-map1"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}
H2_REFERENCE=${H2_REFERENCE:-}
if [ -n "$H2_REFERENCE" ]; then
  case "$H2_REFERENCE" in
    /*) ;;
    *) H2_REFERENCE="$PWD/$H2_REFERENCE" ;;
  esac
  test -f "$H2_REFERENCE"
fi

REFERENCE="$ROOT/validation/iterative/inner_sensitivity_reference.sha256"
DECK="$ROOT/validation/iterative/inner_sensitivity_map.x2m"
PROTOCOL="$ROOT/validation/iterative/inner_sensitivity_protocol.json"

test -x "$DRAGON_BIN"
test -f "$GANLIB_LIB"
test -f "$GANLIB_MOD/ganlib.mod"

expected_hash() {
  awk -v file="$1" '$2 == file { print $1 }' "$REFERENCE"
}

require_hash() {
  label=$1
  path=$2
  expected=$(expected_hash "$label")
  test -n "$expected"
  actual=$(shasum -a 256 "$path" | awk '{ print $1 }')
  if [ "$actual" != "$expected" ]; then
    echo "INNER-SENSITIVITY INPUT HASH FAIL: $label" >&2
    exit 1
  fi
}

validate_h2_reference() {
  awk '
    BEGIN {
      expected[1] = "basis_reference.xsm"
      expected[2] = "state0_axial.xsm"
      expected[3] = "state1_system.xsm"
      expected[4] = "state1_axial.xsm"
      expected[5] = "state1_snapshots.xsm"
    }
    {
      digest = substr($0, 1, 64)
      separator = substr($0, 65, 2)
      name = substr($0, 67)
      if (NR > 5 || length(digest) != 64 ||
          digest ~ /[^0-9a-f]/ || separator != "  " ||
          name != expected[NR]) {
        exit 1
      }
    }
    END {
      if (NR != 5) {
        exit 1
      }
    }
  ' "$1" || {
    echo "INNER-SENSITIVITY FAIL: invalid five-file H2 reference." >&2
    exit 1
  }
}

PYTHONDONTWRITEBYTECODE=1 python3 -m json.tool "$PROTOCOL" >/dev/null
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/check_inner_sensitivity_contract.py" >/dev/null
if [ -n "$H2_REFERENCE" ]; then
  validate_h2_reference "$H2_REFERENCE"
fi

require_hash Dragon "$DRAGON_BIN"
require_hash one_corrected_map.x2m \
  "$ROOT/validation/iterative/one_corrected_map.x2m"
require_hash SpotRefFS.c2m "$ROOT/data/SpotRefFS.c2m"
require_hash SpotPlaneFS.c2m "$ROOT/data/SpotPlaneFS.c2m"
for name in initial_snapshots.xsm initial_axial_track.xsm \
  initial_axial_macrolib.xsm initial_radial_track.bin
do
  require_hash "$name" "$SEED_DIR/$name"
done
for name in basis_reference.xsm state0_axial.xsm state1_system.xsm \
  state1_axial.xsm state1_snapshots.xsm
do
  require_hash "$name" "$BASELINE_DIR/$name"
done

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-inner-sensitivity.XXXXXX")
cleanup() {
  if [ "${KEEP_WORK:-0}" = 1 ]; then
    printf 'INNER-SENSITIVITY WORKDIR: %s\n' "$WORK"
  else
    rm -rf "$WORK"
  fi
}
trap cleanup EXIT HUP INT TERM

for name in initial_snapshots.xsm initial_axial_track.xsm \
  initial_axial_macrolib.xsm initial_radial_track.bin
do
  cp "$SEED_DIR/$name" "$WORK/$name"
done
cp "$ROOT/data/SpotRefFS.c2m" "$ROOT/data/SpotPlaneFS.c2m" "$WORK/"
if [ -n "$H2_REFERENCE" ]; then
  cp "$H2_REFERENCE" "$WORK/h2_reference.sha256"
  cmp "$H2_REFERENCE" "$WORK/h2_reference.sha256"
  validate_h2_reference "$WORK/h2_reference.sha256"
fi
mkdir -p "$WORK/base"
cp "$BASELINE_DIR/state0_axial.xsm" "$WORK/base/x0.xsm"
cp "$BASELINE_DIR/state1_axial.xsm" "$WORK/base/x1.xsm"
cp "$BASELINE_DIR/state1_snapshots.xsm" "$WORK/base/snap1.xsm"

"$FC" -std=f2008 -O0 -Wall -Wextra -Werror -Wno-compare-reals \
  -fcheck=all -ffp-contract=off -fno-fast-math -I "$GANLIB_MOD" \
  "$ROOT/validation/iterative/check_one_map_xsm.f90" \
  "$GANLIB_LIB" -lstdc++ -o "$WORK/check_one_map_xsm"
"$FC" -std=f2008 -O0 -Wall -Wextra -Werror -Wno-compare-reals \
  -fcheck=all -ffp-contract=off -fno-fast-math -I "$GANLIB_MOD" \
  "$ROOT/validation/iterative/check_inner_sensitivity_xsm.f90" \
  "$GANLIB_LIB" -lstdc++ -o "$WORK/check_inner_sensitivity_xsm"

for source in check_one_map_xsm.f90 check_inner_sensitivity_xsm.f90
do
  if rg -i '\b(LCMPUT|LCMPTC|LCMPPD|LCMLID|LCMLIL|LCMEQU|LCMDEL)\b' \
    "$ROOT/validation/iterative/$source" >/dev/null
  then
    echo "INNER-SENSITIVITY FAIL: checker contains LCM mutation." >&2
    exit 1
  fi
done
for checker in check_one_map_xsm check_inner_sensitivity_xsm
do
  nm "$WORK/$checker" > "$WORK/$checker.nm"
  if rg -i 'SPOASM|SPOPOD|SPOT1P|SPOFSRC|SPOFCHK|SPOGBAL|SPOPROJ|SPOSTATE|SPOXCONV|Dragon' \
    "$WORK/$checker.nm" >/dev/null
  then
    echo "INNER-SENSITIVITY FAIL: checker links solver symbols." >&2
    exit 1
  fi
  rg -i 'lcmop' "$WORK/$checker.nm" >/dev/null
done

shasum -a 256 \
  "$DRAGON_BIN" "$DECK" "$PROTOCOL" "$REFERENCE" \
  "$ROOT/validation/iterative/one_corrected_map.x2m" \
  "$ROOT/validation/iterative/check_inner_sensitivity_contract.py" \
  "$ROOT/validation/iterative/check_inner_sensitivity_status.py" \
  "$ROOT/validation/iterative/check_one_map_runtime.py" \
  "$ROOT/validation/iterative/check_one_map_xsm.f90" \
  "$ROOT/validation/iterative/check_inner_sensitivity_xsm.f90" \
  "$ROOT/validation/iterative/run_inner_sensitivity.sh" \
  "$WORK/check_one_map_xsm" "$WORK/check_inner_sensitivity_xsm" \
  "$WORK/SpotRefFS.c2m" "$WORK/SpotPlaneFS.c2m" \
  "$WORK/initial_snapshots.xsm" "$WORK/initial_axial_track.xsm" \
  "$WORK/initial_axial_macrolib.xsm" \
  "$WORK/initial_radial_track.bin" \
  "$WORK/base/x0.xsm" "$WORK/base/x1.xsm" "$WORK/base/snap1.xsm" \
  > "$WORK/input_manifest.sha256"
if [ -n "$H2_REFERENCE" ]; then
  shasum -a 256 "$H2_REFERENCE" "$WORK/h2_reference.sha256" \
    >> "$WORK/input_manifest.sha256"
  cmp "$H2_REFERENCE" "$WORK/h2_reference.sha256"
fi

(
  cd "$WORK"
  "$DRAGON_BIN" < "$DECK" > inner_sensitivity.log 2>&1
)

PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/check_one_map_runtime.py" \
  "$WORK/inner_sensitivity.log" > "$WORK/runtime_check.log"

(
  cd "$WORK"
  ./check_one_map_xsm basis_reference.xsm state1_system.xsm \
    state0_axial.xsm state1_axial.xsm state1_snapshots.xsm \
    > h2_one_map_xsm_check.log
  ./check_inner_sensitivity_xsm \
    base/x0.xsm base/x1.xsm state0_axial.xsm state1_axial.xsm \
    base/snap1.xsm state1_snapshots.xsm \
    > inner_sensitivity_xsm_check.log
)

cmp "$BASELINE_DIR/basis_reference.xsm" "$WORK/basis_reference.xsm"
cmp "$BASELINE_DIR/state0_axial.xsm" "$WORK/state0_axial.xsm"

if [ -n "$H2_REFERENCE" ]; then
  (
    cd "$WORK"
    shasum -a 256 -c h2_reference.sha256
  ) > "$WORK/h2_replay_check.log"
else
  echo "INNER-SENSITIVITY H2 REPLAY PENDING" \
    > "$WORK/h2_replay_check.log"
fi

if [ -n "$H2_REFERENCE" ]; then
  PYTHONDONTWRITEBYTECODE=1 python3 \
    "$ROOT/validation/iterative/check_inner_sensitivity_status.py" \
    "$WORK/inner_sensitivity_xsm_check.log" "$PROTOCOL" --replay \
    > "$WORK/inner_sensitivity_status.log"
else
  PYTHONDONTWRITEBYTECODE=1 python3 \
    "$ROOT/validation/iterative/check_inner_sensitivity_status.py" \
    "$WORK/inner_sensitivity_xsm_check.log" "$PROTOCOL" \
    > "$WORK/inner_sensitivity_status.log"
fi

shasum -a 256 -c "$WORK/input_manifest.sha256" \
  > "$WORK/input_replay_check.log"
if [ -n "$H2_REFERENCE" ]; then
  cmp "$H2_REFERENCE" "$WORK/h2_reference.sha256"
fi

shasum -a 256 \
  "$WORK/input_manifest.sha256" \
  "$WORK/input_replay_check.log" \
  "$WORK/basis_reference.xsm" "$WORK/state0_axial.xsm" \
  "$WORK/state1_system.xsm" "$WORK/state1_axial.xsm" \
  "$WORK/state1_snapshots.xsm" "$WORK/inner_sensitivity.log" \
  "$WORK/runtime_check.log" "$WORK/h2_one_map_xsm_check.log" \
  "$WORK/inner_sensitivity_xsm_check.log" \
  "$WORK/inner_sensitivity_status.log" \
  "$WORK/h2_replay_check.log" \
  "$WORK/check_one_map_xsm.nm" \
  "$WORK/check_inner_sensitivity_xsm.nm" \
  > "$WORK/artifact_manifest.sha256"
if [ -n "$H2_REFERENCE" ]; then
  shasum -a 256 "$WORK/h2_reference.sha256" \
    >> "$WORK/artifact_manifest.sha256"
fi

require_hash Dragon "$DRAGON_BIN"
require_hash one_corrected_map.x2m \
  "$ROOT/validation/iterative/one_corrected_map.x2m"
require_hash SpotRefFS.c2m "$ROOT/data/SpotRefFS.c2m"
require_hash SpotPlaneFS.c2m "$ROOT/data/SpotPlaneFS.c2m"
require_hash SpotRefFS.c2m "$WORK/SpotRefFS.c2m"
require_hash SpotPlaneFS.c2m "$WORK/SpotPlaneFS.c2m"
for name in initial_snapshots.xsm initial_axial_track.xsm \
  initial_axial_macrolib.xsm initial_radial_track.bin
do
  require_hash "$name" "$SEED_DIR/$name"
  require_hash "$name" "$WORK/$name"
done
require_hash state0_axial.xsm "$WORK/base/x0.xsm"
require_hash state1_axial.xsm "$WORK/base/x1.xsm"
require_hash state1_snapshots.xsm "$WORK/base/snap1.xsm"
for name in basis_reference.xsm state0_axial.xsm state1_system.xsm \
  state1_axial.xsm state1_snapshots.xsm
do
  require_hash "$name" "$BASELINE_DIR/$name"
done

cat "$WORK/runtime_check.log"
cat "$WORK/h2_one_map_xsm_check.log"
cat "$WORK/inner_sensitivity_xsm_check.log"
cat "$WORK/inner_sensitivity_status.log"
cat "$WORK/h2_replay_check.log"
echo "INNER-SENSITIVITY INPUT REPLAY PASS"
cat "$WORK/input_manifest.sha256"
cat "$WORK/artifact_manifest.sha256"
if [ -n "$H2_REFERENCE" ]; then
  echo "INNER-SENSITIVITY REPLAY EXECUTION PASS: Stage-4 machine status is reported above; outer convergence was not evaluated."
else
  echo "INNER-SENSITIVITY CAPTURE PASS: Stage 4 is not qualified without a fresh h/2 replay; outer convergence was not evaluated."
fi
