#!/usr/bin/env python3
"""Transport-free tests for the thin corrected D4-A Picard series owner."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
CONTROLLER = HERE / "run_d4a_rank2_picard_series.sh"
PARENT_INPUTS = (
    "closed_axial.xsm",
    "closed_snapshots.xsm",
    "initial_radial_track.bin",
    "initial_axial_track.xsm",
    "initial_axial_macrolib.xsm",
    "basis_reference.xsm",
    "route_contract.xsm",
)
PORTABLE_EVIDENCE = (
    "gate.log",
    "prepare.log",
    "admission.log",
    "close.log",
    "independent_check.log",
    "input_manifest.sha256",
    "output_manifest.sha256",
)


RUNNER_STUB = r"""#!/bin/sh
set -eu
test "$#" -eq 2
parent=$1
raw=$2
printf 'runner\t%s\t%s\n' "$parent" "$raw" >> "$SYNTH_CALLS"
count=0
test ! -f "$SYNTH_COUNT" || count=$(cat "$SYNTH_COUNT")
count=$((count + 1))
printf '%s\n' "$count" > "$SYNTH_COUNT"

mkdir "$raw"
start=${SYNTH_START_EPOCH:-0}
closed=$((start + count - 1))
projected=$((closed + 1))
close_epoch=$projected
test "$SYNTH_MODE" != bad_epoch || close_epoch=$((projected + 1))
printf '%s\n%s\n' \
  "SPOT-R64 B2J CLOSED/$closed -> PROJECTED/$projected" \
  'SPOT-R64 B2J PROJECT PREPARATION COMPLETE NO-TRANSPORT' \
  > "$raw/prepare.log"
printf '%s\n%s\n' \
  'SPOT-R64 B2W CLOSE PASS STATUS=2' \
  "SPOT-R64 CLOSED/$close_epoch COMPLETE NO-TRANSPORT" \
  > "$raw/close.log"
case "$SYNTH_MODE:$count" in
  success:1|never_met:*|bad_epoch:1) classification=VALID_NOT_MET ;;
  success:2|met:1) classification=VALID_MET ;;
  duplicate:1)
    printf '%s\n' \
      'CLASSIFICATION=VALID_NOT_MET' \
      'CLASSIFICATION=VALID_MET' \
      'SPOT-GATE COMPLETE' > "$raw/gate.log"
    exit 0
    ;;
  *) echo "unexpected synthetic map call $count" >&2; exit 9 ;;
esac
printf '%s\n%s\n' \
  "CLASSIFICATION=$classification" \
  'SPOT-GATE COMPLETE' > "$raw/gate.log"
printf 'synthetic map %s\n' "$count" > "$raw/payload.dat"
"""


FREEZER_STUB = r"""#!/bin/sh
set -eu
test "$#" -eq 3
build=$1
raw=$2
portable=$3
printf 'freezer\t%s\t%s\t%s\n' "$build" "$raw" "$portable" \
  >> "$SYNTH_CALLS"
mkdir "$portable"
cp "$raw/gate.log" "$raw/payload.dat" "$portable/"
classification=$(grep -E '^CLASSIFICATION=VALID_(MET|NOT_MET)$' \
  "$raw/gate.log")
case "$classification" in
  CLASSIFICATION=VALID_NOT_MET)
    printf '%s\n%s\n%s\n' \
      'MAP_CLASSIFICATION=VALID_NOT_MET' \
      'PORTABLE_ROLE=NEXT_MAP_PARENT_ONLY' \
      'FINAL_CONVERGENCE=NOT_CLAIMED' \
      > "$portable/portable_classification.txt"
    ;;
  CLASSIFICATION=VALID_MET)
    printf '%s\n%s\n' \
      'MAP_CLASSIFICATION=VALID_MET' \
      'PORTABLE_ROLE=CONVERGED_MAP' \
      > "$portable/portable_classification.txt"
    ;;
  *) exit 8 ;;
