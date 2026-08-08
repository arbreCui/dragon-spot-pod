#!/usr/bin/env python3
"""Fail-closed static contract for one bounded B2v continuation return."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OBSERVER = HERE / "b2v_spor64t_observer.f90"
PRODUCTION_ADAPTER = ROOT / "src/SPOR64_B2U.f90"
HOST = ROOT / "data/SpotStepR64.c2m"
DECK = HERE / "one_real_continuation.x2m"
BOUNDED = HERE / "run_bounded_b2v.py"
RUNNER = HERE / "run_phase_a9b_b2v_one_real_continuation.sh"
POSTERIOR = HERE / "check_b2v_real_returned.f90"
B2S = ROOT / "src/SPOR64_B2S.f90"
B2T = ROOT / "src/SPOR64_B2T.f90"
README = HERE / "README.md"
MANIFEST = HERE / "precision_manifest.json"
RUNTIME_RESULT = HERE / "runtime_result.txt"
ROOT_README = ROOT / "README.md"
ITERATIVE_README = ROOT / "validation/iterative/README.md"


class GateError(RuntimeError):
    """Raised when the B2v contract differs."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def fortran_without_comments(text: str) -> str:
    return "\n".join(line.split("!", 1)[0] for line in text.splitlines())


def deck_without_comments(text: str) -> str:
    return "\n".join(
        line for line in text.splitlines() if not line.lstrip().startswith("*")
    )


def packed(text: str) -> str:
    return re.sub(r"[\s&]+", "", text).upper()


def check_observer(observer_text: str, production_text: str) -> None:
    begin = "! B2V_OBSERVER_BEGIN"
    end = "! B2V_OBSERVER_END"
    require(observer_text.count(begin) == 1, "observer begin marker differs")
    require(observer_text.count(end) == 1, "observer end marker differs")
    start = observer_text.index(begin)
    stop = observer_text.index(end, start) + len(end)
    block = observer_text[start:stop]
    stripped = observer_text[:start] + observer_text[stop:]
    require(
        packed(fortran_without_comments(stripped))
        == packed(fortran_without_comments(production_text)),
        "observer differs from production SPOR64_B2U outside its marked write",
    )
    code = packed(fortran_without_comments(block))
    expected = (
        "WRITE(6,'(A,I0,A,I0,A,I0,A,I0)')"
        "'B2V-OBSERVERSTATUS=',STATUS,"
        "'CUTOFF-P1=',CUTOFF_BY_PLANE(1),"
        "'CUTOFF-P2=',CUTOFF_BY_PLANE(2),"
        "'CUTOFF-P3=',CUTOFF_BY_PLANE(3)"
    )
    require(code == expected, "observer block is not the one fixed-format write")
    require("IF(" not in code and "LCM" not in code, "observer write branches or mutates LCM")
    full = packed(fortran_without_comments(observer_text))
    call = (
        "CALLSPOR64_B2T_HOST_STEP(KENTRY(1),KENTRY(2),SYSTEMS,KENTRY(6),"
        "STATUS,CUTOFF_BY_PLANE,.TRUE.)"
    )
    write_at = full.index(expected)
    require(full.index(call) < write_at, "observer write must follow B2T")
    require(
        write_at < full.index("IF(STATUS/=SPOR64_B2T_RETURNED)"),
        "observer write must precede status dispatch",
    )


