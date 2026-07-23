#!/usr/bin/env python3
"""Fail-closed public receipt check for the bounded radial-floor result."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "radial_floor_protocol.json"
STATUS = HERE / "radial_floor_status.txt"
XSM = HERE / "radial_floor_xsm_result.txt"
RESULT = HERE / "radial_floor_result.md"
RECEIPT = HERE / "radial_floor_result_receipt.sha256"


def fail(message: str) -> None:
    raise SystemExit(f"RADIAL-FLOOR RESULT FAIL: {message}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


for path in (PROTOCOL, STATUS, XSM, RESULT, RECEIPT):
    if not path.is_file() or path.is_symlink():
        fail(f"missing regular public result file: {path.name}")

expected_hashes = {
    PROTOCOL: (
        "6a68bb319c382b96df7289e848bbfb4da3341bf6406b72cfe2c381e579d863a2"
    ),
    STATUS: (
        "1147ebc3dfa39613e73cb7e68e1f903e4b6fc4ba0a14057f79d78f990512e636"
    ),
    XSM: (
        "c1c49a226296068a3448aa240f2c633a5931f79097547e07f54f1c27ce6b9016"
    ),
    RESULT: (
        "79ef29c9119a9d4f5764a8bf3f6e1848070cfcc2fbdf9b8bdf55957d1e62fdc2"
    ),
    RECEIPT: (
        "8b440f48e4fb7293d72ee4051dd17ff2c897b5dcce9dc14417fab68ffc0a4d1f"
    ),
}
for path, expected in expected_hashes.items():
    if sha256(path) != expected:
        fail(f"{path.name} differs from the published result")

expected_status = (
    "RADIAL-FLOOR CAPTURE VALID-DIAGNOSTIC",
    "RADIAL-FLOOR STATUS ARM NATIVE CAP IEXTF=6 "
    "INNER-RECORDS=8 OUTER-RECORDS=6",
    "RADIAL-FLOOR STATUS ARM STATIONARY CAP IEXTF=6 "
    "INNER-RECORDS=7 OUTER-RECORDS=6",
    "RADIAL-FLOOR STATUS PROBE NATIVE ONE-STEP-DIAGNOSTIC IEXTF=1",
    "RADIAL-FLOOR STATUS PROBE STATIONARY ONE-STEP-DIAGNOSTIC IEXTF=1",
    "RADIAL-FLOOR STATUS COMPARISON BOTH-CAP",
    "RADIAL-FLOOR STATUS FIXED-POINT-DEFECT NOT-A-PHI-MINUS-Q-RESIDUAL",
    "RADIAL-FLOOR STATUS THRESHOLD NONE",
    "RADIAL-FLOOR STATUS STAGE4 INVALID",
    "RADIAL-FLOOR STATUS STAGE5 NOT-AUTHORIZED",
    "RADIAL-FLOOR STATUS OUTER-CONVERGENCE NOT-EVALUATED",
    "RADIAL-FLOOR STATUS COMPLETE",
)
if tuple(STATUS.read_text(encoding="ascii").splitlines()) != expected_status:
    fail("published status lines differ from the frozen classification")

xsm_text = XSM.read_text(encoding="ascii")
number = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)[Ee][+-]\d+"
metric_re = re.compile(
    rf"^RADIAL-FLOOR-XSM (NATIVE|STATIONARY) "
    rf"(V2-NUM|V2-DEN|D-V2|MAX-NUM|MAX-DEN|D-MAX)  ({number})$",
    re.MULTILINE,
)
metrics = {
    (arm, name): float(value)
    for arm, name, value in metric_re.findall(xsm_text)
}
if len(metrics) != 12:
    fail("published XSM result lacks the twelve scalar defect records")
for arm in ("NATIVE", "STATIONARY"):
    if metrics[(arm, "V2-NUM")] / metrics[(arm, "V2-DEN")] != metrics[
        (arm, "D-V2")
    ]:
        fail(f"{arm} D-V2 is not the printed numerator/denominator ratio")
    if metrics[(arm, "MAX-NUM")] / metrics[(arm, "MAX-DEN")] != metrics[
        (arm, "D-MAX")
    ]:
        fail(f"{arm} D-MAX is not the printed numerator/denominator ratio")

result_text = RESULT.read_text(encoding="utf-8")
for token in (
    "de4297cc4d1aeca63307191df70c6eeaef4b1e2a",
    "`BOTH-CAP`",
    "not an independently assembled",
    "No model term, relaxation, fitted factor, empirical coefficient",
    "STAGE4 INVALID",
    "STAGE5 NOT-AUTHORIZED",
    "OUTER-CONVERGENCE NOT-EVALUATED",
    "7.6 MB",
    "GitHub repository",
):
    if token not in result_text:
        fail(f"result interpretation lacks required token: {token}")

receipt_rows = [
    row.split()
    for row in RECEIPT.read_text(encoding="ascii").splitlines()
    if row.strip()
]
if (
    len(receipt_rows) != 13
    or any(len(row) != 2 for row in receipt_rows)
    or len({row[1] for row in receipt_rows}) != len(receipt_rows)
    or any(not re.fullmatch(r"[0-9a-f]{64}", row[0]) for row in receipt_rows)
):
    fail("tracked result receipt has an invalid or duplicate census")
for path, expected in ((STATUS, expected_hashes[STATUS]), (XSM, expected_hashes[XSM])):
    relative = str(path.relative_to(HERE.parents[1]))
    if [expected, relative] not in receipt_rows:
        fail(f"tracked result receipt does not bind {path.name}")

print(
    "RADIAL-FLOOR RESULT PASS: BOTH-CAP; exact public one-step defects; "
    "no equation-residual, convergence, Stage-4, or acceleration-choice claim."
)