esac
(
  cd "$portable"
  find . -type f ! -name result.sha256 -print | LC_ALL=C sort |
    while IFS= read -r file; do shasum -a 256 "$file"; done \
      > result.sha256
)
"""


class PicardSeriesTest(unittest.TestCase):
    def setUp(self) -> None:
        self._temporary = tempfile.TemporaryDirectory(
            prefix="spot-picard-series-test."
        )
        self.root = Path(self._temporary.name)
        self.tools = self.root / "tools"
        self.tools.mkdir()
        shutil.copy2(CONTROLLER, self.tools / CONTROLLER.name)
        self._write_executable(
            self.tools / "run_d4a_rank2_picard_map.sh", RUNNER_STUB
        )
        self._write_executable(
            self.tools / "freeze_d4a_corrected_map.sh", FREEZER_STUB
        )
        os.chmod(self.tools / CONTROLLER.name, 0o755)

        self.build = self.root / "build"
        self.build.mkdir()
        payload = b"synthetic admitted bootstrap\n"
        (self.build / "bootstrap.dat").write_bytes(payload)
        digest = hashlib.sha256(payload).hexdigest()
        (self.build / "d4a_bootstrap_result.sha256").write_text(
            f"{digest}  bootstrap.dat\n", encoding="ascii"
        )
        for name in PARENT_INPUTS:
            (self.build / name).write_text(
                f"synthetic {name}\n", encoding="ascii"
            )
        self.calls = self.root / "calls.tsv"
        self.count = self.root / "count.txt"

    def tearDown(self) -> None:
        self._temporary.cleanup()

    @staticmethod
    def _write_executable(path: Path, text: str) -> None:
        path.write_text(text, encoding="utf-8")
        os.chmod(path, 0o755)

    def make_portable_parent(
        self, name: str, *, symlink_input: str | None = None
    ) -> Path:
        parent = self.root / name
        parent.mkdir()
        for input_name in PARENT_INPUTS:
            destination = parent / input_name
            if input_name == symlink_input:
                destination.symlink_to(self.build / input_name)
            else:
                shutil.copy2(self.build / input_name, destination)
        (parent / "portable_classification.txt").write_text(
            "MAP_CLASSIFICATION=VALID_NOT_MET\n"
            "PORTABLE_ROLE=NEXT_MAP_PARENT_ONLY\n"
            "FINAL_CONVERGENCE=NOT_CLAIMED\n",
            encoding="ascii",
        )
        for evidence_name in PORTABLE_EVIDENCE:
            (parent / evidence_name).write_text(
                f"synthetic sealed {evidence_name}\n", encoding="ascii"
            )
        receipt = []
        for path in sorted(parent.iterdir()):
            if path.name == "result.sha256":
                continue
            receipt.append(
                f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n"
            )
        (parent / "result.sha256").write_text("".join(receipt), encoding="ascii")
        return parent

    def run_series(
        self,
        mode: str,
        maximum: int,
        *,
        parent: Path | None = None,
        output: Path | None = None,
        start_epoch: int = 0,
    ) -> subprocess.CompletedProcess[str]:
        if parent is None:
            parent = self.build
        if output is None:
            output = self.root / "series"
        environment = os.environ.copy()
        environment.update(
            {
                "RADIAL_TIMEOUT_SECONDS": "1",
                "AXIAL_TIMEOUT_SECONDS": "1",
                "SYNTH_MODE": mode,
                "SYNTH_CALLS": str(self.calls),
                "SYNTH_COUNT": str(self.count),
                "SYNTH_START_EPOCH": str(start_epoch),
            }
        )
        return subprocess.run(
            [
                "sh",
                str(self.tools / CONTROLLER.name),
                str(self.build),
                str(parent),
                str(output),
                str(maximum),
            ],
            check=False,
            capture_output=True,
            text=True,
            env=environment,
        )

    def call_rows(self) -> list[list[str]]:
        if not self.calls.exists():
            return []
        return [line.split("\t") for line in self.calls.read_text().splitlines()]

    def test_not_met_parent_is_frozen_before_next_map_and_first_met_stops(self) -> None:
        result = self.run_series("success", 5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("D4A PICARD SERIES CONVERGED: step=2", result.stdout)

        rows = self.call_rows()
        self.assertEqual(
            [row[0] for row in rows],
            ["runner", "freezer", "runner", "freezer"],
        )
        first_portable = self.root / "series" / "map-001.portable"
        self.assertEqual(Path(rows[2][1]).resolve(), first_portable.resolve())
        self.assertFalse((self.root / "series" / "map-003.raw").exists())
        self.assertIn(
            "PORTABLE_ROLE=NEXT_MAP_PARENT_ONLY",
            (first_portable / "portable_classification.txt").read_text(),
        )
        self.assertIn(
            "PORTABLE_ROLE=CONVERGED_MAP",
            (
                self.root
                / "series"
                / "map-002.portable"
                / "portable_classification.txt"
            ).read_text(),
        )
        series_rows = (
            self.root / "series" / "picard_series.tsv"
        ).read_text().splitlines()
        self.assertEqual(len(series_rows), 3)
        self.assertIn("\t1\tVALID_NOT_MET\t", series_rows[1])
        self.assertIn("\t2\tVALID_MET\t", series_rows[2])

    def test_duplicate_classification_is_rejected_without_freeze_or_retry(self) -> None:
        result = self.run_series("duplicate", 5)
        self.assertEqual(result.returncode, 2)
        self.assertIn(
            "has 2 classification lines and 2 canonical classifications",
            result.stderr,
        )
        rows = self.call_rows()
        self.assertEqual([row[0] for row in rows], ["runner"])
        self.assertFalse((self.root / "series" / "map-001.portable").exists())
        self.assertFalse((self.root / "series" / "map-002.raw").exists())

    def test_maximum_is_a_nonconvergence_stop_not_an_acceptance(self) -> None:
        result = self.run_series("never_met", 2)
        self.assertEqual(result.returncode, 3)
        self.assertIn(
            "MAX_MAPS_REACHED=2 NO_CONVERGENCE_CLAIM", result.stderr
        )
        rows = self.call_rows()
        self.assertEqual(
            [row[0] for row in rows],
            ["runner", "freezer", "runner", "freezer"],
        )
        self.assertFalse((self.root / "series" / "map-003.raw").exists())

    def test_nested_output_is_rejected_without_polluting_parent(self) -> None:
        before = {
            path.relative_to(self.build): (
                "symlink" if path.is_symlink() else path.read_bytes()
            )
            for path in self.build.rglob("*")
            if path.is_file() or path.is_symlink()
        }
        nested = self.build / "forbidden-series"
        result = self.run_series("met", 1, output=nested)
        self.assertEqual(result.returncode, 2)
        self.assertIn("lie inside it", result.stderr)
        self.assertFalse(nested.exists())
        after = {
            path.relative_to(self.build): (
                "symlink" if path.is_symlink() else path.read_bytes()
            )
            for path in self.build.rglob("*")
            if path.is_file() or path.is_symlink()
        }
        self.assertEqual(after, before)
        self.assertEqual(self.call_rows(), [])

    def test_bootstrap_fixed_input_symlink_is_rejected_before_runner(self) -> None:
        basis = self.build / "basis_reference.xsm"
        target = self.build / "basis_reference.target"
        target.write_bytes(basis.read_bytes())
        basis.unlink()
        basis.symlink_to(target.name)
        result = self.run_series("met", 1)
        self.assertEqual(result.returncode, 2)
        self.assertIn(
            "initial parent is missing regular basis_reference.xsm",
            result.stderr,
        )
        self.assertEqual(self.call_rows(), [])

    def test_inconsistent_prepare_and_close_epochs_are_rejected(self) -> None:
        result = self.run_series("bad_epoch", 2)
        self.assertEqual(result.returncode, 2)
        self.assertIn("close epoch differs from projected epoch", result.stderr)
        self.assertEqual([row[0] for row in self.call_rows()], ["runner"])
        self.assertFalse((self.root / "series" / "map-001.portable").exists())

    def test_portable_parent_symlink_is_rejected_before_runner(self) -> None:
        parent = self.make_portable_parent(
            "linked-parent", symlink_input="basis_reference.xsm"
        )
        result = self.run_series("met", 1, parent=parent)
        self.assertEqual(result.returncode, 2)
        self.assertIn(
            "portable parent inventory or receipt is invalid",
            result.stderr,
        )
        self.assertEqual(self.call_rows(), [])

    def test_token_only_receipt_cannot_admit_fake_portable_parent(self) -> None:
        parent = self.make_portable_parent("token-only-parent")
        token = parent / "unrelated.token"
        token.write_text("unrelated\n", encoding="ascii")
        (parent / "result.sha256").write_text(
            f"{hashlib.sha256(token.read_bytes()).hexdigest()}  unrelated.token\n",
            encoding="ascii",
        )
        result = self.run_series("met", 1, parent=parent)
        self.assertEqual(result.returncode, 2)
        self.assertIn(
            "portable parent inventory or receipt is invalid",
            result.stderr,
        )
        self.assertEqual(self.call_rows(), [])

    def test_unsealed_extra_file_rejects_portable_parent(self) -> None:
        parent = self.make_portable_parent("extra-file-parent")
        (parent / "unsealed.extra").write_text("not in receipt\n", encoding="ascii")
        result = self.run_series("met", 1, parent=parent)
        self.assertEqual(result.returncode, 2)
        self.assertIn(
            "portable parent inventory or receipt is invalid",
            result.stderr,
        )
        self.assertEqual(self.call_rows(), [])

    def test_actual_epoch_is_reported_when_starting_after_map3(self) -> None:
        parent = self.make_portable_parent("map3-portable")
        output = self.root / "continued-series"
        result = self.run_series(
            "met", 1, parent=parent, output=output, start_epoch=3
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = (output / "picard_series.tsv").read_text().splitlines()
        self.assertEqual(
            rows[0], "step\tepoch\tclassification\traw\tportable"
        )
        self.assertEqual(rows[1].split("\t")[:3], ["1", "4", "VALID_MET"])


if __name__ == "__main__":
    unittest.main()
