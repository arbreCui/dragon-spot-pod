#!/bin/sh
#----
# run_d3_het_baseline.sh -- W4 D3 heterogeneous 5-snapshot baseline
#
# Pincell, 5 fuel temperatures (600/700/750/800/900 C). eps_pod=0.
# Output: ./d3_het.log
#----
set -eu

ROOT="/Users/wen/spot"
RUN="$ROOT/runs/irena_spot_d3"
LIB="/Users/wen/dragon-5.1/Dragon/irena_colorset_assembly_pin/pincell"
DAT="$ROOT/data/rnr_0burn_spot_proc"
MAIN="$ROOT/data"

cd "$RUN"

rm -f _DUMMY _main* _SpotPodMic* _SpotSnapBld* _Spot* _assert* _rnr* \
      DUMMYSQ TRACK_f TRACK_FUEL_f \
      glowpost_d3.eps \
      irena_pincell.dat \
      SpotPodMic.c2m  SpotPodMic.l2m  SpotPodMic.o2m \
      SpotSnapBld.c2m SpotSnapBld.l2m SpotSnapBld.o2m \
      assertS.c2m assertS.l2m assertS.o2m \
      rnr_cc.c2m rnr_cc.l2m rnr_cc.o2m \
      rnr_interpol.c2m rnr_interpol.l2m rnr_interpol.o2m \
      DLIB8R1_370 \
      d3_het.log d3_het.err 2>/dev/null || true

ln -sf "$LIB/DLIB_370" DLIB8R1_370
ln -sf "$DAT/irena_pincell.dat" .
ln -sf "$MAIN/SpotPodMic.c2m"      .
ln -sf "$MAIN/SpotSnapBld.c2m"   .
ln -sf "$MAIN/assertS.c2m"         .
ln -sf "$DAT/rnr_cc.c2m"           .
ln -sf "$DAT/rnr_interpol.c2m"     .

echo "==> running Dragon on irena_pincell_spot_d3_het_baseline.x2m"
"$ROOT/bin/Darwin_arm64/Dragon" < irena_pincell_spot_d3_het_baseline.x2m \
    > d3_het.log 2> d3_het.err
echo "==> Dragon exit OK; log: d3_het.log"
