"""Read the two preserved BOOT control records; never modify or solve anything.

The runner verifies completed snapshot receipts before calling this module.
This reader implements the little-endian, four-byte-word Ganlib XSM format
used by the pinned runtime (xsm_c.c:xsmdir/xsmlid, kdi_c.c:kdiget_c).
It is not a general XSM or complete B2B admission validator.
"""

from __future__ import annotations

from contextlib import contextmanager
import math
import mmap
import os
from pathlib import Path
import struct


class SnapshotControlError(ValueError):
    pass


class _XSM:
    def __init__(self, data):
        self.data = data
        if self.read(0, 3)[:4] != b"$XSM":
            raise SnapshotControlError("not a supported little-endian Ganlib XSM archive")
        self.root = self.directory(self.integers(2, 1)[0])

    def read(self, offset, words):
        if offset < 0 or words < 0 or (offset + words) * 4 > len(self.data):
            raise SnapshotControlError("XSM record offset/length outside file")
        return self.data[offset * 4:(offset + words) * 4]

    def integers(self, offset, count):
        return struct.unpack(f"<{count}i", self.read(offset, count))

    def directory(self, start):
        result, seen, offset = {}, set(), start
        while offset not in seen:
            seen.add(offset)
            header = self.read(offset, 8)
            magic, capacity, count, following, _ = struct.unpack_from("<4s4i", header)
            if magic != b"$$$$" or not 0 <= count <= capacity <= 30:
                raise SnapshotControlError("invalid XSM directory header")
            payload = self.read(offset + 8, 6 * capacity)
            for index in range(count):
                record = tuple(struct.unpack_from("<i", payload, 4 * (k * capacity + index))[0]
                               for k in range(3))
                try:
                    name = payload[12 * (capacity + index):12 * (capacity + index + 1)].decode("ascii").rstrip(" \0")
                except UnicodeDecodeError as error:
                    raise SnapshotControlError("invalid XSM record name") from error
                if name in result:
                    raise SnapshotControlError(f"duplicate XSM record: {name}")
                result[name] = record
            offset = following
        if offset != start:
            raise SnapshotControlError("invalid XSM directory extent cycle")
        return result

    def record(self, directory, name, length, type_code):
        entry = directory.get(name)
        if entry is None or entry[1:] != (length, type_code):
            raise SnapshotControlError(f"{name}: expected length={length}, type={type_code}; actual={entry}")
        return self.read(entry[0], length)

    def object(self, name):
        # LCM lists store each archive item through the reserved handle node.
        raw = self.record(self.root, name, 1, 10)
        item = self.directory(struct.unpack("<i", raw)[0])
        handle = item.get("***HANDLE***")
        if handle is None or handle[1:] != (-1, 0):
            raise SnapshotControlError(f"{name}: expected a directory-valued archive item")
        return self.directory(handle[0])


@contextmanager
def _open_xsm(path):
    with Path(path).open("rb") as stream:
        before = os.fstat(stream.fileno())
        if before.st_size < 12:
            raise SnapshotControlError("truncated XSM header")
        with mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_READ) as data:
            yield _XSM(data)
        after = os.fstat(stream.fileno())
        if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
            raise SnapshotControlError("snapshot changed during read-only control audit")


def _float_bits(value):
    try:
        raw = struct.pack("<f", value)
    except (OverflowError, struct.error) as error:
        raise SnapshotControlError("route control is not representable as REAL32") from error
    promoted = struct.unpack("<f", raw)[0]
    if not math.isfinite(promoted) or promoted <= 0:
        raise SnapshotControlError("route control must be finite and positive in REAL32")
    return struct.unpack("<I", raw)[0]


def audit_snapshot_controls(path: Path, *, eps_radial: float, eps_axial: float,
                            eps_mccg: float) -> dict:
    """Apply exactly B2B:296-307 and 374-379 to one completed archive slot."""
    allowed = [_float_bits(eps_radial), _float_bits(eps_axial)]
    tracking = _float_bits(eps_mccg)
    reports = {}
    with _open_xsm(path) as archive:
        if struct.unpack("<i", archive.record(archive.root, "LISTDIM", 1, 1))[0] != 1:
            raise SnapshotControlError("snapshot archive must have LISTDIM=1")
        for owner, name, count, targets, source in (
                ("FLUX", "EPS-CONVERGE", 5, allowed, "src/SPOR64_B2B.f90:296-307"),
                ("TRACK", "REAL-PARAM", 4, [tracking], "src/SPOR64_B2B.f90:374-379")):
            raw = archive.record(archive.object(owner), name, count, 2)
            values = struct.unpack(f"<{count}f", raw)
            bits = struct.unpack(f"<{count}I", raw)
            failures = []
            if not all(math.isfinite(value) for value in values):
                failures.append("all fields must be finite")
            if bits[0] not in targets:
                failures.append("field 1 does not match an allowed REAL32 bit pattern")
            if owner == "FLUX" and (bits[1] != bits[0] or bits[2] != bits[0]):
                failures.append("fields 2 and 3 must match field 1 bitwise")
            # B2B uses abs(value)>0, so both signed zeros are accepted here.
            tail = values[3:] if owner == "FLUX" else values[1:]
            if any(abs(value) > 0 for value in tail):
                failures.append("remaining fields must be zero")
            reports[f"{owner}/{name}"] = {
                "source_predicate": source, "pass": not failures, "failures": failures,
                "actual_bits": [f"0x{value:08x}" for value in bits],
                "allowed_field1_bits": [f"0x{value:08x}" for value in targets]}
    return {"classification": "PASS_SNAPSHOT_CONTROL_COMPATIBILITY" if all(
                record["pass"] for record in reports.values()) else "FAIL_SNAPSHOT_CONTROL_COMPATIBILITY",
            "archive": str(Path(path)), "records": reports,
            "scope": "Preserved EPS/TRACK controls only; remaining B2B and scientific gates still apply."}
