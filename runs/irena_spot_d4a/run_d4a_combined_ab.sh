#!/bin/sh
#----
# run_d4a_combined_ab.sh -- W4 D4-A combined A/B (snapshot once, two ε)
#----
set -eu

ROOT="/Users/ww/phdCode/5.1-main2026-spot/Dragon"
RUN="$ROOT/runs/irena_spot_d4a"
LIB="/Users/ww/phdCode/libraries/l_endian"
DAT="$ROOT/data/rnr_0burn_spot_proc"
MAIN="$ROOT/data"

cd "$RUN"

rm -f _DUMMY _main* _SpotPodMic* _Snap1Ring* _Spot* _assert* _rnr* \
      DUMMYSQ TRACK_f TRACK_T_f TRACK_FUEL_f \
      glowpost_d4a.eps \
      irena_assembly_tiso_1_12_1ring.dat \
      SpotPodMic.c2m  SpotPodMic.l2m  SpotPodMic.o2m \
      SpotPodEps.c2m  SpotPodEps.l2m  SpotPodEps.o2m \
      Snap1Ring.c2m  Snap1Ring.l2m  Snap1Ring.o2m \
      assertS.c2m assertS.l2m assertS.o2m \
      rnr_cc.c2m rnr_cc.l2m rnr_cc.o2m \
      rnr_interpol.c2m rnr_interpol.l2m rnr_interpol.o2m \
      DLIB8R1_366 \
      d4a_combined_ab.log d4a_combined_ab.err 2>/dev/null || true

ln -sf "$LIB/draglibendfb8r1SHEM366_v5p1" DLIB8R1_366
ln -sf "$DAT/irena_assembly_tiso_1_12_1ring.dat" .
ln -sf "$MAIN/SpotPodEps.c2m"   .
ln -sf "$MAIN/Snap1Ring.c2m"    .
ln -sf "$MAIN/assertS.c2m"      .
ln -sf "$DAT/rnr_cc.c2m"        .
ln -sf "$DAT/rnr_interpol.c2m"  .

echo "==> running Dragon on d4a_combined_ab.x2m (~12h estimated)"
"$ROOT/bin/Darwin_arm64/Dragon" < d4a_combined_ab.x2m \
    > d4a_combined_ab.log 2> d4a_combined_ab.err
echo "==> Dragon exit OK; log: d4a_combined_ab.log"
