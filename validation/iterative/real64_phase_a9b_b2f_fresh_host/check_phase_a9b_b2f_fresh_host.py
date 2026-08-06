#!/usr/bin/env python3
"""Independent static gate for the B2f fresh-output bootstrap contract."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
B2B = ROOT / "src/SPOR64_B2B.f90"
B2C = ROOT / "src/SPOR64_B2C.f90"
FLU = ROOT / "src/FLU.f"
FLUGPI = ROOT / "src/FLUGPI.f"
PLANE = ROOT / "data/SpotPlaneR64.c2m"
REFERENCE = ROOT / "data/SpotRefR64.c2m"
LEGACY_PLANE = ROOT / "data/SpotPlaneFS.c2m"
LEGACY_REFERENCE = ROOT / "data/SpotRefFS.c2m"
HARNESS = HERE / "test_b2f_fresh_host.f90"
STUBS = HERE / "b2f_accept_stubs.f90"
RUNNER = HERE / "run_phase_a9b_b2f_fresh_host.sh"
MANIFEST = HERE / "precision_manifest.json"
PROJECT_README = ROOT / "README.md"

PARENT_COMMIT = "bbc188a6b5a268fdb30a7e855e2c3a140ac9d066"
PARENT_RECEIPT_SHA256 = (
    "a87f8d14706e6d9f0812f1140b8e2fced59e52c60486860a59c221a963cd2bae"
)
LEGACY_SHA256 = {
    LEGACY_PLANE: "69a2931c817d298a3af36f5e1f55760c58dd55229c73002b4b01d3a4797e27b5",
    LEGACY_REFERENCE: "db763e8c013d9f753ae6eb635dc5490c6bb34b9f23ea211dd3b282b6ec031742",
}
ARTIFACTS = {
    "validation/artifacts/iterative-radial-floor/restart_cap.xsm": (
        "7291d8d88b5be07cd570131ea45ce5f283d55a37e3577197626001c59d9b8c89",
        904652,
    ),
    "validation/artifacts/raw-moc-capture/common/restart_macro0.xsm": (
        "6eb2920473f4cb8d27b6377bcb59b42833c8ebf9a0fc57925341d12ccac0a617",
        9878532,
    ),
    "validation/artifacts/raw-moc-capture/common/restart_track.xsm": (
        "2d868b87e2003c10c09da1ec8f8e6fd97f2a2629a680a46d7f898e2e5e1ed598",
        8080,
    ),
    "validation/artifacts/raw-moc-capture/common/restart_system.xsm": (
        "a8797a7d42fdab574eb183bc2ecf0e2b53c992fdd2dd4c61d40c72a53746e599",
        840124,
    ),
    "validation/artifacts/raw-moc-capture/common/restart_source.xsm": (
        "6942f61ba2cc7ab0d5cf9a4104959809a388fab441da82730cf64de74a48769f",
        303620,
    ),
}


class ContractError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def where(text: str, token: str, message: str) -> int:
    require(token in text, message)
    return text.index(token)


def digest_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def strip_fortran_comments(text: str) -> str:
    kept: list[str] = []
    for raw in text.splitlines():
        if raw.startswith(("*", "c", "C")):
            kept.append("")
            continue
        quote: str | None = None
        line: list[str] = []
        index = 0
        while index < len(raw):
            char = raw[index]
            if quote is not None:
                line.append(char)
                if char == quote:
                    if index + 1 < len(raw) and raw[index + 1] == quote:
                        line.append(raw[index + 1])
                        index += 1
                    else:
                        quote = None
            elif char in "'\"":
                quote = char
                line.append(char)
            elif char == "!":
                break
            else:
                line.append(char)
            index += 1
        kept.append("".join(line))
    return "\n".join(kept)


def compact_fortran(text: str) -> str:
    return re.sub(r"[\s&]+", "", strip_fortran_comments(text)).upper()


def compact_deck(text: str) -> str:
    kept = [line for line in text.splitlines() if not line.lstrip().startswith("*")]
    return re.sub(r"\s+", "", "\n".join(kept)).upper()


def reject_empirical_terms(text: str, label: str) -> None:
    clean = strip_fortran_comments(text)
    for word in ("ALPHA", "OMEGA", "DAMPING", "RELAXATION", "MIXING"):
        require(re.search(rf"\b{word}\b", clean, re.IGNORECASE) is None,
                f"{label} introduces {word}")


def check_legacy_bytes(plane_bytes: bytes, reference_bytes: bytes) -> None:
    require(digest_bytes(plane_bytes) == LEGACY_SHA256[LEGACY_PLANE],
            "legacy SpotPlaneFS changed")
    require(digest_bytes(reference_bytes) == LEGACY_SHA256[LEGACY_REFERENCE],
            "legacy SpotRefFS changed")


def check_plane_text(text: str) -> None:
    packed = compact_deck(text)
    exact_call = (
        "FLUX:=FLU:MACRO0TRACKTRACK_FSYSTEMFSOURCEFLUX_OLD::"
        "EDIT0TYPESINITONREBAEXTE500<<FLU_EPS>>"
        "UNKT<<FLU_EPS>>THER740<<FLU_EPS>>ACCE33R64;"
    )
    require(packed.count(exact_call) == 1, "exact seven-entry R64 plane call")
    require(
        "PARAMETERSYSTEMFLUXSNAPMICROLIB2TRACKTRACK_FFLUX_OLD::" in packed,
        "FLUX_OLD plane parameter missing",
    )
    require(packed.count("R64") == 1, "R64 must be one bare opt-in")
    require("REBAON" not in packed, "REBA takes no ON operand")
    reject_empirical_terms(text, "SpotPlaneR64")


def check_reference_text(text: str) -> None:
    packed = compact_deck(text)
    require(packed.count("PROCEDURESPOTPLANER64;") == 1,
            "SpotPlaneR64 procedure declaration")
    require(packed.count("FLUX_OLD:=FLUX;") == 1,
            "one deep FLUX_OLD copy")
    require(packed.count("FLUX:=DELETE:FLUX;") == 1,
            "one old-output delete")
    require(
        packed.count(
            "SYSTEMFLUX:=SPOTPLANER64SNAPMICROLIB2TRACKTRACK_FFLUX_OLD::"
            "<<ISNAP>><<KEFF>><<FLU_EPS>>;"
        ) == 1,
        "copy-delete-call lifecycle",
    )
    require(
        where(packed, "FLUX_OLD:=FLUX;", "seed-copy statement")
        < where(packed, "FLUX:=DELETE:FLUX;", "output-delete statement")
        < where(packed, "SYSTEMFLUX:=SPOTPLANER64", "R64 procedure call"),
        "seed copy must precede delete and call",
    )
    require(
        packed.count("SNAP:=BACKUP:SNAPFLUX::ITEM<<ISNAP>>;") == 1,
        "fresh result backup",
    )
    reject_empirical_terms(text, "SpotRefR64")


def check_default_off() -> None:
    check_legacy_bytes(LEGACY_PLANE.read_bytes(), LEGACY_REFERENCE.read_bytes())
    for path in sorted(
        candidate for candidate in ROOT.rglob("*")
        if candidate.suffix.lower() in (".c2m", ".x2m")
    ):
        if path in (PLANE, REFERENCE):
            continue
        clean = "\n".join(
            line for line in path.read_text(errors="replace").splitlines()
            if not line.lstrip().startswith("*")
        )
        require("SpotPlaneR64" not in clean and "SpotRefR64" not in clean,
                f"shipped deck selects R64: {path.relative_to(ROOT)}")


def check_b2b_text(text: str) -> None:
    packed = compact_fortran(text)
    required = (
        "IF(NENTRY/=7)RETURN",
        "IF(HENTRY(1)/='FLUX')RETURN",
        "IF(HENTRY(2)/='MACRO0')RETURN",
        "IF(HENTRY(3)/='TRACK')RETURN",
        "IF(HENTRY(4)/='TRACK_F')RETURN",
        "IF(HENTRY(5)/='SYSTEM')RETURN",
        "IF(HENTRY(6)/='FSOURCE')RETURN",
        "IF(HENTRY(7)/='FLUX_OLD')RETURN",
        "IF(IENTRY(1)/=1)RETURN",
        "IF(.NOT.LCM_ENTRY_KIND(IENTRY(7)))RETURN",
        "IF(JENTRY(1)/=0)RETURN",
        "IF(ANY(JENTRY(2:7)/=2))RETURN",
        "DOIR=1,7IF(.NOT.C_ASSOCIATED(KENTRY(IR)))RETURNENDDO",
        "IPFLUX=KENTRY(1)",
        "IPSEED=KENTRY(7)",
        "DOIR=2,7IF(C_ASSOCIATED(IPFLUX,KENTRY(IR)))RETURNENDDO",
        "CALLLCMINF(IPFLUX,OUTPUT_FILE,OUTPUT_NAME,OUTPUT_EMPTY,ILONG,OUTPUT_LCM)",
        "IF(.NOT.OUTPUT_LCM.OR.ILONG/=-1.OR..NOT.OUTPUT_EMPTY)RETURN",
        "IF(TRIM(OUTPUT_NAME)/='/')RETURN",
        "IF(REC.OR..NOT.LIMERG)RETURN",
        "ABSENT_RECORD(IPSEED,'SPOT-R64')",
        "MACRO_STORED_COMPONENTS=3",
        "TRACK_ACTIVE_COMPONENTS=1",
        "RECORD_MATCHES(KPMACR,'NJJS01',NMAT,1)",
        "RECORD_MATCHES(KPMACR,'NJJS02',NMAT,1)",
        "JPFLUX=LCMGID(IPSEED,'FLUX')",
        "JPSOURCE=LCMGID(IPSOU,'DSOUR')",
        "CALLLCMGET(KPMACR,'NJJS00',NJJ_STAGE)",
        "CALLLCMGET(KPMACR,'IJJS00',IJJ_STAGE)",
        "CALLLCMGET(KPMACR,'IPOS00',IPOS_STAGE)",
        "CALLLCMGET(KPMACR,'SCAT00',SCAT_STAGE32)",
        "TERMINAL_FLUX64,TERMINAL_SOURCE64,KEYFLX_BASE1,NMERG,IMERG,",
    )
    for token in required:
        require(token in packed, f"B2B contract token missing: {token}")

    require("LCMGID(IPFLUX" not in packed and "LCMGET(IPFLUX" not in packed,
            "fresh output is read as input")
    require("LCMGID(IPSEED,'SOUR')" not in packed,
            "legacy seed SOUR used as fixed source")
    require("ABSENT_RECORD(IPSEED,'SOUR')" not in packed,
            "legacy seed SOUR incorrectly blocks bootstrap")
    for label in ("01", "02"):
        require(f"LCMGET(KPMACR,'NJJS{label}'" not in packed,
                f"inactive NJJS{label} loaded")
        for prefix in ("IJJS", "IPOS", "SCAT"):
            require(f"'{prefix}{label}'" not in packed,
                    f"inactive {prefix}{label} enters B2B")
    for writer in ("LCMDID", "LCMLID", "LCMLIL", "LCMPDL", "LCMPTC",
                   "LCMPUT", "LCMDEL"):
        require(re.search(rf"\b{writer}\s*\(", strip_fortran_comments(text),
                          re.IGNORECASE) is None,
                f"B2B owns forbidden write {writer}")
    require("FLUDRV" not in packed, "B2B fallback to FLUDRV")
    reject_empirical_terms(text, "SPOR64_B2B")


def api_count(text: str, name: str) -> int:
    return len(re.findall(rf"\b{name}\s*\(", strip_fortran_comments(text),
                          re.IGNORECASE))


def check_b2c_text(text: str) -> None:
    packed = compact_fortran(text)
    signature = (
        "SUBROUTINESPOR64_B2C_PUBLISH(IPFLUX,ACCEPTED_TOKEN,TERMINAL_FLUX64,"
        "TERMINAL_SOURCE64,KEYFLX_BASE1,NMERG_INPUT,IMERGE_INPUT,"
        "LEAK1D_INPUT32,EPSOUT32,EPSUNK32,EPSINR32,COPTIO,MACRO_NAME,"
        "TRACK_NAME,SYSTEM_NAME,STATUS)"
    )
    require(signature in packed, "exact B2C publisher ABI")
    for token in (
        "IF(ACCEPTED_TOKEN/=ACCEPTED_UNPUBLISHED)RETURN",
        "IF(NMERG_INPUT/=1.OR.SIZE(IMERGE_INPUT)/=NMAT)RETURN",
        "IF(ANY(IMERGE_INPUT/=1))RETURN",
        "IF(.NOT.EMPTY_LCM_ROOT(IPFLUX))RETURN",
        "CALLLCMPTC(IPFLUX,'SIGNATURE',12,SIGNATURE)",
        "CALLLCMPUT(IPFLUX,'IMERGE-LEAK',NMAT,1,IMERGE_INPUT)",
        "STATE_VECTOR(18)=NMERG_INPUT",
        "TRIM(OBJECT_NAME)=='/'",
    ):
        require(token in packed, f"B2C contract token missing: {token}")

    inventory = {
        "LCMINF": 1,
        "LCMDID": 1,
        "LCMLID": 4,
        "LCMPDL": 4,
        "LCMPTC": 5,
        "LCMPUT": 5,
        "LCMGID": 0,
        "LCMLIL": 0,
        "LCMDEL": 0,
    }
    for name, expected in inventory.items():
        require(api_count(text, name) == expected,
                f"B2C {name} inventory differs")

    empty = where(packed, "IF(.NOT.EMPTY_LCM_ROOT(IPFLUX))RETURN",
                  "empty-root preflight")
    allocate = where(packed, "ALLOCATE(FLUX_STAGE32", "REAL32 staging allocate")
    convert_flux = where(packed, "FLUX_STAGE32=REAL(TERMINAL_FLUX64,REAL32)",
                         "flux staging conversion")
    convert_source = where(
        packed, "SOURCE_STAGE32=REAL(TERMINAL_SOURCE64,REAL32)",
        "source staging conversion")
    first_write = where(packed, "AUTHORITY=LCMDID(IPFLUX,'SPOT-R64')",
                        "first authority write")
    require(empty < allocate < convert_flux < first_write,
            "flux staging is not pre-write")
    require(empty < allocate < convert_source < first_write,
            "source staging is not pre-write")

    order = (
        "CALLLCMPDL(AUTHORITY_FLUX,IG,NUNKNO,4,TERMINAL_FLUX64(:,IG))",
        "CALLLCMPDL(AUTHORITY_SOURCE,IG,NUNKNO,4,TERMINAL_SOURCE64(:,IG))",
        "CALLLCMPDL(LEGACY_FLUX,IG,NUNKNO,2,FLUX_STAGE32(:,IG))",
        "CALLLCMPDL(LEGACY_SOURCE,IG,NUNKNO,2,SOURCE_STAGE32(:,IG))",
        "STATUS=SPOR64_B2C_CHILD_PUBLISHED",
        "CALLLCMPTC(IPFLUX,'SIGNATURE',12,SIGNATURE)",
        "CALLLCMPUT(IPFLUX,'IMERGE-LEAK',NMAT,1,IMERGE_INPUT)",
        "STATUS=SPOR64_B2C_DRIVER_COMMITTED",
        "CALLLCMPTC(IPFLUX,'LINK.MACRO',12,MACRO_NAME)",
        "CALLLCMPUT(IPFLUX,'SPOT-LEAK1D',NGRP,2,LEAK1D_INPUT32)",
        "STATUS=SPOR64_B2C_HOST_COMMITTED",
    )
    positions = [where(packed, token, f"publication token: {token}")
                 for token in order]
    require(positions == sorted(positions), "B2C publication order differs")
    require("FLUX_OLD" not in packed, "publisher can access seed")
    require("FLUDRV" not in packed, "publisher fallback to FLUDRV")
    reject_empirical_terms(text, "SPOR64_B2C")


def check_flu_text(flu_text: str, flugpi_text: str) -> None:
    packed = compact_fortran(flu_text)
    start = where(packed, "IF(LR64)THEN", "FLU R64 branch")
    require("ENDIF" in packed[start:], "FLU R64 branch terminator")
    end = packed.index("ENDIF", start) + len("ENDIF")
    branch = packed[start:end]
    require(branch.count("CALLSPOR64_B2B_INGRESS(") == 1,
            "one FLU B2B call")
    require("RETURN" in branch, "R64 branch does not return")
    require("CALLFLUDRV" not in branch, "R64 branch falls back to FLUDRV")
    require("CALLFLUDRV" in packed[end:],
            "legacy FLUDRV call is not after R64 return")
    parser = compact_fortran(flugpi_text)
    require("LR64=.FALSE." in parser, "R64 no longer defaults OFF")
    require(parser.count("LR64=.TRUE.") == 1, "R64 parser assignment differs")


def check_global_publisher_callsites(overrides: dict[str, str] | None = None) -> None:
    found: list[str] = []
    overrides = overrides or {}
    for path in sorted((ROOT / "src").glob("*.[fF]*")):
        text = overrides.get(path.name, path.read_text(errors="replace"))
        if re.search(r"\bCALL\s+SPOR64_B2C_PUBLISH\s*\(",
                     strip_fortran_comments(text), re.IGNORECASE):
            found.append(path.name)
    require(found == ["SPOR64_B2B.f90"],
            f"publisher callsites differ: {found}")


def check_harness_text(text: str) -> None:
    packed = compact_fortran(text)
    for token in (
        "INTEGER,PARAMETER::NENTRY=7",
        "HENTRY=[CHARACTER(LEN=12)::'FLUX','MACRO0','TRACK','TRACK_F',"
        "'SYSTEM','FSOURCE','FLUX_OLD']",
        "IENTRY=[1,2,2,3,2,2,2]",
        "JENTRY=[0,2,2,2,2,2,2]",
        "CALLRUN_BLOCKED_CASE('B2F-LIMERG',1)",
        "CALLRUN_BLOCKED_CASE('B2F-NONEMPTY',2)",
        "CALLRUN_BLOCKED_CASE('B2F-ALIAS',3)",
        "CALLRUN_BLOCKED_CASE('B2F-NOSEED',4)",
        "CALLRUN_BLOCKED_CASE('B2F-ACCESS',5)",
        "CALLRUN_BLOCKED_DAUGHTER_CASE()",
        "IF(B2B_CALLS/=7)ERRORSTOP'B2BCALLINVENTORYDIFFERS'",
        "IF(PUBLISHER_CALLS/=8)ERRORSTOP'PUBLISHERCALLINVENTORYDIFFERS'",
        "IF(SPOMOC_TOTAL/=1.OR.XDRTA2_TOTAL/=1.OR.CORE_TOTAL/=1)",
        "'B2FFRESH-HOSTPASS'",
        "'B2FREAL-B2B-CALLS='",
        "'B2FPRODUCTION-PUBLISHER-CALLS='",
        "CALLREQUIRE_RECORD_COUNT(ROOT,13)",
        "IF(FOUND/=EXPECTED)ERRORSTOP'CHARACTERRECORDDIFFERS'",
    ):
        require(token in packed, f"harness token missing: {token}")
    require(text.count("call LCMOP(") == 14, "harness LCMOP inventory differs")
    require(text.count(",2,2,0)") == 5, "five XSM opens must be read-only")
    require(api_count(text, "SPOR64_B2C_PUBLISH") == 7,
            "seven direct publisher calls")
    require(packed.count("PUBLISHER_CALLS=PUBLISHER_CALLS+1") == 8,
            "publisher counter increments")
    require("DOORFV" not in packed and "MCGMRE" not in packed,
            "harness embeds a production solver")


def check_stub_text(text: str) -> None:
    packed = compact_fortran(text)
    for token in (
        "TERMINAL_FLUX64=INITIAL_FLUX64",
        "TERMINAL_SOURCE64=FIXED_SOURCE64",
        "CUTOFF_VISIT64=0_INT64",
        "ACCEPTED=.TRUE.",
        "OK=.TRUE.",
        "SPOMOC_ACTIVE=.FALSE.",
        "XDRTA2_TOTAL=XDRTA2_TOTAL+1",
        "CORE_TOTAL=CORE_TOTAL+1",
    ):
        require(token in packed, f"stub token missing: {token}")
    require("CALLDOORFV" not in packed and "CALLMCGMRE" not in packed,
            "stub acquired transport work")


def check_runner_text(text: str) -> None:
    required = (
        f"EXPECTED_PARENT_COMMIT={PARENT_COMMIT}",
        f"EXPECTED_PARENT_HASH={PARENT_RECEIPT_SHA256}",
        "FC=/opt/homebrew/bin/gfortran",
        'copy_exact "$ROOT/src/SPOR64_B2C.f90" "$SOURCE_DIR/SPOR64_B2C.f90"',
        'copy_exact "$ROOT/src/SPOR64_B2B.f90" "$SOURCE_DIR/SPOR64_B2B.f90"',
        'chmod 444 "$CASE_DIR/seed.xsm"',
        '-Wno-unused-dummy-argument',
        '"$OBJECT_DIR/b2f_accept_stubs.o"',
        '"$OBJECT_DIR/SPOR64_B2C.o"',
        '"$OBJECT_DIR/SPOR64_B2B.o"',
        '"$BUILD_DIR/test_b2f_fresh_host"',
        "^B2F FRESH-HOST PASS$",
        "^B2F REAL-B2B-CALLS=7$",
        "^B2F PRODUCTION-PUBLISHER-CALLS=8 COMMITS=1$",
        "python3 -m unittest -v test_phase_a9b_b2f_fresh_host_contract",
        "CONTRACT-TESTS=47 MUTATION-CASES=46",
        "PRODUCTION-XDRTA2-CALLS=0 PRODUCTION-CORE-CALLS=0",
        "DRAGON-EXECUTIONS=0 SEQUENTIAL-TRACKING-RECORD-READS=0 TRANSPORT-SOLVES=0",
        "RADIAL-CONVERGENCE=NOT-EVALUATED",
        "OUTER-PICARD-CONVERGENCE=NOT-EVALUATED",
    )
    for token in required:
        require(token in text, f"runner token missing: {token}")
    for forbidden in (
        '"$ROOT/src/SPOR64_A9.f90"',
        '"$ROOT/src/XDRTA2.f"',
        '"$ROOT/bin/Darwin_arm64/Dragon"',
        "make -C src",
        "FILOPN",
        ".x2m",
    ):
        require(forbidden not in text, f"runner crosses boundary: {forbidden}")
    require(text.count('"$BUILD_DIR/test_b2f_fresh_host" \\\n') == 1,
            "harness execution count differs")


def check_manifest_data(data: dict) -> None:
    require(data["schema"] == "spot.real64.phase-a9b-b2f.fresh-host.v1",
            "manifest schema")
    require(data["claim"] ==
            "FRESH-OUTPUT-READ-ONLY-SEED-BOOTSTRAP-CONTRACT-CLOSED",
            "manifest claim")
    require(data["parent"]["commit"] == PARENT_COMMIT, "manifest parent")
    require(data["parent"]["receipt_sha256"] == PARENT_RECEIPT_SHA256,
            "manifest parent receipt")
    default = data["default_off"]
    require(default["r64_default"] is False, "R64 default")
    require(default["legacy_SpotPlaneFS_changed"] is False,
            "legacy plane status")
    require(default["legacy_SpotRefFS_changed"] is False,
            "legacy reference status")
    require(default["shipped_top_level_selects_SpotRefR64"] is False,
            "top-level R64 selection")
    host = data["host_contract"]
    require(host["entry_count"] == 7, "manifest entry count")
    require(host["entries"] ==
            ["FLUX", "MACRO0", "TRACK", "TRACK_f", "SYSTEM", "FSOURCE",
             "FLUX_OLD"], "manifest entry order")
    require(host["access"] == ["create"] + ["read-only"] * 6,
            "manifest access roles")
    require(host["output_active_directory"] == "/",
            "manifest output root")
    require(host["seed_container_type"] == 10 and
            host["seed_element_type"] == 2, "manifest seed schema")
    require(host["bootstrap_only"] is True and
            host["continuous_REAL64_iteration"] is False, "bootstrap scope")
    scattering = data["scattering_order"]
    require(scattering["stored_components"] == 3 and
            scattering["active_components"] == 1 and
            scattering["effective_max_order"] == 0, "active P0 identity")
    require(scattering["P0_records_loaded"] ==
            ["NJJS00", "IJJS00", "IPOS00", "SCAT00"], "P0 records")
    require(scattering["P1_P2_shape_records_validated"] ==
            ["NJJS01", "NJJS02"], "inactive shape records")
    evidence = data["execution_evidence"]
    expected_counts = {
        "contract_tests": 47,
        "mutation_cases": 46,
        "real_B2B_calls": 7,
        "accepted_ingress_scenarios": 1,
        "blocked_ingress_scenarios": 6,
        "production_publisher_calls": 8,
        "production_publisher_commits": 1,
        "publisher_preflight_rejections": 7,
        "stub_XDRTA2_calls": 1,
        "stub_core_calls": 1,
        "production_XDRTA2_calls": 0,
        "production_core_calls": 0,
        "Dragon_executions": 0,
        "sequential_tracking_record_reads": 0,
        "transport_solves": 0,
        "original_artifact_mutations": 0,
        "C2M_host_executions": 0,
    }
    for key, value in expected_counts.items():
        require(evidence[key] == value, f"manifest evidence {key}")
    for key, value in data["scope"].items():
        require(value is False, f"manifest scope {key}")
    status = data["status"]
    require(status["production_execution_authorized"] is False,
            "production execution authorization")
    require(status["online_REAL64_Picard_iteration_validated"] is False,
            "Picard iteration claim")
    require(status["radial_convergence"] == "NOT-EVALUATED",
            "radial convergence claim")
    require(status["outer_picard_convergence"] == "NOT-EVALUATED",
            "outer convergence claim")
    require("explicit REAL64 continuation owner" in data["next_gate"],
            "explicit continuation next gate")

    manifest_artifacts = data["real_read_only_inputs"]
    require(set(manifest_artifacts) == set(ARTIFACTS), "artifact inventory")
    for relative, (expected_hash, expected_size) in ARTIFACTS.items():
        path = ROOT / relative
        require(path.is_file(), f"artifact missing: {relative}")
        require(path.stat().st_size == expected_size, f"artifact size: {relative}")
        require(digest(path) == expected_hash, f"artifact hash: {relative}")
        require(manifest_artifacts[relative]["sha256"] == expected_hash,
                f"manifest artifact hash: {relative}")
        require(manifest_artifacts[relative]["bytes"] == expected_size,
                f"manifest artifact size: {relative}")


def check_readme_text(text: str) -> None:
    for token in (
        "real64_phase_a9b_b2f_fresh_host/run_phase_a9b_b2f_fresh_host.sh",
        "first fresh-output REAL64 bootstrap contract only",
        "REAL64-to-REAL32-to-REAL64 Picard continuation",
        "Radial and outer Picard convergence remain",
        "`NOT-EVALUATED`",
    ):
        require(token in text, f"project README token missing: {token}")


def main() -> None:
    for path in (B2B, B2C, FLU, FLUGPI, PLANE, REFERENCE, HARNESS, STUBS,
                 RUNNER, MANIFEST, PROJECT_README):
        require(path.is_file(), f"missing file: {path.relative_to(ROOT)}")
    check_default_off()
    check_plane_text(PLANE.read_text())
    check_reference_text(REFERENCE.read_text())
    check_b2b_text(B2B.read_text())
    check_b2c_text(B2C.read_text())
    check_flu_text(FLU.read_text(), FLUGPI.read_text())
    check_global_publisher_callsites()
    check_harness_text(HARNESS.read_text())
    check_stub_text(STUBS.read_text())
    check_runner_text(RUNNER.read_text())
    check_manifest_data(json.loads(MANIFEST.read_text()))
    check_readme_text(PROJECT_README.read_text())
    print("SPOR64 PHASE-A9b-B2f CHECK PASS")


if __name__ == "__main__":
    main()
