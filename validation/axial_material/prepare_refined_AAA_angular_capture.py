"""Prepare and run one archival-only replay of the sealed production map012.

Preparation never compiles or starts transport. The only numerical child is the
original warm axial deck, with a separately linked archival callback module.
The capture is a diagnostic of the actual production calculation, not an AAA
accuracy qualification or a continuation of either failed proxy comparison.
"""

import argparse
import ast
from contextlib import contextmanager
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "validation/artifacts"
OUT = ART / "axial-material-AAA-production-angular-capture-20261006"
PROD = ART / "axial-material-production-qualified-AB-white-trace-refined-envpin-20261005"
FINAL, PARENT = PROD / "AAA/map012", PROD / "AAA/map011"
ANG = ART / "axial-material-AAA-white-trace-angular-convergence-20261005"
COLD = ART / "axial-material-AAA-white-trace-cold-control-paths-20261004"
COMP = ART / "axial-material-AAA-compensated-flight-20261004"
CAUSAL = ART / "axial-material-AAA-white-trace-refined-layered-propagation-causal-20261005"
MODULE = ROOT / "validation/axial_material/axmat_capture_angles.f90"
BINARY_REVIEW = ROOT / "validation/axial_material/production_source_factor_binary_review.json"
PREPARED_SHA = "024ffb9263e3d3b6cf10301d6fe2bac5a87a9b368008440e01038982291a6d53"
FINAL_SEAL_SHA = "f3716289ced3716fa89747ecb99b01757cd8d0f85ed202548f2fb68d5518606c"
STATUS_SHA = "1acb16adc59f91e66599f74d11993d300bae73647dc870d148936935d199012f"
ANG_DECL_SHA = "aec1389e18a009a09fd1919e5e8291b23be1122136b0dbc301afd19d46ee91a8"
ANG_BUILD_SHA = "978197add22c895c1d988032a1a567d77b5ddb1d3a2d8bd598d0f76a587214fa"
DRAGON_SHA = "51b2d3ff947daa3ea523932bcc28276b054632f0bfc6cf76fa21ac458a4f7be4"
LIB_SHA = "954ed8568c59fdfc3ee566d027abac35c7a1469436afb0b147e4db7a7f28a1d9"
OBJECT_SHA = "4ba03f8b762eb1936118b35b5196a3257d151e5564cdb0fe77a41d9b36b6d175"
BASE_REVISION = "299546c405a47f7e3a7f75af54d392492d649781"
BASE_SHA = "90bedc3f7cc4d320355dbbf43988ca8fb43e59dbee493a7f19fa8c050c42e8a5"
CURRENT_SHA = "df3cfcb6c320f62afe91b6c63563173e4b510d1b142afb9baa2594d80d18db67"
CAUSAL_SHA = "f4a9ecd37a8b224a22869f2d8e670c26d7e8d2cb7af28ba63ecfaeb802dd04b2"
FULL_DECL_SHA = "f032eee5a6dfb9844a57043d1a357a8bfe383f2d6c2c71761841717f3ed6c94b"
NG, NUN, NZ, NA, NR, NL = 370, 1800, 48, 32, 8, 3


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def write_new(path, data):
    with Path(path).open("x") as stream:
        json.dump(data, stream, indent=2, allow_nan=False)
        stream.write("\n")


def require(path, wanted=None):
    path = Path(path)
    if not path.is_file() or (wanted is not None and digest(path) != wanted):
        raise ValueError("missing or changed declared file: " + str(path))
    return path


def verify(files):
    for path, wanted in files.items():
        require(path, wanted)


def modules():
    sys.path.insert(0, str(ROOT / "validation/axial_material"))
    import qualify_refined_AAA_layered_full as full
    sys.path.insert(0, str(PROD / "runtime"))
    # full uses these exact frozen production modules through its admitted import.
    import production_runner as production
    from snapshot_control_preflight import _open_xsm
    from qualified_snapshot_ingestion import list_handles
    return full, production, _open_xsm, list_handles


def environment(declaration):
    verify(declaration["files"])
    for path, target in declaration["native_library_aliases"].items():
        if str(Path(path).resolve()) != target:
            raise ValueError("declared numerical library alias changed")
    actual = {k: v for k, v in os.environ.items()
              if k.startswith("DYLD_") or k == "OPENBLAS_CORETYPE"}
    expected = {k: v for k, v in declaration["numerical_loader_environment"].items()
                if k.startswith("DYLD_") or k == "OPENBLAS_CORETYPE"}
    if actual != expected:
        raise ValueError("declared numerical loader/dispatch environment changed")


def baseline():
    """Recover the source whose old arithmetic is present in the frozen binary.

    The September-23 source/library co-pin does not establish compilation. The
    actual library object and frozen executable contain both old REAL32 angular
    multipliers; rebuild that recovered version, with no scientific correction.
    """
    require(ROOT / "lib/Darwin_arm64/libDragon.a", LIB_SHA)
    require(ROOT / "src/FLU2DR64.o", OBJECT_SHA)
    require(ROOT / "src/FLU2DR64.f", CURRENT_SHA)
    member = subprocess.run(["/usr/bin/ar", "-p", str(ROOT / "lib/Darwin_arm64/libDragon.a"),
                             "FLU2DR64.o"], check=True, capture_output=True, timeout=60).stdout
    if hashlib.sha256(member).hexdigest() != OBJECT_SHA:
        raise ValueError("actual frozen FLU2DR64 archive member changed")
    raw = subprocess.run(["/usr/bin/git", "-C", str(ROOT), "show",
                          BASE_REVISION + ":src/FLU2DR64.f"],
                         check=True, capture_output=True, timeout=60).stdout
    if hashlib.sha256(raw).hexdigest() != BASE_SHA:
        raise ValueError("actual frozen arithmetic source revision changed")
    text = raw.decode("utf-8")
    if text.count("REAL(2*IAL+1)*") != 2:
        raise ValueError("both compiled historical intergroup multipliers required")
    return text


def once(text, old, new):
    if text.count(old) != 1:
        raise ValueError("archival source anchor is absent or ambiguous: " + old[:100])
    return text.replace(old, new, 1)


