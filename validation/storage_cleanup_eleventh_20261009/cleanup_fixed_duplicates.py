#!/usr/bin/env python3
"""Validate a fixed duplicate list; delete only with an explicit execute flag."""
import argparse
import hashlib
import json
import os
import stat
import subprocess
import time
from pathlib import Path

ROOT = Path('/Users/wen/spot')
REPORT = ROOT / 'validation/storage_cleanup_eleventh_20261009'

def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink]

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        while b := f.read(4 * 1024**2):
            h.update(b)
    return h.hexdigest()

def safe_art(raw):
    p = Path(raw)
    if not p.is_absolute() or str(p) != raw or '..' in p.parts or not p.is_relative_to(ROOT / 'validation/artifacts') or p.parent.resolve(strict=True) != p.parent:
        raise ValueError('unsafe artifact path')
    return p

def check_pin(row, artifact=False):
    p = safe_art(row['path']) if artifact else Path(row['path'])
    s = p.lstat()
    if not stat.S_ISREG(s.st_mode) or identity(s) != row['identity'] or s.st_size != row['size']:
        raise ValueError('file identity differs: ' + str(p))
    h = sha(p)
    if h != row['sha256'] or identity(p.lstat()) != row['identity']:
        raise ValueError('file content or identity changed: ' + str(p))
    return p

def snapshot():
    files, links, dirs = {}, {}, []
    for cur, sub, names in os.walk(ROOT, followlinks=False):
        base = Path(cur)
        if base == ROOT:
            sub[:] = [s for s in sub if s != '.git']
        sub[:] = [s for s in sub if base / s != REPORT]
        dirs.append(str(base.relative_to(ROOT)))
        for n in sub + names:
            p = base / n
            s = p.lstat()
            rel = str(p.relative_to(ROOT))
            if stat.S_ISLNK(s.st_mode):
                links[rel] = [identity(s), os.readlink(p)]
            elif stat.S_ISREG(s.st_mode):
                files[rel] = identity(s)
    return {'files': files, 'links': links, 'dirs': sorted(dirs)}

def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def capacity():
    result = subprocess.run(['/usr/bin/du', '-sk', str(ROOT)], check=True, text=True, capture_output=True)
    return {'project_allocated_bytes_du': int(result.stdout.split()[0]) * 1024, 'free_bytes': os.statvfs(ROOT).f_bavail * os.statvfs(ROOT).f_frsize}

def write(name, data):
    (REPORT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest-sha', required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    if REPORT.resolve(strict=True) != REPORT:
        raise ValueError('unsafe report directory')
    manifest_path = REPORT / 'manifest.json'
    if sha(manifest_path) != args.manifest_sha:
        raise ValueError('manifest differs')
    m = json.loads(manifest_path.read_text())
    if sha(Path(__file__)) != m['cleanup_source_sha256'] or sha(REPORT / 'result_document_full_sha_baseline.json') != m['result_document_baseline_sha256']:
        raise ValueError('cleanup source or document baseline differs')
    rows = m['candidates']
    paths = {r['path'] for r in rows}
    primaries = {r['path'] for r in m['retained_primaries']}
    if len(paths) != m['exact_count'] or not rows or paths & primaries:
        raise ValueError('invalid fixed candidates')
    for r in rows:
        if r['category'] != 'EXACT_DUPLICATE_OLD_WORK_COPY' or r['identity'][6] != 1 or r['retained_primary'] not in primaries:
            raise ValueError('unapproved candidate')
        p = check_pin(r, True)
        if p.name in {'result.json', 'result.sha256', 'seal.json'} or p.suffix not in {'.xsm', '.npz', '.bin'}:
            raise ValueError('result/source deletion denied')
    for r in m['retained_primaries']:
        check_pin(r, True)
    for r in m['source_and_review_pins']:
        check_pin(r)
    by_primary = {r['path']: r for r in m['retained_primaries']}
    for r in rows:
        p = by_primary[r['retained_primary']]
        if (r['size'], r['sha256']) != (p['size'], p['sha256']):
            raise ValueError('duplicate differs from primary')
    documents = json.loads((REPORT / 'result_document_full_sha_baseline.json').read_text())
    for r in documents['rows']:
        check_pin({**r, 'path': str(ROOT / r['path'])})
    before = snapshot()
    started = time.time()
    pre = {'status': 'PASS_FIXED_FULL_SHA_PREFLIGHT', 'manifest_sha256': args.manifest_sha, 'candidates': len(rows), 'result_documents_full_sha_checked': len(documents['rows']), 'result_document_bytes': documents['bytes'], 'untouched_snapshot_sha256': fingerprint(before), 'capacity': capacity(), 'timestamp': started, 'executed': False}
    if not args.execute:
        write('preflight.json', pre)
        print(json.dumps(pre))
        return
    prior = json.loads((REPORT / 'preflight.json').read_text())
    if prior['status'] != pre['status'] or prior['manifest_sha256'] != args.manifest_sha or prior['untouched_snapshot_sha256'] != pre['untouched_snapshot_sha256']:
        raise ValueError('preflight baseline changed')
    if (REPORT / 'retirement_ledger.jsonl').exists() or (REPORT / 'cleanup_result.json').exists():
        raise ValueError('cleanup already attempted')
    removed = []
    with (REPORT / 'retirement_ledger.jsonl').open('x') as ledger:
        for r in rows:
            p = check_pin(r, True)
            check_pin(by_primary[r['retained_primary']], True)
            p.unlink()
            removed.append(str(p))
            ledger.write(json.dumps({**r, 'removed_at': time.time()}, ensure_ascii=False) + '\n')
            ledger.flush()
            os.fsync(ledger.fileno())
    after = snapshot()
    expected = {**before, 'files': {k: v for k, v in before['files'].items() if str(ROOT / k) not in paths}}
    if after != expected:
        raise ValueError('unrelated project paths/identities changed')
    for r in m['retained_primaries']:
        check_pin(r, True)
    for r in m['source_and_review_pins']:
        check_pin(r)
    for r in documents['rows']:
        check_pin({**r, 'path': str(ROOT / r['path'])})
    result = {'status': 'PASS_ACTUAL_EXACT_DUPLICATE_CLEANUP', 'manifest_sha256': args.manifest_sha, 'removed_count': len(removed), 'removed_paths': removed, 'removed_allocated_bytes': sum(r['allocated_bytes'] for r in rows), 'removed_logical_bytes': sum(r['size'] for r in rows), 'all_other_regular_paths_and_identities_unchanged': True, 'all_symlinks_and_directory_paths_unchanged': True, 'result_documents_full_sha_checked_before_and_after': len(documents['rows']), 'all_retained_primaries_and_source_pins_full_sha_unchanged': True, 'before_capacity': pre['capacity'], 'after_capacity': capacity(), 'started': started, 'finished': time.time(), 'scientific_credit': False}
    write('cleanup_result.json', result)
    print(json.dumps(result))

if __name__ == '__main__':
    main()
