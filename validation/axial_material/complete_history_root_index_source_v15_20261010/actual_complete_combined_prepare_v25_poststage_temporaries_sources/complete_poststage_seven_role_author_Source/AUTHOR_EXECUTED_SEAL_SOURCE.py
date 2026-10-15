from pathlib import Path
import ast,hashlib,json,stat
P=Path('/private/tmp/axmat_V25_poststage_temporaries_complete_UNREADY_Source_v2ept7ev')
S=P.with_name(P.name+'_seal_receipt')
def i7(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 a=p.lstat();assert stat.S_ISREG(a.st_mode)and a.st_nlink==1 and not p.is_symlink();r=p.read_bytes();assert i7(a)==i7(p.lstat())
 return dict(path=str(p),sha256=hashlib.sha256(r).hexdigest(),size_bytes=len(r),identity=i7(a))
for q in P.rglob('*'):assert not q.is_symlink()
report=json.loads((P/'AUTHOR_SOURCE_ONLY_REPORT.json').read_bytes());assert report['all_checks_typed_true']is True and report['check_count']==66 and report['blockers']==[]
proof=json.loads((P/'COMPLETE_SOURCE_INVERSES.json').read_bytes())
for role,rel in proof['role_filenames'].items():
 text=(P/rel).read_text();ast.parse(text)
 for row in reversed(proof['exact_finite_transforms'][role]):assert text.count(row['new'])==row['count'];text=text.replace(row['new'],row['old'])
 parent=(P/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).read_text();assert text==parent and ast.dump(ast.parse(text),include_attributes=False)==ast.dump(ast.parse(parent),include_attributes=False)
for row in json.loads((P/'ALL_ORIGINAL_READ_SOURCE_AND_SMALL_META_PINS.json').read_bytes())['full_read_input_pins']:assert pin(Path(row['path']))==row
S.mkdir(exist_ok=False);target=P/'MANIFEST.json';target.touch(exist_ok=False)
members={str(q.relative_to(P)):pin(q)for q in sorted(P.rglob('*'))if q.is_file()and q!=target}
directories={'.':i7(P.lstat()),**{str(q.relative_to(P)):i7(q.lstat())for q in sorted(P.rglob('*'))if q.is_dir()}}
manifest=dict(schema='COMPLETE_V25_POSTSTAGE_TEMPORARIES_UNREADY_SOURCE_PACKAGE_V1',source_only=True,author_not_independent_peer=True,member_count=len(members),members=members,directories=directories,candidate_helper_guard_API_compile_numeric_executed=False,new_business_or_science_qualified=False)
with target.open('w')as f:json.dump(manifest,f,indent=2,allow_nan=False);f.write('\n')
for rel,row in members.items():assert pin(P/rel)==row
for rel,row in directories.items():assert i7((P if rel=='.'else P/rel).lstat())==row
assert set(members)=={str(q.relative_to(P))for q in P.rglob('*')if q.is_file()and q!=target}
out=dict(source_only=True,complete_Source_package_fixed=True,manifest=pin(target),report=pin(P/'AUTHOR_SOURCE_ONLY_REPORT.json'),inverse=pin(P/'COMPLETE_SOURCE_INVERSES.json'),member_count=len(members),total_files=len(members)+1,directory_count=len(directories),full_file_bytes=sum(x['size_bytes']for x in members.values())+target.stat().st_size,roles={role:pin(P/rel)for role,rel in proof['role_filenames'].items()},all_original_Source_and_small_META_unchanged=True,candidate_helper_guard_API_compile_numeric_executed=False,new_business_or_science_qualified=False)
with(S/'FULL_SOURCE_SEAL_VERIFICATION.json').open('x')as f:json.dump(out,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(out))
