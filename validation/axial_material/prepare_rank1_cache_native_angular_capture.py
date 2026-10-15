"""Archival-only replay of actual cache map012; no import-time experiment.

Uses the sealed map011 parent and byte-exact original map012 deck. New sources
only insert INTENT(IN) archival callbacks into the two actually compiled cache
sources. Existing solver, cache, arithmetic, iteration and thresholds are kept.
The original capture diagnosis budget is 1800/600/512, separate from the failed
120-second precision-analysis family. Root alone records actual terminal exits.
"""
import argparse
import ast
from contextlib import contextmanager
import difflib
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import shutil
import stat
import struct
import sys
import time
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'validation/artifacts'
SOURCE=ART/'axial-material-rank1-cache-native-angular-capture-admission-20261007'
OUT=ART/'axial-material-rank1-cache-native-angular-capture-20261007'
TERMINAL=ART/'axial-material-rank1-cache-native-angular-capture-terminal-20261007'
PROD=ART/'axial-material-production-qualified-AB-rank1-factor-cache-20261007'
FINAL,PARENT=PROD/'AAA/map012',PROD/'AAA/map011'
BUILD=ART/'axial-material-rank1-factor-cache-build-20261007'
BUILD_SOURCE=ART/'axial-material-qualified-AB-rank1-factor-cache-build-admission-20261007'
BUILD_TERM=ART/'axial-material-qualified-AB-rank1-factor-cache-build-terminal-20261007'
BUILDER=ROOT/'validation/axial_material/prepare_qualified_AB_rank1_cache_production.py'
BUILDER_SHA='92d73658e349ea2b2816b2b770549ca22378c2595f2c9e5c9331bbf91c6abf8a'
BUILD_SEAL='e86ee99baec88585c5965b67043658a519ebde61bb32d195fc35598970e4b39f'
BUILD_TERM_SHA='c5eecbff0064a9285460c98bc01bad26ab9180a4b4e38a6186be779378ba9d96'
PREPARED_SHA='7d2154e9c722eab23f4411c9a8588ed8250da658ae880298c24dfb53308656b5'
STATUS_SHA='03b68ebd59c7bfff9eca8f02961e1ae528bf4debf815dd23ae0d0a2cdf03051d'
FINAL_SEAL_SHA='64293bc1022a44d3cbf5e738bf1b79f4f2aa7b8958d572a59cc8c2b3ca968d59'
PARENT_SEAL_SHA='907867d184b856b2e8a7aeadceb0e9c40a006b2fd1798a3895577e2d50c3aa15'
KERNEL_SHA='c017167b5c48bc922efb7353db8c11a91758add1c2c5a02c42bd2baaeba210a2'
SENDER_SHA='bb901bfed9a4199a5b4c98c58c93bf3b3dda597fd2047bfed6d267c8dcadac81'
MODULE=ROOT/'validation/axial_material/rank1_cache_capture_angles.f90'
NG,NUN,NZ,NA,NR,NL=370,1800,48,32,8,3
TOTAL_WALL,STAGE_WALL,RSS=1800,600,512
HISTORY_CAP,FREE_FLOOR=96*2**30,8*2**30
THREAD_KEYS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
TERMINAL_SCHEMA='AXMAT_RANK1_NATIVE_ANGULAR_CAPTURE_ACTUAL_EXTERNAL_TERMINAL_RETURN_V1'
TAIL_FIELDS=('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources')


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()

def read(path):
    return json.loads(Path(path).read_text())

def write_new(path, data):
    with Path(path).open("x") as stream:
        json.dump(data, stream, indent=2, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())

def require(path, wanted=None):
    path = Path(path)
    normal_path(path)
    if not path.is_file() or (wanted is not None and digest(path) != wanted):
        raise ValueError("missing or changed declared file: " + str(path))
    return path


def normal_path(path,allow_missing=False):
    """Ordinary paths have no leaf or ancestor aliases; native aliases are explicit."""
    path=Path(path)
    if not path.is_absolute() or '..' in path.parts:raise ValueError('absolute ordinary path required')
    for endpoint in [*reversed(path.parents),path]:
        try:info=endpoint.lstat()
        except FileNotFoundError:
            if allow_missing:continue
            raise ValueError('ordinary path component missing: '+str(endpoint))
        if stat.S_ISLNK(info.st_mode):raise ValueError('ordinary path/ancestor alias forbidden: '+str(endpoint))
        if endpoint!=path and not stat.S_ISDIR(info.st_mode):raise ValueError('ordinary ancestor is not a directory')
    return path

def verify(files):
    for path, wanted in files.items():
        require(path, wanted)

def once(text, old, new):
    if text.count(old) != 1:
        raise ValueError("archival source anchor is absent or ambiguous: " + old[:100])
    return text.replace(old, new, 1)

def patched(original, changes, path, origin):
    changed = original
    for old, new in changes:
        changed = once(changed, old, new)
    restored = changed
    for old, new in reversed(changes):
        restored = once(restored, new, old)
    if restored != original:
        raise ValueError("archival patch changed native text outside listed insertions")
    path.write_text(changed)
    path.with_suffix(path.suffix + ".patch").write_text("".join(difflib.unified_diff(
        original.splitlines(True), changed.splitlines(True),
        fromfile=origin, tofile="isolated-archival-callbacks-only")))
    return dict(origin=origin, original_sha256=hashlib.sha256(original.encode()).hexdigest(),
                candidate_sha256=digest(path), replacements=changes,
                full_text_restored_exactly=True, native_expressions_changed=False)

def guard_admission(full):
    path = Path(full.__file__).resolve()
    require(path, "70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6")
    folder = full.OUT / "preflight/live_guard"
    require(folder / "guard_controls.json", "ae4d7e86423a187c29efd5bf87d54053081d7b7fcf18ac88cd9e49639cb07454")
    guard = read(folder / "guard_controls.json")
    tested = require(folder / "tested_driver_source.py", guard["source_sha256"])
    verify({str(folder / name): sha for name, sha in guard["control_files"].items()})
    def class_text(source):
        text = source.read_text()
        return next(ast.get_source_segment(text, n) for n in ast.parse(text).body
                    if isinstance(n, ast.ClassDef) and n.name == "OwnRSSSerialExecutor")
    if (class_text(path) != class_text(tested) or not guard["positive_child_completed"]
            or not guard["actual_oversize_child_rejected"] or not guard["terminated_own_child_not_live"]
            or guard["rss_cap_mib"] != 512):
        raise ValueError("byte-exact tested live guard with actual positive/oversize controls required")
    return [path, folder / "guard_controls.json", tested,
            *[folder / name for name in guard["control_files"]]]

def read_capture(path):
    """Parse native stream words without any scale correction or field repair."""
    import numpy as np
    with Path(path).open("rb") as stream:
        def words(dtype, count):
            raw = stream.read(np.dtype(dtype).itemsize * count)
            if len(raw) != np.dtype(dtype).itemsize * count:
                raise ValueError("truncated production capture")
            return np.frombuffer(raw, dtype).copy()
        if stream.read(8) != b"AXCAP002":
            raise ValueError("undeclared capture schema")
        dims = words("<i4", 11)
        if dims[:6].tolist() != [NG, NUN, NZ, NA, NR, NL] or dims[7] != 3:
            raise ValueError("full actual production capture dimensions required")
        term_int, term_real = words("<i4", 9), words("<f8", 7)
        b2, norm = words("<f4", 4), words("<f8", 2)
        cache_stats = words("<i8", 6)
        groups = []
        for g in range(1, NG + 1):
            record = dict(context=words("<i4", 9))
            for name in ("published", "published_source"):
                record[name] = words("<f8", NUN)
            if record["context"][0] != g:
                raise ValueError("all 370 groups in original order required")
            groups.append(record)
        if stream.read(1):
            raise ValueError("unexpected capture trailing words")
    directory = Path(path).parent
    with (directory / "angular_pre_normal.bin").open("rb") as stream:
        if stream.read(8) != b"AXCPN001" or np.frombuffer(stream.read(8), "<i4").tolist() != [NUN, NG]:
            raise ValueError("original pre-normalization archive dimensions differ")
        raw = stream.read()
        if len(raw) != NUN * NG * 8:
            raise ValueError("original pre-normalization field is incomplete")
        before = np.frombuffer(raw, "<f8").copy().reshape((NUN, NG), order="F")
    for g, record in enumerate(groups, 1):
        record["before_normal"] = before[:, g - 1]
        with (directory / f"angular_field_g{g:03d}.bin").open("rb") as stream:
            if stream.read(8) != b"AXCFD001":
                raise ValueError("actual angular field schema differs")
            header = np.frombuffer(stream.read(32), "<i4").copy()
            if header[:4].tolist() != record["context"][:4].tolist() or header[4:7].tolist() != dims[8:11].tolist():
                raise ValueError("angular field is not the last chronological source call")
            for name, dtype, count in [("integer", "<i4", dims[8]), ("single", "<f4", dims[9]),
                                        ("double", "<f8", dims[10])]:
                raw = stream.read(int(count) * np.dtype(dtype).itemsize)
                if len(raw) != int(count) * np.dtype(dtype).itemsize:
                    raise ValueError("actual angular field payload is incomplete")
                record[name] = np.frombuffer(raw, dtype).copy()
            if stream.read(1):
                raise ValueError("unexpected angular field trailing words")
        for name, prefix, magic in [("s2", "source", b"AXCS2001"),
                                     ("returned", "return", b"AXCRT001")]:
            with (directory / f"angular_{prefix}_g{g:03d}.bin").open("rb") as stream:
                if stream.read(8) != magic:
                    raise ValueError("actual source/return schema differs")
                header = np.frombuffer(stream.read(20), "<i4").copy()
                if header[:4].tolist() != record["context"][:4].tolist() or header[4] != NUN:
                    raise ValueError("source/return is not the final original group call")
                raw = stream.read()
                if len(raw) != NUN * 8:
                    raise ValueError("actual full source/return payload is incomplete")
                record[name] = np.frombuffer(raw, "<f8").copy()
    return dict(dimensions=dims, terminal_integer=term_int, terminal_real=term_real,
                b2=b2, normalization=norm, cache_stats=cache_stats, groups=groups)

