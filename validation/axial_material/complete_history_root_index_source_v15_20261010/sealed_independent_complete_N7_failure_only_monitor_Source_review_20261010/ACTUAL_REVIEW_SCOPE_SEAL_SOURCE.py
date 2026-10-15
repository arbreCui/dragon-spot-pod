import ast,hashlib,json,os,stat
from pathlib import Path
P=Path('/private/tmp/axmat_complete_native_observation_N7_failure_only_monitor_UNREADY_Source_piquf6v6')
F=Path('/private/tmp/axmat_N7_complete_Source_independent_xxd8yrrc')
N6=Path('/private/tmp/axmat_complete_native_observation_N6_shared_original_libraries_UNREADY_Source_p8u1h6xc')
def ident(p):
 s=p.lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 i=ident(p);assert p.is_absolute()and p.resolve()==p and stat.S_ISREG(i[2])and i[3]==1
 with p.open('rb')as stream:sha=hashlib.file_digest(stream,'sha256').hexdigest()
 assert ident(p)==i;return dict(path=str(p),sha256=sha,size_bytes=i[4],identity=i)
def strict(raw):
 def pairs(rows):
  d={}
  for k,v in rows:assert k not in d;d[k]=v
  return d
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in()).throw(ValueError(x)))
def copy(src,dst):
 q=pin(src);assert not os.path.lexists(dst)
 with src.open('rb')as a,dst.open('xb')as b:
  while raw:=a.read(2**20):b.write(raw)
 assert pin(src)==q;z=pin(dst);assert(z['sha256'],z['size_bytes'])==(q['sha256'],q['size_bytes'])
 return dict(original_pin=q,retained_byte_copy_pin=z)

report_pin=pin(F/'REVIEW.json');assert report_pin['sha256']=='356496012ce1f3a3d3d154a375321a905b31bb94f4c6f3c355f850a9ff57ba0b'
report=strict((F/'REVIEW.json').read_bytes());assert report['schema']=='INDEPENDENT_COMPLETE_NATIVE_OBSERVATION_BUILD_HOST_BINDER_SOURCE_REVIEW_V1'and report['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'and report['source_only']is True and report['all_checks_passed']is True and report['all_checks_typed_true']is True and report['blockers']==[]
checks=report['checks'];assert type(report['check_count'])is int and report['check_count']==len(checks)==5213 and len({c['check']for c in checks})==5213 and all(set(c)=={'check','passed'}and type(c['check'])is str and c['check']and type(c['passed'])is bool and c['passed']is True for c in checks)
for q in report['actual_author_Source_contract'].values():assert pin(Path(q['path']))==q
assert len(report['actual_author_Source_contract'])==14
truth=strict((F/'ACTUAL_INDEPENDENT_REVIEW_TOOL_RETURNS.json').read_bytes());t=truth['terminal_tool_return'];assert truth['closed']is True and truth['observed_terminal']is True and truth['session_repolled_after_close']is False and truth['source_only']is True and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t and t['chunk_id']==truth['actual_terminal_chunk']=='3de872'
stdout=strict(t['output']);assert stdout['review_pin']==report_pin and stdout['check_count']==5213 and stdout['all_checks_passed']is True and stdout['blockers']==[]and stdout['actual_author_Source_contract']==report['actual_author_Source_contract']and stdout['candidate_guard_API_compile_native_material_executed']is False
newdir=F/'FINITE_REVIEWED_ACTIVE_ROLE_SOURCE';newdir.mkdir();motherdir=F/'FINITE_REVIEWED_ORIGINAL_N6_ROLE_SOURCE';motherdir.mkdir();retained={}
for role in ('host_template','runtime_template','binder','postclose_writer','request_preparer'):
 src=Path(report['actual_author_Source_contract'][role]['path']);retained['N7_'+role]=copy(src,newdir/src.name)
 if role!='host_template':retained['N6_'+role]=copy(N6/src.name,motherdir/src.name)
value=dict(schema='FINITE_INDEPENDENT_N7_COMPLETE_SOURCE_REVIEW_PROVENANCE_V1',source_only=True,actual_author_Source_manifest_pin=report['actual_author_Source_contract']['qualified_source_manifest'],actual_complete_review_pin=report_pin,actual_review_terminal_chunk='3de872',actual_review_initial_chunk='fae29f',actual_review_session=69842,closed_review_session_not_repolled=True,actual_complete_Source_check_count=5213,complete182_author_files_and24_directories_full_EOF_and_identity_verified=True,all148_unchanged_N6_members_full_byte_verified=True,full_N7_4_role_byte_AST_inverse_verified=True,full1365_native_Source_tar_members_EOF_and_gzip_CRC_verified=True,full_original_physics14_and_host12_Source_inverse_verified=True,finite_retained_complete_roles=retained,Source_only_no_entire_mother_tree_reclone=True,candidate_guard_API_native_compile_material_or_numeric_executed=False,scientific_qualification_created=False)
with (F/'FINITE_COMPLETE_SOURCE_REVIEW_PROVENANCE.json').open('x')as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')
# Create manifest file before observing complete root directory identity.
mf=F/'MANIFEST.json'
with mf.open('x')as f:pass
members=[];py_count=0
for p in sorted(F.rglob('*')):
 if not p.is_file()or p==mf:continue
 q=pin(p)
 if p.suffix=='.py':ast.parse(p.read_bytes(),filename=str(p));py_count+=1
 if p.suffix=='.json':strict(p.read_bytes())
 members.append(dict(relative_path=str(p.relative_to(F)),fullpin=q))
dirs={str(p.relative_to(F)):ident(p)for p in [F,*sorted(F.rglob('*'))]if p.is_dir()}
value=dict(schema='INDEPENDENT_COMPLETE_NATIVE_OBSERVATION_SOURCE_REVIEW_MANIFEST_V1',status='SEALED_SOURCE_ONLY_PASS_NO_RUNTIME_OR_SCIENCE_CREDIT',source_only=True,members=members,member_count=len(members),file_count_including_manifest=len(members)+1,directory_count=len(dirs),complete_directory_identity=dirs,review_pin=report_pin,actual_review_tool_truth_pin=pin(F/'ACTUAL_INDEPENDENT_REVIEW_TOOL_RETURNS.json'),actual_original_Source_manifest_pin=report['actual_author_Source_contract']['qualified_source_manifest'],qualified_source_manifest=report['actual_author_Source_contract']['qualified_source_manifest'],whole_original_native_Source_archive_members=1365,independent_aggregate_Source_checks=5213,complete_retained_py_AST_count=py_count,blocker_count=0,actual_Root_Source_admission=None,actual_native_execution=None,scientific_qualification_created=False)
with mf.open('w')as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')
assert dirs=={str(p.relative_to(F)):ident(p)for p in [F,*sorted(F.rglob('*'))]if p.is_dir()}
for row in members:assert pin(Path(row['fullpin']['path']))==row['fullpin']
assert {str(p.relative_to(F))for p in F.rglob('*')if p.is_file()}=={r['relative_path']for r in members}|{'MANIFEST.json'}
print(json.dumps(dict(status='SEALED_SOURCE_ONLY_PASS_NO_RUNTIME_OR_SCIENCE_CREDIT',source_only=True,manifest_pin=pin(mf),review_pin=report_pin,members=len(members),files=len(members)+1,directories=len(dirs),blockers=[],actual_candidate_execution=False),allow_nan=False))
