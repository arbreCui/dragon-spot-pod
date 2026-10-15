import hashlib,json,stat
from pathlib import Path
P=Path(__file__).parent
def ids(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 i=ids(p);assert stat.S_ISREG(i[2]) and i[3]==1 and not p.is_symlink()
 with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 assert ids(p)==i;return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
m=json.loads((P/'MANIFEST.json').read_bytes())
assert set(str(p.relative_to(P)) for p in P.rglob('*') if p.is_file())==set(m['members'])|{'MANIFEST.json'}
for n,v in m['members'].items():assert pin(P/n)==v
assert {'.':ids(P),**{str(p.relative_to(P)):ids(p) for p in P.rglob('*') if p.is_dir()}}==m['directories']
s=json.loads((P.with_name(P.name+'_seal_receipt')/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json').read_bytes());t=s['terminal_tool_return']
assert s['closed'] is True and type(t['exit_code']) is int and t['exit_code']==0 and 'session_id' not in t
v=json.loads(t['output']);assert v['manifest_pin']==pin(P/'MANIFEST.json') and v['review_pin']==pin(P/'REVIEW.json')
r=json.loads((P/'REVIEW.json').read_bytes());assert v['qualified_bound_manifest_pin']==r['qualified_bound_manifest_pin']
assert r['check_count']==1445 and all(type(c['passed']) is bool and c['passed'] is True for c in r['checks'])
for q in r['complete_full_EOF_Source_META_pins']:assert pin(Path(q['path']))==q
print(json.dumps(dict(source_only=True,status='POSTSEALED_DIRECTORY_ONLY_BOUND_SOURCE_REVIEW_UNCHANGED',manifest_pin=pin(P/'MANIFEST.json'),review_pin=pin(P/'REVIEW.json'),member_count=len(m['members']),check_count=1445,candidate_helper_guard_API_compiler_or_numeric_executed=False,new_PREP_BUILD_or_science_qualified=False)))
