#!/bin/sh
#----
# run_d3_het_iter.sh -- D3 SPOT outer iteration probe (SpotPodItr)
#----
set -eu

ROOT="/Users/wen/spot"
RUN="$ROOT/runs/irena_spot_d3"
LIB="/Users/wen/dragon-5.1/Dragon/irena_colorset_assembly_pin/pincell"
DAT="$ROOT/data/rnr_0burn_spot_proc"
MAIN="$ROOT/data"

cd "$RUN"

rm -f _DUMMY _main* _SpotPodItr* _SpotSnapBld* _Spot* _assert* _rnr* \
      DUMMYSQ TRACK_f TRACK_T_f TRACK_FUEL_f \
      glowpost_d3_iter.eps \
      SpotPodItr.c2m SpotPodItr.l2m SpotPodItr.o2m \
      SpotSnapBld.c2m SpotSnapBld.l2m SpotSnapBld.o2m \
      assertS.c2m assertS.l2m assertS.o2m \
      rnr_cc.c2m rnr_cc.l2m rnr_cc.o2m \
      rnr_interpol.c2m rnr_interpol.l2m rnr_interpol.o2m \
      DLIB8R1_370 \
      d3_het_iter.log d3_het_iter.err 2>/dev/null || true

ln -sf "$LIB/DLIB_370" DLIB8R1_370
ln -sf "$MAIN/SpotPodItr.c2m"        .
ln -sf "$MAIN/SpotSnapBld.c2m"       .
ln -sf "$MAIN/assertS.c2m"           .
ln -sf "$DAT/rnr_cc.c2m"             .
ln -sf "$DAT/rnr_interpol.c2m"       .

echo "==> running Dragon on d3_het_iter.x2m"
"$ROOT/bin/Darwin_arm64/Dragon" < d3_het_iter.x2m \
    > d3_het_iter.log 2> d3_het_iter.err
echo "==> Dragon exit; log: d3_het_iter.log"
