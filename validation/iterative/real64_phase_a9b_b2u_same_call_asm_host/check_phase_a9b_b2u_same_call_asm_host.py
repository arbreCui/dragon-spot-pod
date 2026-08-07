#!/usr/bin/env python3
"""Fail-closed static contract for the B2u same-call ASM host route."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from typing import Any, Mapping


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
HOST = ROOT / "data/SpotStepR64.c2m"
FROZEN_HOST = ROOT / "data/SpotAsmR64.c2m"
ADAPTER = ROOT / "src/SPOR64_B2U.f90"
KDRDRV = ROOT / "src/KDRDRV.F"
DRAMOD = ROOT / "src/dramod.f90"
GANMOD_MIRROR = ROOT / "Ganlib/src/ganmod.f90"
TRACK_ARTIFACT = (
    ROOT / "validation/artifacts/iterative-seed/initial_radial_track.bin"
)
README = HERE / "README.md"
MANIFEST = HERE / "precision_manifest.json"
PARENT_RECEIPT = (
    ROOT
    / "validation/iterative/real64_phase_a9b_b2t_owned_source_host_step"
    / "phase_a9b_b2t_owned_source_host_step_receipt.sha256"
)

PARENT_COMMIT = "1251f3a5eff95384f83d98d460ca430288736db7"
PARENT_RECEIPT_SHA256 = (
    "08d539c973a4881bbc3e431ddb4dace3da836a245fab9a7d19303c44a823e8af"
)
PARENT_B2T_SHA256 = (
    "ee77bb076c1b6239017067a32ead8a95c45a0cf49cd1426ef51aca30bac79816"
)
FROZEN_HOST_SHA256 = (
    "31ec89036bbd2ea62b27fbd4dff5aa1054f3f24997e383f05389e1dda91e364d"
)
TRACK_SHA256 = (
    "f7b27cb4a5d37f903b93e49610e2daa2290d55c164e2ca0e73ccb8d22fe486b8"
)
TRACK_BYTES = 2_275_636
DECK_SUFFIXES = {".x2m", ".d2p", ".access", ".c2m"}


class GateError(AssertionError):
    """The narrow B2u static contract was violated."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def strip_fortran_comments(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        if line.lstrip().startswith("!"):
            continue
        if line and line[0] in "cC*":
            continue
        lines.append(line.split("!", 1)[0])
    return "\n".join(lines)


def strip_deck_comments(text: str) -> str:
    return "\n".join(
        line for line in text.splitlines()
        if not line.lstrip().startswith("*")
    )


def packed(text: str) -> str:
    return re.sub(r"[\s&]+", "", text).upper()


def routine(text: str, name: str) -> str:
    match = re.search(
        rf"(?is)\bsubroutine\s+{re.escape(name)}\b.*?"
        rf"\bend\s+subroutine\s+{re.escape(name)}\b",
        strip_fortran_comments(text),
    )
    require(match is not None, f"missing subroutine {name}")
    return match.group(0)


def require_order(owner: str, text: str, fragments: tuple[str, ...]) -> None:
    code = packed(text)
    position = -1
    for fragment in fragments:
        needle = packed(fragment)
        found = code.find(needle, position + 1)
        require(found > position, f"{owner}: missing or reordered {fragment}")
        position = found


