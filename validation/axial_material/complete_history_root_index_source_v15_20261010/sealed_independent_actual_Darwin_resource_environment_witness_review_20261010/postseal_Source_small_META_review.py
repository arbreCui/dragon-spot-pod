import ast,hashlib,json,stat,sys
from pathlib import Path
F=Path('/private/tmp/axmat_INDEPENDENT_Darwin_resource_environment_witness_puchj6jp');S=Path(str(F)+'_seal_receipt')
RESOURCE=Path('/Users/wen/miniforge3/envs/openmc-dev/lib/python3.12/lib-dynload/resource.cpython-312-darwin.so')
def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p,resource_endpoint=False):
 i=identity(p);assert p.is_absolute()and p.resolve()==p and stat.S_ISREG(i[2])
 if resource_endpoint:assert p==RESOURCE and i[3]==2
 else:assert i[3]==1
 h=hashlib.sha256();n=0
 with p.open('rb')as f:
  while True:
   r=f.read(2**20)
   if not r:break
   h.update(r);n+=len(r)
 assert n==i[4]and identity(p)==i
 return dict(path=str(p),sha256=h.hexdigest(),size_bytes=n,identity=i)
def strict(raw):
 def pairs(rows):
  d={}
  for k,v in rows:assert k not in d;d[k]=v
  return d
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in()).throw(ValueError(x)))
def main():
 assert len(sys.argv)==1 and not sys.flags.optimize
 sp=S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json';seal=strict(sp.read_bytes());actual=seal['actual_tool_return']
 assert seal['closed']is True and seal['observed_terminal']is True and type(actual['exit_code'])is int and actual['exit_code']==0 and 'session_id'not in actual
 parsed=strict(actual['output']);mf=F/'MANIFEST.json';m=strict(mf.read_bytes());rp=pin(F/'REVIEW.json');report=strict((F/'REVIEW.json').read_bytes())
 assert pin(mf)==parsed['manifest_pin']and rp==parsed['review_pin']==m['review_pin']
 files=[];dirs={};seen=set();pycount=0
 for p in [F,*sorted(F.rglob('*'))]:
  i=identity(p);assert not stat.S_ISLNK(i[2])
  if stat.S_ISDIR(i[2]):dirs[str(p.relative_to(F))]=i
  else:
   assert (i[0],i[1])not in seen;seen.add((i[0],i[1]));files.append(str(p.relative_to(F)))
   if p!=mf:assert pin(p)==m['members'][str(p.relative_to(F))]
   if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p));pycount+=1
 assert set(files)==set(m['members'])|{'MANIFEST.json'}and len(files)==16 and len(dirs)==2 and list(dirs)==m['directories']and dirs==parsed['complete_directory_identity_after_manifest']
 assert pycount==m['complete_py_AST_count']==parsed['complete_py_AST_count']and report['check_count']==11 and report['all_checks_typed_true']is True and report['blockers']==[]
 for q in report['all_original_read_Source_small_META_and_environment_fullpins'].values():assert pin(Path(q['path']),resource_endpoint=Path(q['path'])==RESOURCE)==q
 result=dict(schema='INDEPENDENT_ACTUAL_DARWIN_RESOURCE_ENVIRONMENT_SOURCE_SMALL_META_FULL_POSTSEAL_V1',status='PASS_ACTUAL_ENVIRONMENT_DEPENDENCY_ONLY_FULL_POSTSEAL',source_only=True,all_checks_typed_true=True,blockers=[],qualified_manifest_pin=pin(mf),qualified_review_pin=rp,qualified_actual_witness_pin=report['qualified_actual_witness_pin'],actual_seal_tool_receipt_pin=pin(sp),actual_review_terminal_chunk='612e3d',actual_seal_terminal_chunk=actual['chunk_id'],complete_file_count=16,complete_directory_count=2,complete_py_AST_count=pycount,independent_checks=11,all_packet_members_full_EOF_SHA_size7ID_unchanged=True,complete_packet_directory7IDs_unchanged=True,all_original_Source_small_META_and_exact_Python_resource_endpoint_fullEOF7ID_unchanged=True,actual_resource_query_reexecuted=False,current_RSS_verified=False,genuine_guard_peak_verified=False,whole_BUILD_qualified=False,whole_INPUT_qualified=False,native_or_science_qualified=False,candidate_guard_binder_API_PS_lsof_compile_material_numeric_executed=False,project_or_parent_modified=False)
 out=S/'FULL_SOURCE_SMALL_META_POSTSEAL_VERIFICATION.json';assert not out.exists();out.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
 assert pin(mf)==parsed['manifest_pin']and pin(F/'REVIEW.json')==rp
 print(json.dumps(dict(status=result['status'],manifest_pin=pin(mf),review_pin=rp,verification_pin=pin(out),complete_file_count=16,complete_directory_count=2,complete_py_AST_count=pycount,independent_checks=11,blockers=[],actual_witness_pin=report['qualified_actual_witness_pin'],native_or_science_qualification=False),allow_nan=False))
if __name__=='__main__':main()
