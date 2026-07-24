#!/usr/bin/env python3
"""Independent exact replay of a raw-MOC ULP bridge reader log."""

from __future__ import annotations

import argparse
from collections import Counter
import math
from pathlib import Path
import re
import struct


NGROUP = 370
NREGION = 8
NUNKNOWN = 14
NSCALAR = NGROUP * NREGION
KEY_ZERO = 0x80000000
HEX32 = re.compile(r"[0-9A-F]{8}")
HEX64 = re.compile(r"[0-9A-F]{16}")


def fail(message: str) -> None:
    raise SystemExit(f"RAW-MOC-ULP LOG FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def f32_to_f64_bits(bits: int) -> int:
    value = struct.unpack(">f", bits.to_bytes(4, "big"))[0]
    return int.from_bytes(struct.pack(">d", value), "big")


def round_shift_right_even(value: int, shift: int) -> int:
    quotient = value >> shift
    remainder = value & ((1 << shift) - 1)
    half = 1 << (shift - 1)
    return quotient + (
        remainder > half or (remainder == half and (quotient & 1) == 1)
    )


def round_f64_bits_to_f32_bits(bits: int) -> tuple[int, bool]:
    """Exact IEEE binary64-to-binary32 roundTiesToEven replay."""

    negative = bool(bits >> 63)
    exponent_field = (bits >> 52) & 0x7FF
    fraction = bits & ((1 << 52) - 1)
    overflow = False

    if exponent_field == 0x7FF:
        magnitude = 0x7F800000
        overflow = True
    elif exponent_field == 0:
        magnitude = 0
    else:
        exponent = exponent_field - 1023
        significand = (1 << 52) + fraction
        if exponent > 127:
            magnitude = 0x7F800000
            overflow = True
        elif exponent >= -126:
            rounded = round_shift_right_even(significand, 29)
            output_exponent = exponent
            if rounded == 1 << 24:
                rounded = 1 << 23
                output_exponent += 1
            if output_exponent > 127:
                magnitude = 0x7F800000
                overflow = True
            else:
                magnitude = (
                    (output_exponent + 127) * (1 << 23)
                    + rounded
                    - (1 << 23)
                )
        else:
            shift = -exponent - 97
            rounded = (
                0
                if shift >= 54
                else round_shift_right_even(significand, shift)
            )
            require(rounded <= 1 << 23, "subnormal rounding overflow")
            magnitude = rounded

    return magnitude | (0x80000000 if negative else 0), overflow


def ordered_key(bits: int) -> int:
    magnitude = bits & 0x7FFFFFFF
    if magnitude == 0:
        return KEY_ZERO
    if bits & 0x80000000:
        return KEY_ZERO - magnitude
    return KEY_ZERO + magnitude


def positive_finite_f32(bits: int) -> bool:
    return 0 < bits < 0x7F800000


def positive_finite_f64(bits: int) -> bool:
    return 0 < bits < 0x7FF0000000000000


def self_test() -> None:
    def bits64(value: float) -> int:
        return int.from_bytes(struct.pack(">d", value), "big")

    def rounded(value: float) -> tuple[int, bool]:
        return round_f64_bits_to_f32_bits(bits64(value))

    require(rounded(1.0) == (0x3F800000, False), "selftest exact")
    require(
        rounded(1.0 + 2.0**-25) == (0x3F800000, False),
        "selftest collapse",
    )
    tie_down = 1.0 + 2.0**-24
    require(
        rounded(tie_down) == (0x3F800000, False),
        "selftest tie-to-even down",
    )
    require(
        rounded(math.nextafter(tie_down, -math.inf))
        == (0x3F800000, False),
        "selftest below half",
    )
    require(
        rounded(math.nextafter(tie_down, math.inf))
        == (0x3F800001, False),
        "selftest above half",
    )
    require(
        rounded(1.0 + 3.0 * 2.0**-24) == (0x3F800002, False),
        "selftest tie-to-even up",
    )
    require(rounded(2.0**-150) == (0, False), "selftest underflow tie")
    require(
        rounded(3.0 * 2.0**-150) == (2, False),
        "selftest subnormal tie",
    )
    threshold = float.fromhex("0x1.ffffffp+127")
    require(
        rounded(math.nextafter(threshold, -math.inf))
        == (0x7F7FFFFF, False),
        "selftest below overflow",
    )
    require(
        rounded(threshold) == (0x7F800000, True),
        "selftest overflow tie",
    )
    require(
        ordered_key(0x80000000) == ordered_key(0),
        "selftest signed zero key",
    )
    require(
        ordered_key(0x80000001) == KEY_ZERO - 1
        and ordered_key(1) == KEY_ZERO + 1,
        "selftest zero adjacency",
    )
    require(
        ordered_key(0x3F800000) - ordered_key(0x3F7FFFFF) == 1,
        "selftest binade adjacency",
    )
    require(
        ordered_key(0x00800000) - ordered_key(0x007FFFFF) == 1,
        "selftest subnormal-normal adjacency",
    )


def canonical_text(path: Path) -> list[str]:
    require(path.is_file() and not path.is_symlink(), "invalid log file")
    raw = path.read_bytes()
    require(raw.endswith(b"\n") and b"\r" not in raw, "noncanonical log")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        fail(f"log is not ASCII: {exc}")
    return text.splitlines()


def parse_int(text: str, owner: str) -> int:
    require(re.fullmatch(r"-?[0-9]+", text) is not None, f"{owner} integer")
    return int(text)


def parse_hex(text: str, width: int, owner: str) -> int:
    pattern = HEX32 if width == 8 else HEX64
    require(pattern.fullmatch(text) is not None, f"{owner} hex")
    return int(text, 16)


def split_sections(lines: list[str]) -> list[list[str]]:
    starts = [
        index
        for index, line in enumerate(lines)
        if line.startswith("RAW-MOC-ULP ARM ")
    ]
    require(starts and starts[0] == 0, "first arm section is missing")
    starts.append(len(lines))
    sections = [
        lines[starts[index] : starts[index + 1]]
        for index in range(len(starts) - 1)
    ]
    require(all(section for section in sections), "empty arm section")
    return sections


def parse_bridge_row(
    fields: list[str],
    expected_group: int,
    expected_region: int,
) -> dict[str, int | str]:
    require(len(fields) == 15, "malformed RAW-BRIDGE ledger row")
    arm = fields[1]
    require(
        fields[:4] == ["RAW-MOC-ULP", arm, "RAW-BRIDGE", "LEDGER"],
        "RAW-BRIDGE prefix",
    )
    group = parse_int(fields[4], "bridge group")
    region = parse_int(fields[5], "bridge region")
    key = parse_int(fields[6], "bridge key")
    require(
        (group, region) == (expected_group, expected_region),
        "RAW-BRIDGE row order",
    )
    require(1 <= key <= NUNKNOWN, "RAW-BRIDGE key range")
    raw_bits = parse_hex(fields[7], 16, "RAW64")
    reference_bits = parse_hex(fields[8], 8, "bridge reference")
    target_bits = parse_hex(fields[9], 8, "bridge target")
    reference_key = parse_int(fields[10], "bridge reference key")
    target_key = parse_int(fields[11], "bridge target key")
    step = parse_int(fields[12], "bridge step")
    absolute = parse_int(fields[13], "bridge absolute")
    classification = fields[14]

    require(positive_finite_f64(raw_bits), "RAW64 is not positive finite")
    require(
        positive_finite_f32(reference_bits),
        "bridge reference is not positive finite",
    )
    expected_target, overflow = round_f64_bits_to_f32_bits(raw_bits)
    require(not overflow, "RAW64 conversion overflows")
    require(target_bits == expected_target, "RAW64 RNE replay differs")
    require((target_bits & 0x80000000) == 0, "rounded RAW is negative")
    require(
        (target_bits & 0x7F800000) != 0x7F800000,
        "rounded RAW is nonfinite",
    )
    require(reference_key == ordered_key(reference_bits), "reference K")
    require(target_key == ordered_key(target_bits), "target K")
    require(step == target_key - reference_key, "bridge signed step")
    require(absolute == abs(step), "bridge absolute step")

    raw_exact = raw_bits == f32_to_f64_bits(reference_bits)
    expected_class = (
        "RAW-EXACT"
        if raw_exact
        else (
            "ROUND-COLLAPSED-NONZERO"
            if step == 0
            else ("PROJECTED-UP" if step > 0 else "PROJECTED-DOWN")
        )
    )
    require(classification == expected_class, "bridge classification")
    return {
        "arm": arm,
        "group": group,
        "region": region,
        "key": key,
        "raw_bits": raw_bits,
        "reference_bits": reference_bits,
        "target_bits": target_bits,
        "reference_key": reference_key,
        "target_key": target_key,
        "step": step,
        "absolute": absolute,
        "classification": classification,
    }


def parse_production_row(
    fields: list[str],
    expected_group: int,
    expected_region: int,
) -> dict[str, int | str]:
    require(len(fields) == 13, "malformed PRODUCTION-STEP ledger row")
    arm = fields[1]
    require(
        fields[:4]
        == ["RAW-MOC-ULP", arm, "PRODUCTION-STEP", "LEDGER"],
        "PRODUCTION-STEP prefix",
    )
    group = parse_int(fields[4], "production group")
    region = parse_int(fields[5], "production region")
    key = parse_int(fields[6], "production key")
    require(
        (group, region) == (expected_group, expected_region),
        "PRODUCTION-STEP row order",
    )
    require(1 <= key <= NUNKNOWN, "PRODUCTION-STEP key range")
    reference_bits = parse_hex(fields[7], 8, "production reference")
    target_bits = parse_hex(fields[8], 8, "production target")
    reference_key = parse_int(fields[9], "production reference key")
    target_key = parse_int(fields[10], "production target key")
    step = parse_int(fields[11], "production step")
    absolute = parse_int(fields[12], "production absolute")
    require(
        positive_finite_f32(reference_bits)
        and positive_finite_f32(target_bits),
        "production scalar is not positive finite",
    )
    require(reference_key == ordered_key(reference_bits), "production ref K")
    require(target_key == ordered_key(target_bits), "production target K")
    require(step == target_key - reference_key, "production signed step")
    require(absolute == abs(step), "production absolute step")
    return {
        "arm": arm,
        "group": group,
        "region": region,
        "key": key,
        "reference_bits": reference_bits,
        "target_bits": target_bits,
        "reference_key": reference_key,
        "target_key": target_key,
        "step": step,
        "absolute": absolute,
    }


def summary_lines(
    arm: str,
    name: str,
    rows: list[dict[str, int | str]],
    bridge: bool,
) -> list[str]:
    steps = [int(row["step"]) for row in rows]
    counts = Counter(steps)
    unchanged = counts[0]
    upward = sum(count for step, count in counts.items() if step > 0)
    downward = sum(count for step, count in counts.items() if step < 0)
    adjacent = counts[1] + counts[-1]
    maximum = max(abs(step) for step in steps)
    result = [
        f"RAW-MOC-ULP {arm} {name} TOTAL {len(rows)}",
        f"RAW-MOC-ULP {arm} {name} UNCHANGED {unchanged}",
        f"RAW-MOC-ULP {arm} {name} UPWARD {upward}",
        f"RAW-MOC-ULP {arm} {name} DOWNWARD {downward}",
        f"RAW-MOC-ULP {arm} {name} ADJACENT {adjacent}",
    ]
    if bridge:
        raw_exact = sum(row["classification"] == "RAW-EXACT" for row in rows)
        collapsed = sum(
            row["classification"] == "ROUND-COLLAPSED-NONZERO"
            for row in rows
        )
        rounded_zero = sum(
            (int(row["target_bits"]) & 0x7FFFFFFF) == 0 for row in rows
        )
        rounded_subnormal = sum(
            0 < (int(row["target_bits"]) & 0x7FFFFFFF) < 0x00800000
            for row in rows
        )
        require(
            unchanged == raw_exact + collapsed,
            "RAW exact/collapsed partition",
        )
        result.extend(
            [
                f"RAW-MOC-ULP {arm} {name} RAW-EXACT {raw_exact}",
                "RAW-MOC-ULP "
                f"{arm} {name} ROUND-COLLAPSED-NONZERO {collapsed}",
                f"RAW-MOC-ULP {arm} {name} ROUNDED-TO-ZERO {rounded_zero}",
                "RAW-MOC-ULP "
                f"{arm} {name} ROUNDED-SUBNORMAL {rounded_subnormal}",
            ]
        )
    result.append(f"RAW-MOC-ULP {arm} {name} MAX-STEPS {maximum}")
    for step in sorted(counts):
        result.append(f"RAW-MOC-ULP {arm} {name} HIST {step} {counts[step]}")
    for row in rows:
        if int(row["absolute"]) == maximum:
            result.append(
                "RAW-MOC-ULP "
                f"{arm} {name} MAX-TIE "
                f"{row['group']} {row['region']} {row['key']} "
                f"{row['step']} {row['absolute']}"
            )
    return result


def bridge_ledger_line(row: dict[str, int | str]) -> str:
    return (
        "RAW-MOC-ULP "
        f"{row['arm']} RAW-BRIDGE LEDGER "
        f"{row['group']} {row['region']} {row['key']} "
        f"{int(row['raw_bits']):016X} "
        f"{int(row['reference_bits']):08X} "
        f"{int(row['target_bits']):08X} "
        f"{row['reference_key']} {row['target_key']} "
        f"{row['step']} {row['absolute']} {row['classification']}"
    )


def production_ledger_line(row: dict[str, int | str]) -> str:
    return (
        "RAW-MOC-ULP "
        f"{row['arm']} PRODUCTION-STEP LEDGER "
        f"{row['group']} {row['region']} {row['key']} "
        f"{int(row['reference_bits']):08X} "
        f"{int(row['target_bits']):08X} "
        f"{row['reference_key']} {row['target_key']} "
        f"{row['step']} {row['absolute']}"
    )


def fixture_checks(
    bridge: list[dict[str, int | str]],
    production: list[dict[str, int | str]],
) -> None:
    keyflux = [8, 1, 7, 2, 6, 3, 5, 4]
    for bridge_row, production_row in zip(bridge, production, strict=True):
        group = int(bridge_row["group"])
        region = int(bridge_row["region"])
        key = keyflux[region - 1]
        base_bits = 0x3F000000 + 64 * group + key
        expected_bridge = (group + 2 * region) % 7 - 3
        expected_production = (3 * group + region) % 9 - 4
        require(int(bridge_row["key"]) == key, "fixture KEYFLX sentinel")
        require(
            int(bridge_row["reference_bits"]) == base_bits,
            "fixture group/unknown sentinel",
        )
        require(
            int(bridge_row["step"]) == expected_bridge,
            "fixture bridge region sentinel",
        )
        require(
            int(production_row["key"]) == key
            and int(production_row["reference_bits"]) == base_bits
            and int(production_row["step"]) == expected_production,
            "fixture production sentinel",
        )


def validate_section(
    section: list[str], fixture: bool
) -> tuple[str, int, tuple[int, ...]]:
    arm_fields = section[0].split()
    require(
        len(arm_fields) == 3
        and arm_fields[:2] == ["RAW-MOC-ULP", "ARM"]
        and arm_fields[2] in {"NATIVE", "STATIONARY"},
        "invalid arm header",
    )
    arm = arm_fields[2]
    require(
        section[1] == "RAW-MOC-ULP DIMS 370 8 14",
        f"{arm} dimensions",
    )
    require(
        section[2]
        == "RAW-MOC-ULP ROUNDING IEEE-BINARY64-TO-BINARY32-RNE-ONCE",
        f"{arm} rounding declaration",
    )
    require(
        section[3]
        == "RAW-MOC-ULP RAW-BRIDGE DECLARED-DIRECT-PROJECTION",
        f"{arm} projection declaration",
    )

    bridge_lines = [
        line
        for line in section
        if line.startswith(f"RAW-MOC-ULP {arm} RAW-BRIDGE LEDGER ")
    ]
    production_lines = [
        line
        for line in section
        if line.startswith(
            f"RAW-MOC-ULP {arm} PRODUCTION-STEP LEDGER "
        )
    ]
    require(
        len(bridge_lines) == NSCALAR
        and len(production_lines) == NSCALAR,
        f"{arm} ledger census",
    )
    bridge_rows = [
        parse_bridge_row(
            line.split(),
            index // NREGION + 1,
            index % NREGION + 1,
        )
        for index, line in enumerate(bridge_lines)
    ]
    production_rows = [
        parse_production_row(
            line.split(),
            index // NREGION + 1,
            index % NREGION + 1,
        )
        for index, line in enumerate(production_lines)
    ]
    require(
        all(row["arm"] == arm for row in bridge_rows + production_rows),
        f"{arm} ledger arm identity",
    )
    keyflux = [int(bridge_rows[region]["key"]) for region in range(NREGION)]
    require(
        len(set(keyflux)) == NREGION
        and all(1 <= key <= NUNKNOWN for key in keyflux),
        f"{arm} inferred KEYFLX layout",
    )
    for index, (bridge_row, production_row) in enumerate(
        zip(bridge_rows, production_rows, strict=True)
    ):
        region = index % NREGION
        require(
            int(bridge_row["key"]) == keyflux[region]
            and int(production_row["key"]) == keyflux[region],
            f"{arm} key layout changes",
        )
        require(
            int(bridge_row["reference_bits"])
            == int(production_row["reference_bits"]),
            f"{arm} EVAL/PRE reference differs in ledgers",
        )

    if fixture:
        fixture_checks(bridge_rows, production_rows)

    expected = [
        f"RAW-MOC-ULP ARM {arm}",
        "RAW-MOC-ULP DIMS 370 8 14",
        "RAW-MOC-ULP ROUNDING IEEE-BINARY64-TO-BINARY32-RNE-ONCE",
        "RAW-MOC-ULP RAW-BRIDGE DECLARED-DIRECT-PROJECTION",
    ]
    expected.extend(summary_lines(arm, "RAW-BRIDGE", bridge_rows, True))
    expected.extend(bridge_ledger_line(row) for row in bridge_rows)
    expected.extend(
        summary_lines(arm, "PRODUCTION-STEP", production_rows, False)
    )
    expected.extend(production_ledger_line(row) for row in production_rows)
    expected.extend(
        [
            f"RAW-MOC-ULP {arm} LEDGERS NOT-SUBTRACTED",
            f"RAW-MOC-ULP {arm} ATTRIBUTION NONE",
            f"RAW-MOC-ULP {arm} ACCEPTANCE-THRESHOLD NONE",
            "RAW-MOC-ULP "
            f"{arm} CLASSIFICATION DESCRIPTIVE-ULP-CENSUS",
            f"RAW-MOC-ULP {arm} OUTER-CONVERGENCE NOT-EVALUATED",
            f"RAW-MOC-ULP {arm} STAGE4 NOT-AUTHORIZED",
            f"RAW-MOC-ULP {arm} COMPLETE",
        ]
    )
    require(section == expected, f"{arm} canonical grammar or summary differs")
    return arm, len(bridge_rows) + len(production_rows), tuple(keyflux)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("log", type=Path)
    parser.add_argument("--fixture", action="store_true")
    args = parser.parse_args()

    self_test()
    sections = split_sections(canonical_text(args.log))
    validated = [validate_section(section, args.fixture) for section in sections]
    arms = [arm for arm, _, _ in validated]
    require(len(arms) == len(set(arms)), "duplicate arm section")
    require(
        arms in (["NATIVE"], ["STATIONARY"], ["NATIVE", "STATIONARY"]),
        "arm section order differs",
    )
    require(
        len({keyflux for _, _, keyflux in validated}) == 1,
        "arm KEYFLX layouts differ",
    )
    rows = sum(count for _, count, _ in validated)
    print(
        "RAW-MOC-ULP LOG CHECK PASS: "
        f"ARMS={','.join(arms)}; LEDGERS={2 * len(arms)}; "
        f"ROWS={rows}; RNE-REPLAY={NSCALAR * len(arms)}"
    )


if __name__ == "__main__":
    main()