def check_host(text: str) -> None:
    code = packed(strip_deck_comments(text))
    require(
        "PARAMETERRETURNEDPROJECTEDTRACK_F::"
        ":::LINKED_LISTRETURNEDPROJECTED;:::SEQ_BINARYTRACK_F;;" in code,
        "SpotStepR64 formal media contract differs",
    )
    require(
        "LINKED_LISTMICROLIB2MACRO0TRACKSYSTEM1SYSTEM2SYSTEM3;" in code,
        "SpotStepR64 private-object inventory differs",
    )
    require(
        "MODULERECOVER:ASM:SPOR64T:DELETE:END:;" in code,
        "SpotStepR64 module allowlist differs",
    )
    require(code.count(":=ASM:") == 3,
            "SpotStepR64 must contain exactly three ASM calls")

    plane_blocks: list[str] = []
    for plane in (1, 2, 3):
        block = (
            f"MICROLIB2:=RECOVER:PROJECTED::ITEM{plane};"
            "MACRO0:=MICROLIB2;MICROLIB2:=DELETE:MICROLIB2;"
            f"TRACK:=RECOVER:PROJECTED::ITEM{plane};"
            f"SYSTEM{plane}:=ASM:MACRO0TRACKTRACK_FPROJECTED::"
            f"EDIT0ARMLK1D{plane};"
            "MACRO0TRACK:=DELETE:MACRO0TRACK;"
        )
        require(code.count(block) == 1,
                f"SpotStepR64 same-index plane-{plane} block differs")
        plane_blocks.append(block)

    bridge = (
        "RETURNED:=SPOR64T:PROJECTEDSYSTEM1SYSTEM2SYSTEM3TRACK_F::;"
    )
    cleanup = (
        "SYSTEM1SYSTEM2SYSTEM3:=DELETE:SYSTEM1SYSTEM2SYSTEM3;"
    )
    require(code.count(bridge) == 1,
            "SpotStepR64 must make one exact SPOR64T call")
    require(code.count(":=SPOR64T:") == 1,
            "SpotStepR64 must contain exactly one SPOR64T dispatch")
    require(code.count(cleanup) == 1,
            "SpotStepR64 must delete all three SYSTEM objects after return")
    require_order(
        "SpotStepR64 causal order",
        code,
        (plane_blocks[0], plane_blocks[1], plane_blocks[2], bridge, cleanup),
    )

    bridge_at = code.index(bridge)
    before_bridge = code[:bridge_at]
    require(
        re.search(r"SYSTEM[123](?:SYSTEM[123])*:=DELETE:", before_bridge)
        is None,
        "candidate SYSTEM deleted before SPOR64T",
    )
    require(code.count("TRACK_FPROJECTED::EDIT0ARMLK1D") == 3,
            "ASM calls do not share exact TRACK_f/PROJECTED symbols")

    for forbidden in (
        "SPOR64K:", "FLU:", "SPOFSRC:", "SPOFCHK:", "SPOASM:",
        "SPOSTATE:", "SPOLEAK:", "CONT", "WHILE", "REPEAT", "UNTIL",
        "PICARD", "RELAX", "DAMP", "CLIP", "FITTED", "FIT ",
        "MODEL-COMPLETION", "TOLERANCE", "ALPHA", "BETA",
    ):
        require(forbidden not in code,
                f"SpotStepR64 acquired forbidden token {forbidden}")
    require("::>>" not in code,
            "SpotStepR64 acquired an unreviewed scalar control")


