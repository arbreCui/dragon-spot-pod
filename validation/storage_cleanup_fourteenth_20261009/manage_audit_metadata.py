"""Losslessly archive ten fixed historical audit inventories; default is read-only.

Old reports and scripts stay unchanged. Replaying an old inventory reader requires
restoring its original JSON first. This does not restore historical inode/ctime.
"""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat

ROOT = Path('/Users/wen/spot')
OUT = ROOT / 'validation/storage_cleanup_fourteenth_20261009'
PLAN = OUT / 'audit_metadata_candidates.json'
MANIFEST = OUT / 'audit_metadata_manifest.json'
CHUNK = 1024 * 1024


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(CHUNK), b''):
            h.update(b)
    return h.hexdigest()


def identity(path):
    s = path.lstat()
    assert stat.S_ISREG(s.st_mode) and s.st_nlink == 1
    assert path.resolve() == path and path.is_relative_to(ROOT)
    return dict(size=s.st_size, allocated=s.st_blocks * 512, dev=s.st_dev,
                ino=s.st_ino, nlink=s.st_nlink, mode=s.st_mode,
                mtime_ns=s.st_mtime_ns, ctime_ns=s.st_ctime_ns)


def write_new(path, value):
    with path.open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')
        f.flush(); os.fsync(f.fileno())


def fingerprint(excluded):
    """Preserve all other regular identities and symlink targets, excluding Git/R14."""
    h = hashlib.sha256(); count = links = directories = 0
    for base, dirs, files in os.walk(ROOT, followlinks=False):
        dirs.sort(); files.sort()
        dirs[:] = [d for d in dirs if Path(base) / d not in (ROOT / '.git', OUT)]
        for name in dirs + files:
            p = Path(base) / name
            if str(p) in excluded:
                continue
            s = p.lstat()
            if stat.S_ISREG(s.st_mode):
                row = [str(p.relative_to(ROOT)), s.st_dev, s.st_ino, s.st_mode,
                       s.st_nlink, s.st_size, s.st_blocks, s.st_mtime_ns, s.st_ctime_ns]
                count += 1
            elif stat.S_ISLNK(s.st_mode):
                row = [str(p.relative_to(ROOT)), 'symlink', os.readlink(p)]
                links += 1
            elif stat.S_ISDIR(s.st_mode):
                row = [str(p.relative_to(ROOT)), 'directory_path']
                directories += 1
            else:
                continue
            h.update(json.dumps(row, separators=(',', ':')).encode() + b'\n')
    return dict(sha256=h.hexdigest(), regular_files=count, symlinks=links,
                directory_paths=directories)


def valid_plan():
    items = json.loads(PLAN.read_text())
    assert type(items) is list and len(items) == 10
    assert len({r['path'] for r in items}) == 10
    allowed_names = {'preservation_baseline.json', 'independent_before_project_snapshot.json',
                     'full_project_actual_after_snapshot_metadata_only.json',
                     'all_fresh_retained_source_document_FULL_SHA_identity.json',
                     'independent_preflight_fresh_SHA_records.json',
                     'independent_actual_fresh_SHA_records.json', 'independent_full_SHA_records.json'}
    for r in items:
        p = Path(r['path'])
        assert p.is_relative_to(ROOT / 'validation')
        assert p.parts[len(ROOT.parts) + 1].startswith('storage_cleanup_')
        assert p.name in allowed_names and r['size'] > 5 * CHUNK
    return items


def verified_archive(record):
    archive = Path(record['archive_path'])
    assert archive.parent == OUT / 'metadata_archives'
    before = identity(archive)
    assert digest(archive) == record['archive_sha256']
    h = hashlib.sha256(); size = 0
    with gzip.open(archive, 'rb') as f:
        for b in iter(lambda: f.read(CHUNK), b''):
            h.update(b); size += len(b)
    assert h.hexdigest() == record['sha256'] and size == record['size']
    assert identity(archive) == before


