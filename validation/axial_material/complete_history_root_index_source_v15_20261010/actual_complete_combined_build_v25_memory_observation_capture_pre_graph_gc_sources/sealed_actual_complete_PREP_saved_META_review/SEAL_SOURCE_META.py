"""Seal the already executed saved-PREP review; Source/small-META only."""
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
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

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
    return dict(path=str(p), sha256=hashlib.sha256(data).hexdigest(), size_bytes=len(data), identity=before), data

def strict(data):
    def pairs(items):
        out = {}
        for key, value in items:
            assert key not in out
            out[key] = value
        return out
    def reject(value):
        raise ValueError(value)
    return json.loads(data, object_pairs_hook=pairs, parse_constant=reject)

def view():
    directories = {'.': identity(ROOT)}
    files = {}
    ast_count = 0
    for p in sorted(ROOT.rglob('*')):
        assert not p.is_symlink()
        rel = str(p.relative_to(ROOT))
        i = identity(p)
        if stat.S_ISDIR(i[2]):
            directories[rel] = i
        else:
            q, data = pin(p)
            files[rel] = q
            if p.suffix == '.py':
                ast.parse(data.decode('utf-8'), filename=str(p))
                ast_count += 1
            elif p.suffix == '.json' and data:
                strict(data)
    assert directories == {rel: identity(ROOT if rel == '.' else ROOT / rel) for rel in directories}
    for rel, q in files.items():
        assert pin(ROOT / rel)[0] == q
    return files, directories, ast_count

def main():
    review_pin, raw = pin(ROOT / 'REVIEW.json')
    review = strict(raw)
    assert review['schema'] == 'INDEPENDENT_V25_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_V1'
    assert review['status'] == 'PASS_ACTUAL_COMPLETE_PREP_ONLY'
    assert review['source_only'] is True and review['all_checks_typed_true'] is True and review['blockers'] == []
    checks = review['checks']
    assert type(review['check_count']) is int and review['check_count'] == len(checks) == 31
    assert len({c['check'] for c in checks}) == 31
    assert all(type(c['passed']) is bool and c['passed'] is True for c in checks)
    assert review['new_reviewer_business_or_API_execution'] is False
    for name in ('whole_combined_build_qualified','whole_combined_INPUT_admitted','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','goal_complete'):
        assert review[name] is False
    receipt = strict(pin(ROOT / 'ACTUAL_REVIEW_TOOL_TERMINAL_RETURN.json')[1])
    terminal = receipt['terminal_tool_return']
    assert receipt['closed'] is True and receipt['observed_terminal'] is True and receipt['session_repolled_after_close'] is False
    assert type(terminal['exit_code']) is int and terminal['exit_code'] == 0 and 'session_id' not in terminal
    observed = strict(terminal['output'])
    assert observed['review_pin'] == review_pin and observed['check_count'] == 31 and observed['blockers'] == []
    adaptation = strict(pin(ROOT / 'METHOD_PROVENANCE/ADAPTATION.json')[1])
    current = pin(ROOT / 'REVIEWER_EXECUTED_SOURCE.py')[1]
    original = pin(ROOT / 'METHOD_PROVENANCE/ORIGINAL_P4_ACTUAL_31_REVIEWER_SOURCE.byte_exact.py')[1]
    inverse = current.decode('utf-8')
    for h in reversed(adaptation['finite_hunks']):
        assert inverse.count(h['new']) == h['count']
        inverse = inverse.replace(h['new'], h['old'])
    assert inverse.encode('utf-8') == original
    assert ast.dump(ast.parse(inverse), include_attributes=False) == ast.dump(ast.parse(original), include_attributes=False)
    assert hashlib.sha256(current).hexdigest() == adaptation['current_Source']['sha256']
    assert hashlib.sha256(original).hexdigest() == adaptation['original_Source']['sha256']
    manifest = ROOT / 'MANIFEST.json'
    with manifest.open('xb') as f:
        f.flush()
        os.fsync(f.fileno())
    files, directories, ast_count = view()
    members = {rel: q for rel, q in files.items() if rel != 'MANIFEST.json'}
    body = dict(schema='INDEPENDENT_V25_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_SOURCE_META_MANIFEST_V1',source_only=True,status='PASS_ACTUAL_COMPLETE_PREP_ONLY',root=str(ROOT),member_count=len(members),file_count=len(members)+1,directory_count=len(directories),python_ast_count=ast_count,members=members,directories=directories,review_pin=review_pin,executed_review_chunk=terminal['chunk_id'],new_business_or_science_execution=False)
    with manifest.open('wb') as f:
        f.write((json.dumps(body,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
        f.flush()
        os.fsync(f.fileno())
    actual, after_dirs, after_ast = view()
    assert after_dirs == directories and after_ast == ast_count and set(actual) == set(members) | {'MANIFEST.json'}
    assert all(actual[rel] == q for rel,q in members.items()) and actual['REVIEW.json'] == review_pin
    manifest_pin = actual['MANIFEST.json']
    assert strict(pin(manifest)[1]) == body
    print(json.dumps(dict(schema='INDEPENDENT_V25_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_SOURCE_META_SEAL_V1',source_only=True,status=review['status'],manifest_pin=manifest_pin,review_pin=review_pin,member_count=len(members),file_count=len(actual),directory_count=len(directories),python_ast_count=ast_count,check_count=31,blockers=[],actual_review_chunk=terminal['chunk_id'],candidate_or_genuine_guard_or_API_or_business_executed=False,new_science_qualification=False),ensure_ascii=False,sort_keys=True))

if __name__ == '__main__':
    main()
