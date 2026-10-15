#!/usr/bin/env python3
"""Exclusive v5 Source fix for the original SerialExecutor record directory."""
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import stat

REC=Path(__file__).resolve().parent
SERIAL=REC/'streaming_full_ledger_serializer_min5_source_bundle_v1_20261013/runtime/production_runner.py'
FAIL_TOOL=REC/'ROOT_ACTUAL_COMPACT_BQ_MODEL_V4_RECORD_DIRECTORY_FAILURE_TRUE_TOOL_RETURNS_20261013.json'
FAIL_SUMMARY=Path('/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-private-GANLIB-model-controls-20261013-v4/Root_actual_control_summary.json')
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()
 b=p.read_bytes();assert len(b)==s.st_size and ids(p.lstat())==ids(s)
 return b,dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=ids(s))
def read(p):
 b,pf=pin(p);return json.loads(b),pf
def put(folder,name,value):
 b=value if isinstance(value,bytes)else(json.dumps(value,indent=2)+'\n').encode()
 p=folder/name;fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
 try:assert os.write(fd,b)==len(b);os.fsync(fd)
 finally:os.close(fd)
 assert pin(p)[0]==b;return pin(p)[1]
def main():
 serial,serialpf=pin(SERIAL);assert b'self.stages_path = work / case / "stages.json"'in serial
 fail,failpf=read(FAIL_SUMMARY);_,failtoolpf=pin(FAIL_TOOL)
 assert failpf['sha256']=='34c65012cf6444f03839792d9ccc6294fbe2fb1b7731cf67419757ab03298dbc'
 assert len(fail['records'])==1 and fail['records'][0]['status']=='RUNNING'
 assert not (FAIL_SUMMARY.parent/'build/control.o').exists()
 produced=[]
 for kind,stem,outstem in [('model','bq64_private_GANLIB_model_control_host','axial-material-new-BQ64-private-GANLIB-model-controls-20261013-'),('public','public_read_compact_bq_admission_control_host','axial-material-new-BQ64-genuine-public-READ-seven-controls-20261013-')]:
  oldfolder=REC/(stem+'_source_v4_20261013');newfolder=REC/(stem+'_source_v5_20261013')
  old,oldpf=pin(oldfolder/('run_guarded_'+kind+'_controls.py'))
  oldplan,oldplanpf=read(oldfolder/'EXACT_CONTROL_HOST_SOURCE_ONLY_PLAN.json')
  _,oldhfpf=pin(oldfolder/'COMPLETE_CONTROL_HOST_SOURCE_FREEZE.json')
  _,oldclipf=pin(oldfolder/'ROOT_REVIEWABLE_EXACT_CONTROL_ARGV_SOURCE_TEMPLATE.json')
  before=outstem+'v4';after=outstem+'v5'
  oldmkdir="    OUT.mkdir();(OUT/'runtime').mkdir();(OUT/'build').mkdir()\n"
  newmkdir=oldmkdir+"    (OUT/('compact-'+KIND+'-controls')).mkdir()\n"
  t=old.decode();assert t.count(before)==1 and t.count(oldmkdir)==1
  t=t.replace(before,after,1).replace(oldmkdir,newmkdir,1)
  back=t.replace(newmkdir,oldmkdir,1).replace(after,before,1);assert back.encode()==old
  tree=ast.parse(t);oldtree=ast.parse(old)
  def defs(raw,tr):return{x.name:ast.get_source_segment(raw,tr.body[i])for i,x in enumerate(tr.body)if isinstance(x,(ast.FunctionDef,ast.ClassDef))}
  a=defs(old.decode(),oldtree);b=defs(t,tree);assert a.keys()==b.keys()and all(a[k]==b[k]for k in a if k!='main')
  assert b['main'].replace(newmkdir.strip(),oldmkdir.strip(),1)==a['main']
  # Caller creates exactly the original work/case/stages.json parent before construction and execution.
  assert t.index(newmkdir)<t.index('runner=full.OwnRSSSerialExecutor(')<t.index('check();runner.execute(')
  assert "runner=full.OwnRSSSerialExecutor(OUT,1800-(time.monotonic()-start),'compact-'+KIND+'-controls',resources)"in t
  expected_stage_parent=Path(oldplan['planned_output_root'].removesuffix('v4')+'v5')/('compact-'+kind+'-controls')
  assert expected_stage_parent==Path('/Users/wen/spot/validation/artifacts/'+after)/('compact-'+kind+'-controls')
  assert not expected_stage_parent.parent.exists()
  newfolder.mkdir(exist_ok=False);hostpf=put(newfolder,'run_guarded_'+kind+'_controls.py',t.encode())
  plan=copy.deepcopy(oldplan);plan['host_source_pin']=hostpf;plan['planned_output_root']=str(expected_stage_parent.parent)
  changed={k:oldplan[k]for k in oldplan if oldplan[k]!=plan[k]};assert set(changed)=={'host_source_pin','planned_output_root'}
  restored=copy.deepcopy(plan);restored.update(changed);assert restored==oldplan
  planpf=put(newfolder,'EXACT_CONTROL_HOST_SOURCE_ONLY_PLAN.json',plan)
  invpf=put(newfolder,'COMPLETE_V4_TO_V5_RECORD_DIRECTORY_HOST_PLAN_INVERSE.json',dict(
    schema='COMPLETE_COMPACT_BQ_CONTROL_HOST_V4_TO_V5_RECORD_DIRECTORY_WHOLE_INVERSE_V1',
    source_only=True,original_host_pin=oldpf,new_host_pin=hostpf,
    original_plan_pin=oldplanpf,new_plan_pin=planpf,host_exact_splices=[dict(before=before,after=after),dict(before=oldmkdir,after=newmkdir)],
    complete_original_host_whole_byte_inverse_observed=True,exact_original_plan_changed_fields=changed,
    complete_original_plan_canonical_data_inverse_observed=True,
    original_guard_serializer_budget_Fortran_math_oracles_flags_firsterror_bytes_unchanged=True,
    old_Host_source_freeze_pin=oldhfpf,old_argv_Source_template_pin=oldclipf,
    actual_failed_model4_summary_pin=failpf,actual_failed_model4_true_tool_return_pin=failtoolpf,
    old_failed_output_unmodified=True,public_v4_never_run=True,compiler_executed=False,numerical_executed=False))
  proof=put(newfolder,'AUTHOR_STATIC_ORIGINAL_SERIAL_EXECUTOR_RECORD_DIRECTORY_SOURCE_PROOF.json',dict(
    schema='COMPACT_BQ_CONTROL_HOST_ORIGINAL_SERIAL_RECORD_DIRECTORY_CALLER_SOURCE_PROOF_V1',
    status='PASS_SOURCE_ONLY_EXACT_ORIGINAL_STAGES_PARENT_PRECREATED',kind=kind,
    original_SerialExecutor_Source_pin=serialpf,caller_Source_pin=hostpf,whole_inverse_pin=invpf,
    original_stages_path_expression='work / case / "stages.json"',
    original_runner_work_argument='OUT',original_runner_case_argument="'compact-'+KIND+'-controls'",
    new_directory_creation_expression="(OUT/('compact-'+KIND+'-controls')).mkdir()",
    exact_planned_stages_parent=str(expected_stage_parent),
    mkdir_before_original_OwnRSS_constructor_and_all_runner_execute=True,
    all_other_11_definitions_whole_bytes_unchanged=True,main_only_one_mkdir_statement_inserted=True,
    Host_AST_parsed_only=True,Host_imported=False,Host_main_executed=False,
    compiler_executed=False,numerical_executed=False,
    future_actual_control_report_pin=None,reader_qualified=False))
  ready=put(newfolder,'HOST_SOURCE_REVIEW_READY.json',dict(
    schema='COMPACT_BQ_CONTROL_HOST_SOURCE_REVIEW_READY_V1',kind=kind,source_only=True,
    compiler_executed=False,numerical_executed=False,Host_imported=False,
    host_source=hostpf,control_host_plan_pin=planpf,complete_host_plan_inverse_pin=invpf,
    original_SerialExecutor_record_directory_static_proof_pin=proof,
    selected_control_Source_freeze_pin=plan['selected_control_Source_freeze_pin'],
    selected_new_build_Host_freeze_pin=plan['selected_new_build_Host_freeze_pin'],
    selected_post_release_Common_Source_freeze_pin=plan['selected_post_release_Common_Source_freeze_pin'],
    predecessor_Host_source_freeze_pin=oldhfpf,predecessor_argv_Source_template_pin=oldclipf,
    actual_failed_model4_summary_pin=failpf,actual_failed_model4_true_tool_return_pin=failtoolpf,
    future_Host_freeze_pin=None,future_actual_control_report_pin=None,reader_qualified=False))
  produced.append(dict(kind=kind,host_source_pin=hostpf,control_host_plan_pin=planpf,whole_inverse_pin=invpf,
    caller_directory_static_proof_pin=proof,source_review_ready_pin=ready))
 print(json.dumps({'status':'TWO_V5_RECORD_DIRECTORY_SOURCE_ONLY_HOST_PLAN_CANDIDATES_PREPARED',
  'packages':produced,'actual_failed_model4_summary_pin':failpf,'old_v4_files_and_failed_OUTPUT_unmodified':True,
  'Host_imported':False,'compiler_executed':False,'numerical_executed':False,'deleted':False}))
if __name__=='__main__':main()
