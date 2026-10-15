import ast,hashlib,json,os,stat
from pathlib import Path
D=Path('/private/tmp/axmat_V25_actual_PREP_bound_Source_INDEPENDENT_review_q1lqskpj');S=D.with_name(D.name+'_seal_receipt')
def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);i=ident(p.lstat());assert stat.S_ISREG(i[2]) and i[3]==1 and 0<=i[4]<=2**20;fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  assert ident(os.fstat(fd))==i;h=hashlib.sha256();n=0
  while True:
   b=os.read(fd,65536)
   if not b:break
   h.update(b);n+=len(b)
  assert n==i[4] and os.read(fd,1)==b'' and ident(os.fstat(fd))==i and ident(p.lstat())==i
 finally:os.close(fd)
 return dict(path=str(p),sha256=h.hexdigest(),size_bytes=n,identity=i)
r=json.loads((D/'REVIEW.json').read_bytes());a=json.loads((D/'ACTUAL_SOURCE_REVIEW_TOOL_RETURN.json').read_bytes());tr=a['terminal_tool_return'];o=json.loads(tr['output'])
assert r['schema']=='INDEPENDENT_ACTUAL_V25_MEMORY_OBSERVATION_COMPLETE_PREP_BOUND_SOURCE_REVIEW_V1' and r['status']=='PASS_ACTUAL_Q_BOUND_COMPLETE_PREP_MEMORY_OBSERVATION_SOURCE_ONLY_NOT_INSTALLED_OR_EXECUTED'
assert r['source_only'] is True and r['all_checks_typed_true'] is True and r['blockers']==[] and r['check_count']==len(r['checks'])==38 and len({c['name'] for c in r['checks']})==38 and all(type(c['passed']) is bool and c['passed'] is True for c in r['checks'])
assert a['observed_terminal'] is True and a['closed'] is True and type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr and o['status']==r['status'] and o['check_count']==38 and o['passed_count']==38 and o['failed_checks']==[]
assert o['actual_bound_manifest_pin']==r['actual_complete_bound_Source_manifest_pin'] and o['actual_ready_role_Source_pins']==r['actual_ready_role_Source_pins']
for q in r['complete_bound_member_pins'].values():assert pin(q['path'])==q
assert pin(r['actual_Root_Source_binding_tool_receipt_pin']['path'])==r['actual_Root_Source_binding_tool_receipt_pin']
assert all(v is None for v in r['all6_future_business_pins'].values())
mp=D/'MANIFEST.json';assert not mp.exists();mp.touch(mode=0o600)
files={};dirs={'.':ident(D.lstat())};ac=0
for p in sorted(D.rglob('*')):
 assert not p.is_symlink()
 if p.is_dir():dirs[str(p.relative_to(D))]=ident(p.lstat())
 elif p!=mp:
  files[str(p.relative_to(D))]=pin(p)
  if p.suffix=='.py':ast.parse(p.read_bytes(),filename=str(p),type_comments=True);ac+=1
m=dict(schema='INDEPENDENT_ACTUAL_V25_MEMORY_OBSERVATION_COMPLETE_PREP_BOUND_SOURCE_REVIEW_PACKAGE_V1',source_only=True,status=r['status'],member_count=len(files),members=files,directories=dirs,actual_Source_review_exit_int=0,Source_only_review_qualified=True,runtime_or_RSS_or_science_qualified=False,reviewer_candidate_or_API_or_business_executed=False)
mp.write_text(json.dumps(m,indent=2)+'\n');assert ident(D.lstat())==dirs['.'] and all(pin(D/k)==q for k,q in files.items())
S.mkdir(mode=0o700)
result=dict(source_only=True,status=r['status'],manifest_pin=pin(mp),review_pin=pin(D/'REVIEW.json'),actual_Source_review_tool_return_pin=pin(D/'ACTUAL_SOURCE_REVIEW_TOOL_RETURN.json'),actual_complete_bound_Source_manifest_pin=r['actual_complete_bound_Source_manifest_pin'],actual_ready_role_Source_pins=r['actual_ready_role_Source_pins'],complete_review_files=len(files)+1,complete_review_directories=len(dirs),all_reviewer_Python_AST_count=ac,Source_review_actual_exit_int=0,Source_verdict_PASS=True,no_packet_append_after_seal=True,reviewer_candidate_or_API_or_business_executed=False,runtime_or_RSS_or_science_qualified=False)
(S/'SEAL_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,sort_keys=True))
