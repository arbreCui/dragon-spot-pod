#!/usr/bin/env python3
"""Fail-closed static contract for one bounded real RETURNED close."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DECK = HERE / "one_real_returned_close.x2m"
RUNNER = HERE / "run_phase_a9b_b2y_one_real_returned_close.sh"
BOUNDED = HERE / "run_bounded_b2y.py"
PUBLISHER = HERE / "publish_b2y_artifact.py"
ATTEMPT_RESULT = HERE / "attempt_result.txt"
MANIFEST = HERE / "precision_manifest.json"
HOST = ROOT / "data/SpotCloseR64.c2m"
FLU2DR = ROOT / "src/FLU2DR.f"

EXECUTION_SNAPSHOT_COMMIT = "5713f2eba8d267cb7eaaa36155b2888e07f19a32"
EXECUTED_WRAPPER_SHA256 = (
    "c8e7905aac3d4e24e41602b6809d5a8e066690f9b523416bf77df0eefa4ad7b1"
)
EXECUTED_RUNNER_SHA256 = (
    "148ee567be1ec3bedf4af5bf930595fa7f15ca72802f2ab1a40d4f964092b24c"
)

RETURNED_SHA256 = (
    "dd41a37d484b85612a495ff7b1f2233a53fbae1b462d89bd84db2a8809cef054"
)
RETURNED_BYTES = 231_572_260
TRACK_AX_SHA256 = (
    "101ba0ad64c91723fdeb002e62c6226347fcfaeff188e125d699d70e113febc7"
)
MACROLIB3_SHA256 = (
    "2e01e806683ce25b5771af055112dc86dcf147245abc5a5c3dceac4d9939373a"
)
BASIS_REF_SHA256 = (
    "dc65467731947901393f9fb7114b7cd2e956a9992bb97db18e665b47e7446504"
)
A9_MODULE_SHA256 = (
    "485c66a6f083d9c1a1cac39800acb110a1d4e82f559b3465e833150cd7ceaed8"
)
SPOMOC_MODULE_SHA256 = (
    "7e3754b1ae85c7d18ea123a387c4ecf80ce1439281ccebf315b215faa6609948"
)
B2Z_RECEIPT_SHA256 = (
    "2f003d175a2ff7eea2feb73cc87e46d83c1c11e1e09f97ebe228472f7d741844"
)
B2Z_RUNTIME_SHA256 = (
    "6627924e8bed19e23537ede946c3c7c2cc7dcf2f53b84055a4b8e047fe444850"
)
B2Z_ARTIFACT_MANIFEST_SHA256 = (
    "22949de59c8662c43ca7f7ec3293e27287571ae85b58ecddf24fc2148a67ca0f"
)


class GateError(AssertionError):
    """The narrow B2y execution contract was violated."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def read_required(path: Path) -> str:
    require(path.is_file(), f"required B2y input is missing: {path}")
    return path.read_text(encoding="utf-8")


