#!/usr/bin/env python3
"""Independent static audit for the B2t owned-source host step."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_PATH = ROOT / "src/SPOR64_B2T.f90"
MANIFEST_PATH = HERE / "precision_manifest.json"
README_PATH = HERE / "README.md"
PARENT_RECEIPT_PATH = (
    ROOT
    / "validation/iterative/real64_phase_a9b_b2s_immediate_host_bridge"
    / "phase_a9b_b2s_immediate_host_bridge_receipt.sha256"
)

PARENT_COMMIT = "c2a4fb644c50a45f28ce6f3b040ab4247908adf1"
PARENT_RECEIPT_SHA256 = (
    "28ca392d1126b8e118f261d309a9e00583bf7516ee9b5e6fc7399cf0aaa949d8"
)


class GateError(AssertionError):
    """The frozen B2t static contract was violated."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def strip_comments(text: str) -> str:
    return "\n".join(line.split("!", 1)[0] for line in text.splitlines())


def packed(text: str) -> str:
    return re.sub(r"[\s&]+", "", strip_comments(text)).upper()


def routine(text: str, name: str, kind: str = "subroutine") -> str:
    if kind == "subroutine":
        expression = (
            rf"(?is)\bsubroutine\s+{re.escape(name)}\b.*?"
            rf"\bend\s+subroutine\s+{re.escape(name)}\b"
        )
    elif kind == "logical function":
        expression = (
            rf"(?is)\blogical\s+function\s+{re.escape(name)}\b.*?"
            rf"\bend\s+function\s+{re.escape(name)}\b"
        )
    else:
        raise ValueError(f"unsupported routine kind: {kind}")
    match = re.search(expression, text)
    require(match is not None, f"missing {kind} {name}")
    return match.group(0)


def require_tokens(owner: str, text: str, tokens: tuple[str, ...]) -> None:
    body = packed(text)
    for token in tokens:
        require(packed(token) in body, f"{owner} contract missing: {token}")


def require_order(owner: str, text: str, tokens: tuple[str, ...]) -> None:
    body = packed(text)
    cursor = 0
    for token in tokens:
        needle = packed(token)
        position = body.find(needle, cursor)
        require(position >= 0, f"{owner} order token missing: {token}")
        cursor = position + len(needle)


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def load_source() -> str:
    return SOURCE_PATH.read_text(encoding="utf-8")