def check_deck(text: str) -> None:
    code = deck_without_comments(text).upper()
    compact = packed(code)
    for token in (
        "SEQ_BINARYTRACK_F::FILE'./INITIAL_RADIAL_TRACK.BIN';",
        "XSM_FILEPROJ_XSM::FILE'./PROJECTED.XSM';",
        "XSM_FILERET_XSM::FILE'./RETURNED.XSM';",
        "LINKED_LISTPROJECTEDRETURNED;",
        "PROCEDURESPOTSTEPR64;",
    ):
        require(token in compact, f"deck missing {token}")
    input_copy = "PROJECTED:=PROJ_XSM;"
    host_call = "RETURNED:=SPOTSTEPR64PROJECTEDTRACK_F::;"
    evidence = "RET_XSM:=RETURNED;"
    cleanup = "PROJECTEDRETURNED:=DELETE:PROJECTEDRETURNED;"
    for fragment in (input_copy, host_call, evidence, cleanup):
        require(compact.count(fragment) == 1, f"deck count differs: {fragment}")
    positions = [compact.index(item) for item in (input_copy, host_call, evidence, cleanup)]
    require(positions == sorted(positions), "deck lifecycle order differs")
    require(code.count("B2V-REAL-CONTINUATION-BEGIN") == 1, "begin marker differs")
    require(code.count("B2V-REAL-CONTINUATION-COMPLETE") == 1, "complete marker differs")
    for forbidden in (
        "WHILE", "REPEAT", "UNTIL", "PICARD", "RELAX", "DAMP", "CLIP",
        "SPOSTATE:", "SPOLEAK:", "SPOR64K:", "FLU:", "CONT:", "CLOSED",
    ):
        require(forbidden not in code, f"forbidden deck token {forbidden}")


def check_host(text: str) -> None:
    code = packed(deck_without_comments(text))
    require(code.count(":=ASM:") == 3, "SpotStepR64 must call ASM exactly three times")
    for plane in (1, 2, 3):
        require(
            f"SYSTEM{plane}:=ASM:MACRO0TRACKTRACK_FPROJECTED::"
            f"EDIT0ARMLK1D{plane};" in code,
            f"SpotStepR64 plane-{plane} ASM differs",
        )
    dispatch = "RETURNED:=SPOR64T:PROJECTEDSYSTEM1SYSTEM2SYSTEM3TRACK_F::;"
    require(code.count(dispatch) == 1, "SpotStepR64 SPOR64T dispatch differs")
    require(code.rfind(":=ASM:") < code.index(dispatch), "SPOR64T precedes final ASM")
    for forbidden in ("WHILE", "REPEAT", "RELAX", "DAMP", "CLIP", "SPOSTATE:", "SPOLEAK:"):
        require(forbidden not in code, f"forbidden host token {forbidden}")


def check_chain(b2s_text: str, b2t_text: str) -> None:
    s = packed(fortran_without_comments(b2s_text))
    t = packed(fortran_without_comments(b2t_text))
    require(s.count("DOPLANE=1,NSNAP") >= 1, "B2S lacks canonical plane loop")
    require(s.count("CALLSPOR64_B2B_INGRESS(") == 1, "B2S B2B call site count differs")
    require("SPOR64_B2B_CONT,RADIAL_STATUS,CUTOFF_BY_PLANE(PLANE)" in s,
            "B2S cutoff plane binding differs")
    require("IF(RADIAL_STATUS/=SPOR64_B2C_HOST_COMMITTED)THEN" in s,
            "B2S strict radial status gate differs")
    require(s.count("CALLSPOR64_B2R_COLLECT(") == 1, "B2S collector count differs")
    require(t.count("CALLSPOR64_B2S_HOST_BRIDGE(") == 1, "B2T bridge count differs")
    for forbidden in ("RELAX", "DAMP", "CLIP", "EMPIRICAL"):
        require(forbidden not in s + t, f"forbidden chain token {forbidden}")


