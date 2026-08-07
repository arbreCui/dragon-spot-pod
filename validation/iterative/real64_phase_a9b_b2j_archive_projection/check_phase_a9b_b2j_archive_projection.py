#!/usr/bin/env python3
"""Fail-closed static gate for the isolated B2j archive projection."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Mapping


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "src/SPOR64_B2J.f90"
HERE = Path(__file__).resolve().parent


class GateError(RuntimeError):
    """Raised when the narrow B2j contract is not satisfied."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def fortran_code(text: str) -> str:
    return "\n".join(line.split("!", 1)[0] for line in text.splitlines())


def packed(text: str) -> str:
    return re.sub(r"\s+", "", fortran_code(text)).replace("&", "").upper()


def routine(text: str, name: str) -> str:
    match = re.search(
        rf"(?is)\bsubroutine\s+{re.escape(name)}\s*\(.*?"
        rf"\bend\s+subroutine\s+{re.escape(name)}\b",
        fortran_code(text),
    )
    require(match is not None, f"missing subroutine {name}")
    return match.group(0)


def ordered(code: str, fragments: tuple[str, ...], owner: str) -> None:
    position = -1
    for fragment in fragments:
        found = code.find(fragment, position + 1)
        require(found > position, f"{owner}: missing or reordered {fragment}")
        position = found


def check_api(text: str) -> None:
    code = packed(text)
    body = packed(routine(text, "SPOR64_B2J_PROJECT_ARCHIVE"))
    require(
        "SUBROUTINESPOR64_B2J_PROJECT_ARCHIVE("
        "IPARCHIVEOUT,IPAX,IPAXTRACK,IPARCHIVE,STATUS)" in body,
        "B2j API must accept one fresh output and the sealed input roots only",
    )
    for token in (
        "SPOR64_B2J_ADMISSION_FAILED=1",
        "SPOR64_B2J_ARCHIVE_PROJECTED=2",
        "BOOTSTRAP_INPUT_EPOCH=0",
        "BOOTSTRAP_OUTPUT_EPOCH=1",
        "NGRP=370",
        "NREG=8",
        "NSNAP=3",
        "NUNKNO=14",
    ):
        require(token in code, f"frozen constant missing: {token}")
    require("STATUS=SPOR64_B2J_ADMISSION_FAILED" in body,
            "fail-closed status initialization")
    require("STATUS=SPOR64_B2J_ARCHIVE_PROJECTED" in body,
            "single successful status")
    header = body.split(")", 1)[0]
    for forbidden in (
        "RHO", "BASIS", "COORDINATE", "PROJECTED", "EPOCH",
        "ALPHA", "OMEGA", "TOLERANCE", "CUTOFF",
    ):
        require(forbidden not in header, f"loose API argument forbidden: {forbidden}")


def check_input_lifecycle(text: str) -> None:
    body = packed(routine(text, "SPOR64_B2J_PROJECT_ARCHIVE"))
    for token in (
        "CHARACTER_RECORD_MATCHES(IPAX,'SPOT-X-STATE',3,12,'CLOSED')",
        "RECORD_MATCHES(IPAX,'SPOT-X-EPOCH',1,1)",
        "IF(AXIAL_EPOCH/=BOOTSTRAP_INPUT_EPOCH)RETURN",
        "PROJECTED_EPOCH=BOOTSTRAP_OUTPUT_EPOCH",
        "CLOSED_ARCHIVE_ROOT_IS_EXACT(IPARCHIVE)",
        "CLOSED_ROOT_AUTHORITY_IS_EXACT(ROOT_AUTHORITY)",
        "CHARACTER_RECORD_MATCHES(ROOT_AUTHORITY,'STATE',3,12,'CLOSED')",
        "IF(ROOT_PLANES/=NSNAP.OR.ARCHIVE_EPOCH/=AXIAL_EPOCH)RETURN",
        "SOLVED_AUTHORITY_IS_EXACT(PLANE_AUTHORITY)",
        "CHARACTER_RECORD_MATCHES(PLANE_AUTHORITY,'STATE',3,12,'SOLVED')",
        "IF(PLANE_EPOCH/=AXIAL_EPOCH)RETURN",
    ):
        require(token in body, f"lifecycle/provenance check missing: {token}")
    require(
        "TRANSFER(ROOT_RHO64,0_INT64)/=TRANSFER(RHO64,0_INT64)" in body,
        "archive root RHO must match AX bitwise",
    )
    require(
        "TRANSFER(PLANE_RHO64,0_INT64)/=TRANSFER(RHO64,0_INT64)" in body,
        "every plane RHO must match AX bitwise",
    )
    require(
        "EXPECTED64=TRANSFER(1.0_REAL64/REAL(KEFF32,REAL64),0_INT64)"
        in body,
        "AX RHO must be the exact inverse stored by SPOSTATE",
    )
    require(
        "EXPECTED64=TRANSFER(REAL(KEFF32,REAL64),0_INT64)" in body,
        "archive K must exactly promote AX K",
    )


