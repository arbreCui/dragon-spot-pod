"""One Source-only publication of SF/HF/dynamic24; never prepare a request or launch evidence."""
import argparse,hashlib,json,os
from pathlib import Path
BASE=Path(__file__).absolute().parent
REC=BASE.parent
SF=BASE/'COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_FREEZE.json'
HF=BASE/'COMPLETE_CURRENT_MATERIAL_EVIDENCE_HOST_SOURCE_FREEZE.json'
DYN=BASE/'ROOT_REVIEWABLE_MATERIAL_EVIDENCE_DYNAMIC_INTERFACE_SOURCE_ONLY.json'
POSTDIR=REC/'independent_short_FIL_A10_closed_capture_continuation_v3_actual_completion_postverify_20261014'
def require(ok,msg):
 if type(ok)is not bool or not ok:raise RuntimeError(msg)
def pin(path):
 p=Path(path);s=p.lstat();ids=lambda z:[z.st_dev,z.st_ino,z.st_mode,z.st_nlink,z.st_size,z.st_mtime_ns,z.st_ctime_ns]
 require(s.st_size<=64*2**20,'only bounded Source and metadata EOF')
 with p.open('rb')as f:raw=f.read()
 require(ids(p.lstat())==ids(s),'metadata before/after7')
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=ids(s))
def read(p):
 require(pin(p['path'])==p,'exact Source metadata PF');return json.loads(Path(p['path']).read_bytes())