def unpack(group, nmat):
    import numpy as np
    output = {}
    def split(data, fields):
        first = 0
        for name, shape in fields:
            count = int(np.prod(shape));output[name] = data[first:first + count].reshape(shape, order="F")
            first += count
        if first != data.size:
            raise ValueError("actual production archive payload layout differs")
    split(group["integer"], [("mat1d", (NZ,)), ("mat", (NZ, NR)),
                             ("ncode", (2,)), ("opposite", (NA,)), ("white_row", (1,)), ("ischm", (1,)), ("lfixup", (1,))])
    split(group["single"], [("vol1d", (NZ,)), ("total", (nmat + 1,)),
        ("sgas", (nmat + 1, NL)), ("basis", (NR, 1)), ("vol2d", (NR,)),
        ("zcode", (2,)), ("mu", (NA,)), ("w", (NA,)), ("pl", (NL, NA))])
    split(group["double"], [("white_perimeter", (1,)), ("radial2d", (NR, 3)), ("weight", (NR,)), ("mass", (1, 1)),
        ("total_projected", (1, 1, NZ)), ("radial_projected", (1, 1, NZ)),
        ("scat_projected", (1, 1, NL, NZ)), ("mn", (NA, NL)), ("dn", (NL, NA)),
        ("white_angle", (NA, NA)), ("white_mode", (1, 1)), ("qext", (1, NL, NZ, NR)),
        ("source_projected", (NL, NZ, 1)), ("cell", (NA, 1, NZ)), ("face", (NA, 1, NZ + 1)),
        ("modal_flux", (NL, NZ, 1)), ("modal_current", (NZ + 1, 1)),
        ("flux", (1, NL, NZ, NR)), ("current", (NZ + 1, NR)), ("xnei", (NA, NR))])
    return output

def audit_events(capture):
    import numpy as np
    latest = np.zeros((NG, 3), dtype="<i4")
    per_group_calls = np.zeros(NG, dtype="<i4")
    count = 0
    with (OUT / "AAA/angular_capture_events.bin").open("rb") as stream:
        if stream.read(8) != b"AXCEV002":
            raise ValueError("actual source dispatch inventory schema differs")
        header = np.frombuffer(stream.read(72), "<i4").copy()
        if header.size != 18 or header[11:].tolist() != [1, 2, 1, 1, 0, 32, 1]:
            raise ValueError("actual ITPIJ/NANIS/NDIM/INSB/LSCAL source contract differs")
        if header[[0, 1, 2, 4, 5, 6, 7, 8, 9, 10]].tolist() != [NG, NUN, NR * NZ, NL, 3, 3, 1, 0, 3, 0]:
            raise ValueError("actual source dispatch production contract differs")
        if header[3] != capture["dimensions"][6]:
            raise ValueError("actual dispatched material count differs")
        while raw := stream.read(16):
            if len(raw) != 16:
                raise ValueError("incomplete chronological source event")
            sequence, outer, inner, nactive = np.frombuffer(raw, "<i4")
            count += 1
            if sequence != count or not 1 <= nactive <= NG or outer <= 0 or inner <= 0:
                raise ValueError("invalid chronological source dispatch")
            raw = stream.read(int(nactive) * 4)
            if len(raw) != int(nactive) * 4:
                raise ValueError("incomplete original NGIND event")
            ngind = np.frombuffer(raw, "<i4").copy()
            raw = stream.read(NG * 4)
            if len(raw) != NG * 4:
                raise ValueError("incomplete original NPSYS event")
            npsys = np.frombuffer(raw, "<i4").copy()
            raw = stream.read(16)
            if len(raw) != 16:
                raise ValueError("incomplete original B2 event")
            b2 = np.frombuffer(raw, "<f4").copy()
            if (len(set(ngind.tolist())) != nactive or (ngind < 1).any() or (ngind > NG).any()
                    or not np.array_equal(ngind, np.flatnonzero(npsys) + 1) or b2[3] != 0):
                raise ValueError("actual post-SIGS dispatch metadata differs")
            latest[ngind - 1] = [sequence, outer, inner]
            per_group_calls[ngind - 1] += 1
    if count != capture["terminal_integer"][7]:
        raise ValueError("final publication does not cover every actual dispatch")
    for g, group in enumerate(capture["groups"]):
        if not np.array_equal(latest[g], group["context"][1:4]):
            raise ValueError("published group did not retain its chronological last call")
        if group["context"][6] != 1:
            raise ValueError("one actual first miss must archive each group block")
    return dict(dispatches=count, all_370_groups_last_context=[3, 1],
                actual_NGIND_and_NPSYS_archived=True, per_group_calls=per_group_calls.tolist(), metric_based_selection=False)

@contextmanager
def stream_xsm(path):
    """Use the frozen parser with bounded record reads, avoiding two 238 MiB maps.

    The complete snapshot equality walk touches both archives. Keeping those
    mappings resident alongside the capture would needlessly cross 512 MiB.
    """
    from snapshot_control_preflight import _XSM
    with Path(path).open("rb") as stream:
        before = os.fstat(stream.fileno())
        class Words:
            def __len__(self):
                return before.st_size
            def __getitem__(self, item):
                if not isinstance(item, slice) or item.step not in (None, 1):
                    raise ValueError("frozen XSM reader requested an unsupported byte access")
                first, stop, _ = item.indices(before.st_size)
                result = os.pread(stream.fileno(), stop - first, first)
                if len(result) != stop - first:
                    raise ValueError("incomplete original XSM record read")
                return result
        yield _XSM(Words())
        after = os.fstat(stream.fileno())
        if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
            raise ValueError("scientific archive changed during equality audit")

