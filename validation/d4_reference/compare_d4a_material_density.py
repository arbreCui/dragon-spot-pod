#!/usr/bin/env python3
"""Report all three-state REAL32 printed SPOT densities against CE binary64.

No fitted tolerance or material-agreement gate is defined here.  PASS covers
complete physical inventory, valid values and unchanged 750 C legacy anchors;
the numerical differences remain REPORTED_ONLY.  The printed half-quantum is
an output-format bound, not a bound on the preceding REAL32 calculation.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
import re


STATES = (650, 750, 850)
LEGACY = {
    "N_Na": "2.237345e-02", "N_U8": "1.881861e-02",
    "N_Pu39": "2.747854e-03", "N_O": "4.719196e-02",
    "N_Fe56_AIM1": "5.000890e-02",
}
VARIABLES = {
    f"N_{variable}": ("FUEL_MOX", nuclide)
    for variable, nuclide in (
        ("U5", "U235"), ("U8", "U238"), ("Pu38", "Pu238"),
        ("Pu39", "Pu239"), ("Pu40", "Pu240"), ("Pu41", "Pu241"),
        ("Pu42", "Pu242"), ("Am", "Am241"), ("O", "O16"),
    )
}
for suffix, material in (("AIM1", "CLAD_AIM1"), ("EM10", "BOX_EM10")):
    for nuclide in (
        "Fe54", "Fe56", "Fe57", "Fe58", "Cr50", "Cr52", "Cr53", "Cr54",
        "Ni58", "Ni60", "Ni61", "Ni62", "Ni64", "Mn55", "Mo92", "Mo94",
        "Mo95", "Mo96", "Mo97", "Mo98", "Mo100", "Si28", "Ti48",
    ):
        variable = {"Si28": "Si", "Ti48": "Ti"}.get(nuclide, nuclide)
        VARIABLES[f"N_{variable}_{suffix}"] = (material, nuclide)
VARIABLES.update({
    "N_C12_EM10": ("BOX_EM10", "C12"),
    "N_Na": ("COOLANT_Na", "Na23"),
    "N_He_1": ("He_HOLE", "He4"), "N_He_2": ("He_GAP", "He4"),
})
TOKEN = r"[+-]?\d\.\d{6}[eE][+-]\d{2,3}"


def parse_log(text: str) -> dict[int, dict[str, str]]:
    if text.count("normal end of execution for dragon") != 1 or re.search(
        r"XABORT|FATAL|SIG(?:SEGV|FPE|BUS|ILL|ABRT)|fortran runtime error",
        text, re.IGNORECASE,
    ):
        raise ValueError("missing unique normal Dragon end or abnormal terminal")
    states: dict[int, dict[str, str]] = {}
    active = None
    for line in text.splitlines():
        echo = re.fullmatch(r">\|(.*?)\s*\|>\d+\s*", line)
        if echo is None:
            continue
        record = echo[1].strip()
        if record.startswith("D4A-NDENS-BEGIN"):
            values = record.split()[1:]
            expected = (STATES[len(states)], 620, 475) if len(states) < 3 else ()
            if active is not None or tuple(map(float, values)) != expected:
                raise ValueError("duplicated, out-of-order or incorrect material state")
            active = int(float(values[0]))
            states[active] = {}
        elif record == "D4A-NDENS-END":
            if active is None or set(states[active]) != set(VARIABLES):
                raise ValueError("incomplete or unexpected material density inventory")
            active = None
        elif record.startswith("N_"):
            match = re.fullmatch(rf"(N_\w+)=\s+({TOKEN})", record)
            if active is None or match is None:
                raise ValueError("density outside state or noncanonical REAL print format")
            name, token = match.groups()
            if name not in VARIABLES or name in states[active]:
                raise ValueError("unknown or duplicate material density")
            if not math.isfinite(float(token)) or float(token) <= 0.0:
                raise ValueError("nonpositive or nonfinite material density")
            states[active][name] = token.lower()
    if tuple(states) != STATES or active is not None:
        raise ValueError("three complete temperature states are required")
    if any(states[750][name] != token for name, token in LEGACY.items()):
        raise ValueError("750 C reviewed legacy printed anchors changed")
    return states


def ce_reference() -> dict[int, dict[str, float]]:
    import build_d4a_ce_reference as builder
    import check_d4a_ce_static as checker

    base = builder.load_audited_base(builder.DEFAULT_BASE)
    result = {}
    for floor, temperature in enumerate(STATES, start=1):
        materials, _mapping, _anchors = builder.make_floor_materials(
            base, floor, float(temperature)
        )
        expected, _ = checker.independent_expected_materials(base, float(temperature))
        built = {material.name.removeprefix(f"F{floor}_"): material for material in materials}
        if set(built) != set(expected):
            raise ValueError("CE builder and independent checker material sets differ")
        inventory = {(material, nuclide) for material, (_, values) in expected.items()
                     for nuclide in values}
        if inventory != set(VARIABLES.values()) or len(VARIABLES) != 59:
            raise ValueError("audit does not cover every CE model material/nuclide")
        for name, (temperature_k, values) in expected.items():
            material = built[name]
            if material.temperature != temperature_k or material.density_units != "sum":
                raise ValueError("CE builder and independent checker state differs")
            actual = {entry.name: entry.percent for entry in material.nuclides
                      if entry.percent_type == "ao"}
            if actual != values or len(actual) != len(material.nuclides):
                raise ValueError("CE builder differs from independent material formula")
        result[temperature] = {
            variable: expected[material][1][nuclide]
            for variable, (material, nuclide) in VARIABLES.items()
        }
    return result


def report(states, expected) -> None:
    print("D4A MATERIAL DIFFERENCES status=REPORTED_ONLY REAL32_PRINTED_VS_CE_BINARY64")
    print("fuel_C\tmaterial\tnuclide\tSPOT_printed\tCE_binary64\tabs_diff\trel_diff\tprint_half_quantum")
    for temperature in STATES:
        differences = []
        for variable, (material, nuclide) in VARIABLES.items():
            token = states[temperature][variable]
            ce = expected[temperature][variable]
            delta = abs(float(token) - ce)
            relative = delta / abs(ce)
            half_quantum = 0.5 * 10.0 ** (int(token.split("e")[1]) - 6)
            differences.append((relative, delta, variable))
            print(f"{temperature}\t{material}\t{nuclide}\t{token}\t{ce:.17g}\t"
                  f"{delta:.9g}\t{relative:.9g}\t{half_quantum:.9g}")
        relative, delta, variable = max(differences)
        print(f"D4A MATERIAL SUMMARY fuel_C={temperature} count=59 "
              f"max_rel_diff={relative:.9g} variable={variable} "
              f"abs_diff_at_max_rel={delta:.9g} "
              f"max_abs_diff={max(item[1] for item in differences):.9g} "
              "status=REPORTED_ONLY")
    print("D4A MATERIAL INVENTORY PASS: 3 states x 59 material/nuclide densities; "
          "750 C legacy anchors unchanged")
    print("Excluded: N_U5_f/N_U8_f/N_O_f are unused fertile-material outputs, "
          "not materials of the six-medium D4-A model")


def self_test() -> None:
    def echo(record):
        return f">|{record} |>0001\n"
    text = ""
    for temperature in STATES:
        text += echo(f"D4A-NDENS-BEGIN {temperature} 620 475")
        for name in VARIABLES:
            text += echo(f"{name}= {LEGACY.get(name, '1.000000e-03')}")
        text += echo("D4A-NDENS-END")
    text += "normal end of execution for dragon\n"
    assert len(parse_log(text)[650]) == 59
    for broken in (
        text.replace(echo("D4A-NDENS-END"), "", 1),
        text.replace(echo("N_U5= 1.000000e-03"), "", 1),
        text.replace(echo("N_U5= 1.000000e-03"), echo("N_U5= 1.000000e-03") * 2, 1),
        text.replace("N_U5= 1.000000e-03", "N_U5= -1.000000e-03", 1),
        text.replace("N_U5= 1.000000e-03", "N_U5= nan", 1),
        text.replace("N_Na= 2.237345e-02", "N_Na= 2.237346e-02"),
        text.replace("850 620 475", "650 620 475"),
        text + "normal end of execution for dragon\n",
    ):
        try:
            parse_log(broken)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid material log accepted")
    ce_reference()
    print("D4A MATERIAL COMPARISON SELF-TEST PASS: parser rejection and full CE inventory")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    elif args.log is not None:
        report(parse_log(args.log.read_text()), ce_reference())
    else:
        parser.error("provide a material-only Dragon log or --self-test")


if __name__ == "__main__":
    main()
