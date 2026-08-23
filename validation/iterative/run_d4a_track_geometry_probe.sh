#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
ARCH=$(uname -s)_$(uname -m)
DRAGON="$ROOT/bin/$ARCH/Dragon"
GANLIB="$ROOT/Ganlib/lib/$ARCH"
GEOMETRY="$ROOT/data/rnr_0burn_spot_proc/irena_assembly_tiso_1_12_1ring.dat"
DECK="$ROOT/validation/iterative/d4a_track_geometry_probe.x2m"
CHECKER="$ROOT/validation/iterative/check_d4a_track_geometry.f90"
BOUNDED="$ROOT/validation/iterative/run_bounded_dragon.py"
EXPECTED_GEOMETRY_SHA=ca46ef77ea769059ddc612f1a78e4b565c32990401b21652c822bf2e11497a3e
FC=${FC:-gfortran}
WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-d4a-track.XXXXXX")
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

for input in "$DRAGON" "$GEOMETRY" "$DECK" "$CHECKER" "$BOUNDED" \
             "$GANLIB/libGanlib.a" "$GANLIB/modules/ganlib.mod"; do
  test -f "$input"
  test ! -L "$input"
done
test -x "$DRAGON"

geometry_hash_output=$(shasum -a 256 "$GEOMETRY")
geometry_sha=${geometry_hash_output%% *}
test "$geometry_sha" = "$EXPECTED_GEOMETRY_SHA"

cp "$GEOMETRY" "$WORK/geometry.dat"
cp "$DECK" "$WORK/probe.x2m"

FFLAGS='-std=f2008 -O0 -g -pedantic -Wall -Wextra -Werror -fcheck=all -ffp-contract=off -fno-fast-math'
"$FC" $FFLAGS -I "$GANLIB/modules" \
  "$CHECKER" "$GANLIB/libGanlib.a" -lstdc++ \
  -o "$WORK/check_d4a_track_geometry"

python3 "$BOUNDED" "$DRAGON" "$WORK/probe.x2m" "$WORK/probe.log"

for output in "$WORK/track.xsm" "$WORK/track.bin" "$WORK/probe.log"; do
  test -s "$output"
  test -f "$output"
  test ! -L "$output"
done
if ! grep -q '^>|D4A TRACK GEOMETRY PROBE COMPLETE' "$WORK/probe.log"; then
  echo 'D4A-TRACK GEOMETRY-ONLY FAIL: completion marker is absent.' >&2
  exit 1
fi
if grep -Eiq 'XABORT|(^|[^A-Z])(ERROR|FATAL)([^A-Z]|$)' "$WORK/probe.log"; then
  echo 'D4A-TRACK GEOMETRY-ONLY FAIL: Dragon log contains a fatal marker.' >&2
  exit 1
fi

(
  cd "$WORK"
  ./check_d4a_track_geometry track.xsm
)

xsm_hash_output=$(shasum -a 256 "$WORK/track.xsm")
track_hash_output=$(shasum -a 256 "$WORK/track.bin")
xsm_sha=${xsm_hash_output%% *}
track_sha=${track_hash_output%% *}
xsm_bytes=$(wc -c < "$WORK/track.xsm" | tr -d ' ')
track_bytes=$(wc -c < "$WORK/track.bin" | tr -d ' ')

echo "D4A-TRACK GEOMETRY-SHA256=$geometry_sha"
echo "D4A-TRACK XSM-SHA256=$xsm_sha BYTES=$xsm_bytes"
echo "D4A-TRACK BINARY-SHA256=$track_sha BYTES=$track_bytes"
echo 'D4A-TRACK GENERATED-ARTIFACT-SCOPE TEMPORARY'
