from pathlib import Path
import hashlib,json,shutil,stat,tempfile
CORE=Path('/private/tmp/axmat_INDEPENDENT_N4_complete_OS_tool_role_Source_review_va2y57jp');N=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_role_limited_OS_tools_N4_UNREADY_Source_3gnnt2it');S=Path(str(N)+'_seal_receipt')
Q=Path(tempfile.mkdtemp(prefix='axmat_INDEPENDENT_N4_full_Source_review_FINAL_',dir='/private/tmp'))
def pin(p):
 p=Path(p);s=p.lstat();i=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns];assert p.resolve()==p and stat.S_ISREG(s.st_mode)and s.st_nlink==1
 with p.open('rb')as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 t=p.lstat();assert i==[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns];return dict(path=str(p),sha256=h,size_bytes=s.st_size,identity=i)
def read(p):
 before=pin(p);d=json.loads(Path(p).read_text());assert pin(p)==before;return d,before
r,rp=read(CORE/'REVIEW.json');truth,tp=read(CORE/'ACTUAL_CORE_REVIEW_TOOL_RETURN.json');tr=truth['terminal_tool_return']
assert tr['chunk_id']=='b1fe99'and type(tr['exit_code'])is int and tr['exit_code']==0 and 'session_id'not in tr and truth['closed']is True and truth['observed_terminal']is True and json.loads(tr['output'])['review_pin']==rp
assert r['check_count']==60 and r['all_checks_passed']is True and r['blockers']==[]
# Preserve whole reviewed N4 Source once and exact finite previous review histories.
for p in sorted(CORE.rglob('*')):
 rel=p.relative_to(CORE);dest=Q/rel
 if p.is_dir():dest.mkdir(parents=True,exist_ok=True)
 else:
  assert not p.is_symlink();before=pin(p);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest);assert pin(dest)['sha256']==before['sha256']
(Q/'REVIEW.json').rename(Q/'CORE_REVIEW.byte_exact.json')
proofs={}
for name in ('ACTUAL_SOURCE_SEAL_TOOL_RETURN.json','ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json','FULL_SOURCE_POSTSEAL_VERIFICATION.json'):
 m,p=read(S/name);proofs[name]=dict(fullpin=p,contents=m)
 target=Q/'ACTUAL_ORIGINAL_N4_AUTHOR_TRUE_SEAL_PROVENANCE'/name;target.parent.mkdir(exist_ok=True);shutil.copyfile(p['path'],target)
checks=r['checks'];blockers=r['blockers']
def check(k,value):
 assert type(value)is bool and k not in {x['check']for x in checks};checks.append(dict(check=k,passed=value))
 if not value:blockers.append(dict(check=k,detail='genuine author seal or Source review terminal coupling'))
for name,chunk in (('ACTUAL_SOURCE_SEAL_TOOL_RETURN.json','6c61f5'),('ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json','3784ef')):
 m=proofs[name]['contents'];t=m['terminal_tool_return'];out=json.loads(t['output'])
 check('genuine original N4 author '+chunk+' exact closed intzero and complete current manifest SHA7ID coupling',m['closed']is True and m['observed_terminal']is True and m['session_repolled_after_close']is False and type(t['exit_code'])is int and t['exit_code']==0 and t['chunk_id']==chunk and 'session_id'not in t and m['actual_terminal_chunk']==chunk and out['manifest_pin']==pin(N/'MANIFEST.json'))
v=proofs['FULL_SOURCE_POSTSEAL_VERIFICATION.json']['contents'];po=json.loads(proofs['ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json']['contents']['terminal_tool_return']['output'])
check('genuine original author postseal full98files13dirs Source verification and true seal proof exact coupling',v['all97members_full_EOF_SHA7ID_verified']is True and v['all13directories_full7ID_verified']is True and v['original_N3_full81files_unchanged']is True and v['manifest_pin']==pin(N/'MANIFEST.json')and po['postseal_verification_pin']==proofs['FULL_SOURCE_POSTSEAL_VERIFICATION.json']['fullpin']and po['actual_seal_tool_return_pin']==proofs['ACTUAL_SOURCE_SEAL_TOOL_RETURN.json']['fullpin'])
check('actual complete independent core Source b1fe99 typed zero observed terminal full report coupling',truth['source_only']is True and truth['closed']is True and truth['observed_terminal']is True and json.loads(tr['output'])['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'and json.loads(tr['output'])['review_pin']==rp)
r['evidence']['actual_complete_core_Source_review_pin']=rp;r['evidence']['actual_complete_core_Source_review_tool_return_pin']=tp;r['evidence']['complete_original_N4_author_true_seal_proofs']=proofs
r['check_count']=len(checks);r['all_checks_passed']=r['all_checks_typed_true']=not blockers and all(type(c['passed'])is bool and c['passed']is True for c in checks);r['status']='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'if not blockers else'BLOCKED_SOURCE_ONLY_NO_EXECUTION_OR_SCIENCE'
r['complete_reviewed_source_namespace_after']=r['complete_reviewed_source_namespace_before']
for name,p in r['complete_reviewed_source_namespace_after']['files'].items():assert pin(N/name)==p
for name,i in r['complete_reviewed_source_namespace_after']['directories'].items():
 s=(N/name).lstat();assert i==[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
with (Q/'REVIEW.json').open('x')as f:json.dump(r,f,indent=2,allow_nan=False);f.write('\n')
shutil.copyfile(__file__,Q/'FINAL_INDEPENDENT_SOURCE_SEAL_COUPLING_ADDON.py')
print(json.dumps(dict(source_only=True,status=r['status'],check_count=r['check_count'],all_checks_typed_true=r['all_checks_typed_true'],blockers=blockers,final_package=str(Q),review_pin=pin(Q/'REVIEW.json'),all_current_N4_author14_role_pins=r['actual_author_Source_contract'],candidate_or_guard_or_native_compiler_or_material_executed=False)))
