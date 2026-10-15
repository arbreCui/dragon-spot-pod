from pathlib import Path
import ast,hashlib,json,stat
P=Path('/private/tmp/axmat_V25_complete_BUILD_memory_observation_UNREADY_Source_ynjrvdf7')
S=Path(str(P)+'_seal_receipt')
def identity(p):
 s=p.lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 before=identity(p);assert stat.S_ISREG(before[2])and before[3]==1 and not p.is_symlink()
 with p.open('rb')as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 assert identity(p)==before
 return dict(path=str(p),sha256=h,size_bytes=before[4],identity=before)
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
proof=json.loads((P/'COMPLETE_SOURCE_INVERSES.json').read_text())
report=json.loads((P/'AUTHOR_COMPLETE_SOURCE_ONLY_REPORT.json').read_text())
assert report['source_only']is True and report['all_checks_typed_true']is True and report['blockers']==[] and type(report['check_count'])is int and report['check_count']==len(report['checks'])==63
assert len({r['check']for r in report['checks']})==63 and all(type(r['passed'])is bool and r['passed']is True for r in report['checks'])
for role,rel in proof['role_current_paths'].items():
 text=(P/rel).read_text();ast.parse(text)
 for row in reversed(proof['exact_finite_transforms'][role]):
  assert text.count(row['new'])==row['count'];text=text.replace(row['new'],row['old'])
 parent=(P/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).read_text()
 assert text==parent and ast.dump(ast.parse(text),include_attributes=False)==ast.dump(ast.parse(parent),include_attributes=False)
 for q in (proof['original_parent_fullpins'][role],report['parent_source_fullpins'][role]):assert pin(Path(q['path']))==q
for q in list(report['qualified_role_Source_pins'].values())+list(report['qualified_utility_Source_pins'].values()):assert pin(Path(q['path']))==q
pyfiles=[p for p in P.rglob('*.py')]
for p in pyfiles:ast.parse(p.read_bytes())
# Append only before the one final manifest freeze.
dump(P/'FINAL_FULL_SOURCE_AUTHOR_SEAL_CHECK.json',dict(schema='AUTHOR_COMPLETE_BUILD_MEMORY_DIAGNOSTIC_FINAL_SOURCE_SEAL_CHECK_V1',source_only=True,author_typed_unique_checks=63,complete_roles=14,full_Source_AST_count=len(pyfiles),whole_byte_AST_inverses=True,all_original_parent_role_fullpins_unchanged=True,all_candidate_roles_UNREADY=True,future_environment_witness_None=True,candidate_guard_helper_API_resource_native_material_or_business_executed=False))
(P/'FINAL_SOURCE_SEAL_TEXT_ONLY.py').write_bytes(Path(__file__).read_bytes())
(P/'MANIFEST.json').write_text('{}\n')
files={str(p.relative_to(P)):pin(p)for p in sorted(P.rglob('*'))if p.is_file()and p.name!='MANIFEST.json'}
directories={'.':identity(P),**{str(p.relative_to(P)):identity(p)for p in sorted(P.rglob('*'))if p.is_dir()}}
dump(P/'MANIFEST.json',dict(schema='V25_COMPLETE_BUILD_MEMORY_OBSERVATION_UNREADY_SOURCE_PACKAGE_V1',source_only=True,status='UNREADY_SOURCE_ONLY_PENDING_INDEPENDENT_REVIEW_AND_ROOT_ENVIRONMENT_BINDING',member_count=len(files),members=files,directories=directories,total_member_bytes=sum(q['size_bytes']for q in files.values()),all_actual_future_business_or_environment_qualification_pins=None,candidate_or_business_executed=False))
assert directories=={'.':identity(P),**{str(p.relative_to(P)):identity(p)for p in sorted(P.rglob('*'))if p.is_dir()}}
for rel,q in files.items():assert pin(P/rel)==q
S.mkdir()
value=dict(source_only=True,closed_Source_payload_immutable=True,manifest_pin=pin(P/'MANIFEST.json'),review_pin=pin(P/'AUTHOR_COMPLETE_SOURCE_ONLY_REPORT.json'),inverse_pin=pin(P/'COMPLETE_SOURCE_INVERSES.json'),complete_members=len(files),complete_files_including_manifest=len(files)+1,complete_directories_including_root=len(directories),full_Source_AST_count=len(pyfiles)+1,all63_author_checks_typed_true=True,candidate_guard_helper_API_resource_native_material_or_business_executed=False)
dump(S/'SOURCE_SEAL_RESULT.json',value)
print(json.dumps(value,allow_nan=False))
