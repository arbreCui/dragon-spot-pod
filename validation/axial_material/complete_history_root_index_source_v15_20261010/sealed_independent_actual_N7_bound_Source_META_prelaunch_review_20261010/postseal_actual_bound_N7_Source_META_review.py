import ast,hashlib,json,os,stat
from pathlib import Path
F=Path('/private/tmp/axmat_N7_actual_bound_Source_prelaunch_V2_im4o9o48');S=Path(str(F)+'_seal_receipt')
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
mp=pin(F/'MANIFEST.json');m=strict((F/'MANIFEST.json').read_bytes());rp=pin(F/'REVIEW.json');r=strict((F/'REVIEW.json').read_bytes())
assert m['review_pin']==rp and r['source_only']is True and r['all_checks_passed']is True and r['all_checks_typed_true']is True and r['blockers']==[]and m['independent_Source_META_checks']==r['check_count']
n=r['check_count'];members=m['members'];assert len(members)==m['member_count']and len({c['relative_path']for c in members})==len(members)and {str(p.relative_to(F))for p in F.rglob('*')if p.is_file()}=={c['relative_path']for c in members}|{'MANIFEST.json'}
for row in members:
 p=F/row['relative_path'];assert pin(p)==row['fullpin']
 if p.suffix=='.py':ast.parse(p.read_bytes(),filename=str(p))
 if p.suffix=='.json':strict(p.read_bytes())
dirs={str(p.relative_to(F)):ident(p)for p in [F,*sorted(F.rglob('*'))]if p.is_dir()};assert dirs==m['complete_directory_identity']
for key,view in r['actual_namespace_pins'].items():
 root=Path(next(p for p in view['directories']if len(Path(p).parts)==min(len(Path(v).parts)for v in view['directories'])))
 assert tree(root)==view
req=strict(Path(r['actual_Root_request_pin']['path']).read_bytes());assert all(not os.path.lexists(req['namespaces'][k])for k in ('host','output','control'))
seal_pin=pin(S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json');seal=strict((S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json').read_bytes());t=seal['terminal_tool_return'];out=strict(t['output'])
assert seal['source_only']is True and seal['closed']is True and seal['observed_terminal']is True and seal['session_repolled_after_close']is False and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t and t['chunk_id']==seal['actual_terminal_chunk']and out['manifest_pin']==mp and out['review_pin']==rp and out['files']==len(members)+1 and out['directories']==len(dirs)and out['checks']==n and out['blockers']==[]and out['actual_candidate_execution']is False
v=dict(schema='INDEPENDENT_ACTUAL_N7_BOUND_SOURCE_META_PRELAUNCH_FULL_POSTSEAL_V1',status='FULL_POSTSEAL_VERIFIED_ACTUAL_BOUND_SOURCE_META_PRELAUNCH_NO_EXECUTION_OR_SCIENCE',source_only=True,manifest_pin=mp,review_pin=rp,complete_review_package_file_count=len(members)+1,complete_review_package_directory_count=len(dirs),checks=n,blockers=[],complete_actual_D_E_views_all_EOF_SHA7ID_and_directories_unchanged=True,actual_namespace_file_counts={k:len(w['files'])for k,w in r['actual_namespace_pins'].items()},actual_namespace_directory_counts={k:len(w['directories'])for k,w in r['actual_namespace_pins'].items()},actual_HOC_all_absent=True,actual_review_terminal_chunk=m['actual_review_terminal_chunk'],actual_seal_terminal_chunk=t['chunk_id'],actual_seal_receipt_pin=seal_pin,actual_candidate_execution=False,scientific_qualification_created=False)
q=S/'FULL_SOURCE_POSTSEAL_VERIFICATION.json'
with q.open('x')as stream:json.dump(v,stream,indent=2,allow_nan=False);stream.write('\n')
assert pin(F/'MANIFEST.json')==mp and pin(F/'REVIEW.json')==rp and dirs=={str(p.relative_to(F)):ident(p)for p in [F,*sorted(F.rglob('*'))]if p.is_dir()}
print(json.dumps(dict(status=v['status'],source_only=True,manifest_pin=mp,review_pin=rp,postseal_verification_pin=pin(q),files=len(members)+1,directories=len(dirs),checks=n,blockers=[],actual_candidate_execution=False),allow_nan=False))
