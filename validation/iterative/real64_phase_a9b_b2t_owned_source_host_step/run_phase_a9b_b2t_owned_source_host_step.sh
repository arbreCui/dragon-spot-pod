#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)
STATIC_CHECKER="$HERE/check_phase_a9b_b2t_owned_source_host_step.py"
MUTATION_TEST=test_phase_a9b_b2t_owned_source_host_step
PROBES="$HERE/b2t_stub_probes.f90"
STUBS="$HERE/b2t_orchestration_stubs.f90"
HARNESS="$HERE/test_b2t_owned_source_orchestration.f90"
CONTENT_STUBS="$HERE/b2t_content_capture_stubs.f90"
CONTENT_HARNESS="$HERE/test_b2t_content_owned_source_host_step.f90"
CONTENT_POSTERIOR="$HERE/check_b2t_content_owned_source_host_step.f90"
B2S_CAPTURE_STUB="$ROOT/validation/iterative/real64_phase_a9b_b2s_immediate_host_bridge/b2s_capture_stubs.f90"
PREPARER="$ROOT/validation/iterative/real64_phase_a9b_b2l_one_plane_real_asm/prepare_b2l_projected.f90"
B2M_RECEIPT="$ROOT/validation/iterative/real64_phase_a9b_b2m_three_plane_real_asm_commit/phase_a9b_b2m_three_plane_real_asm_commit_receipt.sha256"
B2N_RECEIPT="$ROOT/validation/iterative/real64_phase_a9b_b2n_real64_frozen_qfiss/phase_a9b_b2n_real64_frozen_qfiss_receipt.sha256"
B2S_RECEIPT="$ROOT/validation/iterative/real64_phase_a9b_b2s_immediate_host_bridge/phase_a9b_b2s_immediate_host_bridge_receipt.sha256"
RECEIPT="$HERE/phase_a9b_b2t_owned_source_host_step_receipt.sha256"
EXPECTED_PARENT_COMMIT=c2a4fb644c50a45f28ce6f3b040ab4247908adf1
EXPECTED_B2M_RECEIPT_HASH=8caa46c1af00e9dbe896123a6294dfa96b790e020c9592e0b76d13f093c09314
EXPECTED_B2N_RECEIPT_HASH=06f9349e341a1bb3d07087e4f5236f8408b6fe67599a565d68c1b18ca7c51cc5
EXPECTED_B2S_RECEIPT_HASH=28ca392d1126b8e118f261d309a9e00583bf7516ee9b5e6fc7399cf0aaa949d8
EXPECTED_B2K_HASH=5cd0f757b5169526e5f2c47255df1c92085f9973c69365c488def65204937d0d
EXPECTED_B2N_HASH=a8247eda3e2ed30126c0c92be6e69f49be48c91008881abab9fec990d8a453de
EXPECTED_B2S_HASH=7066f0695dff6ba55005cd1bb7a074f3282e850054ca636e4f168e8d804e8e50

AX_ARTIFACT="$ROOT/validation/artifacts/iterative-map1/state1_axial.xsm"
ARCHIVE_ARTIFACT="$ROOT/validation/artifacts/iterative-map1/state1_snapshots.xsm"
AXIAL_TRACK_ARTIFACT="$ROOT/validation/artifacts/iterative-seed/initial_axial_track.xsm"
EXPECTED_AX_HASH=2323a256002f1e6f75f5af72c31479b0f6a7bff561d401cee363dcf9fc6ff484
EXPECTED_ARCHIVE_HASH=1b5a0c98aba0f5b4f366b64a8157f4a104df0f89f4cdeafc60eb6ce7811018e1
EXPECTED_AXIAL_TRACK_HASH=101ba0ad64c91723fdeb002e62c6226347fcfaeff188e125d699d70e113febc7
EXPECTED_PROJECTED_HASH=c010c0a860884a4e4d3842dffe45ffb4898f2aaca99557e0411ee8c66d60b90c
EXPECTED_PROJECTED_BYTES=225315452
EXPECTED_M1_HASH=6430b5e43b03125f8bd94c350bae2d8fc97978f86b3a5bb25f2026fd10914ada
EXPECTED_S1_HASH=37a3499742125db65fb51e505797e2890f6ae29461af9640bf14352aad898f2d
EXPECTED_M2_HASH=0fd2afcda8b2ca6c2248d616f7f85c2d272625b04c07717723f907701ce8b8e0
EXPECTED_S2_HASH=bf148826c9637b534df4cfe6719381fd3a3f702e2c303c8cba1f02592643c324
EXPECTED_M3_HASH=72b651fccfd4ab98cdb488783625748251ff0515f1f988bfcb2e073476f64cc7
EXPECTED_S3_HASH=787bb1d815e6abe98156544d8caa6a0b10da676edc4e8881096ba59bf16317e6
EXPECTED_MACRO_BYTES=9878532
EXPECTED_SOURCE_BYTES=625560

