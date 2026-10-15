#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../.." && pwd)
TOOLS="$ROOT/validation/iterative"
DRAGON="$ROOT/bin/Darwin_arm64/Dragon"
# This corrected route uses the executable already pinned by the CLOSED/0
# release checker. Building belongs to setup, never to a frozen map run.
EXPECTED_DRAGON_SHA=2908cf383be163cb0534847fe7115d42c9deed97684c28abdd9c29f24c6722db
REPAIRED_RUNTIME_SHA=8888d5772c39472fe4d4895120737370fd471200c4ace9e7bf41ed8c7e74db1b
REPAIRED_BOOTSTRAP_SHA=acab72a87521339f9eb0540130d0fc4ea1946b59df6bb5db4fcb83cd3528eb1c
REPAIRED_TRACK_SHA=6e90eda20bc4807f80467c54127ea33065ea60eca59800a57c61a77206e64589
MESH12_RUNTIME_SHA=af7069315a59ae6de9c0bd3edd6f497bf4dcaef1140917b4239c32bcff8da12b
MESH12_BOOTSTRAP_SHA=805c06e1ec873809a890be3a90afe1b8c16ec57272c3eaa5c315aa8feb64b32f
MESH12_TRACK_SHA=a6ad22a6c0bc997b195f3b62f22fe799d6115ba3e7b2cb14c5c05e49955cbf03
hash() { shasum -a 256 "$1" | awk '{print $1}'; }
PROCEDURE_DIR="$ROOT/data"
RUNTIME=
PREFLIGHT_ONLY=0
while [ "$#" -gt 0 ]; do
  case "$1" in
    --repaired-runtime)
      [ "$#" -ge 2 ] || exit 2
      RUNTIME=$(CDPATH= cd -- "$2" && pwd)
      TOOLS=$RUNTIME
      PROCEDURE_DIR=$RUNTIME
      DRAGON="$RUNTIME/Dragon"
      EXPECTED_DRAGON_SHA=873ad14272a2f0765d95e6de067194a01708ccf9aa88d58cd782049e6d331fef
      shift 2 ;;
    --preflight-only) PREFLIGHT_ONLY=1; shift ;;
    *) break ;;
  esac
done
if [ "$PREFLIGHT_ONLY" -eq 0 ]; then
  : "${RADIAL_TIMEOUT_SECONDS:?set an explicit bounded wall time for the radial half-step}"
  : "${AXIAL_TIMEOUT_SECONDS:?set an explicit bounded wall time for the axial half-step}"
  for limit in "$RADIAL_TIMEOUT_SECONDS" "$AXIAL_TIMEOUT_SECONDS"; do
    case "$limit" in ''|*[!0-9]*) echo 'wall caps must be positive integers' >&2; exit 2 ;; esac
    [ "$limit" -gt 0 ] || exit 2
  done
fi

if [ "$#" -ne 2 ]; then
  echo "usage: $0 [--repaired-runtime directory] [--preflight-only] parent-map-directory fresh-output-directory" >&2
  exit 2
fi

PARENT=$(CDPATH= cd -- "$1" && pwd)
WORK=$2
if [ -e "$WORK" ] || [ -L "$WORK" ]; then
  echo "output directory must be fresh: $WORK" >&2
  exit 2
fi
for name in closed_axial.xsm closed_snapshots.xsm \
  initial_radial_track.bin initial_axial_track.xsm \
  initial_axial_macrolib.xsm basis_reference.xsm route_contract.xsm
do
  if [ ! -f "$PARENT/$name" ]; then
    echo "missing parent input: $PARENT/$name" >&2
    exit 2
  fi
done

