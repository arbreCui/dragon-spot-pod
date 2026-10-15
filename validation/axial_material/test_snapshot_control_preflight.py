"""Synthetic XSM records and sealed historical data; no solver invocation."""

import hashlib
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

from snapshot_control_preflight import SnapshotControlError, audit_snapshot_controls


def write_snapshot(path, *, flux=(2.5e-7, 2.5e-7, 2.5e-7, 0., 0.),
                   track=(1e-5, 0., 0., 0.), flux_type=2, listdim=1, tag="A"):
    """Small native-layout XSM fixture, including LCM's list handle wrappers."""
    data = bytearray(b"$XSM" + b"\0" * 8)

    def record(type_code, values):
        raw = (values.encode("ascii") if type_code == 3 else
               struct.pack("<" + str(len(values)) + {1: "i", 2: "f", 10: "i"}[type_code], *values))
        offset = len(data) // 4
        data.extend(raw)
        return offset, len(raw) // 4, type_code

    def directory(entries):
        offset = len(data) // 4
        data.extend(b"\0" * (188 * 4))
        struct.pack_into("<4s4i12s", data, offset * 4, b"$$$$", 30, len(entries), offset, -1, b"/           ")
        for i, (name, entry) in enumerate(entries.items()):
            for k, value in enumerate(entry):
                struct.pack_into("<i", data, 4 * (offset + 8 + k * 30 + i), value)
            data[4 * (offset + 98 + 3 * i):4 * (offset + 101 + 3 * i)] = name.encode().ljust(12, b" ")
        return offset

    def archive_object(entries):
        child = directory(entries)
        wrapper = directory({"***HANDLE***": (child, -1, 0)})
        return record(10, [wrapper])

    entries = {"LISTDIM": record(1, [listdim]), "TEST-TAG": record(3, tag.ljust(4))}
    entries["FLUX"] = archive_object({"EPS-CONVERGE": record(flux_type, flux)})
    entries["TRACK"] = archive_object({"REAL-PARAM": record(2, track)})
    root = directory(entries)
    struct.pack_into("<2i", data, 4, len(data) // 4, root)
    Path(path).write_bytes(data)


def audit(path):
    return audit_snapshot_controls(path, eps_radial=2.5e-7, eps_axial=5e-8, eps_mccg=1e-5)


class SnapshotControlTests(unittest.TestCase):
    def test_allowed_radial_or_axial_bits_and_signed_zero_are_readonly(self):
        for eps in (2.5e-7, 5e-8):
            with self.subTest(eps=eps), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "snapshot.xsm"
                write_snapshot(path, flux=(eps, eps, eps, -0., 0.), track=(1e-5, -0., 0., 0.))
                before = path.read_bytes()
                with patch("subprocess.Popen", side_effect=AssertionError("no subprocess allowed")):
                    result = audit(path)
                self.assertEqual(result["classification"], "PASS_SNAPSHOT_CONTROL_COMPATIBILITY")
                self.assertEqual(before, path.read_bytes())

    def test_each_raw_predicate_remains_strict(self):
        cases = [dict(flux=(2e-6, 2e-6, 2e-6, 0., 0.)),
                 dict(flux=(2.5e-7, 5e-8, 2.5e-7, 0., 0.)),
                 dict(flux=(2.5e-7, 2.5e-7, 2.5e-7, 1e-30, 0.)),
                 dict(flux=(float("nan"), 2.5e-7, 2.5e-7, 0., 0.)),
                 dict(track=(float("inf"), 0., 0., 0.)),
                 dict(track=(1e-5, float("nan"), 0., 0.)),
                 dict(track=(1e-5, 0., 1e-30, 0.)), dict(track=(2e-6, 0., 0., 0.))]
        for change in cases:
            with self.subTest(change=change), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "snapshot.xsm"
                write_snapshot(path, **change)
                self.assertEqual(audit(path)["classification"], "FAIL_SNAPSHOT_CONTROL_COMPATIBILITY")

    def test_malformed_shapes_types_counts_and_truncation_refuse(self):
        for change in (dict(flux=(0.,) * 4), dict(flux=(0,) * 5, flux_type=1), dict(listdim=2)):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "snapshot.xsm"
                write_snapshot(path, **change)
                with self.assertRaises(SnapshotControlError):
                    audit(path)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "snapshot.xsm"
            for content in (b"$XSM", b"not an xsm archive", b"$XSM" + struct.pack("<2i", 3, 999999)):
                path.write_bytes(content)
                with self.assertRaises(SnapshotControlError):
                    audit(path)

    def test_sealed_historical_inputs_report_both_conflicts_without_changes(self):
        inputs = Path(__file__).resolve().parents[1] / "artifacts/axial-material-inputs-20261003"
        if not inputs.exists():
            self.skipTest("sealed local historical experiment is unavailable")
        for state in ("A", "B"):
            path = inputs / state / f"snapshot_{state}.xsm"
            before = hashlib.sha256(path.read_bytes()).hexdigest()
            with patch("subprocess.Popen", side_effect=AssertionError("no subprocess allowed")):
                result = audit(path)
            self.assertEqual(result["classification"], "FAIL_SNAPSHOT_CONTROL_COMPATIBILITY")
            self.assertEqual(set(result["records"]), {"FLUX/EPS-CONVERGE", "TRACK/REAL-PARAM"})
            self.assertTrue(all(not record["pass"] for record in result["records"].values()))
            self.assertEqual(result["records"]["FLUX/EPS-CONVERGE"]["actual_bits"][:3], ["0x360637bd"] * 3)
            self.assertEqual(result["records"]["TRACK/REAL-PARAM"]["actual_bits"][0], "0x360637bd")
            self.assertEqual(before, hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