FC=/opt/homebrew/bin/gfortran
EXPECTED_FC_BANNER='GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0'
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-a9b-b2t.XXXXXX")
ORCH_SOURCE_DIR="$BUILD_DIR/orchestration-source"
ORCH_OBJECT_DIR="$BUILD_DIR/orchestration-objects"
ACTUAL_SOURCE_DIR="$BUILD_DIR/actual-source"
ACTUAL_OBJECT_DIR="$BUILD_DIR/actual-objects"
CONTENT_SOURCE_DIR="$BUILD_DIR/content-source"
CONTENT_OBJECT_DIR="$BUILD_DIR/content-objects"
CASE_DIR="$BUILD_DIR/case"
trap 'cd /; rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

LC_ALL=C
export LC_ALL

fail()
{
  printf '%s\n' "SPOR64 PHASE-A9b-B2t FAILURE: $*" >&2
  exit 1
}

count_exact()
{
  expected=$1
  pattern=$2
  file=$3
  found=$(grep -c -E "$pattern" "$file" || true)
  [ "$found" -eq "$expected" ] || \
    fail "$file: expected $expected matches for $pattern, found $found"
}

hash_of()
{
  shasum -a 256 "$1" | awk '{print $1}'
}

require_hash()
{
  path=$1
  expected=$2
  [ "$(hash_of "$path")" = "$expected" ] || fail "hash differs: $path"
}

require_receipt_entry()
{
  receipt=$1
  relative_path=$2
  expected=$3
  grep -F -x "$expected  $relative_path" "$receipt" >/dev/null || \
    fail "upstream receipt entry differs: $relative_path"
  require_hash "$ROOT/$relative_path" "$expected"
}

verify_upstream_lineage()
{
  require_hash "$B2M_RECEIPT" "$EXPECTED_B2M_RECEIPT_HASH"
  require_hash "$B2N_RECEIPT" "$EXPECTED_B2N_RECEIPT_HASH"
  require_hash "$B2S_RECEIPT" "$EXPECTED_B2S_RECEIPT_HASH"
  require_receipt_entry "$B2M_RECEIPT" src/SPOR64_B2K.f90 \
    "$EXPECTED_B2K_HASH"
  require_receipt_entry "$B2N_RECEIPT" src/SPOR64_B2N.f90 \
    "$EXPECTED_B2N_HASH"
  require_receipt_entry "$B2S_RECEIPT" src/SPOR64_B2S.f90 \
    "$EXPECTED_B2S_HASH"
  git -C "$ROOT" cat-file -e "$EXPECTED_PARENT_COMMIT^{commit}" || \
    fail "B2s parent commit is missing"
  git -C "$ROOT" merge-base --is-ancestor "$EXPECTED_PARENT_COMMIT" HEAD || \
    fail "B2s parent commit is not an ancestor"
}

verify_receipt()
{
  [ -f "$RECEIPT" ] || fail "B2t contract receipt missing"
  (
    cd "$ROOT"
    shasum -a 256 -c "$RECEIPT" >/dev/null
  ) || fail "B2t contract receipt verification failed"
}

verify_seals()
{
  verify_upstream_lineage
  verify_receipt
}

copy_exact()
{
  source_path=$1
  target_path=$2
  cp "$source_path" "$target_path"
  cmp "$source_path" "$target_path" || fail "copy differs: $target_path"
}

run_limited()
(
  ulimit -c 0
  ulimit -t 15
  ulimit -f 524288
  perl -e '$seconds=shift @ARGV; alarm $seconds; exec @ARGV' 15 "$@"
)

require_regular_evidence()
{
  path=$1
  expected_hash=$2
  expected_bytes=$3
  [ -f "$path" ] || fail "content evidence missing: $path"
  [ ! -L "$path" ] || fail "content evidence is a symlink: $path"
  [ "$(stat -f '%z' "$path")" -eq "$expected_bytes" ] || \
    fail "content evidence size differs: $path"
  [ "$expected_bytes" -le 134217728 ] || \
    fail "content evidence exceeds the 128 MiB gate: $path"
  require_hash "$path" "$expected_hash"
}

