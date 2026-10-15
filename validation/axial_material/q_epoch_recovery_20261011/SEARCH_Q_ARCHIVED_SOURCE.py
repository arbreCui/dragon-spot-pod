"""Read-only project archive Source search; does not import archived Sources."""
import ast
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import stat
import sys
import tarfile
import threading
import time
import zipfile

ROOT = Path('/Users/wen/spot')
OUT = Path(__file__).resolve().parent
START = time.monotonic()
TARGET = {
    72784: ('pure_helper_controls.py', '7ae39903114ec50ab77b203edd7cf88f16690c0519af3e2e8877dbe28d8700a8'),
    14682: ('read_open_short_index_state_controls.py', 'c3a81b4cfd93f40e458e999305e6917227ad3fbb08d4b6116ed6cddf281d6f95'),
    43643: ('wire67_saved_evidence_review.py', 'f133f92b39c5376dd719eb3942ac7049c34a850c500afd79028b63f12b9a207c'),
}
ATTEMPTS = []


def forbid(event, args):
    if event in ('subprocess.Popen', 'os.system', 'os.fork', 'os.forkpty', 'os.exec',
                 'os.posix_spawn', 'os.spawn', 'os.startfile', 'os.startfile/2'):
        ATTEMPTS.append(event)
        raise RuntimeError('archive Source search forbids process creation')


sys.addaudithook(forbid)


def deadline(signum, frame):
    raise TimeoutError('600s archive Source search cap')


signal.signal(signal.SIGALRM, deadline)
signal.setitimer(signal.ITIMER_REAL, 600)


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns]


def pin(path):
    path = Path(path)
    before = path.lstat()
    assert stat.S_ISREG(before.st_mode) and before.st_nlink == 1
    for p in (path, *path.parents):
        assert not p.is_symlink()
    h = hashlib.sha256()
    count = 0
    with path.open('rb') as f:
        assert identity(os.fstat(f.fileno())) == identity(before)
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
            count += len(block)
        assert identity(os.fstat(f.fileno())) == identity(before)
    assert identity(path.lstat()) == identity(before) and count == before.st_size
    return dict(path=str(path), size_bytes=count, sha256=h.hexdigest(), identity=identity(before))


def checkpoint():
    elapsed = time.monotonic() - START
    rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if sys.platform != 'darwin':
        rss *= 1024
    assert elapsed < 600 and rss < 512 * 2**20
    assert threading.active_count() == 1 and not ATTEMPTS
    return dict(elapsed_seconds=elapsed, own_peak_rss_bytes=rss,
                process_creation_attempts=list(ATTEMPTS))