def check_manifest(manifest: Mapping[str, Any]) -> None:
    require(manifest.get("phase") == "A9b-B2t", "manifest phase changed")
    require(
        manifest.get("purpose")
        == "own one same-call PROJECTED-to-ASSEMBLED and three-plane frozen-source chain before entering the default-off B2s bridge",
        "manifest purpose changed",
    )
    require(manifest.get("parent_phase") == "A9b-B2s",
            "parent phase changed")
    require(manifest.get("parent_commit") == PARENT_COMMIT,
            "parent commit changed")
    require(manifest.get("parent_receipt_sha256") == PARENT_RECEIPT_SHA256,
            "parent receipt identity changed")
    require(manifest.get("contract_version") == 1,
            "contract version changed")
    require(manifest.get("production_source_changes") == [
        "src/SPOR64_B2T.f90"
    ], "production-source inventory changed")

    api = manifest.get("api", {})
    require(api == {
        "module": "SPOR64_B2T",
        "procedure": "SPOR64_B2T_HOST_STEP",
        "arguments": [
            "ipout", "ipprojected", "ipsystems(3)", "iptrack_file",
            "status", "cutoff_by_plane(3)", "enable(optional)",
        ],
        "disabled_status": 0,
        "failed_status": 1,
        "returned_status": 2,
        "caller_assembled_objects": False,
        "caller_macro0_objects": False,
        "caller_source_objects": False,
        "caller_solved_objects": False,
        "caller_plane": False,
        "caller_rho": False,
        "caller_k": False,
        "caller_epoch": False,
        "caller_tolerance": False,
        "caller_relaxation": False,
    }, "public API contract changed")

    off = manifest.get("default_off", {})
    require(off == {
        "enable_is_optional": True,
        "absent_enable_returns_disabled": True,
        "false_enable_returns_disabled": True,
        "object_accesses_before_return": 0,
        "lcm_operations_before_return": 0,
        "scratch_objects_before_return": 0,
        "production_subcalls_before_return": 0,
        "cutoff_output_when_disabled": [0, 0, 0],
    }, "default-off semantics changed")

    inputs = manifest.get("enabled_input_contract", {})
    require(inputs == {
        "projected": "one committed PROJECTED/1 archive used as the common B2K and B2N parent",
        "systems": "three distinct immutable candidate SYSTEM objects admitted together by B2K",
        "track_file": "one shared external TRACK_f handle forwarded unchanged to B2s; mode and historical identity remain outer-host obligations",
        "output_must_be_fresh_memory_lcm": True,
        "caller_lcm_inputs_are_read_only": True,
        "track_handle_forwarded_unchanged": True,
        "track_os_read_only_mode_verified_by_b2t": False,
        "track_file_identity_verified_by_b2t": False,
        "output_projected_track_pairwise_distinct": True,
        "each_system_distinct_from_output_projected_track": True,
        "systems_pairwise_distinct": True,
    }, "enabled input/alias contract changed")

    chain = manifest.get("owned_chain", {})
    require(chain == {
        "private_assembled_roots": 1,
        "private_macro0_roots": 3,
        "private_source_roots": 3,
        "b2k_calls": 1,
        "b2k_only_success_status": "SPOR64_B2K_ARCHIVE_ASSEMBLED",
        "b2k_output_is_private": True,
        "b2n_calls": 3,
        "b2n_order": [1, 2, 3],
        "b2n_only_success_status": "SPOR64_B2N_COMMITTED",
        "b2n_outputs_are_private_same_call_pairs": True,
        "all_b2n_commits_before_b2s": True,
        "b2s_calls": 1,
        "b2s_enable_argument": True,
        "b2s_only_success_status": "SPOR64_B2S_RETURNED",
        "caller_visible_publication_owner": "B2S/B2R",
        "output_generation": "RETURNED/1",
        "recoverable_failure_cleanup": True,
    }, "owned causal chain changed")

    controls = manifest.get("numerical_controls", {})
    require(controls == {
        "new_empirical_parameters": 0,
        "relaxation_added": False,
        "damping_added": False,
        "clipping_added": False,
        "fitted_coefficient_added": False,
        "model_completion_added": False,
        "automatic_retry_added": False,
    }, "numerical-control scope changed")

    cutoff = manifest.get("cutoff_diagnostic", {})
    require(cutoff == {
        "kind": "INT64",
        "shape": 3,
        "index_owner": "canonical plane label inside B2s",
        "initialized_to_zero": True,
        "aggregated": False,
        "feeds_acceptance": False,
        "feeds_solver": False,
        "written_into_returned_archive": False,
    }, "cutoff diagnostic acquired a physical role")

    provenance = manifest.get("provenance_scope", {})
    require(
        provenance.get("proved")
        == "same-call custody from one PROJECTED parent through one private B2K ASSEMBLED commit and three canonical private B2N source pairs into one B2s invocation",
        "proved provenance scope changed",
    )
    for key in (
        "private_b2n_macro_source_sibling_lineage",
        "private_assembled_and_sources_share_projected_parent",
    ):
        require(provenance.get(key) is True,
                f"owned provenance weakened: {key}")
    for key in (
        "candidate_systems_historically_from_same_call_asm",
        "track_file_historically_matches_archive_track",
        "track_hash_alone_is_historical_identity_proof",
        "filunit_or_link_name_is_file_identity_proof",
        "metadata_alone_is_physical_proof",
    ):
        require(provenance.get(key) is False,
                f"historical provenance overclaim: {key}")

    gate = manifest.get("short_gate_design", {})
    require(gate == {
        "static_mutation_tests": 49,
        "actual_production_abi_compile_only": True,
        "orchestration_stubs_are_control_and_custody_witness_only": True,
        "production_b2n_builds": 3,
        "content_b2k_calls_are_stubs": True,
        "content_b2s_calls_are_capture_stubs": True,
        "content_posterior_runs": 2,
        "projected_and_evidence_read_only_verified": True,
        "real64_qfiss_bit_checks": 15540,
        "real32_dsour_projection_checks": 15540,
        "real32_qint_projection_checks": 1110,
        "positive_zero_nusigf_checks": 284160,
        "unchanged_macro_records_recursive_bitwise": True,
        "real_asm_calls": 0,
        "true_transport_solves": 0,
        "dragon_processes": 0,
        "axial_solves": 0,
        "picard_maps": 0,
        "long_calculations": 0,
    }, "short-gate execution scope changed")

    not_claimed = set(manifest.get("not_claimed", []))
    for claim in (
        "historical same-call host ASM production of the three candidate SYSTEM objects",
        "historical identity of the shared TRACK_f handle and archived TRACK objects",
        "a true radial transport execution by a stub gate",
        "radial convergence",
        "outer Picard convergence",
        "SPOD truncation accuracy",
        "eigenvalue or benchmark accuracy",
        "an enabled outer production host call site",
        "a CLOSED/1 archive",
    ):
        require(claim in not_claimed, f"missing nonclaim: {claim}")