write_evidence_manifest()
{
  target=$1
  : >"$target"
  for name in macro1.xsm source1.xsm macro2.xsm source2.xsm \
    macro3.xsm source3.xsm
  do
    printf '%s %s %s\n' "$(hash_of "$CASE_DIR/$name")" \
      "$(stat -f '%z' "$CASE_DIR/$name")" "$name" >>"$target"
  done
}

[ "$(uname -s)" = Darwin ] || fail "frozen platform is Darwin"
[ "$(uname -m)" = arm64 ] || fail "frozen architecture is arm64"
[ -x "$FC" ] || fail "frozen compiler missing"
command -v perl >/dev/null 2>&1 || fail "wall-time limiter missing"
[ "$($FC --version | sed -n '1p')" = "$EXPECTED_FC_BANNER" ] || \
  fail "unaudited compiler"

for path in "$STATIC_CHECKER" "$HERE/$MUTATION_TEST.py" "$PROBES" \
  "$STUBS" "$HARNESS" "$CONTENT_STUBS" "$CONTENT_HARNESS" \
  "$CONTENT_POSTERIOR" "$B2S_CAPTURE_STUB" "$PREPARER" \
  "$AX_ARTIFACT" "$ARCHIVE_ARTIFACT" "$AXIAL_TRACK_ARTIFACT"
do
  [ -f "$path" ] || fail "required input missing: $path"
done
for source in SPOR64_B2C SPOR64_B2B SPOR64_B2O SPOR64_B2R SPOR64_B2S \
  SPOR64_B2K SPOR64_B2N SPOR64_B2T SPOR64_B2I SPOR64_B2H SPOR64_B2J
do
  [ -f "$ROOT/src/$source.f90" ] || fail "production $source missing"
done
require_hash "$AX_ARTIFACT" "$EXPECTED_AX_HASH"
require_hash "$ARCHIVE_ARTIFACT" "$EXPECTED_ARCHIVE_HASH"
require_hash "$AXIAL_TRACK_ARTIFACT" "$EXPECTED_AXIAL_TRACK_HASH"
verify_seals

mkdir -p "$ORCH_SOURCE_DIR" "$ORCH_OBJECT_DIR" \
  "$ACTUAL_SOURCE_DIR" "$ACTUAL_OBJECT_DIR" \
  "$CONTENT_SOURCE_DIR" "$CONTENT_OBJECT_DIR" "$CASE_DIR"

if ! PYTHONDONTWRITEBYTECODE=1 python3 "$STATIC_CHECKER" \
  >"$BUILD_DIR/static.log" 2>&1
then
  sed -n '1,240p' "$BUILD_DIR/static.log" >&2
  fail "static owned-source-host-step contract rejected"
fi
count_exact 1 '^B2T STATIC OWNED-SOURCE-HOST-STEP PASS$' "$BUILD_DIR/static.log"
count_exact 1 '^B2T DEFAULT=OFF OBJECT-ACCESS=0 SCRATCH=0 SUBCALLS=0$' \
  "$BUILD_DIR/static.log"
count_exact 1 '^B2T ON=B2K\(1\)->B2N\(1,2,3\)->B2S\(\.TRUE\.\)\(1\)$' \
  "$BUILD_DIR/static.log"
count_exact 1 '^B2T CALLER-MACRO/SOURCE/SOLVED/ASSEMBLED=FORBIDDEN$' \
  "$BUILD_DIR/static.log"
count_exact 1 '^B2T CUTOFF=INT64-PER-PLANE-DIAGNOSTIC-ONLY$' \
  "$BUILD_DIR/static.log"
count_exact 1 '^B2T ASM-LINEAGE/TRACK-FILE-IDENTITY/TRANSPORT=NOT-PROVED$' \
  "$BUILD_DIR/static.log"
[ "$(wc -l <"$BUILD_DIR/static.log" | tr -d '[:space:]')" -eq 6 ] || \
  fail "unexpected static checker output line count"

if ! (
  cd "$HERE"
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$HERE" \
    python3 -m unittest -v "$MUTATION_TEST" \
    >"$BUILD_DIR/mutations.log" 2>&1
)
then
  sed -n '1,320p' "$BUILD_DIR/mutations.log" >&2
  fail "owned-source-host-step mutation suite rejected"
fi
count_exact 1 '^Ran 50 tests in [0-9.]+s$' "$BUILD_DIR/mutations.log"
count_exact 1 '^OK$' "$BUILD_DIR/mutations.log"
verify_seals

