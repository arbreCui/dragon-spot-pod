"""Exact-list storage audit. No import-time reads, writes, or deletion."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import stat
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
REC = ROOT / 'validation/axial_material/root64_epoch_recovery_20261011'
PACKAGE = REC / 'storage_release_20261012'
BIND = REC / 'native_warm_B_bounded_host_source_v1/CURRENT_WARM_B_COMPLETE_HOST_SOURCE_BINDING.json'
B_FREEZE = REC / 'native_warm_B_initial_storage_reserve_source_v2/COMPLETE_WARM_B_INITIAL_STORAGE_SOURCE_FREEZE.json'
OLD_B_FREEZE = REC / 'native_warm_B_bounded_host_source_v1/COMPLETE_WARM_B_CANDIDATE_SOURCE_FREEZE.json'
FACTORY = ROOT / 'validation/axial_material/moment_order_complete_history_resource_trie_20261010.py'
CAPTURE_NAMES = [
    'axial-material-rank1-cache-native-angular-capture-20261007',
    'axial-material-rank1-cache-memory-native-angular-capture-20261007',
    'axial-material-rank1-cache-memory-dedup-native-angular-capture-20261007',
    'axial-material-rank1-cache-memory-dedup-deferred-snapshot-native-angular-capture-20261007',
]
V3 = 'axial-material-production-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-file-snapshot-scipy-env-physical-basis-own-pid-peak-v3-20261008'
V9 = 'axial-material-production-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-scipy-env-physical-basis-own-pid-peak-v9-20261009'
GROUP_ROOTS = [ART / n for n in CAPTURE_NAMES + [V3, V9]]
EXPECTED_BYTES = 3566694788
RSS_CAP = 512 * 2**20
START = time.monotonic()

def guard():
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss >= RSS_CAP:
        raise RuntimeError('SELF reached 512 MiB')
    if time.monotonic() - START >= 1800:
        raise RuntimeError('storage audit reached whole 1800 second cap')

def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def ancestors(path):
    path = Path(path)
    if not path.is_absolute() or '..' in path.parts or not path.is_relative_to(ROOT):
        # The compiler and system dependency pins are read-only external inputs.
        if not path.is_absolute() or '..' in path.parts:
            raise RuntimeError('absolute canonical path required')
    for p in reversed(path.parents):
        s = p.lstat()
        if not stat.S_ISDIR(s.st_mode):
            raise RuntimeError('symlink or non-directory ancestor: ' + str(p))

def pin(path):
    path = Path(path)
    ancestors(path)
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode):
        raise RuntimeError('ordinary non-symlink file required: ' + str(path))
    h = hashlib.sha256()
    count = 0
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        if identity(os.fstat(fd)) != identity(before):
            raise RuntimeError('identity changed before open')
        while True:
            block = os.read(fd, 1024 * 1024)
            if not block:
                break
            h.update(block)
            count += len(block)
            guard()
        at_eof = identity(os.fstat(fd))
    finally:
        os.close(fd)
    after = identity(path.lstat())
    if identity(before) != at_eof or at_eof != after or count != before.st_size:
        raise RuntimeError('full EOF file identity changed: ' + str(path))
    return dict(path=str(path), sha256=h.hexdigest(), size_bytes=count, identity=after)

def normalize(row):
    return dict(path=row['path'], sha256=row['sha256'],
                size_bytes=row.get('size_bytes', row.get('bytes')),
                identity=row.get('identity', row.get('seven_id')))

def same(row):
    expected = normalize(row)
    if pin(expected['path']) != expected:
        raise RuntimeError('full SHA/7ID mismatch: ' + expected['path'])
    return expected

def read_pinned_json(row):
    row = same(row)
    with open(row['path'], encoding='utf-8') as stream:
        data = json.load(stream)
    if identity(Path(row['path']).lstat()) != row['identity']:
        raise RuntimeError('JSON identity changed during read')
    return data

def add_nested_pins(data, table):
    if isinstance(data, dict):
        if 'path' in data and 'sha256' in data and ('identity' in data or 'seven_id' in data):
            row = normalize(data)
            old = table.get(row['path'])
            if old is not None and old != row:
                raise RuntimeError('conflicting full pins: ' + row['path'])
            table[row['path']] = row
        for value in data.values():
            add_nested_pins(value, table)
    elif isinstance(data, list):
        for value in data:
            add_nested_pins(value, table)

def candidates():
    paths = []
    common = ['parent_snapshots_closed.xsm', 'candidate_radial.xsm',
              'parent_axial_closed.xsm', 'initial_axial_macrolib.xsm']
    for name in CAPTURE_NAMES:
        paths += [ART / name / 'AAA' / f for f in common]
    paths += [ART / CAPTURE_NAMES[-1] / 'AAA' / f
              for f in ['candidate_snapshots.xsm', 'candidate_axial.xsm']]
    for name in [V3, V9]:
        paths += [ART / name / 'archives' / f
                  for f in ['training_snapshots.xsm', 'aaa_snapshots.xsm', 'aba_snapshots.xsm']]
    if len(paths) != 24 or len(set(paths)) != 24:
        raise RuntimeError('exact 24 target paths required')
    return sorted(paths)

def failure_documents():
    out = []
    for name in CAPTURE_NAMES + [V3, V9]:
        path = ART / name / ('driver_result.json' if name in CAPTURE_NAMES else 'cold_source_failure.json')
        row = pin(path)
        d = read_pinned_json(row)
        if (not d.get('classification', '').startswith('FAILED_')
                or 'NO_RETRY' not in d['classification']
                or d.get('error') != "RuntimeError('own-child 512 MiB RSS cap reached')"
                or d.get('AAA_accuracy_qualified') is not False or d.get('ABA_admitted') is not False):
            raise RuntimeError('exact closed failed attempt proof required')
        out.append(dict(pin=row, classification=d['classification'], error=d['error']))
    return out

def current_protection():
    table = {}
    frow = pin(B_FREEZE)
    freeze = read_pinned_json(frow)
    brow = freeze['unchanged_complete_runtime_and_physical_binding_pin']
    if brow['path'] != str(BIND):
        raise RuntimeError('unchanged current B binding path')
    b = read_pinned_json(brow)
    add_nested_pins(b, table)
    immediate = [b[k] for k in ['actual_core83_report', 'actual_AB_ingress_report', 'selected_actual_current17_report']]
    immediate += [x['actual_compile_origin_report'] for x in b['actual_covered_Source_object_compile_origins']]
    immediate += [pin(ART / 'axial-material-new-REAL64-native-warm-A-20261012-v3/Root_actual_single_plane_warm_A_summary.json'),
                  pin(ART / 'axial-material-current-warm-B-CLE-entry-controls-20261012-v1/Root_actual_entry_controls_summary.json')]
    seen = set()
    for row in immediate:
        if row['path'] in seen:
            continue
        seen.add(row['path'])
        report = read_pinned_json(row)
        # These are the actual current rows verified by the production hosts.
        # Historical coherent-tamper before/after events are observations, not
        # simultaneously applicable full pins of the now-mutated fixture.
        for key in ['fixed_current_pins', 'output_pins', 'owned_runtime_pins']:
            add_nested_pins(report.get(key, []), table)
        if row['path'] == b['selected_actual_current17_report']['path']:
            add_nested_pins(report['independent_coherent_baseline_manifest_pin'], table)
    # Two resource-contract references in the prior 2201-path audit carried
    # SHA only. Upgrade them to current full SHA/7ID pins here.
    for p in [ART / 'axial-material-qualified-AB-white-trace-refined-envpin-admission-20261005/case_spec.json',
              ART / 'axial-material-qualified-AB-white-trace-refined-envpin-admission-20261005/resource_addendum.json']:
        table[str(p)] = pin(p)
    original_union_count = len(table)
    if len(b['fixed_current_pins']) != 2032 or original_union_count != 2201:
        raise RuntimeError('previously reviewed 2032/2201 current scope changed')
    # Extend protection to the current frozen host packages and owning reports themselves.
    for row in immediate + [frow, brow, pin(OLD_B_FREEZE)]:
        table[row['path']] = normalize(row)
    add_nested_pins(freeze, table)
    add_nested_pins(read_pinned_json(pin(OLD_B_FREEZE)), table)
    table[str(FACTORY)] = pin(FACTORY)
    for p in [ART / 'axial-material-qualified-AB-white-trace-refined-envpin-admission-20261005/case_spec.json',
              ART / 'axial-material-qualified-AB-white-trace-refined-envpin-admission-20261005/resource_addendum.json']:
        table[str(p)] = pin(p)
    rows = sorted(table.values(), key=lambda x: x['path'])
    for row in rows:
        same(row)
    return rows, dict(B_direct_fixed_pins=2032, immediate_report_union_pins=original_union_count,
                      extended_current_frozen_host_and_owning_report_pins=len(rows), immediate_report_paths=sorted(seen),
                      immediate_report_pin_fields=['fixed_current_pins', 'output_pins', 'owned_runtime_pins'],
                      actual17_extra_required_field='independent_coherent_baseline_manifest_pin',
                      historical_coherent_before_after_observations_are_not_current_dependency_pins=True,
                      actual_current_coherent_fixture_output_pin_protected=True)

def inventory():
    files, links, directories = {}, {}, []
    stack = list(GROUP_ROOTS)
    while stack:
        p = stack.pop()
        ancestors(p)
        ds = p.lstat()
        if not stat.S_ISDIR(ds.st_mode):
            raise RuntimeError('ordinary target group directory required')
        directories.append(str(p))
        fd = os.open(p, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            with os.scandir(fd) as entries:
                for entry in entries:
                    q = p / entry.name
                    s = entry.stat(follow_symlinks=False)
                    if stat.S_ISDIR(s.st_mode):
                        stack.append(q)
                    elif stat.S_ISREG(s.st_mode):
                        files[str(q)] = identity(s)
                    elif stat.S_ISLNK(s.st_mode):
                        links[str(q)] = dict(identity=identity(s), target=os.readlink(q))
                    else:
                        raise RuntimeError('unexpected special file: ' + str(q))
        finally:
            os.close(fd)
        guard()
    return dict(ordinary_file_identities=files, symlinks=links, directories=sorted(directories))

def protected_disjoint(rows, protected):
    paths = {r['path'] for r in protected}
    ids = set()
    for row in protected:
        s = Path(row['path']).lstat()
        if identity(s) != row['identity']:
            raise RuntimeError('protected 7ID changed')
        ids.add((s.st_dev, s.st_ino))
    for row in rows:
        p = Path(row['path'])
        if p not in candidates() or p.suffix != '.xsm':
            raise RuntimeError('target outside hard-coded exact list')
        s = p.lstat()
        if not stat.S_ISREG(s.st_mode) or s.st_nlink != 1 or identity(s) != row['identity']:
            raise RuntimeError('candidate regular/nlink1/stable 7ID required')
        if str(p) in paths or (s.st_dev, s.st_ino) in ids:
            raise RuntimeError('target intersects current mandatory pin path or inode')

def budget():
    spec = importlib.util.spec_from_file_location('storage_release_original_history_factory', FACTORY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    roots = module.history_roots([], ART)
    observer = module.DynamicHistoryResources(ART, roots, 8 * 2**30, 96 * 2**30)
    d = observer.check()
    d['original_cold_reserve_bytes'] = 20971764748
    d['metadata_reserve_bytes'] = 64 * 2**20
    d['initial_fresh_reserve_bytes'] = 2 * 2**30
    d['remaining_after_original_initial_reserves_bytes'] = (96 * 2**30 - d['artifact_bytes']
        - 20971764748 - 64 * 2**20 - 2 * 2**30)
    d['original_initial_reserve_admitted'] = d['remaining_after_original_initial_reserves_bytes'] > 0
    return d

def write_new(path, data):
    raw = (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode()
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
    with os.fdopen(fd, 'wb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())

def update_owned_receipt(path, data):
    temp = path.with_suffix('.pending')
    write_new(temp, data)
    os.replace(temp, path)

