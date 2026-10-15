"""Read-only same-byte lookup for retained ROOT64 historical input pins.

This recovers byte provenance only. It does not qualify an old identity, run
Native, compile, execute controls, train, or alter original project inputs.
"""
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import sys
import time

ROOT = Path('/Users/wen/spot')
OUT = ROOT / 'validation/axial_material/root64_epoch_recovery_20261011'
BINDINGS = [
    ROOT / 'validation/artifacts/axial-material-ROOT64-connected-typed-fixture-original-guard-20261011/Root_fixed_source_and_exact_command_binding.json',
    ROOT / 'validation/artifacts/axial-material-ROOT64-real-entry-compile-only-original-guard-20261011-v2/Root_fixed_source_and_exact_command_binding.json',
]
START = time.monotonic()
WALL_CAP = 600
RSS_CAP = 512 * 1024 * 1024


def budget():
    if time.monotonic() - START >= WALL_CAP:
        raise RuntimeError('metadata audit exceeded 600 seconds')
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform != 'darwin':
        peak *= 1024
    if peak > RSS_CAP:
        raise RuntimeError('metadata audit exceeded sampled own 512 MiB')


def identity(st):
    return [st.st_dev, st.st_ino, st.st_mode, st.st_nlink,
            st.st_size, st.st_mtime_ns, st.st_ctime_ns]


def pin(path):
    path = Path(path)
    before = identity(path.stat())
    digest = hashlib.sha256()
    read_bytes = 0
    with path.open('rb') as stream:
        opened = identity(os.fstat(stream.fileno()))
        while True:
            budget()
            block = stream.read(1024 * 1024)
            if not block:
                break
            digest.update(block)
            read_bytes += len(block)
        eof = identity(os.fstat(stream.fileno()))
    after = identity(path.stat())
    if not before == opened == eof == after or read_bytes != before[4]:
        raise RuntimeError('file identity changed during full EOF: ' + str(path))
    return {'path': str(path), 'size_bytes': read_bytes,
            'sha256': digest.hexdigest(), 'identity': after,
            'before_open_EOF_after_identity_equal': True}


def save(path, obj):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(obj, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())


def main():
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(
        RuntimeError('metadata audit alarm exceeded 600 seconds')))
    signal.alarm(WALL_CAP)
    rows = {}
    binding_pins = []
    for binding in BINDINGS:
        binding_pins.append(pin(binding))
        data = json.loads(binding.read_text())
        for old in data['fixed']:
            if (old['path'].startswith('/private/tmp/')
                    or Path(old['path']).suffix.lower() in {'.f', '.f90', '.py', '.c2m'}):
                key = (old['path'], old['sha256'])
                if key not in rows:
                    rows[key] = {'historical_pin': old, 'binding_records': []}
                rows[key]['binding_records'].append(str(binding))
    # The actual five compile / seventeen control host Source is pinned by the
    # real-entry binding's before list, rather than its fixed list.
    def collect(value):
        if isinstance(value, dict):
            path = value.get('path', '')
            if (path == '/private/tmp/Root_run_ROOT64_connected_typed_fixture_original_guards_20261011.py'
                    and 'sha256' in value):
                rows.setdefault((path, value['sha256']),
                    {'historical_pin': value, 'binding_records': [str(BINDINGS[1])]})
            for child in value.values():
                collect(child)
        elif isinstance(value, list):
            for child in value:
                collect(child)
    collect(json.loads(BINDINGS[1].read_text()))
    expected_sizes = {r['historical_pin']['size_bytes'] for r in rows.values()}
    by_sha_size = {}
    scanned = 0
    candidates = 0
    hashed_bytes = 0
    skipped = []
    for directory, subdirs, names in os.walk(ROOT, followlinks=False):
        budget()
        subdirs[:] = [x for x in subdirs if x not in {'.git', '.aws', '.codex', '.agents'}]
        if Path(directory) == OUT:
            subdirs[:] = []
            continue
        for name in names:
            path = Path(directory) / name
            scanned += 1
            try:
                st = path.stat()
                if not path.is_file() or st.st_size not in expected_sizes:
                    continue
                current = pin(path)
                candidates += 1
                hashed_bytes += current['size_bytes']
                by_sha_size.setdefault((current['sha256'], current['size_bytes']), []).append(current)
            except (FileNotFoundError, PermissionError) as exc:
                skipped.append({'path': str(path), 'error': type(exc).__name__})
    result_rows = []
    counts = {}
    for row in rows.values():
        old = row['historical_pin']
        current = None
        if Path(old['path']).is_file():
            current = pin(old['path'])
        copies = by_sha_size.get((old['sha256'], old['size_bytes']), [])
        if current is not None:
            state = 'CURRENT_BYTES_MATCH' if current['sha256'] == old['sha256'] else 'CURRENT_BYTES_DIFFER'
        else:
            state = 'EXACT_SAME_BYTE_COPY_FOUND' if copies else 'MISSING_NO_EXACT_COPY_FOUND'
        row.update(status=state, current_original_path_pin=current,
                   same_byte_project_copies=copies,
                   historical_identity_is_current_qualification=False)
        counts[state] = counts.get(state, 0) + 1
        result_rows.append(row)
    mapping = {
        'schema': 'ROOT64_CURRENT_EPOCH_SAME_BYTE_SOURCE_LOOKUP_V1',
        'scope': 'Full project regular-file size lookup including ignored ART; exact SHA only for candidate sizes',
        'excluded_directories': ['.git', '.aws', '.codex', '.agents', str(OUT)],
        'current_audit_source': pin(__file__),
        'historical_bindings_current_pins': binding_pins,
        'counts': counts, 'rows': result_rows,
        'scan': {'files_seen': scanned, 'size_candidates_full_EOF_hashed': candidates,
                 'candidate_bytes_full_EOF_hashed': hashed_bytes, 'skipped': skipped},
        'whole_native_compile_control_online_or_science_qualification': False,
        'old_identities_restored_or_device_normalized': False,
        'source_or_project_inputs_changed': False,
    }
    save(OUT / 'ROOT64_CURRENT_SOURCE_MAPPING.json', mapping)
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform != 'darwin':
        peak *= 1024
    summary = {'status': 'READ_ONLY_SOURCE_BYTE_LOOKUP_COMPLETED',
               'counts': counts, 'wall_seconds': time.monotonic() - START,
               'sampled_own_peak_bytes': peak,
               'wall_cap_seconds': WALL_CAP, 'sampled_own_rss_cap_bytes': RSS_CAP,
               'OS_RSS_hard_limit_claimed': False,
               'scan': mapping['scan'],
               'mapping': pin(OUT / 'ROOT64_CURRENT_SOURCE_MAPPING.json'),
               'science_or_current_identity_qualification': False}
    save(OUT / 'ROOT64_SOURCE_LOOKUP_SUMMARY.json', summary)
    print(json.dumps(summary, ensure_ascii=False, allow_nan=False))


if __name__ == '__main__':
    main()
