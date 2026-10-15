import ast,hashlib,json,stat,sys
from pathlib import Path
F=Path('/private/tmp/axmat_INDEPENDENT_Darwin_resource_environment_witness_puchj6jp')
def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 i=identity(p);assert p.resolve()==p and stat.S_ISREG(i[2])and i[3]==1
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
 out=F/'MANIFEST.json';assert not out.exists()
 report=strict((F/'REVIEW.json').read_bytes());rp=pin(F/'REVIEW.json');tool=strict((F/'ACTUAL_REVIEW_TOOL_RETURN.json').read_bytes());actual=tool['actual_tool_return']
 assert tool['closed']is True and tool['observed_terminal']is True and type(actual['exit_code'])is int and actual['exit_code']==0 and 'session_id'not in actual and actual['chunk_id']=='612e3d'
 parsed=strict(actual['output']);assert parsed['review_pin']==rp and parsed['check_count']==report['check_count']==11 and report['blockers']==[]and report['all_checks_typed_true']is True
 assert len(report['checks'])==11 and len({r['name']for r in report['checks']})==11 and all(r['passed']is True for r in report['checks'])
 members={};dirs=[];seen=set();pycount=0
 for p in [F,*sorted(F.rglob('*'))]:
  i=identity(p);assert not stat.S_ISLNK(i[2])
  if stat.S_ISDIR(i[2]):dirs.append(str(p.relative_to(F)))
  else:
   assert (i[0],i[1])not in seen;seen.add((i[0],i[1]));members[str(p.relative_to(F))]=pin(p)
   if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p));pycount+=1
 assert len(members)==15 and len(dirs)==2
 m=dict(schema='INDEPENDENT_ACTUAL_DARWIN_RESOURCE_ENVIRONMENT_WITNESS_SOURCE_SMALL_META_MANIFEST_V1',status=report['status'],source_only=True,members=members,directories=dirs,member_count=15,file_count_including_manifest=16,directory_count=2,review_pin=rp,actual_review_tool_receipt_pin=pin(F/'ACTUAL_REVIEW_TOOL_RETURN.json'),actual_review_terminal_chunk='612e3d',complete_py_AST_count=pycount,independent_checks=11,blockers=[],qualified_actual_witness_pin=report['qualified_actual_witness_pin'],diagnostic_dependency_only=True,actual_resource_QUERY_reexecuted_here=False,whole_BUILD_INPUT_native_or_science_qualified=False,manifest_directory_identity_policy='Relative names in manifest; exact directory7IDs after manifest creation saved in actual seal stdout and verified postseal')
 out.write_text(json.dumps(m,indent=2,allow_nan=False)+'\n')
 for q in members.values():assert pin(Path(q['path']))==q
 d={str(p.relative_to(F)):identity(p)for p in [F,*sorted(F.rglob('*'))]if p.is_dir()};assert list(d)==dirs
 print(json.dumps(dict(status='SEALED_ENVIRONMENT_DEPENDENCY_SOURCE_SMALL_META_ONLY',manifest_pin=pin(out),review_pin=rp,member_count=15,file_count_including_manifest=16,directory_count=2,complete_directory_identity_after_manifest=d,complete_py_AST_count=pycount,independent_checks=11,blockers=[],actual_review_terminal_chunk='612e3d',actual_witness_pin=report['qualified_actual_witness_pin'],native_or_science_qualification=False),allow_nan=False))
if __name__=='__main__':main()
