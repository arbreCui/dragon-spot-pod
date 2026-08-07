#!/usr/bin/env python3
"""Independent static audit for the B2q lifecycle/RHO contract."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MANIFEST_PATH = HERE / "precision_manifest.json"
RUNNER_PATH = HERE / "run_phase_a9b_b2q_lifecycle_rho_contract.sh"

SOURCE_PATHS = {
    name: ROOT / name
    for name in (
        "src/SPOR64_B2B.f90",
        "src/SPOR64_B2C.f90",
        "src/SPOR64_B2H.f90",
        "src/SPOR64_B2I.f90",
        "src/SPOR64_B2J.f90",
        "src/SPOR64_B2K.f90",
        "src/SPOR64_B2N.f90",
        "src/SPOR64_B2O.f90",
    )
}

PARENT_COMMIT = "e9af085dfb73f1a69df4cbc3eacf989d3382e105"
PARENT_RECEIPT_SHA256 = (
    "147d0c1ff95502344eb33234af4804be0e879bc3befae10699ddf8e9d3c642cc"
)


class GateError(AssertionError):
    """A frozen lifecycle assertion was violated."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def packed(text: str) -> str:
    code = "\n".join(line.split("!", 1)[0] for line in text.splitlines())
    return re.sub(r"[\s&]+", "", code).upper()


def routine(text: str, name: str, kind: str = "subroutine") -> str:
    if kind == "subroutine":
        pattern = (
            rf"(?is)\bsubroutine\s+{re.escape(name)}\b.*?"
            rf"\bend\s+subroutine\s+{re.escape(name)}\b"
        )
    else:
        pattern = (
            rf"(?is)\b(?:logical\s+)?function\s+{re.escape(name)}\b.*?"
            rf"\bend\s+function\s+{re.escape(name)}\b"
        )
    match = re.search(pattern, text)
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
    require(positions == sorted(positions), f"{owner} lifecycle order changed")