def check_fixed_space_math(text: str) -> None:
    body = packed(routine(text, "SPOR64_B2J_PROJECT_ARCHIVE"))
    for schema in (
        "RECORD_MATCHES(IPAX,'SPOT-X-DIMS',4,1)",
        "RECORD_MATCHES(IPAX,'SPOT-X-RANK',NGRP,1)",
        "RECORD_MATCHES(IPAX,'SPOT-X-OFF',NGRP+1,1)",
        "RECORD_MATCHES(IPAX,'SPOT-X-BOFF',NGRP+1,1)",
        "RECORD_MATCHES(IPAX,'SPOT-X-BASIS',TOTAL_BASIS,2)",
        "RECORD_MATCHES(IPAX,'SPOT-X-A',NCOEF,4)",
        "RECORD_MATCHES(IPAX,'SPOT-X-RHO',1,4)",
        "RECORD_MATCHES(IPAX,'SPOT-X-L',NGRP*NSNAP,4)",
        "CHARACTER_RECORD_MATCHES(IPAX,'SPOT-X-NID',3,12,'NUFISS-UNIT')",
        "CHARACTER_RECORD_MATCHES(IPAX,'SPOT-X-BTYP',3,12,'POD-FIXED')",
    ):
        require(schema in body, f"canonical schema missing: {schema}")
    ordered(
        body,
        (
            "DOIG=1,NGRP",
            "NMODE=RANK(IG)",
            "DOA=1,NMODE",
            "BASIS_OFFSET(IG)+(A-1)*NREG+1:",
            "BASIS_OFFSET(IG)+A*NREG",
            "DOIP=1,NSNAP",
            "OFFSET(IG)+(IP-1)*NMODE+1:OFFSET(IG)+IP*NMODE",
            "CALLSPOR64_B2H_RECONSTRUCT(BASIS_SLICE32(:,1:NMODE),"
            "COORDINATE_SLICE64(1:NMODE),PROJECTED_REGION64(:,IG,IP),"
            "RECONSTRUCTION_OK)",
            "IF(.NOT.RECONSTRUCTION_OK)RETURN",
        ),
        "frozen B_g*a_(g,p) reconstruction",
    )
    require("MATMUL(" not in body, "unfrozen MATMUL contraction forbidden")
    require("SPOR64_B2H_RECONSTRUCT" in body,
            "B2h must remain the sole contraction implementation")


def check_tuple_and_leakage(text: str) -> None:
    body = packed(routine(text, "SPOR64_B2J_PROJECT_ARCHIVE"))
    for list_name in ("TRACK", "MICROLIB2", "SYSTEM", "FLUX"):
        require(
            f"RECORD_MATCHES(IPARCHIVE,'{list_name}',NSNAP,10)" in body,
            f"complete B2i input list required: {list_name}",
        )
    for token in (
        "CHARACTER_RECORD_MATCHES(INPUT_LIBRARY(IP),'SIGNATURE',3,12,'L_LIBRARY')",
        "CHARACTER_RECORD_MATCHES(LIBRARY_MACRO,'SIGNATURE',3,12,'L_MACROLIB')",
        "RECORD_MATCHES(LIBRARY_MACRO,'GROUP',NGRP,10)",
        "CHARACTER_RECORD_MATCHES(INPUT_SYSTEM(IP),'SIGNATURE',3,12,'L_PIJ')",
        "RECORD_MATCHES(INPUT_SYSTEM(IP),'GROUP',NGRP,10)",
        "RECORD_MATCHES(INPUT_SYSTEM(IP),'SPOT-L1-SNAP',1,1)",
        "IF(SYSTEM_SNAPSHOT/=IP)RETURN",
        "IF(PLANE_TRACK_STATE(4)/=NMAT.OR.PLANE_TRACK_STATE(5)/=6)RETURN",
        "IF(PLANE_TRACK_STATE(6)/=1.OR.PLANE_TRACK_STATE(9)/=0)RETURN",
        "IF(PLANE_TRACK_STATE(14)/=4)RETURN",
        "CHARACTER_RECORD_MATCHES(INPUT_TRACK(IP),'TRACK-TYPE',3,12,'MCCG')",
        "CHARACTER_RECORD_MATCHES(INPUT_TRACK(IP),'LINK.FTRACK',3,12,'TRACK_F')",
        "RECORD_MATCHES(INPUT_TRACK(IP),'KEYFLX',NREG,1)",
        "RECORD_MATCHES(INPUT_TRACK(IP),'KEYFLX$ANIS',NREG,1)",
        "IF(PLANE_KEY(IR)/=ANIS_KEY(IR))RETURN",
        "IF(ANY(SEED_KEY/=ANIS_KEY))RETURN",
        "TRANSFER(PLANE_VOLUME32(IR),0_INT32)",
        "TRANSFER(AREA32(IR),0_INT32)",
        "FOUND64=TRANSFER(LEAKAGE64((IP-1)*NGRP+IG),0_INT64)",
        "EXPECTED64=TRANSFER(REAL(PLANE_LEAKAGE32(IG),REAL64),0_INT64)",
    ):
        require(token in body, f"same-index/feedback identity missing: {token}")