def check_parent_receipt() -> None:
    require(PARENT_RECEIPT_PATH.is_file(), "B2s parent receipt missing")
    digest = hashlib.sha256(PARENT_RECEIPT_PATH.read_bytes()).hexdigest()
    require(digest == PARENT_RECEIPT_SHA256,
            "B2s parent receipt changed")


def check_readme_scope() -> None:
    text = " ".join(README_PATH.read_text(encoding="utf-8").split())
    for required in (
        "returns before the first pointer-association test, LCM query, private object creation, B2k call, B2n call, or B2s call",
        "All three B2n pairs are committed before B2s is entered.",
        "does **not** prove that the three candidate SYSTEM objects were historically produced by same-call host `ASM`",
        "does **not** prove that the supplied `TRACK_f` handle names the binary tracking file historically associated with the archived TRACK objects",
        "it does not prove historical TRACK identity by itself",
        "executes production B2n exactly three times from the same frozen PROJECTED parent",
        "Neither gate is a true radial transport execution.",
    ):
        require(required in text, f"README scope changed: {required}")


def check_source(text: str) -> None:
    whole = packed(text)
    step_text = routine(text, "SPOR64_B2T_HOST_STEP")
    step = packed(step_text)
    open_text = routine(text, "OPEN_PRIVATE")
    close_text = routine(text, "CLOSE_PRIVATE")
    empty_text = routine(text, "EMPTY_LCM_ROOT", "logical function")

    require(re.search(r"(?im)^\s*module\s+SPOR64_B2T\s*$",
                      strip_comments(text)) is not None,
            "B2t module name changed")
    require("PUBLIC::SPOR64_B2T_HOST_STEP" in whole,
            "owned host step is not public")
    require_tokens("B2t imported owners", text, (
        "use SPOR64_B2K, only : SPOR64_B2K_ARCHIVE_ASSEMBLED, SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE",
        "use SPOR64_B2N, only : SPOR64_B2N_COMMITTED, SPOR64_B2N_BUILD",
        "use SPOR64_B2S, only : SPOR64_B2S_RETURNED, SPOR64_B2S_HOST_BRIDGE",
    ))
    require("SPOR64_B2T_DISABLED=0" in whole, "disabled status changed")
    require("SPOR64_B2T_FAILED=1" in whole, "failed status changed")
    require("SPOR64_B2T_RETURNED=2" in whole, "returned status changed")
    require("NSNAP=3" in whole, "plane count changed")

    signature = step.split(")", 1)[0]
    require(
        signature
        == "SUBROUTINESPOR64_B2T_HOST_STEP(IPOUT,IPPROJECTED,IPSYSTEMS,IPTRACK_FILE,STATUS,CUTOFF_BY_PLANE,ENABLE",
        "owned-host-step ABI changed",
    )
    for forbidden_argument in (
        "IPASSEMBLED", "IPMACROS", "IPSOURCES", "IPSOLVED", "PLANE_INDEX",
        "RHO", "KEFF", "EPOCH", "TOLERANCE", "RELAXATION",
    ):
        require(forbidden_argument not in signature,
                f"forbidden loose/external ABI input: {forbidden_argument}")
    require_tokens("B2t ABI", step_text, (
        "type(c_ptr), intent(in) :: ipout, ipprojected",
        "type(c_ptr), intent(in) :: ipsystems(NSNAP), iptrack_file",
        "integer, intent(out) :: status",
        "integer(int64), intent(out) :: cutoff_by_plane(NSNAP)",
        "logical, intent(in), optional :: enable",
    ))

    require_order("B2t default-off prefix", step_text, (
        "status = SPOR64_B2T_DISABLED",
        "cutoff_by_plane = 0_int64",
        "if (.not. present(enable)) return",
        "if (.not. enable) return",
        "status = SPOR64_B2T_FAILED",
    ))
    enabled_at = step.index("STATUS=SPOR64_B2T_FAILED")
    disabled_prefix = step[:enabled_at]
    for forbidden in (
        "C_ASSOCIATED(", "LCM", "CALL", "OPEN_PRIVATE(",
        "EMPTY_LCM_ROOT(", "SPOR64_B2K_", "SPOR64_B2N_", "SPOR64_B2S_",
    ):
        require(forbidden not in disabled_prefix,
                f"default-off path acquired access/subcall: {forbidden}")

    require_tokens("B2t enabled association preflight", step_text, (
        "if (.not. c_associated(ipout)) return",
        "if (.not. c_associated(ipprojected)) return",
        "if (.not. c_associated(iptrack_file)) return",
        "if (c_associated(ipout,ipprojected)) return",
        "if (c_associated(ipout,iptrack_file)) return",
        "if (c_associated(ipprojected,iptrack_file)) return",
        "if (.not. c_associated(ipsystems(plane))) return",
        "if (c_associated(ipout,ipsystems(plane))) return",
        "if (c_associated(ipprojected,ipsystems(plane))) return",
        "if (c_associated(iptrack_file,ipsystems(plane))) return",
        "if (c_associated(ipsystems(plane),ipsystems(other))) return",
        "if (.not. EMPTY_LCM_ROOT(ipout)) return",
    ))
    require_tokens("B2t alias-loop bounds", step_text, (
        "do plane = 1, NSNAP",
        "do plane = 1, NSNAP-1",
        "do other = plane+1, NSNAP",
    ))

    require_order("B2t freshness-before-scratch", step_text, (
        "if (.not. EMPTY_LCM_ROOT(ipout)) return",
        "assembled = c_null_ptr",
        "macros = c_null_ptr",
        "sources = c_null_ptr",
        "call OPEN_PRIVATE(assembled,'B2T-ASMB',0)",
        "call OPEN_PRIVATE(macros(plane),'B2T-MAC',plane)",
        "call OPEN_PRIVATE(sources(plane),'B2T-SRC',plane)",
    ))
    require(step.count("CALLOPEN_PRIVATE(") == 3,
            "private scratch call-site inventory changed")
    require(
        "DOPLANE=1,NSNAP"
        "CALLOPEN_PRIVATE(MACROS(PLANE),'B2T-MAC',PLANE)"
        "CALLOPEN_PRIVATE(SOURCES(PLANE),'B2T-SRC',PLANE)ENDDO" in step,
        "three-plane private source-pair creation loop changed",
    )
    require_tokens("B2t private creation helper", open_text, (
        "call LCMOP(stage,name,0,1,0)",
        "if (.not. c_associated(stage)) call XABORT",
    ))

    b2k_call = (
        "CALLSPOR64_B2K_COMMIT_SYSTEM_ARCHIVE(ASSEMBLED,IPPROJECTED,"
        "IPSYSTEMS,ASSEMBLE_STATUS)"
    )
    b2n_call = (
        "CALLSPOR64_B2N_BUILD(IPPROJECTED,PLANE,MACROS(PLANE),"
        "SOURCES(PLANE),SOURCE_STATUS)"
    )
    b2s_call = (
        "CALLSPOR64_B2S_HOST_BRIDGE(IPOUT,ASSEMBLED,MACROS,SOURCES,"
        "IPTRACK_FILE,BRIDGE_STATUS,CUTOFF_BY_PLANE,.TRUE.)"
    )
    require(step.count("CALLSPOR64_B2K_COMMIT_SYSTEM_ARCHIVE(") == 1,
            "B2K call-site count changed")
    require(step.count("CALLSPOR64_B2N_BUILD(") == 1,
            "B2N must have one call site inside its canonical loop")
    require(step.count("CALLSPOR64_B2S_HOST_BRIDGE(") == 1,
            "B2S call-site count changed")
    require(b2k_call in step, "private B2K tuple changed")
    require(b2n_call in step, "private canonical B2N tuple changed")
    require(b2s_call in step, "private B2S tuple or explicit .true. changed")

    b2k_at = step.index(b2k_call)
    b2n_at = step.index(b2n_call)
    b2s_at = step.index(b2s_call)
    require(b2k_at < b2n_at < b2s_at,
            "B2K -> B2N -> B2S causal order changed")
    require(
        "DOPLANE=1,NSNAP" + b2n_call in step[b2k_at:b2s_at],
        "B2N is not called in canonical p=1,2,3 order",
    )
    require_tokens("B2t strict statuses", step_text, (
        "if (assemble_status /= SPOR64_B2K_ARCHIVE_ASSEMBLED) then",
        "if (source_status /= SPOR64_B2N_COMMITTED) then",
        "if (bridge_status == SPOR64_B2S_RETURNED) status = SPOR64_B2T_RETURNED",
    ))
    require_order("B2t complete-before-consume", step_text, (
        "call SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE",
        "assemble_status /= SPOR64_B2K_ARCHIVE_ASSEMBLED",
        "call SPOR64_B2N_BUILD",
        "source_status /= SPOR64_B2N_COMMITTED",
        "end do",
        "call SPOR64_B2S_HOST_BRIDGE",
        "bridge_status == SPOR64_B2S_RETURNED",
    ))

    require(step.count("CALLCLOSE_PRIVATE(") == 3,
            "recoverable cleanup call-site inventory changed")
    require(step.rfind("CALLCLOSE_PRIVATE(") > b2s_at,
            "final cleanup no longer follows B2S")
    require_tokens("B2t private cleanup helper", close_text, (
        "do plane = 1, NSNAP",
        "if (c_associated(sources(plane))) call LCMCL(sources(plane),2)",
        "if (c_associated(macros(plane))) call LCMCL(macros(plane),2)",
        "sources(plane) = c_null_ptr",
        "macros(plane) = c_null_ptr",
        "if (c_associated(assembled)) call LCMCL(assembled,2)",
        "assembled = c_null_ptr",
    ))
    require_order("B2t B2K-failure cleanup", step_text, (
        "assemble_status /= SPOR64_B2K_ARCHIVE_ASSEMBLED",
        "call CLOSE_PRIVATE(assembled,macros,sources)",
        "return",
    ))
    b2n_failure = step_text[step_text.upper().find(
        "IF (SOURCE_STATUS /= SPOR64_B2N_COMMITTED)"
    ):]
    require_order("B2t B2N-failure cleanup", b2n_failure, (
        "source_status /= SPOR64_B2N_COMMITTED",
        "call CLOSE_PRIVATE(assembled,macros,sources)",
        "return",
    ))

    require(step.count("CUTOFF_BY_PLANE") == 4,
            "cutoff diagnostic use inventory changed")
    for forbidden in (
        "IF(CUTOFF_BY_PLANE", "SUM(CUTOFF_BY_PLANE",
        "MAXVAL(CUTOFF_BY_PLANE", "MINVAL(CUTOFF_BY_PLANE",
        "CUTOFF_BY_PLANE=",  # exact initialization is admitted below
    ):
        if forbidden == "CUTOFF_BY_PLANE=":
            require(step.count(forbidden) == 1 and
                    "CUTOFF_BY_PLANE=0_INT64" in step,
                    "cutoff acquired a nonzero or repeated assignment")
        else:
            require(forbidden not in step,
                    f"cutoff acquired acceptance/aggregate role: {forbidden}")

    for mutator in (
        "LCMPUT(", "LCMPTC(", "LCMPDL(", "LCMDEL(",
        "LCMDID(", "LCMLID(", "LCMEQU(",
    ):
        require(mutator not in whole,
                f"B2t acquired direct data mutation/publication: {mutator}")
        require(mutator not in packed(empty_text),
                f"freshness helper acquired mutation: {mutator}")

    for forbidden in (
        "SPOR64_B2O", "SPOR64_B2B", "SPOR64_B2R",
        "FLU2DR64_CORE", "XDRTA2", "CALLASM(", "CALLFLU(",
        "CALLSPOASM(", "CALLSPOSTATE(", "CALLSPOLEAK(",
        "ALPHA=", "RELAX", "DAMP", "CLIP", "FITTED",
        "MODEL_COMPLETION", "AUTOMATIC_RETRY",
    ):
        require(forbidden not in whole,
                f"B2t acquired forbidden direct model/solver token: {forbidden}")


def check_all(source: str, manifest: Mapping[str, Any]) -> None:
    check_manifest(manifest)
    check_parent_receipt()
    check_readme_scope()
    check_source(source)


def main() -> None:
    source = load_source()
    manifest = load_manifest()
    check_all(source, manifest)
    print("B2T STATIC OWNED-SOURCE-HOST-STEP PASS")
    print("B2T DEFAULT=OFF OBJECT-ACCESS=0 SCRATCH=0 SUBCALLS=0")
    print("B2T ON=B2K(1)->B2N(1,2,3)->B2S(.TRUE.)(1)")
    print("B2T CALLER-MACRO/SOURCE/SOLVED/ASSEMBLED=FORBIDDEN")
    print("B2T CUTOFF=INT64-PER-PLANE-DIAGNOSTIC-ONLY")
    print("B2T ASM-LINEAGE/TRACK-FILE-IDENTITY/TRANSPORT=NOT-PROVED")


if __name__ == "__main__":
    main()
