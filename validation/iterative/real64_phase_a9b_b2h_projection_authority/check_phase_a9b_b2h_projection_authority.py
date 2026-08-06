#!/usr/bin/env python3
"""Fail-closed static gate for the isolated B2h projection authority.

This gate intentionally proves only a source-level boundary.  B2h may build a
fresh PROJECTED type-4 flux authority, but no production host is allowed to
call it yet, and the legacy SPOPROJ stale-authority hazard must remain visible.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Mapping


ROOT = Path(__file__).resolve().parents[3]
B2H_SOURCE = ROOT / "src/SPOR64_B2H.f90"
SPOPROJ_SOURCE = ROOT / "src/SPOPROJ.f90"


class GateError(RuntimeError):
    """Raised when the narrow B2h projection contract is not satisfied."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def fortran_code(text: str) -> str:
    """Remove free-form comments while retaining declarations and ordering."""

    return "\n".join(line.split("!", 1)[0] for line in text.splitlines())


def compact_free(text: str) -> str:
    """Return comment-free, case-folded free-form Fortran without whitespace."""

    return re.sub(r"\s+", "", fortran_code(text)).replace("&", "").upper()


def routine_region(text: str, name: str) -> str:
    pattern = re.compile(
        rf"(?is)\b(?:pure\s+)?subroutine\s+{re.escape(name)}\s*\(.*?"
        rf"\bend\s+subroutine\s+{re.escape(name)}\b"
    )
    match = pattern.search(fortran_code(text))
    require(match is not None, f"missing subroutine {name}")
    return match.group(0)


def check_reconstruct(text: str) -> None:
    """Freeze the REAL64 fixed-space contraction and its exact loop order."""

    raw = routine_region(text, "SPOR64_B2H_RECONSTRUCT")
    packed = compact_free(raw)
    require(
        re.search(
            r"(?i)\bpure\s+subroutine\s+SPOR64_B2H_RECONSTRUCT\b", raw
        )
        is not None,
        "RECONSTRUCT must remain pure",
    )
    for declaration in (
        "REAL(REAL32),INTENT(IN)::BASIS32(:,:)",
        "REAL(REAL64),INTENT(IN)::COORDINATES64(:)",
        "REAL(REAL64),INTENT(OUT)::PROJECTED64(:)",
    ):
        require(declaration in packed, f"REAL64 contraction declaration: {declaration}")

    contraction = (
        "PROJECTED64=+0.0_REAL64"
        "IF(SIZE(BASIS32,1)/=SIZE(PROJECTED64))RETURN"
        "IF(SIZE(BASIS32,2)/=SIZE(COORDINATES64))RETURN"
    )
    require(contraction in packed, "zero-before-shape-guard contraction prelude")
    ordered = (
        "DOI=1,SIZE(PROJECTED64)"
        "DOA=1,SIZE(COORDINATES64)"
        "PROJECTED64(I)=PROJECTED64(I)+"
        "REAL(BASIS32(I,A),REAL64)*COORDINATES64(A)"
        "ENDDOENDDO"
    )
    require(ordered in packed, "frozen i-outer/a-inner REAL64 contraction order")
    require(packed.count("REAL(BASIS32(I,A),REAL64)") == 1,
            "one exact stored-basis promotion at arithmetic use")
    require("REAL(COORDINATES64" not in packed,
            "coordinates must not be converted")
    require("REAL(PROJECTED64" not in packed,
            "accumulator must not be converted")
    for forbidden in (
        "MATMUL(", "DOT_PRODUCT(", "SUM(", "DDOT(", "DGEMM(",
        "BLAS", "OMP", "DO CONCURRENT", "COARRAY",
    ):
        require(forbidden.replace(" ", "") not in packed,
                f"unordered/reassociated contraction forbidden: {forbidden}")