def check_staging_and_commit(text: str) -> None:
    body = packed(routine(text, "SPOR64_B2J_PROJECT_ARCHIVE"))
    module_code = packed(text)
    require(body.count("CALLLCMOP(STAGED_FLUX(IP),STAGE_NAME(IP),0,1,0)") == 1,
            "one three-plane staging loop")
    require(body.count("CALLSPOR64_B2H_PROJECT(") == 1,
            "one production B2h call site")
    require(
        "STAGED_PROJECTED_OBJECT_IS_COMMITTED(STAGED_FLUX(IP),RHO64,"
        "PROJECTED_EPOCH,LEAKAGE64((IP-1)*NGRP+1:IP*NGRP))" in body,
        "staged lifecycle and canonical leakage check",
    )
    for token in (
        "IF(.NOT.PROJECTED_PLANE_ROOT_IS_EXACT(IPLIST))RETURN",
        "PROJECTED_AUTHORITY_IS_EXACT(AUTHORITY)",
        "RECORD_MATCHES(AUTHORITY,'FLUX',NGRP,10)",
        "RECORD_MATCHES(IPLIST,'FLUX',NGRP,10)",
        "IF(ILONG/=NUNKNO.OR.ITYLCM/=4)RETURN",
        "IF(ILONG/=NUNKNO.OR.ITYLCM/=2)RETURN",
        "EXPECTED32=TRANSFER(REAL(AUTHORITY_FLUX64(IU),REAL32),0_INT32)",
    ):
        require(token in module_code, f"independent staged check missing: {token}")
    first_output_write = "CALLLCMPTC(IPARCHIVEOUT,'SIGNATURE',12,SIGNATURE)"
    require(first_output_write in body, "first output mutation")
    before = body[:body.index(first_output_write)]
    for mutation in (
        "CALLLCMPUT(IPARCHIVEOUT", "CALLLCMPTC(IPARCHIVEOUT",
        "LCMLID(IPARCHIVEOUT", "LCMDID(IPARCHIVEOUT",
    ):
        require(mutation not in before, f"caller output mutated before staging: {mutation}")
    require(body.count("IF(.NOT.EMPTY_LCM_ROOT(IPARCHIVEOUT))") == 2,
            "output freshness checked at entry and immediately before commit")

    require("LCMLID(IPARCHIVEOUT,'TRACK',NSNAP)" in body,
            "fresh TRACK output")
    require("LCMLID(IPARCHIVEOUT,'MICROLIB2',NSNAP)" in body,
            "fresh MICROLIB2 output")
    require("LCMLID(IPARCHIVEOUT,'FLUX',NSNAP)" in body,
            "fresh FLUX output")
    require("LCMLID(IPARCHIVEOUT,'SYSTEM'" not in body,
            "lagged SYSTEM must be absent from PROJECTED archive")
    require("LCMEQU(INPUT_SYSTEM(IP),OUTPUT_ITEM)" not in body,
            "lagged SYSTEM must never be copied")
    require("CALLLCMEQU(INPUT_TRACK(IP),OUTPUT_ITEM)" in body,
            "TRACK deep copy")
    require("CALLLCMEQU(INPUT_LIBRARY(IP),OUTPUT_ITEM)" in body,
            "MICROLIB2 deep copy")
    require("CALLLCMEQU(STAGED_FLUX(IP),OUTPUT_ITEM)" in body,
            "fresh B2h plane replacement")
    ordered(
        body,
        (
            "CALLLCMEQU(STAGED_FLUX(IP),OUTPUT_ITEM)",
            "CALLCLOSE_STAGES(STAGED_FLUX)",
            "OUTPUT_AUTHORITY=LCMDID(IPARCHIVEOUT,'SPOT-R64')",
            "CALLLCMPUT(OUTPUT_AUTHORITY,'RHO',1,4,RHO64)",
            "CALLLCMPUT(OUTPUT_AUTHORITY,'NPLANE',1,1,ARCHIVE_PLANES)",
            "CALLLCMPTC(OUTPUT_AUTHORITY,'STATE',12,LIFECYCLE_STATE)",
            "CALLLCMPUT(OUTPUT_AUTHORITY,'EPOCH',1,1,PROJECTED_EPOCH)",
            "STATUS=SPOR64_B2J_ARCHIVE_PROJECTED",
        ),
        "stage release and archive commit order",
    )
    mutations = list(re.finditer(
        r"CALLLCM(?:EQU|PUT|PTC|PDL|DEL)\(|=LCM(?:DID|LID|DIL)\(", body
    ))
    require(mutations, "output publication has LCM mutations")
    last = mutations[-1].start()
    require(body.startswith(
        "CALLLCMPUT(OUTPUT_AUTHORITY,'EPOCH',1,1,PROJECTED_EPOCH)", last
    ), "archive root EPOCH must be the final LCM mutation")


