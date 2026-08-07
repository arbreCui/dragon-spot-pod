#!/usr/bin/env python3
"""Independent static contract audit for the B2r returned archive."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MANIFEST_PATH = HERE / "precision_manifest.json"
README_PATH = HERE / "README.md"
SOURCE_PATH = ROOT / "src/SPOR64_B2R.f90"
PARENT_RECEIPT_PATH = (
    ROOT
    / "validation/iterative/real64_phase_a9b_b2q_lifecycle_rho_contract"
    / "phase_a9b_b2q_lifecycle_rho_contract_receipt.sha256"
)

PARENT_COMMIT = "69adf38dba7b67698ac0f83f6286f729695d72d1"
PARENT_RECEIPT_SHA256 = (
    "85dba806828efd557869b78b248feabaa5c11828d8e4afdd3f3a2cb8df739287"
)


class GateError(AssertionError):
    """The frozen B2r contract was violated."""


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
    else:
        expression = (
            rf"(?is)\blogical\s+function\s+{re.escape(name)}\b.*?"
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
    for token in tokens:
        needle = packed(token)
        require(needle in body, f"{owner} order token missing: {token}")
        positions.append(body.index(needle))
    require(positions == sorted(positions), f"{owner} order changed")


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def load_source() -> str:
    return SOURCE_PATH.read_text(encoding="utf-8")


def check_manifest(manifest: Mapping[str, Any]) -> None:
    require(manifest.get("phase") == "A9b-B2r", "manifest phase changed")
    require(manifest.get("purpose") ==
            "collect three supplied committed detached SOLVED/1 radial-state objects into one unclosed RETURNED/1 archive containing the complete SPOASM payload",
            "manifest purpose or provenance scope changed")
    require(manifest.get("parent_commit") == PARENT_COMMIT,
            "parent commit changed")
    require(manifest.get("parent_receipt_sha256") ==
            PARENT_RECEIPT_SHA256, "parent receipt identity changed")
    require(manifest.get("contract_version") == 1,
            "contract version changed")
    require(manifest.get("production_source_changes") == [
        "src/SPOR64_B2R.f90",
    ], "production-source inventory changed")
    require(manifest.get("empirical_controls_added") is False,
            "manifest permits empirical controls")

    api = manifest.get("api", {})
    require(api == {
        "module": "SPOR64_B2R",
        "procedure": "SPOR64_B2R_COLLECT",
        "arguments": [
            "ipout", "ipassembled", "ipsolved(3)", "ipsources(3)",
            "status",
        ],
        "preflight_status": 1,
        "returned_status": 2,
        "loose_plane_rho_k_epoch_arguments": False,
    }, "public API contract changed")

    inputs = manifest.get("input_contract", {})
    require(inputs.get("solved_plane_labels") == [1, 2, 3],
            "SOLVED plane-label set changed")
    require(inputs.get("qsource_plane_labels") == [1, 2, 3],
            "QFISS-source plane-label set changed")
    for key in (
        "bind_by_label_not_argument_order", "reject_duplicates",
        "reject_omissions", "output_must_be_fresh",
        "all_inputs_immutable",
    ):
        require(inputs.get(key) is True, f"input contract changed: {key}")
    require(inputs.get("assembled") ==
            "one committed ASSEMBLED/1 archive with exact root and authority inventories, validated same-index fields, and recursively copied TRACK, MICROLIB2 and SYSTEM payloads",
            "ASSEMBLED input owner changed")
    require(inputs.get("solved") ==
            "three distinct exact detached SOLVED/1 roots",
            "SOLVED input contract changed")
    require(inputs.get("qsource") ==
            "three distinct exact detached FROZEN-QFIS/1 roots",
            "QFISS-source input contract changed")

    binding = manifest.get("same_index_binding", {})
    require(binding.get("system_plane_owner") == "SYSTEM/SPOT-L1-SNAP",
            "SYSTEM plane owner changed")
    require(binding.get("archive_plane_owner") ==
            "one-based archive list index", "archive plane owner changed")
    require(binding.get("solved_detached_plane_owner") ==
            "SOLVED/SPOT-R64/PLANE", "SOLVED plane owner changed")
    require(binding.get("qsource_detached_plane_owner") ==
            "FROZEN-QFIS/SPOT-R64/PLANE",
            "QFISS-source plane owner changed")
    require("binary64 bit-identical" in binding.get("rho", ""),
            "RHO bit-identity changed")
    require(binding.get("epoch") ==
            "ASSEMBLED root, SYSTEM, SOLVED and QFISS-source EPOCH are exactly 1",
            "epoch binding changed")
    require("binary32 bit-identical" in binding.get("leakage", ""),
            "leakage bit-identity changed")
    require("integer-identical" in binding.get("keyflx", ""),
            "KEYFLX identity changed")
    require(binding.get("k") ==
            "source SPOT-KEFF is binary32 bit-identical to real(ASSEMBLED/SPOT-ITER-K,real32)",
            "source-K binding changed")
    require(binding.get("qfiss") ==
            "source SPOT-R64/QFISS is the binary64 authority and source DSOUR is its one-time binary32 mirror",
            "QFISS precision ownership changed")
    require(binding.get("track_microlib_system_copy") ==
            "recursive exact copy from the single ASSEMBLED archive",
            "archive tuple-copy contract changed")

    output = manifest.get("output_contract", {})
    require(output.get("root_inventory") == [
        "SIGNATURE", "LISTDIM", "TRACK", "MICROLIB2", "SYSTEM",
        "FLUX", "SPOT-R64",
    ], "RETURNED root inventory changed")
    require(output.get("root_signature") == "L_ARCHIVE",
            "RETURNED root signature changed")
    require(output.get("root_listdim") == 3,
            "RETURNED root plane count changed")
    require(output.get("root_authority_inventory") == [
        "NPLANE", "STATE", "EPOCH",
    ], "RETURNED authority inventory changed")
    require(output.get("root_state") == "RETURNED",
            "RETURNED state changed")
    require(output.get("root_epoch") == 1,
            "RETURNED epoch changed")
    require(output.get("root_has_rho") is False,
            "RETURNED root acquired RHO")
    require(output.get("root_has_spot_iter_k") is False,
            "RETURNED root acquired SPOT-ITER-K")
    require(output.get("child_root_inventory") == [
        "SPOT-R64", "FLUX", "SOUR", "SIGNATURE", "STATE-VECTOR",
        "EPS-CONVERGE", "IMERGE-LEAK", "KEYFLX", "OPTION",
        "LINK.MACRO", "LINK.TRACK", "LINK.SYSTEM", "SPOT-LEAK1D",
        "SPOT-FS-EQN", "SPOT-FS-K", "SPOT-QFISS",
    ], "RETURNED child root inventory changed")
    require(output.get("child_authority_inventory") == [
        "RHO", "FLUX", "SOUR", "QFISS", "STATE", "EPOCH",
    ], "RETURNED child authority inventory changed")
    require(output.get("child_state") == "SOLVED" and
            output.get("child_epoch") == 1,
            "RETURNED child lifecycle changed")
    require(output.get("child_has_plane") is False,
            "archive child acquired a duplicate PLANE owner")
    require(output.get("fixed_source_marker") == 1,
            "fixed-source equation marker changed")
    require(output.get("legacy_qfiss_shape") ==
            "SPOT-QFISS outer list length 1 containing 370 binary32 group vectors of length 14",
            "legacy QFISS shape changed")
    require(output.get("authoritative_qfiss_shape") ==
            "SPOT-R64/QFISS list length 370 containing binary64 group vectors of length 14",
            "authoritative QFISS shape changed")
    require(output.get("child_epoch_is_final_child_mutation") is True,
            "child commit ordering changed")
    require(output.get("root_epoch_is_final_output_mutation") is True,
            "root commit ordering changed")

    roles = manifest.get("source_roles", {})
    require(roles.get("QFISS") ==
            "the frozen fission contribution F*phi_n/k_n admitted by the radial equation",
            "QFISS physical meaning changed")
    require(roles.get("SOUR") ==
            "the accepted terminal total radial right-hand side returned by the solver",
            "SOUR physical meaning changed")
    require(roles.get("SOUR_may_replace_QFISS") is False,
            "terminal SOUR may replace frozen QFISS")
    require(roles.get("numerical_inequality_is_required") is False,
            "an unphysical SOUR/QFISS inequality gate was introduced")
    require("adds final off-group scattering to QFISS" in
            roles.get("reason", ""), "SPOASM source role changed")

    lifecycle = manifest.get("lifecycle", {})
    require(lifecycle.get("input_generation") ==
            "ASSEMBLED/1 + FROZEN-QFIS/1 + SOLVED/1",
            "collector input generation changed")
    require(lifecycle.get("output_generation") == "RETURNED/1",
            "collector output generation changed")
    for key in (
        "output_is_closed", "binds_ax_next", "publishes_rho_1",
        "publishes_k_1",
    ):
        require(lifecycle.get(key) is False,
                f"collector overreaches lifecycle boundary: {key}")
    require(lifecycle.get("next_consumer") == "SPOASM",
            "collector consumer changed")
    require(lifecycle.get("future_sequence") ==
            "SPOASM->axial FLU->SPOSTATE->SPOLEAK->separate close gate",
            "post-collector sequence changed")

    provenance = manifest.get("provenance_scope", {})
    require(provenance.get("proved") ==
            "exact label/index binding for listed fields, bitwise binding for admitted numerical fields, and recursive same-index copying of TRACK, MICROLIB2 and SYSTEM",
            "proved provenance scope changed")
    require(provenance.get(
        "historical_derivation_proved_from_detached_bits_alone") is False,
        "detached labels overclaim historical derivation")
    require(provenance.get("strong_physical_claim_scope") ==
            "immediate integrated B2O->B2B->B2R host path or a future sealed tuple receipt",
            "strong physical claim scope changed")
    require(provenance.get(
        "matching_plane_rho_epoch_alone_is_sufficient") is False,
        "metadata-only provenance was permitted")

    execution = manifest.get("execution_scope", {})
    require(set(execution) == {
        "transport_solves", "dragon_processes", "asm_calls", "spod_calls",
        "axial_flu_calls", "picard_maps", "long_calculations",
    }, "execution-scope inventory changed")
    require(all(value == 0 for value in execution.values()),
            "manifest permits physical execution")

    not_claimed = set(manifest.get("not_claimed", []))
    for claim in (
        "historical QFISS or SYSTEM derivation from detached bits alone",
        "an integrated B2O->B2B->B2R host path",
        "a new radial solve", "a new QFISS calculation", "SPOASM execution",
        "an axial solve", "a CLOSED/1 archive", "rho_1", "k_1",
        "radial convergence", "outer Picard convergence",
        "benchmark accuracy",
    ):
        require(claim in not_claimed, f"missing nonclaim: {claim}")


def check_parent_receipt() -> None:
    require(PARENT_RECEIPT_PATH.is_file(), "B2q parent receipt missing")
    digest = hashlib.sha256(PARENT_RECEIPT_PATH.read_bytes()).hexdigest()
    require(digest == PARENT_RECEIPT_SHA256,
            "B2q parent receipt changed")


def check_readme_scope() -> None:
    text = " ".join(README_PATH.read_text(encoding="utf-8").split())
    for required in (
        "B2r alone does **not** prove",
        "This phase does not implement that host integration.",
        "When off-group scattering is nonzero",
        "Their values are not required to be unequal",
    ):
        require(required in text, f"README provenance scope changed: {required}")


def check_source(text: str) -> None:
    whole = packed(text)
    body_text = routine(text, "SPOR64_B2R_COLLECT")
    body = packed(body_text)
    system_text = routine(text, "SYSTEM_IS_VALID", "function")
    track_text = routine(text, "TRACK_IS_VALID", "function")
    solved_text = routine(text, "SOLVED_IS_VALID", "function")
    source_text = routine(text, "SOURCE_IS_VALID", "function")
    mirror_text = routine(text, "MIRROR_MATCHES_REAL64", "function")
    exact_text = routine(text, "EXACT_INVENTORY", "function")

    require(re.search(r"(?im)^\s*module\s+SPOR64_B2R\s*$",
                      strip_comments(text)) is not None,
            "B2r module name changed")
    require("PUBLIC::SPOR64_B2R_COLLECT" in whole,
            "collector is not public")
    require("SPOR64_B2R_PREFLIGHT_FAILED=1" in whole,
            "preflight status changed")
    require("SPOR64_B2R_RETURNED=2" in whole,
            "returned status changed")
    require("NSNAP=3" in whole and "NGRP=370" in whole and
            "NUNKNO=14" in whole,
            "frozen returned-archive dimensions changed")

    signature = body.split(")", 1)[0]
    require(signature ==
            "SUBROUTINESPOR64_B2R_COLLECT(IPOUT,IPASSEMBLED,IPSOLVED,IPSOURCES,STATUS",
            "collector ABI changed")
    for forbidden in ("PLANE", "RHO", "KEFF", "EPOCH", "ALPHA",
                      "RELAX", "TOL"):
        require(forbidden not in signature,
                f"collector acquired loose scalar/control: {forbidden}")
    require_tokens("B2r ABI", body_text, (
        "type(c_ptr), intent(in) :: ipout, ipassembled",
        "type(c_ptr), intent(in) :: ipsolved(NSNAP), ipsources(NSNAP)",
        "integer, intent(out) :: status",
        "status = SPOR64_B2R_PREFLIGHT_FAILED",
    ))

    for forbidden in (
        "CALLFLU", "CALLASM", "CALLSPOASM", "CALLSPOLEAK",
        "CALLSPOSTATE", "XDRTA2", "FLU2DR64_CORE", "PICARD",
        "RELAX", "DAMP", "CLIP", "FITTED", "ALPHA=",
    ):
        require(forbidden not in whole,
                f"collector acquired forbidden execution/model token: {forbidden}")

    require_tokens("B2r input ownership", body_text, (
        "if (.not. c_associated(ipout)) return",
        "if (.not. c_associated(ipassembled)) return",
        "if (.not. EMPTY_LCM_ROOT(ipout)) return",
        "if (.not. ASSEMBLED_ROOT_IS_EXACT(ipassembled)) return",
        "CHARACTER_RECORD_MATCHES(ipassembled,'SIGNATURE',3,12,'L_ARCHIVE')",
        "RECORD_MATCHES(ipassembled,'LISTDIM',1,1)",
        "RECORD_MATCHES(ipassembled,'SPOT-ITER-K',1,4)",
        "RECORD_MATCHES(ipassembled,'TRACK',NSNAP,10)",
        "RECORD_MATCHES(ipassembled,'MICROLIB2',NSNAP,10)",
        "RECORD_MATCHES(ipassembled,'SYSTEM',NSNAP,10)",
        "RECORD_MATCHES(ipassembled,'FLUX',NSNAP,10)",
        "ROOT_AUTHORITY_IS_EXACT(root_authority)",
        "CHARACTER_RECORD_MATCHES(root_authority,'STATE',3,12,'ASSEMBLED')",
    ))

    require_tokens("B2r label binding", body_text, (
        "SOLVED_IS_VALID(ipsolved(slot),root_rho64,root_epoch",
        "plane=solved_plane(slot)",
        "if (solved_slot(plane) /= 0) return",
        "solved_slot(plane)=slot",
        "SOURCE_IS_VALID(ipsources(slot),root_rho64,root_epoch",
        "plane=source_plane(slot)",
        "if (source_slot(plane) /= 0) return",
        "source_slot(plane)=slot",
        "if (any(solved_slot == 0) .or. any(source_slot == 0)) return",
    ))
    require_tokens("B2r SOLVED admission", solved_text, (
        "SOLVED_ROOT_IS_EXACT(solved)",
        "SOLVED_AUTHORITY_IS_EXACT(authority)",
        "CHARACTER_RECORD_MATCHES(authority,'STATE',3,12,'SOLVED')",
        "LCMGET(authority,'PLANE',plane)",
        "if (plane < 1 .or. plane > NSNAP) return",
    ))
    require_tokens("B2r source admission", source_text, (
        "SOURCE_ROOT_IS_EXACT(source)",
        "SOURCE_AUTHORITY_IS_EXACT(authority)",
        "CHARACTER_RECORD_MATCHES(authority,'STATE',3,12,'FROZEN-QFIS')",
        "LCMGET(authority,'PLANE',plane)",
        "if (plane < 1 .or. plane > NSNAP) return",
    ))

    require_tokens("B2r same-index tuple", body_text, (
        "input_track(ip)=LCMGIL(tracks,ip)",
        "input_library(ip)=LCMGIL(libraries,ip)",
        "input_system(ip)=LCMGIL(systems,ip)",
        "SYSTEM_IS_VALID(input_system(ip),ip,root_rho64",
        "slot=solved_slot(plane)",
        "if (any(solved_key(:,slot) /= track_key(:,plane))) return",
        "SAME_REAL32_BITS(solved_leak(:,slot),system_leak(:,plane))",
    ))
    require_tokens("B2r TRACK consumer map", track_text, (
        "RECORD_MATCHES(track,'KEYFLX',NREG,1)",
        "RECORD_MATCHES(track,'KEYFLX$ANIS',NREG,1)",
        "LCMGET(track,'KEYFLX',keyflx)",
        "LCMGET(track,'KEYFLX$ANIS',keyanis)",
        "if (any(keyflx /= keyanis)) return",
    ))
    require_tokens("B2r SYSTEM identity", system_text, (
        "SYSTEM_ROOT_IS_EXACT(system)",
        "SYSTEM_AUTHORITY_IS_EXACT(authority)",
        "LCMGET(system,'SPOT-L1-SNAP',found_plane)",
        "if (found_plane /= plane) return",
    ))

    require_tokens("B2r root scalar binding", body_text, (
        "expected64=transfer(1.0_real64/iter_keff64,0_int64)",
        "transfer(root_rho64,0_int64) /= expected64",
        "root_epoch /= RETURN_EPOCH",
    ))
    for owner, helper in (
        ("B2r SYSTEM scalar binding", system_text),
        ("B2r SOLVED scalar binding", solved_text),
        ("B2r source scalar binding", source_text),
    ):
        require_tokens(owner, helper, (
            "transfer(found_rho,0_int64) /= transfer(rho,0_int64)",
            "found_epoch /= epoch",
        ))
    require_tokens("B2r source K binding", source_text, (
        "transfer(source_keff,0_int32)",
        "transfer(real(iter_keff,real32),0_int32)",
    ))

    require_tokens("B2r QFISS authority", source_text, (
        "RECORD_MATCHES(authority,'QFISS',NGRP,10)",
        "RECORD_MATCHES(source,'DSOUR',1,10)",
        "authority_qfiss=LCMGID(authority,'QFISS')",
        "source_outer=LCMGID(source,'DSOUR')",
        "source_inner=LCMGIL(source_outer,1)",
        "LCMGDL(authority_qfiss,ig,qfiss(:,ig))",
        "LCMGDL(source_inner,ig,qmirror(:,ig))",
        "MIRROR_MATCHES_REAL64(qmirror(:,ig),qfiss(:,ig))",
    ))
    require_tokens("B2r one-time projection", mirror_text, (
        "mirror_bits=transfer(mirror,0_int32,size(mirror))",
        "projected_bits=transfer(real(authority,real32),0_int32,size(mirror))",
        "all(mirror_bits == projected_bits)",
    ))
    require_tokens("B2r safe exact inventory", exact_text, (
        "LCMINF(iplist,object_file,object_name,empty,object_length,is_lcm)",
        "if (empty .or. object_length /= -1) return",
        "LCMNXT(iplist,item_name)",
    ))

    require_order("B2r publication", body_text, (
        "if (.not. EMPTY_LCM_ROOT(ipout)) return",
        "call LCMPTC(ipout,'SIGNATURE',12,signature)",
        "output_tracks=LCMLID(ipout,'TRACK',NSNAP)",
        "call LCMEQU(ipsolved(slot),output_item)",
        "call LCMDEL(output_authority,'PLANE')",
        "output_qfiss=LCMLID(output_authority,'QFISS',NGRP)",
        "legacy_outer=LCMLID(output_item,'SPOT-QFISS',1)",
        "call LCMPUT(output_authority,'EPOCH',1,1,root_epoch)",
        "root_authority=LCMDID(ipout,'SPOT-R64')",
        "call LCMPTC(root_authority,'STATE',12,lifecycle_state)",
        "call LCMPUT(root_authority,'EPOCH',1,1,root_epoch)",
        "status=SPOR64_B2R_RETURNED",
    ))
    require_tokens("B2r publication payload", body_text, (
        "call LCMEQU(input_track(plane),output_item)",
        "call LCMEQU(input_library(plane),output_item)",
        "call LCMEQU(input_system(plane),output_item)",
        "slot=solved_slot(plane)",
        "jp=source_slot(plane)",
        "call LCMPUT(output_item,'SPOT-FS-EQN',1,1,fs_marker)",
        "call LCMPUT(output_item,'SPOT-FS-K',1,2,source_keff32(jp))",
        "call LCMPDL(output_qfiss,ip,NUNKNO,4,qfiss64(:,ip,jp))",
        "call LCMPDL(legacy_inner,ip,NUNKNO,2,qmirror32(:,ip,jp))",
        "call LCMPTC(root_authority,'STATE',12,lifecycle_state)",
        "call LCMPUT(root_authority,'NPLANE',1,1,root_planes)",
        "lifecycle_state='RETURNED'",
    ))
    require(body.count("IF(.NOT.EMPTY_LCM_ROOT(IPOUT))RETURN") == 2,
            "fresh-output gate is not repeated immediately before publish")

    first_write = body.index("CALLLCMPTC(IPOUT,'SIGNATURE',12,SIGNATURE)")
    mutator_tokens = (
        "CALLLCMPUT", "CALLLCMPTC", "CALLLCMPDL", "CALLLCMDEL",
        "CALLLCMEQU", "LCMLID(", "LCMLIL(", "LCMDID(", "LCMDIL(",
    )
    prepublication = body[:first_write]
    for token in mutator_tokens:
        require(token not in prepublication,
                f"input/preflight mutation admitted before publish: {token}")
    for helper in re.findall(
        r"(?is)\blogical\s+function\b.*?\bend\s+function\b[^\n]*",
        strip_comments(text),
    ):
        helper_body = packed(helper)
        for token in mutator_tokens:
            require(token not in helper_body,
                    f"validation helper acquired a mutator: {token}")
    source_without_comments = strip_comments(body_text)
    first_write_match = re.search(
        r"(?is)\bcall\s+LCMPTC\s*\(\s*ipout\s*,\s*'SIGNATURE'\s*,"
        r"\s*12\s*,\s*signature\s*\)",
        source_without_comments,
    )
    require(first_write_match is not None, "first output mutation missing")
    require(re.search(r"(?i)\breturn\b", source_without_comments[
        first_write_match.start():
    ]) is None, "recoverable return remains after first output mutation")
    root_epoch_write = body.index(
        "CALLLCMPUT(ROOT_AUTHORITY,'EPOCH',1,1,ROOT_EPOCH)"
    )
    require(body.rfind("CALLLCM") == root_epoch_write,
            "root EPOCH is not the final output LCM mutation")
    publication = body[first_write:]
    require("LCMPUT(ROOT_AUTHORITY,'RHO'" not in publication,
            "RETURNED root acquired RHO")
    require("LCMPUT(IPOUT,'SPOT-ITER-K'" not in publication,
            "RETURNED root acquired SPOT-ITER-K")
    require("LCMPUT(OUTPUT_AUTHORITY,'PLANE'" not in body,
            "archive child retained duplicate PLANE ownership")
    require("LCMDEL(OUTPUT_AUTHORITY,'PLANE')" in body,
            "detached PLANE is not removed at archive insertion")
    require("LCMGID(OUTPUT_AUTHORITY,'SOUR')" not in publication and
            "LCMGID(OUTPUT_ITEM,'SOUR')" not in publication,
            "terminal SOUR was admitted as QFISS provenance")

    expected_inventories = {
        "ASSEMBLED_ROOT_IS_EXACT": (
            "SIGNATURE", "LISTDIM", "SPOT-ITER-K", "TRACK",
            "MICROLIB2", "SYSTEM", "FLUX", "SPOT-R64",
        ),
        "ROOT_AUTHORITY_IS_EXACT": (
            "RHO", "NPLANE", "STATE", "EPOCH",
        ),
        "SOLVED_ROOT_IS_EXACT": (
            "SPOT-R64", "FLUX", "SOUR", "SIGNATURE", "STATE-VECTOR",
            "EPS-CONVERGE", "IMERGE-LEAK", "KEYFLX", "OPTION",
            "LINK.MACRO", "LINK.TRACK", "LINK.SYSTEM", "SPOT-LEAK1D",
        ),
        "SOLVED_AUTHORITY_IS_EXACT": (
            "RHO", "PLANE", "FLUX", "SOUR", "STATE", "EPOCH",
        ),
        "SOURCE_ROOT_IS_EXACT": (
            "SIGNATURE", "STATE-VECTOR", "SPOT-FROZEN", "SPOT-KEFF",
            "SPOT-QINT", "DSOUR", "SPOT-R64",
        ),
        "SOURCE_AUTHORITY_IS_EXACT": (
            "RHO", "PLANE", "STATE", "QFISS", "EPOCH",
        ),
        "SYSTEM_ROOT_IS_EXACT": (
            "SIGNATURE", "LINK.MACRO", "LINK.TRACK", "STATE-VECTOR",
            "SPOT-LEAK1D", "SPOT-L1-SNAP", "GROUP", "SPOT-R64",
        ),
        "SYSTEM_AUTHORITY_IS_EXACT": (
            "RHO", "STATE", "EPOCH",
        ),
    }
    for name, names in expected_inventories.items():
        inventory = packed(routine(text, name, "function"))
        for record in names:
            require(f"'{record}'" in inventory,
                    f"{name} inventory lost {record}")
        require(inventory.count("'") // 2 >= len(names),
                f"{name} exact inventory is incomplete")


def check_all(source: str, manifest: Mapping[str, Any]) -> None:
    check_manifest(manifest)
    check_parent_receipt()
    check_readme_scope()
    check_source(source)


def main() -> None:
    source = load_source()
    manifest = load_manifest()
    check_all(source, manifest)
    print("B2R STATIC RETURNED-ARCHIVE PASS")
    print("B2R API=ASSEMBLED+SOLVED(3)+FROZEN-QFIS(3)->RETURNED/1")
    print("B2R PLANE-BINDING=LABEL-SET-{1,2,3} NOT-ARGUMENT-ORDER")
    print("B2R QFISS=TYPE4-AUTHORITY+TYPE2-SPOASM-MIRROR SOUR=TERMINAL-WITNESS")
    print("B2R CLOSED/1=NOT-PUBLISHED SOLVER-EXECUTIONS=0")


if __name__ == "__main__":
    main()
