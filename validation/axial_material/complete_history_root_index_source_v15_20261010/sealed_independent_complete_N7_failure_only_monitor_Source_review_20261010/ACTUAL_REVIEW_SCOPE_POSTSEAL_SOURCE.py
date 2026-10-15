import ast,hashlib,json,os,stat
from pathlib import Path
F=Path('/private/tmp/axmat_N7_complete_Source_independent_xxd8yrrc')
S=Path(str(F)+'_seal_receipt')
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
mp=pin(F/'MANIFEST.json');m=strict((F/'MANIFEST.json').read_bytes());rp=pin(F/'REVIEW.json');r=strict((F/'REVIEW.json').read_bytes())
assert m['schema']=='INDEPENDENT_COMPLETE_NATIVE_OBSERVATION_SOURCE_REVIEW_MANIFEST_V1'and m['status']=='SEALED_SOURCE_ONLY_PASS_NO_RUNTIME_OR_SCIENCE_CREDIT'and m['source_only']is True and m['review_pin']==rp
assert r['schema']=='INDEPENDENT_COMPLETE_NATIVE_OBSERVATION_BUILD_HOST_BINDER_SOURCE_REVIEW_V1'and r['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'and r['source_only']is True and r['all_checks_passed']is True and r['all_checks_typed_true']is True and r['blockers']==[]
checks=r['checks'];assert type(r['check_count'])is int and r['check_count']==len(checks)==5213 and len({c['check']for c in checks})==5213 and all(set(c)=={'check','passed'}and type(c['check'])is str and c['check']and type(c['passed'])is bool and c['passed']is True for c in checks)
members=m['members'];assert type(m['member_count'])is int and len(members)==m['member_count']and len({c['relative_path']for c in members})==len(members)
assert {str(p.relative_to(F))for p in F.rglob('*')if p.is_file()}=={c['relative_path']for c in members}|{'MANIFEST.json'}
py_count=0
for row in members:
 q=row['fullpin'];p=Path(q['path']);assert p==F/row['relative_path']and pin(p)==q
 if p.suffix=='.py':ast.parse(p.read_bytes(),filename=str(p));py_count+=1
 if p.suffix=='.json':strict(p.read_bytes())
dirs={str(p.relative_to(F)):ident(p)for p in [F,*sorted(F.rglob('*'))]if p.is_dir()};assert dirs==m['complete_directory_identity']and len(dirs)==m['directory_count']
for q in r['actual_author_Source_contract'].values():assert pin(Path(q['path']))==q
author_root=Path(r['actual_author_Source_contract']['qualified_source_manifest']['path']).parent
author_manifest=strict((author_root/'MANIFEST.json').read_bytes())
for row in author_manifest['members']:assert pin(Path(row['fullpin']['path']))==row['fullpin']
assert {str(p.relative_to(author_root))for p in author_root.rglob('*')if p.is_file()}=={row['relative_path']for row in author_manifest['members']}|{'MANIFEST.json'}
assert {str(p):ident(p)for p in [author_root,*sorted(author_root.rglob('*'))]if p.is_dir()}==author_manifest['complete_directory_identity']
seal_pin=pin(S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json');seal=strict((S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json').read_bytes());t=seal['terminal_tool_return'];out=strict(t['output']);assert seal['source_only']is True and seal['closed']is True and seal['observed_terminal']is True and seal['session_repolled_after_close']is False and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t and t['chunk_id']==seal['actual_terminal_chunk']
assert out['status']=='SEALED_SOURCE_ONLY_PASS_NO_RUNTIME_OR_SCIENCE_CREDIT'and out['source_only']is True and out['manifest_pin']==mp and out['review_pin']==rp and out['members']==m['member_count']and out['files']==m['file_count_including_manifest']and out['directories']==m['directory_count']and out['blockers']==[]and out['actual_candidate_execution']is False
review=strict((F/'ACTUAL_INDEPENDENT_REVIEW_TOOL_RETURNS.json').read_bytes());rt=review['terminal_tool_return'];assert type(rt['exit_code'])is int and rt['exit_code']==0 and 'session_id'not in rt and rt['chunk_id']==review['actual_terminal_chunk']=='3de872'
assert pin(F/'MANIFEST.json')==mp and pin(F/'REVIEW.json')==rp and pin(S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json')==seal_pin
value=dict(schema='INDEPENDENT_COMPLETE_NATIVE_OBSERVATION_SOURCE_FULL_POSTSEAL_V1',status='FULL_SOURCE_POSTSEAL_VERIFIED_SOURCE_ONLY_NOT_ROOT_ADMITTED',source_only=True,manifest_pin=mp,review_pin=rp,full_file_count_including_manifest=len(members)+1,member_count=len(members),directory_count=len(dirs),checks=5213,check_count=5213,blockers=0,all_review_package_members_full_EOF_SHA7ID_verified=True,all_original_author_members_full_EOF_SHA7ID_and_directories_unchanged=True,complete_review_package_file_count=len(members)+1,complete_review_package_directory_count=len(dirs),independent_aggregate_Source_checks=5213,all_member_full_EOF_SHA7ID_and_all_directory_identity_verified=True,complete_retained_py_AST_count=py_count,actual_review_terminal_chunk=rt['chunk_id'],actual_seal_terminal_chunk=t['chunk_id'],actual_seal_receipt_pin=seal_pin,actual_candidate_guard_API_compile_native_or_numeric_executed=False,scientific_qualification_created=False)
q=S/'FULL_SOURCE_POSTSEAL_VERIFICATION.json'
with q.open('x')as stream:json.dump(value,stream,indent=2,allow_nan=False);stream.write('\n')
assert dirs=={str(p.relative_to(F)):ident(p)for p in [F,*sorted(F.rglob('*'))]if p.is_dir()}and pin(F/'MANIFEST.json')==mp
print(json.dumps(dict(status='FULL_SOURCE_POSTSEAL_VERIFIED_SOURCE_ONLY_NOT_ROOT_ADMITTED',source_only=True,manifest_pin=mp,review_pin=rp,actual_candidate_execution=False,postseal_verification_pin=pin(q),members=len(members),files=len(members)+1,directories=len(dirs),checks=5213,blockers=[]),allow_nan=False))
