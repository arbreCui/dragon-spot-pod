import ast,hashlib,json,stat
from pathlib import Path
P=Path(__file__).parent
def ident(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 i=ident(p);assert p.resolve()==p and stat.S_ISREG(i[2]) and i[3]==1
 with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 assert ident(p)==i;return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
mfp=pin(P/'MANIFEST.json');m=json.loads((P/'MANIFEST.json').read_text());assert pin(P/'MANIFEST.json')==mfp
actual={};dirs={'.':ident(P)};parsed=0
for p in sorted(P.rglob('*')):
 assert not p.is_symlink();i=ident(p);k=str(p.relative_to(P))
 if stat.S_ISREG(i[2]):
  actual[k]=pin(p)
  if p.suffix=='.py':ast.parse(p.read_bytes(),filename=str(p));parsed+=1
 else:assert stat.S_ISDIR(i[2]);dirs[k]=i
assert set(actual)==set(m['members'])|{'MANIFEST.json'} and dirs==m['directories'] and len(m['members'])==m['member_count']
for k,q in m['members'].items():assert actual[k]==q
for k,i in dirs.items():assert ident(P/k)==i
assert pin(P/'MANIFEST.json')==mfp
print(json.dumps(dict(source_only=True,status='COMPLETE_SEALED_SOURCE_POSTSEAL_FULL_EOF_SHA7ID_UNCHANGED_UNREADY',manifest_pin=mfp,complete_files=len(actual),complete_directories=len(dirs),all_member_bytes=sum(q['size_bytes'] for q in actual.values()),parsed_Source_python=parsed,Source_roles_not_imported_or_executed=True,actual_BUILD_native_science=False)))
