"""Remove only the reviewed fixed cache list; preserve all directories."""
import argparse
import hashlib
import json
import os
import stat
import time
from pathlib import Path

ROOT = Path('/Users/wen/spot')
REPORT = Path(__file__).parent

def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink]

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def check(row):
    p = Path(row['path'])
    s = p.lstat()
    if not stat.S_ISREG(s.st_mode) or identity(s) != row['identity'] or sha(p) != row['sha256'] or identity(p.lstat()) != row['identity']:
        raise ValueError('Changed reviewed file: ' + str(p))
    return p

def other_paths_digest(excluded):
    h = hashlib.sha256()
    counts = {'regular_files': 0, 'symlinks': 0, 'directories': 0}
    for cur, sub, names in os.walk(ROOT, followlinks=False):
        base = Path(cur)
        sub[:] = sorted(n for n in sub if base / n not in {ROOT / '.git', REPORT})
        h.update(json.dumps(['directory', str(base.relative_to(ROOT))], separators=(',', ':')).encode() + b'\n')
        counts['directories'] += 1
        for name in sorted(sub + names):
            p = base / name
            if str(p) in excluded:
                continue
            s = p.lstat()
            if stat.S_ISLNK(s.st_mode):
                value = ['link', str(p.relative_to(ROOT)), identity(s), os.readlink(p)]
                counts['symlinks'] += 1
            elif stat.S_ISREG(s.st_mode):
                value = ['file', str(p.relative_to(ROOT)), identity(s)]
                counts['regular_files'] += 1
            else:
                continue
            h.update(json.dumps(value, separators=(',', ':')).encode() + b'\n')
    return {'sha256': h.hexdigest(), **counts}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--manifest-sha', required=True)
    ap.add_argument('--execute', action='store_true')
    args = ap.parse_args()
    manifest = REPORT / 'cache_manifest.json'
    if REPORT.resolve(strict=True) != REPORT or sha(manifest) != args.manifest_sha:
        raise ValueError('Report or manifest differs')
    m = json.loads(manifest.read_text())
    if sha(Path(__file__)) != m['cleanup_source_sha256']:
        raise ValueError('Cleanup source differs')
    rows = m['candidates']
    paths = {r['path'] for r in rows}
    if len(rows) != 64 or len(paths) != 64:
        raise ValueError('Not the fixed 64-file list')
    for row in rows:
        p = Path(row['path'])
        python_cache = p.is_relative_to(ROOT / 'validation') and p.parent.name == '__pycache__' and p.suffix == '.pyc'
        ruff_cache = p.is_relative_to(ROOT / '.ruff_cache')
        if not (python_cache or ruff_cache) or p.parent.resolve(strict=True) != p.parent or row['identity'][6] != 1:
            raise ValueError('Not a regular regenerable cache: ' + str(p))
        check(row)
    for row in m['retained_sources']:
        check(row)
    before = other_paths_digest(paths)
    result = {'status': 'PASS_FIXED_CACHE_PREFLIGHT', 'manifest_sha256': args.manifest_sha, 'count': len(rows), 'allocated_bytes': sum(r['allocated_bytes'] for r in rows), 'logical_bytes': sum(r['size'] for r in rows), 'other_paths': before, 'executed': False, 'timestamp': time.time()}
    if args.execute:
        ledger = REPORT / 'retirement_ledger.jsonl'
        if os.path.lexists(ledger) or os.path.lexists(REPORT / 'cleanup_result.json'):
            raise ValueError('Cleanup already attempted')
        with ledger.open('x') as f:
            for row in rows:
                check(row).unlink()
                f.write(json.dumps({'path': row['path'], 'sha256': row['sha256'], 'removed_at': time.time()}, ensure_ascii=False) + '\n')
                f.flush()
                os.fsync(f.fileno())
        if any(os.path.lexists(p) for p in paths):
            raise ValueError('A removed cache path was recreated')
        after = other_paths_digest(paths)
        if after != before:
            raise ValueError('Other project paths or identities changed')
        for row in m['retained_sources']:
            check(row)
        result.update(status='PASS_ACTUAL_FIXED_CACHE_CLEANUP', executed=True, other_paths_after=after, scientific_credit=False)
        with (REPORT / 'cleanup_result.json').open('x') as f:
            f.write(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
            f.flush()
            os.fsync(f.fileno())
    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main()
