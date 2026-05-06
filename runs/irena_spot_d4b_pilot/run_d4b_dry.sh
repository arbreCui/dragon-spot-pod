#!/bin/sh
#----
# run_d4b_dry.sh -- D4-B pilot dry-run (single SnapMring snapshot)
#
# Validates SnapMring.c2m end-to-end at T_comb=750°C before launching
# the full ~50h pilot. Output: K_TYPEK_radial vs D4-A 1-ring K=1.365886.
#
# Wall: ~2-3h.
#----
set -eu

ROOT="/Users/ww/phdCode/5.1-main2026-spot/Dragon"
RUN="$ROOT/runs/irena_spot_d4b_pilot"
LIB="/Users/ww/phdCode/libraries/l_endian"
DAT="$ROOT/data/rnr_0burn_spot_proc"
MAIN="$ROOT/data"

cd "$RUN"

# Explicit cleanup, no zsh globs
rm -f _DUMMY _main001 _main002 _main003 \
      _SnapMring001 _SnapMring002 \
      _rnr_cc001 _rnr_cc002 _rnr_interpol001 _rnr_interpol002 \
      DUMMYSQ TRACK_f TRACK_T_f \
      glowpost_d4b_dry.eps \
      irena_assembly_tiso_1_12.dat \
      SnapMring.c2m   SnapMring.l2m   SnapMring.o2m \
      rnr_cc.c2m      rnr_cc.l2m      rnr_cc.o2m \
      rnr_interpol.c2m rnr_interpol.l2m rnr_interpol.o2m \
      DLIB8R1_366 \
      d4b_dry.log d4b_dry.err 2>/dev/null || true

ln -sf "$LIB/draglibendfb8r1SHEM366_v5p1" DLIB8R1_366
ln -sf "$DAT/irena_assembly_tiso_1_12.dat" .
ln -sf "$MAIN/SnapMring.c2m"    .
ln -sf "$DAT/rnr_cc.c2m"        .
ln -sf "$DAT/rnr_interpol.c2m"  .

echo "==> D4-B dry: running Dragon (PATCHED) on d4b_dry_snapMring.x2m (~2-3h)"
"$ROOT/bin/Darwin_arm64/Dragon" < d4b_dry_snapMring.x2m \
    > d4b_dry.log 2> d4b_dry.err
exit_code=$?
echo "==> Dragon exit code: $exit_code"
echo ""
echo "==> Result line + comparison:"
grep -E "SnapMring: snap K_TYPEK_radial|D4-B SnapMring K_TYPEK_radial|D4-A Snap1Ring|4ring - 1ring|d4b_dry_snapMring complete|XABORT|ERROR" d4b_dry.log 2>/dev/null | tail -20
echo ""
echo "==> If 3 pass criteria met (clean exit, K in range, |Δ| < 500 pcm):"
echo "    launch full D4-B pilot via run_d4b_pilot.sh"