RUNTIME_FILES="Dragon prepare_r64_next_projected admit_candidate_radial close_r64_returned check_one_map_xsm check_convergence_gate run_bounded_dragon.py SpotStepR64.c2m d4a_rank2_picard_radial.x2m d4a_rank2_picard_axial.x2m d4a_rank2_checker_parent.x2m"
if [ -n "$RUNTIME" ]; then
  # Bind each registered checker/runtime to its own bootstrap and mesh.
  # This is checked before any output or host/transport invocation.
  EXPECTED_RUNTIME_SHA=$REPAIRED_RUNTIME_SHA
  EXPECTED_BOOTSTRAP_SHA=$REPAIRED_BOOTSTRAP_SHA
  EXPECTED_TRACK_SHA=$REPAIRED_TRACK_SHA
  if [ "$(hash "$RUNTIME/runtime.sha256")" = "$MESH12_RUNTIME_SHA" ]; then
    EXPECTED_RUNTIME_SHA=$MESH12_RUNTIME_SHA
    EXPECTED_BOOTSTRAP_SHA=$MESH12_BOOTSTRAP_SHA
    EXPECTED_TRACK_SHA=$MESH12_TRACK_SHA
  fi
  if [ "$(hash "$RUNTIME/runtime.sha256")" != "$EXPECTED_RUNTIME_SHA" ]; then
    echo 'unregistered repaired runtime; no map started' >&2
    exit 2
  fi
  for name in $RUNTIME_FILES; do
    [ -f "$RUNTIME/$name" ] && [ ! -L "$RUNTIME/$name" ] || exit 2
    grep -Eq "^[0-9a-f]{64}  $name\$" "$RUNTIME/runtime.sha256" || exit 2
  done
  (cd "$RUNTIME" && shasum -a 256 -c runtime.sha256) > /dev/null
  # The repaired chain accepts sealed parents only; no old-epoch relabelling.
  for name in closed_axial.xsm closed_snapshots.xsm initial_radial_track.bin \
    initial_axial_track.xsm initial_axial_macrolib.xsm basis_reference.xsm route_contract.xsm
  do
    grep -Eq "^[0-9a-f]{64}  $name\$" "$PARENT/result.sha256" || exit 2
  done
  (cd "$PARENT" && shasum -a 256 -c result.sha256) > /dev/null
  if [ "$(hash "$PARENT/initial_axial_track.xsm")" != "$EXPECTED_TRACK_SHA" ]; then
    echo 'parent axial mesh differs from the selected runtime epoch; no map started' >&2
    exit 2
  fi
  if [ "$(hash "$PARENT/result.sha256")" != "$EXPECTED_BOOTSTRAP_SHA" ]; then
    # A subsequent CLOSED state must carry this exact runtime, not merely
    # the same Dragon executable shared by both numerical meshes.
    grep -Fxq "$EXPECTED_RUNTIME_SHA  runtime/runtime.sha256" "$PARENT/result.sha256" || {
      echo 'parent is neither the selected bootstrap nor its runtime continuation; no map started' >&2
      exit 2
    }
  fi
  grep -Eq "^$EXPECTED_DRAGON_SHA  (runtime/)?Dragon\$" "$PARENT/result.sha256" || {
    echo 'parent does not belong to the repaired runtime; no map started' >&2
    exit 2
  }
fi

if [ ! -f "$DRAGON" ] || [ -L "$DRAGON" ] || [ ! -x "$DRAGON" ]; then
  echo "missing regular executable canonical Dragon" >&2
  exit 2
fi
if [ "$(shasum -a 256 "$DRAGON" | awk '{print $1}')" != "$EXPECTED_DRAGON_SHA" ]; then
  echo "canonical Dragon content hash differs; no map started" >&2
  exit 2
fi
for name in prepare_r64_next_projected admit_candidate_radial \
  close_r64_returned check_one_map_xsm check_convergence_gate
do
  if [ ! -f "$TOOLS/$name" ] || [ -L "$TOOLS/$name" ] || [ ! -x "$TOOLS/$name" ]; then
    echo "missing regular executable host tool: $name; build during setup" >&2
    exit 2
  fi
done

if [ "$PREFLIGHT_ONLY" -eq 1 ]; then
  echo 'D4A PICARD PREFLIGHT PASS NO-TRANSPORT NO-OUTPUT'
  exit 0
fi

mkdir -p "$WORK"
WORK=$(CDPATH= cd -- "$WORK" && pwd)
if [ -n "$RUNTIME" ]; then
  mkdir "$WORK/runtime"
  for name in $RUNTIME_FILES runtime.sha256; do
    cp -p "$RUNTIME/$name" "$WORK/runtime/$name"
  done
  (cd "$WORK/runtime" && shasum -a 256 -c runtime.sha256) > /dev/null
  TOOLS="$WORK/runtime"
  DRAGON="$TOOLS/Dragon"
  PROCEDURE_DIR=$TOOLS
fi

