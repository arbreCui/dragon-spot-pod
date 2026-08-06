#!/usr/bin/env python3
"""Fail-closed static gate for the isolated B2i archive bootstrap seal."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Mapping


ROOT = Path(__file__).resolve().parents[3]
B2I_SOURCE = ROOT / "src/SPOR64_B2I.f90"
HERE = Path(__file__).resolve().parent


class GateError(RuntimeError):
    """Raised when the narrow B2i lifecycle contract is not satisfied."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def fortran_code(text: str) -> str:
    return "\n".join(line.split("!", 1)[0] for line in text.splitlines())


def compact_free(text: str) -> str:
    return re.sub(r"\s+", "", fortran_code(text)).replace("&", "").upper()


def routine_region(text: str, name: str) -> str:
    pattern = re.compile(
        rf"(?is)\bsubroutine\s+{re.escape(name)}\s*\(.*?"
        rf"\bend\s+subroutine\s+{re.escape(name)}\b"
    )
    match = pattern.search(fortran_code(text))
    require(match is not None, f"missing subroutine {name}")
    return match.group(0)


def ordered(packed: str, fragments: tuple[str, ...], owner: str) -> None:
    position = -1
    for fragment in fragments:
        next_position = packed.find(fragment, position + 1)
        require(next_position >= 0, f"{owner}: missing {fragment}")
        require(next_position > position, f"{owner}: order changed at {fragment}")
        position = next_position


def check_api_and_isolation(text: str, production: Mapping[Path, str]) -> None:
    packed = compact_free(text)
    routine = compact_free(routine_region(text, "SPOR64_B2I_SEAL_BOOTSTRAP"))
    require(
        "SUBROUTINESPOR64_B2I_SEAL_BOOTSTRAP("
        "IPAXOUT,IPARCHIVEOUT,IPAX,IPAXTRACK,IPARCHIVE,STATUS)" in routine,
        "bootstrap seal must accept only the two fresh outputs and three roots",
    )
    for symbol in (
        "SPOR64_B2I_ADMISSION_FAILED=1",
        "SPOR64_B2I_BOOTSTRAP_COMMITTED=2",
        "BOOTSTRAP_EPOCH=0",
        "NGRP=370",
        "NREG=8",
        "NSNAP=3",
        "NUNKNO=14",
    ):
        require(symbol in packed, f"frozen B2i constant: {symbol}")
    require("STATUS=SPOR64_B2I_ADMISSION_FAILED" in routine,
            "fail-closed status must be first")
    require("STATUS=SPOR64_B2I_BOOTSTRAP_COMMITTED" in routine,
            "one explicit committed status")
    for forbidden_argument in ("ALPHA", "OMEGA", "TOLERANCE", "CUTOFF"):
        header = routine.split(")", 1)[0]
        require(forbidden_argument not in header,
                f"loose empirical/control argument forbidden: {forbidden_argument}")

    for path, source in production.items():
        if path.resolve() == B2I_SOURCE.resolve():
            continue
        code = fortran_code(source)
        require(
            re.search(r"(?i)\bSPOR64_B2I(?:_[A-Z0-9_]*)?\b", code) is None,
            f"B2i must remain host-disconnected: {path.relative_to(ROOT)}",
        )