def patched(original, changes, path, origin):
    changed = original
    for old, new in changes:
        changed = once(changed, old, new)
    restored = changed
    for old, new in reversed(changes):
        restored = once(restored, new, old)
    if restored != original:
        raise ValueError("archival patch changed native text outside listed insertions")
    path.write_text(changed)
    path.with_suffix(path.suffix + ".patch").write_text("".join(difflib.unified_diff(
        original.splitlines(True), changed.splitlines(True),
        fromfile=origin, tofile="isolated-archival-callbacks-only")))
    return dict(origin=origin, original_sha256=hashlib.sha256(original.encode()).hexdigest(),
                candidate_sha256=digest(path), replacements=changes,
                full_text_restored_exactly=True, native_expressions_changed=False)


def source_plan(original):
    flu_import = ("      USE SPOT1P64_CACHE_MOD, ONLY: SPOT1P64_CACHE_BEGIN,\n"
                  "     1 SPOT1P64_CACHE_CLEAR,SPOT1P64_CACHE_STATS")
    flu_changes = [(flu_import, flu_import + "\n"
        "      USE AXMAT_CAPTURE_ANGLES_MOD, ONLY: AXMAT_CAPTURE_BEGIN,\n"
        "     1 AXMAT_CAPTURE_CONTEXT,AXMAT_CAPTURE_TERMINAL,\n"
        "     2 AXMAT_CAPTURE_PRENORMAL,AXMAT_CAPTURE_PUBLISH")]
    begin = "      CALL SPOT1P64_CACHE_BEGIN(NGRP,IPHYS_CACHE.EQ.1)"
    flu_changes.append((begin, begin + "\n"
        "      CALL AXMAT_CAPTURE_BEGIN(NGRP,NUNKNO,NREG,NMAT,NFUNL,\n"
        "     1 ITYPEC,ILEAK,LEAKSW,LREBAL,NCPTL,NCPTA,ITPIJ,NANIS,\n"
        "     2 NDIM,INSB,LSCAL)"))
    # One context hook in the actual JT loop covers vector and scalar dispatch.
    jt = next(line for line in original.splitlines() if "DO 270 JT=" in line)
    flu_changes.append((jt, jt + "\n      CALL AXMAT_CAPTURE_CONTEXT(IT,JT)"))
    success = "         GO TO 410\n      ENDIF\n"
    flu_changes.append((success, "         CALL AXMAT_CAPTURE_TERMINAL(IEXTF,ITERF_LAST,\n"
        "     1   IGDEB_LAST,IINR_STATE,IUNK_EVAL,MAXOUT,MAXINR,\n"
        "     2   EEXT,EPSOUT,EUNK_LAST,EPSUNK,EINR_LAST,EPSINR,AKEFF)\n" + success))
    normalization = ("        IF(ITYPEC.LT.5) THEN\n"
                     "          FLUX(:NUNKNO,:NGRP,3)=FLUX(:NUNKNO,:NGRP,3)*(AKEFF/FISOUR)")
    flu_changes.append((normalization, "        CALL AXMAT_CAPTURE_PRENORMAL(NUNKNO,NGRP,\n"
        "     1  FLUX(:NUNKNO,:NGRP,3))\n" + normalization))
    saved = "  510 CONTINUE\n      IF(C_ASSOCIATED(IPSOU)) THEN"
    flu_changes.append((saved, "  510 CONTINUE\n"
        "      CALL AXMAT_CAPTURE_PUBLISH(NUNKNO,NGRP,\n"
        "     1 FLUX(:NUNKNO,:NGRP,3),FLUX(:NUNKNO,:NGRP,4),AKEFF,FISOUR)\n"
        "      IF(C_ASSOCIATED(IPSOU)) THEN"))
    dispatch_use = "      USE GANLIB\n      TYPE(C_PTR) JPSYS,IPTRK"
    flu_changes.append((dispatch_use, "      USE GANLIB\n"
        "      USE AXMAT_CAPTURE_ANGLES_MOD, ONLY: AXMAT_CAPTURE_INPUT,\n"
        "     1 AXMAT_CAPTURE_OUTPUT\n      TYPE(C_PTR) JPSYS,IPTRK"))
    dispatch = ("      CALL SPOF64(KPSYS,IPTRK,IMPX,NGEFF,NGIND,NREG,NMAT,NUN,MAT,\n"
                "     1 KEYFLX,F2,S2,TITR)")
    flu_changes.append((dispatch, "      CALL AXMAT_CAPTURE_INPUT(NGEFF,NGIND,NUN,S2,ILEAK,\n"
        "     1 B2,NPSYS)\n" + dispatch + "\n"
        "      CALL AXMAT_CAPTURE_OUTPUT(NGEFF,NGIND,NUN,F2)"))
    spot = (ANG / "build/SPOT1P64.f90").read_text()
    import_anchor = ("  use AXMAT_WHITE_TRACE_MOD, only: AXMAT_WHITE_ON,AXMAT_WHITE_ROW, &\n"
                     "    AXMAT_WHITE_PERIMETER,AXMAT_WHITE_KERNEL,AXMAT_WHITE_NOTE")
    spot_changes = [(import_anchor, import_anchor + "\n"
        "  use AXMAT_CAPTURE_ANGLES_MOD, only: AXMAT_CAPTURE_FIELD,AXMAT_CAPTURE_BLOCKS")]
    field = "  deallocate(opposite,modal_cour,modal_flux,cell,face)"
    spot_changes.append((field, "  call AXMAT_CAPTURE_FIELD(igroup,nmat,nsnap,mat1d,mat,ncode,opposite, &\n"
        "    vol1d,total,sgas,basis,vol2d,zcode,du,w,pl,radial2d,qext, &\n"
        "    weight,mass_m,total_m,radial_m,scat_m,source_m,mn,dn,white_angle, &\n"
        "    white_mode,cell,face,modal_flux,modal_cour,flux,cour,xnei,AXMAT_WHITE_ON)\n" + field))
    assembly = ("    enddo\n\n    if (cached_path) then\n"
                "      associate(plan => SPOT1P64_PLAN(igroup)%mode(first_mode))\n"
                "        if (cache_hit) then")
    spot_changes.append((assembly, "    enddo\n\n"
        "    if (.not.cache_hit) call AXMAT_CAPTURE_BLOCKS(igroup,lower,diagonal, &\n"
        "      upper,cached_path,cache_hit)\n\n    if (cached_path) then\n"
        "      associate(plan => SPOT1P64_PLAN(igroup)%mode(first_mode))\n"
        "        if (cache_hit) then"))
    return flu_changes, spot, spot_changes


