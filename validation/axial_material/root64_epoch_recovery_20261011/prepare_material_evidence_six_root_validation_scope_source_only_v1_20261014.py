"""Prepare Source only: retain capture and completion roots, preserve scientific child bytes."""
import ast,hashlib,json,os
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=R/'current_formal_material_authority_exact_cache70_post_literal3_latest_full50_source_v9_20261014'
OUT=R/'current_material_evidence_six_root_validation_scope_source_v1_20261014'
OLD_BINDER=R/'bind_material_extract_request_preparation_after_closed_short_FIL_A10_continuation_source_only_v5_20261014.py'
RELATION=r'''    observedroot=Path(state['actual_cwd']).parent;completionroot=Path(mpin['path']).parent
    priorpin=actual['original_failed_phase_pin'];prior=read(priorpin,lambda:None)
    require(actual['completion_only_existing_closed_stage']is True and
      actual['Dragon_or_compiler_or_material_child_launched_by_continuation']is False and
      actual['original_capture_collector_not_reexecuted']is True and
      actual['actual_prior_material_stage_record_reused_wholebytes']is True and
      actual['original_Root_exit_code_retained']==1 and
      prior['status']=='FAILED_CURRENT_OBSERVATION_NO_RETRY'and
      prior['failure']=='RuntimeError: both real process metadata tools fully pinned'and
      actual['original_Root_failure_retained']==prior['failure']and
      actual['records']==prior['records']and
      observedroot==Path(priorpin['path']).parent and
      state['actual_cwd']==str(observedroot/'A')and
      actual['actual_prior_A_cwd']==state['actual_cwd']and
      actual['original_release_owner_output_root']==str(observedroot)and
      Path(state['actual_owning_report_pin']['path']).parent==completionroot and
      m['completion_only_original_Root1_preserved']is True and
      m['original_failed_phase_pin']==priorpin and
      m['original_Root_true_tool_pin']==actual['original_Root_true_tool_pin']and
      observedroot!=completionroot and
      not observedroot.is_relative_to(completionroot)and
      not completionroot.is_relative_to(observedroot),
      'only exact completion report and retained original captured physical owner')
'''
def pin(p):
 p=Path(p);s=p.stat();return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),size_bytes=s.st_size,identity=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns])
def write(p,v):
 raw=v.encode()if isinstance(v,str)else(json.dumps(v,indent=2,allow_nan=False)+'\n').encode()
 with p.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 return pin(p)