def check_project(text: str) -> None:
    """Freeze SOLVED-to-PROJECTED ownership and publication ordering."""

    raw = routine_region(text, "SPOR64_B2H_PROJECT")
    packed = compact_free(raw)
    module_packed = compact_free(text)

    # `found` is deferred-length allocatable.  Intrinsic assignment through
    # `found = ' '` would silently reallocate it to length one before LCMGTC,
    # making every real 4/12-character record fail admission.  Section syntax
    # is therefore part of the executable schema contract, not mere style.
    character_reader = (
        "ALLOCATE(CHARACTER(LEN=CHARACTER_COUNT)::FOUND)"
        "FOUND(:)=''"
        "CALLLCMGTC(IPLIST,NAME,CHARACTER_COUNT,FOUND)"
    )
    require(character_reader in module_packed,
            "character-record buffer length preserved before LCMGTC")
    require("FOUND=''" not in module_packed,
            "deferred-length character buffer must not auto-reallocate")

    for declaration in (
        "REAL(REAL64),INTENT(IN)::PROJECTED_REGION64(:,:)",
        "REAL(REAL64),INTENT(IN)::RHO64",
    ):
        require(declaration in packed, f"project input kind: {declaration}")
    require(
        "INTEGER(INT32),PARAMETER::FROZEN_TOL_BITS="
        "INT(Z'348637BD',INT32)" in compact_free(text),
        "exact frozen binary32 tolerance bits",
    )

    require("STATUS=SPOR64_B2H_ADMISSION_FAILED" in packed,
            "fail-closed initial status")
    require("IF(.NOT.EMPTY_LCM_ROOT(IPOUT))RETURN" in packed,
            "fresh output admission")
    require(packed.count("IF(.NOT.EMPTY_LCM_ROOT(IPOUT))RETURN") == 2,
            "fresh output checked at admission and immediately before write")
    for fragment in (
        "IF(STATE_VECTOR(1)/=NGRP.OR.STATE_VECTOR(2)/=NUNKNO)RETURN",
        "IF(STATE_VECTOR(3)/=1)RETURN",
        "IF(ANY(STATE_VECTOR(4:7)/=0))RETURN",
        "IF(STATE_VECTOR(8)/=3.OR.STATE_VECTOR(9)/=3)RETURN",
        "IF(STATE_VECTOR(10)/=1.OR.STATE_VECTOR(17)/=NMAT)RETURN",
        "IF(STATE_VECTOR(11)/=740.OR.STATE_VECTOR(12)/=500)RETURN",
        "IF(STATE_VECTOR(18)/=1)RETURN",
        "IF(ANY(STATE_VECTOR(13:16)/=0))RETURN",
        "IF(ANY(STATE_VECTOR(19:NSTATE)/=0))RETURN",
    ):
        require(fragment in packed, f"exact seed STATE-VECTOR: {fragment}")
    require("RECORD_MATCHES(IPSEED,'EPS-CONVERGE',5,2)" in packed,
            "seed EPS-CONVERGE schema")
    require("CALLLCMGET(IPSEED,'EPS-CONVERGE',EPS_CONVERGE)" in packed,
            "seed EPS-CONVERGE read")
    for index in (1, 2, 3):
        require(
            f"TRANSFER(EPS_CONVERGE({index}),0_INT32)/=FROZEN_TOL_BITS"
            in packed,
            f"seed EPS-CONVERGE({index}) exact bits",
        )
    require("IF(ANY(ABS(EPS_CONVERGE(4:5))>+0.0_REAL32))RETURN" in packed,
            "unused EPS-CONVERGE slots are numerical zero")

    solved = (
        "CHARACTER_RECORD_MATCHES(SEED_AUTHORITY,'STATE',3,12,'SOLVED')"
    )
    require(solved in packed, "input authority must be explicitly SOLVED")
    require("RECORD_MATCHES(SEED_AUTHORITY,'EPOCH',1,1)" in packed,
            "input integer epoch schema")
    require("CALLLCMGET(SEED_AUTHORITY,'EPOCH',SEED_EPOCH)" in packed,
            "input epoch read")
    require(
        "IF(SEED_EPOCH<0.OR.SEED_EPOCH==HUGE(SEED_EPOCH))RETURN" in packed,
        "epoch overflow preflight",
    )
    require(packed.count("OUTPUT_EPOCH=SEED_EPOCH+1") == 1,
            "exact epoch+1 transition")
    require("RECORD_MATCHES(SEED_AUTHORITY,'RHO',1,4)" in packed,
            "input lifecycle RHO type-4 schema")
    require("CALLLCMGET(SEED_AUTHORITY,'RHO',SEED_RHO64)" in packed,
            "input lifecycle RHO read")
    require("AUTHORITY_STATE='PROJECTED'" in packed,
            "output authority must be explicitly PROJECTED")
    require("CALLLCMPTC(OUTPUT_AUTHORITY,'STATE',12,AUTHORITY_STATE)" in packed,
            "PROJECTED state publication")
    require("CALLLCMPUT(OUTPUT_AUTHORITY,'RHO',1,4,RHO64)" in packed,
            "caller-supplied output lifecycle RHO is type 4")
    require("CALLLCMPUT(OUTPUT_AUTHORITY,'EPOCH',1,1,OUTPUT_EPOCH)" in packed,
            "new state epoch publication")
    # B2h proves only the record name, kind and lifecycle hand-off.  The
    # physical provenance of caller-supplied RHO (including RHO = 1/k) is
    # deliberately outside this isolated projection phase.
    require(re.search(r"\bKEFF\b", fortran_code(raw), re.IGNORECASE) is None,
            "KEFF is forbidden; caller-supplied RHO provenance is unproved")

    seed_reads = (
        "RECORD_MATCHES(SEED_AUTHORITY,'FLUX',NGRP,10)",
        "RECORD_MATCHES(SEED_AUTHORITY,'SOUR',NGRP,10)",
        "SEED_FLUX=LCMGID(SEED_AUTHORITY,'FLUX')",
        "SEED_SOURCE=LCMGID(SEED_AUTHORITY,'SOUR')",
    )
    for fragment in seed_reads:
        require(fragment in packed, f"complete SOLVED seed admission: {fragment}")
    require(packed.count("ITYLCM/=4") == 2,
            "SOLVED FLUX and SOUR elements are both type 4")

    mapping = (
        "PROJECTED_FLUX64=SEED_FLUX64"
        "DOIG=1,NGRP"
        "DOIR=1,NREG"
        "PROJECTED_FLUX64(KEYFLX(IR),IG)=PROJECTED_REGION64(IR,IG)"
        "ENDDOENDDO"
    )
    require(mapping in packed,
            "projected scalar replacement preserves solved non-scalar unknowns")

    # Complete no-write preflight must precede the first output mutation.
    authority_create = "OUTPUT_AUTHORITY=LCMDID(IPOUT,'SPOT-R64')"
    root_create = "LEGACY_FLUX=LCMLID(IPOUT,'FLUX',NGRP)"
    authority_list = "OUTPUT_FLUX=LCMLID(OUTPUT_AUTHORITY,'FLUX',NGRP)"
    authority_write = (
        "CALLLCMPDL(OUTPUT_FLUX,IG,NUNKNO,4,PROJECTED_FLUX64(:,IG))"
    )
    root_write = "CALLLCMPDL(LEGACY_FLUX,IG,NUNKNO,2,FLUX_STAGE32(:,IG))"
    for fragment in (
        authority_create, authority_list, authority_write, root_create, root_write
    ):
        require(packed.count(fragment) == 1, f"single publication step: {fragment}")

    write_tokens = (
        "LCMDID(", "LCMLID(", "CALLLCMPUT(", "CALLLCMPDL(",
        "CALLLCMPTC(", "CALLLCMDEL(", "CALLLCMEQU(",
    )
    before_authority = packed[:packed.index(authority_create)]
    for token in write_tokens:
        require(token not in before_authority,
                f"no output mutation before type-4 authority: {token}")
    require(
        packed.index(authority_create)
        < packed.index(authority_list)
        < packed.index(authority_write)
        < packed.index(root_create)
        < packed.index(root_write)
        < packed.index("CALLLCMPUT(IPOUT,'SPOT-LEAK1D',NGRP,2,LEAK1D)")
        < packed.index("CALLLCMPTC(OUTPUT_AUTHORITY,'STATE',12,AUTHORITY_STATE)")
        < packed.index("CALLLCMPUT(OUTPUT_AUTHORITY,'EPOCH',1,1,OUTPUT_EPOCH)"),
        "type-4 payload precedes compatibility; STATE/EPOCH commit last",
    )

    require(packed.count("FLUX_STAGE32=REAL(PROJECTED_FLUX64,REAL32)") == 1,
            "one authority-derived REAL32 staging conversion")
    require(packed.count("REAL(PROJECTED_FLUX64,REAL32)") == 1,
            "no second REAL64-to-REAL32 flux conversion")
    require("CALLLCMGDL(LEGACY_FLUX" not in packed,
            "root compatibility FLUX is write-only")
    require("CALLLCMGDL(IPOUT" not in packed,
            "output root is never an input authority")

    # The projection object carries only FLUX.  Reading seed SOUR proves the
    # SOLVED input is complete, but neither SOUR nor QFISS may be copied or
    # created in the PROJECTED output.
    require("LCMEQU(" not in packed, "no whole-object copy into output")
    for owner in ("OUTPUT_AUTHORITY", "IPOUT"):
        for name in ("SOUR", "QFISS"):
            for api in ("LCMDID", "LCMLID", "LCMPUT", "LCMPTC"):
                require(f"{api}({owner},'{name}'" not in packed,
                        f"PROJECTED output excludes {owner}/{name}")
    require(packed.count("LCMLID(") == 2,
            "only authority FLUX and root FLUX lists are created")
    require("STATUS=SPOR64_B2H_PROJECTED_COMMITTED" in packed,
            "single complete projected commit status")
    require(packed.rfind("STATUS=SPOR64_B2H_PROJECTED_COMMITTED")
            > packed.index("CALLLCMPUT(OUTPUT_AUTHORITY,'EPOCH',1,1,OUTPUT_EPOCH)"),
            "status commit follows STATE/EPOCH")
    after_epoch = packed.split(
        "CALLLCMPUT(OUTPUT_AUTHORITY,'EPOCH',1,1,OUTPUT_EPOCH)", 1
    )[1]
    for token in write_tokens:
        require(token not in after_epoch,
                f"no LCM mutation after terminal EPOCH commit: {token}")

    forbidden_calls = (
        "FLU2DR64_CORE", "SPOR64_B2B_INGRESS", "SPOR64_B2C_PUBLISH",
        "XDRTA2", "SPOFSRC", "SPOFCHK", "DOORFV", "FLUDRV",
    )
    for name in forbidden_calls:
        require(name not in packed, f"B2h is not a solver/host step: {name}")