def guard_admission(full):
    path = Path(full.__file__).resolve()
    require(path, "70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6")
    folder = full.OUT / "preflight/live_guard"
    require(folder / "guard_controls.json", "ae4d7e86423a187c29efd5bf87d54053081d7b7fcf18ac88cd9e49639cb07454")
    guard = read(folder / "guard_controls.json")
    tested = require(folder / "tested_driver_source.py", guard["source_sha256"])
    verify({str(folder / name): sha for name, sha in guard["control_files"].items()})
    def class_text(source):
        text = source.read_text()
        return next(ast.get_source_segment(text, n) for n in ast.parse(text).body
                    if isinstance(n, ast.ClassDef) and n.name == "OwnRSSSerialExecutor")
    if (class_text(path) != class_text(tested) or not guard["positive_child_completed"]
            or not guard["actual_oversize_child_rejected"] or not guard["terminated_own_child_not_live"]
            or guard["rss_cap_mib"] != 512):
        raise ValueError("byte-exact tested live guard with actual positive/oversize controls required")
    return [path, folder / "guard_controls.json", tested,
            *[folder / name for name in guard["control_files"]]]


def prepare():
    full, production, _, _ = modules()
    guard_files = guard_admission(full)
    require(full.OUT / "declaration.json", FULL_DECL_SHA)
    info = production.verify_prepared(PROD / "prepared.json", PREPARED_SHA)
    require(PROD / "AAA/run_status.json", STATUS_SHA)
    require(FINAL / "result.json", FINAL_SEAL_SHA)
    production.verify_sealed_directory(FINAL)
    production.verify_sealed_directory(PARENT)
    require(ANG / "declaration.json", ANG_DECL_SHA)
    require(ANG / "build_identity.json", ANG_BUILD_SHA)
    require(ANG / "runtime/Dragon", DRAGON_SHA)
    require(CAUSAL / "declaration.json", CAUSAL_SHA)
    old = read(ANG / "declaration.json")
    verify(old["files"])
    require(BINARY_REVIEW)
    evidence = read(BINARY_REVIEW)
    if (evidence["schema"] != "AXMAT_PRODUCTION_SOURCE_FACTOR_BINARY_REVIEW_V1"
            or evidence["classification"] != "CONFIRMED_COMPILED_INTERGROUP_LEGENDRE_FACTOR_MISMATCH"
            or evidence["git_source_evidence"]["old_file_sha256"] != BASE_SHA
            or evidence["actual_files"]["sender_object"]["sha256"] != OBJECT_SHA
            or evidence["actual_files"]["library"]["sha256"] != LIB_SHA
            or evidence["actual_files"]["runtime"]["sha256"] != DRAGON_SHA):
        raise ValueError("independent actual binary source-factor evidence required")
    for entry in evidence["actual_files"].values():
        if "path" in entry and "sha256" in entry:
            require(entry["path"], entry["sha256"])
    causal = read(CAUSAL / "declaration.json")
    original = baseline()
    flu_changes, spot, spot_changes = source_plan(original)
    # Prove every anchor and the insertion-only restoration before creating OUT.
    for text, changes in [(original, flu_changes), (spot, spot_changes)]:
        changed = text
        for a, b in changes:
            changed = once(changed, a, b)
        for a, b in reversed(changes):
            changed = once(changed, b, a)
        if changed != text:
            raise ValueError("source preparation restoration proof failed")
    source_inputs = {name: (FINAL / name).resolve() for name in (
        "initial_axial_track.xsm", "initial_axial_macrolib.xsm", "parent_axial_closed.xsm",
        "parent_snapshots_closed.xsm", "candidate_radial.xsm", "candidate_system.xsm",
        "basis_reference.xsm", "route_contract.xsm")}
    if (source_inputs["parent_axial_closed.xsm"] != (PARENT / "closed_axial.xsm").resolve()
            or source_inputs["parent_snapshots_closed.xsm"] != (PARENT / "closed_snapshots.xsm").resolve()):
        raise ValueError("exact sealed map011 parent inputs required")
    deck = require(FINAL / "picard_axial.x2m")
    terminal = require(FINAL / "picard_axial.log").read_text()
    outer_lines = [line for line in terminal.splitlines() if "FLU2DR-TERM OUTER-GATE=PASS" in line]
    inner_lines = [line for line in terminal.splitlines() if "FLU2DR-TERM INNER-TERMINAL" in line]
    if len(outer_lines) != 1 or len(inner_lines) != 1:
        raise ValueError("one actual original native terminal pair required")
    for line, values in [(outer_lines[0], dict(IEXTF=3, MAXOUT=500)),
                         (inner_lines[0], dict(ITERF=1, MAXINR=740, IGDEB=371, STATE=1, NGRP=370))]:
        for key, wanted in values.items():
            matches = re.findall(r"\b" + re.escape(key) + r"\s*=\s*([+-]?\d+)\b", line)
            if len(matches) != 1 or int(matches[0]) != wanted:
                raise ValueError("actual original predeclared terminal field differs: " + key)
    libraries = [ROOT / name for name in (
        "lib/Darwin_arm64/libDragon.a", "Trivac/lib/Darwin_arm64/libTrivac.a",
        "Utilib/lib/Darwin_arm64/libUtilib.a", "Ganlib/lib/Darwin_arm64/libGanlib.a")]
    reused = [ROOT / "src/DRAGON.o", COMP / "build/SPOR64_A8.o",
              COMP / "build/AXMAT_MCGFCF_COMP.o", ANG / "build/axmat_white_trace_model.o",
              COLD / "build/SPOF64.o"]
    compiler = Path(old["build_commands"][0][0]).resolve()
    files = dict(old["files"])
    paths = [Path(__file__).resolve(), MODULE, compiler, Path(sys.executable).resolve(),
        Path("/bin/ps"), Path("/usr/bin/git"), Path("/usr/bin/ar"), BINARY_REVIEW,
        PROD / "prepared.json", PROD / "AAA/run_status.json", FINAL / "result.json",
        PARENT / "result.json", FINAL / "picard_axial.log", deck,
        ANG / "declaration.json", ANG / "build_identity.json", ANG / "runtime/Dragon",
        CAUSAL / "declaration.json", full.OUT / "declaration.json", ROOT / "src/FLU2DR64.f", ROOT / "src/FLU2DR64.o",
        ANG / "build/SPOT1P64.f90", COLD / "build/SPOF64.f", *libraries, *reused,
        *source_inputs.values(), FINAL / "candidate_axial.xsm", FINAL / "candidate_snapshots.xsm", *guard_files,
        Path(full.__file__).resolve(), Path(production.__file__).resolve(),
        Path(sys.modules["snapshot_control_preflight"].__file__).resolve(),
        Path(sys.modules["qualified_snapshot_ingestion"].__file__).resolve()]
    for p in paths:
        files.setdefault(str(p), digest(require(p)))
    for p in (ROOT / "lib/Darwin_arm64/modules").glob("*.mod"):
        files.setdefault(str(p), digest(p))
    for p in (ROOT / "Ganlib/lib/Darwin_arm64/modules").glob("*.mod"):
        files.setdefault(str(p), digest(p))
    for p, h in causal["files"].items():
        if p.endswith((".so", ".dylib")) or "/numpy/" in p:
            files.setdefault(p, h)
    admitted = dict(files=files, native_library_aliases=causal["native_library_aliases"],
                    numerical_loader_environment=causal["numerical_loader_environment"])
    environment(admitted)
    roots = sorted(set(causal["resource_roots"])
        | set(read(full.OUT / "declaration.json")["resource_roots"])
        | {str(p.resolve()) for p in ART.glob("axial-material-*") if p.is_dir()} | {str(OUT)})
    resources = production.DiskResources(ART, roots, 8 * 2**30, 96 * 2**30)
    before = resources.check()
    copied = sum(p.stat().st_size for p in source_inputs.values())
    # 425 MiB raw native blocks, <64 MiB field archive, ~250 MiB outputs,
    # runtime/build/logs/receipts plus 1 GiB conservative headroom.
    reserve = copied + 2 * 2**30
    if (before["artifact_bytes"] + reserve >= 96 * 2**30
            or before["disk_free_bytes"] - reserve < 8 * 2**30):
        raise ValueError("complete warm capture and archival storage reservation failed")
    OUT.mkdir(exist_ok=False)
    for name in ("build", "runtime", "AAA", "audit"):
        (OUT / name).mkdir()
    shutil.copy2(PROD / "runtime/run_bounded_dragon.py", OUT / "runtime/run_bounded_dragon.py")
    shutil.copy2(MODULE, OUT / "build/axmat_capture_angles.f90")
    (OUT / "build/FLU2DR64.compiled_baseline.f").write_text(original)
    proofs = {}
    proofs["FLU2DR64.f"] = patched(original, flu_changes, OUT / "build/FLU2DR64.f",
                                    "git:" + BASE_REVISION + ":src/FLU2DR64.f")
    proofs["SPOT1P64.f90"] = patched(spot, spot_changes, OUT / "build/SPOT1P64.f90",
                                    str(ANG / "build/SPOT1P64.f90"))
    inputs = {}
    for name, source in source_inputs.items():
        target = OUT / "AAA" / name
        shutil.copy2(source, target)
        if digest(target) != digest(source):
            raise ValueError("private capture input is not byte-exact")
        inputs[name] = dict(source=str(source), sha256=digest(source), private_copy=str(target))
    shutil.copy2(deck, OUT / "AAA/picard_axial.x2m")
    if digest(OUT / "AAA/picard_axial.x2m") != digest(deck):
        raise ValueError("original map012 deck must be byte-exact")
    # Same native flags and frozen object/link chain; only override two patched
    # routines and add the archival module. SPOF64 and the white kernel reused.
    flags = ["-O2", "-march=native", "-ffp-contract=off", "-g", "-fPIC",
             "-frecord-marker=4", "-ffixed-line-length-none",
             "-I" + str(OUT / "build"), "-I" + str(ANG / "build"),
             "-I" + str(ROOT / "lib/Darwin_arm64/modules"),
             "-I" + str(ROOT / "Ganlib/lib/Darwin_arm64/modules"), "-J" + str(OUT / "build")]
    commands = [[str(compiler), *flags, "-c", str(OUT / "build" / name),
                 "-o", str((OUT / "build" / name).with_suffix(".o"))]
                for name in ("axmat_capture_angles.f90", "SPOT1P64.f90", "FLU2DR64.f")]
    commands.append([str(compiler), "-O2", "-march=native", "-ffp-contract=off", "-g",
        str(reused[0]), str(reused[1]), str(reused[2]), str(OUT / "build/axmat_capture_angles.o"),
        str(reused[3]), str(OUT / "build/SPOT1P64.o"), str(reused[4]),
        str(OUT / "build/FLU2DR64.o"), *map(str, libraries), "-o", str(OUT / "runtime/Dragon")])
    write_new(OUT / "archival_source_admission.json", dict(
        patches=proofs, actual_frozen_library_sha256=LIB_SHA, actual_frozen_object_sha256=OBJECT_SHA,
        actual_frozen_executable_sha256=DRAGON_SHA, recovered_compatible_baseline_source_sha256=BASE_SHA,
        recovered_revision=BASE_REVISION, current_source_sha256=CURRENT_SHA,
        current_source_is_not_compiled_baseline=True,
        entire_frozen_compilation_source_identity_proved=False,
        actual_binary_review=dict(path=str(BINARY_REVIEW), sha256=digest(BINARY_REVIEW)),
        static_evidence="Frozen object DWARF FLUSP declaration1595 matches recovered source; both library "
          "member and executable disassembly contain REAL32 (2*IAL+1) conversion/multiply in vector and scalar paths.",
        scientific_source_correction_applied=False, shared_sources_or_libraries_modified=False,
        output_preservation_required="Every scientific XSM record must be word-exact to sealed map012; "
          "all 370 captured final FLUX64 groups, all three moments and all currents must be byte-exact."))
    for p in OUT.rglob("*"):
        if p.is_file():
            files[str(p)] = digest(p)
    write_new(OUT / "declaration.json", dict(
        schema="AXMAT_PRODUCTION_MAP012_ANGULAR_CAPTURE_V1", files=files,
        build_commands=commands, input_copies=inputs, original_deck_sha256=digest(deck),
        original_production_prepared_sha256=PREPARED_SHA, original_map012_seal_sha256=FINAL_SEAL_SHA,
        original_map011_seal_sha256=digest(PARENT / "result.json"),
        resource_roots=roots, min_free_bytes=8 * 2**30, artifact_budget_bytes=96 * 2**30,
        resources_before=before, archive_reserve_bytes=reserve, private_input_copy_bytes=copied,
        total_wall_seconds=1800, stage_wall_seconds=600, threads=1,
        numeric_children_at_once=1, retries=0, rss_cap_mib=512,
        live_guard_controls="Byte-exact existing OwnRSSSerialExecutor; actual positive child completed, "
                            "actual oversized child rejected and confirmed terminated; immutable proof files pinned.",
        numeric_environment=causal["numeric_environment"],
        native_library_aliases=causal["native_library_aliases"],
        native_library_linkage=causal["native_library_linkage"],
        numerical_loader_environment=causal["numerical_loader_environment"],
        actual_original_warm_stage_elapsed_seconds=34.166412875,
        geometry=dict(height_cm=150, physical_zone_heights_cm=[50, 50, 50],
                      axial_cells=48, angular_order=32, scattering_moments=3, basis_rank=1),
        final_call=dict(outer=3, inner=1, first_unconverged_group=371, inner_state=1,
                       group_ids=list(range(1, NG + 1)), selection="All groups' chronological last call; "
                         "every last call must be at the predeclared original native terminal3/1."),
        actual_source_contract=dict(ITPIJ=1, NANIS=2, NDIM=1, INSB=1, LSCAL=False,
                                    self_scattering_reduction_branch_reachable=False),
        capture="Actual post-SIGS S2 and NGIND/NPSYS; all qext/projected source coefficients; "
                "raw modal cell/one shared face array; actual basis, G, weights/mu/PL, "
                "G/T/radial/scattering/white factors; exact pre-factor native lower/diagonal/upper blocks, "
                "first block archive with bit-exact comparison of every subsequent native noncache rebuild; "
                "original normalization operands and pre/post FLUX64/source arrays.",
        scientific_replay_acceptance="Complete scientific XSM record equality to sealed map012; "
                "captured raw F2 equals native pre-normalization field; final capture equals published FLUX64.",
        reconstruction_relative_limit=5e-12, diagnostic_matrix_equation_limit=1e-10,
        original_accuracy_thresholds_changed=False, coefficient_fitting=False, CE_data_used=False,
        capture_only=True, production_solver_promoted=False, AAA_accuracy_qualified=False, ABA_admitted=False))
    print(json.dumps(dict(declaration=str(OUT / "declaration.json"),
                         declaration_sha256=digest(OUT / "declaration.json"))))


