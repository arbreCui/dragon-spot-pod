import hashlib,json,os,stat
from pathlib import Path
D=Path('/private/tmp/axmat_P4_actual_PREP_bound_Source_INDEPENDENT_review_k3w_41pl');S=D.with_name(D.name+'_seal_receipt')
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
m=json.loads((D/'MANIFEST.json').read_bytes());r=json.loads((D/'REVIEW.json').read_bytes());a=json.loads((S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json').read_bytes());tr=a['terminal_tool_return'];o=json.loads(tr['output'])
assert a['closed'] is True and a['observed_terminal'] is True and type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr
files={};dirs={'.':ident(D.lstat())}
for p in sorted(D.rglob('*')):
 assert not p.is_symlink()
 if p.is_dir():dirs[str(p.relative_to(D))]=ident(p.lstat())
 else:files[str(p.relative_to(D))]=pin(p)
assert set(files)==set(m['members'])|{'MANIFEST.json'} and dirs==m['directories'] and all(files[k]==q for k,q in m['members'].items())
assert files['MANIFEST.json']==o['manifest_pin'] and files['REVIEW.json']==o['review_pin'] and r['all_checks_typed_true'] is True and r['blockers']==[]
for q in r['complete_bound_member_pins'].values():assert pin(q['path'])==q
assert pin(r['actual_Root_Source_binding_tool_receipt_pin']['path'])==r['actual_Root_Source_binding_tool_receipt_pin']
report=dict(source_only=True,status='PASS_POSTSEAL_INTEGRITY_ACTUAL_PREP_BOUND_SOURCE_REVIEW_ONLY',Source_review_status=r['status'],manifest_pin=files['MANIFEST.json'],review_pin=files['REVIEW.json'],true_seal_tool_return_pin=pin(S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json'),all_complete_review_member_pins=files,complete_review_directory_7ID=dirs,actual_bound_files_all8_reverified=True,no_packet_append_after_seal=True,Source_review_actual_exit_int=0,Source_verdict_PASS=True,reviewer_candidate_or_API_or_business_executed=False,runtime_or_RSS_or_science_qualified=False)
(S/'POSTSEAL_REPORT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(source_only=True,status=report['status'],Source_review_status=r['status'],manifest_pin=files['MANIFEST.json'],review_pin=files['REVIEW.json'],true_seal_tool_return_pin=report['true_seal_tool_return_pin'],postseal_report_pin=pin(S/'POSTSEAL_REPORT.json'),complete_review_files=len(files),complete_review_directories=len(dirs),Source_review_actual_exit_int=0,Source_verdict_PASS=True,reviewer_candidate_or_API_or_business_executed=False),sort_keys=True))
