#!/usr/bin/env python3
"""Fail closed if SPOGBAL again accepts FLU's saved work RHS."""

from pathlib import Path
import re


root = Path(__file__).resolve().parents[2]
balance = (root / "src/SPOGBAL.f90").read_text(errors="replace")
solve = (
    root / "validation/iterative/one_corrected_map.x2m"
).read_text(errors="replace")

failures: list[str] = []

if len(
    re.findall(
        r":=\s*SPOGBAL:.*?\s+MACROLIB3\s*::\s*;",
        solve,
        re.IGNORECASE | re.DOTALL,
    )
) != 2:
    failures.append("both one-map SPOGBAL calls must receive MACROLIB3")

required = (
    "nentry /= 4",
    "L_MACROLIB",
    "K-EFFECTIVE",
    "NUSIGF",
    "CHI",
    "NJJS00",
    "IJJS00",
    "IPOS00",
    "SCAT00",
    "call SPOQ00",
    "call SPOF00",
    "DRAGON-TXSC",
    "INVALID TXSC RECORD",
    "qfinal(ireg)",
)
folded = balance.casefold()
for token in required:
    if token.casefold() not in folded:
        failures.append(f"SPOGBAL is missing final-source input/use: {token}")

for pattern, label in (
    (r"LCMGID\s*\(\s*kentry\(1\)\s*,\s*['\"]SOUR['\"]", "SOUR directory"),
    (r"LCMGDL\s*\(\s*jpsour", "saved SOUR group"),
    (r"\bjpsour\b", "saved-source pointer"),
):
    if re.search(pattern, balance, re.IGNORECASE):
        failures.append(f"SPOGBAL still accesses the {label}")

if len(re.findall(r"\bcall\s+SPOQ00\s*\(", balance, re.IGNORECASE)) != 1:
    failures.append("SPOGBAL must contain exactly one physical-source evaluator call")
if len(re.findall(r"\bcall\s+SPOF00\s*\(", balance, re.IGNORECASE)) != 1:
    failures.append("SPOGBAL must precompute final fission production once")

cell_start = folded.find("cell=(")
cell_window = folded[cell_start : cell_start + 900] if cell_start >= 0 else ""
if "qfinal(ireg)" not in cell_window:
    failures.append("cell and modal residuals do not consume q_final")
if re.search(r"\bsour\w*\s*\(", cell_window):
    failures.append("cell and modal residuals consume a saved source")

if failures:
    raise SystemExit("FINAL-SOURCE AUDIT FAIL:\n" + "\n".join(failures))

print(
    "FINAL-SOURCE AUDIT PASS: final flux and k feed MACROLIB3 off-group "
    "P0 scattering plus fission; saved SOUR is absent from acceptance."
)
