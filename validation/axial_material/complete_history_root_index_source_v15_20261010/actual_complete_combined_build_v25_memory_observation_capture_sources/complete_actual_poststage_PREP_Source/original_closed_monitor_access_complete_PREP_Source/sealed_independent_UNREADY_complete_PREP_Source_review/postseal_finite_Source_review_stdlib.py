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
m=json.loads((P/'MANIFEST.json').read_bytes());assert set(str(x.relative_to(P))for x in P.rglob('*')if x.is_file())==set(m['members'])|{'MANIFEST.json'}
assert {'.':identity(P),**{str(x.relative_to(P)):identity(x)for x in P.rglob('*')if x.is_dir()}}==m['directories']
for n,v in m['members'].items():assert pin(P/n)==v
r=json.loads((P/'REVIEW.json').read_bytes());assert r['check_count']==len(r['checks'])==79 and all(type(c['passed'])is bool and c['passed']is True for c in r['checks'])
seal=json.loads((P.with_name(P.name+'_seal_receipt')/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json').read_bytes());a=seal['terminal_tool_return'];assert seal['closed']is True and type(a['exit_code'])is int and a['exit_code']==0 and'session_id'not in a
v=json.loads(a['output']);assert v['manifest_pin']==pin(P/'MANIFEST.json')and v['review_pin']==pin(P/'REVIEW.json')
print(json.dumps(dict(source_only=True,status='POSTSEALED_COMPLETE_SOURCE_REVIEW_UNCHANGED',manifest_pin=pin(P/'MANIFEST.json'),review_pin=pin(P/'REVIEW.json'),member_count=len(m['members']),check_count=79,candidate_helper_guard_API_compiler_or_numeric_executed=False)))
