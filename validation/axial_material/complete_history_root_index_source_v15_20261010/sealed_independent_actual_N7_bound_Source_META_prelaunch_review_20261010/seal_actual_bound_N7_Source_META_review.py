import ast,hashlib,json,os,stat
from pathlib import Path
F=Path('/private/tmp/axmat_N7_actual_bound_Source_prelaunch_V2_im4o9o48')
def ident(p):
 s=p.lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 i=ident(p);assert p.is_absolute()and p.resolve()==p and stat.S_ISREG(i[2])and i[3]==1
 with p.open('rb')as stream:h=hashlib.file_digest(stream,'sha256').hexdigest()
 assert ident(p)==i;return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
def strict(raw):
 def pairs(rows):
  d={}
  for k,v in rows:assert k not in d;d[k]=v
  return d
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in()).throw(ValueError(v)))
def tree(root):
 files=[];dirs={}
 for p in [root,*sorted(root.rglob('*'))]:
  i=ident(p);assert not stat.S_ISLNK(i[2])
  if stat.S_ISDIR(i[2]):dirs[str(p)]=i
  else:files.append(pin(p))
 return dict(files=files,directories=dirs)
rp=pin(F/'REVIEW.json');r=strict((F/'REVIEW.json').read_bytes())
assert r['schema']=='INDEPENDENT_ACTUAL_N7_BOUND_SOURCE_META_PRELAUNCH_REVIEW_V1'and r['status']=='PASS_ACTUAL_BOUND_SOURCE_META_PRELAUNCH_NO_EXECUTION_OR_SCIENCE'and r['source_only']is True and r['all_checks_passed']is True and r['all_checks_typed_true']is True and r['blockers']==[]
checks=r['checks'];n=r['check_count'];assert type(n)is int and n==len(checks)>0 and len({c['check']for c in checks})==n and all(set(c)=={'check','passed'}and type(c['passed'])is bool and c['passed']is True for c in checks)
for key,view in r['actual_namespace_pins'].items():
 root=Path(next(p for p in view['directories']if len(Path(p).parts)==min(len(Path(v).parts)for v in view['directories'])))
 assert tree(root)==view
for q in r['actual_four_Root_bound_output_pins'].values():assert pin(Path(q['path']))==q
req=strict(Path(r['actual_Root_request_pin']['path']).read_bytes());assert all(not os.path.lexists(req['namespaces'][k])for k in ('host','output','control'))
truth=strict((F/'ACTUAL_INDEPENDENT_REVIEW_TOOL_RETURN.json').read_bytes());t=truth['terminal_tool_return'];out=strict(t['output'])
assert truth['source_only']is True and truth['closed']is True and truth['observed_terminal']is True and truth['session_repolled_after_close']is False and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t and t['chunk_id']==truth['actual_terminal_chunk']and out['review_pin']==rp and out['all_checks_passed']is True and out['check_count']==n and out['blockers']==[]and out['actual_HOC_all_absent']is True and out['candidate_guard_API_compile_native_or_material_executed']is False
inv=strict((F/'COMPLETE_OWN_CHECKER_N6_TO_N7_SOURCE_INVERSE.json').read_bytes());op=inv['original_full_Source_pin'];dp=inv['derived_full_Source_pin'];assert pin(Path(op['path']))==op and pin(Path(dp['path']))==dp
old=Path(op['path']).read_text();new=Path(dp['path']).read_text();lines=new.splitlines(keepends=True)
for h in reversed(inv['complete_hunks']):
 assert lines[h['new_start0']:h['new_end0']]==h['new_full_lines'];lines[h['new_start0']:h['new_end0']]=h['old_full_lines']
assert ''.join(lines)==old and ast.dump(ast.parse(''.join(lines)),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False)
fix=strict((F/'COMPLETE_TWO_EXACT_TOOL_WRAPPER_SCHEMA_FIX_SOURCE_INVERSE.json').read_bytes());op=fix['old_full_Source_pin'];np=fix['new_full_Source_pin'];assert pin(Path(op['path']))==op and pin(Path(np['path']))==np
old=Path(op['path']).read_text();restored=Path(np['path']).read_text()
for row in reversed(fix['complete_replacements']):assert restored.count(row['new'])==row['count'];restored=restored.replace(row['new'],row['old'])
assert restored==old and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False)
first=strict((F/'ACTUAL_FIRST_OWN_REVIEW_TOOL_WRAPPER_SCHEMA_MISMATCH_TOOL_RETURN.json').read_bytes());ft=first['terminal_tool_return'];fo=strict(ft['output']);frp=fix['actual_first_review_report_original_pin'];assert pin(Path(frp['path']))==frp and fo['review_pin']==frp
assert first['source_only']is True and first['closed']is True and first['observed_terminal']is True and first['session_repolled_after_close']is False and type(ft['exit_code'])is int and ft['exit_code']==0 and 'session_id'not in ft and ft['chunk_id']=='f9d540'and fo['all_checks_passed']is False and fo['check_count']==4299 and fo['blockers']==first['actual_Source_review_blockers']and first['candidate_guard_API_compile_native_or_material_executed']is False
assert pin(F/'ACTUAL_FIRST_OWN_REVIEW_OLD_WRAPPER_SCHEMA_MISMATCH_REPORT.json')['sha256']==frp['sha256']
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
v=dict(schema='INDEPENDENT_ACTUAL_N7_BOUND_SOURCE_META_PRELAUNCH_REVIEW_MANIFEST_V1',status='SEALED_ACTUAL_BOUND_SOURCE_META_PRELAUNCH_NO_EXECUTION_OR_SCIENCE',source_only=True,members=members,member_count=len(members),file_count_including_manifest=len(members)+1,directory_count=len(dirs),complete_directory_identity=dirs,review_pin=rp,actual_review_terminal_chunk=t['chunk_id'],actual_review_tool_receipt_pin=pin(F/'ACTUAL_INDEPENDENT_REVIEW_TOOL_RETURN.json'),complete_py_AST_count=py_count,independent_Source_META_checks=n,actual_namespace_pins=r['actual_namespace_pins'],actual_candidate_execution=False,scientific_qualification_created=False)
with mf.open('w')as stream:json.dump(v,stream,indent=2,allow_nan=False);stream.write('\n')
assert dirs=={str(p.relative_to(F)):ident(p)for p in [F,*sorted(F.rglob('*'))]if p.is_dir()}
for row in members:assert pin(Path(row['fullpin']['path']))==row['fullpin']
print(json.dumps(dict(status=v['status'],source_only=True,manifest_pin=pin(mf),review_pin=rp,members=len(members),files=len(members)+1,directories=len(dirs),checks=n,blockers=[],actual_candidate_execution=False),allow_nan=False))
