"""Own postseal verification. Packet EOF and original HOCDE/input metadata only."""
import ast,hashlib,json,stat,sys
from pathlib import Path
F=Path('/private/tmp/axmat_N7_actual_closed_failure_Source_small_META_1zi95nma')
S=Path(str(F)+'_seal_receipt')
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
def metadata_view(p):
 files={};dirs={};seen=set()
 for q in [p,*sorted(p.rglob('*'))]:
  i=identity(q);assert not stat.S_ISLNK(i[2])
  if stat.S_ISDIR(i[2]):dirs[str(q)]=i
  else:
   assert stat.S_ISREG(i[2])and i[3]==1 and (i[0],i[1])not in seen;seen.add((i[0],i[1]));files[str(q)]=i
 return dict(root=str(p),files=files,directory_identity=dirs,total_bytes=sum(i[4]for i in files.values()))
def main():
 assert len(sys.argv)==1 and not sys.flags.optimize
 sealpath=S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json';seal=strict(sealpath.read_bytes());actual=seal['actual_tool_return']
 assert seal['closed']is True and seal['observed_terminal']is True and type(actual['exit_code'])is int and actual['exit_code']==0 and 'session_id'not in actual
 parsed=strict(actual['output']);mf=F/'MANIFEST.json';m=strict(mf.read_bytes());rp=pin(F/'REVIEW.json');report=strict((F/'REVIEW.json').read_bytes())
 assert pin(mf)==parsed['manifest_pin']and rp==parsed['review_pin']==m['review_pin']
 members=m['members'];assert len(members)==29 and m['file_count_including_manifest']==parsed['file_count_including_manifest']==30 and m['directory_count']==parsed['directory_count']==2
 files=[];dirs={};seen=set();pycount=0
 for p in [F,*sorted(F.rglob('*'))]:
  i=identity(p);assert not stat.S_ISLNK(i[2])
  if stat.S_ISDIR(i[2]):dirs[str(p.relative_to(F))]=i
  else:
   assert (i[0],i[1])not in seen;seen.add((i[0],i[1]));files.append(str(p.relative_to(F)))
   if p!=mf:assert pin(p)==members[str(p.relative_to(F))]
   if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p));pycount+=1
 assert set(files)==set(members)|{'MANIFEST.json'}and list(dirs)==m['directories']and dirs==parsed['complete_directory_identity_after_manifest']
 assert pycount==m['complete_py_AST_count']==parsed['complete_py_AST_count']and report['check_count']==18 and report['blockers']==[]and report['all_checks_typed_true']is True
 for v in report['actual_independent_current_metadata_views_after'].values():assert metadata_view(Path(v['root']))==v
 for q in report['all_154_ordered_protected_input_pins']:assert identity(Path(q['path']))==q['identity']
 for q in report['actual_reviewed_Source_small_META_original_pins'].values():assert identity(Path(q['path']))==q['identity']
 out=S/'FULL_SOURCE_SMALL_META_POSTSEAL_VERIFICATION.json';assert not out.exists()
 result=dict(schema='INDEPENDENT_ACTUAL_N7_FAILED_SOURCE_SMALL_META_FULL_POSTSEAL_V1',status='PASS_COMPLETE_SAVED_FAILED_SOURCE_SMALL_META_POSTSEAL_ONLY',source_only=True,all_checks_typed_true=True,blockers=[],qualified_manifest_pin=pin(mf),qualified_review_pin=rp,actual_seal_tool_receipt_pin=pin(sealpath),actual_review_terminal_chunk='3fdbd6',actual_seal_terminal_chunk=actual['chunk_id'],complete_file_count=30,complete_directory_count=2,complete_py_AST_count=pycount,independent_checks=18,all_packet_members_full_EOF_SHA_size_7ID_unchanged=True,complete_packet_directory7IDs_unchanged=True,all_original_H_O_C_D_E_metadata_views_unchanged=True,all_154_current_protected_input7IDs_unchanged=True,no_candidate_guard_API_PS_lsof_native_compile_material_numeric_executed=True,native_RSS_verified=False,native_build_qualified=False,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,goal_complete=False,original_N6_raw_cause_unknown=True,original_N7_process_state_and_lsof_cause_unknown=True,failed_current_open_unlinked_bytes=None)
 out.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
 assert pin(mf)==parsed['manifest_pin']and pin(F/'REVIEW.json')==rp
 print(json.dumps(dict(status=result['status'],manifest_pin=pin(mf),review_pin=rp,verification_pin=pin(out),complete_file_count=30,complete_directory_count=2,complete_py_AST_count=pycount,independent_checks=18,blockers=[],native_or_science_qualification=False),allow_nan=False))
if __name__=='__main__':main()