def check_forbidden_paths(text: str) -> None:
    code = fortran_code(text)
    identifiers = re.findall(
        r"(?i)\b[A-Z][A-Z0-9_]*\b",
        re.sub(r"'[^']*'|\"[^\"]*\"", " ", code),
    )
    for identifier in identifiers:
        for stem in (
            "alpha", "omega", "relax", "damp", "clip", "empir",
            "anderson", "aitken",
        ):
            require(stem not in identifier.lower(),
                    f"empirical control forbidden: {identifier}")
    identifier_set = {identifier.upper() for identifier in identifiers}
    for forbidden in (
        "SPOPROJ", "SPOFSRC", "FLUDRV", "FLU2DR", "MCCGF", "MCGMRE",
        "SPOMOC", "DOORFV", "XDRTA2", "DRAGON", "CONT", "MATMUL",
    ):
        require(forbidden not in identifier_set,
                f"solver/source/legacy path forbidden: {forbidden}")
    require("QFISS" not in packed(text), "QFISS record/call forbidden")


def load_production(root: Path = ROOT) -> dict[Path, str]:
    result: dict[Path, str] = {}
    for directory, globs in (
        (root / "src", ("*.f", "*.f90", "*.F", "*.F90")),
        (root / "data", ("*.c2m", "*.x2m")),
    ):
        for glob in globs:
            for path in directory.rglob(glob):
                result[path] = path.read_text(errors="replace")
    return result


def check_isolation(production: Mapping[Path, str]) -> None:
    for path, text in production.items():
        if path.resolve() == SOURCE.resolve():
            continue
        require(
            re.search(r"(?i)\bSPOR64_B2J(?:_[A-Z0-9_]*)?\b", fortran_code(text))
            is None,
            f"B2j must remain host-disconnected: {path.relative_to(ROOT)}",
        )


def check_source(text: str) -> None:
    check_api(text)
    check_input_lifecycle(text)
    check_fixed_space_math(text)
    check_tuple_and_leakage(text)
    check_staging_and_commit(text)
    check_forbidden_paths(text)


