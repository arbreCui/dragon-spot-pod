#!/bin/sh
# Build the validation-only GMRES activity source tree.  This script never
# compiles, links, or executes Dragon.

set -eu
umask 077
export LC_ALL=C

fail()
{
  echo "GMRES-ACTIVITY-OVERLAY-BUILD FAIL: $*" >&2
  exit 1
}

if [ "$#" -ne 1 ]; then
  fail "usage: $0 NEW_OUTPUT_DIRECTORY"
fi

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd -P)
MANIFEST="$SCRIPT_DIR/gmres_activity_overlay_manifest.json"
PATCH_FILE="$SCRIPT_DIR/gmres_activity_overlay.patch"
PROTOCOL_CHECKER="$SCRIPT_DIR/check_gmres_activity_protocol.py"

PARENT_COMMIT=4d7abb23ac7975d4146beaa3b0049e36cdad8776
PARENT_ARCHIVE_SHA256=a1ee2a7ef3fb128afe4b1fe14c7021a1cff1b1d80adb18548fb22840969e23aa
MANIFEST_SHA256=b117cea97cfb54b4b043bc923c435a736d01b54fbb8fcfd5fdcb1472c39283a3
PATCH_SHA256=ebdc1eee70422e0c881901802602d053b61079ad942ec1dbdf16fbe88fc8f942
PROTOCOL_CHECKER_SHA256=1084f38ad14c2fb5f0e2b52786a248e29f3461c084145fb55aaae9d6dda2202c

sha256_file()
{
  shasum -a 256 "$1" | awk '{print $1}'
}

require_regular()
{
  [ -f "$1" ] && [ ! -L "$1" ] || fail "invalid regular file: $2"
}

require_sha256()
{
  actual_sha256=$(sha256_file "$1")
  [ "$actual_sha256" = "$2" ] || fail "SHA256 differs: $3"
}

requested_output=$1
case "$requested_output" in
  "")
    fail "empty output directory"
    ;;
  *'
'*|*'	'*)
    fail "output directory contains a control character"
    ;;
esac

output_parent_arg=$(dirname -- "$requested_output")
output_base=$(basename -- "$requested_output")
case "$output_base" in
  ""|"."|"..")
    fail "invalid output directory basename"
    ;;
esac
[ -d "$output_parent_arg" ] || fail "output parent is not an existing directory"
output_parent=$(CDPATH= cd -- "$output_parent_arg" && pwd -P)
output="$output_parent/$output_base"
[ ! -e "$output" ] && [ ! -L "$output" ] ||
  fail "output directory must not already exist"