def check_bounded(path: Path) -> None:
    spec = importlib.util.spec_from_file_location("b2v_bounded", path)
    require(spec is not None and spec.loader is not None, "cannot load bounded helper")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    require(module.PROFILES["dragon"] == {
        "wall_seconds": 60,
        "cpu_seconds": 55,
        "rss_bytes": 2 * 1024**3,
        "file_bytes": 512 * 1024**2,
        "log_bytes": 64 * 1024**2,
    }, "Dragon resource profile differs")
    require(module.RESOURCE_CLASS == {
        "prepare": "INVALID-NO-SCIENTIFIC-RESULT",
        "dragon": "INVALID-NO-SCIENTIFIC-RESULT",
        "posterior": "INVALID-RETURNED-EVIDENCE",
    }, "resource classification map differs")
    require(module.EXIT_CLASS == {
        "prepare": "INVALID-NO-SCIENTIFIC-RESULT",
        "dragon": "FAILED-NO-RETURN",
        "posterior": "INVALID-RETURNED-EVIDENCE",
    }, "exit classification map differs")
    require(module.TERM_GRACE_SECONDS == 5, "termination grace differs")
    text = path.read_text()
    for token in (
        "start_new_session=True", "RLIMIT_CPU", "RLIMIT_FSIZE", "RLIMIT_CORE",
        "os.killpg(process.pid, signal.SIGTERM)",
        "os.killpg(process.pid, signal.SIGKILL)",
        "log_bytes = log_path.stat().st_size",
        'if log_bytes > profile["log_bytes"]:',
        "signal.SIGXCPU",
        "signal.SIGXFSZ",
        "RESOURCE_CLASS[profile_name]",
        "EXIT_CLASS[profile_name]",
    ):
        require(token in text, f"bounded helper missing {token}")


def check_runner(text: str) -> None:
    require("RUN_B2V=${RUN_B2V:-0}" in text, "runtime must default off")
    require(text.count('python3 "$BOUNDED" dragon ') == 1,
            "runner must contain exactly one Dragon activation")
    require("NO-RETRY" in text, "runner lacks explicit no-retry classification")
    require("PRODUCTION-SPOR64T-EXECUTIONS=0" in text,
            "runner must disclose observer substitution")
    require("VALIDATION-OBSERVER-SPOR64T-EXECUTIONS=1" in text,
            "runner lacks observer census")
    require("OUTER-PICARD-CONVERGENCE=NOT-EVALUATED" in text,
            "runner overclaim guard missing")
    require("INVALID-RUNTIME-EVIDENCE" in text,
            "runner lacks insufficient-runtime-evidence classification")
    require("killall" not in text and "pkill" not in text,
            "runner contains broad process termination")


def check_posterior(text: str) -> None:
    code = packed(fortran_without_comments(text))
    require("PROGRAMCHECK_B2V_REAL_RETURNED" in code,
            "posterior program name differs")
    require("B2VREALRETURNEDPOSTERIORPASS" in code,
            "posterior pass marker missing")
    for forbidden in (
        "USESPOR64_", "CALLSPOR64", "CALLASM", "CALLXDRTA2", "CALLFLU",
        "CALLSPOMOC", "CALLSPOASM", "CALLSPOSTATE", "CALLSPOLEAK",
    ):
        require(forbidden not in code, f"posterior links/calls production path: {forbidden}")
    require("CALLLCMOP" in code and "CALLLCMCL" in code,
            "posterior lacks read-only XSM lifecycle")


