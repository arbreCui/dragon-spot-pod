import hashlib,json,os,stat
from pathlib import Path
P=Path(__file__).parent
def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 before=identity(p);assert stat.S_ISREG(before[2])and not p.is_symlink()
 with p.open('rb')as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 assert identity(p)==before
 return dict(path=str(p),sha256=h,size_bytes=before[4],identity=before)
def copy(src,dest):
 before=pin(src);assert not dest.exists();dest.write_bytes(src.read_bytes());saved=pin(dest)
 assert pin(src)==before and saved['sha256']==before['sha256']and saved['size_bytes']==before['size_bytes']
 return dict(original=before,saved=saved)
r=json.loads((P/'REVIEW.json').read_bytes());assert r['source_only']is True and r['all_checks_typed_true']is True and r['blockers']==[] and type(r['check_count'])is int and r['check_count']==len(r['checks'])==79
assert len({c['check']for c in r['checks']})==79 and all(type(c['passed'])is bool and c['passed']is True for c in r['checks'])
t=json.loads((P/'ACTUAL_SOURCE_REVIEW_TOOL_RETURNS.json').read_bytes());a=t['actual_success_tool_return'];assert a['chunk_id']=='e05fe6'and type(a['exit_code'])is int and a['exit_code']==0 and'session_id'not in a
v=json.loads(a['output']);assert v['review_pin']==pin(P/'REVIEW.json')and v['qualified_template_manifest_pin']==r['qualified_template_manifest_pin']and v['qualified_role_Source_pins']==r['qualified_role_Source_pins']
pairs={}
for role,sourcepin in r['qualified_role_Source_pins'].items():
 src=Path(sourcepin['path']);assert pin(src)==sourcepin;pairs['reviewed_'+role+'.py']=copy(src,P/('reviewed_'+role+'.py'))
source_root=Path(r['qualified_template_manifest_pin']['path']).parent
for n in ['MANIFEST.json','COMPLETE_SOURCE_INVERSES.json','COMPLETE_SOURCE_BINDER_INVERSES.json','INDEPENDENT_SOURCE_PEER_REQUIRED_CONTRACT.UNREADY.json','ROOT_BINDING_SOURCE_CONSTANTS.json']:
 pairs['AUTHOR_'+n]=copy(source_root/n,P/('AUTHOR_'+n))
for n in ['ACTUAL_SOURCE_SEAL_TOOL_RETURN.json','ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json']:
 pairs['AUTHOR_'+n]=copy(source_root.with_name(source_root.name+'_seal_receipt')/n,P/('AUTHOR_'+n))
for label,k in [('Root_optional_installer.py','optional_Root_installer_Source_pin'),('Root_optional_prelaunch.py','optional_Root_prelaunch_Source_pin')]:
 src=Path(r[k]['path']);assert pin(src)==r[k];pairs[label]=copy(src,P/label)
pairs['Root_optional_prelaunch_inverse.json']=copy(Path('/private/tmp/spot_v25_complete_PREP_prelaunch_ROOT_FULL_SOURCE_inverse.json'),P/'Root_optional_prelaunch_inverse.json')
(P/'COMPLETE_FINITE_SOURCE_COPIES.json').write_text(json.dumps(pairs,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
# The original author's entire sealed namespace is verified before and after finite copies.
assert pin(source_root/'MANIFEST.json')==r['qualified_template_manifest_pin']
actualfiles={str(x.relative_to(source_root)):pin(x)for x in source_root.rglob('*')if x.is_file()};actualdirs={'.':identity(source_root),**{str(x.relative_to(source_root)):identity(x)for x in source_root.rglob('*')if x.is_dir()}}
assert dict(files=actualfiles,directories=actualdirs)==r['complete_author_package_before_after_pin_inventory']
mp=P/'MANIFEST.json';mp.touch(exist_ok=False)
files={str(x.relative_to(P)):pin(x)for x in sorted(P.rglob('*'))if x.is_file()and x!=mp};dirs={'.':identity(P),**{str(x.relative_to(P)):identity(x)for x in sorted(P.rglob('*'))if x.is_dir()}}
m=dict(schema='INDEPENDENT_V25_COMPLETE_CANONICAL_TRUE_SOURCE_REVIEW_SEALED_PACKAGE_V1',source_only=True,members=files,directories=dirs,member_count=len(files),complete_member_bytes=sum(x['size_bytes']for x in files.values()),qualified_template_manifest_pin=r['qualified_template_manifest_pin'],candidate_helper_guard_API_compiler_or_numeric_executed=False)
mp.write_text(json.dumps(m,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
for n,v in files.items():assert pin(P/n)==v
assert identity(P)==dirs['.']
print(json.dumps(dict(source_only=True,status='SEALED_SOURCE_ONLY_PASS_NO_EXECUTION_OR_BUSINESS_QUALIFICATION',manifest_pin=pin(mp),review_pin=pin(P/'REVIEW.json'),check_count=79,member_count=len(files),complete_member_bytes=m['complete_member_bytes'],qualified_template_manifest_pin=r['qualified_template_manifest_pin'],candidate_helper_guard_API_compiler_or_numeric_executed=False)))
