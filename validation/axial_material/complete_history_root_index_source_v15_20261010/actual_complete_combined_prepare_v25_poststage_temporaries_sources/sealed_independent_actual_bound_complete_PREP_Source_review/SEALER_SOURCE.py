"""Finite own Source peer seal/postseal; no candidate or project execution."""
import hashlib,json,stat,sys
from pathlib import Path
Q=Path(__file__).resolve().parent
def identity(p):
 s=p.lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);before=identity(p)
 if not p.is_absolute()or any(x.is_symlink()for x in(p,*p.parents))or not stat.S_ISREG(before[2])or before[3]!=1:raise ValueError('Source META singlelink')
 with p.open('rb')as f:d=hashlib.file_digest(f,'sha256').hexdigest()
 if identity(p)!=before:raise ValueError('Source META fullEOF7ID changed')
 return dict(path=str(p),sha256=d,size_bytes=before[4],identity=before)
def load(p):
 p=Path(p);before=pin(p);v=json.loads(p.read_bytes())
 if pin(p)!=before:raise ValueError('Source META changed after parse')
 return v
def directories(p):return{'.':identity(p),**{str(q.relative_to(p)):identity(q)for q in p.rglob('*')if q.is_dir()}}
def files(p):return{str(q.relative_to(p)):pin(q)for q in p.rglob('*')if q.is_file()}
def original_scope(r):
 P=Path(r['actual_complete_bound_Source_manifest_pin']['path']).parent
 view=dict(directories=directories(P),files=files(P))
 if view!=r['complete_bound_Source_snapshot_before_and_after']:raise ValueError('complete actual original READYSource changed')
 for v in r['finite_retention_ledger'].values():
  if pin(v['original']['path'])!=v['original']or pin(v['saved']['path'])!=v['saved']:raise ValueError('finite lossless Source provenance changed')
 return view
def main():
 mode=sys.argv[1];report=load(Q/'REVIEW.json');record=load(Q/'ACTUAL_INDEPENDENT_REVIEW_TOOL_RETURN.json');tr=record['terminal_tool_return'];raw=json.loads(tr['output'])
 if not(report['source_only']is True and report['all_checks_typed_true']is True and report['blockers']==[]and report['check_count']==len(report['checks'])==24 and all(type(c['passed'])is bool and c['passed']is True for c in report['checks'])and record['closed']is True and record['observed_terminal']is True and type(tr['exit_code'])is int and tr['exit_code']==0 and 'session_id'not in tr and tr['chunk_id']=='cc0055'and raw['report_pin']==pin(Q/'REVIEW.json')):raise ValueError('genuine own Source review strict0 complete typed24')
 original_scope(report)
 if mode=='seal':
  mf=Q/'MANIFEST.json'
  with mf.open('xb')as f:f.write(b'')
  members={k:v for k,v in files(Q).items()if k!='MANIFEST.json'};ds=directories(Q)
  value=dict(schema='INDEPENDENT_ACTUAL_V25_POSTSTAGE_PREP_BOUND_SOURCE_REVIEW_MANIFEST_V1',status='SEALED_SOURCE_ONLY_ACTUAL_BINDING_REVIEW_NO_EXECUTION_OR_RSS_OR_SCIENCE',source_only=True,members=members,directories=ds,member_count=len(members),file_count_including_manifest=len(members)+1,directory_count=len(ds),review_pin=pin(Q/'REVIEW.json'),actual_review_tool_truth_pin=pin(Q/'ACTUAL_INDEPENDENT_REVIEW_TOOL_RETURN.json'),actual_complete_bound_Source_manifest_pin=report['actual_complete_bound_Source_manifest_pin'],check_count=24,blockers=[],candidate_binder_helper_guard_API_compile_native_material_numeric_or_Rootwriter_executed=False,whole_build_INPUT_RSS_science_qualified=False)
  with mf.open('wb')as f:f.write((json.dumps(value,indent=2,allow_nan=False)+'\n').encode())
  if directories(Q)!=ds:raise ValueError('Source review dirs changed at seal')
 elif mode=='postseal':
  value=load(Q/'MANIFEST.json');members=value['members']
  if files(Q)!={**members,'MANIFEST.json':pin(Q/'MANIFEST.json')}or directories(Q)!=value['directories']:raise ValueError('all sealed Source EOF7ID namespace unchanged')
 else:raise ValueError('fixed seal or postseal own Source mode')
 print(json.dumps(dict(status='SEALED_ACTUAL_PREP_BOUND_SOURCE_ONLY'if mode=='seal'else'POSTSEAL_FULL_SOURCE_AND_ORIGINAL_READY_NAMESPACE_VERIFIED',source_only=True,manifest_pin=pin(Q/'MANIFEST.json'),review_pin=pin(Q/'REVIEW.json'),actual_complete_bound_Source_manifest_pin=report['actual_complete_bound_Source_manifest_pin'],member_count=value['member_count'],file_count=value['file_count_including_manifest'],directory_count=value['directory_count'],check_count=24,blockers=[],candidate_or_guard_or_RSS_or_science_execution=False),allow_nan=False),flush=True)
if __name__=='__main__':main()