def check_frozen_result(
    runtime_text: str,
    manifest_text: str,
    phase_readme: str,
    root_readme: str,
    iterative_readme: str,
) -> None:
    require(len(runtime_text.splitlines()) == 36, "runtime transcript line count differs")
    require(len(runtime_text.encode()) == 2316, "runtime transcript byte count differs")
    require(
        hashlib.sha256(runtime_text.encode()).hexdigest()
        == "ace0bdcf25837c92e26ffd00bd71927ae4294633e71a3822bbc4ad7e32d7c57e",
        "runtime transcript hash differs",
    )
    for line in (
        "CLASSIFICATION=ONE-REAL-THREE-PLANE-CONTINUATION-RETURNED",
        "DRAGON-EXECUTIONS=1 ASM-EXECUTIONS=3 RADIAL-CONT-RETURNS=3 RETRIES=0",
        "VALIDATION-OBSERVER-SPOR64T-EXECUTIONS=1 PRODUCTION-SPOR64T-EXECUTIONS=0",
        "CUTOFF-P1=59 CUTOFF-P2=138 CUTOFF-P3=126",
        "CUTOFF-CLASS=INHERITED-ACA-CUTOFF-LOCAL-PREDICATE-DIFFERENCE-OBSERVED",
        "RETURNED-SHA256=dd41a37d484b85612a495ff7b1f2233a53fbae1b462d89bd84db2a8809cef054 BYTES=231572260",
        "AXIAL-SOLVE=0 OUTER-PICARD-CONVERGENCE=NOT-EVALUATED CLOSED/1=NOT-PUBLISHED",
        "INDEPENDENT-A9-RESIDUAL/NORM-VALIDATION=NOT-EVALUATED INTERNAL-TERMINATION-PATH=PROVENANCE-ONLY",
        "REPRODUCIBILITY=NOT-EVALUATED TRACK-HISTORICAL-IDENTITY=NOT-CLAIMED",
    ):
        require(runtime_text.count(line + "\n") == 1, f"runtime result differs: {line}")
    manifest = json.loads(manifest_text)
    result = manifest.get("runtime_result", {})
    require(result.get("classification") ==
            "ONE-REAL-THREE-PLANE-CONTINUATION-RETURNED",
            "manifest result classification differs")
    require(result.get("dragon_executions") == 1 and
            result.get("automatic_retries") == 0,
            "manifest execution census differs")
    require(result.get("cutoff_by_plane") == [59, 138, 126],
            "manifest cutoff observations differ")
    require(result.get("returned_sha256") ==
            "dd41a37d484b85612a495ff7b1f2233a53fbae1b462d89bd84db2a8809cef054",
            "manifest returned hash differs")
    require(result.get("private_dragon_sha256") ==
            "cda682f5ee2579acbf901b394d06ed6e37fd815077e233e358da22c76eb9bb1f",
            "manifest runtime private Dragon hash differs")
    require(manifest["posterior"]["terminal_norms_recomputed"] is False,
            "manifest overclaims terminal norm validation")
    require(manifest["posterior"]["transport_equation_residual_evaluated"] is False,
            "manifest overclaims residual validation")
    for text, owner in (
        (phase_readme, "phase README"),
        (root_readme, "root README"),
        (iterative_readme, "iterative README"),
    ):
        require("16.332" in text, f"{owner} lacks frozen elapsed result")
        require("dd41a37d484b85612a495ff7b1f2233a53fbae1b462d89bd84db2a8809cef054" in text,
                f"{owner} lacks returned evidence hash")
        require("outer" in text.lower() and "Picard" in text,
                f"{owner} lacks outer-Picard boundary")


def main() -> None:
    for path in (OBSERVER, PRODUCTION_ADAPTER, HOST, DECK, BOUNDED, RUNNER,
                 POSTERIOR, B2S, B2T, README, MANIFEST, RUNTIME_RESULT,
                 ROOT_README, ITERATIVE_README):
        require(path.is_file(), f"missing input: {path}")
    check_observer(OBSERVER.read_text(), PRODUCTION_ADAPTER.read_text())
    check_deck(DECK.read_text())
    check_host(HOST.read_text())
    check_chain(B2S.read_text(), B2T.read_text())
    check_bounded(BOUNDED)
    check_runner(RUNNER.read_text())
    check_posterior(POSTERIOR.read_text())
    check_frozen_result(
        RUNTIME_RESULT.read_text(),
        MANIFEST.read_text(),
        README.read_text(),
        ROOT_README.read_text(),
        ITERATIVE_README.read_text(),
    )
    print("B2V STATIC ONE-REAL-CONTINUATION PASS")
    print("B2V ACTIVATION=DEFAULT-OFF DRAGON-MAX=1 RETRY=0")
    print("B2V OBSERVER=PRODUCTION-SPOR64T-PLUS-ONE-UNCONDITIONAL-WRITE")
    print("B2V HOST=ASM1,2,3->B2T->B2S->B2B1,2,3->B2R")
    print("B2V LIMITS=WALL60 CPU55 RSS2G FILE512M LOG64M")
    print("B2V OUTER-PICARD=NOT-EVALUATED EMPIRICAL-CONTROLS-ADDED=0")
    print("B2V FROZEN-RESULT=ONE-REAL-THREE-PLANE-CONTINUATION-RETURNED")


if __name__ == "__main__":
    main()
