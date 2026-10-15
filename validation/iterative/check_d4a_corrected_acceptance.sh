#!/bin/sh
# Read-only corrected D4-A acceptance gate.  It performs no transport solve;
# FINAL-K-POWER is independently replayed through GREP + SPORATE.
set -u

PATH=/usr/bin:/bin:/usr/sbin:/sbin
export PATH

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TOOLS="$ROOT/validation/iterative"
CANONICAL_DRAGON="$ROOT/bin/Darwin_arm64/Dragon"
CANONICAL_OBSERVABLE_DECK="$TOOLS/d4a_corrected_final_observables.x2m"
CANONICAL_OBSERVABLE_REPLAY="$TOOLS/verify_d4a_corrected_observables.sh"
CANONICAL_BOUNDED_RUNNER="$TOOLS/run_bounded_dragon.py"
OBSERVABLE_DECK_SHA=46a70e2e1ed83b37b03d6a472bf94224557119c358a27fdc1875115f0f569259
OBSERVABLE_REPLAY_SHA=4984c1986cfc8320b3b394e49b8a197f2d9f2e646897d76e422acf74480b737c
BOUNDED_RUNNER_SHA=bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09
REPAIRED_DRAGON_SHA=873ad14272a2f0765d95e6de067194a01708ccf9aa88d58cd782049e6d331fef
REPAIRED_RUNTIME_SHA=8888d5772c39472fe4d4895120737370fd471200c4ace9e7bf41ed8c7e74db1b
REPAIRED_BOOTSTRAP_SHA=acab72a87521339f9eb0540130d0fc4ea1946b59df6bb5db4fcb83cd3528eb1c
MESH12_RUNTIME_SHA=af7069315a59ae6de9c0bd3edd6f497bf4dcaef1140917b4239c32bcff8da12b
MESH12_BOOTSTRAP_SHA=805c06e1ec873809a890be3a90afe1b8c16ec57272c3eaa5c315aa8feb64b32f

# Release acceptance is not a test-injection surface.  A caller may repeat
# the canonical absolute value, but may not substitute a checker or Dragon.
if [ "${CHECKER_DIR+x}" = x ] && [ "$CHECKER_DIR" != "$TOOLS" ]; then
  echo "D4A-CORRECTED-ACCEPT CONFIG FAIL: CHECKER_DIR override refused" >&2
  exit 2
fi
if [ "${DRAGON_BIN+x}" = x ] && [ "$DRAGON_BIN" != "$CANONICAL_DRAGON" ]; then
  echo "D4A-CORRECTED-ACCEPT CONFIG FAIL: DRAGON_BIN override refused" >&2
  exit 2
fi
CHECKER_DIR=$TOOLS
OBSERVABLES_DIR=${D4A_OBSERVABLES_DIR:-}
RUNTIME=
BOOTSTRAP=
while [ "$#" -gt 0 ]; do
  case "$1" in
    --repaired-runtime)
      [ "$#" -ge 2 ] && [ -z "$RUNTIME" ] || exit 2
      RUNTIME=$(CDPATH= cd -- "$2" 2>/dev/null && pwd -P) || exit 2
      shift 2 ;;
    --repaired-bootstrap)
      [ "$#" -ge 2 ] && [ -z "$BOOTSTRAP" ] || exit 2
      BOOTSTRAP=$(CDPATH= cd -- "$2" 2>/dev/null && pwd -P) || exit 2
      shift 2 ;;
    --*) echo "unknown acceptance option: $1" >&2; exit 2 ;;
    *) break ;;
  esac
done
if { [ -n "$RUNTIME" ] && [ -z "$BOOTSTRAP" ]; } ||
   { [ -z "$RUNTIME" ] && [ -n "$BOOTSTRAP" ]; }; then
  echo 'D4A-CORRECTED-ACCEPT CONFIG FAIL: repaired runtime and bootstrap are required together' >&2
  exit 2
fi

if [ "$#" -lt 1 ]; then
  echo "usage: D4A_OBSERVABLES_DIR=/path/to/observables $0 [--repaired-runtime directory --repaired-bootstrap directory] corrected-snapshot-build [map1 ...]" >&2
  exit 2