case "$output" in
  "$ROOT/src"|"$ROOT/src"/*)
    fail "output directory cannot be the live src tree or its descendant"
    ;;
esac

require_regular "$MANIFEST" "overlay manifest"
require_regular "$PATCH_FILE" "overlay patch"
require_regular "$PROTOCOL_CHECKER" "protocol checker"
require_sha256 "$MANIFEST" "$MANIFEST_SHA256" "overlay manifest"
require_sha256 "$PATCH_FILE" "$PATCH_SHA256" "overlay patch"
require_sha256 "$PROTOCOL_CHECKER" "$PROTOCOL_CHECKER_SHA256" \
  "protocol checker"

git -C "$ROOT" cat-file -e "$PARENT_COMMIT^{commit}" 2>/dev/null ||
  fail "frozen parent commit is unavailable"
git -C "$ROOT" diff --quiet "$PARENT_COMMIT" -- src ||
  fail "tracked live src differs from the frozen parent"
live_src_status=$(git -C "$ROOT" status --porcelain=v1 \
  --untracked-files=all -- src)
[ -z "$live_src_status" ] || fail "live src contains a dirty or untracked path"

python3 "$PROTOCOL_CHECKER" --freeze-audit >/dev/null ||
  fail "frozen protocol check failed"

unsafe_tree_entry=$(git -C "$ROOT" ls-tree -r "$PARENT_COMMIT" |
  awk '$1 == "120000" || $1 == "160000" { print; exit }')
[ -z "$unsafe_tree_entry" ] ||
  fail "frozen parent contains a symlink or gitlink"

work=
output_created=0
cleanup()
{
  cleanup_status=$?
  trap - EXIT HUP INT TERM
  if [ "$output_created" -eq 1 ] && [ -d "$output" ] && [ ! -L "$output" ]; then
    chmod -R u+w "$output" 2>/dev/null || true
    rm -rf "$output"
  fi
  if [ -n "$work" ] && [ -d "$work" ] && [ ! -L "$work" ]; then
    chmod -R u+w "$work" 2>/dev/null || true
    rm -rf "$work"
  fi
  exit "$cleanup_status"
}
trap cleanup EXIT HUP INT TERM

work=$(mktemp -d "$output_parent/.gmres-activity-overlay-build.XXXXXX")
[ -d "$work" ] && [ ! -L "$work" ] || fail "cannot create safe work directory"
archive="$work/parent.tar"
parent_tree="$work/parent"
mkdir "$parent_tree"

git -C "$ROOT" archive --format=tar --output="$archive" "$PARENT_COMMIT"
require_regular "$archive" "clean parent archive"
require_sha256 "$archive" "$PARENT_ARCHIVE_SHA256" "clean parent archive"

tar -xf "$archive" -C "$parent_tree"
unsafe_parent=$(find "$parent_tree" ! -type f ! -type d -print -quit)
[ -z "$unsafe_parent" ] || fail "extracted parent contains a special file"

mkdir "$output"
output_created=1
tar -xf "$archive" -C "$output"
unsafe_output=$(find "$output" ! -type f ! -type d -print -quit)
[ -z "$unsafe_output" ] || fail "output contains a symlink or special file"

patch_output=$(patch --directory="$output" -p1 --fuzz=0 --batch --forward \
  --input="$PATCH_FILE" 2>&1) ||
  fail "overlay patch did not apply"
expected_patch_output="patching file 'src/.dragon_deps.mk'
patching file 'src/FLU.f'
patching file 'src/FLUDRV.f'
patching file 'src/FLUGPI.f'
patching file 'src/MCGMRE.f'
patching file 'src/SPOMGMR.f90'"
[ "$patch_output" = "$expected_patch_output" ] ||
  fail "patch output differs or reports fuzz/offset"
chmod 644 "$output/src/SPOMGMR.f90"

python3 - "$parent_tree/src" "$output/src" <<'PY'
from __future__ import annotations

import hashlib
from pathlib import Path
import stat
import sys


EXPECTED = {
    "src/.dragon_deps.mk": "M",
    "src/FLU.f": "M",
    "src/FLUDRV.f": "M",
    "src/FLUGPI.f": "M",
    "src/MCGMRE.f": "M",
    "src/SPOMGMR.f90": "A",
}


def fail(message: str) -> None:
    raise SystemExit(f"GMRES-ACTIVITY-OVERLAY-BUILD FAIL: {message}")


def census(root: Path) -> dict[str, tuple[int, str]]:
    result: dict[str, tuple[int, str]] = {}
    for path in sorted(root.rglob("*")):
        relative = "src/" + path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            fail(f"symlink found: {relative}")
        if stat.S_ISDIR(mode):
            continue
        if not stat.S_ISREG(mode):
            fail(f"special file found: {relative}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        result[relative] = (stat.S_IMODE(mode), digest)
    return result


parent = census(Path(sys.argv[1]))
patched = census(Path(sys.argv[2]))
observed: dict[str, str] = {}
for relative in sorted(parent.keys() | patched.keys()):
    if relative not in parent:
        observed[relative] = "A"
    elif relative not in patched:
        observed[relative] = "D"
    elif parent[relative] != patched[relative]:
        observed[relative] = "M"
if observed != EXPECTED:
    fail(f"source-tree change census differs: {observed!r}")
if patched["src/SPOMGMR.f90"][0] != 0o644:
    fail("new module mode is not 100644")
PY

require_sha256 "$output/src/.dragon_deps.mk" \
  070caabdfffcee6cd33bead91a9f5604998c6ba262723ca603b88f6a795f1295 \
  "patched src/.dragon_deps.mk"
require_sha256 "$output/src/FLU.f" \
  8befd86f9ee77bf5d25186eaf914349b2d4259f354f9bff504f4622339033c0e \
  "patched src/FLU.f"
require_sha256 "$output/src/FLUDRV.f" \
  49fbb86905726c59d75bcb9f67507ffe6bc0a7624d748dc1cb7dea71115dc951 \
  "patched src/FLUDRV.f"
require_sha256 "$output/src/FLUGPI.f" \
  3c5e6e675311761839605422e26a59fc25eb690ea363f2c513708a12d259329a \
  "patched src/FLUGPI.f"
require_sha256 "$output/src/MCGMRE.f" \
  16cf1c03933b1f5c1aa26cc5955999180b0149e6a9ef9fd26a2d54fad7264988 \
  "patched src/MCGMRE.f"
require_sha256 "$output/src/SPOMGMR.f90" \
  608203a9c23714bc2ace276172be4c8e84613f42c83565e30f752819fe79e274 \
  "patched src/SPOMGMR.f90"
require_sha256 "$output/src/SPOMOC.f90" \
  23a1927a133c19a86ffef9c3e0f4e619a899752cae0e7c2f0baa1bfc226502bc \
  "preserved src/SPOMOC.f90"

unsafe_output=$(find "$output" ! -type f ! -type d -print -quit)
[ -z "$unsafe_output" ] || fail "final output contains a symlink or special file"
git -C "$ROOT" diff --quiet "$PARENT_COMMIT" -- src ||
  fail "tracked live src changed during overlay construction"
live_src_status=$(git -C "$ROOT" status --porcelain=v1 \
  --untracked-files=all -- src)
[ -z "$live_src_status" ] ||
  fail "live src changed during overlay construction"

output_created=0
echo "PASS: GMRES activity overlay built at $output"