def check_canonical_bundle(text: str) -> None:
    packed = compact_free(routine_region(text, "SPOR64_B2I_SEAL_BOOTSTRAP"))
    for record, length, type_code in (
        ("SPOT-X-DIMS", "4", "1"),
        ("SPOT-X-RANK", "NGRP", "1"),
        ("SPOT-X-OFF", "NGRP+1", "1"),
        ("SPOT-X-GOFF", "NGRP+1", "1"),
        ("SPOT-X-BOFF", "NGRP+1", "1"),
        ("SPOT-X-BASIS", "TOTAL_BASIS", "2"),
        ("SPOT-X-A", "NCOEF", "4"),
        ("SPOT-X-GRAM", "TOTAL_GRAM", "4"),
        ("SPOT-X-RHO", "1", "4"),
        ("SPOT-X-L", "NGRP*NSNAP", "4"),
        ("SPOT-X-H", "NSNAP", "4"),
        ("SPOT-X-NORM", "1", "4"),
        ("SPOT-X-PERP", "NGRP*NSNAP", "4"),
        ("SPOT-X-GERR", "1", "4"),
    ):
        fragment = f"RECORD_MATCHES(IPAX,'{record}',{length},{type_code})"
        require(fragment in packed, f"canonical record schema: {record}")
    for marker in (
        "CHARACTER_RECORD_MATCHES(IPAX,'SPOT-X-NID',3,12,'NUFISS-UNIT')",
        "CHARACTER_RECORD_MATCHES(IPAX,'SPOT-X-BTYP',3,12,'POD-FIXED')",
        "IF(FIXB/=1)RETURN",
        "IF(.NOT.ABSENT_RECORD(IPAX,'SPOT-X-STATE'))RETURN",
        "IF(.NOT.ABSENT_RECORD(IPAX,'SPOT-X-EPOCH'))RETURN",
    ):
        require(marker in packed, f"canonical provenance marker: {marker}")

    require(
        "EXPECTED64=TRANSFER(1.0_REAL64/REAL(KEFF32,REAL64),0_INT64)"
        in packed,
        "RHO must be the bit-exact inverse of the stored axial eigenvalue",
    )
    require("IF(FOUND64/=EXPECTED64)RETURN" in packed,
            "bitwise RHO identity rejection")
    for geometry in (
        "IF(AXIAL_STATE(2)/=AXIAL_TRACK_STATE(2))RETURN",
        "IF(AXIAL_TRACK_STATE(1)/=NREG*AXIAL_TRACK_STATE(7))RETURN",
        "IF(AXIAL_TRACK_STATE(12)/=NREG*(AXIAL_TRACK_STATE(7)+1))RETURN",
        "IF(AXIAL_TRACK_STATE(11)+AXIAL_TRACK_STATE(12)>"
        "AXIAL_TRACK_STATE(2))RETURN",
        "HEIGHT_CHECK64(MAT1D(IR))=HEIGHT_CHECK64(MAT1D(IR))+"
        "REAL(DZ32(IR),REAL64)",
        "TRANSFER(HEIGHT_CHECK64(IP),0_INT64)/="
        "TRANSFER(HEIGHT64(IP),0_INT64)",
    ):
        require(geometry in packed, f"axial geometry identity: {geometry}")

    gram_order = (
        "GRAM_ERROR_CHECK64=+0.0_REAL64",
        "DOIG=1,NGRP",
        "NMODE=RANK(IG)",
        "DOA=1,NMODE",
        "DOB=1,NMODE",
        "GRAM_VALUE=+0.0_REAL64",
        "DOIR=1,NREG",
        "INDEX_A=BASIS_OFFSET(IG)+(A-1)*NREG+IR",
        "INDEX_B=BASIS_OFFSET(IG)+(B-1)*NREG+IR",
        "GRAM_VALUE=GRAM_VALUE+REAL(AREA32(IR),REAL64)/WEIGHT_SUM*"
        "REAL(BASIS32(INDEX_A),REAL64)*REAL(BASIS32(INDEX_B),REAL64)",
        "INDEX_G=GRAM_OFFSET(IG)+(B-1)*NMODE+A",
        "TRANSFER(GRAM_VALUE,0_INT64)/="
        "TRANSFER(GRAM64(INDEX_G),0_INT64)",
        "TRANSFER(GRAM_ERROR_CHECK64,0_INT64)/="
        "TRANSFER(GRAM_ERROR64,0_INT64)",
    )
    ordered(packed, gram_order, "frozen SPOSTATE Gram replay")
    require("ANY(OFFSPACE64<+0.0_REAL64)" in packed,
            "SPOT-X-PERP integrity is sign/finite only")
    require("GRAM_ERROR64<+0.0_REAL64" in packed,
            "SPOT-X-GERR integrity is sign/finite only")