def load_sources() -> dict[str, str]:
    return {
        name: path.read_text(encoding="utf-8")
        for name, path in SOURCE_PATHS.items()
    }


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def check_manifest(manifest: Mapping[str, Any]) -> None:
    require(manifest.get("phase") == "A9b-B2q", "manifest phase changed")
    require(manifest.get("parent_commit") == PARENT_COMMIT,
            "manifest parent commit changed")
    require(manifest.get("parent_receipt_sha256") ==
            PARENT_RECEIPT_SHA256, "manifest parent receipt changed")
    require(manifest.get("production_source_changes") is False,
            "contract freeze acquired production changes")
    require(manifest.get("contract_version") == 1,
            "contract version changed")
    require(manifest.get("empirical_controls_added") is False,
            "manifest permits empirical controls")

    generation = manifest.get("generation_convention", {})
    require(generation == {
        "closed_n": (
            "sole boundary permitted to introduce rho_n from its accepted "
            "axial eigenvalue"
        ),
        "projected_n_plus_1": "carries rho_n bit-exactly",
        "assembled_n_plus_1": "carries rho_n bit-exactly",
        "frozen_qfis_n_plus_1": "uses and carries rho_n bit-exactly",
        "solved_n_plus_1": (
            "inherits rho_n and the work epoch without recomputation"
        ),
    }, "generation/RHO convention changed")

    implemented = manifest.get("implemented_generation", {})
    require(implemented.get("states") == [
        "CLOSED/0", "PROJECTED/1", "ASSEMBLED/1",
        "FROZEN-QFIS/1", "SOLVED/1",
    ], "implemented lifecycle changed")
    require(implemented.get("rho_owner") == "CLOSED/0",
            "implemented RHO owner changed")
    require(implemented.get("rho_bits") ==
            "identical through every generation-1 authority",
            "generation-1 bit-identity claim changed")
    require(implemented.get("bootstrap_reciprocal") ==
            "1.0_real64/real(K-EFFECTIVE_binary32,real64)",
            "bootstrap reciprocal definition changed")
    require(implemented.get("new_rho_after_solved") is False,
            "SOLVED is allowed to invent a new RHO")

    b2h = manifest.get("b2h_boundary", {})
    require(b2h.get("seed_rho") ==
            "finite positive completeness witness",
            "B2h seed RHO claim changed")
    require(b2h.get("output_rho") ==
            "explicit caller binary64 value",
            "B2h output RHO owner changed")
    require(b2h.get("direct_output_is_canonical") is False,
            "direct B2h output was promoted to canonical")

    b2j = manifest.get("b2j_boundary", {})
    require(b2j.get("plane_root_rho_equality_scope") ==
            "bootstrap CLOSED/0 archive projection only",
            "B2J bootstrap RHO-equality scope changed")
    require(b2j.get("general_closed_n_child_rho_equality_claimed") is False,
            "B2J bootstrap equality was generalized")

    plane = manifest.get("plane_identity_contract", {})
    require(plane.get("archive_member_owner") ==
            "one-based archive list index",
            "archive-member plane owner changed")
    require(plane.get("archive_member_has_plane_record") is False,
            "archive member acquired a duplicate PLANE owner")
    for key in (
        "detached_projected_has_plane_record",
        "detached_solved_has_plane_record",
        "detached_frozen_qfis_has_plane_record",
        "collector_rejects_duplicates",
        "collector_omits_redundant_child_plane",
    ):
        require(plane.get(key) is True,
                f"plane identity contract changed: {key}")
    require(plane.get("system_owner") == "SPOT-L1-SNAP",
            "SYSTEM plane owner changed")
    require(plane.get("collector_required_plane_set") == [1, 2, 3],
            "collector plane set changed")

    future = manifest.get("future_closed_1", {})
    require(future.get("root_rho") ==
            "rho_1 may differ from child SOLVED/1 rho_0",
            "future CLOSED/1 root RHO rule changed")
    require(future.get("child_rho") ==
            "rho_0 labels the equations that produced each child",
            "future child SOLVED RHO rule changed")
    require(future.get("different_root_and_child_rho_is_valid") is True,
            "future CLOSED/child RHO distinction was forbidden")
    require(future.get("collector_required_bindings") == [
        "three accepted SOLVED children", "same-index SYSTEM",
        "same-index TRACK", "same-index MICROLIB2", "same-index QFISS",
        "same-index K",
    ], "future collector binding inventory changed")
    require(future.get("collector_binds_ax_next") is False,
            "returned-archive collector acquired AX_NEXT")
    require(future.get("collector_commits_closed_1") is False,
            "returned-archive collector prematurely closes generation 1")
    require(future.get("collector_output") ==
            "unclosed returned archive for SPOASM",
            "returned-archive collector output changed")
    require(future.get("axial_update_sequence") ==
            "SPOASM->axial FLU->SPOSTATE->SPOLEAK",
            "future axial update sequence changed")
    require(future.get("close_gate_required_bindings") == [
        "returned archive", "AX_NEXT",
    ], "future close-gate binding inventory changed")
    require(future.get("close_gate_commit") == "CLOSED/1",
            "future close-gate commit changed")
    require(future.get("matching_epoch_or_rho_alone_is_sufficient") is False,
            "future collector permits metadata-only provenance")

    epoch = manifest.get("epoch_contract", {})
    require(epoch.get("meaning") ==
            "local generation and logical-commit label",
            "epoch meaning changed")
    for key in (
        "global_identifier", "solver_iteration_counter",
        "convergence_certificate", "b2c_increments_epoch",
    ):
        require(epoch.get(key) is False, f"epoch contract permits {key}")
    require(epoch.get("generation_1_shared_states") == [
        "PROJECTED", "ASSEMBLED", "FROZEN-QFIS", "SOLVED",
    ], "generation-1 epoch state set changed")
    require(epoch.get("b2h_local_transition") ==
            "SOLVED(n)->PROJECTED(n+1)",
            "B2h local epoch transition changed")

    evidence = manifest.get("dynamic_evidence", {})
    for key in (
        "production_solver_executions", "dragon_executions",
        "asm_executions",
    ):
        require(evidence.get(key) == 0,
                f"manifest permits nonzero {key}")
    not_claimed = set(manifest.get("not_claimed", []))
    for claim in (
        "a new CLOSED/1 producer", "a rho_1 value",
        "a second production CONT call", "radial convergence",
        "outer Picard convergence", "benchmark accuracy",
    ):
        require(claim in not_claimed, f"missing nonclaim: {claim}")


def check_source_hashes(
    sources: Mapping[str, str], manifest: Mapping[str, Any]
) -> None:
    frozen = manifest.get("source_freeze_sha256", {})
    require(set(frozen) == set(SOURCE_PATHS),
            "source-freeze inventory changed")
    require(set(sources) == set(SOURCE_PATHS),
            "loaded source inventory changed")
    for name, text in sources.items():
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        require(digest == frozen[name], f"production source changed: {name}")