FLAGS='-O0 -g -std=f2008 -pedantic -Wall -Wextra -Werror'
FLAGS="$FLAGS -fimplicit-none -fcheck=all -fbacktrace"
FLAGS="$FLAGS -ffp-contract=off -fno-fast-math"
GANMOD="$ROOT/Ganlib/lib/Darwin_arm64/modules"
GANLIB="$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a"
UTILIB="$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a"

# Compile the complete production module chain against its actual interfaces.
# This is deliberately compile-only: no radial or axial solver is linked or run.
copy_exact "$B2S_CAPTURE_STUB" "$ACTUAL_SOURCE_DIR/b2s_capture_stubs.f90"
for source in SPOR64_B2C SPOR64_B2B SPOR64_B2O SPOR64_B2R SPOR64_B2S \
  SPOR64_B2K SPOR64_B2N SPOR64_B2T
do
  copy_exact "$ROOT/src/$source.f90" "$ACTUAL_SOURCE_DIR/$source.f90"
done
"$FC" $FLAGS -Wno-unused-dummy-argument -I "$GANMOD" \
  -J "$ACTUAL_OBJECT_DIR" -c "$ACTUAL_SOURCE_DIR/b2s_capture_stubs.f90" \
  -o "$ACTUAL_OBJECT_DIR/b2s_capture_stubs.o"
for source in SPOR64_B2C SPOR64_B2B SPOR64_B2O SPOR64_B2R SPOR64_B2S \
  SPOR64_B2K SPOR64_B2N SPOR64_B2T
do
  "$FC" $FLAGS -I "$ACTUAL_OBJECT_DIR" -I "$GANMOD" \
    -J "$ACTUAL_OBJECT_DIR" -c "$ACTUAL_SOURCE_DIR/$source.f90" \
    -o "$ACTUAL_OBJECT_DIR/$source.o"
done

# Stub-only orchestration witness: call order, cleanup and private pointer custody.
copy_exact "$ROOT/src/SPOR64_B2T.f90" "$ORCH_SOURCE_DIR/SPOR64_B2T.f90"
copy_exact "$PROBES" "$ORCH_SOURCE_DIR/b2t_stub_probes.f90"
copy_exact "$STUBS" "$ORCH_SOURCE_DIR/b2t_orchestration_stubs.f90"
copy_exact "$HARNESS" "$ORCH_SOURCE_DIR/test_b2t_owned_source_orchestration.f90"
"$FC" $FLAGS -I "$GANMOD" -J "$ORCH_OBJECT_DIR" \
  -c "$ORCH_SOURCE_DIR/b2t_stub_probes.f90" \
  -o "$ORCH_OBJECT_DIR/b2t_stub_probes.o"
"$FC" $FLAGS -I "$ORCH_OBJECT_DIR" -I "$GANMOD" -J "$ORCH_OBJECT_DIR" \
  -c "$ORCH_SOURCE_DIR/b2t_orchestration_stubs.f90" \
  -o "$ORCH_OBJECT_DIR/b2t_orchestration_stubs.o"
"$FC" $FLAGS -I "$ORCH_OBJECT_DIR" -I "$GANMOD" -J "$ORCH_OBJECT_DIR" \
  -c "$ORCH_SOURCE_DIR/SPOR64_B2T.f90" -o "$ORCH_OBJECT_DIR/SPOR64_B2T.o"
"$FC" $FLAGS -I "$ORCH_OBJECT_DIR" -I "$GANMOD" -J "$ORCH_OBJECT_DIR" \
  -c "$ORCH_SOURCE_DIR/test_b2t_owned_source_orchestration.f90" \
  -o "$ORCH_OBJECT_DIR/test_b2t_owned_source_orchestration.o"
"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$ORCH_OBJECT_DIR/b2t_stub_probes.o" \
  "$ORCH_OBJECT_DIR/b2t_orchestration_stubs.o" \
  "$ORCH_OBJECT_DIR/SPOR64_B2T.o" \
  "$ORCH_OBJECT_DIR/test_b2t_owned_source_orchestration.o" \
  "$GANLIB" "$UTILIB" -o "$BUILD_DIR/test_b2t_owned_source_orchestration"

nm -g "$BUILD_DIR/test_b2t_owned_source_orchestration" \
  >"$BUILD_DIR/orchestration.nm"
count_exact 1 '___spor64_b2t_MOD_spor64_b2t_host_step$' \
  "$BUILD_DIR/orchestration.nm"
count_exact 1 '___spor64_b2k_MOD_spor64_b2k_commit_system_archive$' \
  "$BUILD_DIR/orchestration.nm"
