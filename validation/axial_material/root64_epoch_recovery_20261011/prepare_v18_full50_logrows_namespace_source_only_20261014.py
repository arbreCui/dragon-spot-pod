"""Mechanical Source repair only; no compiler, solver, science reader or unlink."""
import ast,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=R/'aaa_three_plane_A8_owned_MAP_pipeline_source_v17_20261014'
NEW=R/'aaa_three_plane_A8_owned_MAP_pipeline_source_v18_20261014'
NEWOUT=Path('/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-A8-owned-MAP-20261014-v18')
FAIL=R/'ROOT_ACTUAL_V17_A8_OWNED_MAP_FULL50_PREOUTPUT_BINDING_FAILURE_TRUE_TOOL_RETURNS_20261014.json'
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);s=p.lstat()
 if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('bounded regular Source metadata')
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
  if ident(os.fstat(f.fileno()))!=ident(s):raise RuntimeError('opened7')
  data=f.read()
  if ident(os.fstat(f.fileno()))!=ident(s):raise RuntimeError('EOF7')
 if ident(p.lstat())!=ident(s):raise RuntimeError('after7')
 return dict(path=str(p),sha256=hashlib.sha256(data).hexdigest(),size_bytes=len(data),identity=ident(s))
def read(p):pin(p);return json.loads(Path(p).read_bytes())
def write(p,v):
 data=v if isinstance(v,bytes)else(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
 with os.fdopen(os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644),'wb')as f:f.write(data);f.flush();os.fsync(f.fileno())
 return pin(p)
def unique(rows):
 out={}
 for p in rows:
  if p['path']in out and out[p['path']]!=p:raise RuntimeError('one current PF per path')
  out[p['path']]=p
 return list(out.values())
