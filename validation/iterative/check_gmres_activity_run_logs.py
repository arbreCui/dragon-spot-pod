#!/usr/bin/env python3
"""Independently close the five frozen GMRES-activity run logs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import stat
import sys
from typing import Union


PASS_LINE = "GMRES-ACTIVITY RUN-LOGS PASS"
NUMBER = r"[+-]?(?:\d+(?:\.\d+)?|\.\d+)(?:[EeDd][+-]?\d+)?"
NORMAL_END_RE = re.compile(
    r"^ normal end of execution for dragon 5  Version 5\.1\.0[ \t]*$",
    re.MULTILINE,
)
CPU_TIME_RE = re.compile(
    r"(FLU2DR: CPU TIME=)[ \t]*"
    r"[+-]?(?:\d+(?:\.\d+)?|\.\d+)(?:[EeDd][+-]?\d+)?"
    r"(?=\.[ \t]+(?:INTERNAL|EXTERNAL))"
)
MODULE_RECEIPT_RE = re.compile(
    r"^(?P<prefix>-->>MODULE FLU:        : TIME SPENT=)"
    r"(?P<time>.{13})"
    r"(?P<middle> MEMORY USAGE=)"
    r"(?P<memory>.{10})$",
    re.MULTILINE,
)
MODULE_TIME_RE = re.compile(r" *(?:0|[1-9][0-9]*)\.[0-9]{3}")
MODULE_MEMORY_RE = re.compile(r" [0-9]\.[0-9]{3}E[+-][0-9]{2}")
MODULE_TIME_MARKER = "<MODULE-TIME>"
MODULE_MEMORY_MARKER = "<MEM-TELE>"
CLE_CPU_RE = re.compile(
    r"^(?P<prefix>cle2000_c: cpu time= )"
    r"(?P<value>(?:0|[1-9][0-9]*)\.[0-9]{2})"
    r"(?P<suffix> second)$",
    re.MULTILINE,
)
CLE_CPU_MARKER = "<CLE-CPU>"
SOURCE_LEGACY_MOCA_RE = re.compile(
    r"^ACCE <<free_steps>> <<acc_steps>> MOCA 2 ; +0028$",
    re.MULTILINE,
)
TRACE_LEGACY_MOCA_RE = re.compile(
    r"^<\|ACCE <<free_steps>> <<acc_steps>> MOCA 2 ; +\|<0028$",
    re.MULTILINE,
)
SOURCE_GMRA_RE = re.compile(
    r"^ACCE <<free_steps>> <<acc_steps>> MOCA 2 GMRA ; +0028$",
    re.MULTILINE,
)
TRACE_GMRA_RE = re.compile(
    r"^<\|ACCE <<free_steps>> <<acc_steps>> MOCA 2 GMRA ; +\|<0028$",
    re.MULTILINE,
)
GMRA_FROM = " MOCA 2 GMRA ;"
GMRA_TO_FIXED_WIDTH = " MOCA 2 ;     "
SOURCE_LINE_LENGTH = 127
TRACE_LINE_LENGTH = 128


@dataclass(frozen=True)
class LoadedLog:
    path: Path
    identity: tuple[int, int]
    text: str


def fail(message: str) -> None:
    raise SystemExit(f"GMRES-ACTIVITY RUN-LOGS FAIL: {message}")


def require_one(
    pattern: Union[str, re.Pattern[str]],
    text: str,
    description: str,
) -> re.Match[str]:
    compiled = (
        pattern
        if isinstance(pattern, re.Pattern)
        else re.compile(pattern, re.MULTILINE)
    )
    matches = list(compiled.finditer(text))
    if len(matches) != 1:
        fail(f"{description}: expected one record, found {len(matches)}")
    return matches[0]


def load_log(path: Path, description: str) -> LoadedLog:
    try:
        status = path.lstat()
    except OSError as exc:
        fail(f"cannot inspect {description}: {exc}")
    if stat.S_ISLNK(status.st_mode) or not stat.S_ISREG(status.st_mode):
        fail(f"{description} is not a regular non-symlink file")
    try:
        raw = path.read_bytes()
    except OSError as exc:
        fail(f"cannot read {description}: {exc}")
    if not raw:
        fail(f"{description} is empty")
    if b"\0" in raw:
        fail(f"{description} contains a NUL byte")
    if b"\r" in raw:
        fail(f"{description} does not use canonical LF line endings")
    if not raw.endswith(b"\n"):
        fail(f"{description} lacks a final newline")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError:
        fail(f"{description} is not ASCII")
    return LoadedLog(
        path=path.resolve(strict=True),
        identity=(status.st_dev, status.st_ino),
        text=text,
    )


def require_module_receipt(
    text: str,
    description: str,
) -> re.Match[str]:
    if (
        MODULE_TIME_MARKER in text
        or MODULE_MEMORY_MARKER in text
    ):
        fail(f"{description} contains a forged module telemetry marker")
    if len(re.findall(r"^-->>MODULE ", text, re.MULTILINE)) != 1:
        fail(f"{description} module receipt census differs")
    receipt = require_one(
        MODULE_RECEIPT_RE,
        text,
        description + " FLU module telemetry",
    )
    if MODULE_TIME_RE.fullmatch(receipt.group("time")) is None:
        fail(f"{description} FLU module time telemetry grammar differs")
    if MODULE_MEMORY_RE.fullmatch(receipt.group("memory")) is None:
        fail(f"{description} FLU module memory telemetry grammar differs")
    return receipt


def require_cle_cpu_receipt(
    text: str,
    description: str,
) -> re.Match[str]:
    if CLE_CPU_MARKER in text:
        fail(f"{description} contains a forged CLE CPU marker")
    return require_one(
        CLE_CPU_RE,
        text,
        description + " CLE-2000 CPU telemetry",
    )


def validate_envelope(
    text: str,
    description: str,
    mode: str,
) -> None:
    normal_end = require_one(
        NORMAL_END_RE,
        text,
        description + " normal Dragon termination",
    )
    if text.count("normal end of execution for dragon") != 1:
        fail(f"{description} normal Dragon termination census differs")
    cle_cpu = require_cle_cpu_receipt(text, description)

    for pattern, label in (
        (r"\bXABORT\b", "XABORT"),
        (r"segmentation fault", "segmentation fault"),
        (r"floating invalid", "floating invalid"),
        (r"bus error", "bus error"),
        (r"illegal instruction", "illegal instruction"),
        (r"\b(?:NaN|Inf(?:inity)?)\b", "non-finite text"),
    ):
        if re.search(pattern, text, re.IGNORECASE):
            fail(f"{description} contains abnormal {label}")
    if re.search(r"^[ \t]*FLU2DR-TERM\b", text, re.MULTILINE):
        fail(f"{description} contains a strict-terminal claim")
    for token in ("@ARM@", "@MODE@", "@AUDIT_CONTROL@"):
        if token in text:
            fail(f"{description} contains unresolved template token {token}")
    if "<CPU-TELEMETRY>" in text:
        fail(f"{description} contains a forged normalized CPU marker")

    marker_matches: dict[str, re.Match[str]] = {}
    for marker in ("BEGIN", "COMPLETE"):
        require_one(
            rf'^ECHO "RAW-MOC-CAPTURE-{marker}" '
            rf'"STATIONARY" "{mode}" ;[^\n]*$',
            text,
            f"{description} source {marker} marker",
        )
        marker_matches[marker] = require_one(
            rf"^>\|RAW-MOC-CAPTURE-{marker} STATIONARY {mode}[ \t]*"
            rf"\|>[0-9]{{4}}$",
            text,
            f"{description} execution {marker} marker",
        )

    science = require_one(
        r"^[ \t]*P\. I\. M\.[ \t]+SOLUTION TO TRANSPORT EQUATION[ \t]*$",
        text,
        description + " scientific-block start",
    )
    require_one(
        r"^[ \t]*M O C PARAMETERS:[ \t]+NON CYCLIC[ \t]+"
        r"-[ \t]+STIS 1[ \t]+-[ \t]+SC SCHEME[ \t]+"
        r"-[ \t]+TABULATED EXP[ \t]*$",
        text,
        description + " MCCG MOC-parameter line",
    )
    inner = require_one(
        r"^[ \t]*IN\([ \t]*1\)[ \t]+FLX:.*$",
        text,
        description + " one printed inner update",
    )
    outer = require_one(
        r"^[ \t]*OUT\([ \t]*1\)[ \t]+FLX:.*$",
        text,
        description + " one printed outer update",
    )
    outer_diagnostic = require_one(
        r"^[ \t]*FLU2DR-DIAG OUTER IEXTF=[ \t]*1 "
        r"MAXOUT=[ \t]*1\b.*$",
        text,
        description + " one-step outer diagnostic",
    )
    inner_diagnostic = require_one(
        r"^[ \t]*FLU2DR-DIAG INNER ITERF=[ \t]*1 "
        r"MAXINR=[ \t]*740\b.*NGRP=[ \t]*370[ \t]*$",
        text,
        description + " one-step inner diagnostic",
    )
    tracking = require_one(
        r"^[ \t]*\+\+ TRACKING CALLED=[ \t]*1 TIMES "
        r"PRECISION=[ \t]*0\.00E\+00[ \t]*$",
        text,
        description + " tracking-call count",
    )
    flux_count = require_one(
        r"^[ \t]*\+\+ TOTAL NUMBER OF FLUX CALCULATIONS="
        r"[ \t]*370[ \t]*$",
        text,
        description + " flux-calculation count",
    )
    module_end = require_one(
        r"^->@END MODULE   : FLU:[ \t]*$",
        text,
        description + " FLU module end",
    )
    module_receipt = require_module_receipt(text, description)
    positions = (
        science.start(),
        inner.start(),
        outer.start(),
        outer_diagnostic.start(),
        inner_diagnostic.start(),
        tracking.start(),
        flux_count.start(),
        module_end.start(),
        module_receipt.start(),
        marker_matches["COMPLETE"].start(),
        cle_cpu.start(),
        normal_end.start(),
    )
    if tuple(sorted(positions)) != positions:
        fail(f"{description} one-step records are reordered")

    warnings = re.findall(
        r"^[ \t]*\*\*\* FLU2DR: CONVERGENCE NOT REACHED "
        r"\*\*\*[ \t]*$",
        text,
        re.MULTILINE,
    )
    if len(warnings) != 3:
        fail(f"{description} lacks exactly three one-step warnings")
    internal = require_one(
        r"^[ \t]*FLU2DR: CPU TIME=[ \t]*"
        rf"{NUMBER}\.[ \t]+INTERNAL CONVERGENCE "
        r"\*NEARLY\* REACHED AFTER[ \t]+1 ITERATIONS\.[ \t]*$",
        text,
        description + " internal CPU telemetry",
    )
    external = require_one(
        r"^[ \t]*FLU2DR: CPU TIME=[ \t]*"
        rf"{NUMBER}\.[ \t]+EXTERNAL CONVERGENCE[ \t]+"
        r"\*NOT\* REACHED AFTER[ \t]+1 ITERATIONS\.[ \t]*$",
        text,
        description + " external CPU telemetry",
    )
    if internal.start() >= external.start():
        fail(f"{description} CPU telemetry records are reordered")


def require_fixed_line(
    match: re.Match[str],
    expected_length: int,
    description: str,
) -> None:
    if len(match.group(0)) != expected_length:
        fail(
            f"{description} fixed-width line length differs: "
            f"expected {expected_length}, found {len(match.group(0))}"
        )


def validate_control(
    text: str,
    description: str,
    mode: str,
) -> None:
    moca_count = len(re.findall(r"\bMOCA\b", text))
    gmra_count = len(re.findall(r"\bGMRA\b", text))
    if mode == "OFF":
        if moca_count != 0 or gmra_count != 0:
            fail(f"{description} OFF log contains MOCA or GMRA")
        return
    if mode == "LEGACY_ON":
        if moca_count != 2 or gmra_count != 0:
            fail(f"{description} legacy ON control census differs")
        source = require_one(
            SOURCE_LEGACY_MOCA_RE,
            text,
            description + " source line 0028",
        )
        trace = require_one(
            TRACE_LEGACY_MOCA_RE,
            text,
            description + " execution echo line 0028",
        )
    elif mode == "GMRA_ON":
        if moca_count != 2 or gmra_count != 2:
            fail(f"{description} GMRA ON control census differs")
        source = require_one(
            SOURCE_GMRA_RE,
            text,
            description + " GMRA source line 0028",
        )
        trace = require_one(
            TRACE_GMRA_RE,
            text,
            description + " GMRA execution echo line 0028",
        )
    else:
        fail(f"internal mode error for {description}")
    require_fixed_line(
        source,
        SOURCE_LINE_LENGTH,
        description + " source line 0028",
    )
    require_fixed_line(
        trace,
        TRACE_LINE_LENGTH,
        description + " execution echo line 0028",
    )


def replace_fixed_width_gmra(
    text: str,
    pattern: re.Pattern[str],
    description: str,
) -> str:
    match = require_one(pattern, text, description)
    line = match.group(0)
    if line.count(GMRA_FROM) != 1:
        fail(f"{description} token grammar differs")
    normalized = line.replace(
        GMRA_FROM,
        GMRA_TO_FIXED_WIDTH,
        1,
    )
    if len(normalized) != len(line):
        fail(f"{description} normalization changed fixed line width")
    return text[: match.start()] + normalized + text[match.end() :]


def normalize(text: str, description: str, gmra: bool) -> str:
    if gmra:
        text = replace_fixed_width_gmra(
            text,
            SOURCE_GMRA_RE,
            description + " GMRA source line 0028",
        )
        text = replace_fixed_width_gmra(
            text,
            TRACE_GMRA_RE,
            description + " GMRA execution echo line 0028",
        )
        if re.search(r"\bGMRA\b", text):
            fail(f"{description} GMRA remained after exact normalization")
    elif re.search(r"\bGMRA\b", text):
        fail(f"{description} legacy normalization saw GMRA")

    normalized, substitutions = CPU_TIME_RE.subn(
        r"\1<CPU-TELEMETRY>",
        text,
    )
    if substitutions != 2:
        fail(f"{description} CPU telemetry census differs")
    if normalized.count("<CPU-TELEMETRY>") != 2:
        fail(f"{description} normalized CPU marker census differs")
    receipt = require_module_receipt(normalized, description)
    replacement = (
        receipt.group("prefix")
        + MODULE_TIME_MARKER
        + receipt.group("middle")
        + MODULE_MEMORY_MARKER
    )
    if len(replacement) != len(receipt.group(0)):
        fail(f"{description} module telemetry normalization changed line width")
    normalized = (
        normalized[: receipt.start()]
        + replacement
        + normalized[receipt.end() :]
    )
    if (
        normalized.count(MODULE_TIME_MARKER) != 1
        or normalized.count(MODULE_MEMORY_MARKER) != 1
    ):
        fail(f"{description} normalized module telemetry marker census differs")
    cle_cpu = require_cle_cpu_receipt(normalized, description)
    normalized = (
        normalized[: cle_cpu.start()]
        + cle_cpu.group("prefix")
        + CLE_CPU_MARKER
        + cle_cpu.group("suffix")
        + normalized[cle_cpu.end() :]
    )
    if normalized.count(CLE_CPU_MARKER) != 1:
        fail(f"{description} normalized CLE CPU marker census differs")
    return normalized


def check(paths: tuple[Path, Path, Path, Path, Path]) -> None:
    descriptions = (
        "LEGACY_OFF",
        "LEGACY_ON",
        "ACTUAL_OFF",
        "ACTUAL_ON_A",
        "ACTUAL_ON_B",
    )
    loaded = tuple(
        load_log(path, description)
        for path, description in zip(paths, descriptions)
    )
    if len({item.path for item in loaded}) != 5:
        fail("the five log paths must resolve distinctly")
    if len({item.identity for item in loaded}) != 5:
        fail("the five log files must have distinct inodes")

    legacy_off, legacy_on, actual_off, actual_on_a, actual_on_b = loaded
    validate_envelope(legacy_off.text, "LEGACY_OFF", "OFF")
    validate_control(legacy_off.text, "LEGACY_OFF", "OFF")
    validate_envelope(legacy_on.text, "LEGACY_ON", "ON")
    validate_control(legacy_on.text, "LEGACY_ON", "LEGACY_ON")
    validate_envelope(actual_off.text, "ACTUAL_OFF", "OFF")
    validate_control(actual_off.text, "ACTUAL_OFF", "OFF")
    validate_envelope(actual_on_a.text, "ACTUAL_ON_A", "ON")
    validate_control(actual_on_a.text, "ACTUAL_ON_A", "GMRA_ON")
    validate_envelope(actual_on_b.text, "ACTUAL_ON_B", "ON")
    validate_control(actual_on_b.text, "ACTUAL_ON_B", "GMRA_ON")

    normalized_legacy_off = normalize(
        legacy_off.text,
        "LEGACY_OFF",
        gmra=False,
    )
    normalized_legacy_on = normalize(
        legacy_on.text,
        "LEGACY_ON",
        gmra=False,
    )
    normalized_actual_off = normalize(
        actual_off.text,
        "ACTUAL_OFF",
        gmra=False,
    )
    normalized_actual_on_a = normalize(
        actual_on_a.text,
        "ACTUAL_ON_A",
        gmra=True,
    )
    normalized_actual_on_b = normalize(
        actual_on_b.text,
        "ACTUAL_ON_B",
        gmra=True,
    )

    if normalized_actual_off != normalized_legacy_off:
        fail("ACTUAL_OFF normalized full log differs from LEGACY_OFF")
    if normalized_actual_on_a != normalized_legacy_on:
        fail("ACTUAL_ON_A normalized full log differs from LEGACY_ON")
    if normalized_actual_on_b != normalized_legacy_on:
        fail("ACTUAL_ON_B normalized full log differs from LEGACY_ON")
    if normalized_actual_on_a != normalized_actual_on_b:
        fail("ACTUAL_ON_A and ACTUAL_ON_B normalized full logs differ")


def main() -> None:
    if len(sys.argv) != 6:
        fail(
            "expected exactly LEGACY_OFF LEGACY_ON "
            "ACTUAL_OFF ACTUAL_ON_A ACTUAL_ON_B"
        )
    paths = tuple(Path(argument) for argument in sys.argv[1:])
    check(paths)  # type: ignore[arg-type]
    print(PASS_LINE)


if __name__ == "__main__":
    main()
