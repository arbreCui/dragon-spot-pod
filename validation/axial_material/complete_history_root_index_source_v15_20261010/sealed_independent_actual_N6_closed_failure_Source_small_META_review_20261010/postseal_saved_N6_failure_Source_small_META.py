import ast,hashlib,json,stat
from pathlib import Path
F=Path('/private/tmp/axmat_N6_actual_closed_failure_small_META_LIFTx6');S=Path(str(F)+'_seal_receipt')
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
mp=pin(F/'MANIFEST.json');m=strict((F/'MANIFEST.json').read_bytes());rp=pin(F/'REVIEW.json');r=strict((F/'REVIEW.json').read_bytes());assert m['review_pin']==rp and m['source_only']is True and r['all_checks_typed_true']is True and r['check_count']==242 and r['blockers']==[]
members=m['members'];assert len(members)==m['member_count']and len({q['relative_path']for q in members})==len(members)and{str(p.relative_to(F))for p in F.rglob('*')if p.is_file()}=={q['relative_path']for q in members}|{'MANIFEST.json'}
for row in members:
 p=F/row['relative_path'];assert pin(p)==row['fullpin']
 if p.suffix=='.py':ast.parse(p.read_bytes(),filename=str(p))
 if p.suffix=='.json':strict(p.read_bytes())
dirs={str(p.relative_to(F)):ident(p)for p in [F,*sorted(F.rglob('*'))]if p.is_dir()};assert dirs==m['complete_directory_identity']
for tag,wanted in r['actual_current_namespace_metadata_after'].items():
 root=Path(min(wanted['directories'],key=lambda s:len(Path(s).parts)));assert view(root)==wanted
for row in r['finite_whole_saved_Source_and_small_META_copies'].values():assert pin(Path(row['actual_original_pin']['path']))==row['actual_original_pin']
sealpin=pin(S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json');seal=strict((S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json').read_bytes());t=seal['terminal_tool_return'];out=strict(t['output']);assert seal['closed']is True and seal['observed_terminal']is True and seal['session_repolled_after_close']is False and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t and t['chunk_id']==seal['actual_terminal_chunk']and out['manifest_pin']==mp and out['review_pin']==rp and out['files']==len(members)+1 and out['directories']==len(dirs)and out['checks']==242 and out['blockers']==[]and out['actual_candidate_execution']is False
v=dict(schema='INDEPENDENT_ACTUAL_CLOSED_N6_FAILURE_SOURCE_SMALL_META_FULL_POSTSEAL_V1',status='FULL_POSTSEAL_VERIFIED_SAVED_FAILED_N6_SOURCE_SMALL_META_ONLY_NO_RUNTIME_OR_SCIENCE',source_only=True,manifest_pin=mp,review_pin=rp,complete_package_file_count=len(members)+1,complete_package_directory_count=len(dirs),checks=242,blockers=[],all_independent_package_Source_META_full_EOF_SHA7ID_verified=True,original_frozen_D157_E5_complete_current7ID_and_directory_identity_unchanged=True,actual_review_terminal_chunk='77bcdb',actual_seal_terminal_chunk=t['chunk_id'],actual_seal_receipt_pin=sealpin,actual_saved_runtime_exit_code=1,actual_original_compiler_group_cleanup_verified=False,actual_saved_later_process_group_absent=True,actual_candidate_execution=False,scientific_qualification_created=False)
q=S/'FULL_SOURCE_POSTSEAL_VERIFICATION.json'
with q.open('x')as stream:json.dump(v,stream,indent=2,allow_nan=False);stream.write('\n')
assert pin(F/'MANIFEST.json')==mp and pin(F/'REVIEW.json')==rp and dirs=={str(p.relative_to(F)):ident(p)for p in [F,*sorted(F.rglob('*'))]if p.is_dir()}
print(json.dumps(dict(status=v['status'],source_only=True,manifest_pin=mp,review_pin=rp,postseal_verification_pin=pin(q),files=len(members)+1,directories=len(dirs),checks=242,blockers=[],actual_candidate_execution=False),allow_nan=False))