def check_no_empirical_controls(text: str) -> None:
    """Reject numerical modelling or convergence controls in the B2h module."""

    code = fortran_code(text).upper()
    forbidden_words = (
        "ALPHA", "BETA", "OMEGA", "RELAX", "DAMP", "AITKEN",
        "ANDERSON", "CLIP", "FLOOR", "FITTED", "FITTING", "TUNING",
        "CALIBRATE", "CALIBRATION", "EMPIRICAL", "BLEND", "MIXING",
        "TOLERANCE", "THRESHOLD",
    )
    for word in forbidden_words:
        require(re.search(rf"\b{word}\b", code) is None,
                f"hidden empirical/control token: {word}")
    for physical_source in ("NUSIGF", "CHI", "DSOUR", "QFISS"):
        require(re.search(rf"\b{physical_source}\b", code) is None,
                f"projection phase must not construct a source: {physical_source}")


def production_code(path: str, text: str) -> str:
    """Remove comments from production free/fixed Fortran and CLE-2000."""

    suffix = Path(path).suffix.lower()
    kept: list[str] = []
    for raw in text.splitlines():
        if suffix == ".f" and raw[:1] in {"*", "c", "C", "!"}:
            continue
        if suffix == ".c2m" and raw[:1] in {"*", "!"}:
            continue
        kept.append(raw.split("!", 1)[0])
    return "\n".join(kept)


