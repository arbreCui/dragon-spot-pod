#!/bin/sh
#----
# run_d3_sanity.sh -- minimal SPODB2 patch sanity test
#
# Answers one binary question:
#   On the patched binary, does outer iter 2 have errspo != 1.0E10?
#
# Look in d3_sanity.log for:
#   SpotPodItr: outer iter 1 K= ...  errspo=  1.000000e+10        (expected)
#   SPODB2: LEAK1D ACCURACY= 1.0000E+10  ...                       (matches iter 1)
#   SpotPodItr: outer iter 2 K= ...  errspo=  ???                  (the answer)
#   SPODB2: LEAK1D ACCURACY= <small>  ...                          (the answer)
#
# Estimated wall: 15-30 min on M-series mac (5 snapshots + 2 outer iters,
# flu_eps=1E-4 relaxed).
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
      glowpost_d3_sanity.eps \
      SpotPodItr.c2m SpotPodItr.l2m SpotPodItr.o2m \
      SpotSnapBld.c2m SpotSnapBld.l2m SpotSnapBld.o2m \
      assertS.c2m assertS.l2m assertS.o2m \
      rnr_cc.c2m rnr_cc.l2m rnr_cc.o2m \
      rnr_interpol.c2m rnr_interpol.l2m rnr_interpol.o2m \
      DLIB8R1_370 \
      irena_pincell.dat \
      d3_sanity.log d3_sanity.err 2>/dev/null || true

ln -sf "$LIB/DLIB_370" DLIB8R1_370
ln -sf "$DAT/irena_pincell.dat"      .
ln -sf "$MAIN/SpotPodItr.c2m"        .
ln -sf "$MAIN/SpotSnapBld.c2m"       .
ln -sf "$MAIN/assertS.c2m"           .
ln -sf "$DAT/rnr_cc.c2m"             .
ln -sf "$DAT/rnr_interpol.c2m"       .

echo "==> running Dragon (PATCHED) on d3_sanity.x2m"
"$ROOT/bin/Darwin_arm64/Dragon" < d3_sanity.x2m \
    > d3_sanity.log 2> d3_sanity.err
echo "==> Dragon exit; log: d3_sanity.log"
echo ""
echo "==> Quick verdict (look for the two lines below):"
echo "    iter 2 errspo:"
grep -E "SpotPodItr: outer iter 2|SPODB2: LEAK1D ACCURACY" d3_sanity.log || echo "    (no match yet — log truncated or run failed)"
