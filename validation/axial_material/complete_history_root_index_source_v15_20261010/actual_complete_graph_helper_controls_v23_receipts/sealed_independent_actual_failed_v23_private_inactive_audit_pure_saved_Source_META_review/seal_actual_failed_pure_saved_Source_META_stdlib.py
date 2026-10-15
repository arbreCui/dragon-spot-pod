"""Seal complete small failure review only; no reviewed module imports."""
from pathlib import Path
import hashlib,json,stat
P=Path(__file__).parent
def ident(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 a=ident(p);assert stat.S_ISREG(a[2]) and a[3]==1 and not p.is_symlink();r=p.read_bytes();assert a==ident(p) and len(r)==a[4]
 return dict(path=str(p),sha256=hashlib.sha256(r).hexdigest(),size_bytes=len(r),identity=a)
r=json.loads((P/'REVIEW.json').read_bytes())
assert r['schema']=='INDEPENDENT_V23_ACTUAL_FAILED_PRIVATE_INACTIVE_AUDIT_PURE_SAVED_SOURCE_META_REVIEW_V1'
assert r['status']=='PASS_SAVED_ACTUAL_PURE_CONTROLS_FAILURE_EVIDENCE_ONLY'
assert r['all_checks_typed_true'] is True and r['blockers']==[] and r['check_count']==len(r['checks'])==2922
assert len({x['check'] for x in r['checks']})==len(r['checks']) and all(type(x['passed']) is bool and x['passed'] is True for x in r['checks'])
assert r['actual_terminal_exit_code']==1 and r['actual_original_session']==11505
assert r['actual_pure_protocol_qualified'] is False and r['FreshV23_executed'] is False and r['new_actual_helper_qualification'] is None
assert r['original_HOD_bytes']==24976999 and r['Root_writer_time_HODE_bytes']==26707846 and r['current_HODE_bytes']==26710174
t=json.loads((P/'ACTUAL_REVIEWER_TOOL_RETURNS/inactive_pure_failed_saved_META_actual_review.json').read_bytes())
v=t['actual_tool_return'];assert type(v['exit_code']) is int and v['exit_code']==0 and 'session_id' not in v and t['closed'] is True and t['actual_tool_terminal_return_observed'] is True
actual=json.loads(v['output']);assert actual['review_dir']==str(P) and actual['review_sha256']==pin(P/'REVIEW.json')['sha256'] and actual['check_count']==2922
mp=P/'MANIFEST.json';assert not mp.exists();mp.write_bytes(b'');root=ident(P)
members=[pin(p) for p in sorted(P.rglob('*')) if p.is_file() and p!=mp]
dirs={p.relative_to(P).as_posix():ident(p) for p in sorted(P.rglob('*')) if p.is_dir()}
assert not any(p.is_symlink() for p in P.rglob('*'))
m=dict(schema='INDEPENDENT_V23_ACTUAL_FAILED_PURE_SAVED_SOURCE_META_REVIEW_SEAL_V1',source_and_saved_META_only=True,
 status='SEALED_ACTUAL_FAILED_PURE_EVIDENCE_ONLY_NO_QUALIFICATION',members=members,member_count=len(members),
 complete_member_bytes=sum(p['size_bytes'] for p in members),directories=dirs,package_root_identity=root,
 report_pin=pin(P/'REVIEW.json'),reviewer_actual_tool_receipt_pin=pin(P/'ACTUAL_REVIEWER_TOOL_RETURNS/inactive_pure_failed_saved_META_actual_review.json'),
 actual_Root_failure_exit_code=1,new_actual_helper_qualification=None,reviewer_candidate_helper_guard_API_numeric_or_business_executed=False)
mp.write_text(json.dumps(m,indent=2,allow_nan=False)+'\n')
assert ident(P)==root and [pin(Path(v['path'])) for v in members]==members
assert {p.relative_to(P).as_posix():ident(p) for p in P.rglob('*') if p.is_dir()}==dirs
assert len([p for p in P.rglob('*') if p.is_file()])==len(members)+1
print(json.dumps(dict(source_and_saved_META_only=True,status=m['status'],manifest_pin=pin(mp),review_pin=pin(P/'REVIEW.json'),member_count=len(members),full_file_count=len(members)+1,directory_count=len(dirs),check_count=2922,actual_Root_failure_exit_code=1,new_actual_helper_qualification=None),separators=(',',':')))