def child_admission(expected):
    require(OUT / "declaration.json", expected)
    declaration = read(OUT / "declaration.json")
    claim = read(OUT / "execution_claim.json")
    stages = read(OUT / "AAA/stages.json")["stages"]
    if (claim["parent_pid"] != os.getppid() or claim["declaration_sha256"] != expected
            or not stages or stages[-1]["status"] != "RUNNING"
            or stages[-1]["command"] != [sys.executable, *sys.argv]):
        raise ValueError("actual bounded own-parent archival child required")
    if any(os.environ.get(k) != "1" for k in (
        "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")):
        raise ValueError("one thread required for the archival audit")
    environment(declaration)
    return declaration


def read_capture(path):
    """Parse native stream words without any scale correction or field repair."""
    import numpy as np
    with Path(path).open("rb") as stream:
        def words(dtype, count):
            raw = stream.read(np.dtype(dtype).itemsize * count)
            if len(raw) != np.dtype(dtype).itemsize * count:
                raise ValueError("truncated production capture")
            return np.frombuffer(raw, dtype).copy()
        if stream.read(8) != b"AXCAP001":
            raise ValueError("undeclared capture schema")
        dims = words("<i4", 11)
        if dims[:6].tolist() != [NG, NUN, NZ, NA, NR, NL] or dims[7] != 3:
            raise ValueError("full actual production capture dimensions required")
        term_int, term_real = words("<i4", 9), words("<f8", 7)
        b2, norm = words("<f4", 4), words("<f8", 2)
        groups = []
        for g in range(1, NG + 1):
            record = dict(context=words("<i4", 9))
            for name in ("published", "published_source"):
                record[name] = words("<f8", NUN)
            if record["context"][0] != g:
                raise ValueError("all 370 groups in original order required")
            groups.append(record)
        if stream.read(1):
            raise ValueError("unexpected capture trailing words")
    directory = Path(path).parent
    with (directory / "angular_pre_normal.bin").open("rb") as stream:
        if stream.read(8) != b"AXCPN001" or np.frombuffer(stream.read(8), "<i4").tolist() != [NUN, NG]:
            raise ValueError("original pre-normalization archive dimensions differ")
        raw = stream.read()
        if len(raw) != NUN * NG * 8:
            raise ValueError("original pre-normalization field is incomplete")
        before = np.frombuffer(raw, "<f8").copy().reshape((NUN, NG), order="F")
    for g, record in enumerate(groups, 1):
        record["before_normal"] = before[:, g - 1]
        with (directory / f"angular_field_g{g:03d}.bin").open("rb") as stream:
            if stream.read(8) != b"AXCFD001":
                raise ValueError("actual angular field schema differs")
            header = np.frombuffer(stream.read(32), "<i4").copy()
            if header[:4].tolist() != record["context"][:4].tolist() or header[4:7].tolist() != dims[8:11].tolist():
                raise ValueError("angular field is not the last chronological source call")
            for name, dtype, count in [("integer", "<i4", dims[8]), ("single", "<f4", dims[9]),
                                        ("double", "<f8", dims[10])]:
                raw = stream.read(int(count) * np.dtype(dtype).itemsize)
                if len(raw) != int(count) * np.dtype(dtype).itemsize:
                    raise ValueError("actual angular field payload is incomplete")
                record[name] = np.frombuffer(raw, dtype).copy()
            if stream.read(1):
                raise ValueError("unexpected angular field trailing words")
        for name, prefix, magic in [("s2", "source", b"AXCS2001"),
                                     ("returned", "return", b"AXCRT001")]:
            with (directory / f"angular_{prefix}_g{g:03d}.bin").open("rb") as stream:
                if stream.read(8) != magic:
                    raise ValueError("actual source/return schema differs")
                header = np.frombuffer(stream.read(20), "<i4").copy()
                if header[:4].tolist() != record["context"][:4].tolist() or header[4] != NUN:
                    raise ValueError("source/return is not the final original group call")
                raw = stream.read()
                if len(raw) != NUN * 8:
                    raise ValueError("actual full source/return payload is incomplete")
                record[name] = np.frombuffer(raw, "<f8").copy()
    return dict(dimensions=dims, terminal_integer=term_int, terminal_real=term_real,
                b2=b2, normalization=norm, groups=groups)


