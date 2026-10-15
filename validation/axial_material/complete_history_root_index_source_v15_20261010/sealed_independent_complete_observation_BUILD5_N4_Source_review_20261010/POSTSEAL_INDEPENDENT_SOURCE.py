import ast,hashlib,json,stat
from pathlib import Path
P=Path(__file__).parent;S=Path(str(P)+'_seal_receipt')
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
mfp=pin(P/'MANIFEST.json');m=json.loads((P/'MANIFEST.json').read_text());v=view(P);expected={q['relative_path']:q['fullpin']for q in m['members']}
assert set(v['files'])==set(expected)|{'MANIFEST.json'}and v['directories']==m['complete_directory_identity']and len(expected)==m['member_count']
for k,q in expected.items():assert v['files'][k]==q
r=json.loads((P/'REVIEW.json').read_text());rp=pin(P/'REVIEW.json');assert rp==m['review_pin']
N=Path(r['complete_reviewed_source_manifest_pin']['path']).parent;nv=view(N);assert nv['files']==r['complete_reviewed_source_namespace_after']['files']and nv['directories']==r['complete_reviewed_source_namespace_after']['directories']
seal=json.loads((S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json').read_text());tr=seal['terminal_tool_return'];ss=json.loads(tr['output'])
assert seal['closed']is True and seal['observed_terminal']is True and type(tr['exit_code'])is int and tr['exit_code']==0 and 'session_id'not in tr and ss['manifest_pin']==mfp and ss['review_pin']==rp
for p in sorted(P.rglob('*.py')):ast.parse(p.read_bytes(),filename=str(p))
proof=dict(schema='INDEPENDENT_COMPLETE_NATIVE_OBSERVATION_SOURCE_FULL_POSTSEAL_V1',status='FULL_SOURCE_POSTSEAL_VERIFIED_SOURCE_ONLY_NOT_ROOT_ADMITTED',source_only=True,manifest_pin=mfp,review_pin=rp,all_review_package_members_full_EOF_SHA7ID_verified=True,all_original_author_members_full_EOF_SHA7ID_and_directories_unchanged=True,complete_review_package_file_count=len(v['files']),complete_review_package_directory_count=len(v['directories']),independent_aggregate_Source_checks=r['check_count'],blockers=0,actual_review_terminal_chunk='6d2c39',actual_seal_terminal_chunk=tr['chunk_id'],actual_candidate_guard_API_compile_native_or_numeric_executed=False,scientific_qualification_created=False)
p=S/'FULL_SOURCE_POSTSEAL_VERIFICATION.json'
with p.open('x')as f:json.dump(proof,f,indent=2,allow_nan=False);f.write('\n')
assert pin(P/'MANIFEST.json')==mfp and view(P)==v
print(json.dumps(dict(status=proof['status'],source_only=True,manifest_pin=mfp,review_pin=rp,postseal_verification_pin=pin(p),files=len(v['files']),directories=len(v['directories']),independent_aggregate_Source_checks=r['check_count'],actual_candidate_execution=False)))