def strip_fortran_comments(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        if line.lstrip().startswith("!"):
            continue
        if line and line[0] in "cC*":
            continue
        if len(line) >= 6 and line[:5].isspace() and line[5] not in {" ", "0"}:
            line = line[6:]
        lines.append(line.split("!", 1)[0])
    return "\n".join(lines)


def strip_deck_comments(text: str) -> str:
    return "\n".join(
        line for line in text.splitlines()
        if not line.lstrip().startswith("*")
    )


def strip_shell_comments(text: str) -> str:
    return "\n".join(
        line for line in text.splitlines()
        if not line.lstrip().startswith("#")
    )


def packed(text: str) -> str:
    return re.sub(r"[\s&]+", "", text).upper()


def require_order(owner: str, text: str, fragments: tuple[str, ...]) -> None:
    code = packed(text)
    position = -1
    for fragment in fragments:
        needle = packed(fragment)
        found = code.find(needle, position + 1)
        require(found > position, f"{owner}: missing or reordered {fragment}")
        position = found


def xsm_symbol_by_path(text: str) -> dict[str, str]:
    declarations = re.findall(
        r"(?is)\bXSM_FILE\s+([A-Za-z][A-Za-z0-9_]*)\s*::\s*"
        r"FILE\s*'([^']+)'\s*;",
        text,
    )
    result: dict[str, str] = {}
    for symbol, path in declarations:
        require(path not in result, f"duplicate XSM path in B2y deck: {path}")
        result[path] = symbol.upper()
    return result


def check_attempt_result(text: str) -> None:
    lines = [line for line in text.splitlines() if line]
    require(lines and lines[0] ==
            "SPOR64 PHASE-A9b-B2y UNIQUE ATTEMPT INVALID",
            "B2y attempt-result header differs")
    fields: dict[str, str] = {}
    for line in lines[1:]:
        require("=" in line, f"B2y attempt-result line lacks '=': {line}")
        key, value = line.split("=", 1)
        require(key and key not in fields,
                f"B2y attempt-result duplicate/empty key: {key}")
        fields[key] = value
    required = {
        "RECORD-KIND": "POST-HOC-STRUCTURED-FREEZE",
        "SCIENTIFIC-CLASSIFICATION": "INVALID-RUNTIME-EVIDENCE",
        "SCIENTIFIC-RESULT": "NONE",
        "CLASSIFICATION-BASIS": (
            "BOUNDED-WRAPPER-PASS-NO; "
            "SHELL-RUNTIME-CENSUS-NOT-REACHED"
        ),
        "POSTMORTEM-DESCRIPTION": "VALIDATION-HARNESS-FAILURE",
        "POSTMORTEM-CAUSE": (
            "POST-EXIT-PROCESS-OBSERVATION/CLEANUP-RACE"
        ),
        "ACCEPTED-CLOSED-RESULT": "NO",
        "AUTHORIZATION": (
            "CONSUMED ATTEMPTS=1 RETRIES=0 "
            "FUTURE-B2Y-ACTIVATION=FORBIDDEN"
        ),
        "DRAGON-LAUNCHES": (
            "1 BOUNDED-WRAPPER-PASS=NO BOUNDED-PASS-MARKERS=0"
        ),
        "SHELL-RUNTIME-CENSUS": (
            "NOT-REACHED POSTERIOR-EXECUTIONS=0"
        ),
        "SUCCESS-ARTIFACT-PUBLICATIONS": (
            "0 SUCCESS-ARTIFACT=ABSENT-AT-FREEZE"
        ),
        "VALID-CLOSED-PAIR": (
            "NOT-ESTABLISHED CLOSED-CONTENT=NOT-EVALUATED"
        ),
        "EXECUTION-SNAPSHOT-COMMIT": EXECUTION_SNAPSHOT_COMMIT,
        "EXECUTED-WRAPPER-SHA256": EXECUTED_WRAPPER_SHA256,
        "EXECUTED-RUNNER-SHA256": EXECUTED_RUNNER_SHA256,
        "RAW-DRAGON-LOG": "NOT-RETAINED",
        "CANDIDATE-AX-CLOSED": "NOT-RETAINED",
        "CANDIDATE-ARCHIVE-CLOSED": "NOT-RETAINED",
        "POSTERIOR-REPORTS": "NOT-PRODUCED",
        "ARTIFACT-MANIFEST": "NOT-PRODUCED",
        "ATOMIC-PUBLICATION": "NOT-PERFORMED",
    }
    for key, value in required.items():
        require(fields.get(key) == value,
                f"B2y attempt-result field differs: {key}")
    for index in range(1, 8):
        key = f"CONSOLE-TAIL-OBSERVATION-{index:02d}"
        require(key in fields, f"B2y attempt-result lacks {key}")
    require(fields.get("CONSOLE-TAIL-EVIDENTIARY-STATUS") == (
        "TRANSCRIBED-CONSOLE-ONLY; RAW-LOG-NOT-RETAINED; "
        "NOT-INDEPENDENTLY-VERIFIABLE; NOT-ACCEPTED-CLOSED-EVIDENCE"
    ), "B2y console-only evidentiary boundary differs")
    for index in range(1, 7):
        key = f"NOT-CLAIMED-{index:02d}"
        require(key in fields, f"B2y attempt-result lacks {key}")


def check_manifest(text: str) -> None:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        raise GateError(f"B2y manifest JSON is invalid: {error}") from error
    require(data.get("receipt") in {"pending", "frozen"},
            "B2y invalid-attempt receipt state differs")
    require(data.get("receipt_scope") ==
            "invalid-attempt-freeze-not-success",
            "B2y receipt scope differs")
    require("success_receipt" not in data and
            "attempt_freeze_receipt" not in data,
            "B2y manifest has conflicting receipt states")
    runtime = data.get("runtime_result", {})
    expected_runtime = {
        "status": "INVALID",
        "dragon_executions": 1,
        "scientific_classification": "INVALID-RUNTIME-EVIDENCE",
        "scientific_result": "NONE",
        "postmortem_description": "VALIDATION-HARNESS-FAILURE",
        "postmortem_cause": (
            "POST-EXIT-PROCESS-OBSERVATION/CLEANUP-RACE"
        ),
        "bounded_wrapper_pass": False,
        "shell_runtime_census_reached": False,
        "posterior_executions": 0,
        "success_artifact_publications": 0,
        "accepted_closed_result": False,
        "outer_picard_convergence": "NOT-EVALUATED",
    }
    require(runtime == expected_runtime,
            "B2y manifest actual runtime result differs")
    require(data.get("preflight_result", {}).get("scope") ==
            "execution-era-preflight-before-unique-attempt",
            "B2y historical preflight scope differs")
    require(data.get("post_attempt_freeze_validation") == {
        "status": "PASS",
        "directed_mutation_tests": 81,
        "default_off_compile_and_link": "PASS",
        "dragon_executions": 0,
        "spotcloser64_executions": 0,
        "axial_solves": 0,
        "outer_picard_maps": 0,
    }, "B2y post-attempt freeze validation differs")
    require(data.get("postmortem_wrapper_repair") == {
        "status": "PASS",
        "scope": (
            "future-validation-harness-only-not-used-by-unique-b2y-attempt"
        ),
        "wrapper_sha256": (
            "898b94fe1d546b5b9ac682a1ea91baa75bf627f1ace9f5bc4599d055c79f640a"
        ),
        "absolute_wall_deadline_extended": False,
        "esrch_exit_reconciliation": (
            "process.wait timeout equals only the remaining original "
            "hard-deadline budget"
        ),
        "cleanup": (
            "immediate SIGKILL, idempotent, non-masking, conservative "
            "EPERM classification"
        ),
        "directed_and_synthetic_tests": 91,
        "real_short_non_dragon_children": 1,
        "default_off_compile_and_link": "PASS",
        "independent_code_audit": "PASS",
        "dragon_executions": 0,
        "spotcloser64_executions": 0,
        "axial_solves": 0,
        "outer_picard_maps": 0,
        "empirical_or_model_parameters_added": 0,
        "scientific_reclassification_of_unique_attempt": False,
    }, "B2y postmortem wrapper repair record differs")
    attempt = data.get("attempt_freeze", {})
    required_attempt = {
        "authorization": "consumed",
        "attempts": 1,
        "retries": 0,
        "future_b2y_activation": False,
        "execution_snapshot_commit": EXECUTION_SNAPSHOT_COMMIT,
        "executed_wrapper_sha256": EXECUTED_WRAPPER_SHA256,
        "executed_runner_sha256": EXECUTED_RUNNER_SHA256,
        "raw_dragon_log_retained": False,
        "candidate_closed_files_retained": False,
        "artifact_manifest_produced": False,
        "solver_source_changed_for_attempt": False,
        "unique_attempt_used_pre_repair_wrapper": True,
        "postmortem_wrapper_repair_executed_in_b2y": False,
    }
    for key, value in required_attempt.items():
        require(attempt.get(key) == value,
                f"B2y manifest attempt field differs: {key}")
    require(data.get("required_runtime_census", {}).get("scope") ==
            "success-requirement-not-actual-execution",
            "B2y runtime census requirement scope differs")
    require(data.get("required_independent_posterior", {}).get("scope") ==
            "success-requirement-not-actual-execution",
            "B2y posterior requirement scope differs")
    classes = data.get("failure_classification", {})
    require(classes.get(
        "normal_end_with_bad_runtime_census_or_"
        "wrapper_process_observation_failure"
    ) == "INVALID-RUNTIME-EVIDENCE",
            "B2y wrapper-race classification differs")


def check_deck(text: str) -> None:
    clean = strip_deck_comments(text)
    code = packed(clean)
    paths = xsm_symbol_by_path(clean)
    required_paths = (
        "./returned.xsm",
        "./initial_axial_track.xsm",
        "./initial_axial_macrolib.xsm",
        "./basis_reference.xsm",
        "./ax_closed.xsm",
        "./archive_closed.xsm",
    )
    require(set(paths) == set(required_paths),
            "B2y deck XSM path inventory differs")
    require(len(set(paths.values())) == len(required_paths),
            "B2y deck reuses an XSM symbol")

    required_lists = (
        "RETURNED", "TRACK_AX", "MACROLIB3", "BASIS_REF",
        "AX_CLOSED", "ARCH_CLOSED",
    )
    linked = re.search(r"(?is)\bLINKED_LIST\s+(.*?)\s*;", clean)
    require(linked is not None, "B2y deck lacks its LINKED_LIST inventory")
    linked_names = re.findall(r"[A-Za-z][A-Za-z0-9_]*", linked.group(1))
    require(tuple(name.upper() for name in linked_names) == required_lists,
            "B2y deck LINKED_LIST inventory/order differs")
    require(code.count("PROCEDURESPOTCLOSER64;") == 1,
            "B2y deck must declare SpotCloseR64 exactly once")
    close_call = (
        "AX_CLOSEDARCH_CLOSED:=SPOTCLOSER64"
        "RETURNEDTRACK_AXMACROLIB3BASIS_REF::;"
    )
    require(code.count(close_call) == 1,
            "B2y deck must make one exact SpotCloseR64 call")
    require(code.count("SPOTCLOSER64") == 2,
            "B2y deck has an extra SpotCloseR64 reference")

    imports = (
        f"RETURNED:={paths['./returned.xsm']};",
        f"TRACK_AX:={paths['./initial_axial_track.xsm']};",
        f"MACROLIB3:={paths['./initial_axial_macrolib.xsm']};",
        f"BASIS_REF:={paths['./basis_reference.xsm']};",
    )
    outputs = (
        f"{paths['./ax_closed.xsm']}:=AX_CLOSED;",
        f"{paths['./archive_closed.xsm']}:=ARCH_CLOSED;",
    )
    for expression in (*imports, *outputs):
        require(code.count(expression) == 1,
                f"B2y deck expression differs: {expression}")
    require_order(
        "B2y deck",
        code,
        (*imports, close_call, *outputs),
    )

    forbidden = (
        "SPOTSTEPR64", "SPOR64T", "LK1D", "R64CONT", "R64BOOT",
        "WHILE", "REPEAT", "UNTIL", "RETRY", "FALLBACK", "RETUNE",
        "RELAX", "DAMP", "CLIP", "ALPHA", "OMEGA", "EXTE", "UNKT",
        "THER", "SPOD", "FIXB",
    )
    for token in forbidden:
        require(token not in code, f"forbidden B2y deck token: {token}")


def check_runner(text: str) -> None:
    clean = strip_shell_comments(text)
    clean = re.sub(r"\\\s*\n", " ", clean)
    code = packed(clean)
    required_assignments = (
        "RUN_B2Y=${RUN_B2Y:-0}",
        "B2Y_RETURNED_XSM=${B2Y_RETURNED_XSM:-}",
        f"EXPECTED_RETURNED_HASH={RETURNED_SHA256}",
        f"EXPECTED_RETURNED_BYTES={RETURNED_BYTES}",
        f"EXPECTED_TRACK_AX_HASH={TRACK_AX_SHA256}",
        f"EXPECTED_MACROLIB3_HASH={MACROLIB3_SHA256}",
        f"EXPECTED_BASIS_REF_HASH={BASIS_REF_SHA256}",
        f"EXPECTED_A9_MODULE_HASH={A9_MODULE_SHA256}",
        f"EXPECTED_SPOMOC_MODULE_HASH={SPOMOC_MODULE_SHA256}",
        f"EXPECTED_B2Z_RECEIPT_HASH={B2Z_RECEIPT_SHA256}",
        f"EXPECTED_B2Z_RUNTIME_HASH={B2Z_RUNTIME_SHA256}",
        "EXPECTED_B2Z_RUNTIME_BYTES=1735",
        f"EXPECTED_B2Z_ARTIFACT_MANIFEST_HASH={B2Z_ARTIFACT_MANIFEST_SHA256}",
        "EXPECTED_B2Z_ARTIFACT_MANIFEST_BYTES=483",
        f"EXECUTION_SNAPSHOT_COMMIT={EXECUTION_SNAPSHOT_COMMIT}",
        f"EXECUTED_WRAPPER_HASH={EXECUTED_WRAPPER_SHA256}",
        f"EXECUTED_RUNNER_HASH={EXECUTED_RUNNER_SHA256}",
    )
    for assignment in required_assignments:
        require(packed(assignment) in code,
                f"B2y runner missing frozen assignment: {assignment}")
    require(code.count("DRAGON_STARTED=0") == 1,
            "B2y runner lacks the unique pre-activation state")
    require(code.count("DRAGON_STARTED=1") == 1,
            "B2y runner lacks the unique activation transition")

    require(re.search(r'case\s+"?\$RUN_B2Y"?\s+in', clean) is not None,
            "B2y runner does not validate RUN_B2Y")
    activation_case = re.search(
        r'(?ms)case\s+"?\$RUN_B2Y"?\s+in\s*'
        r'0\)\s*;;\s*'
        r'1\)\s*fail\s+"B2y authorization was consumed; '
        r'future B2y activation is forbidden"\s*;;\s*'
        r'\*\)\s*fail\s+"RUN_B2Y must be exactly 0 or 1"\s*;;\s*esac',
        clean,
    )
    require(activation_case is not None,
            "B2y runner does not permanently reject reactivation")
    off = re.search(
        r'(?is)if\s+\[\s*"\$RUN_B2Y"\s*=\s*0\s*\]\s*;\s*then'
        r'.*?\bexit\s+0\b.*?\bfi\b',
        clean,
    )
    require(off is not None, "B2y default-OFF branch is missing")
    off_text = off.group(0)
    required_off = (
        "ACTIVATION=CONSUMED; FUTURE-B2Y-ACTIVATION=FORBIDDEN",
        "CURRENT-DEFAULT-OFF-CHECK DRAGON=0 SPOTCLOSE=0 ASM=0 "
        "FLU=0 AXIAL-SOLVE=0 PICARD=0",
        "HISTORICAL-B2Y-ATTEMPT DRAGON=1 ATTEMPTS=1 RETRIES=0 "
        "BOUNDED-WRAPPER-PASS=NO",
        "SCIENTIFIC-CLASSIFICATION=INVALID-RUNTIME-EVIDENCE "
        "SCIENTIFIC-RESULT=NONE",
        "SHELL-RUNTIME-CENSUS=NOT-REACHED POSTERIOR-EXECUTIONS=0 "
        "ARTIFACT-PUBLICATIONS=0 ACCEPTED-CLOSED=NO",
    )
    for fragment in required_off:
        require(packed(fragment) in packed(off_text),
                f"B2y default-OFF attempt summary differs: {fragment}")
    for stale in ("SET RUN_B2Y=1", "PENDING-REAL-ACTIVATION",
                  "ONE-REAL-SUPPLIED-RETURNED-CLOSE=NOT-EVALUATED"):
        require(stale not in text,
                f"B2y runner retains stale activation state: {stale}")
    require(activation_case.end() < off.start(),
            "B2y tracked reactivation rejection is not preflight-early")

    snapshot_fragments = (
        'RECEIPT="$HERE/phase_a9b_b2y_invalid_attempt_freeze_receipt.sha256"',
        'ATTEMPT_RESULT="$HERE/attempt_result.txt"',
        'git -C "$ROOT" merge-base --is-ancestor '
        '"$EXECUTION_SNAPSHOT_COMMIT" HEAD',
        'git -C "$ROOT" show "$EXECUTION_SNAPSHOT_COMMIT:$path"',
        'verify_execution_snapshot',
        'RECEIPT_STATE=PENDING-ATTEMPT-FREEZE',
        "count_exact 1 '^Ran 91 tests in [0-9.]+s$'",
    )
    for fragment in snapshot_fragments:
        require(packed(fragment) in code,
                f"B2y execution-snapshot gate missing: {fragment}")

    external_checks = (
        '[ -n "$B2Y_RETURNED_XSM" ]',
        '[ "$B2Y_RETURNED_XSM" = "$B2Z_RETURNED" ]',
        '[ -f "$B2Y_RETURNED_XSM" ]',
        '[ ! -L "$B2Y_RETURNED_XSM" ]',
        'require_hash "$B2Y_RETURNED_XSM" "$EXPECTED_RETURNED_HASH"',
        'copy_exact "$B2Y_RETURNED_XSM" "$CASE_DIR/returned.xsm"',
        'require_hash "$CASE_DIR/returned.xsm" "$EXPECTED_RETURNED_HASH"',
    )
    for fragment in external_checks:
        require(packed(fragment) in code,
                f"B2y external RETURNED guard missing: {fragment}")
    require(
        re.search(
            r'(?is)stat\s+-f\s+["\']?%z["\']?\s+'
            r'["\']?\$B2Y_RETURNED_XSM["\']?.*?'
            r'EXPECTED_RETURNED_BYTES',
            clean,
        ) is not None,
        "B2y external RETURNED byte-count guard is missing",
    )
    require(
        re.search(
            r'(?is)stat\s+-f\s+["\']?%z["\']?\s+'
            r'["\']?\$CASE_DIR/returned\.xsm["\']?.*?'
            r'EXPECTED_RETURNED_BYTES',
            clean,
        ) is not None,
        "B2y private RETURNED byte-count guard is missing",
    )

    b2z_evidence_fragments = (
        'B2Z_DIR="$ROOT/validation/iterative/'
        'real64_phase_a9b_b2z_one_real_returned_staging"',
        'B2Z_RECEIPT="$B2Z_DIR/'
        'phase_a9b_b2z_one_real_returned_staging_receipt.sha256"',
        'B2Z_RUNTIME_RESULT="$B2Z_DIR/runtime_result.txt"',
        'B2Z_ARTIFACT_DIR="$ARTIFACT_PARENT/iterative-b2z"',
        'B2Z_RETURNED="$B2Z_ARTIFACT_DIR/returned.xsm"',
        'B2Z_ARTIFACT_RUNTIME_RESULT="$B2Z_ARTIFACT_DIR/runtime_result.txt"',
        'B2Z_ARTIFACT_MANIFEST="$B2Z_ARTIFACT_DIR/artifact_manifest.sha256"',
        'B2Z_ATTEMPT_DIR="$ARTIFACT_PARENT/.iterative-b2z-attempted"',
        '[ -d "$B2Z_ARTIFACT_DIR" ]',
        '[ ! -L "$B2Z_ARTIFACT_DIR" ]',
        '[ -d "$B2Z_ATTEMPT_DIR" ]',
        '[ ! -L "$B2Z_ATTEMPT_DIR" ]',
        '[ -f "$path" ]',
        '[ ! -L "$path" ]',
        '[ -f "$B2Z_ARTIFACT_DIR/$file" ]',
        '[ ! -L "$B2Z_ARTIFACT_DIR/$file" ]',
        'find "$B2Z_ARTIFACT_DIR" -mindepth 1 -maxdepth 1',
        'require_hash "$B2Z_RECEIPT" "$EXPECTED_B2Z_RECEIPT_HASH"',
        'shasum -a 256 -c "$B2Z_RECEIPT"',
        'require_hash "$B2Z_RUNTIME_RESULT" "$EXPECTED_B2Z_RUNTIME_HASH"',
        'require_bytes "$B2Z_RUNTIME_RESULT" "$EXPECTED_B2Z_RUNTIME_BYTES"',
        'require_hash "$B2Z_ARTIFACT_RUNTIME_RESULT" '
        '"$EXPECTED_B2Z_RUNTIME_HASH"',
        'require_bytes "$B2Z_ARTIFACT_RUNTIME_RESULT" '
        '"$EXPECTED_B2Z_RUNTIME_BYTES"',
        'cmp "$B2Z_RUNTIME_RESULT" "$B2Z_ARTIFACT_RUNTIME_RESULT"',
        'require_hash "$B2Z_ARTIFACT_MANIFEST" '
        '"$EXPECTED_B2Z_ARTIFACT_MANIFEST_HASH"',
        'require_bytes "$B2Z_ARTIFACT_MANIFEST" '
        '"$EXPECTED_B2Z_ARTIFACT_MANIFEST_BYTES"',
        'shasum -a 256 -c artifact_manifest.sha256',
        'require_hash "$B2Z_RETURNED" "$EXPECTED_RETURNED_HASH"',
        'require_bytes "$B2Z_RETURNED" "$EXPECTED_RETURNED_BYTES"',
        '[ "$B2Y_RETURNED_XSM" = "$B2Z_RETURNED" ]',
    )
    for fragment in b2z_evidence_fragments:
        require(packed(fragment) in code,
                f"B2y B2z evidence gate missing: {fragment}")
    b2z_evidence = clean[
        clean.index("verify_b2z_frozen_evidence()"):
        clean.index("verify_b2z_staged_input()")
    ]
    for fragment in (
        '[ ! -L "$B2Z_ARTIFACT_DIR" ]',
        '[ ! -L "$B2Z_ATTEMPT_DIR" ]',
        'shasum -a 256 -c "$B2Z_RECEIPT"',
        'cmp "$B2Z_RUNTIME_RESULT" "$B2Z_ARTIFACT_RUNTIME_RESULT"',
        'cd "$B2Z_ARTIFACT_DIR"',
        'shasum -a 256 -c artifact_manifest.sha256',
        'require_hash "$B2Z_RETURNED" "$EXPECTED_RETURNED_HASH"',
    ):
        require(packed(fragment) in packed(b2z_evidence),
                f"B2y frozen B2z evidence function missing: {fragment}")
    b2z_staged = clean[
        clean.index("verify_b2z_staged_input()"):
        clean.index("verify_receipt()")
    ]
    require(packed('[ "$B2Y_RETURNED_XSM" = "$B2Z_RETURNED" ]') in
            packed(b2z_staged),
            "B2y canonical B2z path equality is outside the staged gate")
    require(packed("verify_b2z_frozen_evidence") in packed(b2z_staged),
            "B2y staged gate does not invoke frozen B2z evidence")
    staged_calls = list(re.finditer(
        r"(?m)^verify_b2z_staged_input\s*$", clean
    ))
    require(len(staged_calls) == 2,
            "B2y must verify canonical B2z staged input exactly twice")

    close_calls = re.findall(
        r'(?m)^\s*(?:if\s+!\s+)?python3\s+"?\$BOUNDED"?\s+close\b',
        clean,
    )
    require(code.count('PYTHON3"$BOUNDED"CLOSE') == 1,
            "B2y runner contains an extra close-profile launch token")
    require(len(close_calls) == 1,
            "B2y runner must launch exactly one close-profile child")
    close_position = clean.find(close_calls[0])
    require(close_position > off.end(),
            "B2y close child is reachable before the default-OFF exit")
    activation = re.search(
        r'(?m)^\s*DRAGON_STARTED=1\s*$\n'
        r'\s*if\s+!\s+python3\s+"?\$BOUNDED"?\s+close\b',
        clean,
    )
    require(activation is not None,
            "B2y activation state does not immediately guard the sole child")
    require(close_position > clean.find(external_checks[-1]),
            "B2y close child precedes the frozen RETURNED guards")

    for module in ("SPOR64V", "ASM", "FLU", "SPOSTATE", "SPOLEAK", "SPOR64X"):
        for direction, spacing in (("BEGIN", ""), ("END", "  ")):
            pattern = f"^->@{direction} MODULE {spacing}: {module}:"
            require(
                re.search(
                    rf'''runtime_count_exact\s+1\s+['"]{re.escape(pattern)}''',
                    clean,
                    re.IGNORECASE,
                ) is not None,
                f"B2y runner lacks exact {direction} census for {module}",
            )

    runtime_patterns = (
        "^ FLU2DR-TERM OUTER-GATE=PASS ",
        "^ FLU2DR-TERM INNER-TERMINAL ",
        "^>\\|B2Y-REAL-RETURNED-CLOSE-BEGIN",
        "^>\\|B2Y-REAL-RETURNED-CLOSE-COMPLETE",
    )
    for pattern in runtime_patterns:
        require(
            re.search(
                rf'''runtime_count_exact\s+1\s+['"]{re.escape(pattern)}''',
                clean,
                re.IGNORECASE,
            ) is not None,
            f"B2y runner lacks exact runtime census for {pattern}",
        )

    line_assignments = (
        ("BEGIN_LINE", "^>\\|B2Y-REAL-RETURNED-CLOSE-BEGIN"),
        ("V_BEGIN", "^->@BEGIN MODULE : SPOR64V:"),
        ("V_END", "^->@END MODULE   : SPOR64V:"),
        ("ASM_BEGIN", "^->@BEGIN MODULE : ASM:"),
        ("ASM_END", "^->@END MODULE   : ASM:"),
        ("FLU_BEGIN", "^->@BEGIN MODULE : FLU:"),
        ("OUTER_TERM_LINE", "^ FLU2DR-TERM OUTER-GATE=PASS "),
        ("INNER_TERM_LINE", "^ FLU2DR-TERM INNER-TERMINAL "),
        ("FLU_END", "^->@END MODULE   : FLU:"),
        ("STATE_BEGIN", "^->@BEGIN MODULE : SPOSTATE:"),
        ("STATE_END", "^->@END MODULE   : SPOSTATE:"),
        ("LEAK_BEGIN", "^->@BEGIN MODULE : SPOLEAK:"),
        ("LEAK_END", "^->@END MODULE   : SPOLEAK:"),
        ("X_BEGIN", "^->@BEGIN MODULE : SPOR64X:"),
        ("X_END", "^->@END MODULE   : SPOR64X:"),
        ("COMPLETE_LINE", "^>\\|B2Y-REAL-RETURNED-CLOSE-COMPLETE"),
    )
    for variable, pattern in line_assignments:
        require(
            re.search(
                rf'''(?m)^\s*{variable}=\$\(line_of\s+['"]'''
                rf'''{re.escape(pattern)}['"]''',
                clean,
            ) is not None,
            f"B2y runner lacks line binding for {variable}",
        )

    order_pairs = (
        ("BEGIN_LINE", "V_BEGIN"),
        ("V_BEGIN", "V_END"),
        ("V_END", "ASM_BEGIN"),
        ("ASM_BEGIN", "ASM_END"),
        ("ASM_END", "FLU_BEGIN"),
        ("FLU_BEGIN", "OUTER_TERM_LINE"),
        ("OUTER_TERM_LINE", "INNER_TERM_LINE"),
        ("INNER_TERM_LINE", "FLU_END"),
        ("FLU_END", "STATE_BEGIN"),
        ("STATE_BEGIN", "STATE_END"),
        ("STATE_END", "LEAK_BEGIN"),
        ("LEAK_BEGIN", "LEAK_END"),
        ("LEAK_END", "X_BEGIN"),
        ("X_BEGIN", "X_END"),
        ("X_END", "COMPLETE_LINE"),
    )
    previous = -1
    for left, right in order_pairs:
        comparison = rf'\[\s*"\${left}"\s*-lt\s*"\${right}"\s*\]'
        matches = list(re.finditer(comparison, clean))
        require(len(matches) == 1,
                f"B2y runner order comparison differs: {left} < {right}")
        require(matches[0].start() > previous,
                "B2y runner route-order comparisons are reordered")
        previous = matches[0].start()

    terminal_guards = (
        '[ "$IEXTF" -ge 2 ]', '[ "$IEXTF" -le 500 ]',
        '[ "$MAXOUT" -eq 500 ]', '[ "$EUNK_VALID" -eq 1 ]',
        '[ "$ITERF" -ge 1 ]', '[ "$ITERF" -le 740 ]',
        '[ "$MAXINR" -eq 740 ]', '[ "$IGDEB" -eq 371 ]',
        '[ "$INNER_STATE" -eq 1 ]', '[ "$NGRP" -eq 370 ]',
    )
    for guard in terminal_guards:
        require(packed(guard) in code,
                f"B2y runner terminal guard differs: {guard}")

    parser_fragments = (
        "OUTER_LINE=$(grep '^ FLU2DR-TERM OUTER-GATE=PASS ' "
        '"$CASE_DIR/dragon.log")',
        "OUTER_VALUES=$(printf '%s\\n' \"$OUTER_LINE\" | sed -E "
        "'s/^ FLU2DR-TERM OUTER-GATE=PASS IEXTF= *([0-9]+) "
        "MAXOUT= *([0-9]+).* EUNK-VALID=([0-9]+)$/\\1 \\2 \\3/')",
        "set -- $OUTER_VALUES",
        "INNER_LINE=$(grep '^ FLU2DR-TERM INNER-TERMINAL ' "
        '"$CASE_DIR/dragon.log")',
        "INNER_VALUES=$(printf '%s\\n' \"$INNER_LINE\" | sed -E "
        "'s/^ FLU2DR-TERM INNER-TERMINAL ITERF= *([0-9]+) "
        "MAXINR= *([0-9]+).* IGDEB= *([0-9]+) STATE=([0-9]+) "
        "NGRP= *([0-9]+)$/\\1 \\2 \\3 \\4 \\5/')",
        "set -- $INNER_VALUES",
    )
    for fragment in parser_fragments:
        require(packed(fragment) in code,
                f"B2y runner terminal parser differs: {fragment}")
    for variable in ("OUTER_LINE", "OUTER_VALUES", "INNER_LINE", "INNER_VALUES"):
        require(len(re.findall(rf"(?m)^\s*{variable}=", clean)) == 1,
                f"B2y runner parser assignment count differs: {variable}")
    require(len(re.findall(r"(?m)^\s*set\s+--\s+\$OUTER_VALUES\s*$", clean)) == 1,
            "B2y runner outer parser is not bound to set --")
    require(len(re.findall(r"(?m)^\s*set\s+--\s+\$INNER_VALUES\s*$", clean)) == 1,
            "B2y runner inner parser is not bound to set --")

    forbidden = (
        "RUN_B2V", "SPOTSTEPR64", "PREPARE_B2L_PROJECTED",
        "RADIAL-CONT", "MAX_RETRIES",
        "RETRY_COUNT", "FALLBACK", "RETUNE", "TOLERANCE_OVERRIDE",
    )
    for token in forbidden:
        require(token not in code, f"forbidden B2y runner token: {token}")
    require(re.search(r"(?im)^\s*(while|until)\b", clean) is None,
            "B2y shell runner contains a retry-capable loop")

    persistence_fragments = (
        'ARTIFACT_DIR="$ARTIFACT_PARENT/real64-phase-a9b-b2y"',
        'LOCK_DIR="$ARTIFACT_PARENT/.real64-phase-a9b-b2y.lock"',
        'ATTEMPT_DIR="$ARTIFACT_PARENT/.real64-phase-a9b-b2y-attempted"',
        'if ! mkdir "$ATTEMPT_DIR"',
        '[ ! -e "$ARTIFACT_DIR" ]',
        '[ ! -L "$ARTIFACT_DIR" ]',
        'if ! mkdir "$LOCK_DIR"',
        'LOCK_ID=$(stat -f \'%d:%i\' "$LOCK_DIR")',
        'ATTEMPT_ID=$(stat -f \'%d:%i\' "$ATTEMPT_DIR")',
        'PUBLISH_STAGE=$(mktemp -d '
        '"$ARTIFACT_PARENT/.real64-phase-a9b-b2y-publish.XXXXXX")',
        'PUBLISH_STAGE_ID=$(stat -f \'%d:%i\' "$PUBLISH_STAGE")',
        'copy_exact "$CASE_DIR/ax_closed.xsm" '
        '"$PUBLISH_STAGE/ax_closed.xsm"',
        'copy_exact "$CASE_DIR/archive_closed.xsm" '
        '"$PUBLISH_STAGE/archive_closed.xsm"',
        'copy_exact "$CASE_DIR/dragon.log" "$PUBLISH_STAGE/dragon.log"',
        'copy_exact "$CASE_DIR/posterior_a.log" '
        '"$PUBLISH_STAGE/posterior_a.log"',
        'copy_exact "$CASE_DIR/posterior_b.log" '
        '"$PUBLISH_STAGE/posterior_b.log"',
        'artifact_manifest.sha256',
        'FINAL_OWNED_ID=$(stat -f \'%d:%i\' "$ARTIFACT_DIR")',
        'cmp "$CASE_DIR/ax_closed.xsm" "$ARTIFACT_DIR/ax_closed.xsm"',
        'cmp "$CASE_DIR/archive_closed.xsm" '
        '"$ARTIFACT_DIR/archive_closed.xsm"',
        "owned_final_id=$PUBLISH_STAGE_ID",
        '[ "$(stat -f \'%d:%i\' "$ARTIFACT_DIR")" = "$owned_final_id" ]',
        "RETRY-AFTER-ANY-ATTEMPT=DISABLED",
    )
    for fragment in persistence_fragments:
        require(packed(fragment) in code,
                f"B2y persistence contract missing: {fragment}")
    publisher_call = (
        'python3 "$PUBLISHER" "$PUBLISH_STAGE" "$ARTIFACT_DIR"'
    )
    require(clean.count(publisher_call) == 1,
            "B2y publisher invocation count differs")
    off_position = clean.index('if [ "$RUN_B2Y" = 0 ]')
    lock_position = clean.index('if ! mkdir "$LOCK_DIR"')
    attempt_position = clean.index('if ! mkdir "$ATTEMPT_DIR"')
    close_position = clean.index('python3 "$BOUNDED" close ')
    posterior_b = clean.index(
        '"$CASE_DIR/posterior_b.log" returned.xsm ax_closed.xsm '
        'archive_closed.xsm'
    )
    final_lineage = clean.rfind("verify_frozen_build_inputs")
    stage_position = clean.index("PUBLISH_STAGE=$(mktemp -d")
    publish_position = clean.index(publisher_call)
    final_compare = clean.index(
        'cmp "$CASE_DIR/ax_closed.xsm" "$ARTIFACT_DIR/ax_closed.xsm"'
    )
    summary_position = clean.index(
        'sed -n \'1,80p\' "$ARTIFACT_DIR/runtime_result.txt"'
    )
    require(
        off_position < lock_position < staged_calls[0].start() < attempt_position <
        close_position < posterior_b < final_lineage < staged_calls[1].start() <
        stage_position < publish_position < final_compare < summary_position,
        "B2y persistence lifecycle order differs",
    )
    cleanup = clean[clean.index("cleanup()"):clean.index("LC_ALL=C")]
    for fragment in (
        'stat -f \'%d:%i\' "$ARTIFACT_DIR"',
        'stat -f \'%d:%i\' "$PUBLISH_STAGE"',
        'stat -f \'%d:%i\' "$LOCK_DIR"',
    ):
        require(fragment in cleanup,
                f"B2y owned rollback guard missing: {fragment}")
    preserve = cleanup.index("PRESERVE_B2Y_FAILURE")
    require(cleanup.index("FINAL_OWNED_ID") < preserve and
            cleanup.index("PUBLISH_STAGE_ID") < preserve and
            cleanup.index("LOCK_ID") < preserve,
            "B2y rollback must precede failure preservation")
    require('rm -rf "$ATTEMPT_DIR"' not in clean and
            'rmdir "$ATTEMPT_DIR"' not in clean,
            "B2y durable attempt sentinel must never be rolled back")


def check_publisher(text: str) -> None:
    required = (
        "renameatx_np",
        "RENAME_EXCL = 0x00000004",
        "AT_FDCWD = -2",
        "source.parent != target.parent",
        'lstat_absent(target, "publication target")',
        "stat.S_ISDIR(status.st_mode)",
        "stat.S_ISLNK(status.st_mode)",
        "source_status.st_dev != parent_status.st_dev",
        "published directory identity differs",
    )
    for fragment in required:
        require(fragment in text, f"B2y publisher missing {fragment}")
    for forbidden in ("os.replace(", "os.rename(", "shutil.move("):
        require(forbidden not in text,
                f"B2y publisher has overwrite fallback {forbidden}")
    require(text.count("result = rename(") == 1,
            "B2y publisher rename count differs")


def integer_value(node: ast.AST) -> int:
    if isinstance(node, ast.Constant) and isinstance(node.value, int):
        return node.value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -integer_value(node.operand)
    if isinstance(node, ast.BinOp):
        left = integer_value(node.left)
        right = integer_value(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Pow):
            return left ** right
    raise GateError("bounded profile contains a nonconstant integer limit")


def dictionary(node: ast.AST) -> dict[object, ast.AST]:
    require(isinstance(node, ast.Dict), "expected a literal dictionary")
    result: dict[object, ast.AST] = {}
    for key, value in zip(node.keys, node.values):
        require(isinstance(key, ast.Constant), "dictionary key is not literal")
        result[key.value] = value
    return result


def check_bounded(text: str) -> None:
    try:
        tree = ast.parse(text)
    except SyntaxError as error:
        raise GateError(f"bounded B2y helper is not valid Python: {error}") from error

    profiles_node: ast.AST | None = None
    for statement in tree.body:
        if isinstance(statement, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == "PROFILES"
                   for target in statement.targets):
                profiles_node = statement.value
    require(profiles_node is not None, "bounded B2y helper lacks PROFILES")
    profiles = dictionary(profiles_node)
    require(set(profiles) == {"close", "posterior"},
            "bounded B2y helper profile inventory differs")
    expected_profiles = {
        "close": {
            "wall_seconds": 80,
            "cpu_seconds": 75,
            "rss_bytes": 2 * 1024**3,
            "file_bytes": 512 * 1024**2,
            "log_bytes": 64 * 1024**2,
        },
        "posterior": {
            "wall_seconds": 30,
            "cpu_seconds": 20,
            "rss_bytes": 2 * 1024**3,
            "file_bytes": 16 * 1024**2,
            "log_bytes": 16 * 1024**2,
        },
    }
    for profile_name, expected in expected_profiles.items():
        found = dictionary(profiles[profile_name])
        require(set(found) == set(expected),
                f"bounded B2y {profile_name} limit inventory differs")
        for key, expected_value in expected.items():
            require(integer_value(found[key]) == expected_value,
                    f"bounded B2y {profile_name} {key} differs")

    popens: list[ast.Call] = []
    forbidden_process_calls: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        function = node.func
        if isinstance(function, ast.Attribute):
            owner = function.value
            if isinstance(owner, ast.Name) and owner.id == "subprocess":
                if function.attr == "Popen":
                    popens.append(node)
                elif function.attr in {
                    "run", "call", "check_call", "check_output", "getoutput",
                }:
                    forbidden_process_calls.append(function.attr)
            if isinstance(owner, ast.Name) and owner.id == "os" and function.attr == "system":
                forbidden_process_calls.append("os.system")
    require(len(popens) == 1,
            "bounded B2y helper must contain exactly one subprocess.Popen")
    require(not forbidden_process_calls,
            "bounded B2y helper contains a second process API")
    keywords = {keyword.arg: keyword.value for keyword in popens[0].keywords}
    start = keywords.get("start_new_session")
    require(isinstance(start, ast.Constant) and start.value is True,
            "bounded B2y child does not start a fresh process group")

    code = packed(text)
    required_fragments = (
        "IMPORTERRNO",
        "RESOURCE.SETRLIMIT(RESOURCE.RLIMIT_CPU",
        "RESOURCE.SETRLIMIT(RESOURCE.RLIMIT_FSIZE",
        "RESOURCE.SETRLIMIT(RESOURCE.RLIMIT_CORE",
        "PROCESS_RSS_BYTES(PROCESS.PID)",
        "OS.KILLPG(PROCESS.PID,SIGNAL.SIGKILL)",
        "OS.KILL(PROCESS.PID,SIGNAL.SIGKILL)",
        "CLASSCLEANUPSTATE:",
        "DEFGROUP_CENSUS(",
        "DEFFAIL_AFTER_CLEANUP(",
        "DEFKILL_GROUP_AT_HARD_DEADLINE(",
        "DEFREAP_ESRCH_EXIT(",
        'HARD_DEADLINE=START+PROFILE["WALL_SECONDS"]',
        "REMAINING=HARD_DEADLINE-TIME.MONOTONIC()",
        "IFREMAINING<=0:",
        "PROCESS.WAIT(TIMEOUT=REMAINING)",
        "CENSUS_ERROR.ERRNO==ERRNO.ESRCH",
        "KILL_GROUP_AT_HARD_DEADLINE(PROCESS,CLEANUP_STATE)",
        "TIME.SLEEP(MIN(0.05,REMAINING))",
        '"OMP_NUM_THREADS":"1"',
        '"OPENBLAS_NUM_THREADS":"1"',
        '"VECLIB_MAXIMUM_THREADS":"1"',
        '"CLOSE":"INVALID-RUNTIME-BUDGET-NO-CLOSED-RESULT"',
        '"CLOSE":"FAILED-NO-CLOSED"',
        '"POSTERIOR":"INVALID-CLOSED-EVIDENCE"',
        "MANAGED_SIGNALS=(SIGNAL.SIGHUP,SIGNAL.SIGINT,SIGNAL.SIGTERM)",
        "EXCEPTMANAGEDINTERRUPTIONASINTERRUPTION:",
        "EXCEPTBASEEXCEPTIONASPRIMARY_ERROR:",
        "TERMINATE_GROUP(PROCESS,CLEANUP_STATE)",
        "PRIMARY_ERROR.ADD_NOTE(",
        "SIGNAL.SIGNAL(SIGNAL_NUMBER,SIGNAL.SIG_IGN)",
        "FINALLY:",
    )
    for fragment in required_fragments:
        require(packed(fragment) in code,
                f"bounded B2y helper missing {fragment}")
    hard_start = text.index("def kill_group_at_hard_deadline(")
    hard_stop = text.index("\n\nclass ProcTaskInfo", hard_start)
    hard_kill = packed(text[hard_start:hard_stop])
    require("TERMINATE_GROUP(PROCESS,STATE)" in hard_kill,
            "B2y hard deadline does not use immediate group termination")
    require("SIGNAL.SIGTERM" not in hard_kill and
            "TIME.SLEEP" not in hard_kill and
            "TERM_GRACE_SECONDS" not in hard_kill,
            "B2y hard deadline includes a grace interval")
    terminate_start = text.index("def terminate_group(")
    terminate_stop = text.index("\n\ndef fail_after_cleanup", terminate_start)
    terminate = packed(text[terminate_start:terminate_stop])
    require("SIGNAL.SIGKILL" in terminate,
            "B2y failure cleanup does not immediately kill its process group")
    require("IFSTATE.ATTEMPTED:" in terminate and
            "RETURNSTATE.OUTCOME" in terminate,
            "B2y failure cleanup is not idempotent")
    require(terminate.index("STATE.ATTEMPTED=TRUE") <
            terminate.index("OS.KILLPG(PROCESS.PID,SIGNAL.SIGKILL)"),
            "B2y cleanup state is not fixed before its first signal")
    require("EXCEPTPROCESSLOOKUPERROR:" in terminate and
            "EXCEPTPERMISSIONERROR:" in terminate and
            "OS.KILL(PROCESS.PID,SIGNAL.SIGKILL)" in terminate,
            "B2y cleanup does not classify ESRCH/EPERM safely")
    require("FAIL(" not in terminate and
            "RAISE" not in terminate and
            "SIGNAL.SIGTERM" not in terminate and
            "TERM_GRACE_SECONDS" not in terminate and
            "TIME.SLEEP" not in terminate,
            "B2y cleanup can throw or contains a computation grace interval")
    reap_start = text.index("def reap_esrch_exit(")
    reap_stop = text.index("\n\ndef wait_bounded", reap_start)
    reap = packed(text[reap_start:reap_stop])
    require("REMAINING=HARD_DEADLINE-TIME.MONOTONIC()" in reap and
            "IFREMAINING<=0:RETURNNONE" in reap and
            "PROCESS.WAIT(TIMEOUT=REMAINING)" in reap and
            "EXCEPTSUBPROCESS.TIMEOUTEXPIRED:RETURNNONE" in reap,
            "B2y ESRCH exit reconciliation exceeds its exact contract")
    wait_timeout_calls = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr != "wait":
            continue
        timeout_keywords = [keyword for keyword in node.keywords
                            if keyword.arg == "timeout"]
        if timeout_keywords:
            wait_timeout_calls.append(timeout_keywords[0].value)
    require(len(wait_timeout_calls) == 1 and
            isinstance(wait_timeout_calls[0], ast.Name) and
            wait_timeout_calls[0].id == "remaining",
            "B2y exit reconciliation timeout is not the deadline remainder")
    require("EXIT_CENSUS_GRACE_SECONDS" not in text and
            "remaining +" not in text and "remaining+" not in text,
            "B2y wrapper adds an exit grace beyond the absolute deadline")
    base_start = text.index("except BaseException as primary_error:")
    base_stop = text.index("\n    finally:", base_start)
    base = packed(text[base_start:base_stop])
    require("TERMINATE_GROUP(PROCESS,CLEANUP_STATE)" in base and
            "PRIMARY_ERROR.ADD_NOTE(" in base and base.endswith("RAISE"),
            "B2y BaseException cleanup can mask the primary failure")
    require(len(re.findall(
        r'(?m)^\s*hard_deadline\s*=\s*start\s*\+\s*'
        r'profile\["wall_seconds"\]\s*$',
        text,
    )) == 1 and len(re.findall(
        r'(?m)^\s*hard_deadline\s*=', text
    )) == 1, "B2y absolute hard-deadline assignment differs")


def check_production_host(text: str) -> None:
    code = packed(strip_deck_comments(text))
    require(code.count("FEEDBACK:=RETURNED;") == 1,
            "SpotCloseR64 RETURNED copy differs")
    require(code.count("SPOR64V:FEEDBACK::;") == 1,
            "SpotCloseR64 returned admission differs")
    asm = (
        "SYSTEM_NEXT:=ASM:MACROLIB3TRACK_AXFEEDBACKBASIS_REF::"
        "EDIT0SPOD1FIXB;"
    )
    flu = (
        "AX_NEXT:=FLU:MACROLIB3TRACK_AXSYSTEM_NEXT::"
        "EDIT-3TYPEKB1SIGSEXTE5002.5E-7"
        "UNKT2.5E-7THER2.5E-7;"
    )
    state = "AX_NEXT:=SPOSTATE:AX_NEXTTRACK_AXSYSTEM_NEXTMACROLIB3::;"
    leak = "FEEDBACK:=SPOLEAK:FEEDBACKAX_NEXTTRACK_AX::>>LEAK_CHANGE<<;"
    close = "AX_CLOSEDARCH_CLOSED:=SPOR64X:AX_NEXTFEEDBACK::;"
    for expression in (asm, flu, state, leak, close):
        require(code.count(expression) == 1,
                f"SpotCloseR64 expression differs: {expression}")
    require_order(
        "SpotCloseR64",
        code,
        ("FEEDBACK:=RETURNED;", "SPOR64V:FEEDBACK::;", asm, flu,
         state, leak, close),
    )
    require(code.count("2.5E-7") == 3,
            "SpotCloseR64 tolerance literal inventory differs")
    forbidden = (
        "WHILE", "REPEAT", "RETRY", "FALLBACK", "RETUNE", "RELAX",
        "DAMP", "CLIP", "ALPHA", "OMEGA",
    )
    for token in forbidden:
        require(token not in code, f"forbidden SpotCloseR64 token: {token}")


def check_flu2dr(text: str) -> None:
    code = packed(strip_fortran_comments(text))
    strict = (
        "IF((EEXT.LT.EPSOUT).AND.(EINN.LT.EPSUNK).AND."
        "(EINR_LAST.LT.EPSINR).AND.(IINR_STATE.EQ.1).AND."
        "(IT.GE.2))THEN"
    )
    guard = (
        "IF((CXDOOR.EQ.'SPOT').AND.(ITYPEC.GE.2).AND."
        "(ITYPEC.LE.3))THEN"
        "CALLXABORT('FLU2DR:SPOTTYPE-KSTRICTTERMINATIONREQUIRED.')"
        "RETURNENDIF"
    )
    require(code.count(strict) == 1,
            "FLU2DR strict success predicate differs")
    require(code.count(guard) == 1,
            "FLU2DR SPOT TYPE-K cap rejection differs")
    cap = code.find("400CONTINUE")
    rejection = code.find(guard)
    publication = code.find("410RKEFF=REAL(AKEFF)")
    require(-1 < cap < rejection < publication,
            "FLU2DR cap rejection no longer precedes publication")


def main() -> None:
    check_attempt_result(read_required(ATTEMPT_RESULT))
    check_manifest(read_required(MANIFEST))
    check_deck(read_required(DECK))
    check_runner(read_required(RUNNER))
    check_bounded(read_required(BOUNDED))
    check_publisher(read_required(PUBLISHER))
    check_production_host(read_required(HOST))
    check_flu2dr(read_required(FLU2DR))
    print("B2Y STATIC ONE-REAL-RETURNED-CLOSE PASS")
    print("B2Y DECK=EXTERNAL-RETURNED->SPOTCLOSER64x1")
    print("B2Y ACTIVATION=DEFAULT-OFF CLOSE-PROFILE-POPEN=1 RETRY=0")
    print("B2Y HISTORICAL-ATTEMPT=CONSUMED CLASS=INVALID-RUNTIME-EVIDENCE")
    print("B2Y STRICT-FLU=FAIL-CLOSED EMPIRICAL-CONTROLS-ADDED=0")


if __name__ == "__main__":
    main()