def unpack(group, nmat):
    import numpy as np
    output = {}
    def split(data, fields):
        first = 0
        for name, shape in fields:
            count = int(np.prod(shape));output[name] = data[first:first + count].reshape(shape, order="F")
            first += count
        if first != data.size:
            raise ValueError("actual production archive payload layout differs")
    split(group["integer"], [("mat1d", (NZ,)), ("mat", (NZ, NR)),
                             ("ncode", (2,)), ("opposite", (NA,))])
    split(group["single"], [("vol1d", (NZ,)), ("total", (nmat + 1,)),
        ("sgas", (nmat + 1, NL)), ("basis", (NR, 1)), ("vol2d", (NR,)),
        ("zcode", (2,)), ("mu", (NA,)), ("w", (NA,)), ("pl", (NL, NA))])
    split(group["double"], [("radial2d", (NR, 3)), ("weight", (NR,)), ("mass", (1, 1)),
        ("total_projected", (1, 1, NZ)), ("radial_projected", (1, 1, NZ)),
        ("scat_projected", (1, 1, NL, NZ)), ("mn", (NA, NL)), ("dn", (NL, NA)),
        ("white_angle", (NA, NA)), ("white_mode", (1, 1)), ("qext", (1, NL, NZ, NR)),
        ("source_projected", (NL, NZ, 1)), ("cell", (NA, 1, NZ)), ("face", (NA, 1, NZ + 1)),
        ("modal_flux", (NL, NZ, 1)), ("modal_current", (NZ + 1, 1)),
        ("flux", (1, NL, NZ, NR)), ("current", (NZ + 1, NR)), ("xnei", (NA, NR))])
    return output