def check_production_isolation(files: Mapping[str, str]) -> None:
    """Prove no existing production caller or procedure selects B2h."""

    require(files, "production isolation inventory is empty")
    for path, text in files.items():
        if Path(path).as_posix() == "src/SPOR64_B2H.f90":
            continue
        code = production_code(path, text)
        require(re.search(r"(?i)\bSPOR64_B2H\b", code) is None,
                f"B2h production connection is forbidden in {path}")
        require(
            re.search(r"(?i)\bSPOR64_B2H_(?:PROJECT|RECONSTRUCT)\s*\(", code)
            is None,
            f"B2h production call is forbidden in {path}",
        )


def check_spoproj_stale_hazard(text: str) -> None:
    """Keep the legacy stale-authority hazard explicit and unclaimed as fixed."""

    packed = compact_free(text)
    require("SUBROUTINESPOPROJ(" in packed, "legacy SPOPROJ source")
    require("JPPLANE=LCMGID(KPFLUX,'FLUX')" in packed,
            "legacy projection selects only root FLUX")
    require("PROJECTED=REAL(CANONICAL_VALUE)" in packed,
            "legacy fixed-space projection still downcasts")
    require("CALLLCMPDL(JPPLANE,IGR,NUNK2D,2,U2D)" in packed,
            "legacy projection still publishes type-2 root FLUX")
    require("SPOT-R64" not in packed,
            "legacy SPOPROJ must not be misrepresented as authority-aware")
    require("SPOR64_B2H" not in packed,
            "B2h must not be connected through legacy SPOPROJ")


