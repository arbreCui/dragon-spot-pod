import ast,hashlib,json,os,stat
from pathlib import Path
F=Path('/private/tmp/axmat_N6_actual_closed_failure_small_META_LIFTx6')
def ident(p):
 s=p.lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 i=ident(p);assert p.resolve()==p and p.is_absolute()and stat.S_ISREG(i[2])and i[3]==1
 with p.open('rb')as stream:h=hashlib.file_digest(stream,'sha256').hexdigest()
 assert ident(p)==i;return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
def strict(raw):
 def pairs(rows):
  d={}
  for k,v in rows:assert k not in d;d[k]=v
  return d
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in()).throw(ValueError(v)))
def view(root):
 files=[];dirs={}
 for p in [root,*sorted(root.rglob('*'))]:
  i=ident(p);assert not stat.S_ISLNK(i[2])
  if stat.S_ISDIR(i[2]):dirs[str(p)]=i
  else:assert stat.S_ISREG(i[2])and i[3]==1;files.append(dict(path=str(p),size_bytes=i[4],identity=i))
 return dict(files=files,directories=dirs)
rp=pin(F/'REVIEW.json');assert rp['sha256']=='b20187a6fdd761db991ce3a12fb3b39c7031b6ef702ac3b88cf67cd81cecabec'
r=strict((F/'REVIEW.json').read_bytes());assert r['schema']=='INDEPENDENT_ACTUAL_CLOSED_N6_FAILURE_SOURCE_SMALL_META_REVIEW_V1'and r['status']=='PASS_SAVED_FAILED_N6_SOURCE_SMALL_META_ONLY_NO_RUNTIME_OR_SCIENCE'and r['source_only']is True and r['all_checks_passed']is True and r['all_checks_typed_true']is True and r['blockers']==[]
checks=r['checks'];assert type(r['check_count'])is int and r['check_count']==len(checks)==242 and len({c['check']for c in checks})==242 and all(set(c)=={'check','passed'}and type(c['check'])is str and c['check']and type(c['passed'])is bool and c['passed']is True for c in checks)
for tag,wanted in r['actual_current_namespace_metadata_after'].items():
 root=Path(min(wanted['directories'],key=lambda s:len(Path(s).parts)));assert view(root)==wanted
for row in r['finite_whole_saved_Source_and_small_META_copies'].values():
 a=row['actual_original_pin'];b=row['retained_whole_byte_copy_pin'];assert pin(Path(a['path']))==a and pin(Path(b['path']))==b and(a['sha256'],a['size_bytes'])==(b['sha256'],b['size_bytes'])
truth=strict((F/'ACTUAL_INDEPENDENT_REVIEW_TOOL_RETURN.json').read_bytes());t=truth['terminal_tool_return'];out=strict(t['output']);assert truth['source_only']is True and truth['closed']is True and truth['observed_terminal']is True and truth['session_repolled_after_close']is False and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t and t['chunk_id']==truth['actual_terminal_chunk']=='77bcdb'and out['review_pin']==rp and out['check_count']==242 and out['all_checks_passed']is True and out['blockers']==[]and out['candidate_guard_API_native_compile_material_or_diagnostic_executed_by_reviewer']is False
assert r['actual_original_compiler_process_group_cleanup_verified']is False and r['actual_current_process_group_absent_at_saved_later_check']is True and r['scientific_qualification_created']is False
mf=F/'MANIFEST.json'
with mf.open('x')as stream:pass
members=[];py_count=0
for p in sorted(F.rglob('*')):
 if not p.is_file()or p==mf:continue
 q=pin(p)
 if p.suffix=='.py':ast.parse(p.read_bytes(),filename=str(p));py_count+=1
 if p.suffix=='.json':strict(p.read_bytes())
 members.append(dict(relative_path=str(p.relative_to(F)),fullpin=q))
dirs={str(p.relative_to(F)):ident(p)for p in [F,*sorted(F.rglob('*'))]if p.is_dir()}
v=dict(schema='INDEPENDENT_ACTUAL_CLOSED_N6_FAILURE_SOURCE_SMALL_META_REVIEW_MANIFEST_V1',status='SEALED_SAVED_FAILED_N6_SOURCE_SMALL_META_ONLY_NO_RUNTIME_OR_SCIENCE',source_only=True,members=members,member_count=len(members),file_count_including_manifest=len(members)+1,directory_count=len(dirs),complete_directory_identity=dirs,review_pin=rp,actual_review_terminal_chunk='77bcdb',actual_review_tool_receipt_pin=pin(F/'ACTUAL_INDEPENDENT_REVIEW_TOOL_RETURN.json'),complete_py_AST_count=py_count,independent_checks=242,blockers=[],actual_saved_runtime_exit_code=1,actual_original_compiler_process_group_cleanup_verified=False,actual_current_process_group_absent_at_saved_later_check=True,candidate_guard_API_native_compile_material_or_diagnostic_executed_by_reviewer=False,scientific_qualification_created=False)
with mf.open('w')as stream:json.dump(v,stream,indent=2,allow_nan=False);stream.write('\n')
assert dirs=={str(p.relative_to(F)):ident(p)for p in [F,*sorted(F.rglob('*'))]if p.is_dir()}
for row in members:assert pin(Path(row['fullpin']['path']))==row['fullpin']
print(json.dumps(dict(status=v['status'],source_only=True,manifest_pin=pin(mf),review_pin=rp,members=len(members),files=len(members)+1,directories=len(dirs),checks=242,blockers=[],actual_candidate_execution=False),allow_nan=False))
