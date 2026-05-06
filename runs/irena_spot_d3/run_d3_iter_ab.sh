#!/bin/sh
#----
# run_d3_iter_ab.sh -- D3 outer iteration A/B (no-POD vs POD)
#----
set -eu

ROOT="/Users/ww/phdCode/5.1-main2026-spot/Dragon"
RUN="$ROOT/runs/irena_spot_d3"
LIB="/Users/ww/phdCode/libraries/l_endian"
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
      DLIB8R1_366 \
      d3_iter_ab.log d3_iter_ab.err 2>/dev/null || true

ln -sf "$LIB/draglibendfb8r1SHEM366_v5p1" DLIB8R1_366
ln -sf "$MAIN/SpotPodItr.c2m"        .
ln -sf "$MAIN/SpotSnapBld.c2m"       .
ln -sf "$MAIN/assertS.c2m"           .
ln -sf "$DAT/rnr_cc.c2m"             .
ln -sf "$DAT/rnr_interpol.c2m"       .

echo "==> running Dragon on d3_iter_ab.x2m"
"$ROOT/bin/Darwin_arm64/Dragon" < d3_iter_ab.x2m \
    > d3_iter_ab.log 2> d3_iter_ab.err
echo "==> Dragon exit; log: d3_iter_ab.log"