ln -s "$PARENT/closed_axial.xsm" "$WORK/parent_axial_closed.xsm"
ln -s "$PARENT/closed_snapshots.xsm" "$WORK/parent_snapshots_closed.xsm"
ln -s "$PARENT/initial_radial_track.bin" "$WORK/initial_radial_track.bin"
ln -s "$PARENT/initial_axial_track.xsm" "$WORK/initial_axial_track.xsm"
ln -s "$PARENT/initial_axial_macrolib.xsm" "$WORK/initial_axial_macrolib.xsm"
ln -s "$PARENT/basis_reference.xsm" "$WORK/basis_reference.xsm"
ln -s "$PARENT/route_contract.xsm" "$WORK/route_contract.xsm"
cp "$PROCEDURE_DIR/SpotStepR64.c2m" "$WORK/SpotStepR64.c2m"
cp "$TOOLS/d4a_rank2_picard_radial.x2m" "$WORK/radial.x2m"
cp "$TOOLS/d4a_rank2_picard_axial.x2m" "$WORK/axial.x2m"
cp "$TOOLS/d4a_rank2_checker_parent.x2m" "$WORK/checker_parent.x2m"
cp "$HERE/$(basename -- "$0")" "$WORK/map_runner.sh"

cd "$WORK"
shasum -a 256 parent_axial_closed.xsm parent_snapshots_closed.xsm \
  initial_radial_track.bin initial_axial_track.xsm initial_axial_macrolib.xsm \
  basis_reference.xsm route_contract.xsm SpotStepR64.c2m radial.x2m axial.x2m \
  checker_parent.x2m map_runner.sh > parent_inputs.sha256
"$TOOLS/prepare_r64_next_projected" \
  parent_axial_closed.xsm parent_snapshots_closed.xsm \
  initial_axial_track.xsm route_contract.xsm projected_proposal.xsm \
  > prepare.log
if grep -Fxq 'SPOT-R64 B2J CLOSED/0 -> PROJECTED/1' prepare.log; then
  CHECK_MODE=--reencoded
elif grep -Eq '^SPOT-R64 B2J CLOSED/[1-9][0-9]* -> PROJECTED/[0-9]+$' \
    prepare.log; then
  CHECK_MODE=--continued
else
  echo "unable to classify the sealed parent epoch" >&2
  exit 2
fi

OMP_NUM_THREADS=1 python3 "$TOOLS/run_bounded_dragon.py" \
  "$DRAGON" "$WORK/radial.x2m" "$WORK/radial.log" \
  "$RADIAL_TIMEOUT_SECONDS" \
  > radial.runner.log
"$TOOLS/admit_candidate_radial" candidate_radial.xsm route_contract.xsm \
  > admission.log

OMP_NUM_THREADS=1 python3 "$TOOLS/run_bounded_dragon.py" \
  "$DRAGON" "$WORK/axial.x2m" "$WORK/axial.log" \
  "$AXIAL_TIMEOUT_SECONDS" \
  > axial.runner.log
"$TOOLS/close_r64_returned" \
  candidate_axial.xsm candidate_snapshots.xsm route_contract.xsm \
  closed_axial.xsm closed_snapshots.xsm > close.log

python3 "$TOOLS/run_bounded_dragon.py" \
  "$DRAGON" "$WORK/checker_parent.x2m" "$WORK/checker_parent.log" 5 \
  > checker_parent.runner.log
"$TOOLS/check_one_map_xsm" "$CHECK_MODE" \
  basis_reference.xsm candidate_system.xsm parent_for_checker.xsm \
  candidate_axial.xsm candidate_snapshots.xsm > independent_check.log
"$TOOLS/check_convergence_gate" closed_axial.xsm > gate.log
grep -Eq '^CLASSIFICATION=VALID_(MET|NOT_MET)$' gate.log
grep -q '^SPOT-GATE COMPLETE$' gate.log
shasum -a 256 -c parent_inputs.sha256 > /dev/null
if [ -n "$RUNTIME" ]; then
  (cd "$TOOLS" && shasum -a 256 -c runtime.sha256) > /dev/null
fi

shasum -a 256 \
  parent_axial_closed.xsm parent_snapshots_closed.xsm \
  initial_radial_track.bin initial_axial_track.xsm \
  initial_axial_macrolib.xsm basis_reference.xsm route_contract.xsm \
  projected_proposal.xsm > input_manifest.sha256
shasum -a 256 \
  candidate_system.xsm candidate_radial.xsm candidate_axial.xsm \
  candidate_snapshots.xsm closed_axial.xsm closed_snapshots.xsm \
  > output_manifest.sha256
if [ -n "$RUNTIME" ]; then
  # Include the copied runtime and both parent identities in the sealed receipt.
  for path in ./* runtime/*; do
    [ "$path" != './result.sha256' ] || continue
    [ -f "$path" ] || continue
    shasum -a 256 "${path#./}"
  done > result.sha256
fi

cat independent_check.log
cat gate.log
echo "D4A RANK-2 PICARD MAP COMPLETE: $WORK"