def same7(p):
 q=Path(p['path']);s=q.lstat()
 require(not q.is_symlink()and [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==p['identity'],'original complete dependency current7')
def contains(obj,p):
 return obj==p or isinstance(obj,dict)and any(contains(v,p)for v in obj.values())or isinstance(obj,list)and any(contains(v,p)for v in obj)
def tool0(t,p,post=False):
 require(t['observed_closed']is True and type(t['original_integer_exit_code'])is int and t['original_integer_exit_code']==0,'genuine actual closed0')
 for k in ['actual_review_return','actual_postverification_return']if post else['actual_review_return']:
  z=t[k];require(type(z['exit_code'])is int and z['exit_code']==0 and z.get('session_id')is None and json.loads(z['output'].strip().splitlines()[-1])['review_pin']==p,'genuine original integer0/stdout exact reviewPF')
def write(p,v):
 with p.open('xb')as f:f.write((json.dumps(v,indent=2,allow_nan=False)+'\n').encode());f.flush();os.fsync(f.fileno())
 return pin(p)
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in ['peer-review','peer-tools']:
  for suffix in ['summary','sha256','seven-id']:ap.add_argument('--'+role+'-'+suffix,required=True)
 a=ap.parse_args();actual={}
 for role in ['peer-review','peer-tools']:
  k=role.replace('-','_');p=pin(getattr(a,k+'_summary'));require(p['sha256']==getattr(a,k+'_sha256')and p['identity']==json.loads(getattr(a,k+'_seven_id')),'actual peer fullPF');actual[role]=p
 peer=read(actual['peer-review']);tool0(read(actual['peer-tools']),actual['peer-review'])
 require(peer['failure']is None and peer['source_only']is True and peer['status'].startswith('PASS')and all(peer[k]is False for k in ['business_executed','compiler_executed','numerical_executed','files_deleted']),'only strict same-round Source review')
 ready=read(pin(BASE/'SOURCE_REVIEW_READY.json'));plan=read(ready['plan_pin']);wp=pin(__file__)
 own=[ready[k]for k in ['host_source_pin','builder_source_pin','scientific_child_source_pin','split_binder_source_pin','aggregation_engine_source_pin','current_formal_plan_pin','current_producer_projection_pin','plan_pin','inverse_pin']]+[pin(BASE/'SOURCE_REVIEW_READY.json'),wp]
 require(all(contains(peer,p)for p in own),'same-round eleven exact Source PFs')
 oldsf=read(plan['predecessor_Source_freeze_pin']);oldhf=read(plan['predecessor_Host_freeze_pin']);olddyn=read(plan['predecessor_dynamic_pin'])
 source=plan['complete_source_file_pins_candidate'];require(len(source)==len(oldsf['complete_source_file_pins'])==13,'all actual original13 Source rows')
 for p in source:require(pin(p['path'])==p,'all exact copied Source/meta PF')
 require(next(p for p in source if Path(p['path']).name=='current_material_lineage_evidence.py')['sha256']=='e921ad84a4b1241827b24d1c3a7fc8e06710098e9fd34bde4e3bd5eec2d10d4d','whole scientific child unchanged')
 rp=pin(POSTDIR/'REVIEW.json');tp=pin(POSTDIR/'TRUE_TOOL_RETURNS.json');post=read(rp);tool0(read(tp),rp,True)
 require(post['schema']=='INDEPENDENT_SHORT_FIL_A10_CLOSED_CAPTURE_CONTINUATION_V3_ACTUAL_COMPLETION_POSTVERIFICATION_V1'and post['status']=='PASS_ACTUAL_SHORT_FIL_A10_CLOSED_CAPTURE_CONTINUATION_V3_COMPLETION_POSTVERIFICATION'and post['failure']is None and post['actual_Root_integer_exit_code']==0 and post['actual_original_Root_integer_exit_code']==1 and post['actual_material_stage_closed0']is True and post['actual_new_material_child_launch_count']==0 and post['actual_original_fullfresh2_reserve_admitted']is True and all(post[k]is False for k in ['business_executed','compiler_executed','numerical_executed','files_deleted']),'actual independent completion/read-only Source premise; original Root1 preserved')
 keys=['actual_report_pin','actual_Host_freeze_pin','actual_CLI_pin','actual_Root_true_tool_return_pin','actual_Root_argv_pin','actual_observation_manifest_pin','actual_closed_owned_library_copy_release_pin'];proof=[post[k]for k in keys];phase=read(post['actual_report_pin'])
 table={}
 for p in oldhf['dependencies']+source+own+list(actual.values())+[ready['Source_author_pin'],plan['predecessor_Source_freeze_pin'],plan['predecessor_Host_freeze_pin'],plan['predecessor_dynamic_pin'],rp,tp]+proof+phase['fixed_current_pins']+phase['output_pins']+plan['projection_current_live_pins']+plan['projection_metadata_authority_pins']+[plan['retained_actual_prior_aggregation_report_pin'],plan['retained_actual_prior_aggregation_request_pin'],plan['retained_actual_prior_aggregation_child_report_pin']]+read(plan['retained_actual_prior_aggregation_report_pin'])['fixed_current_pins']+read(plan['retained_actual_prior_aggregation_report_pin'])['complete_output_pins']:
  require(p['path']not in table or table[p['path']]==p,'one current canonical pin per path');table[p['path']]=p
 deps=list(table.values())
 for p in deps:same7(p)
 require(not any(p.exists()for p in [SF,HF,DYN]),'one metadata publication only')
 provenance=dict(predecessor_Source_freeze_pin=plan['predecessor_Source_freeze_pin'],predecessor_Host_freeze_pin=plan['predecessor_Host_freeze_pin'],same_round_independent_Source_review_pin=actual['peer-review'],same_round_independent_Source_tools_pin=actual['peer-tools'],once_writer_Source_pin=wp,complete_byte_inverse_pin=ready['inverse_pin'],control_plan_pin=ready['plan_pin'],actual_closed_A10_completion_post_pin=rp,actual_closed_A10_completion_post_tools_pin=tp,actual_closed_A10_completion_authority_pins={k:post[k]for k in keys},retained_original_capture_and_completion_metadata_roots_counted=True,joint_scan_base_validation_same_volume=True,all_scientific_child_math_Fortran_and_resource_caps_unchanged=True,scientific_body_EOF_not_repeated_by_writer=True,empty_typed_MACROLIB_root_and_all19619_descendants_retained=True,only_DiskEvidence_inventory_and_request_cumulative_resource_metadata_changed=True,retained_actual_prior_aggregation_report_pin=plan['retained_actual_prior_aggregation_report_pin'],retained_actual_prior_aggregation_request_pin=plan['retained_actual_prior_aggregation_request_pin'],retained_prior_joint_archive_roots=plan['retained_prior_joint_archive_roots'],prior_aggregation_mathematical_qualification_claimed=False,physics_qualified=False)
 newsf=dict(oldsf);newsf.update(provenance,complete_source_file_pins=source,current_producer_consumption_projection_pin=ready['current_producer_projection_pin'],current_formal_producer_plan_pin=ready['current_formal_plan_pin'],retained_current_corrected_aggregation_request_pin=plan['retained_current_corrected_aggregation_request_pin'],retained_current_corrected_aggregation_report_pin=plan['retained_current_corrected_aggregation_report_pin'],retained_corrected_aggregation_joint_archive_roots=plan['retained_corrected_aggregation_joint_archive_roots'],candidate_executed=False,compiler_executed=False,material_job_executed=False)
 sp=write(SF,newsf)
 newhf=dict(oldhf);newhf.update(provenance,host_source=ready['host_source_pin'],dependencies=deps+[sp],candidate_executed=False)
 hp=write(HF,newhf)
 prefix=olddyn['known_argv_prefix'][:11]+[ready['host_source_pin']['path']]
 for role,p in [('source-freeze',sp),('host-freeze',hp)]:prefix+=['--'+role+'-summary',p['path'],'--'+role+'-sha256',p['sha256'],'--'+role+'-seven-id',json.dumps(p['identity'],separators=(',',':'))]
 require(len(prefix)==24,'unchanged dynamic24 interface; actual request triple still required')
 d=dict(olddyn);d.update(host_source_pin=ready['host_source_pin'],selected_source_freeze_pin=sp,selected_host_freeze_pin=hp,known_argv_prefix=prefix,request_builder_source_pin=ready['builder_source_pin'],actual_request_pin=None,is_complete_executable_argv=False,required_actual_prefix='request',original_five_role_roots_plus_exact_completion_metadata_sixth_root=True,joint_scan_validation_base_preserves_ART_and_REC=True,compiler_or_material_executed=False,physics_qualified=False)
 dp=write(DYN,d)
 for p in deps:same7(p)
 fd=os.open(BASE,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='COMPARE_THREE_EXACT_CURRENT_PROJECTION_SF_HF_DYNAMIC24_SOURCE_ONLY_PUBLISHED',Source_freeze_pin=sp,Host_freeze_pin=hp,dynamic_interface_pin=dp,actual_dynamic_prefix_count=24,actual_complete_Source_count=13,actual_dependency_count=len(deps)+1,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()
