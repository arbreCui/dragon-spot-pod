import hashlib,json,stat
from pathlib import Path
P=Path(__file__).parent
DESIGN=Path('/private/tmp/axmat_v25_monitor_access_directory_Source_independent_review_UNREADY_k67d42sg')
def ids(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 i=ids(p);assert stat.S_ISREG(i[2]) and i[3]==1 and not p.is_symlink()
 with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 assert ids(p)==i;return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
def copy(p,q):
 before=pin(p);assert not q.exists();q.write_bytes(p.read_bytes());after=pin(q)
 assert pin(p)==before and (after['sha256'],after['size_bytes'])==(before['sha256'],before['size_bytes'])
 return dict(original=before,saved=after)
r=json.loads((P/'REVIEW.json').read_bytes())
assert r['schema']=='INDEPENDENT_V25_ACTUAL_BOUND_COMPLETE_PREP_SOURCE_REVIEW_V1' and r['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_BUSINESS_QUALIFICATION'
assert r['source_only'] is True and r['all_checks_typed_true'] is True and r['blockers']==[]
assert type(r['check_count']) is int and r['check_count']==len(r['checks'])==1445 and all(type(c['passed']) is bool and c['passed'] is True for c in r['checks'])
t=json.loads((P/'ACTUAL_SOURCE_REVIEW_TOOL_RETURN.json').read_bytes());a=t['actual_tool_return']
assert t['closed'] is True and a['chunk_id']=='8e65fa' and type(a['exit_code']) is int and a['exit_code']==0 and 'session_id' not in a
out=json.loads(a['output']);assert out['review']==str(P/'REVIEW.json') and out['check_count']==1445 and out['qualified_bound_manifest_pin']==r['qualified_bound_manifest_pin'] and out['qualified_role_Source_pins']==r['qualified_role_Source_pins']
for v in r['complete_full_EOF_Source_META_pins']:assert pin(Path(v['path']))==v
for k in ('actual_NEW_PREP_terminal','actual_NEW_PREP_summary','actual_NEW_metadatawriter_terminal','actual_NEW_BUILD_terminal'):assert r[k] is None
for k in ('new_business_or_science_qualification_created','whole_build_qualified','whole_INPUT_admitted','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','goal_complete'):assert r[k] is False
assert pin(DESIGN/'review_directory_isolation_Source_stdlib.UNREADY.py')['sha256']=='15bbeb237b0706eb11573bd406561ab8022aa6e5a3fff191b423cd153ee1e610'
assert pin(DESIGN/'ACTUAL_CLOSED_SOURCE_INPUTS.json')['sha256']=='afe6c1c36831ea6cc86cf23ef74de1aa5514140b387fe527a1eea5d737c05bb9'
copies={}
for n in ('review_directory_isolation_Source_stdlib.UNREADY.py','ACTUAL_CLOSED_SOURCE_INPUTS.json','write_actual_Source_review_inputs_stdlib.py'):copies[n]=copy(DESIGN/n,P/n)
for k,v in {**r['qualified_role_Source_pins'],'prelaunch':r['qualified_prelaunch_Source_pin'],'installer':r['qualified_Source_installer_pin'],'E_snapshot':r['qualified_E_snapshot_Source_pin']}.items():
 assert pin(Path(v['path']))==v;copies[k]=copy(Path(v['path']),P/('REVIEWED_'+k+'.py'))
for k,v in {'BOUND_MANIFEST.json':r['qualified_bound_manifest_pin'],'ROOT_COMPLETE_DIRECTORY_SOURCE_INVERSE.json':r['actual_Root_Source_inverse_pin']}.items():
 assert pin(Path(v['path']))==v;copies[k]=copy(Path(v['path']),P/k)
(P/'COMPLETE_FINITE_SOURCE_COPIES.json').write_text(json.dumps(copies,indent=2,allow_nan=False)+'\n')
root=Path(r['qualified_bound_manifest_pin']['path']).parent;rm=json.loads((root/'MANIFEST.json').read_bytes())
assert {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}==set(rm['members'])|{'MANIFEST.json'}
for n,v in rm['members'].items():assert pin(root/n)==v
assert {'.':ids(root),**{str(p.relative_to(root)):ids(p) for p in root.rglob('*') if p.is_dir()}}==rm['directories']
assert pin(root/'MANIFEST.json')==r['qualified_bound_manifest_pin']
mp=P/'MANIFEST.json';mp.touch(exist_ok=False)
files={str(p.relative_to(P)):pin(p) for p in sorted(P.rglob('*')) if p.is_file() and p!=mp};dirs={'.':ids(P),**{str(p.relative_to(P)):ids(p) for p in P.rglob('*') if p.is_dir()}}
m=dict(schema='INDEPENDENT_V25_ACTUAL_BOUND_COMPLETE_PREP_SOURCE_REVIEW_SEALED_PACKAGE_V1',qualification_scope=r['qualification_scope'],source_only=True,members=files,directories=dirs,member_count=len(files),complete_member_bytes=sum(v['size_bytes'] for v in files.values()),candidate_helper_guard_API_compiler_or_numeric_executed=False,new_PREP_or_BUILD_or_science_qualification_created=False)
mp.write_text(json.dumps(m,indent=2,allow_nan=False)+'\n')
for n,v in files.items():assert pin(P/n)==v
assert ids(P)==dirs['.']
print(json.dumps(dict(source_only=True,status='SEALED_SOURCE_ONLY_PASS_NO_EXECUTION_OR_BUSINESS_QUALIFICATION',manifest_pin=pin(mp),review_pin=pin(P/'REVIEW.json'),check_count=r['check_count'],member_count=len(files),complete_member_bytes=m['complete_member_bytes'],qualified_bound_manifest_pin=r['qualified_bound_manifest_pin'],candidate_helper_guard_API_compiler_or_numeric_executed=False)))