def load_production_files(root: Path = ROOT) -> dict[str, str]:
    files: dict[str, str] = {}
    for directory, suffixes in ((root / "src", {".f", ".f90"}),
                                (root / "data", {".c2m"})):
        for path in sorted(directory.rglob("*")):
            if path.is_file() and path.suffix.lower() in suffixes:
                # Shipped legacy CLE-2000 files are not uniformly UTF-8.
                # Surrogate escape preserves every byte while leaving the
                # ASCII procedure/call tokens available to the isolation gate.
                files[str(path.relative_to(root))] = path.read_text(
                    encoding="utf-8", errors="surrogateescape"
                )
    return files


def check_all(
    b2h_text: str,
    spoproj_text: str,
    production_files: Mapping[str, str],
) -> None:
    check_reconstruct(b2h_text)
    check_project(b2h_text)
    check_no_empirical_controls(b2h_text)
    check_spoproj_stale_hazard(spoproj_text)
    check_production_isolation(production_files)


def main() -> None:
    try:
        check_all(
            B2H_SOURCE.read_text(),
            SPOPROJ_SOURCE.read_text(),
            load_production_files(),
        )
    except (GateError, OSError) as error:
        raise SystemExit(
            f"SPOR64 PHASE-A9b-B2h PROJECTION AUTHORITY FAILURE: {error}"
        ) from error
    print(
        "SPOR64 PHASE-A9b-B2h PROJECTION AUTHORITY STATIC PASS: "
        "SOLVED->PROJECTED EPOCH+1 TYPE4-FIRST HOST-CONNECTED=false "
        "SPOPROJ-STALE-HAZARD=true"
    )


if __name__ == "__main__":
    main()
