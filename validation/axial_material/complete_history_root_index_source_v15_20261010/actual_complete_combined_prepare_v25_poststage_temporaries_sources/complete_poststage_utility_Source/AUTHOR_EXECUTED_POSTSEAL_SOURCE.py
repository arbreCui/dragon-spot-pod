import ast,hashlib,json,stat
from pathlib import Path
U=Path('/private/tmp/axmat_V25_poststage_complete_finite_utilities_V3_UNREADY_Source_20261010')
def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 i=identity(p);assert stat.S_ISREG(i[2]) and i[3]==1 and p.resolve()==p
 raw=p.read_bytes();assert identity(p)==i
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=i)
mp=pin(U/'MANIFEST.json');m=json.loads((U/'MANIFEST.json').read_bytes());files={};dirs={'.':identity(U)};asts=0
for p in sorted(U.rglob('*')):
 assert not p.is_symlink();rel=str(p.relative_to(U));i=identity(p)
 if stat.S_ISDIR(i[2]):dirs[rel]=i
 else:
  files[rel]=pin(p)
  if p.suffix=='.py':ast.parse(p.read_bytes(),filename=str(p));asts+=1
assert set(files)==set(m['members'])|{'MANIFEST.json'} and len(m['members'])==m['member_count'] and dirs==m['directories']
for rel,q in m['members'].items():assert files[rel]==q
assert pin(U/'MANIFEST.json')==mp
print(json.dumps(dict(manifest_pin=mp,review_pin=pin(U/'FINAL_SOURCE_INTEGRATION_CHECK_REPORT.json'),complete_files=len(files),complete_directories_including_root=len(dirs),complete_py_AST_count=asts,all_full_EOF_SHA7ID_unchanged=True,all_members_present_no_append=True,source_only=True,utility_or_business_or_science_executed=False)))
