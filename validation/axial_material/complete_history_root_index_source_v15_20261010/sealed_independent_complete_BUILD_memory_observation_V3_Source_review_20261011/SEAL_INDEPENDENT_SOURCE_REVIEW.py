import ast,hashlib,json,os,stat
from pathlib import Path
D=Path('/private/tmp/axmat_V25_memory_observation_V3_INDEPENDENT_review_2FVRNl')
S=D.with_name(D.name+'_seal_receipt')
def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);before=ident(p.lstat());assert stat.S_ISREG(before[2]) and before[3]==1 and 0<=before[4]<=1048576
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  assert ident(os.fstat(fd))==before;h=hashlib.sha256();total=0
  while True:
   b=os.read(fd,65536)
   if not b:break
   h.update(b);total+=len(b)
  assert total==before[4] and os.read(fd,1)==b'' and ident(os.fstat(fd))==before and ident(p.lstat())==before
 finally:os.close(fd)
 return dict(path=str(p),sha256=h.hexdigest(),size_bytes=total,identity=before)
review=json.loads((D/'REVIEW.json').read_bytes());actual=json.loads((D/'ACTUAL_SOURCE_REVIEW_TOOL_RETURN.json').read_bytes())
assert review['status']=='PASS_COMPLETE_BUILD_MEMORY_OBSERVATION_SOURCE_ONLY_UNREADY_NO_EXECUTION'
assert review['source_only'] is True and review['all_checks_typed_true'] is True
assert type(review['checks']) is list and review['check_count']==len(review['checks'])==186
assert len({q['name'] for q in review['checks']})==186 and all(type(q['passed']) is bool for q in review['checks'])
assert sum(q['passed'] is False for q in review['checks'])==0 and len(review['blockers'])==0
tr=actual['terminal_tool_return'];assert actual['observed_terminal'] is True and actual['closed'] is True and type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr
observed=json.loads(tr['output']);assert observed['status']==review['status'] and observed['check_count']==186 and observed['passed_count']==186
index=json.loads((D/'CANDIDATE_COMPLETE_MEMBER_DIRECTORY_INDEX.json').read_bytes())
assert len(index['files'])==90 and len(index['directories'])==8
for q in index['files'].values():assert pin(q['path'])==q
for rel,i in index['directories'].items():assert ident((Path(index['manifest_pin']['path']).parent/rel).lstat())==i
assert pin(index['manifest_pin']['path'])==index['manifest_pin']==review['qualified_complete_Source_manifest_pin']
mp=D/'MANIFEST.json';assert not mp.exists();mp.touch(mode=0o600)
files={};dirs={'.':ident(D.lstat())};ast_count=0
for p in sorted(D.rglob('*')):
 assert not p.is_symlink()
 if p.is_dir():dirs[str(p.relative_to(D))]=ident(p.lstat())
 elif p!=mp:
  q=pin(p);files[str(p.relative_to(D))]=q
  if p.suffix=='.py':ast.parse(p.read_bytes(),filename=str(p),type_comments=True);ast_count+=1
manifest=dict(schema='INDEPENDENT_V25_MEMORY_OBSERVATION_V3_COMPLETE_SOURCE_REVIEW_PACKAGE_V1',source_only=True,status=review['status'],member_count=len(files),members=files,directories=dirs,actual_Source_review_exit_int=0,Source_verdict_qualification_granted=True,qualification_scope='STATIC_UNREADY_SOURCE_ONLY',candidate_or_business_executed=False)
mp.write_text(json.dumps(manifest,indent=2)+'\n')
assert ident(D.lstat())==dirs['.'] and all(pin(D/rel)==q for rel,q in files.items())
S.mkdir(mode=0o700)
result=dict(source_only=True,closed_review_payload_no_append=True,status=review['status'],manifest_pin=pin(mp),review_pin=pin(D/'REVIEW.json'),actual_Source_review_tool_return_pin=pin(D/'ACTUAL_SOURCE_REVIEW_TOOL_RETURN.json'),candidate_manifest_pin=index['manifest_pin'],complete_review_members=len(files),complete_review_files_including_manifest=len(files)+1,complete_review_directories=len(dirs),reviewer_full_AST_count=ast_count,Source_review_actual_exit_int=0,Source_verdict_PASS=True,candidate_or_business_executed=False)
(S/'SOURCE_REVIEW_SEAL_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,sort_keys=True))