count_exact 1 '___spor64_b2n_MOD_spor64_b2n_build$' \
  "$BUILD_DIR/orchestration.nm"
count_exact 1 '___spor64_b2s_MOD_spor64_b2s_host_bridge$' \
  "$BUILD_DIR/orchestration.nm"
FORBIDDEN_RUNTIME='(^|[[:space:]])_?(dragon|asm|asmdrv|spoasm|doorav|doorfv|doorpv|mccga|mccgf|mcgasm|mcgmre|flu|fludrv|flu2dr|flugpi|xdrkin|xdrexp|spomoc|spor64k)_$|spor64_a8_|spor64_a9_|flu2dr64_core|xdrta2'
if grep -Eiq "$FORBIDDEN_RUNTIME" "$BUILD_DIR/orchestration.nm"
then
  fail "orchestration harness links a forbidden solver boundary"
fi
if ! run_limited "$BUILD_DIR/test_b2t_owned_source_orchestration" \
  >"$BUILD_DIR/orchestration.log" 2>&1
then
  sed -n '1,280p' "$BUILD_DIR/orchestration.log" >&2
  fail "owned-source orchestration harness rejected"
fi
count_exact 1 '^B2T OWNED-SOURCE ORCHESTRATION PASS$' "$BUILD_DIR/orchestration.log"
count_exact 1 '^B2T OFF OMITTED=0-SUBCALLS FALSE=0-SUBCALLS$' \
  "$BUILD_DIR/orchestration.log"
count_exact 1 '^B2T PREFLIGHT ALIAS=REJECTED DUPLICATE=REJECTED NONFRESH=REJECTED$' \
  "$BUILD_DIR/orchestration.log"
count_exact 1 '^B2T B2K-FAIL EVENTS=K OUTPUT=EMPTY$' "$BUILD_DIR/orchestration.log"
count_exact 1 '^B2T B2N2-FAIL EVENTS=K,N1,N2 OUTPUT=EMPTY$' \
  "$BUILD_DIR/orchestration.log"
count_exact 1 '^B2T B2S-FAIL EVENTS=K,N1,N2,N3,S OUTPUT=EMPTY$' \
  "$BUILD_DIR/orchestration.log"
count_exact 1 '^B2T SUCCESS EVENTS=K,N1,N2,N3,S RETURNED=1$' \
  "$BUILD_DIR/orchestration.log"
count_exact 1 '^B2T PRIVATE-HANDLE-BINDINGS=7 REPLAY-SUBSTITUTIONS=0 TRACK-HANDLE=IDENTICAL$' \
  "$BUILD_DIR/orchestration.log"
count_exact 1 '^B2T CUTOFF64=4294967301,4294967302,4294967303$' \
  "$BUILD_DIR/orchestration.log"
count_exact 1 '^B2T DRAGON=0 ASM=0 FLU=0 TRANSPORT=0$' \
  "$BUILD_DIR/orchestration.log"
[ "$(wc -l <"$BUILD_DIR/orchestration.log" | tr -d '[:space:]')" -eq 10 ] || \
  fail "unexpected orchestration output line count"

# Real B2N content witness using a frozen PROJECTED archive; B2K and B2S remain
# capture-only stubs, so this gate constructs sources but performs no solve.
for source in SPOR64_B2C SPOR64_B2I SPOR64_B2H SPOR64_B2J SPOR64_B2N SPOR64_B2T
do
  copy_exact "$ROOT/src/$source.f90" "$CONTENT_SOURCE_DIR/$source.f90"
done
copy_exact "$PREPARER" "$CONTENT_SOURCE_DIR/prepare_b2l_projected.f90"
copy_exact "$CONTENT_STUBS" "$CONTENT_SOURCE_DIR/b2t_content_capture_stubs.f90"
copy_exact "$CONTENT_HARNESS" "$CONTENT_SOURCE_DIR/test_b2t_content_owned_source_host_step.f90"
copy_exact "$CONTENT_POSTERIOR" "$CONTENT_SOURCE_DIR/check_b2t_content_owned_source_host_step.f90"

"$FC" $FLAGS -I "$GANMOD" -J "$CONTENT_OBJECT_DIR" \
  -c "$CONTENT_SOURCE_DIR/b2t_content_capture_stubs.f90" \
  -o "$CONTENT_OBJECT_DIR/b2t_content_capture_stubs.o"