def check_adapter(text: str) -> None:
    body = routine(text, "SPOR64T")
    code = packed(body)
    signature = code.split(")", 1)[0]
    require(
        signature == "SUBROUTINESPOR64T(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY",
        "SPOR64T ABI changed",
    )
    require(
        "USESPOR64_B2T,ONLY:SPOR64_B2T_RETURNED,"
        "SPOR64_B2T_HOST_STEP" in code,
        "SPOR64T does not import the exact B2t boundary",
    )
    for token in (
        "INTEGER,INTENT(IN)::NENTRY,IENTRY(NENTRY),JENTRY(NENTRY)",
        "CHARACTER(LEN=12),INTENT(IN)::HENTRY(NENTRY)",
        "TYPE(C_PTR),INTENT(IN)::KENTRY(NENTRY)",
        "INTEGER(INT64)::CUTOFF_BY_PLANE(3)",
        "TYPE(C_PTR)::SYSTEMS(3)",
        "IF(NENTRY/=6)THEN",
        "IF(HENTRY(1)/='RETURNED'.OR.HENTRY(2)/='PROJECTED')THEN",
        "IF(HENTRY(3)/='SYSTEM1'.OR.HENTRY(4)/='SYSTEM2'.OR."
        "HENTRY(5)/='SYSTEM3')THEN",
        "IF(HENTRY(6)/='TRACK_F')THEN",
        "IF(ANY(IENTRY(1:5)/=1).OR.IENTRY(6)/=3)THEN",
        "IF(JENTRY(1)/=0.OR.ANY(JENTRY(2:6)/=2))THEN",
        "CALLREDGET(INDIC,NITMA,FLOTT,TEXT4,DFLOTT)",
        "IF(INDIC/=3.OR.TEXT4/=';')THEN",
        "SYSTEMS=KENTRY(3:5)",
        "CALLSPOR64_B2T_HOST_STEP(KENTRY(1),KENTRY(2),SYSTEMS,KENTRY(6),"
        "STATUS,CUTOFF_BY_PLANE,.TRUE.)",
        "IF(STATUS/=SPOR64_B2T_RETURNED)THEN",
    ):
        require(token in code, f"SPOR64T contract missing {token}")

    require(code.count("CALLREDGET(") == 1,
            "SPOR64T option-list read count differs")
    require(code.count("CALLSPOR64_B2T_HOST_STEP(") == 1,
            "SPOR64T B2t call count differs")
    require_order(
        "SPOR64T preflight and forwarding order",
        body,
        (
            "if (nentry /= 6)",
            "if (hentry(1) /= 'RETURNED'",
            "if (hentry(3) /= 'SYSTEM1'",
            "if (hentry(6) /= 'TRACK_f')",
            "if (any(ientry(1:5) /= 1)",
            "if (jentry(1) /= 0",
            "call REDGET",
            "if (indic /= 3 .or. text4 /= ';')",
            "systems = kentry(3:5)",
            "call SPOR64_B2T_HOST_STEP",
            "if (status /= SPOR64_B2T_RETURNED)",
        ),
    )
    require(code.count("CUTOFF_BY_PLANE") == 2,
            "cutoff diagnostic acquired an extra role")

    for forbidden in (
        "SUM(CUTOFF_BY_PLANE", "MAXVAL(CUTOFF_BY_PLANE",
        "MINVAL(CUTOFF_BY_PLANE", "IF(CUTOFF_BY_PLANE",
        "CALLSPOR64_B2K", "CALLSPOR64_B2N", "CALLSPOR64_B2S",
        "CALLSPOR64_B2B", "CALLASM", "CALLFLU", "FLU2DR64_CORE",
        "CALLSPOASM", "CALLSPOSTATE", "CALLSPOLEAK", "LCMPUT(",
        "LCMPTC(", "LCMEQU(", "RELAX", "DAMP", "CLIP", "FITTED",
        "MODEL_COMPLETION", "TOLERANCE", "ALPHA=", "BETA=",
    ):
        require(forbidden not in code,
                f"SPOR64T acquired forbidden role {forbidden}")


def check_kdr(text: str) -> None:
    code = packed(strip_fortran_comments(text))
    route = (
        "ELSEIF(HMODUL.EQ.'SPOR64T:')THEN"
        "CALLSPOR64T(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)"
    )
    require(code.count("HMODUL.EQ.'SPOR64T:'") == 1,
            "KDRDRV SPOR64T selector count differs")
    require(code.count("CALLSPOR64T(") == 1,
            "KDRDRV SPOR64T call count differs")
    require(route in code, "KDRDRV SPOR64T route differs")
    require_order(
        "KDRDRV route position",
        code,
        (
            "ELSEIF(HMODUL.EQ.'SPOR64K:')",
            route,
            "ELSEIF(HMODUL.EQ.'FLU:')",
        ),
    )


def check_dramod(text: str) -> None:
    code = packed(strip_fortran_comments(text))
    for token in (
        "IF((IENTRY(I)>=3).AND.(IENTRY(I)<=5))THEN",
        "MY_FILE_ARRAY(I)%MY_FILE=>"
        "FILOPN(HPARAM,JENTRY(I),IENTRY(I)-1,0)",
        "KENTRY(I)=C_LOC(MY_FILE_ARRAY(I)%MY_FILE)",
        "DRAMOD=KDRDRV(HMODUL,NENTRY,HENTRY_F,IENTRY,JENTRY,KENTRY)",
        "IER=FILCLS(MY_FILE_ARRAY(I)%MY_FILE,1)",
    ):
        require(token in code, f"DRAMOD file lifetime token missing: {token}")
    require_order(
        "DRAMOD per-dispatch file lifetime",
        code,
        (
            "FILOPN(HPARAM,JENTRY(I),IENTRY(I)-1,0)",
            "KENTRY(I)=C_LOC(MY_FILE_ARRAY(I)%MY_FILE)",
            "DRAMOD=KDRDRV(HMODUL,NENTRY,HENTRY_F,IENTRY,JENTRY,KENTRY)",
            "FILCLS(MY_FILE_ARRAY(I)%MY_FILE,1)",
        ),
    )