def main():
 if OUT.exists():raise RuntimeError('unique Source bundle')
 dyn=json.loads((OLD/'ROOT_REVIEWABLE_MATERIAL_EVIDENCE_DYNAMIC_INTERFACE_SOURCE_ONLY.json').read_bytes());sf=json.loads(Path(dyn['selected_source_freeze_pin']['path']).read_bytes());hf=json.loads(Path(dyn['selected_host_freeze_pin']['path']).read_bytes())
 locals=[p for p in sf['complete_source_file_pins']if Path(p['path']).parent==OLD];external=[p for p in sf['complete_source_file_pins']if Path(p['path']).parent!=OLD]
 if len(sf['complete_source_file_pins'])!=13 or len(locals)!=10 or len(external)!=3:raise RuntimeError('actual current complete13 Source table')
 prepared=[];entries=[];OUT.mkdir()
 for p in locals:
  name=Path(p['path']).name;a=Path(p['path']).read_text();z=a;changes=[]
  def change(before,after):
   nonlocal z
   if z.count(before)!=1:raise RuntimeError('one exact Source splice '+name)
   z=z.replace(before,after,1);changes.append(dict(before=before,after=after))
  if name=='prepare_current_material_evidence_requests.py':
   anchor="    root=Path(args.request_output_dir);require(root.is_absolute()and not os.path.lexists(root),'fresh metadata request namespace')"
   change(anchor,RELATION+anchor)
   before="    request=base_request(args.operation,sfpin,m['current_case_spec_pin'],out,Path(mpin['path']).parent,root,fixed)"
   after="    request=base_request(args.operation,sfpin,m['current_case_spec_pin'],out,observedroot,root,fixed)\n    request['original_five_role_roots']=list(request['joint_archive_roots'])\n    request['joint_archive_roots'].append(str(completionroot))\n    require(len(request['joint_archive_roots'])==6 and len(set(request['joint_archive_roots']))==6 and\n      not any(Path(a).is_relative_to(Path(b))for a in request['joint_archive_roots']for b in request['joint_archive_roots']if a!=b),\n      'five original roles plus exact retained completion metadata sixth root; same2GiB')\n    request['exact_retained_original_observed_root']=str(observedroot)\n    request['exact_retained_completion_metadata_root']=str(completionroot)\n    request['completion_original_failed_phase_pin']=priorpin"
   change(before,after)
  elif name=='run_current_material_lineage_evidence.py':change('joined=original_parent.DiskResources(c.ART,roots,8*2**30,2*2**30)',"joined=original_parent.DiskResources(ROOT/'validation',roots,8*2**30,2*2**30)")
  ast.parse(z);cp=write(OUT/name,z);prepared.append(cp);back=z
  for c in reversed(changes):
   if back.count(c['after'])!=1:raise RuntimeError('exact Source inverse')
   back=back.replace(c['after'],c['before'],1)
  if back.encode()!=Path(p['path']).read_bytes():raise RuntimeError('whole predecessor bytes')
  entries.append(dict(predecessor_pin=p,candidate_pin=cp,changes=changes,whole_file_inverse_byte_equal=True,whole_bytes_unchanged=not changes))
 builder=next(p for p in prepared if Path(p['path']).name=='prepare_current_material_evidence_requests.py');host=next(p for p in prepared if Path(p['path']).name=='run_current_material_lineage_evidence.py');child=next(p for p in prepared if Path(p['path']).name=='current_material_lineage_evidence.py')
 binder=OLD_BINDER.read_text();bz=binder;changes=[]
 def bc(a,z):
  nonlocal bz
  if bz.count(a)!=1:raise RuntimeError('one binder Source splice '+a)
  bz=bz.replace(a,z,1);changes.append(dict(before=a,after=z))
 for name,value in [('M','REC/'+repr(OUT.name)),('DYNAMIC_SHA',repr('REQUIRED_ACTUAL_PUBLISHED_DYNAMIC_FULLPIN')),('REQUEST_BUILDER_SHA',repr(builder['sha256']))]:
  node=next(n for n in ast.parse(bz).body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)and n.targets[0].id==name);bc(ast.get_source_segment(bz,node),name+'='+value)
 bc("ap.add_argument('--request-output-dir',required=True);ap.add_argument('--future-host-output-dir',required=True)","ap.add_argument('--request-output-dir',required=True);ap.add_argument('--future-host-output-dir',required=True)\n for suffix in('summary','sha256','seven-id'):ap.add_argument('--evidence-dynamic-'+suffix,required=True)")
 bc("if firstpin['sha256']!=FIRST_CLI_SHA or dynamicpin['sha256']!=DYNAMIC_SHA or builderpin['sha256']!=REQUEST_BUILDER_SHA:","if firstpin['sha256']!=FIRST_CLI_SHA or dynamicpin['path']!=a.evidence_dynamic_summary or dynamicpin['sha256']!=a.evidence_dynamic_sha256 or dynamicpin['identity']!=json.loads(a.evidence_dynamic_seven_id)or builderpin['sha256']!=REQUEST_BUILDER_SHA:")
 bc("roots=[str(future),str(child),str(out),str(Path(dynamic['selected_source_freeze_pin']['path']).parent),str(req)]","roots=[str(future),str(child),str(owner),str(Path(dynamic['selected_source_freeze_pin']['path']).parent),str(req),str(out)]")
 bc("if len(set(roots))!=5 or any(Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y):raise RuntimeError('original five disjoint complete roots')","if len(set(roots))!=6 or any(Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y):raise RuntimeError('original five disjoint roles plus retained completion metadata sixth root')")
 anchor="if sf['schema']!='COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_ONLY_FREEZE_V1'or sf['candidate_executed']is not False or hf['host_source']!=dynamic['host_source_pin']:"
 replacement="if sf['schema']!='COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_ONLY_FREEZE_V1'or sf['candidate_executed']is not False or hf['host_source']!=dynamic['host_source_pin']or dynamic['selected_source_freeze_pin']['path']!=str(M/'COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_FREEZE.json')or dynamic['selected_host_freeze_pin']['path']!=str(M/'COMPLETE_CURRENT_MATERIAL_EVIDENCE_HOST_SOURCE_FREEZE.json')or dynamic['host_source_pin']!=EXPECTED_NEW_EVIDENCE_HOST_SOURCE_PIN:"
 bc(anchor,replacement);bc("DYNAMIC_SHA='REQUIRED_ACTUAL_PUBLISHED_DYNAMIC_FULLPIN'","DYNAMIC_SHA='REQUIRED_ACTUAL_PUBLISHED_DYNAMIC_FULLPIN'\nEXPECTED_NEW_EVIDENCE_HOST_SOURCE_PIN="+repr(host))
 bc('AFTER_CLOSED_SHORT_FIL_A10_CONTINUATION_ARGV_20261014.json','AFTER_CLOSED_SHORT_FIL_A10_SIX_ROOT_EVIDENCE_ARGV_20261014.json');bc('AFTER_CLOSED_SHORT_FIL_A10_CONTINUATION_ARGV_V1','AFTER_CLOSED_SHORT_FIL_A10_SIX_ROOT_EVIDENCE_ARGV_V1')
 bc('original_joint_five_roots=roots','original_joint_five_roots=roots[:5],complete_joint_six_roots=roots,exact_retained_completion_metadata_root=str(out),exact_retained_original_observed_root=str(owner)')
 ast.parse(bz);bp=write(OUT/'bind_actual_completion_to_six_root_extract21_metadata_only.py',bz);back=bz
 for c in reversed(changes):
  if back.count(c['after'])!=1:raise RuntimeError('exact binder inverse')
  back=back.replace(c['after'],c['before'],1)
 if back.encode()!=OLD_BINDER.read_bytes():raise RuntimeError('whole actual binder v5 inverse')
 entries.append(dict(predecessor_pin=pin(OLD_BINDER),candidate_pin=bp,changes=changes,whole_file_inverse_byte_equal=True))
 iv=write(OUT/'COMPLETE_SIX_ROOT_EVIDENCE_SOURCE_BYTE_INVERSE.json',dict(schema='COMPLETE_SIX_ROOT_EVIDENCE_SOURCE_BYTE_INVERSE_V1',entries=entries,scientific_child_and_other_eight_local_Source_files_wholebytes_unchanged=True,all_original_Fortran_math_and_guards_and_caps_unchanged=True,Source_only=True))
 plan=write(OUT/'SIX_ROOT_SOURCE_PLAN.json',dict(schema='SIX_ROOT_VALIDATION_SCOPE_EVIDENCE_SOURCE_ONLY_PLAN_V1',predecessor_dynamic_pin=pin(OLD/'ROOT_REVIEWABLE_MATERIAL_EVIDENCE_DYNAMIC_INTERFACE_SOURCE_ONLY.json'),predecessor_Source_freeze_pin=dyn['selected_source_freeze_pin'],predecessor_Host_freeze_pin=dyn['selected_host_freeze_pin'],complete_source_file_pins_candidate=prepared+external,actual_original_complete_Source_count=13,actual_local_Source_count=10,external_original_Source_pins=external,host_source_pin=host,builder_source_pin=builder,scientific_child_source_pin=child,split_binder_source_pin=bp,inverse_pin=iv,observed_root_from_actual_A_cwd_parent=True,only_exact_completion_relationship_adds_retained_sixth_root=True,joined_genuine_DiskResources_scan_base='/Users/wen/spot/validation',original_history_initialize_ART_unchanged=True,original_caps_512_600_1800_8GiB_2GiB_96GiB_and_cold_unchanged=True,future_actual_new_Source_freeze_pin=None,future_actual_new_Host_freeze_pin=None,future_actual_new_dynamic_pin=None,future_actual_extract_request_pin=None,future_actual_extract_report_pin=None,Source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
 ready=write(OUT/'SOURCE_REVIEW_READY.json',dict(schema='SIX_ROOT_EVIDENCE_RESOURCE_INTERFACE_SOURCE_ONLY_READY_V1',host_source_pin=host,builder_source_pin=builder,scientific_child_source_pin=child,split_binder_source_pin=bp,plan_pin=plan,inverse_pin=iv,Source_author_pin=pin(__file__),future_actual_new_Source_freeze_pin=None,future_actual_new_Host_freeze_pin=None,future_actual_new_dynamic_pin=None,Source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
 print(json.dumps(dict(status='SIX_ROOT_EVIDENCE_RESOURCE_WIRING_SOURCE_ONLY_CANDIDATE_READY',host_source_pin=host,builder_source_pin=builder,scientific_child_source_pin=child,split_binder_source_pin=bp,plan_pin=plan,inverse_pin=iv,ready_pin=ready,Source_author_pin=pin(__file__),actual_cloned_complete_Source_count=13,writer_or_host_or_builder_main_executed=False,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()