for source in SPOR64_B2C SPOR64_B2I SPOR64_B2H SPOR64_B2J SPOR64_B2N SPOR64_B2T
do
  "$FC" $FLAGS -I "$CONTENT_OBJECT_DIR" -I "$GANMOD" \
    -J "$CONTENT_OBJECT_DIR" -c "$CONTENT_SOURCE_DIR/$source.f90" \
    -o "$CONTENT_OBJECT_DIR/$source.o"
done
"$FC" $FLAGS -I "$CONTENT_OBJECT_DIR" -I "$GANMOD" \
  -J "$CONTENT_OBJECT_DIR" -c "$CONTENT_SOURCE_DIR/prepare_b2l_projected.f90" \
  -o "$CONTENT_OBJECT_DIR/prepare_b2l_projected.o"
"$FC" $FLAGS -I "$CONTENT_OBJECT_DIR" -I "$GANMOD" \
  -J "$CONTENT_OBJECT_DIR" \
  -c "$CONTENT_SOURCE_DIR/test_b2t_content_owned_source_host_step.f90" \
  -o "$CONTENT_OBJECT_DIR/test_b2t_content_owned_source_host_step.o"
"$FC" $FLAGS -I "$GANMOD" -J "$CONTENT_OBJECT_DIR" \
  -c "$CONTENT_SOURCE_DIR/check_b2t_content_owned_source_host_step.f90" \
  -o "$CONTENT_OBJECT_DIR/check_b2t_content_owned_source_host_step.o"

"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$CONTENT_OBJECT_DIR/SPOR64_B2C.o" "$CONTENT_OBJECT_DIR/SPOR64_B2I.o" \
  "$CONTENT_OBJECT_DIR/SPOR64_B2H.o" "$CONTENT_OBJECT_DIR/SPOR64_B2J.o" \
  "$CONTENT_OBJECT_DIR/prepare_b2l_projected.o" "$GANLIB" "$UTILIB" \
  -o "$BUILD_DIR/prepare_b2l_projected"
"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$CONTENT_OBJECT_DIR/b2t_content_capture_stubs.o" \
  "$CONTENT_OBJECT_DIR/SPOR64_B2N.o" "$CONTENT_OBJECT_DIR/SPOR64_B2T.o" \
  "$CONTENT_OBJECT_DIR/test_b2t_content_owned_source_host_step.o" \
  "$GANLIB" "$UTILIB" -o "$BUILD_DIR/test_b2t_content_owned_source_host_step"
"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$CONTENT_OBJECT_DIR/check_b2t_content_owned_source_host_step.o" \
  "$GANLIB" "$UTILIB" -o "$BUILD_DIR/check_b2t_content_owned_source_host_step"

nm -g "$BUILD_DIR/prepare_b2l_projected" >"$BUILD_DIR/prepare.nm"
nm -g "$BUILD_DIR/test_b2t_content_owned_source_host_step" \
  >"$BUILD_DIR/content.nm"
nm -g "$BUILD_DIR/check_b2t_content_owned_source_host_step" \
  >"$BUILD_DIR/posterior.nm"
if grep -Eiq "$FORBIDDEN_RUNTIME" "$BUILD_DIR/prepare.nm" || \
   grep -Eiq "$FORBIDDEN_RUNTIME|spor64_b2[obr]_mod_" "$BUILD_DIR/content.nm"
then
  fail "content preparation or harness links a forbidden solver boundary"
fi
count_exact 1 '___spor64_b2n_MOD_spor64_b2n_build$' "$BUILD_DIR/content.nm"
count_exact 1 '___spor64_b2t_MOD_spor64_b2t_host_step$' "$BUILD_DIR/content.nm"
count_exact 1 '___spor64_b2k_MOD_spor64_b2k_commit_system_archive$' "$BUILD_DIR/content.nm"
count_exact 1 '___spor64_b2s_MOD_spor64_b2s_host_bridge$' "$BUILD_DIR/content.nm"
if grep -Eiq "spor64_|$FORBIDDEN_RUNTIME" "$BUILD_DIR/posterior.nm"
then
  fail "independent content posterior links SPOR64 or solver code"
fi
grep -i 'lcmop' "$BUILD_DIR/posterior.nm" >/dev/null || \
  fail "independent content posterior lacks GANLIB read path"

ln -s "$AX_ARTIFACT" "$CASE_DIR/ax.xsm"
ln -s "$ARCHIVE_ARTIFACT" "$CASE_DIR/archive.xsm"
ln -s "$AXIAL_TRACK_ARTIFACT" "$CASE_DIR/axial_track.xsm"
if ! (
  cd "$CASE_DIR"
  run_limited "$BUILD_DIR/prepare_b2l_projected" \
    ax.xsm archive.xsm axial_track.xsm projected.xsm >prepare.log 2>&1
)
then
  sed -n '1,260p' "$CASE_DIR/prepare.log" >&2
  fail "bounded PROJECTED preparation rejected"
