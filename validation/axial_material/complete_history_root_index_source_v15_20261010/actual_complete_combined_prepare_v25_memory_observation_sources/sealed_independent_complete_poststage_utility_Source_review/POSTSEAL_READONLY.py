import hashlib,json,os,stat
from pathlib import Path
D=Path('/private/tmp/axmat_V25_memory_observation_V3_INDEPENDENT_review_2FVRNl');S=D.with_name(D.name+'_seal_receipt')
def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 before=ident(p.lstat());assert stat.S_ISREG(before[2]) and before[3]==1 and 0<=before[4]<=1048576
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
assert m['actual_Source_review_exit_int']==0 and m['Source_verdict_qualification_granted'] is True and m['qualification_scope']=='STATIC_UNREADY_SOURCE_ONLY'
candidate_index=json.loads((D/'CANDIDATE_COMPLETE_MEMBER_DIRECTORY_INDEX.json').read_bytes());candidate_files={}
for rel,q in candidate_index['files'].items():
 candidate_files[rel]=pin(Path(q['path']));assert candidate_files[rel]==q
candidate_root=Path(candidate_index['manifest_pin']['path']).parent;candidate_dirs={}
for root,dirs,files in os.walk(candidate_root,followlinks=False):
 root=Path(root);candidate_dirs[str(root.relative_to(candidate_root))]=ident(root.lstat())
 for name in dirs:assert not (root/name).is_symlink()
 assert all(str((root/name).relative_to(candidate_root)) in candidate_files for name in files)
assert candidate_dirs==candidate_index['directories'] and len(candidate_files)==90 and len(candidate_dirs)==8
report=dict(source_only=True,status='PASS_POSTSEAL_INTEGRITY_OF_ACTUAL_SOURCE_REVIEW_SOURCE_ONLY',source_review_status=m['status'],manifest_pin=actual_files['MANIFEST.json'],review_pin=actual_files['REVIEW.json'],true_seal_tool_return_pin=pin(S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json'),complete_review_files=len(actual_files),complete_review_directories=len(actual_dirs),complete_review_member_pins=actual_files,complete_review_directory_7ID=actual_dirs,no_review_packet_append_after_seal=True,all_candidate_90_files_and_8_directories_reverified=True,candidate_complete_member_pins=candidate_files,candidate_complete_directories=candidate_dirs,runtime_or_RSS_or_science_qualified=False,Source_review_actual_exit_int=0,Source_verdict_PASS=True,candidate_or_business_executed=False)
(S/'POSTSEAL_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(source_only=True,status=report['status'],source_review_status=m['status'],manifest_pin=report['manifest_pin'],review_pin=report['review_pin'],postseal_report_pin=pin(S/'POSTSEAL_REPORT.json'),true_seal_tool_return_pin=report['true_seal_tool_return_pin'],complete_review_files=len(actual_files),complete_review_directories=len(actual_dirs),Source_review_actual_exit_int=0,Source_verdict_PASS=True,candidate_or_business_executed=False),sort_keys=True))