def check_archive_admission(text: str) -> None:
    packed = compact_free(routine_region(text, "SPOR64_B2I_SEAL_BOOTSTRAP"))
    module_packed = compact_free(text)
    for root_check in (
        "CHARACTER_RECORD_MATCHES(IPARCHIVE,'SIGNATURE',3,12,'L_ARCHIVE')",
        "RECORD_MATCHES(IPARCHIVE,'LISTDIM',1,1)",
        "IF(ARCHIVE_PLANES/=NSNAP)RETURN",
        "IF(.NOT.ABSENT_RECORD(IPARCHIVE,'SPOT-R64'))RETURN",
        "RECORD_MATCHES(IPARCHIVE,'SPOT-ITER-K',1,4)",
        "TRANSFER(ITER_KEFF64,0_INT64)/="
        "TRANSFER(REAL(KEFF32,REAL64),0_INT64)",
    ):
        require(root_check in packed, f"archive root admission: {root_check}")
    list_variables = {
        "TRACK": "TRACKS",
        "MICROLIB2": "LIBRARIES",
        "SYSTEM": "SYSTEMS",
        "FLUX": "FLUXES",
    }
    for list_name in ("TRACK", "MICROLIB2", "SYSTEM", "FLUX"):
        require(
            f"RECORD_MATCHES(IPARCHIVE,'{list_name}',NSNAP,10)" in packed,
            f"complete same-index archive list: {list_name}",
        )
        require(
            f"LIST_ITEM_IS_DIRECTORY({list_variables[list_name]},IP)"
            in packed,
            f"all {list_name} items are directories",
        )

    for structure in (
        "CHARACTER_RECORD_MATCHES(INPUT_LIBRARY(IP),'SIGNATURE',3,12,'L_LIBRARY')",
        "RECORD_MATCHES(INPUT_LIBRARY(IP),'MACROLIB',-1,0)",
        "CHARACTER_RECORD_MATCHES(LIBRARY_MACRO,'SIGNATURE',3,12,'L_MACROLIB')",
        "RECORD_MATCHES(LIBRARY_MACRO,'GROUP',NGRP,10)",
        "LIST_ITEM_IS_DIRECTORY(MACRO_GROUPS,IG)",
        "CHARACTER_RECORD_MATCHES(INPUT_SYSTEM(IP),'SIGNATURE',3,12,'L_PIJ')",
        "RECORD_MATCHES(INPUT_SYSTEM(IP),'GROUP',NGRP,10)",
        "LIST_ITEM_IS_DIRECTORY(SYSTEM_GROUPS,IG)",
        "CHARACTER_RECORD_MATCHES(INPUT_SYSTEM(IP),'LINK.MACRO',3,12,'MACRO0')",
        "CHARACTER_RECORD_MATCHES(INPUT_SYSTEM(IP),'LINK.TRACK',3,12,'TRACK')",
        "RECORD_MATCHES(INPUT_SYSTEM(IP),'SPOT-LEAK1D',NGRP,2)",
        "RECORD_MATCHES(INPUT_SYSTEM(IP),'SPOT-L1-SNAP',1,1)",
        "IF(SYSTEM_SNAPSHOT/=IP)RETURN",
        "CHARACTER_RECORD_MATCHES(INPUT_TRACK(IP),'TRACK-TYPE',3,12,'MCCG')",
        "CHARACTER_RECORD_MATCHES(INPUT_TRACK(IP),'LINK.FTRACK',3,12,'TRACK_F')",
        "CHARACTER_RECORD_MATCHES(INPUT_FLUX(IP),'OPTION',1,4,'B0')",
        "CHARACTER_RECORD_MATCHES(INPUT_FLUX(IP),'LINK.MACRO',3,12,'MACRO0')",
        "CHARACTER_RECORD_MATCHES(INPUT_FLUX(IP),'LINK.TRACK',3,12,'TRACK')",
        "CHARACTER_RECORD_MATCHES(INPUT_FLUX(IP),'LINK.SYSTEM',3,12,'SYSTEM')",
    ):
        require(structure in packed, f"plane tuple structure: {structure}")
    require(
        "ANY(SYSTEM_STATE(1:14)/=[1,1,1,0,1,1,4,NGRP,NUNKNO,NMAT,1,0,0,0])"
        in packed,
        "frozen radial SYSTEM state vector",
    )
    require("ANY(SYSTEM_STATE(15:NSTATE)/=0)" in packed,
            "unused radial SYSTEM state slots are zero")

    for identity in (
        "TRANSFER(VOLUME32(IR),0_INT32)/=TRANSFER(AREA32(IR),0_INT32)",
        "IF(PLANE_KEY(IR)/=ANIS_KEY(IR))RETURN",
        "IF(ANY(SEED_KEY/=ANIS_KEY))RETURN",
        "FOUND64=TRANSFER(LEAKAGE64((IP-1)*NGRP+IG),0_INT64)",
        "EXPECTED64=TRANSFER(REAL(PLANE_LEAK32(IG),REAL64),0_INT64)",
    ):
        require(identity in packed, f"cross-root bit identity: {identity}")

    require("AUTHORITY_HAS_EXACT_PAYLOAD(PLANE_AUTHORITY(IP))" in packed,
            "authority inventory must be exactly FLUX and SOUR")
    for inventory in (
        "CASE('FLUX')",
        "CASE('SOUR')",
        "IF(ITEM_COUNT>2)RETURN",
        "AUTHORITY_HAS_EXACT_PAYLOAD=ITEM_COUNT==2.AND."
        "SAW_FLUX.AND.SAW_SOURCE",
    ):
        require(inventory in module_packed,
                f"exact authority inventory implementation: {inventory}")
    for absent in ("RHO", "STATE", "EPOCH", "QFISS"):
        require(
            f"ABSENT_RECORD(PLANE_AUTHORITY(IP),'{absent}')" in packed,
            f"unsealed plane authority excludes {absent}",
        )
    require(packed.count("ITYLCM/=4") == 2,
            "both authority list elements are REAL64")
    require(packed.count("ITYLCM/=2") == 2,
            "both compatibility list elements are REAL32")
    require("ANY(ABS(AUTHORITY_FLUX64)>REAL32_MAX64)" in packed,
            "FLUX downcast is representable before conversion")
    require("ANY(ABS(AUTHORITY_SOURCE64)>REAL32_MAX64)" in packed,
            "SOUR downcast is representable before conversion")
    for mirror in (
        "EXPECTED32=TRANSFER(REAL(AUTHORITY_FLUX64(IU),REAL32),0_INT32)",
        "EXPECTED32=TRANSFER(REAL(AUTHORITY_SOURCE64(IU),REAL32),0_INT32)",
    ):
        require(mirror in packed, f"compatibility mirror downcast: {mirror}")