def audit(expected):
    import numpy as np
    from probe_refined_AAA_white_odd_response import same_object, field
    declaration = child_admission(expected)
    _, _, _, list_handles = modules()
    open_xsm = stream_xsm
    actual_env = dict(python=sys.version.split()[0], numpy=np.__version__)
    if any(actual_env[k] != declaration["numeric_environment"][k] for k in actual_env):
        raise ValueError("declared audit numerical environment changed")
    capture = read_capture(OUT / "AAA/angular_capture.bin")
    events = audit_events(capture)
    cache_events = audit_cache_events(capture, events)
    slot_observation = audit_slots(capture)
    integers = capture["terminal_integer"]
    if integers[:7].tolist() != [3, 1, 371, 1, 1, 500, 740] or integers[8] != NG:
        raise ValueError("exact predeclared original terminal is required")
    real = capture["terminal_real"]
    if not (real[0] < real[1] and real[2] < real[3] and real[4] < real[5]):
        raise ValueError("unchanged strict native final gates did not pass")
    # The full output archive comparison checks all scientific moments/currents,
    # source, balance metadata and keff, including records not used by this audit.
    for name in ("candidate_axial.xsm", "candidate_snapshots.xsm"):
        with stream_xsm(FINAL / name) as old, stream_xsm(OUT / "AAA" / name) as new:
            same_object(old, old.root, new, new.root)
    with open_xsm(OUT / "AAA/candidate_axial.xsm") as archive:
        handles = list_handles(archive, archive.root, "FLUX64", NG)
        keff = field(archive, archive.root, "SPOT-KEFF64", "<f8", 1)
        if keff.tobytes() != capture["normalization"][:1].tobytes():
            raise ValueError("captured actual keff differs from published record")
        published = [np.frombuffer(archive.read(h[0], h[1]), "<f8").copy() for h in handles]
        flux32 = [np.frombuffer(archive.read(h[0], h[1]), "<f4").copy()
                  for h in list_handles(archive, archive.root, "FLUX", NG)]
        source32 = [np.frombuffer(archive.read(h[0], h[1]), "<f4").copy()
                    for h in list_handles(archive, archive.root, "SOUR", NG)]
    if not np.isfinite(capture["normalization"]).all() or capture["normalization"][1] <= 0:
        raise ValueError("actual positive native normalization operands required")
    rows = []
    for g, (group, final) in enumerate(zip(capture["groups"], published, strict=True), 1):
        context = group["context"]
        if (context[2:4].tolist() != [3, 1] or context[1] != context[4] or context[5] <= 0
                or context[6] <= 0 or context[6] != 1 or context[7] != context[5] or context[8] != 1):
            raise ValueError("chronological last capture is not original terminal group call")
        if any(not np.isfinite(group[k]).all() for k in (
            "single", "double", "s2", "returned", "before_normal", "published", "published_source")):
            raise ValueError("nonfinite actual archive words")
        a = unpack(group, int(capture["dimensions"][6]))
        independent_keys(group, a, g)
        if (a["ncode"].tolist() != [1, 1] or (a["zcode"] != 0).any()
                or (a["w"] <= 0).any() or (a["vol1d"] <= 0).any()):
            raise ValueError("unchanged positive quadrature and vacuum boundary contract required")
        if group["s2"][:1152].tobytes() != a["qext"].ravel(order="F").tobytes():
            raise ValueError("actual post-SIGS S2/qext source words differ")
        if (0.5 * (a["face"][:, :, :-1] + a["face"][:, :, 1:])).tobytes() != a["cell"].tobytes():
            raise ValueError("actual native diamond cell/shared-face identity differs")
        # Every source projection is tested, with the exact region accumulation
        # order of the frozen rank1 solver, including the native void-material skip.
        projected_source = np.zeros((NL, NZ), dtype="<f8")
        for iz in range(NZ):
            for region in range(NR):
                if a["mat"][iz, region] == 0:
                    continue
                for l in range(NL):
                    projected_source[l, iz] += (float(a["weight"][region]) *
                        float(a["basis"][region, 0])) * float(a["qext"][0, l, iz, region])
        if projected_source.tobytes() != a["source_projected"][:, :, 0].tobytes():
            raise ValueError("actual complete projected source coefficients differ")
        returned = np.concatenate([a["flux"].ravel(order="F"), a["current"].ravel(order="F"),
                                   a["xnei"].ravel(order="F")])
        if (returned.tobytes() != group["returned"].tobytes()
                or group["returned"].tobytes() != group["before_normal"].tobytes()
                or group["published"].tobytes() != final.tobytes()):
            raise ValueError("all raw returned moments/currents or final FLUX64 words changed")
        normalized = group["returned"] * (capture["normalization"][0] / capture["normalization"][1])
        if normalized.tobytes() != final.tobytes():
            raise ValueError("original one global normalization operation differs")
        normalized_source = group["s2"] * (capture["normalization"][0] / capture["normalization"][1])
        if normalized_source.tobytes() != group["published_source"].tobytes():
            raise ValueError("actual raw S2 does not reproduce original normalized REAL64 source")
        if (group['published'].astype('<f4').tobytes()!=flux32[g-1].tobytes()
                or group['published_source'].astype('<f4').tobytes()!=source32[g-1].tobytes()):
            raise ValueError('actual post-normalization fields/source do not reproduce native REAL32 saved records')
        # Reproduce actual native summation/reconstruction order, with no BLAS.
        modal = np.zeros((NL, NZ), dtype="<f8");current = np.zeros(NZ + 1, dtype="<f8")
        for l in range(NL):
            for n in range(NA):
                modal[l] += a["dn"][l, n] * a["cell"][n, 0]
        for n in range(NA):
            current += float(a["w"][n]) * float(a["mu"][n]) * a["face"][n, 0]
        if (modal.tobytes() != a["modal_flux"][:, :, 0].tobytes()
                or current.tobytes() != a["modal_current"][:, 0].tobytes()):
            raise ValueError("stored angular fields do not reproduce actual moments/currents")
        if (a["face"][a["mu"] > 0, 0, 0] != 0).any() or (a["face"][a["mu"] < 0, 0, -1] != 0).any():
            raise ValueError("actual vacuum incoming fields must be exactly zero")
        block_path = OUT / "AAA" / f"angular_collision_g{g:03d}.bin"
        with block_path.open("rb") as stream:
            if stream.read(8) != b"AXCBL001":
                raise ValueError("actual native collision schema differs")
            header = np.frombuffer(stream.read(32), "<i4").copy()
            blocks = np.frombuffer(stream.read(), "<f8").copy()
        if (header[0] != g or header[1] != context[5] or header[4:].tolist() != [NA, NZ + 1, 1, 0]
                or blocks.size != 3 * NA * NA * (NZ + 1) or not np.isfinite(blocks).all()):
            raise ValueError("complete actual first native collision block inventory required")
        lower, diagonal, upper = [
            blocks[j * NA * NA * (NZ + 1):(j + 1) * NA * NA * (NZ + 1)].reshape(
                (NA, NA, NZ + 1), order="F") for j in range(3)]
        face = a["face"][:, 0]
        rhs = np.zeros((NA, NZ + 1))
        for iz in range(NZ):
            q = np.zeros(NA)
            for l in range(NL):
                q += a["mn"][:, l] * a["source_projected"][l, iz, 0]
            rhs[a["mu"] > 0, iz + 1] = float(a["vol1d"][iz]) * q[a["mu"] > 0]
            rhs[a["mu"] < 0, iz] = float(a["vol1d"][iz]) * q[a["mu"] < 0]
        defect = np.empty_like(rhs);scale = np.empty_like(rhs)
        for iz in range(NZ + 1):
            terms = [diagonal[:, :, iz] @ face[:, iz]]
            absolute = [abs(diagonal[:, :, iz]) @ abs(face[:, iz])]
            if iz:
                terms.append(lower[:, :, iz] @ face[:, iz - 1])
                absolute.append(abs(lower[:, :, iz]) @ abs(face[:, iz - 1]))
            if iz < NZ:
                terms.append(upper[:, :, iz] @ face[:, iz + 1])
                absolute.append(abs(upper[:, :, iz]) @ abs(face[:, iz + 1]))
            defect[:, iz] = sum(terms) - rhs[:, iz]
            scale[:, iz] = sum(absolute) + abs(rhs[:, iz])
        null_nonzero = (scale == 0) & (defect != 0)
        ratio = np.divide(abs(defect), scale, out=np.zeros_like(scale), where=scale > 0)
        rows.append(dict(group=g, context=context.tolist(), native_block_assembly_count=int(context[6]),
            native_block_cache_enabled=True, first_cache_miss_blocks_and_all_hits_exact_operator_key=True,
            raw_S2_one_global_normalization_published_source_byte_exact=True,
            minimum_modal_cell=float(a["cell"].min()),
            minimum_shared_face=float(a["face"].min()), negative_modal_cell_count=int((a["cell"] < 0).sum()),
            negative_shared_face_count=int((a["face"] < 0).sum()),
            minimum_physical_angular_cell=float((a["basis"][:, 0, None, None] * a["cell"][:, 0][None]).min()),
            minimum_physical_angular_face=float((a["basis"][:, 0, None, None] * a["face"][:, 0][None]).min()),
            full_native_matrix_equation_relative=float(ratio.max()),
            zero_scale_nonzero_defect_count=int(null_nonzero.sum()),
            original_1e10_diagnostic_gate_passed=bool(not null_nonzero.any() and ratio.max() <= 1e-10),
            all_three_raw_moments_and_currents_byte_exact=True))
        # Preserve the raw defect and scale for every group; positivity and the
        # equation ledger are diagnostic findings, never repaired or hidden.
        np.savez(OUT / "audit" / f"ledger_g{g:03d}.npz", defect=defect, scale=scale,
                 ratio=ratio, zero_scale_nonzero_defect=null_nonzero)
    write_new(OUT / "audit/result.json", dict(
        classification="COMPLETE_RANK1_NATIVE_ANGULAR_CAPTURE_ONLY", groups=rows,
        chronological_inventory=events, cache_identity_inventory=cache_events, slot_observation=slot_observation,
        complete_production_370_groups=True, original_map012_scientific_records_word_exact=True,
        original_terminal_passed=True, all_three_moments_and_currents_byte_exact=True,
        original_keff_byte_exact=True, raw_fields_and_sources_unmodified=True,
        negative_fields_repaired=False, equation_accounting_modified=False,
        original_accuracy_thresholds_changed=False, production_solver_promoted=False,
        AAA_accuracy_qualified=False, ABA_admitted=False))
    print("AXMAT-RANK1-NATIVE-ANGULAR-CAPTURE-AUDITED")


def load(path,name):
    path=require(path)
    if name in sys.modules:
        m=sys.modules[name]
        if Path(m.__file__).resolve()!=path.resolve():raise ValueError('module binding differs')
        return m
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m)
    if Path(m.__file__).resolve()!=path.resolve():raise ValueError('actual source binding differs')
    return m


def builder():
    return load(require(BUILDER,BUILDER_SHA),'rank1_native_capture_actual_builder')


def modules():
    # Genuine frozen helper + tested parent class; no controller/global overlay.
    full,production=builder().helper().modules()
    from snapshot_control_preflight import _open_xsm
    from qualified_snapshot_ingestion import list_handles
    return full,production,_open_xsm,list_handles


def absent(path):
    normal_path(path,allow_missing=True)
    if Path(path).exists() or Path(path).is_symlink():raise ValueError('exclusive new family; no overwrite/retry')


def pin(path):
    return dict(path=str(require(path)),sha256=digest(path))


def inventory(root):
    normal_path(root)
    if not Path(root).is_dir():raise ValueError('private inventory root must be a directory')
    files={};directories=[]
    for folder,dirs,names in os.walk(root,followlinks=False):
        if any((Path(folder)/n).is_symlink() for n in [*dirs,*names]):raise ValueError('private namespace symlink')
        for name in names:
            p=Path(folder)/name
            if not p.is_file():raise ValueError('private namespace must contain regular files')
            files[str(p.relative_to(root))]=digest(p)
        directories.extend(str((Path(folder)/name).relative_to(root)) for name in dirs)
    return dict(files=files,symlinks={},directories=sorted(directories))


def verify_inventory(root,wanted):
    if inventory(root)!=wanted:raise ValueError('complete private namespace differs')


