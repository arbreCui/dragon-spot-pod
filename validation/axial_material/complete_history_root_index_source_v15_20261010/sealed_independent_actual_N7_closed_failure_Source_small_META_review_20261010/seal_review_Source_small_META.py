"""Own finite Source/small META sealing; no candidate or physical reads."""
import ast,hashlib,json,stat,sys
from pathlib import Path
F=Path('/private/tmp/axmat_N7_actual_closed_failure_Source_small_META_1zi95nma')
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
 target=F/'MANIFEST.json';assert not target.exists()
 report=strict((F/'REVIEW.json').read_bytes());rpin=pin(F/'REVIEW.json')
 tool=strict((F/'ACTUAL_REVIEW_TOOL_RETURN.json').read_bytes());actual=tool['actual_tool_return']
 assert tool['closed']is True and tool['observed_terminal']is True and actual['chunk_id']=='3fdbd6'and type(actual['exit_code'])is int and actual['exit_code']==0 and 'session_id'not in actual
 parsed=strict(actual['output']);assert parsed['review_pin']==rpin and parsed['check_count']==report['check_count']==18 and parsed['all_checks_typed_true']is True and parsed['blockers']==report['blockers']==[]
 assert report['source_only']is True and report['all_checks_typed_true']is True and len(report['checks'])==18 and all(c['passed']is True for c in report['checks'])and len({c['name']for c in report['checks']})==18
 members={};dirs=[];seen=set();pycount=0
 for p in [F,*sorted(F.rglob('*'))]:
  i=identity(p);assert not stat.S_ISLNK(i[2])
  if stat.S_ISDIR(i[2]):dirs.append(str(p.relative_to(F)))
  else:
   assert (i[0],i[1])not in seen;seen.add((i[0],i[1]));members[str(p.relative_to(F))]=pin(p)
   if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p));pycount+=1
 assert len(members)==29 and len(dirs)==2
 value=dict(schema='INDEPENDENT_ACTUAL_CLOSED_N7_FAILURE_SOURCE_SMALL_META_REVIEW_MANIFEST_V1',status=report['status'],source_only=True,members=members,directories=dirs,member_count=len(members),file_count_including_manifest=len(members)+1,directory_count=len(dirs),review_pin=rpin,actual_review_terminal_chunk='3fdbd6',actual_review_tool_receipt_pin=pin(F/'ACTUAL_REVIEW_TOOL_RETURN.json'),complete_py_AST_count=pycount,independent_checks=18,blockers=[],actual_saved_runtime_exit_code=1,original_cleanup_success_unknown=True,actual_current_groups_absent_at_saved_later_check=True,candidate_guard_API_native_compile_material_or_diagnostic_executed_by_reviewer=False,scientific_qualification_created=False,manifest_directory_identity_policy='Names frozen in manifest; exact complete directory7IDs after manifest creation retained in genuine seal stdout and verified postseal, avoiding self-append identity cycle')
 target.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
 for q in members.values():assert pin(Path(q['path']))==q
 directories={str(p.relative_to(F)):identity(p)for p in [F,*sorted(F.rglob('*'))]if p.is_dir()}
 assert list(directories)==dirs
 print(json.dumps(dict(status='SEALED_SAVED_FAILED_N7_SOURCE_SMALL_META_ONLY',manifest_pin=pin(target),review_pin=rpin,member_count=len(members),file_count_including_manifest=len(members)+1,directory_count=len(dirs),complete_directory_identity_after_manifest=directories,complete_py_AST_count=pycount,independent_checks=18,blockers=[],actual_review_terminal_chunk='3fdbd6',native_or_science_qualification=False),allow_nan=False))
if __name__=='__main__':main()
