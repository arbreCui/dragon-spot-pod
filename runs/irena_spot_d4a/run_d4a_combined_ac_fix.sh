#!/bin/sh
#----
# run_d4a_combined_ac_fix.sh -- W4 D4-A combined A/C FIX
#   (snapshot once, BACKUP into SNAP_A AND SNAP_C, then run
#    PASS A on SNAP_A and PASS C on SNAP_C; ~11h estimated)
#----
set -eu

ROOT="/Users/wen/spot"
RUN="$ROOT/runs/irena_spot_d4a"
LIB="/Users/wen/dragon-5.1/Dragon/irena_colorset_assembly_pin"
DAT="$ROOT/data/rnr_0burn_spot_proc"
MAIN="$ROOT/data"

cd "$RUN"

rm -f _DUMMY _main* _SpotPodMic* _SpotPodEps* _Snap1Ring* _Spot* _assert* _rnr* \
      DUMMYSQ TRACK_f TRACK_T_f TRACK_FUEL_f \
      glowpost_d4a_fix.eps \
      irena_assembly_tiso_1_12_1ring.dat \
      SpotPodMic.c2m  SpotPodMic.l2m  SpotPodMic.o2m \
      SpotPodEps.c2m  SpotPodEps.l2m  SpotPodEps.o2m \
      Snap1Ring.c2m   Snap1Ring.l2m   Snap1Ring.o2m \
      assertS.c2m     assertS.l2m     assertS.o2m \
      rnr_cc.c2m      rnr_cc.l2m      rnr_cc.o2m \
      rnr_interpol.c2m rnr_interpol.l2m rnr_interpol.o2m \
      DLIB8R1_370 \
      d4a_combined_ac_fix.log d4a_combined_ac_fix.err 2>/dev/null || true

ln -sf "$LIB/DLIB_370" DLIB8R1_370
ln -sf "$DAT/irena_assembly_tiso_1_12_1ring.dat" .
ln -sf "$MAIN/SpotPodEps.c2m"   .
ln -sf "$MAIN/Snap1Ring.c2m"    .
ln -sf "$MAIN/assertS.c2m"      .
ln -sf "$DAT/rnr_cc.c2m"        .
ln -sf "$DAT/rnr_interpol.c2m"  .

echo "==> running Dragon on d4a_combined_ac_fix.x2m (~11h estimated)"
"$ROOT/bin/Darwin_arm64/Dragon" < d4a_combined_ac_fix.x2m \
    > d4a_combined_ac_fix.log 2> d4a_combined_ac_fix.err
echo "==> Dragon exit OK; log: d4a_combined_ac_fix.log"