fi

BUILD=$1
shift
case "$BUILD" in
  /*) ;;
  *) BUILD=$(CDPATH= cd -- "$BUILD" 2>/dev/null && pwd) || exit 2 ;;
esac

overall=0
pass() { echo "D4A-CORRECTED-ACCEPT $1 PASS: $2"; }
fail() { echo "D4A-CORRECTED-ACCEPT $1 FAIL: $2"; overall=1; }
hash() { shasum -a 256 "$1" 2>/dev/null | awk '{print $1}'; }
same() { test -f "$1" && test -f "$2" && test "$(hash "$1")" = "$(hash "$2")"; }
verify() { test -s "$1/$2" && (cd "$1" && shasum -a 256 -c "$2" >/dev/null 2>&1); }
has_entry() {
  awk -v name="$3" 'NF == 2 && $2 == name && length($1) == 64 &&
    $1 !~ /[^0-9a-f]/ {n++} END {exit n != 1}' "$1/$2" 2>/dev/null
}
count_fixed() { grep -F -c "$1" "$2" 2>/dev/null || true; }

# Only this explicit entry may select the separately verified repair epoch.
# BUILD remains the original snapshot/rank provenance, never an old CLOSED parent.
if [ -n "$RUNTIME" ]; then
  # Two independently verified epochs, paired rather than interchangeable.
  if [ "$(hash "$RUNTIME/runtime.sha256")" = "$MESH12_RUNTIME_SHA" ]; then
    REPAIRED_RUNTIME_SHA=$MESH12_RUNTIME_SHA
    REPAIRED_BOOTSTRAP_SHA=$MESH12_BOOTSTRAP_SHA
  fi
  if [ "$(hash "$RUNTIME/runtime.sha256")" != "$REPAIRED_RUNTIME_SHA" ] ||
     ! verify "$RUNTIME" runtime.sha256 ||
     [ "$(hash "$BOOTSTRAP/result.sha256")" != "$REPAIRED_BOOTSTRAP_SHA" ] ||
     ! verify "$BOOTSTRAP" result.sha256; then
    fail REPAIR-EPOCH "repaired runtime/bootstrap identity or manifest differs"
    exit 1
  fi
  for name in Dragon check_one_map_xsm check_convergence_gate; do
    if [ ! -f "$RUNTIME/$name" ] || [ -L "$RUNTIME/$name" ] ||
       [ ! -x "$RUNTIME/$name" ]; then
      fail REPAIR-EPOCH "missing regular executable $name"
      exit 1
    fi
  done
  if [ "$(hash "$RUNTIME/Dragon")" != "$REPAIRED_DRAGON_SHA" ]; then
    fail REPAIR-EPOCH "repaired Dragon identity differs"
    exit 1
  fi
  CHECKER_DIR=$RUNTIME
  CANONICAL_DRAGON="$RUNTIME/Dragon"
  CANONICAL_BOUNDED_RUNNER="$RUNTIME/run_bounded_dragon.py"
  pass REPAIR-EPOCH "explicit sealed repaired runtime and CLOSED/0 selected"
else
  BOOTSTRAP=$BUILD
fi

CC_SHA=594e9e58aae950b003bd410440928c97b59cf67f70844033c69c05b78e8565b5
INTERPOL_SHA=255ddfc61a61026e0f36aefe5ad4cee0b41871fdbd25e2b77c540bd9bccb8ed2
AUDIT="$ROOT/validation/d4_reference/material_epoch_audit_result.md"

material_ok=1
test -f "$AUDIT" || material_ok=0
test "$(count_fixed '`PASS_REVIEWED_MATERIAL_INPUT_NO_TRANSPORT`.' "$AUDIT")" = 1 || material_ok=0
test "$(hash "$BUILD/rnr_cc.c2m")" = "$CC_SHA" || material_ok=0
test "$(hash "$BUILD/rnr_interpol.c2m")" = "$INTERPOL_SHA" || material_ok=0
grep -Fq "$CC_SHA  data/rnr_0burn_spot_proc/rnr_cc.c2m" \
  "$BUILD/frozen_repository_inputs.sha256" 2>/dev/null || material_ok=0
grep -Fq "$INTERPOL_SHA  data/rnr_0burn_spot_proc/rnr_interpol.c2m" \
  "$BUILD/frozen_repository_inputs.sha256" 2>/dev/null || material_ok=0
if [ "$material_ok" -eq 1 ]; then
  pass MATERIAL "reviewed corrected rnr_cc/rnr_interpol hashes match executed inputs"
else
  fail MATERIAL "corrected material audit or executed input hashes are missing/mismatched"
fi

snapshot_ok=1
verify "$BUILD" admitted_snapshot_archive.sha256 || snapshot_ok=0
for name in d4a_snapshots.xsm d4a_three_snapshots.log snapshot_check.log \
  snapshot_check.err run_contract.txt executed_inputs.sha256 \
  frozen_repository_inputs.sha256 snapshot_build_result.sha256 \
  dragon_executable.sha256
do
  has_entry "$BUILD" admitted_snapshot_archive.sha256 "$name" || snapshot_ok=0
done
SNAP_CHECK="$BUILD/snapshot_check.log"
test "$(count_fixed 'D4A-SNAPSHOT TUPLE NSNAP=3 NGRP=370 NREG=132 NMAT=6 NSURF=12 NUNK=144' "$SNAP_CHECK")" = 1 || snapshot_ok=0
test "$(count_fixed 'D4A-SNAPSHOT ARCHIVE GANLIB-ONLY PASS' "$SNAP_CHECK")" = 1 || snapshot_ok=0
test -f "$BUILD/snapshot_check.err" && test ! -s "$BUILD/snapshot_check.err" || snapshot_ok=0
test "$(grep -c '^ FLU2DR-TERM OUTER-GATE=PASS ' "$BUILD/d4a_three_snapshots.log" 2>/dev/null || true)" = 3 || snapshot_ok=0
if [ "$snapshot_ok" -eq 1 ]; then
  pass SNAPSHOTS "three corrected 370-group/132-region snapshots independently admitted"
else
  fail SNAPSHOTS "snapshot manifest, strict terminals, or independent receipt failed"
fi

rank_ok=1
verify "$BUILD" d4a_rank2_admitted.sha256 || rank_ok=0
for name in d4a_snapshots.xsm d4a_rank2_basis.xsm d4a_axial_track.xsm \
  d4a_axial_macrolib.xsm d4a_rank2_check.log d4a_rank2_check.err
do
  has_entry "$BUILD" d4a_rank2_admitted.sha256 "$name" || rank_ok=0
done
RANK_CHECK="$BUILD/d4a_rank2_check.log"
test "$(count_fixed 'D4A-RANK2 DIMENSIONS NGRP=370 NREG2D=132 NSNAP=3 NMODE=2' "$RANK_CHECK")" = 1 || rank_ok=0
test "$(count_fixed 'D4A-RANK2 STORED-DIAGNOSTICS BITWISE PASS' "$RANK_CHECK")" = 1 || rank_ok=0
test "$(count_fixed 'D4A-RANK2 GANLIB-ONLY PASS' "$RANK_CHECK")" = 1 || rank_ok=0
test -f "$BUILD/d4a_rank2_check.err" && test ! -s "$BUILD/d4a_rank2_check.err" || rank_ok=0
if [ "$snapshot_ok" -ne 1 ]; then rank_ok=0; fi
if [ "$rank_ok" -eq 1 ]; then
  pass RANK2 "fixed NMODE=2 basis is hash-tied to the corrected snapshots"
else
  fail RANK2 "rank-2 manifest or independent fixed-basis receipt failed"
fi

closed_ok=1
bootstrap_receipt=d4a_bootstrap_result.sha256
bootstrap_radial_log=d4a_refresh_r64.log
bootstrap_seal_log=b2i_bootstrap.log
if [ -n "$RUNTIME" ]; then
  bootstrap_receipt=result.sha256
  bootstrap_radial_log=radial.log
  bootstrap_seal_log=b2i_seal_bootstrap.log
  same "$BOOTSTRAP/d4a_snapshots.xsm" "$BUILD/d4a_snapshots.xsm" || closed_ok=0
  same "$BOOTSTRAP/route_contract.xsm" "$BUILD/route_contract.xsm" || closed_ok=0
  same "$BOOTSTRAP/initial_radial_track.bin" "$BUILD/initial_radial_track.bin" || closed_ok=0
else
  same "$BOOTSTRAP/initial_axial_track.xsm" "$BUILD/d4a_axial_track.xsm" || closed_ok=0
fi
verify "$BOOTSTRAP" "$bootstrap_receipt" || closed_ok=0
for name in basis_reference.xsm route_contract.xsm closed_axial.xsm \
  closed_snapshots.xsm initial_radial_track.bin initial_axial_track.xsm \
  initial_axial_macrolib.xsm d4a_refreshed_snapshots.xsm \
  "$bootstrap_radial_log" "$bootstrap_seal_log"
do
  has_entry "$BOOTSTRAP" "$bootstrap_receipt" "$name" || closed_ok=0
done
test "$(count_fixed 'SPOT-R64 B2I BOOTSTRAP COMMITTED CLOSED/0' "$BOOTSTRAP/$bootstrap_seal_log")" = 1 || closed_ok=0
test "$(grep -c '^>|SPOT-REFRESH-R64-RESULT' "$BOOTSTRAP/$bootstrap_radial_log" 2>/dev/null || true)" = 3 || closed_ok=0
test "$(grep -c '^>|D4A-R64-REFRESH-COMPLETE' "$BOOTSTRAP/$bootstrap_radial_log" 2>/dev/null || true)" = 1 || closed_ok=0
same "$BOOTSTRAP/basis_reference.xsm" "$BUILD/d4a_rank2_basis.xsm" || closed_ok=0
same "$BOOTSTRAP/initial_axial_macrolib.xsm" "$BUILD/d4a_axial_macrolib.xsm" || closed_ok=0
# The repair's axial TRACK comes from the independently checked new seed,
# pinned by REPAIRED_BOOTSTRAP_SHA; its complete XSM hash differs from the old
# seed's TRACK. Every new map must retain that exact repaired TRACK below.
if [ "$rank_ok" -ne 1 ]; then closed_ok=0; fi
if [ "$closed_ok" -eq 1 ]; then
  pass CLOSED0 "corrected TYPE-S bridge committed the canonical CLOSED/0 pair"
else
  fail CLOSED0 "no fully manifested corrected CLOSED/0 bootstrap"
fi

map_count=$#
map_ok=1
final_map=
if [ "$closed_ok" -ne 1 ]; then
  map_ok=0
elif [ "$map_count" -eq 0 ]; then
  map_ok=0
else
  previous_axial="$BOOTSTRAP/closed_axial.xsm"
  previous_snapshots="$BOOTSTRAP/closed_snapshots.xsm"
  index=0
  for directory in "$@"; do
    index=$((index + 1))
    case "$directory" in
      /*) ;;
      *) directory=$(CDPATH= cd -- "$directory" 2>/dev/null && pwd) || { map_ok=0; break; } ;;
    esac
    test -d "$directory" || { map_ok=0; break; }
    if [ -n "$RUNTIME" ]; then
      repair_map_ok=1
      verify "$directory" result.sha256 || repair_map_ok=0
      verify "$directory" parent_inputs.sha256 || repair_map_ok=0
      for name in input_manifest.sha256 output_manifest.sha256 parent_inputs.sha256 \
        parent_for_checker.xsm prepare.log admission.log close.log independent_check.log \
        gate.log runtime/runtime.sha256 runtime/Dragon
      do
        has_entry "$directory" result.sha256 "$name" || repair_map_ok=0
      done
      same "$directory/runtime/runtime.sha256" "$RUNTIME/runtime.sha256" || repair_map_ok=0
      verify "$directory/runtime" runtime.sha256 || repair_map_ok=0
      if [ "$repair_map_ok" -ne 1 ]; then map_ok=0; break; fi
    fi
    verify "$directory" input_manifest.sha256 || map_ok=0
    verify "$directory" output_manifest.sha256 || map_ok=0
    for name in parent_axial_closed.xsm parent_snapshots_closed.xsm \
      initial_radial_track.bin initial_axial_track.xsm \
      initial_axial_macrolib.xsm basis_reference.xsm route_contract.xsm \
      projected_proposal.xsm
    do
      has_entry "$directory" input_manifest.sha256 "$name" || map_ok=0
    done
    for name in candidate_system.xsm candidate_radial.xsm candidate_axial.xsm \
      candidate_snapshots.xsm closed_axial.xsm closed_snapshots.xsm
    do
      has_entry "$directory" output_manifest.sha256 "$name" || map_ok=0
    done
    same "$directory/parent_axial_closed.xsm" "$previous_axial" || map_ok=0
    same "$directory/parent_snapshots_closed.xsm" "$previous_snapshots" || map_ok=0
    same "$directory/basis_reference.xsm" "$BOOTSTRAP/basis_reference.xsm" || map_ok=0
    same "$directory/route_contract.xsm" "$BOOTSTRAP/route_contract.xsm" || map_ok=0
    same "$directory/initial_axial_track.xsm" "$BOOTSTRAP/initial_axial_track.xsm" || map_ok=0
    same "$directory/initial_axial_macrolib.xsm" "$BOOTSTRAP/initial_axial_macrolib.xsm" || map_ok=0
    same "$directory/initial_radial_track.bin" "$BOOTSTRAP/initial_radial_track.bin" || map_ok=0
    grep -Fxq "SPOT-R64 B2J CLOSED/$((index - 1)) -> PROJECTED/$index" "$directory/prepare.log" 2>/dev/null || map_ok=0
    grep -Fxq 'H2-X2 R64 RETURNED PRODUCTION-ADMISSION PASS STATUS=3' "$directory/admission.log" 2>/dev/null || map_ok=0
    grep -Fxq 'SPOT-R64 B2W CLOSE PASS STATUS=2' "$directory/close.log" 2>/dev/null || map_ok=0
    grep -Fxq "SPOT-R64 CLOSED/$index COMPLETE NO-TRANSPORT" "$directory/close.log" 2>/dev/null || map_ok=0

    tmp_map=$(mktemp "${TMPDIR:-/tmp}/d4a-map-check.XXXXXX") || exit 2
    tmp_gate=$(mktemp "${TMPDIR:-/tmp}/d4a-gate-check.XXXXXX") || exit 2
    if [ "$index" -eq 1 ]; then
      check_mode=--reencoded
    else
      check_mode=--continued
    fi
    if [ ! -x "$CHECKER_DIR/check_one_map_xsm" ] || \
       [ ! -x "$CHECKER_DIR/check_convergence_gate" ]; then
      map_ok=0
    elif ! (cd "$directory" && "$CHECKER_DIR/check_one_map_xsm" "$check_mode" \
      basis_reference.xsm candidate_system.xsm parent_for_checker.xsm \
      candidate_axial.xsm candidate_snapshots.xsm > "$tmp_map" 2>/dev/null); then
      map_ok=0
    elif ! cmp -s "$tmp_map" "$directory/independent_check.log"; then
      map_ok=0
    elif ! (cd "$directory" && "$CHECKER_DIR/check_convergence_gate" \
      closed_axial.xsm > "$tmp_gate" 2>/dev/null); then
      map_ok=0
    elif ! cmp -s "$tmp_gate" "$directory/gate.log"; then
      map_ok=0
    fi
    rm -f "$tmp_map" "$tmp_gate"
    if [ -n "$RUNTIME" ]; then
      verify "$directory" result.sha256 || map_ok=0
    fi

    grep -Fxq 'ONE-MAP-XSM POD-PACKAGE BITWISE PASS' "$directory/independent_check.log" 2>/dev/null || map_ok=0
    grep -Fxq 'ONE-MAP-XSM RADIAL-OP LIVE-CHANGE PASS' "$directory/independent_check.log" 2>/dev/null || map_ok=0
    grep -Fxq 'ONE-MAP-XSM RAW-DEFECT BITWISE PASS' "$directory/independent_check.log" 2>/dev/null || map_ok=0
    grep -Fxq 'ONE-MAP-XSM COMPLETE' "$directory/independent_check.log" 2>/dev/null || map_ok=0
    if [ -n "$RUNTIME" ] && [ "$map_ok" -eq 1 ]; then
      pass MAP-REPLAY "CLOSED/$index lineage and independent logs verify; final gate evaluated separately"
    fi
    if [ "$index" -lt "$map_count" ]; then
      grep -Fxq 'CLASSIFICATION=VALID_NOT_MET' "$directory/gate.log" 2>/dev/null || map_ok=0
    else
      grep -Fxq 'CLASSIFICATION=VALID_MET' "$directory/gate.log" 2>/dev/null || map_ok=0
    fi
    previous_axial="$directory/closed_axial.xsm"
    previous_snapshots="$directory/closed_snapshots.xsm"
    final_map=$directory
  done
fi

if [ "$map_ok" -eq 1 ]; then
  pass MAPS "$map_count corrected direct-Picard receipt(s) form CLOSED/0 through the first VALID_MET map"
else
  fail MAPS "missing, unlinked, legacy, independently rejected receipt, or no final VALID_MET"
fi

if [ "$map_ok" -eq 1 ] && \
   grep -Eq '^SPOT-GATE THRESHOLD +4\.9999999999999998E-07$' "$final_map/gate.log" && \
   test "$(grep -Ec '^SPOT-GATE (RRHO|RLEAK|RA) +[^ ]+ +PASS +$' "$final_map/gate.log")" = 3
then
  residuals=$(grep -E '^SPOT-GATE (RRHO|RLEAK|RA) ' "$final_map/gate.log" | tr '\n' ';')
  pass FINAL-RESIDUALS "$residuals"
else
  fail FINAL-RESIDUALS "no corrected final map with all three defects <= 5e-7"
fi

observables_ok=1
if [ "$map_ok" -ne 1 ] || [ -z "$OBSERVABLES_DIR" ]; then
  observables_ok=0
else
  case "$OBSERVABLES_DIR" in
    /*) ;;
    *) OBSERVABLES_DIR=$(CDPATH= cd -- "$OBSERVABLES_DIR" 2>/dev/null && pwd) || observables_ok=0 ;;
  esac
  verify "$OBSERVABLES_DIR" observables.sha256 || observables_ok=0
  for name in closed_axial.xsm initial_axial_track.xsm \
    initial_axial_macrolib.xsm observables.x2m observables.log
  do
    has_entry "$OBSERVABLES_DIR" observables.sha256 "$name" || observables_ok=0
  done
  same "$OBSERVABLES_DIR/closed_axial.xsm" "$final_map/closed_axial.xsm" || observables_ok=0
  same "$OBSERVABLES_DIR/initial_axial_track.xsm" "$final_map/initial_axial_track.xsm" || observables_ok=0
  same "$OBSERVABLES_DIR/initial_axial_macrolib.xsm" "$final_map/initial_axial_macrolib.xsm" || observables_ok=0
  OBS_LOG="$OBSERVABLES_DIR/observables.log"
  test "$(grep -c '^>|D4A-CORRECTED-K-EFFECTIVE ' "$OBS_LOG" 2>/dev/null || true)" = 1 || observables_ok=0
  test "$(grep -c '^SPORATE NU-FISSION-FRACTIONS ' "$OBS_LOG" 2>/dev/null || true)" = 1 || observables_ok=0
  test "$(grep -c 'normal end of execution for dragon' "$OBS_LOG" 2>/dev/null || true)" = 1 || observables_ok=0
  grep -Eiq 'D4A-MAP8|LEGACY|XABORT|ABORT:|FATAL|fortran runtime error' "$OBS_LOG" 2>/dev/null && observables_ok=0
  awk '/^SPORATE NU-FISSION-FRACTIONS / {n++; s=$3+$4+$5} END {exit !(n==1 && s>=0.99999995 && s<=1.00000005)}' "$OBS_LOG" 2>/dev/null || observables_ok=0
  if [ -n "$RUNTIME" ]; then
    EXPECTED_DRAGON_SHA=$REPAIRED_DRAGON_SHA
  else
    dragon_hash_count=$(grep -Ec '^[0-9a-f]{64}  /[^ ]*/Dragon$' \
      "$BUILD/dragon_executable.sha256" 2>/dev/null || true)
    if [ "$dragon_hash_count" -eq 1 ]; then
      EXPECTED_DRAGON_SHA=$(awk '{print $1}' \
        "$BUILD/dragon_executable.sha256")
    else
      EXPECTED_DRAGON_SHA=
      observables_ok=0
    fi
  fi
  test -f "$CANONICAL_OBSERVABLE_DECK" && \
    test ! -L "$CANONICAL_OBSERVABLE_DECK" && \
    test "$(hash "$CANONICAL_OBSERVABLE_DECK")" = "$OBSERVABLE_DECK_SHA" || \
    observables_ok=0
  test -f "$CANONICAL_OBSERVABLE_REPLAY" && \
    test ! -L "$CANONICAL_OBSERVABLE_REPLAY" && \
    test -x "$CANONICAL_OBSERVABLE_REPLAY" && \
    test "$(hash "$CANONICAL_OBSERVABLE_REPLAY")" = "$OBSERVABLE_REPLAY_SHA" || \
    observables_ok=0
  test -f "$CANONICAL_BOUNDED_RUNNER" && \
    test ! -L "$CANONICAL_BOUNDED_RUNNER" && \
    test "$(hash "$CANONICAL_BOUNDED_RUNNER")" = "$BOUNDED_RUNNER_SHA" || \
    observables_ok=0
  test -f "$CANONICAL_DRAGON" && test ! -L "$CANONICAL_DRAGON" && \
    test -x "$CANONICAL_DRAGON" && \
    test "$(hash "$CANONICAL_DRAGON")" = "$EXPECTED_DRAGON_SHA" || \
    observables_ok=0
  if [ "$observables_ok" -eq 1 ]; then
    "$CANONICAL_OBSERVABLE_REPLAY" \
      "$CANONICAL_DRAGON" "$EXPECTED_DRAGON_SHA" \
      "$CANONICAL_OBSERVABLE_DECK" "$OBSERVABLE_DECK_SHA" \
      "$CANONICAL_BOUNDED_RUNNER" "$BOUNDED_RUNNER_SHA" \
      "$OBSERVABLES_DIR" >/dev/null 2>&1 || observables_ok=0
  fi
fi
if [ "$observables_ok" -eq 1 ]; then
  k=$(grep '^>|D4A-CORRECTED-K-EFFECTIVE ' "$OBS_LOG" | awk '{print $2}')
  power=$(grep '^SPORATE NU-FISSION-FRACTIONS ' "$OBS_LOG" | cut -d' ' -f2-)
  pass FINAL-K-POWER "k=$k; $power"
else
  fail FINAL-K-POWER "no sealed corrected final k and normalized three-floor power output"
fi

if [ -n "$RUNTIME" ]; then
  if ! verify "$BOOTSTRAP" result.sha256 ||
     ! verify "$RUNTIME" runtime.sha256 ||
     ! verify "$BUILD" admitted_snapshot_archive.sha256 ||
     ! verify "$BUILD" d4a_rank2_admitted.sha256; then
    fail IMMUTABLE-INPUTS "sealed inputs changed during acceptance"
  fi
fi
if [ "$overall" -eq 0 ]; then
  echo 'D4A-CORRECTED-ACCEPT OVERALL PASS'
  exit 0
fi
echo 'D4A-CORRECTED-ACCEPT OVERALL FAIL-CLOSED'
exit 1