def audit_events(capture):
    import numpy as np
    latest = np.zeros((NG, 3), dtype="<i4")
    per_group_calls = np.zeros(NG, dtype="<i4")
    count = 0
    with (OUT / "AAA/angular_capture_events.bin").open("rb") as stream:
        if stream.read(8) != b"AXCEV001":
            raise ValueError("actual source dispatch inventory schema differs")
        header = np.frombuffer(stream.read(64), "<i4").copy()
        if header.size != 16 or header[11:].tolist() != [1, 2, 1, 1, 0]:
            raise ValueError("actual ITPIJ/NANIS/NDIM/INSB/LSCAL source contract differs")
        if header[[0, 1, 2, 4, 5, 6, 7, 8, 9, 10]].tolist() != [NG, NUN, NR * NZ, NL, 3, 3, 1, 0, 3, 0]:
            raise ValueError("actual source dispatch production contract differs")
        if header[3] != capture["dimensions"][6]:
            raise ValueError("actual dispatched material count differs")
        while raw := stream.read(16):
            if len(raw) != 16:
                raise ValueError("incomplete chronological source event")
            sequence, outer, inner, nactive = np.frombuffer(raw, "<i4")
            count += 1
            if sequence != count or not 1 <= nactive <= NG or outer <= 0 or inner <= 0:
                raise ValueError("invalid chronological source dispatch")
            raw = stream.read(int(nactive) * 4)
            if len(raw) != int(nactive) * 4:
                raise ValueError("incomplete original NGIND event")
            ngind = np.frombuffer(raw, "<i4").copy()
            raw = stream.read(NG * 4)
            if len(raw) != NG * 4:
                raise ValueError("incomplete original NPSYS event")
            npsys = np.frombuffer(raw, "<i4").copy()
            raw = stream.read(16)
            if len(raw) != 16:
                raise ValueError("incomplete original B2 event")
            b2 = np.frombuffer(raw, "<f4").copy()
            if (len(set(ngind.tolist())) != nactive or (ngind < 1).any() or (ngind > NG).any()
                    or not np.array_equal(ngind, np.flatnonzero(npsys) + 1) or b2[3] != 0):
                raise ValueError("actual post-SIGS dispatch metadata differs")
            latest[ngind - 1] = [sequence, outer, inner]
            per_group_calls[ngind - 1] += 1
    if count != capture["terminal_integer"][7]:
        raise ValueError("final publication does not cover every actual dispatch")
    for g, group in enumerate(capture["groups"]):
        if not np.array_equal(latest[g], group["context"][1:4]):
            raise ValueError("published group did not retain its chronological last call")
        if per_group_calls[g] != group["context"][6]:
            raise ValueError("every original noncache group call must archive or compare its rebuilt blocks")
    return dict(dispatches=count, all_370_groups_last_context=[3, 1],
                actual_NGIND_and_NPSYS_archived=True, metric_based_selection=False)


@contextmanager
def stream_xsm(path):
    """Use the frozen parser with bounded record reads, avoiding two 238 MiB maps.

    The complete snapshot equality walk touches both archives. Keeping those
    mappings resident alongside the capture would needlessly cross 512 MiB.
    """
    from snapshot_control_preflight import _XSM
    with Path(path).open("rb") as stream:
        before = os.fstat(stream.fileno())
        class Words:
            def __len__(self):
                return before.st_size
            def __getitem__(self, item):
                if not isinstance(item, slice) or item.step not in (None, 1):
                    raise ValueError("frozen XSM reader requested an unsupported byte access")
                first, stop, _ = item.indices(before.st_size)
                result = os.pread(stream.fileno(), stop - first, first)
                if len(result) != stop - first:
                    raise ValueError("incomplete original XSM record read")
                return result
        yield _XSM(Words())
        after = os.fstat(stream.fileno())
        if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
            raise ValueError("scientific archive changed during equality audit")