def deployment_sources() -> dict[str, str]:
    sources: dict[str, str] = {}
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in DECK_SUFFIXES:
            continue
        relative = path.relative_to(ROOT)
        if relative.parts[0] in {"validation", ".git"}:
            continue
        if path == HOST:
            continue
        sources[str(relative)] = path.read_text(encoding="utf-8", errors="replace")
    return sources


def check_deployment(sources: Mapping[str, str]) -> None:
    selectors: list[str] = []
    for name, text in sources.items():
        code = strip_deck_comments(text)
        if re.search(r"(?i)\bPROCEDURE\b[^;]*\bSpotStepR64\b", code):
            selectors.append(name)
        elif re.search(r"(?i):=\s*SpotStepR64\b", code):
            selectors.append(name)
    require(not selectors,
            "shipped calculation selects SpotStepR64: " + ", ".join(selectors))


def check_parent_receipt(text: str) -> None:
    require(
        hashlib.sha256(text.encode("utf-8")).hexdigest()
        == PARENT_RECEIPT_SHA256,
        "B2t parent receipt changed",
    )
    require(
        f"{PARENT_B2T_SHA256}  src/SPOR64_B2T.f90" in text.splitlines(),
        "B2t parent source entry differs",
    )


def check_track_artifact(path: Path = TRACK_ARTIFACT) -> None:
    require(path.is_file() and not path.is_symlink(),
            "hash-pinned tracking artifact missing or symbolic")
    require(path.stat().st_size == TRACK_BYTES,
            "hash-pinned tracking artifact byte count differs")
    require(sha256(path) == TRACK_SHA256,
            "hash-pinned tracking artifact SHA-256 differs")