def check_evidence_hashes(manifest: Mapping[str, Any]) -> None:
    evidence = manifest.get("evidence_sha256", {})
    require(len(evidence) == 14, "evidence hash inventory changed")
    for name, expected in evidence.items():
        path = ROOT / name
        require(path.is_file(), f"evidence file missing: {name}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(digest == expected, f"evidence file changed: {name}")


def check_b2i(text: str) -> None:
    body = routine(text, "SPOR64_B2I_SEAL_BOOTSTRAP")
    require("BOOTSTRAP_EPOCH=0" in packed(text),
            "B2I bootstrap epoch changed")
    require_tokens("B2I", body, (
        "expected64 = transfer(1.0_real64/real(keff32,real64),0_int64)",
        "if (found64 /= expected64) return",
        "call LCMPUT(output_authority,'RHO',1,4,rho64)",
        "call LCMPTC(ipaxout,'SPOT-X-STATE',12,lifecycle_state)",
        "call LCMPUT(ipaxout,'SPOT-X-EPOCH',1,1,BOOTSTRAP_EPOCH)",
        "call LCMPTC(output_authority,'STATE',12,lifecycle_state)",
        "call LCMPUT(output_authority,'EPOCH',1,1,BOOTSTRAP_EPOCH)",
    ))
    p = packed(body)
    require(p.count("LCMPUT(OUTPUT_AUTHORITY,'RHO',1,4,RHO64)") == 2,
            "B2I must publish one canonical RHO to planes and root")
    signature = p.split(")", 1)[0]
    require("RHO" not in signature and "ALPHA" not in signature,
            "B2I acquired a loose RHO or empirical scalar")


def check_b2j(text: str) -> None:
    body = routine(text, "SPOR64_B2J_PROJECT_ARCHIVE")
    whole = packed(text)
    require("BOOTSTRAP_INPUT_EPOCH=0" in whole and
            "BOOTSTRAP_OUTPUT_EPOCH=1" in whole,
            "B2J bootstrap generation changed")
    require_tokens("B2J", body, (
        "expected64 = transfer(1.0_real64/real(keff32,real64),0_int64)",
        "if (transfer(root_rho64,0_int64) /= transfer(rho64,0_int64)) return",
        "if (transfer(plane_rho64,0_int64) /= transfer(rho64,0_int64)) return",
        "call SPOR64_B2H_PROJECT(staged_flux(ip),input_flux(ip),",
        "input_track(ip),projected_region64(:,:,ip),rho64,b2h_status)",
        "rho64,projected_epoch,leakage64((ip-1)*NGRP+1:ip*NGRP)",
        "call LCMPUT(output_authority,'RHO',1,4,rho64)",
        "call LCMPUT(output_authority,'EPOCH',1,1,projected_epoch)",
    ))
    require_order("B2J", body, (
        "call LCMGET(ipax,'SPOT-X-RHO',rho64)",
        "call SPOR64_B2H_PROJECT(staged_flux(ip),input_flux(ip),",
        "call LCMPUT(output_authority,'RHO',1,4,rho64)",
        "call LCMPUT(output_authority,'EPOCH',1,1,projected_epoch)",
    ))
    signature = packed(body).split(")", 1)[0]
    require("RHO" not in signature and "ALPHA" not in signature,
            "B2J acquired a loose RHO or empirical scalar")


def check_b2k(text: str) -> None:
    body = routine(text, "SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE")
    whole = packed(text)
    require("PROJECTED_EPOCH=1" in whole and "ASSEMBLED_EPOCH=1" in whole,
            "B2K generation labels changed")
    require_tokens("B2K", body, (
        "expected64 = transfer(1.0_real64/iter_keff64,0_int64)",
        "if (transfer(plane_rho64,0_int64) /= transfer(rho64,0_int64)) return",
        "call LCMPUT(staged_authority,'RHO',1,4,rho64)",
        "call LCMPUT(root_authority,'RHO',1,4,rho64)",
        "call LCMPUT(root_authority,'EPOCH',1,1,ASSEMBLED_EPOCH)",
    ))
    signature = packed(body).split(")", 1)[0]
    require("RHO" not in signature and "ALPHA" not in signature,
            "B2K acquired a loose RHO or empirical scalar")


def check_b2n(text: str) -> None:
    body = routine(text, "SPOR64_B2N_BUILD")
    whole = packed(text)
    require("PROJECTED_EPOCH=1" in whole and
            "FROZEN_SOURCE_EPOCH=1" in whole,
            "B2N generation labels changed")
    require_tokens("B2N", body, (
        "expected64 = transfer(1.0_real64/iter_keff64,0_int64)",
        "if (transfer(plane_rho64,0_int64) /= transfer(rho64,0_int64)) return",
        "contribution64 = contribution64 * rho64",
        "call LCMPUT(source_authority,'RHO',1,4,rho64)",
        "call LCMPUT(source_authority,'EPOCH',1,1,FROZEN_SOURCE_EPOCH)",
    ))
    signature = packed(body).split(")", 1)[0]
    require("RHO" not in signature and "ALPHA" not in signature,
            "B2N acquired a loose RHO or empirical scalar")


def check_b2o(text: str) -> None:
    body = routine(text, "SPOR64_B2O_SEAL_CONT_PAIR")
    require("CONT_EPOCH=1" in packed(text), "B2O CONT epoch changed")
    require_tokens("B2O", body, (
        "expected64 = transfer(1.0_real64/iter_keff64,0_int64)",
        "transfer(source_rho64,0_int64) /= transfer(root_rho64,0_int64)",
        "transfer(seed_rho64,0_int64) /= transfer(root_rho64,0_int64)",
        "transfer(system_rho64,0_int64) /= transfer(root_rho64,0_int64)",
        "if (source_epoch /= root_epoch) return",
        "if (seed_epoch /= root_epoch) return",
        "if (system_epoch /= root_epoch) return",
        "call LCMPUT(output_seed_authority,'EPOCH',1,1,root_epoch)",
        "call LCMPUT(output_system_authority,'EPOCH',1,1,root_epoch)",
    ))
    signature = packed(body).split(")", 1)[0]
    require("RHO" not in signature and "PLANE" not in signature and
            "ALPHA" not in signature,
            "B2O acquired a loose lifecycle scalar")


def check_b2b(text: str) -> None:
    ingress = routine(text, "SPOR64_B2B_INGRESS")
    lifecycle = routine(text, "CONT_LIFECYCLE_IS_BOUND", "function")
    require_tokens("B2B lifecycle", lifecycle, (
        "integer, parameter :: CONT_EPOCH = 1",
        "transfer(seed_rho64,0_int64) /= transfer(source_rho64,0_int64)",
        "transfer(seed_rho64,0_int64) /= transfer(system_rho64,0_int64)",
        "if (seed_epoch /= CONT_EPOCH) return",
        "if (source_epoch /= CONT_EPOCH) return",
        "if (system_epoch /= CONT_EPOCH) return",
        "if (seed_plane /= source_plane) return",
        "if (system_plane /= source_plane) return",
    ))
    require_order("B2B ingress", ingress, (
        "CONT_LIFECYCLE_IS_BOUND(ipseed,ipsou,ipsys,",
        "call XDRTA2",
        "call FLU2DR64_CORE",
        "call SPOR64_B2C_PUBLISH_CONT(ipflux,ipseed,",
    ))


def check_b2c(text: str) -> None:
    body = routine(text, "SPOR64_B2C_PUBLISH_IMPL")
    require_tokens("B2C", body, (
        "call LCMGET(lifecycle_authority,'RHO',lifecycle_rho64)",
        "call LCMGET(lifecycle_authority,'EPOCH',lifecycle_epoch)",
        "call LCMPUT(authority,'RHO',1,4,lifecycle_rho64)",
        "authority_state = 'SOLVED'",
        "call LCMPUT(authority,'EPOCH',1,1,lifecycle_epoch)",
    ))
    p = packed(body)
    require("LIFECYCLE_EPOCH+1" not in p,
            "B2C increments the accepted work epoch")
    require("1.0_REAL64/LIFECYCLE_RHO64" not in p and
            "1.0_REAL64/TERMINAL" not in p,
            "B2C recomputes RHO from terminal data")
    require_order("B2C", body, (
        "call LCMGET(lifecycle_authority,'RHO',lifecycle_rho64)",
        "call LCMPUT(authority,'RHO',1,4,lifecycle_rho64)",
        "call LCMPTC(authority,'STATE',12,authority_state)",
        "call LCMPUT(authority,'EPOCH',1,1,lifecycle_epoch)",
    ))


def check_b2h(text: str) -> None:
    body = routine(text, "SPOR64_B2H_PROJECT")
    require_tokens("B2H", body, (
        "call LCMGET(seed_authority,'RHO',seed_rho64)",
        "if (.not. ieee_is_finite(seed_rho64) .or. seed_rho64 <= +0.0_real64) return",
        "if (.not. ieee_is_finite(rho64) .or. rho64 <= +0.0_real64) return",
        "output_epoch = seed_epoch + 1",
        "call LCMPUT(output_authority,'RHO',1,4,rho64)",
        "call LCMPUT(output_authority,'EPOCH',1,1,output_epoch)",
    ))
    p = packed(body)
    require("LCMPUT(OUTPUT_AUTHORITY,'RHO',1,4,SEED_RHO64)" not in p,
            "B2H silently replaced the explicit projected RHO with seed RHO")
    require("TRANSFER(SEED_RHO64" not in p,
            "B2H falsely claims direct seed/output RHO identity")
    signature = p.split(")", 1)[0]
    require("RHO64" in signature and "ALPHA" not in signature,
            "B2H explicit RHO ABI changed or acquired an empirical scalar")


def check_source_contract(sources: Mapping[str, str]) -> None:
    check_b2b(sources["src/SPOR64_B2B.f90"])
    check_b2c(sources["src/SPOR64_B2C.f90"])
    check_b2h(sources["src/SPOR64_B2H.f90"])
    check_b2i(sources["src/SPOR64_B2I.f90"])
    check_b2j(sources["src/SPOR64_B2J.f90"])
    check_b2k(sources["src/SPOR64_B2K.f90"])
    check_b2n(sources["src/SPOR64_B2N.f90"])
    check_b2o(sources["src/SPOR64_B2O.f90"])


def check_runner(text: str) -> None:
    p = packed(text)
    for token in (
        "-FFP-CONTRACT=OFF", "-FNO-FAST-MATH", "-FCHECK=ALL",
        "TEST_B2H_PROJECTION_AUTHORITY", "PYTHON3-MUNITTEST-V",
        "B2HPROJECTION-AUTHORITYPASS", "SHASUM-A256-C\"$RECEIPT\"",
        "PRODUCTION-SOLVER-EXECUTIONS=0", "DRAGON-EXECUTIONS=0",
        "ASM-EXECUTIONS=0", "RECEIPT=FROZEN",
    ):
        require(token in p, f"runner contract missing: {token}")
    for forbidden in (
        "$ROOT/BIN/DARWIN_ARM64/DRAGON", "SRC/FLU.F", "SRC/SPOR64_A8.F90",
        "SRC/SPOMOC.F90", "SRC/SPOASM", "SRC/SPOR64_B2N.F90",
        "SRC/SPOR64_B2K.F90", "MAKE SPOT-", "./RUN.SH",
    ):
        require(forbidden not in p,
                f"runner acquired a production execution path: {forbidden}")
    require("NM-G" in p and "DOORFV|MCCGF|MCGMRE" in p,
            "runner lacks linked-symbol solver exclusion")


def check_all(
    sources: Mapping[str, str],
    manifest: Mapping[str, Any],
    runner: str | None = None,
    *,
    enforce_hashes: bool = True,
) -> None:
    check_manifest(manifest)
    if enforce_hashes:
        check_source_hashes(sources, manifest)
        check_evidence_hashes(manifest)
    check_source_contract(sources)
    if runner is not None:
        check_runner(runner)


def main() -> None:
    sources = load_sources()
    manifest = load_manifest()
    runner = RUNNER_PATH.read_text(encoding="utf-8")
    check_all(sources, manifest, runner)
    print("B2Q STATIC LIFECYCLE-RHO CONTRACT PASS")
    print("B2Q FLOW=CLOSED(N)/RHO_N->WORK(N+1)/RHO_N")
    print("B2Q CURRENT=CLOSED/0->PROJECTED/1->ASSEMBLED/1->FROZEN-QFIS/1->SOLVED/1")
    print("B2Q PRODUCTION-SOURCE-CHANGES=0 EMPIRICAL-CONTROLS-ADDED=0")


if __name__ == "__main__":
    main()