def main():
 if NEW.exists()or NEWOUT.exists():raise RuntimeError('one new Source namespace; business OUT absent')
 before=(OLD/'run_actual_three_plane_pipeline.py').read_bytes();text=before.decode();changes=[]
 a="    rows,logpin=compact_log_rows(root,report,command)\n    completion=owned_runtime_completion_log('\\n'.join(rows))"
 b="    logrows,logpin=compact_log_rows(root,report,command)\n    completion=owned_runtime_completion_log('\\n'.join(logrows))"
 for old,new in [(a,b),('20261014-v17\'','20261014-v18\'')]:
  if text.count(old)!=1:raise RuntimeError('unique exact repair splice: '+old)
  text=text.replace(old,new,1);changes.append(dict(before=old,after=new,reason='preserve authority rows dict; log local renamed, or new output namespace only'))
 restored=text
 for c in reversed(changes):
  if restored.count(c['after'])!=1:raise RuntimeError('exact inverse splice')
  restored=restored.replace(c['after'],c['before'],1)
 if restored.encode()!=before:raise RuntimeError('whole v17 byte inverse')
 ast.parse(text);prior=read(OLD/'ACTUAL_OWNED_RUNTIME_BOUND_V17_SOURCE_PREPARATION_PLAN.json');oldhf=read(OLD/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json');oldinv=read(OLD/'COMPLETE_V16_TO_V17_OWNED_RUNTIME_ADMISSION_WHOLE_BYTE_INVERSE.json')
 if len(oldhf['dependencies'])!=3939 or prior['host_source']!=pin(OLD/'run_actual_three_plane_pipeline.py'):raise RuntimeError('exact frozen v17 current3939 Source lineage')
 fail=read(FAIL)
 if fail['observed_closed']is not True or fail['original_integer_exit_code']!=1:raise RuntimeError('actual preoutput failure original Root1 retained')
 if any(ident(Path(p['path']).lstat())!=p['identity']for p in oldhf['dependencies']):raise RuntimeError('original3939 current7')
 NEW.mkdir();host=write(NEW/'run_actual_three_plane_pipeline.py',text.encode());helpers=[]
 for row in prior['helper_byte_equality']:
  p=Path(row['candidate_pin']['path']);raw=p.read_bytes()
  if pin(p)!=row['candidate_pin']:raise RuntimeError('whole original helper PF')
  helpers.append(dict(predecessor_pin=row['predecessor_pin'],candidate_pin=write(NEW/p.name,raw),whole_bytes_unchanged=True))
 direct=read(OLD/'DIRECT_ALIAS_ENTRY_BINDING.json');direct['new_probe_source']=str(NEW/'direct_alias_entry_controls.f90');pdir=write(NEW/'DIRECT_ALIAS_ENTRY_BINDING.json',direct)
 inv=dict(oldinv);inv['candidate_pin']=host;inv['changes']=oldinv['changes']+changes;inv['helpers']=helpers;inv['direct_binding_actual_pin']=pdir;inv['predecessor_v17_Host_source_pin']=prior['host_source'];inv['v17_to_v18_exact_two_splices']=changes;inv['v17_to_v18_whole_inverse_bytes_equal']=True
 pinv=write(NEW/'COMPLETE_V16_TO_V17_OWNED_RUNTIME_ADMISSION_WHOLE_BYTE_INVERSE.json',inv)
 deps=unique(oldhf['dependencies']+[pin(OLD/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json'),pin(OLD/'DECLARED_EXECUTION_INTERFACE.json'),pin(FAIL),pin(__file__),host,pdir,pinv]+[p['candidate_pin']for p in helpers])
 plan=dict(prior);plan.update(host_source=host,preparer_source_pin=pin(__file__),dependencies=deps,complete_byte_inverse_pin=pinv,direct_alias_binding_pin=pdir,helper_byte_equality=helpers,planned_output_root=str(NEWOUT),actual_Source_revision=18,predecessor_v17_Host_freeze_pin=pin(OLD/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json'),predecessor_v17_Host_source_pin=prior['host_source'],actual_v17_preoutput_binding_failure_pin=pin(FAIL),only_log_local_name_and_output_namespace_changed=True,original50_math_guards_caps_and14prefix96_unchanged=True)
 pp=write(NEW/'ACTUAL_OWNED_RUNTIME_BOUND_V17_SOURCE_PREPARATION_PLAN.json',plan)
 ready=dict(read(OLD/'SOURCE_REVIEW_READY.json'));ready.update(host_source=host,plan_pin=pp,inverse_pin=pinv,direct_binding_pin=pdir,helpers=helpers,actual_Source_revision=18,actual_Host_freeze_pin=None,actual_CLI_pin=None,actual_v17_report_pin=None)
 pr=write(NEW/'SOURCE_REVIEW_READY.json',ready)
 writer=(R/'write_once_v17_A8_owned_MAP_full50_HF_CLI_v2_20261014.py').read_bytes();wtext=writer.decode();old=str(OLD);new=str(NEW)
 if wtext.count(old)!=1:raise RuntimeError('writer one HERE namespace')
 newwriter=wtext.replace(old,new,1)
 if newwriter.replace(new,old,1).encode()!=writer:raise RuntimeError('writer whole inverse')
 ast.parse(newwriter);pw=write(R/'write_once_v18_A8_owned_MAP_full50_HF_CLI_v1_20261014.py',newwriter.encode())
 pwi=write(R/'COMPLETE_V17_TO_V18_ONCE_WRITER_NAMESPACE_INVERSE_20261014.json',dict(schema='COMPLETE_V17_TO_V18_ONCE_WRITER_NAMESPACE_INVERSE_V1',original_pin=pin(R/'write_once_v17_A8_owned_MAP_full50_HF_CLI_v2_20261014.py'),candidate_pin=pw,changes=[dict(before=old,after=new)],whole_inverse_bytes_equal=True,all_other_writer_Source_peer_gates_O_EXCL_fsync_current7_caps_and14prefix96_wholebytes_unchanged=True))
 print(json.dumps(dict(status='V18_LOGROWS_NAMESPACE_REPAIR_SOURCE_ONLY_CREATED',host_source=host,plan_pin=pp,inverse_pin=pinv,ready_pin=pr,writer_pin=pw,writer_inverse_pin=pwi,dependency_count=len(deps),compiler_executed=False,numerical_executed=False,pipeline_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()
