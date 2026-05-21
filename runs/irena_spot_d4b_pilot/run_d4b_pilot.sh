#!/bin/sh
#----
# run_d4b_pilot.sh -- D4-B pilot multi-ring 1/12 converged A/C
#
# First multi-ring (4 MOX rings per pin) experiment, N=207 regions
# (vs D4-A N=132). Pilot for D4-B/C rank-vs-N math figure.
#
# Estimated wall: ~50-60h CPU (4-MOX-ring TONE ~2x slower than 1-ring,
# 5 snapshots ~12h, PASS A ~5 outer iter ~20h, PASS C ~6 outer iter
# ~24h). Run overnight + half a day.
#
# Uses PATCHED live binary; frozen prod cannot run outer iter.
#
# Diagnostic verdict (look in log after run):
#   SnapMring: snap K_TYPEK_radial = ... (T_comb=750, 4-ring)
#   SpotPodItr: outer iter N K=  ???           errspo=  ?E-?   (converged)
#   SpotPodItr: done. converged= 1  final K_SPOT= ???
#
# After run:
#   1. Add run_id `d4b_pilot_converged_ac` to SPOT_doc/evidence_ledger.md
#      with K_A, K_C, ΔK·1e5 (POD truncation cost)
#   2. Extract SPOPOD spectrum (singular values) — this is the PILOT
#      data point for rank-vs-N. Look for 'SPOPOD: group' lines in log.
#   3. Decide whether to launch D4-C (~14× larger N=1802) based on
#      whether D4-B SPOPOD spectrum shows non-trivial rank.
#----
set -eu

ROOT="/Users/wen/spot"
RUN="$ROOT/runs/irena_spot_d4b_pilot"
LIB="/Users/wen/dragon-5.1/Dragon/irena_colorset_assembly_pin"
DAT="$ROOT/data/rnr_0burn_spot_proc"
MAIN="$ROOT/data"

cd "$RUN"

# Explicit cleanup (no globs to avoid zsh NULL_GLOB issues per
# memory `feedback_diff_before_transport.md` and the d4a_uniform v3
# dragging-glob bug)
rm -f _DUMMY _main001 _main002 _main003 _main004 _main005 \
      _SpotPodItr001 _SpotPodItr002 _SnapMring001 _SnapMring002 \
      _Snap1Ring001 _Snap1Ring002 _Spot001 _assertS001 \
      _rnr_cc001 _rnr_cc002 _rnr_interpol001 _rnr_interpol002 \
      DUMMYSQ TRACK_f TRACK_T_f TRACK_FUEL_f \
      glowpost_d4b_pilot.eps \
      irena_assembly_tiso_1_12.dat \
      SpotPodItr.c2m  SpotPodItr.l2m  SpotPodItr.o2m \
      SnapMring.c2m   SnapMring.l2m   SnapMring.o2m \
      assertS.c2m     assertS.l2m     assertS.o2m \
      rnr_cc.c2m      rnr_cc.l2m      rnr_cc.o2m \
      rnr_interpol.c2m rnr_interpol.l2m rnr_interpol.o2m \
      DLIB8R1_370 \
      d4b_pilot.log d4b_pilot.err 2>/dev/null || true

ln -sf "$LIB/DLIB_370" DLIB8R1_370
ln -sf "$DAT/irena_assembly_tiso_1_12.dat" .
ln -sf "$MAIN/SpotPodItr.c2m"   .
ln -sf "$MAIN/SnapMring.c2m"    .
ln -sf "$MAIN/assertS.c2m"      .
ln -sf "$DAT/rnr_cc.c2m"        .
ln -sf "$DAT/rnr_interpol.c2m"  .

echo "==> running Dragon (PATCHED) on d4b_pilot_converged_ac.x2m (~50-60h estimated)"
"$ROOT/bin/Darwin_arm64/Dragon" < d4b_pilot_converged_ac.x2m \
    > d4b_pilot.log 2> d4b_pilot.err
echo "==> Dragon exit; log: d4b_pilot.log"
echo ""
echo "==> Quick verdict (grep for outer-iter trace + SPOPOD spectrum):"
grep -E "SpotPodItr: outer iter|SpotPodItr: done|D4-B PILOT K_|Delta-rho_AC|SnapMring: snap K_TYPEK_radial|SPOPOD: group" d4b_pilot.log 2>/dev/null | tail -40 || echo "    (no match — run failed or log truncated)"
echo ""
echo "==> NEXT STEPS:"
echo "    1. Add run_id 'd4b_pilot_converged_ac' to SPOT_doc/evidence_ledger.md"
echo "    2. Extract SPOPOD spectrum from log (rank vs N pilot data point)"
echo "    3. Decide D4-C launch based on rank pattern"
