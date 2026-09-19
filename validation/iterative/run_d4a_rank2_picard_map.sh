#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../.." && pwd)
TOOLS="$ROOT/validation/iterative"
DRAGON="$ROOT/bin/Darwin_arm64/Dragon"
CHECK_MODE=${CHECK_MODE:---continued}
: "${RADIAL_TIMEOUT_SECONDS:?set an explicit bounded wall time for the radial half-step}"
: "${AXIAL_TIMEOUT_SECONDS:?set an explicit bounded wall time for the axial half-step}"

if [ "$#" -ne 2 ]; then
  echo "usage: $0 parent-map-directory fresh-output-directory" >&2
  exit 2
fi

case "$CHECK_MODE" in
  --continued|--reencoded) ;;
  *) echo "CHECK_MODE must be --continued or --reencoded" >&2; exit 2 ;;
esac

PARENT=$(CDPATH= cd -- "$1" && pwd)
WORK=$2
if [ -e "$WORK" ]; then
  echo "output directory must be fresh: $WORK" >&2
  exit 2
fi
mkdir -p "$WORK"
WORK=$(CDPATH= cd -- "$WORK" && pwd)

for name in closed_axial.xsm closed_snapshots.xsm \
  initial_radial_track.bin initial_axial_track.xsm \
  initial_axial_macrolib.xsm basis_reference.xsm route_contract.xsm
do
  if [ ! -f "$PARENT/$name" ]; then
    echo "missing parent input: $PARENT/$name" >&2
    exit 2
  fi
done

make -C "$ROOT/src" -j2 >/dev/null
make -C "$TOOLS" -j2 >/dev/null

ln -s "$PARENT/closed_axial.xsm" "$WORK/parent_axial_closed.xsm"
ln -s "$PARENT/closed_snapshots.xsm" "$WORK/parent_snapshots_closed.xsm"
ln -s "$PARENT/initial_radial_track.bin" "$WORK/initial_radial_track.bin"
ln -s "$PARENT/initial_axial_track.xsm" "$WORK/initial_axial_track.xsm"
ln -s "$PARENT/initial_axial_macrolib.xsm" "$WORK/initial_axial_macrolib.xsm"
ln -s "$PARENT/basis_reference.xsm" "$WORK/basis_reference.xsm"
ln -s "$PARENT/route_contract.xsm" "$WORK/route_contract.xsm"
cp "$ROOT/data/SpotStepR64.c2m" "$WORK/SpotStepR64.c2m"
cp "$TOOLS/d4a_rank2_picard_radial.x2m" "$WORK/radial.x2m"
cp "$TOOLS/d4a_rank2_picard_axial.x2m" "$WORK/axial.x2m"
cp "$TOOLS/d4a_rank2_checker_parent.x2m" "$WORK/checker_parent.x2m"

cd "$WORK"
"$TOOLS/prepare_r64_next_projected" \
  parent_axial_closed.xsm parent_snapshots_closed.xsm \
  initial_axial_track.xsm route_contract.xsm projected_proposal.xsm \
  > prepare.log

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

shasum -a 256 \
  parent_axial_closed.xsm parent_snapshots_closed.xsm \
  initial_radial_track.bin initial_axial_track.xsm \
  initial_axial_macrolib.xsm basis_reference.xsm route_contract.xsm \
  projected_proposal.xsm > input_manifest.sha256
shasum -a 256 \
  candidate_system.xsm candidate_radial.xsm candidate_axial.xsm \
  candidate_snapshots.xsm closed_axial.xsm closed_snapshots.xsm \
  > output_manifest.sha256

cat independent_check.log
cat gate.log
echo "D4A RANK-2 PICARD MAP COMPLETE: $WORK"
