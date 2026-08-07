#!/usr/bin/env python3
"""Independent static audit for the B2s default-off host bridge."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_PATH = ROOT / "src/SPOR64_B2S.f90"
MANIFEST_PATH = HERE / "precision_manifest.json"
README_PATH = HERE / "README.md"
PARENT_RECEIPT_PATH = (
    ROOT
    / "validation/iterative/real64_phase_a9b_b2r_returned_archive"
    / "phase_a9b_b2r_returned_archive_receipt.sha256"
)

PARENT_COMMIT = "7d40c0ef71e136a6c424a29b67dd58011b10f3f7"
PARENT_RECEIPT_SHA256 = (
    "8970a7c383259a6f71cda2489ce64a7983ae867c5fc56ddc8a2abd01d58eb394"
)


class GateError(AssertionError):
    """The frozen B2s contract was violated."""


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
        expression = (
            rf"(?is)\binteger\s+function\s+{re.escape(name)}\b.*?"
            rf"\bend\s+function\s+{re.escape(name)}\b"
        )
    match = re.search(expression, text)
    require(match is not None, f"missing {kind} {name}")
    return match.group(0)


def require_tokens(owner: str, text: str, tokens: tuple[str, ...]) -> None:
    body = packed(text)
    for token in tokens:
        require(packed(token) in body, f"{owner} contract missing: {token}")


def require_order(owner: str, text: str, tokens: tuple[str, ...]) -> None:
    body = packed(text)
    positions: list[int] = []
    cursor = 0
    for token in tokens:
        needle = packed(token)
        position = body.find(needle, cursor)
        require(position >= 0, f"{owner} order token missing: {token}")
        positions.append(position)
        cursor = position + len(needle)
    require(positions == sorted(positions), f"{owner} order changed")


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def load_source() -> str:
    return SOURCE_PATH.read_text(encoding="utf-8")


def check_manifest(manifest: Mapping[str, Any]) -> None:
    require(manifest.get("phase") == "A9b-B2s", "manifest phase changed")
    require(
        manifest.get("purpose")
        == "provide one explicitly enabled immediate in-process B2O-to-B2B-to-B2R bridge while leaving the production route default-off",
        "manifest purpose changed",
    )
    require(manifest.get("parent_phase") == "A9b-B2r",
            "parent phase changed")
    require(manifest.get("parent_commit") == PARENT_COMMIT,
            "parent commit changed")
    require(manifest.get("parent_receipt_sha256") == PARENT_RECEIPT_SHA256,
            "parent receipt identity changed")
    require(manifest.get("contract_version") == 1,
            "contract version changed")
    require(manifest.get("production_source_changes") == [
        "src/SPOR64_B2S.f90"
    ], "production-source inventory changed")

    api = manifest.get("api", {})
    require(api == {
        "module": "SPOR64_B2S",
        "procedure": "SPOR64_B2S_HOST_BRIDGE",
        "arguments": [
            "ipout", "ipassembled", "ipmacros(3)", "ipsources(3)",
            "iptrack_file", "status", "cutoff_by_plane(3)",
            "enable(optional)",
        ],
        "disabled_status": 0,
        "failed_status": 1,
        "returned_status": 2,
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
    require(inputs.get("assembled") ==
            "one committed ASSEMBLED/1 archive",
            "ASSEMBLED input boundary changed")
    require(inputs.get("macro0") ==
            "three caller-supplied detached MACRO0 objects carried in the same argument slots as the three sources; read-only sharing between MACRO0 slots is permitted",
            "MACRO0 input boundary changed")
    require(inputs.get("qsource") ==
            "three distinct detached FROZEN-QFIS/1 objects whose source-owned labels form exactly {1,2,3}",
            "source input boundary changed")
    require(inputs.get("track_file") ==
            "one shared TRACK_f handle used by all three canonical plane calls",
            "TRACK_f input boundary changed")
    for key in (
        "same_slot_macro_source_pairing", "output_must_be_fresh",
        "all_caller_objects_immutable",
    ):
        require(inputs.get(key) is True, f"input contract changed: {key}")
    require(inputs.get("source_plane_labels") == [1, 2, 3],
            "source plane-label set changed")

    chain = manifest.get("causal_chain", {})
    require(chain == {
        "b2o_calls": 3,
        "all_b2o_calls_before_first_b2b": True,
        "sealed_plane_set": [1, 2, 3],
        "sealed_plane_duplicates_or_omissions_rejected": True,
        "b2b_calls": 3,
        "b2b_mode": "CONT",
        "b2b_order": [1, 2, 3],
        "b2b_only_success_status": "SPOR64_B2C_HOST_COMMITTED",
        "solved_objects_are_private_immediate_b2b_outputs": True,
        "b2r_calls": 1,
        "b2r_after_all_three_host_commits": True,
        "output_generation": "RETURNED/1",
    }, "immediate causal chain changed")

    controls = manifest.get("numerical_controls", {})
    require(controls == {
        "preexisting_b2b_controls_are_frozen_in_bridge": True,
        "new_empirical_parameters": 0,
        "relaxation_added": False,
        "damping_added": False,
        "clipping_added": False,
        "fitted_coefficient_added": False,
        "model_completion_added": False,
    }, "numerical-control scope changed")

    cutoff = manifest.get("cutoff_diagnostic", {})
    require(cutoff == {
        "kind": "INT64",
        "shape": 3,
        "index_owner": "canonical plane label",
        "initialized_to_zero": True,
        "aggregated": False,
        "feeds_acceptance": False,
        "feeds_solver": False,
        "written_into_returned_archive": False,
    }, "cutoff diagnostic acquired a physical role")

    provenance = manifest.get("provenance_scope", {})
    require(provenance.get("proved") ==
            "same-call causal custody from each B2O-sealed pair through the matching accepted B2B CONT result into the single B2R collection",
            "proved provenance scope changed")
    require(provenance.get("macro0_and_source_follow_same_argument_slot")
            is True, "same-slot custody changed")
    for key in (
        "macro0_historically_derived_from_archive_microlib2",
        "macro0_and_source_historical_sibling_lineage",
        "track_file_historically_matches_archive_track",
        "metadata_alone_is_physical_proof",
    ):
        require(provenance.get(key) is False,
                f"historical provenance overclaim: {key}")

    gate = manifest.get("short_gate_design", {})
    require(gate == {
        "static_mutation_tests": 45,
        "production_b2o_b2b_b2r_path": True,
        "production_a9_implementation_linked": False,
        "stub_core_is_a_publication_witness_only": True,
        "true_transport_solves": 0,
        "dragon_processes": 0,
        "axial_solves": 0,
        "picard_maps": 0,
        "long_calculations": 0,
    }, "short-gate execution scope changed")

    not_claimed = set(manifest.get("not_claimed", []))
    for claim in (
        "historical MACRO0 derivation from the same-index ASSEMBLED/MICROLIB2 payload",
        "historical sibling lineage of detached MACRO0 and FROZEN-QFIS objects",
        "historical identity of the shared TRACK_f handle and archived TRACK objects",
        "a true radial transport execution in the short gate",
        "radial convergence", "outer Picard convergence",
        "benchmark accuracy", "an enabled production host call site",
        "a CLOSED/1 archive",
    ):
        require(claim in not_claimed, f"missing nonclaim: {claim}")


def check_parent_receipt() -> None:
    require(PARENT_RECEIPT_PATH.is_file(), "B2r parent receipt missing")
    digest = hashlib.sha256(PARENT_RECEIPT_PATH.read_bytes()).hexdigest()
    require(digest == PARENT_RECEIPT_SHA256,
            "B2r parent receipt changed")


def check_readme_scope() -> None:
    text = " ".join(README_PATH.read_text(encoding="utf-8").split())
    for required in (
        "before the first object association test, LCM query, scratch-object creation, or B2O/B2B/B2R call",
        "All three B2O calls and the complete label-set check occur before the first B2B call.",
        "Current object schemas do not encode a receipt proving",
        "Same-slot use is an explicit host contract, not a reconstructed history claim.",
        "it is not a true radial transport solve",
    ):
        require(required in text, f"README scope changed: {required}")


def check_source(text: str) -> None:
    whole = packed(text)
    bridge_text = routine(text, "SPOR64_B2S_HOST_BRIDGE")
    bridge = packed(bridge_text)
    plane_reader = routine(text, "READ_SEALED_PLANE", "logical function")
    storage_reader = routine(text, "LCM_STORAGE_KIND", "integer function")
    empty_reader = routine(text, "EMPTY_LCM_ROOT", "logical function")
    record_reader = routine(text, "RECORD_MATCHES", "logical function")
    list_reader = routine(text, "LIST_ITEM_IS_DIRECTORY", "logical function")

    require(re.search(r"(?im)^\s*module\s+SPOR64_B2S\s*$",
                      strip_comments(text)) is not None,
            "B2s module name changed")
    require("PUBLIC::SPOR64_B2S_HOST_BRIDGE" in whole,
            "host bridge is not public")
    require_tokens("B2s imported owners", text, (
        "use SPOR64_B2B, only : SPOR64_B2B_CONT, SPOR64_B2B_INGRESS",
        "use SPOR64_B2C, only : SPOR64_B2C_HOST_COMMITTED",
        "use SPOR64_B2O, only : SPOR64_B2O_SEALED, SPOR64_B2O_SEAL_CONT_PAIR",
        "use SPOR64_B2R, only : SPOR64_B2R_RETURNED, SPOR64_B2R_COLLECT",
    ))
    require("SPOR64_B2S_DISABLED=0" in whole, "disabled status changed")
    require("SPOR64_B2S_FAILED=1" in whole, "failed status changed")
    require("SPOR64_B2S_RETURNED=2" in whole, "returned status changed")
    require("NSNAP=3" in whole and "NENTRY=7" in whole,
            "bridge dimensions changed")
    require("NGRP=370" in whole and "NREG=8" in whole and
            "NMAT=8" in whole and "NIFIS=32" in whole,
            "frozen B2B dimensions changed")
    require("FROZEN_TOL_BITS=INT(Z'348637BD',INT32)" in whole,
            "inherited numerical tolerance bits changed")

    signature = bridge.split(")", 1)[0]
    require(signature ==
            "SUBROUTINESPOR64_B2S_HOST_BRIDGE(IPOUT,IPASSEMBLED,IPMACROS,IPSOURCES,IPTRACK_FILE,STATUS,CUTOFF_BY_PLANE,ENABLE",
            "host-bridge ABI changed")
    require("IPSOLVED" not in signature,
            "caller-supplied SOLVED object entered the ABI")
    require_tokens("B2s ABI", bridge_text, (
        "type(c_ptr), intent(in) :: ipout, ipassembled",
        "type(c_ptr), intent(in) :: ipmacros(NSNAP), ipsources(NSNAP)",
        "type(c_ptr), intent(in) :: iptrack_file",
        "integer, intent(out) :: status",
        "integer(int64), intent(out) :: cutoff_by_plane(NSNAP)",
        "logical, intent(in), optional :: enable",
    ))

    require_order("B2s default-off prefix", bridge_text, (
        "status = SPOR64_B2S_DISABLED",
        "cutoff_by_plane = 0_int64",
        "if (.not. present(enable)) return",
        "if (.not. enable) return",
        "status = SPOR64_B2S_FAILED",
    ))
    enabled_at = bridge.index("STATUS=SPOR64_B2S_FAILED")
    disabled_prefix = bridge[:enabled_at]
    for forbidden in (
        "C_ASSOCIATED(", "LCM", "CALL", "OPEN_PRIVATE(",
        "EMPTY_LCM_ROOT(", "RECORD_MATCHES(",
        "SPOR64_B2O_", "SPOR64_B2B_", "SPOR64_B2R_",
    ):
        require(forbidden not in disabled_prefix,
                f"default-off path acquired access/subcall: {forbidden}")

    require_tokens("B2s enabled preflight", bridge_text, (
        "if (.not. c_associated(ipout)) return",
        "if (.not. c_associated(ipassembled)) return",
        "if (.not. c_associated(iptrack_file)) return",
        "if (c_associated(ipout,ipassembled)) return",
        "if (.not. c_associated(ipmacros(slot))) return",
        "if (.not. c_associated(ipsources(slot))) return",
        "if (c_associated(ipout,ipmacros(slot))) return",
        "if (c_associated(ipout,ipsources(slot))) return",
        "if (c_associated(ipassembled,ipmacros(slot))) return",
        "if (c_associated(ipassembled,ipsources(slot))) return",
        "if (c_associated(ipsources(slot),ipsources(plane))) return",
        "if (c_associated(ipmacros(slot),ipsources(plane))) return",
        "if (.not. EMPTY_LCM_ROOT(ipout)) return",
    ))
    require_order("B2s scratch boundary", bridge_text, (
        "if (.not. EMPTY_LCM_ROOT(ipout)) return",
        "sealed_seed = c_null_ptr",
        "call OPEN_PRIVATE(sealed_seed(slot),'B2S-SEED',slot)",
        "call OPEN_PRIVATE(sealed_system(slot),'B2S-SYS',slot)",
        "call OPEN_PRIVATE(solved_by_plane(slot),'B2S-SOLV',slot)",
        "call SPOR64_B2O_SEAL_CONT_PAIR",
    ))
    require(bridge.count("CALLOPEN_PRIVATE(") == 3,
            "private scratch inventory changed")
    require(bridge.count("CALLCLOSE_PRIVATE(") == 10,
            "private cleanup coverage changed")

    require(bridge.count("CALLSPOR64_B2O_SEAL_CONT_PAIR(") == 1,
            "B2O must have one syntactic call site inside its three-slot loop")
    require_tokens("B2s all-seal-first binding", bridge_text, (
        "do slot = 1, NSNAP",
        "call SPOR64_B2O_SEAL_CONT_PAIR(ipassembled,ipsources(slot), sealed_seed(slot),sealed_system(slot),seal_status)",
        "if (seal_status /= SPOR64_B2O_SEALED) then",
        "READ_SEALED_PLANE(sealed_seed(slot),source_plane(slot))",
        "plane = source_plane(slot)",
        "if (slot_for_plane(plane) /= 0) then",
        "slot_for_plane(plane) = slot",
        "if (any(slot_for_plane == 0)) then",
    ))
    require_tokens("B2s sealed-plane reader", plane_reader, (
        "RECORD_MATCHES(seed,'SPOT-R64',-1,0)",
        "authority = LCMGID(seed,'SPOT-R64')",
        "RECORD_MATCHES(authority,'PLANE',1,1)",
        "call LCMGET(authority,'PLANE',plane)",
        "if (plane < 1 .or. plane > NSNAP) return",
        "READ_SEALED_PLANE = .true.",
    ))

    require_tokens("B2s archive TRACK selection", bridge_text, (
        "RECORD_MATCHES(ipassembled,'TRACK',NSNAP,10)",
        "tracks = LCMGID(ipassembled,'TRACK')",
        "LIST_ITEM_IS_DIRECTORY(tracks,plane)",
        "track = LCMGIL(tracks,plane)",
    ))
    require_tokens("B2s canonical same-slot B2B tuple", bridge_text, (
        "do plane = 1, NSNAP",
        "slot = slot_for_plane(plane)",
        "ientry = [1,LCM_STORAGE_KIND(ipmacros(slot)), LCM_STORAGE_KIND(track),3,1,LCM_STORAGE_KIND(ipsources(slot)),1]",
        "kentry = [solved_by_plane(plane),ipmacros(slot),track, iptrack_file,sealed_system(slot),ipsources(slot),sealed_seed(slot)]",
        "jentry = [0,2,2,2,2,2,2]",
        "imerg = 1",
    ))
    expected_b2b = (
        "CALLSPOR64_B2B_INGRESS(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY,"
        "0,500,740,FROZEN_TOL32,FROZEN_TOL32,FROZEN_TOL32,1,3,3,"
        "'B0',0,1,1,IMERG,0,.FALSE.,0,.TRUE.,NGRP,NREG,NMAT,"
        "NIFIS,1,2,1,.FALSE.,.TRUE.,SPOR64_B2B_CONT,RADIAL_STATUS,"
        "CUTOFF_BY_PLANE(PLANE))"
    )
    require(expected_b2b in bridge, "frozen canonical B2B call changed")
    require(bridge.count("CALLSPOR64_B2B_INGRESS(") == 1,
            "B2B must have one syntactic call site inside its plane loop")
    require(bridge.count("RADIAL_STATUS/=SPOR64_B2C_HOST_COMMITTED") == 1,
            "B2B success is not exactly HOST_COMMITTED")

    require(bridge.count("CALLSPOR64_B2R_COLLECT(") == 1,
            "B2R must be called exactly once")
    require_tokens("B2s immediate collection", bridge_text, (
        "call SPOR64_B2R_COLLECT(ipout,ipassembled,solved_by_plane, ipsources,collect_status)",
        "if (collect_status == SPOR64_B2R_RETURNED) status = SPOR64_B2S_RETURNED",
    ))
    require_order("B2s causal execution", bridge_text, (
        "call SPOR64_B2O_SEAL_CONT_PAIR",
        "if (any(slot_for_plane == 0)) then",
        "do plane = 1, NSNAP",
        "call SPOR64_B2B_INGRESS",
        "if (radial_status /= SPOR64_B2C_HOST_COMMITTED) then",
        "call SPOR64_B2R_COLLECT",
        "status = SPOR64_B2S_RETURNED",
        "call CLOSE_PRIVATE(sealed_seed,sealed_system,solved_by_plane)",
    ))

    require(bridge.count("CUTOFF_BY_PLANE") == 4,
            "cutoff diagnostic use inventory changed")
    require("CUTOFF_BY_PLANE(PLANE)" in bridge,
            "cutoff is not indexed by canonical plane")
    for forbidden in (
        "IF(CUTOFF_BY_PLANE", "SUM(CUTOFF_BY_PLANE",
        "MAXVAL(CUTOFF_BY_PLANE", "MINVAL(CUTOFF_BY_PLANE",
    ):
        require(forbidden not in bridge,
                f"cutoff diagnostic acquired an acceptance/aggregate role: {forbidden}")

    for owner, helper in (
        ("storage-kind reader", storage_reader),
        ("fresh-output reader", empty_reader),
        ("record reader", record_reader),
        ("list-item reader", list_reader),
    ):
        helper_body = packed(helper)
        for mutator in ("LCMPUT(", "LCMPTC(", "LCMPDL(", "LCMDEL(",
                        "LCMDID(", "LCMLID(", "LCMEQU("):
            require(mutator not in helper_body,
                    f"{owner} acquired caller-visible mutation: {mutator}")
    for mutator in ("LCMPUT(", "LCMPTC(", "LCMPDL(", "LCMDEL(",
                    "LCMDID(", "LCMLID(", "LCMEQU("):
        require(mutator not in whole,
                f"B2s acquired direct publication outside B2R: {mutator}")

    for forbidden in (
        "FLU2DR64_CORE", "XDRTA2", "CALLSPOASM", "CALLASM",
        "CALLFLU", "CALLSPOMOC", "CALLSPOSTATE", "CALLSPOLEAK",
        "PICARD", "ALPHA=", "RELAX", "DAMP", "CLIP", "FITTED",
        "MODEL_COMPLETION",
    ):
        require(forbidden not in whole,
                f"bridge acquired forbidden direct model/solver token: {forbidden}")


def check_all(source: str, manifest: Mapping[str, Any]) -> None:
    check_manifest(manifest)
    check_parent_receipt()
    check_readme_scope()
    check_source(source)


def main() -> None:
    source = load_source()
    manifest = load_manifest()
    check_all(source, manifest)
    print("B2S STATIC IMMEDIATE-HOST-BRIDGE PASS")
    print("B2S DEFAULT=OFF OBJECT-ACCESS=0 SCRATCH=0 SUBCALLS=0")
    print("B2S ON=B2O(3)->B2B-CONT/HOST_COMMITTED(3)->B2R(1)")
    print("B2S CALLER-SOLVED=FORBIDDEN LOOSE-PHYSICS-CONTROLS=0")
    print("B2S CUTOFF=INT64-PER-PLANE-DIAGNOSTIC-ONLY")
    print("B2S TRUE-TRANSPORT/CONVERGENCE=NOT-CLAIMED")


if __name__ == "__main__":
    main()
