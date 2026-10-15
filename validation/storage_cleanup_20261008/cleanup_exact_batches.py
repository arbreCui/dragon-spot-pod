#!/usr/bin/env python3
"""Retire only the two reviewed, user-authorized SPOT file batches.

Preflight performs all content checks without deleting anything. Apply requires
the externally observed preflight SHA and deletes ordinary leaf files only.
Historical seals stay untouched; the separate ledger records retirement.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import time

ROOT = Path('/Users/wen/spot')
REVIEW = ROOT / 'validation/storage_review_20261008'
OUT = ROOT / 'validation/storage_cleanup_20261008'
ART = ROOT / 'validation/artifacts'
PINS = {
    'first_batch_24_files.json': 'ca1e408ebfccae3d61588d45d852a3c699b923f95a12d9a91c527aa22e8f6e79',
    'second_batch_replay_arrays.json': '9e06773ede68bd14fd892bfadc42bf2d02088988febd13f5cfb3faf2f5cef3ad',
}
LEGACY = ('native-oblique-full-response-20260930', 'native-segment-composition-compact-20260929')
NAMES = ('projected_proposal.xsm', 'candidate_radial.xsm', 'candidate_snapshots.xsm')


def sig(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink]


def ordinary_ancestors(p):
    p.relative_to(ROOT)
    parent = ROOT
    if not stat.S_ISDIR(parent.lstat().st_mode):
        raise ValueError('workspace root is not ordinary directory')
    for component in p.parent.relative_to(ROOT).parts:
        parent /= component
        if not stat.S_ISDIR(parent.lstat().st_mode):
            raise ValueError('nonordinary ancestor: ' + str(parent))


def fresh(p, expected=None):
    ordinary_ancestors(p)
    before = p.lstat()
    if not stat.S_ISREG(before.st_mode):
        raise ValueError('not ordinary file: ' + str(p))
    fd = os.open(p, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        if sig(os.fstat(fd)) != sig(before):
            raise ValueError('opened identity changed: ' + str(p))
        h = hashlib.sha256()
        count = 0
        while True:
            chunk = os.read(fd, 4 * 1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
            count += len(chunk)
        if sig(os.fstat(fd)) != sig(before):
            raise ValueError('read identity changed: ' + str(p))
    finally:
        os.close(fd)
    if sig(p.lstat()) != sig(before) or count != before.st_size:
        raise ValueError('postread identity or byte count changed: ' + str(p))
    digest = h.hexdigest()
    if expected is not None and digest != expected:
        raise ValueError('content differs from expected seal: ' + str(p))
    return dict(path=str(p), sha256=digest, bytes=count, identity=sig(before), allocated_bytes=before.st_blocks * 512)


def write_new(p, value):
    with p.open('x') as f:
        json.dump(value, f, indent=2, allow_nan=False)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())


def inventory():
    files, links, directories = {}, {}, []
    stack = [ROOT]
    while stack:
        base = stack.pop()
        with os.scandir(base) as entries:
            for entry in entries:
                p = Path(entry.path)
                if p == OUT:
                    continue
                relative = str(p.relative_to(ROOT))
                s = entry.stat(follow_symlinks=False)
                if stat.S_ISREG(s.st_mode):
                    files[relative] = sig(s)
                elif stat.S_ISLNK(s.st_mode):
                    links[relative] = [sig(s), os.readlink(p)]
                elif stat.S_ISDIR(s.st_mode):
                    directories.append(relative)
                    stack.append(p)
                else:
                    raise ValueError('unexpected special workspace entry: ' + relative)
    return dict(files=files, symlinks=links, directories=sorted(directories))


def reviewed_files():
    manifests, rows = {}, []
    for name, expected in PINS.items():
        descriptor = fresh(REVIEW / name, expected)
        d = json.loads((REVIEW / name).read_text())
        if d['file_count'] != len(d['files']):
            raise ValueError('manifest count mismatch')
        manifests[name] = descriptor
        rows.extend(d['files'])
    first = {str(ART / 'axial-material-production-qualified-AB-rank1-factor-cache-20261007/AAA' / ('map%03d' % n) / name)
             for n in range(1, 9) for name in NAMES}
    paths = [r['path'] for r in rows]
    if len(rows) != 7563 or len(set(paths)) != 7563 or set(paths[:24]) != first:
        raise ValueError('exact reviewed batch set/count mismatch')
    for r in rows[24:]:
        p = Path(r['path'])
        if p.suffix != '.npz' or not any(p.is_relative_to(ART / family / 'replay') for family in LEGACY):
            raise ValueError('outside exact legacy replay NPZ scope')
    if sum(r['size_bytes'] for r in rows) != 20073997918:
        raise ValueError('reviewed logical byte count mismatch')
    return manifests, rows


def check_row(r):
    p = Path(r['path'])
    ordinary_ancestors(p)
    s = p.lstat()
    if (not stat.S_ISREG(s.st_mode) or s.st_nlink != 1 or
        [s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink] !=
        [r['device'], r['inode'], r['size_bytes'], r['mtime_ns'], r['ctime_ns'], r['hard_link_count']] or
        s.st_blocks * 512 != r['allocated_bytes']):
        raise ValueError('candidate changed since review: ' + str(p))


def preflight():
    started = time.monotonic()
    if os.path.lexists(OUT):
        raise ValueError('exclusive cleanup evidence directory already exists')
    manifests, rows = reviewed_files()
    for r in rows:
        check_row(r)
    OUT.mkdir()
    # Immutable review document content is checked before cleanup.
    document_pins = json.loads((REVIEW / 'document_inventory.json').read_text())['files']
    documents = [fresh(REVIEW / name, d['sha256']) for name, d in document_pins.items()]
    documents.append(fresh(REVIEW / 'document_inventory.json'))
    owners = {}
    expected_maps = {}
    for family in LEGACY:
        p = ART / family / 'result.sha256'
        owners[str(p)] = fresh(p)
        table = {}
        for line in p.read_text().splitlines():
            if not re.fullmatch(r'[0-9a-f]{64}  .+', line):
                raise ValueError('unexpected historical seal format')
            digest, name = line.split('  ', 1)
            if name in table:
                raise ValueError('duplicate historical seal path')
            table[name] = digest
        expected_maps[family] = table
    baseline = inventory()
    write_new(OUT / 'preservation_baseline.json', baseline)
    baseline_descriptor = fresh(OUT / 'preservation_baseline.json')
    records = []
    for i, row in enumerate(rows):
        check_row(row)
        p = Path(row['path'])
        if i < 24:
            owner = Path(row['old_map_result'])
            if owner != p.parent / 'result.json':
                raise ValueError('unexpected old result owner')
            if str(owner) not in owners:
                owners[str(owner)] = fresh(owner)
            expected = json.loads(owner.read_text())['sha256'][p.name]
            candidate = fresh(p, expected)
            primary = None
        else:
            family = next(f for f in LEGACY if p.is_relative_to(ART / f / 'replay'))
            base = ART / family
            relative = p.relative_to(base)
            primary_path = base.joinpath(*relative.parts[1:])
            if str(primary_path) in {r['path'] for r in rows[:24]} or '/replay/' in str(primary_path):
                raise ValueError('primary falls in deletion set')
            table = expected_maps[family]
            expected = table[str(relative)]
            if table[str(primary_path.relative_to(base))] != expected:
                raise ValueError('historical replay and primary expected SHA disagree')
            candidate = fresh(p, expected)
            primary = fresh(primary_path, expected)
            if primary['bytes'] != candidate['bytes']:
                raise ValueError('primary and replay byte counts disagree')
            owner = base / 'result.sha256'
        if candidate['identity'] != baseline['files'][str(p.relative_to(ROOT))]:
            raise ValueError('candidate differs from preservation baseline')
        records.append(dict(batch=1 if i < 24 else 2, candidate=candidate, primary=primary, historical_owner=str(owner)))
        if (i + 1) % 1000 == 0 or i + 1 == len(rows):
            print(json.dumps(dict(preflight_checked=i + 1, total=len(rows), elapsed_seconds=time.monotonic() - started)), flush=True)
    for owner in owners.values():
        fresh(Path(owner['path']), owner['sha256'])
    write_new(OUT / 'preflight.json', dict(schema='SPOT_EXACT_TWO_BATCH_CLEANUP_PREFLIGHT_V1', status='PASS',
              manifests=manifests, review_documents=documents, historical_owners=owners,
              preservation_baseline=baseline_descriptor, candidates=records, file_count=len(records),
              logical_bytes=sum(r['candidate']['bytes'] for r in records),
              allocated_bytes=sum(r['candidate']['allocated_bytes'] for r in records),
              elapsed_seconds=time.monotonic() - started, deleted_files=0,
              historical_replay_and_primary_contents_freshly_equal=True))
    print(json.dumps(dict(status='PREFLIGHT_PASS_NO_DELETIONS', preflight=fresh(OUT / 'preflight.json'))), flush=True)


def unlink_exact(record):
    p = Path(record['path'])
    parts = p.relative_to(ROOT).parts
    fd = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for component in parts[:-1]:
            next_fd = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = next_fd
        if sig(os.stat(parts[-1], dir_fd=fd, follow_symlinks=False)) != record['identity']:
            raise ValueError('candidate changed immediately before unlink')
        os.unlink(parts[-1], dir_fd=fd)
        try:
            os.stat(parts[-1], dir_fd=fd, follow_symlinks=False)
        except FileNotFoundError:
            return
        raise ValueError('deleted candidate still exists')
    finally:
        os.close(fd)


def apply(expected):
    started = time.monotonic()
    reviewed, rows = reviewed_files()
    fresh(OUT / 'preflight.json', expected)
    pre = json.loads((OUT / 'preflight.json').read_text())
    if pre['status'] != 'PASS' or pre['file_count'] != 7563 or pre['deleted_files'] != 0:
        raise ValueError('invalid preflight')
    if {r['candidate']['path'] for r in pre['candidates']} != {r['path'] for r in rows}:
        raise ValueError('preflight deletion set differs from pinned review')
    for row, record in zip(rows, pre['candidates']):
        if row['path'] != record['candidate']['path']:
            raise ValueError('preflight candidate order differs')
        check_row(row)
        if sig(Path(row['path']).lstat()) != record['candidate']['identity']:
            raise ValueError('candidate changed since fresh preflight')
        if record['primary'] and sig(Path(record['primary']['path']).lstat()) != record['primary']['identity']:
            raise ValueError('retained primary changed since fresh preflight')
    for owner in pre['historical_owners'].values():
        fresh(Path(owner['path']), owner['sha256'])
    fresh(OUT / 'preservation_baseline.json', pre['preservation_baseline']['sha256'])
    baseline = json.loads((OUT / 'preservation_baseline.json').read_text())
    if inventory() != baseline:
        raise ValueError('workspace changed since preflight; no deletion started')
    with (OUT / 'retirement_ledger.jsonl').open('x') as ledger:
        for i, record in enumerate(pre['candidates']):
            unlink_exact(record['candidate'])
            item = dict(sequence=i + 1, batch=record['batch'], **record['candidate'],
                        historical_owner=record['historical_owner'], retained_primary=record['primary'],
                        action='ordinary_leaf_unlinked', absent_after_unlink=True)
            ledger.write(json.dumps(item, allow_nan=False) + '\n')
            ledger.flush()
            os.fsync(ledger.fileno())
            if (i + 1) % 1000 == 0 or i + 1 == len(pre['candidates']):
                print(json.dumps(dict(deleted_files=i + 1, total=len(pre['candidates']))), flush=True)
    for record in pre['candidates']:
        del baseline['files'][str(Path(record['candidate']['path']).relative_to(ROOT))]
    after = inventory()
    if after != baseline:
        changed = [p for p in set(after['files']) | set(baseline['files']) if after['files'].get(p) != baseline['files'].get(p)]
        write_new(OUT / 'preservation_failure.json', dict(changed_retained_paths=changed,
                  symlinks_unchanged=after['symlinks'] == baseline['symlinks'], directories_unchanged=after['directories'] == baseline['directories']))
        raise ValueError('postcleanup preservation mismatch; inspect recorded facts')
    for owner in pre['historical_owners'].values():
        fresh(Path(owner['path']), owner['sha256'])
    for doc in pre['review_documents']:
        fresh(Path(doc['path']), doc['sha256'])
    result = dict(schema='SPOT_EXACT_TWO_BATCH_CLEANUP_ACTUAL_V1', status='PASS',
                  preflight_sha256=expected, deleted_files=7563, batch1_files=24, batch2_files=7539,
                  removed_logical_bytes=pre['logical_bytes'], removed_allocated_bytes=pre['allocated_bytes'],
                  retained_regular_paths=len(after['files']), retained_symlinks=len(after['symlinks']),
                  retained_directories=len(after['directories']), all_retained_file_identities_unchanged=True,
                  all_symlink_entries_unchanged=True, directory_membership_unchanged=True,
                  historical_seals_and_result_documents_unchanged=True, historical_full_replay_retired=True,
                  physics_execution=False, current_INPUT_revalidation_still_required=True,
                  elapsed_seconds=time.monotonic() - started)
    write_new(OUT / 'cleanup_result.json', result)
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=('preflight', 'apply'))
    parser.add_argument('--preflight-sha256')
    args = parser.parse_args()
    if args.mode == 'preflight':
        preflight()
    else:
        if not args.preflight_sha256 or not re.fullmatch(r'[0-9a-f]{64}', args.preflight_sha256):
            raise ValueError('externally observed preflight SHA required')
        apply(args.preflight_sha256)