def archive_bytes():
    total=0
    for root in (SOURCE,OUT):
        normal_path(root)
        for folder,dirs,names in os.walk(root,followlinks=False):
            if any((Path(folder)/n).is_symlink() for n in [*dirs,*names]):raise ValueError('private archive alias forbidden')
            for name in names:
                info=(Path(folder)/name).stat(follow_symlinks=False)
                if not stat.S_ISREG(info.st_mode):raise ValueError('nonregular private archive')
                total+=info.st_size
    return total


def resource(roots):
    return builder().DynamicHistoryResources(ART,roots,FREE_FLOOR,HISTORY_CAP)


def environment(d):
    builder().helper().environment(d)
    if d['resource_scope_contract']!=builder().resource_scope_contract():raise ValueError('family policy differs')
    for key in THREAD_KEYS:
        if os.environ.get(key)!='1':raise ValueError('one thread required')
    if 'native_dependency_alias_bindings' in d:
        for path,expected in d['native_dependency_alias_bindings'].items():
            p=Path(path)
            if not p.is_symlink() or os.readlink(p)!=expected['text'] or str(p.resolve(strict=True))!=expected['target']:
                raise ValueError('explicit native alias literal/canonical binding differs')
            normal_path(expected['target'])


def native_alias_bindings(declared):
    """Freeze only aliases on already-declared native dependency paths."""
    result={}
    for path,target in declared.items():
        p=Path(path)
        if str(p.resolve(strict=True))!=target:raise ValueError('inherited native canonical target differs')
        normal_path(target)
        for component in [*reversed(p.parents),p]:
            if component.is_symlink():
                item=dict(text=os.readlink(component),target=str(component.resolve(strict=True)))
                if str(component) in result and result[str(component)]!=item:raise ValueError('conflicting native alias binding')
                result[str(component)]=item
    return result


def preserved_files(d):
    result=dict(d['files'])
    for entry in d['preserved_predecessors']:
        root=Path(entry['root'])
        for relative,sha in entry['inventory']['files'].items():
            path=str(root/relative)
            if path in result and result[path]!=sha:raise ValueError('conflicting inherited file identity')
            result[path]=sha
    return result


def descriptor_files(value):
    """Only explicit path/SHA descriptors, never path-looking strings."""
    result={}
    def walk(item):
        if isinstance(item,dict):
            if 'path' in item and 'sha256' in item:
                path,sha=item['path'],item['sha256']
                if not isinstance(path,str) or not Path(path).is_absolute() or not re.fullmatch('[0-9a-f]{64}',sha or ''):
                    raise ValueError('malformed inherited endpoint descriptor')
                if path in result and result[path]!=sha:raise ValueError('conflicting inherited descriptor')
                result[path]=sha
            for nested in item.values():walk(nested)
        elif isinstance(item,list):
            for nested in item:walk(nested)
    walk(value)
    return result


def source_plan():
    sender=require(BUILD_SOURCE/'FLU2DR64.f',SENDER_SHA).read_text()
    kernel=require(BUILD_SOURCE/'SPOT1P64.f90',KERNEL_SHA).read_text()
    f=[]
    anchor='     2 SPOT1P64_RANK1_TERMINAL,SPOT1P64_RANK1_PROGRESS'
    f.append((anchor,anchor+',\n     3 SPOT1P64_RANK1_STATS\n      USE AXMAT_RANK1_CAPTURE_MOD, ONLY: AXMAT_CAPTURE_BEGIN,\n     1 AXMAT_CAPTURE_CONTEXT,AXMAT_CAPTURE_TERMINAL,\n     2 AXMAT_CAPTURE_PRENORMAL,AXMAT_CAPTURE_PUBLISH,\n     3 AXMAT_CAPTURE_SLOT7\n      INTEGER(KIND=8) AXMAT_STATS(6)'))
    begin="      CALL SPOT1P64_CACHE_BEGIN(NGRP,IPHYS_CACHE.EQ.1,\n     1 (CXDOOR.EQ.'SPOT').AND.(NDIM.EQ.1).AND.(INSB.GT.0)\n     2 .AND.(IPHYS_CACHE.EQ.0))"
    f.append((begin,begin+'\n      CALL AXMAT_CAPTURE_BEGIN(NGRP,NUNKNO,NREG,NMAT,NFUNL,\n     1 ITYPEC,ILEAK,LEAKSW,LREBAL,NCPTL,NCPTA,ITPIJ,NANIS,\n     2 NDIM,INSB,LSCAL,NLF,NLIN)'))
    jt='      DO 270 JT=1,MAXINR'
    f.append((jt,jt+'\n      CALL AXMAT_CAPTURE_CONTEXT(IT,JT)'))
    accel='      IF(MOD(JT-1,NCTOT).GE.NCPTM) THEN\n         CALL FLU2AC64(NGRP,NUNKNO,IGDEB,FLUX(:,:,5:7),\n     1   AKEEP(5:7),ZMU64,LACCOK)\n         IF(.NOT.LACCOK)\n     1   CALL XABORT(\'FLU2DR64: INNER FLU2AC64 FAILED.\')\n         ZMU=REAL(ZMU64)\n      ELSE\n         ZMU=1.0\n      ENDIF'
    before='      CALL AXMAT_CAPTURE_SLOT7(1,NUNKNO,NGRP,IGDEB,\n     1 MERGE(1,0,MOD(JT-1,NCTOT).GE.NCPTM),\n     2 FLUX(:,:,6),FLUX(:,:,7))\n'
    after='\n      CALL AXMAT_CAPTURE_SLOT7(2,NUNKNO,NGRP,IGDEB,\n     1 MERGE(1,0,MOD(JT-1,NCTOT).GE.NCPTM),\n     2 FLUX(:,:,6),FLUX(:,:,7))'
    f.append((accel,before+accel+after))
    promote='      FLUX(:NUNKNO,:NGRP,3)=FLUX(:NUNKNO,:NGRP,7)'
    f.append((promote,'      CALL AXMAT_CAPTURE_SLOT7(3,NUNKNO,NGRP,IGDEB,0,\n     1 FLUX(:,:,6),FLUX(:,:,7))\n'+promote))
    success='         GO TO 410\n      ENDIF\n'
    f.append((success,'         CALL SPOT1P64_RANK1_STATS(AXMAT_STATS(1),\n     1 AXMAT_STATS(2),AXMAT_STATS(3),AXMAT_STATS(4),\n     2 AXMAT_STATS(5),AXMAT_STATS(6))\n         CALL AXMAT_CAPTURE_TERMINAL(IEXTF,ITERF_LAST,\n     1 IGDEB_LAST,IINR_STATE,IUNK_EVAL,MAXOUT,MAXINR,\n     2 EEXT,EPSOUT,EUNK_LAST,EPSUNK,EINR_LAST,EPSINR,AKEFF,\n     3 AXMAT_STATS,FLUX(:,:,2),FLUX(:,:,3),\n     4 FLUX(:,:,7),FLUX(:,:,8))\n'+success))
    normal='        IF(ITYPEC.LT.5) THEN\n          FLUX(:NUNKNO,:NGRP,3)=FLUX(:NUNKNO,:NGRP,3)*(AKEFF/FISOUR)'
    f.append((normal,'        CALL AXMAT_CAPTURE_PRENORMAL(NUNKNO,NGRP,\n     1 FLUX(:NUNKNO,:NGRP,3))\n'+normal))
    save='  510 CONTINUE\n      IF(C_ASSOCIATED(IPSOU)) THEN'
    f.append((save,'  510 CONTINUE\n      CALL AXMAT_CAPTURE_PUBLISH(NUNKNO,NGRP,\n     1 FLUX(:NUNKNO,:NGRP,3),FLUX(:NUNKNO,:NGRP,4),\n     2 AKEFF,FISOUR)\n      IF(C_ASSOCIATED(IPSOU)) THEN'))
    use='      USE GANLIB\n      TYPE(C_PTR) JPSYS,IPTRK'
    f.append((use,'      USE GANLIB\n      USE AXMAT_RANK1_CAPTURE_MOD, ONLY: AXMAT_CAPTURE_INPUT,\n     1 AXMAT_CAPTURE_OUTPUT\n      TYPE(C_PTR) JPSYS,IPTRK'))
    call='      CALL SPOF64(KPSYS,IPTRK,IMPX,NGEFF,NGIND,NREG,NMAT,NUN,MAT,\n     1 KEYFLX,F2,S2,TITR)'
    f.append((call,'      CALL AXMAT_CAPTURE_INPUT(NGEFF,NGIND,NUN,S2,ILEAK,\n     1 B2,NPSYS)\n'+call+'\n      CALL AXMAT_CAPTURE_OUTPUT(NGEFF,NGIND,NUN,F2)'))
    k=[]
    use='  use AXMAT_WHITE_TRACE_MOD, only: AXMAT_WHITE_ON,AXMAT_WHITE_ROW, &\n    AXMAT_WHITE_PERIMETER,AXMAT_WHITE_KERNEL,AXMAT_WHITE_NOTE'
    k.append((use,use+'\n  use AXMAT_RANK1_CAPTURE_MOD, only: AXMAT_CAPTURE_FIELD, &\n    AXMAT_CAPTURE_BLOCKS,AXMAT_CAPTURE_KEY,AXMAT_CAPTURE_KEY_VALIDATED'))
    field='  deallocate(opposite,modal_cour,modal_flux,cell,face)'
    k.append((field,'  call AXMAT_CAPTURE_FIELD(igroup,nmat,nsnap,mat1d,mat,ncode,opposite, &\n    vol1d,total,sgas,basis,vol2d,zcode,du,w,pl,radial2d,qext, &\n    weight,mass_m,total_m,radial_m,scat_m,source_m,mn,dn,white_angle, &\n    white_mode,cell,face,modal_flux,modal_cour,flux,cour,xnei,AXMAT_WHITE_ON, &\n    AXMAT_WHITE_ROW,AXMAT_WHITE_PERIMETER,ischm,lfixup)\n'+field))
    key='    call SPOT1P64_RANK1_GUARD(igroup,key,phase,eligible,active)'
    k.append((key,'    call AXMAT_CAPTURE_KEY(igroup,key,phase,eligible)\n'+key+'\n    call AXMAT_CAPTURE_KEY_VALIDATED(igroup,phase,active)'))
    assembly='    enddo\n\n    if (cached_path) then\n      associate(plan => SPOT1P64_PLAN(igroup)%mode(first_mode))\n        if (cache_hit) then'
    k.append((assembly,'    enddo\n\n    if (.not.cache_hit) call AXMAT_CAPTURE_BLOCKS(igroup,lower,diagonal, &\n      upper,cached_path,cache_hit)\n\n    if (cached_path) then\n      associate(plan => SPOT1P64_PLAN(igroup)%mode(first_mode))\n        if (cache_hit) then'))
    for text,changes in ((sender,f),(kernel,k)):
        changed=text
        for old,new in changes:changed=once(changed,old,new)
        for old,new in reversed(changes):changed=once(changed,new,old)
        if changed!=text:raise ValueError('entire source inverse restoration differs')
    return sender,f,kernel,k


