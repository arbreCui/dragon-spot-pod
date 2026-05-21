#!/bin/sh
#----
# run_d3_sanity_pod.sh -- POD-case companion to d3_sanity
#
# Verifies whether handoff K_B = 1.409777 (POD eps=1E-3 converged) is real.
# d3_sanity (no-POD) gave K_A = 1.410130 (matches handoff K_A).
#
# Estimated wall: ~12-15 min (POD compresses leakage matrix; possibly
# slightly faster than no-POD case).
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
      glowpost_d3_sanity_pod.eps \
      SpotPodItr.c2m SpotPodItr.l2m SpotPodItr.o2m \
      SpotSnapBld.c2m SpotSnapBld.l2m SpotSnapBld.o2m \
      assertS.c2m assertS.l2m assertS.o2m \
      rnr_cc.c2m rnr_cc.l2m rnr_cc.o2m \
      rnr_interpol.c2m rnr_interpol.l2m rnr_interpol.o2m \
      DLIB8R1_370 \
      irena_pincell.dat \
      d3_sanity_pod.log d3_sanity_pod.err 2>/dev/null || true

ln -sf "$LIB/DLIB_370" DLIB8R1_370
ln -sf "$DAT/irena_pincell.dat"      .
ln -sf "$MAIN/SpotPodItr.c2m"        .
ln -sf "$MAIN/SpotSnapBld.c2m"       .
ln -sf "$MAIN/assertS.c2m"           .
ln -sf "$DAT/rnr_cc.c2m"             .
ln -sf "$DAT/rnr_interpol.c2m"       .

echo "==> running Dragon (PATCHED) on d3_sanity_pod.x2m"
"$ROOT/bin/Darwin_arm64/Dragon" < d3_sanity_pod.x2m \
    > d3_sanity_pod.log 2> d3_sanity_pod.err
echo "==> Dragon exit; log: d3_sanity_pod.log"
echo ""
echo "==> Quick verdict (look for the two lines below):"
echo "    iter 2 errspo:"
grep -E "SpotPodItr: outer iter 2|SPODB2: LEAK1D ACCURACY" d3_sanity_pod.log || echo "    (no match yet — log truncated or run failed)"