def check_publication_boundary(text: str) -> None:
    raw = routine_region(text, "SPOR64_B2I_SEAL_BOOTSTRAP")
    packed = compact_free(raw)
    for output in ("IPAXOUT", "IPARCHIVEOUT"):
        freshness = f"IF(.NOT.EMPTY_LCM_ROOT({output}))RETURN"
        require(packed.count(freshness) == 2,
                f"{output} freshness checked at entry and pre-commit")

    first_write = "CALLLCMEQU(IPAX,IPAXOUT)"
    require(packed.count(first_write) == 1, "single first AX fresh copy")
    before = packed[:packed.index(first_write)]
    write_patterns = (
        "CALLLCMEQU(", "CALLLCMPUT(", "CALLLCMPTC(", "CALLLCMPDL(",
        "=LCMDID(", "=LCMLID(", "=LCMDIL(", "CALLLCMDEL(",
    )
    for token in write_patterns:
        require(token not in before, f"no mutation before complete preflight: {token}")
    require("CALLLCMEQU(IPARCHIVE,IPARCHIVEOUT)" not in packed,
            "legacy transition diagnostics must not be cloned at archive root")
    require(packed.count("CALLLCMEQU(") == 5,
            "one AX and four same-index fresh-target copy statements")

    for list_name in ("TRACK", "MICROLIB2", "SYSTEM", "FLUX"):
        require(
            f"LCMLID(IPARCHIVEOUT,'{list_name}',NSNAP)" in packed,
            f"fresh output list creation: {list_name}",
        )
    for input_name, output_name in (
        ("INPUT_TRACK(IP)", "OUTPUT_ITEM"),
        ("INPUT_LIBRARY(IP)", "OUTPUT_ITEM"),
        ("INPUT_SYSTEM(IP)", "OUTPUT_ITEM"),
        ("INPUT_FLUX(IP)", "OUTPUT_ITEM"),
    ):
        require(f"CALLLCMEQU({input_name},{output_name})" in packed,
                f"fresh item copy: {input_name}")

    ordered(
        packed,
        (
            "CALLLCMPUT(OUTPUT_AUTHORITY,'RHO',1,4,RHO64)",
            "CALLLCMPTC(OUTPUT_AUTHORITY,'STATE',12,LIFECYCLE_STATE)",
            "CALLLCMPUT(OUTPUT_AUTHORITY,'EPOCH',1,1,BOOTSTRAP_EPOCH)",
            "CALLLCMPTC(IPAXOUT,'SPOT-X-STATE',12,LIFECYCLE_STATE)",
            "CALLLCMPUT(IPAXOUT,'SPOT-X-EPOCH',1,1,BOOTSTRAP_EPOCH)",
            "OUTPUT_AUTHORITY=LCMDID(IPARCHIVEOUT,'SPOT-R64')",
            "CALLLCMPUT(OUTPUT_AUTHORITY,'RHO',1,4,RHO64)",
            "CALLLCMPUT(OUTPUT_AUTHORITY,'NPLANE',1,1,ARCHIVE_PLANES)",
            "CALLLCMPTC(OUTPUT_AUTHORITY,'STATE',12,LIFECYCLE_STATE)",
            "CALLLCMPUT(OUTPUT_AUTHORITY,'EPOCH',1,1,BOOTSTRAP_EPOCH)",
            "STATUS=SPOR64_B2I_BOOTSTRAP_COMMITTED",
        ),
        "plane/AX/archive commit order",
    )
    mutations = list(
        re.finditer(
            r"CALLLCM(?:EQU|PUT|PTC|PDL|DEL)\(|=LCM(?:DID|LID|DIL)\(", packed
        )
    )
    require(mutations, "publication must contain GANLIB writes")
    last_mutation = mutations[-1].start()
    expected_last = "CALLLCMPUT(OUTPUT_AUTHORITY,'EPOCH',1,1,BOOTSTRAP_EPOCH)"
    require(packed.startswith(expected_last, last_mutation),
            "archive root EPOCH must be the final LCM mutation")
    require("SPOT-L1-ERR" not in packed and "SPOT-PJ-PERP" not in packed and
            "SPOT-PROJECT" not in packed,
            "old transition diagnostics must not enter the new sealed root")


