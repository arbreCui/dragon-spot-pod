#!/usr/bin/env python3
"""Fail-closed static contract for one bounded real RETURNED close."""

from __future__ import annotations

import ast
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DECK = HERE / "one_real_returned_close.x2m"
RUNNER = HERE / "run_phase_a9b_b2y_one_real_returned_close.sh"
BOUNDED = HERE / "run_bounded_b2y.py"
HOST = ROOT / "data/SpotCloseR64.c2m"
FLU2DR = ROOT / "src/FLU2DR.f"

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
    require(re.search(r'0\|1\)', clean) is not None,
            "B2y runner RUN_B2Y domain is not exactly 0/1")
    off = re.search(
        r'(?is)if\s+\[\s*"\$RUN_B2Y"\s*=\s*0\s*\]\s*;\s*then'
        r'.*?\bexit\s+0\b.*?\bfi\b',
        clean,
    )
    require(off is not None, "B2y default-OFF branch is missing")

    external_checks = (
        '[ -n "$B2Y_RETURNED_XSM" ]',
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
        "RESOURCE.SETRLIMIT(RESOURCE.RLIMIT_CPU",
        "RESOURCE.SETRLIMIT(RESOURCE.RLIMIT_FSIZE",
        "RESOURCE.SETRLIMIT(RESOURCE.RLIMIT_CORE",
        "PROCESS_RSS_BYTES(PROCESS.PID)",
        "OS.KILLPG(PROCESS.PID,SIGNAL.SIGTERM)",
        "OS.KILLPG(PROCESS.PID,SIGNAL.SIGKILL)",
        '"OMP_NUM_THREADS":"1"',
        '"OPENBLAS_NUM_THREADS":"1"',
        '"VECLIB_MAXIMUM_THREADS":"1"',
        '"CLOSE":"INVALID-RUNTIME-BUDGET-NO-CLOSED-RESULT"',
        '"CLOSE":"FAILED-NO-CLOSED"',
        '"POSTERIOR":"INVALID-CLOSED-EVIDENCE"',
        "MANAGED_SIGNALS=(SIGNAL.SIGHUP,SIGNAL.SIGINT,SIGNAL.SIGTERM)",
        "EXCEPTMANAGEDINTERRUPTIONASINTERRUPTION:",
        "EXCEPTBASEEXCEPTION:",
        "TERMINATE_GROUP(PROCESS)",
        "SIGNAL.SIGNAL(SIGNAL_NUMBER,SIGNAL.SIG_IGN)",
        "FINALLY:",
    )
    for fragment in required_fragments:
        require(packed(fragment) in code,
                f"bounded B2y helper missing {fragment}")


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
    check_deck(read_required(DECK))
    check_runner(read_required(RUNNER))
    check_bounded(read_required(BOUNDED))
    check_production_host(read_required(HOST))
    check_flu2dr(read_required(FLU2DR))
    print("B2Y STATIC ONE-REAL-RETURNED-CLOSE PASS")
    print("B2Y DECK=EXTERNAL-RETURNED->SPOTCLOSER64x1")
    print("B2Y ACTIVATION=DEFAULT-OFF CLOSE-PROFILE-POPEN=1 RETRY=0")
    print("B2Y STRICT-FLU=FAIL-CLOSED EMPIRICAL-CONTROLS-ADDED=0")


if __name__ == "__main__":
    main()