def check_manifest(manifest: Mapping[str, Any]) -> None:
    require(manifest.get("phase") == "A9b-B2u", "manifest phase changed")
    require(
        manifest.get("purpose")
        == "freeze the deployment-default-off CLE host route that creates three fresh ASM SYSTEM objects and gives them immediately to the B2t adapter",
        "manifest purpose changed",
    )
    require(manifest.get("parent_phase") == "A9b-B2t",
            "manifest parent phase changed")
    require(manifest.get("parent_commit") == PARENT_COMMIT,
            "manifest parent commit changed")
    require(manifest.get("parent_receipt_sha256") == PARENT_RECEIPT_SHA256,
            "manifest parent receipt changed")
    require(manifest.get("contract_version") == 1,
            "manifest contract version changed")
    require(manifest.get("production_scope") == [
        "data/SpotStepR64.c2m", "src/SPOR64_B2U.f90", "src/KDRDRV.F",
    ], "manifest production scope changed")
    require(manifest.get("supporting_runtime_semantics") == {
        "production_dispatch": "src/dramod.f90",
        "ganlib_mirror": "Ganlib/src/ganmod.f90",
    }, "manifest dispatch support scope changed")

    require(manifest.get("deployment_default_off") == {
        "procedure": "SpotStepR64",
        "shipped_calculation_deck_selections": 0,
        "explicit_procedure_selection_required": True,
        "in_procedure_enable_parameter": False,
        "meaning": "the suffixed procedure is inert because no shipped calculation deck selects it; once explicitly selected it executes its fixed route",
    }, "manifest deployment-default-off contract changed")

    host = manifest.get("host_contract", {})
    require(host == {
        "formal_output": "RETURNED",
        "formal_lcm_input": "PROJECTED",
        "formal_sequential_binary_input": "TRACK_f",
        "private_systems": ["SYSTEM1", "SYSTEM2", "SYSTEM3"],
        "asm_calls": 3,
        "asm_lk1d_order": [1, 2, 3],
        "projected_symbol_for_every_asm": "PROJECTED",
        "track_symbol_for_every_asm": "TRACK_f",
        "spor64t_calls": 1,
        "spor64t_arguments": [
            "RETURNED", "PROJECTED", "SYSTEM1", "SYSTEM2", "SYSTEM3",
            "TRACK_f",
        ],
        "systems_remain_live_until_spor64t_returns": True,
        "systems_deleted_after_spor64t": True,
        "caller_supplied_systems": False,
        "loops": 0,
        "automatic_retries": 0,
    }, "manifest host contract changed")

    adapter = manifest.get("adapter_contract", {})
    require(adapter == {
        "module_name": "SPOR64T:",
        "fortran_procedure": "SPOR64T",
        "nentry": 6,
        "hentry": [
            "RETURNED", "PROJECTED", "SYSTEM1", "SYSTEM2", "SYSTEM3",
            "TRACK_f",
        ],
        "ientry": [1, 1, 1, 1, 1, 3],
        "jentry": [0, 2, 2, 2, 2, 2],
        "option_list": "exact empty semicolon",
        "system_pointer_slice": "KENTRY(3:5)",
        "track_pointer": "KENTRY(6)",
        "b2t_enable": True,
        "only_success_status": "SPOR64_B2T_RETURNED",
        "cutoff_kind": "INT64",
        "cutoff_shape": 3,
        "cutoff_aggregated": False,
        "cutoff_feeds_acceptance": False,
        "direct_solver_calls": 0,
    }, "manifest adapter contract changed")

    require(manifest.get("dispatcher_contract") == {
        "dispatcher": "KDRDRV",
        "route": "SPOR64T:",
        "callee": "SPOR64T",
        "route_count": 1,
        "position": "after SPOR64K: and before FLU:",
    }, "manifest dispatcher contract changed")

    tracking = manifest.get("tracking_lifecycle", {})
    require(tracking == {
        "same_cle_symbol_across_asm_and_spor64t": True,
        "intended_runtime_artifact_hash_pinned_by_gate": True,
        "artifact_opened_by_b2u_gate": False,
        "hash_pinned_artifact": "validation/artifacts/iterative-seed/initial_radial_track.bin",
        "hash_pinned_sha256": TRACK_SHA256,
        "hash_pinned_bytes": TRACK_BYTES,
        "dramod_opens_and_closes_sequential_file_per_module_dispatch": True,
        "same_live_pointer_across_asm1_asm2_asm3_and_spor64t": False,
        "same_live_pointer_inside_spor64t_b2t_b2s_b2b3": True,
        "historical_identity_with_archived_track_proved": False,
        "hash_alone_is_historical_identity_proof": False,
    }, "manifest tracking lifecycle changed")

    require(manifest.get("numerical_controls") == {
        "new_empirical_parameters": 0,
        "relaxation_added": False,
        "damping_added": False,
        "clipping_added": False,
        "fitted_coefficient_added": False,
        "model_completion_added": False,
        "convergence_threshold_added": False,
        "inherits_frozen_downstream_controls_without_retuning": True,
    }, "manifest numerical-control boundary changed")

    require(manifest.get("short_validation") == {
        "static_targeted_mutations": 39,
        "static_baseline_tests": 1,
        "c2m_compiles": 3,
        "production_chain_compile_only": [
            "SPOR64_B2C", "SPOR64_B2B", "SPOR64_B2O", "SPOR64_B2R",
            "SPOR64_B2S", "SPOR64_B2K", "SPOR64_B2N", "SPOR64_B2T",
            "SPOR64_B2U",
        ],
        "asm_compile_only": 1,
        "kdrdrv_compile_only": 1,
        "production_spor64t_adapter_executions": 7,
        "adapter_preflight_rejections": 5,
        "adapter_b2t_stub_failure_rejections": 1,
        "adapter_successes_against_b2t_stub": 1,
        "b2t_capture_stub_calls": 2,
        "dragon_processes": 0,
        "production_asm_runtime_executions": 0,
        "production_b2t_chain_runtime_executions": 0,
        "radial_transport_solves": 0,
        "picard_maps": 0,
        "long_calculations": 0,
    }, "manifest short-validation census changed")

    require(manifest.get("proved") == [
        "exact static ASM plane order 1,2,3",
        "one common PROJECTED symbol and one common TRACK_f symbol in every ASM call",
        "three local SYSTEM symbols remain in scope until the immediate SPOR64T call",
        "exact SPOR64T adapter ABI and KDRDRV route",
        "production SPOR64T preflight and exact pointer forwarding against a deterministic B2t capture stub",
        "deployment default-off because no shipped calculation deck selects SpotStepR64",
        "DRAGON dramod per-dispatch sequential-file reopen and close semantics",
        "no empirical or convergence control added",
    ], "manifest proved-scope changed")
    require(manifest.get("not_proved") == [
        "runtime execution of ASM or the true production B2t/B2s/B2B chain",
        "one live c_ptr shared across the three separate ASM module dispatches and SPOR64T",
        "historical identity of the archived TRACK objects and the hash-pinned binary file",
        "radial transport completion or convergence",
        "an outer Picard map or convergence",
        "response, eigenvalue, power, SPOD truncation, or benchmark accuracy",
    ], "manifest non-claim scope changed")