def check_repository() -> None:
    makefile = (ROOT / "Makefile").read_text()
    readme = (ROOT / "README.md").read_text()
    phase_readme = (HERE / "README.md").read_text()
    runner = (HERE / "run_phase_a9b_b2j_archive_projection.sh").read_text()
    manifest = json.loads((HERE / "precision_manifest.json").read_text())
    tests = (HERE / "test_phase_a9b_b2j_archive_projection_contract.py").read_text()
    support = (HERE / "b2j_fixture_support.f90").read_text()
    harness = (HERE / "test_b2j_archive_projection.f90").read_text()

    rule = (
        ".PHONY: spot-real64-phase-a9b-b2j-projection\n"
        "spot-real64-phase-a9b-b2j-projection :\n"
        "\tsh validation/iterative/real64_phase_a9b_b2j_archive_projection/"
        "run_phase_a9b_b2j_archive_projection.sh\n"
    )
    require(rule in makefile, "B2j Makefile entrypoint")
    require("make spot-real64-phase-a9b-b2j-projection" in readme,
            "root README command")
    require("real64_phase_a9b_b2j_archive_projection/README.md" in readme,
            "root README phase link")
    for claim in (
        "SYSTEM is deliberately absent",
        "B2i-to-B2j direct in-memory lifecycle",
        "RADIAL-CONVERGENCE=NOT-EVALUATED",
        "OUTER-PICARD-CONVERGENCE=NOT-EVALUATED",
    ):
        require(claim in phase_readme, f"phase boundary missing: {claim}")

    require(manifest["phase"] == "A9b-B2j", "manifest phase")
    require(manifest["input_epoch"] == 0 and manifest["output_epoch"] == 1,
            "manifest bootstrap epoch")
    require(manifest["output_contract"]["system_present"] is False,
            "manifest stale-SYSTEM exclusion")
    require(manifest["semantic_boundary"]["qfiss_built"] is False,
            "manifest QFISS boundary")
    require(manifest["semantic_boundary"]["cont_executed"] is False,
            "manifest CONT boundary")
    test_count = len(re.findall(
        r"(?m)^\s+def\s+test_[A-Za-z0-9_]+\(", tests
    ))
    require(test_count == manifest["validation"]["static_contract_tests"],
            "manifest static-test inventory")
    require(
        f"STATIC-CONTRACT-TESTS={test_count} "
        f"MUTATION-REGRESSION-CASES={test_count-1}" in runner,
        "runner mutation inventory",
    )
    for token in (
        "EXPECTED_PARENT_COMMIT=891e67c2cc84aa69e87a9047cf1b230b10c9a48e",
        "EXPECTED_PARENT_HASH=a985deea1344733a8f004cfa1124e8724d188e4ec3d67d11e579305eee6b541f",
        "EXPECTED_AX_HASH=2323a256002f1e6f75f5af72c31479b0f6a7bff561d401cee363dcf9fc6ff484",
        "EXPECTED_ARCHIVE_HASH=1b5a0c98aba0f5b4f366b64a8157f4a104df0f89f4cdeafc60eb6ce7811018e1",
        "EXPECTED_TRACK_HASH=101ba0ad64c91723fdeb002e62c6226347fcfaeff188e125d699d70e113febc7",
        "-ffp-contract=off -fno-fast-math",
        "DRAGON-EXECUTIONS=0 TRANSPORT-SOLVES=0",
        "QFISS=NOT-BUILT CONT=NOT-EXECUTED",
        "SYSTEM=ABSENT-PENDING-ASM",
    ):
        require(token in runner, f"runner frozen claim: {token}")
    require('ln -s "$ARCHIVE_ARTIFACT" "$CASE_DIR/archive.xsm"' in runner,
            "large XSM must remain read-only and linked")
    require('copy_exact "$ARCHIVE_ARTIFACT"' not in runner,
            "228 MB archive copy forbidden")
    for source_name in ("SPOR64_B2C", "SPOR64_B2I", "SPOR64_B2H", "SPOR64_B2J"):
        require(f"src/{source_name}.f90" in runner,
                f"runner compiles production {source_name}")
    require("SPOR64_B2C_PUBLISH" in support,
            "fixture must use production B2C")
    require("SPOR64_B2I_SEAL_BOOTSTRAP" in support,
            "fixture must use production B2i")
    require("SPOR64_B2J_PROJECT_ARCHIVE" in harness,
            "harness must call production B2j")
    harness_code = packed(harness)
    for token in (
        "NREJECTION=12",
        "IF(REGION_BIT_CHECKS/=B2J_NREG*B2J_NGRP*B2J_NSNAP)",
        "IF(NONREGION_BIT_CHECKS/=(B2J_NUNKNO-B2J_NREG)*B2J_NGRP*B2J_NSNAP)",
        "IF(MIRROR_BIT_CHECKS/=B2J_NUNKNO*B2J_NGRP*B2J_NSNAP)",
        "B2J_REQUIRE_ABSENT(OUTPUT,'SYSTEM')",
        "B2J_REQUIRE_ABSENT(OUTPUT,'SOUR')",
        "B2J_REQUIRE_ABSENT(AUTHORITY,'QFISS')",
    ):
        require(token in harness_code, f"dynamic gate contract missing: {token}")


def check_all() -> None:
    check_source(SOURCE.read_text())
    production = load_production()
    check_isolation(production)
    check_repository()


def main() -> None:
    check_all()
    print("B2J STATIC CONTRACT PASS")
    print("B2J SYSTEM-OUTPUT=false HOST-CONNECTED=false EMPIRICAL-CONTROLS=0")


if __name__ == "__main__":
    main()