def pack():
    items = valid_plan(); archives = OUT / 'metadata_archives'
    archives.mkdir(exist_ok=False); records = []
    for item in items:
        p = Path(item['path']); before = identity(p)
        assert before == {k: item[k] for k in before}
        sha = digest(p); archive = archives / (sha + '.json.gz')
        if not archive.exists():
            with p.open('rb') as src, archive.open('xb') as dst:
                with gzip.GzipFile(filename='', mode='wb', fileobj=dst, mtime=0, compresslevel=9) as z:
                    for b in iter(lambda: src.read(CHUNK), b''):
                        z.write(b)
        record = dict(item, sha256=sha, archive_path=str(archive),
                      archive_sha256=digest(archive), archive_size=archive.stat().st_size,
                      archive_allocated=archive.stat().st_blocks * 512)
        verified_archive(record)
        assert identity(p) == before
        records.append(record)
    write_new(MANIFEST, dict(kind='LOSSLESS_OLD_AUDIT_METADATA_ONLY', records=records,
        untouched_before=fingerprint({r['path'] for r in records}),
        old_reader_rule='Restore exact original JSON before replaying old readers; old source/reports unchanged.',
        restores_original_inode_or_ctime=False, scientific_credit=False))
    print(json.dumps(dict(status='ARCHIVES_VERIFIED_ORIGINALS_STILL_PRESENT',
        manifest_sha256=digest(MANIFEST), paths=len(records),
        unique_archives=len(list(archives.iterdir())))))


def load_manifest(expected):
    assert expected and digest(MANIFEST) == expected
    m = json.loads(MANIFEST.read_text()); plan = valid_plan()
    assert [r['path'] for r in m['records']] == [r['path'] for r in plan]
    assert m['kind'] == 'LOSSLESS_OLD_AUDIT_METADATA_ONLY'
    return m


def retire(expected):
    m = load_manifest(expected); records = m['records']
    assert fingerprint({r['path'] for r in records}) == m['untouched_before']
    for r in records:
        p = Path(r['path']); now = identity(p)
        assert now == {k: r[k] for k in now} and digest(p) == r['sha256']
        verified_archive(r)
    assert not os.path.lexists(OUT / 'audit_metadata_retirement_result.json')
    for r in records:
        Path(r['path']).unlink()
    after = fingerprint({r['path'] for r in records})
    assert after == m['untouched_before']
    assert all(not os.path.lexists(r['path']) for r in records)
    write_new(OUT / 'audit_metadata_retirement_result.json', dict(
        status='TEN_ORIGINAL_INVENTORIES_RETIRED_ALL_BYTES_RECOVERABLE',
        manifest_sha256=expected, deleted_paths=[r['path'] for r in records],
        original_allocated_bytes=sum(r['allocated'] for r in records),
        unchanged_other_files=after, scientific_credit=False))
    print(json.dumps(dict(status='RETIRED', paths=len(records), unchanged_other_files=after)))


def restore(expected, selected):
    m = load_manifest(expected)
    matches = [r for r in m['records'] if r['path'] == selected]
    assert len(matches) == 1
    r = matches[0]; p = Path(r['path']); verified_archive(r)
    assert not p.exists() and not p.is_symlink() and p.parent.resolve() == p.parent
    tmp = p.with_name(p.name + '.r14-restore-tmp')
    assert not os.path.lexists(tmp)
    created = False
    try:
        with gzip.open(Path(r['archive_path']), 'rb') as src, tmp.open('xb') as dst:
            created = True
            for b in iter(lambda: src.read(CHUNK), b''):
                dst.write(b)
            dst.flush(); os.fsync(dst.fileno())
        assert digest(tmp) == r['sha256'] and tmp.stat().st_size == r['size']
        os.chmod(tmp, stat.S_IMODE(r['mode']))
        os.utime(tmp, ns=(r['mtime_ns'], r['mtime_ns']))
        os.link(tmp, p); tmp.unlink()
    finally:
        if created and os.path.lexists(tmp): tmp.unlink()
    print(json.dumps(dict(status='RESTORED_ORIGINAL_BYTES', path=str(p), sha256=r['sha256'],
                          restores_original_inode_or_ctime=False)))


def main():
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument('action', nargs='?', choices=('list', 'pack', 'retire', 'restore'), default='list')
    a.add_argument('--manifest-sha256'); a.add_argument('--path')
    n = a.parse_args()
    if n.action == 'pack': pack()
    elif n.action == 'retire': retire(n.manifest_sha256)
    elif n.action == 'restore': restore(n.manifest_sha256, n.path)
    else: print(json.dumps([r['path'] for r in valid_plan()], ensure_ascii=False, indent=2))


if __name__ == '__main__': main()
