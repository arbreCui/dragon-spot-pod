import hashlib,json,stat
from pathlib import Path
P=Path(__file__).parent
def ids(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 i=ids(p);assert stat.S_ISREG(i[2])and not p.is_symlink()
 with p.open('rb')as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 assert ids(p)==i;return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
def copy(p,q):
 before=pin(p);assert not q.exists();q.write_bytes(p.read_bytes());after=pin(q);assert pin(p)==before and (after['sha256'],after['size_bytes'])==(before['sha256'],before['size_bytes']);return dict(original=before,saved=after)
r=json.loads((P/'REVIEW.json').read_bytes());assert r['source_only']is True and r['all_checks_typed_true']is True and r['blockers']==[] and type(r['check_count'])is int and r['check_count']==len(r['checks'])==41 and len({c['check']for c in r['checks']})==41 and all(type(c['passed'])is bool and c['passed']is True for c in r['checks'])
t=json.loads((P/'ACTUAL_SOURCE_REVIEW_TOOL_RETURNS.json').read_bytes());a=t['actual_success_tool_return'];assert a['chunk_id']=='d88ece'and type(a['exit_code'])is int and a['exit_code']==0 and'session_id'not in a
out=json.loads(a['output']);assert out['review_pin']==pin(P/'REVIEW.json')and out['qualified_bound_manifest_pin']==r['qualified_bound_manifest_pin']and out['qualified_role_Source_pins']==r['qualified_role_Source_pins']
root=Path(r['qualified_bound_manifest_pin']['path']).parent;copies={}
for role,wanted in r['qualified_role_Source_pins'].items():
 src=Path(wanted['path']);assert pin(src)==wanted;copies[role]=copy(src,P/('REVIEWED_'+role+'.py'))
for n in ['MANIFEST.json','Root_actual_Q_bound_complete_PREP_Source_inverse.json']:copies[n]=copy(root/n,P/('BOUND_'+n))
copies['actual_Root_binding_receipt']=copy(Path(r['actual_Root_binding_terminal_pin']['path']),P/'ACTUAL_ROOT_SOURCE_BINDING_TOOL_RETURN.json')
(P/'COMPLETE_FINITE_SOURCE_COPIES.json').write_text(json.dumps(copies,indent=2,allow_nan=False)+'\n')
assert pin(root/'MANIFEST.json')==r['qualified_bound_manifest_pin']
assert {str(p.relative_to(root)):pin(p)for p in root.rglob('*')if p.is_file()}==r['actual_bound_namespace_before_after']['files']
assert {'.':ids(root),**{str(p.relative_to(root)):ids(p)for p in root.rglob('*')if p.is_dir()}}==r['actual_bound_namespace_before_after']['directories']
mp=P/'MANIFEST.json';mp.touch(exist_ok=False);files={str(p.relative_to(P)):pin(p)for p in sorted(P.rglob('*'))if p.is_file()and p!=mp};dirs={'.':ids(P),**{str(p.relative_to(P)):ids(p)for p in P.rglob('*')if p.is_dir()}}
m=dict(schema='INDEPENDENT_V25_ACTUAL_BOUND_COMPLETE_PREP_SOURCE_REVIEW_SEALED_PACKAGE_V1',source_only=True,members=files,directories=dirs,member_count=len(files),complete_member_bytes=sum(v['size_bytes']for v in files.values()),candidate_helper_guard_API_compiler_or_numeric_executed=False)
mp.write_text(json.dumps(m,indent=2,allow_nan=False)+'\n')
for n,v in files.items():assert pin(P/n)==v
assert ids(P)==dirs['.']
print(json.dumps(dict(source_only=True,status='SEALED_SOURCE_ONLY_PASS_NO_EXECUTION_OR_BUSINESS_QUALIFICATION',manifest_pin=pin(mp),review_pin=pin(P/'REVIEW.json'),check_count=41,member_count=len(files),complete_member_bytes=m['complete_member_bytes'],qualified_bound_manifest_pin=r['qualified_bound_manifest_pin'],candidate_helper_guard_API_compiler_or_numeric_executed=False)))