def terminal_contract(python):
    return dict(schema=TERMINAL_SCHEMA,root=str(TERMINAL),receipt=str(TERMINAL/'terminal_return.json'),
        record_producer='root',actual_tool_exit_zero_required=True,full_stdout_required=True,full_stderr_required=True,
        record_written_after_actual_terminal_return_required=True,tail_fields=list(TAIL_FIELDS),
        complete_archive_scope_roots=[str(SOURCE),str(OUT)],action='run',python=python,
        scientific_qualification=False)


def prepare(build_seal,build_terminal,build_terminal_sha):
    for p in (SOURCE,OUT,TERMINAL):absent(p)
    if (build_seal!=BUILD_SEAL or Path(build_terminal)!=BUILD_TERM/'terminal_return.json'
            or build_terminal_sha!=BUILD_TERM_SHA):raise ValueError('actual frozen current build terminal chain required')
    b=builder();build=b.production_admission(build_seal,build_terminal,build_terminal_sha)
    bd=read(BUILD/'declaration.json');environment(bd)
    full,production,_,_=modules();guard_files=guard_admission(full)
    prepared=read(require(PROD/'prepared.json',PREPARED_SHA))
    require(PROD/'AAA/run_status.json',STATUS_SHA)
    for name,sha in prepared['local_files'].items():require(PROD/name,sha)
    production.verify_sealed_directory(FINAL);production.verify_sealed_directory(PARENT)
    require(FINAL/'result.json',FINAL_SEAL_SHA);require(PARENT/'result.json',PARENT_SEAL_SHA)
    source_inputs={name:(FINAL/name).resolve(strict=True) for name in (
        'initial_axial_track.xsm','initial_axial_macrolib.xsm','parent_axial_closed.xsm',
        'parent_snapshots_closed.xsm','candidate_radial.xsm','candidate_system.xsm','basis_reference.xsm','route_contract.xsm')}
    if source_inputs['parent_axial_closed.xsm']!=(PARENT/'closed_axial.xsm').resolve(strict=True) or source_inputs['parent_snapshots_closed.xsm']!=(PARENT/'closed_snapshots.xsm').resolve(strict=True):raise ValueError('real map011 parent inputs required')
    sender,fchanges,kernel,kchanges=source_plan()
    deck=require(FINAL/'picard_axial.x2m');native_log=require(FINAL/'picard_axial.log')
    actual_log=native_log.read_text()
    if actual_log.count('AXMAT-MOMENT-ORDER SELECTOR')!=1 or not re.search(r'AXMAT-MOMENT-ORDER SELECTOR\s+32\s+3\s+2\s+3\s+1\s*$',actual_log,re.M):raise ValueError('actual current selector marker differs')
    matches=re.findall(r'^AXMAT-RANK1-CACHE TERMINAL\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$',actual_log,re.M)
    if len(matches)!=1:raise ValueError('one actual cache terminal record required')
    original_cache=list(map(int,matches[0]))
    for text,fields in [('FLU2DR-TERM OUTER-GATE=PASS',{'IEXTF':3,'MAXOUT':500}),('FLU2DR-TERM INNER-TERMINAL',{'ITERF':1,'MAXINR':740,'IGDEB':371,'STATE':1,'NGRP':370})]:
        lines=[line for line in actual_log.splitlines() if text in line]
        if len(lines)!=1:raise ValueError('one actual native terminal pair required')
        for key,value in fields.items():
            m=re.findall(r'\b'+key+r'\s*=\s*([+-]?\d+)\b',lines[0])
            if len(m)!=1 or int(m[0])!=value:raise ValueError('native terminal input differs')
    files=preserved_files(bd)
    for name,sha in read(BUILD/'seal.json')['files'].items():files[str(BUILD/name)]=sha
    for name,sha in bd['source_inventory']['files'].items():files[str(BUILD_SOURCE/name)]=sha
    for path,sha in descriptor_files(build).items():
        if path in files and files[path]!=sha:raise ValueError('inherited actual build descriptor differs')
        files[path]=sha
    for name,sha in prepared['local_files'].items():files[str(PROD/name)]=sha
    paths=[Path(__file__).resolve(),MODULE,BUILDER,PROD/'prepared.json',PROD/'AAA/run_status.json',
        BUILD/'declaration.json',BUILD/'seal.json',BUILD/'runtime/build_identity.json',BUILD_TERM/'terminal_return.json',
        FINAL/'result.json',PARENT/'result.json',deck,native_log,*source_inputs.values(),
        FINAL/'candidate_axial.xsm',FINAL/'candidate_snapshots.xsm',BUILD_SOURCE/'SPOT1P64.f90',BUILD_SOURCE/'FLU2DR64.f',
        *guard_files,PROD/'runtime/run_bounded_dragon.py']
    # Every input of the actual frozen link and compiler chain is byte-pinned.
    parent_link=bd['build_commands'][2]
    for token in parent_link:
        p=Path(token)
        if p.is_absolute() and p.is_file():paths.append(p)
    for p in paths:
        sha=digest(require(p));key=str(p)
        if key in files and files[key]!=sha:raise ValueError('current input differs from inherited pin')
        files[key]=sha
    roots=[str(p) for p in b.validate_history_roots(b.history_roots(sorted(set(bd['resource_roots'])|set(prepared['resource_roots'])|{str(SOURCE),str(OUT),str(TERMINAL)}),ART),ART)]
    resources=resource(roots);before=resources.check();copied=sum(p.stat().st_size for p in source_inputs.values());reserve=copied+2*2**30
    if before['artifact_bytes']+reserve>=HISTORY_CAP or before['disk_free_bytes']-reserve<FREE_FLOOR:raise ValueError('original capture reservation refused')
    SOURCE.mkdir();OUT.mkdir()
    for n in ('build','runtime','AAA','audit'):(OUT/n).mkdir()
    shutil.copy2(MODULE,SOURCE/'rank1_cache_capture_angles.f90')
    proofs={'FLU2DR64.f':patched(sender,fchanges,SOURCE/'FLU2DR64.f',str(BUILD_SOURCE/'FLU2DR64.f')),
        'SPOT1P64.f90':patched(kernel,kchanges,SOURCE/'SPOT1P64.f90',str(BUILD_SOURCE/'SPOT1P64.f90'))}
    write_new(SOURCE/'source_admission.json',dict(patches=proofs,observer_only=True,native_expressions_changed=False,
        original_compiled_kernel=pin(BUILD_SOURCE/'SPOT1P64.f90'),original_compiled_sender=pin(BUILD_SOURCE/'FLU2DR64.f'),
        inherited_current_build_admission=build,full_source_inverse_byte_restoration=True))
    inputs={};aliases={}
    for name,origin in source_inputs.items():
        target=OUT/'AAA'/name;shutil.copy2(origin,target)
        if digest(target)!=digest(origin):raise ValueError('private input copy differs')
        inputs[name]=dict(source=str(origin),sha256=digest(origin),private_copy=str(target))
        original=FINAL/name
        if original.is_symlink():aliases[str(original)]=dict(text=os.readlink(original),target=str(origin),sha256=digest(origin))
    shutil.copy2(deck,OUT/'AAA/picard_axial.x2m');shutil.copy2(PROD/'runtime/run_bounded_dragon.py',OUT/'runtime/run_bounded_dragon.py')
    compiler=bd['build_commands'][0][0]
    flags=bd['build_commands'][0][1:bd['build_commands'][0].index('-c')]
    flags=[token.replace(str(BUILD_SOURCE),str(SOURCE)).replace(str(BUILD),str(OUT)) for token in flags]
    commands=[[compiler,*flags,'-c',str(SOURCE/n),'-o',str(OUT/'build'/Path(n).with_suffix('.o'))] for n in ('rank1_cache_capture_angles.f90','SPOT1P64.f90','FLU2DR64.f')]
    link=[token.replace(str(BUILD/'build/SPOT1P64.o'),str(OUT/'build/SPOT1P64.o')).replace(str(BUILD/'build/FLU2DR64.o'),str(OUT/'build/FLU2DR64.o')).replace(str(BUILD/'runtime/Dragon'),str(OUT/'runtime/Dragon')) for token in parent_link]
    idx=link.index(str(OUT/'build/SPOT1P64.o'));link.insert(idx,str(OUT/'build/rank1_cache_capture_angles.o'));commands.append(link)
    inverse=list(link);inverse.remove(str(OUT/'build/rank1_cache_capture_angles.o'));inverse=[token.replace(str(OUT/'build/SPOT1P64.o'),str(BUILD/'build/SPOT1P64.o')).replace(str(OUT/'build/FLU2DR64.o'),str(BUILD/'build/FLU2DR64.o')).replace(str(OUT/'runtime/Dragon'),str(BUILD/'runtime/Dragon')) for token in inverse]
    if inverse!=parent_link:raise ValueError('exact original link chain restoration differs')
    for root in (SOURCE,OUT):
        for p in root.rglob('*'):
            if p.is_file():files[str(p)]=digest(p)
    import numpy as np
    d=dict(schema='AXMAT_RANK1_NATIVE_ANGULAR_CAPTURE_DECLARATION_V1',files=files,source_inventory=inventory(SOURCE),
        input_copies=inputs,input_aliases=aliases,build_commands=commands,inherited_current_build_admission=build,
        original_production_prepared=pin(PROD/'prepared.json'),original_status=pin(PROD/'AAA/run_status.json'),
        original_map012_seal=pin(FINAL/'result.json'),original_map011_seal=pin(PARENT/'result.json'),
        original_deck=pin(deck),original_native_log=pin(native_log),original_cache_terminal=original_cache,
        original_link_command=parent_link,exact_original_link_inverse_restoration=True,
        preserved_predecessors=bd['preserved_predecessors'],build_python_executable=str(Path(sys.executable).resolve()),
        python_command=sys.executable,numeric_environment=dict(python=sys.version.split()[0],numpy=np.__version__),
        native_library_aliases=bd['native_library_aliases'],native_dependency_alias_bindings=native_alias_bindings(bd['native_library_aliases']),
        numerical_loader_environment=bd['numerical_loader_environment'],
        resource_roots=roots,resource_scope_contract=b.resource_scope_contract(),resource_scope_policy=bd['resource_scope_policy'],
        resources_before=before,artifact_budget_bytes=HISTORY_CAP,min_free_bytes=FREE_FLOOR,
        private_input_copy_bytes=copied,archive_reserve_bytes=reserve,complete_archive_scope_roots=[str(SOURCE),str(OUT)],
        total_wall_seconds=TOTAL_WALL,stage_wall_seconds=STAGE_WALL,rss_cap_mib=RSS,threads=1,numeric_children_at_once=1,retries=0,
        original_capture_budget_inherited=True,precision_analysis_120_second_budget_not_changed=True,
        actual_external_terminal_return_contract=terminal_contract(sys.executable),
        reconstruction_relative_limit=5e-12,diagnostic_matrix_equation_limit=1e-10,
        original_accuracy_thresholds_changed=False,coefficient_fitting=False,CE_data_used=False,
        capture_only=True,production_solver_promoted=False,AAA_accuracy_qualified=False,ABA_admitted=False)
    write_new(OUT/'declaration.json',d)
    print(json.dumps(dict(declaration=str(OUT/'declaration.json'),declaration_sha256=digest(OUT/'declaration.json')),allow_nan=False),flush=True)


