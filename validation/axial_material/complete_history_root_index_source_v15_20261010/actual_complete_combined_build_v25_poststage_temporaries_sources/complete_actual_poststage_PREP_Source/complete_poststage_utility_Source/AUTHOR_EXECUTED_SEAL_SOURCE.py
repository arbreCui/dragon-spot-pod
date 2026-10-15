import ast,hashlib,json,os,stat
from pathlib import Path
U=Path('/private/tmp/axmat_V25_poststage_complete_finite_utilities_V3_UNREADY_Source_20261010')
def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 i=identity(p);assert stat.S_ISREG(i[2]) and i[3]==1 and p.resolve()==p
 raw=p.read_bytes();assert identity(p)==i
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=i)
for name,count in [('AUTHOR_COMPLETE_UTILITY_SOURCE_ONLY_REPORT.json',82),('FINAL_SOURCE_INTEGRATION_CHECK_REPORT.json',566)]:
 d=json.loads((U/name).read_bytes());assert d['source_only'] is True and d['all_checks_typed_true'] is True and d['blockers']==[] and d['check_count']==count and len(d['checks'])==count and all(type(q['passed']) is bool and q['passed'] is True for q in d['checks'])
r=json.loads((U/'AUTHOR_COMPLETE_UTILITY_SOURCE_ONLY_REPORT.json').read_bytes());assert len(r['role_Source_pins'])==7
for name,q in r['role_Source_pins'].items():assert pin(U/name)==q
actual=json.loads((U/'ACTUAL_AUTHOR_AND_SOURCE_CHECK_TOOL_RETURNS.json').read_bytes())
for role,chunk in [('author','f2b2a4'),('source_integration_check','2e1935')]:
 t=actual[role]['actual_tool_return'];assert type(t['exit_code']) is int and t['exit_code']==0 and 'session_id' not in t and t['chunk_id']==chunk
 out=json.loads(t['output']);assert out.get('source_only') is True
mf=U/'MANIFEST.json';assert not os.path.lexists(mf);mf.touch(exist_ok=False)
members={};dirs={'.':identity(U)};ast_count=0
for p in sorted(U.rglob('*')):
 assert not p.is_symlink();rel=str(p.relative_to(U));i=identity(p)
 if p==mf:continue
 if stat.S_ISDIR(i[2]):dirs[rel]=i
 else:
  members[rel]=pin(p)
  if p.suffix=='.py':ast.parse(p.read_bytes(),filename=str(p));ast_count+=1
m=dict(schema='V25_POSTSTAGE_COMPLETE_FINITE_UTILITY_SOURCE_MANIFEST_V1',source_only=True,status='UNREADY_COMPLETE_SOURCE_ONLY_NOT_EXECUTED_PENDING_INDEPENDENT_PEER',members=members,member_count=len(members),directories=dirs,role_Source_names=sorted(r['role_Source_pins']),all_future_business_facts_unknown=True,new_PREP_BUILD_utility_or_guard_API_compile_native_material_executed=False)
with mf.open('w') as f:json.dump(m,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')
assert identity(U)==dirs['.']
for rel,q in members.items():assert pin(U/rel)==q
for rel,i in dirs.items():assert identity(U/rel)==i
print(json.dumps(dict(manifest_pin=pin(mf),review_pin=pin(U/'FINAL_SOURCE_INTEGRATION_CHECK_REPORT.json'),author_report_pin=pin(U/'AUTHOR_COMPLETE_UTILITY_SOURCE_ONLY_REPORT.json'),full_Source_package_members=len(members),complete_files=len(members)+1,complete_directories_including_root=len(dirs),complete_regular_bytes=sum(q['size_bytes'] for q in members.values())+pin(mf)['size_bytes'],complete_py_AST_count=ast_count,source_only=True,utility_or_business_or_science_executed=False)))
