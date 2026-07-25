#!/usr/bin/env python3
"""Synthetic end-to-end tests for check_gmres_activity_artifact.py."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

import check_gmres_activity_artifact as subject


ROOT = Path(__file__).resolve().parents[2]
CHECKER = Path(__file__).with_name("check_gmres_activity_artifact.py")
LEGACY_OFF_LOG = (
    ROOT / "validation/artifacts/raw-moc-capture/stationary_off/probe.log"
)
LEGACY_ON_LOG = (
    ROOT / "validation/artifacts/raw-moc-capture/stationary_on/probe.log"
)
TRACK = ROOT / "validation/artifacts/raw-moc-capture/common/restart_track.xsm"
LEGACY_OFF_XSM = (
    ROOT / "validation/artifacts/raw-moc-capture/stationary/off.xsm"
)
LEGACY_OFF_DECK = (
    ROOT / "validation/artifacts/raw-moc-capture/stationary_off/probe.x2m"
)
LEGACY_ON_DECK = (
    ROOT / "validation/artifacts/raw-moc-capture/stationary_on/probe.x2m"
)
RUN_PROTOCOL = Path(__file__).with_name("gmres_activity_run_protocol.json")
FROZEN_BUILD = ROOT / "validation/artifacts/gmres-activity-build"
CPU_RE = re.compile(
    r"(FLU2DR: CPU TIME=)[ \t]*"
    r"[+-]?(?:\d+(?:\.\d+)?|\.\d+)(?:[EeDd][+-]?\d+)?"
    r"(?=\.[ \t]+(?:INTERNAL|EXTERNAL))"
)


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="ascii", newline="\n") as stream:
        stream.write(text)


def normalized_legacy(raw: str) -> str:
    result, substitutions = CPU_RE.subn(r"\1<CPU-TELEMETRY>", raw)
    if substitutions != 2:
        raise AssertionError("fixture CPU telemetry census")
    return result


def make_ledger(active: bool) -> str:
    mask = [1] + [0] * (subject.NGROUP - 1)
    if active:
        roles = [
            (1, 1, 1, 1, 0, 1, mask),
            (1, 2, 2, 1, 1, 1, mask),
            (1, 3, 3, 2, 1, 1, mask),
        ]
        blocks = [(1, 1, 2, 1, mask, [1] + [0] * 369)]
        role_calls = (1, 1, 1)
        role_groups = (1, 1, 1)
        histogram = [369, 1] + [0] * 9
        nonzero, sum_k, max_k = 1, 1, 1
        classification = subject.ACTIVE
        last_iteration = 2
    else:
        roles = [(1, 1, 1, 1, 0, 1, mask)]
        blocks = []
        role_calls = (1, 0, 0)
        role_groups = (1, 0, 0)
        histogram = [0] * 11
        nonzero, sum_k, max_k = 0, 0, 0
        classification = subject.INACTIVE
        last_iteration = 1

    state = [
        1,
        1,
        2,
        1,
        370,
        14,
        370,
        10,
        1,
        1,
        *role_calls,
        *role_groups,
        len(blocks),
        nonzero,
        sum_k,
        max_k,
        20,
        subject.EPSI_BITS_AS_INTEGER,
        0,
        0,
    ]
    lines = ["GMRES-ACTIVITY RAW TRACK 20 10 3727C5AC"]
    lines.extend(
        f"GMRES-ACTIVITY RAW STATE {field} {value}"
        for field, value in enumerate(state, start=1)
    )
    lines.extend(
        f"GMRES-ACTIVITY RAW NGIND {group} {group}"
        for group in range(1, subject.NGROUP + 1)
    )
    lines.append(
        "GMRES-ACTIVITY RAW CALL "
        f"1 1 {len(roles)} {len(blocks)} {last_iteration}"
    )
    lines.extend(
        f"GMRES-ACTIVITY RAW ROLE-SUM {role} "
        f"{role_calls[role - 1]} {role_groups[role - 1]}"
        for role in range(1, 4)
    )
    for ordinal, (call, index, role, iteration, block, count, values) in enumerate(
        roles,
        start=1,
    ):
        lines.append(
            "GMRES-ACTIVITY RAW ROLE "
            f"{call} {index} {role} {iteration} {block} {count}"
        )
        lines.extend(
            f"GMRES-ACTIVITY RAW ROLE-ACTIVE {ordinal} {group} {value}"
            for group, value in enumerate(values, start=1)
        )
    for ordinal, (call, index, iteration, count, active_mask, k_values) in enumerate(
        blocks,
        start=1,
    ):
        lines.append(
            f"GMRES-ACTIVITY RAW BLOCK {call} {index} {iteration} {count}"
        )
        lines.extend(
            "GMRES-ACTIVITY RAW BLOCK-GROUP "
            f"{ordinal} {group} {active_value} {k_value}"
            for group, (active_value, k_value) in enumerate(
                zip(active_mask, k_values),
                start=1,
            )
        )
    lines.extend(
        f"GMRES-ACTIVITY RAW K-HISTOGRAM {k_value} {count}"
        for k_value, count in enumerate(histogram)
    )
    lines.extend(
        [
            f"GMRES-ACTIVITY NONZERO-K-GROUP-BLOCKS {nonzero}",
            f"GMRES-ACTIVITY SUM-K {sum_k}",
            f"GMRES-ACTIVITY MAX-K {max_k}",
            "GMRES-ACTIVITY THRESHOLD NONE",
            f"GMRES-ACTIVITY CLASSIFICATION {classification}",
            "GMRES-ACTIVITY COMPLETE",
        ]
    )
    return "\n".join(lines) + "\n"


def make_result(active: bool) -> str:
    if active:
        histogram = [369, 1] + [0] * 9
        blocks, nonzero, sum_k, max_k = 1, 1, 1, 1
        classification = subject.ACTIVE
    else:
        histogram = [0] * 11
        blocks, nonzero, sum_k, max_k = 0, 0, 0, 0
        classification = subject.INACTIVE
    lines = [
        "GMRES-ACTIVITY RESULT 1",
        "PROCESSES OFF=1 ON=2",
        f"CORRECTION-BLOCKS {blocks}",
        f"GROUP-BLOCKS {370 * blocks}",
    ]
    lines.extend(
        f"K-HISTOGRAM {k_value} {count}"
        for k_value, count in enumerate(histogram)
    )
    lines.extend(
        [
            f"NONZERO-K-GROUP-BLOCKS {nonzero}",
            f"SUM-K {sum_k}",
            f"MAX-K {max_k}",
            "THRESHOLD NONE",
            f"CLASSIFICATION {classification}",
            "COMPLETE",
        ]
    )
    return "\n".join(lines) + "\n"


def refresh_reader_replay(artifact: Path) -> None:
    names = [
        "on_a/ledger.txt",
        "on_a/ledger_repeat.txt",
        "on_b/ledger.txt",
        "on_b/ledger_repeat.txt",
    ]
    write_text(
        artifact / "reader_replay.sha256",
        "".join(
            f"{digest((artifact / name).read_bytes())}  {name}\n"
            for name in names
        ),
    )


def refresh_manifest(artifact: Path) -> None:
    files = sorted(
        path.relative_to(artifact).as_posix()
        for path in artifact.rglob("*")
        if path.is_file()
        and not path.is_symlink()
        and path.name != "artifact_manifest.sha256"
    )
    write_text(
        artifact / "artifact_manifest.sha256",
        "".join(f"{digest((artifact / name).read_bytes())}  {name}\n" for name in files),
    )


def build_artifact(parent: Path, active: bool) -> Path:
    artifact = parent / "candidate"
    for directory in ("off", "on_a", "on_b"):
        (artifact / directory).mkdir(parents=True)

    protocol_bytes = RUN_PROTOCOL.read_bytes()
    if digest(protocol_bytes) != subject.RUN_PROTOCOL_SHA256:
        raise AssertionError("frozen run protocol identity")
    (artifact / "gmres_activity_run_protocol.json").write_bytes(protocol_bytes)
    write_text(
        artifact / "gmres_activity_run_implementation.sha256",
        "".join(
            f"{'1' * 64}  {name}\n"
            for name in sorted(subject.EXPECTED_RUN_IMPLEMENTATION_PATHS)
        ),
    )
    run_commit = "2" * 40
    write_text(artifact / "run_commit.txt", run_commit + "\n")
    for name in subject.EXPECTED_BUILD_EVIDENCE_SHA256:
        shutil.copyfile(FROZEN_BUILD / name, artifact / name)
    executable_digest = subject.FROZEN_EXECUTABLE_SHA256
    write_text(
        artifact / "implementation_replay.log",
        "GMRES-ACTIVITY IMPLEMENTATION CHECK PASS\n",
    )
    input_receipt = "".join(
        f"{value}  {name}\n"
        for name, value in sorted(subject.EXPECTED_INPUT_HASHES.items())
    )
    write_text(artifact / "inputs_before.sha256", input_receipt)
    write_text(artifact / "inputs_after.sha256", input_receipt)
    preflight = (
        "GMRES-ACTIVITY SYNTHETIC PREFLIGHT EVIDENCE\n"
        "GMRES-ACTIVITY PREFLIGHT PASS\n"
        "GMRES-ACTIVITY PRODUCTION NOT AUTHORIZED\n"
    )
    write_text(artifact / "preflight.log", preflight)
    write_text(artifact / "postflight.log", preflight)

    shutil.copyfile(TRACK, artifact / "track.xsm")
    shutil.copyfile(LEGACY_OFF_XSM, artifact / "off/result.xsm")
    (artifact / "on_a/result.xsm").write_bytes(b"SYNTHETIC-ON-WITH-SPOT-GMR-AUD\n")
    shutil.copyfile(artifact / "on_a/result.xsm", artifact / "on_b/result.xsm")
    shutil.copyfile(LEGACY_OFF_DECK, artifact / "off/deck.x2m")
    legacy_on_deck = LEGACY_ON_DECK.read_bytes()
    on_deck = legacy_on_deck.replace(b" MOCA 2 ;", b" MOCA 2 GMRA ;")
    if on_deck.count(b"GMRA") != 1 or on_deck == legacy_on_deck:
        raise AssertionError("fixture ON deck token census")
    (artifact / "on_a/deck.x2m").write_bytes(on_deck)
    (artifact / "on_b/deck.x2m").write_bytes(on_deck)

    off_raw = LEGACY_OFF_LOG.read_text(encoding="ascii")
    legacy_on_raw = LEGACY_ON_LOG.read_text(encoding="ascii")
    on_raw = legacy_on_raw.replace(" MOCA 2 ;     ", " MOCA 2 GMRA ;")
    if on_raw.count("GMRA") != 2:
        raise AssertionError("fixture GMRA token census")
    write_text(artifact / "off/run.log", off_raw)
    write_text(artifact / "on_a/run.log", on_raw)
    write_text(artifact / "on_b/run.log", on_raw)
    write_text(artifact / "off/normalized.log", normalized_legacy(off_raw))
    normalized_on = normalized_legacy(legacy_on_raw)
    write_text(artifact / "on_a/normalized.log", normalized_on)
    write_text(artifact / "on_b/normalized.log", normalized_on)

    ledger = make_ledger(active)
    for name in (
        "on_a/ledger.txt",
        "on_a/ledger_repeat.txt",
        "on_b/ledger.txt",
        "on_b/ledger_repeat.txt",
    ):
        write_text(artifact / name, ledger)
    write_text(
        artifact / "on_a/non_audit_identity.txt",
        "GMRES-ACTIVITY PAIR CHECK PASS\n",
    )
    write_text(
        artifact / "on_b/non_audit_identity.txt",
        "GMRES-ACTIVITY PAIR CHECK PASS\n",
    )
    write_text(
        artifact / "log_identity.txt",
        "GMRES-ACTIVITY RUN-LOGS PASS\n",
    )
    refresh_reader_replay(artifact)

    classification = subject.ACTIVE if active else subject.INACTIVE
    write_text(artifact / "artifact_check_a.log", classification + "\n")
    write_text(artifact / "artifact_check_b.log", classification + "\n")
    write_text(artifact / "result.txt", make_result(active))
    run_implementation_sha = digest(
        (artifact / "gmres_activity_run_implementation.sha256").read_bytes()
    )
    write_text(
        artifact / "run_receipt.tsv",
        "\n".join(
            [
                "schema\t1",
                f"run_commit\t{run_commit}",
                (
                    "source_implementation_commit\t"
                    f"{subject.SOURCE_IMPLEMENTATION_COMMIT}"
                ),
                f"method_protocol_sha256\t{subject.METHOD_PROTOCOL_SHA256}",
                f"run_protocol_sha256\t{subject.RUN_PROTOCOL_SHA256}",
                (
                    "method_implementation_manifest_sha256\t"
                    f"{subject.METHOD_IMPLEMENTATION_MANIFEST_SHA256}"
                ),
                (
                    "run_implementation_manifest_sha256\t"
                    f"{run_implementation_sha}"
                ),
                f"executable_sha256\t{executable_digest}",
                "process_matrix\tOFF=1,ON=2",
                f"classification\t{classification}",
            ]
        )
        + "\n",
    )
    refresh_manifest(artifact)
    return artifact


def mutate_all_ledgers(artifact: Path, old: str, new: str) -> None:
    for name in (
        "on_a/ledger.txt",
        "on_a/ledger_repeat.txt",
        "on_b/ledger.txt",
        "on_b/ledger_repeat.txt",
    ):
        path = artifact / name
        text = path.read_text(encoding="ascii")
        if text.count(old) != 1:
            raise AssertionError(f"tamper target census in {name}")
        write_text(path, text.replace(old, new, 1))
    refresh_reader_replay(artifact)
    refresh_manifest(artifact)


def snapshot(artifact: Path) -> dict[str, str]:
    return {
        path.relative_to(artifact).as_posix(): digest(path.read_bytes())
        for path in artifact.rglob("*")
        if path.is_file() and not path.is_symlink()
    }


class ArtifactCheckerTest(unittest.TestCase):
    maxDiff = None

    def run_checker(self, artifact: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), str(artifact)],
            check=False,
            text=True,
            capture_output=True,
            env={"PYTHONDONTWRITEBYTECODE": "1", "PATH": "/usr/bin:/bin"},
        )

    def assert_invalid(self, artifact: Path) -> subprocess.CompletedProcess[str]:
        result = self.run_checker(artifact)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "INVALID\n")
        self.assertIn("GMRES-ACTIVITY ARTIFACT INVALID:", result.stderr)
        return result

    def test_valid_active(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            artifact = build_artifact(Path(temporary), active=True)
            before = snapshot(artifact)
            result = self.run_checker(artifact)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, subject.ACTIVE + "\n")
            self.assertEqual(result.stderr, "")
            self.assertEqual(snapshot(artifact), before)

    def test_valid_inactive(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            artifact = build_artifact(Path(temporary), active=False)
            result = self.run_checker(artifact)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, subject.INACTIVE + "\n")
            self.assertEqual(result.stderr, "")

    def test_derived_summary_tamper_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            artifact = build_artifact(Path(temporary), active=True)
            mutate_all_ledgers(
                artifact,
                "GMRES-ACTIVITY SUM-K 1\n",
                "GMRES-ACTIVITY SUM-K 2\n",
            )
            result = self.assert_invalid(artifact)
            self.assertIn("reader SUM-K differs", result.stderr)

    def test_raw_active_mask_tamper_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            artifact = build_artifact(Path(temporary), active=True)
            mutate_all_ledgers(
                artifact,
                "GMRES-ACTIVITY RAW ROLE-ACTIVE 3 1 1\n",
                "GMRES-ACTIVITY RAW ROLE-ACTIVE 3 1 0\n",
            )
            result = self.assert_invalid(artifact)
            self.assertIn("raw role active count", result.stderr)

    def test_raw_kmax_tamper_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            artifact = build_artifact(Path(temporary), active=True)
            mutate_all_ledgers(
                artifact,
                "GMRES-ACTIVITY RAW BLOCK-GROUP 1 1 1 1\n",
                "GMRES-ACTIVITY RAW BLOCK-GROUP 1 1 1 0\n",
            )
            result = self.assert_invalid(artifact)
            self.assertIn("raw Krylov count/MAX-K identity", result.stderr)

    def test_missing_validity_evidence_is_rejected(self) -> None:
        for relative in (
            "off/run.log",
            "on_a/non_audit_identity.txt",
            "run_receipt.tsv",
            "artifact_manifest.sha256",
        ):
            with self.subTest(relative=relative):
                with tempfile.TemporaryDirectory() as temporary:
                    artifact = build_artifact(Path(temporary), active=True)
                    (artifact / relative).unlink()
                    if relative != "artifact_manifest.sha256":
                        refresh_manifest(artifact)
                    self.assert_invalid(artifact)

    def test_invalid_input_creates_no_result_or_final_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            artifact = build_artifact(base, active=True)
            (artifact / "result.txt").unlink()
            refresh_manifest(artifact)
            before = snapshot(artifact)
            self.assert_invalid(artifact)
            self.assertFalse((artifact / "result.txt").exists())
            self.assertFalse((base / "gmres-activity-census").exists())
            self.assertEqual(snapshot(artifact), before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