def declaration_admission(expected):
    if not re.fullmatch('[0-9a-f]{64}',expected or ''):raise ValueError('actual frozen declaration SHA256 is mandatory')
    d=read(require(OUT/'declaration.json',expected))
    if (d['schema']!='AXMAT_RANK1_NATIVE_ANGULAR_CAPTURE_DECLARATION_V1' or d['total_wall_seconds']!=TOTAL_WALL
        or d['stage_wall_seconds']!=STAGE_WALL or d['rss_cap_mib']!=RSS or d['retries']!=0 or d['threads']!=1
        or d['numeric_children_at_once']!=1 or d['archive_reserve_bytes']!=d['private_input_copy_bytes']+2*2**30
        or d['complete_archive_scope_roots']!=[str(SOURCE),str(OUT)]
        or d['actual_external_terminal_return_contract']!=terminal_contract(d['python_command'])
        or d['artifact_budget_bytes']!=HISTORY_CAP or d['min_free_bytes']!=FREE_FLOOR
        or d['capture_only'] is not True or any(d[key] is not False for key in (
            'production_solver_promoted','AAA_accuracy_qualified','ABA_admitted','CE_data_used',
            'coefficient_fitting','original_accuracy_thresholds_changed'))
        or d['reconstruction_relative_limit']!=5e-12 or d['diagnostic_matrix_equation_limit']!=1e-10):raise ValueError('fixed diagnostic contract differs')
    environment(d);verify_inventory(SOURCE,d['source_inventory'])
    for path,item in d['input_aliases'].items():
        p=Path(path)
        if not p.is_symlink() or os.readlink(p)!=item['text'] or str(p.resolve(strict=True))!=item['target']:
            raise ValueError('original map012 input alias binding differs')
        require(item['target'],item['sha256'])
    if archive_bytes()>=d['archive_reserve_bytes']:raise ValueError('complete capture archive cap')
    return d


def child_admission(expected):
    d=declaration_admission(expected);claim=read(OUT/'execution_claim.json');stages=read(OUT/'AAA/stages.json')['stages']
    if claim['parent_pid']!=os.getppid() or claim['declaration_sha256']!=expected or not stages or stages[-1]['status']!='RUNNING' or stages[-1]['command']!=[sys.executable,*sys.argv]:raise ValueError('actual bounded parent/child/command differs')
    resource(d['resource_roots']).check()
    return d


def read_stream(path,magic,header_count,arrays):
    import numpy as np
    with require(path).open('rb') as stream:
        if stream.read(8)!=magic:raise ValueError('raw stream schema differs')
        raw=stream.read(4*header_count)
        if len(raw)!=4*header_count:raise ValueError('incomplete raw stream header')
        header=np.frombuffer(raw,'<i4').copy();values=[]
        for count in arrays:
            raw=stream.read(8*count)
            if len(raw)!=8*count:raise ValueError('incomplete actual REAL64 raw stream')
            a=np.frombuffer(raw,'<f8').copy()
            if not np.isfinite(a).all():raise ValueError('nonfinite raw stream words')
            values.append(a)
        if stream.read(1):raise ValueError('raw stream trailing bytes')
    return header,values


def audit_slots(capture):
    import numpy as np
    count=NUN*NG
    h,arrays=read_stream(OUT/'AAA/angular_terminal_slots.bin',b'AXCTS001',4,[count]*4)
    if h.tolist()!=[NUN,NG,3,1]:raise ValueError('actual terminal slot context differs')
    old_outer,slot3,slot7,slot8=[a.reshape((NUN,NG),order='F') for a in arrays]
    previous=None;rows=[]
    for phase in (1,2,3):
        h,a=read_stream(OUT/'AAA'/f'angular_slot7_phase{phase}.bin',b'AXCS7001',7,[count,count])
        if h[:5].tolist()!=[phase,NUN,NG,3,1] or not 1<=h[5]<=NG+1 or h[6]!=0:raise ValueError('last original inner slot context/acceleration differs')
        six,seven=[x.reshape((NUN,NG),order='F') for x in a]
        if seven.tobytes()!=slot7.tobytes() or previous is not None and seven.tobytes()!=previous:raise ValueError('actual slot7 changed across terminal acceleration/promotion observations')
        if phase==3 and (h[5]!=NG+1 or six.tobytes()!=seven.tobytes()):raise ValueError('all actual converged groups must promote terminal slot7')
        previous=seven.tobytes()
        if phase==1:
            defect=abs(six[:1152]-seven[:1152]).reshape((1,NL,NZ,NR,NG),order='F')
            scale=np.maximum(abs(seven[:1152]),abs(six[:1152])).reshape((1,NL,NZ,NR,NG),order='F')
            np.savez(OUT/'audit/actual_inner_all_moment_defect.npz',defect=defect,scale=scale)
        rows.append(dict(phase=phase,context=h.tolist(),actual_slot7_byte_exact=True))
    if slot3.tobytes()!=slot7.tobytes():raise ValueError('terminal raw outer image differs from actual promoted slot7')
    for g,group in enumerate(capture['groups']):
        if (slot7[:,g].tobytes()!=group['returned'].tobytes() or slot3[:,g].tobytes()!=group['before_normal'].tobytes()
            or slot8[:,g].tobytes()!=group['s2'].tobytes()):raise ValueError('last actual F2/S2 does not match original terminal slots')
    np.savez(OUT/'audit/actual_outer_all_moment_defect.npz',defect=abs(old_outer[:1152]-slot3[:1152]),
        scale=np.maximum(abs(old_outer[:1152]),abs(slot3[:1152])))
    return dict(last_inner_context=[3,1],phases=rows,actual_last_F2_equals_terminal_slot7=True,
        actual_slot7_equals_raw_slot3=True,actual_last_post_SIGS_S2_equals_slot8=True,
        all_moment_iteration_defects_are_diagnostic_only=True,original_P0_convergence_gate_unchanged=True)


