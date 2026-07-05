#!/bin/sh
#----
# run_d4a_converged_ac.sh -- D4-A converged A/C, ledger-governed
#
# First ledger-governed experiment after the 2026-05-02 evidence pivot.
# Replaces stage-1 SpotPodEps with outer-iter SpotPodItr.
#
# Estimated wall: ~12-15h (snapshot phase ~9h + 2 outer-iter SPOT
# passes ~2-3h each). Run overnight.
#
# Uses PATCHED live binary; frozen prod cannot run outer iter.
#
# Diagnostic verdict (look in log after run):
#   SpotPodItr: outer iter 1 K=  1.163428e+00  errspo=  1.0E10  (PASS A iter 1)
#   SpotPodItr: outer iter N K=  ???           errspo=  ?E-?   (converged)
#   SpotPodItr: done. converged= 1  final K_SPOT= ???           (PASS A converged)
#   ... same for PASS C
#
# After run:
#   1. Add new run_id `d4a_converged_ac` to SPOT_doc/evidence_ledger.md
#      with K_iter1 / K_converged / errspo / status
#   2. Update handoff §5 D4-A converged row: TODO -> done with K values
#----
set -eu

ROOT="/Users/wen/spot"
RUN="$ROOT/runs/irena_spot_d4a"
LIB="/Users/wen/dragon-5.1/Dragon/irena_colorset_assembly_pin/assembly"
DAT="$ROOT/data/rnr_0burn_spot_proc"
MAIN="$ROOT/data"

cd "$RUN"

rm -f _DUMMY _main* _SpotPodMic* _SpotPodEps* _SpotPodItr* _Snap1Ring* _Spot* _assert* _rnr* \
      DUMMYSQ TRACK_f TRACK_T_f TRACK_FUEL_f \
      glowpost_d4a_converged.eps \
      irena_assembly_tiso_1_12_1ring.dat \
      SpotPodItr.c2m  SpotPodItr.l2m  SpotPodItr.o2m \
      Snap1Ring.c2m   Snap1Ring.l2m   Snap1Ring.o2m \
      assertS.c2m     assertS.l2m     assertS.o2m \
      rnr_cc.c2m      rnr_cc.l2m      rnr_cc.o2m \
      rnr_interpol.c2m rnr_interpol.l2m rnr_interpol.o2m \
      DLIB8R1_370 \
      d4a_converged_ac.log d4a_converged_ac.err 2>/dev/null || true

ln -sf "$LIB/DLIB_370" DLIB8R1_370
ln -sf "$DAT/irena_assembly_tiso_1_12_1ring.dat" .
ln -sf "$MAIN/SpotPodItr.c2m"   .
ln -sf "$MAIN/Snap1Ring.c2m"    .
ln -sf "$MAIN/assertS.c2m"      .
ln -sf "$DAT/rnr_cc.c2m"        .
ln -sf "$DAT/rnr_interpol.c2m"  .

echo "==> running Dragon (PATCHED) on d4a_converged_ac.x2m (~12-15h estimated)"
"$ROOT/bin/Darwin_arm64/Dragon" < d4a_converged_ac.x2m \
    > d4a_converged_ac.log 2> d4a_converged_ac.err
echo "==> Dragon exit; log: d4a_converged_ac.log"
echo ""
echo "==> Quick verdict (grep for outer-iter trace):"
grep -E "SpotPodItr: outer iter|SpotPodItr: done|D4-A CONVERGED K_|Delta-rho_AC" d4a_converged_ac.log 2>/dev/null | tail -30 || echo "    (no match — run failed or log truncated)"
echo ""
echo "==> NEXT STEPS:"
echo "    1. Add run_id 'd4a_converged_ac' to SPOT_doc/evidence_ledger.md"
echo "    2. Update handoff §5 D4-A converged row"
echo "    3. Compare Delta-rho_AC to D3 sanity -17.8 pcm reference"
