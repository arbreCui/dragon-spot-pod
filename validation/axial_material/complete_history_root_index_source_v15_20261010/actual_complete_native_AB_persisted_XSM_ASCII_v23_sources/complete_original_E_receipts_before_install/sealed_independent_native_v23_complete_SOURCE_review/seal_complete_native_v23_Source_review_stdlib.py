"""Own Source package seal; reviewed binder/host/checker are never imported."""
import hashlib,json,stat
from pathlib import Path
R=Path(__file__).parent
def pin(p):
 s=p.lstat();a=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 assert p.resolve()==p and stat.S_ISREG(a[2])and a[3]==1
 with p.open('rb')as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 t=p.lstat();b=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
 assert a==b
 return dict(path=str(p),sha256=h,size_bytes=a[4],identity=a)
r=json.loads((R/'REVIEW.json').read_text())
assert r['schema']=='INDEPENDENT_COMPLETE_NATIVE_GENUINE_HOST_BINDER_SOURCE_REVIEW_V1'and r['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'and r['source_only']is True and r['all_checks_passed']is True and r['blockers']==[]
assert r['check_count']==len(r['checks'])==4528 and len({q['check']for q in r['checks']})==4528
assert all(type(q)is dict and set(q)=={'check','passed'}and type(q['check'])is str and q['check']and q['passed']is True for q in r['checks'])
for k in ('qualified_source_manifest','host_template','checker_template','binder'):assert pin(Path(r[k]['path']))==r[k]
for q in r['full_Source_META_reads'].values():assert pin(Path(q['path']))==q
members={}
for p in sorted(R.rglob('*')):
 assert not p.is_symlink()
 if p.is_file():members[str(p.relative_to(R))]=pin(p)
manifest=dict(schema='INDEPENDENT_COMPLETE_NATIVE_V23_SOURCE_REVIEW_PACKAGE_MANIFEST_V1',source_only=True,status=r['status'],members=members,member_count=len(members),member_bytes=sum(q['size_bytes']for q in members.values()),manifest_excluded_from_own_members=True,actual_source_review_terminal=members['actual_complete_Source_review_tool_return.json'],own_initial_failed_literal_expectation_and_true_tool_return_retained=True,no_candidate_guard_native_numeric_executed=True)
with (R/'MANIFEST.json').open('x')as f:json.dump(manifest,f,indent=2,allow_nan=False);f.write('\n')
for k,q in members.items():assert pin(R/k)==q
assert set(str(p.relative_to(R))for p in R.rglob('*')if p.is_file())==set(members)|{'MANIFEST.json'}
print(json.dumps(dict(status='SEALED_SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE',manifest=pin(R/'MANIFEST.json'),review=pin(R/'REVIEW.json'),member_count=len(members),member_bytes=manifest['member_bytes'],check_count=4528,four_role_pins_exact=True,no_candidate_guard_native_numeric_executed=True)))