def audit(expected):
    import numpy as np
    from probe_refined_AAA_white_odd_response import same_object, field
    declaration = child_admission(expected)
    full, _, open_xsm, list_handles = modules()
    actual_env = dict(python=sys.version.split()[0], numpy=np.__version__)
    if any(actual_env[k] != declaration["numeric_environment"][k] for k in actual_env):
        raise ValueError("declared audit numerical environment changed")
    capture = read_capture(OUT / "AAA/angular_capture.bin")
    events = audit_events(capture)
    integers = capture["terminal_integer"]
    if integers[:7].tolist() != [3, 1, 371, 1, 1, 500, 740] or integers[8] != NG:
        raise ValueError("exact predeclared original terminal is required")
    real = capture["terminal_real"]
    if not (real[0] < real[1] and real[2] < real[3] and real[4] < real[5]):
        raise ValueError("unchanged strict native final gates did not pass")
    # The full output archive comparison checks all scientific moments/currents,
    # source, balance metadata and keff, including records not used by this audit.
    for name in ("candidate_axial.xsm", "candidate_snapshots.xsm"):
        with stream_xsm(FINAL / name) as old, stream_xsm(OUT / "AAA" / name) as new:
            same_object(old, old.root, new, new.root)
    with open_xsm(OUT / "AAA/candidate_axial.xsm") as archive:
        handles = list_handles(archive, archive.root, "FLUX64", NG)
        keff = field(archive, archive.root, "SPOT-KEFF64", "<f8", 1)
        if keff.tobytes() != capture["normalization"][:1].tobytes():
            raise ValueError("captured actual keff differs from published record")
        published = [np.frombuffer(archive.read(h[0], h[1]), "<f8").copy() for h in handles]
    if not np.isfinite(capture["normalization"]).all() or capture["normalization"][1] <= 0:
        raise ValueError("actual positive native normalization operands required")
    rows = []
    for g, (group, final) in enumerate(zip(capture["groups"], published, strict=True), 1):
        context = group["context"]
        if (context[2:4].tolist() != [3, 1] or context[1] != context[4] or context[5] <= 0
                or context[6] <= 0 or context[7] != context[4] or context[8] != 0):
            raise ValueError("chronological last capture is not original terminal group call")
        if any(not np.isfinite(group[k]).all() for k in (
            "single", "double", "s2", "returned", "before_normal", "published", "published_source")):
            raise ValueError("nonfinite actual archive words")
        a = unpack(group, int(capture["dimensions"][6]))
        if (a["ncode"].tolist() != [1, 1] or (a["zcode"] != 0).any()
                or (a["w"] <= 0).any() or (a["vol1d"] <= 0).any()):
            raise ValueError("unchanged positive quadrature and vacuum boundary contract required")
        if group["s2"][:1152].tobytes() != a["qext"].ravel(order="F").tobytes():
            raise ValueError("actual post-SIGS S2/qext source words differ")
        if (0.5 * (a["face"][:, :, :-1] + a["face"][:, :, 1:])).tobytes() != a["cell"].tobytes():
            raise ValueError("actual native diamond cell/shared-face identity differs")
        # Every source projection is tested, with the exact region accumulation
        # order of the frozen rank1 solver, including the native void-material skip.
        projected_source = np.zeros((NL, NZ), dtype="<f8")
        for iz in range(NZ):
            for region in range(NR):
                if a["mat"][iz, region] == 0:
                    continue
                for l in range(NL):
                    projected_source[l, iz] += (float(a["weight"][region]) *
                        float(a["basis"][region, 0])) * float(a["qext"][0, l, iz, region])
        if projected_source.tobytes() != a["source_projected"][:, :, 0].tobytes():
            raise ValueError("actual complete projected source coefficients differ")
        returned = np.concatenate([a["flux"].ravel(order="F"), a["current"].ravel(order="F"),
                                   a["xnei"].ravel(order="F")])
        if (returned.tobytes() != group["returned"].tobytes()
                or group["returned"].tobytes() != group["before_normal"].tobytes()
                or group["published"].tobytes() != final.tobytes()):
            raise ValueError("all raw returned moments/currents or final FLUX64 words changed")
        normalized = group["returned"] * (capture["normalization"][0] / capture["normalization"][1])
        if normalized.tobytes() != final.tobytes():
            raise ValueError("original one global normalization operation differs")
        normalized_source = group["s2"] * (capture["normalization"][0] / capture["normalization"][1])
        if normalized_source.tobytes() != group["published_source"].tobytes():
            raise ValueError("actual raw S2 does not reproduce original normalized REAL64 source")
        # Reproduce actual native summation/reconstruction order, with no BLAS.
        modal = np.zeros((NL, NZ), dtype="<f8");current = np.zeros(NZ + 1, dtype="<f8")
        for l in range(NL):
            for n in range(NA):
                modal[l] += a["dn"][l, n] * a["cell"][n, 0]
        for n in range(NA):
            current += float(a["w"][n]) * float(a["mu"][n]) * a["face"][n, 0]
        if (modal.tobytes() != a["modal_flux"][:, :, 0].tobytes()
                or current.tobytes() != a["modal_current"][:, 0].tobytes()):
            raise ValueError("stored angular fields do not reproduce actual moments/currents")
        if (a["face"][a["mu"] > 0, 0, 0] != 0).any() or (a["face"][a["mu"] < 0, 0, -1] != 0).any():
            raise ValueError("actual vacuum incoming fields must be exactly zero")
        block_path = OUT / "AAA" / f"angular_collision_g{g:03d}.bin"
        with block_path.open("rb") as stream:
            if stream.read(8) != b"AXCBL001":
                raise ValueError("actual native collision schema differs")
            header = np.frombuffer(stream.read(32), "<i4").copy()
            blocks = np.frombuffer(stream.read(), "<f8").copy()
        if (header[0] != g or header[1] != context[5] or header[4:].tolist() != [NA, NZ + 1, 0, 0]
                or blocks.size != 3 * NA * NA * (NZ + 1) or not np.isfinite(blocks).all()):
            raise ValueError("complete actual first native collision block inventory required")
        lower, diagonal, upper = [
            blocks[j * NA * NA * (NZ + 1):(j + 1) * NA * NA * (NZ + 1)].reshape(
                (NA, NA, NZ + 1), order="F") for j in range(3)]
        face = a["face"][:, 0]
        rhs = np.zeros((NA, NZ + 1))
        for iz in range(NZ):
            q = np.zeros(NA)
            for l in range(NL):
                q += a["mn"][:, l] * a["source_projected"][l, iz, 0]
            rhs[a["mu"] > 0, iz + 1] = float(a["vol1d"][iz]) * q[a["mu"] > 0]
            rhs[a["mu"] < 0, iz] = float(a["vol1d"][iz]) * q[a["mu"] < 0]
        defect = np.empty_like(rhs);scale = np.empty_like(rhs)
        for iz in range(NZ + 1):
            terms = [diagonal[:, :, iz] @ face[:, iz]]
            absolute = [abs(diagonal[:, :, iz]) @ abs(face[:, iz])]
            if iz:
                terms.append(lower[:, :, iz] @ face[:, iz - 1])
                absolute.append(abs(lower[:, :, iz]) @ abs(face[:, iz - 1]))
            if iz < NZ:
                terms.append(upper[:, :, iz] @ face[:, iz + 1])
                absolute.append(abs(upper[:, :, iz]) @ abs(face[:, iz + 1]))
            defect[:, iz] = sum(terms) - rhs[:, iz]
            scale[:, iz] = sum(absolute) + abs(rhs[:, iz])
        null_nonzero = (scale == 0) & (defect != 0)
        ratio = np.divide(abs(defect), scale, out=np.zeros_like(scale), where=scale > 0)
        rows.append(dict(group=g, context=context.tolist(), native_block_assembly_count=int(context[6]),
            native_block_cache_enabled=False, all_rebuilt_native_blocks_byte_exact=True,
            raw_S2_one_global_normalization_published_source_byte_exact=True,
            minimum_modal_cell=float(a["cell"].min()),
            minimum_shared_face=float(a["face"].min()), negative_modal_cell_count=int((a["cell"] < 0).sum()),
            negative_shared_face_count=int((a["face"] < 0).sum()),
            minimum_physical_angular_cell=float((a["basis"][:, 0, None, None] * a["cell"][:, 0][None]).min()),
            minimum_physical_angular_face=float((a["basis"][:, 0, None, None] * a["face"][:, 0][None]).min()),
            full_native_matrix_equation_relative=float(ratio.max()),
            zero_scale_nonzero_defect_count=int(null_nonzero.sum()),
            original_1e10_diagnostic_gate_passed=bool(not null_nonzero.any() and ratio.max() <= 1e-10),
            all_three_raw_moments_and_currents_byte_exact=True))
        # Preserve the raw defect and scale for every group; positivity and the
        # equation ledger are diagnostic findings, never repaired or hidden.
        np.savez(OUT / "audit" / f"ledger_g{g:03d}.npz", defect=defect, scale=scale,
                 ratio=ratio, zero_scale_nonzero_defect=null_nonzero)
    write_new(OUT / "audit/result.json", dict(
        classification="COMPLETE_PRODUCTION_ANGULAR_CAPTURE_ONLY", groups=rows,
        chronological_inventory=events,
        complete_production_370_groups=True, original_map012_scientific_records_word_exact=True,
        original_terminal_passed=True, all_three_moments_and_currents_byte_exact=True,
        original_keff_byte_exact=True, raw_fields_and_sources_unmodified=True,
        negative_fields_repaired=False, equation_accounting_modified=False,
        original_accuracy_thresholds_changed=False, production_solver_promoted=False,
        AAA_accuracy_qualified=False, ABA_admitted=False))
    print("AXMAT-PRODUCTION-ANGULAR-CAPTURE-AUDITED")