def audit_cache_events(capture,events):
    import numpy as np
    first=np.zeros((2,NG),dtype='<i4');counts=np.zeros((2,NG),dtype='<i4');latest=np.zeros((2,NG,3),dtype='<i4')
    with (OUT/'AAA/angular_cache_events.bin').open('rb') as stream:
        if stream.read(8)!=b'AXCKE001' or np.frombuffer(stream.read(8),'<i4').tolist()!=[NG,2]:raise ValueError('actual cache events schema differs')
        row_count=0
        while raw:=stream.read(32):
            if len(raw)!=32:raise ValueError('truncated cache validation event')
            seq,outer,inner,g,phase,nkey,hit,identical=map(int,np.frombuffer(raw,'<i4'))
            if not(1<=g<=NG and phase in (1,2) and 1<=seq<=events['dispatches'] and outer>0 and inner>0 and nkey>0 and identical==1):raise ValueError('actual key validation event invalid')
            i,j=phase-1,g-1
            if hit!=int(counts[i,j]>0) or seq<=latest[i,j,0]:raise ValueError('key validation chronological identity differs')
            if not counts[i,j]:first[i,j]=seq
            counts[i,j]+=1;latest[i,j]=[seq,outer,inner];row_count+=1
    per=np.array(events['per_group_calls'])
    if not np.array_equal(counts[0],per) or not np.array_equal(counts[1],per):raise ValueError('both raw and projected key must be validated on every actual angular call')
    for g,group in enumerate(capture['groups']):
        if any(not np.array_equal(latest[p,g],group['context'][1:4]) for p in (0,1)) or first[0,g]!=first[1,g] or first[1,g]!=group['context'][5]:raise ValueError('first miss/last actual field not bound to both cache keys')
    built,reused,hits,live,peak,cap=map(int,capture['cache_stats'])
    if built!=NG*(NZ+1) or hits!=int(sum(per-1)) or reused!=hits*(NZ+1) or not 0<live<=peak<=cap==536870912:raise ValueError('native cache counters do not cover actual all-group key validation calls')
    return dict(actual_key_events=row_count,all_370_first_cache_miss_blocks_bound=True,
        every_actual_raw_and_projected_key_validation_archived=True,builtblocks=built,reusedblocks=reused,
        validated_hits=hits,live_accounted_bytes=live,peak_accounted_bytes=peak,cap_bytes=cap)


def independent_keys(group,a,g):
    """Recreate both bit keys from captured primitive inputs in frozen loop order."""
    import numpy as np
    def f4(x):return struct.unpack('<i',np.asarray(x,dtype='<f4').tobytes())[0]
    def f8(x):return struct.unpack('<q',np.asarray(x,dtype='<f8').tobytes())[0]
    raw=[NR,NZ,1,len(a['total'])-1,3,1,int(a['ischm'][0]),NA,NL,int(a['lfixup'][0]),1,int(a['white_row'][0]),f8(a['white_perimeter'][0]),*map(int,a['ncode']),32,64]
    for z in range(NZ):raw.extend([int(a['mat1d'][z]),f4(a['vol1d'][z])])
    raw.extend(map(int,a['mat'].ravel(order='F')))
    raw.extend(map(f4,a['total']))
    raw.extend(map(f4,a['sgas'].ravel(order='F')))
    raw.extend(map(f4,a['basis'].ravel(order='F')))
    raw.extend(map(f4,a['vol2d']))
    raw.extend(map(f8,a['radial2d'].ravel(order='F')))
    for n in range(NA):
        raw.extend([f4(a['mu'][n]),f4(a['w'][n])]);raw.extend(map(f4,a['pl'][:,n]))
    raw.extend(map(f4,a['zcode']))
    projected=[f8(float(a['zcode'][0])),f8(float(a['zcode'][1]))]
    projected.extend(map(f8,a['weight']));projected.extend(map(f8,a['mass'].ravel(order='F')))
    for z in range(NZ):projected.extend([f8(a['total_projected'][0,0,z]),f8(a['radial_projected'][0,0,z])])
    projected.extend(map(f8,a['scat_projected'].ravel(order='F')))
    for l in range(NL):
        for n in range(NA):projected.extend([f8(a['mn'][n,l]),f8(a['dn'][l,n])])
    projected.extend(map(f8,a['white_angle'].ravel(order='F')));projected.extend(map(f8,a['white_mode'].ravel(order='F')))
    for phase,expected in ((1,raw),(2,projected)):
        path=OUT/'AAA'/f'angular_key_p{phase}_g{g:03d}.bin'
        with path.open('rb') as stream:
            if stream.read(8)!=b'AXCKY001':raise ValueError('actual first native key schema differs')
            h=np.frombuffer(stream.read(24),'<i4').copy();payload=stream.read()
        if h.size!=6 or h[:3].tolist()!=[g,phase,int(group['context'][5])] or h[5]!=len(expected) or len(payload)!=8*len(expected) or payload!=np.asarray(expected,dtype='<i8').tobytes():raise ValueError('independent primitive reconstruction of actual native operator key differs')


def stage_commands(d,expected):
    return [*d['build_commands'],[str(OUT/'runtime/Dragon')],
        [d['python_command'],str(Path(__file__).resolve()),'audit','--sha256',expected]]


def stage_labels():
    return [*[f'build/build_{i:02d}' for i in range(4)],'AAA/capture_replay','audit/audit']


def check_watch(stage):
    w=read((OUT/(stage['label']+'.log')).with_suffix('.watchdog.json'))
    actual_wall=w['wall_cap_seconds'];stage_wall=stage['wall_cap_seconds']
    if (w['returncode']!=0 or w['limit_failure'] is not None or not 0<=w['sampled_peak_rss_mib']<RSS
        or w['command']!=stage['command'] or w['rss_cap_mib']!=RSS or not 0<actual_wall<=stage_wall<=STAGE_WALL
        or not 0<=w['elapsed_seconds']<actual_wall or w['own_child_only'] is not True
        or w['liveness_group_cleanup'] is not True or digest(OUT/(stage['label']+'.log'))!=stage['log_sha256']):raise ValueError('actual own-child watchdog/stage/log evidence differs')
    return w


def run(expected):
    started=time.monotonic();d=declaration_admission(expected)
    full,production,_,_=modules();guard_admission(full)
    resources=resource(d['resource_roots']);resources.check()
    write_new(OUT/'execution_claim.json',dict(parent_pid=os.getpid(),declaration_sha256=expected,
        started_unix=time.time(),started_monotonic=started,retries=0))
    remaining=TOTAL_WALL-(time.monotonic()-started)
    if remaining<=0:raise ValueError('original whole capture budget exhausted')
    runner=full.OwnRSSSerialExecutor(OUT,remaining,'AAA',resources)
    result=dict(classification='FAILED_RANK1_NATIVE_ANGULAR_CAPTURE_NO_RETRY',error=None,
        capture_only=True,production_solver_promoted=False,AAA_accuracy_qualified=False,ABA_admitted=False)
    try:
        for i,command in enumerate(d['build_commands']):
            environment(d);runner.execute(OUT/'build',f'build_{i:02d}',command,STAGE_WALL)
        write_new(OUT/'runtime/build_identity.json',dict(files={str(p.relative_to(OUT)):digest(p) for p in
            [OUT/'runtime/Dragon',*sorted((OUT/'build').glob('*.o')),*sorted((OUT/'build').glob('*.mod'))]},
            sole_private_overrides=['SPOT1P64.o','FLU2DR64.o'],all_other_original_link_inputs_unchanged=True,
            source_proofs=d['source_inventory']))
        try:
            environment(d);runner.execute(OUT/'AAA','capture_replay',[str(OUT/'runtime/Dragon')],STAGE_WALL,
                'AXMAT-PICARD-AXIAL-COMPLETE',deck='picard_axial.x2m')
        finally:
            captured=sorted((OUT/'AAA').glob('angular*.bin'))
            write_new(OUT/'raw_capture_receipt.json',dict(files={str(p.relative_to(OUT)):digest(p) for p in captured},
                original_output_files={name:digest(OUT/'AAA'/name) for name in ('candidate_axial.xsm','candidate_snapshots.xsm') if (OUT/'AAA'/name).is_file()},
                raw_capture_count=len(captured),before_numeric_gates=True,selection='Every group chronological last actual call; first miss blocks and every operator key validation'))
        if len(captured)!=6*NG+8:raise ValueError('complete raw angular/source/key/slot/block archive count differs')
        runner.execute(OUT/'audit','audit',stage_commands(d,expected)[-1],STAGE_WALL,'AXMAT-RANK1-NATIVE-ANGULAR-CAPTURE-AUDITED')
        stages=read(OUT/'AAA/stages.json')['stages']
        if len(stages)!=6 or [s['label'] for s in stages]!=stage_labels() or [s['command'] for s in stages]!=stage_commands(d,expected) or any(s['status']!='PASS' for s in stages):raise ValueError('exact six original capture stages must pass once')
        audit_result=read(OUT/'audit/result.json')
        if audit_result['classification']!='COMPLETE_RANK1_NATIVE_ANGULAR_CAPTURE_ONLY' or any(not row['original_1e10_diagnostic_gate_passed'] for row in audit_result['groups']):raise ValueError('original capture diagnostic equation gate failed')
        result.update(classification='COMPLETE_BOUNDED_RANK1_NATIVE_ANGULAR_CAPTURE_ONLY',watchdogs=[check_watch(s) for s in stages],
            original_map012_scientific_records_word_exact=True,complete_all_370_actual_terminal_fields=True)
    except BaseException as error:
        result['error']=repr(error);raise
    finally:
        try:
            environment(d);verify_inventory(SOURCE,d['source_inventory']);snapshot=resources.check()
            retained=archive_bytes();elapsed=time.monotonic()-started
            if retained>=d['archive_reserve_bytes'] or elapsed>=TOTAL_WALL:raise ValueError('original whole capture/archive budget exceeded')
            result.update(elapsed_seconds=elapsed,archive_bytes_before_closeout=retained,resources=snapshot,
                complete_archive_scope_roots=[str(SOURCE),str(OUT)])
        except BaseException as error:
            result.update(classification='FAILED_RANK1_NATIVE_ANGULAR_CAPTURE_NO_RETRY',error=repr(error),elapsed_seconds=time.monotonic()-started)
            write_new(OUT/'driver_result.json',result);raise
        write_new(OUT/'driver_result.json',result)
    complete_inventory=inventory(OUT)
    write_new(OUT/'seal.json',dict(schema='AXMAT_RANK1_NATIVE_ANGULAR_CAPTURE_SEAL_V1',**complete_inventory))
    try:
        snapshot=resources.check();retained=archive_bytes();elapsed=time.monotonic()-started
        if elapsed>=TOTAL_WALL or retained>=d['archive_reserve_bytes']:raise ValueError('mandatory complete post-seal tail failed')
    except BaseException as error:
        write_new(OUT/'closeout_failure.json',dict(error=repr(error),complete=False,AAA_accuracy_qualified=False,ABA_admitted=False));raise
    print(json.dumps(dict(result=result,actual_tail_check='PASS',actual_elapsed_seconds=elapsed,
        actual_archive_bytes=retained,actual_resources=snapshot),allow_nan=False),flush=True)


