from pathlib import Path
import ast,hashlib,json,stat
P=Path(__file__).resolve().parent
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 s=p.lstat();assert stat.S_ISREG(s.st_mode)and s.st_nlink==1 and not p.is_symlink();h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(2**20),b''):h.update(b)
 assert identity(s)==identity(p.lstat());return dict(path=str(p),sha256=h.hexdigest(),size_bytes=s.st_size,identity=identity(s))
mf=P/'MANIFEST.json';start=pin(mf);j=json.loads(mf.read_bytes());members=j['members'];assert type(j['member_count'])is int and j['member_count']==len(members)
before={m['relative_path']:pin(P/m['relative_path'])for m in members};assert all(before[m['relative_path']]==m['fullpin']for m in members)
assert {str(q.relative_to(P))for q in P.rglob('*')if q.is_file()}==set(before)|{'MANIFEST.json'}
dirs={str(q):identity(q.lstat())for q in [P,*sorted(P.rglob('*'))]if q.is_dir()};assert dirs==j['complete_directory_identity']and len(dirs)==j['directory_count']
asts=0
for name in before:
 if name.endswith('.py'):ast.parse((P/name).read_text());asts+=1
assert before=={m['relative_path']:pin(P/m['relative_path'])for m in members}and start==pin(mf)
r=json.loads((P/'AUTHOR_N7_COMPLETE_SOURCE_ONLY_REPORT.json').read_bytes());assert type(r['check_count'])is int and r['check_count']==len(r['checks'])and all(c['passed']is True for c in r['checks'])
print(json.dumps(dict(status='POSTSEAL_COMPLETE_N7_SOURCE_FULL_EOF_AST_READONLY_NO_EXECUTION',source_only=True,manifest_pin=start,report_pin=pin(P/'AUTHOR_N7_COMPLETE_SOURCE_ONLY_REPORT.json'),member_count=len(members),directory_count=len(dirs),complete_AST_count=asts,author_aggregate_Source_checks=r['check_count'],whole_Source_members_and_directories_unchanged=True,actual_instrumented_runtime_controls=None,actual_scientific_qualification=None,candidate_or_helper_or_guard_or_API_or_native_or_material_executed=False),allow_nan=False))