def run(expected):
    if not expected:
        raise ValueError("explicit frozen declaration SHA256 required")
    require(OUT / "declaration.json", expected)
    declaration = read(OUT / "declaration.json")
    environment(declaration)
    full, production, _, _ = modules()
    resource = production.DiskResources(ART, declaration["resource_roots"],
        declaration["min_free_bytes"], declaration["artifact_budget_bytes"])
    write_new(OUT / "execution_claim.json", dict(parent_pid=os.getpid(), declaration_sha256=expected,
        started_unix=time.time(), started_monotonic=time.monotonic()))
    runner = full.OwnRSSSerialExecutor(OUT, declaration["total_wall_seconds"], "AAA", resource)
    result = dict(classification="FAILED_PRODUCTION_ANGULAR_CAPTURE_NO_RETRY", error=None,
                  AAA_accuracy_qualified=False, ABA_admitted=False)
    started = time.monotonic()
    try:
        for i, command in enumerate(declaration["build_commands"]):
            runner.execute(OUT / "build", f"build_{i:02d}", command, 600)
        write_new(OUT / "runtime/build_identity.json", dict(
            files={str(p.relative_to(OUT)): digest(p) for p in [
                OUT / "runtime/Dragon", *sorted((OUT / "build").glob("*.o")),
                *sorted((OUT / "build").glob("*.mod"))]}, callback_only=True))
        runner.execute(OUT / "AAA", "capture_replay", [str(OUT / "runtime/Dragon")], 600,
            "AXMAT-PICARD-AXIAL-COMPLETE", deck="picard_axial.x2m")
        # Raw returned fields and blocks survive every later audit failure.
        captured = sorted((OUT / "AAA").glob("angular*.bin"))
        write_new(OUT / "raw_capture_receipt.json", dict(
            files={str(p.relative_to(OUT)): digest(p) for p in captured},
            original_output_files={name: digest(OUT / "AAA" / name)
                for name in ("candidate_axial.xsm", "candidate_snapshots.xsm")},
            raw_capture_count=len(captured), selection="Original terminal all-group last chronological calls"))
        if len(captured) != 4 * NG + 3:
            raise ValueError("complete all-group raw source/field/return/block archives required")
        runner.execute(OUT / "audit", "audit", [sys.executable, str(Path(__file__).resolve()),
            "audit", "--sha256", expected], 600, "AXMAT-PRODUCTION-ANGULAR-CAPTURE-AUDITED")
        stages = read(OUT / "AAA/stages.json")["stages"]
        if len(stages) != 6 or any(s["status"] != "PASS" for s in stages):
            raise ValueError("all four build stages, one replay and one audit must complete")
        for stage in stages:
            watch = read((OUT / (stage["label"] + ".log")).with_suffix(".watchdog.json"))
            if (watch["returncode"] != 0 or watch["limit_failure"] is not None
                    or not 0 <= watch["sampled_peak_rss_mib"] < 512
                    or not 0 <= watch["elapsed_seconds"] < 600
                    or watch["own_child_only"] is not True
                    or watch["liveness_group_cleanup"] is not True):
                raise ValueError("actual child resource receipt failed")
        if time.monotonic() - started >= declaration["total_wall_seconds"]:
            raise ValueError("complete capture exceeded the unchanged total wall budget")
        actual_bytes = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file() and not p.is_symlink())
        if actual_bytes >= declaration["archive_reserve_bytes"]:
            raise ValueError("actual complete capture archive exceeded its storage reservation")
        result["actual_archive_bytes_before_closeout"] = actual_bytes
        result["classification"] = "COMPLETE_BOUNDED_PRODUCTION_ANGULAR_CAPTURE_ONLY"
    except BaseException as error:
        result["error"] = repr(error)
        raise
    finally:
        result.update(elapsed_seconds=time.monotonic() - started, resources=resource.check())
        write_new(OUT / "driver_result.json", result)
        environment(declaration)
    write_new(OUT / "seal.json", dict(schema="AXMAT_PRODUCTION_ANGULAR_CAPTURE_SEAL_V1",
        files={str(p.relative_to(OUT)): digest(p) for p in OUT.rglob("*") if p.is_file()}))
    print(json.dumps(result))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "run", "audit"))
    parser.add_argument("--sha256")
    args = parser.parse_args()
    dict(prepare=prepare, run=lambda: run(args.sha256), audit=lambda: audit(args.sha256))[args.action]()