def strict_terminal_json(path):
    def pairs(items):
        result={}
        for key,value in items:
            if key in result:raise ValueError('duplicate terminal JSON key')
            result[key]=value
        return result
    return json.loads(require(path).read_text(),object_pairs_hook=pairs,
        parse_constant=lambda value:(_ for _ in ()).throw(ValueError('nonfinite terminal JSON')))


def terminal_file(path,sha):
    path=Path(path)
    normal_path(path)
    if path.parent!=TERMINAL or path.is_symlink() or path.resolve(strict=True)!=path or not stat.S_ISREG(path.stat().st_mode):raise ValueError('real independent terminal regular file required')
    require(path,sha);return path


def external_terminal(d,seal_sha,result,path,sha):
    receipt=terminal_file(path,sha)
    if receipt!=TERMINAL/'terminal_return.json':raise ValueError('fixed Root terminal receipt required')
    e=strict_terminal_json(receipt);decl_sha=digest(OUT/'declaration.json')
    command=[d['python_command'],str(Path(__file__).resolve()),'run','--sha256',decl_sha]
    if (e['schema']!=TERMINAL_SCHEMA or e['record_producer']!='root' or e['actual_tool_terminal_return_observed'] is not True
        or e['record_written_after_actual_terminal_return'] is not True or type(e['returncode']) is not int or e['returncode']!=0
        or e['command']!=command or e['source']!=pin(Path(__file__).resolve())
        or d['files'][str(Path(__file__).resolve())]!=e['source']['sha256']
        or e['declaration']!=dict(path=str(OUT/'declaration.json'),sha256=decl_sha)
        or e['capture_seal']!=dict(path=str(OUT/'seal.json'),sha256=seal_sha)):raise ValueError('actual Root exit-zero/source/declaration/seal chain differs')
    stdout=terminal_file(e['full_stdout']['path'],e['full_stdout']['sha256'])
    if stdout==receipt or e['full_stdout']!=pin(stdout):raise ValueError('complete separately retained stdout required')
    stderr=terminal_file(e['full_stderr']['path'],e['full_stderr']['sha256'])
    if stderr in (receipt,stdout) or e['full_stderr']!=pin(stderr):raise ValueError('complete separately retained stderr required')
    returned=strict_terminal_json(stdout);tail={key:returned[key] for key in TAIL_FIELDS}
    if returned!=dict(result=result,**tail) or any(e[key]!=tail[key] for key in TAIL_FIELDS):raise ValueError('actual full stdout and sealed result/four tails differ')
    elapsed,size,s=tail['actual_elapsed_seconds'],tail['actual_archive_bytes'],tail['actual_resources']
    if (tail['actual_tail_check']!='PASS' or type(elapsed) not in (int,float) or not math.isfinite(elapsed)
        or not result['elapsed_seconds']<=elapsed<TOTAL_WALL or type(size) is not int or size!=archive_bytes()
        or not 0<size<d['archive_reserve_bytes'] or s['artifact_budget_bytes']!=HISTORY_CAP or s['min_free_bytes']!=FREE_FLOOR
        or s['resource_scope_contract']!=d['resource_scope_contract'] or s['resource_scope_policy']!=d['resource_scope_policy']
        or s['declared_resource_roots']!=d['resource_roots'] or not set(d['resource_roots']).issubset(s['resource_roots'])
        or not size<=s['artifact_bytes']<=HISTORY_CAP or s['disk_free_bytes']<FREE_FLOOR):raise ValueError('actual complete terminal resource/wall/archive gates failed')
    builder().validate_history_roots(s['resource_roots'],ART)
    return dict(receipt=pin(receipt),full_stdout=pin(stdout),full_stderr=pin(stderr),command=command,schema=TERMINAL_SCHEMA,**tail)


def diagnostic_admission(seal_sha,terminal_evidence,terminal_evidence_sha256):
    if not re.fullmatch('[0-9a-f]{64}',seal_sha or '') or not re.fullmatch('[0-9a-f]{64}',terminal_evidence_sha256 or ''):
        raise ValueError('actual capture seal and independent Root receipt hashes are mandatory')
    seal=read(require(OUT/'seal.json',seal_sha))
    if seal['schema']!='AXMAT_RANK1_NATIVE_ANGULAR_CAPTURE_SEAL_V1':raise ValueError('new capture seal required')
    actual_inventory=inventory(OUT);actual=actual_inventory['files']
    if actual_inventory['directories']!=seal['directories'] or actual_inventory['symlinks']!=seal['symlinks']:
        raise ValueError('complete sealed directory/alias namespace differs')
    if set(actual)!=set(seal['files'])|{'seal.json'} or any(actual[name]!=sha for name,sha in seal['files'].items()):raise ValueError('complete raw capture/ledger/watch/output namespace differs')
    d=declaration_admission(digest(OUT/'declaration.json'));resource(d['resource_roots']).check()
    result=read(OUT/'driver_result.json');audit_result=read(OUT/'audit/result.json');stages=read(OUT/'AAA/stages.json')['stages']
    if (result['classification']!='COMPLETE_BOUNDED_RANK1_NATIVE_ANGULAR_CAPTURE_ONLY' or result['error'] is not None
        or len(stages)!=6 or [s['label'] for s in stages]!=stage_labels() or any(s['status']!='PASS' for s in stages)
        or [s['command'] for s in stages]!=stage_commands(d,digest(OUT/'declaration.json'))
        or audit_result['classification']!='COMPLETE_RANK1_NATIVE_ANGULAR_CAPTURE_ONLY'
        or len(audit_result['groups'])!=NG or any(not row['original_1e10_diagnostic_gate_passed'] for row in audit_result['groups'])
        or any(result[key] is not False or audit_result[key] is not False for key in ('AAA_accuracy_qualified','ABA_admitted','production_solver_promoted'))):raise ValueError('only actual complete diagnostic result may be admitted')
    for s in stages:check_watch(s)
    raw=read(OUT/'raw_capture_receipt.json')
    if raw['raw_capture_count']!=6*NG+8 or raw['before_numeric_gates'] is not True:raise ValueError('all raw operands retained before gates required')
    verify({str(OUT/name):sha for name,sha in raw['files'].items()})
    proof=external_terminal(d,seal_sha,result,terminal_evidence,terminal_evidence_sha256)
    return dict(schema='AXMAT_RANK1_NATIVE_ANGULAR_CAPTURE_INPUT_ADMISSION_V1',admission='CURRENT_MAP012_NATIVE_ANGULAR_DIAGNOSTIC_ONLY',
        capture_seal=pin(OUT/'seal.json'),declaration=pin(OUT/'declaration.json'),source=pin(Path(__file__).resolve()),
        actual_external_terminal_evidence=dict(path=str(terminal_evidence),sha256=terminal_evidence_sha256),
        actual_external_terminal_validation=proof,inherited_current_build_admission=d['inherited_current_build_admission'],
        capture_only=True,AAA_accuracy_qualified=False,ABA_admitted=False,production_solver_promoted=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('prepare','run','audit','admit-diagnostic'))
    parser.add_argument('--sha256');parser.add_argument('--build-seal-sha256')
    parser.add_argument('--build-terminal-evidence');parser.add_argument('--build-terminal-evidence-sha256')
    parser.add_argument('--capture-seal-sha256');parser.add_argument('--terminal-evidence');parser.add_argument('--terminal-evidence-sha256')
    a=parser.parse_args()
    if a.action=='prepare':prepare(a.build_seal_sha256,a.build_terminal_evidence,a.build_terminal_evidence_sha256)
    elif a.action=='run':run(a.sha256)
    elif a.action=='audit':audit(a.sha256)
    else:print(json.dumps(diagnostic_admission(a.capture_seal_sha256,a.terminal_evidence,a.terminal_evidence_sha256),allow_nan=False),flush=True)
