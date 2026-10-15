"""Stdlib complete independent SOURCE/META seal; never run reviewed code."""
from pathlib import Path
import hashlib,json,stat
P=Path(__file__).parent
def identity(path):
 s=path.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
 a=identity(path);assert stat.S_ISREG(a[2]) and a[3]==1 and not path.is_symlink()
 b=path.read_bytes();assert a==identity(path) and len(b)==a[4]
 return dict(path=str(path),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=a)
r=json.loads((P/'REVIEW.json').read_bytes())
assert r['schema']=='INDEPENDENT_PRIVATE_INACTIVE_AUDIT_COMPLETE_QUALIFICATION_SOURCE_REVIEW_V1'
assert r['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_QUALIFICATION'
assert r['source_only'] is True and r['all_checks_typed_true'] is True and r['blockers']==[]
assert type(r['check_count']) is int and r['check_count']==len(r['checks'])==1122
assert len({x['check'] for x in r['checks']})==len(r['checks'])
assert all(type(x['passed']) is bool and x['passed'] is True for x in r['checks'])
assert r['qualified_helper_candidate_SHA']=='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'
assert r['new_actual_helper_qualification'] is None and r['six_future_business_pins']==[None]*6
assert pin(Path(r['qualified_template_manifest_pin']['path']))==r['qualified_template_manifest_pin']
assert all(pin(Path(v['path']))==v for v in r['qualified_template_Source_pins'].values())
tool=json.loads((P/'inactive_complete_Source_review_first_actual.json').read_bytes())
assert tool['closed'] is True and tool['actual_tool_terminal_return_observed'] is True
t=tool['actual_tool_return'];assert type(t['exit_code']) is int and t['exit_code']==0 and 'session_id' not in t
actual=json.loads(t['output']);assert actual['review_dir']==str(P) and actual['review_sha256']==pin(P/'REVIEW.json')['sha256'] and actual['check_count']==1122
out=P/'MANIFEST.json';assert not out.exists();out.write_bytes(b'')
root=identity(P);members=[pin(f) for f in sorted(P.rglob('*')) if f.is_file() and f!=out]
directories={str(f.relative_to(P)):identity(f) for f in sorted(P.rglob('*')) if f.is_dir()}
assert not any(f.is_symlink() for f in P.rglob('*'))
manifest=dict(schema='INDEPENDENT_COMPLETE_PRIVATE_INACTIVE_AUDIT_QUALIFICATION_SOURCE_REVIEW_SEAL_V1',source_only=True,
 status='SEALED_SOURCE_ONLY_PASS_NO_EXECUTION_OR_QUALIFICATION',members=members,member_count=len(members),
 complete_member_bytes=sum(v['size_bytes'] for v in members),directories=directories,package_root_identity=root,
 qualified_source_report_pin=pin(P/'REVIEW.json'),actual_Source_review_tool_receipt_pin=pin(P/'inactive_complete_Source_review_first_actual.json'),
 qualified_original_template_manifest_pin=r['qualified_template_manifest_pin'],qualified_helper_candidate_SHA=r['qualified_helper_candidate_SHA'],
 new_actual_helper_qualification=None,six_future_business_pins=[None]*6,
 Source_candidate_helper_controller_guard_API_binder_or_numeric_executed=False)
out.write_text(json.dumps(manifest,indent=2,allow_nan=False)+'\n')
assert root==identity(P)
assert [pin(Path(x['path'])) for x in members]==members
assert {str(f.relative_to(P)):identity(f) for f in P.rglob('*') if f.is_dir()}==directories
assert len([f for f in P.rglob('*') if f.is_file()])==len(members)+1
print(json.dumps(dict(source_only=True,status=manifest['status'],manifest_pin=pin(out),review_pin=pin(P/'REVIEW.json'),
 actual_Source_review_tool_receipt_pin=pin(P/'inactive_complete_Source_review_first_actual.json'),member_count=len(members),
 full_file_count=len(members)+1,directory_count=len(directories),check_count=1122,all_checks_typed_true=True,
 new_actual_helper_qualification=None),separators=(',',':')))
