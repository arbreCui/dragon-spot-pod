#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../.." && pwd)
TOOLS="$ROOT/validation/iterative"
PARENT="$ROOT/validation/artifacts/iterative-rank2-h2-r64dp2-picard-fixedpoint/fixedpoint-map"
SEED="$ROOT/validation/artifacts/iterative-seed"
BASIS="$ROOT/validation/artifacts/iterative-rank2-basis/rank2_basis.xsm"
DRAGON="$ROOT/bin/Darwin_arm64/Dragon"

# The repository-complete CLOSED/69 pair is a pre-Gram seed.  This runner
# recomputes one map with the current binary and contract; it is a current-code
# physics regression, not a claim that the seed is the current fixed point.

if [ "$#" -gt 1 ]; then
  echo "usage: $0 [fresh-output-directory]" >&2
  exit 2
fi
if [ "$#" -eq 1 ]; then
  WORK=$1
  if [ -e "$WORK" ]; then
    echo "output directory must be fresh: $WORK" >&2
    exit 2
  fi
  mkdir -p "$WORK"
else
  WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-pin-current.XXXXXX")
fi
WORK=$(CDPATH= cd -- "$WORK" && pwd)

make -C "$ROOT/src" -j2 >/dev/null
make -C "$TOOLS" -j2 >/dev/null

ln -s "$PARENT/candidate_axial_closed.xsm" "$WORK/parent_axial_closed.xsm"
ln -s "$PARENT/candidate_snapshots_closed.xsm" "$WORK/parent_snapshots_closed.xsm"
ln -s "$SEED/initial_radial_track.bin" "$WORK/initial_radial_track.bin"
ln -s "$SEED/initial_axial_track.xsm" "$WORK/initial_axial_track.xsm"
ln -s "$SEED/initial_axial_macrolib.xsm" "$WORK/initial_axial_macrolib.xsm"
ln -s "$BASIS" "$WORK/basis_reference.xsm"
cp "$ROOT/data/SpotStepR64.c2m" "$WORK/SpotStepR64.c2m"
cp "$TOOLS/pin_current_picard_radial.x2m" "$WORK/radial.x2m"
cp "$TOOLS/pin_current_picard_axial.x2m" "$WORK/axial.x2m"
cp "$TOOLS/pin_current_checker_parent.x2m" "$WORK/checker_parent.x2m"

cd "$WORK"
"$TOOLS/make_route_contract" route_contract.xsm PIN-RANK2 \
  2.5e-7 5.0e-8 1.0e-5 500 740 3 3 B0 > contract.log
"$TOOLS/prepare_r64_next_projected" \
  parent_axial_closed.xsm parent_snapshots_closed.xsm \
  initial_axial_track.xsm route_contract.xsm projected_proposal.xsm \
  > prepare.log

OMP_NUM_THREADS=1 python3 "$TOOLS/run_bounded_dragon.py" \
  "$DRAGON" "$WORK/radial.x2m" "$WORK/radial.log" 120
"$TOOLS/admit_candidate_radial" candidate_radial.xsm route_contract.xsm \
  > admission.log
OMP_NUM_THREADS=1 python3 "$TOOLS/run_bounded_dragon.py" \
  "$DRAGON" "$WORK/axial.x2m" "$WORK/axial.log" 80
"$TOOLS/close_r64_returned" \
  candidate_axial.xsm candidate_snapshots.xsm route_contract.xsm \
  closed_axial.xsm closed_snapshots.xsm > close.log

python3 "$TOOLS/run_bounded_dragon.py" \
  "$DRAGON" "$WORK/checker_parent.x2m" "$WORK/checker_parent.log" 5
"$TOOLS/check_one_map_xsm" --continued \
  basis_reference.xsm candidate_system.xsm parent_for_checker.xsm \
  candidate_axial.xsm candidate_snapshots.xsm > independent_check.log
"$TOOLS/check_convergence_gate" closed_axial.xsm > gate.log
grep -q '^CLASSIFICATION=VALID_MET$' gate.log

shasum -a 256 \
  parent_axial_closed.xsm parent_snapshots_closed.xsm \
  initial_radial_track.bin initial_axial_track.xsm \
  initial_axial_macrolib.xsm basis_reference.xsm route_contract.xsm \
  > input_manifest.sha256
shasum -a 256 \
  candidate_system.xsm candidate_radial.xsm candidate_axial.xsm \
  candidate_snapshots.xsm closed_axial.xsm closed_snapshots.xsm \
  > output_manifest.sha256

cat independent_check.log
cat gate.log
echo "PIN CURRENT-CODE PICARD REPLAY PASS: $WORK"