def check_readme(text: str) -> None:
    for required in (
        "deployment-default-OFF",
        "`SpotStepR64` is not selected by any shipped",
        "ASM(LK1D 1) -> SYSTEM1",
        "ASM(LK1D 2) -> SYSTEM2",
        "ASM(LK1D 3) -> SYSTEM3",
        "SPOR64T(PROJECTED,SYSTEM1,SYSTEM2,SYSTEM3,TRACK_f)",
        "It does **not** prove one live `c_ptr` across ASM1, ASM2, ASM3, and SPOR64T.",
        "DRAGON's `dramod` opens a sequential file before each module dispatch and",
        "Inside the single",
        "Neither the symbolic name nor the frozen hash proves",
        "does not open it through ASM or SPOR64T",
        "inherits the already frozen downstream termination and",
        "39 targeted mutations plus one",
        "positive baseline.",
        "calls the production `SPOR64T` adapter seven times",
        "five ABI/option-list preflight rejections",
        "B2t implementation in\nthat executable is a deterministic capture stub",
        "complete production B2C/B2B/B2O/B2R/B2S/B2K/B2N/B2T/B2U",
        "No Dragon, ASM, radial transport, or Picard execution is performed by this",
        "RUNTIME ASM / TRANSPORT / MAP   = NOT EXECUTED",
    ):
        require(required in text, f"README scope missing: {required}")
    for forbidden in (
        "REAL-ASM-PLANES1-3-EXECUTED",
        "RADIAL-CONVERGENCE=PASS",
        "PICARD-CONVERGENCE=PASS",
        "same live `c_ptr` across all four CLE module dispatches",
        "historical TRACK identity is proved",
    ):
        require(forbidden not in text, f"README overclaim present: {forbidden}")


def check_all() -> None:
    require(HOST.is_file(), "SpotStepR64 production host missing")
    require(
        FROZEN_HOST.is_file() and sha256(FROZEN_HOST) == FROZEN_HOST_SHA256,
        "frozen SpotAsmR64 parent changed",
    )
    require(ADAPTER.is_file(), "SPOR64T production adapter missing")
    require(KDRDRV.is_file(), "KDRDRV production dispatcher missing")
    require(DRAMOD.is_file(), "DRAMOD runtime support missing")
    require(GANMOD_MIRROR.is_file(), "GANMOD mirror missing")
    require(README.is_file(), "B2u README missing")
    require(MANIFEST.is_file(), "B2u manifest missing")
    require(PARENT_RECEIPT.is_file(), "B2t parent receipt missing")

    check_host(HOST.read_text(encoding="utf-8"))
    check_adapter(ADAPTER.read_text(encoding="utf-8"))
    check_kdr(KDRDRV.read_text(encoding="utf-8"))
    check_dramod(DRAMOD.read_text(encoding="utf-8"))
    check_deployment(deployment_sources())
    check_parent_receipt(PARENT_RECEIPT.read_text(encoding="utf-8"))
    check_track_artifact()
    check_manifest(json.loads(MANIFEST.read_text(encoding="utf-8")))
    check_readme(README.read_text(encoding="utf-8"))


def main() -> None:
    check_all()
    print("B2U STATIC SAME-CALL ASM HOST PASS")
    print("B2U DEPLOYMENT-DEFAULT=OFF SHIPPED-SELECTIONS=0")
    print("B2U HOST=ASM(1)->ASM(2)->ASM(3)->SPOR64T LIVE-SYSTEMS=3")
    print("B2U TRACK=SAME-CLE-SYMBOL HASH-PINNED-BYTES PER-DISPATCH-OPEN")
    print("B2U SPOR64T-LIVE-HANDLE=B2T->B2S->B2B(1,2,3)")
    print("B2U DRAGON=0 ASM-RUNTIME=0 TRANSPORT=0 PICARD=0")


if __name__ == "__main__":
    main()