fi
count_exact 1 '^B2L FULL PROJECTED PREPARATION PASS$' "$CASE_DIR/prepare.log"
count_exact 1 '^B2L PRODUCTION-B2C-CALLS=3 B2I-CALLS=1 B2J-CALLS=1$' \
  "$CASE_DIR/prepare.log"
count_exact 1 '^B2L FULL-TRACK-LIBRARY-SYSTEM-COPIES=9$' "$CASE_DIR/prepare.log"
count_exact 1 '^B2L POST-B2J-MUTATIONS=0 PROJECTED-SYSTEM=ABSENT$' \
  "$CASE_DIR/prepare.log"
[ "$(wc -l <"$CASE_DIR/prepare.log" | tr -d '[:space:]')" -eq 4 ] || \
  fail "unexpected PROJECTED preparation output line count"
require_hash "$CASE_DIR/projected.xsm" "$EXPECTED_PROJECTED_HASH"
[ "$(stat -f '%z' "$CASE_DIR/projected.xsm")" -eq "$EXPECTED_PROJECTED_BYTES" ] || \
  fail "PROJECTED byte count differs"

if ! (
  cd "$CASE_DIR"
  run_limited "$BUILD_DIR/test_b2t_content_owned_source_host_step" \
    projected.xsm macro1.xsm source1.xsm macro2.xsm source2.xsm \
    macro3.xsm source3.xsm >content.log 2>&1
)
then
  sed -n '1,280p' "$CASE_DIR/content.log" >&2
  fail "owned-source content harness rejected"
fi
count_exact 1 '^B2T CONTENT OWNED-SOURCE HOST-STEP PASS$' "$CASE_DIR/content.log"
count_exact 1 '^B2T CONTENT B2K-STUB=1 B2N-COMMITTED=3 B2S-STUB=1$' \
  "$CASE_DIR/content.log"
count_exact 1 '^B2T CONTENT EVIDENCE MACRO0=3 FSOURCE=3$' "$CASE_DIR/content.log"
count_exact 1 '^B2T CONTENT DRAGON=0 ASM=0 FLU=0 TRANSPORT=0 PICARD=0$' \
  "$CASE_DIR/content.log"
[ "$(wc -l <"$CASE_DIR/content.log" | tr -d '[:space:]')" -eq 4 ] || \
  fail "unexpected content harness output line count"

require_regular_evidence "$CASE_DIR/macro1.xsm" "$EXPECTED_M1_HASH" "$EXPECTED_MACRO_BYTES"
require_regular_evidence "$CASE_DIR/source1.xsm" "$EXPECTED_S1_HASH" "$EXPECTED_SOURCE_BYTES"
require_regular_evidence "$CASE_DIR/macro2.xsm" "$EXPECTED_M2_HASH" "$EXPECTED_MACRO_BYTES"
require_regular_evidence "$CASE_DIR/source2.xsm" "$EXPECTED_S2_HASH" "$EXPECTED_SOURCE_BYTES"
require_regular_evidence "$CASE_DIR/macro3.xsm" "$EXPECTED_M3_HASH" "$EXPECTED_MACRO_BYTES"
require_regular_evidence "$CASE_DIR/source3.xsm" "$EXPECTED_S3_HASH" "$EXPECTED_SOURCE_BYTES"
write_evidence_manifest "$BUILD_DIR/evidence.before"
chmod 444 "$CASE_DIR/projected.xsm" "$CASE_DIR/macro1.xsm" \
  "$CASE_DIR/source1.xsm" "$CASE_DIR/macro2.xsm" "$CASE_DIR/source2.xsm" \
  "$CASE_DIR/macro3.xsm" "$CASE_DIR/source3.xsm"

if ! (
  cd "$CASE_DIR"
  run_limited "$BUILD_DIR/check_b2t_content_owned_source_host_step" \
    projected.xsm macro1.xsm source1.xsm macro2.xsm source2.xsm \
    macro3.xsm source3.xsm >posterior1.log 2>&1
  run_limited "$BUILD_DIR/check_b2t_content_owned_source_host_step" \
    projected.xsm macro1.xsm source1.xsm macro2.xsm source2.xsm \
    macro3.xsm source3.xsm >posterior2.log 2>&1
)
then
  sed -n '1,280p' "$CASE_DIR/posterior1.log" >&2
  sed -n '1,280p' "$CASE_DIR/posterior2.log" >&2
  fail "independent three-plane content posterior rejected"
