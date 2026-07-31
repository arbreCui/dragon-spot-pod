#!/usr/bin/env python3
"""Fail-closed static checker for the Phase-A8 inner REAL64 closure."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "precision_manifest.json"
CORE = HERE / "SPOR64_A8.f90"
ACA = HERE / "SPOR64_A8_ACA.f90"
ADAPTER = HERE / "MCGFFIR64_RANK_ADAPTER.f90"
RUNNER = HERE / "run_phase_a8.sh"
README = HERE / "README.md"
RECEIPT = HERE / "phase_a8_implementation_receipt.sha256"
BASELINE_COMMIT = "287e97308400e40f9b6c72bfde3bfbdf3996dd26"
EXPECTED_A7_RECEIPT_SHA256 = (
    "c744a413f1b75d23ed0f9344a31d3269c4f76051af54e7e4100f3f808d8093e1"
)
EXPECTED_A6_RECEIPT_SHA256 = (
    "d250afba106b0cc55bb77abd78157ffd856f77ecbb1e40a618902633813a0958"
)
EXPECTED_SPOMOC_SHA256 = (
    "23a1927a133c19a86ffef9c3e0f4e619a899752cae0e7c2f0baa1bfc226502bc"
)

EXPECTED_CANONICAL_SHA256 = (
    "5e23155bf8fc378e79cc8d5ba75152c88cc369460cd2bf5bb0f13e6fbc87318c"
)
EXPECTED_IMPLEMENTATION_SHA256 = (
    "eaa8110ce17e109db22e93a95d2b8d5495edfd57c18b1aa8676bc2cdaba9e8d7"
)
EXPECTED_ACA_SHA256 = (
    "a0138a9ad863ef0c6e6eb7c51520d568ee20b6b26c79c332c374f6ba3f09c115"
)
EXPECTED_ADAPTER_SHA256 = (
    "b0f71b95d01e72fe873eae197549ad10cd7f27fca2e3f0e640e7460a2ea4ace7"
)
EXPECTED_RUNNER_SHA256 = (
    "d6448dc54a4bf67a8c04850b389f67126eea8e23807fd12f60eba9c284c0b9c5"
)

EXPECTED_STATUS = {
    "classification": "FROZEN-IMPLEMENTED-COMPILE-ONLY-INNER-CLOSURE",
    "a8_addendum_frozen": True,
    "inner_nodes_implemented": True,
    "compile_only": True,
    "link_authorized": False,
    "execution_authorized": False,
    "production_source_changes": 0,
    "production_route_connected": False,
    "default_runtime_route_changed": False,
    "spomoc_capture64_implemented": False,
    "runtime_provenance_validated": False,
    "tracking_position_validated": False,
    "actual_transport_response_validated": False,
    "continuous_real64_lane": False,
    "radial_convergence": "NOT-EVALUATED",
    "outer_picard_convergence": "NOT-EVALUATED",
    "object_links": 0,
    "object_executions": 0,
    "tracking_reads": 0,
    "transport_solves": 0,
    "dragon_runs": 0,
}

EXPECTED_LOCKED_BRANCH = {
    "NGRP": 370,
    "NREG": 8,
    "NSOUT": 6,
    "NLONG": 14,
    "KPN": 14,
    "NBMIX": 8,
    "NDIM": 2,
    "NANI": 1,
    "NLIN": 1,
    "NFUNL": 1,
    "STIS": 1,
    "IDIR": 0,
    "ISCH": 11,
    "KRYL": 10,
    "IAAC": 80,
    "ISCR": 0,
    "PACA": 4,
    "MAXI": 20,
    "NSTART": 10,
    "MAXIT": 19,
    "MAXACC": 200,
    "LFORW": True,
    "CYCLIC": False,
    "LPRISM": False,
    "MACFLG": False,
    "COMBFLG": False,
    "REBFLG_INSIDE_ACA": False,
    "NGIND": "strict consecutive tail ending at 370",
    "NCONV": (
        "arbitrary nonempty noncontiguous input mask; false entries "
        "are never reactivated"
    ),
}

EXPECTED_STATUS_NODES = [
    "DOORFV64",
    "MCCGF64",
    "MCGFLX64",
    "MCGMRE64",
    "MCGFL164",
    "MCGFCA64",
    "MCGABG64",
]

EXPECTED_LEGACY_HASHES = {
    "src/MCGSIG.f":
        "ab587811d170886439ff7ab1333ac2e89556f2e9deccc95a802b7d7b61eea30d",
    "src/MOCIK3.f":
        "5193a5a8a4922f4c20b34fae19f1d1278722c31c33dae143bf970b7e2595e007",
    "src/MCGFCF.f":
        "60c841dbd2a0a2de2023de8a424b0162bc9898c5c5b877cc4d59f5b892b0deb9",
    "src/MCGFFIR.f":
        "b0400eb5211b5551f86f02608aa122e1301f38996c576dde818834da851cec6b",
    "src/MCGFFAR.f":
        "4bd72f5ec4c71d22e582afdb7f3d7e259e87b308d59c888a67ce88ec33916461",
    "src/MCGFFAL.f":
        "35f4e9e862e19cce47c0caa40dbe43168265c1170653875813bed0fcaaad7056",
    "src/MCGSCA.f":
        "fb16fe47c842d3a8c6e8726efb05195ce47ec88c6fdf6c00c65a91a3573a0159",
    "src/MCGFST.f":
        "bda4ec2376d91e5cf12427288c6bc1c565980cf916639937dca21ad7ad62b5e3",
    "Utilib/src/PRINAM.f":
        "97720815ae3160d75a5dd3d0fcf74183089f2ac693ee7c0567bfde14c012a7b6",
    "Utilib/src/MSRLUS1.f":
        "28af3f35832c64b382f5f6fde155e5d1a72eb0ca3c0eb54375e65fa3d39539bc",
    "Utilib/src/DDOT.f":
        "42d5e9efe18d19507017e85b061e05b5230f189014d8ebea9ba6d8344b143106",
}

EXPECTED_PORTED_LEGACY_HASHES = {
    "src/DOORFV.f":
        "630f84ba8c738e520e471f63f67e2a9813bc9723d3e7ec30db59e478579b0a8d",
    "src/MCCGF.f":
        "621fba6d02d1b1efae2d6d6db8e61d1463a3a24bcf4d0efe3579bfba97c55546",
    "src/MCGFLX.f":
        "89f03dca19474663460736359ff1acf0b3648086d2780286033b85824333344f",
    "src/MCGMRE.f":
        "61f71a4873a744608d429eaccc61807d76b5b50a3d2c10213734bb5b26bf1379",
    "src/MCGFL1.f":
        "6701db8972bd92e339d99879787a126f1ce38b72936852ba331259877894df9f",
    "src/MCGFCS.f":
        "14661cff68e916e0fdc962320c434d5eb7aba247bce138a696cc809aaac78ec6",
    "src/MCGFCA.f":
        "f15b8d7656c00286a1a63856e13e1fcd7ded0289de03b34cca69300fe34f8b52",
    "src/MCGFCR.f":
        "f75842440e598933f0322280fc5f4fabd3cb9811f5a890f0ac16a75c5d2acdfd",
    "src/MCGABG.f":
        "35448795eb5297e7cbb59b962fe314f462ebbb470ef1366d2ffa91651ef8e5d2",
    "src/MCGPRA.f":
        "5cc671a8b084629bd92ca814d1362d55995c6c420bf4d71edaf35000c0132629",
}

EXPECTED_NEGATIVES = [
    "compile_fail_real32_mutable_tail.f90",
    "compile_fail_real64_operator.f90",
    "compile_fail_noncontiguous_mutable.f90",
    "compile_fail_keyflx_rank.f90",
    "compile_fail_flat_pjjind.f90",
    "compile_fail_real32_capture.f90",
    "compile_fail_cf_n1_not_lc.f90",
    "compile_fail_im_n_not_nplus1.f90",
    "compile_fail_int32_cutoff.f90",
]

EXPECTED_SYMBOL_INVENTORIES = [
    "expected_a8_unresolved.txt",
    "expected_aca_unresolved.txt",
    "expected_adapter_unresolved.txt",
    "expected_anchor_unresolved.txt",
    "expected_a8_defined.txt",
    "expected_aca_defined.txt",
    "expected_adapter_defined.txt",
    "expected_anchor_defined.txt",
]

EXPECTED_RECEIPT_PATHS = [
    "validation/iterative/real64_phase_a6/phase_a6_implementation_receipt.sha256",
    "validation/iterative/real64_phase_a7/phase_a7_implementation_receipt.sha256",
    "validation/iterative/real64_phase_a7/README.md",
    "validation/iterative/real64_phase_a7/precision_ownership_manifest.json",
    "validation/iterative/real64_phase_a7/check_phase_a7.py",
    "validation/iterative/real64_phase_a7/test_phase_a7_contract.py",
    "validation/iterative/real64_phase_a7/run_phase_a7.sh",
    "README.md",
    "validation/iterative/README.md",
    "Makefile",
    "validation/iterative/real64_phase_a8/README.md",
    "validation/iterative/real64_phase_a8/precision_manifest.json",
    "validation/iterative/real64_phase_a8/SPOR64_A8.f90",
    "validation/iterative/real64_phase_a8/SPOR64_A8_ACA.f90",
    "validation/iterative/real64_phase_a8/MCGFFIR64_RANK_ADAPTER.f90",
    "validation/iterative/real64_phase_a8/compile_spor64_a8_anchor.f90",
    "validation/iterative/real64_phase_a8/check_phase_a8.py",
    "validation/iterative/real64_phase_a8/test_phase_a8_contract.py",
    "validation/iterative/real64_phase_a8/run_phase_a8.sh",
] + [
    f"validation/iterative/real64_phase_a8/{name}"
    for name in EXPECTED_NEGATIVES
] + [
    f"validation/iterative/real64_phase_a8/{name}"
    for name in EXPECTED_SYMBOL_INVENTORIES
] + list(EXPECTED_PORTED_LEGACY_HASHES) + \
    list(EXPECTED_LEGACY_HASHES) + ["src/SPOMOC.f90"]


class PhaseA8Error(RuntimeError):
    """Raised when an A8 contract is not closed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PhaseA8Error(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(data: dict[str, Any]) -> str:
    work = json.loads(json.dumps(data))
    for key in work["hash_freeze"]:
        work["hash_freeze"][key] = "PLACEHOLDER"
    payload = json.dumps(
        work, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def compact(source: str) -> str:
    return re.sub(r"\s+", " ", source.upper())


def fortran_code(source: str) -> str:
    """Remove free-form comments before structural checks."""
    return "\n".join(line.split("!", 1)[0] for line in source.splitlines())


def dense(source: str) -> str:
    return ";".join(
        re.sub(r"[\s&]+", "", statement.upper())
        for statement in unfolded_statements(source)
    )


def routine_args(source: str, name: str) -> list[str]:
    region = routine_region(source, name)
    match = re.search(
        rf"(?is)\bsubroutine\s+{re.escape(name)}\s*\((.*?)\)",
        region,
    )
    require(match is not None, f"missing header for {name}")
    return [re.sub(r"[\s&]+", "", item).upper()
            for item in match.group(1).split(",")]


def call_sites(source: str, name: str) -> list[tuple[int, int, list[str]]]:
    """Return CALL spans and top-level actual lists for a free-form region."""
    code = fortran_code(source)
    sites: list[tuple[int, int, list[str]]] = []
    pattern = re.compile(rf"(?i)\bcall\s+{re.escape(name)}\s*\(")
    for match in pattern.finditer(code):
        depth = 1
        quote = ""
        item_start = match.end()
        actuals: list[str] = []
        index = item_start
        while index < len(code) and depth:
            char = code[index]
            if quote:
                if char == quote:
                    if index + 1 < len(code) and code[index + 1] == quote:
                        index += 1
                    else:
                        quote = ""
            elif char in ("'", '"'):
                quote = char
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    actuals.append(code[item_start:index])
                    break
            elif char == "," and depth == 1:
                actuals.append(code[item_start:index])
                item_start = index + 1
            index += 1
        require(depth == 0, f"unterminated call {name}")
        normalized = [re.sub(r"[\s&]+", "", item).upper()
                      for item in actuals]
        sites.append((match.start(), index + 1, normalized))
    return sites


def unfolded_statements(source: str) -> list[str]:
    statements: list[str] = []
    buffer = ""
    for raw_line in fortran_code(source).splitlines():
        line = raw_line.strip()
        if not line:
            continue
        leading = line.startswith("&")
        trailing = line.endswith("&")
        if leading:
            line = line[1:].lstrip()
        if trailing:
            line = line[:-1].rstrip()
        buffer = f"{buffer} {line}".strip() if buffer else line
        if not trailing:
            statements.extend(part.strip() for part in buffer.split(";")
                              if part.strip())
            buffer = ""
    require(not buffer, "unterminated Fortran continuation")
    return statements


def normalized_statements(source: str) -> list[str]:
    """Return comment-free, case/spacing-insensitive Fortran statements."""
    return [re.sub(r"\s+", "", statement.upper())
            for statement in unfolded_statements(source)]


def assignments_to(statements: list[str], name: str) -> list[str]:
    """Return normalized statements that define NAME directly."""
    pattern = re.compile(
        rf"(?<![A-Z0-9_]){re.escape(name)}(?:\([^=]*\))?=(?!=)"
    )
    return [statement for statement in statements
            if pattern.search(statement) is not None]


def reject_hidden_math_control(source: str, routines: tuple[str, ...]) -> None:
    """Reject simple alias/dead-branch wrappers around frozen mathematics."""
    for routine in routines:
        for statement in normalized_statements(
                routine_region(source, routine)):
            require(re.match(
                r"^(?:[A-Z][A-Z0-9_]*:)?ASSOCIATE\(", statement
            ) is None, f"{routine} forbids ASSOCIATE aliases")
            require(re.match(
                r"^(?:[A-Z][A-Z0-9_]*:)?BLOCK$", statement
            ) is None, f"{routine} forbids BLOCK wrappers")
            require(re.match(
                r"^(?:[A-Z][A-Z0-9_]*:)?IF\(\.FALSE\.\)THEN$",
                statement,
            ) is None, f"{routine} forbids literal-false dead branches")


def require_statement_subsequence(
        statements: list[str], expected: list[str], label: str) -> list[int]:
    """Require an ordered semantic sequence while allowing guard detail between."""
    positions: list[int] = []
    cursor = -1
    for wanted in expected:
        try:
            cursor = statements.index(wanted, cursor + 1)
        except ValueError as error:
            raise PhaseA8Error(f"{label}: missing or reordered {wanted}") \
                from error
        positions.append(cursor)
    return positions


def require_exact_calls(
        source: str, name: str, expected: list[list[str]],
        label: str) -> list[tuple[int, int, list[str]]]:
    """Require exact call count, ordering and top-level actual lists."""
    sites = call_sites(source, name)
    require([site[2] for site in sites] == expected,
            f"{label}: exact {name} call actuals/order")
    return sites


def statement_contexts(source: str) -> list[tuple[str, tuple[str, ...]]]:
    """Track the enclosing DO/IF blocks for each normalized statement."""
    contexts: list[tuple[str, tuple[str, ...]]] = []
    stack: list[tuple[str, str]] = []
    for statement in normalized_statements(source):
        if statement == "ENDDO":
            require(stack and stack[-1][0] == "DO",
                    "unbalanced END DO in checked source")
            stack.pop()
            contexts.append((statement, tuple(item[1] for item in stack)))
            continue
        if statement == "ENDIF":
            require(stack and stack[-1][0] == "IF",
                    "unbalanced END IF in checked source")
            stack.pop()
            contexts.append((statement, tuple(item[1] for item in stack)))
            continue

        contexts.append((statement, tuple(item[1] for item in stack)))
        if re.match(r"^DO(?:WHILE\(|[A-Z][A-Z0-9_]*=)", statement):
            stack.append(("DO", statement))
        elif statement.startswith("IF(") and statement.endswith(")THEN"):
            stack.append(("IF", statement))
    require(not stack, "unbalanced checked Fortran block")
    return contexts


def require_immediate_map_guards(
        source: str, routine: str, map_name: str,
        expected: list[list[str]]) -> None:
    """Require each admitted record mapping to fail closed immediately."""
    region = routine_region(source, routine)
    require_exact_calls(region, map_name, expected, routine)
    statements = normalized_statements(region)
    for actuals in expected:
        call = f"CALL{map_name}(" + ",".join(actuals) + ")"
        require(statements.count(call) == 1,
                f"{routine}: unique {map_name} mapping {actuals[1]}")
        position = statements.index(call)
        require(position + 1 < len(statements) and
                statements[position + 1] == "IF(.NOT.MAP_OK)RETURN",
                f"{routine}: immediate fail-closed map guard {actuals[1]}")


def validate_status_abi(source: str, name: str) -> None:
    region = routine_region(source, name)
    args = routine_args(source, name)
    require(args[-2:] == ["CUTOFF_DELTA64", "OK"],
            f"{name} status dummies must be final")
    code = dense(region)
    require("INTEGER(INT64),INTENT(OUT)::CUTOFF_DELTA64" in code,
            f"{name} int64 delta declaration")
    require("LOGICAL,INTENT(OUT)::OK" in code,
            f"{name} logical status declaration")
    delta_init = [match.start() for match in re.finditer(
        r"(?<![A-Z0-9_])CUTOFF_DELTA64=0_INT64", code)]
    ok_init = [match.start() for match in re.finditer(
        r"(?<![A-Z0-9_])OK=\.FALSE\.", code)]
    ok_success = [match.start() for match in re.finditer(
        r"(?<![A-Z0-9_])OK=\.TRUE\.", code)]
    require(len(delta_init) == 1, f"{name} unique delta entry reset")
    require(len(ok_init) == 1, f"{name} unique false entry status")
    require(ok_success, f"{name} has an explicit success status")
    first_exit = min(
        (pos for pos in (code.find("CALL"), code.find("RETURN"))
         if pos >= 0),
        default=len(code),
    )
    require(delta_init[0] < first_exit and ok_init[0] < first_exit,
            f"{name} entry status precedes call/return")
    require(all(position > ok_init[0] for position in ok_success),
            f"{name} success order")
    ok_assignments = re.findall(
        r"(?<![A-Z0-9_])OK=(\.[A-Z]+\.)", code
    )
    ok_assignment_count = len(re.findall(
        r"(?<![A-Z0-9_])OK=", code
    ))
    require(len(ok_assignments) == ok_assignment_count and
            set(ok_assignments) <= {".FALSE.", ".TRUE."},
            f"{name} status is literal and fail-closed")


def validate_delta_assignments(
        source: str, name: str, child_additions: int,
        leaf_increments: int = 0) -> None:
    region = routine_region(source, name)
    assignments: list[str] = []
    for statement in unfolded_statements(region):
        match = re.search(
            r"(?i)\bCUTOFF_DELTA64\s*=\s*(.+)$", statement
        )
        if match:
            assignments.append(re.sub(r"\s+", "", match.group(1)).upper())
    expected = (["0_INT64"] +
                ["CUTOFF_DELTA64+CHILD_DELTA64"] * child_additions +
                ["CUTOFF_DELTA64+1_INT64"] * leaf_increments)
    require(assignments == expected,
            f"{name} exact delta reset/addition sequence")


def validate_child_status_edge(
        source: str, parent: str, child: str, expected_calls: int) -> None:
    region = routine_region(source, parent)
    sites = call_sites(region, child)
    require(len(sites) == expected_calls,
            f"{parent}->{child} exact call count")
    code = fortran_code(region)
    add_pattern = re.compile(
        r"(?i)\bcutoff_delta64\s*=\s*cutoff_delta64\s*\+\s*"
        r"child_delta64\b"
    )
    check_pattern = re.compile(
        r"(?i)\bif\s*\(\s*\.not\.\s*child_ok\s*\)\s*return\b"
    )
    additions = list(add_pattern.finditer(code))
    require(len(additions) == expected_calls,
            f"{parent}->{child} one delta addition per call")
    for index, (start, end, actuals) in enumerate(sites):
        segment_end = sites[index + 1][0] if index + 1 < len(sites) \
            else len(code)
        segment_additions = [item for item in additions
                             if end < item.start() < segment_end]
        segment_checks = list(check_pattern.finditer(
            code, segment_additions[0].end() if segment_additions else end,
            segment_end,
        ))
        require(actuals[-2:] == ["CHILD_DELTA64", "CHILD_OK"],
                f"{parent}->{child} status actual order")
        require(len(segment_additions) == 1 and segment_checks,
                f"{parent}->{child} status consumed in call segment")
        require(end < segment_additions[0].start() <
                segment_checks[0].start(),
                f"{parent}->{child} call/add/check order")
        require(re.search(r"(?i)\breturn\b",
                          code[end:segment_additions[0].start()]) is None,
                f"{parent}->{child} no return before delta addition")
        require(re.search(
            r"(?i)\breturn\b",
            code[segment_additions[0].end():segment_checks[0].start()],
        ) is None, f"{parent}->{child} no return before status check")


def validate_nconv_monotonicity(source: str) -> None:
    region = routine_region(source, "MCGMRE64")
    assignments = []
    for statement in unfolded_statements(region):
        match = re.search(
            r"(?i)\b(NCONV(?:\([^)]*\))?)\s*=\s*(?!=)(.+)$",
            statement,
        )
        if match:
            lhs = re.sub(r"\s+", "", match.group(1)).upper()
            rhs = re.sub(r"\s+", "", match.group(2)).upper()
            assignments.append((lhs, rhs))
    require(assignments, "MCGMRE64 must update NCONV")
    for lhs, rhs in assignments:
        require(rhs.startswith(lhs + ".AND."),
                "MCGMRE64 NCONV updates must preserve false inputs")


def validate_mcgmre_exact_contract(source: str) -> None:
    """Lock the three-role REAL64 GMRES state machine and algebra."""
    region = routine_region(source, "MCGMRE64")
    statements = normalized_statements(region)

    common = [
        "KPSYS", "IPTRK", "IFTRAK", "IPRINT", "NGEFF", "NGIND",
        "NUN", "NBTR", "NMAX", "NMU", "NANGL", "NBATCH", "LC",
        "MATALB_TRK", "KEYFLX_TRK3", "KEYCUR_TRK1", "NZON_TRK1",
        "VOLUME_TRK32", "CAZ1_TRACK64", "CAZ2_TRACK64", "CPO32",
        "ZMU32", "WZMU32", "SC_BY_GROUP32", "SIGAL32", "QFR64",
    ]
    tail = ["SOURCE64", "NCONV", "EPSINTO64", "CHILD_DELTA64",
            "CHILD_OK"]
    response_calls = require_exact_calls(region, "MCGFL164", [
        common + ["PHIIN64", tail[0], "RESPONSE64"] + tail[1:],
        common + ["RHS64", tail[0], "FLOUT64"] + tail[1:],
        common + ["GAR64", tail[0], "FLOUT64"] + tail[1:],
    ], "MCGMRE64")
    role_calls = require_exact_calls(region, "SPOMOC_SET_ROLE", [
        ["1", "ITER"], ["2", "ITER"], ["3", "ITER"],
    ], "MCGMRE64")
    require(role_calls[0][0] < response_calls[0][0] <
            role_calls[1][0] < response_calls[1][0] <
            role_calls[2][0] < response_calls[2][0],
            "MCGMRE64 exact role/call lexical order")
    publish = require_exact_calls(
        region, "SPOMOC_PUBLISH", [[""]], "MCGMRE64"
    )
    require(response_calls[0][1] < publish[0][0] < role_calls[1][0],
            "MCGMRE64 publish follows the primary response only")

    contexts = statement_contexts(region)
    response_contexts = [context for statement, context in contexts
                         if statement.startswith("CALLMCGFL164(")]
    require(len(response_contexts) == 3,
            "MCGMRE64 three response-call block contexts")
    outer_loop = "DOWHILE(LNCONV/=0.AND.ITER<MAXIT)"
    inner_loop = (
        "DOWHILE(LNCONV/=0.AND.K<NSTART.AND.ITER<MAXIT)"
    )
    rhs_block = "IF(RHS_PENDING)THEN"
    require(outer_loop in response_contexts[0] and
            rhs_block not in response_contexts[0] and
            inner_loop not in response_contexts[0],
            "MCGMRE64 primary response role context")
    require(outer_loop in response_contexts[1] and
            rhs_block in response_contexts[1] and
            inner_loop not in response_contexts[1],
            "MCGMRE64 one-time RHS role context")
    require(outer_loop in response_contexts[2] and
            inner_loop in response_contexts[2] and
            rhs_block not in response_contexts[2],
            "MCGMRE64 Arnoldi role context")

    pending_assignments = [statement for statement in statements
                           if statement.startswith("RHS_PENDING=")]
    require(pending_assignments == [
        "RHS_PENDING=.TRUE.", "RHS_PENDING=.FALSE.",
    ], "MCGMRE64 one-shot RHS_PENDING assignment sequence")
    require(statements.count(rhs_block) == 1,
            "MCGMRE64 unique one-time RHS branch")
    rhs_copy = "IF(NCONV(II))RHS64(:,II)=FLOUT64(:,II)"
    require(statements.count("RHS64=+0.0_REAL64") == 1 and
            statements.count(rhs_copy) == 1,
            "MCGMRE64 exact one-time RHS population")
    rhs_copy_context = [context for statement, context in contexts
                        if statement == rhs_copy]
    require(len(rhs_copy_context) == 1 and
            outer_loop in rhs_copy_context[0] and
            rhs_block in rhs_copy_context[0] and
            "DOII=1,NGEFF" in rhs_copy_context[0],
            "MCGMRE64 RHS copy is active-group guarded in one-time branch")

    residual = "RESIDUAL64(:,II)=RESPONSE64(:,II)-PHIIN64(:,II)"
    arnoldi = "V64(:,:,K+1)=V64(:,:,K)-FLOUT64+RHS64"
    require(statements.count(residual) == 1,
            "MCGMRE64 primary RESPONSE-PHIIN residual")
    require(statements.count(arnoldi) == 1,
            "MCGMRE64 Arnoldi V-FLOUT+RHS action")
    residual_context = [context for statement, context in contexts
                        if statement == residual]
    arnoldi_context = [context for statement, context in contexts
                       if statement == arnoldi]
    require(len(residual_context) == 1 and
            outer_loop in residual_context[0] and
            "DOII=1,NGEFF" in residual_context[0],
            "MCGMRE64 residual active-group loop")
    require(len(arnoldi_context) == 1 and
            outer_loop in arnoldi_context[0] and
            inner_loop in arnoldi_context[0],
            "MCGMRE64 Arnoldi action loop")

    norm = (
        "H64(K+1,K,II)=SQRT(DOT_PRODUCT(V64(:,II,K+1),"
        "V64(:,II,K+1)))"
    )
    mgs_sequence = [
        "DOJ=1,K",
        "H64(J,K,II)=DOT_PRODUCT(V64(:,II,J),V64(:,II,K+1))",
        "V64(:,II,K+1)=V64(:,II,K+1)-H64(J,K,II)*V64(:,II,J)",
        norm,
        "DOJ=1,K",
        "HR64=DOT_PRODUCT(V64(:,II,J),V64(:,II,K+1))",
        "H64(J,K,II)=H64(J,K,II)+HR64",
        "V64(:,II,K+1)=V64(:,II,K+1)-HR64*V64(:,II,J)",
        norm,
    ]
    require_statement_subsequence(statements, mgs_sequence,
                                  "MCGMRE64 two-pass MGS")
    require(statements.count(norm) == 2,
            "MCGMRE64 exactly two MGS norm evaluations")
    mgs_base = (outer_loop, inner_loop, "DOII=1,NGEFF")
    for statement in (
        "HR64=DOT_PRODUCT(V64(:,II,J),V64(:,II,K+1))",
        "H64(J,K,II)=H64(J,K,II)+HR64",
        "V64(:,II,K+1)=V64(:,II,K+1)-HR64*V64(:,II,J)",
    ):
        statement_blocks = [blocks for item, blocks in contexts
                            if item == statement]
        require(statement_blocks == [mgs_base + ("DOJ=1,K",)],
                f"MCGMRE64 live second-MGS context {statement}")
    norm_blocks = [blocks for item, blocks in contexts if item == norm]
    require(norm_blocks == [mgs_base, mgs_base],
            "MCGMRE64 both MGS norms remain on the live active path")

    givens_sequence = [
        "DOI=1,K-1",
        "W1=C64(I,II)*H64(I,K,II)-SN64(I,II)*H64(I+1,K,II)",
        "W2=SN64(I,II)*H64(I,K,II)+C64(I,II)*H64(I+1,K,II)",
        "H64(I,K,II)=W1",
        "H64(I+1,K,II)=W2",
        "ZNU64=SQRT(H64(K,K,II)**2+H64(K+1,K,II)**2)",
        "IF(ZNU64>0.0_REAL64)THEN",
        "C64(K,II)=H64(K,K,II)/ZNU64",
        "SN64(K,II)=-H64(K+1,K,II)/ZNU64",
        "H64(K,K,II)=C64(K,II)*H64(K,K,II)-"
        "SN64(K,II)*H64(K+1,K,II)",
        "H64(K+1,K,II)=+0.0_REAL64",
        "W1=C64(K,II)*G64(K,II)-SN64(K,II)*G64(K+1,II)",
        "W2=SN64(K,II)*G64(K,II)+C64(K,II)*G64(K+1,II)",
        "G64(K,II)=W1",
        "G64(K+1,II)=W2",
    ]
    require_statement_subsequence(statements, givens_sequence,
                                  "MCGMRE64 prior/new Givens sequence")

    backsolve_sequence = [
        "K=KMAX(II)",
        "IF(K==0)CYCLE",
        "G64(K,II)=G64(K,II)/H64(K,K,II)",
        "DOL=K-1,1,-1",
        "W1=G64(L,II)-DOT_PRODUCT(H64(L,L+1:K,II),G64(L+1:K,II))",
        "G64(L,II)=W1/H64(L,L,II)",
        "DOJ=1,K",
        "PHIIN64(:,II)=PHIIN64(:,II)+G64(J,II)*V64(:,II,J)",
    ]
    require_statement_subsequence(statements, backsolve_sequence,
                                  "MCGMRE64 KMAX backsolve/update")
    require(statements.count(
        "PHIIN64(:,II)=PHIIN64(:,II)+G64(J,II)*V64(:,II,J)"
    ) == 1, "MCGMRE64 unique direct REAL64 PHIIN update")

    expected_writes = {
        "RHS_PENDING": [
            "RHS_PENDING=.TRUE.",
            "RHS_PENDING=.FALSE.",
        ],
        "RHS64": [
            "RHS64=+0.0_REAL64",
            "IF(NCONV(II))RHS64(:,II)=FLOUT64(:,II)",
        ],
        "GAR64": ["GAR64=V64(:,:,K)"],
        "RESIDUAL64": [
            "RESIDUAL64(:,II)=RESPONSE64(:,II)-PHIIN64(:,II)",
        ],
        "V64": [
            "V64=+0.0_REAL64",
            "V64(:,II,1)=RESIDUAL64(:,II)/RHO64(II)",
            "V64(:,:,K+1)=V64(:,:,K)-FLOUT64+RHS64",
            "V64(:,II,K+1)=V64(:,II,K+1)-"
            "H64(J,K,II)*V64(:,II,J)",
            "V64(:,II,K+1)=V64(:,II,K+1)-HR64*V64(:,II,J)",
            "V64(:,II,K+1)=V64(:,II,K+1)/H64(K+1,K,II)",
        ],
        "H64": [
            "H64=+0.0_REAL64",
            "H64(J,K,II)=DOT_PRODUCT(V64(:,II,J),V64(:,II,K+1))",
            norm,
            "H64(J,K,II)=H64(J,K,II)+HR64",
            norm,
            "H64(I,K,II)=W1",
            "H64(I+1,K,II)=W2",
            "H64(K,K,II)=C64(K,II)*H64(K,K,II)-"
            "SN64(K,II)*H64(K+1,K,II)",
            "H64(K+1,K,II)=+0.0_REAL64",
        ],
        "HR64": [
            "HR64=DOT_PRODUCT(V64(:,II,J),V64(:,II,K+1))",
        ],
        "C64": [
            "C64=+0.0_REAL64",
            "C64(K,II)=H64(K,K,II)/ZNU64",
        ],
        "SN64": [
            "SN64=+0.0_REAL64",
            "SN64(K,II)=-H64(K+1,K,II)/ZNU64",
        ],
        "G64": [
            "G64=+0.0_REAL64",
            "G64(1,II)=RHO64(II)",
            "G64(K,II)=W1",
            "G64(K+1,II)=W2",
            "G64(K,II)=G64(K,II)/H64(K,K,II)",
            "G64(L,II)=W1/H64(L,L,II)",
        ],
        "W1": [
            "W1=C64(I,II)*H64(I,K,II)-SN64(I,II)*H64(I+1,K,II)",
            "W1=C64(K,II)*G64(K,II)-SN64(K,II)*G64(K+1,II)",
            "W1=G64(L,II)-DOT_PRODUCT(H64(L,L+1:K,II),"
            "G64(L+1:K,II))",
        ],
        "W2": [
            "W2=SN64(I,II)*H64(I,K,II)+C64(I,II)*H64(I+1,K,II)",
            "W2=SN64(K,II)*G64(K,II)+C64(K,II)*G64(K+1,II)",
        ],
        "ZNU64": [
            "ZNU64=SQRT(H64(K,K,II)**2+H64(K+1,K,II)**2)",
        ],
        "PHIIN64": [
            "PHIIN64(:,II)=PHIIN64(:,II)+G64(J,II)*V64(:,II,J)",
        ],
    }
    for name, expected in expected_writes.items():
        require(assignments_to(statements, name) == expected,
                f"MCGMRE64 exact {name} write sequence")

    maxit_statements = [statement for statement in statements
                        if "MAXIT" in statement]
    require(maxit_statements == [
        "IF(MAXI/=20.OR.NSTART/=10.OR.MAXIT/=19)RETURN",
        outer_loop,
        inner_loop,
    ], "MCGMRE64 MAXIT is a normal strict iteration cap")
    count_positions = [
        index for index, statement in enumerate(statements)
        if statement == "LNCONV=COUNT(NCONV)"
    ]
    require(count_positions, "MCGMRE64 maintains LNCONV from NCONV")
    final_count = max(count_positions)
    require(any(statement == "OK=.TRUE."
                for statement in statements[final_count + 1:]),
            "MCGMRE64 cap falls through to normal status")

    nconv_assignments = [statement for statement in statements
                         if statement.startswith("NCONV(") and
                         "=" in statement]
    convergence_update = (
        "NCONV(II)=NCONV(II).AND."
        "RHO64(II)>=EPSI64*DENOM64(II)"
    )
    require(nconv_assignments == [
        "NCONV(II)=NCONV(II).AND.DENOM64(II)>0.0_REAL64",
        convergence_update,
        convergence_update,
    ], "MCGMRE64 exact false-preserving NCONV assignments")


def validate_mccgf_frozen_contract(source: str) -> None:
    """Lock stored state bits and all checked MCGSIG prerequisites."""
    region = routine_region(source, "MCCGF64")
    statements = normalized_statements(region)

    integer_maps = [
        ["IPTRK", "'STATE-VECTOR'", "40", "STATE_VECTOR", "MAP_OK"],
        ["IPTRK", "'MCCG-STATE'", "40", "MCCG_STATE", "MAP_OK"],
        ["IPTRK", "'NZON$MCCG'", "NLONG", "NZON_TRK1", "MAP_OK"],
        ["IPTRK", "'KEYCUR$MCCG'", "NLONG-NREG", "KEYCUR_TRK1",
         "MAP_OK"],
        ["IPTRK", "'ICODE'", "NSOUT", "ICODE_TRK1", "MAP_OK"],
    ]
    real_maps = [
        ["IPTRK", "'REAL-PARAM'", "4", "REAL_PARAM32", "MAP_OK"],
        ["IPTRK", "'XMU$MCCG'", "NMU", "CPO_VIEW32", "MAP_OK"],
        ["IPTRK", "'WZMU$MCCG'", "NMU", "WZMU32", "MAP_OK"],
        ["IPTRK", "'ZMU$MCCG'", "NMU", "ZMU32", "MAP_OK"],
        ["IPTRK", "'V$MCCG'", "NLONG", "VOLUME_TRK32", "MAP_OK"],
        ["IPTRK", "'ALBEDO'", "NSOUT", "ALBEDO_TRK32", "MAP_OK"],
        ["KPSYS(I)", "'ALBEDO'", "NALBP", "GROUP_ALBEDO32",
         "MAP_OK"],
        ["KPSYS(I)", "'DRAGON-TXSC'", "NBMIX+1", "TXSC_RECORD32",
         "MAP_OK"],
        ["KPSYS(I)", "'DRAGON-S0XSC'", "NBMIX+1", "SC_RECORD32",
         "MAP_OK"],
    ]
    require_immediate_map_guards(source, "MCCGF64", "MAP_INTEGER1",
                                 integer_maps)
    require_immediate_map_guards(source, "MCCGF64", "MAP_REAL321",
                                 real_maps)
    require_immediate_map_guards(source, "MCCGF64", "MAP_INTEGER3", [[
        "IPTRK", "'KEYFLX$ANIS'", "NREG", "NLIN", "NFUNL",
        "KEYFLX_TRK3", "MAP_OK",
    ]])

    frozen_state = [
        "IF(STATE_VECTOR(1)/=NREG.OR.STATE_VECTOR(2)/=KPN)RETURN",
        "IF(STATE_VECTOR(3)/=1.OR.STATE_VECTOR(4)/=NBMIX)RETURN",
        "IF(STATE_VECTOR(5)/=NSOUT.OR.STATE_VECTOR(6)/=NANI)RETURN",
        "IF(STATE_VECTOR(9)/=0.OR.STATE_VECTOR(14)/=4)RETURN",
        "IF(STATE_VECTOR(16)/=2.OR.STATE_VECTOR(22)/=1)RETURN",
        "IF(STATE_VECTOR(27)/=0.OR.STATE_VECTOR(39)/=0)RETURN",
        "IF(STATE_VECTOR(40)/=0)RETURN",
        "IF(MCCG_STATE(2)/=4.OR.MCCG_STATE(3)/=KRYL)RETURN",
        "IF(MCCG_STATE(4)/=0.OR.MCCG_STATE(5)/=17)RETURN",
        "IF(MCCG_STATE(6)/=32.OR.MCCG_STATE(7)/=IAAC)RETURN",
        "IF(MCCG_STATE(8)/=ISCR.OR.MCCG_STATE(9)/=0)RETURN",
        "IF(MCCG_STATE(10)/=PACA.OR.MCCG_STATE(12)/=0)RETURN",
        "IF(MCCG_STATE(13)/=MAXI.OR.MCCG_STATE(15)/=STIS)RETURN",
        "IF(MCCG_STATE(16)/=NFUNL.OR.MCCG_STATE(18)/=0)RETURN",
        "IF(MCCG_STATE(19)/=NFUNL.OR.MCCG_STATE(20)/=NLIN)RETURN",
        "IF(1+10*MCCG_STATE(15)+100*(MCCG_STATE(20)-1)/=ISCH)RETURN",
    ]
    for guard in frozen_state:
        require(statements.count(guard) == 1,
                f"MCCGF64 frozen state guard {guard}")
    state_predicates = [
        statement for statement in statements
        if statement.startswith("IF(") and
        ("STATE_VECTOR(" in statement or "MCCG_STATE(" in statement)
    ]
    require(state_predicates == frozen_state,
            "MCCGF64 only the frozen state predicates")
    contexts = statement_contexts(region)
    for guard in frozen_state:
        guard_contexts = [context for statement, context in contexts
                          if statement == guard]
        require(guard_contexts == [()],
                f"MCCGF64 frozen state guard is top-level {guard}")
    require(assignments_to(statements, "STATE_VECTOR") == [] and
            assignments_to(statements, "MCCG_STATE") == [],
            "MCCGF64 mapped state snapshots are read-only")

    bounds_guard = "IF(J<1.OR.J>KPN)RETURN"
    seen_guard = "IF(SEEN(J))RETURN"
    require_statement_subsequence(statements, [
        "SEEN=.FALSE.",
        "DOI=1,NREG",
        "J=KEYFLX_TRK3(I,1,1)",
        bounds_guard,
        seen_guard,
        "SEEN(J)=.TRUE.",
        "ENDDO",
        "DOI=1,NLONG-NREG",
        "J=KEYCUR_TRK1(I)",
        bounds_guard,
        seen_guard,
        "SEEN(J)=.TRUE.",
        "ENDDO",
        "IF(.NOT.ALL(SEEN))RETURN",
    ], "MCCGF64 bounds-before-SEEN uniqueness loops")
    seen_contexts = [
        (statement, context) for statement, context in contexts
        if statement in (bounds_guard, seen_guard)
    ]
    require(seen_contexts == [
        (bounds_guard, ("DOI=1,NREG",)),
        (seen_guard, ("DOI=1,NREG",)),
        (bounds_guard, ("DOI=1,NLONG-NREG",)),
        (seen_guard, ("DOI=1,NLONG-NREG",)),
    ], "MCCGF64 bounds checks precede indexed SEEN reads")
    require(assignments_to(statements, "SEEN") == [
        "SEEN=.FALSE.", "SEEN(J)=.TRUE.", "SEEN(J)=.TRUE.",
    ], "MCCGF64 exact SEEN write sequence")

    real_parameter_guards = [
        "IF(TRANSFER(REAL_PARAM32(1),0_INT32)/="
        "INT(Z'3727C5AC',INT32))RETURN",
        "IF(.NOT.ALL(IEEE_IS_FINITE(REAL_PARAM32)))RETURN",
        "IF(TRANSFER(REAL_PARAM32(2),0_INT32)/=0_INT32)RETURN",
        "IF(TRANSFER(REAL_PARAM32(3),0_INT32)/=0_INT32)RETURN",
        "IF(TRANSFER(REAL_PARAM32(4),0_INT32)/=0_INT32)RETURN",
        "EPSI64=REAL(REAL_PARAM32(1),REAL64)",
        "IF(.NOT.IEEE_IS_FINITE(EPSI64).OR.EPSI64<=0.0_REAL64)RETURN",
    ]
    require_statement_subsequence(
        statements, frozen_state + real_parameter_guards,
        "MCCGF64 frozen STATE/MCCG-STATE/REAL-PARAM"
    )

    require_exact_calls(region, "LCMLEN", [
        ["KPSYS(1)", "'ALBEDO'", "NALBP", "ITYLCM"],
        ["KPSYS(I)", "'ALBEDO'", "J", "ITYLCM"],
    ], "MCCGF64")
    mcgsig = require_exact_calls(region, "MCGSIG", [[
        "IPTRK", "NBMIX", "NGEFF", "NALBP", "KPSYS", "SIGAL32",
        "LVOID",
    ]], "MCCGF64")
    begin = require_exact_calls(region, "SPOMOC_MCCGF_BEGIN", [[
        "NGRP", "NGEFF", "NGIND", "NUN", "NDIM", ".FALSE.",
        "NLONG", "NREG", "NSOUT", "NANI", "NLIN", "NFUNL", "KRYL",
        "STIS", "IAAC", "ISCR", "0", "PACA", "IDIR",
    ]], "MCCGF64")
    require(routine_args(source, "SPOMOC_MCCGF_BEGIN") == [
        "NGRP", "NGEFF", "NGIND", "NUN", "NDIM0", "CYCLIC",
        "NLONG", "NREG0", "NSOU", "NANI0", "NLIN0", "NFUNL0",
        "KRYL0", "STIS0", "IAAC0", "ISCR0", "IDIFC0", "PACA0",
        "IDIR0",
    ], "SPOMOC_MCCGF_BEGIN exact checked ABI")
    begin_statement = (
        "CALLSPOMOC_MCCGF_BEGIN(NGRP,NGEFF,NGIND,NUN,NDIM,.FALSE.,"
        "NLONG,NREG,NSOUT,NANI,NLIN,NFUNL,KRYL,STIS,IAAC,ISCR,0,PACA,"
        "IDIR)"
    )
    require_statement_subsequence(statements, [
        "READ(IFTRAK,IOSTAT=IOS)I,ISPEC,N2REG,N2SOU,NALBG,NCOR,"
        "NANGL,MXSUB,MXSEG",
        "IF(IOS/=0)RETURN",
        "IF(I/=NDIM.OR.N2REG/=NREG.OR.N2SOU/=NSOUT)RETURN",
        "IF(NCOR/=1.OR.NANGL<=0.OR.MXSUB<=0.OR.MXSEG<=0)RETURN",
        "IF(NALBG<0.OR.ISPEC<0.OR.LEN_TRIM(TEXT4)>4)RETURN",
        begin_statement,
        "ALLOCATE(MATALB_TRK(-NSOUT:NREG))",
    ], "MCCGF64 admitted-header BEGIN placement")
    flx_call = call_sites(region, "MCGFLX64")
    require(len(flx_call) == 1 and begin[0][0] < flx_call[0][0],
            "MCCGF64 BEGIN precedes inner solver dispatch")
    txsc_guard = (
        "IF(.NOT.RECORD_MATCHES(KPSYS(I),'DRAGON-TXSC',"
        "NBMIX+1,2))RETURN"
    )
    s0_guard = (
        "IF(.NOT.RECORD_MATCHES(KPSYS(I),'DRAGON-S0XSC',"
        "NBMIX+1,2))RETURN"
    )
    for guard in (txsc_guard, s0_guard):
        require(statements.count(guard) == 1,
                f"MCCGF64 exact group record guard {guard}")
    record_contexts = statement_contexts(region)
    for guard in (txsc_guard, s0_guard):
        context = [blocks for statement, blocks in record_contexts
                   if statement == guard]
        require(len(context) == 1 and "DOI=1,NGEFF" in context[0],
                f"MCCGF64 every-group admission {guard}")

    admission_tokens = [
        "CALLMAP_INTEGER1(IPTRK,'ICODE',NSOUT,ICODE_TRK1,MAP_OK)",
        "CALLMAP_REAL321(IPTRK,'ALBEDO',NSOUT,ALBEDO_TRK32,MAP_OK)",
        "CALLLCMLEN(KPSYS(1),'ALBEDO',NALBP,ITYLCM)",
        "IF(ANY(ICODE_TRK1>NALBP))RETURN",
        txsc_guard,
        "IF(NALBP==0)THEN",
        "CALLLCMLEN(KPSYS(I),'ALBEDO',J,ITYLCM)",
        "IF(J/=0)RETURN",
        "CALLMAP_REAL321(KPSYS(I),'ALBEDO',NALBP,GROUP_ALBEDO32,MAP_OK)",
        "CALLMAP_REAL321(KPSYS(I),'DRAGON-TXSC',NBMIX+1,"
        "TXSC_RECORD32,MAP_OK)",
        "IF(.NOT.ALL(IEEE_IS_FINITE(TXSC_RECORD32)))RETURN",
        "CALLMCGSIG(IPTRK,NBMIX,NGEFF,NALBP,KPSYS,SIGAL32,LVOID)",
    ]
    admission_positions = require_statement_subsequence(
        statements, admission_tokens, "MCCGF64 pre-MCGSIG admission"
    )
    mcgsig_statement = admission_positions[-1]
    require(all(position < mcgsig_statement
                for position in admission_positions[:-1]),
            "MCCGF64 ICODE/ALBEDO/TXSC admission precedes MCGSIG")
    require("ICODE_TRK1<0" not in compact(region),
            "MCCGF64 negative ICODE preserves tracking ALBEDO")
    require(mcgsig[0][0] > 0, "MCCGF64 checked MCGSIG call present")


def validate_mcgfl1_exact_contract(source: str) -> None:
    """Lock record maps, active loops, and exact transport actual roles."""
    region = routine_region(source, "MCGFL164")
    statements = normalized_statements(region)

    integer_maps = [
        ["IPTRK", "'BC-REFL+TRAN'", "NLONG-NREG", "BC_INDEX_TRK1",
         "MAP_OK"],
        ["IPTRK", "'IM$MCCG'", "NLONG+1", "IM", "MAP_OK"],
        ["IPTRK", "'MCU$MCCG'", "LC", "MCU", "MAP_OK"],
        ["IPTRK", "'PI$MCCG'", "NLONG", "IPERM", "MAP_OK"],
        ["IPTRK", "'JU$MCCG'", "NLONG", "JU", "MAP_OK"],
    ]
    real_maps = [
        ["KPSYS(I)", "'DIAGQ$MCCG'", "NLONG", "RECORD32", "MAP_OK"],
        ["KPSYS(I)", "'CQ$MCCG'", "LC", "RECORD32", "MAP_OK"],
        ["KPSYS(I)", "'ILUDF$MCCG'", "NLONG", "RECORD32", "MAP_OK"],
        ["KPSYS(I)", "'CF$MCCG'", "LC", "RECORD32", "MAP_OK"],
        ["KPSYS(I)", "'DIAGF$MCCG'", "NLONG", "RECORD32", "MAP_OK"],
    ]
    require_immediate_map_guards(source, "MCGFL164", "MAP_INTEGER1",
                                 integer_maps)
    require_immediate_map_guards(source, "MCGFL164", "MAP_INTEGER2", [[
        "IPTRK", "'PJJIND$MCCG'", "NFUNL", "2", "PJJIND_TRK2",
        "MAP_OK",
    ]])
    require_immediate_map_guards(source, "MCGFL164", "MAP_REAL321",
                                 real_maps)

    fcs = require_exact_calls(region, "MCGFCS64", [[
        "NLONG", "NDIM", "NZON_TRK1", "QFR64(:,I)", "PHIIN64(:,I)",
        "NBMIX", "NANI", "NLIN", "NFUNL", "SC_BY_GROUP32(:,:,I)",
        "SOURCE64(:,I)", "KPN", "NREG", "IPRINT", "KEYFLX_TRK3",
        "KEYCUR_TRK1", "BC_INDEX_TRK1", "SIGAL32(:,I)", "STIS",
        "CHILD_OK",
    ]], "MCGFL164")
    mocik3 = require_exact_calls(region, "MOCIK3", [[
        "NANI-1", "NFUNL", "4", "ISGNR", "KEYANI",
    ]], "MCGFL164")
    mcgfcf = require_exact_calls(region, "MCGFCF", [[
        "MCGFFIR64_RANK_ADAPTER", "MCGFFAR", "MCGFFAL", "MCGSCA",
        "IFTRAK", "NBTR", "NMAX", "NDIM", "KPN", "NLONG", "NREG",
        "NBMIX", "NGEFF", "NANGL", "NMU", "NANI", "NFUNL", "4",
        "NANI", "NLIN", "NFUNL", "KEYFLX_TRK3", "KEYCUR_TRK1",
        "NZON_TRK1", "NCONV", "CAZ0_INACTIVE64", "CAZ1_TRACK64",
        "CAZ2_TRACK64", "CPO32", "ZMU32", "WZMU32", "SOURCE64",
        "SIGAL32", "ISGNR", "IDIR", "NSOUT", "NBATCH",
        "XSI_INACTIVE64", "RESPONSE64",
    ]], "MCGFL164")
    mcgfst = require_exact_calls(region, "MCGFST", [[
        "NGEFF", "KPSYS", "NCONV", "KPN", "NLONG", "NREG", "NANI",
        "NFUNL", "NFUNL", "KEYFLX_TRK3(:,1,:)", "KEYCUR_TRK1",
        "PJJIND_TRK2", "NZON_TRK1", "VOLUME_TRK32", "SOURCE64",
        "RESPONSE64", "IDIR",
    ]], "MCGFL164")
    capture = require_exact_calls(region, "SPOMOC_CAPTURE64", [[
        "NGEFF", "NGIND", "NUN", "QFR64", "PHIIN64", "SOURCE64",
        "RESPONSE64", "NCONV",
    ]], "MCGFL164")
    aca = require_exact_calls(region, "MCGFCA64", [[
        "NLONG", "NGEFF", "KPN", "NREG", "NBMIX", "LC", "LFORW",
        "PACA", "KEYFLX_TRK3(:,1,:)", "KEYCUR_TRK1", "NZON_TRK1",
        "NCONV", "MAXACC", "EPSACC64", "RESPONSE64", "PHIIN64",
        "SC_BY_GROUP32", "IM", "MCU", "IPERM", "JU", "DIAGQ32",
        "CQ32", "ILUDF32", "CF32", "DIAGF32", "CHILD_DELTA64",
        "CHILD_OK",
    ]], "MCGFL164")
    chain_positions = [
        fcs[0][0], mocik3[0][0], mcgfcf[0][0], mcgfst[0][0],
        capture[0][0], aca[0][0],
    ]
    require(chain_positions == sorted(chain_positions),
            "MCGFL164 exact source/MOC/STIS/capture/ACA call order")

    skip_loop = "DOICOM=1,6"
    skip_read = "READ(IFTRAK,IOSTAT=IOS)"
    skip_guard = "IF(IOS/=0)RETURN"
    header_read = (
        "READ(IFTRAK,IOSTAT=IOS)I,ISPEC,N2REG,N2SOU,NALBG,NCOR,"
        "NANGL_CHECK,MXSUB,MXSEG"
    )
    mcgfcf_statement = "CALLMCGFCF(" + ",".join(mcgfcf[0][2]) + ")"
    require_statement_subsequence(statements, [
        "REWIND(IFTRAK,IOSTAT=IOS)",
        header_read,
        "IF(IOS/=0)RETURN",
        "IF(I/=NDIM.OR.N2REG/=NREG.OR.N2SOU/=NSOUT)RETURN",
        "IF(NCOR/=1.OR.NANGL_CHECK/=NANGL)RETURN",
        "IF(ISPEC<0.OR.NALBG<0.OR.MXSUB<=0.OR.MXSEG<=0)RETURN",
        skip_loop,
        skip_read,
        skip_guard,
        "ENDDO",
        mcgfcf_statement,
    ], "MCGFL164 exact six-record tracking skip before MCGFCF")
    tracking_contexts = statement_contexts(region)
    skip_loop_context = [context for statement, context in tracking_contexts
                         if statement == skip_loop]
    require(skip_loop_context == [()],
            "MCGFL164 tracking skip loop is top-level")
    skip_body = [
        (statement, context) for statement, context in tracking_contexts
        if skip_loop in context
    ]
    require(skip_body == [
        (skip_read, (skip_loop,)),
        (skip_guard, (skip_loop,)),
    ], "MCGFL164 exact six-record tracking skip body")

    moc_output = (
        "IF(KEYANI(1)/=0.OR..NOT.ALL(ISGNR(:,1)==1))RETURN"
    )
    require(statements.count(moc_output) == 1,
            "MCGFL164 checked MOCIK3 output")
    require(statements.index(moc_output) >
            statements.index("CALLMOCIK3(NANI-1,NFUNL,4,ISGNR,KEYANI)")
            and statements.index(moc_output) <
            statements.index("CALLMCGFCF(" + ",".join(mcgfcf[0][2]) + ")"),
            "MCGFL164 MOCIK3 output checked before MCGFCF")

    pjj_guard = (
        "IF(.NOT.RECORD_MATCHES(KPSYS(I),'PJJ$MCCG',"
        "NREG*NFUNL,2))RETURN"
    )
    require(statements.count(pjj_guard) == 1,
            "MCGFL164 exact active PJJ admission")
    contexts = statement_contexts(region)
    pjj_context = [blocks for statement, blocks in contexts
                   if statement == pjj_guard]
    fcs_context = [blocks for statement, blocks in contexts
                   if statement.startswith("CALLMCGFCS64(")]
    require(len(pjj_context) == 1 and
            pjj_context[0] == (
                "DOI=1,NGEFF", "IF(NCONV(I))THEN",
            ),
            "MCGFL164 PJJ admission active-group loop")
    require([statement for statement in statements
             if "'PJJ$MCCG'" in statement] == [pjj_guard],
            "MCGFL164 unique exact PJJ record predicate")
    require(len(fcs_context) == 1 and
            "DOI=1,NGEFF" in fcs_context[0] and
            "IF(NCONV(I))THEN" in fcs_context[0],
            "MCGFL164 source construction active-group loop")

    moc_context = [blocks for statement, blocks in contexts
                   if statement == moc_output]
    require(moc_context == [()],
            "MCGFL164 MOCIK3 output guard is top-level and live")
    moc_predicates = [
        statement for statement in statements
        if statement.startswith("IF(") and
        ("KEYANI(" in statement or "ISGNR(" in statement)
    ]
    require(moc_predicates == [moc_output],
            "MCGFL164 unique exact MOCIK3 output predicate")
    require(assignments_to(statements, "KEYANI") == [] and
            assignments_to(statements, "ISGNR") == [],
            "MCGFL164 MOCIK3 outputs have no local overwrite")
    for actuals in real_maps:
        call = "CALLMAP_REAL321(" + ",".join(actuals) + ")"
        context = [blocks for statement, blocks in contexts
                   if statement == call]
        require(len(context) == 1 and "DOI=1,NGEFF" in context[0],
                f"MCGFL164 every-group PACA record mapping {actuals[1]}")


def validate_capture_interface(source: str) -> None:
    def has_declarator(code: str, prefix: str, declarator: str) -> bool:
        token = re.compile(
            rf"(?<![A-Z0-9_]){re.escape(declarator)}(?![A-Z0-9_])"
        )
        return any(
            statement.startswith(prefix) and
            token.search(statement[len(prefix):]) is not None
            for statement in code.split(";")
        )

    definitions = list(re.finditer(
        r"(?i)\bsubroutine\s+SPOMOC_CAPTURE64\s*\(", source
    ))
    require(len(definitions) == 1,
            "exactly one unresolved SPOMOC_CAPTURE64 interface")
    contains = re.search(r"(?i)^\s*contains\b", source, re.MULTILINE)
    require(contains is not None and definitions[0].start() < contains.start(),
            "SPOMOC_CAPTURE64 must remain an interface before CONTAINS")
    expected = [
        "NGEFF", "NGIND", "NUN", "QFR64", "EVAL64", "SOURCE64",
        "RAW64", "NCONV",
    ]
    require(routine_args(source, "SPOMOC_CAPTURE64") == expected,
            "exact SPOMOC_CAPTURE64 ABI order")
    region = routine_region(source, "SPOMOC_CAPTURE64")
    code = dense(region)
    for scalar in ("NGEFF", "NUN"):
        require(has_declarator(
            code, "INTEGER,INTENT(IN)::", scalar
        ), f"capture scalar integer dummy {scalar}")
    require(has_declarator(
        code, "INTEGER,INTENT(IN)::", "NGIND(NGEFF)"
    ), "capture NGIND shape")
    for array in ("QFR64", "EVAL64", "SOURCE64", "RAW64"):
        require(has_declarator(
            code, "REAL(REAL64),INTENT(IN)::",
            f"{array}(NUN,NGEFF)",
        ), f"capture REAL64 array {array}")
    require(has_declarator(
        code, "LOGICAL,INTENT(IN)::", "NCONV(NGEFF)"
    ), "capture NCONV shape")
    for token in ("OPTIONAL", "POINTER", "ALLOCATABLE", "BIND(C)"):
        require(token not in code, f"capture forbidden ABI token {token}")

    fl1 = routine_region(source, "MCGFL164")
    calls = call_sites(fl1, "SPOMOC_CAPTURE64")
    require(len(calls) == 1, "one capture call per response")
    require(calls[0][2] == [
        "NGEFF", "NGIND", "NUN", "QFR64", "PHIIN64", "SOURCE64",
        "RESPONSE64", "NCONV",
    ], "capture actual role order")

    probe_args = routine_args(source, "SPOR64_A8_CAPTURE_PROBE")
    require(probe_args == expected + ["OK"], "capture probe ABI")
    probe = dense(routine_region(source, "SPOR64_A8_CAPTURE_PROBE"))
    for scalar in ("NGEFF", "NUN"):
        require(has_declarator(
            probe, "INTEGER,INTENT(IN)::", scalar
        ), f"capture probe scalar integer dummy {scalar}")
    require(has_declarator(
        probe, "INTEGER,INTENT(IN)::", "NGIND(NGEFF)"
    ), "capture probe NGIND shape")
    for array in ("QFR64", "EVAL64", "SOURCE64", "RAW64"):
        require(has_declarator(
            probe, "REAL(REAL64),INTENT(IN)::",
            f"{array}(NUN,NGEFF)",
        ), f"capture probe REAL64 array {array}")
    require(has_declarator(
        probe, "LOGICAL,INTENT(IN)::", "NCONV(NGEFF)"
    ), "capture probe NCONV shape")
    require(has_declarator(
        probe, "LOGICAL,INTENT(OUT)::", "OK"
    ), "capture probe status")


def routine_region(source: str, name: str) -> str:
    pattern = re.compile(
        rf"(?is)\bsubroutine\s+{re.escape(name)}\b(.*?)"
        rf"\bend\s+subroutine\s+{re.escape(name)}\b"
    )
    match = pattern.search(source)
    require(match is not None, f"missing subroutine {name}")
    return match.group(0)


def validate(data: dict[str, Any], verify_hashes: bool = True) -> None:
    require(data.get("schema") == "spot-real64-phase-a8-v1", "schema")
    require(data.get("phase") == "A8", "phase")
    require(data.get("status") == EXPECTED_STATUS, "status boundary")
    require(data.get("locked_branch") == EXPECTED_LOCKED_BRANCH,
            "locked branch")

    authority = data.get("authority", {})
    require(authority.get("parent_commit") == BASELINE_COMMIT,
            "parent commit")
    require(authority.get("parent_receipt_sha256") ==
            EXPECTED_A7_RECEIPT_SHA256, "parent receipt hash")
    require(authority.get("transitive_a6_receipt_sha256") ==
            EXPECTED_A6_RECEIPT_SHA256, "transitive A6 receipt hash")
    require(authority.get("scope") ==
            "validation-only; no source below src is edited", "scope")

    addendum = data.get("a8_addendum", {})
    status_abi = addendum.get("status_abi", {})
    require(status_abi.get("nodes") == EXPECTED_STATUS_NODES,
            "status ABI nodes")
    require(status_abi.get("success_dummy") ==
            "logical, intent(out) :: OK", "OK ABI")
    require(status_abi.get("counter_dummy") ==
            "integer(int64), intent(out) :: CUTOFF_DELTA64",
            "counter ABI")
    capture = addendum.get("capture_boundary", {})
    require(capture.get("checked_a8_signature") ==
            "SPOMOC_CAPTURE64(NGEFF,NGIND,NUN,QFR64,EVAL64,"
            "SOURCE64,RAW64,NCONV)", "capture ABI order")
    require(capture.get("src_spomoc_sha256") == EXPECTED_SPOMOC_SHA256,
            "production capture boundary hash")
    require(capture.get("src_spomoc_changes_in_a8") == 0,
            "capture production boundary")
    require(capture.get("solver_feedback") is False,
            "capture feedback boundary")
    ddot = addendum.get("ddot_reuse", {})
    require(ddot.get("sha256") == EXPECTED_LEGACY_HASHES["Utilib/src/DDOT.f"],
            "DDOT freeze")
    require(ddot.get("replacement_by_intrinsic_allowed") is False,
            "DDOT replacement")
    require(data.get("legacy_source_hashes") == EXPECTED_LEGACY_HASHES,
            "checked legacy source hashes")
    require(data.get("ported_legacy_source_hashes") ==
            EXPECTED_PORTED_LEGACY_HASHES,
            "ported legacy source hashes")

    precision = data.get("precision_contract", {})
    require(precision.get("mutable_real64_to_real32_allowed") is False,
            "mutable downcast")
    require(precision.get("toolchain_guard") ==
            "kind(1.0)==real32 and kind(0.0d0)==real64",
            "kind guard")

    rank = data.get("rank_contract", {})
    require(rank.get("flat_or_sequence_association_allowed") is False,
            "rank shortcuts")
    require(rank.get("MCGFST_and_ACA_actual") ==
            "KEYFLX_TRK3(:,1,:), direct contiguous rank 2",
            "rank-two direct section")
    aca = data.get("aca_contract", {})
    require(aca.get("MCGPRA64_IM") == "IM(NLONG+1)", "IM extent")
    require(aca.get("CF32") == "CF32(LC), never CF32(N1)", "CF extent")
    require(aca.get("JU_partition_bounds") ==
            "IM(I)+1 <= JU(I) <= IM(I+1)+1 before MSRLUS1",
            "JU sparse triangular partition bounds")
    require(aca.get("biCGSTAB_rho_breakdown") ==
            "reject non-finite or exact zero; finite negative is valid",
            "BiCGSTAB rho sign semantics")
    records = data.get("record_admission", {})
    require(records.get("tracking_stream_entry") ==
            "rewind -> header/comments -> nine-integer geometry header -> "
            "exactly six skipped records -> MCGFCF",
            "tracking stream entry lifecycle")
    require(records.get("mcgsig", {}).get("ICODE_semantics") ==
            "ICODE<=0 preserves tracking ALBEDO; only ICODE>NALBP is "
            "rejected before MCGSIG",
            "MCGSIG ICODE admission semantics")

    gate = data.get("compile_gate", {})
    require(gate.get("objects_linked") == 0, "link count")
    require(gate.get("objects_executed") == 0, "execution count")
    require(gate.get("prerequisite_runners_executed") == 0,
            "prerequisite runners")
    require(gate.get("negative_contract_count") == len(EXPECTED_NEGATIVES),
            "negative count")
    require(gate.get("main_symbol_allowed") is False, "main boundary")

    if verify_hashes:
        freeze = data.get("hash_freeze", {})
        require("PLACEHOLDER" not in freeze.values(), "unfrozen hashes")
        require(freeze.get("implementation_sha256") == sha256(CORE),
                "core hash")
        require(freeze.get("aca_sha256") == sha256(ACA), "ACA hash")
        require(freeze.get("adapter_sha256") == sha256(ADAPTER),
                "adapter hash")
        require(freeze.get("runner_sha256") == sha256(RUNNER),
                "runner hash")
        require(freeze.get("canonical_manifest_sha256") ==
                canonical_sha256(data), "canonical hash")
        require(EXPECTED_CANONICAL_SHA256 == canonical_sha256(data),
                "checker canonical freeze")
        require(EXPECTED_IMPLEMENTATION_SHA256 == sha256(CORE),
                "checker core freeze")
        require(EXPECTED_ACA_SHA256 == sha256(ACA), "checker ACA freeze")
        require(EXPECTED_ADAPTER_SHA256 == sha256(ADAPTER),
                "checker adapter freeze")
        require(EXPECTED_RUNNER_SHA256 == sha256(RUNNER),
                "checker runner freeze")


def validate_core_source(source: str) -> None:
    upper = compact(source)
    reject_hidden_math_control(source, (
        "DOORFV64", "MCCGF64", "MCGFLX64", "MCGMRE64", "MCGFL164",
        "MCGFCS64",
    ))
    for name in (
        "DOORFV64", "MCCGF64", "MCGFLX64", "MCGMRE64", "MCGFL164",
        "MCGFCS64",
    ):
        routine_region(source, name)
    reject_hidden_math_control(source, (
        "DOORFV64", "MCCGF64", "MCGFLX64", "MCGMRE64", "MCGFL164",
        "MCGFCS64",
    ))
    for name in (
        "DOORFV64", "MCCGF64", "MCGFLX64", "MCGMRE64", "MCGFL164",
    ):
        validate_status_abi(source, name)
    for name, additions in (
        ("DOORFV64", 1), ("MCCGF64", 1), ("MCGFLX64", 1),
        ("MCGMRE64", 3), ("MCGFL164", 1),
    ):
        validate_delta_assignments(source, name, additions)
    for parent, child, count in (
        ("DOORFV64", "MCCGF64", 1),
        ("MCCGF64", "MCGFLX64", 1),
        ("MCGFLX64", "MCGMRE64", 1),
        ("MCGMRE64", "MCGFL164", 3),
        ("MCGFL164", "MCGFCA64", 1),
    ):
        validate_child_status_edge(source, parent, child, count)
    validate_capture_interface(source)
    validate_nconv_monotonicity(source)
    validate_mcgmre_exact_contract(source)
    validate_mccgf_frozen_contract(source)
    validate_mcgfl1_exact_contract(source)

    require("KIND(1.0) == REAL32" in upper, "default REAL kind guard")
    require("KIND(0.0D0) == REAL64" in upper, "double kind guard")
    require("USE SPOR64_A8_ACA" in upper, "ACA dependency")
    require(not re.search(r"\bUSE\s+SPOR64_A[1-7]\b", upper),
            "dependency on earlier validation modules")

    forbidden = (
        "PRINAM", "CALL MCGPRA(", "CALL SPOMOC_CAPTURE(",
        "XSIXYZ(:,0)", "SAVE ", "COMMON ", "PROGRAM ",
    )
    for token in forbidden:
        require(token not in upper, f"forbidden core token {token}")
    require(not re.search(r"REAL\s*\([^\n)]*,\s*REAL32\s*\)", upper),
            "REAL64-to-REAL32 conversion surface")

    door = compact(routine_region(source, "DOORFV64"))
    require("FUNKNO$USS" in door and "CALL MCCGF64" in door,
            "door admission/call")
    require("FGAR64" in door and "CALL PRINDM" in door,
            "REAL64 door diagnostics")
    require(door.index("CALL MCCGF64") < door.rindex("FLUX"),
            "scatter must follow child call")

    mccgf = compact(routine_region(source, "MCCGF64"))
    require("SC_BY_GROUP32" in mccgf, "SC owner")
    require("DRAGON-S0XSC" in mccgf, "SC source")
    require("CALL MCGSIG" in mccgf and "CALL MCGFLX64" in mccgf,
            "MCCGF children")
    require(mccgf.index("DRAGON-S0XSC") < mccgf.index("CALL MCGFLX64"),
            "SC gather order")
    for record in (
        "XMU$MCCG", "WZMU$MCCG", "ZMU$MCCG", "V$MCCG",
        "NZON$MCCG", "KEYCUR$MCCG", "KEYFLX$ANIS", "ICODE",
        "ALBEDO", "DRAGON-TXSC",
    ):
        require(record in mccgf, f"missing record admission {record}")
    require("TEMP64" in mccgf and "EPSI64" in mccgf,
            "REAL64 convergence diagnostic")

    flx = compact(routine_region(source, "MCGFLX64"))
    require(flx.count("SOURCE64 = 0.0_REAL64") == 1,
            "source positive-zero initialization")
    require("CALL PRINDM" in flx and "CALL MCGMRE64" in flx,
            "MCGFLX dispatch")

    mre = compact(routine_region(source, "MCGMRE64"))
    for token in (
        "NSTART", "MAXIT", "RHS64", "GAR64", "CALL MCGFL164",
        "CALL SPOMOC_SET_ROLE", "CALL SPOMOC_PUBLISH",
    ):
        require(token in mre, f"GMRES contract {token}")
    require("NCONV(II) = NCONV(II) .AND." in mre,
            "false convergence masks cannot reactivate")

    fl1 = compact(routine_region(source, "MCGFL164"))
    required_order = [
        "RESPONSE64 = 0.0_REAL64",
        "CALL MCGFCS64",
        "CALL MOCIK3",
        "CALL MCGFCF",
        "CALL MCGFST",
        "CALL SPOMOC_CAPTURE64",
        "CALL MCGFCA64",
    ]
    positions = [fl1.find(token) for token in required_order]
    require(all(pos >= 0 for pos in positions), "MCGFL164 call chain")
    require(positions == sorted(positions), "MCGFL164 call order")
    require("KEYFLX_TRK3(:,1,:)" in fl1, "direct STIS/ACA section")
    require("PJJIND_TRK2" in fl1, "rank-two PJJ mapping")
    require("CAZ0_INACTIVE64" in fl1 and "XSI_INACTIVE64" in fl1,
            "conforming inactive MOC storage")
    require("DRAGON-S0XSC" not in fl1, "downstream SC gather")

    fcs = compact(routine_region(source, "MCGFCS64"))
    require("REAL(SC32" in fcs and "REAL(SIGAL32" in fcs,
            "exact operator promotion")
    require("QN64" in fcs and "FI64" in fcs and "S64" in fcs,
            "REAL64 source roles")
    fcs_region = routine_region(source, "MCGFCS64")
    fcs_statements = normalized_statements(fcs_region)
    surface_formula = (
        "S64(IND)=REAL(SIGAL32(IBM),REAL64)*FI64(IND2)"
    )
    volume_formula = (
        "S64(IND)=QN64(IND)+REAL(SC32(IBM,1),REAL64)*FI64(IND)"
    )
    require(fcs_statements.count(surface_formula) == 1,
            "MCGFCS64 exact surface formula")
    require(fcs_statements.count(volume_formula) == 1,
            "MCGFCS64 exact volume formula")
    require([statement for statement in fcs_statements
             if statement.startswith("S64(")] ==
            [surface_formula, volume_formula],
            "MCGFCS64 has only the two frozen source assignments")
    branch = fcs_statements.index("IF(IBM<0)THEN")
    surface = fcs_statements.index(surface_formula)
    branch_else = fcs_statements.index("ELSE", branch + 1)
    volume = fcs_statements.index(volume_formula)
    branch_end = fcs_statements.index("ENDIF", branch_else + 1)
    require(branch < surface < branch_else < volume < branch_end,
            "MCGFCS64 formulas remain in their frozen material branches")
    fcs_contexts = statement_contexts(fcs_region)
    for formula in (surface_formula, volume_formula):
        contexts = [context for statement, context in fcs_contexts
                    if statement == formula]
        require(len(contexts) == 1 and
                "DOIR=1,N" in contexts[0] and
                "IF(IBM<0)THEN" in contexts[0],
                "MCGFCS64 formula loop/branch context")


def validate_aca_source(source: str) -> None:
    upper = compact(source)
    source_dense = dense(source)
    reject_hidden_math_control(source, (
        "MCGFCR64", "MCGPRA64", "MCGABG64", "MCGFCA64",
    ))
    for name in ("MCGFCR64", "MCGPRA64", "MCGABG64", "MCGFCA64"):
        routine_region(source, name)
    validate_status_abi(source, "MCGFCA64")
    validate_status_abi(source, "MCGABG64")
    validate_delta_assignments(source, "MCGFCA64", 1)
    validate_delta_assignments(source, "MCGABG64", 0, leaf_increments=4)
    validate_child_status_edge(source, "MCGFCA64", "MCGABG64", 1)
    for token in ("CALL MSRLUS1", "DDOT", "INTEGER(INT64)"):
        require(token in upper, f"ACA token {token}")
    for token in ("CALL MCGPRA(", "CALL MCGABG(", "PROGRAM ",
                  "SAVE ", "COMMON "):
        require(token not in upper, f"forbidden ACA token {token}")
    require(not re.search(r"REAL\s*\([^\n)]*,\s*REAL32\s*\)", upper),
            "ACA downcast")

    pra = compact(routine_region(source, "MCGPRA64"))
    require(re.search(r"IM\s*\(\s*NLONG\s*\+\s*1\s*\)", pra) is not None,
            "MCGPRA64 IM(NLONG+1)")
    require(re.search(
        r"(?<![A-Z0-9_])CF32\s*\(\s*LC\s*\)", pra
    ) is not None, "MCGPRA64 CF(LC)")
    pra_region = routine_region(source, "MCGPRA64")
    pra_statements = normalized_statements(pra_region)
    ju_guard = "IF(JU(I)<IM(I)+1.OR.JU(I)>IM(I+1)+1)RETURN"
    require(pra_statements.count(ju_guard) == 1,
            "MCGPRA64 exact JU partition guard")
    ju_contexts = [context for statement, context in
                   statement_contexts(pra_region) if statement == ju_guard]
    require(len(ju_contexts) == 1 and
            "DOI=1,NLONG" in ju_contexts[0],
            "MCGPRA64 JU guard covers every sparse row")
    ju_position = pra_statements.index(ju_guard)
    msrlus_positions = [index for index, statement in
                        enumerate(pra_statements)
                        if statement.startswith("CALLMSRLUS1(")]
    require(len(msrlus_positions) == 2 and
            ju_position < min(msrlus_positions),
            "MCGPRA64 validates JU before either MSRLUS1 call")

    abg = dense(routine_region(source, "MCGABG64"))
    require(
        "REAL(REAL32),PARAMETER::INHERITED_EPSMAX32=1.0E-7_REAL32"
        in source_dense,
        "inherited binary32 cutoff literal",
    )
    require(
        "REAL(REAL64),PARAMETER::INHERITED_EPSMAX64="
        "REAL(INHERITED_EPSMAX32,REAL64)" in source_dense,
        "inherited cutoff exact promotion",
    )
    require(
        "TRANSFER(INHERITED_EPSMAX32,0_INT32)==INT(Z'33D6BF95',INT32)"
        in source_dense,
        "inherited cutoff binary32 bit identity",
    )
    require(abg.count("INHERITED_EPSMAX64") == 3,
            "three live thresholds use the exact promoted cutoff")
    require("CUTOFF_DELTA64" in abg and "0_INT64" in abg,
            "cutoff delta ABI")
    require(abg.count("GUARD_LIVE=") == 4,
            "four production cutoff evaluations")
    require(abg.count("GUARD_ZERO=") == 4,
            "four zero-cutoff counterfactual evaluations")
    require(abg.count("GUARD_LIVE.NEQV.GUARD_ZERO") == 4,
            "four cutoff Boolean comparisons")
    require(abg.count(
        "CUTOFF_DELTA64=CUTOFF_DELTA64+1_INT64") == 4,
        "four count-only cutoff increments")
    require("IF(GUARD_ZERO" not in abg,
            "counterfactual must not control solver state")
    require("DOT_PRODUCT" not in abg,
            "MCGABG64 must retain checked DDOT reductions")
    require(
        "IF(.NOT.IEEE_IS_FINITE(RT1_64).OR."
        "ABS(RT1_64)<=0.0_REAL64.OR.ABS(WI64)<=0.0_REAL64)RETURN" in abg,
        "BiCGSTAB rho must admit finite negative values and reject exact zero",
    )
    require("RT1_64<=0.0_REAL64" not in abg,
            "BiCGSTAB rho sign must not be treated as a breakdown")

    fca = compact(routine_region(source, "MCGFCA64"))
    require("DIAGF_INACTIVE32" in fca and "LUCF_INACTIVE32" in fca,
            "conforming inactive real storage")
    require("IM0_INACTIVE" in fca and "MCU0_INACTIVE" in fca,
            "conforming inactive integer storage")
    require("CALL MCGFCR64" in fca and "CALL MCGABG64" in fca,
            "ACA call graph")


def validate_adapter_source(source: str) -> None:
    upper = compact(source)
    require(upper.startswith("SUBROUTINE MCGFFIR64_RANK_ADAPTER"),
            "global adapter")
    require("KEYFLX_TRK3(NREG,1,1)" in upper, "adapter rank-three dummy")
    require("KEYFLX_TRK3(:,:,1)" in upper, "adapter direct rank-two section")
    require("CALL MCGFFIR" in upper, "adapter child")
    for token in ("MODULE ", "BIND(C)", "OPTIONAL", "POINTER",
                  "ALLOCATABLE", "SAVE ", "COMMON ", "READ(",
                  "WRITE(", "OPEN("):
        require(token not in upper, f"adapter descriptor/state token {token}")


def validate_makefile_contract(source: str) -> None:
    baseline = subprocess.run(
        ["git", "show", f"{BASELINE_COMMIT}:Makefile"],
        cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout
    a7 = (
        ".PHONY: spot-real64-phase-a7\n"
        "spot-real64-phase-a7 :\n"
        "\tsh validation/iterative/real64_phase_a7/run_phase_a7.sh\n"
    )
    a8 = (
        ".PHONY: spot-real64-phase-a8\n"
        "spot-real64-phase-a8 :\n"
        "\tsh validation/iterative/real64_phase_a8/run_phase_a8.sh\n"
    )
    require(a7 in baseline, "A7 baseline block")
    require(source == baseline.replace(a7, a7 + a8),
            "Makefile must add only isolated A8 target")


def validate_production_tree_unchanged() -> None:
    diff = subprocess.run(
        ["git", "diff", "--quiet", BASELINE_COMMIT, "--", "src",
         "Utilib/src"],
        cwd=ROOT,
    )
    require(diff.returncode == 0,
            "production sources differ from the frozen A7 parent")
    status = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all", "--",
         "src", "Utilib/src"],
        cwd=ROOT, check=True, text=True, capture_output=True,
    ).stdout
    require(status == "", "production source tree is dirty")


def validate_runner_contract(source: str, verify_hash: bool = True) -> None:
    for flag in (
        "-std=f2008", "-pedantic-errors", "-Werror",
        "-Wimplicit-interface", "-Wimplicit-procedure",
        "-Wconversion-extra", "-Warray-temporaries", "-fimplicit-none",
        "-fcheck=all", "-ffp-contract=off", "-fno-fast-math",
    ):
        require(flag in source, f"runner flag {flag}")
    for forbidden in (
        "run_phase_a1.sh", "run_phase_a2.sh", "run_phase_a3.sh",
        "run_phase_a4.sh", "run_phase_a5.sh", "run_phase_a6.sh",
        "run_phase_a7.sh", "make -C", "rdragon", "Dragon", "\nld ",
        "\nar ", "ranlib",
    ):
        require(forbidden not in source, f"runner forbidden {forbidden}")
    for negative in EXPECTED_NEGATIVES:
        require(source.count(negative) == 1,
                f"unique negative compile coverage {negative}")
    require(source.count("-fdefault-real-8") == 1,
            "default real guard loop")
    require("SPOR64_A8_ACA SPOR64_A8 MCGFFIR64_RANK_ADAPTER" in source,
            "all A8 source objects reject default REAL promotion")
    for token in ("capture_nm", "audit_nm_lines", "extract_unresolved",
                  "extract_defined", "nm -g", "anchor_defined"):
        require(token in source, f"object symbol gate {token}")
    require("OBJECT-LINKS=0" in source and "DRAGON-RUNS=0" in source,
            "zero execution claims")
    if verify_hash:
        require(sha256(RUNNER) == EXPECTED_RUNNER_SHA256,
                "runner frozen hash")


def validate_receipt_scope() -> None:
    lines = [line for line in RECEIPT.read_text().splitlines() if line]
    paths = [line.split("  ", 1)[1] for line in lines]
    require(len(paths) == len(set(paths)), "duplicate receipt path")
    require("validation/iterative/real64_phase_a8/phase_a8_implementation_receipt.sha256"
            not in paths, "self-hashing receipt")
    require(paths == EXPECTED_RECEIPT_PATHS,
            "receipt scope/order must be exact")


def run_checks(verify_hashes: bool = True) -> None:
    data = json.loads(MANIFEST.read_text())
    validate(data, verify_hashes=verify_hashes)
    validate_core_source(CORE.read_text())
    validate_aca_source(ACA.read_text())
    validate_adapter_source(ADAPTER.read_text())
    validate_makefile_contract((ROOT / "Makefile").read_text())
    validate_production_tree_unchanged()
    validate_runner_contract(RUNNER.read_text(), verify_hash=verify_hashes)
    for path, expected in EXPECTED_LEGACY_HASHES.items():
        require(sha256(ROOT / path) == expected, f"legacy hash {path}")
    for path, expected in EXPECTED_PORTED_LEGACY_HASHES.items():
        require(sha256(ROOT / path) == expected,
                f"ported legacy hash {path}")
    require(sha256(ROOT / "src/SPOMOC.f90") == EXPECTED_SPOMOC_SHA256,
            "production SPOMOC boundary hash")
    for name in EXPECTED_NEGATIVES:
        require((HERE / name).is_file(), f"missing negative {name}")
    require(sha256(ROOT / "validation/iterative/real64_phase_a7/"
                   "phase_a7_implementation_receipt.sha256") ==
            EXPECTED_A7_RECEIPT_SHA256, "A7 receipt file hash")
    require(sha256(ROOT / "validation/iterative/real64_phase_a6/"
                   "phase_a6_implementation_receipt.sha256") ==
            EXPECTED_A6_RECEIPT_SHA256, "A6 receipt file hash")
    require(README.is_file(), "README")
    if verify_hashes:
        validate_receipt_scope()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-unfrozen", action="store_true")
    args = parser.parse_args()
    try:
        run_checks(verify_hashes=not args.allow_unfrozen)
    except (PhaseA8Error, KeyError, json.JSONDecodeError,
            subprocess.CalledProcessError) as exc:
        print(f"SPOR64 PHASE-A8 CHECK FAILURE: {exc}")
        return 1
    print("SPOR64 PHASE-A8 STATIC CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
