import hashlib,json,os,stat
from pathlib import Path
D=Path('/private/tmp/axmat_V25_memory_observation_INDEPENDENT_review_ZgGEhb');S=D.with_name(D.name+'_seal_receipt')
def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 before=ident(p.lstat());assert stat.S_ISREG(before[2]) and before[3]==1
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  assert ident(os.fstat(fd))==before;h=hashlib.sha256();total=0
  while True:
   b=os.read(fd,65536)
   if not b:break
   total+=len(b);h.update(b)
  assert total==before[4] and os.read(fd,1)==b'' and ident(os.fstat(fd))==before and ident(p.lstat())==before
 finally:os.close(fd)
 return dict(path=str(p),sha256=h.hexdigest(),size_bytes=total,identity=before)
m=json.loads((D/'MANIFEST.json').read_bytes());seal=json.loads((S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json').read_bytes());tr=seal['terminal_tool_return']
assert type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr and seal['observed_terminal'] is True and seal['closed'] is True
observed=json.loads(tr['output']);assert pin(D/'MANIFEST.json')==observed['manifest_pin'] and pin(D/'REVIEW.json')==observed['review_pin']
actual_files={};actual_dirs={'.':ident(D.lstat())}
for p in sorted(D.rglob('*')):
 assert not p.is_symlink()
 if p.is_dir():actual_dirs[str(p.relative_to(D))]=ident(p.lstat())
 else:actual_files[str(p.relative_to(D))]=pin(p)
assert set(actual_files)==set(m['members'])|{'MANIFEST.json'} and actual_dirs==m['directories']
assert all(actual_files[rel]==q for rel,q in m['members'].items())
assert m['actual_Source_review_exit_int']==1 and m['Source_verdict_qualification_granted'] is False
report=dict(source_only=True,status='PASS_POSTSEAL_INTEGRITY_OF_ACTUAL_FAILED_SOURCE_REVIEW_ONLY',source_review_status=m['status'],manifest_pin=actual_files['MANIFEST.json'],review_pin=actual_files['REVIEW.json'],true_seal_tool_return_pin=pin(S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json'),complete_review_files=len(actual_files),complete_review_directories=len(actual_dirs),complete_review_member_pins=actual_files,complete_review_directory_7ID=actual_dirs,no_review_packet_append_after_seal=True,Source_review_actual_exit_int=1,Source_verdict_PASS=False,candidate_or_business_executed=False)
(S/'POSTSEAL_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(source_only=True,status=report['status'],source_review_status=m['status'],manifest_pin=report['manifest_pin'],review_pin=report['review_pin'],postseal_report_pin=pin(S/'POSTSEAL_REPORT.json'),true_seal_tool_return_pin=report['true_seal_tool_return_pin'],complete_review_files=len(actual_files),complete_review_directories=len(actual_dirs),Source_review_actual_exit_int=1,Source_verdict_PASS=False,candidate_or_business_executed=False),sort_keys=True))