def put_json(path, doc):
    data = (json.dumps(doc, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode()
    with Path(path).open('xb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())


assert sys.flags.optimize == 0 and sys.dont_write_bytecode
for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
             'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    assert os.environ.get(name) == '1'
report_path = OUT/'ARCHIVED_SOURCE_SEARCH.json'
assert not report_path.exists()
archives = []
for scope in (ROOT/'validation/axial_material', ROOT/'validation/artifacts'):
    for directory, dirs, files in os.walk(scope, followlinks=False):
        dirs[:] = [name for name in dirs if not (Path(directory)/name).is_symlink()]
        for name in files:
            if name.endswith(('.tar.gz', '.tgz', '.zip')):
                archives.append(Path(directory)/name)
records = []
candidates = []
embedded_matches = []
patch_references = []
matches = []
skipped_large_JSON_members = []


def inspect(name, size, reader, archive_pin):
    if size in TARGET:
        data = reader.read()
        assert len(data) == size
        sought, digest = TARGET[size]
        sha = hashlib.sha256(data).hexdigest()
        candidates.append(dict(archive=archive_pin, member=name,
                               size_bytes=size, sha256=sha, sought_name=sought,
                               exact_match=sha == digest))
        if sha == digest:
            ast.parse(data)
            destination = OUT/'recovered_exact_source'/sought
            assert not destination.exists()
            with destination.open('xb') as f:
                f.write(data)
            assert destination.read_bytes() == data
            matches.append(dict(archive=archive_pin, member=name, new_Source=pin(destination)))
    elif name.endswith('.json') and size <= 2 * 2**20:
        data = reader.read()
        assert len(data) == size
        if not any(wanted.encode() in data for wanted, digest in TARGET.values()):
            return
        value = json.loads(data)

        def walk(v, pointer):
            if type(v) is str:
                d = v.encode()
                if len(d) in TARGET and hashlib.sha256(d).hexdigest() == TARGET[len(d)][1]:
                    embedded_matches.append(dict(archive=archive_pin, member=name,
                                                 JSON_pointer=pointer, sought_name=TARGET[len(d)][0]))
            elif type(v) is dict:
                if 'exact_before' in v or 'exact_after' in v:
                    patch_references.append(dict(archive=archive_pin, member=name, JSON_pointer=pointer,
                                                 keys=list(v), complete_patch_retained_in_archive=True))
                for k, x in v.items():
                    walk(x, pointer + '/' + k)
            elif type(v) is list:
                for i, x in enumerate(v):
                    walk(x, pointer + '/' + str(i))
        walk(value, '')
    elif name.endswith('.json'):
        skipped_large_JSON_members.append(dict(archive=archive_pin, member=name, size_bytes=size))


for path in sorted(archives):
    before = pin(path)
    assert before['size_bytes'] < 64 * 2**20, 'archive larger than bounded Source read'
    count = 0
    regular = 0
    if path.name.endswith('.zip'):
        with zipfile.ZipFile(path) as archive:
            for item in archive.infolist():
                count += 1
                if item.is_dir():
                    continue
                regular += 1
                if item.file_size in TARGET or item.filename.endswith('.json'):
                    with archive.open(item) as reader:
                        inspect(item.filename, item.file_size, reader, before)
    else:
        with tarfile.open(path, 'r:gz') as archive:
            for item in archive:
                count += 1
                if not item.isfile():
                    continue
                regular += 1
                if item.size in TARGET or item.name.endswith('.json'):
                    reader = archive.extractfile(item)
                    assert reader is not None
                    with reader:
                        inspect(item.name, item.size, reader, before)
    assert pin(path) == before
    records.append(dict(archive_pin=before, member_count=count, regular_members=regular))
    checkpoint()
for row in records:
    assert pin(row['archive_pin']['path']) == row['archive_pin']
doc = dict(schema='SPOT_Q_ARCHIVED_SOURCE_RECOVERY_SEARCH_ONLY_V1',
           status='COMPLETE_BOUNDED_PROJECT_ARCHIVE_MEMBER_AND_SMALL_JSON_SOURCE_SEARCH',
           archives=records, exact_size_candidates=candidates,
           exact_member_matches_recovered=matches,
           embedded_exact_Source_matches=embedded_matches,
           complete_patch_references=patch_references,
           large_JSON_members_not_decoded=skipped_large_JSON_members,
           source_recovery_is_not_protocol_or_Q_qualification=True,
           Source=pin(__file__), checkpoint=checkpoint(),
           helper_or_protocol_imported=False, PS_or_native_or_numeric_process_started=False,
           new_Q_created=False, science_or_BOOT_admitted=False)
put_json(report_path, doc)
signal.setitimer(signal.ITIMER_REAL, 0)
print(json.dumps(dict(status=doc['status'], archives=len(records),
                      members=sum(x['member_count'] for x in records),
                      exact_members=len(matches), embedded_Source_matches=len(embedded_matches),
                      full_patch_references=len(patch_references),
                      large_JSON_members_not_decoded=len(skipped_large_JSON_members),
                      report=pin(report_path), helper_or_protocol_imported=False, new_Q_created=False)), flush=True)
