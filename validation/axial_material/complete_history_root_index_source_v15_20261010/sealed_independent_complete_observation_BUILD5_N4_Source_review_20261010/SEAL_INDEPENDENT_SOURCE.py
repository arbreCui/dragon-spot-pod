import ast,hashlib,json,stat
from pathlib import Path
P=Path(__file__).parent
def ident(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 i=ident(p);assert p.resolve()==p and stat.S_ISREG(i[2])and i[3]==1
 with p.open('rb')as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 assert ident(p)==i;return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
def view(root):
 files={};dirs={'.':ident(root)}
 for p in sorted(root.rglob('*')):
  i=ident(p);assert not p.is_symlink();k=str(p.relative_to(root))
  if stat.S_ISREG(i[2]):files[k]=pin(p)
  else:assert stat.S_ISDIR(i[2]);dirs[k]=i
 for k,q in files.items():assert pin(root/k)==q
 for k,i in dirs.items():assert ident(root/k)==i
 return dict(files=files,directories=dirs,symlinks={})
r=json.loads((P/'REVIEW.json').read_text());rp=pin(P/'REVIEW.json');truth=json.loads((P/'ACTUAL_INDEPENDENT_REVIEW_TOOL_RETURNS.json').read_text());tr=truth['terminal_tool_return'];out=json.loads(tr['output'])
assert r['source_only']is True and r['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'and r['all_checks_passed']is True and r['all_checks_typed_true']is True and r['blockers']==[]and r['check_count']==len(r['checks'])==64
assert all(type(c['passed'])is bool and c['passed']is True for c in r['checks'])and len({c['check']for c in r['checks']})==64
assert truth['closed']is True and truth['observed_terminal']is True and type(tr['exit_code'])is int and tr['exit_code']==0 and 'session_id'not in tr and tr['chunk_id']=='6d2c39'and out['review_pin']==rp
N=Path(r['complete_reviewed_source_manifest_pin']['path']).parent;n=view(N);assert n['files']==r['complete_reviewed_source_namespace_after']['files']and n['directories']==r['complete_reviewed_source_namespace_after']['directories']
for q in r['actual_author_Source_contract'].values():assert pin(Path(q['path']))==q
for p in sorted(P.rglob('*.py')):ast.parse(p.read_bytes(),filename=str(p))
mf=P/'MANIFEST.json';assert not mf.exists();mf.touch();v=view(P);members=[dict(relative_path=k,fullpin=q)for k,q in v['files'].items()if k!='MANIFEST.json']
m=dict(schema='INDEPENDENT_COMPLETE_NATIVE_OBSERVATION_SOURCE_REVIEW_MANIFEST_V1',status='SEALED_SOURCE_ONLY_PASS_NO_RUNTIME_OR_SCIENCE_CREDIT',source_only=True,members=members,member_count=len(members),file_count_including_manifest=len(v['files']),directory_count=len(v['directories']),complete_directory_identity=v['directories'],review_pin=rp,actual_review_tool_truth_pin=pin(P/'ACTUAL_INDEPENDENT_REVIEW_TOOL_RETURNS.json'),actual_original_Source_manifest_pin=r['complete_reviewed_source_manifest_pin'],whole_original_native_Source_archive_members=1365,independent_aggregate_Source_checks=64,blocker_count=0,qualified_source_manifest=r['complete_reviewed_source_manifest_pin'],actual_Root_Source_admission=None,actual_native_execution=None,scientific_qualification_created=False)
with mf.open('w')as f:json.dump(m,f,indent=2,allow_nan=False);f.write('\n')
a=view(P);assert a['directories']==v['directories']and len(a['files'])==len(members)+1
for row in members:assert a['files'][row['relative_path']]==row['fullpin']
print(json.dumps(dict(status=m['status'],source_only=True,manifest_pin=pin(mf),review_pin=rp,members=len(members),files=len(a['files']),directories=len(a['directories']),blockers=0,actual_review_terminal_chunk='6d2c39',actual_candidate_execution=False)))
