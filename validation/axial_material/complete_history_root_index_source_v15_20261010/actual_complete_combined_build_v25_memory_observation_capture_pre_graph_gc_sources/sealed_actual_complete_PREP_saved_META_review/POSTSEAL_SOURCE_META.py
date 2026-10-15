"""Full postseal EOF/SHA/7ID reread of the finite Source/small-META review package."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import stat

ROOT = Path(__file__).resolve().parent
LIMIT = 16 * 1024 * 1024

def identity(p):
    s = p.lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(p):
    p = Path(p)
    assert p.is_absolute() and p.resolve() == p
    before = identity(p)
    assert stat.S_ISREG(before[2]) and before[3] == 1 and 0 <= before[4] <= LIMIT
    fd = os.open(p, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        s = os.fstat(fd)
        assert [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns] == before
        with os.fdopen(fd, 'rb', buffering=0, closefd=False) as f:
            data = f.read(LIMIT + 1)
            assert len(data) <= LIMIT and len(data) == before[4] and f.read(1) == b''
        s = os.fstat(fd)
        assert [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns] == before
    finally:
        os.close(fd)
    assert identity(p) == before
    return dict(path=str(p),sha256=hashlib.sha256(data).hexdigest(),size_bytes=len(data),identity=before),data

def strict(data):
    def pairs(items):
        out = {}
        for key,value in items:
            assert key not in out
            out[key] = value
        return out
    def reject(value):
        raise ValueError(value)
    return json.loads(data,object_pairs_hook=pairs,parse_constant=reject)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--manifest-sha256', required=True)
    ap.add_argument('--fresh-postseal-report', required=True)
    args = ap.parse_args()
    mp, raw = pin(ROOT / 'MANIFEST.json')
    assert mp['sha256'] == args.manifest_sha256
    manifest = strict(raw)
    assert manifest['source_only'] is True
    files = {}
    dirs = {'.': identity(ROOT)}
    ast_count = 0
    for p in sorted(ROOT.rglob('*')):
        assert not p.is_symlink()
        rel = str(p.relative_to(ROOT))
        if stat.S_ISDIR(identity(p)[2]):
            dirs[rel] = identity(p)
        else:
            q,data = pin(p)
            files[rel] = q
            if p.suffix == '.py':
                ast.parse(data.decode('utf-8'),filename=str(p))
                ast_count += 1
            elif p.suffix == '.json':
                strict(data)
    assert set(files) == set(manifest['members']) | {'MANIFEST.json'}
    assert files['MANIFEST.json'] == mp and dirs == manifest['directories']
    assert all(files[rel] == q for rel,q in manifest['members'].items())
    assert ast_count == manifest['python_ast_count'] and len(files) == manifest['file_count']
    review = strict(pin(ROOT / 'REVIEW.json')[1])
    assert review['status'] == 'PASS_ACTUAL_COMPLETE_PREP_ONLY' and review['source_only'] is True and review['all_checks_typed_true'] is True and review['blockers'] == []
    assert len(review['checks']) == review['check_count'] == 31
    assert len({c['check'] for c in review['checks']}) == 31 and all(type(c['passed']) is bool and c['passed'] is True for c in review['checks'])
    assert files['REVIEW.json'] == manifest['review_pin']
    for rel,q in files.items():
        assert pin(ROOT / rel)[0] == q
    assert dirs == {rel:identity(ROOT if rel == '.' else ROOT / rel) for rel in dirs}
    destination = Path(args.fresh_postseal_report)
    assert destination.is_absolute() and destination.parent.resolve() == destination.parent and ROOT not in destination.parents
    report = dict(schema='INDEPENDENT_V25_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_FULL_POSTSEAL_V1',source_only=True,status='PASS_ACTUAL_COMPLETE_PREP_ONLY',manifest_pin=mp,review_pin=files['REVIEW.json'],all_package_members_full_EOF_SHA_7ID_unchanged=True,all_directory_7ID_unchanged=True,all_Source_AST_valid=True,files=files,directories=dirs,file_count=len(files),member_count=len(manifest['members']),python_ast_count=ast_count,original_saved_PREP_check_count=31,no_append_after_seal=True,candidate_or_genuine_guard_or_API_or_business_executed=False,new_science_qualification=False)
    with destination.open('xb') as f:
        f.write((json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
        f.flush()
        os.fsync(f.fileno())
    post_pin = pin(destination)[0]
    print(json.dumps(dict(schema=report['schema'],source_only=True,status=report['status'],manifest_pin=mp,review_pin=files['REVIEW.json'],postseal_report_pin=post_pin,file_count=len(files),member_count=len(manifest['members']),directory_count=len(dirs),python_ast_count=ast_count,all_package_members_full_EOF_SHA_7ID_unchanged=True,no_append_after_seal=True,candidate_or_genuine_guard_or_API_or_business_executed=False,new_science_qualification=False),ensure_ascii=False,sort_keys=True))

if __name__ == '__main__':
    main()
