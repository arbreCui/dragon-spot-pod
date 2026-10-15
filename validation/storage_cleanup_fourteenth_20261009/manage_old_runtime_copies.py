"""Five exact old V2-V6 program copies; default only lists recovery mappings."""
import argparse
import json
import os
from pathlib import Path
import runpy
import stat

OUT = Path('/Users/wen/spot/validation/storage_cleanup_fourteenth_20261009')
HELPER = OUT / 'manage_audit_metadata.py'
PLAN = OUT / 'old_runtime_dependency_review/exact5_runtime_candidates.json'
MANIFEST = OUT / 'runtime_retirement_manifest.json'
HELPER_SHA = '886be02cde541acd00e922d5f67965250ca1b50dc8302e374904b3f0839d541d'
PLAN_SHA = '02f7ffe3c5775e381c2326cc766dc3f9274590635fda8838338c30e55835d4ee'


def context():
    import hashlib
    assert hashlib.sha256(HELPER.read_bytes()).hexdigest() == HELPER_SHA
    h = runpy.run_path(str(HELPER))
    assert h['digest'](PLAN) == PLAN_SHA
    rows = json.loads(PLAN.read_text())['candidates']
    assert len(rows) == 5 and [r['version'] for r in rows] == [2, 3, 4, 5, 6]
    for r in rows:
        p = Path(r['path']); year = '20261008'
        assert str(p) == ('/Users/wen/spot/validation/artifacts/axial-material-historical-input-'
            'physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-'
            f"scopes-v{r['version']}-{year}/runtime/Dragon")
        assert r['retained_primary']['sha256'] == r['sha256']
    return h, rows


def same_identity(h, path, expected):
    d = h['identity'](path)
    actual = [d['dev'], d['ino'], d['mode'], d['size'], d['mtime_ns'], d['ctime_ns'], d['nlink']]
    assert actual == expected


def primary(h, rows):
    r = rows[0]['retained_primary']; p = Path(r['path'])
    assert all(x['retained_primary'] == r for x in rows)
    same_identity(h, p, r['identity'])
    assert h['digest'](p) == r['sha256'] and p.stat().st_size == r['size_bytes']
    return p


def main():
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument('action', nargs='?', choices=('list', 'prepare', 'retire', 'restore'), default='list')
    a.add_argument('--manifest-sha256'); a.add_argument('--path'); n = a.parse_args()
    h, rows = context()
    if n.action == 'list':
        print(json.dumps([r['restore_byte_exact_mapping'] for r in rows], indent=2)); return
    if n.action == 'prepare':
        primary(h, rows)
        for r in rows:
            p = Path(r['path']); same_identity(h, p, r['identity'])
            assert h['digest'](p) == r['sha256']
        h['write_new'](MANIFEST, dict(kind='FIVE_EXACT_OLD_FAILED_RUNTIME_COPIES_ONLY',
            source_sha256=h['digest'](Path(__file__)), helper_sha256=HELPER_SHA, plan_sha256=PLAN_SHA,
            candidates=rows, untouched_before=h['fingerprint']({r['path'] for r in rows}), scientific_credit=False))
        print(json.dumps(dict(status='PREPARED_NO_DELETION', manifest_sha256=h['digest'](MANIFEST)))); return
    assert n.manifest_sha256 and h['digest'](MANIFEST) == n.manifest_sha256
    m = json.loads(MANIFEST.read_text())
    assert m['candidates'] == rows and m['source_sha256'] == h['digest'](Path(__file__))
    src = primary(h, rows)
    if n.action == 'retire':
        assert h['fingerprint']({r['path'] for r in rows}) == m['untouched_before']
        assert not os.path.lexists(OUT / 'runtime_retirement_result.json')
        for r in rows:
            p = Path(r['path']); same_identity(h, p, r['identity'])
            assert h['digest'](p) == r['sha256']
        for r in rows: Path(r['path']).unlink()
        assert all(not os.path.lexists(r['path']) for r in rows)
        after = h['fingerprint']({r['path'] for r in rows})
        assert after == m['untouched_before']; primary(h, rows)
        h['write_new'](OUT / 'runtime_retirement_result.json', dict(status='FIVE_RETIRED',
            manifest_sha256=n.manifest_sha256, deleted_paths=[r['path'] for r in rows],
            allocated_bytes=sum(r['allocated_bytes'] for r in rows), unchanged_other_files=after,
            old_failure_promoted=False, scientific_credit=False))
        print(json.dumps(dict(status='FIVE_RETIRED', unchanged_other_files=after))); return
    selected = [r for r in rows if r['path'] == n.path]; assert len(selected) == 1
    r = selected[0]; p = Path(r['path']); tmp = p.with_name('Dragon.r14-restore-tmp')
    assert not os.path.lexists(p) and not os.path.lexists(tmp) and p.parent.resolve() == p.parent
    created = False
    try:
        with src.open('rb') as f, tmp.open('xb') as g:
            created = True
            for b in iter(lambda: f.read(1024 * 1024), b''): g.write(b)
            g.flush(); os.fsync(g.fileno())
        assert h['digest'](tmp) == r['sha256'] and tmp.stat().st_size == r['size_bytes']
        os.chmod(tmp, stat.S_IMODE(r['identity'][2])); os.utime(tmp, ns=(r['identity'][4], r['identity'][4]))
        os.link(tmp, p); tmp.unlink()
    finally:
        if created and os.path.lexists(tmp): tmp.unlink()
    print(json.dumps(dict(status='ORIGINAL_PROGRAM_BYTES_RESTORED', path=str(p), sha256=r['sha256'],
                          original_inode_or_ctime_restorable=False, old_failure_promoted=False)))


if __name__ == '__main__': main()