fi
cmp "$CASE_DIR/posterior1.log" "$CASE_DIR/posterior2.log" || \
  fail "independent content posterior reports differ"
count_exact 1 '^B2T CONTENT THREE-PLANE POSTERIOR PASS$' "$CASE_DIR/posterior1.log"
count_exact 1 '^B2T CONTENT NUSIGF-POSITIVE-ZERO=284160$' "$CASE_DIR/posterior1.log"
count_exact 1 '^B2T CONTENT QFISS-R64-BITS=15540 DSOUR-R32-PROJECTIONS=15540 QINT-R32-PROJECTIONS=1110$' \
  "$CASE_DIR/posterior1.log"
count_exact 1 '^B2T CONTENT MACRO-OTHER-RECORDS=RECURSIVE-BIT-IDENTICAL$' \
  "$CASE_DIR/posterior1.log"
count_exact 1 '^B2T CONTENT PLANES=1,2,3 SAME-PROJECTED-PARENT=YES$' \
  "$CASE_DIR/posterior1.log"
count_exact 1 '^B2T CONTENT DRAGON=0 ASM=0 FLU=0 TRANSPORT=0 PICARD=0$' \
  "$CASE_DIR/posterior1.log"
[ "$(wc -l <"$CASE_DIR/posterior1.log" | tr -d '[:space:]')" -eq 6 ] || \
  fail "unexpected content posterior output line count"

write_evidence_manifest "$BUILD_DIR/evidence.after"
cmp "$BUILD_DIR/evidence.before" "$BUILD_DIR/evidence.after" || \
  fail "read-only posterior changed content evidence"
require_hash "$CASE_DIR/projected.xsm" "$EXPECTED_PROJECTED_HASH"
[ "$(stat -f '%z' "$CASE_DIR/projected.xsm")" -eq "$EXPECTED_PROJECTED_BYTES" ] || \
  fail "read-only posterior changed PROJECTED size"
require_hash "$AX_ARTIFACT" "$EXPECTED_AX_HASH"
require_hash "$ARCHIVE_ARTIFACT" "$EXPECTED_ARCHIVE_HASH"
require_hash "$AXIAL_TRACK_ARTIFACT" "$EXPECTED_AXIAL_TRACK_HASH"
PYTHONDONTWRITEBYTECODE=1 python3 "$STATIC_CHECKER" >/dev/null
verify_seals

cat "$BUILD_DIR/static.log"
cat "$BUILD_DIR/orchestration.log"
cat "$CASE_DIR/content.log"
cat "$CASE_DIR/posterior1.log"
printf '%s\n' 'SPOR64 PHASE-A9b-B2t OWNED-SOURCE-HOST-STEP PASS'
printf '%s\n' 'STATIC-MUTATIONS=49/49 ACTUAL-ABI=STRICT-COMPILE'
printf '%s\n' 'ORCHESTRATION=B2K(1)->B2N(1,2,3)->B2S(1) PRIVATE-BINDINGS=7'
printf '%s\n' 'CONTENT=REAL-B2N(3) B2K-STUB=1 B2S-CAPTURE-STUB=1'
printf '%s\n' 'POSTERIOR-RUNS=2 PROJECTED/EVIDENCE=READ-ONLY'
printf '%s\n' 'DRAGON=0 ASM=0 SPOASM=0 FLU=0 TRANSPORT=0 PICARD=0'
printf '%s\n' "PROJECTED-XSM-SHA256=$EXPECTED_PROJECTED_HASH BYTES=$EXPECTED_PROJECTED_BYTES"
printf '%s\n' "M1-SHA256=$EXPECTED_M1_HASH BYTES=$EXPECTED_MACRO_BYTES"
printf '%s\n' "S1-SHA256=$EXPECTED_S1_HASH BYTES=$EXPECTED_SOURCE_BYTES"
printf '%s\n' "M2-SHA256=$EXPECTED_M2_HASH BYTES=$EXPECTED_MACRO_BYTES"
printf '%s\n' "S2-SHA256=$EXPECTED_S2_HASH BYTES=$EXPECTED_SOURCE_BYTES"
printf '%s\n' "M3-SHA256=$EXPECTED_M3_HASH BYTES=$EXPECTED_MACRO_BYTES"
printf '%s\n' "S3-SHA256=$EXPECTED_S3_HASH BYTES=$EXPECTED_SOURCE_BYTES"
