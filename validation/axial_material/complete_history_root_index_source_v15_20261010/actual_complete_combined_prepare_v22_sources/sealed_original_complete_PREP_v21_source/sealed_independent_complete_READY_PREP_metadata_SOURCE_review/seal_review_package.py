"""Seal this finite SOURCE/META independent review, using standard library only."""
from pathlib import Path
import hashlib
import json
import stat

ROOT = Path(__file__).parent

def pin(path):
    s = path.lstat()
    before = [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]
    if not stat.S_ISREG(s.st_mode) or s.st_nlink != 1:
        raise ValueError('ordinary review SOURCE/META file required')
    with path.open('rb') as f:
        raw = f.read()
        if f.read(1) != b'':
            raise ValueError('EOF required')
    t = path.lstat()
    after = [t.st_dev, t.st_ino, t.st_mode, t.st_nlink, t.st_size, t.st_mtime_ns, t.st_ctime_ns]
    if after != before or len(raw) != s.st_size:
        raise ValueError('immutable full SOURCE/META file required')
    return {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'size_bytes': len(raw), 'identity': before}

review = json.loads((ROOT/'REVIEW.json').read_text())
actual = json.loads((ROOT/'actual_source_review_tool_return.json').read_text())
tr = actual['terminal_tool_return']
if actual['closed'] is not True or actual['actual_tool_terminal_return_observed'] is not True or type(tr['exit_code']) is not int or tr['exit_code'] != 0 or 'session_id' in tr or tr['chunk_id'] != '98ab26':
    raise ValueError('actual independent typed EXIT0 closed terminal required')
printed = json.loads(tr['output'])
if printed['REVIEW_sha256'] != pin(ROOT/'REVIEW.json')['sha256'] or printed['checks'] != len(review['checks']) or review['blockers'] != [] or review['all_checks_typed_true'] is not True or any(c['value'] is not True for c in review['checks']):
    raise ValueError('whole actual Source result required')
names = ['REVIEW.json', 'REPORT.txt', 'review_script.py', 'actual_source_review_tool_return.json', 'seal_review_package.py']
if sorted(p.name for p in ROOT.iterdir()) != sorted(names):
    raise ValueError('finite review package exact inventory required')
members = {name: pin(ROOT/name) for name in names}
manifest = {'schema': 'FINITE_V21_COMPLETE_READY_INDEPENDENT_SOURCE_REVIEW_SEAL_V1', 'status': review['status'], 'review_package': str(ROOT), 'members_excluding_manifest': len(members), 'member_bytes_excluding_manifest': sum(p['size_bytes'] for p in members.values()), 'files': members, 'actual_independent_Source_terminal_chunk': tr['chunk_id'], 'actual_independent_Source_exit_code': tr['exit_code'], 'actual_independent_Source_closed': True, 'all_source_checks_typed_true': True, 'blockers': [], 'complete_fixed_source_package': review['reviewed_outer_manifest'], 'scope': review['scope'], 'source_qualification_only': True, 'actual_PREP_build_INPUT_native_AAA_ABA_physics_qualified': False}
with (ROOT/'sealed_manifest.json').open('x') as f:
    json.dump(manifest, f, indent=2, allow_nan=False)
    f.write('\n')
for name, before in members.items():
    if pin(ROOT/name) != before:
        raise ValueError('review member changed during Source seal')
print(json.dumps({'status': manifest['status'], 'manifest': pin(ROOT/'sealed_manifest.json'), 'actual_Source_review_exit_code': tr['exit_code'], 'actual_Source_review_chunk': tr['chunk_id'], 'checks': len(review['checks']), 'blockers': [], 'actual_candidate_or_business_executed': False}))