def check_no_empirical_or_solver_path(text: str) -> None:
    code = fortran_code(text)
    identifier_code = re.sub(r"'[^']*'|\"[^\"]*\"", " ", code)
    identifiers = re.findall(r"(?i)\b[A-Z][A-Z0-9_]*\b", identifier_code)
    forbidden_stems = (
        "alpha", "omega", "relax", "damp", "clip", "empir",
        "anderson", "aitken",
    )
    for identifier in identifiers:
        for stem in forbidden_stems:
            require(stem not in identifier.lower(),
                    f"empirical iteration identifier forbidden: {identifier}")
    packed = compact_free(text)
    for solver in (
        "FLUDRV", "FLU2DR", "MCCGF", "MCGMRE", "XDRTA2", "SPOMOC",
        "SPOPROJ", "SPOFSRC", "DOORFV", "DRAGON",
    ):
        require(solver not in packed, f"solver/transport path forbidden: {solver}")
    require(packed.count("'QFISS'") == 1 and
            "ABSENT_RECORD(PLANE_AUTHORITY(IP),'QFISS')" in packed,
            "B2i may only reject an input authority QFISS")


def check_repository_surface(root: Path = ROOT) -> None:
    makefile = (root / "Makefile").read_text()
    readme = (root / "README.md").read_text()
    phase_readme = (HERE / "README.md").read_text()
    runner = (HERE / "run_phase_a9b_b2i_bootstrap_lifecycle.sh").read_text()
    harness = (HERE / "test_b2i_bootstrap_lifecycle.f90").read_text()
    contract_tests = (
        HERE / "test_phase_a9b_b2i_bootstrap_lifecycle_contract.py"
    ).read_text()
    manifest = json.loads((HERE / "precision_manifest.json").read_text())

    make_rule = (
        ".PHONY: spot-real64-phase-a9b-b2i-bootstrap\n"
        "spot-real64-phase-a9b-b2i-bootstrap :\n"
        "\tsh validation/iterative/real64_phase_a9b_b2i_bootstrap_lifecycle/"
        "run_phase_a9b_b2i_bootstrap_lifecycle.sh\n"
    )
    require(make_rule in makefile, "B2i Makefile entrypoint")
    require("make spot-real64-phase-a9b-b2i-bootstrap" in readme,
            "root README B2i command")
    require("real64_phase_a9b_b2i_bootstrap_lifecycle/README.md" in readme,
            "root README B2i details link")
    phase_words = re.sub(r"\s+", " ", phase_readme)
    for claim in (
        "B2h is the sole next-stage semantic gate that evaluates `B*A`",
        "SYSTEM/SPOT-LEAK1D` is required to be finite but is deliberately not equated",
        "RHO` stamped on a `SOLVED` plane is the lifecycle label",
        "not a globally unique identifier",
        "RADIAL-CONVERGENCE=NOT-EVALUATED",
        "OUTER-PICARD-CONVERGENCE=NOT-EVALUATED",
    ):
        require(claim in phase_words, f"phase README boundary: {claim}")

    require(manifest["phase"] == "A9b-B2i", "manifest phase")
    require(manifest["parent_commit"] ==
            "b3a24a7b94c715a81b4f03a8dd12963d3765834a",
            "manifest parent commit")
    require(manifest["identity_checks"]["empirical_tolerance"] is False,
            "manifest has no empirical tolerance")
    require(manifest["output_contract"]["legacy_transition_diagnostics_copied"]
            is False, "manifest new-root history policy")
    require(manifest["semantic_boundary"]["B_times_A_evaluated"] is False,
            "manifest projection boundary")
    require(manifest["semantic_boundary"]["qfiss_built"] is False,
            "manifest source boundary")
    require(manifest["semantic_boundary"]["host_connected"] is False,
            "manifest host isolation")
    require(manifest["validation"]["static_contract_tests"] == 30,
            "manifest static-test inventory")
    test_count = len(re.findall(r"(?m)^\s+def\s+test_[A-Za-z0-9_]+\(",
                                contract_tests))
    require(test_count == 30, "actual static-test inventory")
    require(
        f"STATIC-CONTRACT-TESTS={test_count} "
        f"MUTATION-REGRESSION-CASES={test_count-1}" in runner,
        "runner static/mutation inventory matches test definitions",
    )

    for frozen in (
        "EXPECTED_PARENT_COMMIT=b3a24a7b94c715a81b4f03a8dd12963d3765834a",
        "EXPECTED_PARENT_HASH=2c5d7bb317a419c0ba920ed0ed457b8e8f10f5ebeed07fee144738acf80eb2b9",
        "EXPECTED_AX_HASH=2323a256002f1e6f75f5af72c31479b0f6a7bff561d401cee363dcf9fc6ff484",
        "EXPECTED_ARCHIVE_HASH=1b5a0c98aba0f5b4f366b64a8157f4a104df0f89f4cdeafc60eb6ce7811018e1",
        "EXPECTED_TRACK_HASH=101ba0ad64c91723fdeb002e62c6226347fcfaeff188e125d699d70e113febc7",
        "-ffp-contract=off -fno-fast-math",
        "STATIC-CONTRACT-TESTS=30 MUTATION-REGRESSION-CASES=29",
        "B*A=NOT-EVALUATED QFISS=NOT-BUILT CONT=NOT-EXECUTED",
    ):
        require(frozen in runner, f"runner frozen contract: {frozen}")
    require('ln -s "$ARCHIVE_ARTIFACT" "$CASE_DIR/archive.xsm"' in runner,
            "large real archive is linked read-only, not copied")
    require('copy_exact "$ARCHIVE_ARTIFACT"' not in runner,
            "228 MB archive copy forbidden")
    require("src/SPOR64_B2C.f90" in runner and "src/SPOR64_B2I.f90" in runner,
            "real B2C producer and B2i consumer compiled")
    require("SPOR64_B2C_PUBLISH" in harness,
            "dynamic candidate comes from the real B2C producer")
    require("NREJECTION=12" in compact_free(harness) and
            "'B2ISEAL-CALLS=',SEAL_CALLS" in compact_free(harness),
            "dynamic call inventory")
    harness_packed = compact_free(harness)
    require("IF(B2C_PUBLISH_CALLS/=NSNAP)" in harness_packed and
            "'B2IPRODUCTION-B2C-PUBLISH-CALLS=',B2C_PUBLISH_CALLS"
            in harness_packed, "three real producer calls")


def load_production_files(root: Path = ROOT) -> dict[Path, str]:
    result: dict[Path, str] = {}
    for directory, patterns in (
        (root / "src", ("*.f", "*.f90", "*.F", "*.F90")),
        (root / "data", ("*.c2m", "*.x2m")),
    ):
        for pattern in patterns:
            for path in directory.rglob(pattern):
                result[path] = path.read_text(errors="replace")
    return result


def check_all(
    text: str | None = None,
    production: Mapping[Path, str] | None = None,
) -> None:
    source = B2I_SOURCE.read_text() if text is None else text
    sources = load_production_files() if production is None else production
    check_api_and_isolation(source, sources)
    check_canonical_bundle(source)
    check_archive_admission(source)
    check_publication_boundary(source)
    check_no_empirical_or_solver_path(source)
    check_repository_surface()


def main() -> None:
    check_all()
    print("B2I STATIC CONTRACT PASS")
    print("B2I HOST-CONNECTED=false TRANSPORT-SOLVES=0 EMPIRICAL-CONTROLS=0")


if __name__ == "__main__":
    main()
