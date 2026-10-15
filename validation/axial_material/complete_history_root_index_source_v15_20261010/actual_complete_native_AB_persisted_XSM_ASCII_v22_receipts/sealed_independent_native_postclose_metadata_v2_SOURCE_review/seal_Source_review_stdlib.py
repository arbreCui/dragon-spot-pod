"""Seal only this reviewer-owned Source package; no reviewed code is executed."""
import hashlib,json,stat
from pathlib import Path
P=Path(__file__).parent
def pin(p):
    s=p.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    assert p.is_absolute() and p.resolve()==p and stat.S_ISREG(before[2]) and before[3]==1
    with p.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
    t=p.lstat();after=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
    assert before==after
    return dict(path=str(p),sha256=digest,size_bytes=before[4],identity=before)
target=P/'MANIFEST.json'
assert not target.exists()
members={};directories=[]
for p in sorted(P.rglob('*')):
    s=p.lstat();assert not p.is_symlink()
    if stat.S_ISDIR(s.st_mode):directories.append(str(p.relative_to(P)))
    else:members[str(p.relative_to(P))]=pin(p)
report=json.loads((P/'REVIEW.json').read_text())
assert report['status']=='PASS_ROOT_NATIVE_POSTCLOSE_METADATA_SOURCE_ONLY'
assert report['all_checks_typed_true'] is True and report['blockers']==[]
assert report['check_count']==185
for q in report['complete_reviewed_input_pins'].values():assert pin(Path(q['path']))==q
for name,q in members.items():assert pin(P/name)==q
data=dict(schema='INDEPENDENT_ROOT_NATIVE_POSTCLOSE_META_V2_COMPLETE_SOURCE_PACKAGE_MANIFEST_V1',
    source_only=True,root=str(P),status=report['status'],members=members,
    member_count=len(members),member_bytes=sum(q['size_bytes'] for q in members.values()),
    directories=directories,manifest_excluded_from_own_members=True,
    true_actual_review_tool_return=members['actual_v2_Source_review_tool_return.json'],
    no_candidate_guard_native_numeric_executed=True,
    all_previous_source_gap_and_tool_returns_preserved=True)
with target.open('x') as f:json.dump(data,f,indent=2,allow_nan=False);f.write('\n')
assert set(str(p.relative_to(P)) for p in P.rglob('*') if p.is_file())==set(members)|{'MANIFEST.json'}
for name,q in members.items():assert pin(P/name)==q
print(json.dumps(dict(status='SEALED_COMPLETE_NATIVE_POSTCLOSE_META_V2_SOURCE_REVIEW_ONLY',
    manifest=pin(target),report=pin(P/'REVIEW.json'),member_count=len(members),
    member_bytes=data['member_bytes'],all_typed_checks_true=True,
    writer_pin=report['writer_pin'],installer_pin=report['installer_pin'],
    no_candidate_guard_native_numeric_executed=True)))
